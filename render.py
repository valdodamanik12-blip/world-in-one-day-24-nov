#!/usr/bin/env python3
"""Render the front page for news-image-20261124: THE WORLD IN ONE DAY.

Draws a 1024x1024 newspaper front page with PIL + system DejaVu fonts and
writes entry.png next to this script. Deterministic: same inputs, same bytes.
Run: python3 render.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
RED = (163, 22, 33)
GREY = (90, 86, 78)
RULE = (60, 58, 52)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def hrule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    x0, x1 = M, W - M

    # ---- Masthead ----
    f_mast = font(SERIF_B, 62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 26), title, font=f_mast, fill=INK)

    # double rule under masthead
    hrule(d, x0, x1, 108, 3)
    hrule(d, x0, x1, 114, 1)

    # date line — the day, prominent
    f_date = font(SANS_B, 30)
    date = "TUESDAY 24 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 126), date, font=f_date, fill=RED)

    f_sub = font(SANS, 15)
    sub = "SIX STORIES  •  FROM RIYADH TO VILLAVICENCIO  •  ONE DAY OF WORLD NEWS"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 168), sub, font=f_sub, fill=GREY)
    hrule(d, x0, x1, 196, 2)

    # ---- LEAD: Houthis hit PIF Tower ----
    y = 212
    f_kick = font(SANS_B, 16)
    d.text((x0, y), "LEAD  —  MIDDLE EAST", font=f_kick, fill=RED)
    y += 26
    f_h1 = font(SERIF_B, 40)
    d.text((x0, y), "HOUTHIS HIT RIYADH'S PIF TOWER", font=f_h1, fill=INK)
    y += 52
    f_h1b = font(SERIF_B, 27)
    d.text((x0, y), "11 WOUNDED IN SECOND STRIKE IN A WEEK", font=f_h1b, fill=INK)
    y += 40
    f_deck = font(SERIF, 17)
    lead_deck = (
        "Yemen's Houthis struck the 80-storey, 385-metre Public Investment Fund Tower in "
        "Riyadh on Tuesday, wounding 11 people — 2 Saudis, 2 Indians, 3 Nepalis and "
        "4 Egyptians, Saudi Civil Defense said. It is the second hit on the same tower in "
        "under a week; the first, on 19 November, damaged the tower but hurt no one. The "
        "coalition called it a drone attack and vowed a \u201cdecisive\u201d response."
    )
    y = draw_wrapped(d, x0, y, lead_deck, f_deck, x1 - x0, leading=23)
    y += 6

    # skyline strip: Riyadh towers, PIF Tower tallest, marked
    base = y + 46
    d.rectangle([x0, base, x1, base + 2], fill=RULE)
    import random
    rng = random.Random(24)
    bx = x0
    while bx < x1 - 8:
        bw = rng.randint(18, 42)
        bh = rng.randint(12, 30)
        if bx + bw < 690 or bx > 740:  # keep the PIF Tower clear
            d.rectangle([bx, base - bh, bx + bw, base], fill=INK)
        bx += bw + 6
    # PIF Tower: tall, centre-right, with red marker and label to its right
    tx = 700
    d.rectangle([tx, base - 44, tx + 26, base], fill=INK)
    d.polygon([(tx, base - 44), (tx + 13, base - 54), (tx + 26, base - 44)], fill=INK)
    d.ellipse([tx + 6, base - 66, tx + 20, base - 52], fill=RED)
    f_cap = font(SANS_B, 12)
    d.text((tx + 34, base - 44), "PIF TOWER — 385 m", font=f_cap, fill=RED)
    y = base + 10
    hrule(d, x0, x1, y, 2)
    y += 12

    # ---- Grid: stories 2-5 (2 cols x 2 rows) ----
    col_w = (x1 - x0 - 24) // 2
    row_h = 160
    stories = [
        ("UKRAINE",
         "2 DEAD, 40 WOUNDED AS RUSSIAN STRIKE RIPS INTO ZAPORIZHZHIA FLATS",
         "An overnight Russian attack partly destroyed a five-storey block in the "
         "Kosmichnyi district and a private house. Governor Mykhailo Semikin: 2 killed, "
         "40 wounded — 4 children among them, the youngest an infant of a few months."),
        ("GAZA",
         "ISRAEL KILLS HAMAS INTERNAL SECURITY CHIEF IN GAZA CITY STRIKE",
         "Naeem Abu Nahel, 50, director of Hamas' internal security apparatus — in post "
         "only since September — was killed in western Gaza City. The IDF and Shin Bet "
         "confirmed the strike; at least 7 Palestinians were killed in Gaza on Tuesday."),
        ("EUROPE  —  HUMAN RIGHTS",
         "STATES MAY TURN BACK MIGRANTS IN \u2018HYBRID WAR\u2019 EMERGENCIES, TOP EUROPE COURT RULES",
         "The ECHR Grand Chamber: states may push back migrants when migration is "
         "\u201cinstrumentalised\u201d by a hostile state. Three rulings on Poland, Latvia and "
         "Lithuania over 2021–22 Belarus pushbacks. Amnesty: \u201ca devastating blow to the "
         "absolute prohibition of torture\u201d."),
        ("UNITED ARAB EMIRATES",
         "BUS SLAMS INTO PARKED TRUCK IN RAS AL KHAIMAH — 13 KILLED, 14 HURT",
         "A bus carrying 41 people hit a truck parked on Al Watan Road in the early hours. "
         "11 died at the scene, 2 more in hospital. The UAE's second deadly bus crash in "
         "under two weeks — 14 were killed in Fujairah on 12 November."),
    ]
    f_grid_k = font(SANS_B, 14)
    f_grid_h = font(SERIF_B, 19)
    f_grid_d = font(SERIF, 13)
    gy = y
    for i, (kick, head, deck) in enumerate(stories):
        cx = x0 + (i % 2) * (col_w + 24)
        cy = gy + (i // 2) * (row_h + 12)
        if i % 2 == 1:
            d.line([(x0 + col_w + 12, cy), (x0 + col_w + 12, cy + row_h)], fill=RULE, width=1)
        d.text((cx, cy), kick, font=f_grid_k, fill=RED)
        yy = cy + 22
        yy = draw_wrapped(d, cx, yy, head, f_grid_h, col_w, leading=23)
        yy += 4
        draw_wrapped(d, cx, yy, deck, f_grid_d, col_w, leading=15)
    y = gy + 2 * row_h + 12
    hrule(d, x0, x1, y, 2)
    y += 12

    # ---- Story 6: Colombia banner ----
    f_b_k = font(SANS_B, 15)
    d.text((x0, y), "COLOMBIA", font=f_b_k, fill=RED)
    y += 24
    f_b_h = font(SERIF_B, 22)
    y = draw_wrapped(d, x0, y,
                     "CAR BOMB AT COLOMBIA GOVERNOR'S OFFICE WOUNDS 20+ ON EVE OF PEACE ANNIVERSARY",
                     f_b_h, x1 - x0, leading=27)
    y += 4
    f_b_d = font(SERIF, 14)
    y = draw_wrapped(d, x0, y,
                     "A car bomb outside the Meta governor's office in Villavicencio injured 20+ people "
                     "and damaged 80+ buildings; no deaths. The car carried 80–100 kg of pentolite. "
                     "President Abelardo de la Espriella blamed ex-FARC dissidents of the EMC's 39th Front. "
                     "Blast late Monday, first majorly reported Tuesday — the eve of the 10th anniversary "
                     "of Colombia's 2016 peace deal.",
                     f_b_d, x1 - x0, leading=18)

    # ---- Footer ----
    fy = H - 50
    hrule(d, x0, x1, fy, 1)
    f_f = font(SANS, 10)
    foot = ("Sources: Reuters  •  Bloomberg  •  AFP  •  Kyiv Independent  •  BBC  •  ECHR  •  "
            "Amnesty  •  Arab News  •  Gulf Business  •  Khaleej Times  •  Al Jazeera  •  "
            "Colombia Reports")
    fw = d.textlength(foot, font=f_f)
    d.text(((W - fw) / 2, fy + 8), foot, font=f_f, fill=GREY)
    f_f2 = font(SANS, 10)
    foot2 = "All events happened, or were first reported, on Tuesday 24 November 2026."
    fw2 = d.textlength(foot2, font=f_f2)
    d.text(((W - fw2) / 2, fy + 24), foot2, font=f_f2, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
