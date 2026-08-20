#!/usr/bin/env python3
"""Bespoke per-article SVG cover illustrations for scottchacon.com.

One hand-composed scene per post, each reflecting the article's actual topic,
all sharing a single visual system (soft category-tinted background + faint
grid + soft blobs, flat gradient vector illustration) so they read as a set.
No external resources; text uses generic system fonts so it renders inside
an <img>-referenced SVG.
"""
import math, os

W, H = 1200, 800
ROOT = "/Users/schacon/projects/scottchacon-site/public/assets/images"
OUT = f"{ROOT}/covers"      # post covers
PROJ_OUT = f"{ROOT}/projects"  # /projects/ cards + project page rails

PAL = {
    "git": dict(bg=("#fff3ec", "#ffdcc7"), ink="#7c2d12",
                a="#f97316", b="#ea580c", c="#e11d48", d="#f59e0b",
                e="#6366f1", f="#fb923c"),
    "tech": dict(bg=("#eef2ff", "#dbe4ff"), ink="#1e1b4b",
                 a="#4f46e5", b="#2563eb", c="#0ea5e9", d="#7c3aed",
                 e="#06b6d4", f="#818cf8"),
    "life": dict(bg=("#ecfdf5", "#cdf4e2"), ink="#064e3b",
                 a="#0d9488", b="#059669", c="#10b981", d="#f59e0b",
                 e="#ec4899", f="#0ea5e9"),
    "lang": dict(bg=("#fdf2f8", "#fbe2f0"), ink="#831843",
                 a="#ec4899", b="#db2777", c="#a855f7", d="#f59e0b",
                 e="#8b5cf6", f="#f472b6"),
}


class Cover:
    def __init__(self, cat):
        self.p = PAL[cat]
        self.defs = []
        self.body = []
        self._gid = 0
        self._bg()

    # ---- gradient registration ----
    def grad(self, c0, c1, angle=90):
        self._gid += 1
        n = f"g{self._gid}"
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
        self._gid += 1
        n = f"g{self._gid}"
        self.defs.append(
            f'<radialGradient id="{n}"><stop offset="0" stop-color="{c0}"/>'
            f'<stop offset="1" stop-color="{c1}"/></radialGradient>')
        return f"url(#{n})"

    # ---- background shared across all covers ----
    def _bg(self):
        p = self.p
        self.body.append(
            f'<rect width="{W}" height="{H}" fill="{self.grad(*p["bg"], 120)}"/>')
        g = []
        for x in range(100, W, 100):
            g.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>')
        for y in range(100, H, 100):
            g.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
        self.body.append(
            f'<g stroke="{p["ink"]}" stroke-width="1" opacity="0.05">'
            + "".join(g) + "</g>")
        # soft blobs
        self.body.append(
            f'<circle cx="250" cy="170" r="300" fill="{self.rgrad(p["a"], p["bg"][1])}" opacity="0.12"/>')
        self.body.append(
            f'<circle cx="1000" cy="640" r="340" fill="{self.rgrad(p["d"], p["bg"][1])}" opacity="0.10"/>')

    # ---- primitives ----
    def add(self, s):
        self.body.append(s)

    def pill(self, x, y, w, h, fill, **kw):
        extra = "".join(f' {k}="{v}"' for k, v in kw.items())
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
                 f'height="{h:.1f}" rx="{h/2:.1f}" fill="{fill}"{extra}/>')

    def rrect(self, x, y, w, h, r, fill, **kw):
        extra = "".join(f' {k}="{v}"' for k, v in kw.items())
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
                 f'height="{h:.1f}" rx="{r:.1f}" fill="{fill}"{extra}/>')

    def rect_raw(self, x, y, w, h, fill, **kw):
        extra = "".join(f' {k}="{v}"' for k, v in kw.items())
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
                 f'height="{h:.1f}" fill="{fill}"{extra}/>')

    def circle(self, cx, cy, r, fill, **kw):
        extra = "".join(f' {k}="{v}"' for k, v in kw.items())
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
                 f'fill="{fill}"{extra}/>')

    def ring(self, cx, cy, r, stroke, sw=10, **kw):
        extra = "".join(f' {k}="{v}"' for k, v in kw.items())
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" '
                 f'stroke="{stroke}" stroke-width="{sw}"{extra}/>')

    def line(self, x1, y1, x2, y2, stroke, sw=6, dash=None, cap="round"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{d}/>')

    def path(self, d, stroke=None, fill="none", sw=6, **kw):
        s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ""
        extra = "".join(f' {k}="{v}"' for k, v in kw.items())
        self.add(f'<path d="{d}" fill="{fill}"{s}{extra}/>')

    def text(self, x, y, s, size, fill, family="Georgia, 'Times New Roman', serif",
             weight="700", anchor="middle", spacing=None, style=""):
        sp = f' letter-spacing="{spacing}"' if spacing else ""
        st = f' font-style="{style}"' if style else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" '
                 f'font-size="{size}" font-weight="{weight}" fill="{fill}" '
                 f'text-anchor="{anchor}"{sp}{st}>{s}</text>')

    def arrowhead(self, x, y, ang, size, fill):
        a = math.radians(ang)
        p1 = (x, y)
        p2 = (x - size * math.cos(a - 0.5), y - size * math.sin(a - 0.5))
        p3 = (x - size * math.cos(a + 0.5), y - size * math.sin(a + 0.5))
        self.path(f'M{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} '
                  f'L{p3[0]:.1f} {p3[1]:.1f} Z', fill=fill)

    def shadow(self, cx, cy, rx, ry=None, op=0.10):
        ry = ry or rx * 0.28
        self.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" '
                 f'ry="{ry:.1f}" fill="{self.p["ink"]}" opacity="{op}"/>')

    def clip(self, x, y, w, h, r):
        self._gid += 1
        n = f"c{self._gid}"
        self.defs.append(
            f'<clipPath id="{n}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
            f'height="{h:.1f}" rx="{r:.1f}"/></clipPath>')
        return n

    def render(self, label):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
                f'viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
                f'<defs>{"".join(self.defs)}</defs>{"".join(self.body)}</svg>')


def save(slug, svg, outdir=None):
    outdir = outdir or OUT
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, slug + ".svg"), "w") as fh:
        fh.write(svg)
    print(f"wrote {os.path.basename(outdir)}/{slug}.svg ({len(svg)} bytes)")


def save_project(slug, svg):
    save(slug, svg, PROJ_OUT)


# =====================================================================
# SCENES  (one per article)
# =====================================================================

def commit_line(c, y, xs, fill, node_r=16, sw=8):
    c.line(xs[0], y, xs[-1], y, fill, sw=sw)
    for x in xs:
        c.circle(x, y, node_r, fill)


