### Perf issue

**You own the measurement story. Plan, review, verify the numbers.** Tie every fix to a measurement. Don't read source instead of measuring.

1. Capture a baseline trace via the matching control surface.
2. `references/how.md` to ground hypotheses. Don't claim a perf ceiling without running it first. Most fixes come from eight strategy families. Use them as hypothesis generators, not a checklist. A family earns an attempt only when the trace shows the signal it names.
   - **Elimination.** Before optimizing the hot path, ask whether it needs to exist: a computation nobody consumes, a gate always off for this user, a redundant sync, a legacy path kept "just in case". The trace shows what's slow, never that it's deletable, so this family needs the how pass, not the profiler.
   - **Divide and conquer.** The dominant cost scales with input size. Split the work so each piece touches less, or so independent pieces run in parallel.
   - **Caching.** The same computation or fetch repeats on identical inputs. Store and reuse. Name what invalidates it before claiming the win.
   - **Indirection.** The hot path does expensive work a cheaper intermediate could absorb: an index instead of a scan, a queue off the interactive thread. Add the hop only when it removes more from the critical path than it adds.
   - **Batching.** Many small operations each pay a fixed overhead (RPC, query, syscall, draw call). Coalesce to pay it once per batch.
   - **Redundancy.** The wait hangs on one slow instance. Duplicate the work (replicas, hedged requests) and take the fastest result. The trace has to show the wait dominates and the system has headroom.
   - **Lazy evaluation.** Cost lands on results never used or not needed yet. Defer until first use.
   - **Scheduling.** The work must happen, but not during the interactive moment: idle callbacks, background warmup, precompute, post-frame cleanup. The win is perceived latency, so measure the interactive path, not total work.
3. Plan the fix from the trace. If it crosses a function boundary, `references/architect.md` first. Delegate implementation to a subagent on the cheap model. Review the diff. Capture a post-fix trace. Verify each attempt before trying the next (the sequence-verifiable-units principle).
4. Parse and compare the artifacts (JSON to sqlite, diff). "Inconclusive" or wrong-surface is not a pass. Flag it.
5. Cite the measurement in the commit message and PR or MR description.

For sustained improvement against a metric rather than a one-off fix, use the Hillclimb playbook.

**Reply:** baseline number, post-fix number, delta, artifact path.
