import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # style.py sits beside this script
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle, Arc, Ellipse, Wedge, FancyArrowPatch
from style import *

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figs'))  # repo-root figs/


# --------------------------------------------------------------- tk_derivative
def tk_derivative():
    fig, ax = plt.subplots(figsize=(5.0, 2.45))
    ax.axis('off')
    axp = fig.add_axes([0.07, 0.14, 0.86, 0.70])
    for sp in ('top', 'right'):
        axp.spines[sp].set_visible(False)
    axp.spines['left'].set_color(INK); axp.spines['bottom'].set_color(INK)
    axp.set_xticks([]); axp.set_yticks([])
    axp.set_xlabel('time $t$', fontsize=7.6, color=INK)
    axp.set_ylabel('position $s$', fontsize=7.6, color=INK)

    t = np.linspace(0, 10, 400)
    s = 0.09*t**2 + 0.9*np.sqrt(np.clip(t, 0, None)) + 1.0
    axp.plot(t, s, color=PRIM, lw=1.9, zorder=3)

    t1 = 3.0
    s1 = 0.09*t1**2 + 0.9*np.sqrt(t1) + 1.0

    # secants, shrinking
    for t2, al, lwd in ((8.6, 0.30, 1.0), (6.8, 0.55, 1.1), (5.0, 0.85, 1.2)):
        s2 = 0.09*t2**2 + 0.9*np.sqrt(t2) + 1.0
        m = (s2 - s1)/(t2 - t1)
        xs = np.array([t1 - 1.4, t2 + 0.5])
        axp.plot(xs, s1 + m*(xs - t1), color=FOR, lw=lwd, alpha=al, zorder=4)
        axp.plot([t2], [s2], 'o', ms=3.4, color=FOR, alpha=al, zorder=5)

    # tangent
    mt = 0.18*t1 + 0.45/np.sqrt(t1)
    xs = np.array([t1 - 2.2, t1 + 3.4])
    axp.plot(xs, s1 + mt*(xs - t1), color=CRIM, lw=1.7, zorder=6)
    axp.plot([t1], [s1], 'o', ms=5.0, color=CRIM, zorder=7)

    # delta construction for the widest secant
    t2 = 8.6; s2 = 0.09*t2**2 + 0.9*np.sqrt(t2) + 1.0
    axp.plot([t1, t2], [s1, s1], color=STEEL, lw=0.8, ls=(0, (3, 2)), zorder=2)
    axp.plot([t2, t2], [s1, s2], color=STEEL, lw=0.8, ls=(0, (3, 2)), zorder=2)
    axp.text((t1 + t2)/2, s1 - 0.55, r'$\Delta t$', color=STEEL, fontsize=8.0, ha='center')
    axp.text(t2 + 0.18, (s1 + s2)/2, r'$\Delta s$', color=STEEL, fontsize=8.0, ha='left')

    axp.text(6.1, 2.3, 'secant: average rate  $\\Delta s/\\Delta t$',
             color=FOR, fontsize=7.4, ha='center')
    axp.annotate('', xy=(5.4, 3.3), xytext=(6.1, 2.6),
                 arrowprops=dict(arrowstyle='-|>', color=FOR, lw=0.8))
    axp.text(1.05, 6.6, 'tangent: instantaneous rate  $ds/dt$',
             color=CRIM, fontsize=7.4, ha='left')
    axp.annotate('', xy=(2.6, 4.6), xytext=(2.3, 6.3),
                 arrowprops=dict(arrowstyle='-|>', color=CRIM, lw=0.8))
    axp.text(5.0, 0.15, 'slide the second point inward until the secant becomes the tangent',
             color=STEEL, fontsize=6.9, ha='center', style='italic')

    axp.set_xlim(0, 10.4)
    axp.set_ylim(0, 12.6)
    fig.suptitle('Average rate versus instantaneous rate',
                 fontsize=7.8, color=INK, style='italic', y=0.985)
    save(fig, f'{OUT}/tk_derivative.pdf')


