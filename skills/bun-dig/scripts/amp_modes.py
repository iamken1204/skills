#!/usr/bin/env python3
"""Recover Amp's agent-mode table (model, system-prompt key, includeTools, deferredTools).

The bundle contains more than one copy of the mode table; the one that matters is
the copy the tool-gating function reads, which is also the largest. This script
takes the largest table and expands every `[...spread]` list so each mode's tool
lists are literal names.

Usage: amp_modes.py BUNDLE.js [-o OUTDIR]   ->  modes.json, modes.md
"""
import argparse
import json
import os
import re

IDENT = r"[A-Za-z_$][\w$]*"


def balanced(src, i, o, c):
    d = 0
    j = i
    q = None
    while j < len(src):
        ch = src[j]
        if q:
            if ch == "\\":
                j += 2
                continue
            if ch == q:
                q = None
        elif ch in "\"'`":
            q = ch
        elif ch == o:
            d += 1
        elif ch == c:
            d -= 1
            if d == 0:
                return j + 1
        j += 1
    return len(src)


def find_tables(src):
    """Group consecutive {key:"...",displayName:"..."} objects into tables."""
    modes = []
    for m in re.finditer(r"\{key:(\"[^\"]+\"|" + IDENT + r"),displayName:", src):
        end = balanced(src, m.start(), "{", "}")
        body = src[m.start() : end]
        model = re.search(r"model:" + IDENT + r"\(\"([^\"]+)\"\)", body)
        models = re.findall(r"model:" + IDENT + r"\(\"([^\"]+)\"\)", body)
        sp = re.search(r"systemPrompt:\"([^\"]+)\"", body)
        inc = re.search(r"includeTools:(" + IDENT + r")", body)
        dfr = re.search(r"deferredTools:(" + IDENT + r")", body)
        key = m.group(1).strip('"')
        if not m.group(1).startswith('"'):
            # key held in a const, e.g. LXe="nostromo": take the nearest definition before this table
            defs = list(re.finditer(r"(?<![\w$.])" + re.escape(key) + r"=\"([^\"]+)\"", src[max(0, m.start() - 300_000) : m.start()]))
            if defs:
                key = defs[-1].group(1)
        modes.append(dict(pos=m.start(), key=key, model=model.group(1) if model else "/".join(models) or None,
                          systemPrompt=sp.group(1) if sp else None, includeTools=inc.group(1) if inc else None,
                          deferredTools=dfr.group(1) if dfr else None, serverOnly="serverOnly:!0" in body))
    tables = []
    for mode in modes:
        if tables and mode["pos"] - tables[-1][-1]["pos"] < 8000:
            tables[-1].append(mode)
        else:
            tables.append([mode])
    return tables


def expand_lists(src, table_start):
    cache = {}

    def resolve(name):
        if name in cache:
            return cache[name]
        lo = max(0, table_start - 300_000)
        last = None
        for mm in re.finditer(r"(?<![\w$.])" + re.escape(name) + r"=(\[|new Set\(\[|Array\.from\(new Set\(\[)", src[lo:table_start]):
            last = mm
        if not last:
            cache[name] = None
            return None
        s = lo + last.end() - 1
        e = balanced(src, s, "[", "]")
        items = []
        for lit, spread in re.findall(r"\"([^\"]+)\"|\.\.\.(" + IDENT + r")", src[s + 1 : e - 1]):
            if lit:
                items.append(lit)
            else:
                sub = resolve(spread)
                items.extend(sub if sub else [f"<{spread}?>"])
        seen = set()
        cache[name] = [x for x in items if not (x in seen or seen.add(x))]
        return cache[name]

    return resolve


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("bundle")
    ap.add_argument("-o", "--out", default="tools-extracted")
    args = ap.parse_args()
    src = open(args.bundle, encoding="utf-8").read()

    tables = find_tables(src)
    if not tables:
        raise SystemExit("no mode table found ({key:..., displayName:...} objects)")
    table = max(tables, key=len)
    resolve = expand_lists(src, table[0]["pos"])

    result = {}
    for mode in table:
        inc = resolve(mode["includeTools"]) if mode["includeTools"] else None
        dfr = resolve(mode["deferredTools"]) if mode["deferredTools"] else []
        result[mode["key"]] = dict(model=mode["model"], systemPrompt=mode["systemPrompt"], serverOnly=mode["serverOnly"],
                                   includeTools=inc, deferredTools=dfr,
                                   sentUpFront=[t for t in (inc or []) if t not in set(dfr)])

    os.makedirs(args.out, exist_ok=True)
    json.dump(result, open(os.path.join(args.out, "modes.json"), "w"), indent=1)
    with open(os.path.join(args.out, "modes.md"), "w") as f:
        f.write(f"# Agent modes ({len(tables)} table copies found, using the largest with {len(table)} modes)\n\n")
        f.write("| mode | model | systemPrompt | includeTools | deferredTools | sent up front |\n|---|---|---|---|---|---|\n")
        for k, v in result.items():
            f.write(f"| {k} | {v['model']} | {v['systemPrompt']} | {len(v['includeTools'] or [])} | {len(v['deferredTools'])} | {len(v['sentUpFront'])} |\n")
        for k, v in result.items():
            f.write(f"\n## {k}\n\n- includeTools: " + ", ".join(f"`{x}`" for x in (v["includeTools"] or [])) + "\n")
            f.write("- deferredTools: " + (", ".join(f"`{x}`" for x in v["deferredTools"]) or "(none)") + "\n")
    print(f"{len(tables)} table copies; using largest ({len(table)} modes) -> {args.out}/modes.json, modes.md")
    for k, v in result.items():
        print(f"  {k:10s} {v['model']:18s} prompt={v['systemPrompt']:9s} include={len(v['includeTools'] or []):3d} deferred={len(v['deferredTools']):3d}")


if __name__ == "__main__":
    main()
