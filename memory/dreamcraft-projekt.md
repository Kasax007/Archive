# Dreamcraft 26.3 – Projektgedächtnis

Stand 2.11.2026. Auftrag: Modpack **Dreamcraft [FABRIC]** (CurseForge 545167, Slug `dreamcraft-new`) samt Server-Pack
von 1.20.1 V4 auf **Minecraft 26.3** bringen, eigenes Quest-System, Raft-Mod portieren und erweitern, Beschreibungen,
TikTok. Plan und Haken: `dreamcraft/PLAN.md`.

## Projekte und Repos

| Was | Wo | CurseForge |
| --- | --- | --- |
| Modpack-Quelle (Overrides, Quests, Menü, Tools, Beschreibung) | `Kasax007/Modpack-Development`, Branch `26.3` | Modpack 545167 |
| Quest Icons (Quest-System im FTB-Quests-Stil + Icons) | `Kasax007/Kasax_Quests_Items_Mod-1.19.2`, Branch `26.3` | 690531, Datei 9402494 (1.0.0+26.3), 9409345 (1.0.1+26.3) |
| Raft-Mod, auf CurseForge **„Beach Craft“** | `Kasax007/Kasax_Raft_Mod`, Branch `26.3` | 1010922, Datei 9402661 (2.0.0+26.3), 9408472 (2.0.1+26.3) |
| TikTok und Werkzeuge | `Archive/dreamcraft/tiktok` (v2 mit Shadern) | – |
| Beach-Craft-Review und Prüfbericht | `Archive/beachcraft/review` | – |
| Modpack-Dateien | | V1: 9403038 (+ Server-Pack). V1.1: 9408516, Server-Pack 9408519 (Beach Craft 2.0.1, Quests korrigiert). V1.2: 9409459, Server-Pack 9409463 (Menü-Fixes, ohne JER) |

- FTB Quests gibt es für 26.3 Fabric nicht. Das Quest-System steckt deshalb in Quest Icons: Buch mit Taste J,
  SNBT-Dateien in `config/questsicons/quests`, Befehle `/quests` (open, reload, complete, reset, team).
- Die Storyline wird erzeugt mit `tools/dc_quests.py` und `dc_quests_raft.py` im Modpack-Repo, mit 13 Kapiteln und
  über 160 Quests. Die IDs sind FNV-1a-Hashes, also stabil.
- Das Raft-Kapitel heißt „6. The Endless Sea“. Das Portal ist inzwischen machbar: Treibholz wächst an
  Overworld-Stränden, ein Craft ergibt 4 Rahmen, Ringe gibt es in Schiffswrack-, Schatz- und Ruinen-Loot.

## Pack-Technik

- **Basis:** Minecraft 26.3, Fabric Loader 0.20.1, Java 25. 250 CurseForge-Mods plus Quest Icons plus Beach Craft.
- **Build:** `tools/mkpack.py V1 <QuestIcons-Datei> [<BeachCraft-Datei>]` erzeugt das Client-Zip (`manifest.json`,
  `overrides`) und den Server-Pack. Der Server-Pack enthält `start.sh` / `start.bat` mit EULA-Prüfung, `server.properties`
  und `fabric-server-launch.jar`.
- **Entfernte Mods:** stehen mit Grund in `pack/removed.md`. Das waren vor allem Mixin-Konflikte beim frühen Laden
  (FrozenLib, ModernFix-mVUS, SpectreLib) und Registry-Fehler auf dem Server (MCPitanLib, Enhanced Quarries).
  REI wurde durch JEI ersetzt.
- **Menü:** FancyMenu-v3-Layouts `title_screen_dreamcraft_1..8` (zufälliger Hintergrund) und der Drippy-Ladebildschirm.
  Die Welcome-Screens von BetterX und Terralith sind ausgeschaltet.
- **Bekannte harmlose Logs:** In Dungeons and Taverns lassen sich zwei Vorlagen nicht laden (Tippfehler im Mod:
  `axys`, `chisled_polished_blackstone`). Die Teile fehlen dann einfach, das Spiel stürzt nicht ab.
- **Subtle Effects:** Am 2. November (Geburtstag des Mods) zeigt die Mod Partyhüte und kreisende Köpfe. Für
  Aufnahmen `enableEasterEggs = false` setzen.

## Testen (Container)

- **Client-Gametest-Projekt:** `/home/user/dctest`, die Quelle liegt im Modpack-Repo unter `tools/dctest`. Szenen sind
  boot, smoke, quests und film. Die Pack-Mods und -Configs liegen in `build/run/client`.
- **`KeyFix`:** füllt fehlende Tastenbelegungen im Gametest auf.
- **Filmen:** `sh ./gradlew runPack -Pxmx=5G -Pscene=film -Pshots=a,b -Pout=$SP/film [-Prd=12] [-Pnostills=1]`.
  Mehr als 6 GB Heap führte einmal zum SIGKILL.
- **Speicherleck der Fabric-Gametest-API (6.0.11):** `takeScreenshot` gibt das `NativeImage` nie frei, also 8 MB pro
  Bild bei 1080×1920. Nach rund 600 Bildern hat der OOM-Killer den Client beendet (Grenze etwa 13 GB RSS, mit und
  ohne Shader). Behoben mit `mixin/ScreenshotLeakMixin` im Harness: Er schließt das Bild nach dem Speichern.
  Trotzdem filmt `$SP/bc_batches.sh` in Batches zu 5–7 Shots, eine JVM pro Batch.