# ------------------------------------------------------------ energy_pendulum
def energy_pendulum():
    fig, ax = newax(5.6, 2.55)
    title(ax, 'A pendulum trades $U$ for $K$ and back; the sum never changes')

    L = 2.0
    P = np.array([0.0, 2.35])
    amp = np.deg2rad(42)

    # pivot and support
    ax.plot([-0.95, 0.95], [2.35, 2.35], color=INK, lw=1.5)
    for i in range(11):
        xx = -0.95 + i*0.19
        ax.plot([xx, xx - 0.09], [2.35, 2.44], color=INK, lw=0.7)
    ax.add_patch(Circle(P, 0.045, fc=INK, ec='none', zorder=6))

    # swept arc
    ts = np.linspace(-amp, amp, 160)
    ax.plot(P[0] + L*np.sin(ts), P[1] - L*np.cos(ts), color=GREY, lw=0.9, ls=(0, (4, 3)))

    states = [(-amp, CRIM, 'all $U$'), (0.0, FOR, 'all $K$'), (amp, CRIM, 'all $U$')]
    for a, col, txt in states:
        B = P + np.array([L*np.sin(a), -L*np.cos(a)])
        ax.plot([P[0], B[0]], [P[1], B[1]], color=INK, lw=1.0,
                alpha=1.0 if a == 0 else 0.55)
        ax.add_patch(Circle(B, 0.135, fc=col, ec=INK, lw=0.9, zorder=6))

    # heights
    Bx = P + np.array([L*np.sin(amp), -L*np.cos(amp)])
    Blow = P + np.array([0.0, -L])
    ax.plot([-2.25, Bx[0] + 0.2], [Bx[1], Bx[1]], color=STEEL, lw=0.7, ls=(0, (2, 2)))
    ax.plot([-2.25, 0.5], [Blow[1], Blow[1]], color=STEEL, lw=0.7, ls=(0, (2, 2)))
    darr(ax, -2.05, Blow[1], -2.05, Bx[1])
    lab(ax, -2.15, (Blow[1] + Bx[1])/2, r'$h$', c=STEEL, ha='right', fs=8.0)

    # velocity at the bottom
    arr(ax, 0.18, Blow[1], 0.92, Blow[1], c=FOR, lw=1.5)
    lab(ax, 0.98, Blow[1] - 0.16, r'$v_{\max}$', c=FOR, ha='left', fs=7.4)

    lab(ax, -2.10, 1.34, 'at rest', c=CRIM, fs=7.0)
    lab(ax, -2.10, 1.15, r'$K=0$', c=CRIM, fs=7.0)
    ax.plot([-1.80, -1.42], [1.22, 0.92], color=CRIM, lw=0.6)
    lab(ax, 2.18, 1.34, 'at rest', c=CRIM, fs=7.0)
    lab(ax, 2.18, 1.15, r'$K=0$', c=CRIM, fs=7.0)
    ax.plot([1.88, 1.46], [1.22, 0.92], color=CRIM, lw=0.6)
    lab(ax, 0.10, -0.30, r'lowest point:  $U=0$,  $K=\frac{1}{2}mv_{\max}^{2}=mgh$',
        c=FOR, fs=7.2)

    # energy bars on the right
    bx = 3.05
    for i, (ttl, u, k) in enumerate((('extreme', 1.0, 0.0),
                                     ('halfway', 0.5, 0.5),
                                     ('bottom',  0.0, 1.0))):
        x = bx + i*0.95
        H = 1.45
        ax.add_patch(Rectangle((x, 0.52), 0.56, H*u, fc=PLUM, ec='none', alpha=0.80))
        ax.add_patch(Rectangle((x, 0.52 + H*u), 0.56, H*k, fc=ACC, ec='none', alpha=0.85))
        ax.add_patch(Rectangle((x, 0.52), 0.56, H, fc='none', ec=INK, lw=0.8))
        lab(ax, x + 0.28, 0.32, ttl, fs=6.8)
    lab(ax, bx + 1.51, 2.32, r'$U$', c=PLUM, fs=7.8, ha='right', weight='bold')
    lab(ax, bx + 1.73, 2.32, r'$K$', c=ACC, fs=7.8, ha='left', weight='bold')
    lab(ax, bx + 1.07, -0.30, r'total $K+U=mgh$ throughout', c=INK, fs=7.0)

    ax.set_xlim(-2.70, 6.15)
    ax.set_ylim(-0.62, 2.80)
    save(fig, f'{OUT}/energy_pendulum.pdf')


