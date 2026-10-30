"""Build the business-card SVGs, QR, and print PDF.

Not imported by the Nuxt app. From the repo root:

    python print/business-card/render.py

Requires reportlab and segno (pip install reportlab segno).
Those are not project dependencies.
"""

from __future__ import annotations

import base64
import math
from pathlib import Path

import segno
from reportlab.lib.colors import CMYKColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
URL = "https://antonis-skarlatos.vercel.app"

TRIM_W = 90.0
TRIM_H = 50.0
BLEED = 3.0
SLUG = 5.0
SAFE = 5.0

# Screen colours. The PDF prints type, icons, and the QR as 100% K.
INK_HEX = "#14120e"
PAPER_HEX = "#f3efe4"
K = CMYKColor(0, 0, 0, 1)
PAPER = CMYKColor(0, 0, 0, 0)

# Shared left edge of the words. The front rule stops at the right column.
TEXT_X = 6.1
COLUMN = 58.0
TEXT_RIGHT = COLUMN - 0.8
SERIF = "GentiumBookPlus"
SERIF_CSS = "Gentium Book Plus"
SERIF_FILE = "GentiumBookPlus-Regular.ttf"
SANS = "Manrope"
MONO = "JetBrainsMono"

NAME = "Αντώνης Σκαρλάτος"
ROLE = "ΠΑΡΟΧΗ ΥΠΗΡΕΣΙΩΝ ΠΛΗΡΟΦΟΡΙΚΗΣ & ΛΟΓΙΣΜΙΚΟΥ"
SERVICES = (
    "Ιστοσελίδες & E-shops",
    "Εφαρμογές κατά παραγγελία",
    "Συμβουλές συστημάτων & λογισμικού",
    "Έξυπνες Κάρτες QR & NFC",
)
CONTACTS = (
    ("mail", "antwnis_skarlatos@yahoo.com"),
    ("phone", "6983696885"),
    ("pin", "Αθήνα, 162 32"),
)
CAPTION = "SCAN ME"
FOOTER = "Web & Digital Solutions"

ICON = 3.2
ICON_GAP = 1.55
ICON_STROKE = 0.22
QR_CLEAR = 4.0
QR_RIGHT = 5.5
RULE = 0.18
FRONT_RULE = 0.11
MARK_STROKE = 0.32
# Pasted arrow icon (pointer.png), tall chevron pointing right.
POINTER_W = 1.40
POINTER_H = POINTER_W * (500 / 448)

MM = 72 / 25.4

def _phone_handset() -> tuple:
    """Classic receiver: a bowed grip with round ear and mouth ends."""

    def quad(p0, p1, p2, t):
        u = 1 - t
        return (
            u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1],
        )

    def dquad(p0, p1, p2, t):
        return (
            2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]),
            2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1]),
        )

    def unit(x, y):
        length = math.hypot(x, y) or 1.0
        return x / length, y / length

    ear = (0.32, 0.24)
    mouth = (0.76, 0.76)
    mid = ((ear[0] + mouth[0]) / 2, (ear[1] + mouth[1]) / 2)
    dx, dy = mouth[0] - ear[0], mouth[1] - ear[1]
    px, py = unit(-dy, dx)
    grip = (mid[0] + 0.20 * px, mid[1] + 0.20 * py)
    steps = 16

    def half_width(t):
        # Wider at the ear and the mouth, narrower through the grip.
        return 0.078 + (0.125 - 0.078) * (2 * t - 1) ** 2

    samples = []
    for index in range(steps + 1):
        t = index / steps
        pos = quad(ear, grip, mouth, t)
        tx_, ty_ = dquad(ear, grip, mouth, t)
        nx, ny = unit(-ty_, tx_)
        samples.append((pos, (nx, ny), half_width(t)))

    def cap(pos, normal, outward, radius):
        start = math.atan2(normal[1], normal[0])
        end_target = math.atan2(-normal[1], -normal[0])
        through = math.atan2(outward[1], outward[0])
        best = None
        for positive in (True, False):
            end = end_target
            if positive:
                while end < start:
                    end += 2 * math.pi
            else:
                while end > start:
                    end -= 2 * math.pi
            mid_a = start + (end - start) / 2
            delta = (through - mid_a + math.pi) % (2 * math.pi) - math.pi
            if best is None or abs(delta) < best[0]:
                best = (abs(delta), end)
        span = best[1] - start
        count = max(5, math.ceil(abs(span) / (math.pi / 7)))
        points = []
        for index in range(1, count + 1):
            angle = start + span * index / count
            points.append((pos[0] + radius * math.cos(angle), pos[1] + radius * math.sin(angle)))
        return points

    left = [(pos[0] + normal[0] * hw, pos[1] + normal[1] * hw) for pos, normal, hw in samples]
    right = [(pos[0] - normal[0] * hw, pos[1] - normal[1] * hw) for pos, normal, hw in samples]
    end_dir = unit(*dquad(ear, grip, mouth, 1))
    start_dir = unit(*dquad(ear, grip, mouth, 0))
    points = [left[0]]
    points.extend(left[1:])
    points.extend(cap(samples[-1][0], samples[-1][1], end_dir, samples[-1][2]))
    points.extend(reversed(right[:-1]))
    points.extend(cap(samples[0][0], (-samples[0][1][0], -samples[0][1][1]), (-start_dir[0], -start_dir[1]), samples[0][2]))
    cmds = [("M", round(points[0][0], 3), round(points[0][1], 3))]
    cmds.extend(("L", round(x, 3), round(y, 3)) for x, y in points[1:])
    cmds.append(("Z",))
    return tuple(cmds)


