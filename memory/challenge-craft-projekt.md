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
- **Tick-Sprint nur mit `CHALLENGECRAFT_BOT_SIM=1`** (Hinweis des Nutzers 9.11.): Sonst rechnet die Wegsuche nach
  Uhrzeit, und Bob spielt schlechter, je schneller das Spiel läuft (3 Tode bei 1,5×, 18 bei 2,3×). SIM zählt Knoten pro
  Spiel-Tick (`BotNavigator.SIM`, `SIM_NODES_PER_TICK`); `versus.sh` setzt Sprint nur mit SIM=1, der Trainer ebenso.
  Jede neue Such-/Rechenlogik (z. B. der Brett-Planer) muss ihr Budget in Spiel-Ticks/Knoten zählen, nie in Uhrzeit.
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

## Wichtige Regel (7.11.2026)
- **Das Challenge-Craft-Modpack bleibt Vanilla plus der Mod des Nutzers** („Challenge Craft soll vanilla bleiben bis
  auf mein Mod, da soll kein Iron Chests oder sowas rein“). Nur Client-Politur, Leistung, Voice-Chat und Shader wie in
  v4. Die v5 mit Upgraded Iron Chests und Storage Drawers war ein Fehler (der Quality-of-Life-Wunsch vom 4.11. galt dem
  Dreamcraft-Questbuch) und ist gestrichen; das Pack bleibt auf v4 (9399868, Server-Pack 9399871). Ein neues Pack
  kommt erst mit einer neuen Challenge-Craft-Version.

## Stand 9.11.2026 (Challenge Craft 1.1.4, Bob-Modelle, Bob-Plan)

- **1.1.4 veröffentlicht** (Freigabe „Ja 1.1.4 V1“): Bugcheck-Fixes (Infinite Chest Klicks/Speichern/Reichweite,
  Crafter baut keine gesperrten Items, Würfel, Roulette/Kasse, Zähler) per Cherry-Pick auf `release/1.1.4`, ohne den
  Pack-v5-Doku-Commit. Tests `challengecraft-gametest:challenge_fix_tests_*` 5/5. Push auf `26.3-lockout-bot`
  (37246fe) → Action: GitHub-Release v1.1.4, CurseForge-Upload; Modrinth fehlt der Action (kein Secret) → von Hand
  hochgeladen (Version ZyJkDRf0, byte-gleich). Filter für Game-Tests braucht den Namensraum, z. B.
  `-PbotTest='challengecraft-gametest:challenge_fix_tests_*'`.
- **Bob-Modelle vom Laptop (48 h Training, hochgeladen im Chat):** `cover.json` 20261020-192933 (54 Eingaben,
  24.796 Kämpfe; Repo hatte 42 Eingaben/3.124), `goal.json` 20261021-164809 (32 Eingaben, 988 Ziele; Repo 25/617),
  `champion.json` unverändert seit 16.10. (die Liga fand in 48 h keinen besseren Knopf-Satz). Kein Branch „push“ auf
  GitHub. Vergleich alt/neu auf den Kampf-Tests (brawl, guardian, shield) mit `-PbotLearned`: neu 33/34 (nur das
  wackelige `brawl_zombie_trio`), alt 30/34 (Tode in brawl_enderman, brawl_enderman_slope, low_with_two_zombies).
  Übernommen auf `26.3-lockout-bot` = d85f36f (ohne Versionsänderung; der nächste Release trägt sie).
- **Bob-Plan (freigegeben 9.11. abends, „Ich finde deinen Plan mit Schritt 1 bis 4 sehr gut“):** Bob „so gut wie der
  beste Speedrunner im Lockout Bingo“, Algorithmen und Wissen, max. 4 Subagenten, bis der Nutzer „Stop“ sagt. Runden als
  Workflows (Runde 1: Brett-Gehirn mit Simulator und Suchplaner, Speedrunner-Wissen/Zeitschätzung, Eröffnung; dann
  Integration + Liga und ein Paket für den BisectHosting-Server des Nutzers, 22 GB, `docs/bob-bisect-server.md`).
  Wecker `trig_01QyWcet15ZS1jPAYKtU48gK` alle 2 h – bei „Stop“ löschen (delete_trigger) und laufende Workflows stoppen.
  Keine Challenge-Craft-Version veröffentlichen, bevor Bob deutlich besser ist und der Nutzer zustimmt. Rust-Nachbauten
  von Minecraft (Pumpkin, Valence, FerrumC) hat der Nutzer angesprochen; Bewertung in Runde 1 (Brain-Agent).

## Stand 10.11.2026 (Bob Runde 1 übernommen, Runde 2 läuft)