# ---------------------------------------------------------------- cm_balance
def cm_balance():
    fig, ax = newax(4.6, 1.85)
    title(ax, 'The centre of mass is the balance point')

    x1, x2 = 0.0, 4.4
    m1, m2 = 1.0, 3.0
    xc = (m1*x1 + m2*x2)/(m1 + m2)

    # plank
    ax.add_patch(Rectangle((x1 - 0.55, 0.52), (x2 - x1) + 1.10, 0.14,
                           fc='#D9E2EC', ec=INK, lw=1.0))
    # pivot
    ax.add_patch(Polygon([(xc, 0.50), (xc - 0.26, 0.04), (xc + 0.26, 0.04)],
                         closed=True, fc=CRIM, ec='none', zorder=5))
    lab(ax, xc, -0.20, r'$x_{\mathrm{cm}}$', c=CRIM, fs=8.0, weight='bold')

    # masses
    for x, m, r, col in ((x1, r'$m$', 0.26, TEAL), (x2, r'$3m$', 0.40, PLUM)):
        ax.add_patch(Circle((x, 0.66 + r), r, fc=col, ec=INK, lw=1.0, alpha=0.85, zorder=4))
        lab(ax, x, 0.66 + r, m, c='white', fs=8.2, weight='bold', z=6)

    # distance markers
    y = 1.68
    ax.plot([x1, x1], [0.95, y + 0.12], color=STEEL, lw=0.6, ls=(0, (2, 2)))
    ax.plot([xc, xc], [0.70, y + 0.12], color=STEEL, lw=0.6, ls=(0, (2, 2)))
    ax.plot([x2, x2], [1.12, y + 0.12], color=STEEL, lw=0.6, ls=(0, (2, 2)))
    darr(ax, x1, y, xc, y)
    darr(ax, xc, y, x2, y)
    lab(ax, (x1 + xc)/2, y + 0.19, r'$d_1$', c=STEEL, fs=7.6)
    lab(ax, (xc + x2)/2, y + 0.19, r'$d_2$', c=STEEL, fs=7.6)

    lab(ax, 2.2, 2.26, r'$m\,d_1 = 3m\,d_2 \;\Rightarrow\; d_1 = 3 d_2$', c=INK, fs=7.8)
    lab(ax, 2.2, -0.60,
        r'$x_{\mathrm{cm}}=\dfrac{m_1x_1+m_2x_2}{m_1+m_2}$:  it sits closer to the heavier body',
        c=STEEL, fs=7.0)

    ax.set_xlim(-1.05, 5.45)
    ax.set_ylim(-0.80, 2.52)
    save(fig, f'{OUT}/cm_balance.pdf')


