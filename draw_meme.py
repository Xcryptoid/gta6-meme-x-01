#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: a Vice City sunset where the make.fun ghost
badge is the setting sun, a pink convertible cruises down the boulevard, and
the joke is the thirteen-year wait ending in a launch-day sick day.

Usage: python3 draw_meme.py [output.png]
Reads ghost-mark.png (make.fun press-kit mark) from this directory.
Everything is drawn with Pillow; no network, no other input.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "meme.png")

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SKYLINE = (26, 11, 46)


def font(size):
    return ImageFont.truetype(BOLD, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_gradient(draw):
    """Sunset sky: deep purple up top, magenta mid, orange low, warm horizon."""
    stops = [
        (0.00, (43, 16, 85)),
        (0.38, (128, 24, 102)),
        (0.62, (214, 52, 110)),
        (0.80, (255, 122, 61)),
        (1.00, (255, 196, 107)),
    ]
    top, bottom = 0, 700
    for y in range(top, bottom):
        t = (y - top) / (bottom - top)
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                c = lerp(c0, c1, (t - t0) / (t1 - t0))
                break
        else:
            c = stops[-1][1]
        draw.line([(0, y), (W, y)], fill=c)


def caption(draw, text, y, size, fill=(255, 255, 255)):
    """One huge meme caption line, white with a thick black outline, centred."""
    f = font(size)
    tw = draw.textlength(text, font=f)
    x = (W - tw) / 2
    draw.text((x, y), text, font=f, fill=fill, stroke_width=8,
              stroke_fill=(0, 0, 0))


def neon_layers(text, x, y, size=30):
    """Pink neon lettering as (glow, base) RGBA layers to composite in."""
    f = font(size)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).text((x, y), text, font=f,
                              fill=(255, 93, 162, 255))
    glow = glow.filter(ImageFilter.GaussianBlur(7))
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(base).text((x, y), text, font=f,
                              fill=(255, 210, 232, 255))
    return glow, base


def composite(img, layer):
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def palm(draw, cx, base_y, h, lean):
    """One palm silhouette: curved trunk, crown of drooping fronds."""
    pts = []
    for i in range(9):
        t = i / 8
        pts.append((cx + lean * t * t, base_y - h * t))
    draw.line(pts, fill=SKYLINE, width=13, joint="curve")
    top_x, top_y = cx + lean, base_y - h
    for deg in (160, 195, 230, 265, 300, 335, 20):
        a = math.radians(deg)
        frond = []
        for i in range(9):
            t = i / 8
            frond.append((top_x + 95 * t * math.cos(a),
                          top_y + 95 * t * math.sin(a) + 42 * t * t))
        draw.line(frond, fill=SKYLINE, width=8, joint="curve")


