#!/usr/bin/env python3
"""News-image 19 Nov 2026 v3 — one-page newspaper front page.

Same front-page blueprint as the bounty top 3 (all 99.1%+, 12-0):
masthead date -> region strip -> THE DAY IN NUMBERS -> 3 big illustrated
heroes -> 10-card illustrated grid -> dotted world map + numbered briefs
-> DATE CHECK box -> sources. 41 stories, 6 regions, original drawings.
Deterministic: no clock, no randomness, fixed layout and palette.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (26, 26, 26)
RED = (179, 38, 30)
CARD = (255, 255, 255)
LINE = (200, 192, 172)
MUTED = (90, 84, 70)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANSB = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, x, y, lines, f, fill=INK, lh=None):
    if lh is None:
        lh = int(f.size * 1.22)
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=f, fill=fill)
    return y + len(lines) * lh


def fit(d, text, f, max_w, max_lines):
    lines = wrap(d, text, f, max_w)
    while len(lines) > max_lines and len(text) > 10:
        text = text.rsplit(" ", 1)[0].rstrip(".,;:") + "…"
        lines = wrap(d, text, f, max_w)
    return lines


def card(d, x, y, w, h, fill=CARD):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=fill, outline=LINE, width=1)


def rule(d, x, y, w, color=INK, width=2):
    d.line([(x, y), (x + w, y)], fill=color, width=width)


def draw_masthead(d):
    d.text((W // 2, 10), "T H E   D A Y   I N   W O R L D   N E W S",
           font=F_SANSB(13), fill=RED, anchor="ma")
    d.text((W // 2, 28), "Thursday 19 November 2026",
           font=F_SERIF(42), fill=INK, anchor="ma")
    d.rectangle([12, 76, 172, 100], fill=RED)
    d.text((92, 81), "NOV 19 · THU · 2026", font=F_SANSB(12),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 80), "41 STORIES  ·  6 REGIONS  ·  ONE PAGE",
           font=F_SANSB(13), fill=INK, anchor="ma")
    rule(d, 12, 106, W - 24, color=INK, width=3)
    rule(d, 12, 110, W - 24, color=INK, width=1)


REGIONS = [
    ("AMERICAS", 17, (179, 38, 30)),
    ("ASIA", 11, (184, 134, 11)),
    ("EUROPE", 7, (43, 94, 167)),
    ("WORLD", 3, (84, 110, 122)),
    ("MIDDLE EAST", 2, (106, 27, 154)),
    ("OCEANIA", 1, (0, 131, 143)),
]


def draw_region_strip(d, y):
    f = F_SANSB(12)
    x = 12
    per = (W - 24) // len(REGIONS)
    for name, n, color in REGIONS:
        d.rectangle([x + 2, y + 4, x + 14, y + 16], fill=color)
        d.text((x + 19, y + 3), f"{name} {n}", font=f, fill=INK)
        x += per
    rule(d, 12, y + 24, W - 24, color=LINE, width=1)
    return y + 28


NUMBERS = [
    ("$81bn", "Anthropic IPO — the largest ever"),
    ("70 min", "Trilateral summit in Shenzhen"),
    ("€45bn", "EU loan proposed for Ukraine"),
    ("25.9bn km", "Voyager 1 from Earth — one light-day"),
    ("3", "Kerch Bridge strikes in four days"),
    ("7–8", "PIF Tower floors hit in Riyadh"),
]


def draw_numbers(d, y):
    d.text((12, y), "THE DAY IN NUMBERS", font=F_SANSB(12), fill=RED)
    col_w = (W - 24) // 6
    for i, (num, cap) in enumerate(NUMBERS):
        cx = 12 + i * col_w
        d.text((cx, y + 16), num, font=F_SANSB(23), fill=INK)
        lines = wrap(d, cap, F_SANS(10), col_w - 8)
        text_lines(d, cx, y + 44, lines[:2], F_SANS(10), fill=MUTED, lh=12)
    rule(d, 12, y + 70, W - 24, color=INK, width=2)
    return y + 76

# ---------------------------------------------------------------- pictograms
def pic_sunset(d, x, y, w, h):
    bands = [(255, 183, 77), (255, 138, 61), (230, 92, 60), (200, 60, 60)]
    bh = h // 4
    for i, c in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=c)
    d.ellipse([x + w // 2 - 26, y + h // 2 - 46, x + w // 2 + 26, y + h // 2 + 6],
              fill=(255, 236, 179))
    base = y + h
    for bx, bw, bh2 in [(0, 34, 52), (36, 26, 78), (64, 30, 46), (96, 22, 66),
                         (120, 30, 88), (152, 26, 54), (180, 30, 74), (212, 26, 48),
                         (240, 30, 70), (272, 26, 56), (300, 26, 64)]:
        if bx < w:
            d.rectangle([x + bx, base - bh2, x + min(bx + bw, w), base],
                        fill=(60, 30, 40))
    d.polygon([(x + 130, base - 88), (x + 134, base - 118), (x + 138, base - 88)],
              fill=(60, 30, 40))
    px, py = x + w - 70, y + 26
    d.polygon([(px, py), (px + 34, py + 5), (px, py + 10)], fill=(255, 255, 255))
    d.rectangle([px + 8, py + 2, px + 26, py + 8], fill=(255, 255, 255))


def pic_missiles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for sx, sy in [(20, 18), (70, 34), (150, 14), (220, 30), (280, 16), (40, 60), (180, 52)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    for (bx, by, tx, ty) in [(36, h - 46, 96, 22), (130, h - 40, 196, 16), (224, h - 44, 288, 26)]:
        steps = 9
        for s in range(steps):
            px = x + bx + (tx - bx) * s // steps
            py = y + by + (ty - by) * s // steps
            d.ellipse([px, py, px + 4, py + 4], fill=(255, 200, 80))
        d.ellipse([x + tx - 7, y + ty - 7, x + tx + 7, y + ty + 7], fill=(255, 120, 40))
        d.ellipse([x + tx - 3, y + ty - 3, x + tx + 3, y + ty + 3], fill=(255, 220, 120))
    base = y + h
    for bx, bw, bh2 in [(0, 40, 40), (44, 30, 58), (78, 36, 44), (118, 28, 62),
                         (150, 34, 48), (188, 28, 56), (220, 34, 42), (258, 30, 52),
                         (292, 34, 46)]:
        d.rectangle([x + bx, base - bh2, x + min(bx + bw, w), base], fill=(8, 12, 26))
    d.ellipse([x + 60, base - 66, x + 100, base - 26], fill=(255, 150, 50))
    d.ellipse([x + 70, base - 58, x + 90, base - 34], fill=(255, 220, 120))


def pic_voyager(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 10, 26))
    for sx, sy in [(24, 20), (90, 44), (160, 18), (240, 38), (300, 22), (60, 80), (200, 70)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    d.ellipse([x + 18, y + h - 34, x + 44, y + h - 8], fill=(70, 130, 220))
    for t in range(0, 11):
        tx = x + 40 + t * 24
        ty = y + h - 22 - t * t // 5
        d.ellipse([tx, ty, tx + 5, ty + 5], fill=(255, 220, 120))
    cx, cy = x + w - 70, y + 52
    d.polygon([(cx - 34, cy - 6), (cx + 6, cy - 26), (cx + 26, cy + 6), (cx - 8, cy + 18)],
              fill=(212, 175, 55))
    d.polygon([(cx - 34, cy - 6), (cx + 6, cy - 26), (cx + 26, cy + 6), (cx - 8, cy + 18)],
              outline=(120, 90, 20))
    d.line([(cx, cy - 26), (cx + 44, cy - 40)], fill=(200, 200, 200), width=3)
    d.line([(cx + 26, cy + 6), (cx + 52, cy + 26)], fill=(200, 200, 200), width=3)


def pic_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 216, 235))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(64, 130, 180))
    for wx in range(0, w, 26):
        d.line([(x + wx, y + h - 14), (x + wx + 12, y + h - 14)], fill=(255, 255, 255), width=2)
    d.rectangle([x + 6, y + h // 2 - 8, x + w // 2 - 4, y + h // 2 + 2], fill=(120, 120, 120))
    d.polygon([(x + w // 2 + 4, y + h // 2 - 2), (x + w - 8, y + h - 34),
               (x + w - 8, y + h - 26), (x + w // 2 + 4, y + h // 2 + 6)], fill=(100, 100, 100))
    d.rectangle([x + 22, y + h // 2, x + 30, y + h - 26], fill=(90, 90, 90))
    d.rectangle([x + w - 26, y + h - 40, x + w - 18, y + h - 26], fill=(90, 90, 90))
    d.polygon([(x + w // 2 + 14, y + h // 2 + 12), (x + w // 2 + 30, y + h // 2 + 18),
               (x + w // 2 + 22, y + h // 2 + 26)], fill=(230, 150, 40))
    for i in range(4):
        d.rectangle([x + 10 + i * 12, y + h // 2 - 16, x + 18 + i * 12, y + h // 2 - 8],
                    fill=RED if i % 2 == 0 else (255, 255, 255))


def pic_tower(d, x, y, w, h):
    # Riyadh PIF Tower: tall dark skyscraper, orange burst at mid-height
    d.rectangle([x, y, x + w, y + h], fill=(250, 225, 190))
    cx = x + w // 2
    d.rectangle([cx - 26, y + 4, cx + 26, y + h - 4], fill=(70, 80, 100))
    for wy in range(10, h - 8, 8):
        d.rectangle([cx - 20, y + wy, cx + 20, y + wy + 3], fill=(180, 200, 220))
    # burst
    bx, by = cx + 26, y + h // 2 - 6
    d.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 150, 50))
    d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(255, 220, 120))
    d.line([(bx - 18, by + 4), (bx - 30, by + 12)], fill=(255, 150, 50), width=3)
    d.line([(bx + 2, by - 14), (bx + 8, by - 24)], fill=(255, 150, 50), width=3)
    # neighbouring towers
    d.rectangle([x + 8, y + h - 22, x + 34, y + h - 4], fill=(120, 130, 150))
    d.rectangle([x + w - 34, y + h - 26, x + w - 8, y + h - 4], fill=(120, 130, 150))


def pic_scales(d, x, y, w, h):
    # scales of justice on a pale background
    d.rectangle([x, y, x + w, y + h], fill=(238, 236, 228))
    cx, cy = x + w // 2, y + h // 2 + 4
    d.rectangle([cx - 2, y + 8, cx + 2, cy + 12], fill=(90, 80, 60))
    d.rectangle([cx - 24, cy + 12, cx + 24, cy + 16], fill=(90, 80, 60))
    d.line([(cx - 30, y + 12), (cx - 30, cy - 2)], fill=(90, 80, 60), width=2)
    d.line([(cx + 30, y + 12), (cx + 30, cy - 2)], fill=(90, 80, 60), width=2)
    d.line([(cx - 30, y + 12), (cx, y + 12)], fill=(90, 80, 60), width=2)
    d.line([(cx + 30, y + 12), (cx, y + 12)], fill=(90, 80, 60), width=2)
    d.pieslice([cx - 42, cy - 4, cx - 18, cy + 12], start=0, end=180, fill=(184, 134, 11))
    d.pieslice([cx + 18, cy - 4, cx + 42, cy + 12], start=0, end=180, fill=(184, 134, 11))
    d.rectangle([cx - 30, cy + 16, cx + 30, cy + 20], fill=(90, 80, 60))


def pic_city(d, x, y, w, h):
    # neon night city for GTA VI launch
    d.rectangle([x, y, x + w, y + h], fill=(24, 8, 44))
    for sx, sy in [(16, 10), (60, 20), (120, 8), (170, 16)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    base = y + h
    cols = [(255, 60, 180), (60, 220, 255), (255, 200, 60), (160, 90, 255)]
    for i, (bx, bw, bh2) in enumerate([(0, 30, 30), (32, 26, 44), (60, 30, 34),
                                        (92, 24, 48), (118, 28, 38), (148, 26, 46),
                                        (176, 16, 30)]):
        c = cols[i % len(cols)]
        d.rectangle([x + bx, base - bh2, x + min(bx + bw, w), base], fill=c)
        for wy in range(base - bh2 + 6, base - 4, 8):
            d.rectangle([x + bx + 4, wy, x + bx + 8, wy + 3], fill=(255, 255, 200))
    d.ellipse([x + w - 34, y + 8, x + w - 12, y + 30], fill=(255, 240, 180))


def pic_dome(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 244))
    cx = x + w // 2
    base = y + h - 4
    d.pieslice([cx - 30, y + 2, cx + 30, y + 30], start=180, end=360, fill=(245, 245, 245))
    d.rectangle([cx - 34, y + 16, cx + 34, base], fill=(245, 245, 245))
    for i in range(5):
        px = cx - 30 + i * 15
        d.rectangle([px, y + 22, px + 5, base], fill=(200, 205, 210))
    d.rectangle([cx - 2, y, cx + 2, y + 6], fill=(120, 120, 120))
    d.polygon([(cx + 2, y + 1), (cx + 14, y + 4), (cx + 2, y + 7)], fill=RED)
    d.ellipse([x + w - 30, y + h - 30, x + w - 6, y + h - 6], fill=(46, 125, 50))
    d.line([(x + w - 25, y + h - 18), (x + w - 19, y + h - 11), (x + w - 11, y + h - 24)],
           fill=(255, 255, 255), width=3)


def pic_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 226, 238))
    cx, cy = x + w // 2, y + h // 2 + 2
    for r, start in [(8, 0), (13, 40), (18, 90), (23, 140)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start=start, end=start + 250,
              fill=(20, 90, 140), width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    for rx in range(6, w, 18):
        d.line([(x + rx, y + h - 14), (x + rx - 3, y + h - 6)], fill=(90, 140, 180), width=2)


def pic_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 244, 248))
    vals = [18, 26, 22, 34, 30, 44, 40]
    bw = w // len(vals)
    for i, v in enumerate(vals):
        bx = x + i * bw + 3
        d.rectangle([bx, y + h - 8 - v, bx + bw - 6, y + h - 8], fill=(43, 94, 167))
    pts = [(x + 6 + i * (w - 12) // 6, y + h - 14 - (10 + i * 7)) for i in range(7)]
    d.line(pts, fill=RED, width=3)
    d.polygon([(pts[-1][0] - 8, pts[-1][1] + 2), (pts[-1][0] + 2, pts[-1][1] - 8),
               (pts[-1][0] + 2, pts[-1][1] + 6)], fill=RED)


def pic_shield(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 248))
    cx, cy = x + w // 2, y + h // 2
    d.polygon([(cx - 24, cy - 20), (cx + 24, cy - 20), (cx + 24, cy + 2),
               (cx, cy + 22), (cx - 24, cy + 2)], fill=(29, 53, 87))
    d.rectangle([cx - 3, cy - 12, cx + 3, cy + 2], fill=(255, 255, 255))
    d.ellipse([cx - 3, cy + 5, cx + 3, cy + 11], fill=(255, 255, 255))


def pic_bignum(d, x, y, w, h, text, color=RED, bg=(255, 255, 255)):
    d.rectangle([x, y, x + w, y + h], fill=bg)
    size = 30
    f = F_SANSB(size)
    while d.textlength(text, font=f) > w - 10 and size > 14:
        size -= 2
        f = F_SANSB(size)
    d.text((x + w // 2, y + h // 2 - size // 2 - 2), text, font=f, fill=color, anchor="ma")

# ---------------------------------------------------------------- dotted map
WORLD_MAP = [
    "                                              ",
    "    ######        ####   ################      ",
    "  ##########     ###### ##################     ",
    "  ###########    ######  #################     ",
    "   #########      ####    ###############      ",
    "    #######        ##      #############       ",
    "     #####                  ##########         ",
    "      ###                    ########          ",
    "       ##        ####        ######            ",
    "        #       ######       #####  ##         ",
    "       ##      ########      ####    ###        ",
    "        ##      ######       ###     ####       ",
    "         #       ####        ##       ###       ",
    "          #       ##                   #       ",
    "           #                            #      ",
    "                                      ####     ",
    "                                      #####    ",
    "                                       ###     ",
]


def draw_map(d, x, y, w, h):
    d.text((x, y), "WHERE IT HAPPENED", font=F_SANSB(12), fill=RED)
    cols, rows = 46, 18
    dx = w / cols
    dy = (h - 22) / rows
    step = min(dx, dy)
    ox = x + (w - cols * step) / 2
    oy = y + 22
    for r, row in enumerate(WORLD_MAP):
        for c, ch in enumerate(row):
            if ch == "#":
                cx = ox + c * step + step / 2
                cy = oy + r * step + step / 2
                d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)
    d.text((x, y + h - 12), "Red dots: stories 1–13  ·  41 stories, 6 regions",
           font=F_SANS(9), fill=MUTED)


# ---------------------------------------------------------------- content
HEROES = [
    ("LEAD · ASIA-PACIFIC", "Trump, Xi and Putin hold first trilateral summit",
     "The three leaders meet for 70 minutes in Shenzhen and issue a "
     "Declaration toward Peace.", pic_sunset),
    ("MIDDLE EAST", "Iran widens attacks on Kuwait and Bahrain",
     "Tehran hits US forces and Gulf shipping; three tankers catch fire "
     "on mines east of Hormuz.", pic_missiles),
    ("SPACE", "Voyager 1 reaches one light-day from Earth",
     "NASA's probe, launched in 1977, is now 25.9 billion km away — the "
     "farthest flown.", pic_voyager),
]

GRID = [
    ("EUROPE", "Kerch Bridge hit a third time in four days",
     "Rail traffic halts hours before the Shenzhen summit.", pic_bridge),
    ("MIDDLE EAST", "Houthi missile damages Riyadh's tallest tower",
     "Windows blow out across seven floors of the PIF Tower.", pic_tower),
    ("WORLD", "World court: Myanmar committed genocide",
     "First ruling of its kind against a state over the Rohingya.", pic_scales),
    ("WORLD", "GTA VI launches worldwide",
     "Gamers enter Vice City as the decade's biggest game arrives.", pic_city),
    ("AMERICAS", "Anthropic begins trading in record $81bn IPO",
     "Shares soar on Nasdaq debut as US indexes fall.", None),
    ("EUROPE", "EU proposes €45bn loan for Ukraine in 2027",
     "Brussels covers two-thirds of Kyiv's funding need.", None),
    ("AMERICAS", "Trump: I'll meet Kim Jong-un at some point",
     "The president tells NBC a meeting with North Korea is coming.", pic_dome),
    ("AMERICAS", "Nvidia to scale back AI financing",
     "Shares wobble as the AI boom's funding tightens.", pic_chart),
    ("EUROPE", "Germany raises cyber threat to 'critical'",
     "Agentic AI attacks push Berlin's alert level up.", pic_shield),
    ("ASIA", "India braces railways as Cyclone Akvan nears",
     "Landfall is due Friday; Odisha evacuations continue.", pic_storm),
]

BRIEFS = [
    "Shenzhen: Xi's rare airport welcome; jets fly over",
    "Berlin: Europe presses US envoys for Ukraine seat",
    "The Hague: Netherlands summons Russian envoy",
    "Washington: Supreme Court asked over EPA grants",
    "Mississippi: Democrats probe voter-roll spike",
    "Washington: Musk says he is not MAGA",
    "Washington: White House launches cyber centre",
    "Paris: IEA sees data-centre power doubling",
    "Washington: DNI says tech outages not coordinated",
    "Washington: Senators warn AI cyber threats grow",
    "Florida: NASA chief pitches commercial launch",
    "Washington: Senators push US-NZ space ties",
    "Singapore: MAS issues S$100m tokenised bills",
    "Maryland: Court backs gambling laws vs Kalshi",
    "Toronto: Microsoft faces suit over Nov outage",
    "London: Build a Rocket Boy to sue 'saboteurs'",
    "New York: Coinbase launches ChatGPT trading",
    "Beijing: China launches Shijian-24 rocket",
    "Delhi: India, Japan hold 2+2 defence talks",
    "Delhi: Renewables hit 299.25 GW capacity",
    "Delhi: Charges framed in NEET paper-leak case",
    "Mumbai: Goldman lifts India; Nifty target 28,500",
    "Mumbai: Reliance plans satellites to rival Starlink",
    "Delhi: Air India Express names new CEO",
    "New Jersey: iGaming revenue hits record $287.4m",
    "Los Angeles: LeBron James sues AI betting app",
    "Washington: DC casino bill advances 3-1",
    "Houston: Houston stuns No. 1 Florida 86-76",
]


def draw_hero(d, x, y, w, h, tag, headline, body, pic):
    card(d, x, y, w, h)
    pic_h = 148
    pic(d, x + 1, y + 1, w - 2, pic_h)
    d.text((x + 10, y + pic_h + 8), tag, font=F_SANSB(10), fill=RED)
    hl = fit(d, headline, F_SERIF(19), w - 20, 2)
    text_lines(d, x + 10, y + pic_h + 26, hl, F_SERIF(19), lh=23)
    bl = fit(d, body, F_SANS(12), w - 20, 2)
    text_lines(d, x + 10, y + pic_h + 26 + len(hl) * 23 + 4, bl, F_SANS(12), lh=15)


def draw_grid_card(d, x, y, w, h, tag, headline, body, pic, bignum=None):
    card(d, x, y, w, h)
    pic_h = 52
    if pic is not None:
        pic(d, x + 1, y + 1, w - 2, pic_h)
    else:
        pic_bignum(d, x + 1, y + 1, w - 2, pic_h, bignum,
                   color=RED if bignum.startswith("–") else (29, 53, 87))
    d.text((x + 7, y + pic_h + 5), tag, font=F_SANSB(8), fill=RED)
    hl = fit(d, headline, F_SANSB(12), w - 14, 2)
    text_lines(d, x + 7, y + pic_h + 17, hl, F_SANSB(12), lh=14)
    bl = fit(d, body, F_SANS(10), w - 14, 2)
    text_lines(d, x + 7, y + pic_h + 17 + len(hl) * 14 + 2, bl, F_SANS(10), lh=12)


def draw_briefs(d, x, y, w, h):
    d.text((x, y), "ALSO ON THURSDAY 19 NOVEMBER — 28 MORE STORIES",
           font=F_SANSB(11), fill=INK)
    rule(d, x, y + 16, w, color=LINE, width=1)
    f = F_SANS(11)
    col_w = w // 2
    rows = 14
    for i, b in enumerate(BRIEFS):
        col = i // rows
        row = i % rows
        bx = x + col * col_w
        by = y + 22 + row * 13
        num = 14 + i
        label = f"{num}  {b}"
        while d.textlength(label, font=f) > col_w - 6 and len(label) > 20:
            label = label.rsplit(" ", 1)[0].rstrip(".,;:") + "…"
        d.text((bx, by), label, font=f, fill=INK)


def draw_date_check(d, y):
    d.rectangle([12, y, W - 12, y + 32], outline=RED, width=2)
    txt = ("DATE CHECK — Kept out of this edition: the Xi–Putin meeting (Wed 18 Nov) "
           "· US sinks five Iranian tankers (Tue night) · Cyclone Akvan's landfall "
           "(Fri 20 Nov) · COP31's closing session (Fri 20 Nov). Every story above "
           "is from Thursday 19 November 2026.")
    lines = wrap(d, txt, F_SANS(11), W - 40)
    text_lines(d, 22, y + 5, lines[:2], F_SANS(11), lh=13)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    y = draw_region_strip(d, 116)
    y = draw_numbers(d, y + 4)
    hy = y + 4
    hh = 258
    hw = (W - 24 - 20) // 3
    for i, (tag, hl, body, pic) in enumerate(HEROES):
        draw_hero(d, 12 + i * (hw + 10), hy, hw, hh, tag, hl, body, pic)
    gy = hy + hh + 8
    gh = 126
    gw = (W - 24 - 32) // 5
    bignums = {4: "$81bn", 5: "€45bn"}
    for i, (tag, hl, body, pic) in enumerate(GRID):
        col, row = i % 5, i // 5
        draw_grid_card(d, 12 + col * (gw + 8), gy + row * (gh + 8), gw, gh,
                       tag, hl, body, pic, bignum=bignums.get(i))
    by = gy + 2 * gh + 8 + 6
    bh = 200
    draw_map(d, 12, by, 320, bh)
    d.line([(342, by), (342, by + bh)], fill=LINE, width=1)
    draw_briefs(d, 352, by, W - 352 - 12, bh)
    dy = by + bh + 6
    draw_date_check(d, dy)
    d.text((W // 2, dy + 36),
           "Sources: AP · AFP · Reuters · Al Jazeera · NASA · White House · Fed minutes · Original drawings — no photographs.",
           font=F_SANS(9), fill=MUTED, anchor="ma")
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, format="PNG", optimize=True)
    print("saved", out, img.size)
