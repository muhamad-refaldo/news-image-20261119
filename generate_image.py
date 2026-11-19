#!/usr/bin/env python3
"""Generate entry.png v2 - 1024x1024 poster of world news, 19 Nov 2026.
Deterministic: no network, no random, no timestamps, fixed fonts/colours.
Run: python3 generate_image.py  -> writes entry.png next to this file.

v2 is a poster, not a newspaper: one lead story on top, then five
picture-led cards. Headlines are short enough to read at a glance and
every card's picture is drawn big and simple, so the day's stories are
clear from the pictures and the headlines alone. Same six stories and
same facts as v1, only the composition, the pictures and the wording
of the short summaries are new.
"""
from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
PAPER = (247, 243, 232)
DARK = (15, 32, 64)
AMBER = (201, 162, 39)
BLACK = (22, 22, 22)
GREY = (88, 88, 88)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)
EDGE = (218, 212, 198)

BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def typeface(px, bold=True):
    return ImageFont.truetype(BOLD_PATH if bold else REG_PATH, px)


def split_text(text, face, width, limit):
    """Greedy word wrap, at most `limit` lines, each within `width` px."""
    out = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if face.getlength(trial) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
            if len(out) >= limit:
                break
    if current and len(out) < limit:
        out.append(current)
    return out


def rounded(d, box, radius, fill, outline=None):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline,
                        width=1 if outline else 0)


# ---------------------------------------------------------------- pictures
# Every picture is drawn from lines, arcs and rectangles in white on a
# coloured panel. No photos, no copied artwork.

def pic_towers(d, cx, cy, s):
    """Three towers with a flag on the tallest one."""
    ground = cy + s * 0.40
    d.line([(cx - s * 0.78, ground), (cx + s * 0.78, ground)],
           fill=WHITE, width=7)
    for shift, tall in ((-0.60, 0.66), (-0.14, 0.95), (0.34, 0.74)):
        left = cx + shift * s
        right = left + s * 0.26
        top = ground - tall * s
        d.rectangle([left, top, right, ground], fill=WHITE)
        for row in range(3):
            wy = top + s * 0.10 + row * s * 0.17
            if wy < ground - s * 0.05:
                d.rectangle([left + s * 0.05, wy, right - s * 0.05,
                             wy + s * 0.05], fill=DARK)
    tip = cx + 0.26 * s
    d.line([(tip, cy - s * 0.55), (tip, cy - s * 0.95)], fill=WHITE, width=5)
    d.polygon([(tip, cy - s * 0.95), (tip + s * 0.30, cy - s * 0.86),
               (tip, cy - s * 0.77)], fill=AMBER)


def pic_fire(d, cx, cy, s):
    """Flame over waves: a teardrop silhouette with an inner flame."""
    tip = (cx + s * 0.10, cy - s * 0.62)
    outline = [
        (cx - s * 0.34, cy + s * 0.30),
        (cx - s * 0.40, cy - s * 0.02),
        (cx - s * 0.22, cy - s * 0.34),
        tip,
        (cx + s * 0.30, cy - s * 0.28),
        (cx + s * 0.40, cy + s * 0.02),
        (cx + s * 0.34, cy + s * 0.30),
    ]
    d.polygon(outline, fill=WHITE)
    inner = [
        (cx - s * 0.14, cy + s * 0.22),
        (cx - s * 0.17, cy - s * 0.02),
        (cx + s * 0.02, cy - s * 0.26),
        (cx + s * 0.15, cy - s * 0.06),
        (cx + s * 0.17, cy + s * 0.22),
    ]
    d.polygon(inner, fill=AMBER)
    for dy, wide in ((0.44, 0.55), (0.58, 0.68)):
        d.arc([cx - wide * s, cy + dy * s, cx + wide * s, cy + (dy + 0.20) * s],
              start=180, end=360, fill=WHITE, width=6)


def pic_broken_bridge(d, cx, cy, s):
    """A bridge deck snapped in the middle, the right half tilted down."""
    deck = cy - s * 0.16
    gap = s * 0.12
    d.line([(cx - s * 0.78, deck), (cx - gap, deck)], fill=WHITE, width=9)
    d.line([(cx + gap, deck), (cx + s * 0.78, deck + s * 0.26)],
           fill=WHITE, width=9)
    for px in (-0.58, 0.58):
        x = cx + px * s
        top = deck if px < 0 else deck + s * 0.20
        d.line([(x, top), (x, deck + s * 0.42)], fill=WHITE, width=8)
    d.line([(cx - s * 0.10, deck + s * 0.22), (cx + s * 0.16, deck + s * 0.34)],
           fill=AMBER, width=9)
    for dy in (0.62, 0.74):
        d.arc([cx - s * 0.60, cy + dy * s, cx + s * 0.60,
               cy + (dy + 0.16) * s], start=180, end=360, fill=WHITE, width=6)


