"""Solution diagrams for the MEC2047F June 2025 memo (all numbers checked in check_f_answers.py)."""
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "textbook"))
from svgkit import Fig  # noqa: E402

V = lambda x, y: np.array([float(x), float(y)])
T = lambda v: (float(v[0]), float(v[1]))


def U(deg):
    return V(math.cos(math.radians(deg)), math.sin(math.radians(deg)))


# ---------------------------------------------------------------- Q2 (annotated exam figure)
def q2_vars(img_b64, w, h):
    """Overlay the cable routing, datum and position coordinates on the exam's own pulley figure."""
    blue, green, red = "#1c5cc2", "#12804a", "#d0021b"
    L = lambda x1, y1, x2, y2, c, extra="": (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="6" '
        f'stroke-linecap="round" opacity="0.75"{extra}/>')
    parts = [f'<image href="data:image/png;base64,{img_b64}" x="0" y="0" width="{w}" height="{h}"/>']
    for seg in [(45, 790, 45, 165), (192, 165, 192, 535), (65, 340, 105, 520), (178, 340, 150, 530)]:
        parts.append(L(*seg, blue))
    for seg in [(148, 548, 148, 705), (290, 705, 290, 54)]:
        parts.append(L(*seg, green))
    t = lambda x, y, s, c="#000", a="start", sz=26, it=False: (
        f'<text x="{x}" y="{y}" fill="{c}" font-size="{sz}" text-anchor="{a}" '
        f'font-family="Liberation Serif, Times New Roman, serif"{" font-style=\"italic\"" if it else ""}>{s}</text>')
    arrow = lambda x, y1, y2, c: (
        f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2 - 14}" stroke="{c}" stroke-width="2.4"/>'
        f'<polygon points="{x},{y2} {x - 7},{y2 - 16} {x + 7},{y2 - 16}" fill="{c}"/>')
    parts += [
        f'<line x1="0" y1="52" x2="{w + 110}" y2="52" stroke="{red}" stroke-width="2.4" stroke-dasharray="12 8"/>',
        t(w + 105, 36, "Datum (fixed)", red, "end", 24),
        f'<line x1="150" y1="535" x2="252" y2="535" stroke="{red}" stroke-width="1.6" stroke-dasharray="6 5"/>',
        arrow(240, 54, 535, red), t(250, 300, "y", red, it=True), t(266, 308, "C", red, sz=18),
        f'<line x1="219" y1="705" x2="352" y2="705" stroke="{red}" stroke-width="1.6" stroke-dasharray="6 5"/>',
        arrow(340, 54, 705, red), t(350, 420, "y", red, it=True), t(366, 428, "D", red, sz=18),
        t(92, 580, "C", "#000", "end", 28, True), t(138, 760, "D", "#000", "end", 28, True),
        f'<line x1="10" y1="{h + 40}" x2="60" y2="{h + 40}" stroke="{blue}" stroke-width="6" opacity="0.75"/>',
        t(70, h + 49, "cable 1 (from the drum)", "#000"),
        f'<line x1="10" y1="{h + 80}" x2="60" y2="{h + 80}" stroke="{green}" stroke-width="6" opacity="0.75"/>',
        t(70, h + 89, "cable 2 (hub of C → under D → ceiling)", "#000"),
    ]
    W, H = w + 130, h + 110
    return (f'<svg class="fig" viewBox="-10 0 {W} {H}" width="{W * 0.62:.0f}" role="img" '
            f'aria-label="Q2 pulley figure with cables, datum and coordinates marked">' + "".join(parts) + "</svg>")


# ---------------------------------------------------------------- Q3 instantaneous centre
def q3_ic():
    f = Fig(620, "Q3 instantaneous centre of AB")
    O, B = V(0, 0), V(-0.075, 0.1)
    A = V(0.19723, 0.22605)
    C = V(-0.075, -0.08596)
    f.line(T(C), T(O), "cons")
    f.line(T(C), T(B), "cons")
    f.line(T(O), (0.13, 0), "muted", dash="4 4")
    f.link(T(O), T(A))
    f.link(T(A), T(B))
    f.slider(T(B), 0, w=26, h=14, guide=58)
    f.pivot(T(O))
    f.pin(T(A))
    f.text(T(O), "O", dx=14, dy=8, anchor="start")
    f.text(T(A), "A", dx=10, dy=-8, anchor="start")
    f.text(T(B), "B", dx=-6, dy=-18, anchor="end")
    f.arc(T(O), 34, 0, 48.9, "muted", "48.9°", lr=50)
    f.arc(T(O), 24, 330, 270, "muted", None, arrow=True, ccw=False)
    f.text(T(O), "2 rad/s", "muted", dx=22, dy=34, anchor="start")
    dA = U(-41.1)
    f.arrow(T(A), T(A + 0.1 * dA), "abs", "v_{A}", at=("E", 8), lpos=1.0)
    f.arrow(T(B), T(B + V(0.07, 0)), "ans", "v_{B}", at=("E", 6), lpos=1.0)
    f.dot(T(C), r=4.5, cls="dotans")
    f.text(T(C), "C (IC)", "ans", dx=-10, dy=10, anchor="end")
    f.dim(T(C), T(A), "", off=30, side="r")
    f.text(T(C + 0.1 * (A - C)), "r_{A/C} = 414 mm", "muted", dx=34, dy=12, anchor="start")
    f.dim(T(C), T(B), "", off=24, side="l")
    f.text(T((B + C) / 2), "r_{B/C} = 186 mm", "muted", dx=-30, dy=0, anchor="end")
    return f.svg()


