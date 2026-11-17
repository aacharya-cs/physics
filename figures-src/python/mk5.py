import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # style.py sits beside this script
import numpy as np
from matplotlib.patches import Circle, Polygon, Ellipse, Arc, FancyArrowPatch
from style import *

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figs'))  # repo-root figs/


# ---------------------------------------------------------------- thirdlaw_book
def thirdlaw_book():
    fig, ax = newax(5.6, 3.15)

    # ================= LEFT: the two forces on the book (NOT a pair)
    lab(ax, 1.75, 3.52, 'Not a third-law pair', c=CRIM, fs=8.2, weight='bold')
    lab(ax, 1.75, 3.26, 'both forces act on the SAME body', c=INK, fs=7.0, style='italic')

    ground(ax, 0.25, 3.25, 1.05, n=17, d=0.10)
    block(ax, 1.17, 1.05, 1.16, 0.44, fc='#D9E2EC')
    lab(ax, 1.75, 1.27, 'book', fs=7.2)

    arr(ax, 1.75, 1.27, 1.75, 0.42, c=CRIM, lw=1.6)
    lab(ax, 1.90, 0.60, r'$W=mg$  on book', c=CRIM, ha='left', fs=7.0)
    arr(ax, 1.75, 1.49, 1.75, 2.40, c=PRIM, lw=1.6)
    lab(ax, 1.90, 2.12, r'$N$  on book', c=PRIM, ha='left', fs=7.0)

    lab(ax, 1.75, 2.74, 'equal only because the book', c=STEEL, fs=6.8)
    lab(ax, 1.75, 2.54, 'happens to be in equilibrium', c=STEEL, fs=6.8)

    # separator
    ax.plot([3.95, 3.95], [-0.95, 3.62], color=GREY, lw=0.9, ls=(0, (4, 3)))

    # ================= RIGHT: the two genuine pairs
    lab(ax, 6.65, 3.52, 'Two genuine third-law pairs', c=FOR, fs=8.2, weight='bold')
    lab(ax, 6.65, 3.26, 'each pair acts on DIFFERENT bodies', c=INK, fs=7.0, style='italic')

    # table surface
    ax.plot([5.15, 8.15], [1.05, 1.05], color=INK, lw=1.2)
    block(ax, 6.07, 1.05, 1.16, 0.44, fc='#D9E2EC')
    lab(ax, 6.65, 1.27, 'book', fs=7.2)
    lab(ax, 8.12, 0.86, 'table', c=INK, fs=7.0, ha='right')

    # pair 1 (contact): N on book, N' on table
    arr(ax, 6.65, 1.49, 6.65, 2.32, c=PRIM, lw=1.6)
    lab(ax, 6.80, 2.06, r'$N$  on book', c=PRIM, ha='left', fs=7.0)
    arr(ax, 6.65, 1.02, 6.65, 0.30, c=PRIM, lw=1.6)
    lab(ax, 6.80, 0.52, r"$N'$  on table", c=PRIM, ha='left', fs=7.0)
    lab(ax, 5.22, 2.52, 'pair 1: contact', c=PRIM, fs=7.2, ha='left', weight='bold')

    # pair 2 (gravity): W on book (at the book), W' on Earth (at the surface)
    arr(ax, 6.25, 1.27, 6.25, 0.62, c=FOR, lw=1.6)
    lab(ax, 6.10, 0.84, r'$W$  on book', c=FOR, ha='right', fs=7.0)

    # Earth arc
    th = np.linspace(np.deg2rad(60), np.deg2rad(120), 140)
    Rg, cy = 3.9, -4.86
    ax.plot(6.65 + Rg*np.cos(th), cy + Rg*np.sin(th), color=INK, lw=1.3)
    lab(ax, 6.65, -1.14, 'Earth', c=INK, fs=7.2)
    arr(ax, 6.25, -0.92, 6.25, -0.12, c=FOR, lw=1.6, ls=(0, (3, 2)))
    lab(ax, 6.12, -0.46, r"$W'$  on Earth", c=FOR, ha='right', fs=7.0)
    lab(ax, 5.22, 2.74, 'pair 2: gravity', c=FOR, fs=7.2, ha='left', weight='bold')

    ax.set_xlim(0.05, 8.60)
    ax.set_ylim(-1.42, 3.78)
    save(fig, f'{OUT}/thirdlaw_book.pdf')


