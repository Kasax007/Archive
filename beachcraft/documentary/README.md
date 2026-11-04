# Beach Craft 3.0 – Doku „Tides of the Deep“

Eine lange, ruhige Doku über Beach Craft 3.0.0 (Fabric-Mod `raft`, Minecraft 26.3) für den Autor des Mods: die Biome
des Endless Sea, alle 19 Strukturen mit dem Loot ihrer Kisten, die Kreaturen, alle 337 Blöcke und Items (mit Namen)
samt Funktion, und am Ende der Weg eines Spielers durch die ganze Story bis zum Leviathan. Englisch, 1080×1920,
30 fps, 18:35 min, echte Spielgeräusche der Aufnahme, leise Musik von Kevin MacLeod.

Gerendert wurde nach Entscheidung des Nutzers **nur die Fassung mit eingebrannten Untertiteln und mit Musik** (keine
Fassung ohne Untertitel, keine ohne Musik).

| Datei | Inhalt |
| --- | --- |
| `beachcraft3_documentary_part1.mp4` | Teil 1 von 4 (ab 0:00), 73,9 MB – Untertitel eingebrannt, mit Musik |
| `beachcraft3_documentary_part2.mp4` | Teil 2 von 4 (ab 4:38), 68,6 MB – Untertitel eingebrannt, mit Musik |
| `beachcraft3_documentary_part3.mp4` | Teil 3 von 4 (ab 9:17), 94,5 MB – Untertitel eingebrannt, mit Musik |
| `beachcraft3_documentary_part4.mp4` | Teil 4 von 4 (ab 13:56), 59,7 MB – Untertitel eingebrannt, mit Musik |
| `beachcraft3_documentary.srt` | Untertitel (fallen in der Pipeline ohnehin an) |
| `beachcraft3_documentary_voice.m4a` | reine Sprachspur |
| `beachcraft3_documentary_post.txt` | Titel, Beschreibung mit Kapitelmarken, Link, Musik-Credits, Hashtags |
| `beachcraft3_documentary_contact_sheet.png` | Kontaktbogen (alle 6 s ein Bild) |
| `stills/endcard.png` | Endkarte |
| `tools/` | Sprechtext, Aufnahme-Skripte, Schnitt (siehe unten) |

Das Video ist über 95 MB und deshalb verlustfrei in abspielbare Teile geteilt. Zusammenfügen:
`printf "file '%s'\n" beachcraft3_documentary_part*.mp4 > l.txt && ffmpeg -f concat -safe 0 -i l.txt -c copy beachcraft3_documentary.mp4`.

## Kapitel

1. **Opening** – das Endless Sea von oben (Saltmere), Stadt, Graben.
2. **The Way In** – Treibholz-Stümpfe am Overworld-Strand, Portalrahmen, Anzünden mit dem Energy Staff, Reise,
   Ankunftsplattform.
3. **The World** – Ozean über/unter Wasser, Kelpwald, Korallen-Flachwasser, Leuchtlagune, versunkener Schelf
   (Port Solace), Abyssal Trench, Wrack-Friedhof, Eisschollen, Palmen-, Dschungel- und Vulkaninseln, Riesenmuschel
   (öffnen, Perle), Seeigel/Blasenquelle.
4. **Places** – Leuchtturm, Saltmere, Helix-Station, Port Solace, Ashen Forge, Korallentempel, Abyssal Sanctum und die
   zwölf kleinen Strukturen (Galeone, Frachter, Fischerboot, Piratenbucht, Bohrinsel, Flugzeug, Ruinen,
   Schiffbrüchigen-Lager, verlassenes Floß, Eisberg-Station, Strandbar, Bojenfeld); bei den Kisten blendet der Schnitt
   den echten Inhalt ein („IN THE CHEST“, aus der gespeicherten Welt gelesen, `tools/loot.py`).
