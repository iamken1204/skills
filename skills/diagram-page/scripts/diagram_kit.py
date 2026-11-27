"""Components for bilingual (English / Traditional Chinese) diagram pages.

A Label is a str, shown in both languages, or an (english, chinese) tuple.
A "\n" inside a label breaks it onto several lines.

Typical build script:

    import sys; sys.path.insert(0, "<skill>/scripts")
    from diagram_kit import Diagram, write_page, steps_card

    d = Diagram(1200, 560, description=("...", "..."))
    server = d.box(300, 216, 248, 128, title=("Linux server", "Linux 伺服器"))
    d.wire([(170, 280), (server.left, 280)], label="Web UI")
    write_page("out.html", ("Title", "標題"), d)
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence, Union

Label = Union[str, tuple[str, str]]
Point = tuple[float, float]

SHELL_PATH = Path(__file__).resolve().parent.parent / "assets" / "page_shell.html"

# Arrow ends stop this far short of the target edge, so the arrowhead tip meets the edge.
ARROW_CLEARANCE = 2
WIRE_STROKE_WIDTH = 1.6
LINE_HEIGHT = 18
BOX_INSET = 16
TITLE_BASELINE = 27
SUBTITLE_BASELINE = 48
QTY_WIDTH, QTY_HEIGHT = 36, 22
STEP_RADIUS = 11

# tone -> (fill, stroke, text class)
TONES = {
    "neutral": ("var(--panel)", "var(--line)", ""),
    "vendor": ("var(--vendor-fill)", "var(--vendor-stroke)", "vk"),
    "customer": ("var(--customer-fill)", "var(--customer-stroke)", "ck"),
}


INK_COLOURS = {"neutral": "var(--fg)", "vendor": "var(--vendor-ink)", "customer": "var(--customer-ink)"}


def _number(value: float) -> str:
    rounded = round(value, 1)
    return str(int(rounded)) if rounded == int(rounded) else str(rounded)


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def _languages(label: Label) -> list[tuple[str, str]]:
    """Returns (text, language class) pairs; the class is empty for a shared label."""
    if isinstance(label, tuple):
        return [(label[0], "en"), (label[1], "tw")]
    return [(label, "")]


def pick(label: Label, language: str) -> str:
    if isinstance(label, tuple):
        return label[0] if language == "en" else label[1]
    return label


def estimate_width(label: Label, size: float = 13) -> float:
    """Rough rendered width of the longer language, for spacing legend entries."""
    def width(text: str) -> float:
        return sum(size if ord(ch) >= 0x2E80 else size * 0.58 for ch in text)
    return max(width(line) for text, _ in _languages(label) for line in text.split("\n"))


def _tone(tone: str) -> tuple[str, str, str]:
    if tone not in TONES:
        raise ValueError(f"unknown tone {tone!r}; use one of {sorted(TONES)}")
    return TONES[tone]


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.h

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2


@dataclass
class Diagram:
    """One SVG figure. Layers draw in order: zones, boxes, wires, marks."""

    width: int
    height: int
    description: Label
    min_width: int | None = None
    layers: dict[str, list[str]] = field(
        default_factory=lambda: {"zones": [], "boxes": [], "wires": [], "marks": []}
    )
    uses_wall: bool = False

    # ---- text -------------------------------------------------------------

    def text(self, x: float, y: float, label: Label, classes: str = "", anchor: str = "start",
             size: float | None = None, layer: str = "marks") -> None:
        anchor_attr = "" if anchor == "start" else f' text-anchor="{anchor}"'
        style_attr = f' style="font-size:{_number(size)}px"' if size else ""
        for text, language in _languages(label):
            class_names = " ".join(name for name in (classes, language) if name)
            class_attr = f' class="{class_names}"' if class_names else ""
            for index, line in enumerate(text.split("\n")):
                self.layers[layer].append(
                    f'<text x="{_number(x)}" y="{_number(y + index * LINE_HEIGHT)}"'
                    f'{anchor_attr}{class_attr}{style_attr}>{_escape(line)}</text>'
                )

    # ---- containers -------------------------------------------------------

    def zone(self, x: float, y: float, w: float, h: float, label: Label | None = None,
             tone: str = "neutral", note: Label | None = None) -> Box:
        """A grouping frame: a site, a network, or who owns what. Neutral zones are dashed."""
        _, stroke, ink = _tone(tone)
        if tone == "neutral":
            frame = 'style="fill:none;stroke:var(--zone)" stroke-width="1.5" stroke-dasharray="6 5"'
        else:
            frame = f'style="fill:none;stroke:{stroke}" stroke-width="2"'
        self.layers["zones"].append(
            f'<rect x="{_number(x)}" y="{_number(y)}" width="{_number(w)}" height="{_number(h)}" rx="12" {frame}/>'
        )
        if label is not None:
            self.text(x + BOX_INSET, y + 26, label, f"b {ink}".strip(), size=16, layer="zones")
        if note is not None:
            self.text(x + w - BOX_INSET, y + 26, note, "s", anchor="end", layer="zones")
        return Box(x, y, w, h)

    def box(self, x: float, y: float, w: float, h: float, title: Label | None = None,
            subtitle: Label | None = None, tone: str = "neutral", align: str = "start",
            rx: float = 10, filled: bool = True, dashed: bool = False, thick: bool = False,
            qty: str | None = None, icon: str | None = None, title_size: float = 15,
            title_classes: str = "b") -> Box:
        """A device, host or actor. align="middle" centres a lone title in the box.

        rx="pill" rounds the ends fully (people, external actors). icon="person"
        draws a person glyph before the title. qty puts a count badge top right.
        """
        fill, stroke, ink = _tone(tone)
        radius = h / 2 if rx == "pill" else rx
        fill_value = fill if filled else "none"
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.layers["boxes"].append(
            f'<rect x="{_number(x)}" y="{_number(y)}" width="{_number(w)}" height="{_number(h)}" '
            f'rx="{_number(radius)}" style="fill:{fill_value};stroke:{stroke}" '
            f'stroke-width="{2 if thick else 1.5}"{dash}/>'
        )
        text_x = x + BOX_INSET
        if icon == "person":
            glyph_x, glyph_y = x + 24, y + 24
            glyph_style = f'fill="none" style="stroke:{INK_COLOURS[tone]}" stroke-width="1.6"'
            self.layers["boxes"].append(
                f'<circle cx="{_number(glyph_x)}" cy="{_number(glyph_y)}" r="7" {glyph_style}/>'
                f'<path d="M{_number(glyph_x - 12)},{_number(glyph_y + 22)} a12,10 0 0 1 24,0" {glyph_style}/>'
            )
            text_x = x + 46
        elif icon is not None:
            raise ValueError(f"unknown icon {icon!r}; the only icon is 'person'")
        classes = f"{title_classes} {ink}".strip()
        if title is not None:
            if align == "middle":
                lines = max(len(text.split("\n")) for text, _ in _languages(title))
                baseline = y + h / 2 + title_size * 0.35 - (lines - 1) * LINE_HEIGHT / 2
                self.text(x + w / 2, baseline, title, classes, anchor="middle",
                          size=title_size, layer="boxes")
            else:
                self.text(text_x, y + TITLE_BASELINE, title, classes, size=title_size, layer="boxes")
        if subtitle is not None:
            if align == "middle":
                raise ValueError("a subtitle needs align='start'")
            self.text(text_x, y + SUBTITLE_BASELINE, subtitle, "s m", layer="boxes")
        if qty is not None:
            self.qty(x + w - 8 - QTY_WIDTH, y + 8, qty, tone)
        return Box(x, y, w, h)

    def chip(self, x: float, y: float, w: float, h: float, label: Label,
             tone: str = "vendor", solid: bool = False, subtitle: Label | None = None,
             size: float = 14) -> Box:
        """A software component inside a box. solid=True for a small, borderless chip."""
        fill, stroke, ink = _tone(tone)
        style = f"fill:{stroke}" if solid else f"fill:{fill};stroke:{stroke}"
        self.layers["boxes"].append(
            f'<rect x="{_number(x)}" y="{_number(y)}" width="{_number(w)}" height="{_number(h)}" '
            f'rx="6" style="{style}"/>'
        )
        classes = f"b {ink}".strip() + (" s" if size <= 13 else "")
        if subtitle is None:
            self.text(x + w / 2, y + h / 2 + size * 0.35, label, classes, anchor="middle",
                      size=None if size in (13, 14) else size, layer="boxes")
        else:
            self.text(x + BOX_INSET, y + TITLE_BASELINE, label, classes, size=16, layer="boxes")
            self.text(x + BOX_INSET, y + SUBTITLE_BASELINE, subtitle, "s m", layer="boxes")
        return Box(x, y, w, h)

    def wall(self, x: float, y: float, w: float, h: float, label: Label | None = None) -> Box:
        """A firewall or network boundary, drawn as bricks."""
        self.uses_wall = True
        self.layers["boxes"].append(
            f'<rect x="{_number(x)}" y="{_number(y)}" width="{_number(w)}" height="{_number(h)}" '
            f'rx="4" fill="url(#bricks)"/>'
        )
        if label is not None:
            self.text(x + w / 2, y - 10, label, "s b wk", anchor="middle", layer="boxes")
        return Box(x, y, w, h)

    # ---- connections ------------------------------------------------------

    def wire(self, points: Sequence[Point], arrow: str | None = "end", label: Label | None = None,
             label_pos: Point | None = None, label_anchor: str | None = None,
             muted_label: bool = False, dashed: bool = False, origin_dot: bool = False) -> None:
        """An orthogonal connection. Give exact edge coordinates; arrow ends are shortened for you.

        arrow is "end", "start", "both" or None. dashed=True draws a purple LAN-style link.
        The label sits 10 px above the longest horizontal run or 10 px left of a vertical one.
        """
        if arrow not in ("end", "start", "both", None):
            raise ValueError(f"arrow must be 'end', 'start', 'both' or None, not {arrow!r}")
        if len(points) < 2:
            raise ValueError("a wire needs at least two points")
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            if x1 != x2 and y1 != y2:
                raise ValueError(f"wire segment {(x1, y1)} -> {(x2, y2)} is diagonal; route it orthogonally")
        route = [list(point) for point in points]
        if arrow in ("end", "both"):
            _shorten(route[-1], route[-2])
        if arrow in ("start", "both"):
            _shorten(route[0], route[1])
        path = f"M{_number(route[0][0])},{_number(route[0][1])}"
        for (x1, y1), (x2, y2) in zip(route, route[1:]):
            path += f" H{_number(x2)}" if y1 == y2 else f" V{_number(y2)}"
        stroke = "var(--vendor-ink)" if dashed else "currentColor"
        dash = ' stroke-dasharray="5 5"' if dashed else ""
        markers = ""
        if arrow in ("end", "both"):
            markers += ' marker-end="url(#ah)"'
        if arrow in ("start", "both"):
            markers += ' marker-start="url(#ah)"'
        self.layers["wires"].append(
            f'<path d="{path}" fill="none" style="stroke:{stroke}" '
            f'stroke-width="{WIRE_STROKE_WIDTH}"{dash}{markers}/>'
        )
        if origin_dot:
            self.layers["wires"].append(
                f'<circle cx="{_number(points[0][0])}" cy="{_number(points[0][1])}" r="3.5" fill="currentColor"/>'
            )
        if label is not None:
            position, anchor = _label_position(points, label_pos, label_anchor)
            self.text(position[0], position[1], label, "s m" if muted_label else "s", anchor=anchor)

    def fanout(self, start: Point, trunk: float, ends: Sequence[Point], drops: str = "vertical",
               label: Label | None = None, label_pos: Point | None = None,
               label_anchor: str | None = None) -> None:
        """One source split to several targets through a shared trunk.

        drops="vertical": start runs to a horizontal trunk at y=trunk, then drops to each end.
        drops="horizontal": start runs to a vertical trunk at x=trunk, then runs to each end.
        """
        sx, sy = start
        if drops == "vertical":
            self.wire([(sx, sy), (sx, trunk)], arrow=None)
            xs = [sx] + [x for x, _ in ends]
            self.wire([(min(xs), trunk), (max(xs), trunk)], arrow=None)
            for x, y in ends:
                self.wire([(x, trunk), (x, y)])
        elif drops == "horizontal":
            self.wire([(sx, sy), (trunk, sy)], arrow=None)
            ys = [sy] + [y for _, y in ends]
            self.wire([(trunk, min(ys)), (trunk, max(ys))], arrow=None)
            for x, y in ends:
                self.wire([(trunk, y), (x, y)])
        else:
            raise ValueError("drops must be 'vertical' or 'horizontal'")
        if label is not None:
            if label_pos is None:
                raise ValueError("a fanout label needs label_pos")
            self.text(label_pos[0], label_pos[1], label, "s", anchor=label_anchor or "start")

    # ---- marks ------------------------------------------------------------

    def step(self, cx: float, cy: float, number: int, label: Label | None = None,
             label_pos: Point | None = None) -> None:
        """An orange order badge, usually sitting on the wire it numbers."""
        self.layers["marks"].append(
            f'<circle cx="{_number(cx)}" cy="{_number(cy)}" r="{STEP_RADIUS}" style="fill:var(--step)"/>'
        )
        self.text(cx, cy + 4.5, str(number), "sk", anchor="middle")
        if label is not None:
            x, y = label_pos if label_pos is not None else (cx + 20, cy - 8)
            self.text(x, y, label, "s")

    def qty(self, x: float, y: float, value: str, tone: str = "customer") -> None:
        """A count badge such as ×1 or ×3."""
        _, stroke, ink = _tone(tone)
        background = "var(--code-bg)" if tone == "neutral" else stroke
        self.layers["marks"].append(
            f'<rect x="{_number(x)}" y="{_number(y)}" width="{QTY_WIDTH}" height="{QTY_HEIGHT}" '
            f'rx="6" style="fill:{background}"/>'
        )
        self.text(x + QTY_WIDTH / 2, y + 16, value, f"b {ink}".strip(), anchor="middle", size=13)

    def legend(self, x: float, y: float, entries: Sequence[tuple[str, Label]], gap: float = 40) -> None:
        """A row of keys. Each entry is (kind, label); kind is a tone, "dashed" or "step"."""
        cursor = x
        for kind, label in entries:
            if kind == "step":
                self.layers["marks"].append(
                    f'<circle cx="{_number(cursor + 10)}" cy="{_number(y + 10)}" r="{STEP_RADIUS}" '
                    f'style="fill:var(--step)"/>'
                )
                self.text(cursor + 10, y + 14.5, "1", "sk", anchor="middle")
            elif kind == "dashed":
                self.layers["marks"].append(
                    f'<rect x="{_number(cursor)}" y="{_number(y)}" width="20" height="20" rx="5" '
                    f'style="fill:none;stroke:var(--zone)" stroke-width="1.5" stroke-dasharray="4 3"/>'
                )
            else:
                fill, stroke, _ = _tone(kind)
                self.layers["marks"].append(
                    f'<rect x="{_number(cursor)}" y="{_number(y)}" width="20" height="20" rx="5" '
                    f'style="fill:{fill};stroke:{stroke}" stroke-width="1.5"/>'
                )
            self.text(cursor + 28, y + 14.5, label, "s")
            cursor += 28 + estimate_width(label) + gap

    # ---- output -----------------------------------------------------------

    def render(self) -> str:
        minimum = self.min_width if self.min_width is not None else int(self.width * 0.8)
        defs = [
            '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
            'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker>'
        ]
        if self.uses_wall:
            defs.append(
                '<pattern id="bricks" width="16" height="12" patternUnits="userSpaceOnUse">'
                '<rect width="16" height="12" style="fill:var(--wall)"/>'
                '<path d="M0,6 H16 M8,0 V6 M0,6 V12 M16,6 V12" style="stroke:var(--bg);stroke-width:1.2" fill="none"/>'
                '</pattern>'
            )
        english, chinese = pick(self.description, "en"), pick(self.description, "tw")
        lines = [
            f'<svg class="diagram" viewBox="0 0 {self.width} {self.height}" style="min-width:{minimum}px" role="img"',
            f'     aria-label="{_escape(english)}"',
            f'     data-label-en="{_escape(english)}"',
            f'     data-label-tw="{_escape(chinese)}">',
            f'  <defs>{"".join(defs)}</defs>',
        ]
        for layer in ("zones", "boxes", "wires", "marks"):
            lines.extend("  " + element for element in self.layers[layer])
        lines.append("</svg>")
        return "\n".join(lines)


def _shorten(end: list[float], previous: list[float]) -> None:
    if end[0] == previous[0]:
        end[1] += ARROW_CLEARANCE if previous[1] > end[1] else -ARROW_CLEARANCE
    else:
        end[0] += ARROW_CLEARANCE if previous[0] > end[0] else -ARROW_CLEARANCE


def _label_position(points: Sequence[Point], label_pos: Point | None,
                    label_anchor: str | None) -> tuple[Point, str]:
    if label_pos is not None:
        return label_pos, label_anchor or "middle"
    segments = list(zip(points, points[1:]))
    horizontal = [s for s in segments if s[0][1] == s[1][1]]
    if horizontal:
        (x1, y), (x2, _) = max(horizontal, key=lambda s: abs(s[1][0] - s[0][0]))
        return ((x1 + x2) / 2, y - 10), label_anchor or "middle"
    (x, y1), (_, y2) = max(segments, key=lambda s: abs(s[1][1] - s[0][1]))
    return (x - 10, (y1 + y2) / 2 + 5), label_anchor or "end"


# ---- cards below the diagram ------------------------------------------------

@dataclass
class Card:
    kind: str
    title: Label
    body: list
    tone: str | None = None
    wide: bool = False
    note: Label | None = None


@dataclass(frozen=True)
class TableGroup:
    """A bold heading row inside a table card."""
    label: Label


def items_card(title: Label, items: Sequence[tuple[str, Label, Label | None]],
               tone: str | None = None, wide: bool = False, note: Label | None = None) -> Card:
    """A checklist of what someone supplies: (quantity such as "×2" or "✓", name, detail)."""
    return Card("items", title, list(items), tone, wide, note)


def steps_card(title: Label, steps: Sequence[tuple[Label | None, Label]], wide: bool = True,
               note: Label | None = None) -> Card:
    """Numbered steps that match the step badges in the diagram: (lead word or None, text)."""
    return Card("steps", title, list(steps), None, wide, note)


def facts_card(title: Label, facts: Sequence[Label], wide: bool = False,
               note: Label | None = None) -> Card:
    return Card("facts", title, list(facts), None, wide, note)


def table_card(title: Label, columns: Sequence[Label], rows: Sequence, wide: bool = True,
               note: Label | None = None) -> Card:
    """rows holds lists of cells (the first cell is the row heading) and TableGroup headings."""
    return Card("table", title, [list(columns), list(rows)], None, wide, note)


def _inline(label: Label, language: str) -> str:
    """Escapes text and turns `backticks` into <code>."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", _escape(pick(label, language)))


