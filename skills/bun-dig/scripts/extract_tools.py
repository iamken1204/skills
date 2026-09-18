#!/usr/bin/env python3
"""Pull tool specs (name, description, inputSchema, fn body) out of a minified agent bundle.

Works on the pattern most TS agents compile down to:

    {spec:{name:CONST,description:...,inputSchema:...,source:"builtin"},fn:IMPL}
    {name:CONST,description:...,inputSchema:...}

where CONST is a minified identifier bound to a string literal (`,zme="skill"`).
Minified names change every build, so everything here keys off structure and
string literals, never off identifiers you saw last time.

Resolution handled:
  - description as literal, template literal, tagged template, or a const reference
  - `${IDENT}` inside templates -> string/number const (nearest definition before the site)
  - `${FN(IDENT)}` where IDENT is an array of {description, args} -> rendered "# Examples"
  - inputSchema as an object literal, or `FN(ZOD_IDENT)` -> the zod literal (best effort)
  - `fn:IDENT` -> first-level implementation body

Usage:
  extract_tools.py BUNDLE.js [-o OUTDIR]         write tools.json, tools.md, impls.js
  extract_tools.py --diff OLD/tools.json NEW/tools.json   show what changed between versions
"""
import argparse
import difflib
import json
import os
import re
import sys

# ---------------------------------------------------------------- scanner ----

src = ""
N = 0


def scan_string(i):
    q = src[i]
    j = i + 1
    while j < N:
        c = src[j]
        if c == "\\":
            j += 2
            continue
        if c == q:
            return j + 1, src[i + 1 : j]
        j += 1
    raise ValueError(f"unterminated string at {i}")


def scan_template(i):
    j = i + 1
    while j < N:
        c = src[j]
        if c == "\\":
            j += 2
            continue
        if c == "$" and src[j + 1] == "{":
            j = scan_balanced(j + 1, "{", "}")
            continue
        if c == "`":
            return j + 1, src[i + 1 : j]
        j += 1
    raise ValueError(f"unterminated template at {i}")


def scan_balanced(i, open_c, close_c):
    depth = 0
    j = i
    while j < N:
        c = src[j]
        if c in "\"'":
            j, _ = scan_string(j)
            continue
        if c == "`":
            j, _ = scan_template(j)
            continue
        if c == open_c:
            depth += 1
        elif c == close_c:
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    raise ValueError(f"unbalanced at {i}")


def stmt_end(i):
    """End of an expression starting at i: first top-level , ; or closing bracket."""
    depth = 0
    j = i
    q = None
    while j < N:
        c = src[j]
        if q:
            if c == "\\":
                j += 2
                continue
            if c == q:
                q = None
        elif c in "\"'`":
            q = c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            if depth == 0:
                return j
            depth -= 1
        elif c in ",;" and depth == 0:
            return j
        j += 1
    return N


def unescape_js(s):
    def rep(m):
        e = m.group(1)
        table = {"n": "\n", "t": "\t", "r": "\r", "`": "`", "$": "$", "\\": "\\", '"': '"', "'": "'"}
        if e in table:
            return table[e]
        if e[0] == "u" and len(e) == 5:
            return chr(int(e[1:], 16))
        if e[0] == "x" and len(e) == 3:
            return chr(int(e[1:], 16))
        return e

    return re.sub(r"\\(u[0-9a-fA-F]{4}|x[0-9a-fA-F]{2}|.)", rep, s)


IDENT = r"[A-Za-z_$][\w$]*"


def ident_re(name):
    return r"(?<![\w$.])" + re.escape(name)


# ------------------------------------------------------- const resolution ----


def nearest_before(pattern, pos, window=2_000_000):
    """Last match of pattern that starts before pos (minified bundles define before use)."""
    lo = max(0, pos - window)
    last = None
    for m in re.finditer(pattern, src[lo:pos]):
        last = m
    if last is None:
        return None
    return lo + last.start(), last


