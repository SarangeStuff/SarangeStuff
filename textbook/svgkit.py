"""A tiny SVG builder for to-scale mechanism and vector-polygon drawings.

World coordinates are y-up (metres, or m/s, or m/s^2); the builder converts
them to screen pixels with a fixed pixels-per-unit (ppu) and works out the
viewBox from everything drawn. Colours come from CSS classes, so the page's
light/dark tokens apply:  abs (absolute, known), n (normal / fully known
relative), t (perpendicular-to-bar, size unknown), ans (what we solve for),
cons (construction lines), ink, muted.
"""
import html
import math
import re

GREEK = "ωαθβρφ"
_LET = f"[A-Za-z{GREEK}]+"
_NOT = f"[^A-Za-z{GREEK}]+"


def esc(s):
    return html.escape(s, quote=True)


def fmt_label(s):
    """Mini markup: x_{sub}. Letters italic, subscripts upright and small."""
    parts = re.split(r"_\{([^}]*)\}", s)
    out, shifted = [], False
    for k, seg in enumerate(parts):
        if seg == "":
            continue
        if k % 2 == 1:
            dy = "" if shifted else ' dy="4"'
            out.append(f'<tspan{dy} font-size="0.74em">{esc(seg)}</tspan>')
            shifted = True
        else:
            for m in re.finditer(f"{_LET}|{_NOT}", seg):
                t = m.group(0)
                dy = ' dy="-4"' if shifted else ""
                shifted = False
                if re.match(_LET, t) and t not in ("rad", "mm", "m", "s", "IC", "deg"):
                    out.append(f'<tspan font-style="italic"{dy}>{esc(t)}</tspan>')
                else:
                    out.append(f"<tspan{dy}>{esc(t)}</tspan>")
    return "".join(out)


def plain_len(s):
    return len(re.sub(r"_\{([^}]*)\}", lambda m: m.group(1)[: max(1, int(len(m.group(1)) * 0.75))], s))


