# 06 – Videos, Footage und CurseForge-Beschreibungen

Alle Videos liegen im Archiv-Repo (`Kasax007/Archive`, Branch `main`, alles gepusht). Format wie immer: Englisch,
1080×1920, 30 fps, für TikTok und YouTube; je eine Fassung mit und ohne eingebrannte Untertitel, mit und ohne Musik,
dazu SRT, reine Sprachspur und Post-Text. Sprecher ist Kokoro `am_michael` (Tempo 0,95, im Schnitt ×1,06), jeder
Absatz mit Whisper geprüft. Musik von Kevin MacLeod (incompetech.com, CC BY 4.0) – der Credit steht im Post-Text.

## 1. Neu in diesem Projekt

### Dreamcraft-TikTok (`dreamcraft/tiktok/`)
Schneller Promo-Short für Dreamcraft 26.3, **44,2 s**.
- **Ablauf:** Hook mit Luftaufnahme einer Burg und dem Titel „MINECRAFT 26.3 MODPACK“, dann Hauptmenü, Quest-Buch,
  Kirschblüten-Dorf, Feuer-Magier, Mutant, Küche, Tech Reborn, Floß mit Hai, Nether und End. Endkarte
  „FREE ON CURSEFORGE“.
- **Version 1** (2.11., Commit `d77dcb8`): ohne Shader. Die Dateien wurden von v2 ersetzt, v1 gibt es nur noch in der
  Git-Historie (z. B. `git show d77dcb8:dreamcraft/tiktok/dreamcraft_tiktok_captions_music.mp4 > v1.mp4`).
- **Version 2** (2.11., Commit `dce27ca`, aktuell): neu gefilmt **mit Shadern** (Iris + Complementary Reimagined
  r5.9.3) und Sichtweite 12. Der Film-Harness wartet vor jedem Shot, bis alle Chunks gezeichnet sind – im Bild lädt
  nichts nach. Nur der End-Shot stammt aus v1, weil das End mit Shadern auf der Software-GPU hängen blieb.

| Datei | Inhalt |
| --- | --- |
| `dreamcraft_tiktok_captions_music.mp4` / `_captions_nomusic.mp4` | mit Untertiteln, mit / ohne Musik (je ~46 MB) |
| `dreamcraft_tiktok_clean_music.mp4` / `_clean_nomusic.mp4` | ohne Untertitel |
| `dreamcraft_tiktok.srt`, `dreamcraft_tiktok_voice.m4a` | Untertitel, Sprachspur |
| `dreamcraft_tiktok_post.txt` | Titelvorschlag „This Minecraft modpack has over 250 mods...“, Beschreibung, Link, Musik „Overworld“, Hashtags |
| `dreamcraft_tiktok_contact_sheet.png` | Kontaktbogen |
| `stills/endcard_short.png` | Endkarte |
| `tools/` | `dc.py` (Schnitt), `script.py` (Sprechtext), `tts_kokoro.py`, `endcard.py`, `cut.py`, `v3lib.py`, `sfx.py`, `check.py` |
| `README.md` | Anleitung zum Neubauen |

### Beach-Craft-Review (`beachcraft/review/`)
Review-Video zu **Beach Craft 2.0.1**, **5:07**. Es zeigt und erklärt jedes Feature einmal – damit du prüfen kannst,
was entwickelt wurde und ob alles funktioniert. Der Ton enthält die **echten Spielgeräusche** der Aufnahme (aus den
Ton-Protokollen gemischt), Musik („Hep Cats“) nur leise darunter; GUI-Shots sind vergrößert. Beim Filmen fiel ein echter
Fehler auf: das Paddel schob das Boot nicht (in 2.0.1 behoben).

| Datei | Inhalt |
| --- | --- |
| `beachcraft_review_captions_music.mp4` / `_captions_nomusic.mp4` | mit Untertiteln, mit / ohne Musik (61–64 MB, keine Teilung nötig) |
| `beachcraft_review_clean_music.mp4` / `_clean_nomusic.mp4` | ohne Untertitel |
| `beachcraft_review.srt`, `beachcraft_review_voice.m4a` | Untertitel, Sprachspur |
| `beachcraft_review_post.txt` | Titelvorschlag „Beach Craft 2.0 for Minecraft 26.3 - every feature in one review“, Beschreibung, Link, Musik-Credit, Hashtags |
| `beachcraft_review_contact_sheet.png`, `stills/endcard_review.png` | Kontaktbogen, Endkarte |
| `REPORT.md` | **Prüfbericht** (Deutsch) |
| `tools/` | `bc.py` (Review-Schnitt, `GUI_ZOOM`, `SKIP`), `gamesound.py` (Spielgeräusche), `script.py`, `tts_kokoro.py`, `endcard.py` … |

