"""Endkarte des Beach-Craft-Reviews (wie dreamcraft/tiktok/tools/endcard.py): verschwommenes Floss-Standbild mit
Meeres-Verlauf, aufsteigende Luftblasen, Titel BEACH CRAFT, vier Standbilder aus dem Review und "FREE ON CURSEFORGE".
  python tools/endcard.py   -> $SP/video/cards/endcard_review/f%05d.jpg (150 Bilder) und ../stills/endcard_review.png
env BC_STILLS = Querformat-Standbilder des Film-Laufs (Standard $SP/film/bc/stills), BC_TILES = vier Namen, Komma (Standard raft_tour, shark_attack, crops, portal_light)."""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cut
W, H = cut.W, cut.H
SP = cut.SP
STILLS = os.environ.get('BC_STILLS', SP + '/film/bc/stills')
FONT = cut.CAPTION_FONT
VIOLET, DEEP, WHITE, SAND = (24, 132, 186), (10, 42, 78), (255, 255, 255), (238, 214, 160)
CF_ORANGE = (241, 100, 54)
N = 150
TILES = os.environ.get('BC_TILES', 'raft_tour,shark_attack,crops,portal_light').split(',')


def crops_still():
    """'crops' is cut from a portrait frame of bc_crops (2.4 s: the plot row ripe, the farmland row still green)."""
    p, src = f'{STILLS}/crops.png', f'{SP}/film/bc/bc_crops/f00072.png'
    if not os.path.exists(p) and os.path.exists(src):
        Image.open(src).convert('RGB').crop((0, 560, 1080, 1168)).save(p)


def background():
    p = f'{STILLS}/{TILES[0]}.png'
    bg = Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (1920, 1080), VIOLET)
    s = H / bg.height
    bg = bg.resize((int(bg.width * s), H), Image.LANCZOS)
    x = (bg.width - W) // 2
    bg = bg.crop((x, 0, x + W, H)).filter(ImageFilter.GaussianBlur(10))
    over = Image.new('RGBA', (W, H))
    d = ImageDraw.Draw(over)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(10 + 10 * t), int(42 + 40 * t), int(78 + 60 * t), int(140 + 80 * t)))
    return Image.alpha_composite(bg.convert('RGBA'), over)


def text_fit(text, size, max_w, fill, stroke, stroke_fill, shadow=None):
    f = ImageFont.truetype(FONT, size)
    while f.getlength(text) + 2 * stroke > max_w:
        size -= 4
        f = ImageFont.truetype(FONT, size)
    asc, desc = f.getmetrics()
    w, h = int(f.getlength(text)) + 2 * stroke + 40, asc + desc + 2 * stroke + 40
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if shadow:
        d.text((20 + stroke + shadow[0], 20 + stroke + shadow[1]), text, font=f, fill=stroke_fill, stroke_width=stroke, stroke_fill=stroke_fill)
    d.text((20 + stroke, 20 + stroke), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    bb = im.getbbox()
    return im.crop((max(0, bb[0] - 6), max(0, bb[1] - 6), min(w, bb[2] + 6), min(h, bb[3] + 6)))


def rounded(im, r):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255)
    out = im.convert('RGBA')
    out.putalpha(m)
    return out


