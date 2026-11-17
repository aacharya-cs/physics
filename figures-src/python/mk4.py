import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # style.py sits beside this script
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle, Arc, Ellipse, FancyArrowPatch
from style import *

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figs'))  # repo-root figs/


# --------------------------------------------------------------- lift_apparent
def lift_apparent():
    fig, ax = newax(6.4, 2.75)

    cases = [
        ('At rest or constant $v$', r'$a=0$',    0.0,  r'$N=mg$',      STEEL, 'scale reads your weight'),
        ('Accelerating up', r'$a$ upward',       1.0,  r'$N=m(g+a)$',  FOR,   'scale reads MORE'),
        ('Accelerating down', r'$a$ downward',  -1.0,  r'$N=m(g-a)$',  ACC,   'scale reads LESS'),
        ('Free fall',       r'$a=g$ downward',  -2.0,  r'$N=0$',       CRIM,  'weightless'),
    ]

    for k, (name, asub, sgn, res, col, note) in enumerate(cases):
        x = k * 3.05

        # lift cabin
        ax.add_patch(Rectangle((x + 0.25, 0.55), 2.10, 2.05, fc='none', ec=INK, lw=1.2))
        # floor / scale
        ax.add_patch(Rectangle((x + 0.95, 0.55), 0.72, 0.17, fc='#D9E2EC', ec=INK, lw=1.0))
        lab(ax, x + 1.31, 0.635, 'scale', fs=6.0)

        # person as a block
        block(ax, x + 1.02, 0.72, 0.58, 0.76, fc='#CBD7E4')
        lab(ax, x + 1.31, 1.10, 'm', fs=7.2, style='italic')

        # forces
        if sgn > -1.5:
            Nlen = {0.0: 0.86, 1.0: 1.06, -1.0: 0.52}[sgn]
            arr(ax, x + 1.31, 1.48, x + 1.31, 1.48 + Nlen, c=PRIM, lw=1.5)
            lab(ax, x + 1.44, 1.48 + Nlen - 0.16, r'$N$', c=PRIM, ha='left', fs=7.4)
        else:
            lab(ax, x + 1.31, 1.95, r'$N=0$', c=PRIM, fs=7.6, style='italic')
        arr(ax, x + 1.31, 1.10, x + 1.31, 0.14, c=CRIM, lw=1.5)
        lab(ax, x + 1.44, 0.26, r'$mg$', c=CRIM, ha='left', fs=7.4)

        # acceleration arrow outside the cabin
        if sgn != 0.0:
            y0 = 1.30
            dy = 0.62 * (1 if sgn > 0 else -1)
            arr(ax, x + 0.03, y0 - dy/2, x + 0.03, y0 + dy/2, c=col, lw=1.8)
            lab(ax, x - 0.10, y0, r'$a$', c=col, ha='right', fs=8.0, weight='bold')


        # headings and result
        lab(ax, x + 1.31, 3.14, name, c=INK, fs=7.4, weight='bold')
        lab(ax, x + 1.31, 2.92, asub, c=col, fs=7.0)
        lab(ax, x + 1.31, -0.26, res, c=col, fs=8.0, weight='bold')
        lab(ax, x + 1.31, -0.52, note, c=STEEL, fs=6.6, style='italic')

        if k < 3:
            ax.plot([x + 2.70, x + 2.70], [-0.62, 2.78], color=GREY, lw=0.8, ls=(0, (3, 3)))

    lab(ax, 5.70, 3.52, 'Only two forces act on the person; the scale reads $N$',
        c=INK, fs=7.6, style='italic')

    ax.set_xlim(-0.55, 11.95)
    ax.set_ylim(-0.80, 3.70)
    save(fig, f'{OUT}/lift_apparent.pdf')


