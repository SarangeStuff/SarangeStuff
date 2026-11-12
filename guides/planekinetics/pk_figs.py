"""Diagrams for the plane-kinetics workthrough (Tutorials 10 and 11).

Colour code used everywhere:  forces (FBD) = red "ans";  kinetic-diagram terms (m a_G, I_G alpha) = blue "abs";
accelerations on kinematic diagrams = green "t" / orange "n";  geometry and dimensions = grey "muted".
Figures marked TRUE are emitted with a physical width in mm, so their scale bars are exactly 1 cm
when the PDF is printed at 100 %.
"""
import math
import pathlib
import re
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "textbook"))
from svgkit import Fig  # noqa: E402

V = lambda x, y: np.array([float(x), float(y)])
T = lambda v: (float(v[0]), float(v[1]))
PX_PER_CM = 96 / 2.54          # CSS px per cm


def U(deg):
    return V(math.cos(math.radians(deg)), math.sin(math.radians(deg)))


def true_size(svg):
    """Give the SVG a physical width so 1 px of the drawing = 1 CSS px = 1/96 in on paper."""
    m = re.search(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+) [\d.]+" width="(\d+)"', svg)
    w = float(m.group(1))
    svg = svg.replace(f'width="{m.group(2)}"', f'width="{w * 25.4 / 96:.1f}mm"', 1)
    return svg.replace('class="fig ', 'class="fig true ', 1)


def ppu_for(units_per_cm):
    """px per world unit for a scale of 1 cm = units_per_cm."""
    return PX_PER_CM / units_per_cm


def poly(f, pts, cls="body"):
    f.path_world([T(p) for p in pts] + [T(pts[0])], cls)


def curl(f, c, label, cw=True, r=20, start=None):
    """Moment / angular-acceleration curl drawn at c."""
    if cw:
        a1, a2 = (150 if start is None else start), 30
        f.arc(T(c), r, a1, a2, "abs", label, arrow=True, ccw=False, lr=r + 14, la=90)
    else:
        a1, a2 = (30 if start is None else start), 150
        f.arc(T(c), r, a1, a2, "abs", label, arrow=True, ccw=True, lr=r + 14, la=90)


def right_mark(f, p, d1, d2, s=9):
    """Small right-angle mark at world point p between unit directions d1 and d2 (px size s)."""
    q = p + (s / f.ppu) * d1
    w = p + (s / f.ppu) * (d1 + d2)
    e = p + (s / f.ppu) * d2
    f.path_world([T(q), T(w), T(e)], "muted")


# =============================================================== concept: where I_O = I_G + m r^2 comes from
def c_paxis():
    f = Fig(300, "Kinetic diagram of a body pinned at O: I_G alpha plus m r alpha at arm r; m r omega^2 passes through O")
    O, G = V(0, 0), V(0.62, -0.32)
    poly(f, [V(-0.12, 0.08), V(0.9, -0.2), V(0.78, -0.6), V(-0.05, -0.25)])
    f.pin(T(O), 4.6)
    f.text(T(O), "O (fixed)", "muted", dx=-8, dy=-14, anchor="end")
    f.line(T(O), T(G), "cons")
    u = (G - O) / np.linalg.norm(G - O)
    t = V(-u[1], u[0]) * -1                       # tangential direction for a CW alpha
    f.arrow(T(G), T(G + 0.36 * t), "abs", "m(a_{G})_{t} = m r α", at=("E", 8), lpos=1.0)
    f.arrow(T(G), T(G - 0.3 * u), "abs", "m(a_{G})_{n} = m r ω²", at=("N", 12), lpos=0.75)
    curl(f, G, "I_{G}α", cw=True, r=22, start=200)
    f.dot(T(G))
    f.text(T(G), "G", dx=10, dy=12, anchor="start")
    f.text(T((O + G) / 2), "r", "muted", dx=8, dy=-10)
    return f.svg()


