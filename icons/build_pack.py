#!/usr/bin/env python3
"""Builds the icon pack: the icons and logos of all projects on CurseForge and Modrinth.

    python3 build_pack.py            build pack/ and Kasax-Projekt-Icons.zip from the sources on disk
    python3 build_pack.py --fetch    download the platform originals again first (CurseForge, Modrinth)

Sources
  * pack/plattform-originale/   the files exactly as CurseForge and Modrinth serve them (table LIVE)
  * beachcraft/logo/            in this archive
  * the mod repositories        next to this archive (REPOS, default: the parent folder), read through git

Rules
  * The largest version that exists is kept untouched (same bytes).
  * Smaller sizes are made from it with Lanczos. Nothing is scaled up, except real pixel art (nearest neighbour).
  * Images with transparency keep it; Pillow resizes them with premultiplied alpha, so edges get no dark fringe.
"""
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
ORIG = os.path.join(PACK, 'plattform-originale')
NAME = 'Kasax-Projekt-Icons'
STAND = '13.11.2026'
SIZES = [1024, 512, 400, 256, 128, 64]
UA = 'icon-pack-builder/1.0'

# Where the platforms serve the icons. CurseForge: media.forgecdn.net/avatars/<path> (original) and
# .../avatars/thumbnails/<a>/<b>/256/256/<file> (thumbnail). Modrinth: cdn.modrinth.com/data/<id>/<sha1>.png and
# ..._96.webp. A new icon gets a new path, so this table has to be updated when an icon changes.
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


def git(repo, spec):
    """A file from a repository: 'HEAD:path' or a blob hash, so the result does not depend on the checkout."""
    return ('git', os.path.join(REPOS, repo), spec)


BC_LOGO = os.path.join(ARCHIVE, 'beachcraft', 'logo')
CC_LOGO = git('Kasax_Challenge_Craft', 'HEAD:docs/curseforge/src/pack_logo.jpg')
DC_MENU = 'HEAD:pack/overrides/config/fancymenu/assets/dreamcraft/loading_logo.png'

