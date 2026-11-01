# Challenge Craft – Projektgedächtnis

> Liegt im Archiv (`memory/`), weil der Nutzer `CLAUDE.md` im Mod-Repo per `.gitignore` ausschließt. Kann als lokale
> `CLAUDE.md` in den Mod-Checkout kopiert werden, damit Claude Code sie dort automatisch lädt.

Dieses Dokument sammelt das Wissen aus der Zusammenarbeit (September–Oktober 2026), damit jede neue Sitzung nahtlos
weiterarbeiten kann. Es ist kurz gehalten; Details stehen in den verlinkten Dokumenten. Bei Widersprüchen gilt die
neueste Anweisung des Nutzers.

## Der Nutzer und wie er arbeiten möchte

- **Sprache:**
  - Antworten in der Sprache der Nachricht, meist Deutsch, manchmal Englisch.
  - Kurz, klar, ohne Fachjargon-Ballast.
  - Der Nutzer liest Ergebnisse oft am Handy.
- **Nutzungslimit:**
  - Der Nutzer achtet stark auf sein Limit („effizient arbeiten“, „wenige Tokens“).
  - Sagt er „Achtung, Nutzungslimit“: sehr knapp antworten und keine Test-Suite laufen lassen, außer er erlaubt es.
  - Subagenten nur, wenn er es ausdrücklich erlaubt, und dann mit knappem, vollständigem Briefing.
  - Ein Subagent ist zweimal ins Limit gelaufen. Mittelgroße Aufgaben besser selbst erledigen.
- **Eigenständig arbeiten:**
  - Er gibt gern große Aufträge mit „arbeite selbstständig durch“.
  - Dafür einen Plan mit Stand-Liste anlegen, damit ein Abbruch durch Limits nichts verliert.
- **Grenze bei Bob:** Keine Abhängigkeit zu Baritone oder anderen Mods. Bob ist ein eigenes, integriertes Feature,
  der Mod muss standalone spielbar sein. Baritone darf Inspiration sein.
- **Entwicklungsumgebung des Nutzers:**
  - Windows 11 mit IntelliJ, Projekt unter `C:\Users\lars6\IdeaProjects\Kasax_Challenge_Craft`, JDK 25 in
    `%USERPROFILE%\.jdks`.
  - Er aktualisiert über „GitHub Update“ in IntelliJ.
  - Am 19.10.2026 hat er die Maschine gewechselt.
  - Der Trainings-Laptop hat 32 Kerne, 31 GB RAM und eine RTX 3070 Ti.
  - Zusätzlich hat er einen BisectHosting-Server mit 22 GB angeboten.

## Repos, Branches, Regeln

- **Mod-Repo:** `Kasax007/Kasax_Challenge_Craft`.
  - `26.3` = Hauptentwicklung.
  - `26.3-lockout-bot` = Bob und Training; aktueller Arbeits-Branch.
  - Ältere Versionen: `26.2`, `26.1.2`, `1.21.5`.
  - Nie auf `26.3` pushen, außer der Nutzer erlaubt es. PRs nur auf Wunsch.
- **Commit-Fußzeile:** Immer der Footer aus der Sitzung (Co-Authored-By + Claude-Session). Keine Modellnamen in
  Dateien, Commits oder Videos.
- **Archiv-Repo:** `Kasax007/Archive`, lokal `/home/user/archive`.
  - Ablage für alles, was nicht in den Mod-Code gehört: Videos, Footage, Shorts, Stills, CurseForge-Texte, Logs,
    Recherche.
  - **Video-Material gehört ins Archiv, nicht in den Mod-Branch.** Ausnahme: der Film-Harness `src/film`, weil er
    mit dem Mod kompiliert wird.
  - Siehe `/home/user/archive/CLAUDE.md`.
- **Bob-Bot standalone:** `Kasax007/Bob-Bot`. Bob als eigener Begleiter-Mod; später als KI-Mitspieler für
  Challenge Craft gedacht.

## Der Mod (Stand 1.1.3, veröffentlicht am 1.11.2026; Minecraft 26.3, Fabric, Java 25)

- **Inhalt:**
  - 51 Challenges (seit 1.1.3), einzeln oder gestapelt; jede Kombination bekommt eine Difficulty Rating.
  - Lifetime XP, Level 1–20 mit Freischaltungen und Perks, danach Infinity Stars (Namens-Auren).
  - Weitere Features: Daily Challenge, Challenge Codes und Presets, Run Summary Card, Hub, Multiplayer.
