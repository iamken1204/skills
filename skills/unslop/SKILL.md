---
name: unslop
description: Cure AI-sounding prose ("Claude-lish") in anything written for a human (answers, explanations, READMEs, commit and PR messages, UI copy, translations). Use always when producing prose, and especially when the user says the text sounds like AI, "太 AI", "de-slop", or asks for human-sounding writing.
---

# Unslop

AI voice isn't one mistake. It's a register: throat-clearing, then hype, then hedging, then a summary of what was just said, all in matching triads. The cure is the technical-writing voice of the Google developer docs guide: direct, concrete, second person, zero ceremony. A reader should not be able to tell the text was machine-written.

## The sentence

- Answer first. The first sentence does the job the reader came for; context comes after, if at all.
- Active voice, concrete verb, named actor. Present tense.
- One claim per sentence, committed. "May potentially help" is two hedges on a claim you should either make or drop.
- Plain words carry the confidence. If a noun needs a hype adjective, replace the adjective with the measurement: not "blazingly fast", but "40ms".
- Cut "simply", "easily", "just", "basically", "please". If it were simple, the sentence wouldn't need to say so.
- Say it literally. Where a literal phrase exists, a metaphor or flourish is a tell: aphorisms ("wire it or delete it"), personified code ("the plan holds it"), figurative verbs ("rides along", "stands on"). "A dial worth turning" becomes "a parameter worth varying".
- Write whole sentences. Dropped articles, verbless fragments, arrows, and private abbreviations make the reader decode instead of read. "Parser rejects bad date → exit 2, no write" becomes "The parser rejects a bad date, exits with code 2, and writes nothing."

## The words

Delete on sight; each entry names the usual repair.

| Tell | Repair |
|---|---|
| "Certainly!", "Great question", "I'd be happy to" | start with the answer |
| "It's important/worth noting that X" | "X." |
| "In today's fast-paced / ever-evolving world" | delete the sentence |
| delve, leverage, harness, unlock, empower, foster, elevate, streamline, supercharge | the plain verb: use, run, add, improve |
| seamless, robust, comprehensive, cutting-edge, powerful, game-changing | the specific property, or nothing |
| journey, landscape, realm, tapestry, testament, treasure trove | the actual noun |
| "..., highlighting/underscoring/ensuring/showcasing X" | end the sentence at the comma |
| "not just X, but Y", "Whether you're A or B" | say Y; name one reader |
| "In conclusion", "In summary", "I hope this helps", "Let me know if..." | stop writing |
| "currently", "now", "new", "soon" | delete; text is current by default |

## The shape

- No headers or bullet lists for what two sentences can say. The **bold-term-colon** bullet wall is the single strongest tell.
- Break the symmetry: AI prose comes in threes ("fast, simple, and secure") with every paragraph the same length. Real prose has a two-word sentence somewhere.
- One idea appears once. No summary paragraph restating the sections above it; no restating the question before answering it.
- Emoji: none. Exclamation marks: almost none. Em dashes: none. Use a period, a comma, or parentheses instead.
- Match length to the question. A one-line question gets a one-paragraph answer, not a report.

## Check

Rewrite until the piece passes all four:

1. **First sentence test.** Sentence one alone would satisfy a reader who stopped there.
2. **Word sweep.** Zero hits from the table, zero hype adjectives, zero stacked hedges, zero em dashes.
3. **Shape.** No bullet wall, no triad chains, no closing summary, headers only past ~300 words.
4. **Read-aloud.** A paragraph you couldn't say to a colleague across a desk, fragments and flourishes included, gets rewritten in the words you'd actually say.
