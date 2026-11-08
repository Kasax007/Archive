"""Beach Craft logo for CurseForge: a small isometric beach chunk (palm island, a raft with a striped sail, shallow
turquoise water) built from the mod's own textures, with the title in Luckiest Guy like the CurseForge page.

  python3 beachcraft/logo/make_logo.py MOD_ROOT FONTS_DIR OUT_DIR [--preview]

MOD_ROOT: a Kasax_Raft_Mod checkout (the textures). FONTS_DIR: Archive/fonts (LuckiestGuy-Regular.ttf).
Vanilla textures (sand, sandstone, water, flowers) come from the Minecraft client jar ($MC_JAR, default: Loom cache).
The scene is drawn three times larger and scaled down (--preview: once, quick). Writes logo_1024.png (the upload),
logo_512.png, logo_400.png, logo_256.png, icon_1024.png (the scene alone), icon_128.png (the in-game mod icon,
src/main/resources/assets/raft/icon.png: 128 px stays sharp where Mod Menu draws it at 32 GUI pixels) and preview.png
(the logo at the sizes CurseForge shows it, on a light and a dark page)."""
import io
import math
import os
import sys
import zipfile

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT, FONTS, OUT = sys.argv[1:4]
SS = 1 if '--preview' in sys.argv else 3
N = 1024 * SS
MAIN = os.path.join(ROOT, 'src', 'main')
JAR = zipfile.ZipFile(os.environ.get('MC_JAR')
                      or os.path.expanduser('~/.gradle/caches/fabric-loom/26.3/minecraft-client.jar'))
TITLE_FONT = os.path.join(FONTS, 'LuckiestGuy-Regular.ttf')

NAVY = (10, 42, 78)            # outline colour of every title on the CurseForge page
SAND = (238, 214, 160)


# ----------------------------------------------------------------------------------------------- textures
def tex(path):
    """Mod texture 'module:kind/name' (module '' = the 2.0 resources), first frame."""
    mod, rel = path.split(':', 1)
    base = os.path.join(MAIN, 'modules', mod) if mod else os.path.join(MAIN, 'resources')
    im = Image.open(os.path.join(base, 'assets', 'raft', 'textures', rel + '.png')).convert('RGBA')
    return im.crop((0, 0, im.width, im.width))


def van(rel):
    """Vanilla texture 'block/x', first frame."""
    im = Image.open(io.BytesIO(JAR.read('assets/minecraft/textures/%s.png' % rel))).convert('RGBA')
    return im.crop((0, 0, im.width, im.width))


def shade(im, f):
    if f == 1:
        return im
    r, g, b, a = im.split()
    r, g, b = (c.point(lambda v: min(255, int(v * f))) for c in (r, g, b))
    return Image.merge('RGBA', (r, g, b, a))


def ramp(im, c0, c1, lo, hi, alpha=255):
    """Grey texture (water) coloured from c0 (grey lo) to c1 (grey hi)."""
    g = im.convert('L')
    lut = [[int(c0[k] + (c1[k] - c0[k]) * min(1, max(0, (v - lo) / (hi - lo)))) for v in range(256)] for k in range(3)]
    out = Image.merge('RGB', [g.point(lut[k]) for k in range(3)]).convert('RGBA')
    out.putalpha(alpha)
    return out


def solid(im, under):
    """Cut-out texture over a solid colour (leaves as with 'fast' graphics: a clean shape when small)."""
    return Image.alpha_composite(Image.new('RGBA', im.size, under + (255,)), im)


