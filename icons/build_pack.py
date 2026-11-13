#!/usr/bin/env python3
"""Builds the icon pack: the icons and logos of all projects on CurseForge and Modrinth.

    python3 build_pack.py            build pack/ and Kasax-Projekt-Icons.zip from the sources on disk
    python3 build_pack.py --fetch    first download the platform files again and check CurseForge for new icons

Sources
  * plattform-originale/   the files exactly as CurseForge and Modrinth serve them (table LIVE)
  * quellen/               originals that are in no repository (see quellen/QUELLEN.md)
  * beachcraft/logo/       in this archive
  * the mod repositories   next to this archive (REPOS, default: the parent folder), read as git objects by
                           their hash, so the checked-out branch does not matter

Rules
  * The largest version that exists is kept untouched (same bytes).
  * Smaller sizes are made from it with Lanczos. Nothing is scaled up, except real pixel art (nearest neighbour).
  * Images with transparency keep it; Pillow resizes them with premultiplied alpha, so edges get no fringe.
  * The pack is built in a fresh folder and swapped in at the end, so nothing stale can stay behind.
  * --fetch notices a new icon only on CurseForge (the Modrinth addresses contain the hash of the file).
"""
import datetime
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE = os.path.dirname(HERE)
REPOS = os.environ.get('REPOS', os.path.dirname(ARCHIVE))
PACK = os.path.join(HERE, 'pack')
WORK = os.path.join(HERE, '.pack_build')
ORIG = os.path.join(HERE, 'plattform-originale')
QUELLEN = os.path.join(HERE, 'quellen')
NAME = 'Kasax-Projekt-Icons'
TODAY = datetime.date.today()
STAND = TODAY.strftime('%d.%m.%Y')
SIZES = [1024, 512, 400, 256, 128, 64]
UNIFORM = (400, 256)
UA = 'icon-pack-builder/1.0'
MAGIC = {'.png': b'\x89PNG\r\n\x1a\n', '.jpg': b'\xff\xd8\xff', '.webp': b'RIFF'}

# Where the platforms serve the icons. CurseForge: media.forgecdn.net/avatars/<path> (original) and
# .../avatars/thumbnails/<a>/<b>/256/256/<file> (thumbnail). Modrinth: cdn.modrinth.com/data/<id>/<sha1>.png and
# ..._96.webp. A new icon gets a new path; --fetch compares the CurseForge paths with api.cfwidget.com.
LIVE = {
    'dreamcraft': dict(cf='578/913/637943586710882910.png', mr=('jRXfjUwW', 'b554ba8eb87417663bc7cec4cdace54d8b6d331f')),
    'beach-craft': dict(cf='2184/685/639296932728613749.png', mr=('3PmzwJU0', '9a933184e90419101663414a239f56d5f01056f9')),
    'quest-icons': dict(cf='675/770/638066120936047746.png', mr=('ohf5LwXu', 'f8f1f55efe68d4124ed4052a3af472583772318b')),
    'tamacraft': dict(cf='2137/963/639282088201946200.png', mr=('lyuVXQEh', '1303288ca812c6b06c5de549cb80bfe629145a28')),
    'challenge-craft': dict(cf='1915/887/639194707807914830.png', mr=('3qs3GQyx', '05c21a3e23604a0ac2f7437c44c8c12e40e8c221')),
    'challenge-craft-modpack': dict(cf='1985/635/639223989696353052.png', mr=('XVYCqsNs', '37ccecfb49e1ad14882a8fc511d311675731b3d3')),
    'dreamcraft-forge': dict(cf='596/196/637971947191207526.png'),
    'lightspeed-performance': dict(cf='462/790/637742313661806565.png'),
    'beautifully': dict(cf='462/774/637742284980164703.png'),
}


def cf_orig(key):
    return os.path.join(ORIG, 'curseforge', f'{key}_curseforge_original.png')


def blob(repo, sha):
    """A file from a repository by the hash of its git object."""
    return ('git', os.path.join(REPOS, repo), sha)


def quelle(name):
    return os.path.join(QUELLEN, name)


BC_LOGO = os.path.join(ARCHIVE, 'beachcraft', 'logo')
CC_LOGO = quelle('challenge-craft_logo_3240.png')
CC_SOURCE = ('Menü des Modpacks (`config/fancymenu/assets/final.png` in Challenge Craft 26.3 v4.2), gesichert im '
             'Archiv unter `icons/quellen`')