# =============================================================== W1  T10 Q2 mast
def w1_geom():
    f = Fig(ppu_for(200 / 100), "Mast geometry to scale 1:200")      # 1 cm on paper = 2 m
    O = V(0, 0); u = U(30)
    A, G, B = 16 * u, 12 * u, 24 * u
    f.link(T(O), T(B), w=6)
    f.pivot(T(O))
    f.line(T(A), T(A + V(-5, 0)), "rope")
    f.text(T(A + V(-5, 0)), "cable (horizontal)", "muted", dy=-10, anchor="start")
    f.line(T(O), T(V(13, 0)), "muted", dash="4 4")
    f.arc(T(O), 40, 0, 30, "muted", "30°", lr=54)
    for p, s in ((A, "A"), (G, "G"), (B, "B")):
        f.dot(T(p))
        f.text(T(p), s, dx=-4, dy=-14)
    f.text(T(O), "O", dx=-10, dy=10, anchor="end")
    f.dim(T(V(G[0], 0)), T(O), "12 cos 30° = 10.39 m", off=22, side="l")
    f.line(T(G), T(V(G[0], 0)), "muted", dash="3 4")
    f.dim(T(O), T(V(0, A[1])), "16 sin 30° = 8 m", off=26, side="l")
    f.line(T(A), T(V(0, A[1])), "muted", dash="3 4")
    f.set_scalebar(2, "1 cm = 2 m (scale 1:200)")
    return true_size(f.svg())


def w1_fbd():
    f = Fig(9, "Mast free-body diagram")
    O = V(0, 0); u = U(30); A, G = 16 * u, 12 * u
    f.link(T(O), T(24 * u), w=5)
    f.arrow(T(A), T(A + V(-6, 0)), "ans", "2T = 4333 N", at=("N", 10), lpos=0.5)
    f.arrow(T(G), T(G + V(0, -6)), "ans", "mg = 2943 N", at=("E", 6), lpos=0.85)
    f.arrow(T(O + V(-5, 0)), T(O), "ans", "O_{x}", at=("S", 12), lpos=0.3)
    f.arrow(T(O + V(0, -5)), T(O), "ans", "O_{y}", at=("E", 6), lpos=0.2)
    f.dot(T(G)); f.text(T(G), "G", dx=10, dy=6, anchor="start")
    f.text(T(A), "A", dx=8, dy=10, anchor="start")
    f.text(T(O), "O", dx=-10, dy=10, anchor="end")
    return f.svg()


def w1_kd():
    f = Fig(9, "Mast kinetic diagram")
    O = V(0, 0); u = U(30); G = 12 * u
    f.link(T(O), T(24 * u), w=5)
    f.arrow(T(G), T(G + 5.5 * U(120)), "abs", "m(a_{G})_{t} = m(12α)", at=("W", 8), lpos=0.9)
    curl(f, G, "I_{G}α", cw=False, r=18, start=-20)
    f.dot(T(G)); f.text(T(G), "G", dx=10, dy=10, anchor="start")
    f.text(T(O), "O", dx=-10, dy=10, anchor="end")
    f.text(T(V(14, -3)), "m(a_{G})_{n} = m(12ω²) = 0", "muted", anchor="middle")
    return f.svg()


def w1_acc():
    f = Fig(ppu_for(0.2), "Mast: acceleration of G to scale")
    o = V(0, 0); a = 0.850 * U(120)
    f.line(T(o), T(0.5 * U(30)), "muted", dash="4 4")
    f.text(T(0.5 * U(30)), "mast direction", "muted", dx=6, anchor="start")
    f.arrow(T(o), T(a), "t", "a_{G} = 12α = 0.850 m/s²", at=("W", 8), lpos=0.6)
    f.line(T(a), T(V(a[0], 0)), "muted", dash="3 3")
    f.line(T(o), T(V(a[0], 0)), "muted", dash="3 3")
    f.text(T(V(a[0] / 2, 0)), "0.425 ←", "muted", dy=12)
    f.text(T(V(a[0], a[1] / 2)), "0.737 ↑", "muted", dx=-6, anchor="end")
    right_mark(f, o, U(30), U(120))
    f.set_scalebar(0.2, "1 cm = 0.2 m/s²")
    return true_size(f.svg())


# =============================================================== W2  T11 Q1 plate pinned at a corner
B2 = 0.2


def _plate(f, cls="body"):
    poly(f, [V(0, 0), V(2 * B2, 0), V(2 * B2, -B2), V(0, -B2)], cls)


