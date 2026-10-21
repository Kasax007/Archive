"""Sprecher der Tamagotchi-Videos mit Kokoro (am_michael, speed 0.95), ein Aufruf pro Absatz, jeder Absatz mit
Whisper geprueft (angepasst von longform/tools/tts_kokoro.py).
  $SP/video/tts/bin/python tools/tts_kokoro.py short|long [Absatz-Indizes neu erzeugen]     (env HF_HOME=$SP/video/hf)
Ausgabe: $SP/video/vo/<name>/uNNN.wav (24 kHz) + uNNN.txt, units.json, report.json (Dauer je Absatz, vor/nach atempo)."""
import os, sys, json, re, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SP = os.environ.get('SP') or os.path.expanduser('~/tama_scratch')
os.environ.setdefault('HF_HOME', SP + '/video/hf')
import numpy as np, soundfile as sf
from script import SCRIPTS, SAY
from check import missing

name = sys.argv[1]
VO = f'{SP}/video/vo/{name}'
os.makedirs(VO, exist_ok=True)
VOICE, SPEED = os.environ.get('TAMA_VOICE', 'am_michael'), float(os.environ.get('TAMA_SPEED', '0.95'))
SLOW = float(os.environ.get('TAMA_SLOW', '1.06'))        # Faktor des Builders (atempo), nur fuer die Dauerangabe
U = [(i, p['text'].replace('*', '')) for i, p in enumerate(SCRIPTS[name])]
json.dump(U, open(VO + '/units.json', 'w'), indent=0)
from kokoro import KPipeline
from faster_whisper import WhisperModel
pipe = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
wh = WhisperModel(os.environ.get('TAMA_WHISPER', 'small.en'), device='cpu', compute_type='int8', cpu_threads=3)
only = [int(x) for x in sys.argv[2:] if x.isdigit()]
rep = json.load(open(VO + '/report.json')) if os.path.exists(VO + '/report.json') else {}
for i, text in U:
    out = f'{VO}/u{i:03d}.wav'
    if only and i not in only:
        continue
    if os.path.exists(out) and not only:
        continue
    say = text
    for k, v in SAY.items():
        say = re.sub(r'\b%s\b' % re.escape(k), v, say)
    best = None
    for sp in (SPEED, SPEED - 0.04, SPEED + 0.04, SPEED - 0.08, SPEED + 0.08):       # another pace = another take
        a = np.concatenate([x for _, _, x in pipe(say, voice=VOICE, speed=sp)])
        sf.write(out + '.try.wav', a, 24000)
        segs, _ = wh.transcribe(out + '.try.wav', language='en')
        heard = ' '.join(s.text for s in segs)
        miss, nw = missing(text, heard)
        if best is None or len(miss) < len(best[2]):
            best = (a, heard, miss, sp)
        if not miss:
            break
    a, heard, miss, sp = best
    sf.write(out, a, 24000)
    os.remove(out + '.try.wav')
    open(out[:-4] + '.txt', 'w').write(text)
    want = text.split()
    dur = len(a) / 24000
    rep[str(i)] = dict(id=SCRIPTS[name][i]['id'], seconds=round(dur, 2), seconds_final=round(dur / SLOW, 2),
                       words=len(want), wps=round(len(want) / (dur / SLOW), 2), miss=miss, speed=round(sp, 2), heard=heard.strip())
    print(f"{SCRIPTS[name][i]['id']} {dur:.1f}s -> {dur/SLOW:.1f}s {len(want)/(dur/SLOW):.2f} w/s speed={sp:.2f} miss={miss} | {heard.strip()}", flush=True)
    json.dump(rep, open(VO + '/report.json', 'w'), indent=1)
print('TTS DONE', flush=True)