def resolve_string_const(name, pos, depth=0):
    if depth > 4:
        return None
    hit = nearest_before(ident_re(name) + r"=([\"'`])", pos) or (None, None)
    if hit[0] is None:
        m = re.search(ident_re(name) + r"=([\"'`])", src)
        if not m:
            return None
        start = m.start()
    else:
        start = hit[0]
    q_at = start + len(name) + 1
    if src[q_at] == "`":
        _, raw = scan_template(q_at)
        return resolve_template(raw, q_at, depth + 1)
    _, raw = scan_string(q_at)
    return unescape_js(raw)


def resolve_number_const(name, pos):
    hit = nearest_before(ident_re(name) + r"=(\d+(?:\.\d+)?)(?=[,;)])", pos)
    if hit:
        return hit[1].group(1)
    m = re.search(ident_re(name) + r"=(\d+(?:\.\d+)?)(?=[,;)])", src)
    return m.group(1) if m else None


def find_array_literal(name, pos):
    hit = nearest_before(ident_re(name) + r"=\[", pos)
    if hit:
        return hit[0] + len(name) + 1
    m = re.search(ident_re(name) + r"=\[", src)
    return m.end() - 1 if m else None


def js_object_to_json(s):
    """Best-effort: quote keys, !0/!1 -> booleans, template literals -> JSON strings."""
    s = re.sub(r"`((?:[^`\\]|\\.)*)`", lambda m: json.dumps(unescape_js(m.group(1))), s)
    s = re.sub(r"([{,])(" + IDENT + r"):", r'\1"\2":', s)
    return s.replace("!0", "true").replace("!1", "false")


def render_examples(array_ident, pos):
    """[{description, args}, ...] -> the '# Examples' block agents commonly embed."""
    at = find_array_literal(array_ident, pos)
    if at is None:
        return None
    end = scan_balanced(at, "[", "]")
    arr = src[at:end]
    out = ["# Examples", ""]
    j = 0
    while True:
        dm = re.search(r"\{description:", arr[j:])
        if not dm:
            break
        di = j + dm.end()
        c = arr[di]
        if c in "\"'":
            k = di + 1
            while arr[k] != c:
                k += 2 if arr[k] == "\\" else 1
            desc = unescape_js(arr[di + 1 : k])
            k += 1
        else:
            k = arr.index("`", di)
            kk = k + 1
            while arr[kk] != "`":
                kk += 2 if arr[kk] == "\\" else 1
            desc = unescape_js(arr[k + 1 : kk])
            k = kk + 1
        am = re.match(r",args:", arr[k:])
        if not am:
            break
        ai = k + am.end()
        depth = 0
        q = None
        x = ai
        while True:
            ch = arr[x]
            if q:
                if ch == "\\":
                    x += 2
                    continue
                if ch == q:
                    q = None
            elif ch in "\"'`":
                q = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
            x += 1
        out += [desc, "```json", js_object_to_json(arr[ai : x + 1]), "```", ""]
        j = x + 1
    return "\n".join(out).rstrip()


def resolve_template(raw, pos, depth=0):
    out = []
    j = 0
    while j < len(raw):
        if raw[j] == "\\":
            out.append(raw[j : j + 2])
            j += 2
            continue
        if raw.startswith("${", j):
            k = j + 2
            d = 1
            while k < len(raw) and d:
                d += (raw[k] == "{") - (raw[k] == "}")
                k += 1
            expr = raw[j + 2 : k - 1].strip()
            val = None
            if re.fullmatch(IDENT, expr):
                val = resolve_string_const(expr, pos, depth + 1) or resolve_number_const(expr, pos)
            else:
                call = re.fullmatch(r"(" + IDENT + r")\((" + IDENT + r")\)", expr)
                if call:
                    val = render_examples(call.group(2), pos)
            out.append(val if val is not None else "${" + expr + "}")
            j = k
            continue
        out.append(raw[j])
        j += 1
    return unescape_js("".join(out))


def zod_literal(name, pos):
    hit = nearest_before(ident_re(name) + r"=(" + IDENT + r")\(\{", pos)
    if not hit:
        return None
    start = hit[0]
    paren = src.index("(", start)
    end = scan_balanced(paren, "(", ")")
    body = src[paren + 1 : end - 1]
    return "/* zod object; z.string()/z.boolean() factories are minified */ " + body


