"""Answer-key values for the guided practice paper (each derived two ways where possible)."""
import numpy as np
from math import *
k = np.array([0, 0, 1.0]); V = lambda x, y: np.array([x, y, 0.0]); cr = lambda w, r: w * np.cross(k, r)
ang = lambda v: degrees(atan2(v[1], v[0])) % 360

print("Q0 warm-up")
r = 0.5 * V(1, 0); print("  (a)", cr(2, r)[:2])
r = 0.25 * V(cos(radians(30)), sin(radians(30))); vba = cr(-4, r); print("  (b) v_B/A", vba[:2].round(3), round(np.linalg.norm(vba), 3), round(ang(vba), 1))
print("  (c) v_A/B", (-vba)[:2].round(3), round(ang(-vba), 1))
an = 16 * 0.25; print("  (d) (a_B/A)_n =", an, "at", (30 + 180) % 360)

print("Q1 5/17")
B = 0.5 * V(sin(radians(15)), -cos(radians(15))); A = B + 0.3 * V(cos(radians(-15)), sin(radians(-15)))
print("  OA^2 =", round(0.25 + 0.09 - 2 * 0.5 * 0.3 * cos(radians(120)), 4), "B =", B[:2].round(4), "A =", A[:2].round(4))
print("  v =", cr(2, A)[:2].round(3), "alpha x r =", cr(-5, A)[:2].round(3), "-w2 r =", (-4 * A)[:2].round(3), "a =", (cr(-5, A) - 4 * A)[:2].round(3))

print("Q2 5/26: w =", 1.5 / 0.075, "alpha =", 45 / 0.4, "an =", 0.36 * 400, "at =", 0.36 * 112.5, "aC =", round(hypot(144, 40.5), 1), "angle =", round(degrees(atan(40.5 / 144)), 1))

print("Q3 5/44 with r = 0.2, x = 0.5, v = 1.5")
r_, x_, v_ = 0.2, 0.5, 1.5
print("  theta =", round(degrees(asin(r_ / x_)), 2), " w =", round(v_ / (x_ * sqrt((x_ / r_) ** 2 - 1)), 3), " (x/r)^2 - 1 =", round((x_ / r_) ** 2 - 1, 3))

print("Q4 5/119")
B = 0.8 * V(cos(radians(-30)), sin(radians(-30))); A = V(B[0] + sqrt(0.49 - B[1] ** 2), 0)
C = V(A[0], -A[0] * tan(radians(30)))
vD = 0.6 / sin(radians(60)); w = vD / 1.2; vB = 0.8 * w
print(f"  vD={vD:.4f} wOD={w:.4f} vB={vB:.4f} B={B[:2].round(4)} sqrt(0.7^2-0.4^2)={sqrt(0.49 - 0.16):.4f} xA={A[0]:.4f}")
print(f"  C={C[:2].round(4)} OC={np.linalg.norm(C):.4f} rB/C={np.linalg.norm(B - C):.4f} rA/C={np.linalg.norm(A - C):.4f} wAB={vB / np.linalg.norm(B - C):.4f} vA={vB / np.linalg.norm(B - C) * np.linalg.norm(A - C):.4f}")
dAB = ang(A - B); print(f"  AB direction (B to A) = {dAB:.2f}, perpendicular = {dAB + 90:.2f} / {dAB + 270:.2f}")
vBv = cr(-w, B); vA = -0.5095; vAB = V(vA, 0) - vBv
print(f"  v_B vec={vBv[:2].round(4)} at {ang(vBv):.1f}; v_A/B = {vAB[:2].round(4)} |{np.linalg.norm(vAB):.4f}| at {ang(vAB):.2f}; w = {np.linalg.norm(vAB)/0.7:.4f}")
print(f"  sine rule: angles 60, {180 - (ang(vAB) - 60):.2f}?, check vA = {vB*sin(radians(64.85))/sin(radians(55.15)):.4f}, vA/B = {vB*sin(radians(60))/sin(radians(55.15)):.4f}")

print("Q5 5/108: C = (xB, yD): vertical A-C =", 0.3 * sin(radians(30)), "w =", round(2 / 0.15, 3), "horizontal C-D =", round(0.2 * cos(radians(30)), 4), "vD =", round(2 / 0.15 * 0.2 * cos(radians(30)), 3))

print("Q6 T11 Q4: see ../planekinetics/check_answers.py -> B = 4.03 N, Ax = 0.32 N, Ay = 4.06 N, alpha_AB = 0.667 CW, alpha_CB = 2 CCW, aG = (0.4, 0.3)")

print("== Practice-exam variants")
U2 = lambda d: np.array([cos(radians(d)), sin(radians(d))])
vA, vB = np.array([24.0, 0]), np.array([0, 10.0]); r = vB - vA
print(f"Q1b cars: v_B/A = {r} |{np.linalg.norm(r):.2f}| at {degrees(atan2(r[1], r[0])):.1f} deg = {degrees(atan(10/24)):.1f} N of W")
print("Q1c gears: (a_A')_t = 100, alpha_B = 100/2 =", 100 / 2, " alpha_C = 100/1 =", 100 / 1)
vAm, vBm, aBt = 90 / 3.6, 72 / 3.6, 0.8
VA, VB = vAm * U2(115), vBm * U2(90)
AA = vAm**2 / 375 * U2(205); AB = vBm**2 / 360 * U2(180) + aBt * U2(90)
vr, ar = VA - VB, AA - AB
print(f"Q2 variant: vA={vAm} vB={vBm} VA={VA.round(3)} VB={VB.round(3)} v_A/B={vr.round(3)} |{np.linalg.norm(vr):.3f}| at {degrees(atan2(vr[1], vr[0])) % 360:.1f}")
print(f"   (aA)n={vAm**2/375:.4f} AA={AA.round(4)} (aB)n={vBm**2/360:.4f} AB={AB.round(4)} a_A/B={ar.round(4)} |{np.linalg.norm(ar):.4f}| at {degrees(atan2(ar[1], ar[0])) % 360:.1f} -> {degrees(atan2(-ar[1], -ar[0])):.1f} deg below the -x axis")
print(f"   cosine rule check |vA/B|: {sqrt(vAm**2 + vBm**2 - 2*vAm*vBm*cos(radians(25))):.3f}")
