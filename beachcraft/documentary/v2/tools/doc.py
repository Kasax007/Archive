"""Schnitt, Ton und Render der Beach-Craft-3.0-Doku (aufgebaut auf beachcraft/review/tools/bc.py).

Ruhiges Format: Die Stimme fuehrt (Absaetze aus script.py, Wortzeiten per Whisper), die Shots haengen an Phrasen.
  - Standbilder (still, 1350x2400) laufen mit langsamem Zoom/Schwenk (Ken Burns).
  - Clips (rec-Aufnahmen, 15-30 fps Spielzeit) werden auf 30 fps gebracht (Ueberblendung benachbarter Bilder),
    bei Bedarf leicht verlangsamt (bis 0,6x), danach das letzte Bild gehalten.
  - Zwischen den Shots weiche Ueberblendungen, an Kapitelanfaengen ueber Schwarz.
  - Ton: Stimme + die ECHTEN Spielgeraeusche jedes Clips (sounds.jsonl) + leise Musik (je Kapitel ein Stueck).
  - Render parallel, mit und ohne Untertitel im selben Durchgang.

  $SP/tts/bin/python tools/doc.py [--plan] [--audio] [--deliver] [--no-verify] [--limit SEK]
Quellen: $SP/doc3/shots/<name>.jpg (Standbild) oder $SP/doc3/shots/<name>/ (Clip: f*.jpg, shot.json, sounds.jsonl)
oder Archive/footage/bc3/<name>.mp4 (+ .shot.json, .sounds.jsonl)."""
import os, sys, json, math, subprocess, shutil, functools, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import v3lib
from v3lib import _load, script_tokens, align, write_wav, ts, SR, norm1
from script import SCRIPTS, POST
from check import missing

W, H, FPS = 1920, 1080, 60
SP = os.environ.get('SP') or '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad'
WORK = SP + '/doc4'
os.environ.setdefault('HF_HOME', SP + '/hf')
if os.path.isdir(SP + '/hf/hub'):
    os.environ.setdefault('HF_HUB_OFFLINE', '1')
ARCH = os.path.abspath(os.path.join(HERE, '..'))
FOOTAGE = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', 'footage', 'bc3v2'))
SHOTS = WORK + '/shots'
FONTS = os.environ.get('FONTS') or os.path.abspath(os.path.join(HERE, '..', '..', '..', 'fonts'))
CAP_FONT = FONTS + '/Inter-SemiBold.otf'
TITLE_FONT = FONTS + '/InterDisplay-Bold.otf'
MUSIC_DIR = os.environ.get('DOC_MUSIC') or (WORK + '/music')
MUSIC = {'manatees': ('Music for Manatees.mp3', 0.0), 'voyage': ('Living Voyage.mp3', 0.0), 'infinite': ('Infinite Perspective.mp3', 0.0),
         'jellyfish': ('Jellyfish in Space.mp3', 0.0), 'wholesome': ('Wholesome.mp3', 0.0),
         'journey': ('Enchanted Journey.mp3', 0.0), 'deep': ('Thunderbird.mp3', 0.0), 'hope': ('Eternal Hope.mp3', 0.0)}
CREDITS = {'manatees': 'Music for Manatees', 'voyage': 'Living Voyage', 'infinite': 'Infinite Perspective', 'jellyfish': 'Jellyfish in Space',
           'wholesome': 'Wholesome', 'journey': 'Enchanted Journey', 'deep': 'Thunderbird', 'hope': 'Eternal Hope'}
AQUA = (110, 222, 238)
WHITE = (255, 255, 255)
LEAD = 0.10                       # a cut lands this much before the word it belongs to
D = 0.6                           # cross-fade between shots (s)
DB = 1.0                          # fade through black at a chapter start (s)

CFG = dict(file='beachcraft3_documentary_v2', lead_in=1.2, gap=0.55, gap_ch=1.4, tail=3.0, slow=1.0,
           cap_size=50, cap_y=978, maxc=62, maxw=12, crf=24, preset='medium',
           fade_in=2.5, fade_out=4.0, title_len=4.0, game_gain=1.9, duck=0.5, music_under=0.075, music_gaps=0.2)

# per shot: still -> zoom (from, to), focus ((x0, y0), (x1, y1)) as 0..1 of the frame; gui -> fixed zoom on a menu
# clip -> speed (playback speed, 1 = real time), start (s into the clip), zoom, end (use the clip only up to here),
#         hold ([[a, b], ...]: show the frame at a instead of the frames from a to b, e.g. a camera jolt)
SHOT_OPTS = {}
GUI = {}                          # name -> (zoom, focus) for menu screenshots (GUI scale 3 is small in portrait)
CAPS_TOP = set()                  # shots with something to read where the subtitles are (the HUD air gauge)
DEFAULT_STILL = [((1.0, 1.07), ((0.5, 0.5), (0.5, 0.48))), ((1.07, 1.0), ((0.5, 0.52), (0.5, 0.5))),
                 ((1.0, 1.06), ((0.42, 0.5), (0.58, 0.5))), ((1.02, 1.08), ((0.58, 0.5), (0.45, 0.5)))]
MIN_SPEED = 0.6


def opts_file():
    p = os.path.join(HERE, 'shots.json')
    if os.path.exists(p):
        d = json.load(open(p))
        SHOT_OPTS.update(d.get('opts', {}))
        GUI.update({k: tuple(v) for k, v in d.get('gui', {}).items()})
        CAPS_TOP.update(d.get('caps_top', []))


opts_file()


# ------------------------------------------------------------------ sources

def find_source(name):
    """-> ('still', path) | ('clip', path, fps) | ('card', dir, fps) | None
    'a|b': a, or b while a is not there yet (placeholders for footage that is still being filmed elsewhere)"""
    if '|' in name:
        for alt in name.split('|'):
            s = find_source(alt)
            if s:
                return s
        return None
    if name == 'endcard':
        d = WORK + '/cards/endcard'
        return ('clip', d, 60.0) if os.path.isdir(d) else None
    for ext in ('.jpg', '.png'):
        if os.path.exists(f'{SHOTS}/{name}{ext}'):
            return ('still', f'{SHOTS}/{name}{ext}')
    m60 = f'{SHOTS}/{name}.mp4'                     # v2: clips interpolated to 60 fps by ingest2.py
    if os.path.exists(m60):
        return ('clip', m60, clip_fps(m60))
    d = f'{SHOTS}/{name}'
    if os.path.isdir(d) and any(f.startswith('f') for f in os.listdir(d)):
        return ('clip', d, clip_fps(d))
    m = f'{FOOTAGE}/{name}.mp4'
    if os.path.exists(m):
        return ('clip', m, clip_fps(m))
    return None


def clip_fps(src):
    j = src + '/shot.json' if os.path.isdir(src) else src[:-4] + '.shot.json'
    return float(json.load(open(j))['fps']) if os.path.exists(j) else 30.0


@functools.lru_cache(maxsize=None)
def clip_frames(src):
    if os.path.isdir(src):
        return len([f for f in os.listdir(src) if f.startswith('f') and f.endswith(('.jpg', '.png'))])
    out = subprocess.run(['ffmpeg', '-v', 'error', '-count_packets', '-i', src, '-map', '0:v:0', '-c', 'copy', '-f', 'null', '-'],
                         capture_output=True, text=True)
    r = subprocess.run(['ffmpeg', '-i', src], capture_output=True, text=True).stderr
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r)
    fps = clip_fps(src)
    return int(round((int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))) * fps)) if m else 0


