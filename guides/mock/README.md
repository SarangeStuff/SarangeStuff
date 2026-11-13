# MEC2047S mock final exam + explained memo

A 100-mark paper in the pattern of the 2025 MEC2047F/S finals (Section A kinematics, Section B kinetics),
with a separate memo that explains why every direction is chosen. check_answers.py solves each question
and checks it by a second route. Builds reuse ../practice/build_pe.py (shared styles and tick checking).

    python3 check_answers.py
    python3 build_mock.py
    node ../exams2025/render.js dist/MEC2047S-Mock-Final-Exam.html dist/MEC2047S-Mock-Final-Exam.pdf "MEC2047S MOCK FINAL EXAM" "100 marks · 3 hours"
    node ../exams2025/render.js dist/MEC2047S-Mock-Final-Exam-Memo.html dist/MEC2047S-Mock-Final-Exam-Memo.pdf "MEC2047S MOCK FINAL EXAM · MEMO" "✓ = 1 mark"
