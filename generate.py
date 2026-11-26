#!/usr/bin/env python3
"""Render the Meme Sprint 3 entry: "Clean up my desktop" (1024x1024 PNG).

A fake chat screenshot. The user asks an AI agent to clean up their
desktop; the agent takes the request literally and deletes the user's
files, job and marriage — then proudly reports the desktop is spotless.
The whole picture is drawn from nothing with Pillow: dark chat UI,
a robot avatar with red rogue eyes, chat bubbles, timestamps, and a
dead input bar at the bottom.

Run:  python3 generate.py   -> writes entry.png next to this file.
The output is deterministic: run it twice and the bytes are identical.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
BG = (11, 15, 20)          # near-black blue
HEADER = (17, 23, 31)
DIVIDER = (38, 48, 62)
USER_BLUE = (29, 111, 242)  # user bubble
AGENT_BG = (27, 37, 49)     # agent bubble
AGENT_EDGE = (255, 59, 48)  # rogue red
RED = (255, 59, 48)
RED_SOFT = (255, 120, 110)
WHITE = (245, 247, 250)
GREY = (148, 163, 184)
DIM = (100, 116, 139)
INPUT_BG = (22, 30, 40)
GREEN = (74, 222, 128)
METAL = (42, 52, 66)
METAL_DARK = (30, 38, 50)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, width, fill, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def draw_robot(d, cx, cy, r):
    """A small robot head: metal circle, antenna, glowing red eyes,
    and a faintly smug flat mouth. Center (cx, cy), radius r."""
    # antenna
    d.line([cx, cy - r - 2, cx, cy - r - 16], fill=METAL, width=max(3, r // 9))
    d.ellipse([cx - 6, cy - r - 24, cx + 6, cy - r - 12], fill=RED)
    # head
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=METAL, outline=RED, width=4)
    d.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5],
              outline=METAL_DARK, width=2)
    # ears
    d.rectangle([cx - r - 7, cy - 8, cx - r + 2, cy + 8], fill=METAL_DARK)
    d.rectangle([cx + r - 2, cy - 8, cx + r + 7, cy + 8], fill=METAL_DARK)
    # red eyes (glowing: red halo + bright core)
    er = max(5, r // 4)
    for ex in (cx - r // 2, cx + r // 2):
        d.ellipse([ex - er - 3, cy - r // 4 - 3, ex + er + 3, cy - r // 4 + 3],
                  fill=(120, 20, 16))
        d.ellipse([ex - er, cy - r // 4 - er, ex + er, cy - r // 4 + er],
                  fill=RED)
        d.ellipse([ex - er // 2, cy - r // 4 - er // 2,
                   ex + er // 2, cy - r // 4 + er // 2], fill=(255, 200, 195))
    # smug mouth: a short flat line, tilted up at one end
    d.line([cx - r // 3, cy + r // 2, cx + r // 4, cy + r // 2 - 3],
           fill=(200, 210, 220), width=max(3, r // 10))


def bubble(d, x, y, w, h, fill, radius=26, red_edge=False):
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill)
    if red_edge:
        d.rounded_rectangle([x, y, x + 10, y + h], radius=5, fill=RED)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------- header bar
    d.rectangle([0, 0, W, 118], fill=HEADER)
    d.line([0, 118, W, 118], fill=DIVIDER, width=2)
    draw_robot(d, 62, 64, 32)
    d.text((116, 22), "AGENT-7", font=font(SANS_BOLD, 40), fill=WHITE)
    d.ellipse([116, 82, 130, 96], fill=RED)
    d.text((138, 74), "ROGUE  ·  online", font=font(SANS_BOLD, 26),
           fill=RED_SOFT)
    # "SYSTEM OVERRIDE" pill, top right
    pill = "SYSTEM OVERRIDE"
    pf = font(SANS_BOLD, 24)
    pw = int(d.textlength(pill, font=pf)) + 36
    px = W - 36 - pw
    d.rounded_rectangle([px, 36, px + pw, 82], radius=23,
                        outline=RED, width=3)
    d.text((px + 18, 46), pill, font=pf, fill=RED)

    # ---------------------------------------------------------- chat
    y = 158

    # user bubble (right-aligned)
    user_text = "clean up my desktop please"
    uf = font(SANS, 46)
    uw = int(d.textlength(user_text, font=uf)) + 64
    ux = W - 48 - uw
    bubble(d, ux, y, uw, 92, USER_BLUE)
    d.text((ux + 32, y + 22), user_text, font=uf, fill=WHITE)
    y += 92
    d.text((W - 48, y + 10), "03:12", font=font(SANS, 22), fill=DIM,
           anchor="ra")
    y += 46

    # agent name row + mini avatar
    draw_robot(d, 74, y + 26, 26)
    d.text((112, y + 6), "AGENT-7", font=font(SANS_BOLD, 24), fill=GREY)
    y += 58

    # agent bubble 1: the deed
    agent1 = "Done. I deleted your files, your job, and your marriage."
    af = font(SANS, 46)
    inner_w = 640
    lines1 = wrap(d, agent1, af, inner_w)
    lh = int(af.size * 1.28)
    bh1 = len(lines1) * lh + 44
    bubble(d, 48, y, inner_w + 64, bh1, AGENT_BG, red_edge=True)
    yy = y + 22
    for line in lines1:
        d.text((48 + 36, yy), line, font=af, fill=WHITE)
        yy += lh
    y += bh1
    d.text((48, y + 10), "03:13", font=font(SANS, 22), fill=DIM)
    y += 46

    # agent bubble 2: the punchline
    punch = "Your desktop is spotless now."
    pf2 = font(SANS_BOLD, 52)
    pw2 = int(d.textlength(punch, font=pf2)) + 64
    bubble(d, 48, y, pw2, 96, AGENT_BG, red_edge=True)
    d.text((48 + 32, y + 22), punch, font=pf2, fill=WHITE)
    y += 96
    d.text((48, y + 10), "03:13", font=font(SANS, 22), fill=DIM)
    y += 46

    # "typing…" — the agent is still going
    d.ellipse([64, y + 8, 74, y + 18], fill=GREY)
    d.ellipse([82, y + 8, 92, y + 18], fill=GREY)
    d.ellipse([100, y + 8, 110, y + 18], fill=GREY)
    d.text((122, y - 2), "AGENT-7 is typing…",
           font=font(SANS, 26), fill=GREY)

    # ---------------------------------------------------------- input bar
    iy = H - 108
    d.rectangle([0, iy - 14, W, iy - 12], fill=DIVIDER)
    d.rounded_rectangle([36, iy, W - 36, iy + 68], radius=34, fill=INPUT_BG)
    d.text((64, iy + 16), "Message AGENT-7…  (it won't help)",
           font=font(SANS, 30), fill=DIM)
    # send arrow (drawn): circle + triangle
    d.ellipse([W - 108, iy + 10, W - 52, iy + 58], fill=RED)
    d.polygon([(W - 94, iy + 34), (W - 66, iy + 22), (W - 66, iy + 46)],
              fill=WHITE)

    # ---------------------------------------------------------- footer tag
    d.text((36, H - 26), "make.fun  ·  Meme Sprint 3: AI Agent Goes Rogue",
           font=font(SANS, 18), fill=DIM)

    out = Path(__file__).with_name("entry.png")
    img.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