class ClipReader:
    """Frames of a clip by source time (s); neighbouring frames are blended for the in-between times."""

    def __init__(self, src, fps):
        self.src, self.fps = src, fps
        self.n = clip_frames(src)
        self.proc = None
        self.pos = -1
        self.buf = {}
        if os.path.isdir(src):
            self.files = sorted(f for f in os.listdir(src) if f.startswith('f') and f.endswith(('.jpg', '.png')))

    def _get(self, i):
        i = max(0, min(self.n - 1, i))
        if i in self.buf:
            return self.buf[i]
        if os.path.isdir(self.src):
            im = np.asarray(Image.open(os.path.join(self.src, self.files[i])).convert('RGB').resize((W, H), Image.BICUBIC)
                            if Image.open(os.path.join(self.src, self.files[i])).size != (W, H)
                            else Image.open(os.path.join(self.src, self.files[i])).convert('RGB'))
        else:
            if self.proc is None or i <= self.pos - 1:
                self.close()
                self.proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', self.src, '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                                              '-vf', f'scale={W}:{H}', '-'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                self.pos = -1
            im = None
            while self.pos < i:
                raw = self.proc.stdout.read(W * H * 3)
                if len(raw) < W * H * 3:
                    im = self.buf.get(self.pos)
                    self.n = max(1, self.pos + 1)
                    break
                self.pos += 1
                im = np.frombuffer(raw, np.uint8).reshape(H, W, 3)
                self.buf[self.pos] = im
                for k in [k for k in self.buf if k < self.pos - 2]:
                    del self.buf[k]
            if im is None:
                im = self.buf[max(self.buf)]
        self.buf[i] = im
        for k in [k for k in self.buf if k < i - 2]:
            del self.buf[k]
        return im

    def at(self, t):
        x = max(0.0, t * self.fps)
        i = int(math.floor(x))
        f = x - i
        if i >= self.n - 1:
            return self._get(self.n - 1)
        a = self._get(i)
        if f < 0.04:
            return a
        b = self._get(i + 1)
        if f > 0.96:
            return b
        return (a.astype(np.float32) * (1 - f) + b.astype(np.float32) * f).astype(np.uint8)

    @property
    def length(self):
        return self.n / self.fps

    def close(self):
        if self.proc:
            self.proc.stdout.close()
            self.proc.kill()
            self.proc.wait()
            self.proc = None


LABELS = json.load(open(os.path.join(HERE, 'labels.json'))) if os.path.exists(os.path.join(HERE, 'labels.json')) else {}
LOOT = json.load(open(os.path.join(HERE, 'loot.json'))) if os.path.exists(os.path.join(HERE, 'loot.json')) else {}


@functools.lru_cache(maxsize=8)
def still_image(path):
    im = Image.open(path).convert('RGB')
    name = os.path.basename(path)[:-4]
    if name in LABELS:                       # the exhibition: item names under the items (positions from museum.py)
        im = im.convert('RGBA')
        for e in LABELS[name]:
            lab = label_image(e['text'], int(round(30 * im.width / W)), int(0.215 * im.width))
            im.alpha_composite(lab, (int(e['x'] * im.width - lab.width / 2), int(e['y'] * im.height - lab.height * 0.32)))
        im = im.convert('RGB')
    return im


