"""Rebuild a plain question paper for MEC2047S Final Exam (13/11/2025) from its official memo.

    python3 build_s_exam.py <S-memo.pdf>

Each question statement (text + figure) is cropped from the memo pages, so the wording and
figures are the examiners' own; the solutions are left out. A 1 cm grid sheet is added for the
scaled vector diagram in Q4(b). Output: dist/ (not committed).
"""
import base64
import io
import pathlib
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).parent
DPI = 300
K = DPI / 72.0  # px per pt

# (memo page, top pt, bottom pt, [white-out boxes in pt], break-before-page)
CROPS = [
    ("Q1", 1, 155, 594, [], False),
    ("Q2", 2, 365, 720, [], True),
    ("Q3", 4, 95, 345, [], False),
    ("Q4", 5, 110, 510, [], True),
    ("Q5", 7, 66, 384, [], True),
    ("Q6", 8, 62, 381, [(50, 360, 118, 381)], False),
    ("Q7", 9, 58, 346, [], True),
    ("Q8", 10, 50, 357, [], False),
]
X0, X1 = 40, 566


def render(pdf, page, outdir, dpi=DPI):
    stem = outdir / f"p{page}"
    subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(page), "-l", str(page), "-png", "-singlefile",
                    str(pdf), str(stem)], check=True)
    return Image.open(f"{stem}.png").convert("RGB")


def trim_bottom(im, pad=18):
    g = im.convert("L").point(lambda v: 255 if v > 235 else 0)
    inv = Image.eval(g, lambda v: 255 - v)
    bbox = inv.getbbox()
    if not bbox:
        return im
    return im.crop((0, 0, im.width, min(im.height, bbox[3] + pad)))


def b64png(im):
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "PNG", optimize=True)  # greyscale PNGs print as 254-grey in Chromium
    return base64.b64encode(buf.getvalue()).decode()


def b64jpg(im, q=88):
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


CSS = """
@page { size: A4; }
body { font: 12pt/1.35 'Liberation Serif', 'Times New Roman', Times, serif; color: #000; margin: 0; }
.cover { text-align: center; padding-top: 30mm; }
.cover .uni { font-size: 18pt; margin: 0; } .cover .dept { font-size: 16pt; margin: 4pt 0 26pt; }
.cover h1 { font-size: 22pt; margin: 0 0 4pt; } .cover h2 { font-size: 18pt; font-weight: bold; margin: 0 0 30pt; }
.cover table { margin: 0 auto 22pt; text-align: left; border-collapse: collapse; }
.cover td { padding: 3pt 14pt 3pt 0; vertical-align: top; }
.cover .ins { text-align: left; max-width: 150mm; margin: 0 auto; }
.cover .ins h3 { font-size: 12pt; margin: 0 0 6pt; }
.cover .ins ol { list-style: lower-alpha; margin: 0; padding-left: 22pt; } .cover .ins li { margin: 2pt 0; }
.note { font-size: 10pt; color: #444; border-top: 1px solid #999; margin-top: 24pt; padding-top: 6pt; text-align: left; }
.q { break-inside: avoid; margin: 0 0 14pt; }
.q img { display: block; width: 100%; height: auto; }
.brk { break-before: page; }
.sheet h2 { font-size: 13pt; margin: 0 0 4pt; } .sheet p { margin: 0 0 8pt; font-size: 11pt; }
.grid { width: 170mm; height: 220mm; margin: 0 auto;
  background-image: linear-gradient(#bbb 1px, transparent 1px), linear-gradient(90deg, #bbb 1px, transparent 1px),
                    linear-gradient(#e2e2e2 1px, transparent 1px), linear-gradient(90deg, #e2e2e2 1px, transparent 1px);
  background-size: 10mm 10mm, 10mm 10mm, 2mm 2mm, 2mm 2mm; border: 1px solid #888; }
.formula img { display: block; width: 100%; height: auto; }
.end { text-align: center; font-weight: bold; margin-top: 18pt; }
"""


def main(memo):
    memo = pathlib.Path(memo)
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp(dir=out))
    pages = {}
    blocks = []
    for name, pg, top, bot, boxes, brk in CROPS:
        if pg not in pages:
            pages[pg] = render(memo, pg, tmp)
        im = pages[pg].crop((round(X0 * K), round(top * K), round(X1 * K), round(bot * K)))
        d = ImageDraw.Draw(im)
        for bx0, by0, bx1, by1 in boxes:
            d.rectangle(((bx0 - X0) * K, (by0 - top) * K, (bx1 - X0) * K, (by1 - top) * K), fill="white")
        im = trim_bottom(im)
        cls = "q brk" if brk else "q"
        blocks.append(f'<div class="{cls}" id="{name}"><img alt="{name} statement and figure" '
                      f'src="data:image/png;base64,{b64png(im)}"></div>')
    cover = """
<section class="cover">
  <p class="uni">University of Cape Town</p>
  <p class="dept">Department of Mechanical Engineering</p>
  <h1>MEC2047S – Engineering Dynamics</h1>
  <h2>Final Exam</h2>
  <table>
    <tr><td><b>Date:</b></td><td>13 November 2025</td></tr>
    <tr><td><b>Marks:</b></td><td>100 &nbsp;(Section A: 53 · Section B: 47)</td></tr>
    <tr><td><b>Suggested time:</b></td><td>Three [3] hours</td></tr>
  </table>
  <div class="ins">
    <h3>INSTRUCTIONS</h3>
    <ol>
      <li>This is a closed book exam.</li>
      <li>Be neat and clear and show evidence of logical thought.</li>
      <li>State fundamental assumptions and highlight your answers appropriately.</li>
      <li>Question 4(b) must be answered with a scaled vector diagram: use the grid sheet at the back.</li>
    </ol>
    <p class="note">Practice copy. The questions and figures are cropped from the official 2025 MEC2047S memo
    with every solution removed. The memo has no cover page or formula sheet, so the time allowed and the instructions
    follow the June 2025 MEC2047F paper; use your course formula sheet.</p>
  </div>
</section>"""
    sheet = """
<section class="sheet brk">
  <h2>Answer sheet – Question 4(b): scaled acceleration vector diagram</h2>
  <p>Scale 10 m/s² : 1 cm (heavy lines 1 cm, light lines 2 mm).</p>
  <div class="grid"></div>
</section>"""
    body = cover + '<div class="brk"></div>' + "".join(blocks) + '<p class="end">TOTAL MARKS: 100</p>' + sheet
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>MEC2047S 2025 Final Exam</title>'
            f"<style>{CSS}</style></head><body>{body}</body></html>")
    dst = out / "MEC2047S-2025-Final-Exam.html"
    dst.write_text(html)
    for f in tmp.iterdir():
        f.unlink()
    tmp.rmdir()
    print(f"wrote {dst} ({len(html) / 1024:.0f} KB)")


if __name__ == "__main__":
    main(sys.argv[1])
