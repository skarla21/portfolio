"""Build the business-card SVGs, QR, and print PDF.

Not imported by the Nuxt app. From the repo root:

    python print/business-card/render.py

Requires reportlab and segno (pip install reportlab segno).
Those are not project dependencies.
"""

from __future__ import annotations

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

# Screen colours. The PDF prints black as 100% K and the lime as CMYK.
INK_HEX = "#14120e"
LIME_HEX = "#d6f26a"
PAPER_HEX = "#f3efe4"
LIME = CMYKColor(0.18, 0.0, 0.60, 0.0)
K = CMYKColor(0, 0, 0, 1)

# Shared left edge of the words. The lime bar sits just outside it.
TEXT_X = 6.1
SERIF_SUB = "SourceSerif4Subhead"
SERIF_CAP = "SourceSerif4Caption"
SANS = "SourceSans3"

PLACE = "ΑΘΗΝΑ"
NAME = ("Αντώνης", "Σκαρλάτος")
LATIN = "Antonis Skarlatos"
LEDE = "Φυσικός στην εκπαίδευση, προγραμματιστής στην πράξη."
SERVICES = (
    ("Ιστοσελίδες", "Ανάλυση δεδομένων"),
    ("Εφαρμογές", "SEO"),
    ("E-shops", "AEO"),
)
CONTACT = (
    ("E-MAIL", "antwnis_skarlatos@yahoo.com"),
    ("ΤΗΛΕΦΩΝΟ", "+30 698 369 6885"),
    ("ΙΣΤΟΤΟΠΟΣ", "antonis-skarlatos.vercel.app"),
)

MM = 72 / 25.4


def pt_mm(pt: float) -> float:
    return pt * 25.4 / 72


def mm_pt(mm: float) -> float:
    return mm * MM


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont(SERIF_SUB, str(FONTS / "SourceSerif4Subhead-Regular.ttf")))
    pdfmetrics.registerFont(TTFont(SERIF_CAP, str(FONTS / "SourceSerif4Caption-Regular.ttf")))
    pdfmetrics.registerFont(TTFont(SANS, str(FONTS / "SourceSans3-Regular.ttf")))


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
# Font ascender metrics are taller than the Greek we actually set.
INK = {
    "sans-caps": (0.2357, 0.01),
    "sans-latin": (0.251, 0.01),
    "sans-service": (0.265, 0.075),
    "sans-value": (0.252, 0.074),
    "serif-name": (0.2675, 0.0725),
    "serif-lede": (0.2735, 0.0723),
}


def ink(kind: str, pt: float) -> tuple[float, float]:
    above, below = INK[kind]
    return above * pt, below * pt


def lede_box(baseline: float, pt: float) -> tuple[float, float, float, float]:
    pad_x = 0.22 * pt_mm(pt)
    above, below = ink("serif-lede", pt)
    pad_top = 0.16
    pad_bot = 0.22
    top = baseline - above - pad_top
    height = above + below + pad_top + pad_bot
    width = text_width(LEDE, SERIF_CAP, pt) + pad_x * 2
    return TEXT_X - pad_x, top, width, height


def front_layout() -> dict:
    place_pt = 7.0
    name_pt = 22.0
    latin_pt = 7.25
    lede_pt = 7.75
    service_pt = 8.0

    place_baseline = 7.00
    name_above, name_below = ink("serif-name", name_pt)
    name_1 = place_baseline + 0.03 + 2.15 + name_above
    name_2 = name_1 + name_above + name_below + 0.70
    latin_above, _latin_below = ink("sans-latin", latin_pt)
    latin_baseline = name_2 + name_below + 1.65 + latin_above
    lede_above, _lede_below = ink("serif-lede", lede_pt)
    lede_baseline = latin_baseline + 0.03 + 1.70 + 0.16 + lede_above
    bar = lede_box(lede_baseline, lede_pt)
    service_above, service_below = ink("sans-service", service_pt)
    service_1 = bar[1] + bar[3] + 1.85 + service_above
    service_step = service_below + 0.75 + service_above
    return {
        "place_pt": place_pt,
        "place_baseline": place_baseline,
        "name_pt": name_pt,
        "name_baselines": (name_1, name_2),
        "latin_pt": latin_pt,
        "latin_baseline": latin_baseline,
        "lede_pt": lede_pt,
        "lede_baseline": lede_baseline,
        "bar": bar,
        "service_pt": service_pt,
        "service_baselines": tuple(service_1 + i * service_step for i in range(3)),
        "col2": 46.0,
    }