def w2_geom():
    f = Fig(ppu_for(0.04), "Plate geometry to scale 1:4")
    O, G = V(0, 0), V(B2, -B2 / 2)
    _plate(f)
    f.pivot(T(O), down=False)
    f.line(T(O), T(G), "cons")
    f.line(T(O), T(V(0.26, 0)), "muted", dash="4 4")
    f.arc(T(O), 46, 333.4, 360, "muted", "θ = 26.6°", lr=66, la=340)
    f.dot(T(G)); f.text(T(G), "G", dx=8, dy=12, anchor="start")
    f.text(T(O), "O", dx=-10, dy=-4, anchor="end")
    f.text(T((O + G) / 2), "r = √5 b/2 = 223.6 mm", "muted", dx=-4, dy=16, anchor="end")
    f.dim(T(V(0, -B2)), T(V(2 * B2, -B2)), "2b = 400 mm", off=16, side="r")
    f.dim(T(V(2 * B2, -B2)), T(V(2 * B2, 0)), "b = 200 mm", off=14, side="r")
    f.set_scalebar(0.04, "1 cm = 40 mm (scale 1:4)")
    return true_size(f.svg())


def w2_fbd():
    f = Fig(420, "Plate free-body diagram")
    O, G = V(0, 0), V(B2, -B2 / 2)
    _plate(f)
    f.arrow(T(O + V(-0.14, 0)), T(O), "ans", "O_{x}", at=("N", 10), lpos=0.3)
    f.arrow(T(O + V(0, -0.14)), T(O), "ans", "O_{y}", at=("W", 6), lpos=0.2)
    f.arrow(T(G), T(G + V(0, -0.17)), "ans", "mg = 29.43 N", at=("E", 6), lpos=0.85)
    f.dot(T(G)); f.text(T(G), "G", dx=8, dy=-10, anchor="start")
    f.text(T(O), "O", dx=8, dy=-10, anchor="start")
    return f.svg()


def w2_kd():
    f = Fig(420, "Plate kinetic diagram")
    O, G = V(0, 0), V(B2, -B2 / 2)
    _plate(f, "outline")
    f.line(T(O), T(G), "cons")
    d = U(243.43)
    f.arrow(T(G), T(G + 0.17 * d), "abs", "m(a_{G})_{t} = m r α", at=("E", 8), lpos=0.95)
    curl(f, G, "I_{G}α", cw=True, r=18)
    right_mark(f, G, -(G - O) / np.linalg.norm(G - O), d)
    f.dot(T(G)); f.text(T(G), "G", dx=10, dy=4, anchor="start")
    f.text(T(V(0.2, -0.27)), "m(a_{G})_{n} = m r ω² = 0 (from rest)", "muted", anchor="middle")
    return f.svg()


def w2_acc():
    f = Fig(ppu_for(2), "Plate: acceleration of G to scale")
    o = V(0, 0); a = 6.58 * U(243.43)
    f.line(T(o), T(4 * U(-26.57)), "muted", dash="4 4")
    f.text(T(4 * U(-26.57)), "line OG", "muted", dx=6, anchor="start")
    f.arrow(T(o), T(a), "t", "a_{G} = rα = 6.58 m/s²", at=("W", 8), lpos=0.55)
    f.line(T(a), T(V(0, a[1])), "muted", dash="3 3")
    f.line(T(o), T(V(0, a[1])), "muted", dash="3 3")
    f.text(T(V(a[0] / 2, a[1])), "2.94 ←", "muted", dy=12)
    f.text(T(V(0, a[1] / 2)), "5.89 ↓", "muted", dx=6, anchor="start")
    right_mark(f, o, U(-26.57), U(243.43))
    f.set_scalebar(2, "1 cm = 2 m/s²")
    return true_size(f.svg())


# =============================================================== W3  T10 Q3 L-shaped body
def w3_geom():
    f = Fig(ppu_for(0.02), "L-shaped body to scale 1:2 with both part centroids and the overall G")
    O = V(0, 0); E = V(0.1875, 0); Tp = V(0.1875, 0.0625)
    G1, G2, G = V(0.09375, 0), V(0.1875, 0.03125), V(0.1171875, 0.0078125)
    f.link(T(O), T(E), w=8)
    f.link(T(E), T(Tp), w=8)
    f.pivot(T(O), down=False)
    f.text(T(O), "O", dx=-10, dy=10, anchor="end")
    f.arrow(T(G1), T(G1 + V(0, -0.03)), "ans", "m₁g = 22.07 N", at=("W", 6), lpos=0.75)
    f.arrow(T(G2), T(G2 + V(0, -0.03)), "ans", "m₂g = 7.36 N", at=("E", 6), lpos=0.75)
    f.dot(T(G1)); f.text(T(G1), "G₁", dx=0, dy=-14)
    f.dot(T(G2)); f.text(T(G2), "G₂", dx=12, dy=-2, anchor="start")
    f.dot(T(G), cls="dotans"); f.text(T(G), "G", "ans", dx=0, dy=-14)
    f.line(T(O), T(G2), "cons")
    f.text(T(G2 * 0.55), "d₂ = 190.1 mm", "muted", dx=0, dy=-12)
    f.dim(T(O), T(V(G[0], 0)), "x̄ = 15L/32 = 117.2 mm", off=76, side="r")
    f.dim(T(O), T(E), "3L/4 = 187.5 mm", off=104, side="r")
    f.dim(T(E), T(Tp), "L/4", off=14, side="r")
    f.set_scalebar(0.02, "1 cm = 20 mm (scale 1:2)")
    return true_size(f.svg())


