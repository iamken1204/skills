# Technical writing

The goal is writing a tired engineer understands on the first read. Four layers, one question each: what kind of document is this, how do sentences address the reader, how much does each sentence carry, and can any sentence be read two ways. Apply all four to docs, RFCs, readmes, commit messages, and PR or MR descriptions.

Three rules sit above the layers:

- **Cut every word that does no work.** "In order to" is "to". "It is important to note that" is nothing.
- **Use the short, everyday word.** "Use", not "utilize". A long word has to buy its length with precision.
- **When a rule makes a sentence worse, fix the sentence another way or leave it alone.** The rules serve the reader.

The codebase is the word list: write the real symbol, file, flag, or command name, not a synonym. Don't invent jargon; use the words a developer would say out loud ("move", "delete", "a budget that only decreases"). A named pattern is fine when the doc says what it means the first time.

## Vary the rhythm

A doc can obey every rule and still read machine-written. Mix sentence lengths on purpose: short sentences land a point; longer ones carry a fact with its condition. One thought per sentence does not mean one length per sentence. Have a view where the mode allows it (explanation weighs trade-offs; reference stays dry). Be specific over sterile: not "schema changes can cause issues" but "a column rename fails the build".

## Pick the mode first (Diátaxis)

One document, one mode. Two questions pick it: action or understanding, learning or work.

- **Tutorial** (action + learning). You are the teacher; the learner's success is your job. Open with what they will build. Every step produces a visible result, and you tell them what they should see. Cut explanation to one clause and a link. Write as "we", in commands.
- **How-to** (action + work). Solve a problem a person has. Assume competence, skip teaching, action only. Allow forks: "If you want x, do y." Name it by the task: "How to calibrate the radar array".
- **Reference** (understanding + work). Describe, only describe. Dry, complete, sure; no instruction, no opinion. Mirror the structure of the thing described. Generate from code where possible.
- **Explanation** (understanding + learning). One bounded topic, readable away from the product. Anchor on a real why question; give design decisions, history, constraints, alternatives. Opinion is allowed here and nowhere else.

Don't mix modes; split and link instead.

## Write sentences to the reader (developer style)

- Talk to the reader as "you", in the present tense.
- Say who does what: "the compiler checks", not "is checked".
- Write instructions as commands: "Click Submit." Never "should be done".
- Put the condition before the instruction: "To delete the document, click Delete."
- Common case first, exceptions after.
- No buzzwords, no "please" in instructions, never "simply", "easy", or "quickly" in a procedure.
- Don't pre-announce, don't start consecutive sentences with the same phrase, read awkward sentences aloud and rewrite.
- Links say where they go (page title or short description), never "click here".
- Headings carry the point, not just the topic ("Pick the mode first", not "Modes"), sentence case. Task headings are bare verb phrases; concept headings are noun phrases.
- Numbered lists for sequences, bullets otherwise, introduced by a complete sentence, items parallel.
- Code in code font, UI elements in bold, serial commas, no "etc.".

## Make statements load one at a time (STE)

- One instruction per sentence; one thought per sentence everywhere else.
- Split instructions longer than ~20 words, other sentences longer than ~25.
- Warning or condition before the step it guards.
- Keep "the" and "a": "Remove backup file" reads two ways; "Remove the backup file" reads one.
- One meaning per word, one word per action ("start", not "start" here and "initiate" there).
- Procedures as direct commands, never narration, never passive.
- Avoid "-ing" words where you can; they breed misreadings.

## Leave no sentence open to two readings (Global English)

- Keep "only" and "not" next to the word they change.
- Break up long noun strings: "the proto import budget check script" becomes "the script that checks the proto-import budget".
- Make every "it", "they", "this" point at one obvious thing; repeat the noun when in doubt; never point "this" at a whole clause.
- Don't drop verbs; give every clause one.
- Keep the small words that show structure ("Ensure that the switch is off"). Never trade clarity for word count.
- Repeat the article in a series when it prevents a misread: "the client and the host".
- Disambiguate "and"/"or" grouping with "both...and", "either...or", "if...then".
- Periods, not semicolons. A new sentence instead of an em dash.
- Parentheses hold a full grammatical unit; never form plurals with "(s)"; no slashes ("a, b, or both", not "a/b").
- Call each thing by one name, everywhere. Don't reword unchanged sentences between edits.
- Skip idioms, Latin abbreviations, and metaphors.

## Voice

Apply `references/unslop.md` to every doc this file touches; it owns the slop-pattern catalog. Commit messages and PR or MR descriptions are writing too: every layer except Diátaxis applies. Make every count or tree claim true at the commit that lands it, and include the command that regenerates it.

## Review checklist

1. Is each file one Diátaxis mode, with links where modes meet?
2. Is every instruction a command, with its condition in front?
3. Does any sentence carry two instructions or two thoughts? Split it.
4. Can any word be cut without losing meaning? Cut it.
5. Is "only" next to the word it changes? Does every "it" point at one thing? Does every clause keep its verb?
6. Does each thing have exactly one name across the docs?
7. Would a developer say these words out loud? Replace invented metaphors with the plain word or the real symbol name.
8. Are all symbols, paths, and counts real at this commit, with the commands that regenerate them?
