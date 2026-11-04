# Beach Craft 3.0 – Doku „Tides of the Deep“

Eine lange, ruhige Doku über Beach Craft 3.0.0 (Fabric-Mod `raft`, Minecraft 26.3) für den Autor des Mods: jedes Biom,
jede Struktur mit dem Loot ihrer Kisten, jede Kreatur, jeder Block und jedes Item (mit Namen) samt Funktion, und am
Ende der Weg eines Spielers durch die ganze Story bis zum Leviathan. Englisch, 1080×1920, 30 fps, echte
Spielgeräusche der Aufnahme, leise Musik von Kevin MacLeod.

| Datei | Inhalt |
| --- | --- |
| `beachcraft3_documentary_captions_music_partN.mp4` / `_captions_nomusic_partN.mp4` | Untertitel eingebrannt, mit / ohne Musik |
| `beachcraft3_documentary_clean_music_partN.mp4` / `_clean_nomusic_partN.mp4` | ohne Untertitel |
| `beachcraft3_documentary.srt`, `beachcraft3_documentary_voice.m4a` | Untertitel, reine Sprachspur |
| `beachcraft3_documentary_post.txt` | Titel, Beschreibung mit Kapiteln, Link, Musik-Credits, Hashtags |
| `beachcraft3_documentary_contact_sheet.png` | Kontaktbogen (alle 6 s ein Bild) |
| `stills/endcard.png` | Endkarte |
| `tools/` | Sprechtext, Aufnahme-Skripte, Schnitt (siehe unten) |

Die Videos sind über 95 MB und deshalb verlustfrei in Teile geteilt (`_part1`, `_part2`, …). Zusammenfügen:
`printf "file '%s'\n" x_part1.mp4 x_part2.mp4 x_part3.mp4 > l.txt && ffmpeg -f concat -safe 0 -i l.txt -c copy x.mp4`.

## Aufnahme

Gefilmt mit dem skriptbaren Spieltest des Mods (`Kasax_Raft_Mod/tools/bctest/run.sh`). Für die Doku bekam
`src/gametest/.../BcScript.java` neue Befehle (Commit auf Branch `26.3`):

- `rec <name> <frames> <fps> [optionen]` nimmt einen Clip auf: Bild i zeigt die Spielzeit i/fps (die Ticks laufen
  dazwischen, jedes Bild mit seinem Teil-Tick, also flüssig). Kamerafahrten werden vor jedem Bild auf dem Client
  gesetzt: `to=`/`by=` (Fahrt), `orbit=` (Kreis), `look=<entity>` mit `chase=`, `yawoff=`, `pitch=` (Tier verfolgen).
  Zeilen `@<bild> <befehl>` laufen vor diesem Bild. Dazu `sounds.jsonl`/`shot.json` (welche Geräusche das Spiel
  spielte, für den Ton im Schnitt).
- `still` (Standbild größer als das Fenster, 1350×2400, für langsame Zooms), `open`/`keep` (eine Welt über mehrere
  Läufe weiterverwenden: `saves/bcdoc`, Seed `beachcraft`), `deadline`, `pose`, `face`, `lookat`, `faceblock`,
  `nearblock`, `openbe`, `openloot` (die nächste Kiste mit einer Loot-Tabelle öffnen), `tpbiome`, `scout`
  (Bounding-Box einer Struktur), `chests`, `find`, `press`/`release`, `click`, `arrow`, `chat`, `fov`, `gamma`, `fly`.
- Mixins nur im Testpaket: `SoundLogMixin` (Ton-Protokoll), `NoRenderMixin` (zeichnet die Zwischenbilder der Ticks
  während `rec`/`wait` nicht), `UserMixin` (immer derselbe Spieler „Castaway“ mit Steve-Skin; sonst wechselte der
  Skin mit jedem Start).

Die Läufe stehen in `tools/runs.py` (je eine Funktion, unter 20 Minuten), die Bausteine in `tools/film.py`, die
Ausstellung aller 337 Blöcke und Items in `tools/museum.py` (Namen kommen im Schnitt dazu, `tools/labels.json`).
`tools/ingest.py` legt Standbilder nach `$SP/doc3/shots` und Clips als MP4 (CRF 16) mit Ton-Protokoll nach
`footage/bc3/`. Die Standbilder liegen je Kapitel als MP4 in `footage/bc3/stills_<kapitel>.mp4` (ein Bild pro
Standbild, Reihenfolge in `stills_<kapitel>.json`).

```sh
cd /home/user/Kasax_Raft_Mod
python3 /home/user/Archive/beachcraft/documentary/tools/runs.py r04 $SP/doc3/scripts/s04.txt
BC_TIMEOUT=1260 BC_XMX=4G tools/bctest/run.sh $SP/doc3/scripts/s04.txt $SP/doc3/runs/r04
python3 -I /home/user/Archive/beachcraft/documentary/tools/ingest.py $SP/doc3/runs/r04
```

## Schnitt

```sh
SP=<Scratchpad>; export SP HF_HOME=$SP/hf FONTS=/home/user/Archive/fonts
$SP/tts/bin/python tools/tts_kokoro.py doc        # Stimme: Kokoro am_michael, speed 0.92, jeder Absatz mit Whisper geprüft
python3 -I tools/endcard.py                       # Endkarte
$SP/tts/bin/python tools/doc.py --plan            # Schnittplan
DOC_WORKERS=4 $SP/tts/bin/python tools/doc.py --deliver
```

`tools/doc.py`: Die Stimme führt, die Shots hängen an Phrasen (`tools/script.py`). Standbilder laufen mit langsamem
Zoom, Menüs sind vergrößert (`tools/shots.json`), Clips werden auf 30 fps gebracht und bei Bedarf bis 0,6× verlangsamt.
Weiche Überblendungen, an Kapitelanfängen über Schwarz. Ton: Stimme, die echten Spielgeräusche der Clips (unter der
Stimme geduckt), Musik etwa 20 dB unter der Stimme, in Pausen lauter, loudnorm −14 LUFS.

Musik: Kevin MacLeod (incompetech.com), CC BY 4.0: „Music for Manatees“, „Infinite Perspective“, „Jellyfish in Space“,
„Wholesome“, „Enchanted Journey“, „Thunderbird“, „Eternal Hope“ (Quelle: `https://incompetech.com/music/royalty-free/mp3-royaltyfree/<Titel>.mp3`).