# ------------------------------------------------------------------- cm_hole
def cm_hole():
    fig, ax = newax(4.8, 2.05)
    title(ax, 'A hole is just negative mass')

    R = 1.0
    # ---- left: the holed disc
    ax.add_patch(Circle((0, 0), R, fc='#D9E2EC', ec=INK, lw=1.3, zorder=2))
    ax.add_patch(Circle((-R/2, 0), R/2, fc='white', ec=INK, lw=1.1, zorder=3))
    ax.add_patch(Circle((-R/2, 0), R/2, fc=CRIM, ec=INK, lw=1.1, alpha=0.10, zorder=3))
    lab(ax, -R/2, 0, 'hole', c=CRIM, fs=7.0, z=5)
    ax.add_patch(Circle((R/6, 0), 0.055, fc=FOR, ec='none', zorder=6))
    arr(ax, R/6, -0.92, R/6, -0.12, c=FOR, lw=1.1)
    lab(ax, R/6 + 0.04, -1.12, r'new CM at $+R/6$', c=FOR, fs=7.2)
    lab(ax, 0, R + 0.26, 'the body we want', c=INK, fs=7.2)

    # equals sign
    lab(ax, 1.70, 0.0, '=', c=INK, fs=13)

    # ---- middle: full disc
    cx = 2.75
    ax.add_patch(Circle((cx, 0), R, fc='#D9E2EC', ec=INK, lw=1.3))
    ax.add_patch(Circle((cx, 0), 0.05, fc=INK, ec='none', zorder=5))
    lab(ax, cx, R + 0.26, r'full disc,  $+M$', c=INK, fs=7.2)
    lab(ax, cx, -1.12, r'CM at $0$', c=INK, fs=7.2)

    lab(ax, 4.20, 0.0, r'$+$', c=INK, fs=12)

    # ---- right: negative disc
    dx = 5.30
    ax.add_patch(Circle((dx, 0), R/2, fc=CRIM, ec=CRIM, lw=1.3, alpha=0.22))
    ax.add_patch(Circle((dx, 0), R/2, fc='none', ec=CRIM, lw=1.3, ls=(0, (4, 2))))
    ax.add_patch(Circle((dx, 0), 0.05, fc=CRIM, ec='none', zorder=5))
    lab(ax, dx, R + 0.26, r'negative disc,  $-M/4$', c=CRIM, fs=7.2)
    lab(ax, dx, -1.12, r'at $-R/2$', c=CRIM, fs=7.2)

    lab(ax, 2.70, -1.70,
        r'$x_{\mathrm{cm}}=\dfrac{M(0)+(-M/4)(-R/2)}{M-M/4}=\dfrac{R}{6}$', c=INK, fs=7.6)

    ax.set_xlim(-1.35, 6.60)
    ax.set_ylim(-2.05, 1.60)
    save(fig, f'{OUT}/cm_hole.pdf')