# --------------------------------------------------------- cd_threeparticles
def cd_threeparticles():
    fig, ax = newax(3.9, 3.45)
    title(ax, 'Three equal masses, each pulled toward the centroid')

    a = 2.0
    P = [np.array([0.0, 0.0]), np.array([a, 0.0]), np.array([a/2, a*np.sqrt(3)/2])]
    G = sum(P) / 3.0

    # triangle
    ax.add_patch(Polygon(P, closed=True, fc='none', ec=GREY, lw=1.0, ls=(0, (4, 3))))

    # circumscribed orbit
    R = np.linalg.norm(P[0] - G)
    ax.add_patch(Circle(G, R, fc='none', ec=PRIM, lw=1.0, alpha=0.55))

    names = ['A', 'B', 'C']
    for i, p in enumerate(P):
        halo(ax, p[0], p[1], 0.16, c=AMBER, alpha=0.25)
        ax.add_patch(Circle(p, 0.085, fc=INK, ec='none', zorder=5))

    # forces on A from B and C, plus resultant
    A = P[0]
    for other, col in ((P[1], TEAL), (P[2], TEAL)):
        u = (other - A) / np.linalg.norm(other - A)
        arr(ax, A[0], A[1], A[0] + 0.62*u[0], A[1] + 0.62*u[1], c=col, lw=1.3)
    lab(ax, 0.70, -0.16, r'$F$', c=TEAL, fs=7.6, ha='left')
    lab(ax, 0.34, 0.66, r'$F$', c=TEAL, fs=7.6)

    u = (G - A) / np.linalg.norm(G - A)
    arr(ax, A[0], A[1], A[0] + 1.02*u[0], A[1] + 1.02*u[1], c=CRIM, lw=1.7)
    lab(ax, 1.16, 0.40, r'$F_{\mathrm{net}}=\sqrt{3}\,F$', c=CRIM, fs=7.2, ha='left')

    # centroid and radius
    ax.add_patch(Circle(G, 0.055, fc=CRIM, ec='none', zorder=6))
    lab(ax, G[0] + 0.14, G[1] + 0.06, 'centroid', c=CRIM, fs=6.9, ha='left')
    ax.plot([G[0], P[2][0]], [G[1], P[2][1]], color=PRIM, lw=0.9, ls=(0, (3, 2)))
    lab(ax, G[0] - 0.12, G[1] + 0.46, r'$r=\dfrac{a}{\sqrt{3}}$', c=PRIM, fs=7.2, ha='right')

    # side label
    lab(ax, a/2, -0.33, r'side $a$', c=INK, fs=7.2)
    for i, p in enumerate(P):
        off = np.array([-0.27, -0.21]) if i == 0 else (np.array([0.27, -0.21]) if i == 1 else np.array([0.0, 0.29]))
        lab(ax, p[0] + off[0], p[1] + off[1], r'$m$', c=INK, fs=7.6, weight='bold')

    lab(ax, a/2, -0.66, r'each force $F=Gm^{2}/a^{2}$;  the two add to $\sqrt{3}F$ toward the centre',
        c=STEEL, fs=6.8)

    ax.set_xlim(-1.05, a + 1.05)
    ax.set_ylim(-0.92, a*np.sqrt(3)/2 + 0.50)
    save(fig, f'{OUT}/cd_threeparticles.pdf')


