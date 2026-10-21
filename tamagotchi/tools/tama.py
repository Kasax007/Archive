"""Schnitt, Ton und Render der beiden Tamagotchi-Videos (angepasst von longform/tools/longlib.py + showcase.py).
Die Stimme fuehrt, der Schnitt folgt ihr: Absaetze aus script.py -> Wortzeiten (Whisper) -> Untertitel, Shots je Absatz
(an Phrasen verankert) -> Ton (Stimme + Spiel-SFX geduckt + Musik) -> Render (mit/ohne Untertitel in einem Durchgang).

  $SP/video/tts/bin/python tools/tama.py short|long|all [--plan] [--audio] [--deliver]
                                        [--placeholder] [--fill-missing] [--film DIR] [--no-verify]
  --plan          nur Timing/Schnittplan ausgeben (kein Ton, kein Render)
  --audio         Stimme, SRT, Mixe und Pruefung, aber kein Video
  --deliver       fertige Dateien nach Archive/tamagotchi/short bzw. longform kopieren (zu grosse Dateien geteilt)
  --placeholder   Platzhalter-Footage ($SP/video/film_ph) statt des echten Materials ($SP/film/tama)
  --fill-missing  fehlende Shots durch Platzhalter ersetzen (nur zum Testen; verbietet --deliver)"""
import os, sys, json, math, subprocess, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cut, sfx, v3lib
from cut import Clip, Caption
from v3lib import _load, script_tokens, align, captions, write_wav, ts, SR, FPS, norm1
from script import SCRIPTS, POST
from check import missing

SP = cut.SP
VID = SP + '/video'
os.environ.setdefault('HF_HOME', VID + '/hf')
if os.path.isdir(VID + '/hf/hub'):
    os.environ.setdefault('HF_HUB_OFFLINE', '1')      # models are cached by tts_kokoro.py; no rate-limited hub calls
ARCH = os.path.abspath(os.path.join(HERE, '..'))
MUSIC_FILE = os.path.abspath(os.path.join(HERE, '..', '..', 'longform', 'music', 'Itty Bitty 8 Bit.mp3'))
REAL_FILM = SP + '/film/tama'
PH_FILM = VID + '/film_ph'
LEAD = 0.07                      # a cut lands this much before the word it belongs to

CFG = dict(
    short=dict(file='tamagotchi_short', dir='short', slow=1.06, lead_in=0.08, gap=0.26, gap_ch=0.26, tail=1.1,
               cap_size=84, cap_y=None, maxc=32, maxw=7, maxclip=2.6, crf=20, preset='slow', whoosh=0.07,
               fade_in=0.8, fade_out=2.0, hook_end=2.4),
    long=dict(file='tamagotchi_showcase', dir='longform', slow=1.06, lead_in=0.6, gap=0.5, gap_ch=0.9, tail=2.5,
              cap_size=68, cap_y=1390, maxc=42, maxw=9, maxclip=3.4, crf=26, preset='slow', whoosh=0.06,
              fade_in=1.5, fade_out=3.0, title_len=3.6),
)
END_CAP_Y = 1560

