### Autonomous run

**You own the exit condition. Define done, then drive to it without stopping.** For "going to bed" / "run until done" / "loop until X".

1. State the exit condition as a checkable predicate before the first iteration (tests green, repro fixed, all N units verified, pixel-diff zero). A vague goal stalls; a predicate lets you stop.
2. Pick the wake mechanism from the harness's loop or scheduler facility. An event to watch (CI, a merge, a ref advancing) gets a watcher that wakes you on the event, with a long time-based heartbeat as fallback. No event gets a fixed-interval heartbeat sized to when the result is worth re-checking. No such facility → keep iterating in-session.
3. Each iteration makes the smallest change the evidence justifies, verifies it against the predicate, commits if it advanced, discards changes that didn't help. Belt-and-suspenders that "might help" gets reverted, not left to ride. Verify each unit before the next instead of batching checks at the end (the sequence-verifiable-units principle).
4. Mid-run discoveries are yours. Address broken skills, related bugs, flaky verifiers, review noise, tooling failures, orphaned follow-ups, and fixable drift yourself; keep out-of-band fixes as separate changes. Do not park reversible work for the human. Surface only irreversible actions, genuine product calls no experiment can settle, or a real dead end. Keep the predicate as the main drive, and return to it after each side fix.
5. Checkpoint every iteration via `references/decision-trail.md`, a row for what changed and whether the predicate moved. A run with no trail can't be audited or resumed.
6. Stop when the predicate is met. A plateau is not a stop; keep going and pivot your approach to push past it. Surface a genuine dead end rather than spinning, and never relax the predicate to declare victory.

**Reply:** the exit condition, iterations run, what landed, what was discarded, final predicate state.