# ---------------------------------------------------------------- Q4 geometry and polygons
def q4_geom():
    f = Fig(420, "Q4 link geometry with the given angles")
    A, B = V(0, 0), 0.5 * U(60)
    C = B + 0.25 * U(315)
    f.line(T(A), (0.2, 0), "muted", dash="4 4")
    f.line(T(B), T(B + V(0.17, 0)), "muted", dash="4 4")
    f.link(T(A), T(B))
    f.link(T(B), T(C))
    f.slider(T(A), 0, w=26, h=14, guide=50)
    f.pivot(T(C))
    f.pin(T(B))
    f.text(T(A), "A", dx=-10, dy=-16, anchor="end")
    f.text(T(B), "B", dx=-10, dy=-8, anchor="end")
    f.text(T(C), "C", dx=14, dy=-4, anchor="start")
    f.arc(T(A), 36, 0, 60, "muted", "θ = 60°", lr=62)
    f.arc(T(B), 30, 240, 315, "muted", "β = 75°", lr=50)
    f.arc(T(B), 46, 315, 360, "ans", "45°", lr=62)
    f.text(T((A + B) / 2), "0.5 m", "muted", dx=-16, dy=0, anchor="end")
    f.text(T((B + C) / 2), "0.25 m", "muted", dx=-10, dy=12, anchor="end")
    return f.svg()


def q4_vel():
    f = Fig(150, "Q4 velocity polygon drawn to scale")
    o, a = V(0, 0), V(-1, 0)
    b = a + 0.73205 * U(330)
    f.arrow(T(o), T(a), "abs", "v_{A} = 1 m/s", at=("N", 10), lpos=0.5)
    f.arrow(T(a), T(b), "n", "v_{B/A} = 0.732", at=("SW", 8), lpos=0.6)
    f.arrow(T(o), T(b), "ans", "v_{B} = 0.518", at=("SE", 6), lpos=0.6)
    f.arc(T(o), 30, 180, 225, "muted", "45°", lr=44)
    f.arc(T(a), 30, 330, 360, "muted", "30°", lr=44)
    f.arc(T(b), 22, 45, 150, "muted", "105°", lr=36)
    f.text(T(o), "o", dx=8, dy=-8, anchor="start")
    f.text(T(a), "a", dx=-8, dy=-8, anchor="end")
    f.text(T(b), "b", dx=0, dy=14)
    f.set_scalebar(0.5, "1 cm = 0.5 m/s")
    return f.svg()


def q4_acc():
    f = Fig(215, "Q4 acceleration polygon drawn to scale")
    o, a = V(0, 0), V(-0.25, 0)
    p = a + 1.0718 * U(240)
    q = 1.0718 * U(315)
    b = p + 1.0054 * U(330)
    f.line(T(p - 0.25 * U(330)), T(b + 0.35 * U(330)), "cons")
    f.line(T(q - 0.25 * U(225)), T(b + 0.35 * U(225)), "cons")
    f.arrow(T(o), T(a), "abs", "a_{A} = 0.25", at=("N", 10), lpos=0.5)
    f.arrow(T(a), T(p), "n", "(a_{B/A})_{n} = 1.072", at=("W", 8), lpos=0.5)
    f.arrow(T(p), T(b), "t", "(a_{B/A})_{t} = 1.01", at=("SW", 8), lpos=0.55)
    f.arrow(T(o), T(q), "n", "(a_{B})_{n} = 1.072", at=("NE", 6), lpos=0.6)
    f.arrow(T(q), T(b), "t", "(a_{B})_{t} = 0.952", at=("SE", 8), lpos=0.5)
    f.arrow(T(o), T(b), "ans", "a_{B} = 1.43", at=("E", 6), lpos=0.42, dashed=True)
    f.text(T(o), "o", dx=6, dy=-10, anchor="start")
    f.set_scalebar(0.2, "1 cm = 0.2 m/s²")
    return f.svg()