# =============================================================== W4  T10 Q1 semicircular pipe
R4 = 0.5
YB = 2 * R4 / math.pi


def _pipe(f, cls="outline"):
    pts = [V(-R4 * math.cos(math.radians(t)), R4 * math.sin(math.radians(t))) for t in range(0, 181, 6)]
    f.path_world([T(p) for p in pts], cls)
    f.line((-0.7, 0), (0.7, 0), "muted")


def w4_mech():
    f = Fig(150, "Parallelogram linkage: the platform and pipe translate")
    P1, P2 = V(0, 0), V(1.6, 0)
    u = U(45)
    T1, T2 = P1 + u, P2 + u
    f.link(T(P1), T(T1)); f.link(T(P2), T(T2))
    f.link(T(T1 + V(-0.2, 0)), T(T2 + V(0.2, 0)), w=10)
    f.pivot(T(P1)); f.pivot(T(P2))
    c = (T1 + T2) / 2 + V(0, 0.04)
    pts = [c + V(-R4 * math.cos(math.radians(t)), R4 * math.sin(math.radians(t))) * 0.7 for t in range(0, 181, 10)]
    f.path_world([T(p) for p in pts], "ink")
    f.line(T(P1), T(P1 + V(0, 0.45)), "muted", dash="4 4")
    f.arc(T(P1), 40, 90, 45, "muted", "θ = 45°", ccw=False, lr=58)
    f.arrow(T(T1), T(T1 + 0.55 * U(135)), "t", "a = rα (⊥ link)", at=("W", 8), lpos=0.9)
    f.arrow(T(T2), T(T2 + 0.55 * U(135)), "t", "same a", at=("N", 10), lpos=1.0)
    f.text(T(P1 + 0.5 * u), "r = 1 m", "muted", dx=10, dy=6, anchor="start")
    return f.svg()


def w4_fbd():
    f = Fig(260, "Pipe free-body diagram")
    A, B, G = V(-R4, 0), V(R4, 0), V(0, YB)
    _pipe(f)
    f.arrow(T(A + V(0, -0.32)), T(A), "ans", "N_{A}", at=("W", 6), lpos=0.3)
    f.arrow(T(B + V(0, -0.32)), T(B), "ans", "N_{B}", at=("E", 6), lpos=0.3)
    f.arrow(T(A), T(A + V(-0.3, 0)), "ans", "F_{A}", at=("N", 10), lpos=0.8)
    f.arrow(T(B), T(B + V(-0.3, 0)), "ans", "F_{B}", at=("S", 12), lpos=0.6)
    f.arrow(T(G), T(G + V(0, -0.3)), "ans", "W = 784.8 N", at=("E", 6), lpos=0.7)
    f.dot(T(G)); f.text(T(G), "G", dx=10, dy=-6, anchor="start")
    f.text(T(A), "A", dx=6, dy=14, anchor="start"); f.text(T(B), "B", dx=-6, dy=14, anchor="end")
    f.dim(T(V(0, 0)), T(G), "2r/π = 318 mm", off=12, side="l")
    return f.svg()


