"""Build the MEC2047S problem-solving playbook (topic detector + one card per topic).

    python3 build_playbook.py
    node ../exams2025/render.js dist/MEC2047S-Problem-Solving-Playbook.html dist/MEC2047S-Problem-Solving-Playbook.pdf \
        "MEC2047S DYNAMICS · PROBLEM-SOLVING PLAYBOOK" "spot it · run the flow" [<local-mathjax-dir>]

Diagrams are reused from the textbook (textbook/figs.py) and the polar guide (guides/polar/polar_figs.py).
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "textbook"))
sys.path.insert(0, str(ROOT / "guides" / "polar"))
import figs  # noqa: E402
import figs2  # noqa: E402,F401  (registers the kinetics diagrams in figs.FIGS)
import polar_figs  # noqa: E402

CSS = """
:root { --bg: #fff; --paper: #fff; --ink: #141a22; --muted: #566273; --rule: #d3d9e2;
  --c-abs: #1c5cc2; --c-n: #b25c00; --c-t: #12804a; --c-ans: #c0154c; --c-cons: #8791a1; --link: #c9d3e0;
  --tint-abs: #e6eefb; --tint-n: #fbefe0; --tint-t: #e2f3e9; --tint-ans: #fbe6ed; color-scheme: light;
  --sans: 'Liberation Sans', 'DejaVu Sans', Arial, sans-serif; }
