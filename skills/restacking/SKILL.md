---
name: restacking
description: "Rebuilds an over-fragmented branch from its latest tree into logically scoped commits with titles and bodies. Use when the user asks to split, regroup, restack, or rewrite all commits, including 「commit 太多」、「拆掉 commits」 or 「重新整理 commits」."
---

# Restacking

Treat the latest repository state as the source of truth and the existing commits as raw material. Replace the requested history range with a reviewable sequence while preserving the final tree exactly.

## Establish the range

1. Inspect the working tree, current branch, upstream, recent graph, and candidate base refs. Read the repository's commit conventions.
2. Resolve the base from the user's target, the PR base, or the merge-base with the remote default branch, in that order. Ask if the choice remains ambiguous; commit count is not evidence of a base.
3. A direct request to tear down, rebuild, or rewrite the commits authorizes the local history rewrite. A force-push is separate shared-state approval: leave it to the user unless they explicitly request it.
4. Record the original HEAD SHA and the chosen base SHA before moving HEAD.

## Freeze the latest state

Review every modified and untracked file. Exclude secrets, local artifacts, and generated files that the repository does not track.

Stage the intended repository state and record its tree with `git write-tree`. This tree hash is the invariant for the rebuild. Reset the branch to the base with a mixed reset so the files stay at their latest contents while the old commits disappear from the branch.

If the request applies only to committed changes, preserve unrelated worktree changes separately and restore them after rebuilding the committed range.

## Design the stack

Read the complete base-to-final diff, then group it by reason for change:

- One commit carries one coherent behavior or responsibility, including the tests, types, fixtures, and documentation required by that behavior.
- Independent behavior, mechanical refactors, migrations, and generated output get separate commits when each can stand on its own.
- Shared prerequisites land before their consumers. Every intermediate tree should remain understandable and, where practical, testable.
- File count does not define granularity. Split a file by hunks when it contains more than one reason for change; keep several files together when they implement one reason.

Write the proposed stack before committing. Each entry names its scope, purpose, owned paths or hunks, and dependency on earlier entries. Start rebuilding once every changed hunk belongs to exactly one entry.

## Write every commit

Load the `unslop` skill before drafting commit messages.

Use this title shape:

```text
<actual-scope>: <plain-language change>
```

Derive the scope from the product surface, subsystem, package, or owned module, such as `api-executions` or `ui-capture`. Do not use conventional prefixes such as `feat`, `fix`, `chore`, `refactor`, `docs`, or `test`. Match the repository's capitalization and wording after the scope.

Every commit has a non-empty body. State why the change exists and any implementation choice or constraint a reviewer needs; do not repeat the title. Use real paragraph breaks through separate `-m` arguments or a commit-message file, never literal `\n` text.

For each stack entry:

1. Stage only its paths or hunks.
2. Inspect `git diff --cached` and confirm it expresses one reason for change with no borrowed or missing pieces.
3. Run the narrowest useful check when the commit can be tested independently.
4. Commit with its scoped title and body.

Do not leave fixup, WIP, or message-only cleanup commits in the finished stack.

## Prove the rebuild

After the last commit:

1. Compare `HEAD^{tree}` with the recorded final tree hash. A mismatch means the rebuild changed the latest state; stop and account for the difference.
2. Inspect the base-to-HEAD diff and working tree. Every intended change must be committed exactly once, while excluded local files remain untouched.
3. Read the rebuilt log in full format. Every commit needs an actual scope, a specific title, and a non-empty body written under `unslop`.
4. Run the relevant final checks for the combined tree.

Report the base and original HEAD, list the rebuilt commits in order, name the checks run, and state that nothing was pushed.
