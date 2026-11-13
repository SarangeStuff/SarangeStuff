# MEC2047S final exam (13 November 2026): unofficial memo

All ten questions solved independently and checked a second way (check_answers.py). Question figures are
cropped from the scanned paper with handwriting whited out (dist/ only); solution diagrams are in ex26_figs.py.
Tick counts are verified at build time (100 in total).

    python3 check_answers.py
    python3 build_memo.py <scanned-paper.pdf>
    node ../exams2025/render.js dist/MEC2047S-2026-Final-Exam-Memo.html dist/MEC2047S-2026-Final-Exam-Memo.pdf \
        "MEC2047S FINAL EXAM · NOVEMBER 2026" "Memo (unofficial)" [<mathjax-dir>]
