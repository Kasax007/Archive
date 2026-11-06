# Beach Craft – Doku v2 „Tides of the Deep“ (3.1, Querformat, Shader)

Zweite Fassung der Doku für Beach Craft 3.1.0 (Fabric, Minecraft 26.3): Englisch, **1920×1080, 60 fps**, Shader
(Iris 1.11.7 + Sodium 0.9.2 + Complementary Reimagined r5.9.3), Sichtweite 10 (unter Wasser 6), tagsüber gefilmt
(Nacht nur für die Lichter), Kamera frei (Zuschauer) – der Spieler ist nur bei Vorführungen im Bild. Ruhiger
Sprecher (Kokoro `am_michael`, jeder Absatz mit Whisper geprüft), eingebrannte Untertitel, Musik von Kevin MacLeod
(incompetech.com, CC BY 4.0), echte Spielgeräusche aus den Ton-Protokollen der Clips (für ältere Clips auf die
Klänge von 3.1 umgelegt). Nur eine Fassung: mit Untertiteln und Musik.

Kapitel: The Way In · The World · The Places · The Creatures · Blocks and Items (in der Reihenfolge, in der ein
Spieler sie findet) · Your Own Raft (3.1) · People of the Sea (3.1, eine Person je Absatz) · The Story.

| Datei | Inhalt |
| --- | --- |
| `beachcraft3_documentary_v2_part*.mp4` | Film in abspielbaren Teilen unter 95 MB (Zusammenfügen siehe unten) |
| `beachcraft3_documentary_v2.srt` | Untertitel |
| `beachcraft3_documentary_v2_voice.m4a` | reine Sprachspur |
| `beachcraft3_documentary_v2_post.txt` | Titel, Beschreibung mit Kapitelmarken, Musik-Credits, Hashtags |
| `beachcraft3_documentary_v2_contact_sheet.png` | Kontaktbogen |
| `stills/endcard.png` | Endkarte |
| `tools/` | Sprechtext (`script.py`), Aufnahme (`film2.py`, `runs2.py`), Übernahme (`ingest2.py`, `ingest_ext.py`), Schnitt (`doc.py`), Stimme, Endkarte |

Zusammenfügen: `printf "file '%s'\n" beachcraft3_documentary_v2_part*.mp4 > l.txt && ffmpeg -f concat -safe 0 -i l.txt -c copy beachcraft3_documentary_v2.mp4`

**Neuer Schnitt 6.11. (Rückmeldung des Nutzers):** Treibholz-Stumpf (W1), Portalrahmen und Energiestab werden
gecraftet, Ring aus der Schiffswrack-Truhe und im Hochofen (W2/W3), der zerbrochene Frachter (P9), Mantas mit neuer
Stimme (B3, C0, C4), Anglerfisch beleuchtet mit Biss (C6), Muräne im Loch mit Zustoßen (C7), Krabben graben sich ein
(C8), Möwenschwarm über dem Meer und Möwen im Weizen (C10), Feld mit Vogelscheuche (I21), Taucherausrüstung neu
(I11/I13/I15: Inventar, Taucher über dem Riff, Luftanzeige groß mit Untertiteln oben), Motor startet (R0). Ton: alle
Spielgeräusche jetzt zeitrichtig (siehe Zeitbasis unten), neuer Motor als Schleife, Kampf mit dem Leviathan neu
gemischt. Whisper auf der Mischung: 99,5 %.

Rohmaterial: `footage/bc3v2/` (eine MP4 je Clip, 30 Spiel-fps, CRF 16–18, dazu `.sounds.jsonl`/`.shot.json`;
Standbilder als `stills_<lauf>.mp4`). Die NPC- und Floßbau-Clips (`n_*`, `r_*`) stammen aus einer zweiten Sitzung
(`footage/bc3v2/README_npc_raft.md`).

## Aufnahme

Welt `bcdoc2` (Seed `beachcraft`) mit dem Test-Harness des Mods (`Kasax_Raft_Mod/tools/bctest`): neu für v2 sind die
freie Kamera (`cam=`, `freecam`), Skript-Variablen (`{cx+20}` aus `scout`, `find`, `openloot … peek`, `where`,
`height`), `respawn`, und ein `settle`, das erst den Server die Chunks erzeugen lässt und dabei kaum Bilder zeichnet
(mit Shadern kostet ein Bild ~3 s). Läufe in `tools/runs2.py` (Teile ≤ 90 min, damit andere Tests den Build-Lock
dazwischen bekommen):