# ---------------------------------------------------------------- Q5 drum FBD
def q5_fbd():
    f = Fig(150, "Q5 free-body diagram of the drum")
    O = V(0, 0)
    f.circle(T(O), 0.5, "outline")
    f.circle(T(O), 0.48, "outline thin", dash="5 4")
    f.arrow(T(V(0, 0.5)), T(V(0.62, 0.5)), "ans", "T = 400 N", at=("N", 10), lpos=0.65)
    f.arrow(T(V(-0.42, 0)), T(O), "muted", "O_{x}", at=("N", 10), lpos=0.35)
    f.arrow(T(V(-0.06, -0.42)), T(V(-0.06, 0)), "muted", "O_{y}", at=("W", 6), lpos=0.3)
    f.arrow(T(V(0.06, 0)), T(V(0.06, -0.4)), "muted", "W", at=("E", 6), lpos=0.8)
    f.dot(T(O))
    f.text(T(O), "O", dx=10, dy=12, anchor="start")
    f.dim(T(O), T(V(0, 0.5)), "0.5 m", off=40, side="r")
    f.arc(T(O), 92, 140, 200, "abs", "ω_{1} = 3 rad/s", arrow=True, lr=118, la=140)
    return f.svg()


# ---------------------------------------------------------------- Q6 FBD and acceleration diagram
def q6_fbd():
    f = Fig(150, "Q6 free-body diagram just after cable B breaks")
    A, B = V(0, 0), V(1.5, 0)
    G = (A + B) / 2
    f.line(T(A), T(V(-0.35, 0)), "muted", dash="4 4")
    f.link(T(A), T(B), w=10)
    f.arrow(T(A), T(A + 0.5 * U(120)), "ans", "T", at=("E", 8), lpos=0.8)
    f.arrow(T(G), T(G + V(0, -0.45)), "muted", "W = mg", at=("E", 8), lpos=0.8)
    f.arc(T(A), 34, 120, 180, "muted", "60°", lr=50)
    f.dot(T(G))
    f.text(T(G), "G", dx=0, dy=-16)
    f.text(T(A), "A", dx=-4, dy=18, anchor="end")
    f.text(T(B), "B: T_{B} = 0", dx=-6, dy=-18)
    f.dim(T(A), T(G), "l/2", off=30, side="r")
    return f.svg()


def q6_acc():
    f = Fig(150, "Q6 acceleration diagram: a_A perpendicular to the cable, alpha(l/2) at G")
    A, B = V(0, 0), V(1.5, 0)
    G = (A + B) / 2
    f.line(T(A), T(A + 0.4 * U(120)), "cons")
    f.link(T(A), T(B), w=10)
    f.arrow(T(A), T(A + 0.4 * U(210)), "abs", "a_{A} (⊥ cable)", at=("S", 12), lpos=1.0)
    f.arrow(T(G), T(G + V(0, -0.42)), "n", "(a_{G/A})_{t} = α l/2", at=("E", 8), lpos=0.75)
    f.arc(T(G), 30, 150, 40, "ans", "α", arrow=True, ccw=False, lr=44, la=95)
    f.dot(T(G))
    f.text(T(A), "A", dx=6, dy=16, anchor="start")
    f.text(T(B), "B", dx=6, dy=16, anchor="start")
    P0 = V(2.05, 0.05)
    P1 = P0 + 0.4 * U(210)
    P2 = P1 + V(0, -0.42)
    f.arrow(T(P0), T(P1), "abs", "a_{A}", at=("N", 8), lpos=0.5)
    f.arrow(T(P1), T(P2), "n", "α l/2", at=("W", 8), lpos=0.5)
    f.arrow(T(P0), T(P2), "ans", "a_{G}", at=("E", 8), lpos=0.6)
    f.text(T(V(1.85, -0.75)), "ω = 0: no normal terms", "muted", anchor="middle")
    return f.svg()


# ---------------------------------------------------------------- Q7 spring states
def q7_states():
    f = Fig(3.6, "Q7 plunger positions and spring deformations (mm)")
    lv = [(40, "(1) released from rest", "ink"), (12.26, "spring at natural length", "muted"),
          (0, "equilibrium position", "muted"), (-6, "(2) hits button A (datum)", "ink")]
    for y, s, c in lv:
        f.line((-10, y), (30, y), c, dash=None if c == "ink" else "5 4")
        f.text((33, y), s, c, anchor="start")
    f.dim((-12, 12.26), (-12, 40), "", off=8, side="r")
    f.text((-24, 26.1), "x_{1} = 27.74 (stretch)", "ans", anchor="end")
    f.dim((-12, -6), (-12, 12.26), "", off=8, side="r")
    f.text((-24, 3.1), "x_{2} = 18.26 (squash)", "ans", anchor="end")
    f.dim((84, 0), (84, 12.26), "", off=8, side="l")
    f.text((89, 6.1), "δ_{st} = 12.26", "muted", anchor="start")
    return f.svg()


