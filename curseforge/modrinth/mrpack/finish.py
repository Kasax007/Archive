#!/usr/bin/env python3
"""Add the user's own mods to the prepared Modrinth indexes and write the .mrpack files.

Usage:
  python3 finish.py own.json [--out DIR] [--allow-incomplete]
  python3 finish.py --template            # print an own.json skeleton (urls left empty)

own.json is a list of objects:
  {"path": "mods/x.jar", "url": "https://cdn.modrinth.com/...", "sha1": "...", "sha512": "...",
   "size": 123, "env": {"client": "required", "server": "required"}}
Optional per entry: "packs": ["dreamcraft", "challengecraft"] to force the target packs.
Without "packs", an entry goes into every pack whose mapping.json lists an own_pending file
with the same sha1 (the uploads are meant to be byte-identical to the CurseForge files).

Nothing is uploaded; this only writes zip files.
"""
import json, os, re, sys, zipfile
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
PACKS = {
    'dreamcraft': 'Dreamcraft 26.3 V1.5.1.mrpack',
    'challengecraft': 'Challenge Craft 26.3-v4.2.mrpack',
}
ALLOWED_HOSTS = {'cdn.modrinth.com', 'github.com', 'raw.githubusercontent.com', 'gitlab.com'}
ENV_VALUES = {'required', 'optional', 'unsupported'}


def load(pack):
    d = os.path.join(HERE, pack)
    with open(os.path.join(d, 'modrinth.index.json')) as f:
        idx = json.load(f)
    with open(os.path.join(d, 'mapping.json')) as f:
        mapping = json.load(f)
    return d, idx, mapping


def template():
    out = []
    for pack in PACKS:
        _, _, mapping = load(pack)
        for m in mapping:
            if m['status'] == 'own_pending':
                o = m['own']
                out.append({'path': o['path'], 'url': '', 'sha1': o['sha1'], 'sha512': o['sha512'],
                            'size': o['size'], 'env': o['env'],
                            '_note': f"{m['modrinth']['title']} ({pack}, CurseForge file {o['cf_fileID']})"})
    json.dump(out, sys.stdout, indent=2)
    print()


def check_entry(e, i):
    errs = []
    for k in ('path', 'url', 'sha1', 'sha512', 'size', 'env'):
        if k not in e:
            errs.append(f'entry {i}: missing "{k}"')
    if errs:
        return errs
    u = urlparse(e['url'])
    if u.scheme != 'https' or u.hostname not in ALLOWED_HOSTS:
        errs.append(f'entry {i}: url host not allowed by Modrinth: {e["url"]}')
    if not re.fullmatch(r'[0-9a-f]{40}', e['sha1']):
        errs.append(f'entry {i}: bad sha1')
    if not re.fullmatch(r'[0-9a-f]{128}', e['sha512']):
        errs.append(f'entry {i}: bad sha512')
    if not isinstance(e['size'], int) or e['size'] <= 0:
        errs.append(f'entry {i}: bad size')
    env = e['env']
    if not isinstance(env, dict) or set(env) != {'client', 'server'} or not set(env.values()) <= ENV_VALUES:
        errs.append(f'entry {i}: env must be {{"client": ..., "server": ...}} with required/optional/unsupported')
    p = e['path']
    if p.startswith('/') or '..' in p.split('/') or '\\' in p:
        errs.append(f'entry {i}: unsafe path {p}')
    return errs


def main(argv):
    if '--template' in argv:
        template()
        return 0
    out_dir = os.path.join(HERE, 'out')
    rest = list(argv)
    if '--out' in rest:
        k = rest.index('--out')
        if k + 1 >= len(rest):
            print(__doc__)
            return 2
        out_dir = rest[k + 1]
        del rest[k:k + 2]
    allow_incomplete = '--allow-incomplete' in rest
    args = [a for a in rest if not a.startswith('--')]
    if len(args) != 1:
        print(__doc__)
        return 2
    with open(args[0]) as f:
        own = json.load(f)
    if not isinstance(own, list):
        print('own.json must be a list')
        return 2

    errs = []
    for i, e in enumerate(own):
        errs += check_entry(e, i)
    if errs:
        print('\n'.join(errs))
        return 1

    plans = {}
    used = [False] * len(own)
    for pack in PACKS:
        d, idx, mapping = load(pack)
        pending = {m['own']['sha1']: m for m in mapping if m['status'] == 'own_pending'}
        add = []
        for i, e in enumerate(own):
            if 'packs' in e:
                take = pack in e['packs']
            else:
                take = e['sha1'] in pending
            if take:
                used[i] = True
                add.append(e)
                m = pending.get(e['sha1'])
                if m and m['own']['size'] != e['size']:
                    errs.append(f'{pack}: size of {e["path"]} differs from the CurseForge file')
        covered = {e['sha1'] for e in add}
        not_covered = [m for s, m in pending.items() if s not in covered]
        for m in not_covered:
            msg = f'{pack}: own mod not in own.json (or not byte-identical): {m["modrinth"]["title"]} sha1 {m["own"]["sha1"]}'
            if allow_incomplete:
                print('WARNING ' + msg)
            else:
                errs.append(msg)
        files = list(idx['files'])
        paths = {f['path'] for f in files}
        for e in add:
            if e['path'] in paths:
                errs.append(f'{pack}: duplicate path {e["path"]}')
            paths.add(e['path'])
            files.append({'path': e['path'], 'hashes': {'sha1': e['sha1'], 'sha512': e['sha512']},
                          'env': e['env'], 'downloads': [e['url']], 'fileSize': e['size']})
        idx = dict(idx)
        idx['files'] = sorted(files, key=lambda f: f['path'].lower())
        plans[pack] = (d, idx, len(add))
    for i, u in enumerate(used):
        if not u:
            errs.append(f'entry {i} ({own[i]["path"]}): sha1 matches no own_pending file; add "packs": [...] to force it')
    if errs:
        print('\n'.join(errs))
        return 1

    os.makedirs(out_dir, exist_ok=True)
    for pack, (d, idx, n) in plans.items():
        target = os.path.join(out_dir, PACKS[pack])
        tmp = target + '.part'
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
            z.writestr('modrinth.index.json', json.dumps(idx, indent=2))
            ov = os.path.join(d, 'overrides')
            for root, dirs, fnames in os.walk(ov):
                dirs.sort()
                for fn in sorted(fnames):
                    full = os.path.join(root, fn)
                    rel = os.path.relpath(full, d).replace(os.sep, '/')
                    z.write(full, rel)
        os.replace(tmp, target)
        print(f'{target}: {len(idx["files"])} files ({n} own added), {os.path.getsize(target)} bytes')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