def w4_kd():
    f = Fig(260, "Pipe kinetic diagram: only m a at G (no I_G alpha, the pipe translates)")
    A, G = V(-R4, 0), V(0, YB)
    _pipe(f)
    d = U(135)
    f.line(T(G - 0.55 * d), T(G + 0.25 * d), "cons")
    f.arrow(T(G), T(G + 0.35 * d), "abs", "m a = m(rα)", at=("E", 8), lpos=1.0)
    foot = G + np.dot(A - G, d) * d
    f.line(T(A), T(foot), "ans")
    right_mark(f, foot, (A - foot) / np.linalg.norm(A - foot), -d)
    f.text(T((A + foot) / 2), "d = 0.5786 m", "ans", dx=-8, dy=8, anchor="end")
    f.dot(T(G)); f.text(T(G), "G", dx=10, dy=4, anchor="start")
    f.text(T(A), "A", dx=-6, dy=14, anchor="end")
    f.text(T(V(0.2, -0.16)), "I_{G}α = 0 (translation)", "muted")
    return f.svg()


def w4_acc():
    f = Fig(ppu_for(2), "Pipe acceleration to scale")
    o = V(0, 0); a = 5.946 * U(135)
    f.arrow(T(o), T(a), "t", "a = rα = 5.95 m/s²", at=("E", 8), lpos=0.6)
    f.line(T(a), T(V(a[0], 0)), "muted", dash="3 3"); f.line(T(o), T(V(a[0], 0)), "muted", dash="3 3")
    f.text(T(V(a[0] / 2, 0)), "4.20 ←", "muted", dy=12)
    f.text(T(V(a[0], a[1] / 2)), "4.20 ↑", "muted", dx=-6, anchor="end")
    f.arc(T(o), 30, 90, 135, "muted", "45°", lr=44)
    f.line(T(o), T(V(0, 4.6)), "muted", dash="4 4")
    f.set_scalebar(2, "1 cm = 2 m/s²")
    return true_size(f.svg())


# =============================================================== W5  T10 Q4 / T11 Q2 square plate (top view)
H5 = 0.1


def w5_geom():
    f = Fig(ppu_for(5 / 100), "Square plate, top view, to scale 1:5")
    G, A, B = V(0, 0), V(H5, -H5), V(H5, H5)
    poly(f, [V(-H5, -H5), V(H5, -H5), V(H5, H5), V(-H5, H5)])
    f.arrow(T(A + V(0, -0.08)), T(A), "ans", "P = 120 N", at=("E", 6), lpos=0.4)
    f.line(T(A), T(B + V(0, 0.04)), "cons")
    f.dot(T(G)); f.text(T(G), "G", dx=-10, dy=-2, anchor="end")
    f.text(T(A), "A", dx=8, dy=10, anchor="start"); f.text(T(B), "B", dx=8, dy=-8, anchor="start")
    f.line(T(G), T(B), "muted", dash="4 4")
    f.text(T(B * 0.55), "141.4 mm", "muted", dx=-6, dy=-10, anchor="end")
    f.dim(T(G), T(V(H5, 0)), "b/2 = 100 mm (arm of P)", off=12, side="r")
    f.arrow(T(V(-H5 - 0.04, -H5 - 0.04)), T(V(-H5 + 0.03, -H5 - 0.04)), "muted", "x", at=("E", 4), lpos=1.0)
    f.arrow(T(V(-H5 - 0.04, -H5 - 0.04)), T(V(-H5 - 0.04, -H5 + 0.03)), "muted", "y", at=("N", 6), lpos=1.0)
    f.set_scalebar(0.05, "1 cm = 50 mm (scale 1:5)")
    return true_size(f.svg())


def w5_fbd():
    f = Fig(500, "Square plate FBD (in the plane of the table)")
    G, A = V(0, 0), V(H5, -H5)
    poly(f, [V(-H5, -H5), V(H5, -H5), V(H5, H5), V(-H5, H5)])
    f.arrow(T(A + V(0, -0.1)), T(A), "ans", "P = 120 N", at=("E", 6), lpos=0.4)
    f.dot(T(G)); f.text(T(G), "G", dx=-8, dy=-8, anchor="end")
    f.text(T(V(0, -0.16)), "W and N act ⊥ to the table: they cancel", "muted")
    return f.svg()


def w5_kd():
    f = Fig(500, "Square plate kinetic diagram")
    G = V(0, 0)
    poly(f, [V(-H5, -H5), V(H5, -H5), V(H5, H5), V(-H5, H5)], "outline")
    f.arrow(T(G), T(G + V(0, 0.09)), "abs", "m a_{G}", at=("E", 6), lpos=0.8)
    curl(f, G, "I_{G}α", cw=False, r=22, start=-30)
    f.dot(T(G))
    return f.svg()