# ---------------------------------------------------------------- Q8 impact n-t axes
def q8_nt():
    f = Fig(125, "Q8 line of impact (n) at 20 degrees and the tangent (t)")
    A = V(0, 0)
    n = U(20)
    Bc = 0.92 * n
    K = 0.5 * n
    f.circle(T(A), 0.5, "outline")
    f.circle(T(Bc), 0.42, "outline")
    f.line(T(K - 0.95 * n), T(K + 0.95 * n), "cons")
    f.line(T(K - 0.55 * U(110)), T(K + 0.55 * U(110)), "cons")
    f.text(T(K + 0.98 * n), "n", "muted", dx=8, anchor="start")
    f.text(T(K + 0.58 * U(110)), "t", "muted", dy=-8)
    f.line(T(K), T(K + V(0.6, 0)), "muted", dash="3 3")
    f.arc(T(K), 40, 0, 20, "muted", "20°", lr=58, la=-8)
    f.arrow(T(V(-0.32, -0.12)), T(V(0.12, -0.12)), "abs", "v_{A} = 18", at=("S", 12), lpos=0.5)
    f.arrow(T(Bc + V(0.95, -0.02)), T(Bc + V(0.48, -0.02)), "abs", "v_{B} = 38", at=("S", 12), lpos=0.4)
    f.arrow(T(Bc), T(Bc + 0.62 * U(45.7)), "ans", "v′_{B} = 30.0 m/s", at=("E", 6), lpos=1.0)
    f.line(T(Bc), T(Bc + V(0.38, 0)), "muted", dash="3 3")
    f.arc(T(Bc), 30, 0, 45.7, "ans", "β", lr=44)
    f.text(T(A + V(-0.3, 0.42)), "A (bat)", anchor="end")
    f.text(T(Bc), "B", dx=-12, dy=-14, anchor="end")
    return f.svg()


# ---------------------------------------------------------------- Q9 FBD = KD
def _q9_beam(f):
    O, A, B = V(0, 0), V(0, -0.9), V(4, -0.9)
    f.line(T(O), T(A), "muted")
    f.line(T(O), T(V(0.7, -0.9)), "muted")
    f.link(T(A), T(B), w=10)
    f.pin(T(O), 4.6)
    f.text(T(O), "O", dx=-8, dy=-10, anchor="end")
    f.text(T(A), "A", dx=-8, dy=8, anchor="end")
    f.text(T(B), "B", dx=8, dy=8, anchor="start")
    return O, V(2, -0.9)


def q9_fbd():
    f = Fig(58, "Q9 free-body diagram just after support B is removed")
    O, G = _q9_beam(f)
    f.arrow(T(O + V(-0.9, 0)), T(O), "muted", "O_{x}", at=("N", 8), lpos=0.4)
    f.arrow(T(O + V(0, 0.9)), T(O), "muted", "O_{y}", at=("E", 6), lpos=0.4)
    f.arrow(T(G), T(G + V(0, -1.0)), "ans", "W = 300(9.81)", at=("E", 6), lpos=0.7)
    f.dot(T(G))
    f.text(T(G), "G", dx=-8, dy=-14)
    f.dim(T(O), T(V(2, 0)), "2 m", off=18, side="l")
    f.line(T(O), T(V(2.2, 0)), "muted", dash="3 4")
    f.dim(T(V(2, 0)), T(G), "0.9 m", off=14, side="l")
    return f.svg()


def q9_kd():
    f = Fig(58, "Q9 kinetic diagram: I_G alpha and m a_G with omega = 0")
    O, G = _q9_beam(f)
    f.line(T(O), T(G), "cons")
    f.arrow(T(G), T(G + V(-1.0, 0)), "n", "m(0.9α)", at=("S", 12), lpos=0.6)
    f.arrow(T(G), T(G + V(0, -1.0)), "n", "m(2α)", at=("E", 6), lpos=0.75)
    f.arc(T(G), 22, 160, 30, "ans", "I_{G}α", arrow=True, ccw=False, lr=36, la=95)
    f.dot(T(G))
    return f.svg()


def build_all(q2img=None):
    out = {"q3_ic": q3_ic(), "q4_geom": q4_geom(), "q4_vel": q4_vel(), "q4_acc": q4_acc(),
           "q5_fbd": q5_fbd(), "q6_fbd": q6_fbd(), "q6_acc": q6_acc(), "q7_states": q7_states(),
           "q8_nt": q8_nt(), "q9_fbd": q9_fbd(), "q9_kd": q9_kd()}
    if q2img:
        out["q2_vars"] = q2_vars(*q2img)
    return out


if __name__ == "__main__":
    for k, v in build_all().items():
        print(k, len(v))
