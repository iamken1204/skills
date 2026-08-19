### Multi-phase plan

Produce a phased implementation plan grounded in the rigor-impl Principles. The plan is the deliverable. Do not implement.

Open a todolist with one item per step below.

**0. Triage.** Skip the plan when the change is one or two files with an obvious approach; say so and stop. Plan when the change spans three or more files, introduces architecture, has competing approaches or unclear scope, or the user asked for one.

**1. Re-read principles.** Read the rigor-impl Principles index end to end, and the full rules in `PRINCIPLES.md` for the ones the plan will lean on. They govern every plan decision; cross-link them.

**2. Scope and constraints.** State your read of scope and constraints in one paragraph. Ask the user only for genuinely ambiguous intent (the never-block-on-the-human principle), with concrete options per open question. Resolve what is in scope vs explicitly out, technical or platform constraints, patterns to preserve, and the definition of done.

**3. Explore in subagents.** Delegate codebase exploration (the guard-the-context-window principle): each explorer returns file pointers, conventions, dependencies, test infrastructure, and entry points. No inlined dumps. Explorers read this SKILL.md before working.

**4. Write the plan.** The user specifies where the plan lives. Single file `NN-slug.md` for small plans; for three or more phases, a directory with `overview.md` plus phase files and a `testing.md`.

Phase sizing: one function or type plus tests, or one bug fix, not "one file". Two to three files touched, max. Prefer eight to ten small phases over three to four large ones to preserve option value. Split if a phase has more than five test cases or three functions.

Overview file: **Context** (problem and why now), **Scope** (included; explicitly excluded), **Constraints**, **Alternatives** (two or three approaches sketched, choice and rationale per the exhaust-the-design-space principle; skip when constraints dictate one), **Applicable skills** the implementer should invoke by name, **Phases** (ordered links to phase files), **Verification** (project-level commands), **Implementation guidance** (per step 6).

Phase files: back-link to overview, **Goal**, **Changes** (files affected and the change at a high level; what and why, not how; no code snippets), **Data structures** (key types or schemas, one-line sketch only), **Verification** (per step 5).

Order phases so infrastructure and shared types land first. Each phase should be independently shippable. For changes touching existing code, apply the redesign-from-first-principles principle: if we'd built this with the new requirement on day one, what would it look like? Redesign holistically; deliver incrementally.

**5. Verification per phase.** Each phase needs both. Static: type check, lint, project tests. Runtime: exercise the feature on the matching control surface; no automation for the touched surface → flag it in the plan. For bug fixes the loop is reproduce on the surface, fix, verify on the same surface; unit tests show a branch behaves a certain way, they do not prove the bug is gone.

**6. Implementation guidance.** In the overview, name which rigor-impl non-negotiables the implementer must apply, by name: `references/how.md` over each unfamiliar subsystem, `references/interrogate.md` on contested designs before shipping, a slop-strip over each diff and `references/unslop.md` over any prose surface, and `references/decision-trail.md` when the plan is large enough to need an auditable record.

**7. Hand back.** Summarize phases, scope boundaries, applicable skills, and verification. Stop. The user decides when implementation starts.