def flags():
    """On Using Flags to Represent Languages — a row of stylized flags."""
    c = Cover("lang"); p = c.p
    fw, fh, top = 210, 138, 280
    xs = [175, 430, 685, 940]
    basey = 620
    for x in xs:
        c.line(x + 8, top, x + 8, basey, p["ink"], sw=7)
        c.circle(x + 8, top - 6, 12, p["ink"])
        c.shadow(x + 8, basey + 6, 46, 12, 0.10)

    def wave(x):  # a gentle flag bottom wave, as a clipped rounded rect
        cid = c.clip(x, top, fw, fh, 14)
        return cid

    # 1: vertical tricolor
    x = xs[0]; cid = wave(x)
    c.add(f'<g clip-path="url(#{cid})">')
    c.rect_raw(x, top, fw/3, fh, c.grad("#4f46e5", "#6366f1"))
    c.rect_raw(x + fw/3, top, fw/3, fh, "#ffffff")
    c.rect_raw(x + 2*fw/3, top, fw/3, fh, c.grad("#e11d48", "#fb7185"))
    c.add("</g>")
    # 2: rising sun
    x = xs[1]; cid = wave(x)
    c.add(f'<g clip-path="url(#{cid})">')
    c.rect_raw(x, top, fw, fh, "#ffffff")
    c.circle(x + fw/2, top + fh/2, 42, c.grad("#ef4444", "#f97316"))
    c.add("</g>")
    # 3: horizontal bands
    x = xs[2]; cid = wave(x)
    c.add(f'<g clip-path="url(#{cid})">')
    c.rect_raw(x, top, fw, fh/3, c.grad("#0ea5e9", "#38bdf8"))
    c.rect_raw(x, top + fh/3, fw, fh/3, "#ffffff")
    c.rect_raw(x, top + 2*fh/3, fw, fh/3, c.grad("#059669", "#34d399"))
    c.add("</g>")
    # 4: diagonal cross
    x = xs[3]; cid = wave(x)
    c.add(f'<g clip-path="url(#{cid})">')
    c.rect_raw(x, top, fw, fh, c.grad("#7c3aed", "#a78bfa"))
    c.line(x, top, x + fw, top + fh, "#ffffff", sw=18, cap="butt")
    c.line(x + fw, top, x, top + fh, "#fde68a", sw=18, cap="butt")
    c.add("</g>")

    c.text(600, 210, "one icon, every language", 40, p["ink"],
           family="Georgia, serif", weight="700", style="italic")
    c.text(600, 690, "hello · bonjour · こんにちは · hola", 30,
           p["ink"], family="Georgia, serif", weight="500")
    save("flags", c.render("A row of stylized national flags on poles representing languages"))


def _flow_icon(c, x, y, kind):
    w = "#ffffff"
    if kind == "fork":
        c.line(x - 20, y - 24, x - 20, y + 24, w, sw=7)
        c.line(x - 20, y, x + 20, y - 24, w, sw=7)
        c.circle(x - 20, y + 24, 9, w); c.circle(x - 20, y - 24, 9, w)
        c.circle(x + 20, y - 24, 9, w)
    elif kind == "dot":
        c.circle(x, y, 20, w)
    elif kind == "chat":
        c.rrect(x - 30, y - 26, 60, 42, 12, w)
        c.path(f"M{x-8} {y+16} l0 20 l20 -20 Z", fill=w)
        for i in range(3):
            c.circle(x - 16 + i * 16, y - 5, 5, c.p["d"])
    else:  # up arrow (deploy)
        c.line(x, y + 22, x, y - 20, w, sw=8)
        c.path(f"M{x-18} {y-4} L{x} {y-26} L{x+18} {y-4} Z", fill=w)


def github_flow():
    """GitHub Flow — the flow as a labelled pipeline of steps."""
    c = Cover("tech"); p = c.p
    steps = [("BRANCH", "fork"), ("COMMIT", "dot"),
             ("REVIEW", "chat"), ("DEPLOY", "up")]
    grads = [c.grad(p["a"], p["f"]), c.grad(p["b"], p["c"]),
             c.grad(p["d"], "#c4b5fd"), c.grad("#22c55e", "#16a34a")]
    y = 380
    xs = [225, 470, 715, 960]
    r = 74
    for i in range(3):
        c.line(xs[i] + r + 6, y, xs[i + 1] - r - 24, y, p["ink"], sw=6)
        c.arrowhead(xs[i + 1] - r - 12, y, 0, 24, p["ink"])
    for i, (lbl, icon) in enumerate(steps):
        x = xs[i]
        c.shadow(x, y + r + 22, r * 0.8, 16, 0.09)
        c.circle(x, y, r, grads[i])
        _flow_icon(c, x, y, icon)
        c.text(x, y + r + 52, lbl, 24, p["ink"],
               family="'Courier New', monospace", weight="700", spacing="1")
    c.text(600, 150, "the github flow", 40, p["ink"],
           family="Georgia, serif", weight="700", style="italic")
    save("github-flow",
         c.render("The GitHub flow as a pipeline: branch, commit, review, deploy"))


def reset():
    """Reset Demystified — Git's three trees: HEAD, Index, Working."""
    c = Cover("git"); p = c.p
    labels = ["HEAD", "INDEX", "WORKING"]
    cols = [c.grad(p["e"], "#a5b4fc"), c.grad(p["a"], p["f"]),
            c.grad(p["c"], "#fb7185")]
    xs = [170, 500, 830]
    pw, ph, top = 200, 320, 240
    for i, x in enumerate(xs):
        c.shadow(x + pw/2, top + ph + 18, 120, 20, 0.10)
        c.rrect(x, top, pw, ph, 22, "#ffffff", opacity="0.95")
        c.rrect(x, top, pw, 56, 22, cols[i])
        c.rrect(x, top + 34, pw, 22, 0, cols[i])
        c.text(x + pw/2, top + 38, labels[i], 26, "#ffffff",
               family="'Courier New', monospace", weight="700", spacing="1")
        # little commit stack
        for j in range(3):
            cy = top + 130 + j * 60
            c.circle(x + pw/2, cy, 18, cols[i])
            if j < 2:
                c.line(x + pw/2, cy + 18, x + pw/2, cy + 42, cols[i], sw=6)
    # arrows between panels (reset moves the trees)
    ay = top + ph/2
    for x0, x1 in [(xs[0] + pw, xs[1]), (xs[1] + pw, xs[2])]:
        c.line(x0 + 14, ay, x1 - 26, ay, p["ink"], sw=7)
        c.arrowhead(x1 - 14, ay, 0, 26, p["ink"])
    c.text(600, 160, "the three trees", 42, p["ink"], family="Georgia, serif",
           weight="700", style="italic")
    save("reset", c.render("Git's three trees: HEAD, index and working directory with reset arrows"))


def notes():
    """Note to Self — a commit with a sticky note attached."""
    c = Cover("git"); p = c.p
    y = 430
    fill = c.grad(p["a"], p["f"], 0)
    c.line(180, y, 1020, y, fill, sw=10)
    for x in [180, 400, 820, 1020]:
        c.circle(x, y, 20, fill)
    # highlight middle node
    c.circle(600, y, 30, c.grad(p["c"], "#fb7185"))
    c.circle(600, y, 30, "none", stroke="#ffffff", **{"stroke-width": "6"})
    # sticky note attached
    nx, ny, nw, nh = 470, 150, 260, 210
    c.line(600, y - 30, nx + nw/2, ny + nh, p["ink"], sw=5, dash="2 10")
    g = f'<g transform="rotate(-6 {nx+nw/2} {ny+nh/2})">'
    c.add(g)
    c.shadow(nx + nw/2 + 10, ny + nh + 6, 120, 18, 0.10)
    c.rrect(nx, ny, nw, nh, 14, c.grad("#fde68a", "#fcd34d"))
    c.rrect(nx, ny, nw, 40, 14, c.grad("#fbbf24", "#f59e0b"))
    for i in range(3):
        c.line(nx + 26, ny + 90 + i * 38, nx + nw - 26, ny + 90 + i * 38,
               p["ink"], sw=6)
    c.add("</g>")
    c.text(600, 640, "git notes", 40, p["ink"],
           family="'Courier New', monospace", weight="700")
    save("notes", c.render("A commit node on a graph with a yellow sticky note attached"))


