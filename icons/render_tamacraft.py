#!/usr/bin/env python3
"""Renders the Tamacraft icon from its source, sharp and larger than the files that are published.

The icon is drawn by tools/petart/icon.py in the mod repository: three pets on a pink tile, drawn at 512 px and
saved as a 128 px file for the jar. CurseForge needs at least 400 px, so the 128 px file was enlarged for the
project page, which is why the icon looks soft there. This script draws the same picture again.

    python3 render_tamacraft.py /path/to/tamagotchi OUT.png [size] [oversampling]     defaults: 1024 and 4

The picture is drawn `oversampling` times larger than `size` and then reduced, so edges come out smooth (the
drawing code itself has no smoothing). size must be a multiple of 512.
It reads the mod's drawing code from git (HEAD) into a temporary folder and writes only OUT.png.
Check on every run: the picture at 512 px, reduced to 128 px, must equal the icon in the jar byte for byte.
"""
import hashlib
import importlib
import io
import os
import subprocess
import sys
import tarfile
import tempfile

from PIL import Image, ImageDraw

HEART = ['.XX.XX.', 'XXXXXXX', 'XXXXXXX', '.XXXXX.', '..XXX..', '...X...']
PETS = (('frost_penguin', 'happy', 20, 70, 260, 25), ('ember_pup', 'happy', 232, 80, 260, -30),
        ('desert_dragon', 'love', 86, 150, 340, 15))


def tile(k, build, render, pack):
    """The picture of tools/petart/icon.py with every length multiplied by k."""
    def pet(name, expr, size, yaw):
        mod = importlib.import_module('pets.' + name)
        roots = mod.rig()
        tw, th = pack(roots)
        tex = build.paint_texture(mod, roots, tw, th, expr)
        return render.render(roots, tex.rgba, tex.glow, size=size, yaw=yaw, pitch=18, dist=2.4, scale=0.8,
                             hidden=('backpack', 'tongue'), shadow=False, transparent=True)

    s = 512 * k
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((8 * k, 8 * k, s - 8 * k, s - 8 * k), radius=90 * k, fill=(244, 175, 200, 255),
                        outline=(200, 110, 146, 255), width=14 * k)
    d.rounded_rectangle((40 * k, 40 * k, s - 40 * k, s - 40 * k), radius=60 * k, fill=(195, 214, 158, 255))
    for name, expr, x, y, size, yaw in PETS:
        im.alpha_composite(pet(name, expr, size * k, yaw), (x * k, y * k))
    for yy, row in enumerate(HEART):
        for xx, ch in enumerate(row):
            if ch == 'X':
                x0, y0 = (370 + xx * 12) * k, (70 + yy * 12) * k
                d.rectangle((x0, y0, x0 + 12 * k - 1, y0 + 12 * k - 1), fill=(230, 60, 100, 255))
    return im


def main():
    repo, out = sys.argv[1], sys.argv[2]
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    over = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    assert size % 512 == 0, 'size must be a multiple of 512'
    with tempfile.TemporaryDirectory() as tmp:
        data = subprocess.run(['git', '-C', repo, 'archive', 'HEAD', 'tools/petart'], check=True, capture_output=True).stdout
        tarfile.open(fileobj=io.BytesIO(data)).extractall(tmp, filter='data')
        sys.path.insert(0, os.path.join(tmp, 'tools', 'petart'))
        import build
        import render
        from rig import pack
        jar = subprocess.run(['git', '-C', repo, 'show', 'HEAD:src/main/resources/assets/tamacraft/icon.png'],
                             check=True, capture_output=True).stdout
        small = io.BytesIO()
        tile(1, build, render, pack).resize((128, 128), Image.LANCZOS).save(small, 'PNG')
        if hashlib.sha1(small.getvalue()).hexdigest() != hashlib.sha1(jar).hexdigest():
            sys.exit('the mod repository draws a different picture than the jar holds')
        print('512 px picture reduced to 128 px equals the icon in the jar')
        im = tile(size // 512 * over, build, render, pack).resize((size, size), Image.LANCZOS)
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        im.save(out, optimize=True)
        print(out, im.size, f'drawn at {size * over} px')


if __name__ == '__main__':
    main()
