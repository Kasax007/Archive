"""trim.py <frames-dir> <first> <last> [new-name]: keep frames first..last (inclusive), renumber from f00000; with
new-name the folder (and its shot.json / sounds.jsonl, times shifted) is renamed."""
import sys, os, glob, json
d, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
fs = sorted(glob.glob(os.path.join(d, 'f*.jpg')))
keep = fs[a:b + 1]
for f in fs:
    if f not in keep:
        os.remove(f)
for i, f in enumerate(keep):
    os.rename(f, os.path.join(d, f'tmp{i:05d}.jpg'))
for i in range(len(keep)):
    os.rename(os.path.join(d, f'tmp{i:05d}.jpg'), os.path.join(d, f'f{i:05d}.jpg'))
fps = 15.0
sj = os.path.join(d, 'shot.json')
if os.path.exists(sj):
    meta = json.load(open(sj))
    fps = float(meta.get('fps', 15))
    meta['frames'] = len(keep)
    json.dump(meta, open(sj, 'w'))
sl = os.path.join(d, 'sounds.jsonl')
if os.path.exists(sl):
    t0 = a / fps
    out = []
    for line in open(sl):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        e['t'] = round(e['t'] - t0, 4)
        if 0 <= e['t'] <= (b - a + 1) / fps:
            out.append(json.dumps(e))
    open(sl, 'w').write('\n'.join(out) + ('\n' if out else ''))
if len(sys.argv) > 4:
    nd = os.path.join(os.path.dirname(d.rstrip('/')), sys.argv[4])
    os.rename(d, nd)
    d = nd
print(d, len(keep), 'frames')
