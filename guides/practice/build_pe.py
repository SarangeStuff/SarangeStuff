"""Build the guided practice exam and its separate memo.

    python3 build_pe.py <L11.pdf> <L12.pdf> <L13.pdf> <Tutorial_11_Memo.pdf>
    node ../exams2025/render.js dist/MEC2047S-Practice-Exam.html dist/MEC2047S-Practice-Exam.pdf "MEC2047S PRACTICE EXAM (GUIDED)" "Do it with me · 100 marks"
    node ../exams2025/render.js dist/MEC2047S-Practice-Exam-Memo.html dist/MEC2047S-Practice-Exam-Memo.pdf "MEC2047S PRACTICE EXAM · MEMO" "Mark yourself: ✓ = 1 mark"

Question slides are cropped from your PDFs into dist/ only, with any printed answers blanked out.
"""
import pathlib
import re
import sys
import tempfile

from PIL import ImageDraw

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "guides" / "exams2025"))
sys.path.insert(0, str(ROOT / "guides" / "hwmemo"))
import build_f_memo  # noqa: E402
import build_hw  # noqa: E402
from build_s_exam import b64png, render, trim_bottom  # noqa: E402
import pe_figs  # noqa: E402

DPI = 200
# name: (pdf index, page, crop box @100 dpi, [white-out boxes @100 dpi])
CROPS = {
    "p5119": (2, 1, (125, 95, 627, 472), []),
    "p5108": (2, 1, (125, 530, 627, 888), [(455, 882, 627, 888)]),
    "p5120": (2, 2, (125, 530, 627, 880), []),
    "p517": (0, 1, (125, 530, 627, 905), []),
    "p544": (1, 1, (125, 535, 627, 868), [(470, 855, 627, 868)]),
    "t11q4": (3, 3, (55, 60, 752, 268), []),
}

CSS = """
.cover { margin: 0 auto 10pt; border-collapse: collapse; } .cover td { padding: 2pt 10pt; }
.hint { border: 1pt dashed #1c5cc2; background: #f4f8ff; border-radius: 4pt; padding: 5pt 9pt; margin: 6pt 0; font-size: 10.4pt; break-inside: avoid; }
.hb { font: bold 9pt 'Liberation Sans', Arial, sans-serif; color: #fff; background: #1c5cc2; border-radius: 3pt; padding: 1pt 5pt; margin-right: 4pt; }
ol.steps { margin: 3pt 0 0; padding-left: 18pt; font-size: 10pt; color: #333; } ol.steps li { margin: 1.5pt 0; }
.work { border: 0.8pt solid #999; border-radius: 3pt; margin: 6pt 0 4pt; break-inside: avoid;
  background-image: repeating-linear-gradient(to bottom, transparent 0, transparent 7.5mm, #ddd 7.5mm, #ddd 7.8mm); }
.work::before { content: "Working"; font: 8pt 'Liberation Sans', Arial, sans-serif; color: #999; padding: 2pt 5pt; display: block; }
.qh { font-size: 12.5pt; margin: 4pt 0 6pt; }
ol.parts { list-style: lower-alpha; margin: 2pt 0 6pt; padding-left: 20pt; } ol.parts.roman { list-style: lower-roman; }
ol.tight { margin: 3pt 0; padding-left: 18pt; } ol.tight li { margin: 2pt 0; }
table.th { border-collapse: collapse; width: 100%; font-size: 9.8pt; margin: 4pt 0; }
table.th th { text-align: left; border-bottom: 1.2pt solid #333; padding: 3pt 5pt; font-family: 'Liberation Sans', Arial, sans-serif; font-size: 8.8pt; }
table.th td { border-bottom: 0.6pt solid #ccc; padding: 4pt 5pt; vertical-align: top; }
.gridpage .grid1 { width: 180mm; height: 240mm; margin: 0 auto; border: 1px solid #888;
  background-image: linear-gradient(#bbb 1px, transparent 1px), linear-gradient(90deg, #bbb 1px, transparent 1px),
                    linear-gradient(#e6e6e6 1px, transparent 1px), linear-gradient(90deg, #e6e6e6 1px, transparent 1px);
  background-size: 10mm 10mm, 10mm 10mm, 2mm 2mm, 2mm 2mm; }
.row > .txt img.crop { width: 100%; }
img.crop { width: 72%; }
"""


def crops(pdfs):
    out, pages = {}, {}
    with tempfile.TemporaryDirectory() as td:
        for name, (i, pg, box, boxes) in CROPS.items():
            if (i, pg) not in pages:
                sub = pathlib.Path(td) / f"{i}"
                sub.mkdir(exist_ok=True)
                pages[(i, pg)] = render(pdfs[i], pg, sub, dpi=DPI)
            k = DPI / 100
            im = pages[(i, pg)].crop(tuple(round(v * k) for v in box))
            d = ImageDraw.Draw(im)
            for bx0, by0, bx1, by1 in boxes:
                d.rectangle(((bx0 - box[0]) * k, (by0 - box[1]) * k, (bx1 - box[0]) * k, (by1 - box[1]) * k), fill="white")
            im = trim_bottom(im)
            out[name] = f'<img class="crop" alt="Question figure {name}" src="data:image/png;base64,{b64png(im)}">'
    return out


def assemble(body, figs, cr, title):
    for kind, table in (("fig", figs), ("crop", cr)):
        missing = sorted(set(re.findall(r"\{\{%s:([a-z0-9_]+)\}\}" % kind, body)) - set(table))
        if missing:
            raise SystemExit(f"missing {kind}: {missing}")
        body = re.sub(r"\{\{%s:([a-z0-9_]+)\}\}" % kind, lambda m: table[m.group(1)], body)
    mj = ("<script>window.MathJax = { tex: { inlineMath: [['$', '$']], processEscapes: true }, "
          "svg: { fontCache: 'global' } };</script>"
          '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>')
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>'
            f"<style>{build_f_memo.CSS}\n{build_f_memo.fig_css()}\n{build_hw.CSS}\n{CSS}</style>{mj}</head><body>{body}</body></html>")


def check_ticks(memo):
    total = 0
    for m in re.finditer(r'<section class="q" data-marks="(\d+)" id="(q\d+)">(.*?)</section>', memo, re.S):
        marks, qid, txt = int(m.group(1)), m.group(2), m.group(3)
        ticks = sum(int(n or 1) for n in re.findall(r"\{\{t(\d?)\}\}", txt))
        print(f"  {qid}: {ticks} ticks / {marks} marks")
        if ticks != marks:
            raise SystemExit(f"{qid}: ticks {ticks} != marks {marks}")
        total += marks
    if total != 100:
        raise SystemExit(f"total {total} != 100")
    return re.sub(r"\{\{t(\d?)\}\}", lambda m: '<span class="tk">' + "✓" * int(m.group(1) or 1) + "</span>", memo)


def main(*pdfs):
    figs = pe_figs.build_all()
    cr = crops([pathlib.Path(p) for p in pdfs])
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    exam = assemble((HERE / "exam_body.html").read_text(), figs, cr, "MEC2047S Practice Exam")
    memo = assemble(check_ticks((HERE / "memo_body.html").read_text()), figs, cr, "MEC2047S Practice Exam Memo")
    (out / "MEC2047S-Practice-Exam.html").write_text(exam)
    (out / "MEC2047S-Practice-Exam-Memo.html").write_text(memo)
    print(f"wrote exam ({len(exam) // 1024} KB) and memo ({len(memo) // 1024} KB)")


if __name__ == "__main__":
    main(*sys.argv[1:5])