T = {
    'sand': van('block/sand'), 'sandstone': van('block/sandstone'), 'sandstone_top': van('block/sandstone_top'),
    'shell': tex('world:block/shell_sand'),
    'log': tex(':block/palm_log'), 'log_top': tex(':block/palm_log_top'),
    'leaves': solid(tex(':block/palm_leaves'), (40, 104, 38)),
    'cleaves': solid(tex(':block/palm_coconut_leaves'), (40, 104, 38)),
    'raft': tex(':block/raft_foundation'), 'pole': tex(':block/stripped_palm_log'),
    'sail': tex(':block/sail_canvas_red_striped'), 'flag': tex(':block/raft_flag'),
    'coconut': tex(':item/coconut'), 'grass': tex('world:block/beach_grass'),
    'hibiscus': tex('world:block/hibiscus'), 'plumeria': tex('world:block/plumeria'),
}
WATER = van('block/water_still')
T['water_top'] = ramp(WATER, (34, 160, 206), (170, 240, 248), 165, 255, alpha=168)
T['water_side'] = ramp(WATER, (22, 118, 176), (90, 200, 232), 165, 255, alpha=214)


# ----------------------------------------------------------------------------------------------- projection
A = 55 * SS                    # block edge on screen: x -> (A, A/2), z -> (-A, A/2), y -> (0, -A)
O = [0.0, 0.0]                 # screen position of the world origin (set by place())
LIGHT = (1.0, 0.8, 0.62)       # top, +z (left) and +x (right) faces, as Minecraft lights a block in the inventory


def P(x, y, z):
    return (O[0] + (x - z) * A, O[1] + (x + z) * A / 2 - y * A)


def tiled(t, u1, v1):
    w, h = t.width * max(1, math.ceil(u1 / 16 - 1e-6)), t.height * max(1, math.ceil(v1 / 16 - 1e-6))
    if (w, h) == t.size:
        return t
    out = Image.new('RGBA', (w, h))
    for x in range(0, w, t.width):
        for y in range(0, h, t.height):
            out.paste(t, (x, y))
    return out


def quad(layer, t, p0, pu, pv, uv=(0, 0, 16, 16), alpha=1.0):
    """Texture region uv (texels, 16 per block, tiles beyond 16) on the parallelogram p0 (u0,v0), pu (u1,v0),
    pv (u0,v1)."""
    p3 = (pu[0] + pv[0] - p0[0], pu[1] + pv[1] - p0[1])
    pts = (p0, pu, p3, pv)
    bx, by = math.floor(min(p[0] for p in pts)), math.floor(min(p[1] for p in pts))
    w, h = math.ceil(max(p[0] for p in pts)) - bx, math.ceil(max(p[1] for p in pts)) - by
    u0, v0, u1, v1 = uv
    ex = ((pu[0] - p0[0]) / (u1 - u0), (pu[1] - p0[1]) / (u1 - u0))
    ey = ((pv[0] - p0[0]) / (v1 - v0), (pv[1] - p0[1]) / (v1 - v0))
    det = ex[0] * ey[1] - ey[0] * ex[1]
    if w <= 0 or h <= 0 or abs(det) < 1e-9:
        return
    a, b = ey[1] / det, -ey[0] / det
    d, e = -ex[1] / det, ex[0] / det
    c = u0 + a * (bx - p0[0]) + b * (by - p0[1])
    f = v0 + d * (bx - p0[0]) + e * (by - p0[1])
    img = tiled(t, u1, v1).transform((w, h), Image.AFFINE, (a, b, c, d, e, f), resample=Image.NEAREST,
                                     fillcolor=(0, 0, 0, 0))
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).polygon([(p[0] - bx, p[1] - by) for p in pts], fill=int(255 * alpha))
    img.putalpha(ImageChops.multiply(img.getchannel('A'), m))
    layer.alpha_composite(img, (bx, by))


