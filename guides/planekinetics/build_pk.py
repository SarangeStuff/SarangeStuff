"""Build the plane-kinetics workthrough (Tutorials 10 and 11).

    python3 build_pk.py <Tutorial_10_Memo.pdf> <Tutorial_11_Memo.pdf>
    node ../exams2025/render.js dist/MEC2047S-Plane-Kinetics-Workthrough.html dist/MEC2047S-Plane-Kinetics-Workthrough.pdf \
        "MEC2047S · PLANE KINETICS WORKTHROUGH" "Tutorials 10 & 11" [<local-mathjax-dir>]

The question figures are cropped from your own memo PDFs (kept in dist/ only, not committed).
Every number in the text is re-derived in check_answers.py.
"""
import base64
import io
import pathlib
import re
import subprocess
import sys
import tempfile

from PIL import Image

import pk_figs

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "guides" / "playbook"))
import build_playbook  # noqa: E402  (reuse the playbook's card styles)

# name: (which pdf, page, box in px at 100 dpi)
CROPS = {
    "t10q1": (0, 1, (430, 148, 762, 272)),
    "t10q2": (0, 1, (468, 700, 778, 880)),
    "t10q3": (0, 2, (493, 228, 778, 348)),
    "t10q4": (0, 2, (522, 672, 782, 802)),
    "t10q5": (0, 3, (463, 136, 802, 256)),
    "t11q1": (1, 1, (528, 152, 748, 292)),
    "t11q3": (1, 2, (478, 566, 738, 692)),
    "t11q4": (1, 3, (418, 66, 748, 268)),
}
DPI = 200

CSS = """
.p1 { --c: #1c5cc2; --tint: #eaf1fc; } .p2 { --c: #6b3fa0; --tint: #f1ebf8; }
.legend { display: flex; flex-wrap: wrap; gap: 6pt 16pt; font: 9pt var(--sans); color: #333; margin: 0 0 10pt; align-items: center; }
.legend .sw { display: inline-block; width: 18pt; height: 3pt; border-radius: 2pt; margin-right: 4pt; vertical-align: middle; }
.sw.ans { background: var(--c-ans); } .sw.abs { background: var(--c-abs); } .sw.t { background: var(--c-t); } .sw.n { background: var(--c-n); margin-left: -2pt; }
.sw.muted { background: var(--muted); } .legend .ruler { flex-basis: 100%; }
table.cmp { font-size: 9.6pt; margin: 4pt 0 6pt; } table.cmp td:first-child { font-weight: bold; font-family: var(--sans); font-size: 8.8pt; }
th.c-ans { color: var(--c-ans) !important; } th.c-abs { color: var(--c-abs) !important; } th.c-t { color: var(--c-t) !important; }
.key { background: var(--tint); border-left: 3pt solid var(--c); padding: 4pt 8pt; margin: 5pt 0; break-inside: avoid; }
.tags { display: flex; flex-wrap: wrap; gap: 4pt; margin: 0 0 6pt; }
.tags span { font: 8.6pt var(--sans); background: var(--tint); color: var(--c); border: 0.8pt solid var(--c); border-radius: 9pt; padding: 1pt 7pt; }
.qrow { display: flex; gap: 12pt; align-items: center; background: #fafafa; border: 0.6pt solid var(--rule); border-radius: 4pt; padding: 5pt 8pt; margin: 0 0 6pt; break-inside: avoid; }
.qrow img { max-width: 44%; max-height: 40mm; width: auto; height: auto; flex: 0 0 auto; mix-blend-mode: multiply; }
.wide svg.fig { max-width: 100% !important; max-height: 70mm !important; }
.qtext { margin: 0; font-size: 10pt; }
.ans { font: bold 10.5pt var(--sans); color: #fff; background: var(--c); border-radius: 4pt; padding: 4pt 10pt; display: inline-block; margin: 6pt 0 0; }
.flag { border: 1.2pt solid #d0021b; background: #fff3f1; border-radius: 4pt; padding: 5pt 8pt; margin: 0 0 6pt; font-size: 10pt; break-inside: avoid; }
.figrow.two > figure { flex: 0 1 auto; min-width: 0; }
.figrow.two svg.fig, .figrow.three svg.fig { max-height: 62mm; }
svg.fig.true { max-width: none !important; max-height: none !important; }
.fig line.n { stroke: var(--c-n); stroke-width: 2.2; } .fig line.t { stroke: var(--c-t); stroke-width: 2.2; }
.fig line.ans { stroke: var(--c-ans); stroke-width: 1.8; } .fig line.abs { stroke: var(--c-abs); stroke-width: 1.8; }
.card { break-inside: auto; }
h2.part.p2 { break-before: page; }
"""


def crops(pdfs):
    out = {}
    with tempfile.TemporaryDirectory() as td:
        pages = {}
        for name, (which, pg, box) in CROPS.items():
            key = (which, pg)
            if key not in pages:
                stem = pathlib.Path(td) / f"p{which}_{pg}"
                subprocess.run(["pdftoppm", "-r", str(DPI), "-f", str(pg), "-l", str(pg), "-png", "-singlefile",
                                str(pdfs[which]), str(stem)], check=True)
                pages[key] = Image.open(f"{stem}.png").convert("RGB")
            k = DPI / 100
            im = pages[key].crop(tuple(round(v * k) for v in box))
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=86, optimize=True)
            out[name] = (f'<img alt="Question figure from the memo" '
                         f'src="data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}">')
    return out


def main(t10, t11):
    figs = pk_figs.build_all()
    cr = crops([pathlib.Path(t10), pathlib.Path(t11)])
    body = (HERE / "pk_body.html").read_text()
    for kind, table in (("fig", figs), ("crop", cr)):
        missing = sorted(set(re.findall(r"\{\{%s:([a-z0-9_]+)\}\}" % kind, body)) - set(table))
        if missing:
            raise SystemExit(f"missing {kind}: {missing}")
        body = re.sub(r"\{\{%s:([a-z0-9_]+)\}\}" % kind, lambda m: table[m.group(1)], body)
    mj = ("<script>window.MathJax = { tex: { inlineMath: [['$', '$']], processEscapes: true }, "
          "svg: { fontCache: 'global' } };</script>"
          '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>')
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>MEC2047S Plane Kinetics Workthrough</title>'
            f"<style>{build_playbook.CSS}\n{CSS}\n{build_playbook.fig_css()}</style>{mj}</head><body>{body}</body></html>")
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    dst = out / "MEC2047S-Plane-Kinetics-Workthrough.html"
    dst.write_text(html)
    print(f"wrote {dst} ({len(html) / 1024:.0f} KB)")


if __name__ == "__main__":
    main(*sys.argv[1:3])