```sh
python3 tools/runs2.py b $SP/doc4/scripts/b.txt         # bzw. e -> e1.txt … (Teile)
BC_TIMEOUT=6600 BC_XMX=6G Kasax_Raft_Mod/tools/bctest/run.sh $SP/doc4/scripts/b.txt $SP/doc4/runs/b
python3 -I tools/ingest2.py $SP/doc4/runs/b             # Clips -> footage (30 fps) und $SP/doc4/shots (60 fps, minterpolate)
python3 -I tools/ingest_ext.py n_ r_                    # Clips der zweiten Sitzung -> $SP/doc4/shots
```

## Schnitt

```sh
export SP HF_HOME=$SP/hf FONTS=/home/user/Archive/fonts DOC_MUSIC=$SP/doc3/music
$SP/tts/bin/python tools/tts_kokoro.py doc               # Stimme (unveränderte Absätze aus v1 übernommen)
python3 -I tools/endcard.py
$SP/tts/bin/python tools/doc.py --plan                   # meldet fehlende Shots
DOC_WORKERS=3 DOC_PARTS=12 $SP/tts/bin/python tools/doc.py --deliver
# nur Teile neu: DOC_KEEP_BOUNDS=<k> DOC_ONLY=<k>,<k+1>,… (Teilgrenzen bis k bleiben gleich)
```

Höchstens 3 Render-Prozesse (je ~2 GB; mit 4 griff der OOM-Killer). Ein Teil von ~98 s brauchte ~14,5 min.

Ton (Stand 6.11., nach der Rückmeldung zum Schnitt):

- Spielgeräusche kommen aus dem Mod (`DOC_MOD=<Mod-Ordner>`, Standard `/home/user/Kasax_Raft_Mod`; für Klänge, die
  noch nicht in 26.3 sind, z. B. `DOC_MOD=/home/user/wt/raft-building`). Raft-Events, deren `sounds.json` eine
  Vanilla-Datei abspielt (Möwen, Pinguine, Otter, Tidelinge, …), waren bis 6.11. stumm; jetzt behalten die Namen
  ihren Namensraum.
- Regeln je Clip in `doc.py`: `THIN` (Tideling-Flops höchstens alle 0,7 s), `SOUND_GAIN` (Schwimmgeräusche in `s_lev*`
  −8 dB; `None` nimmt ein Event aus der Mischung).
- Motor: `raft:block.raft_motor.run` wird als Schleife gelegt (einmal je Shot, 0,7 × Entfernungsfaktor über 32 Blöcke,
  Tonhöhe 1,05, über 8 Blöcke/s 1,15). Alte Clips mit dem Bassdrum-Ticken bekommen dieselbe Schleife statt der Ticks.
- `shots.json` → `caps_top`: über diesen Shots stehen die Untertitel oben (die Luftanzeige des HUD sitzt sonst darunter).
- Standbilder gehen vor Clips: kommt ein Shot als Clip neu (z. B. `f_gauge`), vorher `$SP/doc4/shots/<name>.jpg` löschen
  (`ingest_ext.py` lässt ein vorhandenes Standbild außerdem stehen).
- **Zeitbasis:** Die Ton-Protokolle zählen Spielsekunden, die Clips laufen schneller: Beim Bildschirmfoto des Harness
  vergehen zwei Ticks pro Bild, eine Sekunde Clip (30 Bilder) zeigt also 3 s Spielzeit (74 Clips gemessen; Bisse und
  Harpunenschüsse liegen genau auf den Bildern, auf denen sie passieren). `doc.py` teilt die Protokollzeit deshalb durch
  `GAME_PER_CLIP = 3` (vorher kam jeder Ton dreimal zu spät, die meisten fielen hinter das Ende ihres Shots). Weil drei
  Spielsekunden in eine Clip-Sekunde fallen, dünnt `THIN` dichte Wiederholungen aus (Möwenflügel, Schritte, Schwimmen);
  die Spielgeräusche sind dafür leiser gemischt (`game_gain` 1,9 statt 2,6).
- Optionen je Shot in `shots.json`: `end` (Clip nur bis hier, auch der Ton), `hold` ([[a, b]]: statt der Bilder von a bis b
  das Bild bei a, z. B. ein Kamerastoß beim Treffer). Wo `minterpolate` schlimme Geisterbilder macht (Moräne), liegt die
  60-fps-Fassung in `$SP/doc4/minterp_off/` und der Schnitt nimmt die 30-fps-Aufnahme aus `footage/bc3v2`.
