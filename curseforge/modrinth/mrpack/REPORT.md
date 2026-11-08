# Modrinth-Modpacks: Prüfbericht (Vorbereitung, nichts hochgeladen)

Stand 2026-11-08. Quelle: die CurseForge-Exporte `out/Dreamcraft 26.3 V1.5.1.zip` und `cc41/Challenge Craft 26.3-v4.2.zip`.
Abgleich über die öffentliche Modrinth-API (`POST /v2/version_files` mit SHA-1, danach Projekt-/Versionssuche).
Es wurde nichts hochgeladen und auf Modrinth/CurseForge nichts verändert.

## Zahlen

| Pack | Dateien im CF-Manifest | matched_by_hash | matched_other_version | own_pending | missing | Einträge in files[] jetzt |
| --- | --- | --- | --- | --- | --- | --- |
| Dreamcraft 26.3 V1.5.1 | 253 | 231 | 11 | 3 | 8 | 242 |
| Challenge Craft 26.3-v4.2 | 30 | 29 | 0 | 1 | 0 | 29 |

Bei jedem Hash-Treffer stimmen SHA-1, SHA-512 und Dateigröße der Modrinth-Datei mit der CurseForge-Datei überein (geprüft).
Alle Download-URLs in files[] liegen auf `cdn.modrinth.com`.

## Abhängigkeiten in modrinth.index.json

| Pack | minecraft | fabric-loader | versionId |
| --- | --- | --- | --- |
| Dreamcraft | 26.3 | 0.20.1 (aus dem CF-Manifest `fabric-0.20.1`) | V1.5.1 |
| Challenge Craft | 26.3 | 0.19.5 (aus dem CF-Manifest `fabric-0.19.5`) | v4.2 |

Beide Loader-Versionen und Minecraft 26.3 stehen im Fabric-Manifest von Modrinth (`launcher-meta.modrinth.com/fabric/v0/manifest.json`).
Kein Mod der beiden Packs verlangt laut `fabric.mod.json` einen neueren Loader als den eingetragenen.
Hinweis: Challenge Craft läuft damit auf einem älteren Loader als Dreamcraft (0.19.5 statt 0.20.1); so steht es im CF-Manifest.

## Eigene Mods (own_pending, noch nicht in files[])

Werden mit `finish.py` und einer `own.json` ergänzt (Vorlage: `python3 finish.py --template`). Die Uploads müssen byte-identisch sein, sonst lehnt `finish.py` den Eintrag ab (Abgleich per SHA-1).

| Pack | Mod | Modrinth-Projekt | CF-Datei-ID | Datei | Größe | SHA-1 |
| --- | --- | --- | --- | --- | --- | --- |
| Dreamcraft | Quest Icons | quest-icons (ohf5LwXu) | 9501059 | `mods/QuestIcons-1.3.0-26.3.jar` | 1155678 | `20deeb9d6270c58d4ec39487e5bfd924915de1dc` |
| Dreamcraft | Beach Craft | beach-craft (3PmzwJU0) | 9507188 | `mods/raft-3.3.0-26.3.jar` | 28132885 | `a0c26ad17e3fa7e10f958ba9e50dd69c6ae1978a` |
| Dreamcraft | Tamacraft | tamacraft (lyuVXQEh) | 9501672 | `mods/tamacraft-1.3.0.jar` | 1865607 | `328cedd50a8b62ebd9eb36d149e965a72bf68d04` |
| Challenge Craft | Challenge Craft | challenge-craft (3qs3GQyx) | 9399763 | `mods/challengecraft-1.1.3.jar` | 3228269 | `3606cbbb2ae8a91b8aeb6be9ffa332a2a0a15a4a` |

SHA-512 und env stehen in `mapping.json` unter `own`. Alle vier: env client required / server required (`fabric.mod.json` environment `*`).

## Ersetzt durch eine andere Modrinth-Datei (matched_other_version, nur Dreamcraft)

Bei allen elf ist es **dieselbe Mod-Version** wie auf CurseForge; die Dateien unterscheiden sich nur im Hash. Geprüft durch Vergleich der Jar-Inhalte (CRC jedes Eintrags außer `META-INF/`).

