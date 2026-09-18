# Decision trail

Keep one canonical log. Other playbooks route their audit trail here instead of inventing one. Reference this file and don't restate the columns.

## The format

A single TSV file, one row per decision. Cells stay single-line. Evidence is a pointer, not prose.

Columns:

- **ts.** ISO8601 timestamp.
- **phase.** The phase or workstream.
- **decision.** What was chosen or done, one line.
- **why.** The reason in plain words. If a principle drove it, say it plainly, not as a jargon tag.
- **evidence.** A link or path that proves it: commit SHA, change identifier, `file:line`, artifact, trace, or screenshot path. Never a paragraph.
- **result.** The outcome or predicate state: `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, `open`.

Example rows (illustration only):

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components	wanted the size before starting a long run	commit 3a9f1c2	found 5 things to sort out first
2026-05-24T11:15:00Z	widget	moved the widget styles over unchanged	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work, its screenshots were blank	checked the real files instead of trusting its summary	scratch output discarded	reverted, tightened the next brief
```

## Logging a row

Write each entry the way you'd tell a teammate what you did. Plain words, concrete actions (unslop applies to log text too). Row hygiene: strip stray tabs and newlines from cells, and prefix any cell starting with `=`, `+`, `-`, or `@` with a single quote so a spreadsheet doesn't execute it as a formula.

Log decision points and checkpoints, not every action: a fork chosen, a unit completed with its verification result, a pivot or revert with its trigger, a blocker surfaced, a gate fixed. For loop runs, one row per iteration. Skip the trivial.

## Where it lives

By default the log is a working artifact, not committed: `decisions.tsv` in the work dir, or `.audit/<task-slug>.tsv` when several efforts run at once, kept out of git. Commit it only when the work is ambitious enough that a reviewer needs the trail to trust the result.

## Rules

- One row is one decision or checkpoint.
- Append-only. A wrong call gets a new row that supersedes it; never edit or delete history.
- Prefer evidence produced by committed scripts over hand-made one-offs (the encode-lessons-in-structure principle).

## Audit the log before handing back

Check the log told the truth. Where the harness exposes this run's transcript or session log, walk the log against what actually happened; where it doesn't, audit against the git history and the artifacts on disk, and say which you used.

- Every row maps to a real action. Cut invented or aspirational entries.
- Each row's evidence resolves and shows what the row claims.
- A fork, pivot, or abandoned approach that shaped the work but isn't logged is a gap. Add it.
- Drop padding.

Fix the log, not the story. If the work diverged from what a row claims, the row is wrong.

## Cross-model review of the trail

Before handing back, spawn a reviewer on a different model family (or a fresh context that sees only the trail and artifacts, never your conversation). Self-review is not a substitute. It reads the trail and the run's record, then flags what the user should scrutinize: decisions with weak or absent evidence, verification claimed without proof, choices that look risky in hindsight, gaps a casual skim would miss.

Every reply for a run that produced a trail ends with an "Attention" section: the reviewer's identity on its own line (`reviewed by <model/context>`), then each flag pointing at specific rows. "No flags" is a valid value. The reviewer line is not optional.

## Reviewing the trail

Read top to bottom, follow the evidence pointers, spot-check.
