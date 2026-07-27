#!/usr/bin/env python3
"""In-article illustrations for the 'Hungarian Desks' post.

Three explanatory diagrams that share the site's cover visual system (tech
indigo palette + soft grid/blob background, flat gradient vector art) but are
sized and composed for inline figures rather than cover cards:

  1. hungarian-lottery      — why first-drawn-first-served is a poor fit
  2. hungarian-bets         — how bets normalize into a 0..1 happiness score
  3. hungarian-cost-matrix  — the assignment that maximizes total happiness

No external resources; generic fonts so they render inside an <img>-referenced
SVG. Run:  python3 _tools/generate-hungarian-figures.py
"""
import math, os

OUT = "/Users/schacon/projects/scottchacon-site/assets/images"

BG0, BG1, INK = "#eef2ff", "#dbe4ff", "#1e1b4b"
A, B, C, D, E, F = "#4f46e5", "#2563eb", "#0ea5e9", "#7c3aed", "#06b6d4", "#818cf8"
ROSE, GOLD, GREEN = "#e11d48", "#f59e0b", "#10b981"


class Fig:
    def __init__(self, w, h):
        self.W, self.H = w, h
        self.defs, self.body, self._g = [], [], 0
        self._bg()

    def grad(self, c0, c1, angle=90):
        self._g += 1
        n = f"g{self._g}"
        a = math.radians(angle)
        x1, y1 = 0.5 - 0.5 * math.cos(a), 0.5 - 0.5 * math.sin(a)
        x2, y2 = 0.5 + 0.5 * math.cos(a), 0.5 + 0.5 * math.sin(a)
        self.defs.append(
            f'<linearGradient id="{n}" x1="{x1:.3f}" y1="{y1:.3f}" '
            f'x2="{x2:.3f}" y2="{y2:.3f}">'
            f'<stop offset="0" stop-color="{c0}"/>'
            f'<stop offset="1" stop-color="{c1}"/></linearGradient>')
        return f"url(#{n})"

    def rgrad(self, c0, c1):
        self._g += 1
        n = f"g{self._g}"
        self.defs.append(
            f'<radialGradient id="{n}"><stop offset="0" stop-color="{c0}"/>'
            f'<stop offset="1" stop-color="{c1}"/></radialGradient>')
        return f"url(#{n})"

    def _bg(self):
        W, H = self.W, self.H
        self.body.append(f'<rect width="{W}" height="{H}" fill="{self.grad(BG0, BG1, 120)}"/>')
        g = []
        for x in range(100, W, 100):
            g.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>')
        for y in range(100, H, 100):
            g.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
        self.body.append(f'<g stroke="{INK}" stroke-width="1" opacity="0.05">' + "".join(g) + "</g>")
        self.body.append(f'<circle cx="{int(W*0.2)}" cy="{int(H*0.22)}" r="{int(H*0.5)}" '
                         f'fill="{self.rgrad(A, BG1)}" opacity="0.12"/>')
        self.body.append(f'<circle cx="{int(W*0.85)}" cy="{int(H*0.85)}" r="{int(H*0.55)}" '
                         f'fill="{self.rgrad(D, BG1)}" opacity="0.10"/>')

    # ---- primitives ----
    def add(self, s): self.body.append(s)

    def rrect(self, x, y, w, h, r, fill, **kw):
        extra = "".join(f' {k.replace("_","-")}="{v}"' for k, v in kw.items())
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
                 f'rx="{r:.1f}" fill="{fill}"{extra}/>')

    def rect(self, x, y, w, h, fill, **kw):
        extra = "".join(f' {k.replace("_","-")}="{v}"' for k, v in kw.items())
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{extra}/>')

    def circle(self, cx, cy, r, fill, **kw):
        extra = "".join(f' {k.replace("_","-")}="{v}"' for k, v in kw.items())
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"{extra}/>')

    def line(self, x1, y1, x2, y2, stroke, sw=6, dash=None, cap="round", **kw):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        extra = "".join(f' {k.replace("_","-")}="{v}"' for k, v in kw.items())
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{d}{extra}/>')

    def path(self, d, stroke=None, fill="none", sw=6, **kw):
        s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ""
        extra = "".join(f' {k.replace("_","-")}="{v}"' for k, v in kw.items())
        self.add(f'<path d="{d}" fill="{fill}"{s}{extra}/>')

    def text(self, x, y, s, size, fill, family="Georgia, 'Times New Roman', serif",
             weight="700", anchor="middle", spacing=None, style=""):
        sp = f' letter-spacing="{spacing}"' if spacing else ""
        st = f' font-style="{style}"' if style else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
                 f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{sp}{st}>{s}</text>')

    def arrowhead(self, x, y, ang, size, fill):
        a = math.radians(ang)
        p2 = (x - size * math.cos(a - 0.5), y - size * math.sin(a - 0.5))
        p3 = (x - size * math.cos(a + 0.5), y - size * math.sin(a + 0.5))
        self.path(f'M{x:.1f} {y:.1f} L{p2[0]:.1f} {p2[1]:.1f} L{p3[0]:.1f} {p3[1]:.1f} Z', fill=fill)

    def shadow(self, cx, cy, rx, ry=None, op=0.10):
        ry = ry or rx * 0.28
        self.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
                 f'fill="{INK}" opacity="{op}"/>')

    # ---- reusable glyphs ----
    def person(self, cx, cy, r, fill):
        self.circle(cx, cy, r, fill)
        self.circle(cx, cy - r * 0.24, r * 0.32, "#ffffff")
        s = r * 0.5
        self.path(f"M{cx-s} {cy+r*0.52} C {cx-s} {cy+r*0.06}, {cx+s} {cy+r*0.06}, "
                  f"{cx+s} {cy+r*0.52} Z", fill="#ffffff")

    def desk(self, cx, cy, w=84, h=62, fill=None):
        fill = fill or self.grad(C, "#7dd3fc", 120)
        self.rrect(cx - w / 2, cy - h / 2, w, h, 12, fill)
        self.rect(cx - w * 0.3, cy - h * 0.1, w * 0.6, 8, "#ffffff")
        self.rect(cx - w * 0.26, cy + 0.02 * h, 6, h * 0.32, "#ffffff")
        self.rect(cx + w * 0.26 - 6, cy + 0.02 * h, 6, h * 0.32, "#ffffff")

    def mood(self, cx, cy, r, kind):
        col = {"happy": GREEN, "sad": ROSE, "meh": GOLD}[kind]
        self.circle(cx, cy, r, "#ffffff")
        self.circle(cx, cy, r, "none", stroke=col, stroke_width=str(max(3, r * 0.22)))
        self.circle(cx - r * 0.38, cy - r * 0.18, r * 0.12, col)
        self.circle(cx + r * 0.38, cy - r * 0.18, r * 0.12, col)
        if kind == "happy":
            self.path(f"M{cx-r*0.42} {cy+r*0.18} Q {cx} {cy+r*0.62}, {cx+r*0.42} {cy+r*0.18}",
                      stroke=col, sw=max(3, r * 0.2))
        elif kind == "sad":
            self.path(f"M{cx-r*0.42} {cy+r*0.42} Q {cx} {cy-r*0.02}, {cx+r*0.42} {cy+r*0.42}",
                      stroke=col, sw=max(3, r * 0.2))
        else:
            self.line(cx - r * 0.42, cy + r * 0.32, cx + r * 0.42, cy + r * 0.32, col,
                      sw=max(3, r * 0.2))

    def star(self, cx, cy, ro, ri, fill):
        pts = []
        for i in range(10):
            ang = math.pi / 5 * i - math.pi / 2
            r = ro if i % 2 == 0 else ri
            pts.append(f"{cx + r*math.cos(ang):.1f} {cy + r*math.sin(ang):.1f}")
        self.path("M" + " L".join(pts) + " Z", fill=fill)

    def render(self, label):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}" height="{self.H}" '
                f'viewBox="0 0 {self.W} {self.H}" role="img" aria-label="{label}">'
                f'<defs>{"".join(self.defs)}</defs>{"".join(self.body)}</svg>')