| Mod (CF-Datei) | Modrinth-Projekt | Modrinth-Version | Unterschied |
| --- | --- | --- | --- |
| Bobby (`bobby-5.2.16+mc26.3.jar`) | bobby | 5.2.16+mc26.3 | same mod version; jar content identical apart from META-INF (separate upload/build) |
| Cloth Config API (Fabric/Forge/NeoForge) (`cloth-config-26.3.158.jar`) | cloth-config | 26.3.158+fabric | same mod version 26.3.158; only the random architectury_inject_* class folder name differs (separate build) |
| Cooking for Blockheads (`cookingforblockheads-fabric-26.3-26.3.0.2.jar`) | cooking-for-blockheads | 26.3.0.2+fabric-26.3 | same mod version; content identical apart from META-INF |
| FallingTree (`FallingTree-26.3-25.jar`) | fallingtree | 26.3-26.3.0.4 | same file FallingTree-26.3-25.jar (CF upload 2026-10-20 = Modrinth 26.3.0.4 upload); only META-INF/MANIFEST.MF differs |
| Farming for Blockheads (`farmingforblockheads-fabric-26.3-26.3.0.1.jar`) | farming-for-blockheads | 26.3.0.1+fabric-26.3 | same mod version; content identical apart from META-INF (Modrinth also has newer 26.3.0.2) |
| Forgiving Void (`forgivingvoid-fabric-26.3-26.3.0.2.jar`) | forgiving-void | 26.3.0.2+fabric-26.3 | same mod version; content identical apart from META-INF |
| Just Enough Professions (JEP) (`JustEnoughProfessions-fabric-26.3-130.0.jar`) | just-enough-professions-jep | 130.0 | same mod version; content identical apart from META-INF |
| Macaw's Bridges (`mcw-bridges-3.1.2-mc26.3fabric.jar`) | macaws-bridges | 3.1.2 | same mod version; only a LICENSE_template-mod file differs |
| Shogi (`shogi-fabric-26.3-26.3.0.3.jar`) | shogi | 26.3.0.3+fabric-26.3 | same mod version; content identical apart from META-INF |
| Storage Drawers (`StorageDrawers-fabric-26.3.0.1.jar`) | storagedrawers | 26.3.0.1+fabric | same mod version; content identical apart from META-INF |
| TerraBlender (Fabric) (`TerraBlender-fabric-26.3-26.3.0.0.9.jar`) | terrablender | 26.3.0.0.9 | same mod version; content identical apart from META-INF |

## Fehlende Mods (missing, nur Dreamcraft) – nicht in files[] und nicht in overrides

| Mod (CF-Projekt / Datei) | Mod-ID | Lizenz | Auf Modrinth | Overrides erlaubt? | Was hängt daran | Empfehlung |
| --- | --- | --- | --- | --- | --- | --- |
| Cupboard (326652 / `cupboard-fabric-26.3-4.2.jar`) | `cupboard` 26.3-4.2 | ARR (fabric.mod.json) | not found (Someaddons mods are not on Modrinth) | no | required library of Memory Settings, Server Performance - Smooth Chunk Save and Structure Essentials (all also missing); no quest references | drop together with its three dependants |
| EpheroLib (885449 / `epherolib-fabric-26.3-1.3.0.jar`) | `epherolib` 1.3.0 | LGPL-3.0 (fabric.mod.json; Modrinth page: LGPL-3.0-only) | project epherolib (DIIgdJzf) exists, but has no Minecraft 26.3 Fabric version (newest Fabric: 1.21.2) | yes by license (LGPL-3.0: redistribution allowed with license text; attribution required) | no other mod in the pack declares it as a dependency and no jar references com/epherical classes; no quest references | drop (unused library) |
| fix GPU memory leak (882495 / `gpumemleakfix-fabric-26.3-1.9.jar`) | `gpumemleakfix` 26.3-1.9 | ARR (fabric.mod.json) | not found | no | nothing depends on it; no quest references (performance fix only) | drop |
| Memory Settings (526901 / `memorysettings-fabric-26.3-6.1.jar`) | `memorysettings` 26.3-6.1 | ARR (fabric.mod.json) | not found | no | nothing depends on it; no quest references (needs Cupboard) | drop |
| More Villagers [Fabric] (486080 / `morevillagers-fabric-8.2.1+26.3.jar`) | `morevillagers` 8.2.1 | MIT in fabric.mod.json, but the source repo LICENSE (github.com/samedifferent/morevillagers) puts all resources (textures, models, data) under All Rights Reserved; only code is MIT | not found (search for More Villagers / morevillagers finds only other projects) | no (the jar contains the ARR resources) | nothing depends on it; no quest references; no override config references | drop (or ask the author for permission) |
| Quarry Reborn (511254 / `quarry-reborn-26.3-1.2.2.jar`) | `quarrymod` 1.2.2 | CC0-1.0 in the jar fabric.mod.json, but the Modrinth project page says CC-BY-NC-4.0 (conflict); source repo github.com/TED-inc/FabricQuarry not reachable (403/404) | project quarry-reborn (Hg6ZLVmu) exists, but newest Fabric version is for 1.20.4; no 26.3 version | unclear: CC0 in the jar would allow it, the Modrinth page license (CC BY-NC 4.0) allows only non-commercial with attribution | no mod depends on it (it depends on Tech Reborn); one optional quest "Quarry Reborn" in chapters/industry.snbt (task quarrymod:quarry, reward 16x quarrymod:drill_tube); no other quest depends on that quest | drop for the Modrinth version and remove/replace the optional quest, or ask the author before shipping it in overrides |
| Server Performance - Smooth Chunk Save (582327 / `smoothchunk-fabric-26.1-4.4.jar`) | `smoothchunk` 26.1-4.4 | ARR (fabric.mod.json) | not found | no | nothing depends on it; no quest references (needs Cupboard); note: this CF file is the 26.1 build (26.1-4.4) | drop |
| Structure Essentials (832882 / `structureessentials-fabric-26.3-5.1.jar`) | `structureessentials` 26.3-5.1 | ARR (fabric.mod.json) | not found | no | nothing depends on it; no quest references (needs Cupboard) | drop |

