# The comic strip

One rendered HTML file: a vertical stack of scenes read top to bottom, one beat each — the whole flow, one picture at a time. The reader never traces anything. A story that wants a single clever diagram (a timeline, a branch curve, a loop with scattered numbers) gets rebuilt as separate stacked scenes.

## Panels

- **Titles are the story.** Each panel title is a plain subject-verb-object sentence, so reading the titles alone, top to bottom, is the explanation: "Everyone shares one copy of the code." → "You take your own copy." → "You edit it." → "You merge — the two become one." Delete every picture and the titles still tell it.
- **One action per scene.** Three or four elements, one left-to-right action. A scene with two actions is two scenes. Richness comes from the sequence of panels, never from density inside one.
- **A consistent cast.** The same friendly glyphs — a little person, a document, a robot with a face, a browser window — drawn identically in every frame, one SVG `<symbol>` per character reused across scenes, so the reader recognises the characters. Labelled rectangles that change shape from panel to panel are not a cast.
- **One caption per scene** carries the little truth — the "why it matters" aside: "This is the real thing users run. Nobody edits it directly." "The live code keeps moving without you."
- **A subhead adds, never restates.** "You copy the codebase" over "grab your own copy of the code" is one sentence twice; the subhead carries the next fact — the concrete example, the caveat, the little truth.
- **The page is the content.** Everything on it is explanation: no slash-command tag, no category eyebrow, no "here's a fun visual" framing, no footer about the reader's level.

## Build

- Hand-draw the scenes as inline SVG with reusable `<symbol>`s for the cast. Mermaid inside the HTML is acceptable for a genuine timeline; the strip is what reads as a story.
- Self-contained: inline CSS and SVG, system fonts, no external assets. Paint `body` background explicitly so the dark theme holds on any host.

## Visual system

Editorial and restrained, committed dark theme.

- **Type:** Georgia serif, regular weight (400), for the title question and every panel title; Helvetica/Arial sans for body, captions, and labels.
- **Palette:** ground `#0B0D0F`; charcoal surfaces and bands `#17191D` and `#24272D`; warm-white ink `#F5F5F0`; muted secondary `#A7A9B2`; one Zed-purple accent `#A78BFA`, used sparingly — step eyebrows, the active/"your" element, key terms, one arrow. The active thing is purple, the shared/neutral thing is warm white, fills are charcoal; those are the only hues.

  ```css
  .graphic-ground { background: #0B0D0F; }
  .graphic-charcoal { background: #17191D; }
  .graphic-charcoal-band { background: #24272D; }
  .graphic-ink { color: #F5F5F0; }
  .graphic-muted { color: #A7A9B2; }
  .graphic-accent { color: #A78BFA; }
  ```

- **Shapes:** near-square corners (border-radius 3–4px); `1.5px solid #F5F5F0` hairline borders on cards; a full-width charcoal hero band with a `1.5px` warm-white bottom rule.
- **Labels:** tiny uppercase, letter-spaced — ~11px, `letter-spacing: .12em` — "STEP 1", "STEP 2", in Zed purple.

## Check

1. **Titles-only** — the titles alone, top to bottom, tell the whole story.
2. **Two seconds** — each picture is grasped in two seconds with no tracing; every scene has at most four elements and one action.
3. **Cast** — the same symbols appear in every frame.
4. **Copy** — every subhead adds a fact; nothing on the page is framing.
5. **Delivery** — one self-contained HTML file saved to disk as `eli30-<topic>.html`, its path in the reply.
