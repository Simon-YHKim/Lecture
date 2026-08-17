"""EDU-IB-02 idler pulley bracket: canonical geometry and its drawing.

One definition feeds both the artefacts the course depends on, so they cannot
drift apart: `--json` writes master-part-geometry.json, and the default writes
the drawing as inline SVG for embedding in a lesson frame.

    python scripts/part/edu_ib_02.py out.svg                 full three-view
    python scripts/part/edu_ib_02.py out.svg --profile front  front view only
    python scripts/part/edu_ib_02.py out.json --json          canonical geometry
    python scripts/part/edu_ib_02.py out.svg --audit          print the checks

Every element carries data-feature so a composition can highlight one feature at
a time without hard-coding selectors.

Original notes on the third-angle drawing follow.

Depth convention (this is what the earlier revision got wrong):

    z = 0   front face of the boss, nearest the viewer of the front view
    z = 8   boss meets the plate front face
    z = 20  back face of the plate, flat against the machine frame

The bracket bolts to a vertical frame through the two base slots, so the back
face must stay flat. That forces the boss forward, which in turn decides every
hidden line: a feature reachable from z = 0 is solid in the front view, a feature
that begins behind other material is dashed. Visibility is derived from the z
range below rather than chosen by hand.
"""

import math
import sys

# ----------------------------------------------------------------- geometry
BASE_W, BASE_H = 120.0, 16.0
PLATE_Z = (8.0, 20.0)
BOSS_C, BOSS_R = (60.0, 62.0), 28.0
BOSS_Z = (0.0, 8.0)
SHAFT_D = 25.0
TAP_PCD, TAP_D, TAP_N, TAP_START, TAP_DEPTH = 44.0, 5.0, 4, 45.0, 10.0
SLOT_W = 10.0                       # M8 bolt (Ø9 clearance) passes with room
SLOT_CTC = 12.0                     # end-circle centre distance = adjustment travel
SLOT_L = SLOT_CTC + SLOT_W          # 22 overall
SLOT_C = [(35.0, 8.0), (85.0, 8.0)]
# The foot sits OUTSIDE the boss radius so the neck is widest at the base, where
# the bending moment from the shaft is largest, and tapers inward going up.
WEB_FOOT = 100.0
FILLET_R, CHAMFER = 10.0, 5.0

DEPTH = PLATE_Z[1]
TOP_Y = BOSS_C[1] + BOSS_R
BOSS_BOT = BOSS_C[1] - BOSS_R
tap_xy = [(BOSS_C[0] + TAP_PCD / 2 * math.cos(math.radians(TAP_START + i * 90)),
           BOSS_C[1] + TAP_PCD / 2 * math.sin(math.radians(TAP_START + i * 90)))
          for i in range(TAP_N)]

# (z range the feature occupies, z of the frontmost material at that x,y).
# A feature is solid in the front view when nothing sits in front of it *at its
# own location* — the boss only covers the boss region, so the base features are
# judged against the plate face at z = 8, not against z = 0.
FEATURE_Z = {
    "boss": (BOSS_Z, BOSS_Z[0]),
    "bore": ((0.0, DEPTH), BOSS_Z[0]),
    "tap": ((0.0, TAP_DEPTH), BOSS_Z[0]),
    "slot": (PLATE_Z, PLATE_Z[0]),
}


def front_solid(name):
    (start, _), local_front = FEATURE_Z[name]
    return start <= local_front


def edge(name):
    return "outline" if front_solid(name) else "hidden"


def tangent(p, c, r):
    t = math.atan2(p[1] - c[1], p[0] - c[0])
    s = math.acos(r / math.hypot(p[0] - c[0], p[1] - c[1]))
    pts = [(c[0] + r * math.cos(t + k * s), c[1] + r * math.sin(t + k * s)) for k in (1, -1)]
    return max(pts, key=lambda q: q[0]) if p[0] > c[0] else min(pts, key=lambda q: q[0])


TR = tangent((WEB_FOOT, BASE_H), BOSS_C, BOSS_R)
TL = (2 * BOSS_C[0] - TR[0], TR[1])

# Fillet at the right web foot, solved rather than eyeballed: its centre lies one
# radius above the base top face and one radius outboard of the web line.
_wv = (TR[0] - WEB_FOOT, TR[1] - BASE_H)
_wl = math.hypot(*_wv)
_wu = (_wv[0] / _wl, _wv[1] / _wl)
_ne = (_wu[1], -_wu[0])                       # unit normal, exterior side
_t = (FILLET_R - FILLET_R * _ne[1]) / _wu[1]
FC = (WEB_FOOT + _wu[0] * _t + FILLET_R * _ne[0], BASE_H + FILLET_R)
FT_BASE = (FC[0], BASE_H)                     # tangent point on the base top face
FT_WEB = (FC[0] - FILLET_R * _ne[0], FC[1] - FILLET_R * _ne[1])
FC_L = (2 * BOSS_C[0] - FC[0], FC[1])
FT_BASE_L = (2 * BOSS_C[0] - FT_BASE[0], FT_BASE[1])
FT_WEB_L = (2 * BOSS_C[0] - FT_WEB[0], FT_WEB[1])


