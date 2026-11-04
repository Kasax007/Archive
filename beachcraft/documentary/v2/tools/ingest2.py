"""Ein Aufnahme-Lauf -> Archiv und Schnitt (v2).
Clips (Ordner mit f%05d.jpg, 30 fps Spielzeit): footage/bc3v2/<shot>.mp4 (CRF 18, 30 fps, die echten Bilder) mit
<shot>.sounds.jsonl/<shot>.shot.json; fuer den Schnitt $SP/doc4/shots/<shot>.mp4 auf 60 fps bewegungs-interpoliert
(ffmpeg minterpolate). Standbilder: $SP/doc4/shots/<name>.jpg, im Archiv als footage/bc3v2/stills_<lauf>.mp4 (ein Bild
je Standbild, Reihenfolge in stills_<lauf>.json). Die Bild-Ordner des Laufs werden danach geloescht (Platz).
Aufruf: python3 -I ingest2.py <lauf-ordner> [--keep]"""
import json
import os
import shutil
import subprocess
import sys

SP = os.environ.get('SP') or '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
FOOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', 'footage', 'bc3v2'))
SHOTS = SP + '/doc4/shots'


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main(rd, keep=False):
    os.makedirs(FOOT, exist_ok=True)
    os.makedirs(SHOTS, exist_ok=True)
    tag = os.path.basename(rd.rstrip('/'))
    stills = []
    for n in sorted(os.listdir(rd)):
        p = os.path.join(rd, n)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, 'f00000.jpg')):
            nf = len([f for f in os.listdir(p) if f.endswith('.jpg')])
            if nf < 8:
                continue
            run(['ffmpeg', '-y', '-framerate', '30', '-i', f'{p}/f%05d.jpg', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
                 '-pix_fmt', 'yuv420p', f'{FOOT}/{n}.mp4'])
            run(['ffmpeg', '-y', '-i', f'{FOOT}/{n}.mp4', '-vf',
                 'minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1', '-c:v', 'libx264', '-preset', 'fast',
                 '-crf', '17', '-pix_fmt', 'yuv420p', f'{SHOTS}/{n}.mp4'])
            for f, dst in (('sounds.jsonl', '.sounds.jsonl'), ('shot.json', '.shot.json')):
                if os.path.exists(os.path.join(p, f)):
                    shutil.copy(os.path.join(p, f), f'{FOOT}/{n}{dst}')
                    shutil.copy(os.path.join(p, f), f'{SHOTS}/{n}{dst}')
            j = f'{SHOTS}/{n}.shot.json'
            d = json.load(open(j)) if os.path.exists(j) else {}
            d['fps'] = 60
            json.dump(d, open(j, 'w'))
            print('clip', n, nf, 'frames', flush=True)
            if not keep:
                shutil.rmtree(p)
        elif n.endswith(('.jpg', '.png')) and not n.startswith('f0'):
            name = n[:-4]
            if n.endswith('.png'):
                from PIL import Image
                Image.open(p).convert('RGB').save(f'{SHOTS}/{name}.jpg', quality=95)
            else:
                shutil.copy(p, f'{SHOTS}/{name}.jpg')
            stills.append(name)
    if stills:
        lst = f'{SP}/doc4/stills_{tag}.txt'
        with open(lst, 'w') as f:
            for s in stills:
                f.write(f"file '{SHOTS}/{s}.jpg'\nduration 1\n")
        run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2,fps=1',
             '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', f'{FOOT}/stills_{tag}.mp4'])
        json.dump(stills, open(f'{FOOT}/stills_{tag}.json', 'w'), indent=1)
        print('stills', len(stills))


if __name__ == '__main__':
    main(sys.argv[1], '--keep' in sys.argv)