DC_LOGO = blob('Kasax_Quests_Items_Mod-1.19.2', 'd579c973c575b62a2ba2d7d3d84649873581124d')   # textures/item/logo_fabric.png
DC_LOADING = blob('Modpack-Development', '38206e145769f6375676795bf6f8c259a66211d2')          # .../dreamcraft/loading_logo.png
DC_SERVER = blob('Modpack-Development', '8d970902a0c4a7b18e4f9e6840fb13d166ba7e64')           # pack/server-icon.png
QI_MOD = blob('Kasax_Quests_Items_Mod-1.19.2', '7ad8d701802a1f718f7ba7c7b492bf01c5d8dbe0')    # assets/questsicons/icon.png
TC_MOD = blob('tamagotchi', '036efb2a3cc6bbb8ea2496c728ff5b5f2c6cf860')                       # assets/tamacraft/icon.png
CC_MOD = blob('Kasax_Challenge_Craft', 'e26376f134084c1104b71346e7acac672c533883')            # assets/challengecraft/icon.png

# One entry per project.
# sets: files <key>_<tag>_<size>.png. master = the largest version; fixed = sizes that exist as their own file;
#       pixel = pixel art with that many points per side (nearest neighbour, may grow); top = largest size to
#       ship when the original itself lives in another folder.
# extras: files in extras/ ({w}x{h} in the name is filled in). make: 'trim' cuts the empty border away,
#       ('pixel', n) enlarges pixel art n times. show: the label under the small picture on the overview sheet.
# on_sheet / in_table: a remark for the overview sheet and for the table in the readme.
PROJECTS = [
    dict(nr='01', key='dreamcraft', name='Dreamcraft - Quests & Adventure', kind='Modpack (Fabric)', cf_id=545167,
         cf_url='https://www.curseforge.com/minecraft/modpacks/dreamcraft-new', mr_url='https://modrinth.com/modpack/dreamcraft',
         sets=[dict(tag='icon', label='Projekt-Icon', master=cf_orig('dreamcraft'),
                    source='CurseForge (dieselbe Datei liegt auf Modrinth)')],
         extras=[dict(file='dreamcraft_logo_1440x1080.png', src=DC_LOGO,
                      note='Logo „DREAMCRAFT FABRIC“ mit Mond und Sternen, durchsichtiger Grund'),
                 dict(file='dreamcraft_logo_zugeschnitten_{w}x{h}.png', src=DC_LOGO, make='trim', show='Logo',
                      note='dasselbe Logo ohne den leeren Rand'),
                 dict(file='dreamcraft_schriftzug_1440x1080.png', src=DC_LOADING,
                      note='Schriftzug „DREAMCRAFT FABRIC“ vom Ladebildschirm, ohne Mond und Sterne'),
                 dict(file='dreamcraft_schriftzug_zugeschnitten_{w}x{h}.png', src=DC_LOADING, make='trim', show='Schriftzug',
                      note='derselbe Schriftzug ohne den leeren Rand'),
                 dict(file='dreamcraft_server-icon_64.png', src=DC_SERVER, show='Server-Icon',
                      note='Icon in der Serverliste (aus dem Server-Pack)'),
                 dict(file='dreamcraft_fenster-icon_32.png', src=quelle('dreamcraft_fenster-icon_32.png'),
                      show='Fenster-Icon', show_px='32 px (auch 16, 256)',
                      note='Icon des Spielfensters (Mond mit Sternen), aus dem Pack für 1.20.1; die kleinen Sterne '
                           'sind durchsichtige Punkte'),
                 dict(file='dreamcraft_fenster-icon_16.png', src=quelle('dreamcraft_fenster-icon_16.png'),
                      note='dasselbe in 16 px, aus dem Pack für 1.20.1'),
                 dict(file='dreamcraft_fenster-icon_256.png', src=quelle('dreamcraft_fenster-icon_32.png'), make=('pixel', 8),
                      note='das Fenster-Icon achtfach vergrößert (Pixel-Art, verlustfrei)')]),
    dict(nr='02', key='beach-craft', name='Beach Craft – Raft Survival', kind='Mod', cf_id=1010922,
         cf_url='https://www.curseforge.com/minecraft/mc-mods/beach-craft', mr_url='https://modrinth.com/mod/beach-craft',
         sets=[dict(tag='icon', label='Projekt-Icon (mit Titel)', master=os.path.join(BC_LOGO, 'logo_1024.png'),
                    fixed={512: os.path.join(BC_LOGO, 'logo_512.png'), 400: os.path.join(BC_LOGO, 'logo_400.png'),
                           256: os.path.join(BC_LOGO, 'logo_256.png')},
                    source='Archiv `beachcraft/logo` (die 1024er liegt auf Modrinth, eine 400er auf CurseForge)'),
               dict(tag='icon-ohne-titel', label='Icon ohne Titel', master=os.path.join(BC_LOGO, 'icon_1024.png'),
                    fixed={128: os.path.join(BC_LOGO, 'icon_128.png')},
                    source='Archiv `beachcraft/logo`; die 128er ist das Mod-Icon in der Jar (seit 3.2.0)')],
         extras=[dict(file='beach-craft_altes-mod-icon_1024.jpg', src=quelle('beach-craft_altes-mod-icon_1024.jpg'),
                      show='altes Mod-Icon',
                      note='altes Mod-Icon (Floß zwischen Inseln), in der Jar bis Version 3.1; ein JPEG, so lag es in der Jar')]),
    dict(nr='03', key='quest-icons', name='Quest Icons - Quest Book & Icons', kind='Mod', cf_id=690531,
         cf_url='https://www.curseforge.com/minecraft/mc-mods/quest-icons', mr_url='https://modrinth.com/mod/quest-icons',
         sets=[dict(tag='icon', label='Projekt-Icon', master=cf_orig('quest-icons'), source='CurseForge'),
               dict(tag='mod-icon', label='Mod-Icon (im Spiel)', pixel=16, sizes=[512, 256, 128, 64, 16], master=QI_MOD,
                    source='Jar (`assets/questsicons/icon.png`); Pixel-Art mit 16×16 Punkten')]),
    dict(nr='04', key='tamacraft', name='Tamacraft – Rare Pets', kind='Mod', cf_id=1758309,
         cf_url='https://www.curseforge.com/minecraft/mc-mods/tamacraft', mr_url='https://modrinth.com/mod/tamacraft',
         on_sheet='neu gezeichnet, schärfer als online',
         sets=[dict(tag='icon', label='Projekt-Icon', master=quelle('tamacraft_icon_render_1024.png'),
                    master_how='neu gezeichnet',
                    source='neu gezeichnet mit `icons/render_tamacraft.py` im Archiv; das Skript nutzt den Zeichen-Code '
                           'des Mods (`tools/petart`) und die Maße aus `icon.py`'),
               dict(tag='mod-icon', label='Mod-Icon (im Spiel)', master=TC_MOD, source='Jar (`assets/tamacraft/icon.png`)')],
         extras=[dict(file='tamacraft_icon_curseforge_400.png', src=cf_orig('tamacraft'), show='Fassung von CurseForge',
                      note='das Icon, wie es auf CurseForge liegt: weich, weil es eine Vergrößerung des Mod-Icons (128 px) ist')]),
    dict(nr='05', key='challenge-craft', name='Challenge Craft – Challenge Runs & Lockout Bingo', kind='Mod (Fabric)',
         cf_id=1508454, cf_url='https://www.curseforge.com/minecraft/mc-mods/challenge',
         mr_url='https://modrinth.com/mod/challenge_craft',
         sets=[dict(tag='icon', label='Projekt-Icon', master=CC_LOGO, source=CC_SOURCE),
               dict(tag='mod-icon', label='Mod-Icon (im Spiel)', master=CC_MOD, source='Jar (`assets/challengecraft/icon.png`)')],
         extras=[dict(file='challenge-craft_schriftzug_2040x427.png', src=quelle('challenge-craft_schriftzug_2040x427.png'),
                      show='Schriftzug', note='Schriftzug „CHALLENGE CRAFT“ aus dem Menü des Modpacks, durchsichtiger Grund; '
                                               'ohne Rand, beim Einsetzen etwas Abstand lassen'),
                 dict(file='challenge-craft_by-kasax_2048x298.png', src=quelle('challenge-craft_by-kasax_2048x298.png'),
                      show='„By Kasax“', note='Schriftzug „BY KASAX“ aus dem Menü des Modpacks, durchsichtiger Grund; ohne Rand')]),
    dict(nr='06', key='challenge-craft-modpack', name='Challenge Craft Modpack', kind='Modpack (Fabric)', cf_id=1653698,
         cf_url='https://www.curseforge.com/minecraft/modpacks/challenge-craft',
         mr_url='https://modrinth.com/modpack/challenge-craft-modpack',
         on_sheet='gleiches Bild wie 05, Original dort', in_table='gleiches Bild wie 05 (Original mit 3240 px dort)',
         sets=[dict(tag='icon', label='Projekt-Icon', master=CC_LOGO, top=1024,
                    source='dasselbe Bild wie beim Mod Challenge Craft; das Original mit 3240 px und die Schriftzüge '
                           'liegen im Ordner 05')]),
    dict(nr='07', key='dreamcraft-forge', name='Dreamcraft [FORGE]', kind='Modpack (Forge, 2022)', cf_id=582205,
         cf_url='https://www.curseforge.com/minecraft/modpacks/dreamcraft-forge',
         on_sheet='gleiches Bild wie 01', in_table='gleiches Bild wie 01',
         sets=[dict(tag='icon', label='Projekt-Icon', master=cf_orig('dreamcraft-forge'),
                    source='CurseForge; dasselbe Bild wie bei Dreamcraft (Ordner 01)')],
         extras=[dict(file='dreamcraft-forge_schriftzug_1440x1080.png', src=quelle('dreamcraft-forge_schriftzug_1440x1080.png'),
                      note='Schriftzug „DREAMCRAFT FORGE“ vom Ladebildschirm des Forge-Packs, durchsichtiger Grund'),
                 dict(file='dreamcraft-forge_schriftzug_zugeschnitten_{w}x{h}.png', src=quelle('dreamcraft-forge_schriftzug_1440x1080.png'),
                      make='trim', show='Schriftzug', note='derselbe Schriftzug ohne den leeren Rand')]),
    dict(nr='08', key='lightspeed-performance', name='Lightspeed Performance', kind='Modpack (2021)', cf_id=552356,
         cf_url='https://www.curseforge.com/minecraft/modpacks/lightspeed-performance',
         sets=[dict(tag='icon', label='Projekt-Icon', master=cf_orig('lightspeed-performance'), source='CurseForge')]),
    dict(nr='09', key='beautifully', name='Beautifully [NEW]', kind='Modpack (2021)', cf_id=552343,
         cf_url='https://www.curseforge.com/minecraft/modpacks/beautifully-new',
         sets=[dict(tag='icon', label='Projekt-Icon', master=cf_orig('beautifully'), source='CurseForge')]),
]


