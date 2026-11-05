"""Endkarte der Beach-Craft-3.0-Doku (nach beachcraft/review/tools/endcard.py, ruhiger): unscharfes Standbild mit
Meeres-Verlauf, aufsteigende Luftblasen, Titel BEACH CRAFT 3.0, Untertitel TIDES OF THE DEEP, vier Bilder aus dem Film,
"FREE ON CURSEFORGE" und "LINK IN DESCRIPTION".
  python3 -I tools/endcard.py   -> $SP/doc3/cards/endcard/f%05d.jpg (240 Bilder, 8 s) und stills/endcard.png
env DOC_TILES = vier Standbild-Namen (Komma), DOC_BG = Hintergrund."""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.environ.get('SP') or '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad'
SHOTS = SP + '/doc4/shots'
FONTS = os.environ.get('FONTS') or os.path.abspath(os.path.join(HERE, '..', '..', '..', 'fonts'))
W, H, N = 1920, 1080, 480
DEEP, WHITE, SAND, AQUA = (8, 34, 62), (255, 255, 255), (238, 214, 160), (110, 222, 238)
CF_ORANGE = (241, 100, 54)
TILES = os.environ.get('DOC_TILES', 'p_saltmere_air,b_coral,p_rig_air,p_temple_air').split(',')
BG = os.environ.get('DOC_BG', 'p_lighthouse_air')


def load(name):
    p = f'{SHOTS}/{name}.jpg'
    if os.path.exists(p):
        return Image.open(p).convert('RGB')
    m = f'{SHOTS}/{name}.mp4'                        # a clip: its middle frame
    if os.path.exists(m):
        import subprocess, io
        r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '2', '-i', m, '-frames:v', '1', '-f', 'image2pipe', '-c:v', 'png', '-'],
                           capture_output=True)
        if r.stdout:
            return Image.open(io.BytesIO(r.stdout)).convert('RGB')
    return Image.new('RGB', (1920, 1080), DEEP)


def background():
    bg = load(BG).resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(14))
    over = Image.new('RGBA', (W, H))
    d = ImageDraw.Draw(over)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(6 + 8 * t), int(30 + 30 * t), int(60 + 50 * t), int(150 + 80 * t)))
    return Image.alpha_composite(bg.convert('RGBA'), over)


def text_img(text, font, size, fill, stroke, stroke_fill, track=0, max_w=W - 120):
    f = ImageFont.truetype(font, size)
    def width(fn):
        return sum(fn.getlength(c) for c in text) + track * (len(text) - 1)
    while width(f) + 2 * stroke > max_w:
        size -= 4
        f = ImageFont.truetype(font, size)
    asc, desc = f.getmetrics()
    w, h = int(width(f)) + 2 * stroke + 40, asc + desc + 2 * stroke + 40
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 20 + stroke
    for c in text:
        d.text((x, 20 + stroke), c, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
        x += f.getlength(c) + track
    sh = im.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda a: int(a * 0.55))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    out.paste((0, 0, 0, 255), (0, 8), sh)
    out.alpha_composite(im)
    bb = out.getbbox()
    return out.crop(bb)


def rounded(im, r):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255)
    out = im.convert('RGBA')
    out.putalpha(m)
    return out


def mosaic():
    tw, th, gap = 400, 225, 14
    inner = Image.new('RGBA', (2 * tw + gap, 2 * th + gap), (0, 0, 0, 0))
    for k, name in enumerate(TILES):
        im = load(name)
        s = max(tw / im.width, th / im.height)
        im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
        x, y = (im.width - tw) // 2, (im.height - th) // 2
        inner.alpha_composite(rounded(im.crop((x, y, x + tw, y + th)), 26), ((k % 2) * (tw + gap), (k // 2) * (th + gap)))
    frame = Image.new('RGBA', (inner.width + 24, inner.height + 24), (0, 0, 0, 0))
    ImageDraw.Draw(frame).rounded_rectangle([0, 0, frame.width - 1, frame.height - 1], 36, fill=(255, 255, 255, 235))
    frame.alpha_composite(inner, (12, 12))
    sh = Image.new('RGBA', (frame.width + 60, frame.height + 60), (0, 0, 0, 0))
    sh.paste((0, 10, 30, 140), (30, 42), frame.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    sh.alpha_composite(frame, (30, 30))
    return sh


def pill(text, size, sub=None):
    t = text_img(text, FONTS + '/InterDisplay-Bold.otf', size, WHITE, 0, (0, 0, 0), track=2)
    pad_x, pad_y = 64, 30
    w, h = t.width + 2 * pad_x, t.height + 2 * pad_y
    im = Image.new('RGBA', (w, h + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 12, w - 1, h + 11], h // 2, fill=(150, 56, 20, 255))
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=CF_ORANGE + (255,), outline=WHITE + (255,), width=6)
    im.alpha_composite(t, ((w - t.width) // 2, (h - t.height) // 2))
    return im


def ease(t, start, dur=0.9):
    x = min(1.0, max(0.0, (t - start) / dur))
    return x * x * (3 - 2 * x)


def paste(canvas, im, cx, cy, a=1.0, dy=0.0):
    if a <= 0.01:
        return
    if a < 0.999:
        im = im.copy()
        im.putalpha(im.split()[3].point(lambda v: int(v * a)))
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2 + dy)))


def make(still_dir, frames_dir):
    rnd = random.Random(30)
    bg = background()
    logo = text_img('BEACH CRAFT 3.1', FONTS + '/InterDisplay-Black.otf', 112, WHITE, 0, DEEP, track=4, max_w=820)
    sub = text_img('TIDES OF THE DEEP', FONTS + '/InterDisplay-SemiBold.otf', 56, AQUA, 0, DEEP, track=12, max_w=820)
    mos = mosaic()
    p1 = pill('FREE ON CURSEFORGE', 74)
    link = text_img('LINK IN DESCRIPTION', FONTS + '/InterDisplay-SemiBold.otf', 50, SAND, 0, DEEP, track=8)
    bubbles = [(rnd.randint(30, W - 30), rnd.randint(0, H + 200), rnd.uniform(40, 110), rnd.randint(6, 16), rnd.uniform(0, 6)) for _ in range(34)]
    os.makedirs(frames_dir, exist_ok=True)
    for i in range(N):
        t = i / 60
        f = bg.copy()
        d = ImageDraw.Draw(f)
        for (x, y0, sp, r, ph) in bubbles:
            y = (y0 - sp * t) % (H + 200) - 100
            xx = x + 8 * math.sin(t * 1.4 + ph)
            d.ellipse([xx - r, y - r, xx + r, y + r], outline=(200, 240, 255, 150), width=3)
        paste(f, logo, W * 0.265, 330, ease(t, 0.2), 30 * (1 - ease(t, 0.2)))
        paste(f, sub, W * 0.265, 450, ease(t, 0.7), 20 * (1 - ease(t, 0.7)))
        paste(f, mos, W * 0.745, 520, ease(t, 0.4), 40 * (1 - ease(t, 0.4)))
        paste(f, p1, W * 0.265, 690 + 6 * math.sin(t * 2.2), ease(t, 1.2))
        paste(f, link, W * 0.265, 820, ease(t, 1.6))
        out = f.convert('RGB')
        out.save(f'{frames_dir}/f{i:05d}.jpg', quality=93)
        if i == 240:
            os.makedirs(still_dir, exist_ok=True)
            out.save(f'{still_dir}/endcard.png')


if __name__ == '__main__':
    make(os.path.join(HERE, '..', 'stills'), f'{SP}/doc4/cards/endcard')
    print('endcard done')
