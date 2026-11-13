"""Placeholder speech with the small fast model. Usage: draft_k.py <text file> <out wav> [voice]
The text file may hold many lines "id<TAB>text": then <out wav> is a directory and one file per id is written."""
import os, re, sys
import soundfile as sf
from kokoro_onnx import Kokoro
here = os.path.dirname(os.path.abspath(__file__))
k = Kokoro(os.path.join(here, "kokoro/kokoro-v1.0.onnx"), os.path.join(here, "kokoro/voices-v1.0.bin"))
src, out = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else "am_michael"
def say(text, path):
    text = re.sub(r"\[[a-z ]+\]", " ", text).strip()
    w, sr = k.create(text, voice=voice, speed=1.0, lang="en-us")
    sf.write(path, w, sr)
lines = [l.rstrip("\n") for l in open(src, encoding="utf-8") if l.strip()]
if lines and all("\t" in l for l in lines):
    os.makedirs(out, exist_ok=True)
    for l in lines:
        i, t = l.split("\t", 1)
        say(t, os.path.join(out, i + ".wav"))
else:
    say(" ".join(lines), out)