def contact_layout() -> dict:
    label_pt = 6.5
    value_pt = 8.5
    label_above, _label_below = ink("sans-caps", label_pt)
    value_above, value_below = ink("sans-value", value_pt)
    label_to_value = 0.85
    item = label_above + label_to_value + value_above + value_below
    gap = 3.4
    height = 3 * item + 2 * gap
    top = (TRIM_H - height) / 2
    qr = 22.0
    return {
        "label_pt": label_pt,
        "value_pt": value_pt,
        "label_above": label_above,
        "value_above": value_above,
        "label_to_value": label_to_value,
        "item": item,
        "gap": gap,
        "top": top,
        "qr": qr,
        "qr_x": TRIM_W - 5.5 - qr,
        "qr_y": (TRIM_H - qr) / 2,
    }


def svg_font_css() -> str:
    return """
    @font-face {
      font-family: "Source Serif 4 Subhead";
      src: url("fonts/SourceSerif4Subhead-Regular.ttf") format("truetype");
      font-weight: 400;
    }
    @font-face {
      font-family: "Source Serif 4 Caption";
      src: url("fonts/SourceSerif4Caption-Regular.ttf") format("truetype");
      font-weight: 400;
    }
    @font-face {
      font-family: "Source Sans 3";
      src: url("fonts/SourceSans3-Regular.ttf") format("truetype");
      font-weight: 400;
    }
    text { fill: #14120e; }
    """


