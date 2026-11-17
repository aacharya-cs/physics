import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # style.py sits beside this script
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, Arc, Ellipse
from style import *

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figs'))  # repo-root figs/
BLK = '#93C5C6'


def plain_axes(fig, rect):
    ax = fig.add_axes(rect)
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
    for sp in ('left', 'bottom'): ax.spines[sp].set_color(INK)
    ax.set_xticks([]); ax.set_yticks([])
    return ax


# ------------------------------------------------------------- grav_universal
def grav_universal():
    fig, ax = newax(5.0, 2.75)
    title(ax, 'The evidence for "universal": one law, two very different measurements')
    Re = 0.60
    ax.add_patch(Circle((0, 0), Re, fc='#BFD3E6', ec=INK, lw=1.3, zorder=4))
    lab(ax, 0, 0, 'Earth', fs=8.0, z=6)
    ax.add_patch(Circle((0.0, Re + 0.17), 0.10, fc=CRIM, ec=INK, lw=0.7, zorder=6))
    arr(ax, 0.0, Re + 0.10, 0.0, Re - 0.16, c=CRIM, lw=1.3, z=7)
    lab(ax, 0.20, Re + 0.36, r'apple: $a=g$', c=CRIM, fs=8.0, ha='left')
    D = 4.0
    tt = np.linspace(np.deg2rad(-14), np.deg2rad(16), 120)
    ax.plot(D*np.cos(tt), D*np.sin(tt), color=GREY, lw=0.9, ls=(0, (5, 4)), zorder=1)
    ax.add_patch(Circle((D, 0), 0.20, fc='#D9E2EC', ec=INK, lw=1.1, zorder=5))
    lab(ax, D + 0.32, -0.02, 'Moon', fs=8.0, ha='left')
    arr(ax, D - 0.22, 0.0, D - 0.86, 0.0, c=PRIM, lw=1.4, z=7)
    lab(ax, D - 0.58, -0.26, r'$a_{\mathrm{Moon}}$', c=PRIM, fs=8.0)
    arr(ax, D, 0.22, D, 0.90, c=FOR, lw=1.3, z=7)
    lab(ax, D + 0.12, 0.76, r'$v$', c=FOR, fs=8.0, ha='left')
    ax.plot([0, 0], [-Re - 0.08, -1.05], color=STEEL, lw=0.6, ls=(0, (2, 2)))
    ax.plot([D, D], [-0.24, -1.05], color=STEEL, lw=0.6, ls=(0, (2, 2)))
    darr(ax, 0, -0.92, D, -0.92)
    lab(ax, D/2, -1.16, r'$r=60\,R_E$', c=STEEL, fs=8.2)
    lab(ax, -1.0, 2.05, 'From dropping things', c=CRIM, fs=8.0, ha='left', weight='bold')
    lab(ax, -1.0, 1.72, r'$g=9.8\ \mathrm{m/s^{2}}$', c=CRIM, fs=8.4, ha='left')
    lab(ax, 2.35, 2.05, "From the Moon's period", c=PRIM, fs=8.0, ha='left', weight='bold')
    lab(ax, 2.35, 1.62, r'$a_{\mathrm{Moon}}=\dfrac{4\pi^{2}r}{T^{2}}=0.0027\ \mathrm{m/s^{2}}$',
        c=PRIM, fs=8.4, ha='left')
    lab(ax, 2.0, -1.78, r'$\dfrac{a_{\mathrm{Moon}}}{g}=\dfrac{1}{3600}=\dfrac{1}{60^{2}}$,'
        r'  exactly as an inverse-square law requires', fs=8.6)
    ax.set_xlim(-1.15, 5.85); ax.set_ylim(-2.25, 2.3)
    save(fig, f'{OUT}/grav_universal.pdf')


