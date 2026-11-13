"""Stage 2: is the line what was written? Trims silence at both ends, lets a recogniser listen, measures pace and gaps.
Usage: stage_words.py <jobs.json> <results.json>;  jobs: {"items": [{"id", "wav", "text"}]}
results: {id: {"heard", "ratio", "dur", "wps", "gap"}} (ratio: similarity of the letters heard and written, 0..1)"""
import difflib, json, os, re, sys
import librosa
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

jobs = json.load(open(sys.argv[1]))
model = WhisperModel(os.environ.get("QC_MODEL", "base.en"), device="cpu", compute_type="int8",
                     cpu_threads=int(os.environ.get("THREADS", "4")))
NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight",
       "9": "nine", "10": "ten", "11": "eleven", "12": "twelve", "20": "twenty", "30": "thirty", "40": "forty",
       "50": "fifty", "60": "sixty", "100": "onehundred"}
def letters(s):
    s = re.sub(r"\[[a-z ]+\]", " ", s.lower())
    s = re.sub(r"\d+", lambda m: NUM.get(m.group(0), m.group(0)), s)
    return re.sub(r"[^a-z0-9]", "", s)
results = {}
for it in jobs["items"]:
    y, sr = sf.read(it["wav"], dtype="float32")
    if y.ndim > 1:
        y = y.mean(axis=1)
    if len(y) < sr // 4:
        results[it["id"]] = {"heard": "", "ratio": 0.0, "dur": 0.0, "wps": 0.0, "gap": 0.0}
        continue
    # trim to 60 ms before the first and 120 ms after the last sound
    iv = librosa.effects.split(y, top_db=38, frame_length=1024, hop_length=256)
    if len(iv):
        a, b = max(0, iv[0][0] - int(0.06 * sr)), min(len(y), iv[-1][1] + int(0.12 * sr))
        gap = max([(iv[k + 1][0] - iv[k][1]) / sr for k in range(len(iv) - 1)] or [0.0])
        y = y[a:b]
        sf.write(it["wav"], y, sr)
    else:
        gap = 0.0
    y16 = librosa.resample(y, orig_sr=sr, target_sr=16000)
    segs, _ = model.transcribe(y16, language="en", beam_size=3)
    heard = " ".join(s.text.strip() for s in segs)
    ratio = difflib.SequenceMatcher(None, letters(it["text"]), letters(heard)).ratio()
    dur = len(y) / sr
    words = len(re.sub(r"\[[a-z ]+\]", " ", it["text"]).split())
    results[it["id"]] = {"heard": heard, "ratio": round(ratio, 3), "dur": round(dur, 2), "wps": round(words / dur, 2),
                         "gap": round(gap, 2)}
json.dump(results, open(sys.argv[2], "w"))
print("words: %d clips checked" % len(results), flush=True)
