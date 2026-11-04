"""Nach jedem Film-Lauf: Standbilder nach $SP/doc3/shots/<name>.jpg, Clips als MP4 (CRF 16) nach Archive/footage/bc3/
<name>.mp4 mit <name>.shot.json und <name>.sounds.jsonl (Ton-Protokoll); die Einzelbilder werden danach geloescht.
  python3 -I tools/ingest.py <lauf-ordner> [--keep-frames] [--only a,b]
  python3 -I tools/ingest.py --pack-stills       Standbilder je Kapitel als MP4 ins Archiv (footage/bc3/stills_<x>.mp4 + .json)
Namen mit sc_ oder t_ (Erkundung, Tests) werden uebersprungen."""
import os, sys, json, shutil, subprocess, glob

SP = os.environ.get('SP') or '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = SP + '/doc3/shots'
FOOTAGE = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'footage', 'bc3'))


def skip(name):
    return name.startswith(('sc_', 't_', 'x_'))


def encode(frames_dir, dst, fps):
    files = sorted(f for f in os.listdir(frames_dir) if f.startswith('f') and f.endswith(('.jpg', '.png')))
    if not files:
        return False
    ext = files[0][-4:]
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(fps), '-i', f'{frames_dir}/f%05d{ext}',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-threads', '2',
                    '-movflags', '+faststart', dst], check=True)
    return True


def ingest(run, keep=False, only=None):
    os.makedirs(SHOTS, exist_ok=True)
    os.makedirs(FOOTAGE, exist_ok=True)
    for name in sorted(os.listdir(run)):
        p = os.path.join(run, name)
        base = name.rsplit('.', 1)[0]
        if skip(base) or (only and base not in only):
            continue
        if os.path.isfile(p) and name.endswith(('.jpg', '.png')):
            shutil.copy(p, f'{SHOTS}/{base}.jpg' if name.endswith('.jpg') else f'{SHOTS}/{name}')
            print('still', base)
        elif os.path.isdir(p) and os.path.exists(f'{p}/shot.json'):
            fps = float(json.load(open(f'{p}/shot.json'))['fps'])
            if not encode(p, f'{FOOTAGE}/{name}.mp4', fps):
                print('empty clip', name)
                continue
            shutil.copy(f'{p}/shot.json', f'{FOOTAGE}/{name}.shot.json')
            if os.path.exists(f'{p}/sounds.jsonl'):
                shutil.copy(f'{p}/sounds.jsonl', f'{FOOTAGE}/{name}.sounds.jsonl')
            n = len([f for f in os.listdir(p) if f.startswith('f')])
            if os.path.isdir(f'{SHOTS}/{name}'):
                shutil.rmtree(f'{SHOTS}/{name}')
            if not keep:
                shutil.rmtree(p)
            print(f'clip {name}: {n} frames at {fps:g} fps -> {os.path.getsize(f"{FOOTAGE}/{name}.mp4") // 1024} KB')


def pack_stills():
    """All stills of one chapter (prefix before the first _) as one MP4, a frame per still, plus an index."""
    groups = {}
    for f in sorted(glob.glob(f'{SHOTS}/*.jpg')):
        n = os.path.basename(f)[:-4]
        groups.setdefault(n.split('_')[0], []).append(f)
    for g, files in groups.items():
        tmp = f'{SP}/doc3/pack_{g}'
        os.makedirs(tmp, exist_ok=True)
        for i, f in enumerate(files):
            shutil.copy(f, f'{tmp}/f{i:05d}.jpg')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '1', '-i', f'{tmp}/f%05d.jpg', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-g', '1',
                        f'{FOOTAGE}/stills_{g}.mp4'], check=True)
        json.dump([os.path.basename(f)[:-4] for f in files], open(f'{FOOTAGE}/stills_{g}.json', 'w'), indent=0)
        shutil.rmtree(tmp)
        print(f'stills_{g}: {len(files)} stills')


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--pack-stills' in a:
        pack_stills()
    else:
        only = set(a[a.index('--only') + 1].split(',')) if '--only' in a else None
        ingest(a[0], keep='--keep-frames' in a, only=only)
