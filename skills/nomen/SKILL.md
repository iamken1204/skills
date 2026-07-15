---
name: nomen
description: Layered naming — use when the user wants a name for anything (project, product, library, tool, feature, character, team), asks "what should I call this", wants a rename, or wants an acronym/backronym.
---

# Nomen

This skill named itself: *nomen* is Latin for "name"; it contains *omen* — a name that foretells its bearer; and it backronyms to **N**ames **O**verloaded with **M**eaning, **E**mbedded **N**ods. Three readings, all pointing home. That is the method.

A great name is a stack of readings that all **point home** — every layer resolves to the subject or one of its traits. Calibration example, GLaDOS:

- **Expansion**: Genetic Lifeform and Disk Operating System — honestly describes her (an AI grown from a human, running a facility).
- **Nod**: "DOS" embeds the old disk operating system — she *is* an operating system.
- **Sound**: spoken aloud it's "Gladys", a woman's name — matching her voice and persona.
- **Shape**: the lone lowercase *a* fences "DOS" off visually, telegraphing the nod.

A reading that points nowhere is a **dead layer** — decoration. Cut the layer or the candidate.

## The four layers

1. **Expansion** — what the name unpacks to (acronym or portmanteau). Must be an honest description of the subject, not word salad assembled to force letters.
2. **Nod** — an embedded reference (substring, homophone, loanword) to the subject's lineage: what it descends from, replaces, or pays tribute to.
3. **Sound** — the spoken name lands as a real word or natural name whose feel matches the persona (menacing, friendly, corporate, playful).
4. **Shape** — casing or typography that telegraphs the other layers.

Two live layers is a good name; three is a great one. Never fake a layer to hit a count.

## Steps

### 1. Intake

Ask the user (AskUserQuestion when available, one round):

- What is it, and its 2–3 defining traits?
- Lineage — what does it descend from, replace, or nod to? Any canon worth referencing (unix lore, mythology, a language the user speaks)?
- Persona — how should the name *feel*?
- Constraints — acronym required? Length, casing, and whether it needs a free npm/pypi package, domain, or trademark.

**Done when** you can write one honest sentence: "X is a ___ that ___, descends from ___, and should feel ___." Open step 2 by stating it, so the user can correct course.

### 2. Mine anchors

List raw material: trait words, lineage names, domain jargon, myth/canon figures, cross-language words. **Done when** ≥6 anchors spanning at least two of those categories.

### 3. Forge

Generate from both ends:

- **Anchor-out**: take an anchor, grow letters around it into a pronounceable word, then backronym the remaining letters honestly.
- **Phrase-in**: write the honest descriptive phrase, compress it to an acronym or portmanteau, then hunt the result for accidental nods and sounds.

**Done when** ≥6 raw candidates exist, at least two from each direction.

### 4. Audit

Per candidate, list every reading and mark it live (points home) or dead. Kill:

- candidates with fewer than 2 live layers
- strained expansions (filler "and"/"very", a forced adjective) — unless the payoff is GLaDOS-grade
- practical failures: unsayable, unspellable after hearing it once, unsearchable (drowned by a common word), or colliding with an existing name in its domain (quick registry/web check when it's a product)

**Done when** 3–5 survivors remain, each with ≥2 live layers and passing practicals.

### 5. Present

One breakdown block per survivor — the name, how to say it, then each layer on its own line with what it points to; flag any dead layer honestly. Recommend exactly one, naming the deciding layer.
