"""Checks for the reconstructed CT2 2026 question (bar AB: A on a horizontal track, B in a 0.5 m circular guide)."""
import numpy as np
from math import *
U = lambda d: np.array([cos(radians(d)), sin(radians(d))])
R, L, vA = 0.5, 1.2, 3.0
h1 = R * cos(radians(60)); h2 = R - h1; beta = degrees(asin(h2 / L))
print(f"h1={h1} h2={h2} beta={beta:.3f} deg")
# directions: v_B ⊥ radius (radius B->centre at 30 deg) -> 300 deg ; v_B/A ⊥ AB (AB from A to B at 180-beta) -> 258 deg
dB, dBA = 300.0, 270.0 - beta
M = np.column_stack([U(dB), -U(dBA)]); vB, vBA = np.linalg.solve(M, np.array([vA, 0.0]))
print(f"sine rule angles: at o {dB - 360 + 360 - 300 + 60:.0f}, v_B = {vA*sin(radians(90-beta))/sin(radians(180-60-(90-beta))):.4f}")
print(f"vB={vB:.4f} @ {dB}, vB/A={vBA:.4f} @ {dBA:.1f}, w_OB={vB/R:.4f}, w_AB={vBA/L:.4f}")
aBn = vB**2 / R; aBAn = vBA**2 / L
rhs = aBAn * U(360 - beta) - aBn * U(30)      # aBn U(30) + t1 U(300) = aBAn U(348) + t2 U(78)
M2 = np.column_stack([U(300), -U(90 - beta)]); t1, t2 = np.linalg.solve(M2, rhs)
print(f"aBn={aBn:.3f} (memo 38.54 with rounded w) aBAn={aBAn:.3f}")
print(f"(aB)t = {t1:.3f} along 300 deg -> {abs(t1):.2f} @ {300 if t1 > 0 else 120} deg ; (aB/A)t = {t2:.3f} along {90-beta:.0f} deg")
print(f"alpha_AB = {abs(t2)/L:.3f} rad/s^2 ; |a_B| = {hypot(aBn, t1):.3f}")
aB = aBn * U(30) + t1 * U(300); print("a_B vector:", aB.round(3), "check RHS:", (aBAn * U(360 - beta) + t2 * U(90 - beta)).round(3))
# sense of alpha: (aB/A)t at 78 deg at B; r_B/A at 168 deg; k x e(168) = e(258) for CCW -> 78 deg means CW
print("alpha sense: CW" if abs(((90 - beta) - (168 + 90)) % 360 - 180) < 1e-6 else "check")
