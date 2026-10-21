# Tamagotchi – Videos (Short und Long-form)

Zwei Videos über den Minecraft-Mod **Tamagotchi** (Pets finden, zähmen, pflegen). Video-Inhalt Englisch, 1080×1920,
30 fps, für TikTok und YouTube. Gleiche Regeln wie bei Challenge Craft (siehe `../CLAUDE.md`).

| Video | Länge | Inhalt |
| --- | --- | --- |
| `short/` | ca. 43 s | Hook (Drache in der Pyramide), zehn seltene Pets, Zähmen, Rucksack, Pflege, Talente, Goldener Apfel, Endkarte |
| `longform/` | ca. 2:03 | Showcase in acht Kapiteln: Finding pets, Taming, Care, Play, Backpack, Talents, Adventures, The Tamacon |

## Dateien (pro Video, nach `--deliver`)

| Datei | Inhalt |
| --- | --- |
| `*_captions_music.mp4` / `*_captions_nomusic.mp4` | Untertitel eingebrannt, mit / ohne Musik (ohne Musik: Stimme + Pet-Sounds) |
| `*_clean_music.mp4` / `*_clean_nomusic.mp4` | ohne Untertitel, mit / ohne Musik |
| `*.srt`, `*_voice.m4a` | Untertitel, reine Sprachspur |
| `*_post.txt` | Titel, Beschreibung, Link, Musik-Credit, Hashtags |
| `*_contact_sheet.png` | Kontaktbogen zur Prüfung |
| `stills/endcard_short.png`, `endcard_long.png` | die Endkarten (im Video leicht animiert) |

Dateien über 90 MB würden automatisch in zwei Hälften geteilt (`*_partN.mp4`, Zusammenfügen wie in
`../longform/README.md`). Bei diesen Längen bleiben sie darunter.

## Neu bauen

Voraussetzungen (alles unter `$SP/video/`, flüchtig): Python-3.12-venv `tts` mit `kokoro`, `soundfile`, `faster-whisper`,
`pillow`, `numpy`; `av` auf 16.x festnageln (`av` 19 passt nicht zu faster-whisper); `VIRTUAL_ENV` muss beim ersten Lauf
gesetzt sein, weil misaki sein spaCy-Modell per `uv pip` nachlädt.

```sh
SP=<Scratchpad>; export SP HF_HOME=$SP/video/hf VIRTUAL_ENV=$SP/video/tts
uv venv --python 3.12 $SP/video/tts
uv pip install kokoro soundfile faster-whisper pillow numpy "av==16.1.0"
PY=$SP/video/tts/bin/python; cd tamagotchi/tools

$PY tts_kokoro.py short ; $PY tts_kokoro.py long      # Stimme, jeder Absatz mit Whisper geprüft
$PY endcard.py                                         # Endkarten
$PY tama.py all --plan                                 # nur Schnittplan (Footage muss in $SP/film/tama liegen)
$PY tama.py all --deliver                              # alles rendern und nach short/ und longform/ kopieren
```

`tama.py short|long|all` mit `--audio` (nur Ton, SRT, Prüfung), `--placeholder` (farbiges Test-Footage, nichts wird
ausgeliefert), `--fill-missing` (fehlende Shots testweise ersetzen), `--film DIR` (anderes Footage).
Rendern: ca. 5 min (Short) und 15 min (Long) auf 4 Kernen (`TAMA_WORKERS`).

## Aufbau der Werkzeuge (`tools/`)

- `script.py`: Sprechtext, Kapiteltitel, Shot-Zuordnung je Absatz, Aussprache (`SAY`), Post-Texte. `*Wort*` = Akzentwort.
- `tts_kokoro.py`: Kokoro `am_michael`, `speed=0.95`, im Builder ×1,06 (`atempo`) wie bei Challenge Craft.
  Jeder Absatz wird mit Whisper (small.en) geprüft und bei Fehlern mit anderem Tempo neu gesprochen.
  Namen wie „Tamagotchi“, „Tamacon“, „Tama Pager“ stehen als IPA in `SAY` (sonst „tarmac on“).
- `tama.py`: Stimme → Wortzeiten → Untertitel in Satzstücken (nie über Absatzgrenzen) → Schnittplan → Ton → Render.
  Zoom höchstens 1,08 (Punch bis 1,12 nur beim Hook), Schnitt alle 1,5–3,5 s.
  Ein Shot, der länger gebraucht wird als vorhanden, wird auf mindestens 0,7× verlangsamt, dann gehalten;
  mehrfach genutzte Shots starten an anderen Stellen des Materials.
- `cut.py`, `v3lib.py`, `sfx.py`: aus den Challenge-Craft-Werkzeugen übernommen. Sounds kommen aus dem Mod
  (`assets/tamagotchi/sounds`, Env `TAMA_SOUNDS`), Untertitelschrift aus `../fonts`.
- `endcard.py`: Endkarte im Tamagotchi-Stil aus dem CurseForge-Header des Mod-Repos.
- `placeholder.py`: Test-Footage, `check.py`: Whisper-Abgleich.

## Footage-Konvention

`$SP/film/tama/<shot>/f00000.jpg …`, 30 fps, 1080×1920, 3–6 s je Shot. Optionale Shots (nur genutzt, wenn der Ordner
existiert): `jungle_wild` (Jungle Dragon im Tempel) und `monument_wild` (Tide Dragon am Ozeanmonument) im Long-form-Kapitel
Finding pets. `endcard` wird von `endcard.py` erzeugt. Zwei Takes in einem Ordner ergeben Flackern; `tama.py` prüft
das fertige Video darauf.

## Musik

Kevin MacLeod (incompetech.com), „Itty Bitty 8 Bit“, CC BY 4.0. Der Credit steht in den `*_post.txt` und gehört in die
Beschreibung. Die Musik liegt rund 14 dB unter der Stimme, in Pausen lauter; Ausgabe loudnorm ca. −14 LUFS.

## Offen

- Der CurseForge-Link `…/mc-mods/tamagotchi` ist eine Annahme (TODO-Zeile am Anfang der Post-Texte).
