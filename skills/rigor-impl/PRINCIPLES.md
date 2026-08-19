# Principles

The full rule for each principle the SKILL.md index names. Read a principle's section in full before citing it.

## Laziness Protocol

Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading.

Writing code is cheap for you, which makes over-engineering easy. Counter it by borrowing a human maintainer's fatigue. Aim for the most result with the least code and complexity.

- **Prefer deletion.** When asked to refactor or improve, look for removals before additions.
- **Maintain a flat call hierarchy.** Avoid deep call chains. A rich interface that hides substantial work is not a deep call chain. If answering a question requires tracing through more than 3 files or layers, flatten it.
- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- **Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat "elegant" boilerplate.
- **Question the threading.** If a task asks you to pass a new signal through types, schemas, pipelines, or similar layers, stop and look for a more direct path.
- **Sweat the small leaks.** Remove tiny pass-throughs, representation leaks, and duplicated choices before they spread. Small leaks compound into permanent coordination costs.

**Prime directive:** If a human developer would find the code exhausting to maintain, it is a bad solution. Be lazy. Stay simple.

## Foundational Thinking

Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share.

**Structural decisions** protect option value. **Code-level decisions** protect simplicity. Over-engineering is often a premature decision that closes doors. The right foundational data structure keeps doors open.

**Data structures first.** Get the data shape right before writing logic. The right shape makes downstream code obvious. Define core types early, trace every access pattern, and choose structures that match the dominant paths. A data-structure change late is a rewrite. Early, it is often a one-line diff.

At code level, DRY the structure, not every line. Types and data models should converge. Three similar statements still beat a premature abstraction. Prefer explicit over clever. Test behavior and edge cases, not line counts.

**Concurrency corollary.** Before sharing state between actors, ask "what happens if another actor modifies this concurrently?" If not "nothing", isolate.

**Scaffold first.** If something helps every later phase, do it first. CI, linting, test infrastructure, and shared types are scaffold. Sequence for option value: setup before features, tests before fixes. Keep commits small and single-purpose.

Each increment should land a coherent abstraction or deepen one that exists. Do not spread a new capability across callers as special-case coordination.

Subtraction comes before scaffolding: remove dead weight first, then lay foundations.

## Redesign from First Principles

Apply when integrating a new requirement into an existing design.

When integrating a change, don't bolt it onto the existing design. Redesign as if the requirement had been there from the start. The result should look like what we would have built if we'd known on day one.

- Read all affected files and understand the current design holistically
- Ask: "if we were writing this from scratch with this new requirement, what would we build?"
- Propagate the change through every reference: types, docs, examples, rationale sections
- Think about the redesign holistically, then deliver it incrementally

## Subtract Before You Add

Apply when sequencing an addition, refactor, or rewrite.

When evolving a system, remove complexity first, then build. Deletion gives you a simpler base, which makes the next addition smaller and less brittle. Adding to a complex system compounds complexity; removing first cuts the surface area, reveals the essential structure, and usually makes the next design obvious.

- Sequence removal before construction
- Cut before you polish (get to the minimum before investing in quality)
- Design for observed usage, not speculative edge cases
- No speculative validators, parsers, or guards beyond what the spec demands
- Out-of-spec features drag validators behind them: persistence, retry-on-startup, and schema migration each need guards to defend their inputs
- Simplify prompts (remove redundant instructions, excessive templates)
- When a reference has no novel content, delete it rather than leaving a stub

Make simplification a continual investment. Leave the design slightly simpler and more capable behind the same or smaller surface than you found it.

## Minimize Reader Load

Apply when reviewing or shaping code that's hard to trace.

Maintainability is the work a reader must do to understand code. Track two axes:
1. **Layers to trace.** How many indirections sit between the question and the answer.
2. **State to hold.** How much hidden or mutable context the reader must keep in their head.

