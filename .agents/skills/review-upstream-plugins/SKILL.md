---
name: review-upstream-plugins
description: Fetch cursor/plugins, read what changed in thermos and pstack since the local checkout, and report which changes the skills derived from them should adopt.
disable-model-invocation: true
metadata:
  internal: true
---

# Review upstream plugins

Several skills in this repository were distilled from two plugins in `cursor/plugins`. The local checkout of that repository marks the last reviewed commit: everything between its `HEAD` and `origin/main` is unreviewed. This skill reviews that range, reports, and then advances the checkout.

The checkout is `../cursor-plugins` relative to this repository's root, unless `$ARGUMENTS` names another path.

| Upstream | Derived skills |
| --- | --- |
| `thermos/` | `review-risk`, `review-shape` |
| `pstack/` | `caddie` and the skills it invokes (`fairway`, `minimal-impl`, `unslop`), `create-verification-skill`, `maintain-verification-skill` |

## 1. Fetch and fix the range

In the checkout, run `git fetch`, then record `git rev-parse origin/main` as the target. Every later command uses `HEAD..<target>`, so a second fetch cannot move the range under you.

Report the commit count of the range. If `HEAD` is not an ancestor of the target, stop and report the divergence.

## 2. Find the relevant commits

```sh
git log --stat --format='=== %h %ad %s' --date=short HEAD..<target> -- thermos pstack
```

Report the count for each directory separately. A directory with no commits is finished: say so and skip it in step 3.

## 3. Read every change against its derived skills

For each relevant commit, read the full commit message (`git log -1 --format=%B`), then the diff of each skill, playbook, principle, and agent file it touches. The commit message states what the author kept and what they cut; the diff alone does not.

Read the current text of each derived skill, and `git log --oneline` of this repository for earlier commits that folded upstream changes in. A rule upstream still carries from before the range was either taken or declined then; it is not a finding now.

Sort each change into one of four kinds:

- **New rule.** Behavior upstream did not ask for before. Compare it to the derived skill and say whether the skill already covers it, and where.
- **Compression.** The same rules in fewer words. Not a finding, unless the commit message cites evidence that the shorter text performs better.
- **Removal.** A rule upstream dropped. Check whether a derived skill still carries it, and report it as a question.
- **Host-specific.** Model routing, Cursor tooling, harness adapters, version bumps, and skills with no derived counterpart. Name the group in one line.

The step is done when every file in the step 2 stat output belongs to one of the four kinds.

## 4. Report

Reply in the user's language:

- the range: commit count, old `HEAD`, target
- the relevant commits, one line each
- per derived skill: the changes worth adopting, each with the upstream file, the sentence it would add or change, and the behavior it would change. Say "nothing to adopt" when that is the result.
- changes you considered and recommend against, each with a one-line reason

Do not edit a derived skill in this round. Adoption is a separate request.

## 5. Advance the checkout

After the report, run `git merge --ff-only <target>` in the checkout and confirm `HEAD` equals the target. Untracked files stay as they are. If the working tree has local modifications that block the merge, report them and leave the checkout where it is.
