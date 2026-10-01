---
name: caddie
description: Carry a task through the standard implementation round in one go. Understand the brief, raise questions or proceed, open a worktree, implement with fairway, review with review-risk and review-shape, fix with minimal-impl, commit with a message cleaned by unslop. Use when the user hands over a plan, a description, or a research question that should end in a commit without further prompting.
argument-hint: <what to build: a plan path, a description, or a question to research then implement>
disable-model-invocation: true
---

# Caddie

Carry a brief from reading to commit. You hand over the right skill at each step; this skill adds no rules of its own. Every rule about how to write code, review, or phrase prose lives in the skill it names.

Sibling skills are invoked through the harness's skill tool. If the harness has none, read `../<name>/SKILL.md` and follow it.

## 1. Understand

`$ARGUMENTS` is the brief. It may be a path to a plan, a description of the change, or a question to research first. Do whatever it takes to know what you are building:

- A path: read it in full, plus whatever it links to and the code it touches.
- A description: read the code it touches and the nearby conventions.
- A research question: investigate until you can state the design in a few lines. Write that design down before step 2; it is the plan from here on.

Then decide:

- **Questions.** Anything that would change the implementation if answered differently: an ambiguous requirement, a conflict with existing code, a missing decision, a step you believe is wrong. List them, one line each, and stop. Do not open a worktree. Do not start coding.
- **No questions.** Say so in one line and continue. Do not ask whether to proceed.

Questions of taste you can settle yourself are not questions. Facts you can check by reading or running code are not questions.

## 2. Worktree

Use the harness's worktree tool if it has one. Otherwise:

```sh
git worktree add -b <branch> ../<repo>-<branch> <base>
```

Branch name comes from the plan's filename or the brief's subject. Base is the current branch. Everything after this step runs inside the worktree.

## 3. Implement

Invoke `fairway` with the plan as its brief. Finish the whole plan, not the easy parts. Run the project's existing checks before moving on.

## 4. Review

Invoke `review-risk` and `review-shape` on the worktree's diff against the base. Run them in parallel where the harness allows. Collect findings from both.

## 5. Fix

For each finding you accept, invoke `minimal-impl` to fix it. Re-run the project's checks.

A finding you reject stays in the report with a one-line reason. A high-severity finding you cannot fix stops the round. Report it and leave the worktree uncommitted.

## 6. Commit

Write the commit message, then invoke `unslop` on it. Title under 60 characters, body that says why. Commit. Do not push.

One commit per brief by default. Split only when the brief itself names independent deliverables.

## Reply

Four lines, then the findings:

- worktree path and branch
- commit hash and title
- checks run and their result
- findings accepted, rejected, and open, each one line

A round that stopped at step 1 or step 5 says which step and why.
