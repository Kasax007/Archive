#!/usr/bin/env python3
"""Records the mod's voice lines (the lead's side of docs/VOICE.md).

For every line of the spoken script: a speech model performs it from the speaker's description and the line's direction,
a recogniser checks the words, a second model gives it the speaker's one voice (the reference clip), a speaker encoder
checks that voice, then the line is processed with the speaker's preset and written as Ogg. A line that fails a check is
performed again (up to four times), then listed. Everything is resumable: state in <work>/state.json.

Usage: synth.py --repo <mod repo> [--work DIR] [--refs] [--speaker ID ...] [--tier N] [--limit N] [--chunk 32]
                [--batch 8] [--minutes M] [--report] [--redo ID ...]
Needs the speech environments under $VOICE_HOME (q312: design model and recogniser; c311: voice conversion)."""
import argparse, glob, hashlib, json, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.environ.get("VOICE_HOME", "/tmp/claude-0/-home-user/e2686f39-d632-56d3-aa9e-a2a2f832009c/scratchpad/voice")
TAGS = {"laugh": "laughs", "chuckle": "chuckles", "sigh": "sighs", "gasp": "gasps", "cough": "coughs",
        "clear throat": "clears the throat", "groan": "groans", "sniff": "sniffs", "shush": "makes a shushing sound"}
MAX_TRIES = 4


def log(work, msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    with open(os.path.join(work, "log.txt"), "a") as f:
        f.write(line + "\n")


def load_cast(repo):
    raw = json.load(open(os.path.join(repo, "tools/content/voice/cast.json")))
    if isinstance(raw, dict) and "speakers" in raw:
        raw = raw["speakers"]
    cast = {}
    entries = raw.items() if isinstance(raw, dict) else ((e.get("id"), e) for e in raw)
    for sid, e in entries:
        desc = e.get("voice") or e.get("description") or e.get("desc") or ""
        cast[sid] = {"desc": desc.strip(), "preset": e.get("preset", "room"), "name": e.get("name", sid),
                     "tempo": float(e.get("tempo", 1.0))}
    return cast


def load_script(repo):
    lines = []
    for path in sorted(glob.glob(os.path.join(repo, "tools/content/voice/script/*.json"))):
        d = json.load(open(path))
        for l in d.get("lines", []):
            lines.append({"speaker": d["speaker"], "id": l["id"], "text": l["text"], "how": l.get("how", ""),
                          "tier": int(l.get("tier", 2)), "long": bool(l.get("long", False))})
    return lines


def spoken(text, how):
    """The text without sound tags, and the direction with the tags written out."""
    notes = []
    plain = re.sub(r"\s+", " ", re.sub(r"\[[a-z ]+\]", " ", text)).strip()
    for m in re.finditer(r"\[([a-z ]+)\]", text):
        verb = TAGS.get(m.group(1))
        if not verb:
            continue
        before = re.sub(r"\[[a-z ]+\]", " ", text[:m.start()]).split()
        after = re.sub(r"\[[a-z ]+\]", " ", text[m.end():]).split()
        if not before:
            notes.append("The speaker %s before the first word." % verb)
        elif not after:
            notes.append("The speaker %s after the last word." % verb)
        else:
            notes.append('The speaker %s briefly after "%s".' % (verb, " ".join(before[-3:])))
    return plain, " ".join([how.strip()] + notes).strip()


def key(l):
    return l["speaker"] + "/" + l["id"]


def digest(l, cast):
    c = cast.get(l["speaker"], {})
    return hashlib.sha1("|".join([l["text"], l["how"], c.get("desc", ""), c.get("preset", ""), "%.3f" % c.get("tempo", 1.0)]).encode()).hexdigest()[:12]


def stage(work, env_name, script, jobs, tag):
    jp, rp = os.path.join(work, tag + ".jobs.json"), os.path.join(work, tag + ".results.json")
    json.dump(jobs, open(jp, "w"))
    if os.path.exists(rp):
        os.remove(rp)
    env = dict(os.environ, HF_HOME=os.path.join(HOME, "hf"), THREADS=os.environ.get("THREADS", "4"),
               TOKENIZERS_PARALLELISM="false", QC_MODEL=os.environ.get("QC_MODEL", "small.en"),
               KMP_BLOCKTIME="0", OMP_WAIT_POLICY="PASSIVE")  # do not spin while the engineers' runs hold the cores
    cmd = ["nice", "-n", "10", os.path.join(HOME, env_name, "bin", "python"), os.path.join(HERE, script), jp, rp]
    def first_to_go():  # if memory runs out the speech job is killed, not a build or a test of the engineers
        try:
            open("/proc/self/oom_score_adj", "w").write("900")
        except OSError:
            pass

    with open(os.path.join(work, "stage.log"), "a") as lf:
        p = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=lf, text=True, preexec_fn=first_to_go)
    for line in p.stdout.splitlines():
        if line.startswith(("design:", "voice:", "batch failed")):
            log(work, "  " + line)
    if not os.path.exists(rp):
        log(work, "  stage %s gave no result (exit %d): see stage.log" % (tag, p.returncode))
        return {}
    return json.load(open(rp))