def pro_git_zh():
    """Pro Git 简体中文版 — a book with a branch motif and Chinese title."""
    c = Cover("git"); p = c.p
    bx, by, bw, bh = 430, 210, 340, 420
    c.shadow(bx + bw/2, by + bh + 20, 200, 26, 0.12)
    # book cover
    c.rrect(bx, by, bw, bh, 18, c.grad(p["b"], p["a"], 120))
    c.rrect(bx, by, 26, bh, 8, p["ink"], opacity="0.25")  # spine
    # branch motif on cover
    gy = by + 150
    c.line(bx + 80, gy, bx + 80, gy + 150, "#ffffff", sw=8)
    c.circle(bx + 80, gy, 16, "#ffffff")
    c.path(f"M{bx+80} {gy+70} C {bx+80} {gy+110}, {bx+220} {gy+70}, {bx+220} {gy+110}",
           stroke="#ffffff", sw=8)
    c.circle(bx + 220, gy + 116, 16, "#fde68a")
    c.circle(bx + 80, gy + 150, 16, "#ffffff")
    # titles
    c.text(bx + bw/2 + 12, by + 90, "Pro Git", 46, "#ffffff",
           family="Georgia, serif", weight="700")
    c.text(bx + bw/2 + 12, by + bh - 40, "简体中文版", 44, "#fde68a",
           family="'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif",
           weight="700")
    save("pro-git-zh", c.render("The Pro Git book cover with a branch motif and a Simplified Chinese title"))


def pro_git_kindle():
    """Pro Git on Kindle — an e-reader showing the book."""
    c = Cover("git"); p = c.p
    dx, dy, dw, dh = 420, 180, 360, 480
    c.shadow(dx + dw/2, dy + dh + 18, 210, 26, 0.12)
    c.rrect(dx, dy, dw, dh, 30, c.grad("#3f3f46", "#18181b"))  # device
    sx, sy, sw2, sh = dx + 30, dy + 40, dw - 60, dh - 110
    c.rrect(sx, sy, sw2, sh, 8, "#f8fafc")  # screen (e-ink)
    # book content on screen
    c.text(sx + sw2/2, sy + 80, "Pro Git", 40, p["ink"],
           family="Georgia, serif", weight="700")
    # branch motif
    gy = sy + 150
    c.line(sx + sw2/2, gy, sx + sw2/2, gy + 120, p["a"], sw=7)
    c.circle(sx + sw2/2, gy, 13, p["a"])
    c.path(f"M{sx+sw2/2} {gy+50} C {sx+sw2/2} {gy+90}, {sx+sw2/2+90} {gy+50}, {sx+sw2/2+90} {gy+90}",
           stroke=p["c"], sw=7)
    c.circle(sx + sw2/2 + 90, gy + 96, 13, p["c"])
    c.circle(sx + sw2/2, gy + 120, 13, p["a"])
    for i in range(3):
        c.line(sx + 40, sy + sh - 90 + i*26, sx + sw2 - 40, sy + sh - 90 + i*26,
               p["ink"], sw=5, dash="2 10")
    # home button
    c.circle(dx + dw/2, dy + dh - 34, 20, "none", stroke="#a1a1aa",
             **{"stroke-width": "5"})
    save("pro-git-on-kindle", c.render("An e-reader device showing the Pro Git book on its screen"))


def blog_over():
    """My New Blog — a fresh page with a sunrise and a sparkle."""
    c = Cover("life"); p = c.p
    # sunrise arc
    c.circle(600, 470, 210, c.rgrad("#fef3c7", p["bg"][1]), opacity="0.6")
    for i, r in enumerate([150, 200, 250]):
        c.path(f"M{600-r} 470 A {r} {r} 0 0 1 {600+r} 470",
               stroke=p["d"], sw=6, opacity=str(0.5 - i*0.12))
    # old faded page behind
    c.rrect(430, 250, 300, 380, 16, "#ffffff", opacity="0.45",
            transform="rotate(-8 580 440)")
    # new page front
    px, py, pw, ph = 470, 220, 300, 400
    c.shadow(px + pw/2, py + ph + 14, 150, 20, 0.10)
    c.rrect(px, py, pw, ph, 16, "#ffffff")
    c.rrect(px, py, pw, 60, 16, c.grad(p["a"], p["c"]))
    c.rrect(px, py + 40, pw, 20, 0, c.grad(p["a"], p["c"]))
    for i in range(5):
        w = pw - 60 if i % 2 == 0 else pw - 130
        c.line(px + 30, py + 130 + i*52, px + 30 + w, py + 130 + i*52,
               p["ink"], sw=7, dash="2 12")
    # sparkle / new badge
    c.text(770, 250, "✦", 60, p["d"], family="sans-serif")
    save("blog-over", c.render("A fresh blank page with a sunrise, marking a new blog"))


def environment():
    """Git Loves the Environment — a terminal sprouting a plant (env pun)."""
    c = Cover("git"); p = c.p
    tx, ty, tw, th = 300, 320, 600, 320
    c.shadow(tx + tw/2, ty + th + 16, 300, 26, 0.12)
    c.rrect(tx, ty, tw, th, 20, c.grad("#27272a", "#18181b"))
    c.rrect(tx, ty, tw, 48, 20, "#3f3f46")
    c.rrect(tx, ty + 26, tw, 22, 0, "#3f3f46")
    for i, col in enumerate(["#ef4444", "#f59e0b", "#22c55e"]):
        c.circle(tx + 34 + i*34, ty + 24, 10, col)
    # env var lines
    envs = ["$ export GIT_AUTHOR_NAME", "$ export GIT_DIR=.git",
            "$ export GIT_EDITOR=vim"]
    for i, s in enumerate(envs):
        c.text(tx + 34, ty + 120 + i*58, s, 26,
               "#86efac" if i == 0 else "#e4e4e7",
               family="'Courier New', monospace", weight="400", anchor="start")
    # plant growing out of the top
    stem_x = tx + tw - 150
    c.path(f"M{stem_x} {ty} C {stem_x} {ty-90}, {stem_x-30} {ty-120}, {stem_x} {ty-180}",
           stroke=p["b"], sw=10)
    leaf = c.grad("#22c55e", "#16a34a")
    c.path(f"M{stem_x} {ty-70} C {stem_x-70} {ty-90}, {stem_x-80} {ty-150}, {stem_x-20} {ty-140} "
           f"C {stem_x-30} {ty-100}, {stem_x} {ty-80}, {stem_x} {ty-70} Z", fill=leaf)
    c.path(f"M{stem_x} {ty-110} C {stem_x+70} {ty-130}, {stem_x+80} {ty-190}, {stem_x+20} {ty-180} "
           f"C {stem_x+30} {ty-140}, {stem_x} {ty-120}, {stem_x} {ty-110} Z", fill=leaf)
    c.circle(stem_x, ty - 180, 22, c.grad(p["d"], p["a"]))
    save("environment", c.render("A terminal window showing Git environment variables with a plant growing out"))


def replace():
    """Replace Kicker — swapping one commit object for another."""
    c = Cover("git"); p = c.p
    y = 400
    base = c.grad(p["a"], p["f"], 0)
    c.line(180, y, 1020, y, base, sw=9)
    for x in [180, 360, 840, 1020]:
        c.circle(x, y, 18, base)
    # old node (dashed, faded) up top; new node solid below, swap arrows
    old_c = 600
    c.ring(old_c, y - 150, 46, p["c"], sw=8, **{"stroke-dasharray": "6 12", "opacity": "0.7"})
    c.text(old_c, y - 138, "old", 26, p["c"], family="Georgia, serif",
           weight="700", style="italic")
    c.circle(old_c, y, 46, c.grad(p["e"], "#a5b4fc"))
    c.text(old_c, y + 10, "new", 26, "#ffffff", family="Georgia, serif", weight="700")
    # swap arrows (curved)
    c.path(f"M{old_c-70} {y-120} C {old_c-140} {y-70}, {old_c-140} {y-30}, {old_c-70} {y-10}",
           stroke=p["ink"], sw=6)
    c.arrowhead(old_c - 70, y - 10, 20, 24, p["ink"])
    c.path(f"M{old_c+70} {y-10} C {old_c+140} {y-30}, {old_c+140} {y-70}, {old_c+70} {y-120}",
           stroke=p["ink"], sw=6)
    c.arrowhead(old_c + 70, y - 120, 200, 24, p["ink"])
    c.text(600, 650, "git replace", 40, p["ink"],
           family="'Courier New', monospace", weight="700")
    save("replace", c.render("Swapping one commit object for another with git replace"))


