### Feature

**You own the design. Plan, review, verify.** Delegate implementation; stay in the lead.

1. `references/how.md` over the affected subsystem.
2. `references/architect.md` for parallel design exploration. Skipping stays as `architect skipped: <reason>`; do not fold the design decision silently into implementation.
3. Write the throughput checkpoint as four todo items. A dimension that genuinely does not apply keeps its item with `n/a: <reason>` rather than being dropped:
   - **Blocking first steps.** Gates run before fan-out.
   - **Independent workstreams.** Disjoint files, services, or layers parallelize. Shared writes serialize.
   - **Shared mutable state.** Default to splitting the target (the separate-before-serializing-shared-state principle). Serialize only for real invariants.
   - **Smallest safe decomposition.** If one worker is best, name why.
4. Delegate code-writing to a subagent on the fast model with a specific scope: file paths, the named data shape and its organizing structure per the model-the-domain principle (a state machine over scattered booleans, a table over branching, a typed model over repeated shape assumptions, chosen before the delegate writes logic), and success criteria. Review its diff yourself. When the implementation admits multiple valid shapes (error handling, abstraction layer, test structure), delegate via `references/arena.md` instead so the runners surface the alternatives and the cross-judge guards the pick. Mandatory: no skip-with-reason escape, and the Laziness Protocol does not override it (the gain is review separation, not lines saved). You can spawn a subagent even though you are one; "the app is small" and "a subagent cannot spawn one" are both wrong. A subagent forbidden to spawn satisfies this by owning the diff directly with the same review separation. Comments per the mode's Comments section. Surgical edits; re-ground against the source for upstream-derived files. Port shared-primitive improvements to all consumers and verify each. Commit liberally.
5. Verify on the matching surface. "Inconclusive" or wrong-surface is not a pass; flag it.
6. Organize the work into small, ordered commits. Build, verify, and commit each small unit before the next (the sequence-verifiable-units principle).
7. If the design is contested, `references/interrogate.md` before shipping.

Code-coupled work (one feature, one migration) goes to a single owner with the checkpoint inline; that owner fans out internally after the blocking phase. Parent-level fan-out is for slices that produce independent artifacts (audits, cross-subsystem investigations, competing experiments). Rewrite the checkpoint at phase boundaries; spawn a fresh owner rather than chaining interrupts.

**Reply:** what you built, what you chose and why, open decisions. Tables for design alternatives.
