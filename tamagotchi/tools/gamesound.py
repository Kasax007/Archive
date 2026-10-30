"""Die echten Spielgeraeusche zum Footage. Der Film-Harness des Mods (src/film, FilmSound) schreibt pro Shot
sounds.jsonl: welche Sounddatei wann (Sekunden Spielzeit ab Shot-Anfang) mit welcher Lautstaerke und Tonhoehe wo
gespielt wurde und wo die Kamera stand, dazu shot.json (Bilder pro Sekunde Spielzeit).
track() mischt diese Dateien entlang des Schnitts so, wie Minecraft sie spielt: Lautstaerke (0..1), Tonhoehe
(0.5..2, als Abspielgeschwindigkeit), lineare Abnahme mit der Entfernung zur Kamera bis zur Hoerweite des Sounds.
Mono, 48 kHz wie der Rest der Pipeline. Musik, Ambiente und Wetter der Welt bleiben draussen (die Musik kommt extra)."""
import os, json, subprocess
import numpy as np

SR = 48000
FPS = 30
MC_INDEX = '/root/.gradle/caches/fabric-loom/assets/indexes/26.3-34.json'
MC_OBJECTS = '/root/.gradle/caches/fabric-loom/assets/objects'
MOD_ASSETS = os.environ.get('TAMA_ASSETS', '/home/user/Tamagotchi/src/main/resources/assets')
SKIP_SOURCES = {'music', 'ambient', 'weather'}
# Props of the film's stage that are not part of a shot: the campfire (crackles near the middle of the stage) and the
# vault of the treasure room. Shot names that may keep them: event prefix -> shots
STAGE_NOISE = {'minecraft:block.campfire.': {'campfire_warm'}, 'minecraft:block.vault.': set()}
FADE = 0.06                     # a sound still playing at a cut fades out this fast
_index, _cache = None, {}


def _decode(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def load(file_id):
    """'minecraft:sounds/block/barrel/open1.ogg' (vanilla assets) or 'tamagotchi:sounds/pet/petting1.ogg' (the mod)."""
    global _index
    if file_id in _cache:
        return _cache[file_id]
    ns, path = file_id.split(':', 1)
    if ns == 'minecraft':
        if _index is None:
            _index = json.load(open(MC_INDEX))['objects']
        h = _index['minecraft/' + path]['hash']
        src = f'{MC_OBJECTS}/{h[:2]}/{h}'
    else:
        src = f'{MOD_ASSETS}/{ns}/{path}'
    a = _decode(src)
    _cache[file_id] = a
    return a


def render(e):
    """One logged sound as the game plays it: pitch as playback speed, volume, distance falloff."""
    a = load(e['file'])
    pitch = min(2.0, max(0.5, e['pitch']))
    if abs(pitch - 1) > 1e-3:
        n = int(len(a) / pitch)
        a = np.interp(np.arange(n) * pitch, np.arange(len(a)), a).astype(np.float32)
    gain = min(1.0, max(0.0, e['volume']))
    if e['attenuation'] == 'LINEAR' and not e['relative']:
        d = np.sqrt((e['x'] - e['cam_x']) ** 2 + (e['y'] - e['cam_y']) ** 2 + (e['z'] - e['cam_z']) ** 2)
        gain *= max(0.0, 1.0 - d / max(1.0, e['distance']))
    return a * gain


def shot_sounds(shot_dir):
    """-> (frames per second of game time, [events]) or None when the shot has no sound log."""
    f = os.path.join(shot_dir, 'sounds.jsonl')
    if not os.path.exists(f):
        return None
    meta = os.path.join(shot_dir, 'shot.json')
    fps = json.load(open(meta))['fps'] if os.path.exists(meta) else FPS
    evs = [json.loads(l) for l in open(f) if l.strip()]
    return fps, [e for e in evs if e['source'] not in SKIP_SOURCES]


def track(pl, total):
    """pl: [(Clip, start s, cues)] from tama.plan -> mono track of the game sounds along the cut, plus a log."""
    n = int(total * SR) + SR
    mix = np.zeros(n, np.float32)
    log = []
    for clip, t0, _ in pl:
        got = shot_sounds(clip.shot)
        if got is None:
            continue
        fps, evs = got
        evs = [e for e in evs if not any(e['event'].startswith(k) and clip.label not in keep for k, keep in STAGE_NOISE.items())]
        s0 = clip.start * FPS                                      # first source frame shown
        played = int(round((clip.length - clip.hold_last) * FPS))  # output frames that move
        c0, c1 = int(t0 * SR), int((t0 + clip.length) * SR)
        for e in evs:
            src_frame = e['t'] * fps                               # frame index of the event in the shot folder
            k = (src_frame - s0) / clip.speed                      # output frames into the clip
            if k >= played:
                continue
            a = render(e)
            if k < 0:                                              # started before the clip: join it mid-way
                skip = int(-k / FPS * SR * clip.speed)
                if skip >= len(a):
                    continue
                a = a[skip:]
                k = 0
            i0 = c0 + int(k / FPS * SR)
            i1 = min(i0 + len(a), c1)
            if i1 <= i0:
                continue
            seg = a[:i1 - i0].copy()
            if i0 + len(a) > c1:                                   # cut: fade out quickly
                f = min(len(seg), int(FADE * SR))
                seg[-f:] *= np.linspace(1, 0, f)
            mix[i0:i1] += seg
            if np.abs(seg).max() > 0.01:
                log.append(dict(t=round(t0 + k / FPS, 2), shot=clip.label, event=e['event'], gain=round(float(np.abs(seg).max()), 3)))
    return mix[:int(total * SR)], log