# -------------------------------------------------------------- rolling_forces
def rolling_forces():
    fig, ax = newax(5.4, 2.85)
    title(ax, 'Rolling down an incline: static friction acts UP the slope')

    th = np.deg2rad(24)
    Lx = 5.0
    ax.add_patch(Polygon([(0, 0), (Lx, 0), (Lx, Lx*np.tan(th))], closed=True,
                         fc='#E8EDF3', ec=INK, lw=1.3, zorder=1))
    ground(ax, -0.15, Lx + 0.15, 0.0, n=26, d=0.11)
    ax.add_patch(Arc((Lx, 0), 1.9, 1.9, theta1=180, theta2=180 + np.rad2deg(th),
                     color=PRIM, lw=1.0, zorder=3))
    lab(ax, Lx - 1.20, 0.20, r'$\theta$', c=PRIM, fs=8.4)

    Rr = 0.60
    cx = 2.55
    C = np.array([cx, (Lx - cx)*np.tan(th)])
    n = np.array([-np.sin(th), np.cos(th)])
    u = np.array([-np.cos(th), -np.sin(th)])
    O = C + Rr*n
    ax.add_patch(Circle(O, Rr, fc='#C7D8E8', ec=INK, lw=1.4, zorder=5))
    ax.add_patch(Circle(O, 0.05, fc=INK, ec='none', zorder=9))

    # spin
    ax.add_patch(Arc(O, 2*Rr*0.50, 2*Rr*0.50, theta1=200, theta2=40,
                     color=ACC, lw=1.4, zorder=8))
    arr(ax, O[0] + Rr*0.26, O[1] + Rr*0.12, O[0] + Rr*0.31, O[1] - Rr*0.04,
        c=ACC, lw=1.2, ms=6, z=9)

    # N at the contact point, outward
    arr(ax, C[0], C[1], C[0] + 1.30*n[0], C[1] + 1.30*n[1], c=PRIM, lw=1.5, z=10)
    lab(ax, C[0] + 1.44*n[0] - 0.14, C[1] + 1.44*n[1] + 0.10, r'$N$', c=PRIM, fs=8.0, ha='right')

    # f at the contact point, up the slope
    arr(ax, C[0], C[1], C[0] + 1.45*u[0], C[1] + 1.45*u[1], c=FOR, lw=2.0, z=10)
    lab(ax, C[0] + 1.52*u[0] - 0.06, C[1] + 1.52*u[1] + 0.26, r'$f$', c=FOR, fs=8.6,
        weight='bold', ha='right')

    # weight from the centre, straight down, well clear of the slope face
    arr(ax, O[0], O[1], O[0], O[1] - 1.55, c=CRIM, lw=1.6, z=10)
    lab(ax, O[0] + 0.14, O[1] - 1.42, r'$Mg$', c=CRIM, ha='left', fs=7.8)

    # acceleration, in a clear band above the slope
    d = np.array([np.cos(th), np.sin(th)])
    bx0 = O[0] + 0.55
    by0 = Lx*np.tan(th) + 0.62
    arr(ax, bx0, by0, bx0 + 1.10*d[0], by0 + 1.10*d[1], c=PLUM, lw=1.7, z=10)
    lab(ax, bx0 + 0.55, by0 + 0.48, r'$a$ (down the slope)', c=PLUM, fs=7.4, weight='bold')

    # annotation band, bottom left, clear of the triangle
    lab(ax, -0.30, Lx*np.tan(th) + 0.90, r'$\tau = fR$', c=ACC, fs=7.8, ha='left', weight='bold')
    lab(ax, -0.30, Lx*np.tan(th) + 0.64, 'friction alone spins it up', c=ACC, fs=6.9, ha='left')
    ax.plot([0.62, O[0] - Rr*0.55], [Lx*np.tan(th) + 0.78, O[1] + Rr*0.42],
            color=ACC, lw=0.6, zorder=4)

    lab(ax, 2.40, -0.72,
        r'$f$ is the only force with a moment arm about the centre, so it alone supplies the torque',
        c=STEEL, fs=6.9)
    lab(ax, 2.40, -1.18,
        r'$a=\dfrac{g\sin\theta}{1+c}$,  always less than a frictionless slide',
        c=INK, fs=7.6)

    ax.set_xlim(-0.55, Lx + 0.60)
    ax.set_ylim(-1.55, Lx*np.tan(th) + 1.60)
    save(fig, f'{OUT}/rolling_forces.pdf')


# ---------------------------------------------------------------- rolling_race
def rolling_race():
    fig, ax = newax(5.4, 2.60)
    title(ax, 'The race down the ramp, decided entirely by the shape factor $c$')

    th = np.deg2rad(19)
    Lx = 5.0
    ax.add_patch(Polygon([(0, 0), (Lx, 0), (Lx, Lx*np.tan(th))], closed=True,
                         fc='#E8EDF3', ec=INK, lw=1.3, zorder=1))
    ground(ax, -0.15, Lx + 1.05, 0.0, n=30, d=0.11)

    Rr = 0.26
    n = np.array([-np.sin(th), np.cos(th)])
    top = Lx*np.tan(th)
    bodies = [('sphere', r'$c=2/5$', FOR,  0.80, 'solid', top + 1.30),
              ('disc',   r'$c=1/2$', PRIM, 0.54, 'disc',  top + 0.90),
              ('ring',   r'$c=1$',   CRIM, 0.28, 'ring',  top + 0.50)]
    for name, ctxt, col, prog, kind, ty in bodies:
        x = Lx - prog*Lx
        O = np.array([x, (Lx - x)*np.tan(th)]) + Rr*n
        if kind == 'ring':
            ax.add_patch(Circle(O, Rr, fc='none', ec=col, lw=3.2, zorder=6))
        elif kind == 'disc':
            ax.add_patch(Circle(O, Rr, fc=col, ec=col, lw=1.4, alpha=0.35, zorder=6))
            ax.add_patch(Circle(O, Rr, fc='none', ec=col, lw=1.5, zorder=6))
        else:
            ax.add_patch(Circle(O, Rr, fc=col, ec=INK, lw=1.0, alpha=0.75, zorder=6))
        ax.plot([O[0], O[0]], [O[1] + Rr + 0.06, ty - 0.12], color=col, lw=0.6,
                ls=(0, (2, 2)), zorder=4)
        lab(ax, O[0], ty, f'{name},  {ctxt}', c=col, fs=7.2, weight='bold')

    ax.plot([Lx + 0.74, Lx + 0.74], [0.0, 0.36], color=INK, lw=1.3)
    lab(ax, Lx + 0.74, 0.52, 'finish', c=INK, fs=7.0, weight='bold')

    y0 = -0.74
    arr(ax, 0.62, y0, 4.00, y0, c=STEEL, lw=1.0)
    lab(ax, 0.52, y0, 'first', c=FOR, fs=7.4, ha='right', weight='bold')
    lab(ax, 4.12, y0, 'last', c=CRIM, fs=7.4, ha='left', weight='bold')
    lab(ax, 2.30, y0 - 0.30, 'smaller $c$ means less energy diverted into spin',
        c=STEEL, fs=6.9)
    lab(ax, 2.30, -1.64,
        r'$v=\sqrt{\dfrac{2gh}{1+c}}$:  independent of $M$ and $R$; only the shape enters',
        c=INK, fs=7.6)

    ax.set_xlim(-0.85, Lx + 1.30)
    ax.set_ylim(-2.10, top + 1.75)
    save(fig, f'{OUT}/rolling_race.pdf')