# Geraeusche je Shot: (Versatz ab Shot-Anfang in s, Ton aus dem Mod ('pfad unter sounds/') oder 'impact', Lautstaerke)
SHOT_SFX = {
    'hook_petting': [(0.15, 'pet/petting1', 0.5), (0.9, 'desert_dragon/happy2', 0.45)],
    'pyramid_wild': [(0.4, 'desert_dragon/ambient2', 0.4)],
    'jungle_wild': [(0.4, 'jungle_dragon/ambient1', 0.4)],
    'monument_wild': [(0.4, 'tide_dragon/ambient1', 0.4)],
    'igloo_penguin': [(0.3, 'frost_penguin/ambient1', 0.45)],
    'mimic_chamber': [(0.3, 'mimic/ambient1', 0.45)],
    'tame_heart': [(1.2, 'pet/tame1', 0.55), (1.2, 'talent/blessing1', 0.3)],
    'pet_screen': [(0.2, 'pager/open1', 0.5)],
    'bowl_eat': [(0.2, 'block/bowl_fill1', 0.4), (1.0, 'pet/eat1', 0.5)],
    'bath': [(0.4, 'pet/splash1', 0.5)],
    'bounce': [(0.5, 'block/bounce1', 0.5), (1.4, 'block/bounce2', 0.5)],
    'wheel': [(0.2, 'block/wheel1', 0.4)],
    'bed_sleep': [(0.4, 'pet/yawn1', 0.45), (1.6, 'pet/snore1', 0.4)],
    'laser_chase': [(0.2, 'toy/laser1', 0.5)],
    'petting_closeups': [(0.2, 'pet/petting2', 0.5), (1.2, 'pet/celebrate1', 0.4)],
    'backpack_on': [(0.6, 'backpack/equip1', 0.6)],
    'feed_owner': [(0.8, 'pet/feed_owner1', 0.6)],
    'roast': [(0.4, 'talent/roast1', 0.5)],
    'ore_glow': [(0.3, 'talent/sniff1', 0.5), (1.4, 'talent/ping1', 0.4)],
    'frost_steps': [(0.4, 'talent/freeze1', 0.5)],
    'lava_swim': [(0.4, 'ember_pup/happy1', 0.45)],
    'fly_follow': [(0.3, 'desert_dragon/happy1', 0.45)],
    'fight': [(0.4, 'desert_dragon/attack1', 0.5)],
    'faint_egg': [(0.3, 'pet/faint1', 0.5), (2.4, 'pet/wake1', 0.45)],
    'dance': [(0.3, 'pet/celebrate2', 0.45)],
    'campfire_warm': [(0.4, 'talent/warm1', 0.5)],
    'tamacon_book': [(0.3, 'pager/open2', 0.5)],
    'endcard': [(0.0, 'impact', 0.4), (0.15, 'pet/celebrate2', 0.5)],
}
ZOOMS = [(1.0, 1.05), (1.04, 1.08), (1.0, 1.04), (1.05, 1.08)]          # V3 rule: at most 1.08
SHOT_OPTS = {'hook_petting': dict(zoom=(1.04, 1.12), punch=True)}         # punch-zoom (<= 1.12) only on the hook highlight
FRAC = [0.0, 1.0, 0.5, 0.25, 0.75]                                         # where a re-used shot is entered


# ------------------------------------------------------------------ voice

def _wm():
    from faster_whisper import WhisperModel
    return WhisperModel('base.en', device='cpu', compute_type='int8', cpu_threads=3)


def voice(name, cfg):
    """-> wav, words per paragraph [(display, hot, t0, t1)], speech end, paragraph start times"""
    paras = SCRIPTS[name]
    VO = f'{VID}/vo/{name}'
    slow = cfg['slow']
    wm = None
    wav = [np.zeros(int(cfg['lead_in'] * SR), np.float32)]
    t = cfg['lead_in']
    pstart, wbp = [], []
    for pi, p in enumerate(paras):
        if pi > 0:
            g = cfg['gap_ch'] if p.get('ch') else cfg['gap']
            wav.append(np.zeros(int(g * SR), np.float32)); t += g
        pstart.append(t)
        src = f'{VO}/u{pi:03d}.wav'
        if not os.path.exists(src):
            raise SystemExit(f'voice missing: {src}  (run tools/tts_kokoro.py {name})')
        use = f'{VO}/u{pi:03d}.s{slow:.2f}.wav'
        if not os.path.exists(use) or os.path.getmtime(use) < os.path.getmtime(src):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-filter:a', f'atempo={slow}', use], check=True)
        a = _load(use)
        a = a / (np.abs(a).max() + 1e-6) * 0.85
        jf = use[:-4] + '.words.json'
        if os.path.exists(jf) and os.path.getmtime(jf) >= os.path.getmtime(use):
            ws = json.load(open(jf))
        else:
            wm = wm or _wm()
            segs, _ = wm.transcribe(use, language='en', word_timestamps=True)
            ws = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
            json.dump(ws, open(jf, 'w'))
        wav.append(a); t += len(a) / SR
        wbp.append(align(script_tokens(p['text']), ws, len(a) / SR, pstart[pi]))
    return np.concatenate(wav), wbp, t, pstart