# ----------------------------------------------------------------- grav_shell
def grav_shell():
    fig = plt.figure(figsize=(4.3, 2.75))
    fig.suptitle('Gravity inside and outside a planet', fontsize=8.2, color=INK, style='italic', y=0.98)
    ax = plain_axes(fig, [0.12, 0.16, 0.84, 0.70])
    R = 1.0
    ri = np.linspace(0, R, 50); ro = np.linspace(R, 3.4, 200)
    ax.plot(ri, ri, color=PRIM, lw=2.0); ax.plot(ro, 1/ro**2, color=CRIM, lw=2.0)
    ax.plot([R, R], [0, 1], color=GREY, lw=0.8, ls=(0, (3, 3)))
    ax.plot(R, 1, 'o', color=INK, ms=4.5, zorder=5)
    ax.text(R, 1.07, 'surface: the peak', ha='center', fontsize=8.0, color=INK)
    ax.text(0.40, 0.70, r'$g\propto r$', color=PRIM, fontsize=9.0, ha='right')
    ax.text(0.58, 0.16, 'inside: only the mass\nwithin $r$ pulls', color=PRIM, fontsize=7.4, ha='left')
    ax.text(1.85, 0.42, r'$g\propto 1/r^{2}$', color=CRIM, fontsize=9.0)
    ax.text(2.25, 0.20, 'outside: all the mass,\nas if at the centre', color=CRIM, fontsize=7.4, ha='left')
    ax.set_xlim(0, 3.45); ax.set_ylim(0, 1.2)
    ax.set_xlabel('distance from centre $r$', fontsize=8.0, color=INK)
    ax.set_ylabel('$g$', fontsize=8.6, color=INK, rotation=0, labelpad=8)
    ax.set_xticks([R]); ax.set_xticklabels(['$R$'], fontsize=8.0)
    save(fig, f'{OUT}/grav_shell.pdf')


# ------------------------------------------------------------------ grav_well
def grav_well():
    fig = plt.figure(figsize=(4.4, 2.85))
    fig.suptitle('The gravitational potential well', fontsize=8.2, color=INK, style='italic', y=0.98)
    ax = plain_axes(fig, [0.12, 0.12, 0.62, 0.76])
    r = np.linspace(0.18, 4.0, 300)
    U = -1/r
    ax.plot(r, U, color=PLUM, lw=2.0, zorder=3)
    ax.axhline(0, color=INK, lw=0.8)
    Eb = -0.45
    for E, col, ls in ((0.35, PRIM, (0, (5, 3))), (0.0, FOR, '-'), (Eb, CRIM, (0, (5, 3)))):
        if E != 0.0:
            ax.plot([0.18, 4.0], [E, E], color=col, lw=1.4, ls=ls)
    rt = -1/Eb
    ax.plot(rt, Eb, 'o', color=CRIM, ms=4.5, zorder=5)
    ax.annotate('turning point', xy=(rt, Eb), xytext=(rt + 0.35, Eb - 0.55), fontsize=7.4, color=CRIM,
                arrowprops=dict(arrowstyle='-', color=CRIM, lw=0.7))
    ax.text(1.45, -1.25, r'$U=-\dfrac{GMm}{r}$', color=PLUM, fontsize=9.0)
    ax.set_xlim(0, 4.0); ax.set_ylim(-2.4, 0.75)
    ax.set_xlabel('$r$', fontsize=8.6, color=INK)
    ax.set_ylabel('energy', fontsize=8.0, color=INK)
    # legend-style labels in the right margin, aligned with each line
    for E, col, txt in ((0.35, PRIM, '$E>0$: escapes\nwith speed to spare'),
                        (0.0, FOR, '$E=0$: just escapes'),
                        (Eb, CRIM, '$E<0$: bound;\ncannot pass the\nturning point')):
        fig.text(0.76, 0.12 + 0.76*(E + 2.4)/3.15, txt, color=col, fontsize=7.4, va='center')
    save(fig, f'{OUT}/grav_well.pdf')