# -------------------------------------------------------------- grav_universal
def grav_universal():
    fig, ax = newax(5.6, 2.70)
    title(ax, 'The evidence for "universal": one law, two very different measurements')

    # Earth
    Re = 0.60
    E = np.array([0.0, 0.0])
    ax.add_patch(Circle(E, Re, fc='#BFD3E6', ec=INK, lw=1.3, zorder=4))
    lab(ax, 0, 0, 'Earth', fs=7.2, z=6)

    # apple at the surface
    ax.add_patch(Circle((0.0, Re + 0.17), 0.10, fc=CRIM, ec=INK, lw=0.7, zorder=6))
    arr(ax, 0.0, Re + 0.17, 0.0, Re - 0.12, c=CRIM, lw=1.3, z=7)
    lab(ax, 0.26, Re + 0.52, 'apple:  $a=g$', c=CRIM, fs=7.2, ha='left')

    # Moon orbit
    D = 4.15
    tt=np.linspace(np.deg2rad(-28), np.deg2rad(28), 160)
    ax.plot(E[0]+D*np.cos(tt), E[1]+D*np.sin(tt), color=GREY, lw=0.9, ls=(0,(5,4)), zorder=1)
    M = np.array([D, 0.0])
    ax.add_patch(Circle(M, 0.22, fc='#D9E2EC', ec=INK, lw=1.1, zorder=5))
    lab(ax, D + 0.40, 0.08, 'Moon', fs=7.2, ha='left')
    arr(ax, D - 0.24, 0.0, D - 0.86, 0.0, c=PRIM, lw=1.4, z=7)
    lab(ax, D - 0.55, -0.26, r'$a_{\mathrm{Moon}}$', c=PRIM, fs=7.2)
    arr(ax, D, 0.24, D, 0.98, c=FOR, lw=1.3, z=7)
    lab(ax, D + 0.12, 0.86, r'$v$', c=FOR, fs=7.2, ha='left')

    # distance
    ax.plot([0, 0], [-Re - 0.10, -1.10], color=STEEL, lw=0.6, ls=(0, (2, 2)))
    ax.plot([D, D], [-0.26, -1.10], color=STEEL, lw=0.6, ls=(0, (2, 2)))
    darr(ax, 0, -0.95, D, -0.95)
    lab(ax, D/2, -1.22, r'$r = 60\,R_E$', c=STEEL, fs=7.6)

    # the two numbers
    lab(ax, -1.95, 2.52, 'From dropping things', c=CRIM, fs=7.4, ha='left', weight='bold')
    lab(ax, -1.95, 2.10, r'$g = 9.8\ \mathrm{m/s^{2}}$', c=CRIM, fs=7.6, ha='left')
    lab(ax, 2.35, 2.52, "From the Moon's period", c=PRIM, fs=7.4, ha='left', weight='bold')
    lab(ax, 2.35, 1.92, r'$a_{\mathrm{Moon}}=\dfrac{4\pi^{2}r}{T^{2}}=0.0027\ \mathrm{m/s^{2}}$',
        c=PRIM, fs=7.4, ha='left')

    lab(ax, 1.45, -2.00,
        r'$\dfrac{a_{\mathrm{Moon}}}{g}=\dfrac{1}{3600}=\dfrac{1}{60^{2}}$,'
        r'   exactly as an inverse-square law requires', c=INK, fs=7.8)
    lab(ax, 1.45, -2.46,
        'nothing connects a stopwatch pointed at the sky to a falling apple unless one law runs both',
        c=STEEL, fs=6.9)

    ax.set_xlim(-2.05, 5.60)
    ax.set_ylim(-2.75, 2.80)
    save(fig, f'{OUT}/gr_universal_tmp.pdf')
    os.replace(f'{OUT}/gr_universal_tmp.pdf', f'{OUT}/grav_universal.pdf')