def bundles():
    """Git's Little Bundle of Joy — a wrapped parcel holding a git graph."""
    c = Cover("git"); p = c.p
    bx, by, bw, bh = 400, 250, 400, 320
    c.shadow(bx + bw/2, by + bh + 16, 230, 26, 0.12)
    c.rrect(bx, by, bw, bh, 22, c.grad(p["f"], p["a"], 120))
    # ribbon
    c.rrect(bx + bw/2 - 26, by, 52, bh, 0, c.grad(p["c"], "#fb7185"))
    c.rrect(bx, by + bh/2 - 26, bw, 52, 0, c.grad(p["c"], "#fb7185"))
    # bow
    c.circle(bx + bw/2, by + bh/2, 30, c.grad(p["c"], "#fb7185"))
    c.path(f"M{bx+bw/2} {by+bh/2} l-70 -34 l0 68 Z", fill=c.grad(p["c"], "#fb7185"))
    c.path(f"M{bx+bw/2} {by+bh/2} l70 -34 l0 68 Z", fill=c.grad(p["c"], "#fb7185"))
    # tiny git graph "shipping label" on parcel
    lx, ly = bx + 40, by + 54
    c.rrect(lx, ly, 120, 90, 10, "#ffffff", opacity="0.92")
    c.line(lx + 24, ly + 45, lx + 96, ly + 45, p["a"], sw=6)
    for gx in [lx + 24, lx + 60, lx + 96]:
        c.circle(gx, ly + 45, 10, p["a"])
    # motion / sneakernet dashes
    for i in range(3):
        c.line(bx - 40 - i*44, by + bh/2 - 20 + i*20, bx - 90 - i*44,
               by + bh/2 - 20 + i*20, p["ink"], sw=7, dash="2 14")
    c.text(600, 660, "git bundle", 40, p["ink"],
           family="'Courier New', monospace", weight="700")
    save("bundles", c.render("A wrapped parcel containing a git graph, moved by sneakernet"))


def rerere():
    """Rerere — record & replay a conflict resolution."""
    c = Cover("git"); p = c.p
    cx, cy = 560, 400
    # two branches colliding into a conflict burst
    left = c.grad(p["e"], "#a5b4fc", 0)
    right = c.grad(p["c"], "#fb7185", 180)
    c.path(f"M200 250 C 360 250, 400 {cy}, {cx-60} {cy}", stroke=left, sw=10)
    c.path(f"M200 {cy+150} C 360 {cy+150}, 400 {cy}, {cx-60} {cy}", stroke=right, sw=10)
    c.circle(200, 250, 18, left); c.circle(200, cy + 150, 18, right)
    # conflict burst (star)
    pts = []
    for i in range(10):
        ang = math.pi / 5 * i - math.pi / 2
        r = 66 if i % 2 == 0 else 30
        pts.append(f"{cx + r*math.cos(ang):.1f} {cy + r*math.sin(ang):.1f}")
    c.path("M" + " L".join(pts) + " Z", fill=c.grad(p["d"], p["a"]))
    c.text(cx, cy + 12, "!", 44, "#ffffff", family="Georgia, serif", weight="800")
    # circular replay arrow around it
    rr = 120
    c.path(f"M{cx+rr} {cy} A {rr} {rr} 0 1 1 {cx} {cy-rr}",
           stroke=p["ink"], sw=7)
    c.arrowhead(cx, cy - rr, 180, 26, p["ink"])
    # "memory" chip to the right (remembered resolution)
    mx, my = 900, 340
    c.rrect(mx, my, 120, 120, 18, c.grad(p["b"], p["a"]))
    for i in range(3):
        c.line(mx - 16, my + 28 + i*32, mx, my + 28 + i*32, p["ink"], sw=6)
        c.line(mx + 120, my + 28 + i*32, mx + 136, my + 28 + i*32, p["ink"], sw=6)
    c.text(mx + 60, my + 74, "↻", 56, "#ffffff", family="sans-serif")
    c.line(cx + rr + 10, cy, mx - 24, my + 60, p["ink"], sw=6, dash="2 12")
    save("rerere", c.render("Recording and replaying a git conflict resolution"))


def smart_http():
    """Smart HTTP Transport — fast data over http between two nodes."""
    c = Cover("git"); p = c.p
    y = 400
    # two endpoints
    for x, lbl in [(210, ""), (990, "")]:
        c.shadow(x, y + 120, 90, 22, 0.10)
    # server (left) and client (right) as rounded devices
    c.rrect(140, y - 90, 150, 180, 20, c.grad(p["b"], p["a"], 120))
    c.rrect(910, y - 70, 160, 140, 20, c.grad(p["e"], "#a5b4fc", 120))
    # git repo mark on server
    c.circle(215, y - 20, 14, "#ffffff")
    c.line(215, y - 20, 215, y + 40, "#ffffff", sw=7)
    c.circle(215, y + 46, 14, "#ffffff")
    c.path(f"M215 {y+6} C215 {y+26}, 255 {y+6}, 255 {y+30}", stroke="#ffffff", sw=7)
    c.circle(255, y + 34, 12, "#fde68a")
    # wire
    c.line(300, y, 900, y, p["ink"], sw=6)
    # http pill + lightning + speed dashes
    c.pill(520, y - 34, 160, 68, c.grad(p["d"], p["a"]))
    c.text(600, y + 12, "http://", 30, "#ffffff",
           family="'Courier New', monospace", weight="700")
    c.path(f"M470 {y-70} l-30 46 l24 0 l-16 40 l44 -56 l-26 0 Z",
           fill=c.grad("#fde68a", p["d"]))
    for i in range(4):
        xx = 720 + i*40
        c.line(xx, y - 6 - i*2, xx + 26, y - 6 - i*2, p["c"], sw=6)
    save("smart-http", c.render("Fast git data transfer over HTTP between a server and client"))


def undoing_merges():
    """Undoing Merges — a merge point being reversed with an undo arc."""
    c = Cover("git"); p = c.p
    y = 430
    main = c.grad(p["a"], p["f"], 0)
    feat = c.grad(p["e"], "#a5b4fc", 0)
    c.line(180, y, 1020, y, main, sw=10)
    for x in [180, 360, 820, 1020]:
        c.circle(x, y, 18, main)
    # feature branch merging in at x=600
    c.path(f"M360 {y} C 460 {y}, 470 280, 560 280 L 620 280 "
           f"C 700 280, 520 {y}, 600 {y}", stroke=feat, sw=10)
    for x in [560, 620]:
        c.circle(x, 280, 16, feat)
    # merge node highlighted
    c.circle(600, y, 26, c.grad(p["c"], "#fb7185"))
    # big counter-clockwise undo arc over the merge
    cx, cy, r = 600, y, 150
    c.path(f"M{cx+r} {cy-6} A {r} {r} 0 1 0 {cx-r*0.2:.0f} {cy-r+20:.0f}",
           stroke=p["ink"], sw=8)
    c.arrowhead(cx - r*0.2, cy - r + 20, 250, 30, p["ink"])
    c.text(600, 690, "git reset --hard HEAD^", 34, p["ink"],
           family="'Courier New', monospace", weight="700")
    save("undoing-merges", c.render("A git merge point being reversed with an undo arc"))


