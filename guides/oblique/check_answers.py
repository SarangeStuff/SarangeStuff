"""Checks for the oblique-impact explainer (S25 Q6, F25 Q8, the wall warm-up)."""
import numpy as np
from math import *

print("Warm-up: ball hits a smooth wall at 10 m/s, 30 deg to the wall, e = 0.6")
v, ang, e = 10, 30, 0.6
vt, vn = v * cos(radians(ang)), v * sin(radians(ang))
vn2 = e * vn
print(f"  v_t = {vt:.3f} (kept), v_n = {vn:.3f} -> {vn2:.3f} back, speed {hypot(vt, vn2):.3f} at {degrees(atan2(vn2, vt)):.1f} deg to the wall")

print("S25 Q6: mA = 8 (5 m/s left), mB = 6 (7 m/s right), e = 0.5, n along the 5-12-13 line")
th = atan(5 / 12); n = np.array([5 / 13, 12 / 13]); t = np.array([12 / 13, -5 / 13])
vA, vB, mA, mB, e = np.array([-5.0, 0]), np.array([7.0, 0]), 8, 6, 0.5
An, At, Bn, Bt = vA @ n, vA @ t, vB @ n, vB @ t
print(f"  theta = {degrees(th):.2f}, sin = {sin(th):.4f} (5/13), cos = {cos(th):.4f} (12/13)")
print(f"  A: n {An:.3f} t {At:.3f} | B: n {Bn:.3f} t {Bt:.3f}")
M = np.array([[mA, mB], [1, -1]]); r = np.array([mA * An + mB * Bn, e * (Bn - An)])
An2, Bn2 = np.linalg.solve(M, r)
vA2, vB2 = An2 * n + At * t, Bn2 * n + Bt * t
print(f"  after: A n {An2:.4f} t {At:.3f} -> {np.linalg.norm(vA2):.3f} m/s, vec {vA2.round(3)}, {degrees(atan2(vA2[1], -vA2[0])):.1f} deg above the -x axis")
print(f"         B n {Bn2:.4f} t {Bt:.3f} -> {np.linalg.norm(vB2):.3f} m/s, vec {vB2.round(3)}, {degrees(atan2(-vB2[1], vB2[0])):.1f} deg below +x")
print(f"  momentum n before {mA*An + mB*Bn:.4f} after {mA*An2 + mB*Bn2:.4f}; KE before {0.5*mA*25 + 0.5*mB*49:.1f} after {0.5*mA*vA2@vA2 + 0.5*mB*vB2@vB2:.1f}")
print(f"  approach (Bn - An) = {Bn - An:.3f}, separation (An2 - Bn2) = {An2 - Bn2:.4f}")

print("F25 Q8: bat A 0.5 kg -> 18 (in a horizontal slot), ball B 0.146 kg <- 38, e = 0.5, n at 20 deg")
n = np.array([cos(radians(20)), sin(radians(20))]); t = np.array([-sin(radians(20)), cos(radians(20))])
mA, mB = 0.5, 0.146; vA, vB = np.array([18.0, 0]), np.array([-38.0, 0])
Bt = vB @ t; An, Bn = vA @ n, vB @ n
M = np.array([[mA, mB * n[0]], [-n[0], 1]]); r = np.array([mA * 18 + mB * -38 - mB * Bt * t[0], -e * (Bn - An)])
vA2, Bn2 = np.linalg.solve(M, r); vB2 = Bn2 * n + Bt * t
print(f"  A n {An:.3f} | B n {Bn:.3f} t {Bt:.3f}")
print(f"  after: bat {vA2:.3f} ->, ball n {Bn2:.3f} t {Bt:.3f} -> {np.linalg.norm(vB2):.3f} m/s at {degrees(atan2(vB2[1], vB2[0])):.1f} deg; vec {vB2.round(3)}")
print(f"  KE before {0.5*mA*18**2 + 0.5*mB*38**2:.1f} after {0.5*mA*vA2**2 + 0.5*mB*vB2@vB2:.1f}")
print(f"  WRONG way (conserving momentum along n as if the bat were free): ", end="")
An2w, Bn2w = np.linalg.solve(np.array([[mA, mB], [1, -1]]), np.array([mA*An + mB*Bn, e*(Bn - An)]))
print(f"ball n {Bn2w:.2f}, speed {hypot(Bn2w, Bt):.2f}")
