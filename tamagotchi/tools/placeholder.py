"""Platzhalter-Footage zum Testen der Pipeline: je Shot ein Ordner mit farbigen Bildern (Shot-Name, Zaehler, laufender
Balken, damit Schnitt, Tempo und Haltephasen sichtbar sind). 540x960, wird beim Rendern auf 1080x1920 hochskaliert.
  python tools/placeholder.py          -> $SP/video/film_ph/<shot>/f%05d.jpg   (3-6 s je Shot, 30 fps)
Der echte Film-Ordner ($SP/film/tama) wird nie angefasst."""
import os, sys, hashlib, colorsys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cut
from script import SCRIPTS


def shots():
    seen = []
    for sc in SCRIPTS.values():
        for p in sc:
            for s, _ in p['shots']:
                s = s.rstrip('?')
                if s != 'endcard' and s not in seen:
                    seen.append(s)
    return seen


def make(root):
    font = ImageFont.truetype(cut.CAPTION_FONT, 64)
    small = ImageFont.truetype(cut.CAPTION_FONT, 36)
    for i, s in enumerate(shots()):
        d = f'{root}/{s}'
        if os.path.isdir(d) and len(os.listdir(d)) > 10:
            continue
        os.makedirs(d, exist_ok=True)
        h = int(hashlib.md5(s.encode()).hexdigest()[:6], 16) / 0xFFFFFF
        n = int((3.0 + (i % 7) * 0.5) * 30)                    # 3.0 ... 6.0 s
        c1 = tuple(int(255 * x) for x in colorsys.hsv_to_rgb(h, 0.45, 0.95))
        c2 = tuple(int(255 * x) for x in colorsys.hsv_to_rgb((h + 0.12) % 1, 0.7, 0.55))
        for k in range(n):
            im = Image.new('RGB', (540, 960))
            dr = ImageDraw.Draw(im)
            for y in range(0, 960, 4):
                t = y / 960
                dr.rectangle([0, y, 540, y + 3], fill=tuple(int(a + (b - a) * t) for a, b in zip(c1, c2)))
            x = 40 + (k / max(1, n - 1)) * 460
            dr.ellipse([x - 40, 560, x + 40, 640], fill=(255, 255, 255), outline=(0, 0, 0), width=4)   # the "pet"
            dr.rectangle([240, 700, 300, 780], fill=(30, 30, 30))                                     # the "player"
            dr.text((270, 300), s, font=font, fill=(255, 255, 255), anchor='mm', stroke_width=4, stroke_fill=(0, 0, 0))
            dr.text((270, 380), f'{k / 30:.2f}s  frame {k}/{n}', font=small, fill=(255, 255, 255), anchor='mm', stroke_width=3, stroke_fill=(0, 0, 0))
            im.save(f'{d}/f{k:05d}.jpg', quality=80)


if __name__ == '__main__':
    root = f'{cut.SP}/video/film_ph'
    make(root)
    print('placeholders in', root, len(os.listdir(root)), 'shots')
