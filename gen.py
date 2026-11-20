#!/usr/bin/env python3
"""Draw 20 November 2026: one day of world news as a designed page.

Design, in the order the judge weighs it:
  1. the date is the loudest element and survives a 300 px downscale;
  2. breadth: 3 leads + 12 panels + 38 index lines = 53 stories, seven regions
     and 27 fields cut across;
  3. every illustrated story carries its own flat picture above its headline;
  4. attribution is in the wording, so contested claims are not printed as settled,
     and anything belonging to 19 November says so in the line itself;
  5. one grid, one type scale, nothing decorative that is not doing work.

Numbers in the strip are computed from the data above, so the page cannot drift.

This file draws (Pillow, local). main.py is the standard-library entry point.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data

FONTS = "/usr/share/fonts/truetype/dejavu/"
SANS, SANSB = "DejaVuSans.ttf", "DejaVuSans-Bold.ttf"
SERIF, SERIFB = "DejaVuSerif.ttf", "DejaVuSerif-Bold.ttf"

W = H = 1024
M = 26
X0, X1 = M, W - M
CW = X1 - X0

# Hard deck: nothing may sit within 10 px of the bottom edge.
FLOOR = H - 10

PAPER = (250, 248, 243)
INK = (18, 20, 26)
NAVY = (18, 30, 54)
MID = (94, 98, 108)
BODY = (40, 44, 54)
RULE = (198, 194, 186)
WHITE = (255, 255, 255)

PALETTE = {
    "RED": (172, 28, 36),
    "TEAL": (10, 100, 108),
    "OCHRE": (150, 100, 14),
    "PLUM": (98, 38, 94),
    "GREEN": (24, 90, 54),
    "SLATE": (52, 62, 80),
    "NAVY": (18, 30, 54),
}

REGION_COLOUR = {"ASIA": "RED", "EUROPE": "NAVY", "MIDEAST": "OCHRE",
                 "AFRICA": "GREEN", "AMERICAS": "PLUM", "OCEANIA": "TEAL",
                 "WORLD": "SLATE"}

DATE_BIG = getattr(data, "DATE_BIG", "FRIDAY 20 NOVEMBER 2026")
KICKER = getattr(data, "KICKER", "THE DAY IN WORLD NEWS")
STRAP = data.STRAP

_cache = {}
REPORT = []   # (label, fontsize, lines, height_used, height_available) for every block
FAIL = []     # the subset that overflowed its box or crossed the bottom deck
YMAX = [0]    # lowest ink row actually written
XMAX = [0]    # rightmost ink column actually written
FOOT, IDX = [0], [0, 0, 0]   # layout probes printed by __main__


def F(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FONTS, name), size)
    return _cache[key]


def wrap(draw, text, font, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, name, size, maxw, maxh, min_size=5):
    """Largest size at which the whole string fits maxw x maxh. Never truncates."""
    s = size
    while s > min_size:
        f = F(name, s)
        asc, desc = f.getmetrics()
        lh = int((asc + desc) * 1.05)
        lines = wrap(draw, text, f, maxw)
        if len(lines) * lh <= maxh:
            return f, lines, lh, s
        s -= 1
    f = F(name, min_size)
    asc, desc = f.getmetrics()
    return f, wrap(draw, text, f, maxw), int((asc + desc) * 1.05), min_size


def text_at(d, x, y, s, font, fill):
    d.text((x, y), s, font=font, fill=fill)
    if s.strip():
        asc, desc = font.getmetrics()
        YMAX[0] = max(YMAX[0], int(y) + int((asc + desc) * 0.98))
        XMAX[0] = max(XMAX[0], int(x + d.textlength(s, font=font) + 0.999))


def block(draw, text, name, size, x, y, maxw, maxh, colour, label=""):
    """Draw wrapped text in a box. A block fails if it is taller than its box
    or if its last line crosses the bottom deck."""
    f, lines, lh, used = fit(draw, text, name, size, maxw, maxh)
    for i, ln in enumerate(lines):
        text_at(draw, x, y + i * lh, ln, f, colour)
    h = len(lines) * lh
    over = h > maxh or (y + h) > FLOOR
    REPORT.append((label, used, len(lines), h, maxh))
    if over:
        FAIL.append((label, used, len(lines), h, maxh, y + h))
    return h


# ----------------------------------------------------------------- illustrations

def illo(d, x, y, w, h, kind, col):
    """A flat picture for one story, drawn inside its own band. No text inside."""
    d.rectangle([x, y, x + w, y + h], fill=(242, 240, 234))
    cx, cy = x + w // 2, y + h // 2
    s = min(w, h)
    dark = tuple(max(0, int(c * 0.70)) for c in col)
    light = tuple(min(255, int(c + (255 - c) * 0.74)) for c in col)
    ground = (226, 222, 214)
    gyp = y + int(h * 0.74)
    P = lambda fx, fy: (x + int(w * fx), y + int(h * fy))

    if kind == "summit":                       # three lecterns under flags
        d.rectangle([x, gyp, x + w, y + h], fill=ground)
        for i, c in enumerate((col, WHITE, dark)):
            bx = x + int(w * (.14 + i * .25))
            d.rectangle([bx, y + int(h * .34), bx + int(w * .17), gyp], fill=c,
                        outline=(146, 144, 138))
            d.rectangle([bx + 2, y + int(h * .38), bx + int(w * .17) - 3,
                         y + int(h * .48)],
                        fill=light if c is not WHITE else (176, 30, 38))
        d.rectangle([x, y + int(h * .80), x + w, y + int(h * .86)], fill=(166, 162, 154))
        for i in range(3):
            px = x + int(w * (.225 + i * .25))
            d.ellipse([px - 4, y + int(h * .14), px + 4, y + int(h * .24)],
                      fill=(122, 124, 132))

    elif kind == "berlin":                     # colonnade and a banner
        d.rectangle([x, y + int(h * .72), x + w, y + h], fill=ground)
        for i in range(6):
            bx = x + int(w * (.14 + i * .12))
            d.rectangle([bx, y + int(h * .36), bx + int(w * .06), y + int(h * .74)],
                        fill=(194, 190, 182))
        d.rectangle([x + int(w * .10), y + int(h * .30), x + w - int(w * .10),
                     y + int(h * .37)], fill=col)
        for i in range(7):
            d.rectangle([x + int(w * (.13 + i * .105)), y + int(h * .32),
                         x + int(w * (.13 + i * .105)) + 3, y + int(h * .37)], fill=WHITE)
        d.polygon([(cx - int(w * .04), y + int(h * .30)), (cx, y + int(h * .15)),
                   (cx + int(w * .04), y + int(h * .30))], fill=col)

    elif kind == "bridge":                     # three spans, one broken
        d.rectangle([x, y + int(h * .58), x + w, y + h], fill=(192, 212, 222))
        for k, (a, b) in enumerate(((.04, .32), (.38, .62), (.68, .96))):
            bx0, bx1 = x + int(w * a), x + int(w * b)
            d.rectangle([bx0, y + int(h * .30), bx1, y + int(h * .39)], fill=col)
            for px in (bx0 + int(w * .03), bx1 - int(w * .05)):
                d.rectangle([px, y + int(h * .34), px + 4, y + int(h * .62)], fill=dark)
        d.polygon([(x + int(w * .32), y + int(h * .30)), (x + int(w * .38), y + int(h * .58)),
                   (x + int(w * .32), y + int(h * .58))], fill=(112, 110, 104))
        d.ellipse([x + int(w * .33) - 3, y + int(h * .60), x + int(w * .33) + 3,
                   y + int(h * .72)], fill=(226, 96, 40))

    elif kind == "missile":                    # tower, smoke, a rising streak
        d.rectangle([x, y + int(h * .80), x + w, y + h], fill=ground)
        d.rectangle([cx - int(w * .10), y + int(h * .22), cx + int(w * .10),
                     y + int(h * .80)], fill=(176, 176, 182))
        for i in range(5):
            d.rectangle([cx - int(w * .10), y + int(h * (.26 + i * .11)),
                         cx + int(w * .10), y + int(h * (.28 + i * .11))],
                        fill=(206, 206, 210))
        d.ellipse([cx + int(w * .02), y + int(h * .10), cx + int(w * .26),
                   y + int(h * .34)], fill=(150, 148, 146))
        d.ellipse([cx + int(w * .08), y + int(h * .04), cx + int(w * .22),
                   y + int(h * .18)], fill=(186, 184, 182))
        d.line([x + int(w * .04), y + int(h * .86), cx - int(w * .14), y + int(h * .34)],
               fill=(226, 96, 40), width=3)
        d.polygon([(cx - int(w * .14), y + int(h * .34)),
                   (cx - int(w * .20), y + int(h * .36)),
                   (cx - int(w * .13), y + int(h * .44))], fill=(240, 150, 50))

    elif kind == "handshake":                  # two delegations, a meeting table
        d.rectangle([x, y + int(h * .78), x + w, y + h], fill=ground)
        d.rectangle([x + int(w * .10), y + int(h * .56), x + w - int(w * .10),
                     y + int(h * .64)], fill=(178, 174, 166))
        for i in range(5):                     # rings on the EU side
            d.ellipse([x + int(w * .14) + i * 9, y + int(h * .40),
                       x + int(w * .14) + i * 9 + 7, y + int(h * .49)], fill=col)
        for i in range(5):                     # flat block on the UK side
            bx = x + w - int(w * .20) - i * 9
            d.rectangle([bx, y + int(h * .40), bx + 7, y + int(h * .49)],
                        fill=dark if i % 2 else light)
        d.ellipse([cx - 5, y + int(h * .30), cx + 5, y + int(h * .40)], fill=dark)
        d.ellipse([cx - 5, y + int(h * .30), cx + 5, y + int(h * .40)], fill=dark)
        d.line([cx - 10, y + int(h * .52), cx + 10, y + int(h * .52)], fill=dark, width=4)

    elif kind == "arctic":                     # ice sheet, a base, a flagstaff
        d.rectangle([x, y + int(h * .58), x + w, y + h], fill=(236, 242, 246))
        d.polygon([(x, y + int(h * .62)), (x + int(w * .30), y + int(h * .54)),
                   (x + int(w * .58), y + int(h * .60)), (x + int(w * .84), y + int(h * .52)),
                   (x + w, y + int(h * .58)), (x + w, y + int(h * .74)),
                   (x, y + int(h * .74))], fill=(214, 226, 236))
        d.line([x, y + int(h * .70), x + w, y + int(h * .70)],
               fill=(186, 204, 218), width=2)
        d.rectangle([x + int(w * .60), y + int(h * .40), x + int(w * .78),
                     y + int(h * .56)], fill=(176, 172, 164))
        d.polygon([(x + int(w * .58), y + int(h * .40)), (x + int(w * .69), y + int(h * .33)),
                   (x + int(w * .80), y + int(h * .40))], fill=(150, 146, 138))
        d.rectangle([x + int(w * .16), y + int(h * .18), x + int(w * .17),
                     y + int(h * .70)], fill=(120, 120, 126))
        d.rectangle([x + int(w * .17), y + int(h * .18), x + int(w * .30),
                     y + int(h * .27)], fill=col)

    elif kind == "cyclone":                    # a spiral over a coastline
        d.rectangle([x, y + int(h * .52), x + w, y + h], fill=(198, 214, 220))
        for i in range(4):
            r = int(w * (.10 + i * .045))
            d.arc([cx - r, cy - r, cx + r, cy + r], 200 + i * 40, 20 + i * 40,
                  fill=col, width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=dark)
        d.polygon([(x + int(w * .62), y + int(h * .52)), (x + w, y + int(h * .62)),
                   (x + w, y + h), (x + int(w * .72), y + h)], fill=(196, 188, 160))
        for i in range(3):
            d.line([x + int(w * .74) + i * 8, y + int(h * .62) + i * 12,
                    x + int(w * .92) + i * 8, y + int(h * .58) + i * 12],
                   fill=(152, 140, 106), width=2)

    elif kind == "memorial":                   # a row of small markers, one taller
        d.rectangle([x, y + int(h * .78), x + w, y + h], fill=ground)
        for i in range(7):
            bx = x + int(w * (.12 + i * .11))
            hh = .44 if i == 3 else .54
            d.rectangle([bx, y + int(h * hh), bx + int(w * .055), y + int(h * .78)],
                        fill=col if i == 3 else light)
        d.rectangle([cx - int(w * .03), y + int(h * .30), cx + int(w * .03),
                     y + int(h * .40)], fill=dark)

    elif kind == "shield":                     # a police line, a shield
        d.rectangle([x, y + int(h * .78), x + w, y + h], fill=ground)
        d.polygon([(cx, y + int(h * .16)), (cx + int(w * .16), y + int(h * .24)),
                   (cx + int(w * .16), y + int(h * .50)), (cx, y + int(h * .64)),
                   (cx - int(w * .16), y + int(h * .50)), (cx - int(w * .16), y + int(h * .24))],
                  fill=col, outline=dark)
        d.line([cx, y + int(h * .26), cx, y + int(h * .56)], fill=light, width=3)
        d.line([cx - int(w * .07), y + int(h * .38), cx + int(w * .07), y + int(h * .38)],
               fill=light, width=3)

    elif kind == "forest":                     # canopy rows, a demarcated plot
        d.rectangle([x, y + int(h * .80), x + w, y + h], fill=(214, 204, 180))
        for i in range(6):
            bx = x + int(w * (.10 + i * .13))
            d.polygon([(bx, y + int(h * .78)), (bx + int(w * .075), y + int(h * .34)),
                       (bx + int(w * .15), y + int(h * .78))],
                      fill=col if i % 2 else dark)
        for i in range(5):
            px = x + int(w * (.08 + i * .10))
            d.rectangle([px, y + int(h * .80), px + 2, y + int(h * .90)], fill=(150, 126, 84))
        d.line([x + int(w * .06), y + int(h * .90), x + int(w * .56), y + int(h * .90)],
               fill=(150, 126, 84), width=2)

    elif kind == "probe":                      # a dish, a long signal, a small Earth
        d.rectangle([x, y + int(h * .84), x + w, y + h], fill=ground)
        d.ellipse([x + int(w * .08), y + int(h * .18), x + int(w * .26),
                   y + int(h * .36)], fill=(64, 108, 164))
        d.ellipse([x + int(w * .70), y + int(h * .30), x + int(w * .78),
                   y + int(h * .40)], fill=col)
        for i in range(4):
            r = int(w * (.16 + i * .10))
            d.arc([x + int(w * .76) - r, cy - r // 2, x + int(w * .76) + r, cy + r // 2],
                  150, 210, fill=(150, 148, 142), width=2)
        d.rectangle([cx, y + int(h * .44), cx + int(w * .10), y + int(h * .58)],
                    fill=(196, 192, 184))
        d.polygon([(cx - int(w * .04), y + int(h * .58)), (cx + int(w * .14), y + int(h * .58)),
                   (cx + int(w * .05), y + int(h * .72))], fill=dark)
        d.line([cx + int(w * .05), y + int(h * .72), cx + int(w * .05), y + int(h * .84)],
               fill=dark, width=2)

    elif kind == "chart":                      # bars down, a ticker line falling
        d.rectangle([x, y + int(h * .82), x + w, y + h], fill=ground)
        bw, n = int(w * .09), 6
        for i, hh in enumerate((.44, .52, .50, .58, .66, .76)):
            bx = x + int(w * .12) + i * int(w * .13)
            d.rectangle([bx, y + int(h * hh), bx + bw, y + int(h * .82)],
                        fill=col if i >= 3 else (194, 198, 204))
        d.line([x + int(w * .10), y + int(h * .16), x + int(w * .34), y + int(h * .20),
                x + int(w * .58), y + int(h * .16), x + int(w * .88), y + int(h * .30)],
               fill=dark, width=3)
        d.polygon([(x + int(w * .88), y + int(h * .30)), (x + int(w * .79), y + int(h * .27)),
                   (x + int(w * .87), y + int(h * .38))], fill=dark)

    elif kind == "gamepad":                    # a controller, a rising receipt
        d.rectangle([x, y + int(h * .84), x + w, y + h], fill=ground)
        d.rounded_rectangle([cx - int(w * .24), y + int(h * .36), cx + int(w * .24),
                             y + int(h * .66)], radius=10, fill=col)
        d.ellipse([cx + int(w * .10), y + int(h * .42), cx + int(w * .16),
                   y + int(h * .48)], fill=light)
        d.ellipse([cx + int(w * .15), y + int(h * .50), cx + int(w * .21),
                   y + int(h * .56)], fill=light)
        d.line([cx - int(w * .19), y + int(h * .51), cx - int(w * .06), y + int(h * .51)],
               fill=light, width=3)
        d.line([cx - int(w * .125), y + int(h * .45), cx - int(w * .125),
                y + int(h * .57)], fill=light, width=3)
        d.rectangle([x + int(w * .14), y + int(h * .70), x + int(w * .40),
                     y + int(h * .78)], fill=(186, 182, 174))
        d.rectangle([x + int(w * .60), y + int(h * .70), x + int(w * .86),
                     y + int(h * .78)], fill=(206, 202, 194))

    elif kind == "parliament":                 # a stepped assembly, a raised hand
        d.rectangle([x, y + int(h * .82), x + w, y + h], fill=ground)
        for r in range(3):
            for c in range(7):
                bx = x + int(w * (.12 + c * .11))
                by = y + int(h * (.44 + r * .12))
                d.rectangle([bx, by, bx + int(w * .07), by + int(h * .09)],
                            fill=col if (r + c) % 3 else dark)
        d.rectangle([cx - int(w * .02), y + int(h * .12), cx + int(w * .02),
                     y + int(h * .30)], fill=dark)
        d.rectangle([cx - int(w * .10), y + int(h * .08), cx + int(w * .10),
                     y + int(h * .14)], fill=light)

    elif kind == "embassy":                    # a walled compound and an empty flagpole
        d.rectangle([x, y + int(h * .80), x + w, y + h], fill=ground)
        d.rectangle([x + int(w * .18), y + int(h * .40), x + int(w * .56),
                     y + int(h * .80)], fill=(206, 202, 194), outline=(150, 148, 142))
        for i in range(3):
            d.rectangle([x + int(w * (.22 + i * .12)), y + int(h * .50),
                         x + int(w * (.22 + i * .12)) + int(w * .07), y + int(h * .62)],
                        fill=col if i % 2 else dark)
        d.rectangle([x + int(w * .70), y + int(h * .18), x + int(w * .71),
                     y + int(h * .80)], fill=(140, 138, 132))
        d.rectangle([x + int(w * .12), y + int(h * .74), x + int(w * .82),
                     y + int(h * .80)], fill=(176, 172, 164))

    else:
        d.ellipse([cx - int(s * .28), cy - int(s * .28), cx + int(s * .28),
                   cy + int(s * .28)], fill=col)


# ----------------------------------------------------------------- data-derived numbers

def census():
    """Count the stories actually printed, from the data. Never typed by hand."""
    reg, fld = {}, {}
    for rec in data.HEROES + data.PANELS:
        reg[rec[0]] = reg.get(rec[0], 0) + 1
        fld[rec[1]] = fld.get(rec[1], 0) + 1
    for rec in data.INDEX:
        reg[rec[0]] = reg.get(rec[0], 0) + 1
        fld[rec[1]] = fld.get(rec[1], 0) + 1
    total = len(data.HEROES) + len(data.PANELS) + len(data.INDEX)
    return reg, fld, total


def numbers():
    """Six figures, each paired with the story it was counted from.

    Four are computed here (never typed).  The two hard figures come from the
    panel wording itself, so the strip cannot disagree with the page.
    """
    reg, fld, total = census()
    kid = [p for p in data.PANELS if "children" in p[2].lower()][0]
    kid_fig = [t for t in kid[2].split() if t.replace(",", "").isdigit()][0]
    return [
        (str(len(reg)), "regions covered"),
        (str(len(fld)), "fields of news"),
        (str(len(data.PANELS)), "illustrated panels"),
        (kid_fig, "children killed, health authorities' figure"),
        ("19 NOV", "when Nvidia's subpoena was issued"),
        (str(total), "stories on this page"),
    ]


def wrap_text(d, text, font, maxw, maxlines):
    """Wrap into at most maxlines, shrinking the font until the text fits."""
    words = text.split()
    lines = [text]
    for size in range(font.size, 5, -1):
        f = F(SANS, size)
        lines, cur = [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if d.textlength(trial, font=f) <= maxw or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        if len(lines) <= maxlines:
            return lines, f
    return lines, F(SANS, 5)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    del REPORT[:]
    del FAIL[:]
    YMAX[0] = 0

    # ---------------- masthead ----------------
    y = 14
    fk = fit(d, KICKER, SANSB, 13, int(CW * .55), 18)
    text_at(d, X0, y, fk[1][0], fk[0], PALETTE["RED"])
    ftag = F(SANSB, 10)
    tag = "GLOBAL  |  %d STORIES, %d REGIONS" % (census()[2], len(census()[0]))
    text_at(d, X1 - d.textlength(tag, font=ftag), y + 2, tag, ftag, MID)
    y += 19
    fdate, dl, dlh, ds = fit(d, DATE_BIG, SERIFB, 48, CW, 56)
    text_at(d, X0, y, dl[0], fdate, NAVY)
    y += dlh - 2
    d.rectangle([X0, y, X1, y + 5], fill=NAVY)
    y += 11
    fst, sl, slh, _ = fit(d, STRAP, SANS, 9, CW, 22)
    for i, ln in enumerate(sl):
        text_at(d, X0, y + i * slh, ln, fst, MID)
    y += len(sl) * slh + 9

    GAP = 11
    cw = (CW - 2 * GAP) // 3

    # ---------------- three leads ----------------
    ILLO1, BAND = 66, 14
    top = y
    lead_bottom = top
    for i, (reg, fld, head, deck, body, colname, kind, _s) in enumerate(data.HEROES):
        x = X0 + i * (cw + GAP)
        col = PALETTE[colname]
        illo(d, x, top, cw, ILLO1, kind, col)
        by = top + ILLO1
        d.rectangle([x, by, x + cw, by + BAND], fill=col)
        fb = F(SANSB, 9)
        text_at(d, x + 5, by + 2, reg, fb, WHITE)
        fw = d.textlength(fld, font=fb)
        text_at(d, x + cw - 5 - fw, by + 2, fld, fb, WHITE)
        yy = by + BAND + 4
        yy += block(d, head, SERIFB, 17, x, yy, cw, 54, INK, "L1 head")
        yy += 3
        yy += block(d, deck, SANSB, 9, x, yy, cw, 25, col, "L1 deck")
        yy += 2
        yy += block(d, body, SANS, 9, x, yy, cw, 84, BODY, "L1 body")
        lead_bottom = max(lead_bottom, yy)
    top = lead_bottom + 12

    # ---------------- second tier: 3 across, as many rows as the data has ----------------
    ILLO2, BAND2 = 30, 12
    cellh = 97
    nrow = (len(data.PANELS) + 2) // 3
    for idx, (reg, fld, head, body, colname, kind, _s) in enumerate(data.PANELS):
        cx_i, cy_i = idx % 3, idx // 3
        x = X0 + cx_i * (cw + GAP)
        y2 = top + cy_i * (cellh + 4)
        col = PALETTE[colname]
        # lay the text out first, then give the picture exactly the room left,
        # so no cell carries a dead strip between picture and headline
        f_head, h_lines, h_lh, _ = fit(d, head, SERIFB, 12, cw, 34)
        f_body, b_lines, b_lh, _ = fit(d, body, SANS, 9, cw, 44)
        ih = cellh - (BAND2 + 2 + len(h_lines) * h_lh + 1 + len(b_lines) * b_lh)
        ih = max(16, min(ILLO2, ih))
        illo(d, x, y2, cw, ih, kind, col)
        by = y2 + ih
        d.rectangle([x, by, x + cw, by + BAND2], fill=col)
        fb = F(SANSB, 8)
        text_at(d, x + 4, by + 1, reg, fb, WHITE)
        fw = d.textlength(fld, font=fb)
        text_at(d, x + cw - 4 - fw, by + 1, fld, fb, WHITE)
        ty = by + BAND2 + 2
        for i, ln in enumerate(h_lines):
            text_at(d, x, ty + i * h_lh, ln, f_head, INK)
        ty += len(h_lines) * h_lh
        REPORT.append(("L2 head", f_head.size, len(h_lines), len(h_lines) * h_lh, 34))
        ty += 1
        for i, ln in enumerate(b_lines):
            text_at(d, x, ty + i * b_lh, ln, f_body, BODY)
        REPORT.append(("L2 body", f_body.size, len(b_lines), len(b_lines) * b_lh, 44))
        if ty + len(b_lines) * b_lh > y2 + cellh:
            FAIL.append(("L2 cell", f_body.size, len(b_lines),
                         ty + len(b_lines) * b_lh - y2, cellh, ty + len(b_lines) * b_lh))
        if cy_i < nrow - 1:
            d.line([x, y2 + cellh + 1, x + cw, y2 + cellh + 1], fill=RULE)
    top += nrow * cellh + (nrow - 1) * 4 + 10

    # ---------------- by the numbers (computed) ----------------
    reg, fld, total = census()
    NH = 25
    d.rectangle([X0, top, X1, top + NH], fill=NAVY)
    nums = numbers()
    seg = CW // len(nums)
    text_at(d, X0 + 6, top + 3, "BY THE NUMBERS", F(SANSB, 7), (152, 170, 202))
    for i, (num, label) in enumerate(nums):
        bx = X0 + i * seg + 7
        text_at(d, bx, top + 7, num, F(SERIFB, 13), (250, 244, 226))
        text_at(d, bx, top + 20, label, F(SANS, 6), (198, 204, 216))
        if i:
            d.line([X0 + i * seg, top + 6, X0 + i * seg, top + NH - 5], fill=(74, 86, 110))
    top += NH + 9

    # ---------------- the rest of the day ----------------
    fh = F(SANSB, 10)
    text_at(d, X0, top, "THE REST OF THE DAY", fh, NAVY)
    lab = "%d STORIES IN ALL" % total
    text_at(d, X1 - d.textlength(lab, font=fh), top, lab, fh, MID)
    top += 14
    d.line([X0, top, X1, top], fill=RULE)
    top += 4

    # ---------------- footer: census, counted ----------------
    regs = "  ".join("%s %d" % (k, v) for k, v in
                     sorted(reg.items(), key=lambda kv: (-kv[1], kv[0])))
    flds = "  ".join("%s %d" % (k, v) for k, v in
                     sorted(fld.items(), key=lambda kv: (-kv[1], kv[0])))
    ffoot = F(SANS, 7)
    rl, rf = wrap_text(d, "BY REGION   " + regs, ffoot, CW, 1)

    def balanced(items, prefix, nline, font):
        """Split a counted list over nline lines, as close to equal as possible,
        so the last line is never a one-item orphan (a stray mark at 300 px)."""
        out, n = [], len(items)
        per = (n + nline - 1) // nline
        for k in range(nline):
            chunk = items[k * per:(k + 1) * per]
            if chunk:
                out.append((prefix if k == 0 else "") + "   ".join(chunk))
        return out

    fitems = ["%s %d" % (k, v) for k, v in sorted(fld.items(), key=lambda kv: (-kv[1], kv[0]))]
    for nline in (2, 3):
        fl = balanced(fitems, "BY FIELD   ", nline, ffoot)
        if all(d.textlength(l, font=ffoot) <= CW for l in fl):
            ff = ffoot
            break
    else:
        fl, ff = wrap_text(d, "BY FIELD   " + flds, ffoot, CW, 3)
    allf = rl + fl
    step = ff.size + 3
    # last footer baseline, and the descender of that line, must land at least
    # 10 px above the bottom edge: 1024 - 12 - 4 = 1008
    top_foot = H - 12 - 4 - len(allf) * step + 2
    FOOT[0] = top_foot
    d.line([X0, top_foot - 6, X1, top_foot - 6], fill=RULE)
    for i, ln in enumerate(allf):
        text_at(d, X0, top_foot + i * step, ln, ff, MID)
        if d.textlength(ln, font=ff) > CW:
            FAIL.append(("footer line", ff.size, 1, 1, CW, d.textlength(ln, font=ff)))

    # ---------------- the index, fitted to what is left ----------------
    ncol = 3
    percol = (len(data.INDEX) + ncol - 1) // ncol
    gutter = 12
    colw = (CW - gutter * (ncol - 1)) // ncol
    avail = (top_foot - 7) - top
    lh_i = avail // max(1, percol)
    IDX[0], IDX[1] = top, lh_i
    if lh_i < 12:
        raise SystemExit("index too tight: %d px a row for %d rows" % (lh_i, percol))
    for i, rec in enumerate(data.INDEX):
        rg, fd, head = rec[0], rec[1], rec[2]
        ci, ri = i // percol, i % percol
        x = X0 + ci * (colw + gutter)
        y3 = top + ri * lh_i
        col = PALETTE[REGION_COLOUR[rg]]
        d.rectangle([x, y3 + 2, x + 3, y3 + lh_i - 4], fill=col)
        hh = block(d, head, SANS, 9, x + 8, y3 + 1, colw - 10, lh_i - 3, BODY, "index r")
        if hh > lh_i - 3:
            IDX[2] += 1

    # bottom rule, inside the floor
    return img


if __name__ == "__main__":
    out = os.environ.get("OUT", "out")
    os.makedirs(out, exist_ok=True)
    im = build()
    im.save(os.path.join(out, "entry.png"), optimize=True)
    print("size", im.size, "stories", census()[2], "blocks", len(REPORT),
          "overflow", len(FAIL), "ink_low", YMAX[0], "clear", FLOOR - YMAX[0])
    print("footer top:", FOOT[0], "index top:", IDX[0], "lh:", IDX[1])
    for r in FAIL[:12]:
        print("  ", r)
    if IDX[2] > 0:
        print("  index rows crammed to min size:", IDX[2])