def _render_card(card: Card, language: str) -> str:
    classes = ["card", language]
    if card.wide:
        classes.append("wide")
    if card.tone in ("vendor", "customer"):
        classes.append(f"own-{card.tone}")
    out = [f'<section class="{" ".join(classes)}">', f"<h2>{_inline(card.title, language)}</h2>"]
    if card.kind == "items":
        out.append('<ul class="items">')
        for quantity, name, detail in card.body:
            detail_html = f'<br><span class="det">{_inline(detail, language)}</span>' if detail else ""
            out.append(f'<li><span class="qty">{_escape(quantity)}</span><span>'
                       f'<span class="who">{_inline(name, language)}</span>{detail_html}</span></li>')
        out.append("</ul>")
    elif card.kind == "steps":
        out.append('<ol class="steps">')
        for number, (lead, text) in enumerate(card.body, start=1):
            lead_html = f'<span class="who">{_inline(lead, language)}</span> ' if lead else ""
            out.append(f'<li><span class="badge">{number}</span><span>{lead_html}{_inline(text, language)}</span></li>')
        out.append("</ol>")
    elif card.kind == "facts":
        out.append('<ul class="facts">')
        out.extend(f"<li>{_inline(fact, language)}</li>" for fact in card.body)
        out.append("</ul>")
    elif card.kind == "table":
        columns, rows = card.body
        out.append('<div class="tablewrap"><table class="spec"><thead><tr>')
        out.extend(f'<th scope="col">{_inline(column, language)}</th>' for column in columns)
        out.append("</tr></thead><tbody>")
        for row in rows:
            if isinstance(row, TableGroup):
                out.append(f'<tr class="group"><th colspan="{len(columns)}">{_inline(row.label, language)}</th></tr>')
                continue
            heading, *cells = row
            out.append(f'<tr><th scope="row">{_inline(heading, language)}</th>'
                       + "".join(f"<td>{_inline(cell, language)}</td>" for cell in cells) + "</tr>")
        out.append("</tbody></table></div>")
    else:
        raise ValueError(f"unknown card kind {card.kind!r}")
    if card.note is not None:
        out.append(f'<p class="note">{_inline(card.note, language)}</p>')
    out.append("</section>")
    return "\n".join(out)


