# Why

Recover historical constraints only when they can change the implementation. Use this reference for a suspicious workaround, regression, ownership boundary, compatibility rule, or design choice whose intent is not visible in the current code. Do not run a broad history search for routine changes.

## Steps

1. **Name the decision.** State the implementation choice that historical evidence could change. If no plausible evidence would change it, return to the calling playbook without searching.
2. **Anchor the code.** Record the relevant files, symbols, and lines. Read the current behavior first so history answers a concrete question rather than supplying a story.
3. **Read source history.** Start with `git blame -L`, `git log --follow`, and focused commit history for the target. Follow change identifiers, review discussion, or linked documents only when the commit record points there.
4. **Expand on evidence.** Search issues, design documents, team chat, observability, error tracking, or product analytics only when the target and available evidence make that source relevant. Parallelize independent searches when several sources are already necessary. Do not query every category by default.
5. **Derive implementation constraints.** Separate direct evidence from inference. Cite each direct claim and state any contradiction or unresolved gap that could affect the change.

## Evidence rules

- Code proves current mechanics, not original intent.
- A commit, review, issue, document, or comment can prove intent when it states the reason directly.
- A correlation in logs, errors, or analytics supports a hypothesis; it does not prove the decision unless another source connects them.
- Missing evidence means the constraint is unverified. Do not turn an absence into a confident story.
- Stop when additional history would not change the implementation or its verification plan.

## Return to implementation

Return a compact constraint set to the calling playbook:

- **Preserve.** Behavior or invariants backed by evidence.
- **Change.** Historical choices that no longer apply.
- **Avoid.** Rejected approaches and the reason they failed.
- **Risk.** Gaps, contradictions, or uncertain assumptions that need verification.

The calling playbook resumes design or debugging. This reference does not end the task with a standalone history report.