def pic_missile_tower(d, cx, cy, s):
    """A tower struck by a missile: impact star where it hits."""
    base = cy + s * 0.48
    d.rectangle([cx - s * 0.30, cy - s * 0.30, cx + s * 0.02, base],
                fill=WHITE)
    d.line([(cx - s * 0.14, cy - s * 0.30), (cx - s * 0.14, cy - s * 0.62)],
           fill=WHITE, width=5)
    for row in range(3):
        wy = cy - s * 0.16 + row * s * 0.20
        d.rectangle([cx - s * 0.24, wy, cx - s * 0.04, wy + s * 0.07],
                    fill=DARK)
    d.line([(cx - s * 0.70, base), (cx + s * 0.70, base)], fill=WHITE, width=7)
    hx, hy = cx + s * 0.62, cy - s * 0.62
    d.line([(cx + s * 0.10, cy - s * 0.10), (hx, hy)], fill=WHITE, width=6)
    d.polygon([(hx, hy), (hx + s * 0.16, hy - s * 0.06),
               (hx + s * 0.04, hy + s * 0.12)], fill=WHITE)
    ix, iy = cx - s * 0.02, cy - s * 0.28
    for dx, dy in ((0, -0.16), (0.12, -0.05), (0.16, 0.08), (0.05, 0.14),
                   (-0.06, 0.14), (-0.16, 0.06), (-0.12, -0.06)):
        d.line([(ix, iy), (ix + dx * s, iy + dy * s)], fill=AMBER, width=6)


def pic_scales(d, cx, cy, s):
    """Scales of justice: post, beam, two pans, base."""
    d.line([(cx, cy - s * 0.60), (cx, cy + s * 0.48)], fill=WHITE, width=7)
    d.line([(cx - s * 0.62, cy - s * 0.44), (cx + s * 0.62, cy - s * 0.44)],
           fill=WHITE, width=7)
    d.ellipse([cx - s * 0.10, cy - s * 0.72, cx + s * 0.10, cy - s * 0.52],
              fill=AMBER)
    for side in (-1, 1):
        px = cx + side * s * 0.62
        d.line([(px, cy - s * 0.44), (px - s * 0.20, cy - s * 0.06)],
               fill=WHITE, width=5)
        d.line([(px, cy - s * 0.44), (px + s * 0.20, cy - s * 0.06)],
               fill=WHITE, width=5)
        d.arc([px - s * 0.24, cy - s * 0.14, px + s * 0.24, cy + s * 0.22],
              start=0, end=180, fill=WHITE, width=6)
    d.line([(cx - s * 0.42, cy + s * 0.48), (cx + s * 0.42, cy + s * 0.48)],
           fill=WHITE, width=7)


def pic_rocket(d, cx, cy, s):
    """A rocket lifting off, with a star beside it."""
    d.polygon([(cx - s * 0.18, cy + s * 0.28), (cx - s * 0.18, cy - s * 0.22),
               (cx, cy - s * 0.58), (cx + s * 0.18, cy - s * 0.22),
               (cx + s * 0.18, cy + s * 0.28)], fill=WHITE)
    d.ellipse([cx - s * 0.09, cy - s * 0.28, cx + s * 0.09, cy - s * 0.10],
              fill=DARK)
    d.polygon([(cx - s * 0.18, cy + s * 0.10), (cx - s * 0.42, cy + s * 0.42),
               (cx - s * 0.18, cy + s * 0.32)], fill=WHITE)
    d.polygon([(cx + s * 0.18, cy + s * 0.10), (cx + s * 0.42, cy + s * 0.42),
               (cx + s * 0.18, cy + s * 0.32)], fill=WHITE)
    d.polygon([(cx - s * 0.12, cy + s * 0.30), (cx + s * 0.12, cy + s * 0.30),
               (cx, cy + s * 0.62)], fill=AMBER)
    sx, sy = cx + s * 0.62, cy - s * 0.52
    for dx, dy in ((0, -0.14), (0.10, -0.04), (0.13, 0.08), (0.04, 0.12),
                   (-0.05, 0.12), (-0.13, 0.06), (-0.10, -0.05)):
        d.line([(sx, sy), (sx + dx * s, sy + dy * s)], fill=AMBER, width=5)


# ---------------------------------------------------------------- stories
# Same six stories and same facts as v1.

