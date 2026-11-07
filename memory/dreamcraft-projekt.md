# Dreamcraft 26.3 – Projektgedächtnis

Stand 2.11.2026. Auftrag: Modpack **Dreamcraft [FABRIC]** (CurseForge 545167, Slug `dreamcraft-new`) samt Server-Pack
von 1.20.1 V4 auf **Minecraft 26.3** bringen, eigenes Quest-System, Raft-Mod portieren und erweitern, Beschreibungen,
TikTok. Plan und Haken: `dreamcraft/PLAN.md`.

## Projekte und Repos

| Was | Wo | CurseForge |
| --- | --- | --- |
| Modpack-Quelle (Overrides, Quests, Menü, Tools, Beschreibung) | `Kasax007/Modpack-Development`, Branch `26.3` | Modpack 545167 |
| Quest Icons (Quest-System im FTB-Quests-Stil + Icons) | `Kasax007/Kasax_Quests_Items_Mod-1.19.2`, Branches `26.3` und `26.2` | 690531, Datei 9402494 (1.0.0+26.3), 9409345 (1.0.1+26.3), 9415031 (1.0.2+26.3), 9429010 (1.1.0+26.3, Dream Star); 1.2.0+26.3 und 1.2.0+26.2 (FTB-Import) gebaut, Upload wartet auf Freigabe (7.11.) |
| Raft-Mod, auf CurseForge **„Beach Craft“** | `Kasax007/Kasax_Raft_Mod`, Branch `26.3` | 1010922, Datei 9402661 (2.0.0+26.3), 9408472 (2.0.1+26.3), 9431301 (3.0.0+26.3), 9474711 (3.1.0+26.3) |
| TikTok und Werkzeuge | `Archive/dreamcraft/tiktok` (v2 mit Shadern) | – |
| Beach-Craft-Review und Prüfbericht | `Archive/beachcraft/review` | – |
| Beach-Craft-3.0-Doku „Tides of the Deep“ (18:35, nur Fassung mit Untertiteln + Musik) | `Archive/beachcraft/documentary`, Rohmaterial `footage/bc3` | – |
| Modpack-Dateien | | V1: 9403038 (+ Server-Pack). V1.1: 9408516, Server-Pack 9408519 (Beach Craft 2.0.1, Quests korrigiert). V1.2: 9409459, Server-Pack 9409463 (Menü-Fixes, ohne JER). V1.2.1: 9415062, Server-Pack 9415063 (Quest-Buch-Klick-Hotfix). V1.3: 9431378, Server-Pack 9431379 (Beach Craft 3.0.0, Tamagotchi 1.2.0 = 9431312, Dream Star, 328 Quests)  V1.4: 9475197, Server-Pack 9475219 (Beach Craft 3.1.0 = 9474711, Upgraded Iron Chests, 348 Quests). V1.4.1: 9487507, Server-Pack 9487509 (Menü-Fix). V1.4.2: 9499392, Server-Pack 9499399 (Bisect-Config, Changelog nur „Bug fixes“). |

- FTB Quests gibt es für 26.2 und 26.3 nicht (neueste Datei 26.1.2.10 vom 5.11., nur NeoForge). Seit Quest Icons 1.2.0
  holt `/quests import ftbquests` FTB-Bücher herüber. Das Quest-System steckt in Quest Icons: Buch mit Taste J,
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
- **26.3 nutzt SDL statt GLFW:** Maustaste 1 ist dort LINKS, rechts ist 3. Das gilt auch für `MouseButtonEvent.button()`
  in eigenen Screens: Quest Icons 1.0.1 prüfte noch `button == 0`, ein Linksklick verschob nur die Karte (Spieler im
  Discord konnten keine Quests öffnen/abhaken). Fix in 1.0.2 mit `InputConstants.MOUSE_BUTTON_LEFT/RIGHT/MIDDLE`.
  Eigene GUIs immer mit echten Klicks testen (`setCursorPos` + `pressMouse(InputConstants.MOUSE_BUTTON_LEFT)`), nicht
  nur per Methodenaufruf. `pressMouse(1)` hat deshalb Blöcke
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

## Beach Craft 3.0 (Nov 2026) – Aufbau und Lehren

