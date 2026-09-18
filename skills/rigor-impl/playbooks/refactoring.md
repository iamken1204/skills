### Refactoring

**You own the contract. The structure changes. The behavior does not.** Distinct from Feature, which adds behavior, and Bug fix, which corrects it.

If the cleanup reveals a missing feature or a real bug, split it out and ship the structural change first against the pinned contract. A redesign is allowed, but name it and route to Feature. Large or cross-cutting structural work belongs to `references/figure-it-out.md`. This playbook is the focused-to-medium change.

1. Pin the behavior contract first. Run `references/how.md` over the affected subsystem to learn the contract, then write a characterization test, snapshot, or equivalence harness that captures current behavior before any structure moves. No coverage → write the pin before touching structure. Type check and lint are not a pin.
2. Name the structure the code is missing per the model-the-domain principle. Boring code stays when the shape is already clear and local. The reshape must delete branches or invalid states, not add indirection.
3. Name the target shape: what the module layout, types, and call graph should be if built today (the foundational-thinking and redesign-from-first-principles principles). If the target crosses a function boundary, run `references/architect.md` for parallel design exploration before the move.
4. Subtract before you add. Delete dead code, collapse one-caller wrappers, drop redundant validators, remove orphan references before introducing the new shape. The smallest change that reaches the target shape ships. A speculative cleanup that "might help" gets reverted.
5. Move in small behavior-preserving steps, each keeping the pin green. For API reshapes, migrate every caller and delete the old API in the same wave (the migrate-callers-then-delete-legacy-apis principle). No compatibility shims, no parallel old-and-new paths. Spot-check every rename against the actual files. Renames silently miss usages in strings, prose, and back-references. Delegate the mechanical edits to a subagent on the cheap model with a specific scope. Review the diff yourself.
6. Prove behavior is unchanged on the real artifact, not "it compiles". For larger reshapes, run an equivalence check: a script diffing old-vs-new outputs, a recorded baseline replayed against the new code, or a smoke run on the matching control surface. Own the verification yourself. Don't trust a delegate's "looks good".
7. Confirm the change is worth keeping. The success measure is reduced reader load (the minimize-reader-load principle). If the diff does not lower reader load somewhere, revert it.
8. Organize the work into small ordered commits. A subtraction commit, then the reshape, then any follow-on cleanup, each behavior-preserving slice staying green before the next (the sequence-verifiable-units principle).

**Reply:** the structure that changed, the pin you held it against, the equivalence proof, the reader-load delta, what shipped and what got reverted. No new behavior.