def box(layer, x0, y0, z0, x1, y1, z1, top, side, side_x=None, faces='tzx', uv=None, alpha=1.0, light=LIGHT):
    """Block-like box; faces: t = top, z = +z face (left), x = +x face (right). uv: per face texel regions."""
    uv = uv or {}
    side_x = side_x or side
    if 'z' in faces:
        quad(layer, shade(side, light[1]), P(x0, y1, z1), P(x1, y1, z1), P(x0, y0, z1),
             uv.get('z', (16 * (x0 % 1), 16 * (1 - y1 % 1 if y1 % 1 else 0), 16 * (x0 % 1) + 16 * (x1 - x0),
                          16 * (1 - y1 % 1 if y1 % 1 else 0) + 16 * (y1 - y0))), alpha)
    if 'x' in faces:
        quad(layer, shade(side_x, light[2]), P(x1, y1, z1), P(x1, y1, z0), P(x1, y0, z1),
             uv.get('x', (16 * (1 - z1 % 1 if z1 % 1 else 0), 16 * (1 - y1 % 1 if y1 % 1 else 0),
                          16 * (1 - z1 % 1 if z1 % 1 else 0) + 16 * (z1 - z0),
                          16 * (1 - y1 % 1 if y1 % 1 else 0) + 16 * (y1 - y0))), alpha)
    if 't' in faces:
        quad(layer, shade(top, light[0]), P(x0, y1, z0), P(x1, y1, z0), P(x0, y1, z1),
             uv.get('t', (16 * (x0 % 1), 16 * (z0 % 1), 16 * (x0 % 1) + 16 * (x1 - x0),
                          16 * (z0 % 1) + 16 * (z1 - z0))), alpha)


def sprite(layer, t, x, y, z, size=1.0):
    """Flat plant or item standing at (x, y, z), facing the viewer (a cross plant shows one face in this view)."""
    s = size * A
    quad(layer, t, P(x - size / 2 * 0.5, y + size, z + size / 2 * 0.5), P(x + size / 2 * 0.5, y + size, z - size / 2 * 0.5),
         P(x - size / 2 * 0.5, y, z + size / 2 * 0.5))
    return s


# ----------------------------------------------------------------------------------------------- the scene
SIZE = 8
ISLAND = {  # (x, z): height of the sand (1 = one block above the sea floor, i.e. at sea level)
    (0, 0): 2, (1, 0): 2, (2, 0): 2, (3, 0): 1, (4, 0): 1,
    (0, 1): 2, (1, 1): 2, (2, 1): 2, (3, 1): 1,
    (0, 2): 2, (1, 2): 2, (2, 2): 1, (3, 2): 1,
    (0, 3): 1, (1, 3): 1, (2, 3): 1,
    (0, 4): 1, (1, 4): 1, (2, 4): 1,
    (0, 5): 1, (1, 5): 1,
    (0, 6): 1,
}
SHELL = {(3, 1), (1, 4), (0, 5), (2, 3)}
PALM = (1, 1)                  # trunk on the dune
TRUNK = 5
RAFT = [(x, z) for x in (5, 6) for z in (2, 3, 4)]
MAST = (5.95, 3.35)            # mast foot (x, z) on the raft