@functools.lru_cache(maxsize=512)
def label_image(text, size, max_w):
    font = ImageFont.truetype(CAP_FONT, size)
    d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    lines, line = [], ''
    for w in text.split():
        t = (line + ' ' + w).strip()
        if line and d0.textlength(t, font=font) > max_w:
            lines.append(line)
            line = w
        else:
            line = t
    lines.append(line)
    asc, desc = font.getmetrics()
    lh = int((asc + desc) * 1.05)
    img = Image.new('RGBA', (max_w + 40, lh * len(lines) + 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for k, ln in enumerate(lines):
        x = (img.width - d.textlength(ln, font=font)) / 2
        d.text((x, 10 + k * lh), ln, font=font, fill=WHITE, stroke_width=max(3, size // 9), stroke_fill=(10, 28, 40))
    return img


def kenburns(path, f, zoom, focus):
    """The still at progress f (0..1): zoom from zoom[0] to zoom[1], centre moving from focus[0] to focus[1]."""
    im = still_image(path)
    sw, sh = im.size
    z = zoom[0] + (zoom[1] - zoom[0]) * f
    fx = focus[0][0] + (focus[1][0] - focus[0][0]) * f
    fy = focus[0][1] + (focus[1][1] - focus[0][1]) * f
    # the source is larger than the output (still 1.25x): zoom 1.0 shows the whole source
    cw, ch = sw / z, sh / z
    left = min(max(0.0, fx * sw - cw / 2), sw - cw)
    top = min(max(0.0, fy * sh - ch / 2), sh - ch)
    return np.asarray(im.resize((W, H), Image.BICUBIC, box=(left, top, left + cw, top + ch)))


def zoomed(arr, z, focus):
    if z <= 1.0005:
        return arr
    im = Image.fromarray(arr)
    cw, ch = W / z, H / z
    left = min(max(0.0, focus[0] * W - cw / 2), W - cw)
    top = min(max(0.0, focus[1] * H - ch / 2), H - ch)
    return np.asarray(im.resize((W, H), Image.BICUBIC, box=(left, top, left + cw, top + ch)))


# ------------------------------------------------------------------ captions (calm style: fade, no pop)

@functools.lru_cache(maxsize=128)
def loot_image(text, size):
    """'In the chest' panel: the item names, centred, on a dark rounded panel"""
    font = ImageFont.truetype(CAP_FONT, size)
    head = ImageFont.truetype(TITLE_FONT, int(size * 0.8))
    items = text.split('|')
    d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    max_w = W - 160
    lines, line = [], ''
    for it in items:
        t = (line + '  ·  ' + it) if line else it
        if line and d0.textlength(t, font=font) > max_w:
            lines.append(line)
            line = it
        else:
            line = t
    lines.append(line)
    asc, desc = font.getmetrics()
    lh = int((asc + desc) * 1.15)
    hh = int(size * 1.25)
    w = int(max(d0.textlength(l, font=font) for l in lines)) + 80
    w = max(w, 420)
    h = hh + lh * len(lines) + 40
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 26, fill=(6, 24, 38, 205), outline=(110, 222, 238, 160), width=3)
    title = 'IN THE CHEST'
    d.text(((w - d.textlength(title, font=head)) / 2, 16), title, font=head, fill=AQUA)
    for k, ln in enumerate(lines):
        d.text(((w - d.textlength(ln, font=font)) / 2, 14 + hh + k * lh), ln, font=font, fill=WHITE)
    return img


@functools.lru_cache(maxsize=512)
def caption_image(text, kind, size):
    if kind == 'loot':
        return loot_image(text, size)
    if kind == 'title':
        font = ImageFont.truetype(TITLE_FONT, size)
        stroke, track = 6, 6
    else:
        font = ImageFont.truetype(CAP_FONT, size)
        stroke, track = 5, 0
    words, inside = [], False
    for raw in text.split(' '):
        hot = inside or '*' in raw
        if raw.count('*') % 2:
            inside = not inside
        words.append((raw.replace('*', ''), hot))
    d0 = ImageDraw.Draw(Image.new('RGBA', (10, 10)))

    def tw(s):
        return d0.textlength(s, font=font) + track * max(0, len(s) - 1)

    max_w = W - 150
    lines, line = [], []
    for w in words:
        if line and tw(' '.join(x for x, _ in line + [w])) > max_w:
            lines.append(line)
            line = [w]
        else:
            line.append(w)
    if line:
        lines.append(line)
    asc, desc = font.getmetrics()
    lh = int((asc + desc) * 1.12)
    img = Image.new('RGBA', (W, lh * len(lines) + 2 * stroke + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = stroke + 8
    space = d.textlength(' ', font=font) + track
    for ln in lines:
        x = (W - tw(' '.join(w for w, _ in ln))) / 2
        for w, hot in ln:
            for ch_ in (w if track else [w]):
                d.text((x, y), ch_, font=font, fill=AQUA if hot else WHITE, stroke_width=stroke, stroke_fill=(8, 22, 34))
                x += d.textlength(ch_, font=font) + track
            if not track:
                pass
            x += space - (track if track else 0)
        y += lh
    shadow = img.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda a: int(a * 0.5))
    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    out.paste((0, 0, 0, 255), (0, 5), shadow)
    out.alpha_composite(img)
    return out


class Cap:
    def __init__(self, t0, t1, text, kind='cap', y=None, size=None):
        self.t0, self.t1, self.text, self.kind, self.y, self.size = t0, t1, text, kind, y, size


def draw_caps(frame, t, caps):
    for c in caps:
        if not (c.t0 <= t < c.t1):
            continue
        img = caption_image(c.text, c.kind, c.size or (94 if c.kind == 'title' else 34 if c.kind == 'loot' else CFG['cap_size']))
        fade = 0.35 if c.kind == 'title' else 0.12
        a = min(1.0, (t - c.t0) / fade, (c.t1 - t) / fade)
        if a < 0.999:
            img = img.copy()
            img.putalpha(img.split()[3].point(lambda v: int(v * a)))
        y = c.y if c.y is not None else CFG['cap_y']
        frame.alpha_composite(img, ((W - img.width) // 2, int(y - img.height / 2)))


# ------------------------------------------------------------------ voice

def _wm():
    from faster_whisper import WhisperModel
    return WhisperModel('base.en', device='cpu', compute_type='int8', cpu_threads=3)


def voice(name, cfg):
    paras = SCRIPTS[name]
    VO = f'{WORK}/vo/{name}'
    slow = cfg['slow']
    wm = None
    wav = [np.zeros(int(cfg['lead_in'] * SR), np.float32)]
    t = cfg['lead_in']
    pstart, wbp = [], []
    for pi, p in enumerate(paras):
        if pi > 0:
            g = (cfg['gap_ch'] if p.get('ch') else cfg['gap']) + paras[pi - 1].get('pause', 0)
            wav.append(np.zeros(int(g * SR), np.float32))
            t += g
        pstart.append(t)
        src = f'{VO}/u{pi:03d}.wav'
        if not os.path.exists(src):
            raise SystemExit(f'voice missing: {src}  (run tools/tts_kokoro.py {name})')
        use = src
        if abs(slow - 1.0) > 1e-3:
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
        wav.append(a)
        t += len(a) / SR
        wbp.append(align(script_tokens(p['text']), ws, len(a) / SR, pstart[pi]))
    return np.concatenate(wav), wbp, t, pstart


# ------------------------------------------------------------------ plan

class Shot:
    def __init__(self, name, src, t0, t1, chapter=False):
        self.name, self.src, self.t0, self.t1, self.chapter = name, src, t0, t1, chapter
        self.kind = src[0]
        self.opts = dict(SHOT_OPTS.get(name, {}))

    def setup(self, k):
        L = self.t1 - self.t0 + D
        self.span = L
        key = next((a for a in self.name.split('|') if find_source(a)), self.name)    # placeholder names a|b
        if self.kind == 'still':
            gui = key in GUI or (still_image(self.src[1]).size == (W, H) and 'zoom' not in self.opts)
            if gui:
                z, fc = GUI.get(key, (1.75, (0.5, 0.45)))
                self.zoom, self.focus = (z, z * 1.02), (tuple(fc), tuple(fc))
            elif self.name in LABELS:
                self.zoom, self.focus = (1.0, 1.025), ((0.5, 0.5), (0.5, 0.5))
            else:
                z, fc = DEFAULT_STILL[k % len(DEFAULT_STILL)]
                self.zoom = tuple(self.opts.get('zoom', z))
                self.focus = tuple(tuple(x) for x in self.opts.get('focus', fc))
        else:
            n = clip_frames(self.src[1])
            S = n / self.src[2]
            if 'end' in self.opts:                              # use the clip only up to here (s)
                S = min(S, float(self.opts['end']))
            self.clip_len = S
            start = float(self.opts.get('start', 0.0))
            avail = max(0.05, S - start)
            if 'speed' in self.opts:
                self.speed = float(self.opts['speed'])
            else:
                self.speed = 1.0 if avail >= L else max(MIN_SPEED, avail / L)
            if avail > L * self.speed and 'start' not in self.opts and self.name != 'endcard':
                start = min(S - L * self.speed, float(self.opts.get('center', 0.0)) * (S - L * self.speed))
            self.start = start
            self.zoom = tuple(self.opts.get('zoom', (1.0, 1.0) if self.name == 'endcard' else (1.0, 1.035)))
            self.focus = tuple(self.opts.get('focus', (0.5, 0.5)))

    def info(self):
        if self.kind == 'still':
            return f'{self.name}: still {self.t1 - self.t0:.1f}s zoom {self.zoom}'
        hold = max(0.0, self.span - (self.clip_len - self.start) / self.speed)
        return f'{self.name}: clip {self.t1 - self.t0:.1f}s of {self.clip_len:.1f}s from {self.start:.1f}s x{self.speed:.2f}' + (f' hold {hold:.1f}s' if hold > 0.05 else '')


def _find(words, phrase, para):
    want = [norm1(x) for x in phrase.split()]
    toks = [norm1(w[0]) for w in words]
    for i in range(len(toks) - len(want) + 1):
        if toks[i:i + len(want)] == want:
            return i
    raise SystemExit(f'anchor {phrase!r} not found in paragraph {para}')


def plan(name, words_by_para, pstart, total, allow_missing=False):
    paras = SCRIPTS[name]
    shots, titles, table, missing_ = [], [], [], []
    for pi, p in enumerate(paras):
        t_start = 0.0 if pi == 0 else max(0.0, pstart[pi] - LEAD - (0.5 if p.get('ch') else 0.0))
        t_end = total if pi + 1 == len(paras) else max(0.0, pstart[pi + 1] - LEAD - (0.5 if paras[pi + 1].get('ch') else 0.0))
        wp = words_by_para[pi]
        segs = []
        for shot, anchor in p['shots']:
            opt = shot.endswith('?')
            shot = shot.rstrip('?')
            src = find_source(shot)
            if src is None:
                if not opt:
                    missing_.append(shot)
                continue
            if segs and anchor and anchor.startswith('@'):            # '@<s>': seconds after the paragraph start
                t = t_start + float(anchor[1:])
            else:
                t = t_start if not segs else max(0.0, wp[_find(wp, anchor, p['id'])][2] - LEAD) if anchor else None
            if t is None:
                raise SystemExit(f'{p["id"]}: shot {shot} needs an anchor')
            if segs and t - segs[-1][1] < 1.2:
                continue
            segs.append((shot, t, src))
        for i, (shot, t, src) in enumerate(segs):
            te = segs[i + 1][1] if i + 1 < len(segs) else t_end
            shots.append(Shot(shot, src, t, te, chapter=(i == 0 and bool(p.get('ch')))))
        if p.get('ch'):
            titles.append(Cap(t_start + 0.6, min(t_end, t_start + 0.6 + CFG['title_len']), p['ch'], 'title', y=250))
        table.append(dict(id=p['id'], start=t_start, end=t_end, speech=pstart[pi], shots=[(s, round(t, 2)) for s, t, _ in segs]))
    for sh in shots:
        if sh.name in LOOT and LOOT[sh.name]:
            titles.append(Cap(sh.t0 + 0.4, sh.t1 - 0.1, '|'.join(LOOT[sh.name]), 'loot', y=1335))
    if missing_ and not allow_missing:
        raise SystemExit('missing footage: ' + ', '.join(missing_))
    for k, s in enumerate(shots):
        s.setup(k)
    return shots, titles, table, missing_


# ------------------------------------------------------------------ frames

class Renderer:
    def __init__(self, shots):
        self.shots = shots
        self.readers = {}

    def reader(self, s):
        if s.name not in self.readers:
            self.readers[s.name] = ClipReader(s.src[1], s.src[2])
        return self.readers[s.name]

    def shot_frame(self, s, tl):
        """Frame of shot s at its local time tl (0 = D/2 before its nominal start)."""
        f = min(1.0, max(0.0, tl / max(0.01, s.span)))
        if s.kind == 'still':
            return kenburns(s.src[1], f, s.zoom, s.focus)
        r = self.reader(s)
        ct = s.start + tl * s.speed
        if 'end' in s.opts:
            ct = min(ct, s.clip_len)
        for a, b in s.opts.get('hold', []):                       # bad frames (camera jolt, a gull on the lens)
            if a <= ct < b:
                ct = a
                break
        arr = r.at(ct)
        z = s.zoom[0] + (s.zoom[1] - s.zoom[0]) * f
        return zoomed(arr, z, s.focus)

    def frame(self, t):
        sh = self.shots
        i = 0
        lo, hi = 0, len(sh) - 1
        while lo <= hi:                                           # last shot with t0 <= t
            m = (lo + hi) // 2
            if sh[m].t0 <= t:
                i = m
                lo = m + 1
            else:
                hi = m - 1
        s = sh[i]
        a = self.shot_frame(s, t - s.t0 + D / 2)
        if i + 1 < len(sh) and t >= sh[i + 1].t0 - (DB if sh[i + 1].chapter else D) / 2:
            n = sh[i + 1]
            if n.chapter:                                         # through black
                x = (t - (n.t0 - DB / 2)) / DB
                a = (a.astype(np.float32) * max(0.0, 1 - 2 * x)).astype(np.uint8)
            else:
                x = (t - (n.t0 - D / 2)) / D
                b = self.shot_frame(n, t - n.t0 + D / 2)
                a = (a.astype(np.float32) * (1 - x) + b.astype(np.float32) * x).astype(np.uint8)
        elif s.chapter and t < s.t0 + DB / 2:
            x = (t - (s.t0 - DB / 2)) / DB
            a = (a.astype(np.float32) * max(0.0, min(1.0, 2 * x - 1))).astype(np.uint8)
        return a

    def close(self):
        for r in self.readers.values():
            r.close()
        self.readers = {}


def _render_part(args):
    k, f0, f1, shots, caps, prefix, total = args
    r = Renderer(shots)

    def enc(path):
        return subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                                 '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', CFG['preset'], '-crf', str(CFG['crf']),
                                 '-pix_fmt', 'yuv420p', '-threads', '2', path], stdin=subprocess.PIPE)
    pc = enc(f'{prefix}_part{k:02d}_captions.mp4')            # only the version with captions (user decision)
    fade_in, fade_out = CFG['fade_in'] * 0.5, CFG['fade_out'] * 0.5
    subs = [c for c in caps if c.kind == 'cap']
    overlays = [c for c in caps if c.kind != 'cap']           # chapter titles and loot panels: in both versions
    for n in range(f0, f1):
        t = n / FPS
        arr = r.frame(t)
        if t < fade_in:
            arr = (arr.astype(np.float32) * (t / fade_in)).astype(np.uint8)
        im = Image.fromarray(arr).convert('RGBA')
        draw_caps(im, t, overlays)
        draw_caps(im, t, subs)
        pc.stdin.write(im.convert('RGB').tobytes())
    r.close()
    pc.stdin.close()
    pc.wait()
    return k


def render_parallel(shots, caps, prefix, total, workers=4):
    """DOC_PARTS (default 12) parts of equal length, rendered by `workers` processes (a fresh one per part). The part
    files stay: with DOC_ONLY=3,4 only those parts are rendered again (e.g. after new footage arrived for them), the
    others are reused; then all are joined."""
    import multiprocessing as mp
    import time as _time
    nparts = int(os.environ.get('DOC_PARTS', '12'))
    only = {int(x) for x in os.environ.get('DOC_ONLY', '').split(',') if x.strip()}
    nf = int(round(total * FPS))
    bounds = [int(round(nf * i / nparts)) for i in range(nparts + 1)]
    keep = int(os.environ.get('DOC_KEEP_BOUNDS', '0'))     # the first parts end where they ended last time
    if keep and os.path.exists(f'{prefix}_parts.json'):
        old = [int(round(b * FPS)) for b in json.load(open(f'{prefix}_parts.json'))['bounds_s']]
        rest = nparts - keep
        bounds = old[:keep + 1] + [int(round(old[keep] + (nf - old[keep]) * i / rest)) for i in range(1, rest + 1)]
    todo = [k for k in range(nparts) if (k in only if only else True)
            or not os.path.exists(f'{prefix}_part{k:02d}_captions.mp4')]
    jobs = [(k, bounds[k], bounds[k + 1], shots, caps, prefix, total) for k in todo]
    json.dump({'parts': nparts, 'bounds_s': [b / FPS for b in bounds]}, open(f'{prefix}_parts.json', 'w'))
    t0 = _time.time()
    with mp.get_context('fork').Pool(workers, maxtasksperchild=1) as pool:
        for k in pool.imap_unordered(_render_part, jobs):
            print(f'  part {k} done ({bounds[k] / FPS:.0f}-{bounds[k + 1] / FPS:.0f} s) after {_time.time() - t0:.0f} s', flush=True)
    for vid in ('captions',):
        lst = f'{prefix}_{vid}_parts.txt'
        with open(lst, 'w') as f:
            for k in range(nparts):
                f.write(f"file '{prefix}_part{k:02d}_{vid}.mp4'\n")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy',
                        f'{prefix}_{vid}_video.mp4'], check=True)
        os.remove(lst)


# ------------------------------------------------------------------ audio

MC_INDEX = '/root/.gradle/caches/fabric-loom/assets/indexes/26.3-34.json'
MC_OBJECTS = '/root/.gradle/caches/fabric-loom/assets/objects'
import glob as _glob
MOD = os.environ.get('DOC_MOD') or '/home/user/Kasax_Raft_Mod'     # DOC_MOD: a worktree with sounds not merged yet
MOD_ASSET_DIRS = [MOD + '/src/main/resources/assets'] + sorted(_glob.glob(MOD + '/src/main/modules/*/assets'))


def _sound_defs():
    """raft sound events -> files as defined by the mod now (3.1 gave many creatures new sounds): older clips logged
    the files of 3.0, so the mix plays what the game plays today. A name keeps its namespace: many raft events play
    vanilla files ('minecraft:entity/fish/flop1' is minecraft:sounds/entity/fish/flop1.ogg); until 6.11. they were all
    looked up under raft: and stayed silent (gull flaps and pecks, tideling flops, penguins, otters, ...).
    Also -> the attenuation distance of each event (sounds.json, default 16)."""
    files, att = {}, {}
    for base in MOD_ASSET_DIRS:
        f = f'{base}/raft/sounds.json'
        if os.path.exists(f):
            for k, d in json.load(open(f)).items():
                fl, at = [], None
                for s in d.get('sounds', []):
                    if isinstance(s, dict) and s.get('type') == 'event':
                        continue                                  # a reference to another event, not a file
                    n = s if isinstance(s, str) else s.get('name')
                    if not n:
                        continue
                    ns, p = n.split(':', 1) if ':' in n else ('minecraft', n)
                    fl.append(f'{ns}:sounds/{p}.ogg')
                    if at is None and isinstance(s, dict):
                        at = s.get('attenuation_distance')
                if fl:
                    files['raft:' + k] = fl
                    att['raft:' + k] = float(at or 16)
    return files, att


EVENT_FILES, EVENT_ATT = _sound_defs()
SKIP_SOURCES = {'music', 'ambient', 'weather', 'record'}
# The sound logs count game seconds, the clips run faster: the harness's screenshot lets two ticks pass per frame, so
# 30 frames (one second of clip) show 3 s of game time (74 clips: last logged sound at 2.96 x the clip length, bites
# and harpoon shots on the frames where they happen). Before 6.11. the logs were read as clip time: every sound came
# 3x too late and most fell after the end of their shot.
GAME_PER_CLIP = float(os.environ.get('DOC_GAME_PER_CLIP', '3.0'))
_index, _scache = None, {}

# Per clip, after the feedback of 6.11. (clip = file name of the clip): THIN keeps an event only this many seconds of
# clip time after the last one kept that can be heard (one tideling clip logs 67 flops in a few seconds); SOUND_GAIN
# changes an event in clips whose name starts with the prefix by so many dB, None leaves it out of the mix.
THIN = {'raft:entity.tideling.flop': 0.7, 'raft:entity.tideling.bite': 0.3,
        # clips run 3x faster than the game, so a flock or a swimmer logs three times as many sounds per second
        'raft:entity.seagull.flap': 0.12, 'raft:entity.seagull.peck': 0.1, 'raft:entity.seagull.ambient': 0.25,
        'minecraft:entity.parrot.step': 0.15, 'minecraft:entity.player.swim': 0.2, 'minecraft:entity.dolphin.swim': 0.2}
SOUND_GAIN = [('s_lev', 'minecraft:entity.hostile.swim', -8.0),        # the Leviathan's generic swim splashes
              ('c_manta', 'minecraft:entity.guardian.hurt', None),      # old take: two mantas stuck in the reef
              ('c_manta', 'minecraft:entity.guardian.death', None),
              ('c_crab_dig', 'raft:entity.crab.hurt', None)]             # retake 6.11.: the crabs are run into
# The raft motor: now a loop ('run', 2 s; in a film log the client renews it about every 5 s, each at volume 0.001)
# and a 'start' when it starts; before 6.11. a bass drum every 4-6 ticks (old clips). Both become the loop, once per
# shot: gain x distance factor, pitch by the raft's speed (not by the playback speed), faded at both ends.
# under the voice the game sounds go down by CFG['duck'], in these shots by more: with the Leviathan's sounds in
# sync (6.11.) Whisper missed a dozen words of the fight
DUCK_MORE = (('s_lev', 's_wake'), 0.75)
MOTOR_RUN, MOTOR_START = 'raft:block.raft_motor.run', 'raft:block.raft_motor.start'
MOTOR_TICK = 'minecraft:block.note_block.basedrum'
MOTOR = dict(gain=0.7, pitch=1.05, fast_pitch=1.15, fast_bps=8.0, gap=6.0, renew=5.5, tick_gap=1.5, tail=0.5,
             fade=0.25, start_gain=0.8, started_after=0.35)


def sound_path(file_id):
    global _index
    ns, path = file_id.split(':', 1)
    if ns == 'minecraft':
        if _index is None:
            _index = json.load(open(MC_INDEX))['objects']
        ent = _index.get('minecraft/' + path)
        return f'{MC_OBJECTS}/{ent["hash"][:2]}/{ent["hash"]}' if ent else None
    for base in MOD_ASSET_DIRS:
        if os.path.exists(f'{base}/{ns}/{path}'):
            return f'{base}/{ns}/{path}'
    return None


def sound_file(file_id):
    if file_id not in _scache:
        src = sound_path(file_id)
        _scache[file_id] = _load(src) if src else None
    return _scache[file_id]


@functools.lru_cache(maxsize=4)
def loop_file(file_id, seconds=40):
    """A seamless loop decoded as one long stream (resampled across the joins: no click every 2 s)."""
    src = sound_path(file_id)
    if not src:
        return None
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-stream_loop', '-1', '-i', src, '-t', str(seconds), '-f', 'f32le',
                          '-ac', '1', '-ar', str(SR), '-'], check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def event_gain(e):
    """volume x linear attenuation from the camera, as the game hears it"""
    g = min(1.0, max(0.0, e['volume'])) * e.get('gain', 1.0)
    if e['attenuation'] == 'LINEAR' and not e['relative']:
        dd = math.dist((e['x'], e['y'], e['z']), (e['cam_x'], e['cam_y'], e['cam_z']))
        g *= max(0.0, 1.0 - dd / max(1.0, e['distance']))
    return g


def clip_sounds(src):
    f = src + '/sounds.jsonl' if os.path.isdir(src) else src[:-4] + '.sounds.jsonl'
    if not os.path.exists(f):
        return []
    clip = os.path.basename(src.rstrip('/'))
    clip = clip if os.path.isdir(src) else clip[:-4]
    out, last = [], {}
    for e in (json.loads(l) for l in open(f) if l.strip()):
        if e['source'] in SKIP_SOURCES:
            continue
        e['tg'] = e['t']                                   # game time of the log
        e['t'] = e['t'] / GAME_PER_CLIP                    # clip time
        ev = e.get('event')
        db, drop = 0.0, False
        for pre, name, d in SOUND_GAIN:
            if ev == name and clip.startswith(pre):
                if d is None:
                    drop = True
                else:
                    db += d
        if drop:
            continue
        if db:
            e['gain'] = 10 ** (db / 20)
        if ev in THIN and event_gain(e) >= 0.01:
            if ev in last and e['t'] - last[ev] < THIN[ev]:
                continue
            last[ev] = e['t']
        files = EVENT_FILES.get(ev)
        if files and e.get('file') not in files:
            e['file'] = files[int(e['t'] * 1000) % len(files)]
        out.append(e)
    return out


def is_motor(e):
    return e['event'] == MOTOR_RUN or (e['event'] == MOTOR_TICK and e['source'] == 'neutral')


def motor_spans(events):
    """The raft motor of a clip as loop spans in clip time: dict(a, b, pts=[(t, distance factor)], fast, start).
    New clips: from the first 'run' event on; a span ends only when no 'run' comes for MOTOR['gap'] s (the client
    renews the loop about every 5 s), b is then the last + gap. Without a 'start' just before it the motor was already
    running: the span starts with the clip. Old clips: the bass drum ticks, from the first to the last + tail; a start
    sound if the ticks begin later than one tick into the recording (the motor started in the shot). The MOTOR times
    are game seconds (as the log counts them)."""
    att = EVENT_ATT.get(MOTOR_RUN, 32.0)
    k = GAME_PER_CLIP
    starts = [e['tg'] for e in events if e['event'] == MOTOR_START]
    spans = []
    for kind in ('run', 'tick'):
        ev = [e for e in events if is_motor(e) and (e['event'] == MOTOR_RUN) == (kind == 'run')]
        gap = MOTOR['gap'] if kind == 'run' else MOTOR['tick_gap']
        groups = []
        for e in ev:
            if groups and e['tg'] - groups[-1][-1]['tg'] <= gap:
                groups[-1].append(e)
            else:
                groups.append([e])
        for g in groups:
            pts = [(e['t'], max(0.0, 1.0 - math.dist((e['x'], e['y'], e['z']), (e['cam_x'], e['cam_y'], e['cam_z'])) / att))
                   for e in g]
            way = sum(math.dist((p['x'], p['z']), (q['x'], q['z'])) for p, q in zip(g, g[1:]))
            fast = len(g) > 1 and way / max(1e-3, g[-1]['tg'] - g[0]['tg']) > MOTOR['fast_bps']
            a = g[0]['tg']
            if kind == 'run':
                if a <= MOTOR['renew'] and not any(abs(t - a) <= 0.5 for t in starts):
                    a = 0.0
                spans.append(dict(a=a / k, b=(g[-1]['tg'] + MOTOR['gap']) / k, pts=pts, fast=fast, start=None))
            else:
                st = g[0] if g[0]['tg'] > MOTOR['started_after'] else None
                spans.append(dict(a=a / k, b=(g[-1]['tg'] + MOTOR['tail']) / k, pts=pts, fast=fast, start=st))
    return spans


def place(mix, a, tout, vis0, vis1):
    """add sound a at output time tout, only inside the visible part [vis0, vis1] of the shot (faded out at its end)"""
    n = len(mix)
    if tout < vis0:
        skip = int((vis0 - tout) * SR)
        if skip >= len(a):
            return False
        a = a[skip:]
        tout = vis0
    i0 = int(tout * SR)
    i1 = min(i0 + len(a), int(vis1 * SR), n)
    if i1 <= i0:
        return False
    seg = a[:i1 - i0].copy()
    if i0 + len(a) > int(vis1 * SR):
        fl = min(len(seg), int(0.25 * SR))
        seg[-fl:] *= np.linspace(1, 0, fl)
    mix[i0:i1] += seg
    return True


def motor_loop(mix, s, sp, v0, vis0, vis1, log):
    """lay the motor loop of span sp over shot s (clip time -> output time as for the other sounds)"""
    files = EVENT_FILES.get(MOTOR_RUN)
    base = loop_file(files[0]) if files else None
    if base is None:
        print(f'  WARNING: no motor loop ({MOTOR_RUN} not in the mod\'s sounds, DOC_MOD?): {s.name} without motor')
        return
    c0 = s.start + (vis0 - v0) * s.speed                       # visible part in clip time
    c1 = s.start + (vis1 - v0) * s.speed
    if 'end' in s.opts:
        c1 = min(c1, s.clip_len)
    a, b = max(sp['a'], c0), min(sp['b'], c1)
    o0, o1 = v0 + (a - s.start) / s.speed, v0 + (b - s.start) / s.speed
    m = int((o1 - o0) * SR)
    if m < int(0.1 * SR):
        return
    pitch = MOTOR['fast_pitch'] if sp['fast'] else MOTOR['pitch']   # not x playback speed: no jumps at the cuts
    pos = np.arange(m) * pitch
    if pos[-1] + 2 > len(base):
        base = np.tile(base, int(pos[-1] // len(base)) + 2)
    snd = np.interp(pos, np.arange(len(base)), base).astype(np.float32)
    tclip = a + np.arange(m) / SR * s.speed
    env = MOTOR['gain'] * np.interp(tclip, [p[0] for p in sp['pts']], [p[1] for p in sp['pts']])
    fl = min(m // 2, int(MOTOR['fade'] * SR))
    env[:fl] *= np.linspace(0, 1, fl)
    env[m - fl:] *= np.linspace(1, 0, fl)
    i0 = int(o0 * SR)
    i1 = min(i0 + m, len(mix))
    mix[i0:i1] += (snd * env)[:i1 - i0]
    log.append(dict(t=round(o0, 2), shot=s.name, event=MOTOR_RUN + ' (loop)', gain=round(float(env.max()), 3),
                    until=round(o1, 2), pitch=round(pitch, 3)))
    st = sp['start']
    sf = EVENT_FILES.get(MOTOR_START)
    if st is not None and sf and c0 <= st['t'] < c1:
        snd = sound_file(sf[0])
        d = math.dist((st['x'], st['y'], st['z']), (st['cam_x'], st['cam_y'], st['cam_z']))
        g = MOTOR['start_gain'] * max(0.0, 1.0 - d / EVENT_ATT.get(MOTOR_START, 16.0))
        if snd is not None and g >= 0.01:
            tout = v0 + (st['t'] - s.start) / s.speed
            if place(mix, snd * g, tout, vis0, vis1):
                log.append(dict(t=round(tout, 2), shot=s.name, event=MOTOR_START + ' (for the old ticks)', gain=round(g, 3)))


def game_track(shots, total):
    n = int(total * SR) + SR
    mix = np.zeros(n, np.float32)
    log = []
    for s in shots:
        if s.kind != 'clip' or s.name == 'endcard':
            continue
        v0 = s.t0 - D / 2                                       # output time of local time 0
        vis0, vis1 = max(0.0, s.t0 - D / 2), s.t1 + D / 2
        events = clip_sounds(s.src[1])
        for sp in motor_spans(events):
            motor_loop(mix, s, sp, v0, vis0, vis1, log)
        for e in events:
            if is_motor(e) or ('end' in s.opts and e['t'] > s.clip_len):    # 'end': nothing after the part shown
                continue
            if 'start' in s.opts and e['t'] < s.start:          # nor from before it (a bite cut away by 'start')
                continue
            tout = v0 + (e['t'] - s.start) / s.speed
            if tout >= vis1 - 0.05:
                continue
            a = sound_file(e['file'])
            if a is None:
                continue
            pitch = min(2.0, max(0.5, e['pitch'] * s.speed))
            if abs(pitch - 1) > 1e-3:
                m = int(len(a) / pitch)
                a = np.interp(np.arange(m) * pitch, np.arange(len(a)), a).astype(np.float32)
            g = event_gain(e)
            if g < 0.01:
                continue
            if place(mix, a * g, tout, vis0, vis1):
                log.append(dict(t=round(tout, 2), shot=s.name, event=e['event'], gain=round(float(g), 3)))
    return mix[:int(total * SR)], log


def movavg(x, n):
    c = np.concatenate([[0.0], np.cumsum(x, dtype=np.float64)])
    h = n // 2
    idx = np.arange(len(x))
    lo, hi = np.clip(idx - h, 0, len(x)), np.clip(idx - h + n, 0, len(x))
    return ((c[hi] - c[lo]) / n).astype(np.float32)


def music_bed(paras, pstart, total, voice_wav):
    """Each chapter's track from its start, cross-faded (4 s) where a paragraph names a new one, ducked under the voice."""
    n = int(total * SR)
    out = np.zeros(n, np.float32)
    cues = []
    for pi, p in enumerate(paras):
        if p.get('music'):
            cues.append((max(0.0, pstart[pi] - 2.5) if pi else 0.0, p['music']))
    xf = int(4.0 * SR)
    used = []
    for ci, (t0, key) in enumerate(cues):
        t1 = cues[ci + 1][0] if ci + 1 < len(cues) else total
        fn, off = MUSIC[key]
        a = _load(os.path.join(MUSIC_DIR, fn))
        a = a / (np.abs(a).max() + 1e-6)
        a = a[int(off * SR):]
        i0, i1 = int(t0 * SR), min(n, int(t1 * SR) + (xf if ci + 1 < len(cues) else 0))
        need = i1 - i0
        seg = np.tile(a, int(math.ceil(need / len(a))))[:need].copy()
        if ci > 0:
            seg[:xf] *= np.linspace(0, 1, xf)
        if ci + 1 < len(cues):
            seg[-xf:] *= np.linspace(1, 0, xf)
        out[i0:i1] += seg
        used.append(key)
    fi, fo = int(CFG['fade_in'] * SR), int(CFG['fade_out'] * SR)
    out[:fi] *= np.linspace(0, 1, fi) ** 0.8
    out[-fo:] *= np.linspace(1, 0, fo)
    v = np.pad(voice_wav, (0, max(0, n - len(voice_wav))))[:n]
    env = np.clip(movavg((np.abs(v) > 0.02).astype(np.float32), int(0.6 * SR)) * 4, 0, 1)
    return out * (CFG['music_gaps'] + (CFG['music_under'] - CFG['music_gaps']) * env), used


def loudnorm(src, dst, target=-14):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', f'loudnorm=I={target}:TP=-1.5:LRA=11',
                    '-ar', str(SR), dst], check=True)


def verify(name, wav, tag, out):
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


# ------------------------------------------------------------------ checks

def flicker_check(video, cut_times):
    # small landscape frames, differences in chunks: the whole 21 min film at 60 fps as float32 needed ~14 GB
    w, h = 128, 72
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-vf', f'scale={w}:{h},format=gray', '-f', 'rawvideo', '-'],
                         check=True, capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w)
    d = np.empty(max(0, len(fr) - 1), np.float32)
    for s0 in range(0, len(d), 2000):
        a = fr[s0:s0 + 2001].astype(np.int16)
        d[s0:s0 + len(a) - 1] = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    del raw, fr
    cuts = {int(round(t * FPS)) for t in cut_times}
    bad = []
    for i in range(2, len(d) - 2):
        if any(abs(i + 1 - c) <= int(DB * FPS) for c in cuts):
            continue
        base = np.median(d[max(0, i - 6):i + 7]) + 0.5
        if d[i] > 4 * base and d[i] > 6:
            bad.append(round((i + 1) / FPS, 2))
    print(f'  flicker check: {"no spikes" if not bad else "spikes at " + str(bad[:30])}')
    return bad


def contact_sheet(video, out_png, every=6.0, cols=12, thumb=150):
    import tempfile
    tmp = tempfile.mkdtemp(dir=WORK)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-vf', f'fps=1/{every},scale={thumb}:-1', f'{tmp}/t%04d.png'], check=True)
    files = sorted(os.listdir(tmp))
    rows = math.ceil(len(files) / cols)
    th = int(thumb * H / W)
    sheet = Image.new('RGB', (cols * thumb, rows * (th + 22)), (16, 22, 30))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = Image.open(os.path.join(tmp, f))
        x, y = (i % cols) * thumb, (i // cols) * (th + 22)
        sheet.paste(im, (x, y + 22))
        t = i * every
        d.text((x + 4, y + 4), f'{int(t // 60)}:{t % 60:04.1f}', fill=(255, 230, 120))
    sheet.save(out_png)
    shutil.rmtree(tmp)


# ------------------------------------------------------------------ build

def museum_top(caps, shots):
    """Over the exhibition stills the subtitles go to the top: the bottom row of items and names sits where they
    normally are. The same over the shots in shots.json "caps_top" (the air gauge of the HUD sits above the hotbar)."""
    spans = [(s.t0, s.t1) for s in shots if s.name in LABELS or s.name in CAPS_TOP]
    for c in caps:
        mid = (c.t0 + c.t1) / 2
        if any(a <= mid < b for a, b in spans):
            c.y = 150


def build(name='doc', plan_only=False, audio_only=False, do_verify=True, limit=None, allow_missing=False):
    cfg = CFG
    OUT = f'{WORK}/out/{name}'
    os.makedirs(OUT, exist_ok=True)
    wav, wbp, vend, pstart = voice(name, cfg)
    total = round((vend + cfg['tail']) * FPS) / FPS
    v3lib.MAXC, v3lib.MAXW = cfg['maxc'], cfg['maxw']
    caps = []
    for pi, wp in enumerate(wbp):
        nxt = pstart[pi + 1] if pi + 1 < len(wbp) else total
        for c in v3lib.captions(wp, nxt, size=cfg['cap_size'], y=cfg['cap_y']):
            caps.append(Cap(c.t0, c.t1, c.text, 'cap'))
    shots, titles, table, miss = plan(name, wbp, pstart, total, allow_missing=allow_missing)
    museum_top(caps, shots)
    if SCRIPTS[name][-1].get('end'):
        for c in caps:
            if c.t0 >= pstart[-1] - 0.2:
                c.noburn = True                                  # the end card says it already (still in the SRT)
    print(f'{name}: voice ends {vend:.1f} s, video {total:.1f} s ({total / 60:.1f} min), {len(shots)} shots, '
          f'avg {total / max(1, len(shots)):.2f} s/shot, {len(caps)} captions' + (f', MISSING {miss}' if miss else ''))
    for t in table:
        print(f"  {t['id']:>4} {t['start']:7.1f}-{t['end']:7.1f} s ({t['end'] - t['start']:5.1f} s)  " +
              ', '.join(f'{s}@{f:.1f}' for s, f in t['shots']))
    for s in shots:
        print('   ', s.info())
    json.dump(dict(total=total, voice_end=vend, paragraphs=table,
                   captions=[dict(t0=c.t0, t1=c.t1, text=c.text) for c in caps],
                   shots=[dict(name=s.name, t0=s.t0, t1=s.t1, kind=s.kind) for s in shots]),
              open(f'{OUT}/timeline.json', 'w'), indent=1)
    if plan_only:
        return OUT
    n = int(total * SR)
    v = np.pad(wav, (0, max(0, n - len(wav))))[:n]
    g, glog = game_track(shots, total)
    g = np.tanh(g * cfg['game_gain'] / 0.8) * 0.8
    g = np.pad(g, (0, max(0, n - len(g))))[:n]
    env = movavg((np.abs(v) > 0.02).astype(np.float32), int(0.3 * SR))
    duck = np.full(n, cfg['duck'], np.float32)
    for s in shots:                                       # the boss fight: its sounds keep out of the narration
        if s.name.startswith(DUCK_MORE[0]):
            duck[max(0, int((s.t0 - D / 2) * SR)):int((s.t1 + D / 2) * SR)] = DUCK_MORE[1]
    g = g * (1.0 - duck * np.clip(env * 3, 0, 1))
    json.dump(glog, open(f'{OUT}/game_sounds.json', 'w'), indent=1)
    print(f'  game sounds: {len(glog)} placed')
    write_wav(f'{OUT}/voice.wav', v)
    mb, used = music_bed(SCRIPTS[name], pstart, total, v)
    sp = np.abs(v) > 0.02
    print(f'  music vs voice during speech: {20 * np.log10(np.sqrt((mb[sp] ** 2).mean()) / np.sqrt((v[sp] ** 2).mean())):.1f} dB')
    for tag, bed in (('music', mb),):
        m = v + g
        if bed is not None:
            m = m + bed
        m = m / max(1.0, np.abs(m).max() / 0.95)
        write_wav(f'{OUT}/{tag}0.wav', m)
        loudnorm(f'{OUT}/{tag}0.wav', f'{OUT}/{tag}.wav')
        os.remove(f'{OUT}/{tag}0.wav')
    with open(f'{OUT}/{cfg["file"]}.srt', 'w') as f:
        for k, c in enumerate(caps, 1):
            f.write(f'{k}\n{ts(c.t0)} --> {ts(c.t1)}\n{c.text.replace("*", "")}\n\n')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/voice.wav', '-c:a', 'aac', '-b:a', '128k',
                    f'{OUT}/{cfg["file"]}_voice.m4a'], check=True)
    write_post(name, OUT, table, used)
    if do_verify:
        for tag in ('music',):
            verify(name, f'{OUT}/{tag}.wav', tag, OUT)
    if audio_only:
        return OUT
    rtotal = min(total, limit) if limit else total
    burn = [c for c in caps if not getattr(c, 'noburn', False)]
    render_parallel(shots, burn + titles, f'{OUT}/v', rtotal, workers=int(os.environ.get('DOC_WORKERS', '4')))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{OUT}/v_captions_video.mp4', '-i', f'{OUT}/music.wav', '-c:v', 'copy',
                    '-af', f'volume=2dB,alimiter=limit=0.89,afade=t=out:st={max(0, rtotal - 2.5):.2f}:d=2.5',
                    '-c:a', 'aac', '-b:a', '160k', '-t', f'{rtotal:.2f}',
                    '-movflags', '+faststart', f'{OUT}/{cfg["file"]}.mp4'], check=True)
    flicker_check(f'{OUT}/v_captions_video.mp4', [s.t0 for s in shots])
    contact_sheet(f'{OUT}/v_captions_video.mp4', f'{OUT}/sheet.png')
    os.remove(f'{OUT}/v_captions_video.mp4')
    print('done', name, f'{rtotal:.1f} s ->', OUT)
    return OUT