- **Branch:** `Kasax_Raft_Mod` `3.0-dev` (Version 3.0.0+26.3), Spezifikation `docs/design/beachcraft3.md` (Abschnitt 14 =
  Abweichungen, gilt vor dem Plan). Inhalt: Inselwelt mit 12 Biomen, Story „Tides of the Deep“ (8 Kapitel, 4 Siegel,
  Tidewarden-Schlüssel, Boss Leviathan), 7 Story- und 12 Nebenstrukturen, 13 Kreaturen, Expeditionsfloß + 4 Boote,
  Tauchausrüstung, ~150 Bau-/Dekoblöcke, Guide Book „Seafarer's Almanac“, 95 überarbeitete 2.0-Texturen.
- **Module:** `net.kasax.raft.content.<modul>` (world, building, decor, shore, marine, voyage, diving, story, boss, guide)
  plus Strukturmodule (nur Daten). Jedes Modul hat eigene Ressourcen in `src/main/modules/<modul>/`, eigene Mixin-Config
  `raft-<modul>.mixins.json` und Python-Generatoren `tools/content/<modul>/gen.py`. Gradle `mergeResources` führt Lang,
  Tags und sounds.json zusammen; jede andere doppelte Datei bricht den Build ab.
- **Werkzeuge:** `tools/bclib` (assets.py 26.3-JSON, tex.py Pixel-Art, nbt.py Strukturvorlagen im 26.3-Format
  id/properties, preview.py isometrische Vorschau), `tools/bctest/run.sh <skript> <out>` = skriptbarer Client-Gametest
  (world/cmd/pcmd/settle/shot/count/sneakuse/esc/slot; `BC_JFR=` für Profiling), `$SP/ref/jc.sh` = schneller javac-Check
  unter dem gemeinsamen Lock `$SP/ref/build.lock`.
- **Gesamtdokumentation** (Deutsch, alle Projekte): `dokumentation/README.md` und Kapitel 01–08.
- **Lehren:**
  - 26.3/SDL: Maustasten links=1, Mitte=2, rechts=3 und Escape=41 – nie feste GLFW-Zahlen; GUIs mit echten Klicks testen.
  - Strukturvorlagen: Blöcke ohne `rotate()/mirror()`-Override (BaseEntityBlock mit FACING) drehen sich bei gedrehten
    Jigsaw-Starts nicht mit. Teppiche/Fackeln in überfluteten Strukturen werden weggespült (Items liegen herum).
  - Jigsaw-Start mit fester Höhe liegt 1 Block unter `start_height` (Ground-Level-Delta).
  - Dimension-Licht: `ambient_light` 0.0 + `ambient_light_color` #0a0a0a wie die Oberwelt, sonst ist alles immer hell.
    Vanilla hellt Wasser-Nebel nach ein paar Sekunden auf (Kanal-Skalierung) – Tiefsee-Nebel ohne Rotanteil wählen.
  - Spawns: Kreaturen-Dichte über Spawn-Kosten (Fabric `addMobCharge`), sonst füllen Korsaren/Wale/Mantas die Caps.
  - `/give` erzeugt zuerst ein Fake-Item: Despawn-Schutz im ENTITY_LOAD-Event muss Fake-Items (Alter 5999) auslassen.
  - Gametest-Rechner ist langsam (neues Gebiet 3–5 min bei rd 8, Oberwelt ähnlich): `rd 5`, Läufe bündeln.
  - Nutzungslimit: höchstens ein, wenn nötig zwei Subagenten (Wunsch des Nutzers, 4.11.); Arbeit vorher in WIP-Commits sichern.
  - Strukturen: Features eines Schritts laufen nach den Strukturen desselben Schritts, Features der Nachbar-Chunks
    auch noch später. Alles, was Blöcke setzt, braucht `raft:clear_of_structures` (ohne Höhe: `whole_column`).
    Strukturen überlappen ohne Schutz: Rang-Tags `raft:priority/*` (StructurePriority). Vor dem Release jede Struktur
    mit `bctest audit` prüfen (`scout`, `forceload add {x0:i} {z0:i} {x1:i} {z1:i}`, `audit`, `npcview`, `shotif`).
  - Wasser spült Spinnweben, Teppiche, Fackeln und Schädel weg: Items treiben dann herum (Fischerboot-Netze).
  - Doku-Filmen mit bctest (`rec`/`still`, Welt `saves/bcdoc`): nach `fill`/`setblock` und nach weiten Teleports ein
    `settle`, sonst zeigen Bilder alte Chunk-Meshes; `faceblock`+`use` nur innerhalb eines `rec`; in der dritten Person
    das Ziel seitlich legen (sonst hinter dem Kopf); die Raft-Dimension hat feste Tageszeit (Hängematte setzt nur den
    Spawn). Details und weitere Lehren: `beachcraft/documentary/README.md`.
