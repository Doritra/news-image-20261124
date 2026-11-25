"""Render the Tuesday 24 November 2026 world-news front page.

One 1024x1024 PNG holding 40 stories reported on 24 November 2026:
three lead stories on top (the COP31 collapse in Antalya, the ICJ
genocide ruling on Myanmar, Jensen Huang's return to Nvidia), then
eight sections across regions and fields, plus a "day in numbers"
strip. All text is drawn programmatically with Pillow from the story
lists below, so no lettering can be garbled. The render is fully
deterministic: fixed palette, fixed fonts, no clock, no randomness,
no network. Running it twice writes byte-identical output.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
PAPER = (250, 248, 241)
INK = (13, 16, 22)
BODY = (34, 37, 44)
MUTED = (92, 96, 104)
RULE = (196, 188, 168)
NAVY = (16, 32, 56)
GOLD = (214, 186, 120)
RED = (168, 32, 36)
TEAL = (14, 102, 96)
LEAD_BG = (232, 226, 208)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


LEAD = [
    ("COP31 TALKS COLLAPSE",
     "UN climate summit in Antalya ends with no deal after 90+ nations "
     "reject a final draft that never mentions fossil fuels."),
    ("ICJ: MYANMAR GENOCIDE",
     "The world court rules Myanmar committed genocide against the "
     "Rohingya; 14 countries back the ruling."),
    ("HUANG BACK AT NVIDIA",
     "Nvidia reinstates Jensen Huang as chief executive after Trump "
     "intervenes; shares surge and markets rally."),
]

SECTIONS_LEFT = [
    ("EUROPE & UKRAINE", RED, [
        "Zaporizhzhia strike kills 2, wounds 40 incl. children",
        "NATO vows to defend space after satellite reports",
        "Medvedev warns of 'preventive nuclear attack'",
        "Germany first to access Ukraine's Delta system",
        "Seven states back EU curbs on Russian tourist visas",
        "Zelensky urges NATO to admit Ukraine in Berlin",
    ]),
    ("ASIA-PACIFIC", TEAL, [
        "Russian jets enter South Korea's air defence zone",
        "Seoul offers $375,000 rewards to catch AI cheats",
        "China opens Tiangong station to first foreign astronaut",
        "Nepal quake 5.6 strikes near the China border",
        "Seoul stocks jump 6%+, Nikkei +3.9%",
    ]),
    ("MIDDLE EAST", GOLD, [
        "Israeli strikes kill Hamas security chief, six in Gaza",
        "UN: Gaza war erased 77 years of development",
        "Vance, Rubio meet Qatar PM at White House on Iran",
        "Iran vows to fight US naval blockade; no talks yet",
        "Iraq PM orders ministry to run Kurdish-area oilfields",
        "Houthis report dozens dead in Saudi strikes in Yemen",
    ]),
]

SECTIONS_RIGHT = [
    ("AFRICA", RED, [
        "Congo fighting traps Ebola response teams in Ituri",
        "UN urges probe into Benghazi port attacks in Libya",
        "Borno school enrolment nearly doubles after war",
    ]),
    ("AMERICAS", NAVY, [
        "US loses measles elimination status after 25+ years",
        "Pennsylvania records ninth measles death",
        "States sue Musk firms over Grok sexualised images",
        "Pentagon accuses Canada of falling short",
        "Mexico to try 'El Chapo Isidro' despite US bid",
        "Colombia car bomb wrecks buildings in Villavicencio",
        "Cuba: WHO chief visits deteriorating health system",
    ]),
    ("ECONOMY & TECHNOLOGY", TEAL, [
        "Markets surge: S&P +4.73%, Nasdaq +6.51%",
        "Sanofi agrees $41bn buy of US biotech Insmed",
        "US blacklists Singapore cloud firm Megaspeed",
        "Guterres urges talks on global AI safety rules",
        "FDA approves first drug for limb-girdle dystrophy",
    ]),
    ("SCIENCE & HEALTH", GOLD, [
        "Astronomers find most distant glowing black hole",
        "47,000 women killed by partners or relatives in 2025",
    ]),
    ("SPORT & CULTURE", RED, [
        "Real Madrid rout PSV 5-1 as Mbappé scores twice",
        "Arsenal held 1-1 by Dortmund; City draw 2-2 Napoli",
        "Galatasaray edge Villa 1-0 in Champions League",
    ]),
]

NUMBERS = [
    ("90+", "nations reject COP31 draft"),
    ("+6.51%", "Nasdaq surge"),
    ("47,000", "women killed by relatives, 2025"),
    ("$41bn", "Sanofi buys Insmed"),
    ("5–1", "Real Madrid rout PSV"),
]


def wrap(draw, text, size, width):
    """Greedy word wrap measured at the real font size."""
    fnt = font(SANS, size)
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def draw_section(draw, x, y, width, title, colour, items):
    draw.rectangle([x, y, x + width, y + 28], fill=colour)
    draw.text((x + 10, y + 5), title, font=font(SANS_B, 18), fill=(255, 255, 255))
    y += 34
    item_font = font(SANS, 19)
    for item in items:
        if draw.textlength(item, font=item_font) > width - 26:
            raise ValueError(f"item overflows column ({width}px): {item!r}")
        draw.text((x + 4, y), "\u2022", font=font(SANS_B, 19), fill=colour)
        draw.text((x + 22, y), item, font=item_font, fill=INK)
        y += 23
    return y + 4


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    draw.text((36, 14), "THE WORLD IN ONE DAY", font=font(SANS_B, 21), fill=GOLD)
    draw.text((36, 40), "Tuesday 24 November 2026", font=font(SERIF_B, 46),
              fill=(255, 255, 255))
    draw.text((36, 94), "40 stories  \u00b7  every region  \u00b7  one page",
              font=font(SANS, 16), fill=(196, 208, 224))
    draw.text((812, 48), "24 NOV", font=font(SERIF_B, 34), fill=(255, 255, 255))
    draw.text((812, 86), "2026", font=font(SANS_B, 18), fill=GOLD)

    # Lead band: first story dominates, the other two support it
    y = 130
    draw.rectangle([24, y, W - 24, y + 152], fill=LEAD_BG)
    col_w = 312
    for i, (head, body) in enumerate(LEAD):
        x = 40 + i * (col_w + 12)
        head_size = 23 if i == 0 else 20
        body_size = 16 if i == 0 else 15
        body_lh = 21 if i == 0 else 20
        draw.text((x, y + 12), head, font=font(SANS_B, head_size),
                  fill=RED if i == 0 else INK)
        lines = wrap(draw, body, body_size, col_w - 6)
        by = y + 46
        for line in lines[:5]:
            draw.text((x, by), line, font=font(SANS, body_size), fill=BODY)
            by += body_lh
    y += 164

    # Two-column sections
    left_y = y
    for title, colour, items in SECTIONS_LEFT:
        left_y = draw_section(draw, 24, left_y, 484, title, colour, items)
    right_y = y
    for title, colour, items in SECTIONS_RIGHT:
        right_y = draw_section(draw, 524, right_y, 476, title, colour, items)

    # Day in numbers strip
    ny = max(left_y, right_y) + 2
    draw.rectangle([24, ny, W - 24, ny + 54], outline=RULE, width=2)
    draw.text((40, ny + 2), "THE DAY IN NUMBERS", font=font(SANS_B, 13), fill=NAVY)
    nx = 40
    for value, label in NUMBERS:
        draw.text((nx, ny + 17), value, font=font(SERIF_B, 20), fill=RED)
        draw.text((nx, ny + 38), label, font=font(SANS, 9), fill=MUTED)
        nx += 192

    draw.text((24, H - 16),
              "Sources: AP, Reuters, AFP, Al Jazeera, The Guardian, UEFA and national reports of 24 Nov 2026.",
              font=font(SANS, 11), fill=MUTED)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