# ---------------------------------------------------------------- reading and writing

def read(src):
    if isinstance(src, tuple):
        return subprocess.run(['git', '-C', src[1], 'cat-file', 'blob', src[2]], check=True, capture_output=True).stdout
    with open(src, 'rb') as f:
        return f.read()


def write(path, data):
    """Writes a file and refuses content that does not fit the name (a JPEG called .png, for example)."""
    magic = MAGIC.get(os.path.splitext(path)[1])
    assert magic is None or data.startswith(magic), f'{path}: content does not fit the extension'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)


def png(im):
    out = io.BytesIO()
    im.save(out, 'PNG', optimize=True)
    return out.getvalue()


def load(data):
    im = Image.open(io.BytesIO(data))
    im.load()
    if im.mode == 'P':
        im = im.convert('RGBA' if 'transparency' in im.info else 'RGB')
    return im


def opaque(im):
    """True when nothing of the image is see-through (CurseForge stores some opaque icons with alpha 250-255)."""
    return im.mode not in ('RGBA', 'LA') or im.convert('RGBA').getchannel('A').getextrema()[0] >= 250


def scaled(im, size, pixel=False):
    if pixel:
        return im.resize((size, size), Image.NEAREST)
    return im.convert('RGB' if opaque(im) else 'RGBA').resize((size, size), Image.LANCZOS)


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def fetch():
    """Downloads the platform files again; a file is only replaced by something that opens as an image."""
    for p in PROJECTS:
        live = LIVE[p['key']]
        a, b, name = live['cf'].split('/')
        thumb = f'https://media.forgecdn.net/avatars/thumbnails/{a}/{b}/256/256/{name}'
        try:
            now = json.loads(get(f'https://api.cfwidget.com/{p["cf_id"]}')).get('thumbnail')
            if now != thumb:
                print(f'WARNING {p["key"]}: CurseForge now shows another icon ({now}); update LIVE')
        except Exception as e:  # the check is a convenience, the download below does not depend on it
            print(f'could not ask api.cfwidget.com about {p["key"]}: {e}')
        jobs = [(f'https://media.forgecdn.net/avatars/{live["cf"]}', cf_orig(p['key'])),
                (thumb, os.path.join(ORIG, 'curseforge', f'{p["key"]}_curseforge_256.png'))]
        if 'mr' in live:
            pid, sha = live['mr']
            jobs += [(f'https://cdn.modrinth.com/data/{pid}/{sha}.png', os.path.join(ORIG, 'modrinth', f'{p["key"]}_modrinth_original.png')),
                     (f'https://cdn.modrinth.com/data/{pid}/{sha}_96.webp', os.path.join(ORIG, 'modrinth', f'{p["key"]}_modrinth_vorschau.webp'))]
        for url, out in jobs:
            data = get(url)
            Image.open(io.BytesIO(data)).verify()
            write(out, data)
            print('fetched', os.path.relpath(out, HERE))