# ---------------------------------------------------------------- grav_cannon
def grav_cannon():
    fig, ax = newax(3.7, 3.3)
    title(ax, "Newton's cannon")
    R = 1.0; GM = 0.62; h0 = 1.32
    ax.add_patch(Circle((0, 0), R, fc='#BFD3E6', ec=INK, lw=1.3, zorder=2))
    lab(ax, 0, -0.08, 'Earth', fs=8.2, z=4)
    # a (much exaggerated) mountain carrying the cannon
    ax.add_patch(Polygon([(-0.22, R - 0.02), (0.0, h0), (0.22, R - 0.02)], closed=True,
                         fc='#9AA8B6', ec=INK, lw=1.0, zorder=3))
    ax.add_patch(Rectangle((-0.04, h0 - 0.01), 0.16, 0.05, fc=INK, ec='none', zorder=6))
    def traj(v0, tmax=40.0, dt=0.002):
        x, y, vx, vy = 0.0, h0, v0, 0.0; X = [x]; Y = [y]
        for _ in range(int(tmax/dt)):
            r = np.hypot(x, y)
            if r < R: break
            vx += -GM*x/r**3*dt; vy += -GM*y/r**3*dt; x += vx*dt; y += vy*dt
            X.append(x); Y.append(y)
            if len(X) > 2 and np.hypot(X[-1]-X[0], Y[-1]-Y[0]) < 0.01 and len(X) > 500: break
        return np.array(X), np.array(Y)
    vc = np.sqrt(GM/h0)
    for v0, col in ((0.40, ACC), (0.56, CRIM)):
        X, Y = traj(v0); ax.plot(X, Y, color=col, lw=1.6, zorder=4)
    ph = np.linspace(0, 2*np.pi, 300)
    ax.plot(h0*np.cos(ph), h0*np.sin(ph), color=PLUM, lw=1.6, ls=(0, (5, 3)), zorder=3)
    X, Y = traj(np.sqrt(2)*vc*1.02, tmax=3.2); ax.plot(X, Y, color=FOR, lw=1.6, zorder=4)
    ax.plot([1.40, 0.92], [-0.14, 0.42], color=CRIM, lw=0.6)
    lab(ax, 1.44, -0.22, 'too slow:', c=CRIM, fs=7.6, ha='left')
    lab(ax, 1.44, -0.40, 'falls back', c=CRIM, fs=7.6, ha='left')
    lab(ax, -1.40, -1.10, r'$v=\sqrt{GM/r}$: orbit', c=PLUM, fs=7.6, ha='right')
    ax.plot([-1.36, -0.98], [-1.04, -0.86], color=PLUM, lw=0.6)
    lab(ax, 1.55, 1.98, r'$v=\sqrt{2GM/r}$: escapes', c=FOR, fs=7.6, ha='left')
    lab(ax, 0, -1.62, 'an orbit is a fall that never lands', fs=8.0)
    ax.set_xlim(-2.6, 3.4); ax.set_ylim(-1.8, 2.2)
    save(fig, f'{OUT}/grav_cannon.pdf')


# --------------------------------------------------------------- kepler_areas
def kepler_areas():
    fig, ax = newax(4.6, 2.85)
    title(ax, "Kepler's area law")
    a, e = 1.8, 0.62
    b = a*np.sqrt(1 - e**2); c = a*e
    th = np.linspace(0, 2*np.pi, 400)
    ax.plot(a*np.cos(th), b*np.sin(th), color=PRIM, lw=1.8, zorder=3)
    S = np.array([c, 0.0])
    def pt(E): return np.array([a*np.cos(E), b*np.sin(E)])
    # two sectors of equal area (eccentric anomaly ranges giving equal M)
    from scipy.optimize import brentq
    M = lambda E: E - e*np.sin(E)
    dM = 0.55
    E1a = brentq(lambda E: M(E) - (np.pi - dM/2), 0, 2*np.pi); E1b = brentq(lambda E: M(E) - (np.pi + dM/2), 0, 2*np.pi)
    E2a = brentq(lambda E: M(E) - (-dM/2 + 2*np.pi), 0, 2*np.pi + 1) - 2*np.pi; E2b = brentq(lambda E: M(E) - dM/2, -1, 1)
    for Ea, Eb, col in ((E1a, E1b, FOR), (E2a, E2b, CRIM)):
        Es = np.linspace(Ea, Eb, 80)
        poly = [tuple(S)] + [tuple(pt(E)) for E in Es]
        ax.add_patch(Polygon(poly, closed=True, fc=col, ec='none', alpha=0.28, zorder=2))
    ax.add_patch(Circle(S, 0.11, fc=AMBER, ec=ACC, lw=1.0, zorder=5))
    lab(ax, c, -0.30, 'Sun', fs=8.0, z=6)
    lab(ax, -a - 0.12, 0.62, 'aphelion:', c=FOR, fs=8.0, ha='right')
    lab(ax, -a - 0.12, 0.40, 'slow, long sweep', c=FOR, fs=7.6, ha='right')
    lab(ax, a + 0.12, 0.62, 'perihelion:', c=CRIM, fs=8.0, ha='left')
    lab(ax, a + 0.12, 0.40, 'fast, short arc', c=CRIM, fs=7.6, ha='left')
    lab(ax, 0, -b - 0.42, r'equal areas in equal times $\Leftrightarrow$ angular momentum is conserved', fs=8.0)
    ax.set_xlim(-a - 1.45, a + 1.45); ax.set_ylim(-b - 0.65, b + 0.25)
    save(fig, f'{OUT}/kepler_areas.pdf')


