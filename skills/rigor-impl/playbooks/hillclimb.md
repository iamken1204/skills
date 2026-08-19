### Hillclimb

**You own the metric and the experiment's integrity. Supervise and review; delegate the attempts.** For sustained, iterative improvement of one measurable thing against a target ("make startup 50% faster", "keep trying until <metric> improves by N%"). A one-off fix is Bug fix or Perf issue; this is the loop.

Core discipline: one change, one measurement, keep or revert. Never stack untested changes, and never claim a win from code inspection. The data decides (the prove-it-works principle).

1. Ground the workload and architecture before choosing the ruler. Run `references/how.md` over the target, name the realistic workload dimensions that can move the result (data size, history, state, concurrency), and select a case that reproduces the user's complaint. If no case reproduces it, fix the repro instead of hillclimbing. Then fix one metric, the direction that counts as better, and a checkable stop predicate that pairs a target with a floor on attempts so a lucky early win can't end the run ("at least 50% better than baseline and at least 10 iterations"). Use the user's numbers when given, otherwise agree them.
2. Build the measurement harness, prove its sensitivity, then freeze it (the build-the-lever principle). Run contrasting realistic workloads and confirm the target case reproduces the symptom while easier cases separate as expected. If the ruler cannot distinguish them, revise the workload or metric. Once frozen, one repeatable command emits the metric, sampled enough to clear the noise (median of N, not a single run); changing it invalidates every earlier number. Record the baseline metric and a green run of the regression gate before any change.
3. Open the decision log via `references/decision-trail.md`: one row per attempt with id, hypothesis, change, before, after, delta, tests, verdict (kept or reverted), note. This is the run's memory; read it before each attempt so the search accumulates instead of circling. Keep it out of the tree (gitignored) so it survives reverts.
4. Ground each hypothesis in the step-1 architecture model, so it names a specific mechanism ("defer X off the boot path because it blocks first paint"), not "try memoizing something".
5. Loop, one hypothesis per iteration:
   - Hand the change to a subagent on the instruction model with a tight scope; supervise and review the diff rather than typing it. When several independent hypotheses are live, fan them to parallel subagents, each with an isolated writable output so they can't collide.
   - Measure before and after with the frozen harness, and run the regression gate.
   - Accept only when the metric moves past noise and the gate stays green. Otherwise revert in full; a tweak that "might help" does not ride along.
   - One commit per accepted fix, staging only the files you changed (`git add <files>`, never `-A`). Log the row either way.
   Each iteration ends in a check before the next begins. If the run is unattended, borrow only the wake mechanism from the Autonomous run playbook, not its stop rule; this playbook's stop criteria govern, so a plateau means pivot, not stop.
6. Push past the first plateau. On a stall, pivot category, combine near-misses, re-read the source, or try something more radical before concluding the hill is climbed. Correctness and simplicity outrank the number: revert a win that breaks behavior, keep a simplification that holds the number.
7. Stop when the predicate is met, or when the remaining ideas are genuinely marginal. Don't relax the predicate to declare victory, and don't quit while cheap untried hypotheses remain. Stuck → surface it instead of spinning.

**Reply:** the metric and target, baseline to final with the percent delta, iterations run (kept vs reverted), each accepted fix on one line, the decision-log path, and the best idea you'd try next if pushed further.
