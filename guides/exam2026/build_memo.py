"""Build the memo for the MEC2047S final exam (13 November 2026).

    python3 build_memo.py <scanned-paper.pdf>
    node ../exams2025/render.js dist/MEC2047S-2026-Final-Exam-Memo.html dist/MEC2047S-2026-Final-Exam-Memo.pdf \
        "MEC2047S FINAL EXAM · NOVEMBER 2026" "Memo (unofficial)" [<mathjax-dir>]

Question figures are cropped from the scan (handwriting whited out) into dist/ only.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "guides" / "practice"))
import build_pe  # noqa: E402
import crops  # noqa: E402
import ex26_figs  # noqa: E402

EXTRA = """
.qbox { border: 0.8pt solid #bbb; background: #fafafa; border-radius: 4pt; padding: 6pt 9pt; margin: 0 0 6pt; break-inside: avoid; }
.qbox p { margin: 2pt 0; }
.qh { break-after: avoid; } .q { break-before: auto; }
img.fig-crop { width: 100%; max-height: 62mm; object-fit: contain; mix-blend-mode: multiply; }
.row > figure.side { max-width: 46%; }
.review { border: 1.2pt solid #d0021b; border-radius: 5pt; padding: 6pt 10pt; background: #fff6f4; margin-top: 14pt; }
table.ku { border-collapse: collapse; font-size: 10.5pt; margin: 4pt 0; } table.ku td, table.ku th { border-bottom: 0.6pt solid #ccc; padding: 2pt 8pt; text-align: left; }
"""


def main(scan):
    cr = crops.build(pathlib.Path(scan))
    build_pe.CSS += EXTRA
    memo = build_pe.assemble(build_pe.check_ticks((HERE / "memo_body.html").read_text()), ex26_figs.build_all(), cr,
                             "MEC2047S 2026 Final Exam Memo")
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    (out / "MEC2047S-2026-Final-Exam-Memo.html").write_text(memo)
    print("wrote memo")


if __name__ == "__main__":
    main(sys.argv[1])
