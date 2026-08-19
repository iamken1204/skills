# Arena

Fan out N parallel attempts at the same task. Read every candidate end to end. Pick the strongest as the base. Graft the best ideas from the others into it. Verify the synthesized result.

Open a todolist with one entry per phase: Frame, Fan out, Cross-judge, Pick, Graft, Verify.

## Phase A: Frame

The N candidates receive the same prompt, so the prompt is the contract. Get it right before spawning anything.

1. State the artifact each candidate is producing.
2. Derive the rubric: what success looks like for *this* task, as 3-6 concrete gradeable criteria (`Adds a --dry-run flag that skips writes`, not `code is correct`). The rubric is the picker's tool in Phase D; candidates only see the task.
3. Pick the runners: one per available model family by default; more when the arena covers multiple design directions; the same model N times when the work is generation-bound rather than judgment-sensitive. A single-model harness still runs N fresh contexts.
4. Assign output paths. Each candidate writes to its own isolated location. N candidates writing to one path is shared mutable state and fails the separate-before-serializing-shared-state principle.

## Phase B: Fan out

Spawn all N at once, background where offered, each with the task, the shared grounding, its own output path, and instructions to produce the artifact plus a short rationale. The rationale is mandatory: without it the parent cannot tell whether a candidate's structure is principled or accidental, which makes grafting unreliable. Each rationale names the alternatives considered and rejected. If a candidate fails to produce output, proceed with N-1 and note the dropout.

## Phase C: Cross-judge

After all candidates complete, spawn one read-only judge on a different model family from your own (or a fresh context). It sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with your own reading in Phase D, never while candidates are still writing (it would score partial outputs as dropouts).

## Phase D: Pick a base

Read every candidate end to end before picking; skimming surfaces only the candidate whose surface looks most familiar. Score each against the rubric criterion by criterion, not holistic feel. Compare with the cross-judge: agreement confirms the pick; disagreement means one of you is biased or the rubric was ambiguous, so read both rationales before deciding. Pick the base a future maintainer can extend most easily without breaking invariants; prefer the cleaner boundary or smaller surface when tied. Record the pick, the reason, and the judge's verdict in a short synthesis note.

## Phase E: Graft

Walk each losing candidate once more and identify what is worth porting: usually one or two things per candidate, not most of it. Fold each graft in by hand per the redesign-from-first-principles principle; don't paste mechanically. The result must remain coherent under one mental model. Record what was grafted, from which candidate, and what was rejected and why; the rejection notes are the highest-signal part of the record.

When candidates converge on the same shape, that is strong agreement: note it and ship the consensus, no graft needed. When they wildly diverge, Phase A was under-specified: reframe and re-run rather than averaging.

## Phase F: Verify

The synthesized artifact holds up under the same scrutiny as any other output (the prove-it-works principle); the arena does not earn a pass. If verification surfaces a problem the arena didn't catch, either Phase A was wrong (re-frame and re-run) or one candidate caught it and you missed the graft (back to Phase E). Don't paper over.

## Outputs

One synthesized artifact and one synthesis note: the base, the grafts with sources, the rejections, dropouts if any, and the verification result.