def this_year():
    """This Year — a 2009 calendar, quiet year-end reflection."""
    c = Cover("life"); p = c.p
    cx, cy, cw, ch = 420, 250, 360, 360
    c.shadow(cx + cw/2, cy + ch + 16, 200, 24, 0.10)
    c.rrect(cx, cy, cw, ch, 22, "#ffffff")
    c.rrect(cx, cy, cw, 90, 22, c.grad(p["a"], p["c"]))
    c.rrect(cx, cy + 60, cw, 30, 0, c.grad(p["a"], p["c"]))
    # binder rings
    for rx in [cx + 90, cx + cw - 90]:
        c.line(rx, cy - 24, rx, cy + 26, p["ink"], sw=10)
        c.circle(rx, cy - 24, 10, p["ink"])
    c.text(cx + cw/2, cy + 58, "2009", 46, "#ffffff",
           family="Georgia, serif", weight="800", spacing="4")
    # sparse marked days grid
    for r in range(3):
        for col in range(5):
            gx = cx + 60 + col*60
            gy = cy + 150 + r*70
            marked = (r*5 + col) in (2, 9, 13)
            c.circle(gx, gy, 20, c.grad(p["c"], p["b"]) if marked else "#e2e8f0")
    # crescent moon / star for reflective year-end
    c.circle(940, 210, 60, c.grad("#fcd34d", p["d"]))
    c.circle(968, 194, 52, p["bg"][0])
    c.text(300, 200, "★", 40, p["d"], family="sans-serif")
    save("this-year", c.render("A 2009 calendar with a crescent moon for a quiet year-end reflection"))


def translate_this():
    """Translate This — one speech bubble forking into many languages."""
    c = Cover("git"); p = c.p
    # source bubble
    sx, sy = 240, 400
    c.circle(sx, sy, 6, p["ink"])
    src = c.grad(p["a"], p["f"])
    c.rrect(sx - 30, sy - 70, 200, 140, 26, src)
    c.path(f"M{sx+40} {sy+60} l0 60 l50 -50 Z", fill=src)
    c.text(sx + 70, sy + 12, "git", 40, "#ffffff",
           family="Georgia, serif", weight="700")
    # fork lines to translated bubbles
    targets = [
        (760, 210, "あ", c.grad(p["c"], "#fb7185")),
        (860, 400, "Я", c.grad(p["e"], "#a5b4fc")),
        (760, 590, "文", c.grad(p["b"], p["a"])),
    ]
    for tx, ty, glyph, g in targets:
        c.path(f"M{sx+180} {sy} C {sx+300} {sy}, {tx-160} {ty}, {tx-30} {ty}",
               stroke=p["ink"], sw=6)
        c.rrect(tx - 30, ty - 60, 170, 120, 24, g)
        c.path(f"M{tx-10} {ty+50} l0 50 l44 -42 Z", fill=g)
        c.text(tx + 55, ty + 16, glyph, 46, "#ffffff",
               family="sans-serif", weight="700")
    save("translate-this", c.render("One speech bubble forking into bubbles of different languages"))


def gory_details():
    """The Gory Details — a launch-day traffic spike with a book."""
    c = Cover("git"); p = c.p
    ax, ay, aw, ah = 200, 620, 820, 380
    # axes
    c.line(ax, ay, ax + aw, ay, p["ink"], sw=6)
    c.line(ax, ay, ax, ay - ah + 40, p["ink"], sw=6)
    # spiking area chart
    pts = [(ax, ay), (ax + 120, ay - 60), (ax + 260, ay - 90),
           (ax + 420, ay - 150), (ax + 560, ay - 120), (ax + 700, ay - 300),
           (ax + aw, ay - 250)]
    d = f"M{pts[0][0]} {pts[0][1]} " + " ".join(f"L{x} {y}" for x, y in pts[1:])
    area = c.grad(p["a"], p["f"], 90)
    c.path(d + f" L{ax+aw} {ay} L{ax} {ay} Z", fill=area, opacity="0.35")
    c.path(d, stroke=c.grad(p["c"], p["a"], 0), sw=8)
    for x, y in pts:
        c.circle(x, y, 9, p["a"])
    # 10k marker at the peak
    px, py = ax + 700, ay - 300
    c.pill(px - 60, py - 78, 150, 56, c.grad(p["c"], "#fb7185"))
    c.text(px + 15, py - 40, "10,000", 30, "#ffffff",
           family="Georgia, serif", weight="800")
    c.line(px, py - 22, px, py - 10, p["ink"], sw=5)
    # book at origin
    c.rrect(ax - 70, ay - 90, 90, 120, 8, c.grad(p["b"], p["a"], 120))
    c.line(ax - 25, ay - 90, ax - 25, ay + 30, "#ffffff", sw=4, dash="2 8")
    save("the-gory-details", c.render("A launch-day traffic spike chart peaking at ten thousand visitors"))


def do_what_you_want():
    """Do What You Want — a signpost of diverging paths, one sparked."""
    c = Cover("life"); p = c.p
    # ground + post
    px = 600
    c.shadow(px, 640, 150, 24, 0.10)
    c.rrect(px - 12, 240, 24, 400, 10, c.grad("#a16207", "#ca8a04"))
    # direction signs
    signs = [
        (250, c.grad(p["a"], p["c"]), False, 1),
        (330, c.grad(p["f"], p["b"]), True, -1),
        (410, c.grad(p["d"], "#fcd34d"), False, 1),
        (490, c.grad(p["e"], "#f9a8d4"), True, -1),
    ]
    for y, g, left, dirn in signs:
        w = 240
        if left:
            x = px - 12 - w
            c.path(f"M{x} {y} L{x+w} {y} L{x+w} {y+56} L{x} {y+56} "
                   f"L{x-40} {y+28} Z", fill=g)
        else:
            x = px + 12
            c.path(f"M{x} {y} L{x+w} {y} L{x+w+40} {y+28} L{x+w} {y+56} "
                   f"L{x} {y+56} Z", fill=g)
        # dashed line on sign
        cxs = x + 30 if not left else x + 20
        c.line(cxs, y + 28, cxs + w - 60, y + 28, "#ffffff", sw=7, dash="2 14")
    # a spark / heart on the chosen (top) sign
    c.text(px + 300, 232, "✦", 58, p["d"], family="sans-serif")
    # sun
    c.circle(230, 210, 66, c.grad("#fcd34d", p["d"]))
    save("do-what-you-want", c.render("A signpost with diverging paths, one marked with a spark"))