def max_tokens(text, long):
    words = len(text.split())
    seconds = words / 1.9 + 2.5 + text.count("...") * 1.0
    return int(min(900 if long else 520, max(50, seconds * 12.5 * 1.3)))


def process(repo, preset, wav, ogg, tempo=1.0):
    os.makedirs(os.path.dirname(ogg), exist_ok=True)
    tool = os.path.join(repo, "tools/content/voice/process.py")
    if os.path.exists(tool):
        r = subprocess.run([sys.executable, tool, preset, wav, ogg, "%.3f" % tempo], capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(ogg):
            return True
    if abs(tempo - 1.0) > 0.005:  # the speaker's pace, set in the cast (pitch stays)
        fast = wav[:-4] + ".tempo.wav"
        r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", wav, "-af", "atempo=%.3f" % tempo, fast],
                           capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(fast):
            wav = fast
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", wav, "-af",
                        "highpass=f=70,loudnorm=I=-19:TP=-1.5:LRA=11", "-ar", "24000", "-ac", "1", "-c:a", "libvorbis",
                        "-q:a", "3", ogg], capture_output=True, text=True)
    return r.returncode == 0 and os.path.exists(ogg)


OUT = {"dir": None}


def out_path(repo, l):
    base = OUT["dir"] or os.path.join(repo, "src/main/modules/voice/assets/crawloffame/sounds/voice")
    return os.path.join(base, l["speaker"], l["id"].replace(".", "_") + ".ogg")