def write_post(name, out, table, used):
    p = POST[name]
    chapters = []
    for t, para in zip(table, SCRIPTS[name]):
        if para.get('ch'):
            s = t['start'] + 0.6
            chapters.append(f"{int(s // 60):02d}:{int(s % 60):02d} {para['ch'].replace('*', '').title()}")
    credits = '\n'.join(f'"{CREDITS[k]}" Kevin MacLeod (incompetech.com)' for k in dict.fromkeys(used))
    txt = f"""TITLE (suggestion)
{p['title']}

DESCRIPTION
{p['body'].format(chapters=chr(10).join(chapters))}
Beach Craft is free on CurseForge: https://www.curseforge.com/minecraft/mc-mods/beach-craft

Music:
{credits}
Licensed under Creative Commons: By Attribution 4.0 - http://creativecommons.org/licenses/by/4.0/

{p['tags']}
"""
    open(f'{out}/{CFG["file"]}_post.txt', 'w').write(txt)


def deliver(name='doc'):
    cfg = CFG
    OUT = f'{WORK}/out/{name}'
    dst = ARCH
    total = json.load(open(f'{OUT}/timeline.json'))['total']
    files = [f'{cfg["file"]}.mp4']                     # captions burned in, with music (the only version rendered)
    for f in files:
        src = f'{OUT}/{f}'
        if not os.path.exists(src):
            raise SystemExit('missing output ' + src)
        size = os.path.getsize(src)
        base = f[:-4]
        for old in [x for x in os.listdir(dst) if x.startswith(base)]:
            os.remove(os.path.join(dst, old))
        if size > 90 * 2 ** 20:                          # GitHub: < 95 MB per file -> playable parts
            parts = math.ceil(size / (85 * 2 ** 20))
            times = ','.join(f'{total * k / parts:.2f}' for k in range(1, parts))
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-c', 'copy', '-map', '0', '-f', 'segment',
                            '-segment_times', times, '-reset_timestamps', '1', '-segment_start_number', '1',
                            f'{dst}/{base}_part%d.mp4'], check=True)
            print(f'  split into {parts}:', f)
        else:
            shutil.copy(src, f'{dst}/{f}')
    for f in (f'{cfg["file"]}.srt', f'{cfg["file"]}_voice.m4a', f'{cfg["file"]}_post.txt'):
        shutil.copy(f'{OUT}/{f}', f'{dst}/{f}')
    shutil.copy(f'{OUT}/sheet.png', f'{dst}/{cfg["file"]}_contact_sheet.png')
    print('delivered ->', dst)


if __name__ == '__main__':
    a = sys.argv[1:]
    flags = {x for x in a if x.startswith('--')}
    limit = float(a[a.index('--limit') + 1]) if '--limit' in a else None
    if '--deliver-only' in flags:
        deliver('doc')
        raise SystemExit
    build('doc', plan_only='--plan' in flags, audio_only='--audio' in flags, do_verify='--no-verify' not in flags,
          limit=limit, allow_missing='--allow-missing' in flags)
    if '--deliver' in flags and not ({'--plan', '--audio'} & flags) and not limit:
        deliver('doc')