# ------------------------------------------------------------------ plan (cut)

def _find(words, phrase, para):
    want = [norm1(x) for x in phrase.split()]
    toks = [norm1(w[0]) for w in words]
    for i in range(len(toks) - len(want) + 1):
        if toks[i:i + len(want)] == want:
            return i
    raise SystemExit(f'anchor {phrase!r} not found in paragraph {para}')


def shot_dir(name, shot, root, fill):
    if shot == 'endcard':
        return f'{VID}/cards/endcard_{name}'
    d = f'{root}/{shot}'
    if os.path.isdir(d) and cut._files(d):
        return d
    if fill and os.path.isdir(f'{PH_FILM}/{shot}'):
        return f'{PH_FILM}/{shot}'
    return None


def plan(name, cfg, words_by_para, pstart, total, root, fill):
    """-> [(Clip, start s, cues)], caption extras, caption y overrides, paragraph table, word cues"""
    paras = SCRIPTS[name]
    n_total = int(round(total * FPS))
    use, out, extra, capy, table, wcues, missing_dirs = {}, [], [], [], [], [], []
    gi = 0
    for pi, p in enumerate(paras):
        f0 = 0 if pi == 0 else int(round(max(0, pstart[pi] - LEAD) * FPS))
        f1 = n_total if pi + 1 == len(paras) else int(round(max(0, pstart[pi + 1] - LEAD) * FPS))
        wp = words_by_para[pi]
        segs = []
        for si, (shot, anchor) in enumerate(p['shots']):
            opt = shot.endswith('?')
            shot = shot.rstrip('?')
            d = shot_dir(name, shot, root, fill)
            if d is None:
                if opt:
                    continue
                missing_dirs.append(shot)
                continue
            if not segs:
                f = f0
            elif anchor:
                f = int(round(max(0, wp[_find(wp, anchor, p['id'])][2] - LEAD) * FPS))
            else:
                raise SystemExit(f'{p["id"]}: shot {shot} needs an anchor')
            if segs and f - segs[-1][1] < int(0.6 * FPS):         # too short: leave the previous shot on
                continue
            segs.append((shot, f, d))
        for i, (shot, f, d) in enumerate(segs):
            fe = segs[i + 1][1] if i + 1 < len(segs) else f1
            L = (fe - f) / FPS
            S = len(cut._files(d)) / FPS
            n = 1 if shot == 'endcard' else max(1, int(math.ceil(L / cfg['maxclip'] - 0.15)))
            fa = f
            for j in range(n):
                fb = fe if j == n - 1 else f + int(round((fe - f) * (j + 1) / n))
                l = (fb - fa) / FPS
                k = use.get(shot, 0)
                use[shot] = k + 1
                speed, hold, start = 1.0, 0.0, 0.0
                if S >= l + 0.05:
                    start = (S - l) * FRAC[k % len(FRAC)]
                else:
                    speed = max(0.7, S / l)
                    if S / l < 0.7:
                        hold = l - S / 0.7
                z = ZOOMS[gi % len(ZOOMS)]
                o = dict(zoom=z)
                if shot == 'endcard':
                    o = dict(zoom=(1.0, 1.04))
                if j == 0 and shot in SHOT_OPTS and k == 0:
                    o = dict(SHOT_OPTS[shot])
                o.pop('punch', None)
                if max(o['zoom']) > 1.12 + 1e-6 or (max(o['zoom']) > 1.08 + 1e-6 and shot not in SHOT_OPTS):
                    raise SystemExit('zoom rule broken for ' + shot)
                c = Clip(d, start, l, speed=speed, zoom=o['zoom'], hold_last=hold, label=shot)
                cues = [] if j else [(off, nm, g) for off, nm, g in SHOT_SFX.get(shot, [])]
                out.append((c, fa / FPS, cues))
                gi += 1
                fa = fb
        for phrase, nm, g in p.get('sfx', []):
            wcues.append((wp[_find(wp, phrase, p['id'])][2], nm, g))
        if p.get('ch'):
            extra.append(Caption(f0 / FPS, min(f1 / FPS, f0 / FPS + cfg.get('title_len', 3.6)), p['ch'], 'hook', y=300))
        if p.get('hook'):
            extra.append(Caption(f0 / FPS, min(f1 / FPS, cfg.get('hook_end', 2.4)), p['hook'], 'hook', y=330))
        if p.get('end'):
            capy.append((f0 / FPS, f1 / FPS, END_CAP_Y))
        table.append(dict(id=p['id'], start=f0 / FPS, end=f1 / FPS, speech=pstart[pi],
                          shots=[(s, f / FPS) for s, f, _ in segs]))
    if missing_dirs:
        raise SystemExit('missing footage in %s: %s\n(--placeholder / --fill-missing only for tests)' % (root, ', '.join(sorted(set(missing_dirs)))))
    return out, extra, capy, table, wcues