def svg_text(
    text: str,
    family: str,
    pt: float,
    x: float,
    y: float,
    tracking_em: float = 0,
) -> str:
    size = pt_mm(pt)
    spacing = f' letter-spacing="{tracking_em * size:.4f}"' if tracking_em else ""
    return (
        f'<text x="{x:.3f}" y="{y:.3f}" '
        f'font-family="{family}" font-size="{size:.4f}"{spacing}>'
        f"{esc(text)}</text>"
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


def write_front_svg(layout: dict) -> None:
    x, y, w, h = layout["bar"]
    parts = [
        f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{LIME_HEX}"/>',
        svg_text(PLACE, "Source Sans 3", layout["place_pt"], TEXT_X, layout["place_baseline"], 0.22),
        svg_text(NAME[0], "Source Serif 4 Subhead", layout["name_pt"], TEXT_X, layout["name_baselines"][0], -0.03),
        svg_text(NAME[1], "Source Serif 4 Subhead", layout["name_pt"], TEXT_X, layout["name_baselines"][1], -0.03),
        svg_text(LATIN, "Source Sans 3", layout["latin_pt"], TEXT_X, layout["latin_baseline"], 0.02),
        svg_text(LEDE, "Source Serif 4 Caption", layout["lede_pt"], TEXT_X, layout["lede_baseline"]),
    ]
    for row, (left, right) in enumerate(SERVICES):
        baseline = layout["service_baselines"][row]
        parts.append(svg_text(left, "Source Sans 3", layout["service_pt"], TEXT_X, baseline))
        parts.append(svg_text(right, "Source Sans 3", layout["service_pt"], layout["col2"], baseline))
    body = "\n  ".join(parts)
    (ROOT / "front.svg").write_text(
        svg_document("Αντώνης Σκαρλάτος — μπροστά", body),
        encoding="utf-8",
    )


def write_back_svg(layout: dict, matrix: list[list[int]]) -> None:
    n = len(matrix)
    scale = layout["qr"] / n
    dark = []
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                dark.append(f"M{x} {y}h1v1h-1z")
    parts = [
        (
            f'<g transform="translate({layout["qr_x"]:.3f} {layout["qr_y"]:.3f}) scale({scale:.6f})">'
            f'<path fill="{INK_HEX}" d="{" ".join(dark)}"/></g>'
        )
    ]
    y = layout["top"]
    for label, value in CONTACT:
        label_baseline = y + layout["label_above"]
        value_baseline = label_baseline + layout["label_to_value"] + layout["value_above"]
        parts.append(svg_text(label, "Source Sans 3", layout["label_pt"], TEXT_X, label_baseline, 0.18))
        parts.append(svg_text(value, "Source Sans 3", layout["value_pt"], TEXT_X, value_baseline))
        y += layout["item"] + layout["gap"]
    body = "\n  ".join(parts)
    (ROOT / "back.svg").write_text(
        svg_document("Αντώνης Σκαρλάτος — πίσω", body),
        encoding="utf-8",
    )


def draw_text(c: canvas.Canvas, text: str, font: str, pt: float, x_mm: float, baseline: float, tracking_em: float = 0) -> None:
    c.setFillColor(K)
    c.setFont(font, pt)
    c.drawString(tx(x_mm), ty(baseline), text, charSpace=tracking_em * pt)


def draw_qr(c: canvas.Canvas, matrix: list[list[int]], layout: dict) -> None:
    n = len(matrix)
    module = mm_pt(layout["qr"] / n)
    origin_x = tx(layout["qr_x"])
    origin_top = ty(layout["qr_y"])
    c.setFillColor(K)
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

    x, y, w, h = front["bar"]
    c.setFillColor(LIME)
    c.rect(tx(x), ty(y + h), mm_pt(w), mm_pt(h), stroke=0, fill=1)
    draw_text(c, PLACE, SANS, front["place_pt"], TEXT_X, front["place_baseline"], 0.22)
    draw_text(c, NAME[0], SERIF_SUB, front["name_pt"], TEXT_X, front["name_baselines"][0], -0.03)
    draw_text(c, NAME[1], SERIF_SUB, front["name_pt"], TEXT_X, front["name_baselines"][1], -0.03)
    draw_text(c, LATIN, SANS, front["latin_pt"], TEXT_X, front["latin_baseline"], 0.02)
    draw_text(c, LEDE, SERIF_CAP, front["lede_pt"], TEXT_X, front["lede_baseline"])
    for row, (left, right) in enumerate(SERVICES):
        baseline = front["service_baselines"][row]
        draw_text(c, left, SANS, front["service_pt"], TEXT_X, baseline)
        draw_text(c, right, SANS, front["service_pt"], front["col2"], baseline)
    draw_crop_marks(c, media_w, media_h)
    draw_slug(c, media_w, "FRONT  ·  90 × 50 mm trim  ·  3 mm bleed")
    c.showPage()

    c.setTrimBox(trim)
    c.setBleedBox(bleed)
    c.setArtBox(trim)
    draw_qr(c, matrix, back)
    y_cursor = back["top"]
    for label, value in CONTACT:
        label_baseline = y_cursor + back["label_above"]
        value_baseline = label_baseline + back["label_to_value"] + back["value_above"]
        draw_text(c, label, SANS, back["label_pt"], TEXT_X, label_baseline, 0.18)
        draw_text(c, value, SANS, back["value_pt"], TEXT_X, value_baseline)
        y_cursor += back["item"] + back["gap"]
    draw_crop_marks(c, media_w, media_h)
    draw_slug(c, media_w, "BACK  ·  90 × 50 mm trim  ·  3 mm bleed  ·  flip on long edge")
    c.save()


def check_safe(front: dict, back: dict) -> None:
    problems = []

    def box(name: str, x: float, baseline: float, width: float, kind: str, pt: float) -> None:
        above, below = ink(kind, pt)
        top = baseline - above
        bottom = baseline + below
        right = x + width
        if top < SAFE - 0.05 or bottom > TRIM_H - SAFE + 0.05 or x < SAFE - 0.05 or right > TRIM_W - SAFE + 0.05:
            problems.append(f"{name}: x={x:.2f} top={top:.2f} right={right:.2f} bottom={bottom:.2f}")

    box("place", TEXT_X, front["place_baseline"], text_width(PLACE, SANS, front["place_pt"], 0.22), "sans-caps", front["place_pt"])
    for i, line in enumerate(NAME):
        box(
            f"name{i}",
            TEXT_X,
            front["name_baselines"][i],
            text_width(line, SERIF_SUB, front["name_pt"], -0.03),
            "serif-name",
            front["name_pt"],
        )
    box("latin", TEXT_X, front["latin_baseline"], text_width(LATIN, SANS, front["latin_pt"], 0.02), "sans-latin", front["latin_pt"])
    box("lede", TEXT_X, front["lede_baseline"], text_width(LEDE, SERIF_CAP, front["lede_pt"]), "serif-lede", front["lede_pt"])
    x, y, w, h = front["bar"]
    if x < SAFE - 0.05 or y < SAFE - 0.05 or x + w > TRIM_W - SAFE + 0.05 or y + h > TRIM_H - SAFE + 0.05:
        problems.append(f"lime: x={x:.2f} y={y:.2f} r={x+w:.2f} b={y+h:.2f}")
    for row, (left, right) in enumerate(SERVICES):
        baseline = front["service_baselines"][row]
        box(f"s{row}a", TEXT_X, baseline, text_width(left, SANS, front["service_pt"]), "sans-service", front["service_pt"])
        box(f"s{row}b", front["col2"], baseline, text_width(right, SANS, front["service_pt"]), "sans-service", front["service_pt"])
    y_cursor = back["top"]
    for label, value in CONTACT:
        label_baseline = y_cursor + back["label_above"]
        value_baseline = label_baseline + back["label_to_value"] + back["value_above"]
        box(label, TEXT_X, label_baseline, text_width(label, SANS, back["label_pt"], 0.18), "sans-caps", back["label_pt"])
        box(value, TEXT_X, value_baseline, text_width(value, SANS, back["value_pt"]), "sans-value", back["value_pt"])
        if TEXT_X + text_width(value, SANS, back["value_pt"]) > back["qr_x"] - 4:
            problems.append(f"{value} runs into the QR quiet zone")
        y_cursor += back["item"] + back["gap"]
    if back["qr_x"] < SAFE or back["qr_y"] < SAFE or back["qr_x"] + back["qr"] > TRIM_W - SAFE or back["qr_y"] + back["qr"] > TRIM_H - SAFE:
        problems.append(
            f"qr: x={back['qr_x']:.2f} y={back['qr_y']:.2f} r={back['qr_x']+back['qr']:.2f} b={back['qr_y']+back['qr']:.2f}"
        )
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
- Κείμενο και QR: 100% K
- Λαχανί, μόνο η γραμμή πίσω από τη μία πρόταση: C 18, M 0, Y 60, K 0
  Στόχος στην οθόνη: #d6f26a. Σε αφουάρωτο χαρτί το λαχανί θα κάτσει λίγο πιο σκούρο.

Οι γραμματοσειρές είναι ενσωματωμένες στο PDF.
Φινίρισμα: χωρίς γυαλιστερή πλαστικοποίηση. Θαμπώνει το λαχανί και γυαλίζει πάνω στο QR.
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
- Type and QR: 100% black (K)
- Lime, the bar behind one sentence only: C 18, M 0, Y 60, K 0
  Screen target #d6f26a. On uncoated stock it will sit a little deeper.

Fonts are embedded in the PDF.
No gloss laminate. It dulls the lime and glares on the QR.
Rounded corners are fine. Type sits 5 mm inside the trim.

Order one printed proof before the run.
"""
    (ROOT / "PRINTER.txt").write_text(note, encoding="utf-8")


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
    bar = front["bar"]
    print("front name baselines", tuple(round(v, 2) for v in front["name_baselines"]))
    print("lede baseline", round(front["lede_baseline"], 2), "bar", tuple(round(v, 2) for v in bar))
    print("services", tuple(round(v, 2) for v in front["service_baselines"]))
    print("qr modules", len(matrix), "including quiet zone")
    print("wrote", ROOT)


if __name__ == "__main__":
    main()
