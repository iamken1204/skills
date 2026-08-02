---
name: review-risk
description: "Audit a branch or PR diff for bugs, breaking changes, security vulnerabilities, devex regressions, and feature-flag leaks. Use when the user asks to review a branch for correctness or security."
---

# Review Risk

Audit a checked-out branch's diff adversarially, end-to-end. Unfinished research is not a valid finding: if the client, server, or caller is in your reach, read it before reporting or clearing an issue.

## Scope

Only code **added or modified** in this diff. Pre-existing issues in code the branch didn't touch are out of scope, no matter how real.

## What counts as a finding

- **Breaking changes** — trace side effects across package/module boundaries; a small change in one place often breaks something non-obvious elsewhere.
- **Devex regressions** — changes to where secrets are read from, env var names, ports/networking, or new required setup steps that alter how developers currently run or build the code. Adding a dependency through the normal package manager doesn't count; requiring a manual out-of-band install does.
- **Feature-flag leaks** — anything meant to sit behind a flag or internal-only check escaping that gate. Check every path that reaches the new code, not just the obvious one.
- **Security vulnerabilities** and **correctness bugs** in the changed code.

## Judgment calls

- **Intended breakage**: skip reporting a high-risk finding that is the branch's stated intent (removing a flag, a safeguard, a feature) when the blast radius is well-contained — unless the author seems unaware of the full implications, or the change reads as reckless or malicious regardless of stated intent.
- **Severity honesty**: report only the severity you'd stand behind after tracing the issue end-to-end. A miscalibrated "High" costs more trust than a missed low-priority finding.

## Before finishing

If there's a PR for this branch and you have medium-or-higher findings, check its discussion via `gh`/`glab` for BugBot or human comments — but only *after* your own independent pass, so your first read stays unbiased. Fold in anything valid they caught that you didn't, and credit overlaps you both found.

Report each finding with file:line evidence — where it is, not just what's wrong.