- **Runde 1 (Bob-plan Abschnitt 27, „Runde 22“) übernommen:** `26.3-lockout-bot` = d9c5cac (83aa770 = Runde 1 + Merge
  des Server-Pakets). Liga 9 (12 Seeds, 20 min, hart, SIM=1): 2,88 statt 2,08 Felder pro Bob (gepaart +0,79, SE 0,39),
  erstes Feld Median 265 statt 440 s, Tode gleich (0,25/Bob), aber Ertrinken 5 in 40 Bot-Spielen (alt 0) – AirTask
  „dig instead“ hängt. Eröffnung: vier Steinwerkzeuge 109 statt 196 s, 1,88 statt 0,62 Felder in 10 min.
  Brett-Gehirn (Simulator `bot/lockout/sim`, Vorausschau `search=1`): im Simulator +1,68 Felder/90 min, in echten
  Spielen (Liga 10) schlechter (−1,0 Felder) → bleibt aus. Wissensbasis `bob-knowledge/speedrun.json` (304 Ziele,
  46 Mobs, 16 Strukturen), `docs/bob-reference-times.md`. SIM-Regel geprüft: die Vorausschau zählt in SIM nach Spiel-
  Ticks (60 Spiele/Tick), Uhrzeit nur als Hänger-Wächter.
- **Rust-Nachbauten (Pumpkin, Valence, FerrumC):** geprüft – nein. Keiner kann Fabric/Java-Bob laufen lassen, Mob-KI,
  Loot, Kampf und Advancements fehlen. Stattdessen: abstrakter Simulator für Strategie, Vanilla-Server mit SIM=1 und
  Test-Arenen für Fähigkeiten.
- **BisectHosting-Paket (Bob-Autopilot, `src/autopilot`, `docs/bob-bisect-server.md`):** eigene Start-Jar
  `bob-autopilot.jar` (reines Java 17), startet pro Spiel einen Fabric-Server mit frischer Welt, Liga wie
  `bobleague.py`, Export-Zip alle 12 h zum Hochladen im Chat. Dem Nutzer am 10.11. als `bob-bisect-paket.zip`
  geschickt (Anleitung, Autopilot, Mod-Jar mit Bob-Commit d9c5cac, Fabric API 0.161.0+26.3). Auf einem echten
  Bisect-Panel noch ungetestet; bei 22 GB `league_games=auto` = 3 Spiele parallel.
- **Runde 2 (ab 10.11. ~10:45 UTC):** zwei Build-Workflows – A: `bob/r2-survival` (Ertrinken, Zombies ohne Waffe,
  Skelette vor dem Schild, Deckungsmodell gegen Gruppen) und `bob/r2-kit` (Eisen aus bekannten Strukturen/Höhlen,
  Schmelzen ohne Warten, Adern ganz abbauen, Sprinten, Essen in Sicht, baumlose Starts, Item-Verlangsamung als Knopf);
  B: `bob/r2-brain` (zu optimistische Schätzungen, Simulator auf neuen Code kalibrieren, Vorausschau entscheidet Chores,
  Loot-/Jagd-Routen testen). Danach Integration mit Liga (16 Seeds) und Gate; Wecker kennt den Ablauf.

## Stand 10.11.2026 abends (Bob-Runden beendet, Messen auf dem Server)

- **Nutzer-Feedback (wichtig):** Er wollte große, radikale Verbesserungen, keine kleinen Schritte; die zwei
  Agenten-Runden waren ihm zu teuer für den messbaren Gewinn (je Runde ~3 Mio. erzeugte Tokens, dazu viel
  wiederholt gelesener Kontext, weil Agenten stundenlang auf den Build-Lock warteten). Runde 2 auf seinen Wunsch
  gestoppt, der Zwei-Stunden-Wecker ist gelöscht. **Keine weiteren Bob-Agenten-Runden ohne neuen Auftrag.**
  Vor teurer Arbeit immer Kosten und erwarteten Nutzen nennen.
- **Entscheidung „Option 1“:** Ertrinken-Fix fest an (`drystairs`, `halfair`, `airsafe`, `drowsafe`); alle anderen
  Runde-2-Änderungen zusammengeführt (`bob/r2-knobs`, `26.3-lockout-bot` = 0249894), im normalen Spiel aus
  (`bob-models/champion.json`) und in den Liga-Tabellen (Autopilot `Knobs.java`, Laptop `bobleague.py`, Standard 0;
  `search` 0/2). Die Server-Liga schaltet sie als Herausforderer um. Dem Nutzer `bob-bisect-paket-2.zip`
  geschickt (Mod-Jar Bob-Commit 0249894). Er schickt Export-Zips; eine kurze Sitzung wertet aus.
- **Reserve „Bob Pro“:** falls die Server-Liga nichts bringt – höchste Stufe mit offenen Vorteilen (schneller
  abbauen/laufen, kein Hunger, Start-Kit, Strukturwissen). Vom Nutzer vorerst abgelehnt („wenn 1 nichts bringt,
  dann in Zukunft das“).
- Zwischenstand Runde 2 und offene Testpunkte: `docs/bob-plan.md` Abschnitt 28.

## Stand 10.11.2026 nachts (Runde 3: Algorithmen + Laptop-App „Bob-Trainer“)

