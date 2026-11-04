"""Was in den gefilmten Kisten liegt: liest die gespeicherte Welt (Region-Dateien, Anvil/NBT) und schreibt pro
Kisten-Aufnahme die Item-Namen nach tools/loot.json. doc.py blendet sie unter dem Kisten-Bild ein.
  python3 -I tools/loot.py [welt-ordner]        (Standard: Kasax_Raft_Mod/build/run/bctest/saves/bcdoc)
Die Positionen der Kisten stehen in CHESTS (Name der Aufnahme -> Dimension, x y z)."""
import os, sys, json, zlib, struct, io, gzip

HERE = os.path.dirname(os.path.abspath(__file__))
WORLD = '/home/user/Kasax_Raft_Mod/build/run/bctest/saves/bcdoc'
VANILLA_LANG = '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad/vanilla/assets/minecraft/lang/en_us.json'
R = 'raft/raftdim'
CHESTS = {
    'p_galleon_chest': (R, -343, 46, -250), 'p_galleon_treasure': (R, -324, 53, -250), 'p_cargo_chest': (R, -304, 70, -224),
    'p_cargo_barrel': (R, -304, 59, -221), 'p_plane_crate': (R, -458, 61, -262), 'p_ruins_chest': (R, -486, 46, -229),
    'p_raft_chest': (R, -572, 101, -317), 'p_fishing_barrel': (R, 23, 53, 52), 'p_sanctum_reward': (R, -497, 70, -363),
    'p_sanctum_offer': (R, -502, 69, -357), 'p_temple_chest': (R, -316, 104, -301), 'p_temple_offer': (R, -326, 103, -292),
    's_saltmere_elder': (R, 146, 103, -8), 's_saltmere_shrine': (R, 172, 102, -39), 'p_saltmere_market': (R, 165, 102, -9),
    'p_saltmere_house': (R, 155, 103, 10), 'p_buoy_crate': (R, 105, 99, 12), 'p_iceberg_chest': (R, 34, 102, 257),
    'p_rig_chest': (R, 239, 115, 157), 's_lighthouse': (R, 447, 105, 75), 'p_lighthouse_storage': (R, 436, 104, 90),
    'p_shack_crate': (R, 444, 101, 178), 's_cove_captain': (R, 248, 101, 552), 'p_cove_loot': (R, 245, 102, 591),
}


# ------------------------------------------------------------------ minimal NBT reader

def _nbt(f, t):
    if t == 1:
        return struct.unpack('>b', f.read(1))[0]
    if t == 2:
        return struct.unpack('>h', f.read(2))[0]
    if t == 3:
        return struct.unpack('>i', f.read(4))[0]
    if t == 4:
        return struct.unpack('>q', f.read(8))[0]
    if t == 5:
        return struct.unpack('>f', f.read(4))[0]
    if t == 6:
        return struct.unpack('>d', f.read(8))[0]
    if t == 7:
        n = struct.unpack('>i', f.read(4))[0]
        return f.read(n)
    if t == 8:
        n = struct.unpack('>H', f.read(2))[0]
        return f.read(n).decode('utf-8', 'replace')
    if t == 9:
        et = f.read(1)[0]
        n = struct.unpack('>i', f.read(4))[0]
        return [_nbt(f, et) for _ in range(n)]
    if t == 10:
        d = {}
        while True:
            tt = f.read(1)[0]
            if tt == 0:
                return d
            n = struct.unpack('>H', f.read(2))[0]
            name = f.read(n).decode('utf-8', 'replace')
            d[name] = _nbt(f, tt)
    if t == 11:
        n = struct.unpack('>i', f.read(4))[0]
        return list(struct.unpack('>%di' % n, f.read(4 * n)))
    if t == 12:
        n = struct.unpack('>i', f.read(4))[0]
        return list(struct.unpack('>%dq' % n, f.read(8 * n)))
    raise ValueError('nbt tag %d' % t)


def read_root(data):
    f = io.BytesIO(data)
    t = f.read(1)[0]
    n = struct.unpack('>H', f.read(2))[0]
    f.read(n)
    return _nbt(f, t)