# ------------------------------------------------------------------- cmd_cone
def cmd_cone():
    fig, ax = newax(3.3, 3.5)
    title(ax, 'Slicing the cone into discs')

    R, h = 1.15, 2.5
    apex = np.array([0.0, h])

    # cone outline (apex at top, base at bottom)
    ax.plot([-R, 0.0, R], [0.0, h, 0.0], color=INK, lw=1.3, zorder=4)
    ax.add_patch(Ellipse((0, 0), 2*R, 0.42, fc='#D9E2EC', ec=INK, lw=1.2, zorder=3))
    ax.add_patch(Polygon([(-R, 0), (0, h), (R, 0)], closed=True,
                         fc='#D9E2EC', ec='none', alpha=0.45, zorder=2))

    # the slice
    z = 1.55                      # depth below apex
    y = h - z                     # height above base
    r = R * z / h
    ax.add_patch(Ellipse((0, y), 2*r, 0.36*r/R + 0.10, fc=ACC, ec=ACC,
                         lw=1.1, alpha=0.42, zorder=5))
    ax.add_patch(Ellipse((0, y + 0.13), 2*r, 0.36*r/R + 0.10, fc='none', ec=ACC,
                         lw=1.1, zorder=5))
    ax.plot([-r, -r], [y, y + 0.13], color=ACC, lw=1.1, zorder=5)
    ax.plot([r, r], [y, y + 0.13], color=ACC, lw=1.1, zorder=5)

    # axis
    ax.plot([0, 0], [-0.35, h + 0.30], color=STEEL, lw=0.8, ls=(0, (4, 3)), zorder=1)

    # z measured down from apex
    arr(ax, -1.62, h, -1.62, y, c=PRIM, lw=1.1, ms=6)
    ax.plot([-1.72, 0.0], [h, h], color=PRIM, lw=0.6, ls=(0, (2, 2)))
    ax.plot([-1.72, -r], [y, y], color=PRIM, lw=0.6, ls=(0, (2, 2)))
    lab(ax, -1.78, (h + y)/2, r'$z$', c=PRIM, fs=8.0, ha='right')

    # dz
    lab(ax, r + 0.46, y + 0.07, r'$dz$', c=ACC, fs=7.4, ha='left')
    arr(ax, r + 0.38, y + 0.30, r + 0.12, y + 0.12, c=ACC, lw=0.8, ms=5)

    # radius of slice
    arr(ax, 0, y + 0.13, r, y + 0.13, c=ACC, lw=1.0, ms=6)
    ax.plot([r, r + 0.06], [y + 0.13, y + 0.48], color=ACC, lw=0.6)
    lab(ax, r + 0.08, y + 0.52, r'$r=\dfrac{R}{h}z$', c=ACC, fs=7.4, ha='left')

    # base radius and height
    arr(ax, 0, -0.52, R, -0.52, c=STEEL, lw=0.9, ms=6)
    lab(ax, R/2, -0.72, r'$R$', c=STEEL, fs=7.4)
    darr(ax, 1.62, 0.0, 1.62, h)
    ax.plot([R, 1.72], [0, 0], color=STEEL, lw=0.6, ls=(0, (2, 2)))
    ax.plot([0, 1.72], [h, h], color=STEEL, lw=0.6, ls=(0, (2, 2)))
    lab(ax, 1.78, h/2, r'$h$', c=STEEL, fs=7.4, ha='left')

    lab(ax, 0, h + 0.46, r'$dm \propto r^{2}dz \propto z^{2}dz$', c=INK, fs=7.2)
    lab(ax, 0, -1.02, 'wide discs near the base carry most of the mass',
        c=STEEL, fs=6.8)

    ax.set_xlim(-2.25, 2.25)
    ax.set_ylim(-1.25, h + 0.75)
    save(fig, f'{OUT}/cmd_cone.pdf')


# -------------------------------------------------------------- cmd_hemisphere
def cmd_hemisphere():
    fig, ax = newax(3.45, 2.95)
    title(ax, 'Slicing the solid hemisphere into discs')

    R = 1.6
    th = np.linspace(0, np.pi, 240)
    ax.plot(R*np.cos(th), R*np.sin(th), color=INK, lw=1.3, zorder=4)
    ax.plot([-R, R], [0, 0], color=INK, lw=1.3, zorder=4)
    ax.fill_between(R*np.cos(th), 0, R*np.sin(th), color='#D9E2EC', alpha=0.55, zorder=1)

    # slice at height z
    z = 0.92
    r = np.sqrt(R**2 - z**2)
    ax.add_patch(Ellipse((0, z), 2*r, 0.30, fc=ACC, ec=ACC, lw=1.1, alpha=0.42, zorder=5))
    ax.add_patch(Ellipse((0, z + 0.14), 2*r, 0.30, fc='none', ec=ACC, lw=1.1, zorder=5))
    ax.plot([-r, -r], [z, z + 0.14], color=ACC, lw=1.1, zorder=5)
    ax.plot([r, r], [z, z + 0.14], color=ACC, lw=1.1, zorder=5)

    # axis
    ax.plot([0, 0], [-0.30, R + 0.35], color=STEEL, lw=0.8, ls=(0, (4, 3)), zorder=1)

    # z
    arr(ax, -2.05, 0.0, -2.05, z, c=PRIM, lw=1.1, ms=6)
    ax.plot([-2.15, 0], [0, 0], color=PRIM, lw=0.6, ls=(0, (2, 2)))
    ax.plot([-2.15, -r], [z, z], color=PRIM, lw=0.6, ls=(0, (2, 2)))
    lab(ax, -2.20, z/2, r'$z$', c=PRIM, fs=8.0, ha='right')

    # radius of slice
    arr(ax, 0, z + 0.14, -r, z + 0.14, c=ACC, lw=1.0, ms=6)
    ax.plot([-r/2, -r/2 - 0.22], [z + 0.14, z + 0.62], color=ACC, lw=0.6)
    lab(ax, -r/2 - 0.26, z + 0.70, r'$r=\sqrt{R^{2}-z^{2}}$', c=ACC, fs=7.2, ha='right')
    lab(ax, r + 0.42, z + 0.03, r'$dz$', c=ACC, fs=7.4, ha='left')
    arr(ax, r + 0.34, z + 0.28, r + 0.10, z + 0.12, c=ACC, lw=0.8, ms=5)

    # R to the rim
    u = np.array([np.cos(np.deg2rad(34)), np.sin(np.deg2rad(34))])
    arr(ax, 0, 0, R*u[0], R*u[1], c=STEEL, lw=1.0, ms=6)
    lab(ax, 0.62*R*u[0] + 0.14, 0.62*R*u[1] - 0.14, r'$R$', c=STEEL, fs=7.4)

    ax.add_patch(Circle((0, 0), 0.045, fc=INK, ec='none', zorder=6))
    lab(ax, -0.16, -0.22, 'O', c=INK, fs=7.2)
    lab(ax, 0, R + 0.62, r'$dm = \rho\,\pi (R^{2}-z^{2})\,dz$', c=INK, fs=7.2)

    ax.set_xlim(-2.55, 2.25)
    ax.set_ylim(-0.60, R + 0.98)
    save(fig, f'{OUT}/cmd_hemisphere.pdf')


