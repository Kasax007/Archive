# Archiv – Gedächtnis für Videos, Material und Ablage

Dieses Repo (`Kasax007/Archive`, lokal `/home/user/archive`, Branch `main`) ist die Ablage für alles rund um den
Mod Challenge Craft, das nicht in den Mod-Code gehört. Das Projektwissen zum Mod selbst (Bob, Training, Tests,
Branches, Vorlieben des Nutzers) steht in **`memory/challenge-craft-projekt.md`**: zu Beginn jeder Sitzung lesen, nach wichtigen Änderungen aktualisieren.
Im Mod-Repo ist `CLAUDE.md` vom Nutzer per `.gitignore` ausgeschlossen (seine lokale Datei) – dort nichts einchecken.

## Regeln für dieses Repo

- **Was hierher gehört:**
  - Alle Videos, Clips, Untertitel, Sprachspuren, Post-Texte und Werkzeuge der Videoproduktion.
  - Rohmaterial (`footage/`), Standbilder, CurseForge-Texte, Logs und Recherche.
  - Video-Material kommt **nicht** in den Mod-Branch. Ausnahme: der Film-Harness `src/film`, weil er mit dem Mod
    kompiliert wird.
- **Dateigröße:**
  - Jede Datei unter 95 MB. GitHub lehnt ab 100 MB ab und warnt ab 50 MB.
  - Git LFS ist nicht installiert. GitHub-Releases darf eine Sitzung nicht anlegen (HTTP 403).
  - Lange Videos deshalb verlustfrei in zwei abspielbare Hälften teilen:
    `ffmpeg -i x.mp4 -c copy -map 0 -f segment -segment_times 235 -reset_timestamps 1 -segment_start_number 1 x_part%d.mp4`.
    Das Zusammenfügen steht in `longform/README.md`.
  - Die ganzen Dateien bekommt der Nutzer zusätzlich im Chat.
- **Pushen:**
  - Vorher `git fetch origin main`.
  - Große Mengen in mehreren Commits und Pushes (je höchstens ~400 MB).
  - Keine Einzelbilder ins Repo: Footage als MP4 pro Szene, CRF 15–18.
- **Commits:** Immer mit dem Footer der Sitzung. Keine Modellnamen in Dateien, Commits oder Videos.

## Inhalt

| Ordner | Inhalt |
| --- | --- |
| `shorts/v1`, `v2`, `v3`, `v5.1` | Die Shorts (Challenges, Casino, Blackjack-ums-Leben, Random Chunks, Story); `PLAN-v3.md` |
| `shorts/tools` | Schnitt (`cut.py`, `v3lib.py`), SFX (`sfx.py`), Stimme der Shorts (`tts_v3.py`, Chatterbox) |
| `longform/` | Long-form Showcase v1 (7:50, 9:16). Siehe `longform/README.md` |
| `footage/<gruppe>/` | Rohmaterial, eine MP4 pro Szene (`chal`, `casino`, `ui`, `cards`, `long`; `tama` für den Tamagotchi-Mod, `tama2` mit Ton-Protokoll je Shot: `<shot>.sounds.jsonl`, `<shot>.shot.json`) |
| `tamagotchi/` | Videos zum Mod Tamagotchi (Short, 2-Minuten-Showcase, Review-Schnitt mit echten Spielgeräuschen), Werkzeuge, Endkarten. Siehe `tamagotchi/README.md` |
| `fonts/` | Schriften für Untertitel und Titel (vor dem Rendern nach `$SP/fonts` kopieren) |
| `motion/` | Remotion-Projekt (Motion Graphics für Story 5.1) |
| `stills/`, `research/`, `curseforge/` | Kontaktbögen, Recherche, Mod- und Modpack-Beschreibung, Changelog |
| `memory/` | Langzeitgedächtnis: `challenge-craft-projekt.md` (Mod, Bob, Training, Regeln, Vorlieben des Nutzers) |
| `Testrun Lockout against Bob` | Log einer Runde des Nutzers gegen Bob |

## Was der Nutzer bei Videos will

- **Format:** Englisch, 1080×1920, 30 fps, für TikTok und YouTube.
- **Lieferung:**
  - Eine Fassung mit eingebrannten Untertiteln und eine ohne.
  - Dazu SRT, die reine Sprachspur und einen Post-Text mit Hashtags und Musik-Credit.
  - Beim Long-form zusätzlich je mit und ohne Musik.
- **Shorts:**
  - Junge Zielgruppe, schneller Schnitt, Hook in der ersten halben Sekunde.
  - Seit V3: weniger Zoom (höchstens 1,08, Punch-Zoom bis 1,12 nur an Höhepunkten).
  - Volle Sätze statt Schlagwort-Fetzen, Stimme wie ein begeisterter Creator.
  - Ende mit CTA „Challenge Craft – free on CurseForge“.
