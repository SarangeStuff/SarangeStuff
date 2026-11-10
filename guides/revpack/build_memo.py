"""Build the explained memo for the 2026 tutorial revision pack.

    python3 build_memo.py <image-dir>[:<image-dir>...]

The slide snapshots come from your own lecture PDFs (L06, L07, L08) and Tut02,
rendered to JPEGs named like L06-07.jpg and c_t02.jpg in <slide-image-dir>.
They are embedded in dist/ only and are not committed to the repository.
"""
import base64
import os
import io
import pathlib
import re
import sys

from PIL import Image

import memo_figs as polar_figs

HERE = pathlib.Path(__file__).parent
TEXTBOOK = HERE.parents[1] / "textbook" / "src"

EXTRA_CSS = """
.page { max-width: 820px; margin: 0 auto; padding-block: 28px 60px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.hero h1 { margin: 10px 0 14px; } .hero h1 em { font-style: normal; color: var(--c-abs); }
.contents { border: 1px solid var(--rule); background: var(--paper); border-radius: 6px; padding: 12px 18px; margin-top: 18px; }
.contents h2 { font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }
.memo { font-family: var(--f-display); font-size: 0.92rem; color: var(--muted); margin: 0.2rem 0 0.6rem; }\n.contents ol { columns: 2; column-gap: 28px; margin: 8px 0 0; padding-left: 20px; font-family: var(--f-display); font-size: 0.95rem; }
.contents a { color: var(--ink); text-decoration: none; } .contents a:hover { color: var(--c-abs); }
@media (max-width: 640px) { .contents ol { columns: 1; } }
figure.slide { margin: 1.2rem 0; } figure.slide img { width: 100%; height: auto; display: block; border: 1px solid var(--rule); border-radius: 4px; background: #fff; }
figure.slide figcaption { font-family: var(--f-display); font-size: 0.84rem; color: var(--muted); margin-top: 6px; }
table.six td, table.six th { text-align: center; font-size: 1.05rem; } table.six th:first-child { text-align: left; }
.example > .ex-head h3 { margin: 0; font-size: 1.2rem; }
.cheat { border: 2px solid var(--ink); border-radius: 8px; padding: 14px 18px; margin-top: 1.6rem; background: var(--paper); }
.cheat h3 { margin-top: 0; }
.cheat-grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 4px 26px; font-size: 0.95rem; }
.cheat h4 { margin-top: 0.9rem; font-size: 0.8rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
.cheat p, .cheat ol, .cheat ul { margin: 0.3rem 0; } .cheat ol, .cheat ul { padding-left: 18px; }
@media (max-width: 640px) { .cheat-grid { grid-template-columns: minmax(0, 1fr); } }
@media print { .cheat { break-inside: avoid; } figure.slide { break-inside: avoid; } .eq { overflow: visible !important; } .contents ol { columns: 1; } }
"""


def img_tag(path):
    im = Image.open(path).convert("RGB")
    if im.width > 1000:
        im = im.resize((1000, round(im.height * 1000 / im.width)))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=78, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'<img src="data:image/jpeg;base64,{b64}" alt="Lecture slide snapshot" loading="lazy">'


def main(imgdir):
    imgdir = pathlib.Path(imgdir)
    head = (TEXTBOOK / "shell_head.html").read_text()
    style = re.search(r"<style>.*?</style>", head, re.S).group(0).replace("</style>", EXTRA_CSS + "</style>")
    fonts = re.search(r'<link rel="stylesheet" href="https://fonts[^>]+>', head).group(0)
    tail = (TEXTBOOK / "shell_tail.html").read_text()
    mathjax = tail[tail.index("<script>\n/* Any inline equation"):]
    body = (HERE / "memo_body.html").read_text()
    figs = polar_figs.build_all()
    body = re.sub(r"\{\{fig:([a-z0-9_]+)\}\}", lambda m: figs[m.group(1)], body)
    dirs = [pathlib.Path(p) for p in str(imgdir).split(os.pathsep)]
    def find(name):
        for d in dirs:
            if (d / f"{name}.jpg").exists():
                return d / f"{name}.jpg"
        raise SystemExit(f"missing image {name}")
    body = re.sub(r"\{\{img:([A-Za-z0-9_-]+)\}\}", lambda m: img_tag(find(m.group(1))), body)
    html = ("<title>Revision Pack Explained</title>\n"
            '<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<meta name="description" content="MEC2047S 2026 tutorial revision pack with explained solutions.">\n'
            + fonts + "\n" + style + "\n" + body + "\n" + mathjax)
    out = HERE / "dist" / "revision-pack-explained.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html)
    print(f"wrote {out} ({len(html) / 1024:.0f} KB)")


if __name__ == "__main__":
    main(sys.argv[1])