# --------------------------------------------------------------- orbit_energy
def orbit_energy():
    fig = plt.figure(figsize=(3.9, 3.0))
    fig.suptitle('Higher orbit: more energy, LESS speed', fontsize=8.2, color=INK, style='italic', y=0.98)
    r = np.linspace(1.0, 4.0, 200)
    ax1 = plain_axes(fig, [0.14, 0.56, 0.82, 0.32])
    ax1.plot(r, 1/np.sqrt(r), color=FOR, lw=2.0)
    ax1.set_ylabel('speed $v$', fontsize=7.6, color=INK)
    ax1.text(2.55, 0.80, r'$v=\sqrt{GM/r}$ falls', color=FOR, fontsize=8.0)
    ax1.set_xlim(1, 4); ax1.set_ylim(0.4, 1.08)
    ax2 = plain_axes(fig, [0.14, 0.13, 0.82, 0.36])
    ax2.plot(r, -1/(2*r), color=PLUM, lw=2.0)
    ax2.axhline(0, color=GREY, lw=0.7, ls=(0, (3, 3)))
    ax2.set_ylabel('energy $E$', fontsize=7.6, color=INK)
    ax2.text(1.85, -0.40, r'$E=-GMm/2r$ rises toward $0$', color=PLUM, fontsize=8.0)
    ax2.set_xlim(1, 4); ax2.set_ylim(-0.55, 0.05)
    ax2.set_xlabel('orbit radius $r$', fontsize=8.0, color=INK)
    save(fig, f'{OUT}/orbit_energy.pdf')


# ---------------------------------------------------------------- torque_door
def torque_door():
    fig, ax = newax(4.6, 2.5)
    title(ax, 'Why door handles are fitted far from the hinge')
    W, H = 3.2, 1.1
    ax.add_patch(Rectangle((0, 0), W, H, fc='#CFE3E3', ec=STEEL, lw=1.0, zorder=1))
    ax.plot([0, 0], [-0.08, H + 0.08], color=CRIM, lw=3.0, zorder=3)
    for yy in (0.15, 0.55, 0.95):
        ax.plot([-0.12, 0], [yy, yy], color=INK, lw=2.0, zorder=3)
    lab(ax, -0.22, H/2, 'hinge', c=CRIM, fs=7.8, ha='right', rot=90)
    # best: at the edge, perpendicular
    arr(ax, W, 0.70, W, 1.65, c=FOR, lw=1.8)
    lab(ax, W + 0.10, 1.48, r'best: large $r$, $\theta=90^\circ$', c=FOR, fs=7.8, ha='left')
    # at the hinge
    arr(ax, 0.18, 0.80, 0.18, 1.35, c=CRIM, lw=1.4)
    lab(ax, 0.30, 1.22, r'at the hinge: $r=0$, $\tau=0$', c=CRIM, fs=7.6, ha='left')
    # along the door
    arr(ax, 2.50, 0.32, 1.40, 0.32, c=ACC, lw=1.5)
    lab(ax, 1.95, 0.12, r'along the door: $\theta=0$, $\tau=0$', c=ACC, fs=7.6)
    darr(ax, 0.0, -0.34, W, -0.34)
    lab(ax, W/2, -0.54, r'$r$', c=STEEL, fs=8.4)
    lab(ax, W/2, -0.92, r'$\tau=rF\sin\theta$: a force must MISS the axis to turn it', fs=8.2)
    ax.set_xlim(-0.55, W + 2.15); ax.set_ylim(-1.12, 1.95)
    save(fig, f'{OUT}/torque_door.pdf')


