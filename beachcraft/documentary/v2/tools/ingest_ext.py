"""Clips filmed elsewhere (footage/bc3v2/n_*.mp4, r_*.mp4 from the NPC/raft session) -> the edit: moving clips on
60 fps (ffmpeg minterpolate) into $SP/doc4/shots/<name>.mp4, GUI stills ("still": true in .shot.json) as one frame
<name>.jpg. Aufruf: python3 -I ingest_ext.py <prefix>..."""
import json
import os
import shutil
import subprocess
import sys

SP = os.environ.get('SP') or '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
FOOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', 'footage', 'bc3v2'))
SHOTS = SP + '/doc4/shots'

for f in sorted(os.listdir(FOOT)):
    if not f.endswith('.mp4') or not f.startswith(tuple(sys.argv[1:])):
        continue
    n = f[:-4]
    j = os.path.join(FOOT, n + '.shot.json')
    meta = json.load(open(j)) if os.path.exists(j) else {}
    src = os.path.join(FOOT, f)
    if meta.get('still'):
        if not os.path.exists(f'{SHOTS}/{n}.jpg'):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '1', '-i', src, '-frames:v', '1', '-q:v', '2', f'{SHOTS}/{n}.jpg'], check=True)
            print('still', n, flush=True)
        continue
    if os.path.exists(f'{SHOTS}/{n}.mp4') and os.path.getmtime(f'{SHOTS}/{n}.mp4') > os.path.getmtime(src):
        continue
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', 'minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1',
                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p', f'{SHOTS}/{n}.mp4'], check=True)
    snd = os.path.join(FOOT, n + '.sounds.jsonl')
    if os.path.exists(snd):
        shutil.copy(snd, f'{SHOTS}/{n}.sounds.jsonl')
    meta['fps'] = 60
    json.dump(meta, open(f'{SHOTS}/{n}.shot.json', 'w'))
    print('clip', n, flush=True)
