"""Solution diagrams for the L11-L13 homework memo (rotation, absolute motion, instantaneous centre).

Colours: geometry/dimensions grey "muted"; construction lines (perpendiculars, IC lines) dashed "cons";
given velocities blue "abs"; results red "ans"; acceleration components green "t" / orange "n".
"""
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "textbook"))
sys.path.insert(0, str(ROOT / "guides" / "planekinetics"))
from svgkit import Fig  # noqa: E402
from pk_figs import true_size, ppu_for, right_mark  # noqa: E402

V = lambda x, y: np.array([float(x), float(y)])
T = lambda v: (float(v[0]), float(v[1]))


def U(deg):
    return V(math.cos(math.radians(deg)), math.sin(math.radians(deg)))


def unit(v):
    return v / np.linalg.norm(v)


# ================================================================ ROTATION
def r2():
    f = Fig(110, "5/2 triangular plate: r_A, v_A perpendicular to OA, a_t and a_n at A")
    b, h = 2.0, 1.0
    O, Cn, A = V(0, 0), V(0, -h), V(b, -h)
    f.path_world([T(O), T(Cn), T(A), T(O)], "body")
    f.pivot(T(O), down=False)
    f.text(T(O), "O", dx=-12, anchor="end")
    f.text(T(A), "A", dx=8, dy=10, anchor="start")
    f.line(T(O), T(A), "cons")
    f.text(T((O + A) / 2), "r_{A} = b i − h j", "muted", dx=10, dy=-12, anchor="start")
    e = unit(A - O); t = V(-e[1], e[0])                         # CCW tangential direction
    f.arrow(T(A), T(A + 0.8 * t), "abs", "v_{A} = ω r (⊥ OA)", at=("E", 8), lpos=1.0)
    f.arrow(T(A), T(A - 0.55 * t), "t", "a_{t} = α r (α CW)", at=("E", 8), lpos=1.0)
    f.arrow(T(A), T(A - 0.7 * e), "n", "a_{n} = ω² r → O", at=("S", 12), lpos=0.6)
    right_mark(f, A, -e, t)
    f.arc(T(O), 26, 160, 250, "abs", "ω", arrow=True, ccw=True, lr=38, la=200)
    f.dim(T(Cn), T(A), "b", off=14, side="r")
    f.dim(T(O), T(Cn), "h", off=14, side="r")
    return f.svg()


def r17_geom():
    f = Fig(ppu_for(0.1), "5/17 bent bar to scale 1:10, with OA = 0.7 m from the cosine rule")
    O = V(0, 0); B = 0.5 * V(math.sin(math.radians(15)), -math.cos(math.radians(15)))
    A = B + 0.3 * U(-15)
    f.link(T(O), T(B), w=7); f.link(T(B), T(A), w=7)
    f.pivot(T(O), down=False)
    f.line(T(O), T(A), "cons")
    f.line(T(O), T(V(0, -0.3)), "muted", dash="4 4")
    f.arc(T(O), 34, 270, 285, "muted", "15°", lr=48, la=262)
    f.arc(T(B), 22, -15, 105, "muted", "120°", lr=36, la=45)
    f.arc(T(O), 52, 306.8, 360, "ans", "53.2°", lr=66, la=330)
    f.line(T(O), T(V(0.3, 0)), "muted", dash="4 4")
    f.text(T(O), "O", dx=-10, dy=-4, anchor="end"); f.text(T(B), "B", dx=-10, anchor="end")
    f.text(T(A), "A", dx=8, dy=10, anchor="start")
    f.text(T((O + A) / 2), "OA = 0.7 m", "ans", dx=12, dy=-4, anchor="start")
    f.text(T((O + B) / 2), "0.5 m", "muted", dx=-10, anchor="end")
    f.text(T((B + A) / 2), "0.3 m", "muted", dy=14)
    f.set_scalebar(0.1, "1 cm = 0.1 m")
    return true_size(f.svg())