- **26.3 nutzt SDL statt GLFW:** Maustaste 1 ist dort LINKS, rechts ist 3. `pressMouse(1)` hat deshalb Blöcke
  abgebaut (Truhe zerbrochen). Klicks immer über die Tastenbelegung auslösen: `pressKey(o -> o.keyUse)` bzw.
  `holdKey(o -> o.keyAttack)`.
- **Shader:** Iris + Complementary Reimagined r5.9.3 (`run/client/shaderpacks`, `config/iris.properties`
  `enableShaders`). Auf llvmpipe dauert ein Bild 5–7 s. Das End mit Shadern blieb hängen (Server verhungert).
- **Minikarte:** Für Aufnahmen mit HUD steht in `config/xaero/minimap/profiles/default.cfg` `display_minimap = false`.
- **Film-Takt:** Der integrierte Server tickt in Echtzeit weiter, während ein Bild 0,5–2 s braucht. Serverseitige
  Abläufe (Öfen, Wachstum, Treibgut, Portal) laufen pro Filmsekunde deshalb 3–5-mal schneller. Dinge, die man sehen
  soll, erst im Shot starten (z. B. Setzling bei Tick 1 setzen, Treibgut laufend nachspawnen).
- **Kamera hinter dem Spieler:** Mit `tp … facing <Ziel>` landet das Ziel genau hinter der Figur. Besser seitlich
  versetzt stellen und geradeaus schauen lassen.
- **Koordinaten:** Nie `"%d.5"` formatieren, das ergibt bei negativen Werten einen halben Block daneben. Stattdessen
  `%.1f` mit `+0.5`.
- **Raft-Dimension:** Sie nutzt die Geländeform der Oberwelt mit Meeresspiegel 100, deshalb stehen dort große
  Steinmassive. `BcShots.sea()` sucht über die Basishöhen offenes Meer für die Bühnen.
- **Review-Shots:** `BcShots.java` (`bc_*`). Die meisten spielen auf einer 13×13-Floß-Bühne in `raft:raftdim`, eine
  Bühne alle 200 Blöcke ab x=3000.
- **Shots im Meer:** Der Seed `dreamcraft-film` startet im Ozean. Für Szenen an Land deshalb `findLand()`
  verwenden; es sucht über die Basis-Höhen des Generators trockenes, flaches Land.
- **Luftaufnahmen:** Den Spieler auf einen Barriere-Block stellen. Fliegen per Abilities hat nicht gehalten.
- **Server:** `tools/srv.sh` startet einen Test-Server. Chunky lief in allen Dimensionen inklusive `raft:raftdim`
  ohne Fehler.

## Wie Spieler das Pack bekommen (Produktiv-Test)

- **Warum:** Der Loom-Gametest ist eine Entwicklungsumgebung. Nur ein echter Launcher-Start zeigt, was Spieler sehen.
  Werkzeuge in `Modpack-Development/tools/prodtest`:
  - `cf_install.py` lädt das Pack und jede Manifest-Datei von CurseForge.
  - `launch.py` startet Fabric produktiv.
  - `xin.py` sendet Klicks und Tasten, `xwin.py` ändert die Fenstergröße.
- **Vor jedem Pack-Upload:**
  - Installieren wie ein Launcher.
  - Hauptmenü bei 854×480, 1366×768 und 1920×1080 ansehen und jeden Button klicken.
  - Welt laden, Questbuch (J) öffnen.
  - Server-Pack aus der Zip starten.
- **Funde in V1.1, behoben in V1.2:**
  - Menü zu groß für kleine Fenster. Jetzt FancyMenu `autoscale` mit Basis 1920×1080 bei `setscale 2`.
  - Mods- und Rent-a-Server-Button ohne Aktion: `fresh_ids` vergab für dieselbe UUID verschiedene neue IDs.
  - Drippy-Balken weiß; der Vanilla-Balken ignoriert Farben, deshalb jetzt `drippy_vanilla_bar` mit `color`.
  - Shoulder Surfing startete in der Schulterkamera.
  - JER scheitert an BetterNether-Biomen und wurde entfernt.
  - In den Quests stand noch REI statt JEI.
- **Neue Datei auf CurseForge:** Sie ist erst nach rund 10 Minuten Prüfung herunterladbar. Erst dann ein Pack hochladen,
  das sie referenziert.
- **Beschreibungen:**
  - Als HTML in `docs/curseforge/description.html` jedes Repos, für die Quellcode-Ansicht des CurseForge-Editors.
  - Spoiler sind `<div class="spoiler">`.
  - Dreamcraft behält die BisectHosting-Grafiken (`bh_header`, `bh_promo`, `bh_1`…`bh_6`).
  - Quest Icons behält den Stil des Nutzers (Logo, „Made with love, sweat and tears“, Bisect-Banner, Abschnittsbilder).
  - Beach Craft hat ein eigenes Bisect-Banner `img/bisect.png`.
  - Für Beschreibungen gibt es keine API, der Nutzer fügt sie selbst ein.

## Was der Nutzer will (hier gelernt)

- Ohne Rückfragen durcharbeiten; höchstens ein Sonnet-Subagent.
- Der CurseForge-Token liegt nur in `$SP/.cf_token`. Nie committen und nie ausgeben.
- Beschreibungen im Stil der Tamagotchi-Seite: Header-Bild, Abschnitts-Streifen, Screenshots und Badges.
- Beschreibungen mit BisectHosting-Banner (Code KASAX007) und vielen Spoilern; Pack immer so testen, wie Spieler es installieren.
