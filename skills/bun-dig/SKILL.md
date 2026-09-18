---
name: bun-dig
description: "Dig the tool specs, prompts, and implementations out of a Bun-compiled single-file CLI such as Amp. Use when the user wants to know which tools an agent binary ships, extract its tool descriptions or instructions, see what changed between two versions, or unpack a Bun executable at all."
---

# Bun Dig

A Bun single-file executable carries its whole JS bundle inside the binary. `strings` finds almost nothing because the source is stored as UTF-16LE, and every identifier is re-minified per build. Work from structure and string literals, verify on the running binary, and keep one `tools.json` per version so the next release can be diffed instead of re-read.

Scripts live in `scripts/`; each has a docstring with the exact layout it depends on.

## Unpack the bundle

1. `python3 scripts/unpack.py <binary> -o unpacked/`. It locates the `---- Bun! ----` trailer, reads the module table, and writes every module decoded (JS as UTF-8, `.node` and other assets as raw bytes).
2. If the table layout is unknown, the script falls back to the `// @bun` header at the graph base. If that also fails, dump the last 64 bytes before the trailer with `xxd` and update the `Offsets` layout in the script.
3. Note the version (`<binary> --version` usually works) and keep the unpacked JS next to the outputs; every later step reads it.

## Extract the tool specs

1. `python3 scripts/extract_tools.py unpacked/<main>.js -o out/`. It scans for `{name:CONST,description:…,inputSchema:…}` objects, resolves the name constant, description constants, `${…}` interpolations, embedded example arrays, and zod schemas, and writes `tools.json`, `tools.md`, and `impls.js` (first-level `fn` bodies).
2. Read the printed name list. Expect fewer tools than the agent advertises: only tools executed on the user's machine live in the binary. Server-side tools appear as bare names in permission lists and mode tables, never with a description.
3. Anything reported as unresolved is a `${…}` whose expression is not a plain constant or an example-array call. Open the site by its `pos`, read the expression, and resolve it by hand.

## Read the rest by structure, never by name

- Anchor on string literals (`"skill"`, `systemPrompt:"`, `spec:{name:`), then resolve the identifier next to them. Identifiers seen in a previous build are worthless.
- Bundles use lazy-init blocks: `var a,b,c;` is declared far from `a=...` assignments. Resolve a constant with the nearest definition before its use, not the first match in the file.
- Scopes reuse short names. `Ut` was a URI helper in one module and a zod array in another. When a resolved definition makes no sense for the call site, search again restricted to the neighborhood of the site.
- The same table can be bundled twice (a shared package and the CLI). Pick the copy the consumer code reads, or the larger one; `amp_modes.py` does the latter.
- Schemas come in two shapes: JSON-schema literals, and `FN(ZOD_CONST)` where the zod object is another constant. Zod factory names are minified too, so compare schemas with those masked.
- Descriptions embed example arrays through a renderer (`${B0(examples)}` in Amp). Render them; the model sees the rendered text.

## Verify on the real binary

- If the CLI can list its own tools, run it and compare counts, for example `amp tools list --mode high --json`. This is the only check that catches a wrong table copy or a filter you misread.
- A local tool whose `fn` only calls an API client is a thin wrapper; grep the body and its helpers for `fetch(`, `/api/`, or the client object before claiming the work happens locally.

## Diff two versions

1. Keep `out-<version>/tools.json` for every build you have looked at.
2. `python3 scripts/extract_tools.py --diff out-old/tools.json out-new/tools.json` prints added and removed tools and a unified diff of each changed description and schema, with minified names masked.
3. Report description changes as prompt-engineering changes: they are the instructions the model receives.

## Make an implementation readable

Only when asked; it is judgment work, not extraction.

1. Cut the `fn` body and its helper closure out of the bundle, then format each definition separately with `prettier --parser babel` (one bad block must not sink the file).
2. Rename by reading. Keep the original minified name in a comment above each function so the result can be checked against the bundle.
3. Port the tool's own logic in full; stub shared infrastructure (observables, mutexes, guidance-file discovery) with a typed `declare` and one line saying what it does.
4. `tsc --noEmit --strict` on the result; missing third-party modules are the only acceptable errors.

## Amp

`references/amp.md` records what is known about the Amp CLI: executor architecture, which tools are local, the mode table and its gating logic, and the quirks found so far.