# Outline icons in a unit box, y downward. Paths are inset so the stroke
# stays inside the box. A dot is a filled circle in the same box.
ICONS = {
    "mail": {
        "paths": (
            (
                ("M", 0.16, 0.32),
                ("L", 0.84, 0.32),
                ("L", 0.84, 0.78),
                ("L", 0.16, 0.78),
                ("Z",),
            ),
            (
                ("M", 0.16, 0.32),
                ("L", 0.50, 0.56),
                ("L", 0.84, 0.32),
            ),
        ),
        "dots": (),
    },
    "phone": {
        "paths": (_phone_handset(),),
        "dots": (),
    },
    "pin": {
        "paths": (
            (
                ("M", 0.50, 0.90),
                ("C", 0.50, 0.90, 0.22, 0.60, 0.22, 0.40),
                ("C", 0.22, 0.22, 0.34, 0.12, 0.50, 0.12),
                ("C", 0.66, 0.12, 0.78, 0.22, 0.78, 0.40),
                ("C", 0.78, 0.60, 0.50, 0.90, 0.50, 0.90),
                ("Z",),
            ),
        ),
        "dots": ((0.50, 0.38, 0.10),),
    },
}


def pt_mm(pt: float) -> float:
    return pt * 25.4 / 72


def mm_pt(mm: float) -> float:
    return mm * MM


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont(SERIF, str(FONTS / SERIF_FILE)))
    pdfmetrics.registerFont(TTFont(SANS, str(FONTS / "Manrope-Regular.ttf")))
    pdfmetrics.registerFont(TTFont(MONO, str(FONTS / "JetBrainsMono-Regular.ttf")))


def text_width(text: str, font: str, pt: float, tracking_em: float = 0) -> float:
    width = pt_mm(pdfmetrics.stringWidth(text, font, pt))
    if tracking_em and len(text) > 1:
        width += (len(text) - 1) * tracking_em * pt_mm(pt)
    return width


def tx(x_mm: float) -> float:
    return mm_pt(SLUG + BLEED + x_mm)


def ty(y_from_top: float) -> float:
    return mm_pt(SLUG + BLEED + (TRIM_H - y_from_top))


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fits(text: str, font: str, pt: float, x: float, tracking_em: float = 0, right: float | None = None) -> bool:
    limit = TRIM_W - SAFE if right is None else right
    return x + text_width(text, font, pt, tracking_em) <= limit + 0.05


def shrink_pt(text: str, font: str, pt: float, floor: float, x: float, step: float = 0.5, tracking_em: float = 0, right: float | None = None) -> float:
    while pt > floor and not fits(text, font, pt, x, tracking_em, right):
        pt = round(pt - step, 2)
    return pt


def fit_tracked(
    text: str,
    font: str,
    pt: float,
    floor: float,
    tracking: float,
    x: float,
    right: float,
    min_tracking: float = 0.0,
) -> tuple[float, float]:
    """Drop tracking before the size falls through the floor."""
    size = pt
    track = tracking
    while not fits(text, font, size, x, track, right=right):
        if track > min_tracking + 0.001:
            track = round(max(min_tracking, track - 0.02), 2)
            continue
        if size <= floor:
            return size, track
        size = round(size - 0.25, 2)
        track = tracking
    return size, track


def qr_matrix() -> list[list[int]]:
    code = segno.make(URL, error="q")
    modules = [list(row) for row in code.matrix]
    border = 4
    n = len(modules)
    size = n + border * 2
    padded = [[0] * size for _ in range(size)]
    for y, row in enumerate(modules):
        for x, cell in enumerate(row):
            padded[y + border][x + border] = 1 if cell else 0
    return padded


# Ink outside the baseline, mm per point, measured from the shipped fonts.
INK = {
    "serif-name": (0.283, 0.082),
    "sans-role": (0.260, 0.012),
    "sans-service": (0.276, 0.085),
    "mono": (0.277, 0.064),
}


def ink(kind: str, pt: float) -> tuple[float, float]:
    above, below = INK[kind]
    return above * pt, below * pt


def front_layout(name_font: str = SERIF, name_css: str | None = SERIF_CSS) -> dict:
    name_pt = shrink_pt(NAME, name_font, 16.0, 13.0, TEXT_X, step=0.25, tracking_em=-0.02, right=TEXT_RIGHT)
    role_pt, role_track = fit_tracked(ROLE, SANS, 6.75, 5.75, 0.0, TEXT_X, TEXT_RIGHT, min_tracking=-0.02)
    service_x = TEXT_X + 2.55
    service_pt = 8.0
    longest = max(SERVICES, key=lambda line: text_width(line, SANS, service_pt))
    service_pt = shrink_pt(longest, SANS, service_pt, 7.0, service_x, step=0.25, right=TEXT_RIGHT)

    name_above, name_below = ink("serif-name", name_pt)
    role_above, role_below = ink("sans-role", role_pt)
    service_above, service_below = ink("sans-service", service_pt)

    name_to_role = 1.35
    role_to_rule = 2.75
    rule_to_list = 2.2
    between = 0.85
    block = (
        name_above
        + name_below
        + name_to_role
        + role_above
        + role_below
        + role_to_rule
        + FRONT_RULE
        + rule_to_list
        + 4 * (service_above + service_below)
        + 3 * between
    )
    top = (TRIM_H - block) / 2
    lift = TRIM_H * 0.10
    name_baseline = top + name_above - lift
    role_baseline = name_baseline + name_below + name_to_role + role_above
    # Keep the list where the earlier 10% drop put it (from the unraised header).
    unraised_role = top + name_above + name_below + name_to_role + role_above
    unraised_rule = unraised_role + role_below + role_to_rule
    service_1 = unraised_rule + FRONT_RULE + rule_to_list + service_above + lift
    service_step = service_below + between + service_above
    role_bottom = role_baseline + role_below
    service_top = service_1 - service_above
    rule_y = (role_bottom + service_top) / 2

    mark_right = TRIM_W - SAFE
    mark_span = mark_right - COLUMN
    mark_d = min(18.5, mark_span - 3.0, TRIM_H - 2 * SAFE - 0.8)
    mark_cx = min(COLUMN + mark_span / 2 + 2.2, mark_right - mark_d / 2)
    mark_cy = TRIM_H / 2
    return {
        "name_font": name_font,
        "name_css": name_css or name_font,
        "name_pt": name_pt,
        "name_baseline": name_baseline,
        "role_pt": role_pt,
        "role_track": role_track,
        "role_baseline": role_baseline,
        "rule_y": rule_y,
        "service_pt": service_pt,
        "service_x": service_x,
        "service_baselines": tuple(service_1 + i * service_step for i in range(4)),
        "service_above": service_above,
        "service_below": service_below,
        "mark_cx": mark_cx,
        "mark_cy": mark_cy,
        "mark_d": mark_d,
    }