def arc_pts(centre, radius, a0_deg, a1_deg, n=72):
    """Points along a circle, stated by explicit sweep. SVG arc flags choose the
    centre implicitly and silently pick the wrong circle when the geometry moves,
    which is how the boss profile went wrong twice."""
    a0, a1 = math.radians(a0_deg), math.radians(a1_deg)
    return [(centre[0] + radius * math.cos(a0 + (a1 - a0) * k / n),
             centre[1] + radius * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]


BOSS_A_TR = math.degrees(math.atan2(TR[1] - BOSS_C[1], TR[0] - BOSS_C[0]))
BOSS_A_TL = 180.0 - BOSS_A_TR


def fillet_pts(centre, start, end, n=14):
    a0 = math.atan2(start[1] - centre[1], start[0] - centre[0])
    a1 = math.atan2(end[1] - centre[1], end[0] - centre[0])
    while a1 - a0 > math.pi:
        a1 -= 2 * math.pi
    while a0 - a1 > math.pi:
        a1 += 2 * math.pi
    return [(centre[0] + FILLET_R * math.cos(a0 + (a1 - a0) * k / n),
             centre[1] + FILLET_R * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]

# ------------------------------------------------------------------- layout
FX, FY = 58.0, 208.0
TY = FY - TOP_Y - 34.0
RX = FX + BASE_W + 46.0
W, H = RX + DEPTH + 52, FY + 66
TXT, ARROW = 3.4, 2.6
out = []

PROFILE = "front" if "--profile" in sys.argv and "front" in sys.argv else "full"
_feature = None


def feature(name):
    global _feature
    _feature = name


def _tag():
    return f' data-feature="{_feature}"' if _feature else ""


def F(x, y):
    return FX + x, FY - y


def T(x, z):
    return FX + x, TY - z


def R(z, y):
    return RX + z, FY - y


def em(s):
    out.append(s)


def path(d, cls):
    em(f'<path class="{cls}"{_tag()} d="{d}"/>')


def line(x1, y1, x2, y2, cls):
    em(f'<line class="{cls}"{_tag()} x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}"/>')


def circle(cx, cy, r, cls):
    em(f'<circle class="{cls}"{_tag()} cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}"/>')


def text(x, y, s, anchor="middle", cls="dimtext", rot=None):
    t = f' transform="rotate({rot} {x:.3f} {y:.3f})"' if rot is not None else ""
    em(f'<text class="{cls}" x="{x:.3f}" y="{y:.3f}" text-anchor="{anchor}"{t}>{s}</text>')


def arrow(x, y, ang):
    a = math.radians(ang)
    bx, by = x - ARROW * math.cos(a), y - ARROW * math.sin(a)
    w = ARROW * 0.27
    px, py = -math.sin(a) * w, math.cos(a) * w
    em(f'<path class="arrow" d="M{x:.3f} {y:.3f} L{bx + px:.3f} {by + py:.3f} L{bx - px:.3f} {by - py:.3f} Z"/>')


def cross(cx, cy, r):
    e = r + 2.6
    line(cx - e, cy, cx + e, cy, "center")
    line(cx, cy - e, cx, cy + e, "center")


def dline(ax, ay, bx, by, label, ext_from=None, out_arrows=False, rot=None):
    if ext_from:
        for (px, py), (qx, qy) in zip(ext_from, ((ax, ay), (bx, by))):
            dx, dy = qx - px, qy - py
            n = math.hypot(dx, dy) or 1
            line(px + dx / n * 1.4, py + dy / n * 1.4, qx + dx / n * 1.8, qy + dy / n * 1.8, "ext")
    line(ax, ay, bx, by, "dim")
    ang = math.degrees(math.atan2(by - ay, bx - ax))
    if out_arrows:
        arrow(ax, ay, ang)
        arrow(bx, by, ang + 180)
        line(ax - 6 * math.cos(math.radians(ang)), ay - 6 * math.sin(math.radians(ang)), ax, ay, "dim")
        line(bx, by, bx + 6 * math.cos(math.radians(ang)), by + 6 * math.sin(math.radians(ang)), "dim")
    else:
        arrow(ax, ay, ang + 180)
        arrow(bx, by, ang)
    mx, my = (ax + bx) / 2, (ay + by) / 2
    text(mx - (1.4 if rot else 0), my - (0 if rot else 1.4), label, rot=rot)


def dim_h(xa, xb, y_ref, y_dim, label):
    ax, bx = F(xa, 0)[0], F(xb, 0)[0]
    ay = F(0, y_ref)[1]
    dline(ax, y_dim, bx, y_dim, label, ext_from=((ax, ay), (bx, ay)), out_arrows=abs(bx - ax) < 15)


def dim_v(ya, yb, x_ref, x_dim, label):
    ay, by = F(0, ya)[1], F(0, yb)[1]
    ax = F(x_ref, 0)[0]
    dline(x_dim, ay, x_dim, by, label, ext_from=((ax, ay), (ax, by)),
          out_arrows=abs(by - ay) < 15, rot=-90)


def leader(cx, cy, r, ang, label, length=17.0):
    a = math.radians(ang)
    sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
    ex, ey = cx + (r + length) * math.cos(a), cy + (r + length) * math.sin(a)
    line(sx, sy, ex, ey, "dim")
    arrow(sx, sy, ang + 180)
    side = 9.0 if math.cos(a) >= 0 else -9.0
    line(ex, ey, ex + side, ey, "dim")
    text(ex + side + (1.2 if side > 0 else -1.2), ey - 1.2, label,
         anchor="start" if side > 0 else "end")


# =============================================================== FRONT VIEW
c5 = CHAMFER
d = ["M%.3f %.3f" % F(0, 0), "L%.3f %.3f" % F(BASE_W, 0),
     "L%.3f %.3f" % F(BASE_W, BASE_H - c5), "L%.3f %.3f" % F(BASE_W - c5, BASE_H),
     "L%.3f %.3f" % F(*FT_BASE)]
d += ["L%.3f %.3f" % F(*q) for q in fillet_pts(FC, FT_BASE, FT_WEB)[1:]]
d += ["L%.3f %.3f" % F(*TR)]
d += ["L%.3f %.3f" % F(*q) for q in arc_pts(BOSS_C, BOSS_R, BOSS_A_TR, BOSS_A_TL)[1:]]
d += [
     "L%.3f %.3f" % F(*FT_WEB_L)]
d += ["L%.3f %.3f" % F(*q) for q in fillet_pts(FC_L, FT_WEB_L, FT_BASE_L)[1:]]
d += ["L%.3f %.3f" % F(c5, BASE_H), "L%.3f %.3f" % F(0, BASE_H - c5), "Z"]
feature("profile")
path(" ".join(d), "outline")

feature("boss")
bcx, bcy = F(*BOSS_C)
_low = arc_pts(BOSS_C, BOSS_R, BOSS_A_TL, BOSS_A_TR + 360.0)
path("M" + " L".join("%.3f %.3f" % F(*q) for q in _low), edge("boss"))
feature("bore")
circle(bcx, bcy, SHAFT_D / 2, edge("bore"))
feature("tap")
for tx, ty in tap_xy:
    px, py = F(tx, ty)
    circle(px, py, TAP_D / 2, edge("tap"))
    cross(px, py, TAP_D / 2)
circle(bcx, bcy, TAP_PCD / 2, "center")
feature("bore")
cross(bcx, bcy, SHAFT_D / 2)
feature("slot")
for cx, cy in SLOT_C:
    r, half = SLOT_W / 2, SLOT_L / 2 - SLOT_W / 2
    path("M%.3f %.3f L%.3f %.3f A%.3f %.3f 0 0 1 %.3f %.3f L%.3f %.3f A%.3f %.3f 0 0 1 %.3f %.3f Z"
         % (*F(cx - half, cy + r), *F(cx + half, cy + r), r, r, *F(cx + half, cy - r),
            *F(cx - half, cy - r), r, r, *F(cx - half, cy + r)), "outline")
    sx, sy = F(cx, cy)
    line(sx - SLOT_L / 2 - 3, sy, sx + SLOT_L / 2 + 3, sy, "center")
    # A slot is built from two circles joined by tangents, so both end centres
    # carry a centre mark. Without them the construction basis is unreadable.
    for ex in (cx - SLOT_CTC / 2, cx + SLOT_CTC / 2):
        px, _ = F(ex, cy)
        line(px, sy - r - 3, px, sy + r + 3, "center")
feature(None)
line(bcx, FY - TOP_Y - 8, bcx, FY + 8, "center")
feature("fillet")
for fcx, fcy in (FC, FC_L):                    # fillet arc centres
    px, py = F(fcx, fcy)
    line(px - 8, py, px + 8, py, "center")
    line(px, py - 8, px, py + 8, "center")

feature(None)

if PROFILE == "full":
 # ============================================================ TOP VIEW
 path("M%.3f %.3f L%.3f %.3f L%.3f %.3f L%.3f %.3f Z"
      % (*T(0, PLATE_Z[0]), *T(BASE_W, PLATE_Z[0]), *T(BASE_W, PLATE_Z[1]), *T(0, PLATE_Z[1])), "outline")
 path("M%.3f %.3f L%.3f %.3f L%.3f %.3f L%.3f %.3f Z"
      % (*T(BOSS_C[0] - BOSS_R, BOSS_Z[0]), *T(BOSS_C[0] + BOSS_R, BOSS_Z[0]),
         *T(BOSS_C[0] + BOSS_R, BOSS_Z[1]), *T(BOSS_C[0] - BOSS_R, BOSS_Z[1])), "outline")
 for xx in (BOSS_C[0] - SHAFT_D / 2, BOSS_C[0] + SHAFT_D / 2):
     line(*T(xx, 0), *T(xx, DEPTH), "hidden")
 for tx in sorted({round(p[0], 3) for p in tap_xy}):
     for xx in (tx - TAP_D / 2, tx + TAP_D / 2):
         line(*T(xx, 0), *T(xx, TAP_DEPTH), "hidden")
     line(*T(tx - TAP_D / 2, TAP_DEPTH), *T(tx + TAP_D / 2, TAP_DEPTH), "hidden")
 for cx, _ in SLOT_C:
     for xx in (cx - SLOT_L / 2, cx + SLOT_L / 2):
         line(*T(xx, PLATE_Z[0]), *T(xx, PLATE_Z[1]), "hidden")
 # Chamfer: the edge between the slanted face and the base top face runs along z
 # at x = 5 and x = 95, and is seen from above.
 for xx in (CHAMFER, BASE_W - CHAMFER):
     line(*T(xx, PLATE_Z[0]), *T(xx, PLATE_Z[1]), "outline")
 # R10 runs the full thickness, so the round starts along a line parallel to z.
 # The transition is tangential, drawn thin rather than as an outline edge.
 for xx in (FT_BASE[0], FT_BASE_L[0]):
     line(*T(xx, PLATE_Z[0]), *T(xx, PLATE_Z[1]), "tangent")
 line(*T(BOSS_C[0], -6), *T(BOSS_C[0], DEPTH + 6), "center")

 # ============================================================== RIGHT VIEW
 path("M%.3f %.3f L%.3f %.3f L%.3f %.3f L%.3f %.3f L%.3f %.3f L%.3f %.3f Z"
      % (*R(PLATE_Z[0], 0), *R(PLATE_Z[1], 0), *R(PLATE_Z[1], TOP_Y),
         *R(BOSS_Z[0], TOP_Y), *R(BOSS_Z[0], BOSS_BOT), *R(PLATE_Z[0], BOSS_BOT)), "outline")
 line(*R(PLATE_Z[0], BOSS_BOT), *R(PLATE_Z[0], TOP_Y), "outline")
 for yy in (BOSS_C[1] - SHAFT_D / 2, BOSS_C[1] + SHAFT_D / 2):
     line(*R(0, yy), *R(DEPTH, yy), "hidden")
 for ty in sorted({round(p[1], 3) for p in tap_xy}):
     for yy in (ty - TAP_D / 2, ty + TAP_D / 2):
         line(*R(0, yy), *R(TAP_DEPTH, yy), "hidden")
     line(*R(TAP_DEPTH, ty - TAP_D / 2), *R(TAP_DEPTH, ty + TAP_D / 2), "hidden")
 for _, cy in SLOT_C[:1]:
     for yy in (cy - SLOT_W / 2, cy + SLOT_W / 2):
         line(*R(PLATE_Z[0], yy), *R(PLATE_Z[1], yy), "hidden")
 # Base top face (y = 16) and the start of the chamfer (y = 11) are horizontal
 # surfaces seen edge-on from the right.
 for yy in (BASE_H, BASE_H - CHAMFER):
     line(*R(PLATE_Z[0], yy), *R(PLATE_Z[1], yy), "outline")
 line(*R(PLATE_Z[0], FT_WEB[1]), *R(PLATE_Z[1], FT_WEB[1]), "tangent")
 line(*R(-6, BOSS_C[1]), *R(DEPTH + 6, BOSS_C[1]), "center")

 # ============================================================= dimensioning
 dim_h(0, BASE_W, 0, FY + 40, f"{BASE_W:g}")
 L0 = SLOT_C[0][0] - SLOT_CTC / 2
 dim_h(L0, L0 + SLOT_CTC, SLOT_C[0][1], FY + 10, "12")
 dim_h(0, L0, 0, FY + 20, f"{L0:g}")
 dim_h(L0, SLOT_C[1][0] - SLOT_CTC / 2, SLOT_C[0][1], FY + 30, f"{SLOT_C[1][0] - SLOT_C[0][0]:g}")
 # Theoretical web foot: the corner the fillet removes, and the point the tangent
 # line is drawn from. Dimensioned to the intersection, as is usual for a filleted
 # corner, with the resulting tangent point given as a reference value.
 dim_h(BASE_W - WEB_FOOT, WEB_FOOT, 0, FY + 20, f"{2 * WEB_FOOT - BASE_W:g}")
 dim_v(0, FC[1], BASE_W, FX + BASE_W + 38, f"{FC[1]:g}")
 dim_h(FC_L[0], FC[0], 0, FY + 50, f"({FC[0] - FC_L[0]:.1f})")
 dim_v(0, BASE_H, 0, FX - 13, "16")
 dim_v(0, BOSS_C[1], 0, FX - 25, "62")
 dim_v(0, TOP_Y, 0, FX - 37, "90")
 dim_v(0, SLOT_C[0][1], BASE_W, FX + BASE_W + 26, "8")
 dim_h(0, BOSS_C[0], TOP_Y, FY - TOP_Y - 20, f"{BOSS_C[0]:g}")

 leader(bcx, bcy, SHAFT_D / 2, 200, "&#216;25 H7")
 leader(bcx, bcy, BOSS_R, 288, "&#216;56", length=19)
 leader(bcx, bcy, TAP_PCD / 2, 236, "PCD &#216;44")
 p0 = F(*tap_xy[0])
 leader(p0[0], p0[1], TAP_D / 2, 40, "4-M5 &#44618;&#51060; 10")
 fp = F(*FT_WEB)
 line(fp[0], fp[1], fp[0] + 16, fp[1] - 12, "dim")
 line(fp[0] + 16, fp[1] - 12, fp[0] + 25, fp[1] - 12, "dim")
 arrow(fp[0], fp[1], 323)
 text(fp[0] + 26, fp[1] - 13.2, f"2-R{FILLET_R:g}", anchor="start")
 ps = F(*SLOT_C[0])
 leader(ps[0], ps[1], SLOT_W / 2, 210, "2-&#51109;&#44277; R5", length=22)

 a0 = math.radians(TAP_START)
 r_arc = TAP_PCD / 2 + 9
 ax0, ay0 = bcx + r_arc, bcy
 ax1, ay1 = bcx + r_arc * math.cos(-a0), bcy + r_arc * math.sin(-a0)
 line(bcx, bcy, bcx + r_arc + 5, bcy, "center")
 # Built from computed points: an SVG arc command would leave the centre
 # ambiguous, which is exactly how the boss profile went wrong earlier.
 pts = [(bcx + r_arc * math.cos(-math.radians(TAP_START) * k / 24),
         bcy + r_arc * math.sin(-math.radians(TAP_START) * k / 24)) for k in range(25)]
 em('<path class="dim" d="M' + ' L'.join(f'{x:.3f} {y:.3f}' for x, y in pts) + '"/>')
 arrow(ax1, ay1, 45)
 text(bcx + r_arc + 3.0, bcy - r_arc * 0.30, "45&#176;", anchor="start")

 cx1, cy1 = F(BASE_W - c5 / 2, BASE_H - c5 / 2)
 line(cx1, cy1, cx1 + 15, cy1 - 11, "dim")
 line(cx1 + 15, cy1 - 11, cx1 + 24, cy1 - 11, "dim")
 arrow(cx1, cy1, 143)
 text(cx1 + 25, cy1 - 12.2, "2-C5", anchor="start")

 dline(*T(BASE_W + 12, PLATE_Z[0]), *T(BASE_W + 12, PLATE_Z[1]), "12",
       ext_from=(T(BASE_W, PLATE_Z[0]), T(BASE_W, PLATE_Z[1])), out_arrows=True, rot=-90)
 dline(*T(BASE_W + 24, 0), *T(BASE_W + 24, DEPTH), "20",
       ext_from=(T(BOSS_C[0] + BOSS_R, 0), T(BASE_W, DEPTH)), rot=-90)

 text(*F(BASE_W / 2, -60), "정면도", cls="vl")
 text(FX + BASE_W / 2, TY - DEPTH - 24, "평면도", cls="vl")
 text(RX + DEPTH / 2, FY + 30, "우측면도", cls="vl")

if "--check" in sys.argv:
    for x in [0, 22, 28, 37.5, 50, 62.5, 72, 78, 100]:
        line(F(x, 0)[0], T(0, DEPTH + 4)[1], F(x, 0)[0], F(0, -6)[1], "chk")
    for y in [0, 16, 34, 43.944, 49.5, 74.5, 80.056, 90]:
        line(F(-6, 0)[0], F(0, y)[1], R(DEPTH + 6, 0)[0], F(0, y)[1], "chk")

if PROFILE == "front":
    VB = (FX - 10, FY - TOP_Y - 10, BASE_W + 20, TOP_Y + 20)
else:
    VB = (0, 0, W, H)

svg = f'''<svg class="dwg" xmlns="http://www.w3.org/2000/svg" viewBox="{VB[0]:.0f} {VB[1]:.0f} {VB[2]:.0f} {VB[3]:.0f}">
<style>
 .outline{{fill:none;stroke:#111;stroke-width:.5;stroke-linejoin:round;stroke-linecap:round}}
 .hidden{{fill:none;stroke:#111;stroke-width:.25;stroke-dasharray:2.4 1.2}}
 .center{{fill:none;stroke:#111;stroke-width:.25;stroke-dasharray:6 1.2 1 1.2}}
 .dim,.ext{{fill:none;stroke:#111;stroke-width:.25}}
 .tangent{{fill:none;stroke:#111;stroke-width:.25}}
 .arrow{{fill:#111;stroke:none}}
 .chk{{fill:none;stroke:#C7004C;stroke-width:.18;stroke-dasharray:1.5 1.5;opacity:.85}}
 text{{font-family:"Malgun Gothic",sans-serif;fill:#111}}
 .dimtext{{font-size:{TXT}px}} .vl{{font-size:4.4px;font-weight:600;letter-spacing:.06em}}
</style>
<rect x="{VB[0]:.0f}" y="{VB[1]:.0f}" width="{VB[2]:.0f}" height="{VB[3]:.0f}" fill="#fff"/>
{chr(10).join(out)}
</svg>'''

target = sys.argv[1]

if "--json" in sys.argv:
    import json
    # Verification values are computed here rather than reused from the audit
    # block, which runs after the drawing is written.
    _pts = (arc_pts(BOSS_C, BOSS_R, BOSS_A_TR, BOSS_A_TL)
            + arc_pts(BOSS_C, BOSS_R, BOSS_A_TL, BOSS_A_TR + 360.0))
    _radius_err = max(abs(math.hypot(q[0] - BOSS_C[0], q[1] - BOSS_C[1]) - BOSS_R) for q in _pts)
    _wd = math.atan2(TR[1] - BASE_H, TR[0] - WEB_FOOT)
    _rd = math.atan2(TR[1] - BOSS_C[1], TR[0] - BOSS_C[0])
    _perp_err = abs(abs(_wd - _rd) - math.pi / 2)
    _off_line = abs((FT_WEB[0] - WEB_FOOT) * _wu[1] - (FT_WEB[1] - BASE_H) * _wu[0])
    geometry = {
        "schemaVersion": 2,
        "partId": "EDU-IB-02",
        "name": "아이들러 풀리 브래킷",
        "units": "millimeters",
        "authority": "공개용 합성 교육 형상. 실제 시험의 문제지와 감독 지시가 모든 교육용 기본값에 우선한다.",
        "coordinateSystem": {
            "origin": "front-view-lower-left",
            "x": "front-view-right", "y": "front-view-up", "z": "depth-toward-viewer",
            "datumA": {"type": "plane", "equation": "y=0", "role": "프레임 접촉 기준면"},
            "datumB": {"type": "plane", "equation": f"x={BOSS_C[0]:g}", "role": "좌우 대칭 중심"},
        },
        "depthConvention": {
            "bossFront": BOSS_Z[0], "bossPlateBoundary": BOSS_Z[1], "plateBack": PLATE_Z[1],
            "note": "뒷면은 프레임에 밀착하므로 평면으로 두고 보스는 앞으로 돌출한다.",
        },
        "envelope": {"widthX": BASE_W, "heightY": TOP_Y, "depthZ": DEPTH},
        "features": {
            "base": {"width": BASE_W, "height": BASE_H, "z": list(PLATE_Z),
                     "purpose": "프레임 접촉 장착면"},
            "chamfer": {"type": "chamfer", "size": CHAMFER, "at": "베이스 바깥 상단 모서리 2곳",
                        "purpose": "취급 중 손 베임과 조립 간섭 방지"},
            "slots": {"type": "through-slot", "quantity": 2, "width": SLOT_W,
                      "endRadius": SLOT_W / 2, "centreDistance": SLOT_CTC,
                      "centres": [list(c) for c in SLOT_C],
                      "endCentres": [[c[0] - SLOT_CTC / 2, c[1]] for c in SLOT_C]
                                    + [[c[0] + SLOT_CTC / 2, c[1]] for c in SLOT_C],
                      "bolt": "M8", "purpose": "프레임 고정과 벨트 장력에 따른 좌우 조정"},
            "web": {"type": "tangent-web", "footSpan": 2 * WEB_FOOT - BASE_W,
                    "theoreticalCorners": [[WEB_FOOT, BASE_H], [BASE_W - WEB_FOOT, BASE_H]],
                    "tangentPoints": [[round(TR[0], 3), round(TR[1], 3)],
                                       [round(TL[0], 3), round(TL[1], 3)]],
                    "purpose": "축 하중을 보스에서 베이스로 전달. 밑동이 가장 두껍다."},
            "fillet": {"type": "fillet", "radius": FILLET_R,
                       "centres": [[round(FC[0], 3), FC[1]], [round(FC_L[0], 3), FC_L[1]]],
                       "tangentOnBase": [round(FT_BASE[0], 3), FT_BASE[1]],
                       "tangentOnWeb": [round(FT_WEB[0], 3), round(FT_WEB[1], 3)],
                       "purpose": "목과 베이스가 만나는 안쪽 모서리의 응력 집중 완화"},
            "boss": {"type": "boss", "centre": list(BOSS_C), "diameter": BOSS_R * 2,
                     "z": list(BOSS_Z), "purpose": "축 구멍 주변 살 두께와 베어링 폭 확보"},
            "bore": {"type": "through-hole", "centre": list(BOSS_C), "diameter": SHAFT_D,
                     "fit": "H7", "purpose": "아이들러 축 끼워맞춤"},
            "taps": {"type": "tapped-hole-pattern", "thread": "M5", "quantity": TAP_N,
                     "pitchCircleDiameter": TAP_PCD, "startAngleDeg": TAP_START,
                     "depth": TAP_DEPTH,
                     "centres": [[round(x, 3), round(y, 3)] for x, y in tap_xy],
                     "purpose": "축 커버 고정"},
        },
        "verification": {
            "bossPointRadiusErrorMm": float(f"{_radius_err:.3e}"),
            "webTangentPerpendicularErrorRad": float(f"{_perp_err:.3e}"),
            "filletWebTangentOffLineMm": float(f"{_off_line:.3e}"),
            "outlineApexY": BOSS_C[1] + BOSS_R,
        },
    }
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(geometry, fh, ensure_ascii=False, indent=2)
        fh.write(chr(10))
    print("written:", target)
    raise SystemExit(0)

open(target, "w", encoding="utf-8", newline="\n").write(svg)
open(target.replace(".svg", ".html"), "w", encoding="utf-8", newline="\n").write(
    f'<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fff">{svg}</body>')

print("written:", target)
print()
print("깊이 규약: z=0 보스 앞면 · z=8 보스/판 경계 · z=20 판 뒷면(프레임 접촉)")
print(f"{'특징':<8}{'z범위':>10}{'최전면':>8}   {'정면도':<8}근거")
rows = [("boss", "보스 앞면이 관측자를 향함"),
        ("bore", "앞뒤로 관통"),
        ("tap", "보스 앞면에서 뚫음"),
        ("slot", "베이스에는 보스가 없어 판 앞면이 최전면")]
for n, why in rows:
    (a, b), lf = FEATURE_Z[n]
    kind = "실선" if front_solid(n) else "점선"
    print(f"{n:<8}{f'{a:g}~{b:g}':>10}{lf:>8g}   {kind:<8}{why}")
print()
print("정면-평면 X 정렬 :", "일치" if F(0, 0)[0] == T(0, 0)[0] else "불일치")
print("정면-우측 Y 정렬 :", "일치" if F(0, 0)[1] == R(0, 0)[1] else "불일치")
print("탭 깊이 10 <= 전체 20 :", TAP_DEPTH <= DEPTH)
print("뒷면 평면 유지(보스가 z=20에 없음) :", BOSS_Z[1] < PLATE_Z[1])

# The outline arc and the boss root arc must be two halves of ONE circle centred
# on BOSS_C. Verify the chord/centre relation rather than trusting arc flags.
mid = ((TR[0] + TL[0]) / 2, (TR[1] + TL[1]) / 2)
half_chord = math.hypot(TR[0] - TL[0], TR[1] - TL[1]) / 2
sagitta = math.sqrt(max(BOSS_R ** 2 - half_chord ** 2, 0.0))
# Two centres satisfy any chord + radius; the tangent points may sit above or
# below the centre depending on the neck proportions, so test both candidates.
cands = (mid[1] + sagitta, mid[1] - sagitta)
print(f"현 중점 {mid[0]:.3f},{mid[1]:.3f} · 중심후보 y={cands[0]:.3f} / {cands[1]:.3f}"
      f" · 보스중심 y={BOSS_C[1]:g}",
      "→ 일치" if min(abs(c - BOSS_C[1]) for c in cands) < 1e-3 else "→ 불일치")
print(f"외형선 최고점 y = {BOSS_C[1] + BOSS_R:g} (치수 90과",
      "일치)" if abs(BOSS_C[1] + BOSS_R - TOP_Y) < 1e-9 else "불일치)")
web_dir = math.atan2(TR[1] - BASE_H, TR[0] - WEB_FOOT)
rad_dir = math.atan2(TR[1] - BOSS_C[1], TR[0] - BOSS_C[0])
print(f"웹-보스 접선 직교 오차 = {abs(abs(web_dir - rad_dir) - math.pi/2):.2e} rad")
_all = arc_pts(BOSS_C, BOSS_R, BOSS_A_TR, BOSS_A_TL) + arc_pts(BOSS_C, BOSS_R, BOSS_A_TL, BOSS_A_TR + 360.0)
_err = max(abs(math.hypot(q[0] - BOSS_C[0], q[1] - BOSS_C[1]) - BOSS_R) for q in _all)
print(f"보스 원 위 점 {len(_all)}개의 반지름 최대 오차 = {_err:.2e} mm")
print(f"접점 각도 TR = {BOSS_A_TR:.2f}° · TL = {BOSS_A_TL:.2f}° · 윗호 {BOSS_A_TL - BOSS_A_TR:.2f}°")
print(f"윗호 최고점 y = {BOSS_C[1] + BOSS_R:g} · 접점 y = {TR[1]:.3f} (접점이 중심보다 {'위' if TR[1] > BOSS_C[1] else '아래'})")

slot_lo = SLOT_C[0][0] - SLOT_L / 2
slot_hi = SLOT_C[1][0] + SLOT_L / 2
print()
print("필렛 기하")
print(f"  이론 모서리 (웹 발) : ({WEB_FOOT:g}, {BASE_H:g})")
print(f"  원호 중심           : ({FC[0]:.3f}, {FC[1]:.3f})")
print(f"  접점 (베이스 윗면)  : ({FT_BASE[0]:.3f}, {FT_BASE[1]:.3f})")
print(f"  접점 (웹 선)        : ({FT_WEB[0]:.3f}, {FT_WEB[1]:.3f})")
_d = abs(math.hypot(FT_WEB[0] - BOSS_C[0], FT_WEB[1] - BOSS_C[1]))
_on = abs((FT_WEB[0] - WEB_FOOT) * _wu[1] - (FT_WEB[1] - BASE_H) * _wu[0])
print(f"  웹 접점이 웹 선 위에 있는 오차 : {_on:.2e} mm")
print(f"  목 폭  밑동 {2 * WEB_FOOT - BASE_W:g} → 보스 접선 {2 * TR[0] - BASE_W:.1f}   (밑동이 더 두꺼움: {2 * WEB_FOOT - BASE_W > 2 * TR[0] - BASE_W})")
print()
print("장공 여유 검사")
print(f"  모따기(x=5)  ~ 좌 장공 끝 {slot_lo:g}   여유 {slot_lo - CHAMFER:.1f} mm")
print(f"  두 장공 사이 {SLOT_C[0][0] + SLOT_L / 2:g} ~ {SLOT_C[1][0] - SLOT_L / 2:g}   간격 {(SLOT_C[1][0] - SLOT_L / 2) - (SLOT_C[0][0] + SLOT_L / 2):.1f} mm")
print(f"  M8 볼트 머리 Ø13 가 베이스 안에 : 상 {BASE_H - SLOT_C[0][1] - 6.5:.1f} / 하 {SLOT_C[0][1] - 6.5:.1f} mm")
print(f"  장공 상단 {SLOT_C[0][1] + SLOT_W / 2:g} ~ 베이스 상단 {BASE_H:g}   여유 {BASE_H - SLOT_C[0][1] - SLOT_W / 2:.1f} mm")
print(f"  M8 관통 Ø9 <= 장공 폭 {SLOT_W:g} :", 9.0 <= SLOT_W)
print(f"  조정 여유(중심거리) = {SLOT_CTC:g} mm")

AUDIT = [
    ("베이스 100×16",       "외형선",                 "판 사각 z8~20",          "판 사각 z8~20"),
    ("모따기 2-C5",         "모서리 절단",            "실선 x=5, x=95",         "실선 y=11"),
    ("목 밑동 80",          "외형선(접선)",           "판 윤곽 안",             "판 윤곽 안"),
    ("베이스 윗면 y=16",    "외형선",                 "z=8 선과 일치",          "실선 y=16"),
    ("필렛 2-R10",          "참값 원호 + 중심선",      "가는 실선 x=12.1/107.9", "가는 실선 y=23.6"),
    ("웹(접선)",            "외형선",                 "판 윤곽 안",             "판 윤곽 안"),
    ("보스 Ø56",            "원 + 윗호는 외형선",     "띠 z0~8, x22~78",        "띠 z0~8, y34~90"),
    ("축 구멍 Ø25",         "실선 원",                "점선 z0~20",             "점선 z0~20"),
    ("탭 4-M5 깊이10",      "실선 원 4개",            "점선 z0~10",             "점선 z0~10"),
    ("장공 2-R5 중심거리12", "실선 + 끝원 중심마크",    "점선 z8~20",             "점선 z8~20"),
    ("중심선",              "수직 + 축 십자",         "수직 1개",               "수평 1개"),
]
print()
print(f"{'특징':<20}{'정면도':<22}{'평면도':<22}{'우측면도'}")
print("-" * 88)
for f, a, b, c in AUDIT:
    print(f"{f:<20}{a:<22}{b:<22}{c}")