# ------------------------------------------------------------------ audio

def sound(nm):
    s = sfx.impact() if nm == 'impact' else sfx.mod(nm)
    n = int(2.6 * SR)
    if len(s) > n:                                            # long ambient calls: cut with a short fade
        s = s[:n].copy()
        s[-int(0.2 * SR):] *= np.linspace(1, 0, int(0.2 * SR))
    return s


def sfx_track(pl, wcues, total, whoosh):
    mix = sfx.Mix(total + 1)
    for clip, s, cues in pl:
        if s > 0:
            mix.add(s - 0.05, sfx.whoosh(0.18, seed=int(s * 10)), whoosh)
        for off, nm, g in cues:
            mix.add(s + off, sound(nm), g)
    for t, nm, g in wcues:
        mix.add(t, sound(nm), g)
    return mix


def movavg(x, n):
    """Moving average over n samples (centred) via cumulative sums - np.convolve with a long kernel takes minutes."""
    c = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)])
    h = n // 2
    idx = np.arange(len(x))
    lo, hi = np.clip(idx - h, 0, len(x)), np.clip(idx - h + n, 0, len(x))
    return ((c[hi] - c[lo]) / n).astype(np.float32)


def music_bed(total, voice_wav, fade_in, fade_out, under=0.115, gaps=0.34):
    """Itty Bitty 8 Bit (looped if needed), ducked under the voice (`under`), fuller in the pauses (`gaps`)."""
    n = int(total * SR)
    a = _load(MUSIC_FILE)
    a = a / (np.abs(a).max() + 1e-6)
    out = np.tile(a, int(math.ceil(n / len(a))))[:n].copy()
    fi, fo = int(fade_in * SR), int(fade_out * SR)
    out[:fi] *= np.linspace(0, 1, fi) ** 0.8
    out[-fo:] *= np.linspace(1, 0, fo)
    v = np.pad(voice_wav, (0, max(0, n - len(voice_wav))))[:n]
    env = movavg((np.abs(v) > 0.02).astype(np.float32), int(0.5 * SR))
    env = np.clip(env * 4, 0, 1)
    return out * (gaps + (under - gaps) * env)


def loudnorm(src, dst, target=-14):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', f'loudnorm=I={target}:TP=-1.5:LRA=11',
                    '-ar', str(SR), dst], check=True)


def verify(name, wav, tag, out):
    """Whisper (small.en) on the finished mix: share of script words recognised."""
    from faster_whisper import WhisperModel
    wm = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=3)
    segs, _ = wm.transcribe(wav, language='en')
    heard = ' '.join(s.text for s in segs)
    want = ' '.join(p['text'] for p in SCRIPTS[name])
    miss, n = missing(want, heard)
    pct = 100.0 * (n - len(miss)) / n
    print(f'  verify {tag}: {pct:.1f}% of {n} words recognised, missed: {miss}')
    json.dump(dict(percent=round(pct, 2), words=n, missed=miss, heard=heard), open(f'{out}/verify_{tag}.json', 'w'), indent=1)
    return pct