# ------------------------------------------------------------------ springs_sp
def coil(ax, x, y0, y1, n=7, w=0.17, c=INK, lw=1.2, z=4):
    ys = np.linspace(y0, y1, 2*n + 3)
    xs = [x]
    for i in range(1, len(ys) - 1):
        xs.append(x + (w if i % 2 else -w))
    xs.append(x)
    ax.plot(xs, ys, color=c, lw=lw, zorder=z, solid_joinstyle='round')


def springs_sp():
    fig, ax = newax(5.3, 3.05)

    # ---------------- series (left)
    cx = 1.05
    ax.plot([cx - 0.85, cx + 0.85], [3.05, 3.05], color=INK, lw=1.6)
    for i in range(12):
        xx = cx - 0.85 + i * 0.155
        ax.plot([xx, xx - 0.09], [3.05, 3.14], color=INK, lw=0.7)

    coil(ax, cx, 3.05, 2.05, c=PRIM)
    lab(ax, cx + 0.40, 2.56, r'$k_1$', c=PRIM, ha='left', fs=7.8)
    ax.plot([cx, cx], [2.05, 1.88], color=INK, lw=1.1)
    ax.add_patch(Circle((cx, 1.88), 0.055, fc=INK, ec='none', zorder=6))
    coil(ax, cx, 1.88, 0.88, c=TEAL)
    lab(ax, cx + 0.40, 1.38, r'$k_2$', c=TEAL, ha='left', fs=7.8)
    block(ax, cx - 0.30, 0.42, 0.60, 0.40, fc='#D9E2EC')
    arr(ax, cx, 0.42, cx, -0.10, c=CRIM, lw=1.5)
    lab(ax, cx + 0.14, -0.02, r'$F$', c=CRIM, ha='left', fs=7.8)

    lab(ax, cx, 3.62, 'Series', c=PRIM, fs=8.6, weight='bold')
    lab(ax, cx, 3.38, 'same force, extensions add', c=INK, fs=7.0, style='italic')
    lab(ax, cx, -0.52, r'$x=x_1+x_2 \;\Rightarrow\; \frac{1}{k}=\frac{1}{k_1}+\frac{1}{k_2}$',
        c=PRIM, fs=7.6)
    lab(ax, cx, -0.92, 'combination is SOFTER', c=STEEL, fs=7.0)

    # separator
    ax.plot([2.60, 2.60], [-1.05, 3.70], color=GREY, lw=0.9, ls=(0, (4, 3)))

    # ---------------- parallel (right)
    px = 4.25
    ax.plot([px - 1.05, px + 1.05], [3.05, 3.05], color=INK, lw=1.6)
    for i in range(14):
        xx = px - 1.05 + i * 0.16
        ax.plot([xx, xx - 0.09], [3.05, 3.14], color=INK, lw=0.7)

    coil(ax, px - 0.45, 3.05, 1.35, c=PRIM)
    coil(ax, px + 0.45, 3.05, 1.35, c=TEAL)
    lab(ax, px - 0.90, 2.20, r'$k_1$', c=PRIM, ha='right', fs=7.8)
    lab(ax, px + 0.90, 2.20, r'$k_2$', c=TEAL, ha='left', fs=7.8)

    # rigid bar joining them
    ax.add_patch(Rectangle((px - 0.75, 1.20), 1.50, 0.15, fc=INK, ec='none'))
    lab(ax, px + 0.98, 1.27, 'rigid bar', c=INK, ha='left', fs=6.6)
    ax.plot([px, px], [1.20, 0.82], color=INK, lw=1.1)
    block(ax, px - 0.30, 0.42, 0.60, 0.40, fc='#D9E2EC')
    arr(ax, px, 0.42, px, -0.10, c=CRIM, lw=1.5)
    lab(ax, px + 0.14, -0.02, r'$F$', c=CRIM, ha='left', fs=7.8)

    # shared extension marker
    darr(ax, px - 1.42, 1.35, px - 1.42, 3.05)
    lab(ax, px - 1.50, 2.20, r'$x$', c=STEEL, ha='right', fs=7.8)

    lab(ax, px, 3.62, 'Parallel', c=TEAL, fs=8.6, weight='bold')
    lab(ax, px, 3.38, 'same extension, forces add', c=INK, fs=7.0, style='italic')
    lab(ax, px, -0.52, r'$F=F_1+F_2 \;\Rightarrow\; k=k_1+k_2$', c=TEAL, fs=7.6)
    lab(ax, px, -0.92, 'combination is STIFFER', c=STEEL, fs=7.0)

    ax.set_xlim(-0.35, 5.95)
    ax.set_ylim(-1.18, 3.82)
    save(fig, f'{OUT}/springs_sp.pdf')


