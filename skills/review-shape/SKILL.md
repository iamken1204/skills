---
name: review-shape
description: "Audit a branch or PR diff for maintainability — code judo, file sprawl past 1k lines, spaghetti branching, boundary and layering leaks. Use when the user asks for a code-quality or maintainability review."
---

# Review Shape

Audit the branch's diff for maintainability, not correctness. The bar is **code judo**: a restructuring that keeps behavior identical while deleting a category of complexity outright, rather than rearranging it or polishing its edges — even if that means touching more of the codebase than the diff strictly needed to. Don't stop at "this could be a bit cleaner"; look for the reframing that makes whole branches, helpers, or layers disappear.

Findings are ordered by priority below — lead the review with the highest one present, and don't bury it under cosmetic nits. Prefer a small number of high-conviction findings over a long list of low-value ones.

1. **Missed code judo.** A plausible restructuring would delete a category of complexity, not just relocate it or centralize it. *"There's a code-judo move here — reframe this so these branches disappear."*
2. **File size.** The diff pushes a file from under 1000 lines to over. Treat as a blocker by default; only waive it with a real structural reason and a file that stays clearly organized. *"This pushes the file past 1k lines — can we decompose it first?"*
3. **Spaghetti growth.** New ad-hoc conditionals, scattered special cases, or one-off branches bolted onto an existing flow, even if they technically work. Push the logic into its own helper, module, or state machine instead of tangling the path further. *"This adds another special case to an already busy flow — can it live behind its own abstraction?"*
4. **Boundary and type cleanliness.** Unnecessary `any`/`unknown`, casts, or optionality papering over an unclear invariant, or a silent fallback standing in for an explicit contract. *"Why the cast/optional here — can the boundary be explicit instead?"*
5. **Wrong layer or duplicated helper.** Feature-specific logic leaking into a shared path or through an API, or a bespoke one-off reinventing a helper the codebase already has. Push logic to the layer/package that owns the concept; reuse the canonical helper. *"This looks like a bespoke helper for something we already have — can we reuse the canonical one?"*
6. **Needless indirection.** Thin wrappers, identity abstractions, or generic "magic" handling that add a hop without adding clarity, hiding a simple data shape behind a mechanism. Delete rather than polish. *"This abstraction doesn't earn its keep — can we keep the direct flow?"*
7. **Avoidable non-atomicity.** Independent work serialized for no reason, or related updates that can leave state half-applied. Parallelize or make atomic when the cleaner shape is obvious — don't chase this as a micro-optimization when it isn't.

## Approval bar

Block on any of the above unless the author has a clear justification. "Behavior seems correct" is not a pass on its own — a correct-but-messier diff still needs a reason it can't be the code-judo version.

Report each finding with file:line evidence, in the priority order above.