Folgen, wenn alle acht fehlen:
- Spielinhalt: Quarry Reborn (ein optionaler Quest in `industry.snbt`, auf den kein anderer Quest aufbaut), More Villagers (zusätzliche Dorfbewohner-Berufe; keine Quest- oder Config-Bezüge), Structure Essentials (Struktur-Tuning).
- Nur Technik/Leistung: fix GPU memory leak, Memory Settings, Smooth Chunk Save, Cupboard (Bibliothek der drei Someaddons-Mods), EpheroLib (von keinem Mod im Pack benutzt).
- Keine der acht Mod-IDs steht in einer Config der Overrides; nur `modlist.html` (gehört nicht ins .mrpack) nennt EpheroLib und Cupboard.
- Welten, die mit der CurseForge-Fassung erstellt wurden, verlieren beim Wechsel Blöcke/Items von Quarry Reborn und More Villagers.
- Nicht geprüft: ob ein Jar-in-Jar eines anderen Mods EpheroLib braucht (geprüft wurden die `depends` aller `fabric.mod.json` und Klassenverweise auf `com/epherical` in den Haupt-Jars).

Ersatz auf Modrinth wurde nicht gesucht/ausgewählt (Auswahl ist eine Entscheidung des Nutzers). Mögliche Richtung: für Speicher/Leistung ist bereits genug im Pack; für einen Quarry-Ersatz müsste der Quest angepasst werden.

## Umgebung (env)

Regel wie vorgegeben: `fabric.mod.json` environment `client` → server unsupported, `server` → client unsupported, sonst beide required; Shaderpacks client required / server unsupported. Kein Eintrag im CF-Manifest ist `required: false`, deshalb ist nichts optional.
- Dreamcraft: 203 beide required, 41 nur Client, 1 nur Server (`ledger`). Shaderpacks: BSL, Complementary Reimagined.
- Challenge Craft: 20 beide required, 10 nur Client (darunter BSL, Complementary Reimagined, Bliss).

Abweichungen zur Seitenangabe auf Modrinth (dort client- bzw. server-only, im Jar aber environment `*`, deshalb hier beide required). Folge: Client- bzw. Serverinstallationen aus dem .mrpack laden diese Mods auch auf der Seite, die sie nicht braucht (bei Fabric-Mods mit `*` normalerweise harmlos):
- Dreamcraft: Athena (Modrinth: nur Client), Death Backup (Modrinth: nur Server), Double Doors (Modrinth: nur Server), Drippy Loading Screen (Modrinth: nur Client), Durability Tooltip (Modrinth: nur Client), Entity Culling (Modrinth: nur Client), Forgiving Void (Modrinth: nur Server), Formations (Structure Library) (Modrinth: nur Server), Fusion (Connected Textures) (Modrinth: nur Client), Healing Campfire (Modrinth: nur Server), Lithostitched (Modrinth: nur Server), MES - Moog's End Structures (Modrinth: nur Server), MMV - Moog's Missing Villages (Modrinth: nur Server), MNS - Moog's Nether Structures (Modrinth: nur Server), Moog's Structure Lib (moogs_structures) (Modrinth: nur Server), MSS - Moog's Soaring Structures (Modrinth: nur Server), MVS - Moog's Voyager Structures (Modrinth: nur Server), Not Enough Animations (Modrinth: nur Client), Repurposed Structures - Fabric (Modrinth: nur Server), RightClickHarvest (Modrinth: nur Server), 3D Skin Layers (Modrinth: nur Client), Structure Layout Optimizer (Modrinth: nur Server), Structure Pool API (Modrinth: nur Server), WITS (What Is This Structure?) (Modrinth: nur Server)
- Challenge Craft: Just Zoom (Modrinth: nur Client), 3D Skin Layers (Modrinth: nur Client), Entity Culling (Modrinth: nur Client), Drippy Loading Screen (Modrinth: nur Client), Not Enough Animations (Modrinth: nur Client)

