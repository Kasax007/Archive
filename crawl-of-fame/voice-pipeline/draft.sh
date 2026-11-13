#!/bin/sh
# Placeholder speech for the game side of the voice work: draft.sh <text file> <out wav | out dir> [voice]
# (a text file of lines "id<TAB>text" writes one wav per id into the out dir). Voices: am_michael am_fenrir bm_george af_heart bf_emma ...
D=$(cd "$(dirname "$0")" && pwd)
OMP_NUM_THREADS=2 exec nice -n 10 "$D/q312/bin/python" "$D/draft_k.py" "$@"