def scene():
    """Every drawable as (depth, function); drawn far to near (depth = x + y + z of its centre)."""
    items = []
    solid_at = {}

    def block(x, y, z, kind):
        solid_at[(x, y, z)] = kind

    for x in range(SIZE):
        for z in range(SIZE):
            block(x, -2, z, 'sandstone')
            block(x, -1, z, 'sand')
            hgt = ISLAND.get((x, z), 0)
            for y in range(hgt):
                block(x, y, z, 'shell' if (x, z) in SHELL and y == hgt - 1 else 'sand')
            if not hgt:
                block(x, 0, z, 'water')
    px, pz = PALM
    base = ISLAND[PALM]
    ty = base + TRUNK - 1      # top log (the trunk is drawn below, slender and leaning a little to the left)

    opaque = {'sand', 'shell', 'sandstone', 'log'}

    def is_opaque(p):
        return solid_at.get(p) in opaque

    def voxel(x, y, z, kind):
        def draw(layer):
            if kind == 'water':
                faces = ''
                if solid_at.get((x, y + 1, z)) is None:
                    faces += 't'
                if not is_opaque((x, y, z + 1)) and solid_at.get((x, y, z + 1)) != 'water':
                    faces += 'z'
                if not is_opaque((x + 1, y, z)) and solid_at.get((x + 1, y, z)) != 'water':
                    faces += 'x'
                if 'z' in faces or 'x' in faces:
                    box(layer, x, y, z, x + 1, y + 14 / 16, z + 1, T['water_top'], T['water_side'],
                        faces=faces.replace('t', ''), uv={'z': (0, 2, 16, 16), 'x': (0, 2, 16, 16)})
                if 't' in faces:
                    box(layer, x, y, z, x + 1, y + 14 / 16, z + 1, T['water_top'], T['water_side'], faces='t')
                return
            faces = ''.join(f for f, n in (('t', (x, y + 1, z)), ('z', (x, y, z + 1)), ('x', (x + 1, y, z)))
                            if not is_opaque(n))
            if not faces:
                return
            top = {'sand': T['sand'], 'shell': T['shell'], 'sandstone': T['sandstone_top'], 'log': T['log_top']}[kind]
            side = {'sand': T['sand'], 'shell': T['shell'], 'sandstone': T['sandstone'], 'log': T['log']}[kind]
            box(layer, x, y, z, x + 1, y + 1, z + 1, top, side, faces=faces)
        return (x + y + z + 1.5, draw)

    for (x, y, z), kind in solid_at.items():
        items.append(voxel(x, y, z, kind))

    # the trunk: slender rings of palm log, leaning a little to the left
    lean = (-0.07, 0.07)                      # per block: straight to the left on screen
    for i in range(TRUNK):
        cx_, cz_ = px + 0.5 + lean[0] * i, pz + 0.5 + lean[1] * i
        hw = 0.36 - 0.015 * i

        def ring(layer, cx_=cx_, cz_=cz_, hw=hw, y=base + i):
            u0 = 8 - 16 * hw
            box(layer, cx_ - hw, y, cz_ - hw, cx_ + hw, y + 1, cz_ + hw, T['log_top'], T['log'],
                uv={'t': (u0, u0, 16 - u0, 16 - u0), 'z': (u0, 0, 16 - u0, 16), 'x': (u0, 0, 16 - u0, 16)})
        items.append((cx_ + cz_ + base + i + 0.5, ring))
    ccx, ccz = px + 0.5 + lean[0] * TRUNK, pz + 0.5 + lean[1] * TRUNK
    cy = base + TRUNK                         # top of the trunk

    # the crown: a small leaf cap and fronds of half-thick leaves that arch out and hang down
    leaf = [(ccx - 0.62, cy - 0.15, ccz - 0.62, ccx + 0.62, cy + 0.45, ccz + 0.62, 'cleaves')]
    path = [(0.95, 0.12), (1.65, 0.02), (2.35, -0.2), (3.0, -0.5), (3.55, -0.88), (3.95, -1.3)]
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        for k, (d, y0) in enumerate(path):
            half = 0.44 if k < 4 else 0.34
            cx_, cz_ = ccx + dx * d, ccz + dz * d
            wx, wz = (0.45, half) if dx else (half, 0.45)
            leaf.append((cx_ - wx, cy + y0, cz_ - wz, cx_ + wx, cy + y0 + 0.42, cz_ + wz, 'leaves'))
    # fronds to the left and right of the screen (the diagonals across the view) and a short one at the back
    for (dx, dz), n in (((0.7071, -0.7071), 6), ((-0.7071, 0.7071), 6), ((-0.7071, -0.7071), 2)):
        for k, (d, y0) in enumerate(path[:n]):
            h = 0.36 if k < 4 else 0.28
            cx_, cz_ = ccx + dx * d, ccz + dz * d
            leaf.append((cx_ - h, cy + y0 + 0.08, cz_ - h, cx_ + h, cy + y0 + 0.48, cz_ + h, 'leaves'))
    for x0, y0, z0, x1, y1, z1, t in leaf:
        def frond(layer, b=(x0, y0, z0, x1, y1, z1), t=t):
            box(layer, *b, T[t], T[t], uv={'t': (0, 0, 16 * (b[3] - b[0]), 16 * (b[5] - b[2])),
                                           'z': (0, 0, 16 * (b[3] - b[0]), 16 * (b[4] - b[1])),
                                           'x': (0, 0, 16 * (b[5] - b[2]), 16 * (b[4] - b[1]))})
        items.append(((x0 + x1) / 2 + (y0 + y1) / 2 + (z0 + z1) / 2, frond))

    # coconuts under the cap, next to the trunk
    for dx, dz, dy in ((0.6, -0.2, 0.0), (-0.2, 0.6, 0.0), (0.42, 0.42, -0.22)):
        cx, cz = ccx + dx, ccz + dz
        c = T['coconut'].crop((4, 4, 12, 12))

        def coco(layer, cx=cx, cz=cz, c=c, y0=cy - 0.42 + dy):
            box(layer, cx - 0.15, y0, cz - 0.15, cx + 0.15, y0 + 0.3, cz + 0.15, c, c,
                uv={'t': (0, 0, 8, 8), 'z': (0, 0, 8, 8), 'x': (0, 0, 8, 8)})
        items.append((cx + cz + cy - 0.27 + dy, coco))

    # plants on the sand
    for (x, z), t, s in (((3.5, 1.45), 'grass', 0.9), ((0.5, 3.5), 'grass', 0.8), ((4.45, 0.5), 'hibiscus', 0.8),
                         ((2.5, 2.5), 'plumeria', 0.75), ((1.5, 5.5), 'grass', 0.7), ((0.5, 6.5), 'hibiscus', 0.6)):
        y = ISLAND[(int(x), int(z))]

        def plant(layer, x=x, z=z, y=y, t=t, s=s):
            sprite(layer, T[t], x, y, z, s)
        items.append((x + z + y + 0.4, plant))

    # the raft: foundation tiles riding on the water, mast, yard, striped sail and flag
    for (x, z) in RAFT:
        def tile(layer, x=x, z=z):
            box(layer, x + 0.02, 0.62, z + 0.02, x + 0.98, 1.0, z + 0.98, T['raft'], T['raft'],
                uv={'z': (0, 0, 15.4, 6), 'x': (0, 0, 15.4, 6)})
        items.append((x + z + 0.81 + 1.0, tile))
    mx, mz = MAST
    pole = T['pole']
    top = 5.35

    def mast(layer):
        box(layer, mx - 0.08, 1.0, mz - 0.08, mx + 0.08, top, mz + 0.08, pole, pole,
            uv={'z': (6, 0, 8.6, 16 * (top - 1)), 'x': (6, 0, 8.6, 16 * (top - 1)), 't': (6, 6, 8.6, 8.6)})
    items.append((mx + mz + 2.0, mast))
    sz = mz - 0.14                       # the sail hangs just behind the mast
    sx0, sx1, sy0, sy1 = mx - 1.25, mx + 1.25, 1.6, 4.6

    def sail(layer):
        quad(layer, T['sail'], P(sx0, sy1, sz), P(sx1, sy1, sz), P(sx0, sy0, sz), uv=(0, 0, 16, 16))
        box(layer, sx0 - 0.1, sy1, sz - 0.06, sx1 + 0.1, sy1 + 0.12, sz + 0.06, pole, pole,
            uv={'z': (0, 6, 43, 7.9), 'x': (6, 6, 7.9, 7.9), 't': (0, 6, 43, 7.9)})
        box(layer, sx0 - 0.05, sy0 - 0.1, sz - 0.05, sx1 + 0.05, sy0, sz + 0.05, pole, pole,
            uv={'z': (0, 6, 41, 7.6), 'x': (6, 6, 7.6, 7.6), 't': (0, 6, 41, 7.6)})
    items.append((mx + mz + 2.0 - 0.3, sail))

    def flag(layer):
        quad(layer, T['flag'], P(mx + 0.08, top - 0.02, mz), P(mx + 1.15, top - 0.02, mz),
             P(mx + 0.08, top - 0.62, mz), uv=(0, 3, 16, 13))
    items.append((mx + mz + top, flag))
    return items


