"""(aus dem Archiv uebernommen: shorts/tools/v3lib.py, auf die Bausteine gekuerzt, die tama.py nutzt)
Stimme -> Wortzeiten (Whisper) abgleichen mit dem Skripttext, Untertitel in Satzstuecken, WAV/SRT-Helfer.
Die Grenzen der Untertitel-Stuecke (MAXC Zeichen, MAXW Woerter) setzt tama.py je Video."""
import os, sys, re, difflib, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cut
from cut import Caption

FPS = cut.FPS
SR = 48000
norm1 = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())


def _load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def script_tokens(para):
    """[(display word incl. punctuation, hot, core)] from a paragraph with *accent* spans."""
    toks, inside = [], False
    for raw in para.split():
        hot = inside or '*' in raw
        if raw.count('*') % 2:
            inside = not inside
        w = raw.replace('*', '')
        toks.append([w, hot, norm1(w)])
    return toks


def _alias():
    from script import HEARD
    al = {'10': 'ten', '27': 'twentyseven', '20': 'twenty', '1': 'one', 'minecrafts': 'minecraft', 'oars': 'ores'}
    for key, vs in HEARD.items():
        for v in vs:
            al[v.replace(' ', '')] = key
    return al


ALIAS = _alias()
canon = lambda x: ALIAS.get(x, x)


def merge_split(words):
    """Whisper writes 'Curse Forge' as two words; the script has one."""
    out, i = [], 0
    while i < len(words):
        if i + 1 < len(words) and norm1(words[i][0]) == 'curse' and norm1(words[i + 1][0]).startswith('forge'):
            out.append((words[i][0] + words[i + 1][0], words[i][1], words[i + 1][2]))
            i += 2
        else:
            out.append(words[i])
            i += 1
    return out


def align(toks, words, dur, off):
    """Script tokens -> (display, hot, t0, t1) with the times Whisper heard; gaps are interpolated."""
    a = [canon(x[2]) for x in toks]
    words = merge_split(words)
    b = [canon(norm1(w[0])) for w in words]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    t0 = [None] * len(a)
    t1 = [None] * len(a)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            t0[blk.a + k] = words[blk.b + k][1]
            t1[blk.a + k] = words[blk.b + k][2]
    miss = sum(x is None for x in t0)
    if miss:
        print(f'  align: {miss}/{len(a)} script words not matched (interpolated)')
    # interpolate the unmatched
    i = 0
    while i < len(a):
        if t0[i] is None:
            j = i
            while j < len(a) and t0[j] is None:
                j += 1
            lo = t1[i - 1] if i > 0 else 0.0
            hi = t0[j] if j < len(a) else dur
            for k in range(i, j):
                t0[k] = lo + (hi - lo) * (k - i) / (j - i)
                t1[k] = lo + (hi - lo) * (k - i + 1) / (j - i)
            i = j
        else:
            i += 1
    return [(toks[k][0], toks[k][1], off + t0[k], off + t1[k]) for k in range(len(a))]



# ------------------------------------------------------------------ captions

MAXC, MAXW = 42, 9
BREAK_BEFORE = {'and', 'or', 'but', 'so', 'then', 'until', 'into', 'in', 'on', 'of', 'to', 'for', 'with', 'against', 'from', 'where', 'that', 'if', 'as'}


def _chunks(words):
    """Split the aligned words into caption chunks: sentences, then clauses, then balanced halves."""
    sents, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r'[.?!]$', w[0]):
            sents.append(cur)
            cur = []
    if cur:
        sents.append(cur)
    size = lambda ws: sum(len(x[0]) + 1 for x in ws) - 1

    def ok(ws):
        return size(ws) <= MAXC and len(ws) <= MAXW

    out = []
    for s in sents:
        if ok(s):
            out.append(s)
            continue
        clauses, cur = [], []
        for w in s:
            cur.append(w)
            if w[0].endswith(','):
                clauses.append(cur)
                cur = []
        if cur:
            clauses.append(cur)
        merged = []
        for c in clauses:
            if merged and ok(merged[-1] + c):
                merged[-1] = merged[-1] + c
            else:
                merged.append(c)
        for c in merged:
            while not ok(c):
                # break at a conjunction nearest the middle, else the middle
                mid = len(c) / 2
                cands = [k for k in range(2, len(c) - 1) if c[k][0].lower().strip(',.') in BREAK_BEFORE]
                k = min(cands, key=lambda k: abs(k - mid)) if cands else int(round(mid))
                if cands and abs(k - mid) > 3:
                    k = int(round(mid))
                out.append(c[:k])
                c = c[k:]
            out.append(c)
    # glue a very short chunk to its neighbour if they fit together
    res = []
    for c in out:
        if res and len(res[-1]) < 4 and ok(res[-1] + c):
            res[-1] = res[-1] + c
        else:
            res.append(c)
    return res


def chunk_text(ws):
    out, i = [], 0
    while i < len(ws):
        if ws[i][1]:
            j = i
            while j + 1 < len(ws) and ws[j + 1][1]:
                j += 1
            seg = [w[0] for w in ws[i:j + 1]]
            m = re.match(r"^(.*?)([^\w']*)$", seg[-1])
            seg[-1] = m.group(1) + '*' + m.group(2)
            seg[0] = '*' + seg[0]
            out.extend(seg)
            i = j + 1
        else:
            out.append(ws[i][0])
            i += 1
    return ' '.join(out)


def captions(words, total, size=72, y=None):
    ch = _chunks(words)
    caps = []
    for k, c in enumerate(ch):
        t0 = c[0][2] - 0.04
        nxt = ch[k + 1][0][2] - 0.04 if k + 1 < len(ch) else total
        t1 = min(nxt, c[-1][3] + 0.45)
        if nxt - c[-1][3] < 0.6:
            t1 = nxt
        caps.append(Caption(max(0, t0), t1, chunk_text(c), 'cap', y=y, size=size))
    return caps


def write_wav(path, a):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', path],
                   input=a.astype(np.float32).tobytes(), check=True)


def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f'{h:02d}:{m:02d}:{int(s):02d},{int((s % 1) * 1000):03d}'