# ------------------------------------------------------------------ render (parallel, both versions at once)

def _render_part(args):
    from PIL import Image
    k, clips, f0, caps, extra, prefix, cfg = args
    W, H = cut.W, cut.H

    def enc(path):
        return subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                                 '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', cfg['preset'], '-crf', str(cfg['crf']),
                                 '-pix_fmt', 'yuv420p', '-threads', '1', path], stdin=subprocess.PIPE)
    pc, pk = enc(f'{prefix}_part{k:02d}_captions.mp4'), enc(f'{prefix}_part{k:02d}_clean.mp4')
    n = f0
    for clip in clips:
        for i in range(clip.frames):
            t = n / FPS
            f = i / max(1, clip.frames - 1)
            z = clip.zoom[0] + (clip.zoom[1] - clip.zoom[0]) * (f * f * (3 - 2 * f))
            im = cut._zoomed(cut.shot_frame(clip.shot, clip.source_index(i)), z, clip.focus).convert('RGBA')
            pk.stdin.write(im.convert('RGB').tobytes())
            cut._draw_captions(im, t, caps + extra)
            pc.stdin.write(im.convert('RGB').tobytes())
            n += 1
    for p in (pc, pk):
        p.stdin.close(); p.wait()
    return k


def render_parallel(clips, caps, extra, prefix, cfg, workers=4):
    import multiprocessing as mp
    total = sum(c.frames for c in clips)
    parts, cur, f0, start = [], [], 0, 0
    for c in clips:
        cur.append(c); f0 += c.frames
        if f0 - start >= total / workers and len(parts) < workers - 1:
            parts.append((cur, start)); cur, start = [], f0
    if cur:
        parts.append((cur, start))
    jobs = [(k, cl, st, caps, extra, prefix, cfg) for k, (cl, st) in enumerate(parts)]
    with mp.get_context('fork').Pool(len(jobs)) as pool:
        for k in pool.imap_unordered(_render_part, jobs):
            print('  part', k, 'done', flush=True)
    for vid in ('captions', 'clean'):
        lst = f'{prefix}_{vid}_parts.txt'
        with open(lst, 'w') as f:
            for k in range(len(jobs)):
                f.write(f"file '{prefix}_part{k:02d}_{vid}.mp4'\n")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy',
                        f'{prefix}_{vid}_video.mp4'], check=True)
        for k in range(len(jobs)):
            os.remove(f'{prefix}_part{k:02d}_{vid}.mp4')
        os.remove(lst)


def flicker_check(video, cut_times):
    """Frame differences of the clean video; reports spikes that are not at a cut (two takes mixed in one folder)."""
    W, H = 108, 192
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-vf', f'scale={W}:{H},format=gray', '-f', 'rawvideo', '-'],
                         check=True, capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    cuts = {int(round(t * FPS)) for t in cut_times}
    bad = []
    for i in range(2, len(d) - 2):
        if any(abs(i + 1 - c) <= 1 for c in cuts):
            continue
        base = np.median(d[max(0, i - 6):i + 7]) + 0.5
        if d[i] > 4 * base and d[i] > 6:
            bad.append(round((i + 1) / FPS, 2))
    print(f'  flicker check: {"no spikes" if not bad else "spikes at " + str(bad[:20])}')
    return bad


# ------------------------------------------------------------------ build

