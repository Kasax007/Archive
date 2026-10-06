# Shorts V3, Short 5 und 5.1 (Motion Graphics) — Plan, Werkzeuge, Stand

> **Für jeden Agenten, der hier weiterarbeitet:**
>
> - Erst dieses Dokument ganz lesen, dann im Abschnitt **Stand** weitermachen.
> - Nach jedem erledigten Schritt hier den Haken setzen und eine Zeile ins **Protokoll** schreiben.
>   Danach committen und pushen (Repo `/home/user/archive`, Branch `main`).
> - Bei einem Abbruch (Token-Limit, Absturz) übernimmt so der Nachfolger nahtlos.
> - Werkzeuge und Regeln der V2 stehen in `/home/user/bob-dev/docs/marketing/shorts-v2-plan.md`.
>   Erst diesen Plan lesen, dann den V2-Plan für die Technik (`cut.py`, `v2lib.py`, SFX,
>   Chatterbox, `vo/sync.py`, Rendern).

## Auftrag (vom Nutzer, sinngemäß)

Die vier Shorts (V2) sind grafisch sehr gut. Nach nochmaligem Ansehen will der Nutzer Folgendes
geändert haben:

1. **Weniger Zoom.** Der Zoom-Effekt ist manchmal zu stark.
2. **Text in vollen Sätzen.** Untertitel und Sprecher sollen nicht mehr in Schlagwort-Fetzen
   sprechen, sondern flüssig in ganzen Sätzen.
