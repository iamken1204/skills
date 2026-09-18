# Arena

Fan out N parallel attempts at the same task. Read every candidate end to end. Pick the strongest as the base. Graft the best ideas from the others into it. Verify the synthesized result.

Open a todolist with one entry per phase: Frame, Fan out, Cross-judge, Pick, Graft, Verify.

## Phase A: Frame

The N candidates receive the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric. State what success looks like for *this* task, then turn it into 3-6 concrete gradeable criteria. The rubric is the picker's tool in Phase D. Candidates only see the task.
3. Pick the runners. One per available model family by default. More when the arena covers multiple design directions. The same model N times when the work is generation-bound rather than judgment-sensitive. A single-model harness still runs N fresh contexts.
4. Assign output paths. Each candidate writes to its own isolated location, per the separate-before-serializing-shared-state principle.

## Phase B: Fan out

Spawn all N at once, background where offered, each with the task, the shared grounding, its own output path, and instructions to produce the artifact plus a short rationale. Each rationale names the alternatives considered and rejected. If a candidate fails to produce output, proceed with N-1 and note the dropout.

## Phase C: Cross-judge

After all candidates complete, spawn one read-only judge on a different model family from your own (or a fresh context). It sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with your own reading in Phase D, not with the candidates themselves. Don't spawn the judge while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not holistic feel. Compare with the cross-judge. Agreement confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous, so read both rationales before deciding. Pick the base a future maintainer can extend most easily without breaking invariants. Prefer the cleaner boundary or smaller API when tied. Record the pick, the reason, and the judge's verdict in a short synthesis note.

## Phase E: Graft

Walk each losing candidate once more and identify what is worth porting: usually one or two things per candidate, not most of it. Fold each graft in by hand per the redesign-from-first-principles principle. Don't paste mechanically. The result must remain coherent under one mental model. Record what was grafted, from which candidate, and what was rejected and why.

When candidates converge on the same shape, that is strong agreement. Note it and ship the consensus, no graft needed. When they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging.

## Phase F: Verify

The synthesized artifact holds up under the same scrutiny as any other output (the prove-it-works principle). If verification surfaces a problem the arena didn't catch, either Phase A was wrong (re-frame and re-run) or one candidate caught it and you missed the graft (back to Phase E). Don't paper over.

## Outputs

One synthesized artifact and one synthesis note: the base, the grafts with sources, the rejections, dropouts if any, and the verification result.