5. **Creatures** – Hai, Hammerhai, Wal (Almanach-Seite), Mantas, drei Quallen, Anglerfisch, Muräne, Krabben (graben
   sich ein), Glutkrabbe (setzt in Brand), Möwe, Pinguine, Seeotter, Drowned Corsair (Porträts auf einer Sandbühne
   unter Wasser, dazu frei schwimmende Clips).
6. **Blocks and Items** – alle Creative-Tabs als Ausstellung mit Namen (21 Bilder), dann Funktionen: Expedition Raft
   (setzen, fahren, Upgrades, Menü), Boote, Taucherausrüstung mit Luftanzeige, Helmlampe, Anzug, Kompressor,
   Harpune, Sea Scooter, Schiffskanone, Windturbine und Batterie, Sitzen und Hängematte, Lichter bei Nacht, Purifier,
   Grill, Beete, Maschinen, Almanach, Terminal, Funkgerät.
7. **The Story** – Kiste des Schiffbrüchigen, Journal, Logbuch von Tobias Fenn, Korallen-, Perlen-, Sturm- und
   Glut-Siegel (jeweils die echte Kiste), Altar schmiedet den Schlüssel, Tide Seal öffnet sich, Kuppel, Leviathan
   (Erwachen, Kreisen, Brine Bolts, Sprung und Stranden, Brüllen mit Tidelings, Tod), Herz der Flut, Tidebreaker,
   letzte Journalseite „Calm Seas“.

## Aufnahme

Gefilmt mit dem skriptbaren Spieltest des Mods (`Kasax_Raft_Mod/tools/bctest/run.sh`). Für die Doku bekam
`src/gametest/.../BcScript.java` neue Befehle (Branch `26.3`):

- `rec <name> <frames> <fps> [optionen]` nimmt einen Clip auf: Bild i zeigt die Spielzeit i/fps (die Ticks laufen
  dazwischen, jedes Bild mit seinem Teil-Tick, also flüssig). Kamerafahrten werden vor jedem Bild auf dem Client
  gesetzt: `to=`/`by=` (Fahrt; mit gleichem Start und Ziel bleibt der Spieler fest stehen), `orbit=` (Kreis),
  `look=<entity>` mit `chase=`, `yawoff=`, `pitch=` (Tier verfolgen). Zeilen `@<bild> <befehl>` laufen vor diesem
  Bild. Dazu `sounds.jsonl`/`shot.json` (welche Geräusche das Spiel spielte, für den Ton im Schnitt).
- `still` (Standbild größer als das Fenster, 1350×2400, für langsame Zooms), `open`/`keep` (eine Welt über mehrere
  Läufe weiterverwenden: `saves/bcdoc`, Seed `beachcraft`), `deadline`, `pose`, `face`, `lookat`, `faceblock`,
  `nearblock`, `openbe`, `openloot` (die nächste Kiste mit einer Loot-Tabelle öffnen), `tpbiome`, `scout`
  (Bounding-Box einer Struktur), `chests`, `find`, `press`/`release`/`key`, `click`, `arrow`, `chat`, `fov`, `gamma`,
  `fly`, `third on|off|front`.
- Mixins nur im Testpaket: `SoundLogMixin` (Ton-Protokoll), `NoRenderMixin` (zeichnet die Zwischenbilder der Ticks
  während `rec`/`wait` nicht), `UserMixin` (immer derselbe Spieler „Castaway“ mit Steve-Skin).

Die Läufe stehen in `tools/runs.py` (je eine Funktion, unter 20 Minuten), die Bausteine in `tools/film.py`, die
Ausstellung in `tools/museum.py` (Namen kommen im Schnitt dazu, `tools/labels.json`). Verwendet wurde Material aus
r04–r07, r11–r13 und r21–r23 (r21–r23 fassen mehrere Funktionen in einem Spielstart zusammen: Museum + Leviathan,
Overworld + Deck-Demos, Kreaturen + Altar/Siegel). r03, r10 und r16 lieferten kein brauchbares Material.

Lehren aus den Läufen (für das nächste Mal):

