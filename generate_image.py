#!/usr/bin/env python3
"""Generate entry.png - 1024x1024 summary of world news, 19 Nov 2026.
Deterministic: no network, no random, no timestamps, fixed fonts and colours.
Run: python3 generate_image.py  -> writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1024, 1024
BG = (247, 243, 232)
NAVY = (15, 32, 64)
NAVY2 = (27, 58, 110)
GOLD = (201, 162, 39)
INK = (20, 20, 20)
MUTED = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (220, 214, 200)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Header
d.rectangle([0, 0, W, 168], fill=NAVY)
d.rectangle([0, 168, W, 176], fill=GOLD)
d.text((48, 28), "WORLD NEWS  •  IN ONE IMAGE", font=font(24, True), fill=(201, 162, 39))
d.text((48, 58), "19 NOVEMBER 2026", font=font(58, True), fill=(255, 255, 255))
d.text((48, 124), "Thursday  •  Six stories that shaped the world that day", font=font(22), fill=(200, 210, 230))
# Date badge on right
d.rounded_rectangle([788, 36, 976, 128], radius=12, outline=(201, 162, 39), width=2)
d.text((812, 52), "19 NOV", font=font(30, True), fill=(255, 255, 255))
d.text((836, 94), "2026", font=font(24, True), fill=(201, 162, 39))

stories = [
    ("01", "SHENZHEN SUMMIT", "Trump, Xi & Putin meet",
     "First-ever US–China–Russia trilateral talks open in Shenzhen. After 90 minutes, the three leaders announce a peace declaration.", (27, 58, 110)),
    ("02", "GULF ESCALATION", "Iran hits Kuwait & Bahrain",
     "Iran widens attacks on Kuwait and Bahrain. Three oil tankers catch fire after hitting mines east of the Strait of Hormuz.", (140, 30, 30)),
    ("03", "KERCH BRIDGE HIT AGAIN", "Ukraine strikes a third time",
     "A third Ukrainian strike in four days halts rail traffic on the Kerch Bridge linking Russia to occupied Crimea.", (30, 90, 60)),
    ("04", "RIYADH & GAZA", "Missile hits Riyadh tower",
     "A Houthi missile damages Saudi Arabia's wealth-fund tower in Riyadh. Israel acts near Gaza's Nuseirat camp despite the ceasefire.", (120, 70, 20)),
    ("05", "MYANMAR GENOCIDE RULING", "UN court rules on Rohingya",
     "The UN's top court rules Myanmar committed state-sponsored genocide against the Muslim Rohingya — the first ruling of its kind.", (80, 40, 110)),
    ("06", "GTA VI & VOYAGER 1", "A launch, and a first in space",
     "Grand Theft Auto VI launches to global fanfare. Voyager 1 becomes the first human-made object one light-day from Earth.", (0, 90, 110)),
]

# 2 columns x 3 rows
x0, y0 = 32, 200
cw, ch, gap = 472, 240, 16
for i, (num, kicker, headline, body, color) in enumerate(stories):
    col = i % 2
    row = i // 2
    x = x0 + col * (cw + gap)
    y = y0 + row * (ch + gap)
    # card
    d.rounded_rectangle([x, y, x + cw, y + ch], radius=14, fill=CARD, outline=LINE, width=2)
    d.rounded_rectangle([x, y, x + cw, y + 8], radius=4, fill=color)
    d.text((x + 20, y + 22), num, font=font(22, True), fill=color)
    d.text((x + 68, y + 24), kicker, font=font(19, True), fill=color)
    d.text((x + 20, y + 56), headline, font=font(26, True), fill=INK)
    # wrap body to ~38 chars
    lines = textwrap.wrap(body, width=38)
    yy = y + 96
    for line in lines[:4]:
        d.text((x + 20, yy), line, font=font(21), fill=(50, 50, 50))
        yy += 30

# Footer
d.rectangle([0, 952, W, 1024], fill=NAVY)
d.text((48, 972), "Summarised from reports published on 19 November 2026  •  No single story tells the whole day", font=font(19), fill=(200, 210, 230))

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)