def r17_vec():
    f = Fig(ppu_for(1.0), "5/17 velocity and acceleration of A, to scale 1 cm = 1 m/s or 1 m/s^2")
    A = V(0, 0)
    e = unit(V(0.4192, -0.5606)); t = V(-e[1], e[0])           # t = CCW direction at A
    f.line(T(A - 2.2 * e), T(A + 0.6 * e), "cons")
    f.text(T(A - 2.2 * e), "to O", "muted", dx=-4, dy=-8, anchor="end")
    f.arrow(T(A), T(A + 1.4 * t), "abs", "v_{A} = ωr = 1.40 m/s", at=("E", 8), lpos=1.0)
    f.arrow(T(A), T(A - 3.5 * t), "t", "a_{t} = αr = 3.5 (α CW)", at=("W", 8), lpos=0.75)
    f.arrow(T(A - 3.5 * t), T(A - 3.5 * t - 2.8 * e), "n", "a_{n} = ω²r = 2.8 → O", at=("W", 8), lpos=0.6)
    a = -3.5 * t - 2.8 * e
    f.arrow(T(A), T(A + a), "ans", "a_{A} = 4.48 m/s²", at=("S", 12), lpos=0.5, dashed=True)
    f.dot(T(A)); f.text(T(A), "A", dx=8, dy=10, anchor="start")
    f.set_scalebar(1, "1 cm = 1 m/s (or m/s²)")
    return true_size(f.svg())


def r26():
    f = Fig(430, "5/26 point C: a_n towards O and a_t perpendicular to OC")
    O = V(0, 0); C = 0.36 * U(210)
    f.circle(T(O), 0.4, "outline thin")
    f.circle(T(O), 0.075, "outline")
    f.line(T(V(-0.5, 0.4)), T(V(0.05, 0.4)), "rope"); f.line(T(V(-0.5, -0.4)), T(V(0.05, -0.4)), "rope")
    f.pin(T(O)); f.text(T(O), "O", dx=8, dy=-10, anchor="start")
    f.line(T(O), T(C), "cons"); f.dot(T(C)); f.text(T(C), "C", dx=-8, dy=12, anchor="end")
    f.text(T(C * 0.75), "r = 360 mm", "muted", dx=6, dy=16, anchor="start")
    s = 0.0017                                                   # 144 m/s^2 drawn about 2/3 of the radius
    an = 144 * s * U(30); at = 40.5 * s * U(300)
    f.arrow(T(C), T(C + an), "n", "a_{n} = rω² = 144 (→ O)", at=("NW", 8), lpos=0.55)
    f.arrow(T(C), T(C + at), "t", "a_{t} = rα = 40.5", at=("SW", 6), lpos=1.0)
    f.line(T(C + an), T(C + an + at), "muted", dash="3 3"); f.line(T(C + at), T(C + an + at), "muted", dash="3 3")
    f.arrow(T(C), T(C + an + at), "ans", "a_{C} = 149.6 m/s²", at=("E", 6), lpos=1.0)
    f.arc(T(O), 40, 20, 110, "abs", "ω, α (CCW)", arrow=True, ccw=True, lr=56, la=65)
    f.text(T(V(-0.2, 0.4)), "a_{B} = rα ←", "abs", dy=-10)
    return f.svg()


# ================================================================ ABSOLUTE MOTION
def m42():
    f = Fig(150, "5/42 bar resting on the corner P: tan theta = h/x")
    P, A = V(0, 1.0), V(1.8, 0)
    d = unit(P - A)
    f.line(T(V(-1.2, 0)), T(V(2.4, 0)), "ink")
    f.path_world([T(V(-1.2, 1.0)), T(P), T(V(0, 0))], "ink")
    f.link(T(A), T(A + 2.7 * d), w=7)
    f.dot(T(P), cls="dotans"); f.text(T(P), "P (corner)", "ans", dx=-8, dy=-12, anchor="end")
    f.pin(T(A)); f.text(T(A), "A", dx=8, dy=-12, anchor="start")
    f.text(T(A + 2.7 * d), "B", dx=-8, anchor="end")
    f.arc(T(A), 40, 180 - math.degrees(math.atan(1 / 1.8)), 180, "muted", "θ", lr=54)
    f.line(T(A), T(V(0.8, 0)), "muted", dash="3 3")
    f.dim(T(V(0, 0)), T(A), "x", off=18, side="r")
    f.dim(T(V(2.1, 0)), T(V(2.1, 1.0)), "h", off=0, side="l")
    f.line(T(P), T(V(2.2, 1.0)), "muted", dash="3 3")
    f.arrow(T(A + V(0.05, -0.18)), T(A + V(-0.55, -0.18)), "abs", "v_{A} = rω₀", at=("S", 12), lpos=0.5)
    f.arc(T(P), 24, 330, 230, "ans", "ω (CW)", arrow=True, ccw=False, lr=36, la=290)
    return f.svg()