- **Weitere Releases dieser Runde:** Quest Icons 1.0.2 (Klick-Hotfix, Datei 9415031) und 1.1.0 (Dream Star, Datei
  9429010); Dreamcraft V1.2.1 (9415062, Server 9415063). Am 4.11. mit Freigabe des Nutzers hochgeladen: Beach Craft 3.0.0
  (9431301), Tamagotchi 1.2.0 (9431312, direkt per CurseForge-API; Tag `v1.2.0` fehlt, Tag-Push geht aus der Sitzung
  nicht), Dreamcraft V1.3 (9431378, Server 9431379). Challenge Craft: Fixes nur auf
  Branch `bugcheck-2026-11` (Bericht `docs/BUGCHECK-2026-11.md`), keine Versionsänderung.

- **Testrunde (Aufgabe des Nutzers, verschoben auf Mo 9.11.2026 14:10, Reminder gesetzt):** Werkzeuge im Repo
  Modpack-Development: `tools/qsource.py` (statisch: Quelle jedes Quest-Items; 292/298 gefunden, 6 per Mechanik/Code-Loot
  im Spiel prüfen), `tools/qrun_plan.py` + dctest-Szene `qrun` (alle 328 Quests im Spiel), Szene `bccheck` (Checkliste
  Beach Craft/Dreamcraft, BcCheck noch nicht kompiliert), `tools/prodtest/mk121.py` (Upgrade-Test V1.2.1 -> V1.3).
  Details: `tools/dctest/README.md`.