def def_body(name, pos):
    """Implementation bound to a minified identifier: function decl, arrow, or class."""
    for pat, kind in ((r"(?:async )?function " + re.escape(name) + r"\(", "fn"), (ident_re(name) + r"=(?!=)", "assign"), (r"class " + re.escape(name) + r"\b", "class")):
        hit = nearest_before(r"(?<![\w$.])" + pat if not pat.startswith("(?<!") else pat, pos)
        m = re.search(r"(?<![\w$.])" + pat if not pat.startswith("(?<!") else pat, src) if not hit else None
        start = hit[0] if hit else (m.start() if m else None)
        if start is None:
            continue
        if kind in ("fn", "class"):
            return src[start : scan_balanced(src.index("{", start), "{", "}")]
        eq = src.index("=", start)
        return src[start : stmt_end(eq + 1)]
    return None


# ------------------------------------------------------------- extraction ----


def read_description(at):
    c = src[at]
    if c in "\"'":
        _, raw = scan_string(at)
        return unescape_js(raw), "literal"
    if c == "`":
        _, raw = scan_template(at)
        return resolve_template(raw, at), "template"
    m = re.match(IDENT, src[at:])
    if not m:
        return None, "unknown"
    name = m.group(0)
    after = at + len(name)
    if src[after] == "`":
        _, raw = scan_template(after)
        return resolve_template(raw, after), f"tagged:{name}"
    return resolve_string_const(name, at), f"const:{name}"


def read_schema(obj_start, obj):
    sm = re.search(r"(?<![\w$])inputSchema:", obj)
    if not sm:
        return None
    si = obj_start + sm.end()
    if src[si] == "{":
        literal = src[si : scan_balanced(si, "{", "}")]
        # `${MAX}` inside property descriptions: substitute the const so diffs stay clean across builds
        return re.sub(r"\$\{(" + IDENT + r")\}", lambda m: resolve_string_const(m.group(1), si) or resolve_number_const(m.group(1), si) or m.group(0), literal)
    expr = src[si : stmt_end(si)]
    call = re.fullmatch(r"(" + IDENT + r")\((" + IDENT + r")\)", expr)
    if call:
        return zod_literal(call.group(2), si) or expr
    if re.fullmatch(IDENT, expr):
        return zod_literal(expr, si) or expr
    return expr


def extract():
    tools = []
    seen_sites = set()
    site_re = re.compile(r"\{name:(" + IDENT + r"|\"[A-Za-z_][\w]*\"),(?=(?:title:[^,]*,)?description:)")
    for m in site_re.finditer(src):
        start = m.start()
        if start in seen_sites:
            continue
        seen_sites.add(start)
        end = scan_balanced(start, "{", "}")
        obj = src[start:end]
        ref = m.group(1)
        name = ref.strip('"') if ref.startswith('"') else resolve_string_const(ref, start)
        if not name or not re.fullmatch(r"[A-Za-z][\w-]*", name):
            continue
        dm = re.match(r"\{name:[^,]+,(?:title:[^,]*,)?description:", obj)
        desc, kind = read_description(start + dm.end())
        schema = read_schema(start, obj)
        # CLI subcommand tables, MCP prompts and plain records also look like {name,description};
        # a tool spec always carries an object (or zod) inputSchema
        if not schema or schema[0] in "\"'":
            continue
        extra = {}
        for key in ("source", "meta", "executionProfile"):
            km = re.search(r"(?<![\w$])" + key + r":", obj)
            if km:
                ki = start + km.end()
                extra[key] = src[ki : scan_balanced(ki, "{", "}")] if src[ki] == "{" else src[ki : stmt_end(ki)]
        inside_spec = src[max(0, start - 5) : start] == "spec:"
        # {spec:{...},fn:X} wrapper, or {name:...} object referenced later as spec:IDENT,fn:...
        fn = None
        fm = re.match(r",fn:", src[end : end + 10])
        if fm:
            fi = end + 4
            fn = src[fi : stmt_end(fi)]
            if re.fullmatch(IDENT, fn):
                fn = def_body(fn, fi) or fn
        else:
            back = src.rfind("=", max(0, start - 20), start)
            if back > 0:
                holder = re.search(r"(" + IDENT + r")=$", src[back - 40 : back + 1])
                if holder:
                    w = re.search(r"\{spec:" + re.escape(holder.group(1)) + r",fn:", src[end : end + 5000])
                    if w:
                        fi = end + w.end()
                        fn = src[fi : stmt_end(fi)]
                        if re.fullmatch(IDENT, fn):
                            fn = def_body(fn, fi) or fn
        if not (inside_spec or fn or "source" in extra):
            continue
        tools.append(dict(name=name, pos=start, desc_kind=kind, description=desc, inputSchema=schema, fn=fn, **extra))
    tools.sort(key=lambda t: t["name"])
    return tools


