---
name: fairway
description: Implement with happy-path-first orchestration, deep modules, type-driven invariants, and evidence-gated complexity. Use when building or refactoring a feature whose main flow should read plainly, or when code buries its happy path under ceremony and defensive branches.
---

Keep the reader on the fairway: the happy path is the main line of the code, mechanics live in deep modules below it, and complexity is added only on evidence. Failures still get code, below or beside the main line, in proportion to how real they are.

Read the existing code, callsites, data flow, and nearby conventions first. Keep good repository patterns; do not impose a generic architecture.

## Tie-Breakers

Types and boundaries add structure; rent and evidence remove it. When they conflict, decide in this order:

1. **Safety first.** Security boundaries, concurrency primitives, and irreversible data operations (deletes, payments, migrations) may be defended without an observed failure.
2. **Default to the smallest honest implementation**: a direct function, a Transaction Script, a vertical slice.
3. **Promote a raw value to a domain type** only when it crosses a trust boundary or carries an invariant more than one place must respect.
4. **Extract a module, port, or service** only when it hides real complexity, owns a real invariant, or has more than one real implementation.
5. **Remove duplication at the third occurrence** (Rule of Three). Duplication is cheaper than the wrong abstraction.

## Happy Path First

- A top-level function is a Composed Method: it coordinates one use case by calling well-named domain operations in the order the use case happens. Parsing, process plumbing, protocol details, state surgery, and long validation live below it.
- Guard clauses: invalid conditions leave first, and the valid path stays flat. Return early for a legal no-op. Assert or throw for a broken invariant; never swallow it.
- Let errors reach the existing user-facing boundary unless recovery is an explicit product requirement.

## Deep Modules

- Names describe domain intent, not mechanics.
- Required dependencies and state are explicit parameters, impossible to omit. No optional ambient state read deep in the flow.
- Extract one deep operation that hides real complexity. Do not split one flow into shallow helpers (`prepare`, `do`, `finish`) the reader must reassemble.
- Prefer a small cohesive interface over a bag of callbacks, booleans, and behavior switches.
- State and its invariants have one owner. Tell the owner the domain operation (Tell, Don't Ask) instead of reading its state and mutating it from outside.
- Functional core, imperative shell: domain decisions in the core, IO in ports and adapters.

Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. A change that looks right from one file should be right for the whole repo:

- One way to do each task. When you add a new way, move callers off the old one and delete it in the same change.
- Internals are unreachable from outside the module (package `exports`, `internal/` directories, unexported symbols), so an outside import fails the build.
- One list per set of items. Derive the other lists from it, or make the build fail when they disagree.
- One writer per piece of state. A second module that writes it or keeps its own copy drifts.

## Types

- Make invalid states unrepresentable: a discriminated union of the legal states, not nullable fields and booleans that must stay in sync.
- Parse, don't validate. External, persisted, and network data is parsed once at the boundary into a domain type; internal code never re-checks raw data. A loose map type (`Record<string, unknown>`, `map[string]any`, a bare `dict`) stops at the parse.
- Domain types for meaningful IDs, versions, paths, states, and results. No `any` or loose string protocols where a precise type can state the contract.
- When a schema already owns a shape (the repository's runtime schema library, protobuf, OpenAPI, GraphQL, a database migration), derive the type from it. Do not hand-roll a parallel type, and do not add a schema dependency for one guard.
- In a language with weak or no static types (bash, untyped Python, plain JS), validate once at the entry point, fail fast there, and let names carry the trusted form. Where sum types are missing (Go), use the clearest native encoding. Do not simulate a type system the language cannot enforce.

## Patterns Must Pay Rent

A pattern, layer, abstraction, interface, or file is a cost. Add one only when it buys more readability, correctness, testing, or change-isolation than it costs in lines, files, call hops, and concepts. A layer that only forwards (`Controller -> Service -> Repository` around one database call) is negative value; add it later, when it hides stable complexity or gains a second implementation. The code should reveal its use cases (`invoice/pay.ts`), not its layers.

## Evidence Before Complexity

- Outside the safety tie-breaker, edge-case handling needs evidence: an explicit requirement, an API contract, a failure path derived from the code, runtime behavior, logs, a test reproduction, persisted state, or a user report. "Could", "might", and "what if" alone are not evidence; state the concrete failure condition.
- Address the supported failure with the smallest fix at the boundary that owns it, not a general defense system around one case.
- When fixing a failure, first ask whether the state that triggered it is legitimate. If the system may be in that state, handle it where the code broke. If the state should never exist, a guard there hides the bug; find what produced the state. Guards, retries, swallowed errors, clamped values, and discarded state are the usual ways to hide one.
- A crash or restart partway through a command, lifecycle step, or loop is a failure path derived from the code. Derive each step from the state that exists, not from what the previous run meant to do: read the current state, compare it to the goal, apply only the difference. Anything a run leaves behind (a lock, a temporary file, a half-written record, a claimed job) must be recognizable as stale by the next run wherever the previous run stopped; for example, write to a temporary path and rename it into place.
- In existing code, a safeguard you cannot trace to evidence is a question to raise, not a line to silently delete.
- Prefer less code, fewer names, fewer branches, and a net-negative diff when behavior permits.

## Tests

A test claims something about what the code does for its users: a caller, an end user, or another service. Judge each test against two imagined edits:

- **Break the behavior**: return a wrong value, skip an effect, or do it twice. If the test still passes, it proves nothing. The usual causes are an assertion looser than the contract, an expected value computed by the code under test, and an assertion on data the test built itself.
- **Change the internals** and keep every observable result. If the test now fails, it is pinned to the implementation.

Keep a test that catches the first edit and survives the second; rewrite or delete the rest. Drive the code through its users' interface with a concrete input, and derive the expected value from the requirement. The payload an external service receives is behavior; a call to an internal helper is not. Pair "this never happens" with a case where it does happen. Do not build large mock systems for small changes.

## Done

Finish the complete change, run focused verification, delete temporary artifacts, and make one final simplification pass. The result should read as boring, obvious, and native to the codebase.

Task / scope:
$ARGUMENTS