# One entry per project. sets: tag -> files <key>_<tag>_<size>.png. master = the largest version that exists;
# fixed = sizes that exist as their own file (used as they are); pixel = pixel art (nearest neighbour, may grow).
PROJECTS = [
    dict(nr='01', key='dreamcraft', name='Dreamcraft – Quests & Adventure', kind='Modpack (Fabric)', cf_id=545167,
         cf_url='https://www.curseforge.com/minecraft/modpacks/dreamcraft-new', mr_url='https://modrinth.com/modpack/dreamcraft',
         sets=[dict(tag='icon', label='Projekt-Icon', master=cf_orig('dreamcraft'),
                    source='CurseForge (dieselbe Datei liegt auf Modrinth)')],
         extras=[dict(file='dreamcraft_server-icon_64.png', src=git('Modpack-Development', 'HEAD:pack/server-icon.png'),
                      label='Server-Icon', note='Symbol in der Serverliste (aus dem Server-Pack)'),
                 dict(file='dreamcraft_schriftzug_1440x1080.png', src=git('Modpack-Development', DC_MENU),
                      label='Schriftzug', note='Schriftzug vom Ladebildschirm, mit durchsichtigem Rand'),
                 dict(file='dreamcraft_schriftzug_zugeschnitten.png', src=git('Modpack-Development', DC_MENU), trim=True,
                      label='Schriftzug, zugeschnitten', note='derselbe Schriftzug ohne den leeren Rand')]),
    dict(nr='02', key='beach-craft', name='Beach Craft – Raft Survival', kind='Mod', cf_id=1010922,
         cf_url='https://www.curseforge.com/minecraft/mc-mods/beach-craft', mr_url='https://modrinth.com/mod/beach-craft',
         sets=[dict(tag='icon', label='Projekt-Icon (mit Titel)', master=os.path.join(BC_LOGO, 'logo_1024.png'),
                    fixed={512: os.path.join(BC_LOGO, 'logo_512.png'), 400: os.path.join(BC_LOGO, 'logo_400.png'),
                           256: os.path.join(BC_LOGO, 'logo_256.png')},
                    source='Archiv `beachcraft/logo` (1024 liegt auf Modrinth, 400 auf CurseForge)'),
               dict(tag='icon-ohne-titel', label='Icon ohne Titel', master=os.path.join(BC_LOGO, 'icon_1024.png'),
                    fixed={128: os.path.join(BC_LOGO, 'icon_128.png')},
                    source='Archiv `beachcraft/logo`; die 128er Fassung ist das Mod-Icon in der Jar (seit 3.2.0)')],
         extras=[dict(file='beach-craft_mod-icon-alt_1024.png',
                      src=git('Kasax_Raft_Mod', '9c231eb5ed90dc2bec5c52c618a023031e0d275f'),
                      label='altes Mod-Icon', note='Mod-Icon in der Jar bis Version 3.1 (Floß zwischen Inseln)')]),
    dict(nr='03', key='quest-icons', name='Quest Icons – Quest Book & Icons', kind='Mod', cf_id=690531,
         cf_url='https://www.curseforge.com/minecraft/mc-mods/quest-icons', mr_url='https://modrinth.com/mod/quest-icons',
         sets=[dict(tag='icon', label='Projekt-Icon', master=cf_orig('quest-icons'), source='CurseForge'),
               dict(tag='mod-icon', label='Mod-Icon (im Spiel)', pixel=16, sizes=[512, 256, 128, 64, 16],
                    master=git('Kasax_Quests_Items_Mod-1.19.2', 'HEAD:src/main/resources/assets/questsicons/icon.png'),
                    source='Jar (`assets/questsicons/icon.png`); Pixel-Art mit 16×16 Punkten, 128 ist die Datei aus der Jar')]),
    dict(nr='04', key='tamacraft', name='Tamacraft – Rare Pets', kind='Mod', cf_id=1758309,
         cf_url='https://www.curseforge.com/minecraft/mc-mods/tamacraft', mr_url='https://modrinth.com/mod/tamacraft',
         sets=[dict(tag='icon', label='Projekt-Icon', master=cf_orig('tamacraft'),
                    source='CurseForge; die Ecken sind durchsichtig'),
               dict(tag='mod-icon', label='Mod-Icon (im Spiel)',
                    master=git('tamagotchi', 'HEAD:src/main/resources/assets/tamacraft/icon.png'),
                    source='Jar (`assets/tamacraft/icon.png`)')]),
    dict(nr='05', key='challenge-craft', name='Challenge Craft – Challenge Runs & Lockout Bingo', kind='Mod (Fabric)',
         cf_id=1508454, cf_url='https://www.curseforge.com/minecraft/mc-mods/challenge',
         mr_url='https://modrinth.com/mod/challenge_craft',
         sets=[dict(tag='icon', label='Projekt-Icon', master=CC_LOGO, keep_jpg=True,
                    source='Mod-Repo `docs/curseforge/src/pack_logo.jpg` (720 px, JPEG): die größte Fassung, die es gibt'),
               dict(tag='mod-icon', label='Mod-Icon (im Spiel)',
                    master=git('Kasax_Challenge_Craft', 'HEAD:src/main/resources/assets/challengecraft/icon.png'),
                    source='Jar (`assets/challengecraft/icon.png`)')]),
    dict(nr='06', key='challenge-craft-modpack', name='Challenge Craft Modpack', kind='Modpack (Fabric)', cf_id=1653698,
         cf_url='https://www.curseforge.com/minecraft/modpacks/challenge-craft',
         mr_url='https://modrinth.com/modpack/challenge-craft-modpack',
         sets=[dict(tag='icon', label='Projekt-Icon', master=CC_LOGO, keep_jpg=True,
                    source='dasselbe Bild wie beim Mod Challenge Craft')]),
    dict(nr='07', key='dreamcraft-forge', name='Dreamcraft [FORGE]', kind='Modpack (Forge, 2022)', cf_id=582205,
         cf_url='https://www.curseforge.com/minecraft/modpacks/dreamcraft-forge',
         sets=[dict(tag='icon', label='Projekt-Icon', master=cf_orig('dreamcraft-forge'),
                    source='CurseForge; dasselbe Bild wie bei Dreamcraft (Fabric)')]),
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
        _, repo, spec = src
        cmd = ['git', '-C', repo, 'show', spec] if ':' in spec else ['git', '-C', repo, 'cat-file', 'blob', spec]
        return subprocess.run(cmd, check=True, capture_output=True).stdout
    with open(src, 'rb') as f:
        return f.read()


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)