def save(slug, svg):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + ".svg"), "w") as fh:
        fh.write(svg)
    print(f"wrote {slug}.svg ({len(svg)} bytes)")


# =====================================================================
def lottery():
    """Random draw: an indifferent early pick takes the seat someone loved."""
    f = Fig(1200, 560)
    f.text(600, 78, "the lottery: luck, not fit", 40, INK,
           family="Georgia, serif", weight="700", style="italic")

    px, dx = 360, 840
    ys = [190, 320, 450]
    people_fill = f.grad(A, F, 120)

    # coveted "window seat" is the bottom desk
    star_idx = 2
    # lottery result (pick order): P1->star(bottom), P2->mid, P3->top
    result = {0: 2, 1: 1, 2: 0}
    moods = {0: "meh", 1: "happy", 2: "sad"}

    # assignment lines first (behind nodes)
    for i, ly in enumerate(ys):
        j = result[i]
        col = ROSE if (i == 2 or j == star_idx) else INK
        sw = 8 if j == star_idx else 6
        op = "1" if j == star_idx or i == 2 else "0.5"
        f.line(px + 40, ly, dx - 52, ys[j], col, sw=sw, opacity=op,
               dash=None if j == star_idx or i == 2 else "2 12")

    # people (left), numbered in draw order
    for i, ly in enumerate(ys):
        f.person(px, ly, 36, people_fill)
        f.circle(px - 44, ly - 30, 17, INK)
        f.text(px - 44, ly - 23, str(i + 1), 22, "#ffffff",
               family="Georgia, serif", weight="800")
        f.mood(px + 60, ly, 20, moods[i])

    # desks (right); star desk highlighted
    for j, dy in enumerate(ys):
        if j == star_idx:
            f.desk(dx, dy, fill=f.grad(GOLD, "#fcd34d", 120))
            f.star(dx, dy - 62, 20, 9, GOLD)
            f.text(dx + 70, dy + 6, "the seat", 24, INK, anchor="start",
                   family="Georgia, serif", weight="700", style="italic")
            f.text(dx + 70, dy + 34, "everyone wants", 24, INK, anchor="start",
                   family="Georgia, serif", weight="700", style="italic")
        else:
            f.desk(dx, dy)

    # a little heart showing P3 wanted the star seat
    hx, hy, s = px + 118, ys[2] - 46, 15
    f.path(f"M{hx} {hy+s*0.7} C {hx-s} {hy-s*0.3}, {hx-s*0.5} {hy-s}, {hx} {hy-s*0.35} "
           f"C {hx+s*0.5} {hy-s}, {hx+s} {hy-s*0.3}, {hx} {hy+s*0.7} Z", fill=ROSE, opacity="0.9")

    f.text(px, 150, "draw order", 22, INK, family="Georgia, serif",
           weight="700", spacing="1")
    save("hungarian-lottery",
         f.render("A seat lottery where the first name drawn takes the seat another person wanted most"))


