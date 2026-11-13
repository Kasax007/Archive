"""Speaker similarity of clips (cosine of voice encoder embeddings). Usage: spk.py <wav...>"""
import glob, os, sys
import librosa, numpy as np, torch
from safetensors.torch import load_file
from chatterbox.models.voice_encoder import VoiceEncoder
from huggingface_hub import hf_hub_download
snap = os.path.dirname(hf_hub_download(repo_id="ResembleAI/chatterbox", filename="ve.safetensors"))
ve = VoiceEncoder(); ve.load_state_dict(load_file(os.path.join(snap, "ve.safetensors"))); ve.eval()
names, embs = [], []
for p in sys.argv[1:]:
    y, _ = librosa.load(p, sr=16000, mono=True)
    e = ve.embeds_from_wavs([y], sample_rate=16000)
    embs.append(np.asarray(e).reshape(-1)); names.append(os.path.basename(p)[:-4])
E = np.stack(embs); E /= np.linalg.norm(E, axis=1, keepdims=True)
S = E @ E.T
print(" " * 18 + " ".join("%5d" % i for i in range(len(names))))
for i, n in enumerate(names):
    print("%2d %-15s" % (i, n[:15]) + " ".join("%5.2f" % S[i, j] for j in range(len(names))))
np.save(sys.argv[1] + ".emb.npy", E)
