"""Build the mock final exam and its separate explained memo.

    python3 build_mock.py
    node ../exams2025/render.js dist/MEC2047S-Mock-Final-Exam.html dist/MEC2047S-Mock-Final-Exam.pdf "MEC2047S MOCK FINAL EXAM" "100 marks · 3 hours"
    node ../exams2025/render.js dist/MEC2047S-Mock-Final-Exam-Memo.html dist/MEC2047S-Mock-Final-Exam-Memo.pdf "MEC2047S MOCK FINAL EXAM · MEMO" "✓ = 1 mark"
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "guides" / "practice"))
import build_pe  # noqa: E402
import mock_figs  # noqa: E402

COVER = """
.cover { text-align: center; padding-top: 22mm; } .cover .uni { font-size: 13pt; margin: 0 0 20pt; }
.ctitle { font-size: 22pt; margin: 0 0 4pt; } .csub { font-size: 18pt; margin: 0 0 24pt; }
.ctab { margin: 0 auto 20pt; text-align: left; } .ctab td { padding: 3pt 12pt 3pt 0; }
.ins { text-align: left; max-width: 150mm; margin: 0 auto; } .ins h3 { font-size: 12pt; margin: 0 0 6pt; }
.ins ol { padding-left: 20pt; } .ins li { margin: 3pt 0; }
.note { font-size: 10pt; color: #444; border-top: 1px solid #999; margin-top: 20pt; padding-top: 6pt; }
.q { margin-bottom: 18pt; }
.row > figure.side { max-width: 48%; }
"""


def main():
    figs = mock_figs.build_all()
    build_pe.CSS += COVER
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    exam = build_pe.assemble((HERE / "exam_body.html").read_text(), figs, {}, "MEC2047S Mock Final Exam")
    memo = build_pe.assemble(build_pe.check_ticks((HERE / "memo_body.html").read_text()), figs, {}, "MEC2047S Mock Final Exam Memo")
    (out / "MEC2047S-Mock-Final-Exam.html").write_text(exam)
    (out / "MEC2047S-Mock-Final-Exam-Memo.html").write_text(memo)
    print("wrote exam and memo")


if __name__ == "__main__":
    main()