def render_scene():
    """The chunk on a transparent layer, cropped to what was drawn."""
    layer = Image.new('RGBA', (2 * N, 2 * N), (0, 0, 0, 0))
    O[0], O[1] = N, N
    for _, draw in sorted(scene(), key=lambda it: it[0]):
        draw(layer)
    return layer.crop(layer.getbbox())


# ----------------------------------------------------------------------------------------------- backdrop
def vgrad(w, h, stops):
    """Vertical gradient through (position 0..1, colour) stops."""
    col = Image.new('RGB', (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0)
                col.putpixel((0, y), tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(3)))
                break
    return col.resize((w, h)).convert('RGBA')


def glow(size, center, radius, color, strength):
    m = Image.new('L', size, 0)
    d = ImageDraw.Draw(m)
    steps = 40
    for i in range(steps, 0, -1):
        r = radius * i / steps
        d.ellipse([center[0] - r, center[1] - r, center[0] + r, center[1] + r],
                  fill=int(255 * strength * (1 - i / steps) ** 1.6))
    m = m.filter(ImageFilter.GaussianBlur(radius / 12))
    out = Image.new('RGBA', size, color + (0,))
    out.putalpha(m)
    return out


def sun(canvas, cx, cy, s):
    """Minecraft's square sun with a soft glow."""
    canvas.alpha_composite(glow(canvas.size, (cx, cy), s * 2.6, (255, 244, 196), 0.85))
    d = ImageDraw.Draw(canvas)
    d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], fill=(255, 236, 150))
    d.rectangle([cx - s * 0.36, cy - s * 0.36, cx + s * 0.36, cy + s * 0.36], fill=(255, 248, 206))