# ----------------------------------------------------------------------- lami
def lami():
    fig, ax = newax(5.2, 2.6)
    O = np.array([0.0, 0.0])
    ang = [90, 215, 330]                    # directions of F1, F2, F3
    mag = [1.0, 0.0, 0.0]
    # choose magnitudes that close: solve F2, F3 given F1 = 1
    u = [np.array([np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a))]) for a in ang]
    A = np.column_stack([u[1], u[2]]); bvec = -u[0]
    f2, f3 = np.linalg.solve(A, bvec)
    F = [1.0*u[0], f2*u[1], f3*u[2]]
    cols = [PRIM, FOR, CRIM]
    names = [r'$\vec{F}_1$', r'$\vec{F}_2$', r'$\vec{F}_3$']
    lab(ax, 0, 1.55, 'Three concurrent forces in equilibrium', fs=7.8, style='italic')
    for Fi, c, nm in zip(F, cols, names):
        arr(ax, 0, 0, Fi[0], Fi[1], c=c, lw=1.7)
        lab(ax, 1.16*Fi[0], 1.16*Fi[1], nm, c=c, fs=8.6)
    # angles opposite each force (between the other two)
    ax.add_patch(Arc(O, 0.42, 0.42, theta1=215, theta2=330, color=INK, lw=0.9))
    lab(ax, 0.0, -0.32, r'$\alpha$', fs=8.2)
    ax.add_patch(Arc(O, 0.55, 0.55, theta1=-30, theta2=90, color=INK, lw=0.9))
    lab(ax, 0.30, 0.22, r'$\beta$', fs=8.2)
    ax.add_patch(Arc(O, 0.55, 0.55, theta1=90, theta2=215, color=INK, lw=0.9))
    lab(ax, -0.32, 0.20, r'$\gamma$', fs=8.2)
    ax.add_patch(Circle(O, 0.04, fc=INK, ec='none', zorder=6))
    # head-to-tail triangle
    P0 = np.array([3.0, -0.6])
    P1 = P0 + F[0]; P2 = P1 + F[1]
    lab(ax, 3.15, 1.55, 'Head to tail, they close', fs=7.8, style='italic')
    for a_, b_, c, nm, off in ((P0, P1, PRIM, names[0], (0.18, 0.0)),
                               (P1, P2, FOR, names[1], (-0.16, 0.16)),
                               (P2, P0, CRIM, names[2], (0.05, -0.20))):
        arr(ax, a_[0], a_[1], b_[0], b_[1], c=c, lw=1.7)
        m = (a_ + b_)/2
        lab(ax, m[0] + off[0], m[1] + off[1], nm, c=c, fs=8.6)
    lab(ax, 3.05, -1.05, r'$\dfrac{F_1}{\sin\alpha}=\dfrac{F_2}{\sin\beta}=\dfrac{F_3}{\sin\gamma}$', fs=8.8)
    ax.set_xlim(-1.35, 4.35); ax.set_ylim(-1.4, 1.75)
    save(fig, f'{OUT}/lami.pdf')


# ---------------------------------------------------------------- cd_offsetarm
def cd_offsetarm():
    fig, ax = newax(3.9, 2.9)
    title(ax, 'Offset arm: watch the radius')
    ax.plot([0, 0], [-1.25, 1.35], color=INK, lw=2.0, ls=(0, (6, 4)), zorder=1)
    lab(ax, -0.12, 1.20, 'axis', fs=7.8, ha='right')
    a = 0.55; l = 1.5; th = np.deg2rad(42)
    ax.plot([0, a], [1.0, 1.0], color=INK, lw=2.4, zorder=3)
    darr(ax, 0, 1.18, a, 1.18, c=PRIM)
    lab(ax, a/2, 1.36, r'$a$', c=PRIM, fs=8.4)
    B = np.array([a + l*np.sin(th), 1.0 - l*np.cos(th)])
    ax.plot([a, B[0]], [1.0, B[1]], color=INK, lw=1.2, zorder=3)
    ax.plot([a, a], [1.0, 0.25], color=GREY, lw=0.7, ls=(0, (3, 3)))
    ax.add_patch(Arc((a, 1.0), 0.55, 0.55, theta1=270, theta2=270 + 42, color=PLUM, lw=1.0))
    lab(ax, a + 0.08, 0.60, r'$\theta$', c=PLUM, fs=8.2)
    ax.add_patch(Circle(B, 0.11, fc=TEAL, ec=INK, lw=0.9, zorder=5))
    lab(ax, (a + B[0])/2 + 0.14, (1.0 + B[1])/2 + 0.06, r'$l$', fs=8.4)
    darr(ax, 0, B[1] - 0.32, B[0], B[1] - 0.32, c=CRIM)
    lab(ax, B[0]/2, B[1] - 0.52, r'$r=a+l\sin\theta$', c=CRIM, fs=8.4)
    lab(ax, B[0] + 0.30, B[1] + 0.48, r'$\tan\theta=\dfrac{r\omega^{2}}{g}$', fs=8.2, ha='left')
    lab(ax, 0.95, -1.12, r'NOT $l\sin\theta$ alone', c=CRIM, fs=7.8)
    ax.set_xlim(-0.75, 2.75); ax.set_ylim(-1.32, 1.55)
    save(fig, f'{OUT}/cd_offsetarm.pdf')


if __name__ == '__main__':
    grav_universal(); grav_shell(); grav_well(); grav_cannon(); kepler_areas(); orbit_energy()
    torque_door(); lami(); cd_offsetarm()
    print('redrew 9')
