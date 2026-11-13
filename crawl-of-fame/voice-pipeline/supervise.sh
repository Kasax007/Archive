#!/bin/bash
# Keeps the voice recording going in the background: announcer tier 1, then tier 1 of everybody, tier 2, tier 3;
# looks again every ten minutes (the script may have grown). Files in the work folder steer it:
#   repo.txt  the repo whose script and cast are read (tools/content/voice)      PAUSE  wait
#   STOP      the running pass ends after its chunk (removed by this script)      QUIT   end this script
SP=/tmp/claude-0/-home-user/e2686f39-d632-56d3-aa9e-a2a2f832009c/scratchpad
W=$SP/voice/work
cd "$SP/voice/synth" || exit 1
# an earlier pass started by hand: let it finish its chunk first
if [ -n "$1" ]; then while kill -0 "$1" 2>/dev/null; do sleep 20; done; fi
rm -f "$W/STOP"
while true; do
  [ -f "$W/QUIT" ] && exit 0
  if [ -f "$W/PAUSE" ]; then sleep 30; continue; fi
  REPO=$(cat "$W/repo.txt")
  for pass in "--speaker emcee --tier 1" "--tier 1" "--tier 2" "--tier 3"; do
    [ -f "$W/QUIT" ] && exit 0
    [ -f "$W/PAUSE" ] && break
    # two threads: the engineers' Minecraft runs keep two cores
    THREADS=${VOICE_THREADS:-2} python3 synth.py --repo "$REPO" --out "$SP/voice/out_ogg" --work "$W" $pass --chunk 16 >> "$W/run.out" 2>&1
    if [ -f "$W/STOP" ]; then rm -f "$W/STOP"; break; fi
  done
  sleep 600
done
