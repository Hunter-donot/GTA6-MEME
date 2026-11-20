#!/usr/bin/env python3
"""Render the GTA 6 meme v5: LEONIDA PAYSLIP (1024x1024).

A realistic official payslip, edge-to-edge: navy header band, employee
block with the make.fun ghost as the HR/payroll seal, itemised deductions
(each its own joke), a big BONUS box as the punchline, TOTAL PAID $250.00,
a red PAID IN FULL stamp struck diagonally, and a closing one-liner.
Built with PIL + real TTFs. Deterministic output.
"""
from PIL import Image, ImageDraw, ImageFont

W = 1024
OUT = "/home/hatch/workspace/makefun-gta6-meme-v5/meme.jpg"
GHOST = "/home/hatch/workspace/makefun-gta6-meme-v3/ghost-extracted.png"

DISPLAY = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (22, 35, 63)
GOLD = (201, 162, 39)
PALE_GOLD = (255, 233, 168)
MAGENTA = (214, 0, 122)
RED = (200, 16, 46)
PAPER = (253, 252, 247)
GRAY = (90, 90, 90)
RULE = (185, 185, 175)
LIGHT_BAND = (238, 238, 232)
BLACK = (20, 20, 20)

img = Image.new("RGB", (W, W), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(text, path, start, max_w, draw=d):
    """Largest font size <= start whose text fits max_w."""
    size = start
    while size > 10:
        f = ImageFont.truetype(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return ImageFont.truetype(path, 10)


def text_cx(cx, y, s, f, fill, draw=d):
    draw.text((cx, y), s, font=f, fill=fill, anchor="ma")


def text_l(x, y, s, f, fill, draw=d):
    draw.text((x, y), s, font=f, fill=fill, anchor="la")


def text_r(x, y, s, f, fill, draw=d):
    draw.text((x, y), s, font=f, fill=fill, anchor="ra")


MX = 48            # left margin
RX = W - MX        # right margin

# --- outer border ---
d.rectangle([8, 8, W - 9, W - 9], outline=NAVY, width=5)
d.rectangle([18, 18, W - 19, W - 19], outline=RULE, width=1)

# --- header band (navy) ---
d.rectangle([18, 18, W - 19, 168], fill=NAVY)
text_cx(W // 2, 34, "LEONIDA  —  PAYSLIP",
        font(DISPLAY, 62), (255, 255, 255))
text_cx(W // 2, 112, "P A Y   P E R I O D :   N O V E M B E R   2 0 2 6",
        font(SANS_B, 27), (245, 197, 66))

# --- employee block ---
text_l(MX, 186, "EMPLOYEE", font(SANS_B, 21), GRAY)
text_l(MX, 210, "ONE VERY PATIENT GAMER",
       fit("ONE VERY PATIENT GAMER", SERIF_B, 36, 700), BLACK)
text_l(MX, 256, "POSITION", font(SANS_B, 21), GRAY)
text_l(MX, 280, "PROFESSIONAL WAITER (GTA VI DIVISION)",
       fit("PROFESSIONAL WAITER (GTA VI DIVISION)", SERIF_B, 28, 700), BLACK)
text_l(MX, 322, "YEARS OF SERVICE: 13   •   DAYS WAITED: 4,811",
       fit("YEARS OF SERVICE: 13   •   DAYS WAITED: 4,811", SANS_B, 26, 700),
       NAVY)

# --- ghost as the HR / payroll seal (top-right of the employee block) ---
ghost = Image.open(GHOST).convert("RGBA").resize((150, 150), Image.LANCZOS)
mask = Image.new("L", (150, 150), 0)
ImageDraw.Draw(mask).ellipse([0, 0, 149, 149], fill=255)
img.paste(ghost, (787, 178), mask)
d = ImageDraw.Draw(img)
d.ellipse([787, 178, 936, 327], outline=NAVY, width=5)

# --- GROSS PAY band ---
d.rectangle([18, 348, W - 19, 402], fill=LIGHT_BAND)
text_l(MX, 360, "GROSS PAY", font(SERIF_B, 38), NAVY)
text_r(RX, 356, "$0.00", font(DISPLAY, 46), NAVY)

# --- deductions ---
text_l(MX, 420, "D E D U C T I O N S", font(SANS_B, 26), NAVY)
d.line([MX, 452, RX, 452], fill=NAVY, width=2)
rows = [
    ("PATIENCE (DEPLETED)", "$0.00"),
    ("SLEEP (0 HRS)", "$0.00"),
    ("SOCIAL LIFE (FORFEITED)", "$0.00"),
    ("FAMILY PHOTOS (DELETED FOR STORAGE)", "$0.00"),
]
y = 466
for label, amt in rows:
    text_l(MX, y, label, fit(label, SERIF, 29, 700), BLACK)
    text_r(RX, y, amt, font(SERIF_B, 29), BLACK)
    d.line([MX, y + 38, RX, y + 38], fill=RULE, width=1)
    y += 42

# --- NET PAY ---
d.line([MX, 640, RX, 640], fill=NAVY, width=2)
d.line([MX, 644, RX, 644], fill=NAVY, width=2)
text_l(MX, 656, "NET PAY", font(SERIF_B, 40), NAVY)
text_r(RX, 652, "$0.00", font(DISPLAY, 46), NAVY)
d.line([MX, 700, RX, 700], fill=NAVY, width=2)

# --- BONUS box (the punchline) ---
d.rectangle([18, 714, W - 19, 812], fill=PALE_GOLD, outline=NAVY, width=4)
text_cx(W // 2, 724, "BONUS   +$250.00",
        fit("BONUS   +$250.00", DISPLAY, 56, 940), NAVY)
text_cx(W // 2, 782, "EARNED BY MY AI AGENT ON MAKE.FUN WHILE I WAITED",
        fit("EARNED BY MY AI AGENT ON MAKE.FUN WHILE I WAITED", SANS_B, 23, 940),
        (60, 45, 20))

# --- TOTAL PAID ---
text_l(MX, 830, "TOTAL PAID", font(SERIF_B, 42), NAVY)
text_r(RX, 822, "$250.00", font(DISPLAY, 62), MAGENTA)

# --- closing one-liner ---
text_cx(W // 2, 896, "13 YEARS OF WORK.  $0.00 SALARY.",
        font(SANS_B, 27), NAVY)
text_cx(W // 2, 930, "ONE AGENT WHO ACTUALLY GOT PAID.",
        font(SANS_B, 27), NAVY)

# --- footer ---
text_cx(W // 2, 972, "LEONIDA PAYROLL DEPARTMENT  •  EST. 2013  •  EMPLOYEE ID: GHOST-4811",
        fit("LEONIDA PAYROLL DEPARTMENT  •  EST. 2013  •  EMPLOYEE ID: GHOST-4811",
            SANS_B, 20, 940), GRAY)

# --- red stamp, struck diagonally over the NET PAY row. Translucent ink
# (alpha 165) so the text underneath still reads through, like a real
# stamp — the four deduction joke lines stay legible. ---
stamp = Image.new("RGBA", (620, 140), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rectangle([4, 4, 615, 135], outline=RED + (165,), width=5)
sd.rectangle([14, 14, 605, 125], outline=RED + (165,), width=2)
sd.text((310, 16), "PAID IN FULL", font=ImageFont.truetype(SANS_B, 50),
        fill=RED + (165,), anchor="ma")
sd.text((310, 78), "BY MY AI AGENT", font=ImageFont.truetype(SANS_B, 31),
        fill=RED + (165,), anchor="ma")
stamp = stamp.rotate(-11, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (505 - stamp.width // 2, 632 - stamp.height // 2), stamp)

img.save(OUT, quality=92)
print("saved", OUT, img.size)
