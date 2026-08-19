### Eval

**You own the experiment design. Plan, blind, run, synthesize.**

Evals test how a change affects agent behavior before promoting it: a new skill variant, a structural change, a prompt tweak. The failure mode is the observer effect. An agent that knows it's being evaluated behaves differently, so candidates must run blind.

**Non-negotiables for blinding:**

- No `eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `compare`, `benchmark`, `candidate`, or `arena` in any directory, file, or prompt the candidate sees.
- The candidate prompt looks like an organic user request. State the goal, not the meta: "build me a small todo cli", not "show me how you follow the principles chain".
- No chain-eliciting cues. Don't ask the candidate to list which skills or principles it applied; that meta-prompt inflates citation behavior. Ask for design notes generally and grade chain-following from code shape, not self-report.
- Sanitize directory and slug names: project-shaped names a user might pick, not `candidate-1`.
- Don't tell the candidate other candidates exist.
- The judge can know it's judging but sees outputs by sanitized label only, never by model name.
- Comparing two variants: one judge scores both sets in a single pass on one scale, blind to which set each came from. Two judge runs with different prompts don't compare; the calibration drifts.

**Steps:**

1. **Frame.** State the variant under test and what behavior counts as success. Write the rubric (3-6 concrete criteria) for the judge only; hold it back from candidates.
2. **Set up sanitized environments.** Per-candidate working dir with the variant in place. Plant the context an organic task would have: a project skeleton, the files the candidate would naturally read.
3. **Author one organic prompt.** What a user would type, no leakage of what's being measured.
4. **Spawn N parallel candidates** on different model families per `references/arena.md` Phase B, each in its own sanitized dir, same prompt.
5. **Spawn one blinded judge** on a different family per arena Phase C, seeing outputs by sanitized label and the rubric.
6. **Verify the chain from the record, not self-report.** Where the harness exposes candidate transcripts or session logs, read which files each candidate actually opened; stay inside this workspace's logs, never other projects'. Citing a principle is not reading its rule, and reading is not applying. Grade chain-following from the files really read plus the shape of the code, never the candidate's claims. Where no transcript exists, grade from the artifacts alone and say so.
7. **Read every candidate output yourself** end to end. Compare to the judge's verdict; disagreement means a model is biased or the rubric is ambiguous. Synthesize.

**Reply:** variant under test, rubric, per-candidate notes, judge's verdict, your synthesis, and a recommendation for whether to promote the variant.
