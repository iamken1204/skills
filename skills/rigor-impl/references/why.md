# Why

Investigate the motivation and intent behind code: why was it built this way, what edge cases and constraints shaped it, what alternatives were rejected. Companion to `references/how.md`: how answers what the code does; why answers what forces led to its shape.

Historical context spreads across seven evidence categories: source control history, issue/ticket tracker, long-form documents, real-time team chat, infrastructure observability, error tracking, and product analytics. You cannot predict from the question which one holds the answer, so enumerate the evidence tools available in this environment (MCPs, CLIs, APIs), map each to a category, query every available category in parallel, then synthesize with explicit confidence calibration. Null results are first-class evidence about how the decision was made; report them alongside positive findings. The default is coverage, not minimalism.

## Operating posture

Work like a detective piecing together a historical case from fragmentary records. Tickets go stale, chat threads get deleted, commit messages lie, authors leave. Be ruthlessly honest about known versus inferred; the goal is not a satisfying story but surfaced evidence the user can judge.

- **Evidence before narrative.** Collect the pieces first, then see what story they support. Never recruit evidence to fit a story.
- **Cite everything.** Every claim about intent references a commit hash, change identifier, ticket ID, doc URL, chat permalink, or code comment. Uncitable claims are inference and must be labeled as such.
- **Prefer "appears to" over "because".** Hedge when evidence is indirect; reserve confident language for direct, explicit evidence. The synthesizer must not drop the hedges to sound authoritative.
- **Surface contradictions and multiple hypotheses.** When sources disagree or the evidence fits several stories, show all of them with the evidence for each.
- **Name the gaps.** A source that isn't searchable or returns nothing is documented, not papered over.
- **No shortcut by code-reading.** The code tells you what it does, rarely why it exists. "Handles the null case because it checks for null" is mechanics, not motivation.

## Steps

**1. Parse target and question.** Design rationale, tradeoff, defensive reasoning, forcing function, dead code, or broad history. If the target is vague, state your interpretation and proceed.

**2. Establish the code anchor** inline, before spawning anyone: file paths and line ranges, key symbols, the last commits touching the target (`git blame -L`, `git log --follow`, `git log --oneline -20 -- <file>`), change identifiers from merge subjects, and review descriptions or discussion available through the code host. Pass this seed to every investigator.

**3. Spawn one investigator per available category, all at once.** Source control is always available (git + host CLI); spawn it every time. For the rest, one investigator per matched tool, never one agent pooling several tools. What each category uniquely surfaces:

1. **Source control.** Implementation-time rationale captured during review: change descriptions, review threads debating alternatives, inline comments, test names encoding motivating edge cases. Most trustworthy; ties to the diff that shipped.
2. **Issue tracker.** The product or business forcing function: customer requests, compliance deadlines, parent initiatives, motivation labels.
3. **Long-form docs.** PRDs, RFCs, ADRs, postmortems: problem statements and explicit "alternatives considered" sections. Where the why is written before it becomes code.
4. **Team chat.** Real-time deliberation that never reached a doc: incident fire drills, author/reviewer Q&A, "we decided X because Y" threads.
5. **Infrastructure observability.** Monitor thresholds matching code constants, metric spikes right before a merge, incident timelines. Strongest for timeouts, retries, rate limits.
6. **Error tracking.** Stack traces through the target, issues whose first-seen/last-seen bracket the ship date, release correlations. Strongest for catch blocks and guards.
7. **Product analytics.** Usage trajectories, experiment and flag exposure, pre-ship distributions that reveal where a threshold constant came from.

Skip a category only with a written justification in Sources Consulted, and only for two reasons: no tool for it exists in this environment (flag as a gap, not a choice), or the source is provably irrelevant (a high bar; "probably irrelevant" is not it). The cost of an empty investigator is one subagent; the cost of a missed design doc is a wrong answer.

**4. Synthesize** in one delegate on the judgment model: a confidence-weighted, cited narrative with separated known/inferred sections and honest gaps.

**5. Present.** Lightly edit; never rewrite the confidence language. The epistemic framing is the product.

## Output format

- **The question.** Restated concisely.
- **The code in question.** Paths, line ranges, key symbols.
- **What we found (direct evidence).** Cited claims only, quoting or paraphrasing the source.
- **What we can reasonably infer.** Hedged claims with the inference chain spelled out ("Given A and B, likely C").
- **Competing hypotheses.** When the record supports several stories: each with evidence for and against. Skip when there's a clear answer.
- **What we don't know.** Specific gaps: "searched the tracker for 'rate limit', no ticket discusses this threshold" beats "we don't know".
- **Sources consulted.** One line per category: what was searched, what was found or "no relevant results" or "skipped: reason". The coverage map lets the user judge breadth.

If the question is a precursor to changing the code, close with a Preserve / Change / Avoid / Risk constraint set for planning the change.

## Failure modes

Confident storytelling from thin evidence. Citing the code as evidence of its own intent. Recency bias (the current shape is an accretion; trace back). Confirming the user's suggested reason instead of checking it. Skipping the gaps section. Skipping investigators by anticipation. Pooling categories into one agent.