def make_refs(args, work, cast, lines, speakers):
    todo = [s for s in speakers if not os.path.exists(os.path.join(work, "ref", s + ".wav"))]
    if not todo:
        return
    items, texts = [], {}
    for s in todo:
        own = sorted([l for l in lines if l["speaker"] == s], key=lambda l: (l["tier"], abs(len(l["text"].split()) - 14)))
        words, parts = 0, []
        for l in own:
            t = spoken(l["text"], "")[0]
            if words + len(t.split()) > 44:
                continue
            parts.append(t); words += len(t.split())
            if words >= 30:
                break
        if words < 16:
            parts.append("That is all from me for now. Come back any time, and mind how you go.")
        texts[s] = " ".join(parts)
        for n in range(3):
            items.append({"id": "%s#%d" % (s, n), "text": texts[s], "seed": 101 + n, "max_tokens": max_tokens(texts[s], True),
                          "instruct": cast[s]["desc"] + " Speaks naturally and at ease, in the way most typical of this character.",
                          "out": os.path.join(work, "refcand", "%s_%d.wav" % (s, n))})
    log(work, "references: %d speakers, %d candidates" % (len(todo), len(items)))
    res = stage(work, "q312", "stage_design.py", {"batch": args.batch, "items": items}, "ref_design")
    ok = [i for i in items if i["id"] in res and not res[i["id"]].get("capped")]
    words = stage(work, "q312", "stage_words.py", {"items": [{"id": i["id"], "wav": i["out"], "text": i["text"]} for i in ok]}, "ref_words")
    good = [i for i in ok if words.get(i["id"], {}).get("ratio", 0) >= 0.9 and words[i["id"]]["dur"] >= 5.5]
    emb = stage(work, "c311", "stage_vc.py", {"embed": [i["out"] for i in good]}, "ref_embed").get("embed", {})
    os.makedirs(os.path.join(work, "ref"), exist_ok=True)
    for s in todo:
        cands = [i for i in good if i["id"].startswith(s + "#") and i["out"] in emb]
        if not cands:
            log(work, "  no usable reference for %s: run --refs again" % s)
            continue
        if len(cands) > 1:  # the most typical one: closest to the others
            def score(i):
                return sum(sum(a * b for a, b in zip(emb[i["out"]], emb[j["out"]])) for j in cands if j is not i)
            cands.sort(key=score, reverse=True)
        shutil.copyfile(cands[0]["out"], os.path.join(work, "ref", s + ".wav"))
        log(work, "  reference %s: %s (%.1fs)" % (s, os.path.basename(cands[0]["out"]), words[cands[0]["id"]]["dur"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--work", default=os.path.join(HOME, "work"))
    ap.add_argument("--out", help="write the ogg files here (speaker/id.ogg) instead of into the repo's voice module")
    ap.add_argument("--refs", action="store_true", help="make missing reference clips, then stop")
    ap.add_argument("--speaker", nargs="*")
    ap.add_argument("--tier", type=int, default=3, help="record tiers up to this one")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--chunk", type=int, default=32)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--minutes", type=float, default=0, help="stop after this many minutes (after the running chunk)")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--redo", nargs="*", default=[], help="speaker/id keys to record again")
    args = ap.parse_args()
    repo, work = os.path.abspath(args.repo), os.path.abspath(args.work)
    OUT["dir"] = os.path.abspath(args.out) if args.out else None
    os.makedirs(work, exist_ok=True)
    cast, lines = load_cast(repo), load_script(repo)
    sp = os.path.join(work, "state.json")
    state = json.load(open(sp)) if os.path.exists(sp) else {}
    for k in args.redo:
        state.pop(k, None)
    speakers = [s for s in dict.fromkeys(l["speaker"] for l in lines) if not args.speaker or s in args.speaker]
    missing = [s for s in speakers if s not in cast or not cast[s]["desc"]]
    if missing:
        sys.exit("speakers without a voice description in cast.json: " + ", ".join(missing))
    for l in lines:  # a changed line or a lost file is recorded again
        st = state.get(key(l))
        if st and (st.get("digest") != digest(l, cast) or (st.get("status") == "done" and not os.path.exists(out_path(repo, l)))):
            state.pop(key(l))
    if args.report:
        by = {}
        for l in lines:
            st = state.get(key(l), {})
            b = by.setdefault(l["speaker"], {"lines": 0, "done": 0, "failed": 0, "sec": 0.0})
            b["lines"] += 1; b["done"] += st.get("status") == "done"; b["failed"] += st.get("status") == "failed"
            b["sec"] += st.get("dur", 0) if st.get("status") == "done" else 0
        for s, b in by.items():
            print("%-18s %4d lines  %4d done  %3d failed  %5.1f min" % (s, b["lines"], b["done"], b["failed"], b["sec"] / 60))
        print("total: %d lines, %d done, %.1f min" % (len(lines), sum(b["done"] for b in by.values()), sum(b["sec"] for b in by.values()) / 60))
        for l in lines:
            st = state.get(key(l), {})
            if st.get("status") == "failed":
                print("FAILED %s: %s | heard: %s" % (key(l), st.get("why"), st.get("heard", "")[:90]))
        return
    wanted = [s for s in speakers if any(l["speaker"] == s and l["tier"] <= args.tier
                                         and state.get(key(l), {}).get("status") not in ("done", "failed") for l in lines)]
    make_refs(args, work, cast, lines, speakers if args.refs else wanted)
    if args.refs:
        return
    order = {s: n for n, s in enumerate(speakers)}
    todo = [l for l in lines if l["speaker"] in order and l["tier"] <= args.tier
            and state.get(key(l), {}).get("status") not in ("done", "failed")
            and os.path.exists(os.path.join(work, "ref", l["speaker"] + ".wav"))]
    todo.sort(key=lambda l: (l["tier"], order[l["speaker"]], l["id"]))
    if args.limit:
        todo = todo[:args.limit]
    log(work, "to record: %d lines (%d speakers)" % (len(todo), len({l["speaker"] for l in todo})))
    start = time.time()
    while todo:
        if os.path.exists(os.path.join(work, "STOP")) or (args.minutes and time.time() - start > args.minutes * 60):
            log(work, "stopping as asked; %d lines left" % len(todo))
            break
        part, todo = todo[:args.chunk], todo[args.chunk:]
        t0 = time.time()
        items = []
        for l in part:
            st = state.setdefault(key(l), {"tries": 0})
            st.update(tries=st["tries"] + 1, digest=digest(l, cast), status="pending")
            text, how = spoken(l["text"], l["how"])
            items.append({"id": key(l), "text": text, "seed": 7 + 31 * st["tries"], "max_tokens": max_tokens(text, l["long"]),
                          "instruct": (cast[l["speaker"]]["desc"] + " " + how).strip(),
                          "out": os.path.join(work, "raw", l["speaker"], l["id"].replace(".", "_") + ".wav")})
        res = stage(work, "q312", "stage_design.py", {"batch": args.batch, "items": items}, "design")
        by_key = {key(l): l for l in part}
        again = []

        def fail(k, why, **more):
            st = state[k]
            st.update(why=why, **more)
            if st["tries"] >= MAX_TRIES:
                st["status"] = "failed"
            else:
                again.append(by_key[k])

        ok = []
        for i in items:
            r = res.get(i["id"])
            if not r or r.get("capped") or r["dur"] < 0.4:
                fail(i["id"], "no end or no sound")
            else:
                ok.append(i)
        # one voice per speaker, then the checks on what the player will hear
        vjobs = [{"id": i["id"], "wav": i["out"], "ref": os.path.join(work, "ref", by_key[i["id"]]["speaker"] + ".wav"),
                  "out": i["out"].replace(os.sep + "raw" + os.sep, os.sep + "voiced" + os.sep)} for i in ok]
        vres = stage(work, "c311", "stage_vc.py", {"items": vjobs}, "vc") if vjobs else {}
        voiced = {j["id"]: j["out"] for j in vjobs if vres.get(j["id"]) and "error" not in vres[j["id"]]}
        words = stage(work, "q312", "stage_words.py", {"items": [{"id": i["id"], "wav": voiced[i["id"]], "text": i["text"]}
                                                                 for i in ok if i["id"] in voiced]}, "words") if voiced else {}
        done = 0
        for i in ok:
            k, l = i["id"], by_key[i["id"]]
            w, n = words.get(k), len(i["text"].split())
            if k not in voiced:
                fail(k, "voice step failed")
            elif not w:
                fail(k, "not checked")
            elif w["ratio"] < (0.84 if n <= 4 else 0.9):
                fail(k, "words differ (%.2f)" % w["ratio"], heard=w["heard"])
            elif n >= 6 and not 1.1 <= w["wps"] <= 4.6:
                fail(k, "pace %.1f words/s" % w["wps"], heard=w["heard"])
            elif w["gap"] > (3.0 if "..." in i["text"] else 1.6):
                fail(k, "a gap of %.1fs" % w["gap"], heard=w["heard"])
            elif vres[k]["sim"] < 0.78:
                fail(k, "voice differs (%.2f)" % vres[k]["sim"], sim=vres[k]["sim"], heard=w["heard"])
            elif not process(repo, cast[l["speaker"]]["preset"], voiced[k], out_path(repo, l), cast[l["speaker"]]["tempo"]):
                fail(k, "processing failed")
            else:
                state[k].update(status="done", sim=vres[k]["sim"], heard=w["heard"], ratio=w["ratio"], dur=w["dur"],
                                wps=w["wps"], why="")
                done += 1
        json.dump(state, open(sp, "w"), indent=0)
        todo = again + todo
        sec = sum(state[key(l)].get("dur", 0) for l in part if state[key(l)].get("status") == "done")
        log(work, "chunk of %d: %d done, %d again, %d failed; %.0fs of speech in %.0fs; %d left"
            % (len(part), done, len(again), sum(state[key(l)].get("status") == "failed" for l in part), sec, time.time() - t0, len(todo)))
    json.dump(state, open(sp, "w"), indent=0)


if __name__ == "__main__":
    main()