def mit_language():
    """MIT adults learn language — accuracy curves rising to a native line."""
    c = Cover("lang"); p = c.p
    ax, ay, aw, ah = 190, 630, 840, 420
    # axes
    c.line(ax, ay, ax + aw, ay, p["ink"], sw=6)
    c.line(ax, ay, ax, ay - ah + 30, p["ink"], sw=6)
    # "native" threshold line (dashed) near the top
    ny = ay - ah + 90
    c.line(ax, ny, ax + aw, ny, p["b"], sw=4, dash="2 12")
    c.text(ax + aw - 6, ny - 16, "native", 26, p["b"], anchor="end",
           family="Georgia, serif", weight="700", style="italic")
    # three learning curves (start ages) rising toward the line
    curves = [
        (c.grad("#ef4444", "#f97316"), 0),      # started young
        (c.grad(p["d"], "#fcd34d"), 34),
        (c.grad(p["a"], p["c"], 0), 74),        # started as adult (20+)
    ]
    for g, off in curves:
        x0, y0 = ax, ay - 40 - off * 0.2
        d = (f"M{x0} {y0} "
             f"C {ax+220} {ny+70+off}, {ax+380} {ny+30+off}, {ax+540} {ny+18+off} "
             f"S {ax+760} {ny+8+off}, {ax+aw} {ny+6+off}")
        c.path(d, stroke=g, sw=9)
        c.circle(ax + aw, ny + 6 + off, 12, g)
    # a couple of scatter dots in native range for the adult curve
    for dx in [520, 640, 760]:
        c.circle(ax + dx, ny - 8, 9, c.grad(p["a"], p["c"], 0))
    c.text(600, 150, "adults get there too", 40, p["ink"],
           family="Georgia, serif", weight="700", style="italic")
    save("mit-adults-learn-language",
         c.render("Language-accuracy curves for different starting ages rising toward a native line"))


def github_cs():
    """Tips from GitHub: Customer Service — a chat bubble with a heart + star."""
    c = Cover("tech"); p = c.p
    # main support chat bubble
    bx, by, bw, bh = 300, 250, 460, 300
    c.shadow(bx + bw/2, by + bh + 40, 220, 26, 0.12)
    c.rrect(bx, by, bw, bh, 40, c.grad(p["a"], p["f"], 120))
    c.path(f"M{bx+120} {by+bh} l0 90 l90 -90 Z", fill=c.grad(p["a"], p["f"], 120))
    # heart inside
    hx, hy, s = bx + bw/2, by + bh/2 + 6, 46
    c.path(f"M{hx} {hy+s*0.7} C {hx-s} {hy-s*0.3}, {hx-s*0.5} {hy-s}, {hx} {hy-s*0.35} "
           f"C {hx+s*0.5} {hy-s}, {hx+s} {hy-s*0.3}, {hx} {hy+s*0.7} Z",
           fill="#ffffff")
    # smaller reply bubble
    c.rrect(720, 400, 220, 150, 32, c.grad(p["c"], "#7dd3fc", 120))
    c.path(f"M{860} {550} l0 60 l50 -60 Z", fill=c.grad(p["c"], "#7dd3fc", 120))
    for i in range(3):
        c.circle(760 + i * 40, 475, 12, "#ffffff")
    # superfan star
    cx, cy = 880, 230
    pts = []
    for i in range(10):
        ang = math.pi / 5 * i - math.pi / 2
        r = 54 if i % 2 == 0 else 24
        pts.append(f"{cx + r*math.cos(ang):.1f} {cy + r*math.sin(ang):.1f}")
    c.path("M" + " L".join(pts) + " Z", fill=c.grad(p["d"], "#c4b5fd"))
    c.text(600, 160, "create a superfan", 40, p["ink"],
           family="Georgia, serif", weight="700", style="italic")
    save("tips-from-github-customer-service",
         c.render("A customer-support chat bubble with a heart and a superfan star"))


def hungarian_desks():
    """Hungarian Desks — bipartite matching of people to desks."""
    c = Cover("tech"); p = c.p
    lx, rx = 340, 860
    ys = [270, 400, 530]
    people = c.grad(p["a"], p["f"], 120)
    desk = c.grad(p["c"], "#7dd3fc", 120)
    # faint candidate edges (all-to-all)
    matching = {0: 1, 1: 2, 2: 0}
    for i, ly in enumerate(ys):
        for j, ry in enumerate(ys):
            if matching[i] == j:
                continue
            c.line(lx + 34, ly, rx - 40, ry, p["ink"], sw=3,
                   dash="2 12")
    # optimal matching edges (bold, colored)
    for i, ly in enumerate(ys):
        j = matching[i]
        c.line(lx + 34, ly, rx - 40, ys[j], c.grad(p["a"], p["c"], 0), sw=8)
    # people nodes (left) — circles with a head/person mark
    for ly in ys:
        c.circle(lx, ly, 34, people)
        c.circle(lx, ly - 8, 11, "#ffffff")
        c.path(f"M{lx-16} {ly+18} C {lx-16} {ly+2}, {lx+16} {ly+2}, {lx+16} {ly+18} Z",
               fill="#ffffff")
    # desk nodes (right) — little desk glyphs
    for ry in ys:
        c.rrect(rx - 40, ry - 30, 80, 60, 12, desk)
        c.rect_raw(rx - 24, ry - 6, 48, 8, "#ffffff")
        c.rect_raw(rx - 22, ry + 2, 6, 20, "#ffffff")
        c.rect_raw(rx + 16, ry + 2, 6, 20, "#ffffff")
    c.text(600, 155, "everyone's happiest seat", 38, p["ink"],
           family="Georgia, serif", weight="700", style="italic")
    save("hungarian-desks",
         c.render("A bipartite matching of people to desks, one optimal assignment highlighted"))


def cefr_levels():
    """How to Talk about Language Learning — the six CEFR levels as a rising staircase."""
    c = Cover("lang"); p = c.p
    labels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    pairs = [(p["f"], p["a"]), (p["a"], p["b"]), (p["b"], p["e"]),
             (p["e"], p["c"]), (p["c"], "#7c3aed"), ("#7c3aed", "#6d28d9")]
    base = 650
    bw, gap, x0 = 118, 22, 190
    for i, lbl in enumerate(labels):
        h = 90 + i * 62
        x = x0 + i * (bw + gap)
        y = base - h
        c.shadow(x + bw/2, base + 12, bw * 0.6, 12, 0.08)
        c.rrect(x, y, bw, h, 18, c.grad(pairs[i][0], pairs[i][1], 90))
        c.text(x + bw/2, y + 46, lbl, 34, "#ffffff",
               family="'Courier New', monospace", weight="700", spacing="1")
    # a little flag planted on the top (C2) step
    tx = x0 + 5 * (bw + gap) + bw/2
    ty = base - (90 + 5 * 62)
    c.line(tx, ty - 76, tx, ty, p["ink"], sw=7)
    c.path(f"M{tx} {ty-76} L{tx+58} {ty-60} L{tx} {ty-44} Z",
           fill=c.grad(p["d"], "#fcd34d"))
    c.circle(tx, ty - 78, 9, p["ink"])
    c.text(600, 155, "from first word to fluent", 40, p["ink"],
           family="Georgia, serif", weight="700", style="italic")
    save("cefr-language-levels",
         c.render("The six CEFR language levels rising as a staircase from A1 to C2"))


def git_wire_v2():
    """Git Wire Protocol v2 — a terminal showing a v2 capability advertisement."""
    c = Cover("git"); p = c.p
    tx, ty, tw, th = 250, 240, 700, 360
    mono = "'Courier New', monospace"
    c.shadow(tx + tw/2, ty + th + 16, 340, 26, 0.12)
    c.rrect(tx, ty, tw, th, 20, c.grad("#0f2320", "#0a1413"))
    c.rrect(tx, ty, tw, 48, 20, "#173330")
    c.rrect(tx, ty + 26, tw, 22, 0, "#173330")
    for i, col in enumerate(["#e06c4a", "#d9a24a", "#4aa06a"]):
        c.circle(tx + 34 + i * 32, ty + 24, 9, col)
    rows = [
        ("$ git ls-remote origin", "#5F7A76"),
        ("version 2", "#57C6BD"),
        ("ls-refs  fetch  filter", "#E7ECEA"),
        ("object-format=sha1", "#E9915F"),
        ("0000", "#5F7A76"),
    ]
    for i, (s, col) in enumerate(rows):
        c.text(tx + 34, ty + 112 + i * 48, s, 25, col, family=mono,
               weight="400", anchor="start")
    c.rect_raw(tx + 34 + 74, ty + 112 + 4 * 48 - 21, 14, 27, "#57C6BD")  # cursor
    c.text(600, 160, "you are a protocol droid, are you not?", 38, p["ink"],
           family="Georgia, serif", weight="700", style="italic")
    save("git-wire-v2",
         c.render("A terminal showing a Git protocol v2 capability advertisement"))


