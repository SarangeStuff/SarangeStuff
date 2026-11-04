# MEC2047 Dynamics Companion

A plain-language textbook for MEC2047S Dynamics I. Part I covers kinematics (L01–L17) with an
emphasis on relative velocity and acceleration vector diagrams; Part II covers kinetics (L19–L35).

- `dist/mec2047-kinematics-companion.html` – the built book (open in a browser).
- `src/` – chapter sources (`ch*.html`) and the page shell.
- `mech.py` – solves every Part I worked example (velocities, accelerations, ω, α).
- `kinetics.py` – checks every Part II worked example against the course answers.
- `figs.py`, `figs2.py`, `svgkit.py` – draw the mechanisms and to-scale vector diagrams as SVG.
- `build.py` – assembles the book: `python3 textbook/build.py`.
