# Architect

Design before implementing. Sketch types, function signatures, class shapes, and module boundaries with `not implemented` bodies and pseudocode. Synthesize across multiple independent perspectives, then fill in code against the chosen sketch. If implementation proves the sketch wrong, throw it out and redesign.

Open a todolist with one entry per phase: Ground, Sketch, Agree, Implement, Scrap.

## Phase A: Ground

Build a real mental model of every system the new code touches. Run `references/how.md` over the relevant subsystems, Critique mode if existing structure is the constraint. Naming a file isn't grounding; produce the traced model. If the design redefines ownership or layering, also run `references/why.md` on the existing shape so the rationale becomes a constraint, not a guess. Skip Phase A only for genuinely greenfield work with no surrounding system.

## Phase B: Sketch

Run `references/arena.md` with the design-sketch task and the Phase A grounding. Each candidate produces a design package: the caller's usage written first, then the type sketch, function signatures, module map, and a prose rationale derived from it, naming the alternatives it considered and rejected. Use one runner per available model family.

Design it twice. Require at least two structurally distinct candidates before synthesis, even when the first looks sufficient (the exhaust-the-design-space principle). Whole-shape alternatives, not point fixes inside one shape.

Screen every candidate against the red flags below before synthesis. Compare viable candidates on interface depth: prefer the design that hides more complexity behind a smaller public surface. A rich interface can keep call chains short by concentrating capability instead of scattering it across layers.

### Design red flags

- **Shallow module.** A large interface hiding little complexity. Signs: callers coordinate several methods to complete one operation; public options expose internal stages; learning the interface doesn't save the caller from learning the implementation. Don't confuse a deep module (capability concentrated behind one interface) with a deep call chain (understanding scattered across layers).
- **Information leakage.** A representation, policy, or protocol detail appears in more than one place, so changing it requires coordinated edits. Public re-exports of transport or wire types are leakage; parse external data into domain types behind the interface.
- **Temporal decomposition.** Modules organized by execution order (load, validate, transform, save) instead of the knowledge they own, repeating one representation and its invariants across boundaries. Group code around domain knowledge and ownership.
- **Pass-through method.** Forwards the same arguments to another method with the same shape: a layer without hiding. Remove it, or keep a forwarding boundary only when it adds policy, adaptation, or a distinct abstraction.

## Phase C: Agree (opt-in)

Default: proceed directly to implementation with the synthesized design. Opt in to a human checkpoint only when the invoker explicitly asks ("stop and show me before implementing"). The synthesis can ship as its own commit either way; subsequent commits read as filling in bodies against a stable contract. Planned, scoped breakage during fill-in is fine (the outcome-oriented-execution principle). For adversarial pressure on the design before implementing, run `references/interrogate.md` on the sketch. If the human pushes back on the shape, treat that as Phase A evidence: re-ground and re-run Phase B.

## Phase D: Implement against the sketch

Replace `not implemented` bodies with code. The sketch is the contract. Deviations are signal worth surfacing, not friction to absorb silently: if a function needs a parameter the sketch didn't anticipate, ask whether the sketch was wrong, the requirement was missed, or the implementation is overreaching.

## Phase E: Scrap when the architecture is wrong

If implementation keeps producing friction the sketch can't absorb, throw the sketch out rather than bolting fixes onto a wrong design. The signal is a *pattern*, not single instances:

- The same shape of workaround appearing repeatedly across unrelated code.
- Multiple unrelated edge cases all needing special-case branches.
- Types needing escape hatches (`any`, casts, optional fields always set) to compile.
- The "we need a lock" reflex when the sketch said the state wasn't shared.
- Callers having to know the abstraction's internal rules to use it.
- Two or more independent Phase D deviations of the same shape.

Use judgment: a few edge cases don't condemn an architecture, and complexity in the data is not complexity in the design. When you scrap: re-run `references/how.md` over what's been built so the implementation lessons enter the new design as inputs; redesign as if the new constraints had been day-one assumptions; subtract before adding (the new sketch should be smaller than the old one before it grows); return to Phase B.

## Outputs

The caller's usage first, the type sketch derived from it. One file with new types and signatures for small changes; module map plus type definitions for larger work. The rationale ships alongside, including the usage sketch and the synthesis decision.
