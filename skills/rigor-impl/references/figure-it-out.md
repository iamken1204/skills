# Figure it out

When the task matches no playbook, design one. The deliverable before any code is the workflow itself: a sequence of phases that scales rigor to the task, runs the scientific method, and leaves a decision trail a human can audit after stepping away. Bias toward more rigor; the cost of building the wrong thing dwarfs the cost of being careful.

Don't reinvent a playbook you already have. A focused single-unit task routes to its narrow playbook. But a large or cross-cutting version of one (a migration across many call sites, an ambitious multi-part change), or work the user reviews after stepping away, belongs here even though a single-unit version would be a Feature. The rigor and the audit trail are the point.

Open a todolist whose first item is to read the rigor-impl Principles index, then add the phases below.

## Phase A: Frame

Ground first, then commit. Don't start until you can state:

- The definition of done as a falsifiable predicate (the prove-it-works principle). "Done well" has to be checkable.
- Scope, quantified: rough units and effort, plus the blockers grounding surfaced. Raise them before spending hours, not after fifty doomed commits.
- The rigor level, biased high. One-way doors and high blast radius get more; reversible low-stakes steps get less. Rigor is gates and artifacts, not "try harder".

Present the framing and tradeoffs before committing to a long run. Reversible work proceeds (the never-block-on-the-human principle), but a multi-hour run earns one checkpoint.

## Phase B: Design the workflow

Decompose into atomic, independently-landable units. Sequence riskiest-unknown-first so option value stays high. Scaffold and verification before features (the foundational-thinking principle).

- Build the verification harness before the work, with the baseline captured from the pre-change state, so the check reads as "old value vs new value".
- For one-way-door design decisions, run `references/architect.md` (which runs the arena) with diverse, isolated candidates and a read-only judge on a different family. Skip it for mechanical work whose shape is already concrete; a second arena over a settled design is over-engineering.
- Decide what fans out. Parallelize only across genuine seams, each worker with an isolated writable output (the separate-before-serializing-shared-state principle). Don't over-fan.
- Write the designed phase list down. That list is what the human reviews.

Then put the design into motion: add its steps as concrete todos between Phase C and Phase D, run each under the Phase C loop discipline, and weave the Phase D log through them, a row as each step lands.

## Phase C: Run the loop

Each unit is an experiment: state the hypothesis, make the smallest change, measure against the predicate on the real artifact, keep it if it advanced, revert if it didn't. Verify each unit before the next (the sequence-verifiable-units principle).

- Verify by inspecting the artifact, never a self-report. When something passes too easily, suspect the observation method before the system. A blank screenshot passes a lazy gate.
- Pair delegated work with a judge and audit the delegates' artifacts yourself. If a worker games the gate, reset and harden the contract. If the gate itself is wrong, fix the gate in its own change rather than routing around it.
- A verdict is VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Inconclusive is not a pass. Don't hide a negative.

## Phase D: Keep the audit trail

Log the run via `references/decision-trail.md`, one canonical TSV with a row per decision and per unit, evidence as links. This work is usually ambitious enough to commit the trail as a review artifact when confidence has to be shown. Prefer evidence produced by committed scripts a reviewer can re-run.

## Phase E: Verify and hand back

Check the whole against the Phase A predicate on the real product, not just the harness. Encode any recurring correction as a gate, lint, check, or script so the win can't silently regress (the encode-lessons-in-structure principle).

**Reply:** the playbook you designed, the rigor level and why, the decision-trail path, what's verified against the predicate, and what's still open.
