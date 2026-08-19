# How

Build the implementation model before changing code. Trace the runtime flow, data shape, ownership, boundaries, and verification path that the change depends on. The output feeds the calling playbook; it is not a standalone architecture explanation. Use `references/why.md` only when historical intent could change the design.

Two modes apply. **Ground** is the default. **Critique** adds a structural assessment when the existing design constrains the change.

## Ground

1. **Scope the change.** Name the behavior being changed, its entry point, and the observable result. State a best-guess scope when details are missing; do not stop to ask about facts the code can answer.
2. **Trace the real path.** Follow the behavior from input to output through the actual symbols. Read callers, callees, types, tests, and configuration. Do not infer ownership from file names.
3. **Scale the exploration.** Inspect a single-module path directly. For a cross-cutting path, split 2-4 read-only explorers by distinct concerns such as data model, runtime flow, boundaries, and verification. Reconcile overlaps and contradictions before proceeding.
4. **Record the implementation model.** Keep it compact and point to files and symbols rather than pasting code.
5. **Resolve material history.** Run `references/why.md` only when a current invariant, workaround, or ownership boundary may encode a constraint that the implementation must preserve.

### Implementation model

- **Flow.** Trigger, main calls, decisions, and output.
- **Data.** Authoritative types, state owners, transformations, and persistence.
- **Boundaries.** Validation, external systems, framework adapters, and error ownership.
- **Invariants.** Conditions the implementation must preserve and illegal states it must avoid.
- **Verification.** Existing tests, control surface, fixtures, and the shortest real path from input to output.
- **Change map.** Files that must change, likely callers, and areas that should remain untouched.
- **Unknowns.** Unverified facts that could change the design or verification plan.

## Critique

Run Ground first. Then assess only issues that affect the intended change:

- whether the data model matches the access patterns;
- whether ownership and validation sit at the right boundaries;
- whether a layer hides real complexity or only forwards it;
- whether the probable next requirement would change one owner or many unrelated files;
- whether the change can delete complexity instead of adding another path.

Return findings as **Act on**, **Consider**, or **Dismissed**. The calling playbook decides the design and resumes implementation.
