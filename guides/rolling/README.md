# Rolling, all of it

Kinematics of rolling (IC at the contact point, v = rω, a = rα, contact-point acceleration, gear on a rack),
kinetics (FBD/KD, assume no slip then check, particle vs rolling body, massless wheels) and every rolling case
in the course: cylinder on a 30° and a 60° slope, mock Q8 on the flat, the T10 bowling ball, the T11 rod in a
hoop, and a spool. Rigid-body energy is left out (off the syllabus this year).

    python3 check_answers.py
    python3 build_rl.py
    node ../exams2025/render.js dist/MEC2047S-Rolling.html dist/MEC2047S-Rolling.pdf "MEC2047S · ROLLING, ALL OF IT" "kinematics · kinetics · slip" [<mathjax-dir>]