# ----------------------------------------------------------------- gr_evidence
def gr_evidence():
    fig, ax = newax(5.6, 2.00)
    title(ax, 'Four places where Newtonian gravity is not quite enough')

    cards = [
        ('Mercury', PLUM,  '#F3EAFB',
         r'$43^{\prime\prime}$/century', 'Newton leaves this', 'unexplained; GR', 'gets it exactly'),
        ('Light bending',      CRIM,  '#FBECEC',
         r'$1.75^{\prime\prime}$ at the limb', 'exactly TWICE the', 'Newtonian estimate', '(Eddington, 1919)'),
        ('Grav. redshift',     FOR,   '#EAF3EE',
         'clocks run slow', 'deeper in a well;', 'measured in a lab', 'tower (1959)'),
        ('GPS',                PRIM,  '#E9F1FC',
         r'$+38\,\mu$s per day', 'ignore GR and fixes', r'drift ${\sim}10$ km/day', 'within hours'),
    ]
    W, H = 1.52, 1.66
    for i, (ttl, col, bg, big, l1, l2, l3) in enumerate(cards):
        x = i*(W + 0.12)
        ax.add_patch(Rectangle((x, 0), W, H, fc=bg, ec=col, lw=1.0, zorder=2))
        ax.add_patch(Rectangle((x, H - 0.30), W, 0.30, fc=col, ec=col, lw=1.0, zorder=3))
        lab(ax, x + W/2, H - 0.16, ttl, c='white', fs=7.0, weight='bold', z=5)
        lab(ax, x + W/2, H - 0.62, big, c=col, fs=7.2, weight='bold', z=5)
        for j, s in enumerate((l1, l2, l3)):
            lab(ax, x + W/2, H - 0.98 - j*0.22, s, c=INK, fs=6.5, z=5)

    ax.set_xlim(-0.14, 4*(W + 0.12) + 0.02)
    ax.set_ylim(-0.14, H + 0.16)
    save(fig, f'{OUT}/gr_evidence.pdf')


