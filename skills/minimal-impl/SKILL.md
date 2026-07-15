---
name: minimal-impl
description: Write the minimal implementation — use when the user asks for the simplest or bare-bones version, says "YAGNI" or "minimal", or complains about over-engineering or bloat.
---

Ship the **shortest working diff**. Before writing code, stop at the first rung that holds:

1. Speculative need → skip it, say so in one line.
2. Stdlib or native platform feature covers it → use it.
3. An already-installed dependency covers it → use it; never add a new one.
4. Otherwise: the minimum code that works.

Rules:

- No abstraction with a single use: no interface with one implementation, no factory for one product, no config for a value that never changes.
- No scaffolding "for later" — later can scaffold for itself.
- Deletion over addition; boring over clever.

Done when every line in the diff is **load-bearing**: removing it would break the requested behavior. Never cut input validation at trust boundaries, error handling that prevents data loss, or anything explicitly requested.
