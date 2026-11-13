"""Stage 1 of the voice recording: performs lines with the voice design model (description + direction per line).
Usage: stage_design.py <jobs.json> <results.json>
jobs: {"batch": 8, "items": [{"id", "text", "instruct", "out", "seed", "max_tokens"}]}; results: {id: {"dur", "capped"}}"""
import json, os, sys, time
import numpy as np
import soundfile as sf
import torch

jobs = json.load(open(sys.argv[1]))
torch.set_num_threads(int(os.environ.get("THREADS", "4")))
from qwen_tts import Qwen3TTSModel
model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign", device_map="cpu", dtype=torch.bfloat16)
from transformers import StoppingCriteria, StoppingCriteriaList


class OwnCap(StoppingCriteria):
    """Ends a line of the batch at its own length limit, so that one line that never finds its end does not keep the
    whole batch running to the longest limit."""

    def __init__(self, caps):
        self.caps = torch.tensor(caps)

    def __call__(self, input_ids, scores, **kwargs):
        return input_ids.shape[1] >= self.caps.to(input_ids.device)


_talker = model.model.talker
_generate = _talker.generate
_caps = {"now": None}


def _generate_capped(*a, **k):
    if _caps["now"] is not None:
        k["stopping_criteria"] = StoppingCriteriaList([OwnCap(_caps["now"])])
    return _generate(*a, **k)


_talker.generate = _generate_capped
items = sorted(jobs["items"], key=lambda i: i["max_tokens"])
B = int(jobs.get("batch", 4))
results = {}
t_all, audio_all = time.time(), 0.0
for s in range(0, len(items), B):
    part = items[s:s + B]
    cap = max(i["max_tokens"] for i in part) + 2
    _caps["now"] = [i["max_tokens"] for i in part]
    torch.manual_seed(part[0]["seed"] * 1000 + s)
    t = time.time()
    try:
        wavs, sr = model.generate_voice_design(text=[i["text"] for i in part], language=["English"] * len(part),
                                               instruct=[i["instruct"] for i in part], max_new_tokens=cap)
    except Exception as e:  # one bad batch must not lose the rest
        print("batch failed: %r" % (e,), flush=True)
        for i in part:
            results[i["id"]] = {"dur": 0.0, "capped": True, "error": repr(e)[:200]}
        continue
    for i, w in zip(part, wavs):
        w = np.asarray(w, dtype=np.float32)
        os.makedirs(os.path.dirname(i["out"]), exist_ok=True)
        sf.write(i["out"], w, sr)
        dur = len(w) / sr
        audio_all += dur
        results[i["id"]] = {"dur": round(dur, 2), "capped": dur >= 0.97 * i["max_tokens"] / 12.5}
    json.dump(results, open(sys.argv[2], "w"))
    print("design %d-%d of %d: %.0fs" % (s + 1, s + len(part), len(items), time.time() - t), flush=True)
print("design: %.1fs of speech in %.0fs (x%.2f)" % (audio_all, time.time() - t_all, (time.time() - t_all) / max(audio_all, 0.1)), flush=True)