# ---------------------------------------------------------------- the pack

def row(p, kind, rel, how, data, **more):
    im = load(data)
    return dict(project=p['key'], set=kind, file=rel, width=im.size[0], height=im.size[1], how=how,
                sha1=hashlib.sha1(data).hexdigest(), **more)


def build_sets(rows):
    for p in PROJECTS:
        folder = f'{p["nr"]}_{p["key"]}'
        for s in p['sets']:
            data = read(s['master'])
            master = load(data)
            assert master.format == 'PNG' and master.size[0] == master.size[1], (p['key'], s['tag'], master.format, master.size)
            native = master.size[0]
            sizes = s.get('sizes') or [n for n in SIZES if n < native]
            if s.get('top'):  # the original itself is shipped in another folder
                sizes = [n for n in sizes if n <= s['top']]
            else:
                sizes = sorted(set(sizes) | {native})
            s['native'] = max(sizes)
            grid = None
            if s.get('pixel'):
                grid = master.resize((s['pixel'], s['pixel']), Image.NEAREST)
                assert grid.resize(master.size, Image.NEAREST).tobytes() == master.tobytes(), 'not pixel art'
            for size in sorted(sizes, reverse=True):
                rel = f'{folder}/{p["key"]}_{s["tag"]}_{size}.png'
                if size == native:
                    out, how = data, s.get('master_how', 'Original')
                elif grid is not None:
                    assert size % s['pixel'] == 0
                    out = png(scaled(grid, size, pixel=True))
                    how = 'Pixel-Art, verlustfrei vergrößert' if size > native else 'Pixel-Art, verlustfrei verkleinert'
                else:
                    assert size < native, (rel, 'would be scaled up')
                    mine = scaled(master, size)
                    out, how = png(mine), 'verkleinert'
                    if size in s.get('fixed', {}):  # a file of its own: use it, and say so only if it really differs
                        out = read(s['fixed'][size])
                        own = load(out)
                        assert own.size == (size, size), (rel, own.size)
                        if own.convert(mine.mode).tobytes() != mine.tobytes():
                            how = 'eigene Fassung'
                write(os.path.join(WORK, rel), out)
                rows.append(row(p, s['tag'], rel, how, out))
        for e in p.get('extras', []):
            data = read(e['src'])
            make = e.get('make')
            if make == 'trim':
                im = load(data).convert('RGBA')
                box = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
                pad = 16
                data = png(im.crop((max(0, box[0] - pad), max(0, box[1] - pad),
                                    min(im.size[0], box[2] + pad), min(im.size[1], box[3] + pad))))
            elif make:
                im = load(data)
                data = png(im.resize((im.size[0] * make[1], im.size[1] * make[1]), Image.NEAREST))
            size = load(data).size
            e['name'] = e['file'].format(w=size[0], h=size[1])
            rel = f'{folder}/extras/{e["name"]}'
            write(os.path.join(WORK, rel), data)
            rows.append(row(p, 'extras', rel, e['note'], data))