.pa { --c: #1c5cc2; --tint: #eaf1fc; } .pb { --c: #12804a; --tint: #e7f5ec; }
.pc { --c: #b25c00; --tint: #fcf1e4; } .pd { --c: #b3124a; --tint: #fbe9ef; } .pt { --c: #4b5563; --tint: #eef0f3; }
body { font: 10.5pt/1.42 'Liberation Serif', 'Times New Roman', serif; color: var(--ink); background: #fff; margin: 0; }
h1, h2, h3, h4, .kicker, .spot b, table th, .n, figcaption, .seen { font-family: var(--sans); }
.hero { border-bottom: 2.5pt solid var(--ink); padding-bottom: 8pt; margin-bottom: 10pt; }
.kicker { text-transform: uppercase; letter-spacing: 0.14em; font-size: 9pt; color: var(--muted); margin: 0; }
.hero h1 { font-size: 26pt; margin: 2pt 0 4pt; letter-spacing: -0.01em; }
.lede { margin: 0; font-size: 11pt; color: #333; }
h2 { font-size: 14pt; margin: 14pt 0 6pt; break-after: avoid; }
h2.part { color: #fff; background: var(--c); padding: 5pt 10pt; border-radius: 4pt; margin-top: 0; }
ol.routine { margin: 0; padding-left: 18pt; } ol.routine li { margin: 3pt 0; }
table { border-collapse: collapse; width: 100%; }
table.choose, table.ku, table.moi { break-inside: avoid; }
table.detect, table.choose { font-size: 9.6pt; }
table th { text-align: left; font-size: 8.5pt; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted);
  border-bottom: 1.4pt solid var(--ink); padding: 3pt 6pt; }
table td { padding: 3pt 6pt; border-bottom: 0.6pt solid var(--rule); vertical-align: top; }
table.detect td:nth-child(2) { font-weight: bold; white-space: nowrap; color: var(--c); }
table.detect td:nth-child(3) { text-align: center; font-family: var(--sans); font-weight: bold; color: #fff; background: var(--c); width: 26pt; }
table.detect tr { break-inside: avoid; }
.tip { font-size: 9.6pt; font-style: italic; color: #333; margin: 6pt 0 0; }
.card { border: 1pt solid var(--c); border-left: 5pt solid var(--c); border-radius: 5pt; padding: 7pt 11pt 8pt; margin: 0 0 10pt; }
.card h3 { font-size: 13pt; margin: 0 0 5pt; display: flex; align-items: center; gap: 7pt; break-after: avoid; }
.n { display: inline-flex; align-items: center; justify-content: center; min-width: 19pt; height: 19pt; border-radius: 10pt;
  background: var(--c); color: #fff; font-size: 10pt; padding: 0 4pt; }
.spot { background: var(--tint); border-radius: 3pt; padding: 4pt 8pt; margin: 0 0 6pt; font-size: 10pt; break-inside: avoid; }
.spot b { text-transform: uppercase; letter-spacing: 0.08em; font-size: 8pt; color: var(--c); margin-right: 6pt; }
.big { background: var(--tint); border-left: 3pt solid var(--c); padding: 4pt 8pt; margin: 4pt 0 6pt; font-size: 10.6pt; break-inside: avoid; }
.grid { display: grid; grid-template-columns: minmax(0, 1.3fr) minmax(0, 1fr); gap: 12pt; align-items: start; }
.grid > div { min-width: 0; }
h4 { font-size: 8.5pt; text-transform: uppercase; letter-spacing: 0.08em; color: var(--c); margin: 6pt 0 2pt; break-after: avoid; }
.grid > div > h4:first-child { margin-top: 0; }
ol.flow { margin: 0; padding-left: 16pt; } ol.flow > li { margin: 2pt 0; break-inside: avoid; }
ol.flow ul, ul.tight { margin: 1pt 0; padding-left: 14pt; } ul.tight li { margin: 1.5pt 0; break-inside: avoid; }
ol.cols2 { columns: 2; column-gap: 20pt; }
p { margin: 3pt 0; }
.why { font-style: italic; color: #333; font-size: 10pt; }
.small { font-size: 9pt; color: var(--muted); }
.watch { background: #fff6f4; border-left: 3pt solid #d0021b; padding: 3pt 8pt 4pt; margin: 6pt 0 0; break-inside: avoid; }
.watch h4 { color: #b0021a; margin-top: 2pt; } .watch ul { margin: 0; padding-left: 14pt; } .watch li { margin: 1.5pt 0; }
.seen { font-size: 8.8pt; color: var(--muted); margin: 5pt 0 0; } .seen::before { content: "↗ "; color: var(--c); }
table.ku, table.moi { font-size: 9.6pt; margin: 2pt 0; } table.ku td:first-child { white-space: nowrap; }
figure { margin: 0; break-inside: avoid; } figcaption { font-size: 8.6pt; color: var(--muted); text-align: center; margin-top: 3pt; line-height: 1.3; }
.figrow { display: flex; justify-content: center; gap: 12pt; margin: 6pt 0 2pt; break-inside: avoid; }
.figrow > svg.fig { max-width: 52%; max-height: 62mm; }
.grid svg.fig { max-width: 235px; max-height: 58mm; }
.figrow.three svg.fig { max-height: 52mm; }
.figrow.three > figure { flex: 1 1 0; min-width: 0; }
.walk p { font-size: 10pt; }
svg.fig { display: block; margin: 4pt auto; max-width: 100%; height: auto; overflow: visible;
  font-family: 'Liberation Serif', 'Times New Roman', serif; font-size: 14px; }
mjx-container[jax="SVG"] { max-width: 100%; }
"""


def fig_css():
    head = (ROOT / "textbook" / "src" / "shell_head.html").read_text()
    return "\n".join(l for l in head.splitlines() if l.startswith(".fig "))


def main():
    allfigs = dict(figs.build_all())
    allfigs.update(polar_figs.build_all())
    body = (HERE / "playbook_body.html").read_text()
    missing = sorted(set(re.findall(r"\{\{fig:([a-z0-9_]+)\}\}", body)) - set(allfigs))
    if missing:
        raise SystemExit(f"missing figures: {missing}")
    body = re.sub(r"\{\{fig:([a-z0-9_]+)\}\}", lambda m: allfigs[m.group(1)], body)
    mj = ("<script>window.MathJax = { tex: { inlineMath: [['$', '$']], processEscapes: true }, "
          "svg: { fontCache: 'global' } };</script>"
          '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>')
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>MEC2047S Problem-Solving Playbook</title>'
            f"<style>{CSS}\n{fig_css()}</style>{mj}</head><body>{body}</body></html>")
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    dst = out / "MEC2047S-Problem-Solving-Playbook.html"
    dst.write_text(html)
    print(f"wrote {dst} ({len(html) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