# =====================================================================
def bets():
    """Two betting styles normalize into 0..1 happiness scores."""
    f = Fig(1200, 600)
    f.text(600, 74, "a fixed budget of bets → a happiness score", 38, INK,
           family="Georgia, serif", weight="700", style="italic")

    panels = [
        dict(x=90, title="spread it evenly", note="happy with any of the four",
             bets=[5, 5, 5, 5]),
        dict(x=620, title="go (almost) all-in", note="really wants the first",
             bets=[8, 4, 2, 1]),
    ]
    pw, ph = 490, 430
    labels = ["1st", "2nd", "3rd", "4th"]
    bar_fill = f.grad(A, C, 0)

    for pn in panels:
        x = pn["x"]
        f.shadow(x + pw / 2, 150 + ph + 8, pw * 0.4, 18, 0.08)
        f.rrect(x, 150, pw, ph, 22, "#ffffff", opacity="0.96")
        f.person(x + 46, 150 + 46, 26, f.grad(A, F, 120))
        f.text(x + 86, 150 + 40, pn["title"], 26, INK, anchor="start",
               family="Georgia, serif", weight="700")
        f.text(x + 86, 150 + 68, pn["note"], 18, "#6b7280", anchor="start",
               family="Georgia, serif", weight="400", style="italic")
        # column headers
        f.text(x + 118, 150 + 112, "bet", 17, "#9ca3af", anchor="middle",
               family="'Courier New', monospace", weight="700", spacing="1")
        f.text(x + 300, 150 + 112, "happiness", 17, "#9ca3af", anchor="middle",
               family="'Courier New', monospace", weight="700", spacing="1")

        top = max(pn["bets"])
        row_y = 150 + 150
        track_x, track_w = x + 196, 236
        for i, bet in enumerate(pn["bets"]):
            cy = row_y + i * 66
            f.text(x + 58, cy + 7, labels[i], 20, INK, anchor="middle",
                   family="Georgia, serif", weight="700")
            # bet chip
            f.circle(x + 118, cy, 20, f.grad(D, F, 120))
            f.text(x + 118, cy + 7, str(bet), 21, "#ffffff",
                   family="Georgia, serif", weight="800")
            # happiness track + bar
            score = bet / top
            f.rrect(track_x, cy - 14, track_w, 28, 14, "#eef2ff")
            f.rrect(track_x, cy - 14, max(28, track_w * score), 28, 14, bar_fill)
            f.text(track_x + track_w + 34, cy + 7, f"{score:.2f}", 20, INK,
                   anchor="middle", family="'Courier New', monospace", weight="700")

    save("hungarian-bets",
         f.render("Two people's bets across four seat choices normalized into happiness scores from 0 to 1"))


