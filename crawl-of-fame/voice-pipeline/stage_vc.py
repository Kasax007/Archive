"""Stage 3: one voice per speaker. Re-voices every clip with the timbre of its speaker's reference and measures how close
the result is to that reference. Usage: stage_vc.py <jobs.json> <results.json>
jobs: {"items": [{"id", "wav", "ref", "out"}], "embed": [wav...]}; results: {id: {"sim"}} and {"embed": {wav: [..]}}"""
import json, os, sys, time
import librosa
import numpy as np
import soundfile as sf
import torch

torch.set_num_threads(int(os.environ.get("THREADS", "4")))
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from chatterbox.models.voice_encoder import VoiceEncoder
from chatterbox.models.s3gen import S3Gen, S3GEN_SR
from chatterbox.models.s3tokenizer import S3_SR
import perth

jobs = json.load(open(sys.argv[1]))
d = os.path.dirname(hf_hub_download(repo_id="ResembleAI/chatterbox", filename="ve.safetensors"))
ve = VoiceEncoder(); ve.load_state_dict(load_file(os.path.join(d, "ve.safetensors"))); ve.eval()
def emb(path=None, y=None, sr=None):
    if y is None:
        y, sr = librosa.load(path, sr=16000, mono=True)
    elif sr != 16000:
        y = librosa.resample(y, orig_sr=sr, target_sr=16000)
    e = np.asarray(ve.embeds_from_wavs([y], sample_rate=16000)).reshape(-1)
    return e / np.linalg.norm(e)
results = {}
if jobs.get("embed"):
    results["embed"] = {p: [float(x) for x in emb(p)] for p in jobs["embed"]}
items = sorted(jobs.get("items", []), key=lambda i: i["ref"])
if items:
    # the two-step decoder of the same family: as close to the reference as the ten-step one (measured: 0.85-0.94
    # against 0.86-0.94) at a quarter of the time or less
    s3 = S3Gen(meanflow=True)
    s3.load_state_dict(load_file(hf_hub_download(repo_id="ResembleAI/chatterbox-turbo", filename="s3gen_meanflow.safetensors")), strict=True)
    s3.eval()
    mark = perth.PerthImplicitWatermarker()  # the library marks what it makes as synthetic: so do we
    SR = S3GEN_SR
    ref, ref_emb, ref_dict = None, None, None
    t_all, audio_all = time.time(), 0.0
    for n, it in enumerate(items):
        if it["ref"] != ref:
            ref = it["ref"]
            rw, _ = librosa.load(ref, sr=SR)
            ref_dict = s3.embed_ref(rw[:10 * SR], SR, device="cpu")
            ref_emb = emb(ref)
        try:
            with torch.inference_mode():
                a16, _ = librosa.load(it["wav"], sr=S3_SR)
                tokens, _ = s3.tokenizer(torch.from_numpy(a16).float()[None, ])
                wav, _ = s3.inference(speech_tokens=tokens, ref_dict=ref_dict, n_cfm_timesteps=2)
            w = mark.apply_watermark(wav.squeeze(0).numpy(), sample_rate=SR)
        except Exception as e:
            results[it["id"]] = {"sim": 0.0, "error": repr(e)[:200]}
            continue
        peak = float(np.abs(w).max())
        if peak > 0.97:
            w = w * (0.97 / peak)
        os.makedirs(os.path.dirname(it["out"]), exist_ok=True)
        sf.write(it["out"], w, SR)
        audio_all += len(w) / SR
        results[it["id"]] = {"sim": round(float(emb(y=np.asarray(w, dtype=np.float32), sr=SR) @ ref_emb), 3)}
        if n % 8 == 7:
            json.dump(results, open(sys.argv[2], "w"))
            print("voice %d of %d" % (n + 1, len(items)), flush=True)
    print("voice: %.1fs of speech in %.0fs (x%.2f)" % (audio_all, time.time() - t_all, (time.time() - t_all) / max(audio_all, 0.1)), flush=True)
json.dump(results, open(sys.argv[2], "w"))