def build_uniform(rows):
    """One folder per size with the icon of every project, for grids and lists."""
    for size in UNIFORM:
        for p in PROJECTS:
            data = read(os.path.join(WORK, f'{p["nr"]}_{p["key"]}', f'{p["key"]}_icon_{size}.png'))
            rel = f'alle-icons_{size}px/{p["nr"]}_{p["key"]}.png'
            write(os.path.join(WORK, rel), data)
            rows.append(row(p, 'alle', rel, f'Kopie von {p["key"]}_icon_{size}.png', data))


def font(name, size):
    return ImageFont.truetype(os.path.join(ARCHIVE, 'fonts', name), size)


def tile(path, w, h):
    """An image fitted into a box, keeping its shape; transparent parts show the card behind it."""
    im = load(read(path)).convert('RGBA')
    k = min(w / im.size[0], h / im.size[1])
    new = (max(1, round(im.size[0] * k)), max(1, round(im.size[1] * k)))
    return im.resize(new, Image.NEAREST if max(im.size) <= 128 and k >= 1 else Image.LANCZOS)


def build_overview():
    bg, card, line, text, muted, accent = (18, 19, 28), (30, 32, 46), (52, 55, 78), (240, 241, 248), (160, 165, 190), (150, 200, 255)
    cols, cw, ch, gap, margin, top = 3, 620, 372, 24, 40, 150
    rows_n = (len(PROJECTS) + cols - 1) // cols
    W = margin * 2 + cols * cw + (cols - 1) * gap
    H = top + rows_n * ch + (rows_n - 1) * gap + margin
    im = Image.new('RGBA', (W, H), bg + (255,))
    d = ImageDraw.Draw(im)
    f_sub = font('Inter-SemiBold.otf', 18)
    d.text((margin, 30), 'Kasax007 – Projekt-Icons', font=font('InterDisplay-Bold.otf', 44), fill=text)
    assert len(PROJECTS) == 9 and sum(1 for p in PROJECTS if p.get('mr_url')) == 6, 'the texts name nine and six'
    d.text((margin, 88), f'Stand {STAND} · Neun Projekte auf CurseForge, sechs davon auch auf Modrinth · '
                         '„Icon bis 800 px“ = größte vorhandene Größe', font=f_sub, fill=muted)
    d.text((margin, 114), 'Alle neun Icons in einer Größe: Ordner alle-icons_256px und alle-icons_400px', font=f_sub, fill=muted)
    f_name, f_kind, f_small = font('InterDisplay-Bold.otf', 23), font('Inter-SemiBold.otf', 16), font('Inter-SemiBold.otf', 13)
    for i, p in enumerate(PROJECTS):
        x = margin + (i % cols) * (cw + gap)
        y = top + (i // cols) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], 18, fill=card, outline=line)
        folder = os.path.join(WORK, f'{p["nr"]}_{p["key"]}')
        native = p['sets'][0]['native']
        big = tile(os.path.join(folder, f'{p["key"]}_icon_{min(native, 1024)}.png'), 232, 232)
        im.alpha_composite(big, (x + 20, y + 20))
        tx = x + 274
        lines_, cur = [], ''
        for w in p['name'].split():
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=f_name) <= cw - 274 - 18 or not cur:
                cur = t
            else:
                lines_.append(cur)
                cur = w
        lines_.append(cur)
        ty = y + 22
        for ln in lines_[:3]:
            d.text((tx, ty), ln, font=f_name, fill=text)
            ty += 30
        d.text((tx, ty + 4), p['kind'], font=f_kind, fill=muted)
        ty += 30
        d.text((tx, ty), 'CurseForge + Modrinth' if p.get('mr_url') else 'CurseForge', font=f_kind, fill=accent)
        ty += 28
        for ln in [f'Ordner {p["nr"]}_{p["key"]}', f'Icon bis {native} px'] + ([p['on_sheet']] if p.get('on_sheet') else []):
            d.text((tx, ty), ln, font=f_small, fill=muted)
            ty += 20
        # the other pictures of the project, each with its name and size underneath
        small = []
        for s in p['sets'][1:]:
            jar = load(read(s['master'])).size[0]
            px = f'{jar} px (auch {min(s["sizes"])} bis {max(s["sizes"])})' if s.get('pixel') else f'{jar} px'
            small.append((os.path.join(folder, f'{p["key"]}_{s["tag"]}_{jar}.png'), s['label'].split(' (')[0], px))
        for e in p.get('extras', []):
            if e.get('show'):
                path = os.path.join(folder, 'extras', e['name'])
                sz = Image.open(path).size
                small.append((path, e['show'], e.get('show_px') or (f'{sz[0]} px' if sz[0] == sz[1] else f'{sz[0]}×{sz[1]}')))
        sx = x + 20
        for path, label, px in small:
            t = tile(path, 176, 56)
            wide = max(t.size[0], int(d.textlength(label, font=f_small)), int(d.textlength(px, font=f_small)))
            im.alpha_composite(t, (sx, y + 266 + (56 - t.size[1]) // 2))
            d.text((sx, y + 328), label, font=f_small, fill=text)
            d.text((sx, y + 346), px, font=f_small, fill=muted)
            sx += wide + 18
            assert sx <= x + cw, f'{p["key"]}: the small pictures do not fit on the card'
        if not small:
            d.text((x + 20, y + 300), 'nur das Projekt-Icon', font=f_small, fill=muted)
    write(os.path.join(WORK, 'uebersicht.png'), png(im.convert('RGB')))


def build_readme(rows):
    def sizes_of(p, tag):
        return sorted((r['width'] for r in rows if r['project'] == p['key'] and r['set'] == tag), reverse=True)

    L = ['# Icons meiner Projekte (Kasax007)', '',
         f'Stand: {STAND}. Neun Projekte auf CurseForge, sechs davon auch auf Modrinth. Alle Bilder auf einen Blick: '
         '`uebersicht.png`.', '',
         '## Welche Datei nehme ich?', '',
         '- **Website, Projektseite (CurseForge, Modrinth), Endkarte im Video:** die Datei `_icon_` mit der höchsten Zahl '
         'im Namen, höchstens aber `_1024`. Die 3240er von Challenge Craft (8,5 MB) ist nur für Druck oder starke '
         'Vergrößerung gedacht.',
         '- **Discord-Server oder Profilbild:** `_512`; bei Lightspeed Performance und Beautifully `_400`.',
         '- **Liste oder Raster mit allen Projekten:** Ordner `alle-icons_256px` (oder `alle-icons_400px`).',
         '- **Auf farbigem Grund:** Tamacraft hat durchsichtige Ecken und einen schmalen durchsichtigen Rand; alle anderen '
         'Projekt-Icons sind volle Quadrate. Logos und Schriftzüge in `extras/` haben einen durchsichtigen Grund und '
         'wirken am besten auf Dunkel.', '',
         '## Inhalt', '',
         '| Ordner | Projekt | Art | Icon-Größen (px) | Außerdem |', '| --- | --- | --- | --- | --- |']
    for p in PROJECTS:
        more = [s['label'].split(' (')[0] for s in p['sets'][1:]] + [e['show'] for e in p.get('extras', []) if e.get('show')]
        if p.get('in_table'):
            more.insert(0, p['in_table'])
        L.append(f'| `{p["nr"]}_{p["key"]}` | {p["name"]} | {p["kind"]} | {", ".join(map(str, sizes_of(p, "icon")))} | '
                 f'{", ".join(more) or "–"} |')
    L += ['',
          'Dazu `alle-icons_400px` und `alle-icons_256px`: alle neun Projekt-Icons in einer Größe, benannt '
          '`NN_<projekt>.png`.', '',
          '## Dateinamen', '',
          '- `<projekt>_icon_<größe>.png`: das Projekt-Icon. Die Zahl ist die Kantenlänge in Pixeln; alle Icons sind quadratisch.',
          '- `<projekt>_icon-ohne-titel_<größe>.png`: das Beach-Craft-Icon ohne den Titel.',
          '- `<projekt>_mod-icon_<größe>.png`: das Icon, das im Spiel in der Mod-Liste steht (es steckt in der Jar).',
          '- `extras/`: Logos, Schriftzüge, Server- und Fenster-Icon, ältere Fassungen.', '',
          '## So sind die Größen entstanden', '',
          '- Bei jedem Projekt-Icon ist die Datei mit der höchsten Zahl das unveränderte Original (Byte für Byte). '
          'Ausnahmen: Bei Tamacraft ist es eine neu gezeichnete Fassung, und das Original des Challenge Craft Modpacks '
          'liegt im Ordner 05 (siehe unten).',
          '- Kleinere Größen sind daraus verkleinert. Vergrößert wurde nur Pixel-Art, denn das geht ohne Verlust: beim '
          'Mod-Icon von Quest Icons und beim Fenster-Icon von Dreamcraft. Deshalb hört die Liste bei manchen Projekten '
          'schon bei 400 px auf.', '',
          '## Gut zu wissen', '',
          '- **Challenge Craft:** Das Original mit 3240 px stammt aus dem Menü des Modpacks. Mod und Modpack haben dasselbe '
          'Icon; im Ordner 06 liegt es bis 1024 px. Das Mod-Icon im Spiel ist dagegen ein weißes Feld mit dem Text '
          '„Challenge Craft“. Auf Modrinth hat das Modpack bisher nur eine Fassung mit 64 px; '
          '`challenge-craft-modpack_icon_512.png` wäre dort die bessere Wahl.',
          '- **Tamacraft:** Auf CurseForge liegt eine weiche Fassung mit 400 px; sie ist eine Vergrößerung des kleinen '
          'Mod-Icons (128 px). Das Icon in diesem Pack ist neu gezeichnet, mit dem Zeichen-Code des Mods und denselben '
          'Maßen wie das Mod-Icon, nur größer gerechnet: dasselbe Bild, aber scharf und bis 1024 px. Diese Fassung ist '
          'noch nirgends hochgeladen; wenn du sie online haben willst, lade `tamacraft_icon_1024.png` auf CurseForge und '
          'Modrinth hoch. Die bisherige Fassung liegt in `extras/`.',
          '- **Dreamcraft:** Fabric und Forge haben dasselbe Icon. In `extras/` liegen das Logo „DREAMCRAFT FABRIC“ mit '
          'Mond und Sternen, der Schriftzug ohne beides, das Server-Icon und das Fenster-Icon aus dem Pack für 1.20.1. '
          'Das Fenster-Icon nur auf dunklem Grund verwenden: Die kleinen Sterne sind durchsichtige Punkte und erscheinen '
          'auf Hell als helle Flecken (so ist schon das Original). Der Schriftzug „DREAMCRAFT FORGE“ liegt im Ordner 07.',
          '- **Beach Craft:** Das Mod-Icon in der Jar ist `beach-craft_icon-ohne-titel_128.png` (seit 3.2.0). Bis Version '
          '3.1 war es das Bild in `extras/`.',
          '- **Lightspeed Performance, Beautifully:** Von diesen Icons gibt es nur die 400 px von CurseForge. Im Ordner '
          '`alle-icons_400px` wirken sie etwas weicher als die anderen; für ein Raster ist `alle-icons_256px` am '
          'gleichmäßigsten.', '',
          '## Die Projekte im Einzelnen', '']
    for p in PROJECTS:
        links = f'[CurseForge]({p["cf_url"]}) (Projekt-Nr. {p["cf_id"]})' + (f' · [Modrinth]({p["mr_url"]})' if p.get('mr_url') else '')
        L += [f'### {p["nr"]} · {p["name"]}', '', f'{p["kind"]} · {links}', '']
        for s in p['sets']:
            parts = []
            for r in [r for r in rows if r['project'] == p['key'] and r['set'] == s['tag']]:
                mark = {'Original': 'Datei aus der Jar' if s.get('pixel') else 'Original', 'neu gezeichnet': 'neu gezeichnet',
                        'eigene Fassung': 'eigene Fassung'}.get(r['how'], '')
                parts.append(f'{r["width"]}' + (f' ({mark})' if mark else ''))
            tail = ' Die anderen Größen sind verlustfreie Pixel-Art-Fassungen.' if s.get('pixel') else ''
            L.append(f'- **{s["label"]}:** {", ".join(parts)} px. Quelle: {s["source"]}.{tail}')
        for r in [r for r in rows if r['project'] == p['key'] and r['set'] == 'extras']:
            L.append(f'- `extras/{os.path.basename(r["file"])}` ({r["width"]}×{r["height"]}): {r["how"]}.')
        L.append('')
    write(os.path.join(WORK, 'LIESMICH.md'), '\n'.join(L).encode('utf-8'))


def build_zip(files):
    """Writes the ZIP next to its final place and moves it there only when it is complete."""
    out = os.path.join(HERE, f'{NAME}.zip')
    stamp = (TODAY.year, TODAY.month, TODAY.day, 12, 0, 0)
    with zipfile.ZipFile(out + '.neu', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for rel in sorted(files):
            info = zipfile.ZipInfo(f'{NAME}/{rel}', stamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, read(os.path.join(PACK, rel)))
    os.replace(out + '.neu', out)
    return out


def main():
    if '--fetch' in sys.argv:
        fetch()
    # everything the build reads must be there before anything is replaced
    needed = [cf_orig(k) for k in LIVE]
    for p in PROJECTS:
        needed += [s['master'] for s in p['sets']] + [f for s in p['sets'] for f in s.get('fixed', {}).values()]
        needed += [e['src'] for e in p.get('extras', [])]
    for src in needed:
        try:
            read(src)
        except Exception as e:
            sys.exit(f'source missing: {src} ({e})')
    shutil.rmtree(WORK, ignore_errors=True)
    rows = []
    build_sets(rows)
    build_uniform(rows)
    build_overview()
    build_readme(rows)
    files = [r['file'] for r in rows] + ['LIESMICH.md', 'uebersicht.png']
    on_disk = sorted(os.path.relpath(os.path.join(root, n), WORK).replace(os.sep, '/')
                     for root, _, names in os.walk(WORK) for n in names)
    assert on_disk == sorted(files), 'the build folder holds other files than the list'
    # swap: the old pack steps aside, the new one moves in, then the old one goes
    old = PACK + '.alt'
    shutil.rmtree(old, ignore_errors=True)
    if os.path.exists(PACK):
        os.rename(PACK, old)
    os.rename(WORK, PACK)
    shutil.rmtree(old, ignore_errors=True)
    manifest = os.path.join(HERE, 'manifest.json')
    write(manifest + '.neu', json.dumps(rows, ensure_ascii=False, indent=1).encode('utf-8'))
    os.replace(manifest + '.neu', manifest)
    out = build_zip(files)
    print(f'{len(files)} files, {os.path.getsize(out) / 1e6:.1f} MB: {out}')


if __name__ == '__main__':
    main()