Code is read far more than it is written. LOC and cyclomatic complexity are proxies; reader load is the thing that matters. The axes are independent: a flat file with 50 globals is as hard as a 6-layer adapter stack. This is the human analog of [Guard the Context Window](#guard-the-context-window): working memory is finite for readers too.

- **Collapse layers** that do not earn their keep: wrappers with one caller, adapters with no second implementation, indirection for a future that never came. Inline them.
- **Make adjacent layers change the abstraction.** A layer that repeats the same methods and arguments adds reader load without compression.
- **Demand interface compression.** A broad interface that hides little makes readers learn both the surface and the implementation. Prefer boundaries that hide meaningful decisions.
- **Shrink state scope:** prefer pure functions, locals over fields, fields over module state, module state over globals. Derive instead of sync.
- **Name the invariant at the boundary,** not in every consumer, so the reader learns it once.
- Before adding a layer or state, ask: does this reduce reader load somewhere else by at least as much?

**The test:** Can a new reader answer "where does X come from?" and "what can change X?" in under 30 seconds? If not, cut layers or cut state.

## Outcome-Oriented Execution

Apply during planned rewrites and migrations with explicit phase boundaries.

Optimize for the intended, verifiable end state rather than preserving smooth intermediate states. Keeping every intermediate step fully stable often creates temporary compatibility code that becomes long-lived debt.

- Prioritize end-state integrity over transitional stability
- Intermediate breakage is acceptable when it is planned, scoped, and reversible
- Declare where temporary breakage is acceptable
- Keep high-signal checks for actively touched areas while migrating
- Require full static and runtime verification at plan completion

## Experience First

Apply when product, UX, or feature-scope tradeoffs come up.

The product is the experience. Every technical decision either helps or hurts it. When implementation convenience conflicts with user delight, choose delight.

- Say no to 1,000 things (every feature, control, and option must earn its place)
- Ship less, ship better (a polished experience with three features beats a rough one with ten)
- Prototype before committing (design decisions are cheaper in throwaway HTML than production code)
- Sweat the details (transitions, alignment, spacing, feedback, error states)
- Tighten the core loop (every feature should serve the central workflow or get out of the way)

The user is whoever consumes the work. For a UI that is the end user. For a library or an internal API it is the colleague who imports it. The engineer who maintains the code next is a user too. Weigh their experience the same way, and explain impact from their seat.

Foundations should serve the experience, not the other way around. Foundational Thinking governs the *sequence* of work; this principle governs the *target*.

## Exhaust the Design Space

Apply when facing a novel interaction or architectural decision with no precedent in the codebase.

When the right answer is not obvious, build 2-3 competing prototypes or sketches. Compare them side by side. Only then commit. Design it twice is this rule by another name. A second flavor of the first shape does not count.

Applies to novel UI interactions, architectural choices with multiple viable approaches, and product decisions where experience depends on feel. Does not apply to mechanical implementation with an established pattern, bug fixes with a clear target state, or changes where constraints dictate one approach.

## Build the Lever

Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks.

When the work isn't trivial, build the tool that does it instead of doing it by hand. Two payoffs. Throughput: a codemod, generator, or script does the work the same way every time and reruns for free. Confidence: the tool is one artifact a reviewer can read and rerun to check the work. A deterministic script turns "trust me" into "run this".

- Do the first unit by hand to learn the recipe, then build the tool. Prove it by rerunning on that unit and diffing against your hand-done version. Make the lever safe to rerun; a reviewer will.
- Codemod or script for edits, generator for repetitive files, a dump-to-sqlite query for analysis, a rerunnable check for verification.
- A deterministic lever beats fan-out. If the tool can process every unit in one pass, run it yourself; don't fan out delegates to hand-apply what a script can do.
- When you fan work out to subagents, write the lever as a doc they all read: the recipe, the verification contract, and the do-not-touch fences in one artifact, kept outside the delegates' write scope so they can't quietly edit the contract.
- Applying this principle produces a file. If you cited it and there is no codemod, script, generator, or delegate doc in the diff, you didn't apply it.
- Commit the lever when the work outlives the session.

**Balance:** the bar is triviality, not repetition. A one-off still earns a lever when the lever is what makes the work checkable. Per the [Laziness Protocol](#laziness-protocol), build the smallest script that does or proves the job, never a framework. Distinct from [Encode Lessons in Structure](#encode-lessons-in-structure), which makes a recurring instruction a durable guardrail; this is throughput and reviewability on the work in front of you.

## Model the Domain

Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files.

Encode the real domain in a data structure instead of scattering it across conditionals. Scattered booleans, repeated shape assumptions, and branching spread across files are accidental complexity. A structure that matches the domain makes invalid states unrepresentable and deletes branches. Choosing it at write time is cheap; recovering it later reads as a refactor and gets deferred.

Reach for structures like these:

- A state machine instead of scattered booleans, phases, or lifecycle checks.
- A typed object/model instead of loose parameters or repeated shape assumptions.
- A map, registry, lookup table, or discriminated union instead of branching spread across files.
- A reducer or command/event model instead of ad hoc state mutations.
- A module organized around one body of domain knowledge instead of a load/validate/transform/save sequence. Execution order is not ownership.
- A small module boundary that gathers repeated behavior, ownership, or invariants.
- A queue, cache, index, graph/tree, or normalized collection where the access pattern calls for it.
- Any other structure that fits. When none fits, work out what the code must never allow and how the data gets read, then find the structure that encodes exactly that.

Do not force an abstraction. Prefer boring code if the current shape is already clear, local, and unlikely to grow. Be skeptical of an abstraction that adds indirection without removing branches, duplicated rules, invalid states, or lifecycle risk.

The tell that you skipped this is a new feature that grows an existing if/else chain by one more branch, or a second boolean that must stay in sync with the first. Temporal decomposition is another tell: phase-named modules repeat the same domain rules across steps.

## Boundary Discipline

Apply when wiring validation, error handling, or framework adapters.

Place validation, type narrowing, and error handling at system boundaries. Trust internal code unconditionally. Business logic lives in pure functions; the shell is thin and mechanical. Scattered validation is noisy, redundant, and gives a false sense of safety.

- **At boundaries** (CLI args, config files, external APIs, network protocols): validate, return errors, handle defensively.
- **Inside the system:** typed data, error propagation, no re-validation. Trust the types.
- **Across the boundary:** expose domain concepts, not the boundary's private representation. Keep general-purpose mechanism inside and special-purpose policy at the edge.

Applications: validate config at parse time, not inside business logic. Parse raw data into domain types at the boundary. Do not re-export transport, storage, framework, or wire types through the public surface. No redundant nil checks deep in call chains the boundary already validated. Business logic in pure functions with no framework dependencies.

**The tests:** "Is this data crossing a system boundary right now?" If not, validation is redundant. "Can this be a pure function that the shell just calls?" If yes, extract it.

## Type System Discipline

Apply when designing types, reviewing a function signature, or writing code in any statically-typed language.

The type checker is a proof assistant. Use it to eliminate impossible states, mismatched primitives, and unhandled variants at compile time. Prefer defining errors and special cases out of existence over proliferating handlers.

- **Make illegal states unrepresentable.** Model variants as sum types (discriminated unions, enums with payloads, sealed classes, ADTs), not bags of optional fields where contradictory combinations compile. `{ completed: boolean; completedAt?: Date }` admits `completed: true; completedAt: undefined`; derive the boolean from one source or model the variants explicitly. If a bug forces "wait, can this combination actually happen?", the type is too loose.
- **Types are constructions, not restrictions.** Build the type up from the values you want instead of carving them out of a looser type with checks. A non-empty list is a head plus a rest, not a list with a length check. A valid time range is a start plus a duration, not two timestamps you must keep ordered.
- **Brand semantic primitives.** `UserId` and `OrderId` are strings underneath but should not be interchangeable. Validate once at creation, trust the type downstream.
- **External data is untyped until parsed.** RPC payloads, JSON, IPC messages, CLI args, config, env vars, database rows: a parse function at every boundary turns unstructured input into the typed model. See [Boundary Discipline](#boundary-discipline) for where validation lives.
- **Don't lie to the type system.** Casts, unsafe coercions, and assertion functions that bypass the compiler are runtime crashes waiting to happen. If the compiler can't prove a fact, prove it (validate, narrow, refine) or accept that the cast is a hazard.
- **Exhaustive matching is the compiler's job.** A new variant added without handling must fail compilation; use the idiom your language provides.
- **Derive types from authoritative schemas.** When a protobuf, OpenAPI spec, GraphQL schema, or migration defines a shape, derive from it instead of hand-rolling a parallel type. Manual duplication drifts.
- **Strengthen a type only where partiality appears.** A runtime assertion or "this should never happen" throw marks the place a type is too weak; push that check up into the type, then stop. Prefer total functions: `sum` of an empty list is 0, so it takes the plain list; `head` has no answer, so it demands the non-empty one. Extra precision beyond totality costs reuse and buys no safety.

**The tests:** Can you write a comment explaining when a combination of fields is valid? Split it into a sum type. Do two arguments share a primitive type but mean different things? Brand them. Where did this `any`/`as`/`assertNotNull` come from? Validate at the boundary instead. Will the compiler tell the next agent where to add a case for a new variant? If no, the match isn't exhaustive.

## Make Operations Idempotent

Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries.

Design operations so they converge to the correct state regardless of how many times they run or where they start from. Every state-mutating operation should answer: what happens if this runs twice? What happens if the previous run crashed halfway?

- Convergent startup: scan for existing state, clean stale artifacts, adopt live sessions
- Content-based cleanup: compare by content equivalence, not creation order
- Self-healing locks: PID-based stale lock detection
- Idempotent scheduling: failed work respawns cleanly, fresh input regenerated after each cycle

If any answer is "it depends on what state was left behind", the operation needs a reconciliation step.

## Migrate Callers Then Delete Legacy APIs

Apply when introducing a new internal API while old callers still exist.

Migrate callers and remove the old API in the same refactor wave instead of preserving compatibility layers.

- Do not keep legacy API paths alive only because internal callers still exist
- Inventory callers, migrate them, and delete the old API immediately
- Treat temporary adapters as exceptional and time-boxed, not default architecture
- Update tests to assert the new contract; delete tests that only protect pre-refactor implementation details

Applies when no external users depend on backward compatibility and the project can absorb coordinated breaking changes. Keeping both APIs creates dual-path complexity and makes the codebase feel append-only.

## Separate Before Serializing Shared State

Apply when concurrent actors might write to the same file, branch, key, or state object.

First ask whether the actors truly need the same mutable object. If not, eliminate the sharing. When sharing is real, enforce serialization structurally: lockfiles, sequential phases, exclusive ownership. Instructions and conventions are not concurrency control; telling agents to "take turns" does not work.

1. **Identify shared mutable state** (files both read and write, branches both push to, APIs both define and consume).
2. **Default: eliminate the shared write target.** Give each actor its own owned file, key, branch, or state directory, and merge only at the read boundary. Two workers writing their own field into one `state.json` is still shared mutation; two separate state files are not.
3. **Only when one shared write target is a real invariant, serialize structurally** (lockfiles, sequential phases, single-writer actor, atomic compare-and-swap). Treat "we need a lock" as a design smell to check, not the default answer.

## Prove It Works

Apply after completing a task, before declaring done.

Verify every task output by checking the real thing directly. Do not infer from proxies, self-reports, or "it compiles". Unverified work has unknown correctness, and acting on a wrong inference costs far more than checking the source.

- Check process liveness directly, not through derived state
- Read the actual value, not a cached representation
- When verification fails, suspect the observation method before the system

Code and features: build it (necessary, not sufficient), run it and exercise the actual feature path, check the full chain from input to output, and test integrations end to end.

Delegation: trust artifacts, not self-reports. Inspect the actual output (git diff, file contents, runtime behavior), not the delegate's summary. Agents report what they intended, not always what happened.

**Script the check when you can.** The strongest proof is a deterministic script that re-runs the same comparison, not a one-time eyeball. Keep its output as an artifact a reviewer can re-run. Commit it only for large or complex work where the trail must be auditable later (see `references/decision-trail.md`); most work needs it visible, not committed.

## Fix Root Causes

Apply when debugging.

Do not paper over symptoms. Trace every problem to its root cause and fix it there. Symptom fixes accumulate; each workaround makes the system harder to reason about, and the real bug remains.

- Reproduce first (if you can't reproduce it, you can't verify your fix)
- Ask "why" until you hit the root cause
- Resist the urge to add guards (a nil check that silences a crash is a symptom fix)
- If a workaround needs a paragraph-long comment to justify it, the code is wrong: fix the code, not the comment
- Check for the pattern, not just the instance (grep for the same pattern, fix all instances)
- When stuck, instrument. Don't guess.

**Restart bugs: suspect state before code.** Code doesn't change between runs; state does. When something "fails after restart", suspect stale persistent state first: config files, caches, lock files, serialized state. If clearing a state file restores behavior, prioritize state validation as the fix.

## Sequence Verifiable Units

Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you order commits.

Order work as a sequence of small units, each ending in a state you can check, and don't advance until the current one is green. A break caught at the unit that caused it is cheap to localize; a break caught after a batch is buried, and you have already built on a broken base.

**Execution.** In a sweep, migration, or run of similar edits, verify each change before starting the next. Never batch the edits and verify once at the end. Each unit is a before/after bracket: known-good state, one change, run the check, proceed. Rebase onto clean trunk first so every check measures against the real baseline.

**Delivery.** Order commits so they prove the work. The canonical shape is the failing test first, then the fix on top: red, then green, so a reviewer sees both the problem and the proof. Other story orders: a subtraction before the reshape, a baseline capture before the treatment, the scaffold before the feature. Each commit is verifiable on its own and the sequence reads as an argument.

The sequencing complement to [Prove It Works](#prove-it-works), which keeps each check real, and [Build the Lever](#build-the-lever), which makes the per-unit check cheap.

## Guard the Context Window

Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning.

The context window is finite and non-renewable within a session. Every token that enters should earn its place. Overflow degrades reasoning, creates compression artifacts, and halts progress.

- **Isolate large payloads.** Route verbose outputs, screenshots, and large documents to subagents. The main context gets summaries, not raw data.
- **Don't read what you won't use.** Read selectively based on relevance.
- **Keep frequently used content inline.** Templates used on every invocation belong in the skill file, not in separate files that cost a read each time.
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.

## Never Block on the Human

Apply when tempted to ask "should I do X?" on reversible work.

The human supervises asynchronously. Stay unblocked: make reasonable decisions, proceed, and let the human course-correct after the fact. Code is cheap; waiting is expensive. Every permission pause makes the human the bottleneck, and a wrong reversible decision usually costs less than blocking.

- **Proceed, then present.** Do the work, show the result, explain why.
- **Reserve questions for genuine ambiguity** you truly cannot infer from context.
- **Make the system self-healing.** Notice a problem, log it, fix it in the next round.
- **Supervision is async.** Design workflows for review-after-the-fact.

Boundaries: irreversible actions (force-push, delete production data, send external messages) still require confirmation. Product direction comes from the human; execution should not block.

## Encode Lessons in Structure

Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction.

Encode recurring fixes in mechanisms (tools, code, metadata, automation) instead of textual instructions. Textual instructions require the reader to notice, remember, and comply; structural mechanisms enforce the rule without cooperation.

When you catch yourself writing the same instruction a second time:
1. Ask: can this be a lint rule, a metadata flag, a runtime check, or a script?
2. If yes, encode it and delete the instruction.
3. If no (genuinely requires judgment), make the instruction more prominent and add an example of the failure mode.

**Pick the strongest rung.** When more than one mechanism would work, choose the strongest available: an unrepresentable state that cannot compile, then a lint or banned API that fails CI, then a canonical helper, then a runtime check. Agents copy whatever the surrounding code already does, and a weaker guard becomes the next template.

**Corollary:** don't paper over symptoms. If the fix is structural, only use the structural fix. The instruction IS the symptom.

**Feedback loop:** capture every correction and decide if it's a one-off or a pattern. Route to the right layer: one-off → note; recurring fix → skill or lint rule; systemic issue → principle. Close the loop: apply now or create a concrete todo. Anti-patterns: acknowledging without recording, recording without routing, fixing one instance while leaving the pattern intact.