def build(name, plan_only=False, audio_only=False, root=REAL_FILM, fill=False, do_verify=True):
    cfg = CFG[name]
    OUT = f'{VID}/out/{name}'
    os.makedirs(OUT, exist_ok=True)
    wav, wbp, vend, pstart = voice(name, cfg)
    total = round((vend + cfg['tail']) * FPS) / FPS
    words = [w for wp in wbp for w in wp]
    v3lib.MAXC, v3lib.MAXW = cfg['maxc'], cfg['maxw']
    caps = []                                                    # per paragraph: chunks never cross a paragraph
    for pi, wp in enumerate(wbp):
        caps += captions(wp, pstart[pi + 1] if pi + 1 < len(wbp) else total, size=cfg['cap_size'], y=cfg['cap_y'])
    pl, extra, capy, table, wcues = plan(name, cfg, wbp, pstart, total, root, fill)
    for c in caps:
        for a, b2, y in capy:
            if a - 0.01 <= c.t0 < b2:
                c.y = y
    clips = [c for c, _, _ in pl]
    print(f'{name}: voice ends {vend:.1f} s, video {total:.1f} s, {len(clips)} clips, avg {total / len(clips):.2f} s/clip, '
          f'{len(words)} words, {len(caps)} captions')
    for t in table:
        print(f"  {t['id']:>3} {t['start']:6.1f}-{t['end']:6.1f} s ({t['end'] - t['start']:4.1f} s)  " +
              ', '.join(f'{s}@{f:.1f}' for s, f in t['shots']))
    json.dump(dict(total=total, voice_end=vend, paragraphs=table,
                   captions=[dict(t0=c.t0, t1=c.t1, text=c.text) for c in caps],
                   clips=[dict(shot=c.label, start=c.start, length=c.length, t=t, speed=c.speed, zoom=c.zoom) for c, t, _ in pl]),
              open(f'{OUT}/timeline.json', 'w'), indent=1)
    if plan_only:
        return OUT
    mix = sfx_track(pl, wcues, total, cfg['whoosh'])
    swav = f'{OUT}/sfx.wav'
    mix.write(swav, total)
    n = int(total * SR)
    v = np.pad(wav, (0, max(0, n - len(wav))))[:n]
    s = _load(swav)
    s = np.pad(s, (0, max(0, n - len(s))))[:n]
    env = movavg((np.abs(v) > 0.02).astype(np.float32), int(0.3 * SR))
    s = s * (1.0 - 0.75 * np.clip(env * 3, 0, 1))               # game sounds ducked under the voice
    write_wav(f'{OUT}/voice.wav', v)
    mb = music_bed(total, v, cfg['fade_in'], cfg['fade_out'])
    sp = np.abs(v) > 0.02
    print(f'  music vs voice during speech: {20 * np.log10(np.sqrt((mb[sp] ** 2).mean()) / np.sqrt((v[sp] ** 2).mean())):.1f} dB (target about -14)')
    for tag, bed in (('nomusic', None), ('music', mb)):
        m = v + s
        if bed is not None:
            m = m + bed
        m = m / max(1.0, np.abs(m).max() / 0.95)
        write_wav(f'{OUT}/{tag}0.wav', m)
        loudnorm(f'{OUT}/{tag}0.wav', f'{OUT}/{tag}.wav')
        os.remove(f'{OUT}/{tag}0.wav')
    with open(f'{OUT}/{cfg["file"]}.srt', 'w') as f:
        for k, c in enumerate(caps, 1):
            f.write(f'{k}\n{ts(c.t0)} --> {ts(c.t1)}\n{c.text.replace("*", "")}\n\n')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/voice.wav', '-c:a', 'aac', '-b:a', '160k',
                    f'{OUT}/{cfg["file"]}_voice.m4a'], check=True)
    write_post(name, OUT)
    if do_verify:
        for tag in ('music', 'nomusic'):
            verify(name, f'{OUT}/{tag}.wav', tag, OUT)
    if audio_only:
        return OUT
    render_parallel(clips, caps, extra, f'{OUT}/v', cfg, workers=int(os.environ.get('TAMA_WORKERS', '4')))
    for vid in ('captions', 'clean'):
        for tag in ('music', 'nomusic'):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/v_{vid}_video.mp4', '-i', f'{OUT}/{tag}.wav', '-c:v', 'copy',
                            '-af', 'volume=2dB,alimiter=limit=0.89', '-c:a', 'aac', '-b:a', '192k', '-shortest',
                            '-movflags', '+faststart', f'{OUT}/{cfg["file"]}_{vid}_{tag}.mp4'], check=True)
    flicker_check(f'{OUT}/v_clean_video.mp4', [t for _, t, _ in pl])
    every, cols = (2.0, 8) if name == 'short' else (4.0, 12)
    cut.contact_sheet(f'{OUT}/v_captions_video.mp4', f'{OUT}/sheet.png', every=every, cols=cols, thumb=150)
    for vid in ('captions', 'clean'):
        os.remove(f'{OUT}/v_{vid}_video.mp4')
    print('done', name, f'{total:.1f} s ->', OUT)
    return OUT