# ------------------------------------------------------------------ moid_disc
def moid_disc():
    fig, ax = newax(3.2, 3.05)
    title(ax, 'Slicing the disc into rings')

    R = 1.5
    ax.add_patch(Circle((0, 0), R, fc='#D9E2EC', ec=INK, lw=1.3, alpha=0.65, zorder=2))

    r, dr = 0.95, 0.14
    ax.add_patch(Circle((0, 0), r + dr, fc=ACC, ec='none', alpha=0.40, zorder=3))
    ax.add_patch(Circle((0, 0), r, fc='white', ec='none', alpha=1.0, zorder=4))
    ax.add_patch(Circle((0, 0), r, fc='#D9E2EC', ec='none', alpha=0.65, zorder=4))
    ax.add_patch(Circle((0, 0), r, fc='none', ec=ACC, lw=1.1, zorder=5))
    ax.add_patch(Circle((0, 0), r + dr, fc='none', ec=ACC, lw=1.1, zorder=5))

    # axis out of the page
    ax.add_patch(Circle((0, 0), 0.105, fc='white', ec=INK, lw=1.2, zorder=7))
    ax.add_patch(Circle((0, 0), 0.034, fc=INK, ec='none', zorder=8))
    lab(ax, 0.20, 0.22, 'axis (out of page)', c=INK, fs=6.9, ha='left')

    # r and dr
    DEEP = '#A33F00'
    ang = np.deg2rad(212)
    u = np.array([np.cos(ang), np.sin(ang)])
    arr(ax, 0, 0, r*u[0], r*u[1], c=DEEP, lw=1.3, ms=7, z=9)
    lab(ax, 0.55*r*u[0] + 0.02, 0.55*r*u[1] + 0.22, r'$r$', c=DEEP, fs=8.4,
        box=True, z=10)
    arr(ax, (r + 0.03)*u[0], (r + 0.03)*u[1], (r + dr)*u[0], (r + dr)*u[1],
        c=DEEP, lw=1.0, ms=5, z=9)
    lab(ax, (r + dr + 0.34)*u[0], (r + dr + 0.30)*u[1], r'$dr$', c=DEEP, fs=7.6, z=10)

    # R
    ang2 = np.deg2rad(58)
    v = np.array([np.cos(ang2), np.sin(ang2)])
    arr(ax, 0, 0, R*v[0], R*v[1], c=STEEL, lw=1.1, ms=7, z=9)
    lab(ax, 0.72*R*v[0] + 0.20, 0.72*R*v[1] + 0.02, r'$R$', c=STEEL, fs=7.8,
        box=True, z=10)

    lab(ax, 0, -R - 0.34, r'$dm = \sigma\,(2\pi r)\,dr$', c=INK, fs=7.2)
    lab(ax, 0, -R - 0.62, r'every point of the ring is the same distance $r$ from the axis',
        c=STEEL, fs=6.8)
    lab(ax, 0, R + 0.30, r'$dI = r^{2}\,dm \;\Rightarrow\; I=\frac{1}{2}MR^{2}$',
        c=INK, fs=7.2)

    ax.set_xlim(-R - 0.75, R + 0.75)
    ax.set_ylim(-R - 0.90, R + 0.60)
    save(fig, f'{OUT}/moid_disc.pdf')


if __name__ == '__main__':
    thirdlaw_book()
    cd_threeparticles()
    cmd_cone()
    cmd_hemisphere()
    moid_disc()
    print('regenerated 5 figures')