ITEMS = [
    dict(num="01", tag="LEAD STORY  •  SHENZHEN SUMMIT",
         head="Trump, Xi & Putin meet",
         body=("First-ever US–China–Russia trilateral talks open in "
               "Shenzhen. After 90 minutes, the three leaders announce "
               "a peace declaration."),
         colour=DARK, pic=pic_towers, hero=True),
    dict(num="02", tag="GULF ESCALATION",
         head="Iran hits Kuwait & Bahrain",
         body=("Iran widens attacks on Kuwait and Bahrain. Three "
               "tankers hit mines near Hormuz."),
         colour=(140, 47, 47), pic=pic_fire),
    dict(num="03", tag="KERCH BRIDGE HIT AGAIN",
         head="Ukraine strikes a third time",
         body=("A third Ukrainian strike in four days halts rail "
               "traffic on the Kerch Bridge."),
         colour=(31, 92, 61), pic=pic_broken_bridge),
    dict(num="04", tag="RIYADH & GAZA",
         head="Missile hits Riyadh tower",
         body=("A Houthi missile hits Riyadh's wealth-fund tower. "
               "Israel acts near Gaza's Nuseirat camp."),
         colour=(122, 74, 31), pic=pic_missile_tower),
    dict(num="05", tag="MYANMAR GENOCIDE RULING",
         head="UN court rules on Rohingya",
         body=("The UN court rules Myanmar committed state-sponsored "
               "genocide against the Rohingya."),
         colour=(75, 46, 107), pic=pic_scales),
    dict(num="06", tag="GTA VI & VOYAGER 1",
         head="A launch, and a first in space",
         body=("Grand Theft Auto VI launches to global fanfare. Voyager 1 "
               "becomes the first human-made object one light-day from "
               "Earth."),
         colour=(15, 95, 107), pic=pic_rocket),
]


def draw_story_card(d, item, x, y, w, h, pic_w, hero=False):
    """One picture-led card: coloured picture panel left, words right."""
    rounded(d, [x, y, x + w, y + h], 14, PANEL, EDGE)
    d.rounded_rectangle([x, y, x + pic_w, y + h], radius=14, fill=item["colour"])
    d.rectangle([x + pic_w - 14, y, x + pic_w, y + h], fill=item["colour"])
    item["pic"](d, x + pic_w // 2, y + h // 2, 92 if hero else 78)
    tx = x + pic_w + 20
    tw = w - pic_w - 40
    kick = typeface(21 if hero else 19)
    d.text((tx, y + 16), item["tag"], font=kick, fill=item["colour"])
    head_lines = split_text(item["head"], typeface(38 if hero else 29),
                            tw, 2)
    hy = y + 46 if hero else y + 44
    for line in head_lines:
        d.text((tx, hy), line, font=typeface(38 if hero else 29), fill=BLACK)
        hy += 44 if hero else 34
    body_lines = split_text(item["body"], typeface(20 if hero else 18, False),
                            tw, 3)
    by = hy + 6
    for line in body_lines:
        d.text((tx, by), line, font=typeface(20 if hero else 18, False),
               fill=GREY)
        by += 26 if hero else 23


def build():
    img = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    d = ImageDraw.Draw(img)

    # Header.
    d.rectangle([0, 0, CANVAS, 148], fill=DARK)
    d.text((28, 16), "WORLD NEWS  •  IN ONE IMAGE", font=typeface(25),
           fill=AMBER)
    d.text((28, 48), "19 NOVEMBER 2026", font=typeface(62), fill=WHITE)
    d.text((28, 116), "Thursday  •  Six stories that shaped the world that day",
           font=typeface(20, False), fill=(205, 210, 225))
    badge = [CANVAS - 208, 26, CANVAS - 28, 122]
    d.rounded_rectangle(badge, radius=12, outline=AMBER, width=3)
    d.text((CANVAS - 190, 38), "19 NOV", font=typeface(34), fill=WHITE)
    d.text((CANVAS - 178, 78), "2026", font=typeface(28), fill=AMBER)
    d.rectangle([0, 148, CANVAS, 154], fill=AMBER)

    margin = 24
    col_w = (CANVAS - margin * 2 - 16) // 2
    lead = ITEMS[0]
    draw_story_card(d, lead, margin, 170, CANVAS - margin * 2, 196, 288,
                    hero=True)
    y = 382
    for row in (ITEMS[1:3], ITEMS[3:5]):
        for i, item in enumerate(row):
            draw_story_card(d, item, margin + i * (col_w + 16), y, col_w,
                            208, 140)
        y += 224
    draw_story_card(d, ITEMS[5], margin, y, CANVAS - margin * 2, 148, 168)

    # Footer.
    d.rectangle([0, CANVAS - 44, CANVAS, CANVAS], fill=DARK)
    d.text((28, CANVAS - 32),
           "Summarised from reports published on 19 November 2026  •  "
           "No single story tells the whole day",
           font=typeface(18, False), fill=(205, 210, 225))
    return img


if __name__ == "__main__":
    build().save("entry.png", "PNG")