def w5_acc():
    f = Fig(ppu_for(10), "Acceleration diagram for B, to scale 1 cm = 10 m/s^2")
    o = V(0, 0); gp = V(0, 20); b = V(-30, 50)
    f.arrow(T(o), T(gp), "t", "a_{G} = 20", at=("E", 6), lpos=0.5)
    f.arrow(T(gp), T(b), "n", "a_{B/G} = rα = 42.4", at=("E", 8), lpos=0.6)
    f.arrow(T(o), T(b), "ans", "a_{B} = 58.3 m/s²", at=("W", 8), lpos=0.5, dashed=True)
    f.arc(T(gp), 20, 90, 135, "muted", "45°", lr=30, la=112)
    f.arc(T(gp), 14, 135, 270, "muted", "135°", lr=34, la=200)
    f.line(T(gp), T(gp + V(0, 14)), "muted", dash="3 3")
    f.text(T(o), "o", dx=6, dy=10, anchor="start"); f.text(T(gp), "g", dx=8, anchor="start")
    f.text(T(b), "b", dx=-6, dy=-8, anchor="end")
    f.set_scalebar(10, "1 cm = 10 m/s²")
    return true_size(f.svg())


# =============================================================== W6  T10 Q5 bowling ball
R6 = 0.12


def w6_fbd():
    f = Fig(420, "Bowling ball FBD while slipping")
    G, C = V(0, 0), V(0, -R6)
    f.circle(T(G), R6, "outline")
    f.line(T(V(-0.25, -R6)), T(V(0.25, -R6)), "muted")
    f.arrow(T(G), T(G + V(0, -0.1)), "ans", "mg", at=("E", 6), lpos=0.7)
    f.arrow(T(C + V(0, -0.1)), T(C), "ans", "N = mg", at=("E", 6), lpos=0.3)
    f.arrow(T(C), T(C + V(-0.12, 0)), "ans", "F = μN", at=("N", 10), lpos=0.7)
    f.dot(T(G)); f.text(T(G), "G", dx=-8, dy=-8, anchor="end")
    return f.svg()


def w6_kd():
    f = Fig(420, "Bowling ball kinetic diagram")
    G = V(0, 0)
    f.circle(T(G), R6, "outline")
    f.arrow(T(G), T(G + V(-0.11, 0)), "abs", "m a_{G}", at=("N", 10), lpos=0.7)
    curl(f, G, "I_{G}α", cw=True, r=26)
    f.dot(T(G))
    return f.svg()


def w6_graph():
    f = Fig(40, "Speed of G and r omega against time: slipping ends where the lines meet")
    sx = 4.0
    f.line((0, 0), (1.3 * sx, 0), "ink"); f.line((0, 0), (0, 6.6), "ink")
    f.text((1.3 * sx, 0), "t (s)", "muted", dx=6, anchor="start")
    f.text((0, 6.6), "m/s", "muted", dy=-10)
    for tt in (0.5, 1.0):
        f.line((tt * sx, 0), (tt * sx, -0.12), "ink"); f.text((tt * sx, 0), f"{tt}", "muted", dy=14)
    for vv in (2, 4, 6):
        f.line((0, vv), (-0.1, vv), "ink"); f.text((0, vv), f"{vv}", "muted", dx=-6, anchor="end")
    f.line((0, 6), (1.25 * sx, 6 - 1.962 * 1.25), "n")
    f.line((0, 0), (1.25 * sx, 4.101 * 1.25), "t")
    f.text((1.25 * sx, 6 - 1.962 * 1.25), "v_{G} = 6 − 1.962t", "n", dx=4, dy=8, anchor="start")
    f.text((1.25 * sx, 4.101 * 1.25), "rω = 4.10t", "t", dx=4, anchor="start")
    p = (0.9896 * sx, 4.058)
    f.dot(p, cls="dotans")
    f.line(p, (p[0], 0), "muted", dash="3 3")
    f.text(p, "rolls: t = 0.99 s", "ans", dx=-8, dy=-14, anchor="end")
    return f.svg()


# =============================================================== W7  T11 Q3 rod on massless hoop
L7 = 0.25


