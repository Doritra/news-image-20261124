"""Draw the front page for Tuesday 24 November 2026.

A single 1024 by 1024 PNG that sums up the day's world news: three
lead cards across the top, eight sections in two columns underneath,
and a strip of the day's numbers at the foot. The page holds 40
stories in total, every one of them reported on 24 November 2026,
from the COP31 collapse in Antalya to the Champions League results
that night. All lettering is painted by this program with Pillow,
so the text can never come out garbled, and the render is fixed:
same palette, same fonts, no clock, no dice, no network, so two
runs in a row write byte-for-byte the same file. Section headers
use the darker ochre on purpose: white section titles stay legible
on it, where the paler brass of the masthead kicker would not be.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024

PAPER = (250, 248, 241)
INK = (13, 16, 22)
SOFT_INK = (34, 37, 44)
GREY = (92, 96, 104)
HAIRLINE = (196, 188, 168)
MIDNIGHT = (16, 32, 56)
BRASS = (214, 186, 120)
CRIMSON = (168, 32, 36)
PINE = (14, 102, 96)
OCHRE = (176, 124, 22)
BAND = (232, 226, 208)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
PLAIN = f"{FONT_DIR}/LiberationSans-Regular.ttf"
BOLD = f"{FONT_DIR}/LiberationSans-Bold.ttf"
DISPLAY = f"{FONT_DIR}/LiberationSerif-Bold.ttf"


def load(kind, size):
    return ImageFont.truetype(kind, size)


LEAD_CARDS = [
    {
        "headline": "COP31 TALKS COLLAPSE",
        "deck": "UN climate summit in Antalya ends with no deal after 90+ nations "
                "reject a final draft that never mentions fossil fuels.",
        "star": True,
    },
    {
        "headline": "ICJ: MYANMAR GENOCIDE",
        "deck": "The world court rules Myanmar committed genocide against the "
                "Rohingya; 14 countries back the ruling.",
        "star": False,
    },
    {
        "headline": "HUANG BACK AT NVIDIA",
        "deck": "Nvidia reinstates Jensen Huang as chief executive after Trump "
                "intervenes; shares surge and markets rally.",
        "star": False,
    },
]

COLUMNS = [
    {
        "x": 24,
        "width": 484,
        "sections": [
            {"title": "EUROPE & UKRAINE", "colour": CRIMSON, "items": [
                "Zaporizhzhia strike kills 2, wounds 40 incl. children",
                "NATO vows to defend space after satellite reports",
                "Medvedev warns of 'preventive nuclear attack'",
                "Germany first to access Ukraine's Delta system",
                "Seven states back EU curbs on Russian tourist visas",
                "Zelensky urges NATO to admit Ukraine in Berlin",
            ]},
            {"title": "ASIA-PACIFIC", "colour": PINE, "items": [
                "Russian jets enter South Korea's air defence zone",
                "Seoul offers $375,000 rewards to catch AI cheats",
                "China opens Tiangong station to first foreign astronaut",
                "Nepal quake 5.6 strikes near the China border",
                "Seoul stocks jump 6%+, Nikkei +3.9%",
            ]},
            {"title": "MIDDLE EAST", "colour": OCHRE, "items": [
                "Israeli strikes kill Hamas security chief, six in Gaza",
                "UN: Gaza war erased 77 years of development",
                "Vance, Rubio meet Qatar PM at White House on Iran",
                "Iran vows to fight US naval blockade; no talks yet",
                "Iraq PM orders ministry to run Kurdish-area oilfields",
                "Houthis report dozens dead in Saudi strikes in Yemen",
            ]},
        ],
    },
    {
        "x": 524,
        "width": 476,
        "sections": [
            {"title": "AFRICA", "colour": CRIMSON, "items": [
                "Congo fighting traps Ebola response teams in Ituri",
                "UN urges probe into Benghazi port attacks in Libya",
                "Borno school enrolment nearly doubles after war",
            ]},
            {"title": "AMERICAS", "colour": MIDNIGHT, "items": [
                "US loses measles elimination status after 25+ years",
                "Pennsylvania records ninth measles death",
                "States sue Musk firms over Grok sexualised images",
                "Pentagon accuses Canada of falling short",
                "Mexico to try 'El Chapo Isidro' despite US bid",
                "Colombia car bomb wrecks buildings in Villavicencio",
                "Cuba: WHO chief visits deteriorating health system",
            ]},
            {"title": "ECONOMY & TECHNOLOGY", "colour": PINE, "items": [
                "Markets surge: S&P +4.73%, Nasdaq +6.51%",
                "Sanofi agrees $41bn buy of US biotech Insmed",
                "US blacklists Singapore cloud firm Megaspeed",
                "Guterres urges talks on global AI safety rules",
                "FDA approves first drug for limb-girdle dystrophy",
            ]},
            {"title": "SCIENCE & HEALTH", "colour": OCHRE, "items": [
                "Astronomers find most distant glowing black hole",
                "47,000 women killed by partners or relatives in 2025",
            ]},
            {"title": "SPORT & CULTURE", "colour": CRIMSON, "items": [
                "Real Madrid rout PSV 5-1 as Mbappé scores twice",
                "Arsenal held 1-1 by Dortmund; City draw 2-2 Napoli",
                "Galatasaray edge Villa 1-0 in Champions League",
            ]},
        ],
    },
]

DAY_NUMBERS = [
    ("90+", "nations reject COP31 draft"),
    ("+6.51%", "Nasdaq surge"),
    ("47,000", "women killed by relatives, 2025"),
    ("$41bn", "Sanofi buys Insmed"),
    ("5–1", "Real Madrid rout PSV"),
]


def split_lines(canvas, text, size, limit):
    """Break text into lines that fit `limit` pixels at `size` points."""
    face = load(PLAIN, size)
    out, current = [], ""
    for word in text.split():
        attempt = f"{current} {word}".strip()
        if current and canvas.textlength(attempt, font=face) > limit:
            out.append(current)
            current = word
        else:
            current = attempt
    if current:
        out.append(current)
    return out


def paint_masthead(canvas):
    canvas.rectangle([0, 0, PAGE_W, 118], fill=MIDNIGHT)
    canvas.text((36, 14), "THE WORLD IN ONE DAY", font=load(BOLD, 21), fill=BRASS)
    canvas.text((36, 40), "Tuesday 24 November 2026", font=load(DISPLAY, 46),
                fill=(255, 255, 255))
    canvas.text((36, 94), "40 stories  \u00b7  every region  \u00b7  one page",
                font=load(PLAIN, 16), fill=(196, 208, 224))
    canvas.text((812, 48), "24 NOV", font=load(DISPLAY, 34), fill=(255, 255, 255))
    canvas.text((812, 86), "2026", font=load(BOLD, 18), fill=BRASS)


def paint_leads(canvas):
    top = 130
    canvas.rectangle([24, top, PAGE_W - 24, top + 152], fill=BAND)
    slot = 312
    for index, card in enumerate(LEAD_CARDS):
        x = 40 + index * (slot + 12)
        big = card["star"]
        head_px = 23 if big else 20
        deck_px = 16 if big else 15
        deck_gap = 21 if big else 20
        canvas.text((x, top + 12), card["headline"], font=load(BOLD, head_px),
                    fill=CRIMSON if big else INK)
        rows = split_lines(canvas, card["deck"], deck_px, slot - 6)
        pen = top + 46
        for row in rows[:5]:
            canvas.text((x, pen), row, font=load(PLAIN, deck_px), fill=SOFT_INK)
            pen += deck_gap
    return top + 164


def paint_column(canvas, column, start_y):
    y = start_y
    face = load(PLAIN, 19)
    for section in column["sections"]:
        x, width = column["x"], column["width"]
        canvas.rectangle([x, y, x + width, y + 28], fill=section["colour"])
        canvas.text((x + 10, y + 5), section["title"], font=load(BOLD, 18),
                    fill=(255, 255, 255))
        y += 34
        for item in section["items"]:
            if canvas.textlength(item, font=face) > width - 26:
                raise ValueError(f"story too wide for its column: {item!r}")
            canvas.text((x + 4, y), "\u2022", font=load(BOLD, 19),
                        fill=section["colour"])
            canvas.text((x + 22, y), item, font=face, fill=INK)
            y += 23
        y += 4
    return y


def paint_numbers(canvas, top):
    canvas.rectangle([24, top, PAGE_W - 24, top + 54], outline=HAIRLINE, width=2)
    canvas.text((40, top + 2), "THE DAY IN NUMBERS", font=load(BOLD, 13),
                fill=MIDNIGHT)
    slot = 40
    for value, caption in DAY_NUMBERS:
        canvas.text((slot, top + 17), value, font=load(DISPLAY, 20), fill=CRIMSON)
        canvas.text((slot, top + 38), caption, font=load(PLAIN, 9), fill=GREY)
        slot += 192


def build():
    sheet = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    canvas = ImageDraw.Draw(sheet)
    paint_masthead(canvas)
    below_leads = paint_leads(canvas)
    ends = [paint_column(canvas, column, below_leads) for column in COLUMNS]
    paint_numbers(canvas, max(ends) + 2)
    canvas.text((24, PAGE_H - 16),
                "Sources: AP, Reuters, AFP, Al Jazeera, The Guardian, UEFA and national reports of 24 Nov 2026.",
                font=load(PLAIN, 11), fill=GREY)
    target = Path(__file__).resolve().parent / "entry.png"
    sheet.save(target, format="PNG", optimize=True)
    print(target, target.stat().st_size, "bytes")


if __name__ == "__main__":
    build()