- **Long-form:**
  - Showcase-Perspektive („schau mal, cooler Mod“), keine Entwickler-Ich-Perspektive.
  - 5–10 min, erzählt als Geschichte in ganzen Sätzen.
  - Kapitel: How it works, Progression, The Challenges, Casino, Play Together, Meet Bob.
  - Ende: „Free on CurseForge – Link in Description“ (eigene Endkarte in `longform/stills/`).
- **Bild:** Der Spieler muss in jeder Szene sichtbar sein, nichts Gewolltes darf fehlen. Jeden Shot vor dem Schnitt
  per Kontaktbogen prüfen.
- **Bob:** Immer als „early stage of development“ darstellen.
- **Links:**
  - Mod: `https://www.curseforge.com/minecraft/mc-mods/challenge`.
  - Modpack: `https://www.curseforge.com/minecraft/modpacks/challenge-craft`.

## Produktions-Pipeline (Stand Long-form v1)

1. **Sprechtext:** `longform/tools/script.py`. Ein Absatz = eine Einheit, `*Wort*` = farbiges Akzentwort in den
   Untertiteln. Zahlen ausschreiben.
   - Problemwörter: „croupier“ als „dealer“ sprechen, „Jetons“ als „chips“.
2. **Stimme:** Kokoro TTS (Open Source).
   - Stimme `am_michael`, `speed=0.95`, im Builder ×1,06 (`atempo`).
   - Sie passt in der Tonhöhe (~116 Hz) zum Sprecher der Shorts (~119 Hz, `vo3/ref.wav`).
   - Jeden Absatz mit faster-whisper prüfen.
   - Chatterbox (Stimme der Shorts) sprach mit 4–5 Wörtern pro Sekunde zu schnell und war auf der CPU viel zu
     langsam; es wurde aus dem Scratchpad entfernt.
3. **Footage:**
   - Filmen mit dem Film-Harness im Mod-Repo: `./gradlew runFilm -Pfilm=… -PfilmOut=…`, höchstens eine Film-JVM.
   - Die Bilder liegen als `$SP/film/<gruppe>/<shot>/f%05d.jpg`. Aus dem Archiv wiederherstellen:
     `ffmpeg -i footage/x/y.mp4 -q:v 2 f%05d.jpg`.
   - **Achtung:** Zwei Takes in einem Ordner (PNG + JPG) ergeben Flackern.
4. **Schnitt:** `longform/tools/showcase.py` mit `longlib.py`.
   - Beats beginnen auf Phrasen des Sprechtexts; im Schnitt ca. 3,4 s pro Clip.
   - Untertitel in Satzstücken, Kapiteltitel oben.
5. **Ton:**
   - Spiel-SFX werden unter der Stimme geduckt.
   - Musik etwa 14 dB unter der Stimme, in Pausen lauter; loudnorm, Ausgabe +2 dB (~−14 LUFS).
   - Prüfung: Whisper auf dem Mix, Ziel über 99 % Wörter.
6. **Render:** Parallel (`LONG_WORKERS=4`, `LONG_CRF=27`, preset slow). Bilder mit und ohne Untertitel entstehen
   im selben Durchgang. Danach Kontaktbogen ansehen und Flacker-Check machen (Bilddifferenzen; siehe Verlauf
   v1 in `longform/README.md`).
7. **Musik:** Kevin MacLeod (incompetech.com), CC BY 4.0. Der Credit gehört in die Beschreibung.
   - incompetech ist erreichbar, Pixabay und Chosic sind gesperrt (403).

## Arbeitsumgebung (Cloud-Container, flüchtig)

- **Scratchpad:**
  - `SP=/tmp/claude-0/-home-user-Kasax-Challenge-Craft/<session>/scratchpad`.
  - Dort liegen nur Arbeitskopien (Frames, `tts`-venv mit Kokoro und faster-whisper, `hf`-Modelle, Ausgaben). Sie
    gehen beim Zurücksetzen verloren.
  - Was bleiben soll, ins Archiv.
- **Ressourcen:**
  - Plattenplatz knapp halten: Zwischenstände löschen, `df -h /` prüfen.
  - Höchstens 2 JVMs gleichzeitig.
  - Nie `pkill -f <muster>` mit einem Muster aus dem eigenen Befehl.
- **Fehlende Werkzeuge:** Kein `ffprobe` (Dauer mit `ffmpeg -i x 2>&1 | grep Duration`), kein drawtext (Text mit
  PIL zeichnen).
