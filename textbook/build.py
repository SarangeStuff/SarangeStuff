"""Assemble the textbook: shell + chapters, with {{fig:name}} replaced by SVG
and the contents list built from each chapter's <section class="chapter">.

    python3 build.py      ->  dist/mec2047-kinematics-companion.html
"""
import pathlib
import re

from figs import build_all
import figs2  # noqa: F401  (registers the Part II figures)

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "dist" / "mec2047-kinematics-companion.html"


def main():
    figs = build_all()
    chapters = sorted(SRC.glob("ch*.html"))
    body = "\n".join(p.read_text() for p in chapters)

    missing = set()

    def fig(m):
        name = m.group(1)
        if name not in figs:
            missing.add(name)
            return f"<!-- missing fig {name} -->"
        return figs[name]

    body = re.sub(r"\{\{fig:([a-z0-9_]+)\}\}", fig, body)
    if missing:
        raise SystemExit(f"missing figures: {sorted(missing)}")

    toc = []
    for m in re.finditer(r'<section class="chapter([^"]*)" id="([^"]+)" data-num="([^"]*)" data-short="([^"]+)"', body):
        extra, cid, num, short = m.groups()
        if "hero" in extra:
            continue
        if "part-divider" in extra:
            toc.append(f'<li class="toc-part"><a href="#{cid}">Part II · Kinetics</a></li>')
            continue
        if cid == "ch1":
            toc.append('<li class="toc-part"><a href="#start">Part I · Kinematics</a></li>')
        toc.append(f'<li><a href="#{cid}"><span class="toc-num">{num}</span><span>{short}</span></a></li>')
    head = (SRC / "shell_head.html").read_text().replace("{{toc}}", "\n".join(toc))
    tail = (SRC / "shell_tail.html").read_text()
    html = head + body + tail
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html)
    print(f"wrote {OUT} ({len(html) / 1024:.0f} KB, {len(chapters)} chapter files, {len(figs)} figures)")


if __name__ == "__main__":
    main()