def m44():
    f = Fig(150, "5/44 lever OA tangent to the disk: sin theta = r/x")
    O = V(0, 0); Cc = V(-1.6, 0); r = 0.65
    th = math.asin(r / 1.6)
    d = U(180 - math.degrees(th))
    f.circle(T(Cc), r, "outline")
    f.dot(T(Cc)); f.text(T(Cc), "centre", "muted", dx=-6, dy=14, anchor="end")
    f.link(T(O), T(O + 2.3 * d), w=7)
    f.pivot(T(O)); f.text(T(O), "O", dx=10, dy=-8, anchor="start")
    f.text(T(O + 2.3 * d), "A", dx=-8, anchor="end")
    foot = O + np.dot(Cc - O, d) * d
    f.line(T(Cc), T(foot), "cons"); right_mark(f, foot, unit(Cc - foot), d)
    f.text(T((Cc + foot) / 2), "r", "ans", dx=-8, anchor="end")
    f.line(T(Cc), T(O), "muted", dash="4 4")
    f.dim(T(Cc), T(O), "x", off=20, side="r")
    f.arc(T(O), 44, 180 - math.degrees(th), 180, "muted", "θ", lr=58)
    f.arrow(T(Cc + V(0.0, -0.95)), T(Cc + V(0.6, -0.95)), "abs", "v (x shrinks)", at=("S", 12), lpos=0.5)
    f.arc(T(O), 26, 140, 60, "ans", "ω (CW)", arrow=True, ccw=False, lr=40, la=100)
    return f.svg()


def m56():
    f = Fig(ppu_for(0.02), "5/56 Geneva triangle O1 O2 P at theta = 20 degrees, to scale 1:2")
    d, rP = 0.2, 0.2 / math.sqrt(2)
    O1, O2 = V(0, 0), V(d, 0)
    P = rP * U(20)
    f.path_world([T(O1), T(O2), T(P), T(O1)], "ink")
    pts = [rP * U(t) for t in range(-10, 70, 2)]
    f.path_world([T(p) for p in pts], "muted", dash="4 4")
    for p, s, dx in ((O1, "O₁", -10), (O2, "O₂", 10), (P, "P", 0)):
        f.dot(T(p)); f.text(T(p), s, dx=dx, dy=-12 if s == "P" else 12, anchor="end" if dx < 0 else ("start" if dx > 0 else "middle"))
    f.arc(T(O1), 46, 0, 20, "ans", "θ = 20°", lr=70, la=8)
    beta = math.degrees(math.atan2(P[1], d - P[0]))
    f.arc(T(O2), 40, 180 - beta, 180, "ans", f"β = {beta:.1f}°", lr=64, la=172)
    f.text(T(P / 2), "r = 141.4 mm", "muted", dx=-8, dy=-6, anchor="end")
    f.text(T((P + O2) / 2), "O₂P = 82.7 mm", "muted", dx=8, dy=-6, anchor="start")
    f.text(T((O1 + O2) / 2), "d = 200 mm", "muted", dy=14)
    f.arc(T(O1), 24, 150, 40, "abs", "ω₁ = 2 CW", arrow=True, ccw=False, lr=36, la=100)
    f.arc(T(O2), 22, 20, 140, "ans", "ω₂ CCW", arrow=True, ccw=True, lr=36, la=80)
    f.set_scalebar(0.02, "1 cm = 20 mm")
    return true_size(f.svg())