def w7_geom():
    f = Fig(ppu_for(0.05), "Rod on hoop to scale 1:5")
    O, G, C = V(0, 0), V(L7 / 2, 0), V(0, -L7)
    f.circle(T(O), L7, "outline")
    f.line(T(V(-0.32, -L7)), T(V(0.34, -L7)), "ink")
    f.link(T(O), T(V(L7, 0)), w=7)
    f.dot(T(O)); f.text(T(O), "O", dx=-8, dy=-8, anchor="end")
    f.dot(T(G)); f.text(T(G), "G", dx=0, dy=-14)
    f.dot(T(C)); f.text(T(C), "C (contact)", dx=8, dy=14, anchor="start")
    f.line(T(G), T(V(G[0], -L7)), "muted", dash="3 4")
    f.dim(T(V(0, -L7)), T(V(G[0], -L7)), "l/2", off=14, side="r")
    f.dim(T(C), T(O), "l = 250 mm", off=18, side="l")
    f.set_scalebar(0.05, "1 cm = 50 mm (scale 1:5)")
    return true_size(f.svg())


def w7_fbd():
    f = Fig(420, "Rod and hoop FBD")
    O, G, C = V(0, 0), V(L7 / 2, 0), V(0, -L7)
    f.circle(T(O), L7, "outline thin", dash="5 4")
    f.link(T(O), T(V(L7, 0)), w=6)
    f.line(T(V(-0.3, -L7)), T(V(0.3, -L7)), "muted")
    f.arrow(T(G), T(G + V(0, -0.13)), "ans", "mg", at=("E", 6), lpos=0.8)
    f.arrow(T(C + V(0, -0.11)), T(C), "ans", "N", at=("W", 6), lpos=0.3)
    f.arrow(T(C), T(C + V(0.13, 0)), "ans", "F", at=("S", 12), lpos=0.7)
    f.dot(T(G)); f.text(T(G), "G", dx=0, dy=-14)
    f.text(T(C), "C", dx=-8, dy=12, anchor="end")
    return f.svg()


def w7_kd():
    f = Fig(420, "Rod and hoop kinetic diagram with the moment arms about C")
    O, G, C = V(0, 0), V(L7 / 2, 0), V(0, -L7)
    f.circle(T(O), L7, "outline thin", dash="5 4")
    f.link(T(O), T(V(L7, 0)), w=6)
    f.arrow(T(G), T(G + V(0.12, 0)), "abs", "m(a_{G})_{x} = m lα", at=("N", 10), lpos=1.0)
    f.arrow(T(G), T(G + V(0, -0.1)), "abs", "m(a_{G})_{y} = m(l/2)α", at=("E", 6), lpos=1.0)
    curl(f, G, "I_{G}α", cw=True, r=18, start=200)
    f.dot(T(C)); f.text(T(C), "C", dx=-8, dy=12, anchor="end")
    f.dim(T(C), T(V(0, 0)), "arm l", off=16, side="l")
    return f.svg()


def w7_acc():
    f = Fig(ppu_for(1), "Rod and hoop: a_G = a_O + a_G/O to scale")
    o = V(0, 0); p = V(3.679, 0); g = V(3.679, -1.839)
    f.arrow(T(o), T(p), "t", "a_{O} = lα = 3.68", at=("N", 10), lpos=0.5)
    f.arrow(T(p), T(g), "n", "a_{G/O} = (l/2)α = 1.84", at=("E", 6), lpos=0.5)
    f.arrow(T(o), T(g), "ans", "a_{G} = 4.11 m/s²", at=("SW", 6), lpos=0.5, dashed=True)
    f.set_scalebar(1, "1 cm = 1 m/s²")
    return true_size(f.svg())


# =============================================================== W8  T11 Q4 bar AB, crank OA, link CB
def w8_geom():
    f = Fig(ppu_for(0.04), "Bar AB with crank OA and link CB, to scale 1:4")
    O, A, B, C = V(0, 0), V(0, -0.1), V(0.3, -0.1), V(0.3, 0.1)
    f.link(T(O), T(A), w=8); f.link(T(C), T(B), w=6)
    f.link(T(A), T(B), w=9)
    f.pivot(T(O), down=False); f.pivot(T(C), down=False)
    f.pin(T(A)); f.pin(T(B))
    f.text(T(O), "O", dx=-12, dy=0, anchor="end"); f.text(T(C), "C", dx=12, dy=0, anchor="start")
    f.text(T(A), "A", dx=-8, dy=14, anchor="end"); f.text(T(B), "B", dx=8, dy=14, anchor="start")
    f.dot(T(V(0.15, -0.1))); f.text(T(V(0.15, -0.1)), "G", dx=0, dy=14)
    f.arc(T(O), 18, 200, 330, "abs", "ω₀ = 2, α₀ = 4 (CCW)", arrow=True, ccw=True, lr=34, la=265)
    f.dim(T(O), T(A), "100", off=22, side="l")
    f.dim(T(A), T(B), "300 mm", off=30, side="r")
    f.dim(T(B), T(C), "200", off=24, side="r")
    f.set_scalebar(0.04, "1 cm = 40 mm (scale 1:4)")
    return true_size(f.svg())