def write_post(name, out):
    cfg, p = CFG[name], POST[name]
    txt = f"""# TODO(user): the CurseForge slug 'tamagotchi' is an assumption - check the link before posting.
TITLE (suggestion)
{p['title']}

DESCRIPTION
{p['body']}
Tamagotchi is free on CurseForge: https://www.curseforge.com/minecraft/mc-mods/tamagotchi

Music by Kevin MacLeod (incompetech.com) - "Itty Bitty 8 Bit"
Licensed under Creative Commons: By Attribution 4.0 - http://creativecommons.org/licenses/by/4.0/

{p['tags']}
"""
    open(f'{out}/{cfg["file"]}_post.txt', 'w').write(txt)


def deliver(name):
    cfg = CFG[name]
    OUT = f'{VID}/out/{name}'
    dst = f'{ARCH}/{cfg["dir"]}'
    os.makedirs(dst, exist_ok=True)
    files = [f'{cfg["file"]}_{v}_{t}.mp4' for v in ('captions', 'clean') for t in ('music', 'nomusic')]
    files += [f'{cfg["file"]}.srt', f'{cfg["file"]}_voice.m4a', f'{cfg["file"]}_post.txt']
    for f in files:
        src = f'{OUT}/{f}'
        if not os.path.exists(src):
            raise SystemExit('missing output ' + src)
        if f.endswith('.mp4') and os.path.getsize(src) > 90 * 2 ** 20:            # GitHub: < 95 MB per file
            half = json.load(open(f'{OUT}/timeline.json'))['total'] / 2
            base = f[:-4]
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-c', 'copy', '-map', '0', '-f', 'segment',
                            '-segment_times', f'{half:.2f}', '-reset_timestamps', '1', '-segment_start_number', '1',
                            f'{dst}/{base}_part%d.mp4'], check=True)
            print('  split (too big):', f)
        else:
            shutil.copy(src, f'{dst}/{f}')
    shutil.copy(f'{OUT}/sheet.png', f'{dst}/{cfg["file"]}_contact_sheet.png')
    print('delivered', name, '->', dst)


if __name__ == '__main__':
    a = sys.argv[1:]
    flags = {x for x in a if x.startswith('--')}
    names = [x for x in a if x in ('short', 'long', 'all')]
    names = ['short', 'long'] if (not names or 'all' in names) else names
    root = REAL_FILM
    if '--film' in a:
        root = a[a.index('--film') + 1]
    if '--placeholder' in flags:
        root = PH_FILM
        if not os.path.isdir(PH_FILM):
            subprocess.run([sys.executable, HERE + '/placeholder.py'], check=True)
    fill = '--fill-missing' in flags or '--placeholder' in flags
    if fill and '--deliver' in flags:
        raise SystemExit('refusing to deliver placeholder footage')
    for nm in ('short', 'long'):
        if nm in names and not os.path.isdir(f'{VID}/cards/endcard_{nm}'):
            subprocess.run([sys.executable, HERE + '/endcard.py', nm], check=True)
    if '--fill-missing' in flags and not os.path.isdir(PH_FILM):
        subprocess.run([sys.executable, HERE + '/placeholder.py'], check=True)
    for nm in names:
        build(nm, plan_only='--plan' in flags, audio_only='--audio' in flags, root=root, fill=fill, do_verify='--no-verify' not in flags)
        if '--deliver' in flags and '--plan' not in flags and '--audio' not in flags:
            deliver(nm)