# ================================================================ INSTANTANEOUS CENTRE
def i119():
    f = Fig(ppu_for(0.1), "5/119 IC of AB at theta = 30 degrees, to scale 1:10")
    O = V(0, 0); u = U(-30)
    B, D = 0.8 * u, 1.2 * u
    A = V(B[0] + math.sqrt(0.49 - B[1] ** 2), 0)
    C = V(A[0], -A[0] * math.tan(math.radians(30)))
    f.line(T(V(-0.05, 0)), T(V(1.45, 0)), "guide")
    f.link(T(O), T(D), w=6); f.link(T(B), T(A), w=6)
    f.pivot(T(O), down=False)
    f.line(T(D), T(C), "cons"); f.line(T(A), T(C + V(0, -0.06)), "cons")
    f.dot(T(C), r=5, cls="dotans"); f.text(T(C), "C (IC of AB)", "ans", dx=10, dy=6, anchor="start")
    for p, s, dx, dy in ((O, "O", -10, -6), (B, "B", -10, 10), (D, "D", -10, 12), (A, "A", 8, -12)):
        f.dot(T(p)); f.text(T(p), s, dx=dx, dy=dy, anchor="end" if dx < 0 else "start")
    f.arc(T(O), 40, -30, 0, "muted", "θ = 30°", lr=60, la=-15)
    f.arrow(T(B), T(B + 0.2 * U(240)), "abs", "v_{B} ⊥ OB", at=("W", 6), lpos=1.0)
    f.arrow(T(D), T(D + 0.28 * U(240)), "abs", "v_{D}", at=("W", 6), lpos=1.0)
    f.arrow(T(A), T(A + V(-0.22, 0)), "ans", "v_{A}", at=("N", 10), lpos=0.6)
    f.text(T((B + C) / 2), "0.663 m", "ans", dx=6, dy=-10, anchor="start")
    f.text(T((A + C) / 2), "0.732 m", "ans", dx=8, anchor="start")
    f.set_scalebar(0.1, "1 cm = 0.1 m")
    return true_size(f.svg())


def i108():
    f = Fig(ppu_for(0.02), "5/108 IC of ABD at theta = 30 degrees, to scale 1:2")
    A = V(0, 0); u = U(-30); B, D = 0.1 * u, 0.3 * u
    C = V(B[0], D[1])
    f.line(T(V(-0.02, 0.05)), T(V(-0.02, -0.06)), "ink")
    f.text(T(V(-0.02, 0.05)), "plunger plate", "muted", dx=-4, dy=-8, anchor="end")
    f.link(T(A), T(D), w=8)
    f.line(T(D + V(0.012, 0.06)), T(D + V(0.012, -0.04)), "guide"); f.line(T(D + V(-0.012, 0.06)), T(D + V(-0.012, -0.04)), "guide")
    f.line(T(B), T(B + V(0.17, 0)), "guide")
    f.text(T(B + V(0.17, 0)), "rod of F", "muted", dx=6, anchor="start")
    f.line(T(B), T(C + V(0, -0.02)), "cons"); f.line(T(D), T(C + V(-0.03, 0)), "cons")
    f.dot(T(C), r=5, cls="dotans"); f.text(T(C), "C", "ans", dx=-10, dy=10, anchor="end")
    for p, s, dx, dy in ((A, "A", 10, -10), (B, "B", -8, -12), (D, "D", 14, 6)):
        f.dot(T(p)); f.text(T(p), s, dx=dx, dy=dy, anchor="end" if dx < 0 else "start")
    f.arc(T(B), 34, 150, 180, "muted", "θ = 30°", lr=52, la=170)
    f.line(T(B), T(B + V(-0.07, 0)), "muted", dash="3 3")
    f.dim(T(V(C[0] - 0.12, A[1])), T(V(C[0] - 0.12, C[1])), "0.15 m", off=0, side="l")
    f.line(T(A), T(V(C[0] - 0.12, 0)), "muted", dash="3 3")
    f.line(T(C), T(V(C[0] - 0.12, C[1])), "muted", dash="3 3")
    f.text(T((C + D) / 2), "0.1732 m", "ans", dy=14)
    f.arrow(T(A), T(A + V(0.06, 0)), "abs", "2 m/s (only v_{Ax})", at=("N", 10), lpos=0.9)
    f.arrow(T(D), T(D + V(0, -0.07)), "ans", "v_{D}", at=("E", 6), lpos=0.8)
    f.arrow(T(B), T(B + V(0.04, 0)), "muted", None)
    f.set_scalebar(0.02, "1 cm = 20 mm")
    return true_size(f.svg())