- **Stand 4.11. abends:** Challenge Craft Modpack v5 (Upgraded Iron Chests + Storage Drawers) gebaut und Server-Test ok, Upload erst nach der Testrunde (Wunsch des Nutzers). Dreamcraft V1.4 in Arbeit: Upgraded Iron Chests + Kapitel „Quality of Life“ (344 Quests, 15 Kapitel). Beach Craft: Fixes + Doku v2 (Agent), Floß-Bau, Sounds/Musik, NPCs (je ein Agent, Worktrees /home/user/wt/*, Branches feature/*), danach Merge nach 26.3 und Release als 3.1.0.

- **Beach Craft 3.1.0+26.3 (5.11.):** Floß selbst bauen (Werft: Blöcke laufen beim Segeln weiter), Sounds und Musik (Kevin MacLeod, Credits im Jar und in der Beschreibung), 8 NPCs, dazu Tag/Nacht, Coral Temple, keine harten Kanten, neue Pflanzen und Deko. Gemergt nach 26.3 (cf5ceb8), Smoke-Test 15/15, nicht hochgeladen. Jar $SP/release_bc31/ ist von cf5ceb8 und muss vor dem Upload neu gebaut werden. Deck-Fix (Spieler landet nach Teleport, Login oder Dimensionswechsel auf dem Deck, nicht darunter) am 5.11. gemergt: 26.3 = e6b344b (darin auch 212c89e, Blumen auf jeder Palmen-/Dschungelinsel).
- **Testrunde 5.11.:** Quest-Prüflauf aller 344 Dreamcraft-Quests im Spiel bestanden (nach Harness-Fixes; Mutant-Zombie-Text ergänzt), Beach-Craft-Checks bestanden (Deck, Hängematte, Pets, Sounds, Dream Star, Strukturen). Offen: Boss-Heilung nach 30 s ohne Spieler nur im Code geprüft; echte Klicks im Quest-Buch, Server mit zwei Spielern. Ergebnisse stehen in `dokumentation/08_offen_und_zu_testen.md`.
- **Doku v2 (5.11.):** Agent filmt im Querformat mit 60 fps und Shadern (Material `footage/bc3v2`, Werkzeuge `beachcraft/documentary/v2`). Eine zweite Cloud-Sitzung (session_01Fk46dZfoCwmH5t6YA3jjnj) filmt NPC- und Floß-Szenen (n_*, r_*) und pusht sie ins Archiv. Nutzer will nur die Fassung mit Untertiteln und Musik, fürs Handy als Artefakt-Seite (720p, Teile unter 14 MB).

- **Doku v2 fertig (6.11.):** 21:27, 1080p60, in 13 Teilen im Archiv (`beachcraft/documentary/v2/`); Handy-Fassung
  (720p30, 202 MB, 15 Teile à 14 MB) auf der Artefakt-Seite https://claude.ai/artifact/K6LP4TwjmvqFpjuDqEiEoP.
- **Strukturprüfung 6.11.:** neues Werkzeug `bctest audit` (StructAudit: Block-für-Block-Vergleich mit den Vorlagen,
  Personen, Items). 95 Strukturen in 2 Welten: Ashen Forge voll Basalt (Voss in der Wand), Rig auf dem Sanctum,
  Bäume im Leuchtturm, Sand-Rechteck der Strandbar, u. a. Alles behoben im Branch `fix/structure-features`
  (Filter `raft:clear_of_structures`, `StructurePriority`, Ebenheit für Strandbar/Camp, Mindesttiefe Flugzeug,
  Netze, Heavy Core, Port Solace `max_distance_from_center` 104). Kontrolle: 0 Fremdblöcke, 36/36 Personen in
  Ordnung. Gemergt: 26.3 = 88ce4aa (gepusht). Release-Jar neu gebaut ($SP/release_bc31/, 6.11. 02:12), Server-Smoke-Test
  ok (0 Fehler, 256 Chunks Endless Sea). Bericht mit Bildern: Archiv `beachcraft/structure-check/`. 3.1.0 hochgeladen am 6.11.
  (Datei 9474711, mit Kai in allen drei Lagerarten), Dreamcraft V1.4 danach (9475197, Server-Pack 9475219). Alle drei
  Dateien am 6.11. nachmittags freigegeben (Download-Link antwortet mit 307).
- **Beschreibungen 6.11. (nachmittags):** Wunsch: die Doku in die Beach-Craft-Beschreibung, Text deutlich kürzer, mehr
  Grafiken. Neue Seite für 3.1 (26.3 = 2fa8947): 733 statt 8.256 Wörter, 25 Bilder aus `make_images31.py` (header_31,
  video.jpg, glance.png mit Zahlen aus dem Code, flow_start/flow_raft, Shader-Collagen `*_31.jpg`). Der Video-Block steht
  zwischen `<!-- VIDEO START -->` und `<!-- VIDEO END -->` mit dem Platzhalter `VIDEO_ID` (Player und Bild mit Link).
  Übergabeseite https://claude.ai/artifact/8ueVVjUpMDcYKjFBUNtdKL (`curseforge/delivery/build.py`): Kopier-Knöpfe für
  alle vier Beschreibungen; das Feld für den YouTube-Link setzt die ID ein, ohne Link fällt der Block weg; dazu Titel und
  Beschreibung für YouTube. Upload-Kit `beachcraft/documentary/v2/youtube.md`. Dateien im Chat: Limit erst 500, dann 400 MiB;
  die 1080p60-Doku (610 MiB) deshalb als HEVC neu kodiert (2 Pässe, 2250 kbit/s, 374 MiB, geliefert). Die alten 3.0-Bilder in `img/` erst
  löschen, wenn die neue Seite online ist. Offen beim Nutzer: Doku auf YouTube laden, Beschreibungen einfügen.
- **Großer Auftrag 7.11. abends (3 Agenten, Opus, high):** Nutzer: QI hochladen (erledigt: 26.3 = Datei 9499549,
  26.2 = 9499550), dann 1.21.1-Backports von Beach Craft, Tamagotchi und Quest Icons, designte Beschreibungen für
  Challenge Craft Mod + Modpack, Quest Icons für jede sinnvolle MC-Version, Outreach-Tool mit Gmail. Vorher QI 1.3.0
  mit sehr vielen Icons (ABC, Zahlen, Kommentar-Wünsche) und einem einfachen Ingame-Editor ohne SNBT („Not everyone
  can easily write SNBT“). Laufend: Agent A QI 1.3.0 (Icons + Picker + Editor, 26.3/26.2), Agent B Beach Craft
  `port/1.21.1`, Agent C Tamagotchi `port/1.21.1`. Danach: Challenge-Craft-Beschreibungen, QI-Backports (Versionen
  nach Modpack-Daten). Uploads erst nach Prüfung; öffentliche Uploads brauchen die Freigabe im Chat.
- **Outreach v2 (7.11.):** Seite 61GSVUCx8Z4BjonZtYFfpE Version 2: Freigeben → Senden über den Gmail-Connector des
  Nutzers (mcp Gmail send_message/create_draft; Argumente to[], subject, body, includeSignature, replyThreadId),
  „Alle senden“, Kopieren & Öffnen für Kommentare/Discord. E-Mail-Adressen nur in der privaten Datenbank (bei
  stop/no gelöscht). Challenge Craft (Mod 1508454, Modpack 1653698) wird jetzt bei Creatorn beworben (Vorlage E);
  Routine trig_01CCt95NzvUNE8aKqaNFs2oi entsprechend angepasst.
- **Dreamcraft V1.4.3 (in Arbeit, 7.11.):** Nutzer: WorldEdit-Wand Holzhacke statt Holzaxt; Inventar zu voll (lila
  Pfeile = IPN-Nachfüll-Symbole, NONE-Leiste = IPN-Profile), keine Wisch-Animation (Smooth Swapping), kein
  Slot-Highlight. Configs: `config/inventoryprofilesnext/inventoryprofiles.json` (Abschnitte ModSettings,
  GuiSettings, AutoRefillSettings), `config/smoothswapping.json` (toggle_mod false), `config/worldedit/
  worldedit.properties` (wand-item=minecraft\:wooden_hoe).
- **V1.4.2 Bisect-Config (7.11. abends):** Nutzer: „Bei meinem Modpack fehlt die bisectmod config … damit ich meine
  Provision erhalte!! Quick fix!! Nur ‚bug fixes‘ in den Changelog.“ Die Mod bhmenu war im Pack, die Config nie.
  Jetzt `pack/overrides/config/bhmenu/bhmenu.properties` mit partner_id 4395 und pack_id 19732 (aus Dreamcraft
  1.20.1). Challenge Craft hat partner_id 4385 – Nutzer soll die richtige ID in der Bisect-Konsole prüfen. **Jedes
  Pack braucht diese Config; bei neuen Packs immer mitliefern.** Upload: 9499392 / Server-Pack 9499399.
- **Quest Icons 1.2.0 (7.11.):** Wunsch „Quest-Icons machen wir 26.2 plus ein Import von Feedback Requests Feature“
  (als FTB-Quests-Import verstanden und so gemeldet). Agent baute `/quests import ftbquests [preview|run|merge]
  [Ordner]` (Bericht `config/questsicons/ftbquests-import-report.txt`, Backup in `config/questsicons/backups/`; liest
  1.20-SNBT, 1.21-SNBT mit lang und 26.1-JSON5) und portierte auf 26.2 (Branch `26.2`, Loader 0.18.4+). Tests: 16 JUnit,
  sechs echte Modpack-Bücher bis 4.978 Quests, Selbsttest 60/60 auf beiden Versionen, Produktiv-Server. Jars in
  `$SP/release_qi12/` (sha1 26.3 e8d50612…, 26.2 0f871056…), Metadaten `$SP/qi120_<v>_meta.json` (Spielversion 26.3 =
  17045, 26.2 = 16498). Beschreibung 1.2 (81919fa, `make_images_v3.py`) und neue Kurzbeschreibung auf der
  Übergabeseite (Version 7). **Upload offen:** Die Auto-Mode-Prüfung stoppte ihn zweimal („Create Public Surface“);
  der Nutzer muss ihn im Chat freigeben. Danach: Freigabe prüfen (307), Outreach-Holds für 26.2 lösen, Doku 02/08.
- **Outreach (7.11.):** Entscheidungen des Nutzers: Bisect-Banner bleiben oben, Name „Tamagotchi“ bleibt, Modrinth
  später, Quest Icons 26.2 + FTB-Quests-Import (Agent), Outreach ja. `Archive/outreach/` (discover.py, score.py,
  targets.csv, suppression.csv, drafts/, seed_page.py, page/). Freigabeseite mit Datenbank (nur Owner/Editor):
  https://claude.ai/artifact/61GSVUCx8Z4BjonZtYFfpE (25 Entwürfe: 19 bereit, 6 warten auf Modrinth/26.2).
  Werktags-Routine trig_01CCt95NzvUNE8aKqaNFs2oi (7:37 Uhr deutscher Zeit, in diese Sitzung): Status übernehmen,
  Mo/Do suchen, bis 5 neue Entwürfe, freitags KPIs. Nie selbst senden. E-Mails brauchen die Postanschrift des
  Nutzers (auf der Seite eintragen). Den Dreamcraft-Short gibt es schon auf YouTube (G-whF3xKTQ4, alte Fassung).
- **Wachstumsplan (7.11.):** Recherche zu CurseForge-Ranking, Optimierung, neuen Projekten und Outreach:
  `research/curseforge-wachstum-2026-11.md` (+ CSV), Seite https://claude.ai/artifact/PrjZuwcwu8HErjGgS6doef
  (`research/tools/build_growth.py`). Kern: Popularity ≈ Downloads der letzten 60–90 Tage; Suche nur Name +
  Summary; Modpack-Aufnahme ist der größte Hebel; Modrinth fehlt. Offene Entscheidungen beim Nutzer: Bisect-Banner
  nach unten (Regel vom 22.10.2026), Name „Tamagotchi“ (Bandai-Marke), neue Namen/Summaries in der Author Console.
- **V1.4.1 Menü-Fix (6.11. nachts):** Der Nutzer sah im Trailer, dass Singleplayer, Multiplayer, Options und Quit Game
  hinter dem lila Balken lagen (Vanilla-Knöpfe unter dem eigenen Bild-Element). Fix: `render_custom_elements_behind_vanilla
  = true` in allen 8 Titel-Layouts (Modpack-Development 20856ba), im Produktiv-Client geprüft. **mkpack.py baut aus
  `$SP/pack/overrides`, nicht aus dem Repo** – Änderungen dorthin kopieren. V1.4.1 hochgeladen am 7.11. um 7:31 Uhr
  deutscher Zeit: Client 9487507, Server-Pack 9487509. Trailer-Menü-Shot und Seitenbild erneuert.
- **Alle vier Seiten grafisch (6.11. abends):** Wunsch: Dreamcraft, Tamagotchi und Quest Icons „genauso super gestalten
  wie bei Beach Craft“. Zwei Agenten bauten sie, jede Seite mit eigener Optik und eigenem Bild-Generator, jede Zahl aus
  dem Code: Dreamcraft 21bf9e6 (`make_images_v14.py`, Traum-Stil der BisectHosting-Banner, 251 Mods, 348 Quests, 157
  neue Biome, Mod-Liste im Spoiler), Tamagotchi 9a3e063 und Quest Icons c0087b6 (je `make_images_v2.py`). Video-Blöcke:
  Dreamcraft-Trailer (0:44) und Tamagotchi-Showcase (2:03), beide Hochformat, iframe 405×720. Übergabeseite (gleicher
  Link) mit allen vier Vorschauen und einem YouTube-Feld je Video; Werkzeuge in `Archive/curseforge/delivery/`.
  Dreamcraft-Trailer v3: sagt „over three hundred quests“ (vorher 160), Endkarte aus den Shader-Clips, 44,2 s.
  x265 mit zwei Pässen: beide Pässe brauchen `-fps_mode passthrough`, sonst zählt der zweite mehr Bilder und der
  Encoder hängt am Ende (Datei ohne moov, unbrauchbar).
- **Film-Feedback 6.11. (vormittags):** Nutzer vermisste Anglerfisch, Containerschiff und das Crafting am Anfang
  (Ring/Energie aus Schiffswracks). Gewünscht waren neue Sounds für Mantarochen, Motor und Boss, sichtbares Eingraben der
  Krabbe, natürlichere Möwenschwärme und Aale sowie einen besseren Tauch-Clip. Mod (26.3 = 6097aca, gepusht):
  - Motor: Dauerschleife `block.raft_motor.run`, die mit der Geschwindigkeit lauter und höher wird, dazu
    `block.raft_motor.start`.
  - Manta: eigene Rufe.
  - Boss-Sounds mit mehr Präsenz (Mitten und Rauheit).
  - Möwen fliegen in einer V-Formation nach Rang, die sich weich dreht, in langen Bögen.
  - Muränen liegen waagerecht im Loch; Krabben graben sich 0,85 s lang mit Sand ein.
  - Neues bctest-Kommando `track` (Positionsdaten für Bewegungsmessung).
  Neuaufnahmen mit `v2/tools/runs3.py`: c_manta(2), c_moray (Ruinenwand mit Loch, Taucher), c_crab_dig,
  c_gulls(2-4, am besten c_gulls3 über offenem Meer), c_gull_peck, f_crops (Beete + Vogelscheuche auf eigenem Floß),
  r_motor, w_beach (Treibholz-Stumpf). Zweite Sitzung filmte Ring, Schmelzen, Crafting, Anglerfisch, Containerschiff
  und Tauchen. Film-Agent: doc.py-Fix (Vanilla-Dateien von raft-Events waren stumm), Motorschleife statt Basedrum,
  Flop-Ausdünnung. Release-Jar neu (6097aca), Server-Smoke ok.
- **Film-Werkzeug 6.11. abends (wichtig für jede künftige Aufnahme):**
  - `bctest rec` lief bis 26.3 c8da36f dreimal zu schnell. Ein Screenshot ließ das Spiel 2 Ticks laufen, während das
    Bild von der GPU kam. Seitdem hält `holdWorld` (TickRateManager + LocalPlayer) die Welt dabei an: ein Clip-Sekunde
    ist eine Spiel-Sekunde, und shot.json bekommt `"realtime": true`. doc.py liest den Faktor pro Clip (alt = 3).
  - Ein `cmd kill @e[...,distance=..]` des Servers läuft im Overworld-Spawn und erreichte die Floß-Dimension nie.
    Herbeigerufene Tiere häuften sich deshalb in bcdoc2 an. Immer `pcmd kill` (um den Spieler) nutzen;
    film2._kill tut das jetzt.
  - In Echtzeit neu gedreht: c_manta(2), c_moray, c_angler, c_crab_dig, c_gull_peck, c_gulls3/4.
  - Alle älteren Clips der Doku laufen noch dreifach schnell. Echtzeit-Neudreh nur auf Wunsch (großer Aufwand).

## Was der Nutzer will (hier gelernt)

- Ohne Rückfragen durcharbeiten; höchstens ein, wenn nötig zwei Subagenten (Wunsch vom 4.11.2026).
- Der CurseForge-Token liegt nur in `$SP/.cf_token`. Nie committen und nie ausgeben.
- **CurseForge-Uploads nur mit Freigabe im Chat:** Seit 7.11. stoppt die Auto-Mode-Prüfung Uploads als öffentliche
  Veröffentlichung, auch wenn alles vorbereitet ist. Vorher fragen (Datei, Version, Spielversionen nennen), alles
  andere (Beschreibung, Doku, Seite) schon fertig machen.
- **Große Videos nie über den Chat schicken:** Der Nutzer ist meist am Handy, und die Claude-App lädt große Dateien
  aus dem Chat nicht („offline“, 4.11. und 6.11.). Stattdessen eine Artifact-Seite mit „Video laden“ und „Als MP4
  speichern“ (downloads): bis 256 MB als Dateien der Seite, darüber als Assets (Quota 1 GiB je Artefakt, je Stück
  höchstens 20 MiB; ein Stück darf nicht mit `<` beginnen, sonst gilt es als Markup). Beispiel: Doku 1080p60,
  https://claude.ai/artifact/L3gp3aBtLzw4Rt7jdN8Z8L (20 Stücke, Quelltext in `beachcraft/documentary/v2/share/`).
- Beschreibungen im Stil der Tamagotchi-Seite: Header-Bild, Abschnitts-Streifen, Screenshots und Badges.
- Beschreibungen mit BisectHosting-Banner (Code KASAX007) und vielen Spoilern; Pack immer so testen, wie Spieler es installieren.