# ---------------------------------------------------------------- cmd_semiwire
def cmd_semiwire():
    fig, ax = newax(3.6, 2.55)
    title(ax, 'Slicing the semicircular wire into arcs')

    R = 1.6
    th = np.linspace(0, np.pi, 300)
    ax.plot(R*np.cos(th), R*np.sin(th), color=INK, lw=2.4, solid_capstyle='round', zorder=3)
    ax.plot([-R - 0.25, R + 0.25], [0, 0], color=STEEL, lw=0.8, ls=(0, (4, 3)), zorder=1)
    ax.plot([0, 0], [-0.18, R + 0.30], color=STEEL, lw=0.8, ls=(0, (4, 3)), zorder=1)

    # the arc element
    t0, dt = np.deg2rad(55), np.deg2rad(11)
    ta = np.linspace(t0, t0 + dt, 40)
    ax.plot(R*np.cos(ta), R*np.sin(ta), color=ACC, lw=4.4, solid_capstyle='butt', zorder=5)
    tm = t0 + dt/2
    Pm = np.array([R*np.cos(tm), R*np.sin(tm)])

    # radius to the element and the angle
    ax.plot([0, R*np.cos(t0)], [0, R*np.sin(t0)], color=ACC, lw=0.9, ls=(0, (3, 2)), zorder=4)
    ax.plot([0, R*np.cos(t0 + dt)], [0, R*np.sin(t0 + dt)], color=ACC, lw=0.9, ls=(0, (3, 2)), zorder=4)
    ax.add_patch(Arc((0, 0), 1.25, 1.25, theta1=0, theta2=np.rad2deg(t0),
                     color=PRIM, lw=1.0, zorder=4))
    lab(ax, 0.80, 0.26, r'$\theta$', c=PRIM, fs=8.4)

    # label the element
    ax.plot([Pm[0], Pm[0] + 0.50], [Pm[1], Pm[1] + 0.42], color=ACC, lw=0.7)
    lab(ax, Pm[0] + 0.56, Pm[1] + 0.50, r'$d\ell = R\,d\theta$', c=ACC, fs=7.4, ha='left')

    # height y
    ax.plot([Pm[0], -R - 0.18], [Pm[1], Pm[1]], color=TEAL, lw=0.7, ls=(0, (2, 2)))
    arr(ax, -R - 0.42, 0, -R - 0.42, Pm[1], c=TEAL, lw=1.1, ms=6)
    lab(ax, -R - 0.52, Pm[1]/2, r'$y=R\sin\theta$', c=TEAL, fs=7.4, ha='right')

    # R
    ax.add_patch(Circle((0, 0), 0.05, fc=INK, ec='none', zorder=6))
    lab(ax, 0.12, -0.20, 'O', c=INK, fs=7.2, ha='left')
    arr(ax, 0, 0, -R*0.96, 0.0, c=STEEL, lw=0.9, ms=6, z=6)
    lab(ax, -R*0.55, 0.17, r'$R$', c=STEEL, fs=7.4)

    lab(ax, 0, R + 0.52, r'$dm = \lambda R\,d\theta$  (every element has the same mass)',
        c=INK, fs=7.2)
    lab(ax, 0, -0.56, r'sweep $\theta$ from $0$ to $\pi$ to cover the whole wire',
        c=STEEL, fs=6.9)

    ax.set_xlim(-R - 1.55, R + 1.75)
    ax.set_ylim(-0.80, R + 0.80)
    save(fig, f'{OUT}/cmd_semiwire.pdf')


