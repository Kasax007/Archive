"""Voice-over for the V3 shorts: one Chatterbox call per paragraph (2-3 sentences), the same reference
voice for all. Every paragraph is checked with Whisper and re-rolled with another seed if words are lost.
  python tts_v3.py NAME [more names]      (env: HF_HOME, run inside the tts venv, nice -n 15)
Output: $SP/vo3/NAME/pNN.wav (+ pNN.txt = the spoken text)  and  $SP/vo3/ref.wav (the reference voice)."""
import os, sys, json, re
import torch, torchaudio as ta
torch.set_num_threads(3)
from chatterbox.tts import ChatterboxTTS
from faster_whisper import WhisperModel

HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.environ.get('SP', '/tmp/claude-0/-home-user-Kasax-Challenge-Craft/2061deb3-7247-5b5c-aa62-6c43681c8da7/scratchpad')
VO = SP + '/vo3'
S = json.load(open(HERE + '/scripts_v3.json'))
model = ChatterboxTTS.from_pretrained(device='cpu')
wh = WhisperModel('base.en', device='cpu', compute_type='int8', cpu_threads=2)
def norm(s):
    s = s.lower().replace('-', ' ').replace('2025', 'twenty twenty five').replace('50', 'fifty').replace('96', 'ninety six')
    s = re.sub(r'\b20\b', 'twenty', s)
    return re.sub(r'[^a-z0-9 ]', '', s).split()
REF = VO + '/ref.wav'


def trim(a, sr):
    thr = a.abs().max() * 0.02
    idx = (a.abs() > thr).nonzero()
    return a[max(0, int(idx[0]) - 300): int(idx[-1]) + int(sr * 0.25)] if len(idx) else a


for name in sys.argv[1:]:
    os.makedirs(f'{VO}/{name}', exist_ok=True)
    for i, para in enumerate(S[name]):
        out = f'{VO}/{name}/p{i:02d}.wav'
        if os.path.exists(out):
            continue
        text = para.replace('*', '')
        want = norm(text)
        best = None
        for attempt in range(4):
            torch.manual_seed(7 + 101 * i + attempt)
            kw = dict(exaggeration=0.55 + 0.05 * (attempt % 2), cfg_weight=0.45 if attempt < 2 else 0.4)
            if os.path.exists(REF):
                kw['audio_prompt_path'] = REF
            wav = model.generate(text, **kw)
            a = trim(wav[0], model.sr)
            tmp = f'{VO}/_t.wav'
            ta.save(tmp, a.unsqueeze(0), model.sr)
            segs, _ = wh.transcribe(tmp, language='en')
            got = norm(' '.join(s.text for s in segs))
            miss = [w for w in want if w not in got]
            score = len(miss)
            print(f'{name} p{i} try {attempt} miss={miss} dur={a.shape[-1]/model.sr:.1f}', flush=True)
            if best is None or score < best[0]:
                best = (score, a)
            if score <= 0 or (score <= 1 and attempt >= 1):
                break
        ta.save(out, best[1].unsqueeze(0), model.sr)
        open(out[:-4] + '.txt', 'w').write(text)
        if not os.path.exists(REF):
            ta.save(REF, best[1].unsqueeze(0), model.sr)
            print('reference voice saved', flush=True)
print('TTS DONE')