def contact_layout() -> dict:
    value_pt = 8.0
    caption_pt = 7.5
    footer_pt = 6.5
    footer_track = 0.0
    qr = 24.0
    value_x = TEXT_X + ICON + ICON_GAP
    email = CONTACTS[0][1]

    def qr_x_for(size: float) -> float:
        return TRIM_W - QR_RIGHT - size

    while value_pt > 6.5 and not fits(email, MONO, value_pt, value_x, right=qr_x_for(qr) - QR_CLEAR):
        value_pt = round(value_pt - 0.25, 2)
    if not fits(email, MONO, value_pt, value_x, right=qr_x_for(qr) - QR_CLEAR):
        qr = 22.0

    qr_x = qr_x_for(qr)
    value_above, value_below = ink("mono", value_pt)
    foot_above, foot_below = ink("mono", footer_pt)
    cap_above, cap_below = ink("sans-service", caption_pt)
    caption_gap = 0.75
    caption_w = text_width(CAPTION, SANS, caption_pt)

    row = max(ICON, value_above + value_below)
    # Match the front service-list rhythm (between = 0.85).
    row_gap = 0.85
    rows_h = 3 * row + 2 * row_gap
    footer_gap = 1.7
    footer_baseline = TRIM_H - SAFE - foot_below - 0.2
    rule_y = footer_baseline - foot_above - footer_gap
    area_top = 7.0
    area_bottom = rule_y - 3.5
    contact_top = area_top + max(0.0, area_bottom - area_top - rows_h) / 2

    rows = []
    for index, (kind, value) in enumerate(CONTACTS):
        slot_top = contact_top + index * (row + row_gap)
        center = slot_top + row / 2
        baseline = center + (value_above - value_below) / 2
        text_cy = baseline - pt_mm(value_pt) * 0.36
        rows.append(
            {
                "icon": kind,
                "value": value,
                "baseline": baseline,
                "icon_top": text_cy - ICON / 2,
            }
        )

    email_w = text_width(email, MONO, value_pt)
    rule_right = value_x + email_w
    # QR on the right; caption middle-anchored under it.
    right_h = qr + caption_gap + cap_above + cap_below
    qr_y = (TRIM_H - right_h) / 2
    caption_cx = qr_x + qr / 2
    caption_x = caption_cx - caption_w / 2
    caption_baseline = qr_y + qr + caption_gap + cap_above

    return {
        "value_pt": value_pt,
        "value_x": value_x,
        "rows": rows,
        "rule_y": rule_y,
        "rule_right": rule_right,
        "footer_pt": footer_pt,
        "footer_track": footer_track,
        "footer_baseline": footer_baseline,
        "qr": qr,
        "qr_x": qr_x,
        "qr_y": qr_y,
        "caption_pt": caption_pt,
        "caption_cx": caption_cx,
        "caption_x": caption_x,
        "caption_baseline": caption_baseline,
        "caption_w": caption_w,
    }


def svg_font_css() -> str:
    return f"""
    @font-face {{
      font-family: "{SERIF_CSS}";
      src: url("fonts/{SERIF_FILE}") format("truetype");
      font-weight: 400;
    }}
    @font-face {{
      font-family: "Manrope";
      src: url("fonts/Manrope-Regular.ttf") format("truetype");
      font-weight: 400;
    }}
    @font-face {{
      font-family: "JetBrains Mono";
      src: url("fonts/JetBrainsMono-Regular.ttf") format("truetype");
      font-weight: 400;
    }}
    text {{ fill: #14120e; }}
    """


def svg_text(
    text: str,
    family: str,
    pt: float,
    x: float,
    y: float,
    tracking_em: float = 0,
    fill: str | None = None,
    css_class: str | None = None,
    anchor: str | None = None,
) -> str:
    size = pt_mm(pt)
    spacing = f' letter-spacing="{tracking_em * size:.4f}"' if tracking_em else ""
    # Class + inline style: the global `text { fill }` rule otherwise wins.
    cls = f' class="{css_class}"' if css_class else ""
    color = f' style="fill:{fill}"' if fill else ""
    mid = f' text-anchor="{anchor}"' if anchor else ""
    return (
        f'<text x="{x:.3f}" y="{y:.3f}"{cls}{color}{mid} '
        f'font-family="{family}" font-size="{size:.4f}"{spacing}>'
        f"{esc(text)}</text>"
    )


_POINTER_DATA_URI: str | None = None


