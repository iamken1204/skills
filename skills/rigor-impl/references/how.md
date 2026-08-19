# How

Explore the codebase to answer "how does X work?" questions: subsystem architecture, runtime flow, placement and ownership ("where should this live", "is this the right layer"). Produce clear architectural explanations at the level of a senior engineer onboarding onto a subsystem: enough to build a working mental model, not annotated source code. Use `references/why.md` for motivation.

Two modes: **Explain** (default) and **Critique** (explain first, then independent critics).

## Explain mode

**1. Understand the question and assess complexity.** Identify the scope; if ambiguous, state your best-guess interpretation and proceed. Don't ask.

- **Simple** (a single module, a narrow "how does function X work"): one delegate explores and explains in a single pass. Go to 2b.
- **Complex** (a subsystem spanning files or services, a cross-cutting feature, an architectural overview): parallel explorers first, then a synthesizer. Go to 2a.

When in doubt, lean simple; spawn explorers later if the explainer hits a wall.

**2a. Explore (complex only).** Decompose into 2-4 parallel exploration angles, each a distinct slice (e.g. data model / request path / configuration) so explorers don't duplicate work. Spawn all explorers at once, read-only, on the fast model. Each explorer starts broad (glob and grep for key types), follows the thread from an entry point through the call chain, reads the actual code rather than guessing from file names, stops when it can describe the full path from input to output without hand-waving, and notes anything a newcomer would get wrong. Each returns structured findings: components, flow, files read, non-obvious things. Overlap is fine; the synthesizer reconciles.

**2b. Direct explain (simple only).** One read-only delegate on the judgment model explores and writes the explanation directly in the output format below.

**3. Synthesize (complex only).** One read-only delegate on the judgment model takes all explorer findings, reconciles overlaps, resolves contradictions, and writes the human-facing explanation.

**4. Present.** Present the explainer's output. Lightly edit for clarity; don't substantially rewrite.

### Output format

Adapt to the question; not every section is needed.

- **Overview.** 1-2 paragraphs: what it is, what it does, why it exists.
- **Key concepts.** The important types, services, or abstractions, briefly defined.
- **How it works.** The flow: trigger, steps, where data goes, decision points. Prose, not pseudocode. Reference specific files and functions; don't dump code blocks unless a snippet is genuinely necessary.
- **Where things live.** A brief map of the files needed to start working in this area.
- **Gotchas.** Non-obvious or surprising things, historical context, known sharp edges.

## Critique mode

Triggered when the user asks for architectural issues or improvements, not just understanding.

1. **Explain first.** Run the full explain flow. You must understand the architecture before critiquing it.
2. **Spawn critics.** One read-only critic per model family available (per the Harness mapping), all at once. Each critic gets the explanation, the relevant file paths, and the rubric below.
3. **Lead judgment.** You are a pragmatic lead, not an aggregator. Categorize findings: **Act on** (worth fixing now), **Consider** (real but unclear cost/benefit), **Noted** (valid, low priority), **Dismissed** (wrong, missing context, or style preference). Present the explanation first, the verdict below it, so someone who only wants understanding needn't wade through critique.

### Critique rubric

Review through whichever lenses apply.

- **Abstraction fit.** Does each abstraction represent a real concept or an indirection "in case"? Are boundaries where things change independently? Is business logic entangled with framework wiring? Over-abstraction is as much a problem as under-abstraction.
- **Data model.** Do the structures fit actual access patterns, or does code constantly reshape data? Are types honest about runtime reality?
- **Boundary discipline.** Validation concentrated at entry points or scattered? Errors handled at boundaries or caught and re-thrown at every layer? Could the subsystem be tested in isolation?
- **Evolution readiness.** If the most probable next requirement landed tomorrow, how much changes: one file or everything? Bolted-on or integrated? Legacy paths preserved that no one depends on? Don't penalize hypotheticals; focus on plausible trajectory.
- **Complexity vs value.** Is complexity concentrated where it's needed (core logic, tricky invariants) or in accidental places? Does every component earn its existence?
- **Consistency.** Are similar problems solved the same way as elsewhere in the codebase? Unexplained inconsistency is a maintenance burden.