def png(im):
    out = io.BytesIO()
    im.save(out, 'PNG', optimize=True)
    return out.getvalue()


def opaque(im):
    """True when nothing of the image is see-through (CurseForge stores some opaque icons with alpha 250-255)."""
    return im.mode not in ('RGBA', 'LA', 'PA') or im.convert('RGBA').getchannel('A').getextrema()[0] >= 250


def load(data):
    im = Image.open(io.BytesIO(data))
    im.load()
    if im.mode == 'P':
        im = im.convert('RGBA' if 'transparency' in im.info else 'RGB')
    return im


def scaled(im, size, pixel=False):
    if pixel:
        return im.resize((size, size), Image.NEAREST)
    if opaque(im):
        return im.convert('RGB').resize((size, size), Image.LANCZOS)
    return im.convert('RGBA').resize((size, size), Image.LANCZOS)


def fetch():
    def get(url, out):
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            write(out, r.read())
        print('fetched', os.path.relpath(out, PACK))

    for key, live in LIVE.items():
        a, b, name = live['cf'].split('/')
        get(f'https://media.forgecdn.net/avatars/{live["cf"]}', cf_orig(key))
        get(f'https://media.forgecdn.net/avatars/thumbnails/{a}/{b}/256/256/{name}',
            os.path.join(ORIG, 'curseforge', f'{key}_curseforge_256.png'))
        if 'mr' in live:
            pid, sha = live['mr']
            get(f'https://cdn.modrinth.com/data/{pid}/{sha}.png', os.path.join(ORIG, 'modrinth', f'{key}_modrinth_original.png'))
            get(f'https://cdn.modrinth.com/data/{pid}/{sha}_96.webp', os.path.join(ORIG, 'modrinth', f'{key}_modrinth_96.webp'))


# ---------------------------------------------------------------- the pack

def build_sets():
    """Writes the project folders and returns the manifest rows."""
    rows = []
    for p in PROJECTS:
        folder = os.path.join(PACK, f'{p["nr"]}_{p["key"]}')
        shutil.rmtree(folder, ignore_errors=True)
        for s in p['sets']:
            data = read(s['master'])
            master = load(data)
            assert master.size[0] == master.size[1], (p['key'], s['tag'], master.size)
            native = master.size[0]
            sizes = s.get('sizes') or [n for n in SIZES if n < native]
            for size in sorted(set(sizes) | {native}, reverse=True):
                rel = f'{p["nr"]}_{p["key"]}/{p["key"]}_{s["tag"]}_{size}.png'
                if size == native:
                    if master.format == 'PNG':
                        out, how = data, 'Original'
                    else:  # a JPEG master: the same pixels as PNG, and the file itself next to it
                        out, how = png(master.convert('RGB')), f'Original ({master.format}) als PNG'
                        if s.get('keep_jpg'):
                            jpg = rel[:-4] + '.jpg'
                            write(os.path.join(PACK, jpg), data)
                            rows.append(dict(project=p['key'], set=s['tag'], file=jpg, size=native, how='Original'))
                elif size in s.get('fixed', {}):
                    out, how = read(s['fixed'][size]), 'eigene Fassung'
                elif s.get('pixel'):
                    assert size % s['pixel'] == 0 and native % s['pixel'] == 0
                    grid = master.resize((s['pixel'], s['pixel']), Image.NEAREST)
                    assert grid.resize(master.size, Image.NEAREST).tobytes() == master.tobytes(), 'not pixel art'
                    out = png(scaled(grid, size, pixel=True))
                    how = 'Pixel-Art, verlustfrei vergrößert' if size > native else 'Pixel-Art, verlustfrei'
                else:
                    assert size < native, (rel, 'would be scaled up')
                    out, how = png(scaled(master, size)), 'verkleinert'
                write(os.path.join(PACK, rel), out)
                rows.append(dict(project=p['key'], set=s['tag'], file=rel, size=size, how=how))
        for e in p.get('extras', []):
            data = read(e['src'])
            if e.get('trim'):
                im = load(data).convert('RGBA')
                box = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
                pad = 16
                box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.size[0], box[2] + pad), min(im.size[1], box[3] + pad))
                data = png(im.crop(box))
            rel = f'{p["nr"]}_{p["key"]}/extras/{e["file"]}'
            write(os.path.join(PACK, rel), data)
            im = load(data)
            rows.append(dict(project=p['key'], set='extras', file=rel, size=f'{im.size[0]}×{im.size[1]}',
                             how=e['note'], label=e['label']))
    return rows


