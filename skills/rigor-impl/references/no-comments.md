# No comments

Strip comments before review. Spawn a fresh-context comment reviewer, act on accepted findings, and offer structural encodings for claimed constraints. Authoring agents defend their own comments; the fresh perspective is the point, so the reviewer is never the context that wrote the code.

## Scope

The caller's files or diff; otherwise the current diff against the base branch (default `main`), including the working tree.

## The reviewer's rules

Spawn one delegate with the scope and these rules verbatim. It touches comments and identifies refactor targets; it never writes application code, invents nothing, and reports only.

Delete every comment except these:

- Legal or license headers.
- Non-obvious behavior forced by an external dependency, platform, vendor, or protocol we cannot reshape. Surprises in *our own* code get the comment killed and the exact symbol marked `MUST KILL`: rename, extract, type, or rearchitect so the behavior is obvious without prose.
- `// prettier-ignore`. Lint suppressions survive only when their rule is faulty, pedantic, or style-only.
- Doc comments that define a public API contract.
- Issue or RFC links that explain a constraint code cannot express.

When unsure whether a keep clause applies, the comment dies. `eslint-disable`, `@ts-ignore`, `@ts-expect-error`, and similar suppressions: look up the rule; if it catches real bugs or protects correctness or safety, kill the suppression and mark the guilty symbol `MUST KILL`. `IMPORTANT`, `do not remove`, `too risky`, and long justifications are scent, not conviction: read the nearby code, run `references/how.md` or `references/why.md` on the named symbol when the claim isn't obvious, and keep only a foreign gotcha proven true today on a live path. A long justification without a proven exception is a confession.

The report names touched files, the deletion count, `MUST KILL` flags with one line each, and skips.

## Steps

1. Spawn the reviewer with the scope and rules above.
2. Inspect its report and diff. Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty; reshape flags on our-code surprises stay actionable. Do not restore those comments: a keep survives only with proof it is about something we cannot change. Audit missed scoped lint and TypeScript suppressions; correctness or safety suppressions stay actionable `MUST KILL`s. Restore deletions only with exact exceptions and scoped proof. If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it. Revert and rerun one rejected report with the failure named; reject a second, report it open, and fail the pass.
3. Fix trivial accepted flags directly: delete a dead path, drop a parameter, use the real API. If any fix needs a shape, run `references/architect.md` once for the accepted set and stop at the sketch. Architect shapes; step 4 implements.
4. Implement the smallest root-cause fix in scope and remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. The fix-root-causes and redesign-from-first-principles principles guide intent only; neither authorizes widening the fence.
5. Constraint comments ("do not remove", "talk to X before changing"): leave keeps about things we cannot change. Offer the cheapest in-scope type, runtime, test, or CI encoding and wait for approval (unattended runs need caller pre-approval). Approved → encode then delete. Otherwise delete, report the constraint open, and sketch the out-of-scope work.
6. Report the deletion count, restored comments, reruns, architect sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.
