"""Modrinth versions of the CurseForge descriptions.

The CurseForge pages use long <h3> intro sentences, CurseForge spoiler boxes and pictures without alt text. Modrinth checks
every description on its server (labrinth, validate/project/description.rs) and blocks the review when a header is longer
than 80 characters, two headers of the same level follow each other, the text ends with a header, or the text looks like
spam (for example the same credit line repeated per music track). This script turns each CurseForge HTML into a Modrinth
description that passes those checks:
  - long headers become bold centered paragraphs, short ones stay headers;
  - <div class="spoiler"> with its label paragraph becomes <details><summary>;
  - style="text-align:center" becomes align="center" (Modrinth drops style attributes);
  - every picture gets alt text, spacer paragraphs go, the video block gets its YouTube id;
  - per project fixes (music credits as one list, no 1.20.1 picture gallery, Modrinth links in mod lists).

  python3 make_modrinth.py OUT_DIR [urlmap.json]   (urlmap: CurseForge page URL -> Modrinth page URL, for every link)
"""
import json, os, re, sys, html as H

SP = '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad'
PROJECTS = {
    'beach-craft': {'src': '/home/user/Kasax_Raft_Mod/docs/curseforge/description.html', 'video': 'NdFPSYZ32R4'},
    'quest-icons': {'src': f'{SP}/qi13desc/description.html'},
    'tamacraft': {'src': f'{SP}/tc13desc/description.html', 'video': 'UIE0waos-yo'},
    'challenge_craft': {'src': f'{SP}/ccdesc/description-mod.html'},
    'challenge-craft-modpack': {'src': f'{SP}/ccdesc/wt/docs/curseforge/description-modpack.html'},
    'dreamcraft': {'src': '/home/user/Modpack-Development/docs/curseforge/description.html', 'video': 'G-whF3xKTQ4'},
}
BH_ALT = {'bh_header': 'Dreamcraft, hosted by BisectHosting', 'bh_promo': 'BisectHosting: use code Kasax007 for 25% off',
          'bh_1': 'Section banner: what Minecraft in your dreams could look like', 'bh_2': 'Section banner',
          'bh_3': 'Section banner', 'bh_4': 'Section banner', 'bh_5': 'Section banner', 'bh_6': 'Section banner'}


def text_of(fragment):
    return H.unescape(re.sub(r'<[^>]+>', '', fragment)).strip()


def fix_headers(s):
    def repl(m):
        level, attrs, inner = m.group(1), m.group(2), m.group(3)
        if len(text_of(re.sub(r'<br\s*/?>', ' ', inner))) <= 80:
            return m.group(0)
        inner = re.sub(r'^\s*<strong>(.*)</strong>\s*$', r'\1', inner, flags=re.S)
        return f'<p{attrs}><strong>{inner}</strong></p>'
    return re.sub(r'(?is)<h([1-6])([^>]*)>(.*?)</h\1>', repl, s)


def fix_spoilers(s):
    out, pos = [], 0
    pat = re.compile(r'(?is)(?:<p>\s*<strong>(.*?)</strong>\s*</p>\s*)?<div class="spoiler">')
    while True:
        m = pat.search(s, pos)
        if not m:
            out.append(s[pos:]); break
        start_inner = m.end()
        depth, i = 1, start_inner
        while depth:
            o = s.find('<div', i); c = s.find('</div>', i)
            if o != -1 and o < c:
                depth += 1; i = o + 4
            else:
                depth -= 1; i = c + 6
        label = (m.group(1) or 'Details').strip().rstrip(':')
        out.append(s[pos:m.start()])
        out.append(f'<details>\n<summary><strong>{label}</strong></summary>\n\n' + s[start_inner:i - 6].strip() + '\n\n</details>')
        pos = i
    return ''.join(out)


def fix_images(s):
    def repl(m):
        tag = m.group(0)
        a = re.search(r'''\balt\s*=\s*"([^"]*)"''', tag)
        if a and a.group(1).strip():
            return tag
        src = re.search(r'src="([^"]+)"', tag).group(1)
        base = os.path.splitext(src.rsplit('/', 1)[-1])[0]
        alt = BH_ALT.get(base) or re.sub(r'[_\-]+', ' ', base).strip().capitalize() or 'Picture'
        tag = re.sub(r'\balt\s*=\s*"[^"]*"', '', tag)
        return tag[:-1].rstrip('/ ') + f' alt="{H.escape(alt)}">'
    return re.sub(r'(?is)<img\b[^>]*>', repl, s)


