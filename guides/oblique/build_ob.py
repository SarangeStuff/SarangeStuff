"""Build 'Oblique impact, slowly' (the n-t idea from zero, then S25 Q6 and F25 Q8).

    python3 build_ob.py
    node ../exams2025/render.js dist/MEC2047S-Oblique-Impact-Slowly.html dist/MEC2047S-Oblique-Impact-Slowly.pdf \
        "MEC2047S · OBLIQUE IMPACT, SLOWLY" "n–t from zero · S25 Q6 · F25 Q8" [<local-mathjax-dir>]
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "guides" / "playbook"))
sys.path.insert(0, str(ROOT / "guides" / "planekinetics"))
import build_playbook  # noqa: E402
import build_pk  # noqa: E402
import ob_figs  # noqa: E402

EXTRA = """
.brk { break-before: page; } h2.part.p2 { break-before: auto; } h2.part.p2.brk { break-before: page; }
.big { font-size: 11pt; } table.ku td, table.ku th { padding: 3pt 8pt; }
.figrow > svg.fig { max-width: 100%; max-height: 95mm; } .grid svg.fig { max-width: 100%; max-height: 80mm; }
"""


def main():
    figs = ob_figs.build_all()
    body = (HERE / "ob_body.html").read_text()
    missing = sorted(set(re.findall(r"\{\{fig:([a-z0-9_]+)\}\}", body)) - set(figs))
    if missing:
        raise SystemExit(f"missing figures: {missing}")
    body = re.sub(r"\{\{fig:([a-z0-9_]+)\}\}", lambda m: figs[m.group(1)], body)
    mj = ("<script>window.MathJax = { tex: { inlineMath: [['$', '$']], processEscapes: true }, "
          "svg: { fontCache: 'global' } };</script>"
          '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>')
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Oblique Impact, Slowly</title>'
            f"<style>{build_playbook.CSS}\n{build_pk.CSS}\n{EXTRA}\n{build_playbook.fig_css()}</style>{mj}</head><body>{body}</body></html>")
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    dst = out / "MEC2047S-Oblique-Impact-Slowly.html"
    dst.write_text(html)
    print(f"wrote {dst} ({len(html) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