3. **Die Stimme soll wie ein Mensch klingen, der etwas erzählt und verkauft** – „übertrieben
   gesagt, ein Sales Pitch“. Ein zusammenhängender, mitreißender Text mit Übergängen
   („And here's the best part…“, „But it gets worse…“), kein Vorlesen von Einzelzeilen.
4. **V3 aller vier Shorts:** `challenges`, `casino`, `blackjack_life`, `random_chunks`.
5. **Ein fünfter Short über Geschichte und Story des Mods**, eher dokumentarisch und kreativ
   umgesetzt:
   - Ausgangspunkt: Man hat die viralen YouTube-Challenges gesehen, konnte sie aber nie selbst
     spielen.
   - Dann: Wie Challenge Craft entstanden ist und gewachsen ist.
6. **Version 5.1:** wo es Sinn ergibt, eine zusätzliche Fassung mit Motion Graphics, z. B.:
   - animierte Titelkarten;
   - Zähler „1 → 50 Challenges“;
   - eine Zeitleiste;
   - Kinetic Typography;
   - ein animierter Level-Baum oder eine XP-Leiste;
   - ein Casino-Chip-Regen.

   Mindestens Short 5 bekommt eine 5.1; die anderen nur, wo es den Short wirklich besser macht.
7. **Alles ablegen** im Archiv-Repo `Kasax007/Archive` (lokal `/home/user/archive`).

## Feste Regeln

- **Keine Java-/Minecraft-Prozesse starten.** Auf der Maschine laufen Bob-Benchmarks; höchstens
  zwei JVMs sind erlaubt und beide sind belegt. Also kein neues Filmen: Es gibt nur das
  vorhandene Material.
- **Nichts im Repo `Kasax_Challenge_Craft` ändern.** Skripte, Projekte und Ergebnisse gehören ins
  Archiv-Repo.
- **Keine Modellnamen** in Dateien, Commits oder Videos.
- **Commit-Fußzeile** für jeden Commit im Archiv-Repo:

  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01Y6AzZnzN36nEmDk7YFdyve
  ```

- **Dateien unter 95 MB** (GitHub-Grenze 100 MB). Keine Einzelbilder ins Repo; Videos als MP4.
- **Plattenplatz ist knapp** (wenige GB): Zwischenstände löschen. `df -h /` im Blick behalten.
- **Lange Befehle** (TTS, Rendern) im Hintergrund oder in Stücken von höchstens 10 min.
- **Format:**
  - englisch, 1080×1920, 30 fps;
  - je Short eine Fassung mit eingebrannten Untertiteln (`_final`), eine ohne (`_clean`), die
    SRT-Datei und die reine Sprachspur (`_voice.m4a`).

## Material

### Footage

- **Archiv:** `/home/user/archive/footage/<gruppe>/<shot>.mp4` (30 fps, CRF 15). Gruppen:
  - `chal/` – die Challenges;
  - `casino/`;
  - `ui/`;
  - `cards/`;
  - `survey2/`.
- **Lokal:** Solange die Einzelbilder noch unter
  `/tmp/claude-0/-home-user-Kasax-Challenge-Craft/2061deb3-7247-5b5c-aa62-6c43681c8da7/scratchpad/film/<gruppe>/<shot>/f%05d.jpg`
  liegen, liest `cut.py` sie direkt.
- **Wenn die Einzelbilder gelöscht sind** (Platz): nur die gebrauchten Shots aus dem MP4 entpacken,
  mit `ffmpeg -i shot.mp4 -q:v 2 dir/f%05d.jpg`. Oder `cut.py` so anpassen, dass es aus MP4 liest.

### Weitere Bausteine

- **Standbilder:** `/home/user/archive/stills/`.
- **Bisherige Fassungen zum Vergleich:** `/home/user/archive/shorts/v1/`, `/home/user/archive/shorts/v2/`.
- **Schnitt-, SFX- und VO-Skripte** aus V1/V2:
  - im Mod-Repo unter `/home/user/bob-dev/scripts/film/` (`cut.py`, `v2lib.py`, `vo/*`, die
    Short-Skripte);
  - im Scratchpad unter `edit/` und `vo/`.

  Zum Arbeiten ins Archiv kopieren, nach `shorts/tools/`.
- **Geschichte des Mods (für Short 5):**
  - `git -C /home/user/Kasax_Challenge_Craft log --reverse --date=short --format="%ad %s"`;
    erster Commit am 24.04.2025 („Added challenges“), heute über 297 Commits;
  - die Branches zeigen die Minecraft-Versionen: 1.21.5 → 26.1.2 → 26.2 → 26.3;
  - die Konzepte in `/home/user/Kasax_Challenge_Craft/docs/` (`konzept-the-house-always-wins.md`,
    `konzept-bot.md`, `bob-plan.md`);
  - die CurseForge-Texte in `docs/curseforge/`.

  Daraus eine wahre, kurze Story bauen: von den ersten Challenges über 50 Challenges, das
  Level-/XP-System und das Casino-Update „The House Always Wins“ bis zu Bob, der KI, die Lockout
  Bingo lernt. **Keine erfundenen Zahlen.** Was nicht belegt ist, weglassen.

## Vorgaben V3 (gegenüber V2)

### Zoom

- Standard ist kein oder ein sanfter Zoom: höchstens etwa 1,0→1,08 über den ganzen Clip.
- Punch-Zooms nur noch an 1–2 echten Höhepunkten pro Short (Jackpot, Explosion) und dann
  höchstens 1,12.
- Wo in V2 stark auf einen Bildteil gezoomt wurde, um etwas lesbar zu machen (UI), darf das so
  bleiben. Dann aber langsam, nicht ruckartig.
- Shake und Flash sparsam einsetzen.

### Sprechtext

- **Pro Short ein durchgehender Text** von 70–110 Wörtern bei etwa 30–40 s, natürlich und
  verkaufend.
- **Aufbau:**
  1. Hook-Satz;
  2. Neugier aufbauen;
  3. Payoff;
  4. „and that's not even the best part“;
  5. CTA mit „Challenge Craft, free on CurseForge“.
- **Ganze Sätze** mit Bindewörtern, eine Stimme, ein Charakter. Wie ein begeisterter Creator, der
  seinem Publikum etwas zeigt, nicht wie ein Trailer-Sprecher.
- Ein Entwurf pro Short steht unten. Er darf verbessert werden, aber die Fakten bleiben.

### Stimme (Chatterbox)

- **Absatzweise erzeugen** (2–3 Sätze pro Durchgang) statt Zeile für Zeile. Dann klingt die
  Intonation zusammenhängend.
- Moderate Einstellungen: `exaggeration` 0,5–0,65, `cfg_weight` 0,4–0,5.
- **Stimmkonstanz:** dieselbe Stimme über alle Absätze und alle Shorts. Dafür einen gelungenen
  ersten Absatz als `audio_prompt_path` (Referenzstimme) für alle weiteren nutzen.
- Natürliche Pausen von 0,15–0,35 s an Satzenden.
- Den Schnitt an die Stimme anpassen, nicht umgekehrt. Kein `atempo` über 1,1.
- **TTS-Umgebung:** Die frühere venv wurde aus Platzgründen gelöscht. Neu aufsetzen, wie im
  V2-Plan beschrieben: CPU-Torch, `chatterbox-tts`.
- Danach die Modelle unter `~/.cache/huggingface` behalten, solange daran gearbeitet wird.

### Untertitel

- **Volle Sätze**, aber in lesbaren Stücken: ein Satz oder Halbsatz, höchstens 2 Zeilen und etwa
  8–10 Wörter pro Einblendung.
- Die Untertitel folgen dem Sprechtext Wort für Wort, also genau den gesprochenen Text. Die Zeiten
  kommen aus `vo/transcribe.py` bzw. `sync.py` (Wortzeiten).
- Akzentwörter dürfen farbig bleiben, höchstens eins pro Einblendung.
- Der Stil (Schrift, Kontur) bleibt wie in V2, der Nutzer mag die Grafik.

### Länge und Tempo

- 30–45 s. Schnitte weiter lebendig (0,8–2 s), aber ruhiger als V2, passend zum Satzrhythmus.

## Entwürfe Sprechtext (Ausgangspunkt)

**challenges_v3**

> I spent months coding the most viral Minecraft challenges into one mod – and now you can
> actually play them. In Red Light, Green Light, one step on red and you're done. Here, you can
> only walk as far as your dice roll. Every chunk is made of one random block, the floor burns if
> you stand still, and one zombie suddenly becomes ten. Want to race your friends? Try Lockout
> Bingo – or play against Bob, an AI I'm teaching to beat you. Stack challenges for more XP and
> unlock all fifty. It's called Challenge Craft, and it's free on CurseForge. Which one should I
> add next?

**casino_v3**

> I built a real casino inside Minecraft – and the House always wins. Every item you own is worth
> chips, and the croupier will happily buy your loot. But every ten minutes, the House collects
> its fee, and if you can't pay, your run is over. So you can grind… or you can gamble. Spin the
> slots for free spins, drop the Plinko ball, and cash out of Crash before the rocket blows up.
> And if you die? You play Blackjack for your life. This is one of fifty challenges in Challenge
> Craft – free on CurseForge. Would you gamble?

**blackjack_life_v3** and **random_chunks_v3**: written the same way from the V2 versions (see
`shorts/v2/*.srt`). Full sentences, a story arc, a CTA.

**story (Short 5, documentary)** – working title „How a Minecraft mod made viral challenges
playable“:

> For years, I watched creators play the craziest Minecraft challenges – the floor is lava, every
> block drops something random, one heart for the whole game. And every time I thought: why can't
> I just play this myself? So in April 2025, I wrote the first few challenges into a mod. Then
> came more. A timer, a challenge picker, a level tree with XP – until there were fifty of them.
> Then I went further: a whole casino where the House always wins. And now I'm teaching an AI
> called Bob to play Lockout Bingo against you. It's called Challenge Craft, it's free on
> CurseForge, and this is only the beginning.

Visual idea for 5:

- the first commit and the timeline as a graphic;
- „Then came more“ as a fast montage of all challenges;
- the counter going up to 50;
- casino clips;
- Bob clips;
- the end card.

Für die 5.1-Fassung kommen Motion Graphics dazu:

- Zeitleiste mit Daten aus dem Git-Log;
- animierter Zähler;
- Kinetic Typography für den Hook;
- Commit-Messages, die als Karten hereinfliegen;
- Versions-Badges 1.21.5 → 26.3.

## Motion Graphics (5.1)

- **Werkzeug:** Remotion (React → Video).
  - Agenten-Skills liegen im Archiv unter `/home/user/archive/.claude/skills/remotion-*`. Zuerst
    `remotion-best-practices/SKILL.md` lesen, dann `remotion-create`, `remotion-markup` und
    `remotion-render`.
  - Node ist vorhanden. Chromium liegt unter `/opt/pw-browsers`. Damit Remotion keinen Browser
    herunterlädt, `browserExecutable` bzw. `--browser-executable` darauf setzen, falls der
    Download scheitert.
  - Remotion ist für Einzelpersonen und kleine Teams kostenlos; Firmen brauchen eine Lizenz.
- **Projekt:** `/home/user/archive/motion/` (Quellcode ins Repo, `node_modules` NICHT, per
  `.gitignore`).
- **Vorgehen:**
  - Gefilmtes Material als `<OffthreadVideo>` aus `footage/` einbinden.
  - Die Stimme der V3 bzw. von Short 5 als Audio darunterlegen.
  - Die Grafiken obendrauf.
- **Plan B**, falls Remotion an Platz oder Netz scheitert: Motion Graphics mit Python
  (PIL/numpy) als Overlay-Frames erzeugen und mit `cut.py` bzw. ffmpeg compositen. Das im
  Protokoll begründen.

## Ablage (Archiv-Repo)

```
shorts/v3/<name>_v3_{final,clean}.mp4, <name>_v3.srt, <name>_v3_voice.m4a
shorts/v3/story_v3_*                      (Short 5)
shorts/v5.1/<name>_v5.1_{final,clean}.mp4 (Motion-Graphics-Fassungen)
shorts/v3/scripts.md                      (Endgültige Sprechtexte aller Shorts)
shorts/tools/                             (Schnitt-/VO-Skripte, angepasst)
motion/                                   (Remotion-Projekt)
```

Außerdem jede fertige Datei nach
`/tmp/claude-0/-home-user-Kasax-Challenge-Craft/2061deb3-7247-5b5c-aa62-6c43681c8da7/scratchpad/out/send-v3/`
kopieren. Dort holt der Hauptagent sie zum Verschicken ab.

## Qualitätsprüfung vor Abgabe

- [ ] Je Short Kontrollbilder alle ~2 s ziehen (`ffmpeg -vf fps=0.5`) und ansehen: Untertitel
      lesbar, nichts abgeschnitten, Zoom ruhig.
- [ ] Die Sprachspur mit Whisper zurück-transkribieren (`vo/transcribe.py`) und mit dem Skript
      vergleichen. Keine verschluckten oder falschen Wörter.
- [ ] Die Untertitel stimmen mit der Sprache überein (Abweichung unter 0,2 s).
- [ ] Lautheit: Stimme klar über den SFX (Ducking wie in V2).
- [ ] Länge 30–45 s; das Ende hat CTA und Frage.

## Stand

- [x] 0. Plan gelesen, TTS-Umgebung aufgesetzt, Werkzeuge nach `shorts/tools/` kopiert
- [x] 1. Sprechtexte aller 5 Shorts final (`shorts/v3/scripts.md`)
- [x] 2. Stimme: challenges_v3
- [x] 3. Schnitt und Render: challenges_v3
- [x] 4. Stimme, Schnitt, Render: casino_v3
- [x] 5. Stimme, Schnitt, Render: blackjack_life_v3
- [x] 6. Stimme, Schnitt, Render: random_chunks_v3
- [x] 7. Short 5 (story_v3): Stimme, Schnitt, Render
- [ ] 8. Remotion aufgesetzt (oder Plan B begründet)
- [ ] 9. story_v5.1 mit Motion Graphics
- [ ] 10. weitere 5.1-Fassungen, wo sinnvoll (begründen)
- [ ] 11. Qualitätsprüfung aller Fassungen, alles abgelegt und gepusht

## Protokoll

- (Hauptagent) Plan angelegt; Footage als MP4 ins Archiv; Remotion-Skills unter `.claude/skills/`.
- (Agent, 20:5x UTC) Schritte 0+1 erledigt. TTS-Umgebung (tts/, hf/ im Scratchpad) war noch da. Neue Werkzeuge in `shorts/tools/`: `tts_v3.py` (Chatterbox absatzweise, Referenzstimme = erster Absatz, Whisper-Check mit Neuwurf), `v3lib.py` (Stimme zuerst, Wortzeiten per Whisper auf den Skripttext ausgerichtet, Untertitel in Satz-Chunks, Schnitt per Anker-Phrasen, Zoom-Begrenzung 1,08/1,12, Ducking, loudnorm), je Short ein Beat-Skript (`*_v3.py`). Sprechtexte: `shorts/v3/scripts.md`. Maschine ist durch Benchmarks stark ausgelastet: ein TTS-Absatz braucht ca. 5-10 min. Remotion-Projekt `motion/` angelegt (npm install ok, Quellcode geschrieben, noch nicht gerendert).
- (Agent 21:3x UTC) challenges_v3 fertig: shorts/v3/challenges_v3_{final,clean}.mp4 (29,0 s, 26 Clips, 104 Wörter), .srt, _voice.m4a. Whisper-Rücktranskription des Mixes = Skript. Sprache läuft auf 0,95x (Chatterbox spricht sehr schnell). TTS für casino/story/blackjack/random_chunks läuft weiter im Hintergrund (vo3/ im Scratchpad, ca. 8 min je Absatz).
- (Agent 23:5x UTC) Schritte 4-7 fertig: casino_v3 (29,2 s), blackjack_life_v3 (22,2 s), random_chunks_v3 (23,3 s), story_v3 (32,2 s) in shorts/v3/ (final, clean, srt, voice.m4a). Sprache per Whisper gegengeprüft. Hinweis: die Stimme spricht ca. 4 Wörter/s; 70-110 Wörter ergeben daher 22-32 s statt 30-45 s (blackjack/random_chunks bewusst kürzer, wenig Material). Der TTS-Prozess wurde mehrfach vom Speicherlimit (OOM) beendet, wenn parallel gerendert wurde: `tools/vo3loop.sh`-Muster (Neustart-Schleife) nutzen und TTS nicht parallel zum Rendern laufen lassen.