def _bilingual_block(tag: str, label: Label, attributes: str = "") -> str:
    return "\n".join(
        f'<{tag} class="{language}"{attributes}>{_inline(label, language)}</{tag}>'
        for language in ("en", "tw")
    )


def write_page(path: str | Path, title: Label, diagram: Diagram, lead: Label | None = None,
               caption: Label | None = None, card_rows: Sequence[Sequence[Card]] = ()) -> Path:
    """Writes the full page: header, language switch, diagram, caption and card grids."""
    header = _bilingual_block("h1", title)
    if lead is not None:
        header += "\n" + _bilingual_block("p", lead)
    caption_html = _bilingual_block("figcaption", caption) if caption is not None else ""
    sections = []
    for row in card_rows:
        cards = "\n".join(_render_card(card, language) for card in row for language in ("en", "tw"))
        sections.append(f'  <div class="grid">\n{cards}\n  </div>')
    page = (
        SHELL_PATH.read_text(encoding="utf-8")
        .replace("{{DOCUMENT_TITLE}}", _escape(pick(title, "en")))
        .replace("{{HEADER}}", header)
        .replace("{{DIAGRAM}}", diagram.render())
        .replace("{{CAPTION}}", caption_html)
        .replace("{{SECTIONS}}", "\n".join(sections))
    )
    output = Path(path)
    output.write_text(page, encoding="utf-8")
    return output
