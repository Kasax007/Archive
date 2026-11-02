# Dreamcraft 26.3 – Projektgedächtnis

Stand 2.11.2026. Auftrag: Modpack **Dreamcraft [FABRIC]** (CurseForge 545167, Slug `dreamcraft-new`) samt Server-Pack
von 1.20.1 V4 auf **Minecraft 26.3** bringen, eigenes Quest-System, Raft-Mod portieren und erweitern, Beschreibungen,
TikTok. Plan und Haken: `dreamcraft/PLAN.md`.

## Projekte und Repos

| Was | Wo | CurseForge |
| --- | --- | --- |
| Modpack-Quelle (Overrides, Quests, Menü, Tools, Beschreibung) | `Kasax007/Modpack-Development`, Branch `26.3` | Modpack 545167 |
| Quest Icons (Quest-System im FTB-Quests-Stil + Icons) | `Kasax007/Kasax_Quests_Items_Mod-1.19.2`, Branch `26.3` | 690531, Datei 9402494 (1.0.0+26.3) |
| Raft-Mod, auf CurseForge **„Beach Craft“** | `Kasax007/Kasax_Raft_Mod`, Branch `26.3` | 1010922, Datei 9402661 (2.0.0+26.3) |
| TikTok und Werkzeuge | `Archive/dreamcraft/tiktok` | – |

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
- **Filmen:** `sh ./gradlew runPack -Pxmx=5G -Pscene=film -Pshots=a,b -Pout=$SP/film`. Mehr als 6 GB führte einmal
  zum SIGKILL.
- **Shots im Meer:** Der Seed `dreamcraft-film` startet im Ozean. Für Szenen an Land deshalb `findLand()`
  verwenden; es sucht über die Basis-Höhen des Generators trockenes, flaches Land.
- **Luftaufnahmen:** Den Spieler auf einen Barriere-Block stellen. Fliegen per Abilities hat nicht gehalten.
- **Server:** `tools/srv.sh` startet einen Test-Server. Chunky lief in allen Dimensionen inklusive `raft:raftdim`
  ohne Fehler.

## Was der Nutzer will (hier gelernt)

- Ohne Rückfragen durcharbeiten; höchstens ein Sonnet-Subagent.
- Der CurseForge-Token liegt nur in `$SP/.cf_token`. Nie committen und nie ausgeben.
- Beschreibungen im Stil der Tamagotchi-Seite: Header-Bild, Abschnitts-Streifen, Screenshots und Badges.
