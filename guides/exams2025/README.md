# 2025 exam papers: MEC2047F memo and plain MEC2047S paper

- `build_f_memo.py <F-exam.pdf>`: unofficial memo for the MEC2047F June 2025 final, styled like the
  official MEC2047S 2025 memo. Statements and figures are cropped from the paper. The solutions are in
  `f_memo_body.html` and the diagrams in `f_memo_figs.py`. The build checks that the ticks in each
  question add up to its marks.
- `build_s_exam.py <S-memo.pdf>`: plain MEC2047S 13/11/2025 question paper, cropped from the
  official memo with the solutions removed, plus a grid sheet for Q4(b).
- `render.js <in.html> <out.pdf> "<header left>" "<header right>" [mathjax-dir]`: A4 PDF with
  the exam-style running header and "Page x of y" footer.

The source PDFs and the output in `dist/` are not committed.