def mosaic():
    """Four landscape stills of the pack in a white rounded frame (2 x 2)."""
    tw, th, gap = 470, 264, 14
    inner = Image.new('RGBA', (2 * tw + gap, 2 * th + gap), WHITE + (255,))
    for k, name in enumerate(TILES):
        p = f'{STILLS}/{name}.png'
        im = Image.open(p).convert('RGB') if os.path.exists(p) else Image.new('RGB', (1920, 1080), DEEP)
        s = max(tw / im.width, th / im.height)
        im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
        x, y = (im.width - tw) // 2, (im.height - th) // 2
        inner.alpha_composite(rounded(im.crop((x, y, x + tw, y + th)), 22), ((k % 2) * (tw + gap), (k // 2) * (th + gap)))
    frame = Image.new('RGBA', (inner.width + 28, inner.height + 28), (0, 0, 0, 0))
    ImageDraw.Draw(frame).rounded_rectangle([0, 0, frame.width - 1, frame.height - 1], 36, fill=WHITE + (255,))
    frame.alpha_composite(inner, (14, 14))
    shadow = Image.new('RGBA', (frame.width + 60, frame.height + 60), (0, 0, 0, 0))
    shadow.paste((20, 0, 40, 130), (30, 40), frame.split()[3])
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    shadow.alpha_composite(frame, (30, 30))
    return shadow


def layers():
    logo = text_fit('BEACH CRAFT', 190, W - 80, WHITE, 14, DEEP, shadow=(0, 14))
    tag = text_fit('SURVIVE THE ENDLESS SEA ON A RAFT', 58, W - 110, SAND, 8, DEEP)
    pill = pill_img(['FREE ON CURSEFORGE'], [92])
    return logo, tag, mosaic(), pill


def pill_img(lines, sizes):
    parts = [text_fit(t, s, W - 200, WHITE, 8, (110, 40, 10)) for t, s in zip(lines, sizes)]
    gap = 10
    h = sum(p.height for p in parts) + gap * (len(parts) - 1) + 2 * 34
    w = max(p.width for p in parts) + 2 * 56
    im = Image.new('RGBA', (w, h + 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 14, w - 1, h + 13], 60, fill=(150, 56, 20, 255))
    d.rounded_rectangle([0, 0, w - 1, h - 1], 60, fill=CF_ORANGE + (255,), outline=WHITE + (255,), width=8)
    y = 34
    for p in parts:
        im.alpha_composite(p, ((w - p.width) // 2, y))
        y += p.height + gap
    return im


def pop(t, start, dur=0.45):
    """0 before `start`, then an overshoot to 1 (bounce in)."""
    x = (t - start) / dur
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    return 1 + 2.2 * (x - 1) ** 3 + 1.2 * (x - 1) ** 2


def scaled(im, s):
    if abs(s - 1) < 0.005:
        return im
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)


def paste_c(canvas, im, cx, cy):
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def frame(t, bg, L, sparks):
    logo, tag, mos, pill = L
    f = bg.copy()
    d = ImageDraw.Draw(f)
    for (x, y0, sp, sz, ph, col) in sparks:            # dream sparks rising and twinkling
        y = (y0 - sp * t) % (H + 100) - 50
        a = 0.45 + 0.55 * abs(math.sin(t * 2.2 + ph))
        r = int(sz * (0.6 + 0.4 * a))
        c = col + (int(230 * a),)
        xx = x + 10 * math.sin(t * 1.3 + ph)
        d.rectangle([xx - r, y - 3, xx + r, y + 3], fill=c)
        d.rectangle([xx - 3, y - r, xx + 3, y + r], fill=c)
    paste_c(f, scaled(logo, max(0.01, pop(t, 0.05))), W / 2, 330 + 6 * math.sin(t * 2))
    paste_c(f, scaled(tag, max(0.01, pop(t, 0.35))), W / 2, 560)
    paste_c(f, scaled(mos, max(0.01, pop(t, 0.2))), W / 2, 930)
    paste_c(f, scaled(pill, max(0.01, pop(t, 0.6)) * (1 + 0.025 * math.sin(t * 5))), W / 2, 1360)
    return f.convert('RGB')


def make(still_dir, frames_dir):
    rnd = random.Random(26)
    bg = background()
    L = layers()
    sparks = [(rnd.randint(40, W - 40), rnd.randint(0, H + 100), rnd.uniform(30, 90), rnd.randint(10, 24), rnd.uniform(0, 6),
               rnd.choice([(170, 230, 255), (120, 214, 236), (255, 255, 255)])) for _ in range(26)]
    os.makedirs(frames_dir, exist_ok=True)
    for i in range(N):
        im = frame(i / 30, bg, L, sparks)
        im.save(f'{frames_dir}/f{i:05d}.jpg', quality=94)
        if i == 60:
            os.makedirs(still_dir, exist_ok=True)
            im.save(f'{still_dir}/endcard_review.png')


if __name__ == '__main__':
    crops_still()
    make(os.path.join(HERE, '..', 'stills'), f'{SP}/video/cards/endcard_review')
    print('endcard done')