- **Challenge 50 „The House Always Wins“** (Level 8): Casino.
  - Spiele: Jetons, Croupier, Gebühr alle 10 Minuten, Slots „Mine Fever“, Plinko, Crash, Roulette.
  - Mechaniken: Mob-Wellen bei Verlust, Tod = Blackjack um das Leben.
  - Alle Spiele zahlen 96 % zurück (RTP).
  - Konzept: `docs/konzept-the-house-always-wins.md`.
- **Challenge 51 „Void Trail“** (Level 11, Difficulty 6.0, Icon Grundgestein, Okt. 2026):
  - Wer einen Block verlässt, löscht dessen ganze Säule (Bauhöhe bis Weltboden, inkl. Grundgestein, Wasser, Lava).
  - Bleiben: nur Endportalrahmen und Endportal. Netherportale werden mitgelöscht (laut Vorgabe des Nutzers).
  - Schnelle Bewegung: alle überquerten Säulen; Teleport/Perle/Portal: nur die verlassene. Kreativ/Zuschauer löschen nichts.
  - Konflikte: Skyblock, Level = Border, Damage = Border, Chunk Hunt. Game-Test `void_trail_tests_void_trail`.
- **Bob:** KI-Gegner für Lockout Bingo, im Lobby-Menü „Play against Bob“, auf Easy, Normal und Hard.
  - Öffentlich immer als *Early Development Stage* bezeichnen.
  - Konzept: `docs/konzept-bot.md`. Plan und Messungen: `docs/bob-plan.md`, `docs/bob-leagues/`.
- **CurseForge-Texte:** `docs/curseforge/` (Mod, Modpack, Changelogs 1.1.2 und 1.1.3).
- **Veröffentlichen (seit Okt. 2026 automatisch):**
  - `build.gradle`: mod-publish-plugin (`publishMods`) → CurseForge (Projekt 1508454), Modrinth (`3qs3GQyx`,
    Slug `challenge_craft`) und GitHub-Release `v<version>`. Changelog: `docs/curseforge/changelog-<version>.md`.
  - `.github/workflows/publish.yml`: ein Push auf `26.3` oder `26.3-lockout-bot`, der `mod_version` in
    `gradle.properties` ändert, veröffentlicht – nur solange es den Tag `v<version>` noch nicht gibt.
  - Secrets (setzt der Nutzer): `CURSEFORGE_TOKEN`, `MODRINTH_TOKEN` (Scopes: Create/Read/Write versions).
  - Veröffentlichen ist nach außen sichtbar: Version nur nach ausdrücklichem Go des Nutzers erhöhen.
  - Der Workflow prüft je Plattform, ob die Version schon da ist: CurseForge-Dateiliste (Fallback cfwidget),
    Modrinth-Versionen, GitHub-Tag. Er lädt nur hoch, was fehlt. Fehlt ein Secret, gibt es eine Warnung statt eines Abbruchs.
  - Eine Sitzung darf keine Tags pushen (HTTP 403). Den Tag `v<version>` legt der Workflow über das GitHub-Release an.
  - Von Hand (Token nur als Datei außerhalb der Repos): `CURSEFORGE_TOKEN=… ./gradlew publishCurseforge`.
  - Stand 1.1.3: CurseForge-Datei 9399763 (nach ca. 10 Min. freigegeben), GitHub-Release `v1.1.3`. Modrinth hat
    noch 1.1.1 (1.1.2 und 1.1.3 fehlen; der Nutzer hat noch keinen Modrinth-Token gegeben).
  - Projektbeschreibungen lassen sich bei CurseForge nicht per API ändern (Idee CF-I-6366, „Future consideration“).
    Der Nutzer fügt `docs/curseforge/mod-description.md` und `modpack-description.md` von Hand ein.
