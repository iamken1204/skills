# Agent Skills

Reusable skills for AI coding agents, installable with the
[`skills`](https://skills.sh) CLI.

## Install

```sh
npx skills add iamken1204/skills
```

List the available skills without installing them:

```sh
npx skills add iamken1204/skills --list
```

Install one skill non-interactively:

```sh
npx skills add iamken1204/skills --skill minimal-impl --yes
```

## Skills

- `fairway` — implement happy-path-first: deep modules, type-driven invariants, evidence-gated complexity.
- `minimal-impl` — ship the shortest working implementation.
- `nomen` — create names with multiple meaningful layers.
- `orchestrate` — split architecture and verification from delegated implementation.
- `probing` — explain how code works, recover why it exists, and critique its architecture.
- `review-risk` — audit a diff for bugs, breaking changes, and security vulnerabilities.
- `review-shape` — audit a diff for maintainability: code judo, sprawl, layering leaks.
- `rigor-impl` — plan, implement, and verify changes with task-specific engineering playbooks.
- `unsaid` — write strategic-ambiguity copy: definite sentences, referents left unsaid.
- `unslop` — cure AI-sounding prose: answer first, plain verbs, no hype, no bullet walls.
