# Interrogate

Spawn one reviewer per available model family to adversarially review code changes. Each reviewer gets the same prompt and rubric; the adversarial signal comes from independence (different families' blind spots and priors), not assigned personas. Agreement across independent reviewers is high-confidence signal; lone findings are worth reading but lower confidence. A single-model harness spawns N fresh-context reviewers; independence then comes from each seeing only the artifact, never the author's conversation.

The deliverable is a synthesized verdict. Do NOT auto-apply changes.

## Steps

**1. Determine scope.** The files or diff the user points at; otherwise the full changeset against the base branch (`git diff main...HEAD`); otherwise the files the message references. Package the diff plus the surrounding context files reviewers need.

**2. State the intent.** One clear paragraph: what is this code trying to accomplish, derived from the user's message, commits, change description, and the code. Reviewers challenge whether the work achieves the intent well, not whether the intent is correct. Unsure about the intent → ask before proceeding.

**3. Spawn reviewers**, all at once, read-only, one per family. Each gets the intent, the diff, the review rubric, and the code-quality lens below.

**4. Synthesize.** Parse all findings; identify consensus (2+ independent reviewers = highest signal); deduplicate descriptions of the same issue; note explicit disagreements.

**5. Lead judgment.** You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Reviewers saw a slice; you have the goal, constraints, timeline, and which tradeoffs were already considered. Use that context aggressively. Categorize every finding:

- **Act on.** Real issues affecting correctness, security, or maintainability given the actual goals. Would block review.
- **Consider.** Legitimate, but unclear whether it outweighs the cost right now.
- **Noted.** Technically valid but not actionable now.
- **Dismissed.** Wrong, nitpicky, or missing context, with a brief reason.

Filtering principles: reviewers fill their review, so all-nits means the code is probably fine, say so. "What if someone passes null?" is only a finding if the caller can actually pass null; trace the call site. An extraction or interface suggestion is premature unless the code needs to change a second way. "I would have done it differently" is not actionable without a concrete problem. Findings that flag unmodified code or codebase-consistent patterns reveal missing context; dismiss gracefully. Don't dismiss findings just for being uncomfortable: consensus, a concrete execution path, or a gap in your own mental model deserve attention, and security or correctness findings deserve extra scrutiny even from a single reviewer. If "Act on" exceeds ~5 items you're probably not filtering hard enough. The Dismissed section is a trust mechanism, not busywork: it lets the user override your judgment.

## Output format

**Intent** (the paragraph) → **Reviewers** (one bullet each: label, family, finding count) → **Act on** → **Consider** → **Noted** → **Dismissed** (with rationale) → **Agreement map** (where reviewers agreed, diverged, and what the pattern says). For each finding: which reviewers raised it and a one-line rationale for its category.

## Review rubric

Review through whichever lenses are relevant.

- **Correctness.** Edge cases (empty, nil, boundaries, concurrent access); error handling (swallowed errors); off-by-one, coercion, overflow, encoding; races, stale closures, dangling references; idempotency (what if it runs twice, or the previous run crashed halfway); structural serialization of shared mutable state, not conventions. When you find a potential bug, trace the execution path; show the call chain that makes it nil, don't just flag "could be nil".
- **Root causes vs symptoms.** Guard clauses masking an invariant violation; retries hiding a broken contract; casts silencing a modeling error; a fix in module A that belongs in module B's contract; instructions where structure would do (could the "don't do X" comment be a type, lint, or runtime check?). Read beyond the changed files: callers, callees, types, sibling modules.
- **Structural integrity.** Validation at boundaries, not scattered; abstraction levels unmixed; coupling that makes future change harder; data structures matching access patterns; bolted-on vs integrated (would the code look like this if the requirement were known from the start?); new API without deleting the old one. Don't penalize simple code for lacking abstraction.
- **Verification.** Tests that test behavior, not implementation; a test for the bug being fixed; the full integration path exercised; checks against the real thing, not proxies (mtimes, cached state, self-reports).
- **Complexity budget.** Code that could be simpler; one-call-site abstractions; configuration for cases that don't exist; dead code; obsolete compatibility paths. Three lines of duplication beat a premature abstraction.
- **Security.** Only flag issues you can trace through the code: input to dangerous sinks without sanitization, authz gaps in new endpoints, secrets in code or logs, TOCTOU in critical paths.

## Code-quality lens

Every reviewer also applies this strict lens. Be ambitious about structure: actively search for "code judo" moves, restructurings that preserve behavior while making the implementation dramatically simpler, smaller, and more direct.

1. Look for reframings that make whole branches, helpers, modes, or layers disappear. Delete complexity rather than rearranging it.
2. Don't let a change push a file from under 1k lines to over without a very strong reason; prefer extracting first.
3. No spaghetti growth: new ad-hoc conditionals and one-off branches in unrelated flows are a design problem, not a style nit. Push logic into a dedicated helper, state machine, or module.
4. Prefer direct, boring, maintainable code over hacky or magical code. Flag thin abstractions, identity wrappers, and pass-through helpers.
5. Push on type and boundary cleanliness: question unnecessary optionality, `any`, cast-heavy code, and silent fallbacks papering over unclear invariants.
6. Keep logic in the canonical layer; reuse existing helpers over bespoke one-offs.
7. Flag unnecessary sequential orchestration and non-atomic updates when the cleaner structure is obvious.

Prioritize structural regressions and missed simplifications first, then branching complexity, then boundary and type concerns, then smaller legibility issues. A few high-conviction comments beat a long list of nits. Do not approve merely because behavior seems correct; be direct and demanding without being rude.