def write_outputs(tools, out_dir, source_path):
    os.makedirs(out_dir, exist_ok=True)
    json.dump(tools, open(os.path.join(out_dir, "tools.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(out_dir, "tools.md"), "w") as f:
        f.write(f"# Tools extracted from `{os.path.basename(source_path)}`\n\n{len(tools)} tool objects.\n")
        for t in tools:
            f.write(f"\n---\n\n## `{t['name']}`\n\n- pos: {t['pos']} · description via {t['desc_kind']}\n")
            for k in ("source", "meta", "executionProfile"):
                if t.get(k):
                    f.write(f"- {k}: `{t[k][:200]}`\n")
            f.write("\n### description\n\n```\n" + (t["description"] or "<unresolved>") + "\n```\n")
            f.write("\n### inputSchema\n\n```js\n" + (t["inputSchema"] or "<none>") + "\n```\n")
    with open(os.path.join(out_dir, "impls.js"), "w") as f:
        for t in tools:
            f.write(f"\n// ===== {t['name']} =====\n{t['fn'] or '// (no fn found)'}\n")


def mask_minified(s):
    """Zod schemas keep minified factory names (z() one build, j() the next); mask them before comparing."""
    s = re.sub(r"/\* zod[^*]*\*/", "/* zod */", s)
    s = re.sub(r"(?<![\w$.])[A-Za-z_$][\w$]{0,3}(?=\()", "ƒ", s)
    return re.sub(r"\.overwrite\([\w$]+\)", ".overwrite(ƒ)", s)


def diff_versions(old_path, new_path):
    old = {t["name"]: t for t in json.load(open(old_path))}
    new = {t["name"]: t for t in json.load(open(new_path))}
    for name in sorted(set(new) - set(old)):
        print(f"+ added   {name}")
    for name in sorted(set(old) - set(new)):
        print(f"- removed {name}")
    for name in sorted(set(old) & set(new)):
        for field in ("description", "inputSchema"):
            a, b = old[name].get(field) or "", new[name].get(field) or ""
            if field == "inputSchema":
                a, b = mask_minified(a), mask_minified(b)
            if a != b:
                print(f"~ {name}.{field}")
                for line in difflib.unified_diff(a.splitlines(), b.splitlines(), "old", "new", lineterm="", n=1):
                    print("    " + line)


def main():
    global src, N
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("bundle", nargs="?")
    ap.add_argument("-o", "--out", default="tools-extracted")
    ap.add_argument("--diff", nargs=2, metavar=("OLD_JSON", "NEW_JSON"))
    args = ap.parse_args()
    if args.diff:
        diff_versions(*args.diff)
        return
    if not args.bundle:
        ap.error("bundle path required (or --diff)")
    src = open(args.bundle, encoding="utf-8").read()
    N = len(src)
    tools = extract()
    write_outputs(tools, args.out, args.bundle)
    unresolved = [t["name"] for t in tools if not t["description"] or "${" in (t["description"] or "")]
    print(f"{len(tools)} tools -> {args.out}/tools.json, tools.md, impls.js")
    print("names:", ", ".join(t["name"] for t in tools))
    if unresolved:
        print("descriptions with unresolved parts:", ", ".join(unresolved), file=sys.stderr)


if __name__ == "__main__":
    main()