- **Modpack** (CurseForge-Projekt 1653698, Dateien „Challenge Craft 26.3-vN.zip“ plus Zusatzdatei
  „Serverpack Challenge Craft 26.3-vN.zip“):
  - v4 (1.11.2026): Modpack 9399868, Server-Pack 9399871. Nur Challenge Craft 1.1.3 neu, sonst gleich wie v3.
  - Werkzeuge: `curseforge/modpack-tools/` im Archiv. `mkpacks.py` baut aus dem letzten Pack das nächste (nur die
    Challenge-Craft-Datei bzw. -Jar wird getauscht). `upload.sh` lädt über die Upload-API hoch.
  - Reihenfolge: zuerst die Mod hochladen und die Freigabe abwarten (ca. 10 Min.), dann das Modpack (Game-Versions
    26.3 = 17045, Fabric = 7499; Freigabe ca. 15 Min.). Danach den Server-Pack mit `parentFileID` des Modpacks, ohne
    gameVersions.
  - **Server-Pack-Markierung geht nicht per API:** `isServerPack: true` wird beim Upload ignoriert (`hasServerPack`
    bleibt false). `update-file` mit dem Feld gibt HTTP 500, übernimmt aber den Changelog. Der Nutzer muss die
    Zusatzdatei auf CurseForge von Hand als Server Pack markieren (bei v4 offen, Stand 1.11.2026).
  - CurseForge ersetzt Leerzeichen im Dateinamen durch Bindestriche; der Anzeigename behält sie.
  - Den Server-Pack herunterzuladen und zu starten, hat die Sicherheitsprüfung blockiert (fremder Code). Die
    Server-Seite der Mod prüfen die Game-Tests: Sie laufen als Dedicated Server.
- **Links:**
  - Mod: `https://www.curseforge.com/minecraft/mc-mods/challenge` (der Slug ist `challenge`).
  - Modpack: `https://www.curseforge.com/minecraft/modpacks/challenge-craft`.
  - Discord: `https://discord.com/invite/zuZVtVvJaY`.
  - BisectHosting-Promo: `KASAX007`.

## Bob – was der Nutzer will (Leitlinien)

- **Wie ein erfahrener Spieler spielen:**
  - Weiß, was ein Profi weiß: Bastion-Loot, Shipwreck-Truhen, Buried Treasure, Speed-Portal-Gießen,
    Dorf-Looting (Heu → Brot), Portal-Koordinaten merken, Augen-Triangulation, Fast Bridging.
  - Fackeln setzen, Strip-Mining und Flucht-Schleifen gehören nicht dazu.
- **Mining:** Höhlen statt Strip-Mining (in ca. 80 % der Fälle besser). Erzadern ganz abbauen, wenn er das Material
  noch braucht (Schild, Eimer, Rüstung).
- **Nie sterben:** Tode sind der größte Verlust.
  - Ein „Guardian“ (Gefahrenwächter) darf jederzeit übernehmen.
  - Gut kämpfen (Abstand, Bewegung, Schild) statt passiv zu sein.
  - Lava immer meiden, besonders im Nether.
- **Ausstattung:**
  - Startausrüstung inklusive Schild, immer Ersatz-Holz und Cobblestone dabei, Bundles nutzen.
  - Bessere Rüstung craften, wenn Eisen da ist.
- **Sicht:** 24 Chunks, Simulation passend. Nur nutzen, was ein Spieler sehen könnte; die nächste Wasserquelle
  statt „Allwissen“.
- **Schlafen:** Nur wenn er ein Bett hat, nichts nachts braucht und im Multiplayer auch die anderen liegen.
- **Strategie:**
  - Leichte Felder sofort mitnehmen, Ziele bündeln, Gelegenheiten unterwegs nutzen.
  - Volles Brett in 90 min als Ziel. Nicht abbrechen, wenn etwas nicht gefunden wird.
- **Testen:** Lange Läufe auf Zufalls-Seeds. Ein Lockout-Spiel dauert 90 min, das Endspiel zählt mit.

## Training (Deep Learning, `scripts/train`, Doku `docs/bob-training.md`)