**Was in `REPORT.md` steht:** eine Tabelle aller 2.0.1-Features in der Reihenfolge des Videos mit Stand (z. B.
„Segeltuch war nicht herstellbar – behoben“, „Hai spawnte nie natürlich – behoben“, „Paddel schob das Boot nicht –
behoben“, „Titan-Werkzeuge gibt es nicht – Texte korrigiert“) und die **bewusst nicht geänderten Design-Fragen**
(Titanofen verdoppelt alles, Maschinen verlieren Energie beim Abbauen, Chunk Destroyer kostet auch leere Säulen, nur ein
Ausgabe-Slot im Item Catcher, Treibholz-Setzling selten, Plattform auf y 209, Haken zieht durch Wände, Steinmassive im
Meer). Grundlage war eine Code-Analyse aller Bereiche, jeweils von einem zweiten Durchgang gegen den Code geprüft.

Hinweis: Die README des Reviews erwähnt eine Teilung über 90 MB in `_part1`/`_part2`; die Dateien sind aber kleiner und
liegen ungeteilt vor.

### Noch kein Video für Beach Craft 3.0, Quest Icons 1.1.0 oder Tamagotchi 1.2.0
Für die neuen Versionen dieser Runde wurde kein Video gemacht. Für die CurseForge-Seite von Beach Craft 3.0 gibt es
Collagen aus Screenshots (`docs/curseforge/img/*.jpg`, `make_images3.py` im Raft-Repo).

## 2. Footage (`footage/<gruppe>/`)
Rohmaterial als eine MP4 pro Shot (CRF 15–18). Zurück zu Einzelbildern: `ffmpeg -i footage/x/y.mp4 -q:v 2 f%05d.jpg`.

| Ordner | Shots | Größe | Inhalt |
| --- | --- | --- | --- |
| `footage/dc` | 13 | 39 MB | **Dreamcraft-TikTok v2** mit Shadern: castle, end, kitchen, magic, menu, menu_land (Hochformat-Ausschnitt aus dem Menü-Standbild), mutant, nether, questbook, raft, shark, tech, village; teils mit `.sounds.jsonl` / `.shot.json` |
| `footage/bc` | 43 | 147 MB | **Beach-Craft-Review:** z. B. bc_beach, bc_craft_portal, bc_portal_light, bc_portal_trip, bc_portal_arrive, bc_island, bc_debris, bc_hook, bc_catcher, bc_purifier, bc_grill, bc_crops, bc_scarecrow, bc_shark, bc_shark_attack, bc_receiver, bc_paddle, bc_armor, bc_detector, bc_disc, bc_power, bc_quarry, bc_furnaces, bc_deco, bc_raft_tour; jeweils mit Ton-Protokoll `<shot>.sounds.jsonl` |
| `footage/tama`, `footage/tama2` | 28 / 44 | 163 / 269 MB | Tamagotchi (Oktober): Short/Showcase bzw. Review-Schnitt 1.1 mit Ton-Protokollen |
| `footage/chal`, `footage/casino`, `footage/long`, `footage/ui` | 15 / 18 / 21 / 5 | 218 / 158 / 185 / 3 MB | Challenge Craft (Oktober): Challenges, Casino, Long-form, Menüs |

Gefilmt wurde mit dem Film-Harness im Modpack-Repo (`tools/dctest`, `Film.java` für den TikTok, `BcShots.java` für das
Review): `sh ./gradlew runPack -Pxmx=5G -Pscene=film -Pshots=… -Prd=12 -Pout=$SP/film/…`, lange Läufe in Batches zu
5–7 Shots (`$SP/bc_batches.sh`). Die meisten Review-Shots spielen auf einer 13×13-Floß-Bühne in der Raft-Dimension
(eine Bühne alle 200 Blöcke ab x = 3000).

## 3. Ältere Videos im Archiv (vor diesem Projekt)
| Ordner | Inhalt |
| --- | --- |
| `shorts/v1`, `v2`, `v3`, `v5.1` | Challenge-Craft-Shorts (Challenges, Casino, Blackjack ums Leben, Random Chunks, Story; v5.1 mit Remotion-Grafiken aus `motion/`) |
| `longform/showcase_v1` | Challenge-Craft-Showcase (7:50), je Fassung in zwei abspielbaren Hälften; Musik in `longform/music` |
| `tamagotchi/short`, `longform`, `review` | Tamagotchi: Short (~43 s), Showcase (~2:03), Review-Schnitt 1.1 (~3:05, nur für dich) |
| `stills/`, `research/`, `curseforge/` | Kontaktbögen, Recherche, Challenge-Craft-Beschreibungen (Markdown) und `modpack-tools/` |