def local_models_build_an_app():
    """Three build bars of twenty cards; two finished apps still serve a 500."""
    c = Cover("tech"); p = c.p
    green, amber, grey = "#16a34a", "#f59e0b", "#c7cfe3"
    red = "#dc2626"
    rows = [
        # label, per-card status, verdict
        ("GPT-5.6 Sol",  ["g"] * 20,                       True),
        ("Muse Glimmer", ["g"] * 20,                       False),
        ("Qwen3.8",      ["g"] * 6 + ["a"] * 4 + ["n"] * 10, True),
    ]
    x0, w, gap = 306, 29, 6
    y = 300
    for label, cards, works in rows:
        c.text(x0 - 26, y + 10, label, 26, p["ink"], anchor="end",
               family="Georgia, serif", weight="700")
        for i, st in enumerate(cards):
            fill = {"g": green, "a": amber, "n": grey}[st]
            op = ' opacity="0.45"' if st == "n" else ""
            c.add(f'<rect x="{x0 + i * (w + gap)}" y="{y - 14}" width="{w}" '
                  f'height="28" rx="6" fill="{fill}"{op}/>')
        bx = x0 + 20 * (w + gap) + 26
        if works:
            c.circle(bx + 22, y, 21, green)
            c.path(f"M{bx + 12} {y} l7 8 l14 -16", stroke="#ffffff", sw=6)
        else:
            c.rrect(bx, y - 26, 116, 52, 10, "#ffffff")
            c.rect_raw(bx, y - 26, 116, 15, "#f1f5f9")
            for k in range(3):
                c.circle(bx + 14 + k * 13, y - 18, 3.5, "#cbd5e1")
            c.text(bx + 58, y + 15, "500", 28, red,
                   family="'IBM Plex Mono', monospace", weight="700")
        y += 108
    c.text(600, 150, "twenty cards, three models", 40, p["ink"],
           family="Georgia, serif", weight="700", style="italic")
    c.text(600, 700, "every suite green &#183; every build clean",
           27, p["ink"], family="Georgia, serif", weight="400", style="italic")
    save("local-models-build-an-app",
         c.render("Three rows of twenty build cards; two completed rows still "
                  "end in a browser window showing a 500 error"))
def unfurler():
    """unfurler.dev — one link preview card, with the image still a question."""
    c = Cover("tech"); p = c.p

    cw, ch = 560, 500
    cx, cy = (W - cw) / 2, (H - ch) / 2
    c.shadow(cx + cw / 2, cy + ch + 18, 240, 24, 0.12)
    c.rrect(cx, cy, cw, ch, 26, "#ffffff")

    # The image slot, with its contents still unknown.
    slot_h = 320
    cid = c.clip(cx, cy, cw, slot_h, 26)
    c.add(f'<g clip-path="url(#{cid})">')
    c.rect_raw(cx, cy, cw, slot_h, c.grad(p["a"], p["d"], 45))
    c.add("</g>")

    # A question mark drawn as geometry — no web fonts survive inside an <img>.
    qx, qy = 600, cy + 106
    c.path(f"M{qx-46} {qy} A46 46 0 1 1 {qx} {qy+46} L{qx} {qy+82}",
           stroke="#ffffff", sw=24)
    c.circle(qx, qy + 128, 14, "#ffffff")

    # Title, description, domain — bars, not words.
    c.pill(cx + 44, cy + slot_h + 44, 380, 26, p["ink"], opacity="0.80")
    c.pill(cx + 44, cy + slot_h + 92, 264, 22, p["ink"], opacity="0.26")
    c.pill(cx + 44, cy + slot_h + 132, 140, 16, p["ink"], opacity="0.14")

    save("unfurler",
         c.render("A link preview card whose image area holds a large question "
                  "mark, above blank title, description and domain bars"))


SCENES = [flags, github_flow, reset, notes, pro_git_zh, pro_git_kindle,
          blog_over, environment, replace, bundles, rerere, smart_http,
          undoing_merges, this_year, translate_this, gory_details,
          do_what_you_want, mit_language, github_cs, hungarian_desks,
          cefr_levels, git_wire_v2, unfurler,
          local_models_build_an_app]

# =====================================================================
# PROJECT POSTERS  (one per entry in src/projects/, written to PROJ_OUT)
#
# Deliberately NOT the post-cover look. Post covers are soft, illustrated and
# carry a tagline; these are flat, saturated, text-free geometry — two or three
# oversized shapes on one solid field. They have to read as a thumbnail in the
# /projects/ grid and as a 240px rail image on the project page, so: no grid,
# no blobs, no gradients, no type, and nothing thinner than about 14px.
# =====================================================================

PP = {
    "ink":       "#141433",
    "slate":     "#2E2E5C",   # dim key / recessed shape on an ink field
    "cream":     "#F2ECE1",
    "sand":      "#DCD3C2",   # recessed shape on a cream field
    "vermilion": "#FF4A24",
    "mustard":   "#FFC02E",
    "teal":      "#00B39B",
    "cobalt":    "#2743E8",
    "magenta":   "#FF2D7E",
    "violet":    "#7A35F0",
    "sky":       "#3AC0F5",
}


def _polar(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


class Poster:
    """Flat, text-free geometric cover for a project. One solid field, a handful
    of big primitives, nothing else."""

    def __init__(self, bg):
        self.bg = PP[bg]
        self.body = [f'<rect width="{W}" height="{H}" fill="{self.bg}"/>']

    def add(self, s):
        self.body.append(s)

    def _kw(self, kw):
        return "".join(f' {k.replace("_", "-")}="{v}"' for k, v in kw.items())

    def disc(self, cx, cy, r, fill, **kw):
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
                 f'fill="{fill}"{self._kw(kw)}/>')

    def ring(self, cx, cy, r, stroke, sw, **kw):
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" '
                 f'stroke="{stroke}" stroke-width="{sw}"{self._kw(kw)}/>')

    def bar(self, x, y, w, h, fill, r=0, **kw):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
                 f'height="{h:.1f}" rx="{r:.1f}" fill="{fill}"{self._kw(kw)}/>')

    def tri(self, pts, fill, **kw):
        d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}"
                     for i, (x, y) in enumerate(pts)) + " Z"
        self.add(f'<path d="{d}" fill="{fill}"{self._kw(kw)}/>')

    def wedge(self, cx, cy, r, a0, a1, fill, **kw):
        """Pie slice from a0 to a1 degrees (clockwise, 0 = east)."""
        x0, y0 = _polar(cx, cy, r, a0)
        x1, y1 = _polar(cx, cy, r, a1)
        large = 1 if (a1 - a0) % 360 > 180 else 0
        self.add(f'<path d="M{cx:.1f} {cy:.1f} L{x0:.1f} {y0:.1f} '
                 f'A{r:.1f} {r:.1f} 0 {large} 1 {x1:.1f} {y1:.1f} Z" '
                 f'fill="{fill}"{self._kw(kw)}/>')

    def band(self, cx, cy, r, a0, a1, stroke, sw, cap="butt", **kw):
        """Thick arc — a slice of a ring."""
        x0, y0 = _polar(cx, cy, r, a0)
        x1, y1 = _polar(cx, cy, r, a1)
        large = 1 if (a1 - a0) % 360 > 180 else 0
        self.add(f'<path d="M{x0:.1f} {y0:.1f} A{r:.1f} {r:.1f} 0 {large} 1 '
                 f'{x1:.1f} {y1:.1f}" fill="none" stroke="{stroke}" '
                 f'stroke-width="{sw}" stroke-linecap="{cap}"{self._kw(kw)}/>')

    def half(self, cx, cy, r, facing, fill):
        """Half disc; `facing` is the direction the round side points."""
        a0 = {"right": -90, "left": 90, "up": 180, "down": 0}[facing]
        self.wedge(cx, cy, r, a0, a0 + 180, fill)

    def render(self, label):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" '
                f'height="{H}" viewBox="0 0 {W} {H}" role="img" '
                f'aria-label="{label}">{"".join(self.body)}</svg>')




