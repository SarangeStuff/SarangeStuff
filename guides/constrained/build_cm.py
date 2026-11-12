"""Build the constrained-motion + coordinate-vectors pack.

    python3 build_cm.py <MEC2047F_2025_CT1.pdf>
    node ../exams2025/render.js dist/MEC2047S-Constrained-Motion-and-Coordinates.html \
        dist/MEC2047S-Constrained-Motion-and-Coordinates.pdf "MEC2047S · CONSTRAINED MOTION + COORDINATE VECTORS" \
        "Pulleys · n–t · polar · spherical" [<local-mathjax-dir>]

Question figures are cropped from your CT1 PDF into dist/ only. Numbers are re-derived in check_answers.py.
"""
import base64
import io
import pathlib
import re
import subprocess
import sys
import tempfile

from PIL import Image

import cm_figs

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "guides" / "playbook"))
sys.path.insert(0, str(ROOT / "guides" / "planekinetics"))
import build_playbook  # noqa: E402
import build_pk  # noqa: E402

CROPS = {"ct1q1": (428, 232, 642, 496), "ct1q2": (495, 405, 650, 642), "ct1q3": (468, 680, 658, 902)}   # px at 90 dpi
DPI = 220


def crops(pdf):
    out = {}
    with tempfile.TemporaryDirectory() as td:
        stem = pathlib.Path(td) / "p"
        subprocess.run(["pdftoppm", "-r", str(DPI), "-f", "1", "-l", "1", "-png", "-singlefile", str(pdf), str(stem)], check=True)
        page = Image.open(f"{stem}.png").convert("RGB")
        for name, box in CROPS.items():
            im = page.crop(tuple(round(v * DPI / 90) for v in box))
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=86, optimize=True)
            out[name] = f'<img alt="CT1 question figure" src="data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}">'
    return out


def main(ct1):
    figs = cm_figs.build_all()
    cr = crops(pathlib.Path(ct1))
    body = (HERE / "cm_body.html").read_text()
    for kind, table in (("fig", figs), ("crop", cr)):
        missing = sorted(set(re.findall(r"\{\{%s:([a-z0-9_]+)\}\}" % kind, body)) - set(table))
        if missing:
            raise SystemExit(f"missing {kind}: {missing}")
        body = re.sub(r"\{\{%s:([a-z0-9_]+)\}\}" % kind, lambda m: table[m.group(1)], body)
    mj = ("<script>window.MathJax = { tex: { inlineMath: [['$', '$']], processEscapes: true }, "
          "svg: { fontCache: 'global' } };</script>"
          '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>')
    extra = (".qrow img { max-height: 52mm; } .qrow.tall img { height: 64mm; max-height: none; max-width: none; width: auto; }"
             " .key mjx-container[display='true'] { margin: 2pt 0 !important; }"
             " .grid svg.fig { max-width: 100%; max-height: 92mm; } .figrow > svg.fig { max-width: 100%; }")
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>MEC2047S Constrained Motion and Coordinates</title>'
            f"<style>{build_playbook.CSS}\n{build_pk.CSS}\n{extra}\n{build_playbook.fig_css()}</style>{mj}</head><body>{body}</body></html>")
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    dst = out / "MEC2047S-Constrained-Motion-and-Coordinates.html"
    dst.write_text(html)
    print(f"wrote {dst} ({len(html) / 1024:.0f} KB)")


if __name__ == "__main__":
    main(sys.argv[1])