# =====================================================================
def cost_matrix():
    """The assignment that maximizes total happiness across the whole team."""
    f = Fig(1200, 700)
    f.text(600, 72, "one desk per person, maximum total happiness", 36, INK,
           family="Georgia, serif", weight="700", style="italic")

    people = ["Ada", "Bram", "Cleo", "Dev"]
    desks = ["A", "B", "C", "D"]
    M = [
        [0.90, 0.70, 0.10, 0.00],
        [0.80, 0.20, 0.90, 0.10],
        [0.85, 0.60, 0.30, 0.40],
        [0.20, 0.00, 0.50, 0.90],
    ]
    # optimal assignment (row -> col): Ada->B, Bram->C, Cleo->A, Dev->D
    chosen = {0: 1, 1: 2, 2: 0, 3: 3}

    n = 4
    cell = 118
    gx = 452          # grid left
    gy = 210          # grid top
    gw = cell * n

    # column headers (desks)
    for j in range(n):
        cx = gx + j * cell + cell / 2
        f.desk(cx, gy - 66, w=76, h=54)
        f.text(cx, gy - 22, desks[j], 22, INK, family="Georgia, serif", weight="700")
    # row headers (people) — icon + name in the wide left gutter
    for i in range(n):
        cy = gy + i * cell + cell / 2
        f.person(190, cy, 26, f.grad(A, F, 120))
        f.text(228, cy + 7, people[i], 22, INK, anchor="start",
               family="Georgia, serif", weight="600")

    # cells
    for i in range(n):
        for j in range(n):
            x = gx + j * cell
            y = gy + i * cell
            v = M[i][j]
            f.rrect(x + 5, y + 5, cell - 10, cell - 10, 14,
                    f.grad(A, C, 120), opacity=f"{0.10 + 0.85 * v:.3f}")
            tcol = "#ffffff" if v > 0.5 else INK
            f.text(x + cell / 2, y + cell / 2 + 9, f"{v:.2f}", 26, tcol,
                   family="'Courier New', monospace", weight="700")

    # highlight chosen cells
    for i, j in chosen.items():
        x = gx + j * cell
        y = gy + i * cell
        f.rrect(x + 5, y + 5, cell - 10, cell - 10, 14, "none",
                stroke=GREEN, stroke_width="6")
        # check badge, top-right of the cell
        bx, by = x + cell - 22, y + 22
        f.circle(bx, by, 16, GREEN)
        f.path(f"M{bx-7} {by} l5 6 l10 -12", stroke="#ffffff", sw=4)

    # footer note
    total = sum(M[i][chosen[i]] for i in chosen)
    fy = gy + gw + 56
    f.text(gx + gw / 2, fy, "Ada gives up desk A (her 0.90) so Cleo can take it — "
           "that trade makes the whole team happier.", 21, INK,
           family="Georgia, serif", weight="400", style="italic")
    f.text(gx + gw / 2, fy + 34,
           f"total happiness {total:.2f} / {n}  ·  avg {total/n:.2f}", 20, A,
           family="'Courier New', monospace", weight="700")

    save("hungarian-cost-matrix",
         f.render("A people-by-desks happiness matrix with the optimal one-per-row assignment highlighted"))


if __name__ == "__main__":
    lottery()
    bets()
    cost_matrix()
    print("done")