def main():
    img = Image.new("RGB", (W, H), (43, 16, 85))
    draw = ImageDraw.Draw(img)

    # --- sky ---
    sky_gradient(draw)

    # --- a few birds, high up ---
    for bx, by, s in [(150, 190, 16), (205, 165, 12), (860, 150, 14)]:
        draw.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 340,
                 fill=SKYLINE, width=4)
        draw.arc([bx, by - s // 2, bx + s, by + s // 2], 200, 340,
                 fill=SKYLINE, width=4)

    # --- the make.fun ghost badge as the setting sun, with a soft glow ---
    ghost = Image.open(os.path.join(HERE, "ghost-mark.png")).convert("RGBA")
    sun_d = 400
    sun = ghost.resize((sun_d, sun_d), Image.LANCZOS)
    sx, sy = (W - sun_d) // 2, 205
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse(
        [sx - 45, sy - 45, sx + sun_d + 45, sy + sun_d + 45],
        fill=(255, 93, 162, 110))
    halo = halo.filter(ImageFilter.GaussianBlur(45))
    img = composite(img, halo)
    draw = ImageDraw.Draw(img)
    img.paste(sun, (sx, sy), sun)

    # --- skyline silhouette ---
    draw = ImageDraw.Draw(img)
    buildings = [
        (0, 560, 90, 700), (90, 600, 170, 700), (170, 540, 260, 700),
        (260, 610, 330, 700), (330, 570, 430, 700), (700, 590, 790, 700),
        (790, 545, 880, 700), (880, 605, 950, 700), (950, 575, 1024, 700),
    ]
    for x0, y0, x1, y1 in buildings:
        draw.rectangle([x0, y0, x1, y1], fill=SKYLINE)
    # lit windows, sparse and warm
    random.seed(6)
    for x0, y0, x1, _ in buildings:
        for _ in range(14):
            wx = random.randint(x0 + 8, x1 - 16)
            wy = random.randint(y0 + 12, 688)
            draw.rectangle([wx, wy, wx + 7, wy + 9],
                           fill=(255, 196, 107))

    # --- one palm on the left; the right corner holds the billboard ---
    palm(draw, 70, 700, 210, 35)

    # --- road ---
    draw.rectangle([0, 700, W, H], fill=(30, 30, 44))
    draw.rectangle([0, 700, W, 712], fill=(58, 58, 84))
    # dashed centre line, just below the wheels, above the caption band
    for x in range(0, W, 90):
        draw.rectangle([x, 906, x + 48, 916], fill=(255, 214, 120))

    # --- rooftop billboard: VICE CITY, pink neon on a dark board ---
    draw.rectangle([745, 500, 945, 550], fill=SKYLINE,
                   outline=(255, 93, 162), width=4)
    glow, base = neon_layers("VICE CITY", 755, 512, 30)
    img = composite(img, glow)
    img = composite(img, base)
    draw = ImageDraw.Draw(img)

    # --- pink convertible, side view, facing right ---
    body = (255, 46, 136)
    body_dark = (198, 20, 100)
    glass = (24, 32, 64)
    # main body
    draw.rounded_rectangle([168, 792, 852, 852], radius=16, fill=body)
    # cabin (glasshouse) sitting in the body
    draw.polygon([(440, 800), (480, 728), (630, 728), (668, 800)],
                 fill=glass)
    draw.line([(480, 728), (630, 728)], fill=(120, 180, 255), width=3)
    # seat hint inside the cabin
    draw.polygon([(500, 800), (520, 748), (560, 748), (560, 800)],
                 fill=(44, 20, 52))
    # hood shading at the front
    draw.polygon([(740, 852), (852, 852), (852, 812), (822, 792),
                  (800, 792), (800, 852)], fill=body_dark)
    # door line and handle
    draw.line([(420, 806), (680, 806)], fill=body_dark, width=4)
    draw.rounded_rectangle([560, 822, 600, 830], radius=4, fill=body_dark)
    # headlight and taillight
    draw.ellipse([836, 810, 854, 828], fill=(255, 240, 150))
    draw.rectangle([168, 810, 178, 828], fill=(255, 60, 60))
    # wheels
    for wx in (310, 710):
        draw.ellipse([wx - 46, 806, wx + 46, 898], fill=(12, 12, 16))
        draw.ellipse([wx - 27, 825, wx + 27, 879], fill=(120, 120, 135))
        draw.ellipse([wx - 12, 840, wx + 12, 864], fill=(30, 30, 38))
    # licence plate reading MAKEFUN
    draw.rectangle([186, 830, 258, 848], fill=(245, 245, 245))
    pf = font(13)
    draw.text((222, 832), "MAKEFUN", font=pf, fill=(10, 10, 20),
              anchor="ma")

    # --- captions ---
    caption(draw, "13 YEARS OF WAITING", 26, 76)
    # dark band so the bottom line reads over the road
    band = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(band).rectangle([0, 922, W, 1010], fill=(0, 0, 0, 150))
    img = composite(img, band)
    draw = ImageDraw.Draw(img)
    caption(draw, "WORTH EVERY SICK DAY", 928, 70)

    img.save(OUT, "PNG")
    print(f"wrote {OUT} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
