# Beach Craft 2.0.1 – Review-Video

Ein Review des Mods Beach Craft (Raft) für Minecraft 26.3. Es zeigt und erklärt jedes Feature einmal, damit man
prüfen kann, was entwickelt wurde und ob alles funktioniert. Format: rund 5 min, 1080×1920, 30 fps, Englisch.
Der Ton enthält die echten Spielgeräusche der Aufnahme, Musik nur leise darunter. GUI-Shots sind vergrößert.
Die Prüfergebnisse stehen in `REPORT.md`: Was funktioniert, welche Fehler behoben wurden und welche Design-Fragen
offen sind.

| Datei | Inhalt |
| --- | --- |
| `beachcraft_review_captions_music.mp4` / `_captions_nomusic.mp4` | Untertitel eingebrannt, mit / ohne Musik (über 90 MB als `_part1` / `_part2`) |
| `beachcraft_review_clean_music.mp4` / `_clean_nomusic.mp4` | ohne Untertitel |
| `beachcraft_review.srt`, `beachcraft_review_voice.m4a` | Untertitel, reine Sprachspur |
| `beachcraft_review_post.txt` | Titel, Beschreibung, Link, Musik-Credit („Hep Cats“, Kevin MacLeod, CC BY 4.0), Hashtags |
| `beachcraft_review_contact_sheet.png` | Kontaktbogen |
| `stills/endcard_review.png` | Endkarte |
| `REPORT.md` | Prüfbericht (Deutsch) |

Geteilte Hälften wieder zusammenfügen:
`printf "file '%s'\n" x_part1.mp4 x_part2.mp4 > l.txt && ffmpeg -f concat -safe 0 -i l.txt -c copy x.mp4`.

## Neu bauen

Die Werkzeuge stammen aus `dreamcraft/tiktok/tools`. `bc.py` erzeugt den Review-Schnitt: Jeder Shot läuft am Stück,
GUI-Shots werden per `GUI_ZOOM` vergrößert, `SKIP` schneidet unbrauchbare Startbilder ab. `gamesound.py` mischt die
Spielgeräusche aus den Ton-Protokollen der Aufnahme. Der Sprecher ist Kokoro `am_michael` (0,95, im Schnitt ×1,06).

```sh
SP=<Scratchpad>; export SP HF_HOME=$SP/hf VIRTUAL_ENV=$SP/tts
$SP/tts/bin/python tools/tts_kokoro.py review      # Stimme (Absatz für Absatz mit Whisper geprüft)
python3 -I tools/endcard.py                         # Endkarte (Kacheln: raft_tour, shark_attack, crops, portal_light)
$SP/tts/bin/python tools/bc.py --plan               # Schnittplan
DC_WORKERS=4 $SP/tts/bin/python tools/bc.py --deliver
```

## Aufnahme

Gefilmt wird mit dem Film-Harness im Modpack-Repo (`Modpack-Development`, Branch `26.3`, `tools/dctest`, Shots in
`BcShots.java`):
`sh ./gradlew runPack -Pxmx=5G -Pscene=film -Pshots=bc_beach,… -Prd=12 -Pout=$SP/film/bc`.
Lange Läufe gehen in Batches zu 5–7 Shots. Das Rohmaterial liegt als MP4 pro Shot in `footage/bc`, jeweils mit
`<shot>.sounds.jsonl` (Ton-Protokoll). Zurück zu Einzelbildern: `ffmpeg -i footage/bc/x.mp4 f%05d.png`.

Beim Filmen fiel ein echter Fehler auf: Das Paddel schob das Boot nicht. Er ist in Beach Craft 2.0.1 behoben.
Außerdem zeigte die Kamera die Steinmassive der Raft-Dimension. Das ist kein Fehler, sondern eine Design-Frage, siehe
`REPORT.md`.

Fehler des Harness selbst:

- Maus-Klicks unter SDL: Maustaste 1 ist dort links.
- Ein Speicherleck bei Screenshots.
- Halbe Blöcke bei negativen Koordinaten.

Alles Weitere steht in `memory/dreamcraft-projekt.md`.
