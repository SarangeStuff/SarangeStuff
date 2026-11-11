"""Build an unofficial memo for the MEC2047F Final Exam (June 2025) in the style of the MEC2047S 2025 memo.

    python3 build_f_memo.py <F-exam.pdf>

The question statements and figures are cropped from the exam paper itself; the solutions are typed in
f_memo_body.html and the diagrams come from f_memo_figs.py. The build checks that the ticks in every
question add up to that question's marks. Output: dist/ (not committed).
"""
import base64
import io
import pathlib
import re
import sys
import tempfile

from PIL import ImageDraw

import f_memo_figs
from build_s_exam import K, b64png, render, trim_bottom

HERE = pathlib.Path(__file__).parent

# (name, exam page, top pt, bottom pt, [white-out boxes in pt])
CROPS = [
    ("Q1", 2, 107, 256, []),
    ("Q2", 2, 290, 356, []),  # text only: the annotated figure in the solution shows the drawing
    ("Q3", 3, 72, 311, []),
    ("Q4", 3, 345, 598, []),
    ("Q5", 4, 98, 378, []),
    ("Q6", 4, 398, 680, []),
    ("Q7", 5, 86, 314, [(40, 255, 380, 314)]),
    ("Q8", 5, 271, 478, [(380, 271, 570, 364)]),
    ("Q9", 5, 490, 704, []),
]
X0, X1 = 55, 552

CSS = """
:root { --bg: #fff; --paper: #fff; --ink: #111; --muted: #555; --rule: #ccc;
  --c-abs: #1c5cc2; --c-n: #b25c00; --c-t: #12804a; --c-ans: #c0154c; --c-cons: #8791a1; --link: #c9d3e0;
  --tint-abs: #e6eefb; --tint-n: #fbefe0; --tint-t: #e2f3e9; --tint-ans: #fbe6ed; color-scheme: light; }
body { font: 12pt/1.38 'Liberation Serif', 'Times New Roman', Times, serif; color: #000; background: #fff; margin: 0; }
h1.title { text-align: center; font-size: 21pt; line-height: 1.2; margin: 2pt 0 6pt; }
.unoff { text-align: center; font-size: 10pt; color: #555; font-style: italic; margin: 0 0 12pt; }
h2.sec { text-align: center; font-size: 13pt; margin: 10pt 0 12pt; }
.q { margin-bottom: 16pt; } .q + .q { break-before: page; }
.brk { break-before: page; }
img.crop { display: block; width: 100%; height: auto; break-inside: avoid; margin-bottom: 4pt; }
.solh { font-weight: bold; margin: 10pt 0 4pt; break-after: avoid; }
.sub { text-decoration: underline; margin: 8pt 0 3pt; break-after: avoid; }
.ln { margin: 3pt 0; break-inside: avoid; }
.tk { color: #d0021b; font-family: 'DejaVu Sans', sans-serif; font-size: 10.5pt; letter-spacing: -1pt; padding-left: 3pt; }
.rn { color: #d0021b; font-size: 11pt; margin: 3pt 0; }
.mk { display: inline-block; border: 1px solid #333; color: #d0021b; padding: 3pt 10pt; margin: 4pt 0; font-size: 11pt; }
.row { display: flex; gap: 14pt; align-items: flex-start; break-inside: avoid; }
.row > .txt { flex: 1 1 0; min-width: 0; }
.row > figure.side { flex: 0 1 auto; max-width: 46%; margin: 4pt 0 0; }
figure.full { margin: 6pt 0; } figure.full svg.fig { margin: 0 auto; }
.figmk { display: flex; gap: 14pt; align-items: center; break-inside: avoid; } .figmk > figure { flex: 0 1 auto; min-width: 0; }
.figs2 { display: flex; gap: 10pt; align-items: flex-start; break-inside: avoid; }
.figs2 { justify-content: center; } .figs2 > figure { flex: 0 1 auto; min-width: 0; margin: 0; }
figure { margin: 0; } figcaption { text-align: center; font-size: 10pt; color: #555; }
.total { text-align: center; font-weight: bold; margin-top: 20pt; }
mjx-container[jax="SVG"][display="true"] { margin: 4pt 0 !important; }
svg.fig { display: block; margin: 0 auto; max-width: 100%; height: auto; overflow: visible;
  font-family: 'Liberation Serif', 'Times New Roman', serif; font-size: 14px; }
"""


def fig_css():
    head = (HERE.parents[1] / "textbook" / "src" / "shell_head.html").read_text()
    return "\n".join(l for l in head.splitlines() if l.startswith(".fig "))


def main(exam):
    exam = pathlib.Path(exam)
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp(dir=out))
    pages, crops = {}, {}
    for name, pg, top, bot, boxes in CROPS:
        if pg not in pages:
            pages[pg] = render(exam, pg, tmp)
        im = pages[pg].crop((round(X0 * K), round(top * K), round(X1 * K), round(bot * K)))
        d = ImageDraw.Draw(im)
        for bx0, by0, bx1, by1 in boxes:
            d.rectangle(((bx0 - X0) * K, (by0 - top) * K, (bx1 - X0) * K, (by1 - top) * K), fill="white")
        im = trim_bottom(im)
        crops[name] = f'<img class="crop" alt="{name} as set in the exam" src="data:image/png;base64,{b64png(im)}">'
    q2 = pages[2].crop((1040, 1540, 1420, 2560))
    buf = io.BytesIO()
    q2.save(buf, "PNG", optimize=True)
    figs = f_memo_figs.build_all((base64.b64encode(buf.getvalue()).decode(), q2.width, q2.height))
    for f in tmp.iterdir():
        f.unlink()
    tmp.rmdir()

    body = (HERE / "f_memo_body.html").read_text()
    total = 0
    for m in re.finditer(r'<section class="q" data-marks="(\d+)" id="(q\d)">(.*?)</section>', body, re.S):
        marks, qid, txt = int(m.group(1)), m.group(2), m.group(3)
        ticks = sum(int(n or 1) for n in re.findall(r"\{\{t(\d?)\}\}", txt))
        print(f"{qid}: {ticks} ticks / {marks} marks")
        if ticks != marks:
            raise SystemExit(f"{qid}: ticks {ticks} != marks {marks}")
        total += marks
    if total != 100:
        raise SystemExit(f"total {total} != 100")
    body = re.sub(r"\{\{t(\d?)\}\}", lambda m: '<span class="tk">' + "✓" * int(m.group(1) or 1) + "</span>", body)
    body = re.sub(r"\{\{crop:(Q\d)\}\}", lambda m: crops[m.group(1)], body)
    body = re.sub(r"\{\{fig:([a-z0-9_]+)\}\}", lambda m: figs[m.group(1)], body)
    mj = ("<script>window.MathJax = { tex: { inlineMath: [['$', '$']], processEscapes: true }, "
          "svg: { fontCache: 'global' } };</script>"
          '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>')
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>MEC2047F 2025 Memo</title>'
            f"<style>{CSS}\n{fig_css()}</style>{mj}</head><body>{body}</body></html>")
    dst = out / "MEC2047F-2025-Final-Exam-Memo.html"
    dst.write_text(html)
    print(f"wrote {dst} ({len(html) / 1024:.0f} KB)")


if __name__ == "__main__":
    main(sys.argv[1])
