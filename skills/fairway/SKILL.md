---
name: fairway
description: Implement with happy-path-first orchestration, deep modules, type-driven invariants, and evidence-gated complexity. Use when building or refactoring a feature whose main flow should read plainly, or when code buries its happy path under ceremony and defensive branches.
---

Keep the reader on the fairway: the happy path is the main line of the code, mechanics live in deep modules below it, and complexity is added only on evidence.

The happy path should dominate what readers see, in proportion to how much of real behavior it is. That is a bias for layout and emphasis, not a license to skip error handling: failures still get code, below or beside the main line, in proportion to their reality.

Start with context:

- inspect the existing code, callsites, data flow, and nearby conventions
- understand the real use case before choosing abstractions
- preserve good repository patterns; do not impose a generic architecture

Examples below are TypeScript; the rules are language-neutral (see the note under Type-Driven Invariants).

## Tie-Breakers

The rules in this skill pull in two directions: types and boundaries add structure, rent and evidence remove it. When they conflict, decide in this order:

1. **Safety first.** Security boundaries, concurrency primitives, and irreversible data operations (deletes, payments, migrations) may be defended without an observed failure. Elsewhere, use the evidence criteria in Evidence Before Complexity.
2. **Default to the smallest honest implementation**: a direct function, a Transaction Script, a vertical slice.
3. **Promote a raw value to a domain type** only when it crosses a trust boundary or carries an invariant more than one place must respect. Inside a small local scope, a well-named variable is enough.
4. **Extract a module, port, or service** only when it hides real complexity, owns a real invariant, or has more than one real implementation.
5. **Remove duplication at the third occurrence**, when the shared shape is proven (Rule of Three). Duplication is cheaper than the wrong abstraction.

## Happy-Path-First Orchestration

Top-level methods coordinate a use case by calling well-named domain operations. They should not contain parsing, process plumbing, protocol details, state surgery, or long validation branches.

DON'T make the orchestrator own every detail:

```ts
async function update(input: string) {
  if (!input) throw new Error("missing version")
  const child = spawn("sh", ["-c", buildInstallScript(input)])
  const result = await collectOutput(child)
  if (result.code !== 0) throw new Error(result.stderr)
  const installed = parseVersion(await runVersionCommand())
  if (installed !== input) throw new Error("wrong version")
  await killExistingProcess()
  await startProcess()
}
```

DO expose the use case and push mechanics behind deep boundaries, preserving operation order and failure behavior. This example assumes installation can run while the server is active:

```ts
async function update(version: Version) {
  await cli.install(version)
  await cli.requireVersion(version)
  await server.stop()
  await server.start()
}
```

## Guards, Not Nesting

- reject invalid conditions with early guards; keep the valid path flat and linear, never nested inside defensive branches
- return early for a legal no-op: "nothing to do" is a valid outcome
- assert or throw for a broken invariant: a state that should be impossible must fail loudly, never be silently swallowed
- let errors reach the existing user-facing boundary unless recovery is an explicit product requirement
- handle common operational failures clearly; justify handling uncommon cases with the evidence criteria below, even before they occur in production

DON'T bury the valid path in nested conditionals:

```ts
if (config) {
  if (config.enabled) {
    if (server.ready) {
      return run(config)
    }
  }
}
return undefined
```

DO leave invalid conditions first and keep the valid path flat:

```ts
if (!config) return            // legal no-op
if (!config.enabled) return    // legal no-op
assert(server.ready)           // broken invariant: fail loudly
return run(config)
```

## Deep Modules, Deliberate Interfaces

- names describe domain intent, not implementation mechanics
- required dependencies are explicit and impossible to omit
- prefer small cohesive interfaces over bags of callbacks, booleans, and optional behavior switches
- keep IO in infrastructure; keep domain decisions out of wrappers
- extract one deep operation that hides real complexity; do not shatter a flow into shallow helper shrapnel

DON'T force readers to reconstruct one operation from fragments:

```ts
prepareUpdate()
doUpdate()
finishUpdate()
```

DO keep tightly related code together, or extract one deep operation:

```ts
await cli.installExactVersion(version)
```

State and its invariants have one owner. Tell the owner the domain operation instead of reading its state and mutating it from outside.

DON'T:

```ts
if (session.status() === "pending") {
  session.messages().push(message)
  session.setStatus("active")
}
```

DO:

```ts
session.promote(message)
```

Design for the next contributor, and assume it is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. A change that looks right from one file should be right for the whole repo:

- one way to do each task; when you add a new way, move callers off the old one and delete it in the same change, or both keep gaining callers
- internals stay unreachable from outside the module (package `exports`, `internal/` directories, unexported symbols), so an outside import fails the build instead of quietly widening the interface
- one list per set of items; derive the other lists from it, or make the build fail when they disagree
- one writer per piece of state, per the owner rule above; a second module that writes it or keeps its own copy drifts the moment an agent edits only one of them

## Type-Driven Invariants

- make invalid states unrepresentable where the language can express it
- parse external, persisted, and network data once at the boundary; internal code receives trusted values and never re-checks raw data
- use domain types for meaningful IDs, versions, paths, states, and results; no `any`, loose string protocols, or nullable states where a precise type can express the contract
- enforce invariants in constructors, schemas, and narrow signatures, so illegal combinations cannot be constructed, not merely documented
- when a schema already owns a shape (the repository's runtime schema library, a protobuf, OpenAPI, or GraphQL schema, a database migration), derive the type from it, e.g. `z.infer<typeof UserSchema>`; do not hand-roll a parallel type plus a property-by-property guard that drifts from it, and do not add a schema dependency for one guard
- a loose map type (`Record<string, unknown>`, `map[string]any`, a bare `dict`) stops at the parse; past the boundary, data has a named domain type
- make required state explicit in parameters instead of reading optional ambient state deep in the flow

DON'T validate raw values and throw away what the check proved:

```ts
validateVersion(input)
await install(input) // still a raw string
```

DO parse into a trusted domain value once:

```ts
const version = Version.parse(input)
await install(version)
```

DON'T represent mutually exclusive states with nullable fields and booleans:

```ts
type Server = {
  starting: boolean
  url?: string
  error?: string
}
```

DO model the legal states directly:

```ts
type ServerState =
  | { kind: "stopped" }
  | { kind: "starting" }
  | { kind: "ready"; url: ServerUrl }
  | { kind: "failed"; error: ServerError }
```

**Language note.** In languages with weak or no static types (bash, untyped Python, plain JS), keep the same discipline without the ceremony: validate once at the entry point, fail fast there, and let names carry the trusted form downstream. Where sum types are missing (Go), prefer the clearest native encoding over an emulated one. Do not simulate a type system with wrappers the language cannot enforce; that is ceremony without the guarantee.

## Patterns Must Pay Rent

Patterns, layers, abstractions, interfaces, and files are costs. Use one only when it buys more readability, correctness, testing, or change-isolation than it costs in lines, files, call hops, and concepts a reader must learn.

- a pattern name is vocabulary for a design that emerged, not a requirement to manufacture that design
- an abstraction that moves ten obvious lines into five files is negative value
- a repository that only renames one database call is a shallow module, not architecture
- do not build `Controller -> Service -> Repository` chains because a diagram, framework, or blog post says they should exist
- Screaming Architecture means the code reveals its use cases, not that it has layers: `invoice/pay.ts` screams louder than three folders of pass-through methods

DON'T apply a repository pattern to ten obvious lines:

```ts
class UserController {
  constructor(private service: UserService) {}
  get(id: string) {
    return this.service.get(id)
  }
}

class UserService {
  constructor(private repository: UserRepository) {}
  get(id: string) {
    return this.repository.get(id)
  }
}

class UserRepository {
  get(id: string) {
    return database.selectUser(id)
  }
}
```

DO keep a simple use case simple:

```ts
async function getUser(id: UserID) {
  return database.selectUser(id)
}
```

Add the repository later, when data access becomes a real domain port or hides stable complexity that callers should not know.

## Evidence Before Complexity

- prefer one obvious path and one source of truth
- outside the safety carve-out in Tie-Breakers, require evidence for edge-case handling: explicit requirements, API contracts, failure paths derived from the code, runtime behavior, logs, test reproductions, persisted state, or user reports all count
- address the supported failure with the smallest fix at the boundary that owns it; do not build a general defense system around one case
- when fixing a failure, first ask whether the state that triggered it is legitimate. If the system may be in that state, the code that broke on it is the root cause; handle the state there. If the state should never exist, a guard where it surfaced hides the bug; find what produced the state. Guards, retries, swallowed errors, clamped values, and discarded state are the usual ways to hide one
- a crash or restart partway through a command, lifecycle step, or loop is a failure path derived from the code, not an imagined one. Derive each step from the state that exists, not from what the previous run meant to do: read the current state, compare it to the goal, apply only the difference. Anything a run leaves behind (a lock, a temporary file, a half-written record, a claimed job) must be recognizable as stale by the next run, by evidence that holds wherever the previous run stopped; for example, write to a temporary path and rename it into place
- never justify complexity with "could", "might", or "what if" alone; state the concrete failure condition and supporting evidence
- when editing existing code, a safeguard you cannot trace to evidence is a question to raise, not a line to silently delete
- prefer less code, fewer names, fewer branches, and net-negative diffs when behavior permits

DON'T add lifecycle machinery for an imagined race:

```ts
const attempts = new Map<ID, number>()
// counters, stale ownership checks, retries, cleanup, and fallback paths
// added because two calls might theoretically overlap
```

DO implement the required flow directly. Here, installation requires the server to have exited:

```ts
await stopServer(id)
await installCli(version)
await startServer(id)
```

Make `stopServer` await process exit before installation because the next operation requires it; do not wait for a `Text file busy` report. Keep that guarantee inside `stopServer` rather than building a lifecycle framework.

## Domain Core, Infrastructure Shell

DON'T leak infrastructure into domain decisions:

```ts
function promote(message: Message) {
  spawn("sh", ["-c", notifyScript])
  database.insert(message)
}
```

DO keep domain decisions in the core and IO in ports, adapters, or the imperative shell:

```ts
const event = session.promote(message)
await sessionStore.append(event)
```

## Tests At Stable Boundaries

A test claims something about what the code does for its users: a caller, an end user, or another service. Judge each test against two imagined edits:

- **break the behavior**: return a wrong value, skip an effect, or do it twice. If the test still passes, it proves nothing. The usual causes are an assertion looser than the contract, an expected value computed by the code under test, a restated constant that never runs the code that reads it, and an assertion on data the test built itself
- **change the internals**: keep every observable result and restructure the code underneath. If the test now fails, it is pinned to the implementation; it needs a rewrite on every refactor and still catches no bug

Keep a test that catches the first edit and survives the second; rewrite or delete the rest. Drive the code through its users' interface with a concrete input, derive the expected value from the requirement rather than from a run of the code, and assert what the contract promises, no less and no more. The payload an external service receives is behavior, because that service observes it; a call to an internal helper is not. When the contract is that something does not happen, pair the no-call assertion with a case where it does happen, so the test shows it can see the call. Do not build large mock systems for small changes.

DON'T test the implementation sentence by sentence:

```ts
expect(regionFor("eu-1")).toBe("region:eu-1")
expect(shouldRestart({ available: false })).toBe(true)
```

DO test the stable use-case boundary and the observable order of its effects:

```ts
await controller.update("1.2.3")
expect(events).toEqual(["install", "verify", "stop", "start"])
```

## Vocabulary

Name the design that emerged with established terminology:

| Desired quality | Established terminology |
| --- | --- |
| Main flow reads like the use case | Composed Method, use-case orchestration |
| Mechanics hidden below small interfaces | Deep modules, information hiding, complexity pulled downward |
| Domain logic free of process and network code | Functional Core / Imperative Shell, Ports and Adapters |
| Smallest honest implementation of one use case | Transaction Script, vertical slice |
| Boundary checks produce trusted values | Parse Don't Validate, smart constructors |
| Types enforce invariants | Making illegal states unrepresentable, type-driven design |
| Invalid conditions leave before the normal flow | Guard clauses, fail-fast |
| Reuse follows real repetition | Rule of Three, semantic compression, YAGNI |
| State and behavior have one owner | Encapsulation, Tell Don't Ask |

## Sources

- John Ousterhout, [A Philosophy of Software Design](https://stanford.edu/~ouster/cgi-bin/aposd.php): deep modules, complexity pulled downward
- Alexis King, [Parse, Don't Validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)
- Scott Wlaschin, [Making Illegal States Unrepresentable](https://fsharpforfunandprofit.com/posts/designing-with-types-making-illegal-states-unrepresentable/)
- Gary Bernhardt, [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell)
- Martin Fowler: [YAGNI](https://martinfowler.com/bliki/Yagni.html), [guard clauses](https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html), [Tell, Don't Ask](https://martinfowler.com/bliki/TellDontAsk.html)
- Sandi Metz, [The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction): duplication is cheaper than the wrong abstraction
- Casey Muratori, [Semantic Compression](https://caseymuratori.com/blog_0015); Carson Gross, [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/) and [grugbrain.dev](https://grugbrain.dev/)
- Jimmy Bogard, [Vertical Slice Architecture](https://www.jimmybogard.com/vertical-slice-architecture/); Alistair Cockburn, [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)

## Done

Finish the complete change, run focused verification, delete temporary artifacts, and make one final simplification pass. The result should feel boring, obvious, cohesive, and native to the codebase; in typed languages, also typed.

The combined style is: **happy-path-first, use-case-oriented design with deep modules, type-driven invariants, boundary isolation, and evidence-driven complexity.**

Task / scope:
$ARGUMENTS
