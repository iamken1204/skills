---
name: restacking
description: "Rebuilds a branch's history from its latest tree into logically scoped commits with titles and bodies. Use when the user asks to split, regroup, restack, or rewrite all commits, including 「commit 太多」、「拆掉 commits」 or 「重新整理 commits」."
---

# Restacking

The latest tree is the source of truth and the existing commits are raw material: replace the requested range with a reviewable sequence that ends at exactly the same tree.

## Establish the range

1. Inspect the working tree, current branch, upstream, recent graph, and candidate base refs. Read the repository's commit conventions from CONTRIBUTING, commitlint config, and the recent log.
2. Resolve the base from the user's target, the PR base, or the merge-base with the remote default branch, in that order. Ask if the choice remains ambiguous; commit count is not evidence of a base.
3. A direct request to tear down, rebuild, or rewrite the commits authorizes the local history rewrite. A force-push is separate shared-state approval: leave it to the user unless they explicitly request it.

## Freeze the latest state

1. If the request covers only committed changes, `git stash -u` everything else first.
2. Otherwise review every modified and untracked file, exclude secrets, local artifacts, and untracked generated files, stage the rest, and commit it as a WIP.
3. `git branch restack-backup`. Its tree is the invariant for the rebuild, and `git reset --hard restack-backup` recovers from any misstep.
4. `git reset --mixed <base>`. The files keep their latest contents while the old commits leave the branch.

## Design the stack

Read the complete base-to-final diff, then group it by reason for change:

- One commit carries one coherent behavior or responsibility, including the tests, types, fixtures, and documentation it requires.
- Independent behavior, mechanical refactors, migrations, and generated output get separate commits when each can stand on its own.
- Shared prerequisites land before their consumers. Every intermediate tree should remain understandable and, where practical, testable.
- File count does not define granularity. Split a file by hunks when it contains more than one reason for change; keep several files together when they implement one reason.

Show the user the proposed stack and proceed; the request already authorized the rewrite. Each entry names its scope, purpose, owned paths or hunks, and dependency on earlier entries. Start rebuilding once every changed hunk belongs to exactly one entry.

## Write every commit

Follow the repository's own title and body format when it has one. Without one, shape titles as `<scope>: <plain-language change>`, where the scope names the product surface, subsystem, or package, such as `api-executions` or `ui-capture`, never a type prefix such as `feat` or `fix`.

The body states why the change exists and any implementation choice or constraint a reviewer needs, without repeating the title; skip it only when a reviewer needs no reason, such as a typo fix. Write as a maintainer would speak to a colleague: lead with the point, active voice and concrete verbs, one claim per sentence, no throat-clearing, hype, hedging, filler, or closing summaries. Use real paragraph breaks through separate `-m` arguments or a message file, never literal `\n` text.

For each stack entry:

1. Stage only its paths or hunks. For hunks, `git apply --cached` a trimmed patch; `git add -p` needs a terminal.
2. Confirm `git diff --cached` expresses one reason for change with no borrowed or missing pieces.
3. Run the narrowest useful check when the commit can be tested independently.
4. Commit.

Do not leave fixup, WIP, or message-only cleanup commits in the finished stack.

## Prove the rebuild

1. `git diff restack-backup HEAD` must be empty and `git status` must show only the excluded files. Anything else means the rebuild changed the latest state; stop and account for it.
2. Read the rebuilt log in full format and check every message against the rules above.
3. Run the relevant final checks for the combined tree.
4. `git stash pop` if you stashed.

Report the base, the rebuilt commits in order, the checks run, that `restack-backup` still holds the old history, and that nothing was pushed.