class Fig:
    def __init__(self, ppu=100.0, label="figure"):
        self.ppu = ppu
        self.els = []
        self.minx = self.miny = 1e9
        self.maxx = self.maxy = -1e9
        self.label = label
        self.scalebar = None

    # ---- coordinates & bbox
    def P(self, p):
        return (p[0] * self.ppu, -p[1] * self.ppu)

    def bb(self, x, y, hw=0.0, hh=0.0):
        self.minx = min(self.minx, x - hw)
        self.maxx = max(self.maxx, x + hw)
        self.miny = min(self.miny, y - hh)
        self.maxy = max(self.maxy, y + hh)

    def add(self, s, step=None):
        self.els.append((step, s))

    # ---- primitives (world coords in, px out)
    def line(self, p, q, cls="ink", step=None, w=None, dash=None):
        x1, y1 = self.P(p)
        x2, y2 = self.P(q)
        self.bb(x1, y1)
        self.bb(x2, y2)
        extra = ""
        if w:
            extra += f' stroke-width="{w}"'
        if dash:
            extra += f' stroke-dasharray="{dash}"'
        self.add(f'<line class="{cls}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"{extra}/>', step)

    def text(self, p, s, cls="ink", dx=0, dy=0, anchor="middle", step=None, size=None):
        x, y = self.P(p)
        x += dx
        y += dy
        w = plain_len(s) * 7.2
        if anchor == "middle":
            self.bb(x, y, w / 2 + 2, 9)
        elif anchor == "start":
            self.bb(x + w / 2, y, w / 2 + 2, 9)
        else:
            self.bb(x - w / 2, y, w / 2 + 2, 9)
        sz = f' font-size="{size}"' if size else ""
        self.add(
            f'<text class="lbl {cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
            f'dominant-baseline="central"{sz}>{fmt_label(s)}</text>', step)

    COMPASS = {"N": (0, -1, "middle"), "S": (0, 1, "middle"), "E": (1, 0, "start"), "W": (-1, 0, "end"),
               "NE": (0.72, -0.72, "start"), "NW": (-0.72, -0.72, "end"),
               "SE": (0.72, 0.72, "start"), "SW": (-0.72, 0.72, "end")}

    def arrow(self, p, q, cls="ink", label=None, side="l", off=13, step=None, head=10,
              lpos=0.5, ldx=0, ldy=0, w=None, dashed=False, at=None):
        if at is not None and label:
            direction, dist = at if isinstance(at, tuple) else (at, 8)
            self.arrow(p, q, cls, None, step=step, head=head, w=w, dashed=dashed)
            x1, y1 = self.P(p)
            x2, y2 = self.P(q)
            mx, my = x1 + (x2 - x1) * lpos, y1 + (y2 - y1) * lpos
            ux, uy, anchor = self.COMPASS[direction]
            tx, ty = mx + ux * dist + ldx, my + uy * dist + ldy
            wl = plain_len(label) * 7.2
            cx = tx + (wl / 2 if anchor == "start" else -wl / 2 if anchor == "end" else 0)
            self.bb(cx, ty, wl / 2 + 2, 9)
            self.add(f'<text class="lbl {cls}" x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}" '
                     f'dominant-baseline="central">{fmt_label(label)}</text>', step)
            return
        x1, y1 = self.P(p)
        x2, y2 = self.P(q)
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        self.bb(x1, y1)
        self.bb(x2, y2)
        if L < 0.5:
            return
        ux, uy = dx / L, dy / L
        h = min(head, L * 0.55)
        bx, by = x2 - ux * h, y2 - uy * h
        nx, ny = uy, -ux  # screen-left normal
        hw = h * 0.40
        sw = f' stroke-width="{w}"' if w else ""
        da = ' stroke-dasharray="5 4"' if dashed else ""
        g = (f'<g class="vec {cls}"><line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}"{sw}{da}/>'
             f'<polygon points="{x2:.1f},{y2:.1f} {bx + nx * hw:.1f},{by + ny * hw:.1f} '
             f'{bx - nx * hw:.1f},{by - ny * hw:.1f}"/></g>')
        self.add(g, step)
        if label:
            mx, my = x1 + dx * lpos, y1 + dy * lpos
            sgn = 1 if side == "l" else -1
            tx, ty = mx + sgn * nx * off + ldx, my + sgn * ny * off + ldy
            w_ = plain_len(label) * 7.2
            self.bb(tx, ty, w_ / 2 + 2, 9)
            self.add(f'<text class="lbl {cls}" x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" '
                     f'dominant-baseline="central">{fmt_label(label)}</text>', step)

    def cline(self, p, d, t0, t1, cls="cons", step=None):
        """Construction line through world point p along unit direction d, params t0..t1 (world units)."""
        a = (p[0] + d[0] * t0, p[1] + d[1] * t0)
        b = (p[0] + d[0] * t1, p[1] + d[1] * t1)
        self.line(a, b, cls, step=step)

    def dot(self, p, r=3.2, cls="dotk", step=None, label=None, ldx=8, ldy=-9, anchor="start", lcls="ink"):
        x, y = self.P(p)
        self.bb(x, y, r, r)
        self.add(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>', step)
        if label:
            self.text(p, label, lcls, dx=ldx, dy=ldy, anchor=anchor, step=step)

    def link(self, p, q, step=None, w=9):
        x1, y1 = self.P(p)
        x2, y2 = self.P(q)
        self.bb(x1, y1, w, w)
        self.bb(x2, y2, w, w)
        self.add(f'<line class="link" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="{w}"/>', step)

    def pin(self, p, r=4.2):
        x, y = self.P(p)
        self.add(f'<circle class="pin" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>')

    def hatch(self, x1, y1, x2, y2, side=1, gap=7, ln=6):
        """Line from (x1,y1) to (x2,y2) in px with hatch ticks on the screen-right side (side=1)."""
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        rx, ry = -uy * side, ux * side  # screen-right normal
        parts = [f'<line class="ground" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>']
        n = int(L // gap)
        for i in range(n + 1):
            px, py = x1 + ux * i * gap, y1 + uy * i * gap
            ex, ey = px + rx * ln - ux * ln * 0.8, py + ry * ln - uy * ln * 0.8
            parts.append(f'<line class="hatch" x1="{px:.1f}" y1="{py:.1f}" x2="{ex:.1f}" y2="{ey:.1f}"/>')
            self.bb(ex, ey)
        self.bb(x1, y1)
        self.bb(x2, y2)
        self.add("".join(parts))

    def ground(self, p, q, side=1):
        x1, y1 = self.P(p)
        x2, y2 = self.P(q)
        self.hatch(x1, y1, x2, y2, side)

    def pivot(self, p, down=True):
        """Fixed pivot: pin + triangle + hatched base. down=False hangs from a ceiling."""
        x, y = self.P(p)
        s = 1 if down else -1
        tri = f'<polygon class="support" points="{x:.1f},{y:.1f} {x - 8:.1f},{y + 13 * s:.1f} {x + 8:.1f},{y + 13 * s:.1f}"/>'
        self.add(tri)
        self.hatch(x - 12, y + 13 * s, x + 12, y + 13 * s, side=s)
        self.pin(p, 4.6)

    def slider(self, p, ang_deg, w=30, h=16, guide=70):
        x, y = self.P(p)
        a = -ang_deg  # screen rotation
        g = (f'<g transform="translate({x:.1f},{y:.1f}) rotate({a:.1f})">'
             f'<line class="guide" x1="{-guide}" y1="{-h / 2 - 2.5}" x2="{guide}" y2="{-h / 2 - 2.5}"/>'
             f'<line class="guide" x1="{-guide}" y1="{h / 2 + 2.5}" x2="{guide}" y2="{h / 2 + 2.5}"/>'
             f'<rect class="block" x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="2"/></g>')
        self.add(g)
        self.bb(x, y, guide + 2, guide * abs(math.sin(math.radians(ang_deg))) + h)
        self.pin(p, 3.6)

    def arc(self, c, rpx, a1, a2, cls="ink", label=None, lr=None, step=None, arrow=False, ccw=True, la=None, ldx=0, ldy=0):
        """Arc about world point c, radius in px, from world angle a1 to a2 (degrees)."""
        cx, cy = self.P(c)
        if ccw:
            span = (a2 - a1) % 360
        else:
            span = (a1 - a2) % 360
        sx, sy = cx + rpx * math.cos(math.radians(a1)), cy - rpx * math.sin(math.radians(a1))
        ex, ey = cx + rpx * math.cos(math.radians(a2)), cy - rpx * math.sin(math.radians(a2))
        large = 1 if span > 180 else 0
        sweep = 0 if ccw else 1
        path = f'<path class="arc {cls}" d="M{sx:.1f},{sy:.1f} A{rpx},{rpx} 0 {large} {sweep} {ex:.1f},{ey:.1f}"/>'
        self.bb(cx, cy, rpx, rpx)
        if arrow:
            # tangent direction at end (screen)
            t = math.radians(a2)
            if ccw:
                tx, ty = -math.sin(t), -math.cos(t)
            else:
                tx, ty = math.sin(t), math.cos(t)
            h = 8
            bx, by = ex - tx * h, ey - ty * h
            nx, ny = ty, -tx
            path += (f'<polygon class="archead {cls}" points="{ex:.1f},{ey:.1f} {bx + nx * 3.4:.1f},{by + ny * 3.4:.1f} '
                     f'{bx - nx * 3.4:.1f},{by - ny * 3.4:.1f}"/>')
        self.add(path, step)
        if label:
            mid = la if la is not None else (a1 + (span / 2 if ccw else -span / 2))
            r2 = lr if lr else rpx + 12
            lx = cx + r2 * math.cos(math.radians(mid)) + ldx
            ly = cy - r2 * math.sin(math.radians(mid)) + ldy
            w_ = plain_len(label) * 7.2
            self.bb(lx, ly, w_ / 2 + 2, 9)
            self.add(f'<text class="lbl {cls}" x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" '
                     f'dominant-baseline="central">{fmt_label(label)}</text>', step)

    def dim(self, p, q, label, off=16, side="l", step=None):
        """Dimension line parallel to p->q, offset by off px."""
        x1, y1 = self.P(p)
        x2, y2 = self.P(q)
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        nx, ny = (uy, -ux) if side == "l" else (-uy, ux)
        ax, ay = x1 + nx * off, y1 + ny * off
        bx, by = x2 + nx * off, y2 + ny * off
        s = (f'<g class="dim"><line x1="{x1 + nx * 4:.1f}" y1="{y1 + ny * 4:.1f}" x2="{ax + nx * 4:.1f}" y2="{ay + ny * 4:.1f}"/>'
             f'<line x1="{x2 + nx * 4:.1f}" y1="{y2 + ny * 4:.1f}" x2="{bx + nx * 4:.1f}" y2="{by + ny * 4:.1f}"/>'
             f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}"/>'
             f'<polygon points="{ax:.1f},{ay:.1f} {ax + ux * 7 + nx * 2.6:.1f},{ay + uy * 7 + ny * 2.6:.1f} {ax + ux * 7 - nx * 2.6:.1f},{ay + uy * 7 - ny * 2.6:.1f}"/>'
             f'<polygon points="{bx:.1f},{by:.1f} {bx - ux * 7 + nx * 2.6:.1f},{by - uy * 7 + ny * 2.6:.1f} {bx - ux * 7 - nx * 2.6:.1f},{by - uy * 7 - ny * 2.6:.1f}"/></g>')
        self.add(s, step)
        self.bb(ax, ay)
        self.bb(bx, by)
        tx, ty = (ax + bx) / 2 + nx * 10, (ay + by) / 2 + ny * 10
        w_ = plain_len(label) * 7.0
        self.bb(tx, ty, w_ / 2 + 2, 9)
        self.add(f'<text class="lbl dimt" x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" dominant-baseline="central">{fmt_label(label)}</text>', step)

    def circle(self, c, r_world, cls="outline", dash=None, step=None):
        x, y = self.P(c)
        r = r_world * self.ppu
        self.bb(x, y, r, r)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"{da}/>', step)

    def path_world(self, pts, cls="ink", step=None, dash=None):
        d = []
        for i, p in enumerate(pts):
            x, y = self.P(p)
            self.bb(x, y)
            d.append(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}")
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<path class="{cls}" d="{" ".join(d)}"{da}/>', step)

    def set_scalebar(self, value, label):
        self.scalebar = (value, label)

    # ---- output
    def svg(self, pad=12, extra_cls=""):
        if self.scalebar:
            v, lab = self.scalebar
            L = v * self.ppu
            y = self.maxy + 22
            x = self.minx
            s = (f'<g class="scalebar"><line x1="{x:.1f}" y1="{y:.1f}" x2="{x + L:.1f}" y2="{y:.1f}"/>'
                 f'<line x1="{x:.1f}" y1="{y - 4:.1f}" x2="{x:.1f}" y2="{y + 4:.1f}"/>'
                 f'<line x1="{x + L:.1f}" y1="{y - 4:.1f}" x2="{x + L:.1f}" y2="{y + 4:.1f}"/>'
                 f'<text class="lbl muted" x="{x + L + 8:.1f}" y="{y:.1f}" dominant-baseline="central">{esc(lab)}</text></g>')
            self.add(s)
            self.bb(x, y, 0, 6)
            self.bb(x + L + 8 + len(lab) * 7, y)
        x0, y0 = self.minx - pad, self.miny - pad
        w, h = self.maxx - self.minx + 2 * pad, self.maxy - self.miny + 2 * pad
        body = []
        for step, s in self.els:
            if step is None:
                body.append(s)
            else:
                body.append(f'<g data-step="{step}">{s}</g>')
        return (f'<svg class="fig {extra_cls}" viewBox="{x0:.0f} {y0:.0f} {w:.0f} {h:.0f}" '
                f'width="{w:.0f}" role="img" aria-label="{esc(self.label)}">' + "".join(body) + "</svg>")
