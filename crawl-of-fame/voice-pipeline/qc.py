"""Quality proxies for speech files (no ears here): what a recogniser hears, pitch and its movement, pace, level.
Usage: qc.py <wav...>   (env QC_MODEL: faster-whisper model, default base.en)"""
import os
import sys

import librosa
import numpy as np

from faster_whisper import WhisperModel

model = WhisperModel(os.environ.get("QC_MODEL", "base.en"), device="cpu", compute_type="int8", cpu_threads=2)
for path in sys.argv[1:]:
    y, sr = librosa.load(path, sr=16000, mono=True)
    dur = len(y) / sr
    segs, _ = model.transcribe(y, language="en", beam_size=3)
    text = " ".join(s.text.strip() for s in segs)
    f0, voiced, _ = librosa.pyin(y, fmin=60, fmax=450, sr=sr, frame_length=1024)
    f = f0[~np.isnan(f0)]
    if len(f) > 5:
        med = float(np.median(f))
        semis = 12 * np.log2(f / med)
        rng = float(np.percentile(semis, 95) - np.percentile(semis, 5))
        sd = float(np.std(semis))
    else:
        med = rng = sd = 0.0
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0]
    db = 20 * np.log10(np.maximum(rms, 1e-5))
    loud = db[db > db.max() - 35]
    words = len(text.split())
    print("%s\n   %.1fs, %.2f words/s | pitch median %.0f Hz, range %.1f st (sd %.1f) | level spread %.1f dB, peak %.2f\n   heard: %s"
          % (os.path.basename(path), dur, words / dur, med, rng, sd, float(np.std(loud)), float(np.abs(y).max()), text))