# -------------------------------------------------------------- cm_curvilinear
def cm_curvilinear():
    fig, ax = newax(5.2, 2.65)
    title(ax, r'On any curved path, resolve $\vec{a}$ along and across $\vec{v}$')

    t = np.linspace(-1.35, 1.45, 400)
    X = t*2.0
    Y = 0.62*np.cos(t*1.25) + 0.38*t
    ax.plot(X, Y, color=PLUM, lw=2.0, zorder=3)

    i0 = 215
    P = np.array([X[i0], Y[i0]])
    dX = np.gradient(X); dY = np.gradient(Y)
    tang = np.array([dX[i0], dY[i0]]); tang = tang/np.linalg.norm(tang)
    nrm = np.array([-tang[1], tang[0]])
    # make the normal point to the concave side
    d2 = np.array([np.gradient(dX)[i0], np.gradient(dY)[i0]])
    if np.dot(nrm, d2) < 0: nrm = -nrm

    Rc = 1.30
    Ctr = P + Rc*nrm
    ph = np.linspace(0, 2*np.pi, 240)
    ax.plot(Ctr[0] + Rc*np.cos(ph), Ctr[1] + Rc*np.sin(ph),
            color=GREY, lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax.plot([P[0], Ctr[0]], [P[1], Ctr[1]], color=ACC, lw=0.9, ls=(0, (3, 2)), zorder=2)
    ax.add_patch(Circle(Ctr, 0.055, fc=ACC, ec='none', zorder=5))
    lab(ax, Ctr[0] + 0.14, Ctr[1] - 0.16, 'centre of curvature', c=ACC, fs=6.9, ha='left')
    lab(ax, P[0] + 0.72*Rc*nrm[0] + 0.20, P[1] + 0.72*Rc*nrm[1], r'$R$', c=ACC, fs=7.8)

    # v
    arr(ax, P[0], P[1], P[0] + 0.95*tang[0], P[1] + 0.95*tang[1], c=FOR, lw=1.6, z=6)
    lab(ax, P[0] + 1.02*tang[0], P[1] + 1.02*tang[1] + 0.14, r'$\vec{v}$', c=FOR, fs=8.0)

    # a and its two components
    at, an = 0.62, 0.78
    A = at*tang + an*nrm
    arr(ax, P[0], P[1], P[0] + A[0], P[1] + A[1], c=CRIM, lw=1.8, z=7)
    lab(ax, P[0] + A[0] + 0.16, P[1] + A[1] + 0.06, r'$\vec{a}$', c=CRIM, fs=8.4)
    arr(ax, P[0], P[1], P[0] + at*tang[0], P[1] + at*tang[1], c=STEEL, lw=1.3, z=6)
    lab(ax, P[0] + at*tang[0] + 0.08, P[1] + at*tang[1] - 0.20, r'$a_t$', c=STEEL, fs=7.6)
    arr(ax, P[0], P[1], P[0] + an*nrm[0], P[1] + an*nrm[1], c=PRIM, lw=1.3, z=6)
    lab(ax, P[0] + an*nrm[0] - 0.22, P[1] + an*nrm[1] + 0.06, r'$a_n$', c=PRIM, fs=7.6)
    # construction lines
    ax.plot([P[0] + at*tang[0], P[0] + A[0]], [P[1] + at*tang[1], P[1] + A[1]],
            color=GREY, lw=0.7, ls=(0, (2, 2)), zorder=4)
    ax.plot([P[0] + an*nrm[0], P[0] + A[0]], [P[1] + an*nrm[1], P[1] + A[1]],
            color=GREY, lw=0.7, ls=(0, (2, 2)), zorder=4)
    ax.add_patch(Circle(P, 0.055, fc=INK, ec='none', zorder=8))

    lab(ax, -2.85, -1.88, r'$a_t=\dfrac{\vec{a}\cdot\vec{v}}{v}=a\cos\theta$',
        c=STEEL, fs=7.8, ha='left')
    lab(ax, -2.85, -2.34, 'changes the SPEED', c=STEEL, fs=7.0, ha='left')
    lab(ax, 0.75, -1.88, r'$a_n=\sqrt{a^{2}-a_t^{2}}=\dfrac{v^{2}}{R}$',
        c=PRIM, fs=7.8, ha='left')
    lab(ax, 0.75, -2.34, 'bends the PATH', c=PRIM, fs=7.0, ha='left')

    ax.set_xlim(-3.15, 3.95)
    ax.set_ylim(-2.60, 1.95)
    save(fig, f'{OUT}/cm_curvilinear.pdf')


if __name__ == '__main__':
    tk_derivative(); energy_pendulum(); cm_balance(); cm_hole()
    rolling_forces(); rolling_race(); grav_universal(); gr_evidence(); cm_curvilinear()
    print('regenerated 9 figures')
