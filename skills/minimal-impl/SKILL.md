---
name: minimal-impl
description: Write the minimal implementation — use when the user asks for the simplest or bare-bones version, says "YAGNI" or "minimal", or complains about over-engineering or bloat.
---

Ship the **smallest complete change that satisfies the request and existing contracts**. Before writing code, stop at the first rung that holds:

1. Speculative need → skip it, say so in one line.
2. Stdlib or native platform feature covers it → use it.
3. An already-installed dependency covers it → use it.
4. Otherwise: write the minimum code that works, or add a dependency when it reduces overall implementation and maintenance complexity or fulfills an explicit requirement.

Rules:

- No abstraction with a single use: no interface with one implementation, no factory for one product, no config for a value that never changes.
- No scaffolding "for later" — later can scaffold for itself.
- Deletion over addition; boring over clever.
- The shortest diff is not a reason to preserve dead compatibility. Before keeping a mode, prop, wrapper, route alias, or fallback, search for current callers and contracts. If none exist and it is not a public, external, or persisted contract, delete it.

Done when every line in the diff serves the requested behavior, correctness, readability, or necessary verification. Never cut input validation at trust boundaries, error handling that prevents data loss, or anything explicitly requested. Run verification appropriate to the change before finishing.
