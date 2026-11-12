"""Build the memo for the L11-L13 homework problems (rotation, absolute motion, instantaneous centre).

    python3 build_hw.py <L11.pdf> <L12.pdf> <L13.pdf>
    node ../exams2025/render.js dist/MEC2047-Homework-Memo-L11-L13.html dist/MEC2047-Homework-Memo-L11-L13.pdf \
        "MEC2047 HOMEWORK MEMO" "L11 rotation · L12 absolute motion · L13 IC" [<local-mathjax-dir>]

Question slides are cropped from your PDFs into dist/ only. check_answers.py re-derives every answer.
"""
import pathlib
import re
import sys
import tempfile

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "guides" / "exams2025"))
import build_f_memo  # noqa: E402
from build_s_exam import b64png, render, trim_bottom  # noqa: E402
import hw_figs  # noqa: E402

DPI = 200
# name: (pdf index, page, box in px at 100 dpi)
CROPS = {
    "p52": (0, 1, (125, 95, 627, 472)), "p517": (0, 1, (125, 530, 627, 905)), "p526": (0, 2, (125, 95, 627, 440)),
    "p542": (1, 1, (125, 95, 627, 472)), "p544": (1, 1, (125, 535, 627, 905)), "p556": (1, 2, (125, 95, 627, 462)),
    "p5119": (2, 1, (125, 95, 627, 472)), "p5108": (2, 1, (125, 530, 627, 905)),
    "p5117": (2, 2, (125, 95, 627, 472)), "p5120": (2, 2, (125, 530, 627, 905)),
}

CSS = """
.subt { font-size: 13pt; font-weight: normal; }
.q + .q { break-before: auto; } .q { margin-bottom: 22pt; border-top: 0.8pt solid #bbb; padding-top: 8pt; }
img.crop { width: 78%; margin: 0 auto 4pt; }
.howto { border: 1pt solid #1c5cc2; background: #eef3fc; border-radius: 4pt; padding: 6pt 10pt; font-size: 10.6pt; margin: 0 0 12pt; break-inside: avoid; }
.ansl { font: bold 11pt 'Liberation Sans', Arial, sans-serif; color: #fff; background: #1c5cc2; border-radius: 4pt; padding: 4pt 10pt; display: inline-block; margin: 8pt 0 0; }
.figc { margin: 6pt 0; break-inside: avoid; } .figc svg.fig { margin: 0 auto; }
svg.fig.true { max-width: none !important; max-height: none !important; }
.row > figure.side { flex: 0 1 auto; max-width: 44%; }
.fig line.n { stroke: var(--c-n); stroke-width: 2.2; } .fig line.t { stroke: var(--c-t); stroke-width: 2.2; }
.fig line.ans { stroke: var(--c-ans); stroke-width: 1.8; } .fig line.abs { stroke: var(--c-abs); stroke-width: 1.8; }
"""


def crops(pdfs):
    out, pages = {}, {}
    with tempfile.TemporaryDirectory() as td:
        for name, (i, pg, box) in CROPS.items():
            if (i, pg) not in pages:
                sub = pathlib.Path(td) / f"{i}"
                sub.mkdir(exist_ok=True)
                pages[(i, pg)] = render(pdfs[i], pg, sub, dpi=DPI)
            k = DPI / 100
            im = trim_bottom(pages[(i, pg)].crop(tuple(round(v * k) for v in box)))
            out[name] = f'<img class="crop" alt="Homework problem {name[1:]}" src="data:image/png;base64,{b64png(im)}">'
    return out


def main(*pdfs):
    figs = hw_figs.build_all()
    cr = crops([pathlib.Path(p) for p in pdfs])
    body = (HERE / "hw_body.html").read_text()
    for kind, table in (("fig", figs), ("crop", cr)):
        missing = sorted(set(re.findall(r"\{\{%s:([a-z0-9_]+)\}\}" % kind, body)) - set(table))
        if missing:
            raise SystemExit(f"missing {kind}: {missing}")
        body = re.sub(r"\{\{%s:([a-z0-9_]+)\}\}" % kind, lambda m: table[m.group(1)], body)
    mj = ("<script>window.MathJax = { tex: { inlineMath: [['$', '$']], processEscapes: true }, "
          "svg: { fontCache: 'global' } };</script>"
          '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>')
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>MEC2047 Homework Memo L11-L13</title>'
            f"<style>{build_f_memo.CSS}\n{build_f_memo.fig_css()}\n{CSS}</style>{mj}</head><body>{body}</body></html>")
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    dst = out / "MEC2047-Homework-Memo-L11-L13.html"
    dst.write_text(html)
    print(f"wrote {dst} ({len(html) / 1024:.0f} KB)")


if __name__ == "__main__":
    main(*sys.argv[1:4])
