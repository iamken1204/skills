# TDD bug fix

When fixing a bug with a clear, cheap test path, make the broken behavior executable before changing production code. The goal is a focused regression test that fails before the fix and passes after it.

Do not force a test when it would be impractical. If the available test would require broad harness setup, brittle mocks, slow end-to-end infrastructure, production-only state, vague reproduction steps, or large unrelated fixture churn, skip the new test and use the closest useful verification instead.

## Workflow

1. **Understand the bug.** Intended behavior, current behavior, affected path, smallest observable reproduction.
2. **Choose the narrowest executable check.** Prefer the closest unit, component, integration, or regression test already used for that codepath. No practical path → don't create one from scratch just to satisfy the workflow.
3. **Write the failing test first.** The smallest focused test that would have caught the bug, encoding intended behavior, not mirroring the implementation.
4. **Run it before fixing.** Confirm it fails for the intended reason; if it passes or fails for an unrelated reason, correct the test or reproduction first.
5. **Fix the bug.** The smallest production change that satisfies the intended behavior while preserving nearby contracts.
6. **Rerun the regression test.** Confirm it passes.
7. **Run nearby validation** (adjacent tests, types, lint) when the change has broader risk.

## If a failing test is impractical

Do not silently skip the regression step. Explain why before fixing, then choose the closest executable check: a targeted script, a manual reproduction command, browser automation, snapshot comparison, log assertion, or focused integration check.

Prefer no new test over a bad test: one that mostly tests mocks, encodes implementation details, depends on timing or unrelated global state, needs expensive infrastructure for a small fix, or would be deleted right after proving the fix.

## Guardrails

- Do not change tests merely to match a wrong implementation.
- Do not weaken existing assertions unless expected behavior genuinely changed and the reason is clear.
- Keep the regression test focused on the bug; no broad fixture churn.
- If the bug is flaky, make the test deterministic where possible and document the signal being locked down.
- If the bug exposes a broader class of failures, land the focused regression first, then consider sibling coverage.

## Final response

Report the evidence, not just the outcome: the failing-before check and the failure it produced, the passing-after run and nearby validation, or why failing-before evidence couldn't be demonstrated and the closest check used instead.