- **Start:**
  - Ein Prozess, der startet und weiterlernt, bis er gestoppt wird: `scripts\train\train.bat` oder das Dashboard
    `start-dashboard.bat` (`scripts/train/dashboard.py`, http://127.0.0.1:8765).
  - Er skaliert automatisch auf so viele Server, wie der Laptop gerade stabil trägt.
- **Was trainiert wird:**
  - Arena (Deckung im Kampf): Cover-Modell mit 54 Eingaben; die Arena-Prüfung ist das Tor für neue Modelle.
  - Zielzeit-Modell: 32 Eingaben.
  - Liga Bob gegen Bob: Knöpfe in `champion.json`. Liga-Spiele laufen immer volle 90 Spielminuten
    (`CHALLENGECRAFT_FULL_BOARD=1`, kein vorzeitiger Sieg).
- **Ablage:**
  - Daten unter `runs/train/` (nicht in Git).
  - `scripts\train\export.bat` kopiert Modelle und Stand nach `src/main/resources/bob-models/`. Das ist der
    Standard für alle Geräte.
  - `ModelStore` lädt aus `BOB_MODELS`, sonst `bob-models/`, sonst aus dem Classpath.
- **Neue Maschine:** Python 3.10+ („Add to PATH“), JDK 25. Die `.bat` richten `runs\train\venv` ein und prüfen
  numpy/psutil. Optional: `gpu.bat`; Lithium, C2ME und FerriteCore nach `runs\train\mods\`.
- **Sicherheitsnetz:** Das gelernte Cover-Modell darf nicht „stehen und kämpfen“ wählen, wenn die Berechnung den
  Kampf als verloren einstuft und die Regeln einen Ausweg kennen (`Guardian`).

## Bauen und Testen (Container)

- **JDK:** unter `/opt/jdk25/` (zuletzt `jdk-25.0.5+8`, vorher `jdk-25.0.4.1+1`; mit `ls /opt/jdk25` prüfen).
- **Maven Central 429:** Gradle-Init-Skript `~/.gradle/init.d/central-mirror.gradle`, das `repo.maven.apache.org`
  auf `https://maven-central.storage-download.googleapis.com/maven2/` umbiegt (nur vorhandene Central-URLs ersetzen).
- **Kompilieren:** `sh ./gradlew compileJava -q`. Film-Quellen: `compileFilmJava`.
- **Game-Tests:**
  - Alle: `sh ./gradlew runGameTest`.
  - Einzeln: `-PbotTest=challengecraft-gametest:<klasse>_<test>`, z. B. `guardian_tests_wolves_at_his_heels`.
  - Die Tests prüfen die Regeln (`-Dbob.learned=0`). Mit den gelernten Modellen: `-PbotLearned`.
  - Unter Volllast schwanken: `brawl_zombie_trio`, `brawl_enderman_slope`, `shield_walk_strays`, `barter_in_hole`.
    Einzeln nachprüfen, bevor etwas als kaputt gilt.
- **Ressourcen:**
  - Höchstens 2 JVMs gleichzeitig. Lange Läufe im Hintergrund, warten mit `until …; do sleep 20; done`.
  - Nie `pkill -f <muster>`, wenn das Muster im eigenen Befehl steht: Das tötet die eigene Shell. Stattdessen
    `pgrep`/`kill PID`.
- **Container:**
  - Er wird nach Inaktivität zurückgesetzt. Was bleiben soll, committen und pushen.
  - Der Plattenplatz ist knapp (`df -h /` prüfen). Kein ffprobe, kein drawtext in ffmpeg (Text mit PIL zeichnen).

## Film-Harness (`src/film`, für Shorts und Showcase)

- **Neuer Container:** `apt-get update && apt-get install -y libegl1 libegl-mesa0`, Xvfb `:98` und
  `SDL_VIDEO_FORCE_EGL=1` setzen. Sonst „Couldn't find matching GLX visual“ bzw. „Could not load EGL library“.
- **Aufruf:** Client-Gametest mit eigenem Source-Set: `./gradlew runFilm -Pfilm=szeneA,szeneB -PfilmOut=DIR`.
  Bilder werden Tick für Tick aufgenommen (1080×1920, 30 fps).
- **Szenen:** `CasinoScenes`, `ChallengeScenes`, `UiScenes`, `WorldScenes`, `MenuScenes`.
- **Wichtige Fixes (Oktober 2026):**
  - Der Client läuft im Gleichschritt mit der Film-Uhr (`ClientLockstepMixin`; vorher 4× zu schnell).
  - Der lokale Spieler ist unter der freien Kamera immer sichtbar (`FreeCamPlayerMixin`).
  - Feste Film-Identität und Skin; kein Fadenkreuz, keine Toasts; UI-Uhren auf Spielzeit.
- **Falle:** Liegen in einem Shot-Ordner Bilder zweier Takes (PNG + JPG), wechseln sie sich im Schnitt ab: Das Bild
  flackert. Vor dem Schnitt prüfen, ob in einem Ordner gemischte Takes liegen.
