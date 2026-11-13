"""Solution diagrams for the MEC2047S November 2026 final exam memo."""
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
for sub in ("textbook", "guides/planekinetics"):
    sys.path.insert(0, str(ROOT / sub))
from svgkit import Fig  # noqa: E402
from pk_figs import true_size, ppu_for, right_mark, curl  # noqa: E402

V = lambda x, y: np.array([float(x), float(y)])
T = lambda v: (float(v[0]), float(v[1]))
U = lambda d: V(math.cos(math.radians(d)), math.sin(math.radians(d)))


def s1():
    f = Fig(70, "Q1 acceleration components at A (dip, centre above) and at B (hump, centre below)")
    A = V(0, 0)
    pts = [A + V(x, 0.12 * x * x) for x in np.linspace(-2, 2, 21)]
    f.path_world([T(p) for p in pts], "muted")
    f.dot(T(A)); f.text(T(A), "A", dy=14)
    f.arrow(T(A + V(0, 0.08)), T(A + V(0.9, 0.08)), "abs", "v_{A} = 3", at=("N", 10), lpos=0.85)
    f.arrow(T(A), T(A + V(-1.4, 0)), "t", "a_{t} = 0.75 (slowing)", at=("S", 12), lpos=0.6)
    f.arrow(T(A), T(A + V(0, 0.9)), "n", "a_{n} = 0.225 ↑ (to centre)", at=("W", 6), lpos=0.9)
    B = V(5.6, 0.6)
    pts = [B + V(x, -0.15 * x * x) for x in np.linspace(-2, 2, 21)]
    f.path_world([T(p) for p in pts], "muted")
    f.dot(T(B)); f.text(T(B), "B", dy=-14)
    f.arrow(T(B), T(B + V(1.3, 0)), "t", "a_{t} = 0.70 (speeding up)", at=("N", 10), lpos=0.7)
    f.arrow(T(B), T(B + V(0, -0.9)), "n", "a_{n} ↓ (to centre)", at=("E", 6), lpos=0.9)
    return f.svg()


def s4():
    f = Fig(6.5, "Q4 the drop's velocity relative to the car arriving at the windshield, and the normal n")
    Bp = V(0, 0)
    t_dir, n_dir = U(140), U(50)
    f.line(T(Bp - 14 * t_dir), T(Bp + 14 * t_dir), "ink")
    f.text(T(Bp + 14 * t_dir), "windshield", "muted", dy=-10)
    f.line(T(Bp), T(Bp + 22 * n_dir), "cons"); f.text(T(Bp + 22 * n_dir), "n", "n", dx=6, anchor="start")
    rel = V(-27.78, -10.85)
    f.arrow(T(Bp - 0.8 * rel), T(Bp), "ans", "v_{D/C} = 29.8 m/s", at=("S", 14), lpos=0.35)
    f.line(T(Bp), T(Bp + V(24, 0)), "muted", dash="3 3")
    f.arc(T(Bp), 70, 21.3, 50, "ans", "28.7°", lr=92, la=38)
    f.arc(T(Bp), 44, 0, 21.3, "muted", "21.3°", lr=60, la=9)
    f.dot(T(Bp)); f.text(T(Bp), "B", dx=-8, dy=14, anchor="end")
    o = V(-34, 20)
    f.arrow(T(o), T(o + V(27.78, 0) * 0.5), "abs", "v_{C} = 27.8", at=("N", 10), lpos=0.5)
    f.arrow(T(o), T(o + V(0, -10.85) * 0.5), "abs", "v_{D} = 10.85", at=("W", 6), lpos=0.6)
    f.arrow(T(o + V(13.89, 0)), T(o + V(0, -5.43)), "ans", "v_{D/C} = v_{D} − v_{C}", at=("SE", 4), lpos=0.5)
    return f.svg()


A5, B5, C5, D5, E5 = V(0, 0), V(0, 0.09), V(0.225, 0), V(0.225, 0.18), V(0.45, 0.27)


def _mech5(f):
    f.link(T(A5), T(B5), w=8); f.link(T(C5), T(D5), w=8); f.link(T(B5), T(E5), w=8)
    f.pivot(T(A5)); f.pivot(T(C5)); f.pin(T(B5)); f.pin(T(D5)); f.pin(T(E5), 3)
    for p, s, dx, dy in ((A5, "A", -12, -4), (B5, "B", -12, -2), (C5, "C", 12, -4), (D5, "D", 10, 10), (E5, "E", 10, -6)):
        f.text(T(p), s, dx=dx, dy=dy, anchor="end" if dx < 0 else "start")


def s5q():
    f = Fig(ppu_for(0.05), "Q5 mechanism redrawn to scale 1:5")
    _mech5(f)
    f.dim(T(V(-0.07, 0)), T(V(-0.07, 0.09)), "90", off=0, side="l")
    f.dim(T(V(-0.07, 0.09)), T(V(-0.07, 0.18)), "90", off=0, side="l")
    f.dim(T(V(-0.07, 0.18)), T(V(-0.07, 0.27)), "90", off=0, side="l")
    f.dim(T(V(0, -0.05)), T(V(0.225, -0.05)), "225 mm", off=0, side="r")
    f.dim(T(V(0.225, -0.05)), T(V(0.45, -0.05)), "225 mm", off=0, side="r")
    f.arc(T(A5), 20, 150, 30, "abs", "6 rad/s CW", arrow=True, ccw=False, lr=34, la=90, ldy=26)
    f.set_scalebar(0.05, "1 cm = 50 mm")
    return true_size(f.svg())