def cloud(canvas, x, y, cells, u):
    """A flat Minecraft cloud from a list of (column, row) cells of size u x 0.55 u, with a shaded underside."""
    lay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for cx, cy in cells:
        d.rectangle([x + cx * u, y + cy * u * 0.55, x + (cx + 1) * u - 1, y + (cy + 1) * u * 0.55 - 1],
                    fill=(255, 255, 255, 240))
    for cx, cy in cells:
        if (cx, cy + 1) not in cells:
            d.rectangle([x + cx * u, y + (cy + 1) * u * 0.55 - u / 7, x + (cx + 1) * u - 1, y + (cy + 1) * u * 0.55 - 1],
                        fill=(206, 228, 240, 240))
    canvas.alpha_composite(lay)


GULL = ["k.........k",          # k: black wing tip, g: grey wing, #: white body
        "gg.......gg",
        ".gg.....gg.",
        "..gg###gg..",
        "....###....",
        ".....#....."]
GULL_COL = {'k': (52, 56, 64), 'g': (178, 190, 200), '#': (255, 255, 255)}


def gull(canvas, x, y, px, flip=False):
    """A seagull in flight, as a small pixel sprite with a soft dark rim."""
    rows = [r[::-1] for r in GULL] if flip else GULL
    w, h = len(rows[0]), len(rows)
    sp = Image.new('RGBA', (w + 2, h + 2), (0, 0, 0, 0))
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch != '.':
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        sp.putpixel((i + 1 + di, j + 1 + dj), (44, 72, 100, 200))
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch != '.':
                sp.putpixel((i + 1, j + 1), GULL_COL[ch] + (255,))
    sp = sp.resize(((w + 2) * px, (h + 2) * px), Image.NEAREST)
    canvas.alpha_composite(sp, (int(x), int(y)))


# ----------------------------------------------------------------------------------------------- title
def title(canvas, text, cx, cy, size):
    f = ImageFont.truetype(TITLE_FONT, size)
    stroke = int(size * 0.1)
    # soft shadow
    m = Image.new('L', canvas.size, 0)
    ImageDraw.Draw(m).text((cx, cy + size * 0.07), text, font=f, anchor='mm', fill=255, stroke_width=stroke,
                           stroke_fill=255)
    m = m.filter(ImageFilter.GaussianBlur(size * 0.06))
    sh = Image.new('RGBA', canvas.size, NAVY + (0,))
    sh.putalpha(m.point(lambda v: int(v * 0.65)))
    canvas.alpha_composite(sh)
    # outline
    lay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((cx, cy), text, font=f, anchor='mm', fill=NAVY + (255,), stroke_width=stroke,
                             stroke_fill=NAVY + (255,))
    canvas.alpha_composite(lay)
    # fill: white at the top, warm sand at the foot of the letters
    gm = Image.new('L', canvas.size, 0)
    ImageDraw.Draw(gm).text((cx, cy), text, font=f, anchor='mm', fill=255)
    x0, y0, x1, y1 = gm.getbbox()
    g = vgrad(canvas.width, y1 - y0 + 2, [(0, (255, 255, 255)), (0.55, (255, 252, 240)), (1, (250, 222, 160))])
    fill = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    fill.paste(g, (0, y0))
    fill.putalpha(gm)
    canvas.alpha_composite(fill)


