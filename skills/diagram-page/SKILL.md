---
name: diagram-page
description: Build a bilingual (English / 繁體中文) HTML page with one architecture, deployment or topology diagram in the house style — purple for what the vendor provides, green for what the customer prepares, orange step badges, EN/中文 switch, cards below. Use when the user asks for a deployment diagram, architecture diagram, topology, "畫圖", 部署圖 or 架構圖.
---

Every page is produced by a **build script** that calls `scripts/diagram_kit.py`; the page shell, colours, fonts and the language switch live in `assets/page_shell.html` and are never written by hand. Then `scripts/verify_diagram.mjs` measures the page in Chromium. The script, not the HTML, is the source: to change a page, edit its script and rebuild.

`<skill>` below is this skill's directory.

## Steps

1. **Settle the content.** Write down: the page's one point as a sentence; every node (device, host, person, software) with its owner; every connection with what travels on it; the order of work if there is one. Each fact goes in exactly one place: the diagram carries topology and ownership, the cards carry detail (specs, accounts, quantities, steps). Write both languages now; for the Chinese, follow the `tw-speak` skill. Done when every node and wire has an English and a Chinese label.

2. **Lay out on paper.** Pick the archetype from the examples: flow (`examples/build_rpa_deployment_overview.py`: actor → server → fan-out to units → targets, left to right) or ownership (`examples/build_trial_deployment_plan.py`: a vendor zone on the left, a customer zone on the right, numbered install steps on the wires). Read the example you pick before writing code. Give each column and row a coordinate on the 8 px grid, and give repeated units one constant pitch. Done when every box has x, y, w, h chosen.

3. **Write the build script** beside the output page as `build_<page_name>.py` (the page `site-plan.html` gets `build_site_plan.py`). Start it with `sys.path.insert(0, "<skill>/scripts")`. Take wire endpoints from the `Box` that `box()` returns (`server.left`, `pc.right`, `unit.cy`); keep repeated geometry in named constants and loops. Done when `python3 build_<page_name>.py` writes the page.

4. **Verify.** Run `node <skill>/scripts/verify_diagram.mjs <page>.html --output-dir <scratch dir>`. Fix every `ERROR` in the build script and rerun until it prints `PASS`. Judge each `WARN` and fix it unless it is deliberate. Then read `<page>-diagram-en.png`, `-tw.png` and `-en-dark.png` and look for what the checker cannot see: uneven gaps, a wire that doubles back, a label far from its wire, a zone with a large empty area. Done when the checker passes and all three images read cleanly.

5. **Report** the page path, the build script path, the checker result, and show the English diagram image.

## Visual language

| Meaning | How | Kit call |
|---|---|---|
| What the vendor (we) provide or install, including our software | purple fill, purple ink | `tone="vendor"`, `chip()` |
| What the customer prepares or owns | green fill, green ink | `tone="customer"` |
| Plain device, person or host with no ownership point | white panel, grey border | `tone="neutral"` |
| A site, network or group | dashed grey frame; a solid coloured frame when the group is an owner | `zone()` |
| Something that exists already, or is optional | dashed border, no fill | `box(..., filled=False, dashed=True)` |
| Order of work | orange numbered badge on the wire it numbers, same numbers in a steps card | `step()`, `steps_card()` |
| How many | ×N badge at the top right of the box | `box(..., qty="×1")`, `qty()` |
| Firewall or network boundary | brick wall | `wall()` |
| A LAN or logical link, rather than a cable or a call | purple dashed wire | `wire(..., dashed=True)` |

Say what the colours mean in the header `lead` and repeat them in a `legend()` whenever both vendor and customer tones appear.

## Layout rules the kit does not enforce

- Flow runs left to right; a second level (cables to target devices, say) runs downward.
- Wires are orthogonal (the kit rejects diagonals) and end exactly on a box edge; the kit shortens arrow ends for the arrowhead.
- Wire labels are verbs or what travels: "Dispatch execution", "web page", "HDMI + USB cables". Box titles are nouns.
- One box title per box. A second line goes in `subtitle` (muted, 13 px). Specs longer than a few words go in a card.
- The viewBox is as wide as the content needs (1200–1600 is typical) with 24–32 px of margin; `min_width` defaults to 80% of it, which sets where horizontal scrolling begins.
- Size boxes to the longer of the two languages. English usually runs longer, but the checker measures both.
- The figure caption states the one exception or caveat the diagram cannot show; leave it out when there is none.

## Cards

`write_page(..., card_rows=[[card, card], [wide_card]])`, where each inner list is one two-column grid row. Use `items_card` for who supplies what (with `tone` matching the zone), `steps_card` for ordered work, `facts_card` for short points and `table_card` (with `TableGroup` headings) for specifications. Text in cards may use `backticks` for code.