def micro_manager():
    """A keypad grid with four keys lit."""
    p = Poster("ink")
    lit = {0: PP["vermilion"], 2: PP["mustard"], 5: PP["teal"], 9: PP["sky"]}
    cell, gap = 150, 30
    x0 = (W - (4 * cell + 3 * gap)) / 2
    y0 = (H - (3 * cell + 2 * gap)) / 2
    for i in range(12):
        r, c = divmod(i, 4)
        p.bar(x0 + c * (cell + gap), y0 + r * (cell + gap), cell, cell,
              lit.get(i, PP["slate"]), r=26)
    return p.render("A grid of twelve chunky keys, four of them lit")


def ticgit():
    """Squares tethered to nodes on a line."""
    p = Poster("vermilion")
    p.bar(90, 552, 1020, 34, PP["ink"], r=17)
    for x in [190, 420, 650, 880, 1080]:
        p.disc(x, 569, 46, PP["ink"])
    for x in [420, 650, 880]:
        p.bar(x - 14, 380, 28, 180, PP["ink"])
    for x, y in [(420, 200), (650, 156), (880, 224)]:
        p.bar(x - 105, y, 210, 210, PP["cream"], r=24)
    return p.render("Three squares tethered to nodes on a horizontal line")


def unfurler_project():
    """Three fetches, two different answers."""
    p = Poster("teal")
    for x in [330, 600, 870]:
        p.disc(x, 172, 46, PP["ink"])
        p.bar(x - 13, 200, 26, 90, PP["ink"])
    p.bar(150, 290, 430, 380, PP["cream"], r=26)
    p.bar(150, 290, 430, 200, PP["ink"], r=26)
    p.bar(190, 536, 240, 34, PP["ink"], r=17)
    p.bar(190, 594, 150, 34, PP["ink"], r=17)
    p.bar(620, 290, 430, 380, PP["cream"], r=26)
    for angle in (45, -45):
        p.bar(819, 292, 32, 200, PP["ink"], r=16,
              transform=f"rotate({angle} 835 392)")
    p.bar(660, 536, 240, 34, PP["ink"], r=17)
    p.bar(660, 594, 150, 34, PP["ink"], r=17)
    return p.render("Three probes feeding two cards: one with an image block, "
                    "one with a cross where the image should be")


def soe():
    """Lines of text and one enormous caret."""
    p = Poster("mustard")
    p.bar(150, 268, 400, 64, PP["ink"], r=32)
    p.bar(150, 412, 280, 64, PP["ink"], r=32)
    p.bar(590, 180, 140, 440, PP["cream"], r=16)
    return p.render("Three bars of text beside one oversized block caret")


def slidetty():
    """A slide and its progress dots."""
    p = Poster("magenta")
    p.bar(300, 150, 600, 400, PP["cream"], r=30)
    p.bar(360, 226, 460, 58, PP["ink"], r=29)
    p.bar(360, 330, 480, 32, PP["ink"], r=16)
    p.bar(360, 400, 380, 32, PP["ink"], r=16)
    for i in range(6):
        cx = 375 + i * 90
        p.disc(cx, 660, 40 if i == 2 else 24, PP["cream"])
    return p.render("A single slide above a row of progress dots")






def showoff():
    """A small source throwing a big picture."""
    p = Poster("cobalt")
    p.tri([(272, 336), (704, 186), (704, 614), (272, 474)], PP["mustard"])
    p.bar(140, 330, 140, 140, PP["cream"], r=16)
    p.bar(700, 190, 400, 420, PP["cream"], r=26)
    p.disc(900, 400, 96, PP["ink"])
    return p.render("A small square projecting a widening beam onto a large panel")


def git_scribe():
    """One source, four editions."""
    p = Poster("ink")
    cols = [PP["cream"], PP["vermilion"], PP["mustard"], PP["teal"]]
    for i, col in enumerate(cols):
        a0 = -90 + i * 90
        mx, my = _polar(0, 0, 46, a0 + 45)
        p.wedge(600 + mx, 400 + my, 250, a0, a0 + 90, col)
    return p.render("A disc split into four quadrants, fanned apart, each a "
                    "different colour")


def grack():
    """A request driven straight down through a stack."""
    p = Poster("sky")
    for i in range(3):
        p.bar(240, 176 + i * 150, 720, 108, PP["ink"], r=16)
    p.bar(545, 130, 110, 500, PP["cream"], r=12)
    p.disc(600, 672, 62, PP["vermilion"])
    return p.render("Three stacked slabs pierced by a vertical bar ending in a disc")


def git_media():
    """Enormous becomes tiny."""
    p = Poster("magenta")
    p.disc(430, 400, 268, PP["cream"])
    p.bar(700, 380, 200, 40, PP["ink"], r=20)
    p.disc(960, 400, 46, PP["ink"])
    return p.render("A very large disc joined by a bar to a very small one")


def hg_git():
    """Two halves, traffic both ways."""
    p = Poster("vermilion")
    p.half(430, 400, 232, "left", PP["cream"])
    p.half(770, 400, 232, "right", PP["ink"])
    p.bar(400, 336, 400, 44, PP["cream"], r=22)
    p.bar(400, 420, 400, 44, PP["ink"], r=22)
    return p.render("Two facing half discs bridged by two bars, one in each "
                    "direction")




def desks_project():
    """A permutation matrix — one pick per row and column."""
    p = Poster("cream")
    picks = {0: 2, 1: 0, 2: 4, 3: 1, 4: 3}
    cell, gap = 108, 18
    x0 = (W - (5 * cell + 4 * gap)) / 2
    y0 = (H - (5 * cell + 4 * gap)) / 2
    for r in range(5):
        for c in range(5):
            hit = picks[r] == c
            p.bar(x0 + c * (cell + gap), y0 + r * (cell + gap), cell, cell,
                  PP["vermilion"] if hit else PP["sand"], r=14)
    return p.render("A five by five grid with exactly one highlighted cell per "
                    "row and column")


PROJECT_POSTERS = {
    "micro-manager": micro_manager,
    "ticgit": ticgit,
    "unfurler": unfurler_project,
    "soe": soe,
    "slidetty": slidetty,
    "showoff": showoff,
    "git-scribe": git_scribe,
    "grack": grack,
    "git-media": git_media,
    "hg-git": hg_git,
    "hungarian-desks": desks_project,
}


if __name__ == "__main__":
    for scene in SCENES:
        scene()
    for slug, poster in PROJECT_POSTERS.items():
        save_project(slug, poster())
    print("done:", len(SCENES), "covers,", len(PROJECT_POSTERS), "project posters")