- Nach `fill`/`setblock` vor dem nächsten Bild ein `settle` – sonst zeigt das Bild die alten Chunk-Meshes (r16 filmte
  so zehn Porträts im „alten“ Riff). Auch `settle` direkt nach einem weiten Teleport kann zu früh fertig sein
  (Mangroven-Insel blieb leer).
- `faceblock` + `use` zwischen nicht gezeichneten Ticks trifft oft nichts (Terminal, Almanach); dieselbe Aktion
  innerhalb eines `rec` (Bilder dazwischen) klappt.
- In der dritten Person steht das Ziel genau hinter dem Kopf des Spielers – immer mit `yawoff`/seitlichem Standpunkt
  arbeiten; enge Räume (Kuppel-Eingang, Tresorräume) schieben die Kamera in den Kopf.
- `chat on` setzt die Chat-Sichtbarkeit nur im Client: der Server schickt Systemnachrichten (Funkgerät) trotzdem nicht,
  solange die Optionen nicht an den Server gemeldet werden.
- Der feste Spieler in `rec ... to=` springt bei Rückstoß für ein paar Bilder; `tools/deglitch.py` ersetzte diese
  Bilder vor dem Kodieren durch das Bild davor (`tools/trim.py` schneidet Clips zu).

`tools/ingest.py` legt Standbilder nach `$SP/doc3/shots` und Clips als MP4 (CRF 16) mit Ton-Protokoll nach
`footage/bc3/`. Die Standbilder liegen je Kapitel als MP4 in `footage/bc3/stills_<kapitel>.mp4` (ein Bild pro
Standbild, Reihenfolge in `stills_<kapitel>.json`).

```sh
cd /home/user/Kasax_Raft_Mod
python3 /home/user/Archive/beachcraft/documentary/tools/runs.py r21 $SP/doc3/scripts/s21.txt
BC_TIMEOUT=1320 BC_XMX=4G tools/bctest/run.sh $SP/doc3/scripts/s21.txt $SP/doc3/runs/r21
python3 -I /home/user/Archive/beachcraft/documentary/tools/ingest.py $SP/doc3/runs/r21
python3 -I /home/user/Archive/beachcraft/documentary/tools/loot.py      # Kisten-Inhalt -> tools/loot.json
```

## Schnitt

```sh
SP=<Scratchpad>; export SP HF_HOME=$SP/hf FONTS=/home/user/Archive/fonts
$SP/tts/bin/python tools/tts_kokoro.py doc        # Stimme: Kokoro am_michael, speed 0.92, jeder Absatz mit Whisper geprüft
python3 -I tools/endcard.py                       # Endkarte
$SP/tts/bin/python tools/doc.py --plan            # Schnittplan
DOC_WORKERS=4 $SP/tts/bin/python tools/doc.py --deliver
```

`tools/doc.py`: Die Stimme führt, die Shots hängen an Phrasen (`tools/script.py`; ein Anker `@5` heißt „5 s nach
Absatzbeginn“, so liegen die Ausstellungsbilder gleichmäßig). Standbilder laufen mit langsamem Zoom, Menüs sind
vergrößert (`tools/shots.json`, dort auch Startzeiten der Clips), Clips werden auf 30 fps gebracht und bei Bedarf bis
0,6× verlangsamt. Weiche Überblendungen, an Kapitelanfängen über Schwarz. Über den Ausstellungsbildern stehen die
Untertitel oben, auf der Endkarte keine (die sagt dasselbe). Ton: Stimme, die echten Spielgeräusche der Clips (unter
der Stimme geduckt), Musik etwa 20 dB unter der Stimme, in Pausen lauter, loudnorm −14 LUFS.

Musik: Kevin MacLeod (incompetech.com), CC BY 4.0: „Music for Manatees“, „Infinite Perspective“, „Jellyfish in Space“,
„Wholesome“, „Enchanted Journey“, „Thunderbird“, „Eternal Hope“ (Quelle: `https://incompetech.com/music/royalty-free/mp3-royaltyfree/<Titel>.mp3`).