def s5v():
    f = Fig(ppu_for(0.05), "Q5 velocities: v_B and v_D both horizontal, so their perpendiculars are parallel: no IC, omega_BDE = 0")
    _mech5(f)
    f.line(T(B5 + V(0, -0.12)), T(B5 + V(0, 0.25)), "cons"); f.line(T(D5 + V(0, -0.3)), T(D5 + V(0, 0.16)), "cons")
    f.text(T(D5 + V(0, 0.17)), "⊥ v_D", "muted", dy=-8); f.text(T(B5 + V(0, 0.26)), "⊥ v_B", "muted", dy=-8)
    for p in (B5, D5, E5):
        f.arrow(T(p), T(p + V(0.08, 0)), "ans", "0.54 m/s", at=("N", 10), lpos=0.7)
    f.set_scalebar(0.05, "1 cm = 50 mm")
    return true_size(f.svg())


def s5a():
    f = Fig(ppu_for(0.5), "Q5 acceleration polygon, true scale 1 cm = 0.5 m/s^2")
    o = V(0, 0); b = V(0, -3.24); dn = V(0, -1.62); d = V(-0.648, -1.62); e = V(-1.296, 0)
    perp = U(111.8)
    f.line(T(b - 0.4 * perp), T(e + 0.6 * perp), "cons"); f.line(T(dn + V(0.5, 0)), T(dn + V(-1.6, 0)), "cons")
    f.arrow(T(o), T(b), "abs", "a_{B} = 3.24 (B → A)", at=("E", 8), lpos=0.6)
    f.arrow(T(o), T(dn), "n", "(a_{D})_{n} = 1.62 (D → C)", at=("E", 8), lpos=0.5)
    f.arrow(T(dn), T(d), "t", "(a_{D})_{t} = 0.648", at=("S", 12), lpos=0.5)
    f.arrow(T(b), T(d), "t", "(a_{D/B})_{t} = 1.745 ⊥ BD", at=("W", 8), lpos=0.5)
    f.arrow(T(d), T(e), "muted", "(a_{E/D})_{t}", at=("W", 8), lpos=0.5)
    f.arrow(T(o), T(e), "ans", "a_{E} = 1.30 m/s² ←", at=("N", 16), lpos=0.5, dashed=True)
    for p, s, dx, dy in ((o, "o", 8, -6), (b, "b", 8, 6), (d, "d", -8, 6), (e, "e", -8, -4)):
        f.text(T(p), s, dx=dx, dy=dy, anchor="end" if dx < 0 else "start")
    f.set_scalebar(0.5, "1 cm = 0.5 m/s²")
    return true_size(f.svg())


def s9():
    f = Fig(0.0035, "Q9 momentum triangle (kg·km/h)")
    o = V(0, 0); pA = V(0, 58500); pB = V(27279, 0)
    f.arrow(T(o), T(pB), "abs", "m_{B}v_{B} = 1500 v_{B}", at=("S", 12), lpos=0.5)
    f.arrow(T(pB), T(pB + pA), "abs", "m_{A}v_{A} = 1300(45) = 58 500", at=("E", 6), lpos=0.5)
    f.arrow(T(o), T(pB + pA), "ans", "(m_{A}+m_{B})v", at=("W", 8), lpos=0.55)
    f.line(T(o), T(V(0, 40000)), "muted", dash="3 3")
    f.arc(T(o), 50, 65, 90, "ans", "25°", lr=66, la=80)
    return f.svg()


def s10():
    f = Fig(150, "Q10 FBD and KD of the spool (x up the slope)")
    th = 20
    u = U(180 - th)                 # up the slope (to the left)
    nrm = U(90 - th)                # outward normal
    out = []
    for x0, kind in ((0.0, "fbd"), (1.7, "kd")):
        C = V(x0, 0) + V(0, 0)
        G = C + 0.45 * nrm
        f.line(T(C - 0.75 * u), T(C + 0.75 * u), "muted")
        f.circle(T(G), 0.45, "outline"); f.circle(T(G), 0.2, "outline thin", dash="4 3")
        f.dot(T(G)); f.text(T(G), "G", dx=8, dy=-8, anchor="start")
        if kind == "fbd":
            S = G - 0.2 * nrm
            f.arrow(T(S), T(S + 0.6 * u), "ans", "T", at=("N", 8), lpos=1.0)
            f.arrow(T(G), T(G + V(0, -0.6)), "ans", "mg = 294.3 N", at=("E", 6), lpos=0.9)
            f.arrow(T(C - 0.4 * nrm), T(C), "ans", "N", at=("E", 6), lpos=0.3)
            f.arrow(T(C), T(C - 0.45 * u), "ans", "F (down the slope)", at=("S", 12), lpos=0.9)
            f.text(T(G + 0.6 * nrm), "FBD", "muted")
        else:
            f.arrow(T(G), T(G + 0.5 * u), "abs", "m a_{G}", at=("N", 10), lpos=0.9)
            f.arc(T(G), 22, -40, 200, "abs", "I_{G}α", arrow=True, ccw=True, lr=34, la=80)
            f.text(T(G + 0.6 * nrm), "KD (rolling up the slope)", "muted")
    return f.svg()


def build_all():
    return {n: globals()[n]() for n in ("s1", "s4", "s5q", "s5v", "s5a", "s9", "s10")}


if __name__ == "__main__":
    for k_, v_ in build_all().items():
        print(k_, len(v_))
