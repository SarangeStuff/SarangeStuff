"""Numbers for the rolling doc, each checked a second way."""
import numpy as np
from math import *
g = 9.81
k = np.array([0, 0, 1.0]); V = lambda x, y: np.array([x, y, 0.0]); cr = lambda w, r: w * np.cross(k, r)

print("K1 gear on rack (L17 Ex 1): r = 0.3, w = 12 CW, alpha = 6 CW; point A at the top")
r, w, al = 0.3, -12.0, -6.0
aO = V(-al * r, 0); rA = V(0, r); aA = aO + cr(al, rA) - w**2 * rA
print(f"  aO={aO[:2]} (a_A/O)_t={cr(al, rA)[:2]} (a_A/O)_n={(-w**2*rA)[:2]} aA={aA[:2]} |{np.linalg.norm(aA):.2f}| at {degrees(atan2(aA[1], aA[0])):.1f}")
print(f"  contact point C: {(aO + cr(al, V(0, -r)) - w**2 * V(0, -r))[:2]} (= r w^2 up: {r*w*w})")
print(f"  velocities: top = {abs(w)*2*r}, centre = {abs(w)*r}, contact = 0")

print("W1 cylinder 3.6 kg r 0.15 down 30 deg, mu_s 0.30 (no slip expected)")
m, r, th, ms = 3.6, 0.15, radians(30), 0.30
aG = 2 / 3 * g * sin(th); al = aG / r; F = m * g * sin(th) - m * aG; N = m * g * cos(th)
print(f"  aG={aG:.3f} alpha={al:.2f} F={F:.3f} N={N:.3f} Fmax={ms*N:.3f} mu_min={F/N:.4f} = tan/3 {tan(th)/3:.4f}")
print(f"  moments about C: mg r sin = {m*g*r*sin(th):.4f}, (1/2 m r^2 + m r^2) alpha = {1.5*m*r*r*al:.4f}")
print("W2 same cylinder on 60 deg, mu_s 0.30, mu_k 0.25")
th = radians(60); mu_min = tan(th) / 3; mk = 0.25
aG2 = g * (sin(th) - mk * cos(th)); F2 = mk * m * g * cos(th); al2 = F2 * r / (0.5 * m * r * r)
print(f"  mu_min={mu_min:.3f} > 0.30 -> slips; aG={aG2:.3f} alpha={al2:.3f} r*alpha={r*al2:.3f} (aG > r alpha: contact skids down)")

print("Particle vs rolling on 30 deg: a = g sin / (1 + k^2/r^2)")
for name, kk in (("block (no rotation, smooth)", None), ("thin hoop", 1.0), ("solid cylinder", 0.5), ("solid sphere", 0.4)):
    a = g * sin(radians(30)) if kk is None else g * sin(radians(30)) / (1 + kk)
    mm = "-" if kk is None else f"{tan(radians(30))*kk/(1+kk):.3f}"
    print(f"  {name:28s} a = {a:.3f}  mu_min = {mm}")

print("W3 mock Q8: solid cylinder 30 kg r 0.25, P at centre; mu_s 0.2 mu_k 0.15")
m, r = 30.0, 0.25; N = m * g
for P in (120.0, 200.0):
    a = P / (1.5 * m); F = 0.5 * m * a
    if F <= 0.2 * N:
        print(f"  P={P}: a={a:.3f} alpha={a/r:.3f} F={F:.2f} <= {0.2*N:.2f}")
    else:
        Fk = 0.15 * N; print(f"  P={P}: need {F:.2f} > {0.2*N:.2f} -> slips: F={Fk:.2f} a={(P-Fk)/m:.3f} alpha={2*Fk/(m*r):.3f}")

print("W4 bowling ball: m 6.4, r 0.12, k 0.083, v0 6, mu 0.2 -> s = 4.98 m (see planekinetics/check_answers.py)")
v0, r, kG, mu = 6.0, 0.12, 0.083, 0.2
a = mu * g; al = mu * g * r / kG**2; t = v0 / (a + al * r); v = v0 - a * t; s = v0 * t - 0.5 * a * t**2
print(f"  a={a:.3f} alpha={al:.2f} t={t:.4f} v={v:.3f} s={s:.3f}")

print("W5 rod on hoop: alpha = 3g/(8l) = ", 3 * g / (8 * 0.25), " mu_min = 0.462 (see planekinetics)")

print("W6 spool: m 10, outer R 0.3, hub r 0.15, k_G 0.2, string pulled right with T = 50 N")
m, R, ri, kG, T = 10.0, 0.3, 0.15, 0.2, 50.0
for where, arm in (("top of hub", ri), ("bottom of hub", -ri)):
    al = T * (R + arm) / (m * (kG**2 + R**2)); a = R * al; F = m * a - T
    print(f"  string at {where}: alpha={al:.3f} (CW) a={a:.3f} -> F = {F:+.3f} N ({'forwards' if F > 0 else 'backwards'}), mu needed {abs(F)/(m*g):.4f}")