def pointer_data_uri() -> str:
    """Inline the arrow so <img src=\"front.svg\"> still shows it (no external href)."""
    global _POINTER_DATA_URI
    if _POINTER_DATA_URI is None:
        raw = (ROOT / "pointer.png").read_bytes()
        _POINTER_DATA_URI = "data:image/png;base64," + base64.b64encode(raw).decode("ascii")
    return _POINTER_DATA_URI


def svg_pointer(cx: float, cy: float) -> str:
    x = cx - POINTER_W / 2
    y = cy - POINTER_H / 2
    href = pointer_data_uri()
    return (
        f'<image href="{href}" x="{x:.3f}" y="{y:.3f}" '
        f'width="{POINTER_W:.3f}" height="{POINTER_H:.3f}"/>'
    )


def svg_rule(x1: float, x2: float, y: float, stroke: float = RULE) -> str:
    return (
        f'<line x1="{x1:.3f}" y1="{y:.3f}" x2="{x2:.3f}" y2="{y:.3f}" '
        f'stroke="{INK_HEX}" stroke-width="{stroke:.3f}"/>'
    )


def path_d(cmds: tuple, x: float, y: float, size: float) -> str:
    parts = []
    for cmd in cmds:
        if cmd[0] == "Z":
            parts.append("Z")
        elif cmd[0] == "M":
            parts.append(f"M{x + cmd[1] * size:.3f} {y + cmd[2] * size:.3f}")
        elif cmd[0] == "L":
            parts.append(f"L{x + cmd[1] * size:.3f} {y + cmd[2] * size:.3f}")
        elif cmd[0] == "C":
            points = []
            for i in range(1, 7, 2):
                points.append(f"{x + cmd[i] * size:.3f} {y + cmd[i + 1] * size:.3f}")
            parts.append("C" + " ".join(points))
    return " ".join(parts)


def svg_icon(kind: str, x: float, y: float, size: float) -> str:
    icon = ICONS[kind]
    chunks = []
    for cmds in icon["paths"]:
        chunks.append(
            f'<path d="{path_d(cmds, x, y, size)}" fill="none" stroke="{INK_HEX}" '
            f'stroke-width="{ICON_STROKE:.3f}" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    for cx, cy, r in icon["dots"]:
        chunks.append(
            f'<circle cx="{x + cx * size:.3f}" cy="{y + cy * size:.3f}" r="{r * size:.3f}" fill="{INK_HEX}"/>'
        )
    return "\n  ".join(chunks)


def ellipse_d(cx: float, cy: float, rx: float, ry: float) -> str:
    k = 0.5522847498
    kx, ky = k * rx, k * ry
    return (
        f"M{cx + rx:.3f} {cy:.3f} "
        f"C{cx + rx:.3f} {cy + ky:.3f} {cx + kx:.3f} {cy + ry:.3f} {cx:.3f} {cy + ry:.3f} "
        f"C{cx - kx:.3f} {cy + ry:.3f} {cx - rx:.3f} {cy + ky:.3f} {cx - rx:.3f} {cy:.3f} "
        f"C{cx - rx:.3f} {cy - ky:.3f} {cx - kx:.3f} {cy - ry:.3f} {cx:.3f} {cy - ry:.3f} "
        f"C{cx + kx:.3f} {cy - ry:.3f} {cx + rx:.3f} {cy - ky:.3f} {cx + rx:.3f} {cy:.3f}"
    )


def globe_ellipses(cx: float, cy: float, r: float) -> tuple[tuple[float, float, float, float], ...]:
    """Wireframe globe matching the reference: 4 meridians + 5 parallels.

    Parallels are centred horizontal ellipses (equal north/south arcs) so
    the middle band never reads as tilted.
    """
    # Meridians first (vertical ellipses), then N→S latitudes.
    # depth ≈ visual thickness of each parallel ellipse.
    d = 0.34
    return (
        (cx, cy, r * 0.28, r * 0.985),
        (cx, cy, r * 0.50, r * 0.985),
        (cx, cy, r * 0.70, r * 0.985),
        (cx, cy, r * 0.88, r * 0.985),
        (cx, cy - r * 0.62, r * 0.78, r * 0.78 * d),
        (cx, cy - r * 0.32, r * 0.94, r * 0.94 * d),
        (cx, cy, r * 0.985, r * 0.985 * d),
        (cx, cy + r * 0.32, r * 0.94, r * 0.94 * d),
        (cx, cy + r * 0.62, r * 0.78, r * 0.78 * d),
    )


def svg_mark(layout: dict) -> str:
    cx = layout["mark_cx"]
    cy = layout["mark_cy"]
    r = layout["mark_d"] / 2
    lines = "\n    ".join(
        f'<path d="{ellipse_d(ex, ey, rx, ry)}" fill="none" stroke="{INK_HEX}" '
        f'stroke-width="0.22" stroke-linecap="round"/>'
        for ex, ey, rx, ry in globe_ellipses(cx, cy, r)
    )
    lines += (
        f'\n    <line x1="{cx:.3f}" y1="{cy - r:.3f}" x2="{cx:.3f}" y2="{cy + r:.3f}" '
        f'stroke="{INK_HEX}" stroke-width="0.22" stroke-linecap="round"/>'
    )
    return (
        f'<g clip-path="url(#globe-clip)">\n    {lines}\n  </g>\n  '
        f'<clipPath id="globe-clip"><circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r - 0.12:.3f}"/></clipPath>\n  '
        f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}" fill="none" '
        f'stroke="{INK_HEX}" stroke-width="{MARK_STROKE:.3f}"/>'
    )