def w8_acc():
    f = Fig(ppu_for(0.1), "Acceleration polygon for AB to scale 1 cm = 0.1 m/s^2")
    o = V(0, 0); an = V(0, 0.4); a = V(0.4, 0.4); bn = V(0, 0.2); b = V(0.4, 0.2); gq = V(0.4, 0.3)
    f.line(T(a + V(0, 0.08)), T(V(0.4, 0.08)), "cons")
    f.line(T(bn + V(-0.05, 0)), T(b + V(0.1, 0)), "cons")
    f.arrow(T(o), T(an), "n", "(a_{A})_{n} = 0.4", at=("W", 6), lpos=0.78)
    f.arrow(T(an), T(a), "t", "(a_{A})_{t} = 0.4", at=("N", 10), lpos=0.5)
    f.arrow(T(o + V(0.008, 0)), T(bn + V(0.008, 0)), "n", "(a_{B})_{n} = 0.2", at=("W", 14), lpos=0.4)
    f.arrow(T(bn), T(b), "t", "(a_{B})_{t} = 0.4", at=("N", 10), lpos=0.4)
    f.arrow(T(a), T(b), "n", "(a_{B/A})_{t} = 0.2", at=("E", 6), lpos=0.5)
    f.arrow(T(o), T(gq), "ans", "a_{G} = 0.5", at=("SE", 4), lpos=0.45, dashed=True)
    f.dot(T(gq), cls="dotans")
    f.text(T(o), "o", dx=-6, dy=10, anchor="end"); f.text(T(a), "a", dx=-6, dy=-8, anchor="end")
    f.text(T(b), "b", dx=8, dy=8, anchor="start"); f.text(T(gq), "g", "ans", dx=-10, dy=-6, anchor="end")
    f.set_scalebar(0.1, "1 cm = 0.1 m/s²")
    return true_size(f.svg())


def w8_fbd():
    f = Fig(560, "Bar AB free-body diagram")
    A, B, G = V(0, 0), V(0.3, 0), V(0.15, 0)
    f.link(T(A), T(B), w=9)
    f.arrow(T(A + V(-0.09, 0)), T(A), "ans", "A_{x}", at=("N", 10), lpos=0.3)
    f.arrow(T(A + V(0, -0.09)), T(A), "ans", "A_{y}", at=("W", 6), lpos=0.2)
    f.arrow(T(B + V(0, -0.09)), T(B), "ans", "B (force in CB)", at=("E", 6), lpos=0.2)
    f.arrow(T(G), T(G + V(0, -0.09)), "ans", "mg = 7.85 N", at=("E", 6), lpos=0.8)
    f.text(T(A), "A", dx=-4, dy=-14, anchor="end"); f.text(T(B), "B", dx=4, dy=-14, anchor="start")
    f.text(T(G), "G", dx=0, dy=-14)
    return f.svg()


def w8_kd():
    f = Fig(560, "Bar AB kinetic diagram")
    A, B, G = V(0, 0), V(0.3, 0), V(0.15, 0)
    f.link(T(A), T(B), w=9)
    f.arrow(T(G), T(G + V(0.08, 0)), "abs", "m(a_{G})_{x} = 0.32 N", at=("S", 12), lpos=1.0)
    f.arrow(T(G), T(G + V(0, 0.07)), "abs", "m(a_{G})_{y} = 0.24 N", at=("N", 8), lpos=1.0)
    curl(f, G, "I_{G}α", cw=True, r=16, start=210)
    f.text(T(A), "A", dx=-4, dy=-14, anchor="end"); f.text(T(B), "B", dx=4, dy=-14, anchor="start")
    return f.svg()


def build_all():
    names = [n for n in globals() if n[:2] in ("c_", "w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8") and callable(globals()[n])]
    return {n: globals()[n]() for n in names}


if __name__ == "__main__":
    for k_, v_ in build_all().items():
        print(k_, len(v_))
