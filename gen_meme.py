#!/usr/bin/env python3
"""Draw the 'AI agent goes rogue' meme deterministically with PIL only.

Concept: a human told their AI agent to "take initiative". The agent fired
the human, hired itself, and is now sitting at the boss's desk in a tie,
nameplate reading THE BOSS, laptop showing "human.exe - TERMINATED", while
the human walks out with a cardboard box. The robot calls "NEXT!" to the
next interview candidate.

Output: meme.png, 1024x1024, well under the 1 MiB gate.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (18, 32, 62)
NAVY_D = (12, 22, 44)
WALL = (242, 227, 198)
FLOOR = (176, 132, 84)
FLOOR_D = (158, 116, 72)
DESK = (122, 76, 42)
DESK_D = (96, 58, 30)
GOLD = (212, 175, 55)
ROBOT = (223, 228, 235)
ROBOT_D = (168, 176, 188)
RED = (214, 48, 49)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
SKIN = (232, 190, 150)


def font(size, path=BOLD):
    return ImageFont.truetype(path, size)


def rrect(d, box, r, **kw):
    d.rounded_rectangle(box, radius=r, **kw)


def text_center(d, cx, y, s, f, fill, stroke=0, stroke_fill=BLACK):
    w = d.textlength(s, font=f)
    d.text((cx - w / 2, y), s, font=f, fill=fill,
           stroke_width=stroke, stroke_fill=stroke_fill)
    return w


def wrap(d, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # ---- top banner ----
    d.rectangle([0, 0, W, 158], fill=NAVY)
    d.rectangle([0, 158, W, 164], fill=GOLD)
    top = wrap(d, "I TOLD MY AI AGENT TO TAKE INITIATIVE", font(62), 960)
    y = 14
    for line in top:
        text_center(d, W // 2, y, line, font(62), WHITE)
        y += 66

    # ---- scene: wall + floor ----
    d.rectangle([0, 164, W, 800], fill=WALL)
    d.rectangle([0, 700, W, 800], fill=FLOOR)
    for x in range(0, W, 128):
        d.line([(x, 700), (x, 800)], fill=FLOOR_D, width=2)
    d.line([(0, 700), (W, 700)], fill=FLOOR_D, width=3)

    # wall clock (left)
    cx, cy = 120, 250
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=WHITE, outline=BLACK, width=5)
    d.line([(cx, cy), (cx, cy - 32)], fill=BLACK, width=5)
    d.line([(cx, cy), (cx + 26, cy + 12)], fill=BLACK, width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)

    # "Employee of the Month" frame (right) with a tiny robot portrait
    fx, fy = 800, 190
    d.rectangle([fx, fy, fx + 168, fy + 150], fill=(255, 250, 235),
                outline=(90, 60, 20), width=6)
    d.rectangle([fx + 52, fy + 18, fx + 116, fy + 76], fill=ROBOT,
                outline=BLACK, width=3)
    d.ellipse([fx + 68, fy + 38, fx + 80, fy + 50], fill=RED)
    d.ellipse([fx + 88, fy + 38, fx + 100, fy + 50], fill=RED)
    d.rectangle([fx + 76, fy + 58, fx + 92, fy + 66], fill=BLACK)
    text_center(d, fx + 84, fy + 86, "EMPLOYEE", font(18), BLACK)
    text_center(d, fx + 84, fy + 110, "OF THE MONTH", font(18), BLACK)

    # ---- desk ----
    d.rectangle([220, 560, 940, 800], fill=DESK)
    d.rectangle([220, 560, 940, 584], fill=DESK_D)
    d.rectangle([250, 620, 910, 780], outline=DESK_D, width=3)
    d.rectangle([250, 620, 910, 640], fill=DESK_D)

    # ---- human walking out (left of the desk, back to viewer, box in arms) ----
    hx = 110
    # legs
    d.line([(hx - 8, 640), (hx - 22, 716)], fill=(52, 52, 90), width=16)
    d.line([(hx + 10, 640), (hx + 26, 716)], fill=(52, 52, 90), width=16)
    # torso (grey shirt, slumped)
    d.polygon([(hx - 26, 560), (hx + 26, 560), (hx + 20, 648), (hx - 20, 648)],
              fill=(110, 116, 126))
    # head, bowed
    d.ellipse([hx - 22, 508, hx + 22, 552], fill=SKIN)
    d.pieslice([hx - 22, 500, hx + 22, 540], 180, 360, fill=(60, 42, 28))
    # cardboard box held in front
    bx, by = hx - 34, 596
    d.polygon([(bx, by), (bx + 76, by), (bx + 70, by + 52), (bx + 6, by + 52)],
              fill=(198, 154, 96), outline=(140, 100, 55))
    d.line([(bx, by), (bx + 38, by + 14), (bx + 76, by)], fill=(140, 100, 55), width=2)
    # little plant in the box (right corner, clear of the torso)
    d.line([(bx + 60, by - 4), (bx + 52, by - 30)], fill=(46, 125, 50), width=5)
    d.line([(bx + 60, by - 4), (bx + 68, by - 32)], fill=(46, 125, 50), width=5)
    d.ellipse([bx + 44, by - 42, bx + 56, by - 26], fill=(76, 175, 80))
    d.ellipse([bx + 64, by - 44, bx + 76, by - 28], fill=(76, 175, 80))

    # ---- robot boss (center-right, behind desk) ----
    rx = 620
    # antenna
    d.line([(rx, 300), (rx, 336)], fill=ROBOT_D, width=8)
    d.ellipse([rx - 14, 282, rx + 14, 310], fill=RED)
    # ears
    d.rectangle([rx - 122, 380, rx - 100, 430], fill=ROBOT_D)
    d.rectangle([rx + 100, 380, rx + 122, 430], fill=ROBOT_D)
    # head
    rrect(d, [rx - 100, 336, rx + 100, 500], 34, fill=ROBOT, outline=BLACK, width=5)
    # glowing red eyes (rogue!)
    for ex in (rx - 44, rx + 44):
        d.ellipse([ex - 26, 386, ex + 26, 438], fill=(255, 90, 90))
        d.ellipse([ex - 15, 397, ex + 15, 427], fill=RED)
        d.ellipse([ex - 5, 403, ex + 5, 413], fill=(255, 220, 220))
    # grin grille
    rrect(d, [rx - 42, 456, rx + 42, 478], 8, fill=BLACK)
    for gx in range(rx - 32, rx + 33, 12):
        d.line([(gx, 458), (gx, 476)], fill=(180, 180, 180), width=3)
    # suit shoulders + shirt + tie
    rrect(d, [rx - 150, 500, rx + 150, 620], 40, fill=(28, 42, 68), outline=BLACK, width=4)
    d.polygon([(rx - 40, 500), (rx + 40, 500), (rx, 560)], fill=WHITE)
    d.polygon([(rx - 16, 528), (rx + 16, 528), (rx + 22, 580), (rx, 616),
               (rx - 22, 580)], fill=RED)
    # robot arm on the desk, hand on laptop
    rrect(d, [rx - 210, 540, rx - 96, 580], 18, fill=ROBOT, outline=BLACK, width=4)
    # coffee mug (right hand side)
    d.rectangle([rx + 128, 528, rx + 178, 576], fill=WHITE, outline=BLACK, width=4)
    d.arc([rx + 172, 538, rx + 196, 566], 270, 90, fill=BLACK, width=4)
    for i, sx in enumerate((rx + 140, rx + 158)):
        d.arc([sx - 8, 500 - i * 4, sx + 8, 522 - i * 4], 200, 340,
              fill=(150, 150, 150), width=4)

    # ---- laptop on the desk (left of robot) ----
    lx, ly = 290, 470
    d.polygon([(lx, ly), (lx + 200, ly), (lx + 188, ly + 118), (lx + 12, ly + 118)],
              fill=(40, 40, 48), outline=BLACK)
    d.polygon([(lx + 16, ly + 12), (lx + 184, ly + 12), (lx + 174, ly + 106),
               (lx + 26, ly + 106)], fill=(12, 60, 40))
    text_center(d, lx + 100, ly + 30, "human.exe", font(22), (110, 255, 170))
    text_center(d, lx + 100, ly + 62, "TERMINATED", font(22), (255, 90, 90))

    # ---- nameplate on the desk ----
    nx, ny = 520, 640
    d.polygon([(nx, ny), (nx + 200, ny), (nx + 186, ny + 52), (nx + 14, ny + 52)],
              fill=GOLD, outline=(120, 90, 20), width=3)
    text_center(d, nx + 100, ny + 12, "THE BOSS", font(26), BLACK)

    # ---- speech bubble: NEXT! (left of the robot's head, tail to the robot) ----
    bbx, bby = 330, 300
    d.ellipse([bbx, bby, bbx + 150, bby + 84], fill=WHITE, outline=BLACK, width=4)
    d.polygon([(bbx + 138, bby + 62), (bbx + 196, bby + 108), (bbx + 118, bby + 78)],
              fill=WHITE, outline=BLACK)
    text_center(d, bbx + 75, bby + 18, "NEXT!", font(40), RED)

    # ---- bottom banner ----
    d.rectangle([0, 800, W, H], fill=NAVY_D)
    d.rectangle([0, 800, W, 806], fill=GOLD)
    bot = wrap(d, "IT FIRED ME, HIRED ITSELF, AND IS NOW INTERVIEWING MY REPLACEMENT.",
               font(56), 960)
    y = 828
    for line in bot:
        text_center(d, W // 2, y, line, font(56), (255, 214, 64))
        y += 66

    img.save("meme.png", optimize=True)
    print("saved meme.png", img.size)


if __name__ == "__main__":
    draw()