def build_uniform(rows):
    """One folder per size with the icon of every project, for grids and lists."""
    for size in (400, 256):
        folder = os.path.join(PACK, f'alle-icons_{size}px')
        shutil.rmtree(folder, ignore_errors=True)
        for p in PROJECTS:
            src = os.path.join(PACK, f'{p["nr"]}_{p["key"]}', f'{p["key"]}_icon_{size}.png')
            rel = f'alle-icons_{size}px/{p["nr"]}_{p["key"]}.png'
            write(os.path.join(PACK, rel), read(src))
            rows.append(dict(project=p['key'], set='alle', file=rel, size=size, how='Kopie'))


def font(name, size):
    return ImageFont.truetype(os.path.join(ARCHIVE, 'fonts', name), size)


def tile(path, size):
    """An image fitted into a square, on the card colour (transparent parts show the card)."""
    im = load(read(path)).convert('RGBA')
    w, h = im.size
    k = min(size / w, size / h)
    new = (max(1, round(w * k)), max(1, round(h * k)))
    im = im.resize(new, Image.NEAREST if max(w, h) <= 128 and k >= 1 else Image.LANCZOS)
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.alpha_composite(im, ((size - new[0]) // 2, (size - new[1]) // 2))
    return out


def build_overview():
    bg, card, line, text, muted, accent = (18, 19, 28), (30, 32, 46), (52, 55, 78), (240, 241, 248), (160, 165, 190), (150, 200, 255)
    cols, cw, ch, gap, margin, top = 3, 620, 356, 24, 40, 132
    rows_n = (len(PROJECTS) + cols - 1) // cols
    W = margin * 2 + cols * cw + (cols - 1) * gap
    H = top + rows_n * ch + (rows_n - 1) * gap + margin
    im = Image.new('RGBA', (W, H), bg + (255,))
    d = ImageDraw.Draw(im)
    d.text((margin, 34), 'Kasax007 – Projekt-Icons', font=font('InterDisplay-Bold.otf', 44), fill=text)
    d.text((margin, 92), f'Stand {STAND} · 9 Projekte auf CurseForge, 6 davon auch auf Modrinth · '
                         'die Zahl nennt die größte Fassung in Pixeln', font=font('Inter-SemiBold.otf', 18), fill=muted)
    f_name, f_kind, f_small = font('InterDisplay-Bold.otf', 23), font('Inter-SemiBold.otf', 16), font('Inter-SemiBold.otf', 13)
    for i, p in enumerate(PROJECTS):
        x = margin + (i % cols) * (cw + gap)
        y = top + (i // cols) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], 18, fill=card, outline=line)
        folder = os.path.join(PACK, f'{p["nr"]}_{p["key"]}')
        main = p['sets'][0]
        native = load(read(main['master'])).size[0]
        im.alpha_composite(tile(os.path.join(folder, f'{p["key"]}_icon_{native}.png'), 232), (x + 20, y + 20))
        tx = x + 274
        # the name, wrapped to the card
        words, lines_, cur = p['name'].split(), [], ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=f_name) <= cw - 274 - 18 or not cur:
                cur = t
            else:
                lines_.append(cur); cur = w
        lines_.append(cur)
        ty = y + 22
        for ln in lines_[:3]:
            d.text((tx, ty), ln, font=f_name, fill=text); ty += 30
        d.text((tx, ty + 4), p['kind'], font=f_kind, fill=muted); ty += 30
        d.text((tx, ty), 'CurseForge + Modrinth' if p.get('mr_url') else 'CurseForge', font=f_kind, fill=accent); ty += 28
        d.text((tx, ty), f'Ordner {p["nr"]}_{p["key"]}', font=f_small, fill=muted); ty += 20
        d.text((tx, ty), f'Icon bis {native} px', font=f_small, fill=muted)
        # the other pictures of the project
        small = []
        for s in p['sets'][1:]:
            n = load(read(s['master'])).size[0]
            small.append((os.path.join(folder, f'{p["key"]}_{s["tag"]}_{n}.png'), s['label'].split(' (')[0], f'{n} px'))
        for e in p.get('extras', []):
            if e.get('trim'):
                continue
            path = os.path.join(folder, 'extras', e['file'])
            sz = load(read(path)).size
            small.append((path, e['label'], f'{sz[0]} px' if sz[0] == sz[1] else f'{sz[0]}×{sz[1]}'))
        sx = x + 20
        for path, label, px in small[:5]:
            im.alpha_composite(tile(path, 64), (sx, y + 268))
            d.text((sx + 72, y + 276), label, font=f_small, fill=text)
            d.text((sx + 72, y + 296), px, font=f_small, fill=muted)
            sx += 72 + int(max(d.textlength(label, font=f_small), d.textlength(px, font=f_small))) + 22
        if not small:
            d.text((x + 20, y + 290), 'nur das Projekt-Icon', font=f_small, fill=muted)
    write(os.path.join(PACK, 'uebersicht.png'), png(im.convert('RGB')))


def dims(path):
    im = Image.open(path)
    return f'{im.size[0]}×{im.size[1]}'


def build_readme(rows):
    L = []
    L += ['# Icons meiner Projekte (Kasax007)', '',
          f'Stand: {STAND}. 9 Projekte auf CurseForge, 6 davon auch auf Modrinth. Alle Bilder auf einen Blick: '
          '`uebersicht.png`.', '',
          '## Inhalt', '',
          '| Ordner | Projekt | Art | Projekt-Icon bis | Sonst noch |', '| --- | --- | --- | --- | --- |']
    for p in PROJECTS:
        native = max(r['size'] for r in rows if r['project'] == p['key'] and r['set'] == 'icon')
        more = [s['label'] for s in p['sets'][1:]] + [e['label'] for e in p.get('extras', [])]
        L.append(f'| `{p["nr"]}_{p["key"]}` | {p["name"]} | {p["kind"]} | {native} px | {", ".join(more) or "–"} |')
    L += ['| `alle-icons_400px`, `alle-icons_256px` | alle 9 Projekt-Icons in einer Größe | | 400 und 256 px | |',
          '| `plattform-originale` | die Dateien genau so, wie CurseForge und Modrinth sie ausliefern | | | |', '',
          '## Dateinamen', '',
          '- `<projekt>_icon_<größe>.png`: das Projekt-Icon, wie es auf CurseForge und Modrinth zu sehen ist. Die Zahl ist '
          'die Kantenlänge in Pixeln, alle Bilder sind quadratisch.',
          '- `<projekt>_icon-ohne-titel_<größe>.png`: Beach Craft ohne den Schriftzug.',
          '- `<projekt>_mod-icon_<größe>.png`: das Symbol, das im Spiel in der Mod-Liste steht (es steckt in der Jar).',
          '- `extras/`: Server-Icon, Schriftzug und ältere Fassungen.', '',
          '## So sind die Größen entstanden', '',
          '- Die größte Datei jeder Reihe ist das Original und unverändert (Byte für Byte).',
          '- Kleinere Größen sind daraus verkleinert. Nichts wurde hochgerechnet, deshalb gibt es je Projekt '
          'unterschiedlich viele Größen.',
          '- Ausnahme Quest Icons, Mod-Icon: Das ist Pixel-Art mit 16×16 Punkten und lässt sich ohne Verlust vergrößern.',
          '- Beach Craft: 512, 400 und 256 sind die Fassungen aus dem Archiv (400 liegt auf CurseForge).', '',
          '## Gut zu wissen', '',
          '- **Challenge Craft:** Mod und Modpack haben dasselbe Icon. Die größte Fassung ist ein JPEG mit 720 px; sie liegt '
          'als `.jpg` (Original) und als `.png` bei. Auf CurseForge liegt eine Fassung mit 400 px.',
          '- **Dreamcraft:** Fabric und Forge haben dasselbe Icon (800 px).',
          '- **Tamacraft:** Die Ecken des Icons sind durchsichtig. Das Mod-Icon in der Jar ist etwas anders zugeschnitten.',
          '- **Beach Craft:** Das Mod-Icon in der Jar ist `beach-craft_icon-ohne-titel_128.png`. Bis Version 3.1 war es das '
          'Bild in `extras/`.',
          '- **Modrinth:** Dort liegt beim Challenge Craft Modpack nur eine Fassung mit 64 px, bei Quest Icons und Tamacraft '
          'eine mit 256 px. Modrinth zeigt Icons mit 96 px an.',
          '- **Lightspeed Performance, Beautifully:** Von diesen Icons gibt es nur die 400 px von CurseForge.', '']
    L += ['## Alle Dateien', '']
    for p in PROJECTS:
        links = f'[CurseForge]({p["cf_url"]}) (Projekt {p["cf_id"]})' + (f', [Modrinth]({p["mr_url"]})' if p.get('mr_url') else '')
        L += [f'### {p["nr"]} · {p["name"]}', '', f'{p["kind"]} · {links}', '']
        for s in p['sets']:
            L += [f'**{s["label"]}** – Vorlage: {s["source"]}', '', '| Datei | Pixel | Entstehung |', '| --- | --- | --- |']
            for r in [r for r in rows if r['project'] == p['key'] and r['set'] == s['tag']]:
                L.append(f'| `{os.path.basename(r["file"])}` | {r["size"]}×{r["size"]} | {r["how"]} |')
            L.append('')
        ex = [r for r in rows if r['project'] == p['key'] and r['set'] == 'extras']
        if ex:
            L += ['**Extras**', '', '| Datei | Pixel | Was es ist |', '| --- | --- | --- |']
            L += [f'| `extras/{os.path.basename(r["file"])}` | {r["size"]} | {r["how"]} |' for r in ex]
            L.append('')
    L += ['### Plattform-Originale', '',
          'Unverändert heruntergeladen. `original` ist die hochgeladene Datei, `256` und `96` sind die Vorschaubilder der '
          'Plattform.', '', '| Datei | Pixel |', '| --- | --- |']
    for sub in ('curseforge', 'modrinth'):
        for fn in sorted(os.listdir(os.path.join(ORIG, sub))):
            L.append(f'| `plattform-originale/{sub}/{fn}` | {dims(os.path.join(ORIG, sub, fn))} |')
    L.append('')
    write(os.path.join(PACK, 'LIESMICH.md'), '\n'.join(L).encode('utf-8'))


def build_zip():
    out = os.path.join(HERE, f'{NAME}.zip')
    files = []
    for root, dirs, names in os.walk(PACK):
        dirs.sort()
        for n in sorted(names):
            files.append(os.path.join(root, n))
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(files, key=lambda q: os.path.relpath(q, PACK)):
            info = zipfile.ZipInfo(f'{NAME}/' + os.path.relpath(path, PACK).replace(os.sep, '/'), (2026, 11, 13, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, read(path))
    return out, len(files)


def main():
    if '--fetch' in sys.argv:
        fetch()
    missing = [k for k in LIVE if not os.path.exists(cf_orig(k))]
    if missing:
        sys.exit(f'platform originals missing for {missing}: run with --fetch')
    for stale in ('uebersicht.png', 'LIESMICH.md'):
        if os.path.exists(os.path.join(PACK, stale)):
            os.remove(os.path.join(PACK, stale))
    rows = build_sets()
    build_uniform(rows)
    build_overview()
    build_readme(rows)
    for sub in ('curseforge', 'modrinth'):
        for fn in sorted(os.listdir(os.path.join(ORIG, sub))):
            rows.append(dict(project=fn.split('_')[0], set='plattform', file=f'plattform-originale/{sub}/{fn}',
                             size=dims(os.path.join(ORIG, sub, fn)), how='Plattform-Original'))
    for r in rows:
        r['sha1'] = hashlib.sha1(read(os.path.join(PACK, r['file']))).hexdigest()
    write(os.path.join(HERE, 'manifest.json'), json.dumps(rows, ensure_ascii=False, indent=1).encode('utf-8'))
    out, n = build_zip()
    print(f'{n} files, {os.path.getsize(out) / 1e6:.1f} MB: {out}')


if __name__ == '__main__':
    main()
