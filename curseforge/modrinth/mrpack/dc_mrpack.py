"""Dreamcraft 26.3 V1.5.1 for Modrinth: finish the index prepared from the CurseForge pack, write the .mrpack, and
install it the way a launcher does (client) and a host does (server) for a smoke test.
  python3 dc_mrpack.py build      -> $SP/mrpack/out/Dreamcraft 26.3 V1.5.1.mrpack
  python3 dc_mrpack.py install    -> $SP/mrtest/client, $SP/mrtest/server (jars hard-linked from the caches by sha1,
                                     anything else downloaded from its Modrinth URL; every file checked against its sha1)
Left out (not on Modrinth, no permission to bundle): EpheroLib, Cupboard, fix GPU memory leak, Memory Settings,
Smooth Chunk Save, Structure Essentials, More Villagers. Quarry Reborn is bundled in overrides/mods under its CC0-1.0
license (credited in the description and changelog)."""
import json, os, sys, zipfile, hashlib, glob, shutil, urllib.request
SP = '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad'
D = f'{SP}/mrpack/dreamcraft'
OUT = f'{SP}/mrpack/out/Dreamcraft 26.3 V1.5.1.mrpack'
QUARRY_FID = None


def sha1(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def build():
    idx = json.load(open(f'{D}/modrinth.index.json'))
    mapping = json.load(open(f'{D}/mapping.json'))
    for f in idx['files']:
        if os.path.basename(f['path']).startswith('drippyloadingscreen'):
            f['env']['server'] = 'unsupported'          # client-only list of mkpack.py, as in the tested server pack
    done = json.load(open(f'{SP}/mr/versions_done.json'))
    for key in ('ohf5LwXu:1.3.0+26.3', '3PmzwJU0:3.3.0+26.3', 'lyuVXQEh:1.3.0+26.3'):
        v = done[key]; assert v['same_bytes']
        idx['files'].append({'path': 'mods/' + v['file'], 'hashes': {'sha1': v['sha1'], 'sha512': v['sha512']},
                             'env': {'client': 'required', 'server': 'required'}, 'downloads': [v['url']], 'fileSize': v['size']})
    idx['versionId'] = '26.3-V1.5.1'
    idx['name'] = 'Dreamcraft 26.3'
    idx['summary'] = 'Quests and adventure on Minecraft 26.3 Fabric: magic, tech, new biomes, a raft ocean and rare pets.'
    quarry = next(e for e in mapping if e['status'] == 'missing' and e['curseforge']['projectID'] == 511254)
    qjar = glob.glob(f"{SP}/jars/{quarry['curseforge']['fileID']}-*.jar")[0]
    assert sha1(qjar) == quarry['cf_sha1']
    hosts = {u.split('/')[2] for f in idx['files'] for u in f['downloads']}
    assert hosts <= {'cdn.modrinth.com'}, hosts
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    n = 0
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('modrinth.index.json', json.dumps(idx, indent=1))
        for root, _, files in os.walk(f'{D}/overrides'):
            for fn in files:
                p = os.path.join(root, fn)
                z.write(p, 'overrides/' + os.path.relpath(p, f'{D}/overrides').replace(os.sep, '/')); n += 1
        z.write(qjar, 'overrides/mods/' + quarry['curseforge']['file']); n += 1
    print('mrpack', OUT, os.path.getsize(OUT) // 1024, 'KB |', len(idx['files']), 'downloads |', n, 'override files')


def cache_index():
    idx = {}
    for p in glob.glob(f'{SP}/jars/*.jar') + glob.glob(f'{SP}/jars/*.zip') + glob.glob(f'{SP}/mr/jars/*.jar'):
        idx.setdefault(sha1(p), p)
    return idx


def install():
    z = zipfile.ZipFile(OUT)
    idx = json.loads(z.read('modrinth.index.json'))
    cache = cache_index()
    for side in ('client', 'server'):
        root = f'{SP}/mrtest/{side}'
        shutil.rmtree(root, ignore_errors=True); os.makedirs(root)
        got = linked = 0
        for f in idx['files']:
            if f['env'][side] == 'unsupported': continue
            dst = os.path.join(root, f['path']); os.makedirs(os.path.dirname(dst), exist_ok=True)
            src = cache.get(f['hashes']['sha1'])
            if src:
                os.link(src, dst); linked += 1
            else:
                req = urllib.request.Request(f['downloads'][0], headers={'User-Agent': 'Kasax007-release-sync/1.0'})
                open(dst, 'wb').write(urllib.request.urlopen(req, timeout=300).read()); got += 1
                cache[f['hashes']['sha1']] = dst
            assert sha1(dst) == f['hashes']['sha1'], dst
        for n in z.namelist():
            if n.startswith('overrides/') and not n.endswith('/'):
                dst = os.path.join(root, n[len('overrides/'):]); os.makedirs(os.path.dirname(dst), exist_ok=True)
                open(dst, 'wb').write(z.read(n))
        print(side, len(os.listdir(f'{root}/mods')), 'mods |', linked, 'linked from cache,', got, 'downloaded')


if __name__ == '__main__':
    {'build': build, 'install': install}[sys.argv[1]]()