# ----------------------------------------------------------------------------------------------- compose
def backdrop():
    bg = vgrad(N, N, [(0, (64, 168, 226)), (0.55, (150, 222, 242)), (0.78, (72, 178, 214)), (1, (18, 96, 152))])
    sun(bg, 0.16 * N, 0.16 * N, 0.11 * N)
    u = 0.05 * N
    cloud(bg, 0.66 * N, 0.07 * N, [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (1, 0), (2, 0), (3, 0)], u)
    cloud(bg, 0.79 * N, 0.25 * N, [(0, 1), (1, 1), (2, 1), (1, 0)], u * 0.75)
    return bg


def compose(chunk, with_title=True):
    bg = backdrop()
    scale = (0.86 if with_title else 0.9) * N / max(chunk.size)
    ch = chunk.resize((int(chunk.width * scale), int(chunk.height * scale)), Image.LANCZOS)
    x = (N - ch.width) // 2
    y = int(0.035 * N) if with_title else (N - ch.height) // 2
    # a soft shadow under the floating chunk
    sh = Image.new('L', bg.size, 0)
    ImageDraw.Draw(sh).ellipse([x + ch.width * 0.2, y + ch.height * 0.93, x + ch.width * 0.8, y + ch.height * 1.02],
                               fill=110)
    sh = sh.filter(ImageFilter.GaussianBlur(0.025 * N))
    shadow = Image.new('RGBA', bg.size, (8, 50, 90, 0))
    shadow.putalpha(sh)
    bg.alpha_composite(shadow)
    bg.alpha_composite(ch, (x, y))
    gull(bg, 0.74 * N, 0.36 * N, int(0.0072 * N))
    gull(bg, 0.88 * N, 0.31 * N, int(0.0052 * N), flip=True)
    gull(bg, 0.07 * N, 0.36 * N, int(0.0048 * N))
    if with_title:
        title(bg, 'BEACH CRAFT', N / 2, 0.88 * N, int(0.15 * N))
    return bg.convert('RGB').resize((1024, 1024), Image.LANCZOS)


def preview(logo):
    """The logo at CurseForge's sizes (project page, search list, small) on a light and a dark page."""
    W, H = 1200, 316
    sheet = Image.new('RGB', (W, H), (246, 246, 248))
    ImageDraw.Draw(sheet).rectangle([W // 2, 0, W, H], fill=(28, 28, 32))
    for i, s in enumerate((256, 128, 64)):
        for half in (0, 1):
            im = logo.resize((s, s), Image.LANCZOS)
            m = Image.new('L', (s, s), 0)
            ImageDraw.Draw(m).rounded_rectangle([0, 0, s - 1, s - 1], radius=max(4, s // 12), fill=255)
            x = half * W // 2 + 30 + sum((256, 128, 64)[:i]) + 40 * i
            sheet.paste(im, (x, (H - s) // 2), m)
    return sheet


def main():
    os.makedirs(OUT, exist_ok=True)
    chunk = render_scene()
    logo = compose(chunk)
    logo.save(os.path.join(OUT, 'logo_1024.png'))
    for s in (512, 400, 256):
        logo.resize((s, s), Image.LANCZOS).save(os.path.join(OUT, 'logo_%d.png' % s))
    icon = compose(chunk, with_title=False)
    icon.save(os.path.join(OUT, 'icon_1024.png'))
    icon.resize((128, 128), Image.LANCZOS).save(os.path.join(OUT, 'icon_128.png'), optimize=True)
    preview(logo).save(os.path.join(OUT, 'preview.png'))
    print('written to', OUT)


main()
