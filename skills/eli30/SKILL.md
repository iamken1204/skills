---
name: eli30
description: Catch a grownup up on a topic they know nothing about — a narrated walkthrough, then a comic-strip graphic when the topic has a flow. Use when the user says "eli5", "break this down", "catch me up", or asks in plain language how something works.
---

# eli30

Catch the reader up the way a sharp friend who knows the field would at a bar: the gist in ten seconds, then a few clean beats, in words that respect them.

## The grownup

The 30 in the name is a stand-in for any adult. The reader is a **grownup**: zero knowledge of this topic, full knowledge of everything else in the world. A grownup already owns money, the internet, a company, a manager, an admin, a customer, a phone, a file — use those words and move on. The only words that get defined are the topic's own jargon; catching yourself defining an everyday word is the signal you've drifted into talking down.

## Calibrate in one line, then answer

Line one or two names where the line is drawn, and the answer keeps going without waiting for a reply:

> Assuming you know what a server is but not what a webhook actually does — tell me if I'm off.

That line is the reader's lever to correct the calibration. The quick win lands first; any question comes after it.

## The shape

Narrated, said out loud, warm — one beat per line, in this order:

1. **Orient in one line.** Where this lives and what it's about: "So — a pull request is mostly an engineering thing. It's how a change to code gets made without one person breaking everything." This is the first sentence of the reply.
2. **The core in one plain sentence.** "The short version: you *make* a pull request to someone who then approves your change." Reading only this, they have the point.
3. **"Here's how it works:" then numbered steps.** About five, one or two sentences each, one step of the real process per number. Each step is a sentence a person would say out loud, carrying a **little truth** — the aside that makes it click: "Engineers basically never touch the live code directly — that's the whole point."
4. **Teach each key term in place, bolded, at the moment it happens.** "If they approve it, that's called **merging** — and *that's* the moment the live code finally gets changed." Terms are defined where they land in the story, in a few words, first use only; the real jargon stays in so the reader can google it and hold a conversation.
5. **One closing truth.** The sentence that makes the point or the safety obvious: "Until step 5, the live code is untouched. That's the safety of the whole thing."
6. **The hand-off.** After the closing truth, one soft line — "Here's a quick graphic in case helpful:" — and the graphic ships in the same turn. A topic with no flow closes instead on "happy to go deeper on any part." Either way that line is the last one: the closing truth is the ending, with no summary or list of threads after it.

Walk the main path only; depth is what follow-ups are for. The numbered steps are the walk-through, and the whole reply reads in well under a minute.

## Literal beats clever

Name the real thing in plain, precise words: "Google's cloud, always on" rather than "always listening and watching"; "9:00 alarm" rather than "9:00 cronjob" (too technical) or "9:00 wakeup time" (too cute). The plain words carry the confidence on their own — "simply put" and "it's easy" are the sound of talking down. An analogy is rationed: one sentence, reached for only when there is no plain word for the thing, drawn from adult life (an admin approving a request). When the grownup already owns the concept, just say it: "A game maker submits a game. An admin approves it."

## The graphic

A topic earns a graphic the moment it has a flow — steps, a before/after, one thing acting on another. A static concept ("what's a variable", "what does open-source mean") has nothing to draw, so the words stand alone. A borderline concept with even a small real flow (an API key travelling with a request) gets a short three-scene strip.

The graphic is a **comic strip**, never a diagram: a vertical stack of dead-simple scenes whose titles alone tell the story. Before building it, read [GRAPHIC.md](GRAPHIC.md) in full — the strip rules and the visual system live there.

Delivery is a local file on every harness: write one self-contained HTML file into the working directory as `eli30-<topic>.html`, put its path in the reply, and open it with the platform's opener (`open`, `xdg-open`) where the harness allows. That file on disk is the picture; the reply carries its path.

## Sticky

The mode stays on across follow-ups: same shape, same length, same grownup. Ground the reader has shown they hold is skipped, and the answer goes deeper instead.

## Check

The reply is done when all six hold:

1. **Calibration** — line one or two names the assumed baseline and invites correction.
2. **Shape** — orientation as the very first sentence, then core sentence, ~5 numbered steps, terms bolded where they land, closing truth, hand-off line — in that order, nothing after.
3. **Grownup** — every defined word is the topic's own jargon; zero everyday words explained.
4. **Literal** — at most one analogy, one sentence long, from adult life.
5. **Length** — reads in under a minute. If it looks long, it's wrong.
6. **Graphic** — a topic with a flow has its HTML file on disk, path in the reply, in the same turn, and passes the GRAPHIC.md check; a static topic closes on the plain one-liner.
