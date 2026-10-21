"""Endkarte der Tamagotchi-Videos (Tamagotchi-Stil: rosa Punkte, Ei-Geraet und Pets aus dem CurseForge-Header).
  python tools/endcard.py          -> $SP/video/cards/endcard_short|long/f%05d.jpg (150 Bilder, 30 fps, leicht animiert)
                                      und ../stills/endcard_short.png, endcard_long.png
Der Header kommt aus dem Mod-Repo (docs/curseforge/img/header.png); env TAMA_REPO ueberschreibt /home/user/Tamagotchi."""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cut
W, H = cut.W, cut.H
REPO = os.environ.get('TAMA_REPO', '/home/user/Tamagotchi')
HEADER = REPO + '/docs/curseforge/img/header.png'
FONT = cut.CAPTION_FONT
CRIMSON, DARK, WHITE = (214, 52, 104), (150, 24, 72), (255, 255, 255)
CF_ORANGE = (241, 100, 54)
N = 150
HEART = ["..XX.XX..", ".XXXXXXX.", "XXXXXXXXX", "XXXXXXXXX", ".XXXXXXX.", "..XXXXX..", "...XXX...", "....X...."]


def background():
    bg = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(255 - 6 * t), int(222 + 8 * t), int(236 - 4 * t)))
    dots = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for r, y in enumerate(range(20, H, 60)):
        for x in range(20 + (30 if r % 2 else 0), W, 60):
            dd.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(255, 244, 248, 255))
    bg = Image.alpha_composite(bg.convert('RGBA'), dots)
    return bg


def heart_img(px, color):
    im = Image.new('RGBA', (9 * px, 8 * px), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for j, row in enumerate(HEART):
        for i, c in enumerate(row):
            if c == 'X':
                d.rectangle([i * px, j * px, (i + 1) * px - 1, (j + 1) * px - 1], fill=color + (255,))
    return im


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


def layers(kind):
    # the art band: egg + pets of the CurseForge header, in a white rounded frame
    hd = Image.open(HEADER).convert('RGB')
    hdd = ImageDraw.Draw(hd)
    hdd.rectangle([260, 104, 740, 138], fill=(255, 232, 242))          # paint out the tagline of the header ...
    hdd.ellipse([487, 129, 513, 155], fill=(150, 134, 170))            # ... and redraw the egg's ring
    hdd.ellipse([493, 135, 507, 149], fill=(238, 232, 248))
    band = hd.crop((0, 112, 1000, 460)).resize((1000, 348), Image.LANCZOS)
    frame = Image.new('RGBA', (1000 + 28, 348 + 28), (0, 0, 0, 0))
    fd = ImageDraw.Draw(frame)
    fd.rounded_rectangle([0, 0, frame.width - 1, frame.height - 1], 40, fill=WHITE + (255,))
    frame.alpha_composite(rounded(band, 30), (14, 14))
    shadow = Image.new('RGBA', (frame.width + 60, frame.height + 60), (0, 0, 0, 0))
    shadow.paste((120, 20, 60, 110), (30, 38), frame.split()[3])
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    shadow.alpha_composite(frame, (30, 30))
    title = text_fit('Tamagotchi', 230, W - 90, WHITE, 16, CRIMSON, shadow=(0, 14))
    tag = text_fit('Find them. Tame them. Love them.', 60, W - 120, CRIMSON, 0, CRIMSON)
    if kind == 'long':
        pill = pill_img(['FREE ON CURSEFORGE', 'Link in Description'], [84, 58])
    else:
        pill = pill_img(['FREE ON CURSEFORGE'], [92])
    return shadow, title, tag, pill


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
    return 1 + 2.2 * (x - 1) ** 3 + 1.2 * (x - 1) ** 2 if x > 0 else 0.0


def scaled(im, s):
    if abs(s - 1) < 0.005:
        return im
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BICUBIC)


def paste_c(canvas, im, cx, cy):
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def frame(kind, t, bg, L, hearts, sparks):
    shadow, title, tag, pill = L
    f = bg.copy()
    for (x, y0, sp, px, col, ph) in hearts:
        y = (y0 - sp * t) % (H + 200) - 100
        paste_c(f, heart_img(px, col), x + 14 * math.sin(t * 1.6 + ph), y)
    for (x, y, sz, ph) in sparks:
        a = 0.5 + 0.5 * math.sin(t * 3 + ph)
        d = ImageDraw.Draw(f)
        c = (255, 214, 64, int(255 * a))
        r = int(sz * (0.6 + 0.4 * a))
        d.rectangle([x - r, y - 3, x + r, y + 3], fill=c)
        d.rectangle([x - 3, y - r, x + 3, y + r], fill=c)
    paste_c(f, scaled(title, max(0.01, pop(t, 0.05))), W / 2, 400 + 6 * math.sin(t * 2))
    paste_c(f, scaled(tag, max(0.01, pop(t, 0.35))), W / 2, 590)
    paste_c(f, scaled(shadow, max(0.01, pop(t, 0.2))), W / 2, 880)
    paste_c(f, scaled(pill, max(0.01, pop(t, 0.6)) * (1 + 0.025 * math.sin(t * 5))), W / 2, 1250)
    return f.convert('RGB')


def make(kind, still_dir, frames_dir):
    rnd = random.Random(7)
    bg = background()
    L = layers(kind)
    hearts = [(rnd.randint(40, W - 40), rnd.randint(0, H + 200), rnd.uniform(25, 70), rnd.choice([5, 6, 8, 10]),
               rnd.choice([(255, 120, 170), (240, 80, 130), (255, 160, 200)]), rnd.uniform(0, 6)) for _ in range(16)]
    sparks = [(rnd.randint(60, W - 60), rnd.randint(60, 1500), rnd.randint(14, 26), rnd.uniform(0, 6)) for _ in range(14)]
    os.makedirs(frames_dir, exist_ok=True)
    for i in range(N):
        im = frame(kind, i / 30, bg, L, hearts, sparks)
        im.save(f'{frames_dir}/f{i:05d}.jpg', quality=94)
        if i == 60:
            os.makedirs(still_dir, exist_ok=True)
            im.save(f'{still_dir}/endcard_{kind}.png')


if __name__ == '__main__':
    SP = cut.SP
    for kind in (sys.argv[1:] or ['short', 'long']):
        make(kind, os.path.join(HERE, '..', 'stills'), f'{SP}/video/cards/endcard_{kind}')
        print('endcard', kind, 'done')