def chunk(world, dim, cx, cz):
    path = f'{world}/dimensions/{dim}/region/r.{cx >> 5}.{cz >> 5}.mca' if dim != 'overworld' else f'{world}/region/r.{cx >> 5}.{cz >> 5}.mca'
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        head = f.read(4096)
        i = 4 * ((cx & 31) + (cz & 31) * 32)
        off = int.from_bytes(head[i:i + 3], 'big')
        if off == 0:
            return None
        f.seek(off * 4096)
        length = struct.unpack('>i', f.read(4))[0]
        comp = f.read(1)[0]
        data = f.read(length - 1)
    if comp == 2:
        data = zlib.decompress(data)
    elif comp == 1:
        data = gzip.decompress(data)
    return read_root(data)


# ------------------------------------------------------------------ names

LANG = {}


def names():
    import glob
    for f in [VANILLA_LANG] + glob.glob('/home/user/Kasax_Raft_Mod/src/main/resources/assets/raft/lang/en_us.json') + \
            glob.glob('/home/user/Kasax_Raft_Mod/src/main/modules/*/assets/raft/lang/en_us.json'):
        if os.path.exists(f):
            LANG.update(json.load(open(f)))
    n = {}
    if os.path.exists(VANILLA_LANG):
        for k, v in json.load(open(VANILLA_LANG)).items():
            if k.startswith(('item.minecraft.', 'block.minecraft.')) and k.count('.') == 2:
                n['minecraft:' + k.split('.', 2)[2]] = v
    for k, v in json.load(open(os.path.join(HERE, 'names.json'))).items():
        n['raft:' + k] = v
    return n


def text_of(c):
    """a text component from NBT (string, compound or list) -> plain text"""
    if isinstance(c, str):
        return c
    if isinstance(c, dict):
        t = c.get('text', '') or LANG.get(c.get('translate', ''), c.get('translate', ''))
        return t + ''.join(text_of(x) for x in c.get('extra', []))
    if isinstance(c, list):
        return ''.join(text_of(x) for x in c)
    return ''


def item_name(it, N):
    comps = it.get('components', {})
    for key in ('minecraft:custom_name', 'minecraft:item_name'):
        if key in comps:
            t = text_of(comps[key])
            if t:
                return t
    if 'minecraft:written_book_content' in comps:
        title = comps['minecraft:written_book_content'].get('title', {})
        t = title.get('raw', '') if isinstance(title, dict) else str(title)
        if t:
            return t
    return N.get(it['id'], it['id'].split(':')[1].replace('_', ' ').title())


def from_logs(runs_dir):
    """containers opened in the film runs: 'OPENLOOT ... at x, y, z' or 'openbe x y z', followed by 'shot <name>'"""
    import glob, re
    found = {}
    for log in sorted(glob.glob(f'{runs_dir}/r*/latest.log')):
        pos = None
        for line in open(log, errors='replace'):
            m = re.search(r'OPENLOOT \S+ opened Block\{[^}]*\} at (-?\d+), (-?\d+), (-?\d+)', line)
            if m:
                pos = tuple(int(v) for v in m.groups())
                continue
            m = re.search(r'\[bctest\] \d+: openbe (-?\d+) (-?\d+) (-?\d+)', line)
            if m:
                pos = tuple(int(v) for v in m.groups())
                continue
            m = re.search(r'\[bctest\] \d+: shot (\S+)', line)
            if m and pos:
                found[m.group(1)] = (R,) + pos
                pos = None
    return found


def main(world=WORLD):
    N = names()
    out = {}
    CHESTS.update({k: v for k, v in from_logs('/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad/doc3/runs').items()
                   if k not in CHESTS})
    for shot, (dim, x, y, z) in CHESTS.items():
        ch = chunk(world, dim, x >> 4, z >> 4)
        if ch is None:
            print('no chunk for', shot)
            continue
        found = None
        for be in ch.get('block_entities', []):
            if be.get('x') == x and be.get('y') == y and be.get('z') == z:
                found = be
                break
        if found is None:
            print('no container at', shot, x, y, z)
            continue
        items = found.get('Items', [])
        agg = {}
        for it in items:
            nm = item_name(it, N)
            agg[nm] = agg.get(nm, 0) + it.get('count', 1)
        lst = [f'{nm} x{cnt}' if cnt > 1 else nm for nm, cnt in agg.items()]
        out[shot] = lst
        print(shot, '|', ', '.join(lst))
    json.dump(out, open(os.path.join(HERE, 'loot.json'), 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else WORLD)