def music_credits(s):
    """The per-track credit lines (identical except the title) read as spam on Modrinth: one line plus a list."""
    tracks = re.findall(r'<p>"([^"]+)" Kevin MacLeod \(<a href="https://incompetech\.com/"[^>]*>incompetech\.com</a>\)'
                        r'<br>Licensed under Creative Commons: By Attribution 4\.0 License<br><a [^>]*>[^<]*</a></p>\s*', s)
    if not tracks:
        return s
    first = s.index('<p>"' + tracks[0] + '" Kevin MacLeod')
    block = re.compile(r'(<p>"[^"]+" Kevin MacLeod \(<a href="https://incompetech\.com/"[^>]*>incompetech\.com</a>\)'
                       r'<br>Licensed under Creative Commons: By Attribution 4\.0 License<br><a [^>]*>[^<]*</a></p>\s*)+')
    m = block.search(s, first)
    new = ('<p>All tracks by Kevin MacLeod (<a href="https://incompetech.com/">incompetech.com</a>), licensed under '
           '<a href="http://creativecommons.org/licenses/by/4.0/">Creative Commons: By Attribution 4.0 License</a>:</p>\n<ul>\n'
           + ''.join(f'<li>“{t}”</li>\n' for t in tracks) + '</ul>\n')
    return s[:m.start()] + new + s[m.end():]


def drop_spoiler(s, label_start):
    """Remove a whole <details> block whose summary starts with label_start."""
    return re.sub(r'(?is)<details>\s*<summary><strong>' + re.escape(label_start) + r'.*?</details>\s*', '', s)


def convert(key, cfg, mapping):
    s = open(cfg['src']).read()
    s = re.sub(r'(?s)<!-- VIDEO START -->(.*?)<!-- VIDEO END -->', lambda m: m.group(1).replace('VIDEO_ID', cfg.get('video', '')), s)
    s = re.sub(r'(?s)<!--.*?-->', '', s)
    s = re.sub(r'\s*style="\s*text-align:\s*center;?\s*"', ' align="center"', s)
    s = re.sub(r'(?i)<p>\s*&nbsp;\s*</p>\s*', '', s)
    s = fix_headers(s)
    s = fix_spoilers(s)
    s = fix_images(s)
    s = music_credits(s)
    if key == 'dreamcraft':
        s = drop_spoiler(s, 'Pictures from the 1.20.1 version')
        s = re.sub(r'(?is)<p><strong>Donations are much appreciated.*?</p>\s*', '', s)
    for cf, mr in sorted((mapping or {}).items(), key=lambda kv: -len(kv[0])):
        s = re.sub(re.escape(cf) + r'/?(?=["\s<)])', mr, s)
    if key == 'dreamcraft':
        s = dreamcraft_modrinth(s)
    s = s.replace(' rel="nofollow"', '')
    s = re.sub(r'\n{3,}', '\n\n', s).strip() + '\n'
    return s


# Mods of the CurseForge pack that may not be bundled in a Modrinth pack (not on Modrinth, all rights reserved or no
# permission to re-host); the Modrinth version of Dreamcraft leaves them out until their authors allow it.
DC_LEFT_OUT = [('more-villagers-fabric', 'More Villagers'), ('cupboard', 'Cupboard'), ('memory-settings', 'Memory Settings'),
               ('smooth-chunk-save', 'Smooth Chunk Save'), ('structure-essentials-forge-fabric', 'Structure Essentials'),
               ('fix-gpu-memory-leak', 'fix GPU memory leak'), ('epherolib', 'EpheroLib')]
DC_MODS_CF, DC_MODS_MR = 251, 244


def dreamcraft_modrinth(s):
    for slug, _ in DC_LEFT_OUT:
        s = re.sub(r'<li><a href="https://www\.curseforge\.com/minecraft/mc-mods/' + re.escape(slug) + r'">[^<]*</a>[^\n]*</li>\n', '', s)
    s = s.replace(f'All {DC_MODS_CF} mods are in the mod list below.', f'All {DC_MODS_MR} mods of the Modrinth version are in the mod list below.')
    s = s.replace(f'All {DC_MODS_CF} mods of Dreamcraft 26.3 and the two shader packs', f'All {DC_MODS_MR} mods of the Modrinth version and the two shader packs')
    names = ', '.join(n for _, n in DC_LEFT_OUT[:-1]) + ' and ' + DC_LEFT_OUT[-1][1]
    note = (f'<p align="center"><strong>Modrinth version:</strong> {DC_MODS_MR} of the {DC_MODS_CF} mods of Dreamcraft. '
            f'Seven mods exist only on CurseForge and may not be bundled in a Modrinth pack without their authors\' permission: '
            f'{names}. Everything else, all 369 quests included, is the same. As soon as the authors allow it, they come back '
            'here. The complete pack is also on <a href="https://www.curseforge.com/minecraft/modpacks/dreamcraft-new">CurseForge</a>.</p>\n'
            '<p align="center">Included under its license: <a href="https://www.curseforge.com/minecraft/mc-mods/quarry-reborn">Quarry '
            'Reborn</a> by TEDinc, DissiNL and NikiIncredible (CC0-1.0).</p>\n')
    anchor = s.index('<p align="center">With my own mods')
    end = s.index('</p>', anchor) + len('</p>\n')
    return s[:end] + note + s[end:]


if __name__ == '__main__':
    out = sys.argv[1]
    mapping = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}
    os.makedirs(out, exist_ok=True)
    for key, cfg in PROJECTS.items():
        md = convert(key, cfg, mapping)
        open(os.path.join(out, key + '.md'), 'w').write(md)
        print(key, len(md), 'chars')