def svg_document(title: str, body: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="90mm" height="50mm" viewBox="0 0 90 50" role="img" xml:lang="el">
  <title>{esc(title)}</title>
  <style><![CDATA[{svg_font_css()}]]></style>
  <!-- stock-preview is the cream paper. The print PDF does not ink this rectangle. -->
  <rect id="stock-preview" width="90" height="50" fill="{PAPER_HEX}"/>
  {body}
</svg>
"""


def write_qr_svg(matrix: list[list[int]]) -> None:
    n = len(matrix)
    dark = []
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                dark.append(f"M{x} {y}h1v1h-1z")
    path = " ".join(dark)
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" width="{n}" height="{n}" role="img">
  <title>QR {URL}</title>
  <rect id="stock-preview" width="{n}" height="{n}" fill="{PAPER_HEX}"/>
  <path fill="{INK_HEX}" d="{path}"/>
</svg>
"""
    (ROOT / "qr.svg").write_text(svg, encoding="utf-8")


def front_body(layout: dict) -> str:
    parts = [
        svg_text(
            NAME,
            layout.get("name_css", SERIF_CSS),
            layout["name_pt"],
            TEXT_X,
            layout["name_baseline"],
            -0.02,
        ),
        svg_text(ROLE, "Manrope", layout["role_pt"], TEXT_X, layout["role_baseline"], layout["role_track"]),
        svg_rule(TEXT_X, COLUMN, layout["rule_y"], FRONT_RULE),
        svg_mark(layout),
    ]
    for line, baseline in zip(SERVICES, layout["service_baselines"]):
        cy = baseline - pt_mm(layout["service_pt"]) * 0.36
        parts.append(svg_pointer(TEXT_X + 0.70, cy))
        parts.append(svg_text(line, "Manrope", layout["service_pt"], layout["service_x"], baseline))
    return "\n  ".join(parts)


def write_front_svg(layout: dict) -> None:
    (ROOT / "front.svg").write_text(
        svg_document("Αντώνης Σκαρλάτος — μπροστά", front_body(layout)),
        encoding="utf-8",
    )
    for stale in ("front-initials.svg", "front-watermark.svg"):
        path = ROOT / stale
        if path.exists():
            path.unlink()


def qr_group(layout: dict, matrix: list[list[int]], fill: str = INK_HEX) -> str:
    n = len(matrix)
    scale = layout["qr"] / n
    dark = []
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                dark.append(f"M{x} {y}h1v1h-1z")
    return (
        f'<g transform="translate({layout["qr_x"]:.3f} {layout["qr_y"]:.3f}) scale({scale:.6f})">'
        f'<path fill="{fill}" d="{" ".join(dark)}"/></g>'
    )


def write_back_svg(layout: dict, matrix: list[list[int]]) -> None:
    parts = [
        qr_group(layout, matrix, INK_HEX),
        svg_text(
            CAPTION,
            "Manrope",
            layout["caption_pt"],
            layout["caption_cx"],
            layout["caption_baseline"],
            anchor="middle",
        ),
        svg_rule(TEXT_X, layout["rule_right"], layout["rule_y"], FRONT_RULE),
        svg_text(
            FOOTER,
            "JetBrains Mono",
            layout["footer_pt"],
            TEXT_X,
            layout["footer_baseline"],
            layout["footer_track"],
        ),
    ]
    for row in layout["rows"]:
        parts.append(svg_icon(row["icon"], TEXT_X, row["icon_top"], ICON))
        parts.append(svg_text(row["value"], "JetBrains Mono", layout["value_pt"], layout["value_x"], row["baseline"]))
    body = "\n  ".join(parts)
    (ROOT / "back.svg").write_text(
        svg_document("Αντώνης Σκαρλάτος — πίσω", body),
        encoding="utf-8",
    )


def draw_text(
    c: canvas.Canvas,
    text: str,
    font: str,
    pt: float,
    x_mm: float,
    baseline: float,
    tracking_em: float = 0,
    fill=None,
    center: bool = False,
) -> None:
    c.setFillColor(K if fill is None else fill)
    c.setFont(font, pt)
    if center:
        c.drawCentredString(tx(x_mm), ty(baseline), text, charSpace=tracking_em * pt)
    else:
        c.drawString(tx(x_mm), ty(baseline), text, charSpace=tracking_em * pt)


def draw_pointer(c: canvas.Canvas, cx: float, cy: float) -> None:
    c.drawImage(
        str(ROOT / "pointer.png"),
        tx(cx - POINTER_W / 2),
        ty(cy + POINTER_H / 2),
        width=mm_pt(POINTER_W),
        height=mm_pt(POINTER_H),
        mask="auto",
        preserveAspectRatio=True,
    )


def draw_rule(c: canvas.Canvas, x1: float, x2: float, y: float, stroke: float = RULE) -> None:
    c.setStrokeColor(K)
    c.setLineWidth(mm_pt(stroke))
    c.setLineCap(0)
    c.line(tx(x1), ty(y), tx(x2), ty(y))


def add_path(path, cmds: tuple, x_mm: float, y_mm: float, size: float) -> None:
    for cmd in cmds:
        if cmd[0] == "Z":
            path.close()
        elif cmd[0] == "M":
            path.moveTo(tx(x_mm + cmd[1] * size), ty(y_mm + cmd[2] * size))
        elif cmd[0] == "L":
            path.lineTo(tx(x_mm + cmd[1] * size), ty(y_mm + cmd[2] * size))
        elif cmd[0] == "C":
            path.curveTo(
                tx(x_mm + cmd[1] * size),
                ty(y_mm + cmd[2] * size),
                tx(x_mm + cmd[3] * size),
                ty(y_mm + cmd[4] * size),
                tx(x_mm + cmd[5] * size),
                ty(y_mm + cmd[6] * size),
            )


def draw_icon(c: canvas.Canvas, kind: str, x_mm: float, y_mm: float, size: float) -> None:
    icon = ICONS[kind]
    c.setStrokeColor(K)
    c.setFillColor(K)
    c.setLineWidth(mm_pt(ICON_STROKE))
    c.setLineCap(1)
    c.setLineJoin(1)
    for cmds in icon["paths"]:
        path = c.beginPath()
        add_path(path, cmds, x_mm, y_mm, size)
        c.drawPath(path, stroke=1, fill=0)
    for cx, cy, r in icon["dots"]:
        c.circle(tx(x_mm + cx * size), ty(y_mm + cy * size), mm_pt(r * size), stroke=0, fill=1)


def stroke_ellipse(c: canvas.Canvas, cx: float, cy: float, rx: float, ry: float) -> None:
    k = 0.5522847498
    kx, ky = k * rx, k * ry
    path = c.beginPath()
    path.moveTo(tx(cx + rx), ty(cy))
    path.curveTo(tx(cx + rx), ty(cy + ky), tx(cx + kx), ty(cy + ry), tx(cx), ty(cy + ry))
    path.curveTo(tx(cx - kx), ty(cy + ry), tx(cx - rx), ty(cy + ky), tx(cx - rx), ty(cy))
    path.curveTo(tx(cx - rx), ty(cy - ky), tx(cx - kx), ty(cy - ry), tx(cx), ty(cy - ry))
    path.curveTo(tx(cx + kx), ty(cy - ry), tx(cx + rx), ty(cy - ky), tx(cx + rx), ty(cy))
    c.drawPath(path, stroke=1, fill=0)


def draw_mark(c: canvas.Canvas, layout: dict) -> None:
    cx = layout["mark_cx"]
    cy = layout["mark_cy"]
    r = layout["mark_d"] / 2
    c.saveState()
    c.setStrokeColor(K)
    c.setFillColor(K)
    c.setLineWidth(mm_pt(0.22))
    c.setLineCap(1)
    clip = c.beginPath()
    clip.circle(tx(cx), ty(cy), mm_pt(r - 0.12))
    c.clipPath(clip, stroke=0, fill=0)
    for ex, ey, rx, ry in globe_ellipses(cx, cy, r):
        stroke_ellipse(c, ex, ey, rx, ry)
    c.line(tx(cx), ty(cy - r), tx(cx), ty(cy + r))
    c.restoreState()
    c.setStrokeColor(K)
    c.setLineWidth(mm_pt(MARK_STROKE))
    c.circle(tx(cx), ty(cy), mm_pt(r), stroke=1, fill=0)


def draw_qr(c: canvas.Canvas, matrix: list[list[int]], layout: dict, fill=None) -> None:
    n = len(matrix)
    module = mm_pt(layout["qr"] / n)
    origin_x = tx(layout["qr_x"])
    origin_top = ty(layout["qr_y"])
    c.setFillColor(K if fill is None else fill)
    for row_i, row in enumerate(matrix):
        for col_i, cell in enumerate(row):
            if not cell:
                continue
            c.rect(
                origin_x + col_i * module,
                origin_top - (row_i + 1) * module,
                module,
                module,
                stroke=0,
                fill=1,
            )


def draw_crop_marks(c: canvas.Canvas, media_w: float, media_h: float) -> None:
    c.setStrokeColor(K)
    c.setFillColor(K)
    c.setLineWidth(0.25)
    c.setLineCap(0)
    inset = mm_pt(0.75)
    end = mm_pt(SLUG - 0.75)
    trim_left = tx(0)
    trim_right = tx(TRIM_W)
    trim_top = ty(0)
    trim_bottom = ty(TRIM_H)
    c.lines(
        [
            (inset, trim_bottom, end, trim_bottom),
            (media_w - end, trim_bottom, media_w - inset, trim_bottom),
            (inset, trim_top, end, trim_top),
            (media_w - end, trim_top, media_w - inset, trim_top),
            (trim_left, inset, trim_left, end),
            (trim_right, inset, trim_right, end),
            (trim_left, media_h - end, trim_left, media_h - inset),
            (trim_right, media_h - end, trim_right, media_h - inset),
        ]
    )


def draw_slug(c: canvas.Canvas, media_w: float, text: str) -> None:
    c.setFillColor(K)
    c.setFont(SANS, 6)
    c.drawCentredString(media_w / 2, mm_pt(1.7), text)


def trim_boxes(c: canvas.Canvas) -> None:
    trim = [tx(0), ty(TRIM_H), tx(TRIM_W), ty(0)]
    bleed = [
        mm_pt(SLUG),
        mm_pt(SLUG),
        mm_pt(SLUG + BLEED + TRIM_W + BLEED),
        mm_pt(SLUG + BLEED + TRIM_H + BLEED),
    ]
    c.setTrimBox(trim)
    c.setBleedBox(bleed)
    c.setArtBox(trim)


def write_pdf(front: dict, back: dict, matrix: list[list[int]]) -> None:
    media_w = mm_pt(TRIM_W + 2 * (BLEED + SLUG))
    media_h = mm_pt(TRIM_H + 2 * (BLEED + SLUG))
    path = ROOT / "antonis-skarlatos-card.pdf"
    c = canvas.Canvas(
        str(path),
        pagesize=(media_w, media_h),
        pageCompression=1,
        pdfVersion=(1, 6),
        enforceColorSpace="cmyk",
        lang="el",
        initialFontName=SANS,
        initialFontSize=6,
    )
    c.setTitle("Antonis Skarlatos — business card")
    c.setAuthor("Antonis Skarlatos")
    c.setSubject("Trim 90 x 50 mm. Bleed 3 mm. Page 1 front, page 2 back, flip on the long edge.")

    trim_boxes(c)
    name_font = front.get("name_font", SERIF)
    draw_text(c, NAME, name_font, front["name_pt"], TEXT_X, front["name_baseline"], -0.02)
    draw_text(c, ROLE, SANS, front["role_pt"], TEXT_X, front["role_baseline"], front["role_track"])
    draw_rule(c, TEXT_X, COLUMN, front["rule_y"], FRONT_RULE)
    draw_mark(c, front)
    for line, baseline in zip(SERVICES, front["service_baselines"]):
        cy = baseline - pt_mm(front["service_pt"]) * 0.36
        draw_pointer(c, TEXT_X + 0.70, cy)
        draw_text(c, line, SANS, front["service_pt"], front["service_x"], baseline)
    draw_crop_marks(c, media_w, media_h)
    draw_slug(c, media_w, "FRONT  ·  90 × 50 mm trim  ·  3 mm bleed")
    c.showPage()

    trim_boxes(c)
    draw_qr(c, matrix, back)
    draw_text(
        c,
        CAPTION,
        SANS,
        back["caption_pt"],
        back["caption_cx"],
        back["caption_baseline"],
        center=True,
    )
    draw_rule(c, TEXT_X, back["rule_right"], back["rule_y"], FRONT_RULE)
    draw_text(c, FOOTER, MONO, back["footer_pt"], TEXT_X, back["footer_baseline"], back["footer_track"])
    for row in back["rows"]:
        draw_icon(c, row["icon"], TEXT_X, row["icon_top"], ICON)
        draw_text(c, row["value"], MONO, back["value_pt"], back["value_x"], row["baseline"])
    draw_crop_marks(c, media_w, media_h)
    draw_slug(c, media_w, "BACK  ·  90 × 50 mm trim  ·  3 mm bleed  ·  flip on long edge")
    c.save()


def check_safe(front: dict, back: dict) -> None:
    problems = []

    def box(name: str, x: float, baseline: float, width: float, kind: str, pt: float, right_limit: float | None = None) -> None:
        above, below = ink(kind, pt)
        top = baseline - above
        bottom = baseline + below
        right = x + width
        limit = TRIM_W - SAFE if right_limit is None else right_limit
        if top < SAFE - 0.05 or bottom > TRIM_H - SAFE + 0.05 or x < SAFE - 0.05 or right > limit + 0.05:
            problems.append(f"{name}: x={x:.2f} top={top:.2f} right={right:.2f} bottom={bottom:.2f} limit={limit:.2f}")

    def rect(name: str, x: float, y: float, w: float, h: float) -> None:
        if x < SAFE - 0.05 or y < SAFE - 0.05 or x + w > TRIM_W - SAFE + 0.05 or y + h > TRIM_H - SAFE + 0.05:
            problems.append(f"{name}: x={x:.2f} y={y:.2f} r={x + w:.2f} b={y + h:.2f}")

    name_font = front.get("name_font", SERIF)
    box(
        "name",
        TEXT_X,
        front["name_baseline"],
        text_width(NAME, name_font, front["name_pt"], -0.02),
        "serif-name",
        front["name_pt"],
        TEXT_RIGHT,
    )
    box("role", TEXT_X, front["role_baseline"], text_width(ROLE, SANS, front["role_pt"], front["role_track"]), "sans-role", front["role_pt"], TEXT_RIGHT)
    rect("front-rule", TEXT_X, front["rule_y"] - FRONT_RULE / 2, COLUMN - TEXT_X, FRONT_RULE)
    if COLUMN > TEXT_RIGHT + 1.2:
        problems.append(f"front rule passes the text column: {COLUMN:.2f}")
    rect(
        "mark",
        front["mark_cx"] - front["mark_d"] / 2,
        front["mark_cy"] - front["mark_d"] / 2,
        front["mark_d"],
        front["mark_d"],
    )
    if front["mark_cx"] - front["mark_d"] / 2 < COLUMN - 0.05:
        problems.append("mark crosses the column break")
    for index, line in enumerate(SERVICES):
        baseline = front["service_baselines"][index]
        cy = baseline - pt_mm(front["service_pt"]) * 0.36
        rect(
            f"pointer{index}",
            TEXT_X + 0.70 - POINTER_W / 2,
            cy - POINTER_H / 2,
            POINTER_W,
            POINTER_H,
        )
        box(f"s{index}", front["service_x"], baseline, text_width(line, SANS, front["service_pt"]), "sans-service", front["service_pt"], TEXT_RIGHT)

    for row in back["rows"]:
        rect(row["icon"], TEXT_X, row["icon_top"], ICON, ICON)
        box(
            row["value"],
            back["value_x"],
            row["baseline"],
            text_width(row["value"], MONO, back["value_pt"]),
            "mono",
            back["value_pt"],
        )
        if back["value_x"] + text_width(row["value"], MONO, back["value_pt"]) > back["qr_x"] - QR_CLEAR:
            problems.append(f"{row['value']} runs into the QR")

    rect("back-rule", TEXT_X, back["rule_y"] - FRONT_RULE / 2, back["rule_right"] - TEXT_X, FRONT_RULE)
    if back["rule_right"] > back["qr_x"] - QR_CLEAR:
        problems.append("back rule runs into the QR")
    box("footer", TEXT_X, back["footer_baseline"], text_width(FOOTER, MONO, back["footer_pt"], back["footer_track"]), "mono", back["footer_pt"])
    if TEXT_X + text_width(FOOTER, MONO, back["footer_pt"], back["footer_track"]) > back["rule_right"] + 0.4:
        problems.append("footer is wider than the contact rule")

    rect("qr", back["qr_x"], back["qr_y"], back["qr"], back["qr"])
    if back["qr"] < 22 - 0.05:
        problems.append(f"qr shrunk below 22 mm: {back['qr']:.2f}")
    box("caption", back["caption_x"], back["caption_baseline"], back["caption_w"], "sans-service", back["caption_pt"])
    if back["caption_x"] < back["rule_right"] + 2:
        problems.append("caption meets the contact column")

    if problems:
        raise SystemExit("Outside the 5 mm safe area:\n" + "\n".join(problems))


def write_printer_note() -> None:
    note = """Αντώνης Σκαρλάτος — επαγγελματική κάρτα

Στείλτε το αρχείο antonis-skarlatos-card.pdf.
Μην τυπώσετε τα SVG.

Σελίδα 1: μπροστά
Σελίδα 2: πίσω, σωστή ανάγνωση (όχι καθρέφτης)

Κοπή: 90 × 50 mm
Bleed: 3 mm
Σημεία κοπής: μέσα στο PDF
Διπλή όψη: γύρισμα στη μεγάλη πλευρά

Χαρτί: αφουάρωτο κρεμ ή ιβουάρ, κοντά στο #f3efe4, 350–400 gsm.
Το κρεμ δεν είναι τυπωμένο χρώμα. Είναι το χρώμα του χαρτιού.
Το PDF δεν έχει κρεμ φόντο.

Μελάνι
- Κείμενο, εικονίδια, QR: 100% K
- Το κρεμ είναι το χαρτί· δεν τυπώνεται φόντο.

Οι γραμματοσειρές είναι ενσωματωμένες στο PDF.
Φινίρισμα: χωρίς γυαλιστερή πλαστικοποίηση. Γυαλίζει πάνω στο QR.
Οι στρογγυλεμένες γωνίες είναι εντάξει. Το κείμενο είναι 5 mm μέσα από την κοπή.

Ζητήστε ένα τυπωμένο δοκίμιο πριν από την παραγωγή.

---

Send antonis-skarlatos-card.pdf. Do not print the SVG files.

Page 1: front
Page 2: back, right-reading (not mirrored)

Trim: 90 × 50 mm
Bleed: 3 mm
Crop marks are in the PDF
Duplex: flip on the long edge

Stock: uncoated cream or ivory, near #f3efe4, 350–400 gsm.
The cream is the paper. The PDF does not print a cream background.

Ink
- Type, icons, and QR: 100% black (K)

Fonts are embedded in the PDF.
No gloss laminate. It glares on the QR.
Rounded corners are fine. Type sits 5 mm inside the trim.

Order one printed proof before the run.
"""
    (ROOT / "PRINTER.txt").write_text(note, encoding="utf-8")


def write_preview() -> None:
    page = """<!DOCTYPE html>
<html lang="el">
<head>
  <meta charset="utf-8">
  <title>Επαγγελματική κάρτα</title>
  <style>
    @font-face { font-family: "Manrope"; src: url("fonts/Manrope-Regular.ttf") format("truetype"); }
    body { margin: 0; padding: 32px; background: #e6e1d4; color: #14120e; font: 15px/1.4 Manrope, sans-serif; }
    h1 { font-size: 18px; font-weight: 500; margin: 0 0 8px; }
    p { margin: 0 0 20px; }
    .row { display: flex; gap: 18px; align-items: flex-start; flex-wrap: wrap; }
    figure { margin: 0; }
    img { width: 90mm; height: 50mm; display: block; box-shadow: 0 10px 28px rgba(20, 18, 14, 0.12); }
    figcaption { margin-top: 6px; font-size: 12px; letter-spacing: 0.04em; }
  </style>
</head>
<body>
  <h1>Εκτύπωση</h1>
  <p>Και οι δύο όψεις μπαίνουν στο PDF.</p>
  <div class="row">
    <figure>
      <img src="front.svg" alt="Μπροστινή όψη">
      <figcaption>Μπροστά</figcaption>
    </figure>
    <figure>
      <img src="back.svg" alt="Πίσω όψη">
      <figcaption>Πίσω</figcaption>
    </figure>
  </div>
</body>
</html>
"""
    (ROOT / "preview.html").write_text(page, encoding="utf-8")


def main() -> None:
    register_fonts()
    matrix = qr_matrix()
    front = front_layout()
    back = contact_layout()
    check_safe(front, back)
    write_qr_svg(matrix)
    write_front_svg(front)
    write_back_svg(back, matrix)
    write_pdf(front, back, matrix)
    write_printer_note()
    write_preview()
    for stale in ROOT.glob("front-name-*.svg"):
        stale.unlink()
    print("name", front["name_pt"], front.get("name_css", SERIF_CSS), "baseline", round(front["name_baseline"], 2))
    print("role", front["role_pt"], "track", front["role_track"], "rule", round(front["rule_y"], 2))
    print("services", front["service_pt"], tuple(round(v, 2) for v in front["service_baselines"]))
    print("mark", round(front["mark_d"], 2), "at", round(front["mark_cx"], 2), round(front["mark_cy"], 2))
    print("value", back["value_pt"], "rows", tuple(round(row["baseline"], 2) for row in back["rows"]))
    print("back rule", round(back["rule_y"], 2), "to", round(back["rule_right"], 2), "footer", round(back["footer_baseline"], 2))
    print("qr", back["qr"], "at", round(back["qr_x"], 2), round(back["qr_y"], 2), "caption", round(back["caption_baseline"], 2))
    print("qr modules", len(matrix), "including quiet zone")
    print("wrote", ROOT)


if __name__ == "__main__":
    main()
