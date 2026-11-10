"""Figures for the explained revision-pack memo (polar free-body diagram for Tut 7 Q1)."""
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "textbook"))
sys.path.insert(0, str(ROOT / "guides" / "polar"))
from svgkit import Fig  # noqa: E402
import polar_figs  # noqa: E402

V = lambda x, y: np.array([float(x), float(y)])
T = lambda v: (float(v[0]), float(v[1]))


def U(deg):
    return V(math.cos(math.radians(deg)), math.sin(math.radians(deg)))


def t7q1_fbd():
    f = Fig(520, "Tut 7 Q1 free-body diagram of slider P in polar directions")
    th = 30
    O, B = V(0, 0), V(0.3, 0)
    P = 0.6 * U(th)
    er, et = U(th), U(th + 90)
    f.line(T(O), T(0.85 * U(th)), "ink", w=2)
    f.line(T(O), (0.6, 0), "muted", dash="3 4")
    f.line(T(P), T(B), "rope")
    f.pin(T(O))
    f.dot(T(B), label="B", ldx=8, ldy=12, anchor="start")
    f.text(T(O), "O", dx=-12, dy=8)
    f.arc(T(O), 40, 0, th, "muted", "θ = 30°", lr=60, la=12)
    f.arrow(T(P), T(P + 0.16 * er), "muted", "e_{r}", at=("E", 6), lpos=1.0)
    f.arrow(T(P), T(P + 0.16 * et), "muted", "e_{θ}", at=("N", 8), lpos=1.0)
    dPB = (B - P) / np.linalg.norm(B - P)
    f.arrow(T(P), T(P + 0.22 * dPB), "ans", "T", at=("E", 8), lpos=0.75)
    f.arrow(T(P), T(P + V(0, -0.22)), "abs", "W = mg", at=("W", 8), lpos=0.9)
    f.arrow(T(P - 0.17 * et), T(P), "ans", "R (from the slot)", at=("SE", 6), lpos=0.2)
    a1 = math.degrees(math.atan2(-er[1], -er[0]))
    a2 = math.degrees(math.atan2(dPB[1], dPB[0]))
    f.arc(T(P), 40, a1, a2, "muted", "φ", lr=54)
    f.dot(T(P), label="P", ldx=-12, ldy=-8, anchor="end")
    return f.svg()


def t7q1_kd():
    f = Fig(520, "Tut 7 Q1 kinetic diagram: m a_r and m a_theta")
    th = 30
    P = 0.6 * U(th)
    er, et = U(th), U(th + 90)
    f.line((0, 0), T(0.85 * U(th)), "ink", w=2)
    f.pin((0, 0))
    f.text((0, 0), "O", dx=-12, dy=8)
    f.arrow(T(P), T(P - 0.25 * er), "n", "m a_{r} = 0.2(−16.49) = −3.30 N", at=("NW", 14), lpos=0.55)
    f.arrow(T(P), T(P - 0.13 * et), "n", "m a_{θ} = 0.2(−8.47) = −1.69 N", at=("SE", 10), lpos=1.0)
    f.dot(T(P), label="P", ldx=-12, ldy=-8, anchor="end")
    return f.svg()


def build_all():
    out = {"t7q1_fbd": t7q1_fbd(), "t7q1_kd": t7q1_kd()}
    pf = polar_figs.build_all()
    for k in ("pu_unitvec", "pu_project", "pu_derivative", "sph_geom"):
        out[k] = pf[k]
    return out


if __name__ == "__main__":
    for k, v in build_all().items():
        print(k, len(v))