## Overrides

Übernommen wie im CF-Export (Dreamcraft 65 Dateien, 5,2 MB: Configs, Quests, FancyMenu/Drippy-Menü; Challenge Craft 162 Dateien, 14 MB: Configs, `fancymenu_data/`, `menu_art_source/`).
**Keine .jar/.zip in den Overrides** beider Packs (es lagen auch im CF-Export keine dort).

Was Modrinth beanstanden könnte oder aufgeräumt werden sollte (nichts davon wurde verändert):
1. **BisectHosting-Werbung (beide Packs):** Die Mod BH Menu (`bhmenu`) kommt jetzt regulär von Modrinth (Projekt yWSAtnfH, Hash-Treffer) – das war 2023 das Problem (Jar in den Overrides). Ihre Config `config/bhmenu/bhmenu.properties` schaltet aber Server-Banner und öffentliche Serverliste ein, mit Partner-ID 4395 und dem Text „use code "Kasax007" for 25% off“. In Dreamcraft öffnet zusätzlich der Menü-Knopf `btn_rent` in allen acht `title_screen_dreamcraft_*.txt` den Affiliate-Link `https://bisecthosting.com/kasax007`. Ob Modrinth das bei Modpacks zulässt, habe ich nicht geprüft (unklar).
2. **Challenge Craft `overrides/menu_art_source/`:** Python-Quellen der Menügrafik samt `__pycache__/*.pyc` (kompilierter Python-Code) und `dbg_spider.png`. Für das Spiel nicht nötig; ausführbarer Code in einem Modpack kann bei der Moderation Fragen auslösen. Empfehlung: Ordner weglassen, mindestens `__pycache__`.
3. **Challenge Craft persönliche/Alt-Dateien:** `fancymenu_data/last_world.fmdata` (zeigt auf den Server `grmblka.bh-games.com:25565`), 12 `fancymenu_data/buddy/buddy_*.json` (Spielstände des FancyMenu-Buddys), `config/fancymenu/customization/title_screen_challengecraft_summit.txt.bak`, sowie die nirgends referenzierten Bilder `config/fancymenu/assets/old.png`, `screen.png`, `cc_title_bg.png`. `final.png` (8,5 MB) wird von `title_screen_layout.txt` und `drippy_loading_overlay_layout.txt` benutzt.
4. Die FancyMenu-Layouts von Challenge Craft enthalten Felder `url = https://www.curseforge.com/minecraft` (vermutlich Standardwerte von FancyMenu-Elementen); kein Problem, nur zur Kenntnis.
5. `config/iris.properties` (Challenge Craft) wählt `ComplementaryReimagined_r5.9.3.zip`; der Pfad in files[] heißt genauso (bei Hash-Treffern wird immer der CF-Dateiname als Pfad benutzt).

## Unklar / nicht geprüft
- Quarry Reborn: Lizenz widersprüchlich (Jar CC0-1.0, Modrinth-Seite CC-BY-NC-4.0); Quell-Repo nicht erreichbar.
- More Villagers: `fabric.mod.json` sagt MIT, das LICENSE im GitHub-Repo stellt alle Ressourcen unter All Rights Reserved – deshalb nicht in Overrides.
- Die Someaddons-Mods (Cupboard, Memory Settings, Smooth Chunk Save, Structure Essentials, fix GPU memory leak) habe ich auf Modrinth weder per Slug noch per Suche gefunden; dass es sie dort unter anderem Namen gibt, ist nicht völlig ausgeschlossen.
- Die Packs wurden nicht im Spiel gestartet; ob das Modrinth-Pack ohne die acht Mods fehlerfrei startet, ist nicht getestet (laut `depends` sollte nichts Verbleibendes sie brauchen).
- `summary` in modrinth.index.json ist ein neutraler Platzhalter (wird auf Modrinth nicht angezeigt; die Projektbeschreibung kommt aus dem Projekt).

## Dateien
- `dreamcraft/modrinth.index.json`, `dreamcraft/mapping.json`, `dreamcraft/overrides/`
- `challengecraft/modrinth.index.json`, `challengecraft/mapping.json`, `challengecraft/overrides/`
- `finish.py` (eigene Mods ergänzen, .mrpack schreiben nach `out/`; mit Dummy-own.json getestet, Testausgabe gelöscht)