## 4. Die CurseForge-Beschreibungen (finale Fassungen)

Für Projektbeschreibungen gibt es **keine API** – du fügst sie selbst ein. Alle sind als HTML für die
**Quellcode-Ansicht** des CurseForge-Editors geschrieben, im Stil deiner Seiten (Header-Bild, Abschnitts-Streifen,
Screenshots, Badges, BisectHosting-Banner mit Code KASAX007, viele Spoiler).

| Projekt | Datei (Repo, Branch) | Bilder und Banner | Spoiler | Wann einfügen |
| --- | --- | --- | --- | --- |
| **Dreamcraft** (545167) | `Modpack-Development/docs/curseforge/description.html` (`26.3`) | BisectHosting-Grafiken `bh_header`, `bh_promo`, `bh_1`…`bh_6` (von bisecthosting.com), 10 eigene Screenshots (Quest-Buch, Burg, Dorf, Magie, Küche, Technik, Floß, Nether, End, Menü), die alten 1.20.1-Bilder (imgur) | 8 | **schon auf V1.3 aktualisiert** („328 quests“, „New in V1.3“) – erst mit dem V1.3-Upload einfügen |
| **Quest Icons** (690531) | `Kasax_Quests_Items_Mod-1.19.2/docs/curseforge/description.html` (`26.3`) | dein Original-Stil: Logo-Bild, Überschrift „Made with love, sweat and tears“, Bisect-Banner und Abschnittsbilder (imgur), dazu `img/book.png`, `quest.png`, `icons.png` | 10 | **jetzt** (beschreibt 1.1.0 mit Dream Star, das ist veröffentlicht) |
| **Beach Craft** (1010922) | `Kasax_Raft_Mod/docs/curseforge/description.html` (`26.3`), Kopie in `$SP/release_bc3/` | `img/header_3.png`, eigenes Bisect-Banner `img/bisect.png`, Streifen `strip_*.png`, Collagen `world.jpg`, `story.jpg`, `places.jpg`, `creatures.jpg`, `sailing.jpg`, `diving.jpg`, `build.jpg`, `almanac.jpg`, `boss.jpg`, Blockbilder | 23 (Boss nur im Spoiler) | **nach dem Upload von 3.0.0** (beschreibt 3.0) |
| **Tamagotchi** (1758309) | `tamagotchi/docs/curseforge/description.html` (`26.3`) | Badges, Header, Bisect-Banner, Streifen | 14 | unverändert seit 1.1.0; für 1.2.0 nicht angepasst |
| **Challenge Craft** (1508454) | `docs/curseforge/mod-description.md`, `modpack-description.md` im Mod-Repo | – | – | in dieser Runde nicht geändert |

**So fügst du eine Beschreibung ein:**
1. Auf CurseForge das Projekt öffnen → Beschreibung bearbeiten.
2. Im Editor auf die **Quellcode-Ansicht** umschalten (Source).
3. Den ganzen Inhalt der jeweiligen `description.html` einfügen (vorhandenen Text ersetzen) und speichern.
4. Kurz prüfen: Bilder laden, Spoiler klappen auf. Spoiler sind `<div class="spoiler">`-Blöcke, die CurseForge als
   aufklappbare Boxen zeigt.

**Wichtig zu den Bildern:** Die eigenen Bilder werden direkt von GitHub geladen
(`https://raw.githubusercontent.com/Kasax007/<Repo>/26.3/docs/curseforge/img/…`). Der Branch `26.3` und die Bilder
müssen deshalb bestehen bleiben – Branch nicht umbenennen oder Bilder löschen, sonst sind sie auf der Seite weg.

**Changelogs für die Datei-Uploads:** `docs/curseforge/changelog-<version>.md` im jeweiligen Repo
(Dreamcraft `changelog-26.3-V1.3.md`, Quest Icons `changelog-1.1.0+26.3.md`, Beach Craft `changelog-3.0.0+26.3.md`,
Tamagotchi: Abschnitt `## 1.2.0` in `CHANGELOG.md`, Challenge Craft `changelog-1.1.4.md`).

**Auch prüfen:** Die Kurzbeschreibung (Summary) des Dreamcraft-Projekts lautete beim Abruf am 2.11.
„… Featuring 800+ quests …“ (aus der Forge-Zeit). Die 26.3-Version hat 328 Quests (V1.3) bzw. 164 (V1.2.1).
