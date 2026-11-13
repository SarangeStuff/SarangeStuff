"""Build 'Rolling, all of it' (kinematics, kinetics, slip checks, every rolling case in the course).

    python3 build_rl.py
    node ../exams2025/render.js dist/MEC2047S-Rolling.html dist/MEC2047S-Rolling.pdf "MEC2047S · ROLLING, ALL OF IT" "kinematics · kinetics · slip" [<mathjax-dir>]
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
import rl_figs  # noqa: E402

EXTRA = """
.brk { break-before: page; } h2.part.p2 { break-before: auto; } h2.part.p2.brk { break-before: page; }
.grid svg.fig { max-width: 100%; max-height: 72mm; } .figrow > svg.fig { max-width: 100%; max-height: 80mm; }
table.ku td, table.ku th { padding: 3pt 7pt; }
"""


def main():
    figs = rl_figs.build_all()
    body = (HERE / "rl_body.html").read_text()
    missing = sorted(set(re.findall(r"\{\{fig:([a-z0-9_]+)\}\}", body)) - set(figs))
    if missing:
        raise SystemExit(f"missing figures: {missing}")
    body = re.sub(r"\{\{fig:([a-z0-9_]+)\}\}", lambda m: figs[m.group(1)], body)
    mj = ("<script>window.MathJax = { tex: { inlineMath: [['$', '$']], processEscapes: true }, "
          "svg: { fontCache: 'global' } };</script>"
          '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>')
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Rolling, All of It</title>'
            f"<style>{build_playbook.CSS}\n{build_pk.CSS}\n{EXTRA}\n{build_playbook.fig_css()}</style>{mj}</head><body>{body}</body></html>")
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    (out / "MEC2047S-Rolling.html").write_text(html)
    print(f"wrote ({len(html) // 1024} KB)")


if __name__ == "__main__":
    main()
