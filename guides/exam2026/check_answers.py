"""Independent solutions for the MEC2047S final exam (13 Nov 2026), used for the memo."""
import numpy as np
from math import *
g = 9.81
print("Q1"); aA = hypot(0.75, 9/40); an = sqrt(aA**2 - 0.7**2); print(f"  |a_A|={aA:.4f} a_n,A={9/40} a_n,B={an:.4f} v_B={sqrt(an*20):.3f}")
print("Q2  6 strands on A: v_A =", 3.15/6, " (with 5 strands: ", 3.15/5, ")")
k_ = (2/3)*(81**1.5 - 36**1.5)/18; print(f"Q3  k={k_} v20={(81**1.5 - 1.5*k_*20)**(2/3):.3f} t={18/k_:.4f}")
vd = sqrt(2*g*6); vc = 100/3.6; rel = np.array([-vc, -vd]); n = np.array([cos(radians(50)), sin(radians(50))])
print(f"Q4  v_drop={vd:.3f} v_car={vc:.3f} v_rel={rel.round(3)} angle to -n = {degrees(acos((-n)@rel/np.linalg.norm(rel))):.2f}")
k3 = np.array([0,0,1.]); V = lambda x,y: np.array([x,y,0.])
A, B, C, D, E = V(0,0), V(0,.09), V(.225,0), V(.225,.18), V(.45,.27)
vB = -6*np.cross(k3, B-A); print("Q5  vB", vB[:2])
M = np.column_stack([np.cross(k3, D-B)[:2], -np.cross(k3, D-C)[:2]]); wBD, wCD = np.linalg.solve(M, -vB[:2]); print(f"    w_BDE={wBD:.4f} w_CD={wCD:.4f}")
aB = -36*(B-A); rhs = -aB[:2] + wBD**2*(D-B)[:2] - wCD**2*(D-C)[:2]; aBD, aCD = np.linalg.solve(M, rhs)
aE = aB + aBD*np.cross(k3, E-B) - wBD**2*(E-B)
print(f"    aB={aB[:2]} alpha_BDE={aBD:.4f} alpha_CD={aCD:.4f} aE={aE[:2].round(4)} |{np.linalg.norm(aE):.4f}|; BD={np.linalg.norm(D-B):.4f}")
s = (80/3.6)**2/(2*0.32*g); print(f"Q6  a={0.32*g:.4f} s={s:.2f}")
W45 = 45*g; ws, wf = W45*sin(radians(25)), 0.33*W45*cos(radians(25))
net1 = 28*g*1.15 - (ws+wf)*0.575; vc2 = net1/(14 + 45/8); vb2 = vc2/4
d = (0.5*13*vc2 + 0.5*45*vb2)/((ws+wf) - 13*g*2)
print(f"Q7  ws={ws:.2f} wf={wf:.2f} phase1 net={net1:.2f} v_c={sqrt(vc2):.3f} v_b={sqrt(vb2):.3f} extra d={d:.4f} total s={0.575+d:.3f}")
print(f"    (single-cable check: 28g={28*g:.1f} vs resistance {ws+wf:.1f} -> would not move)")
m, L = 0.12, 0.1
Iz = 0 + m*L**2/3 + m*(L**2/3 + 0.1**2) + m*L**2/3 + m*0.1**2; print(f"Q8  I_z={Iz:.6f}")
vB9 = 1300*45*tan(radians(25))/1500; v9 = 1300*45/(2800*cos(radians(25))); print(f"Q9  v_B={vB9:.3f} km/h v={v9:.3f} km/h")
m, ro, ri, kk, th, ms = 30, .45, .2, .275, radians(20), .45
Ws, N = m*g*sin(th), m*g*cos(th)
Ta = Ws/(1 - ri/ro); Fa = -ri*Ta/ro
c = kk**2/ro**2; Fmax = ms*N
# F = -(ri/ro)T - c m a ; m a = T + F - Ws
A_ = np.array([[1, ri/ro, c],[0,0,0],[0,0,0]])
T = (Fmax + c*Ws/(1+c) - 0) ; 
# solve: F = -(ri/ro)T - c(T + F - Ws)  ->  F(1+c) = -(ri/ro + c)T + c Ws
Tb = (Fmax*(1+c) + c*Ws)/(ri/ro + c); ab = (Tb - Fmax - Ws)/m
print(f"Q10 N={N:.2f} Fmax={Fmax:.2f} (a) T={Ta:.2f} F={Fa:.2f} (down slope)  (b) T={Tb:.2f}  (c) a_G={ab:.4f} up slope, alpha={ab/ro:.3f}")
print(f"    user's (a) with F = mu_s N: T = {Ws - Fmax:.1f} or {Ws + Fmax:.1f} (wrong: friction isn't at its limit)")
