"""Build the clean CT2 2026 question + memo.

    python3 build_ct2.py
    node ../exams2025/render.js dist/MEC2047S-2026-CT2-Clean-Memo.html dist/MEC2047S-2026-CT2-Clean-Memo.pdf \
        "MEC2047S 2026 CLASS TEST 2" "Question (reconstructed) and memo" [<local-mathjax-dir>]
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "guides" / "exams2025"))
sys.path.insert(0, str(ROOT / "guides" / "hwmemo"))
import build_f_memo  # noqa: E402
import build_hw  # noqa: E402
import ct2_figs  # noqa: E402

EXTRA = """
ol.parts { list-style: lower-alpha; margin: 4pt 0; } table.ku { border-collapse: collapse; font-size: 10.5pt; margin: 4pt 0; }
table.ku td, table.ku th { border-bottom: 0.6pt solid #ccc; padding: 2pt 8pt; text-align: left; }
ul.tight { margin: 2pt 0; padding-left: 16pt; }
.row > figure.side { max-width: 52%; }
"""


def main():
    figs = ct2_figs.build_all()
    body = (HERE / "ct2_body.html").read_text()
    body = re.sub(r"\{\{fig:([a-z0-9_]+)\}\}", lambda m: figs[m.group(1)], body)
    mj = ("<script>window.MathJax = { tex: { inlineMath: [['$', '$']], processEscapes: true }, "
          "svg: { fontCache: 'global' } };</script>"
          '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>')
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>MEC2047S 2026 CT2 Clean Memo</title>'
            f"<style>{build_f_memo.CSS}\n{build_f_memo.fig_css()}\n{build_hw.CSS}\n{EXTRA}</style>{mj}</head><body>{body}</body></html>")
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    dst = out / "MEC2047S-2026-CT2-Clean-Memo.html"
    dst.write_text(html)
    print(f"wrote {dst} ({len(html) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
