"""Question-figure crops from the scanned paper, with handwritten notes whited out.

Boxes are in pixels of the scan rendered at 80 dpi: (scan page, crop box, [white-out boxes])."""
import pathlib
import sys
import tempfile

from PIL import ImageDraw

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "guides" / "exams2025"))
from build_s_exam import b64png, render, trim_bottom  # noqa: E402

DPI = 200
K = DPI / 80
CROPS = {
    "q1": (5, (150, 240, 520, 400), []),
    "q2": (5, (236, 480, 458, 668), [(236, 603, 352, 668)]),
    "q4": (1, (160, 205, 470, 392), [(300, 375, 470, 392)]),
    "q6": (2, (180, 118, 480, 272), []),
    "q7": (2, (128, 402, 470, 592), [(338, 446, 353, 467), (128, 466, 189, 495), (128, 495, 186, 530), (452, 402, 470, 420)]),
    "q8": (3, (305, 95, 570, 268), [(420, 88, 570, 118)]),
    "q9": (3, (200, 405, 425, 585), []),
    "q10": (4, (150, 282, 560, 442), [(540, 282, 560, 442)]),
}


def build(scan, out_png_dir=None):
    out, pages = {}, {}
    with tempfile.TemporaryDirectory() as td:
        for name, (pg, box, boxes) in CROPS.items():
            if pg not in pages:
                pages[pg] = render(scan, pg, pathlib.Path(td), dpi=DPI)
            im = pages[pg].crop(tuple(round(v * K) for v in box))
            d = ImageDraw.Draw(im)
            for bx0, by0, bx1, by1 in boxes:
                d.rectangle(((bx0 - box[0]) * K, (by0 - box[1]) * K, (bx1 - box[0]) * K, (by1 - box[1]) * K), fill="white")
            im = trim_bottom(im)
            if out_png_dir:
                im.save(pathlib.Path(out_png_dir) / f"{name}.png")
            out[name] = f'<img class="crop fig-crop" alt="Figure for {name.upper()}" src="data:image/png;base64,{b64png(im)}">'
    return out


if __name__ == "__main__":
    build(pathlib.Path(sys.argv[1]), sys.argv[2])