def i117():
    f = Fig(ppu_for(0.04), "5/117 IC of HBA at theta = 45 degrees, to scale 1:4")
    D = V(0, 0); u = U(225)
    F, H = 0.32 * u, 0.24 * u
    yB = H[1] - math.sqrt(0.04 - H[0] ** 2); B = V(0, yB)
    A = B + 0.16 * (B - H) / 0.2
    C = V(yB, yB)
    f.line(T(V(0, 0.03)), T(V(0, -0.42)), "guide")
    f.link(T(D), T(F), w=6); f.link(T(H), T(A), w=6)
    f.line(T(H), T(C + 0.03 * u), "cons"); f.line(T(B), T(C + V(-0.03, 0)), "cons")
    f.dot(T(C), r=5, cls="dotans"); f.text(T(C), "C (IC of HBA)", "ans", dx=-6, dy=16, anchor="end")
    for p, s, dx, dy in ((D, "D", 10, -6), (H, "H", -10, -8), (F, "F", -10, -8), (B, "B", 10, 2), (A, "A", 10, 8)):
        f.dot(T(p)); f.text(T(p), s, dx=dx, dy=dy, anchor="end" if dx < 0 else "start")
    f.line(T(F + V(-0.05, -0.02)), T(F + V(0.05, -0.02)), "ink")
    f.text(T(F + V(0, -0.02)), "plunger cup", "muted", dy=14)
    f.arc(T(D), 36, 225, 270, "muted", "θ = 45°", lr=54, la=250)
    f.arrow(T(F), T(F + V(0, 0.06)), "abs", "2 m/s (only v_{Fy})", at=("W", 6), lpos=1.0)
    f.arrow(T(H), T(H + 0.07 * U(135)), "abs", "v_{H} ⊥ DH", at=("W", 6), lpos=1.0)
    f.arrow(T(A), T(A + 0.12 * unit(V(0.0847, 0.4113))), "ans", "v_{A} ⊥ CA", at=("E", 6), lpos=1.0)
    f.line(T(C), T(A), "cons")
    f.text(T((H + C) / 2), "0.150", "ans", dx=-8, dy=-4, anchor="end")
    f.text(T((C + A) / 2), "0.420 m", "ans", dy=14)
    f.set_scalebar(0.04, "1 cm = 40 mm")
    return true_size(f.svg())


def i120():
    f = Fig(70, "5/120 velocity line across the planet gear: (a) ring fixed, (b) ring turning CCW at 80 rev/min")
    out = []
    for k_, (vring, title) in enumerate(((0.0, "(a) ring D fixed"), (120.0, "(b) ring D at 80 rev/min CCW"))):
        x0 = 6.5 * k_
        s = 1 / 100                                      # 1 unit per 100 a·rpm
        xs = {"sun contact": 0.5, "A (arm)": 1.0, "ring contact": 1.5}
        f.line((x0 + 0.0, 0), (x0 + 1.9 * 2, 0), "muted", dash="3 4")
        X = lambda xa: x0 + xa * 2.0
        f.circle((X(1.0), 0), 1.0, "outline")
        f.dot((x0, 0)); f.text((x0, 0), "O", dx=-8, anchor="end")
        vA = -90.0
        slope = (vring - vA) / 0.5
        vsun = vA - slope * 0.5
        f.arrow((X(1.0), 0), (X(1.0), vA * s), "abs", "90a ↓ (arm)", at=("E", 6), lpos=1.0)
        if abs(vring) > 1e-9:
            f.arrow((X(1.5), 0), (X(1.5), vring * s), "abs", "120a ↑ (ring)", at=("E", 6), lpos=1.0)
        else:
            f.dot((X(1.5), 0), r=4); f.text((X(1.5), 0), "ring: 0", "muted", dx=6, dy=-10, anchor="start")
        f.arrow((X(0.5), 0), (X(0.5), vsun * s), "ans", f"{-vsun:.0f}a ↓", at=("W", 6), lpos=1.0)
        f.line((X(0.5), vsun * s), (X(1.5), vring * s), "cons")
        f.text((X(1.0), 1.9), title, "muted")
        f.text((X(1.0), -3.6), f"ω_B = {-vsun:.0f}a ÷ (a/2) = {-vsun / 0.5:.0f} rev/min CW", "ans")
    return f.svg()


def build_all():
    names = ("r2", "r17_geom", "r17_vec", "r26", "m42", "m44", "m56", "i119", "i108", "i117", "i120")
    return {n: globals()[n]() for n in names}


if __name__ == "__main__":
    for k_, v_ in build_all().items():
        print(k_, len(v_))