# ----------------------------------------------------------- moid_hollowsphere
def moid_hollowsphere():
    fig, ax = newax(3.4, 3.0)
    title(ax, 'Slicing the spherical shell into rings')

    R = 1.5
    ph = np.linspace(0, 2*np.pi, 400)
    ax.plot(R*np.cos(ph), R*np.sin(ph), color=INK, lw=1.6, zorder=3)

    # rotation axis (vertical)
    ax.plot([0, 0], [-R - 0.50, R + 0.50], color=STEEL, lw=1.0, ls=(0, (4, 3)), zorder=1)
    lab(ax, 0.10, R + 0.62, 'axis', c=STEEL, fs=7.0, ha='left')

    # the ring at polar angle theta (measured from the axis)
    t0 = np.deg2rad(52)
    z = R*np.cos(t0)
    r = R*np.sin(t0)
    ax.add_patch(Ellipse((0, z), 2*r, 0.40*r, fc=ACC, ec=ACC, lw=1.6, alpha=0.30, zorder=5))
    ax.add_patch(Ellipse((0, z), 2*r, 0.40*r, fc='none', ec=ACC, lw=1.6, zorder=6))

    # radius line to the ring + polar angle
    ax.plot([0, r], [0, z], color=ACC, lw=1.1, zorder=6)
    ax.add_patch(Arc((0, 0), 0.92, 0.92, theta1=90 - np.rad2deg(t0), theta2=90,
                     color=PRIM, lw=1.0, zorder=6))
    lab(ax, 0.20, 0.56, r'$\theta$', c=PRIM, fs=8.4)
    lab(ax, 0.82*r + 0.12, 0.82*z - 0.14, r'$R$', c=ACC, fs=7.6, box=True, z=8)

    # r = R sin theta
    ax.plot([0, r], [z, z], color=TEAL, lw=0.0)
    arr(ax, 0, z, r, z, c=TEAL, lw=1.2, ms=7, z=8)
    lab(ax, r/2 + 0.04, z + 0.42, r'$r=R\sin\theta$', c=TEAL, fs=7.4, box=True, z=9)

    # the angular width
    t1 = t0 + np.deg2rad(9)
    ax.plot([0, R*np.sin(t1)], [0, R*np.cos(t1)], color=ACC, lw=0.8, ls=(0, (3, 2)), zorder=6)
    lab(ax, R*np.sin(t1) + 0.34, R*np.cos(t1) - 0.22, r'$d\theta$', c=ACC, fs=7.2, ha='left')

    ax.add_patch(Circle((0, 0), 0.05, fc=INK, ec='none', zorder=8))
    lab(ax, -0.12, -0.18, 'O', c=INK, fs=7.2, ha='right')

    lab(ax, 0, R + 1.02, r'$dm = \frac{M}{2}\sin\theta\,d\theta$,   $dI = r^{2}\,dm$',
        c=INK, fs=7.2)
    lab(ax, 0, -R - 0.76,
        r'$I=\int_0^{\pi} R^{2}\sin^{2}\theta\;dm = \frac{2}{3}MR^{2}$', c=INK, fs=7.4)

    ax.set_xlim(-R - 0.95, R + 1.25)
    ax.set_ylim(-R - 1.05, R + 1.25)
    save(fig, f'{OUT}/moid_hollowsphere.pdf')


if __name__ == '__main__':
    from matplotlib.patches import Ellipse
    globals()['Ellipse'] = Ellipse
    lift_apparent(); springs_sp(); cmd_semiwire(); moid_hollowsphere()
    print('regenerated 4 figures')