- Nutzer wollte modernere Algorithmen (1 Weltmodell/Bayes-Suche, 2 Bewegung mit Spielphysik, 3 Risiko in der
  Wegsuche) und eine Laptop-Software statt Bisect. Erlaubt war **ein** effizienter Agent (verbrauchte ~0,6 Mio.
  Tokens, ~1,8 h). Zweig `bob/r3-algos` = `26.3-lockout-bot` = 8ca58ee (mod_version 1.1.4, nichts veröffentlicht).
- Neue Schalter `riskpath`, `beliefs`, `motionsearch`: im Code an (Tests), in champion.json/Knobs.java/bobleague.py
  aus (Standard 0) – die Liga testet sie zuerst. Gemessen (Szenen, je 3 Läufe): riskpath 0 statt 12–21 HP gegen zwei
  Skelette; beliefs: Schätzungen hängen vom Kontext ab (Eisen 202 s Ebene / 68 s Berg / 37 s bekannte Höhle; Kuh diesseits
  statt über den Fluss 103 statt 184 Ticks); motionsearch nur +3–6 % (Bob sprintet in Testkursen schon 5–7 Blöcke/s; die
  3,3 Blöcke/s aus echten Partien kommen von Pausen, Wasser, Graben – noch nicht gemessen).
- **Bob-Trainer** (`src/autopilot`, Gradle `bobTrainerJar`, `scripts/trainer/`, `scripts/bot/package_trainer.sh`):
  Windows-Start per `Bob-Trainer starten.bat` (unsichtbar, javaw), Dashboard http://127.0.0.1:8765 (Pause, Sofort
  pausieren, Weiter, Beenden, Export, Leistung), EULA nur durch den Nutzer, Java-25-Suche/Download (Temurin), Fabric-
  Server-Launcher gebündelt, Lithium + FerriteCore (C2ME/ScalableLux nicht: Weltgleichheit ungeprüft), +18 % Tempo.
  Liga: jede Partie neue Zufallswelt (gepaart), Bayes-Sequenztest (≥ 8 Welten, P > 0,95 befördern, < 0,05 raus, max 24),
  ungetestete Schalter zuerst, dann Thompson-Sampling; 30-min-Spiele, jedes 5. 90 min; Tagebuch mit Kontext je Ziel.
  Paket `Bob-Trainer.zip` (sha1 db064b3e…) am 10.11. geschickt. Windows/macOS-Skripte nicht im Container getestet.
- Weiter: Nutzer lässt den Trainer laufen und lädt Exporte hoch; kurze Sitzung wertet aus. Reserve „Bob Pro“.

## Stand 12.11.2026 (Bob-Trainer 1.1: Windows/OneDrive-Fix)

- Nutzer hatte den Trainer in `C:\Users\…\OneDrive\Documents\Bob Trainer` entpackt, 8 Liga-Plätze. Fehler:
  „Start nicht moeglich: …\work\liga-N\config“ (alle Plätze, jede 2. Runde; OneDrive markiert/sperrt Ordner) und bei
  neuen Plätzen „Detected incomplete install, reinstalling“ → „used by another process“. Ursache 2: die Startjar von
  Fabrics Download-Launcher nennt ihre Bibliotheken relativ (`../../libraries`) zum **Spielordner**; ein geteiltes
  `.fabric/server` ließ jeden neuen Platz die geteilte Startjar neu schreiben, die laufende Spiele offen halten.
- Fix (Zweig `trainer/onedrive-fix` → `26.3-lockout-bot`, Commits 86ee65a + a3b79c3, Trainer-Version 1.1):
  jedes Spiel eigenes `.fabric/server` + eigene `libraries/`; geteilt nur Minecrafts `26.3-server.jar` über
  `-Dfabric.installer.server.gameJar`; erster Download allein. Liegt der Trainer in OneDrive/Dropbox/Google Drive/iCloud,
  kommen Spielwelten + Minecraft nach `%LOCALAPPDATA%\Bob-Trainer\trainer-<hash>` (Liga, Journal, Logs, Export bleiben).
  Löschen OneDrive-fest (markierte Ordner leeren, Junctions als Link), Hardlinks/Junctions bleiben, Wiederholungen,
  klare Meldungen, `work_dir` (Windows-Pfade mit `\`), Start-Fehler blockieren 20 s statt alle Plätze auf einmal.
- Geprüft: 49 Unit-Tests; 3 echte Läufe mit Minecraft in einem „OneDrive“-Pfad (2 Plätze parallel, 0 Fehler); Review-
  Workflow (7 Agenten) fand 2 echte Fehler (Laufwerkswechsel bei work_dir, geteilte Root-libraries) → behoben.
  Unter Windows selbst nicht getestet. ZIP an den Nutzer: `Bob-Trainer.zip` 1.1 (12.11.).
- Lehre: Auf Linux lassen sich offene Dateien löschen – Windows-Sperren fallen hier nicht auf. Geteilte, beschreibbare
  Dateien zwischen gleichzeitigen Servern vermeiden; Nutzer-Ordner in OneDrive immer mitdenken.
