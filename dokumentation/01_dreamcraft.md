# 01 – Das Modpack Dreamcraft 26.3

**Dreamcraft [FABRIC]** ist dein Modpack auf CurseForge (Projekt **545167**, Slug `dreamcraft-new`). In diesem Projekt
wurde es von Minecraft 1.20.1 auf **Minecraft 26.3** gebracht, mit eigenem Quest-System, eigenem Ozean-Mod und neuem
Menü. Die Quelle liegt im Repo `Kasax007/Modpack-Development`, Branch **`26.3`** (alles gepusht, letzter Commit
`1a8ad17`).

## 1. Überblick

| Eckdaten | |
| --- | --- |
| Minecraft / Loader / Java | 26.3, Fabric Loader 0.20.1, Java 25 |
| Mods | 250 CurseForge-Mods (inkl. Tamagotchi seit V1.3) plus deine Mods **Quest Icons** und **Beach Craft** |
| Quests | 14 Kapitel, **328 Quests** (V1.3); bis V1.2.1 waren es 13 Kapitel und 164 Quests |
| Endgame | der **Dream Star** (Quest Icons 1.1.0) |
| Menü | FancyMenu mit 8 zufälligen Hintergründen, Drippy-Ladebildschirm mit lila Balken |
| Shader | Iris mit BSL und Complementary Reimagined, standardmäßig **aus** |
| Server | Server-Pack mit Startskripten für Linux, macOS und Windows |
| Aktuell veröffentlicht | **V1.4** (Datei 9475197, Server-Pack 9475219, hochgeladen am 6.11.2026) |
| Davor | V1.2.1 (Datei 9415062, Server-Pack 9415063) |

### Was im Repo liegt
| Pfad | Inhalt |
| --- | --- |
| `modlist-26.3.md` | alle Mods mit CurseForge-Datei und Seite (Client / beide) |
| `pack/mods.json` | Projekt- und Datei-ID jeder Mod (Quelle der `manifest.json`) |
| `pack/overrides/` | alles außer den Mods: Configs, Hauptmenü und Ladebildschirm, das Quest-Buch |
| `pack/removed.md` | Mods aus 1.20.1 V4, die auf 26.3 fehlen, mit Grund |
| `pack/client_only.json` | Mods, die nicht in den Server-Pack kommen (`drippyloadingscreen`) |
| `tools/pack.py`, `selection.py`, `cfscan.py`, `cfslug.py`, `cfname.py` | Mods auswählen, 26.3-Dateien finden und laden, Abhängigkeiten prüfen |
| `tools/mkpack.py` | baut Client-Zip und Server-Pack |
| `tools/dc_quests.py` + `dc_quests_raft.py` + `dc_quests_pets.py`, `qlib.py` | die Quest-Story als Generator |
| `tools/qcheck.py`, `qjars.py` | prüfen jede ID der Quests gegen das laufende Pack |
| `tools/menu_gen.py` | FancyMenu-Layouts (8 Titelbildschirme, Drippy-Overlay) und Menü-Bilder |
| `tools/gen_models.py` | Hilfsskript aus der Beach-Craft-2.0-Arbeit (schreibt Modelle ins Raft-Repo) |
| `tools/srv.sh`, `srv_bisect.py`, `srv_sync.py` | Test-Server, Fehlersuche per Halbierung der Modliste |
| `tools/dctest/` | Client-Test und Film-Harness (Szenen boot, smoke, quests, film) |
| `tools/prodtest/` | Test der echten CurseForge-Installation |
| `docs/curseforge/` | Beschreibung (`description.html`), Changelogs, Bilder (`make_images.py`) |

---

## 2. Der Port von 1.20.1 V4 auf 26.3

**Ausgangslage:** Die neueste Version war **Dreamcraft 1.20.1 V4** (CurseForge-Datei 5042444, 262 Mods). Auftrag vom
2.11.2026: Pack und Server-Pack auf 26.3, ohne Rückfragen (`dreamcraft/PLAN.md` im Archiv).

**Vorgehen:**
1. **Alle 262 Mods geprüft**, ob es eine 26.3-Fabric-Datei gibt (über die cfwidget-API; Werkzeuge `cfscan.py`,
   `cfslug.py`, `cfname.py`).
2. **Ersatz gesucht** für Kategorien, die sonst fehlen würden: Bauen, Abenteuer, Magie, Technik, Lager, Essen.
   Die Auswahl steht als Projekt-ID → Kategorie in `tools/selection.py`.
3. **Laden und Abhängigkeiten prüfen** mit `tools/pack.py fetch|deps`: Es nimmt je Projekt die neueste
   Release-Datei für 26.3 + Fabric, liest `fabric.mod.json` und ergänzt fehlende Abhängigkeiten (in `selection.py`
   als „dependencies found by the resolver“ markiert).
4. **Fehlersuche im Pack:** Mods, die das Spiel oder den Server auf 26.3 kaputt machten, flogen raus (Abschnitt 4).
5. **Drei Lücken mit eigenem Code geschlossen:** FTB Quests gibt es für 26.3 Fabric nicht → Quest-System in
   **Quest Icons** ([02_quest_icons.md](02_quest_icons.md)). Custom Portal API gibt es nicht → eigenes Portal in
   **Beach Craft** ([03_beach_craft.md](03_beach_craft.md)). Das Menü wurde mit FancyMenu neu gebaut.

**Ergebnis (V1):** 250 CurseForge-Mods. Neu gegenüber 1.20.1 kamen laut V1-Changelog u. a. die **RPG Series**
(Wizards, Paladins & Priests, Archers, Rogues & Warriors, Jewelry, Relics, Arsenal, Armory), **Tech Reborn**,
**Quarry Reborn**, **Mutant Monsters**, **Woodwalkers**, **Tectonic**, **Towns and Towers**, **Dungeons and Taverns**,
**ATi Structures**, Moog's Strukturen, **Farmer's Delight** mit Add-ons, **Cooking for Blockheads**, alle **Macaw's**-Mods,
**Rechiseled** und **Dawn of Time** dazu. Wie viele der 262 V4-Mods genau übernommen wurden, ist nirgends als Zahl
festgehalten (unklar).

**Mod-Anzahl je Version** (aus `pack/mods.json` in Git):

| Version | CurseForge-Mods | dazu |
| --- | --- | --- |
| V1, V1.1 | 250 (mit Just Enough Resources) | Quest Icons, Beach Craft |
| V1.2, V1.2.1 | 249 (JER entfernt) | Quest Icons, Beach Craft (Client-Manifest V1.2.1: 251 Dateien) |
| V1.3 | 250 (Tamagotchi neu) | Quest Icons, Beach Craft |

---

## 3. Alle Mods nach Kategorie

Erzeugt mit einem Skript aus `pack/mods.json` (Stand V1.3, 250 Einträge). Die deutschen Kurzbeschreibungen fassen die
CurseForge-Zusammenfassungen zusammen; bei Bibliotheken steht dabei, welche Mods des Packs sie brauchen (aus den
`fabric.mod.json`-Abhängigkeiten). Die Kategorien folgen `tools/selection.py`, für die Lesbarkeit feiner aufgeteilt.
„Seite“: *Client* = nur im Client-Pack, *beide* = auch im Server-Pack, *Server* = nur Server.

**Deine eigenen Mods** (Quest Icons und Beach Craft stehen nicht in `mods.json`, `mkpack.py` fügt sie mit der
angegebenen Datei-ID hinzu):

| Mod | Was sie macht | Stand im Pack |
| --- | --- | --- |
| [Quest Icons](https://www.curseforge.com/minecraft/mc-mods/quest-icons) | Quest-Buch (Taste J), Loot Crates, Icons, Dream Star | V1.2.1: 1.0.2 · V1.3: 1.1.0 |
| [Beach Craft (Raft)](https://www.curseforge.com/minecraft/mc-mods/beach-craft) | Die Raft-Dimension „Endless Sea“: Floß-Überleben, Story, Boss | V1.2.1: 2.0.1 · V1.3: 3.0.0 |
| [Tamagotchi](https://www.curseforge.com/minecraft/mc-mods/tamagotchi) | Zehn seltene Haustiere | ab V1.3: 1.2.0 (Datei 9431312, siehe [04](04_tamagotchi.md)) |

#### Welt, Gelände und Biome (6)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [Accelerated Decay](https://www.curseforge.com/minecraft/mc-mods/accelerated-decay) | Blätter zerfallen schneller, wenn der Baum gefällt ist | beide |
| [BetterEnd](https://www.curseforge.com/minecraft/mc-mods/betterend) | Überarbeitetes End: Biome, Mobs, Blöcke, eigene Metalle und ewige Portale | beide |
| [BetterNether](https://www.curseforge.com/minecraft/mc-mods/betternether) | Überarbeiteter Nether: Pflanzen, Biome, Strukturen wie die Nether-Städte, Mobs wie die Naga | beide |
| [Tectonic](https://www.curseforge.com/minecraft/mc-mods/tectonic) | Neue Geländeformen: höhere Berge, tiefe Täler, Canyons und Klippen | beide |
| [Terralith](https://www.curseforge.com/minecraft/mc-mods/terralith) | Fast 100 neue Biome und Höhlen in der Oberwelt | beide |
| [This Rocks!](https://www.curseforge.com/minecraft/mc-mods/this-rocks) | Kleine Steine, Stöcke, Zapfen, Muscheln und Seesterne liegen natürlich am Boden | beide |

#### Strukturen und Erkundung (20)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [ATi Structures](https://www.curseforge.com/minecraft/mc-mods/ati-structures) | Viele Strukturen in der Oberwelt, z. B. Burgen und Burgruinen | beide |
| [Better Archeology](https://www.curseforge.com/minecraft/mc-mods/better-archeology) | Artefakte und Fossilien in neuen Strukturen ausgraben | beide |
| [Dungeons and Taverns](https://www.curseforge.com/minecraft/mc-mods/dungeon-and-taverns) | Strukturen im Vanilla-Stil, z. B. Tavernen | beide |
| [Explorations](https://www.curseforge.com/minecraft/mc-mods/explorations) | Weitere Strukturen im Vanilla-Stil | beide |
| [Formations (Structure Library)](https://www.curseforge.com/minecraft/mc-mods/formations) | Hilfsfunktionen für Struktur-Datapacks (Strukturbibliothek) | beide |
| [Hang Glider](https://www.curseforge.com/minecraft/mc-mods/hang-glider) | Hängegleiter, um durch die Luft zu segeln | beide |
| [Lootr (Fabric)](https://www.curseforge.com/minecraft/mc-mods/lootr-fabric) | Beute-Truhen gibt es pro Spieler: niemand geht leer aus | beide |
| [Lost Relics](https://www.curseforge.com/minecraft/mc-mods/lost-relics) | Einzigartige, mächtige Artefakte in alten Strukturen | beide |
| [MES - Moog's End Structures](https://www.curseforge.com/minecraft/mc-mods/moogs-end-structures) | Moog's End Structures: Strukturen für das End | beide |
| [MMV - Moog's Missing Villages](https://www.curseforge.com/minecraft/mc-mods/mmv-moogs-missing-villages) | Moog's Missing Villages: die fehlenden Dschungel- und Sumpfdörfer | beide |
| [MNS - Moog's Nether Structures](https://www.curseforge.com/minecraft/mc-mods/mns-moogs-nether-structures) | Moog's Nether Structures: Strukturen mit Beute und Gegnern im Nether | beide |
| [MSS - Moog's Soaring Structures](https://www.curseforge.com/minecraft/mc-mods/mss-moogs-soaring-structures) | Moog's Soaring Structures: schwebende Inseln mit Beute, Mobs und Dungeons (z. B. Himmelsburgen) | beide |
| [MVS - Moog's Voyager Structures](https://www.curseforge.com/minecraft/mc-mods/moogs-voyager-structures) | Moog's Voyager Structures: über 160 Strukturen in der Oberwelt | beide |
| [Repurposed Structures (Fabric)](https://www.curseforge.com/minecraft/mc-mods/repurposed-structures-fabric) | Viele neue Varianten der Vanilla-Strukturen (Pyramiden, Hexenhütten, Minen, Anwesen …) | beide |
| [Structory](https://www.curseforge.com/minecraft/mc-mods/structory) | Atmosphärische Strukturen | beide |
| [Structory: Towers](https://www.curseforge.com/minecraft/mc-mods/structory-towers) | Türme passend zu ihrem Biom | beide |
| [Structure Essentials](https://www.curseforge.com/minecraft/mc-mods/structure-essentials-forge-fabric) | Struktur-Helfer: schnelleres Orten, Abstände, Befehl für nahe Strukturen, keine Überlappung | beide |
| [Structurify - Structure Control](https://www.curseforge.com/minecraft/mc-mods/structurify) | Struktur-Einstellungen ohne Datapack: Abstände, Überlappung, flaches Gelände, Größe, Biome | beide |
| [The Graveyard (Fabric/Neoforge)](https://www.curseforge.com/minecraft/mc-mods/the-graveyard-fabric) | Friedhof-Strukturen, Mobs (z. B. der Lich) und Blöcke | beide |
| [Towns and Towers](https://www.curseforge.com/minecraft/mc-mods/towns-and-towers) | Neue Dörfer, Plünderer-Außenposten und sogar Schiffe | beide |

#### Kreaturen und Bosse (9)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [Ecologics](https://www.curseforge.com/minecraft/mc-mods/ecologics) | Kleine Biom-Updates mit neuen Tieren (z. B. Pinguine) und Blöcken | beide |
| [Friends&Foes (Fabric)](https://www.curseforge.com/minecraft/mc-mods/friends-and-foes) | Mobs aus den Mob-Votes: Copper Golem, Crab, Glare, Moobloom, Iceologer, Rascal, Tuff Golem, Wildfire, Illusioner, Zombiepferd | beide |
| [Lovely Snails](https://www.curseforge.com/minecraft/mc-mods/lovely-snails) | Niedliche Schnecken | beide |
| [More Villagers [Fabric]](https://www.curseforge.com/minecraft/mc-mods/more-villagers-fabric) | Neue Dorfbewohner-Berufe mit eigenen Handelsangeboten und Arbeitsblöcken | beide |
| [Mutant Monsters](https://www.curseforge.com/minecraft/mc-mods/mutant-monsters) | Mutierte Monster als starke Gegner: Mutant Zombie, Creeper, Skeleton, Enderman und mehr | beide |
| [Naturalist](https://www.curseforge.com/minecraft/mc-mods/naturalist) | 47 Tierarten mit eigenem Verhalten und Drops (z. B. Bären, Giraffen, Elefanten, Schmetterlinge) | beide |
| [Respawnable Pets](https://www.curseforge.com/minecraft/mc-mods/respawnable-pets) | Haustiere kehren nach dem Tod zurück, wenn du schläfst (mit dem Etheric Gem) | beide |
| [Variants&Ventures](https://www.curseforge.com/minecraft/mc-mods/variants-and-ventures) | Neue Varianten bekannter Mobs (z. B. der Gelid) | beide |
| [Woodwalkers](https://www.curseforge.com/minecraft/mc-mods/woodwalkers) | Verwandle dich selbst in einen Mob | beide |

#### Ausrüstung und Fortschritt (3)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [Additional Additions for Fabric: Vanilla+ QoL, Sniffers, Music, Food](https://www.curseforge.com/minecraft/mc-mods/additional-additions) | Vanilla+-Ergänzungen: Sniffer, Musik-Discs, Verzaubern, Landwirtschaft, Essen, Redstone und mehr | beide |
| [Advanced Netherite (Fabric)](https://www.curseforge.com/minecraft/mc-mods/advanced-netherite-fabric) | Weitere Netherit-Stufen über normalem Netherit | beide |
| [Mythic Upgrades](https://www.curseforge.com/minecraft/mc-mods/mythic-upgrades) | Kristalle und Edelsteine in neuen Höhlen; wertet Netherit-Ausrüstung auf (Ametrine aus dem End) | beide |

#### Magie, Klassen und Kampf (14)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [Archers (RPG Series)](https://www.curseforge.com/minecraft/mc-mods/archers) | Klasse Bogenschütze: Bögen, Armbrüste und Fähigkeiten | beide |
| [Armory (RPG Series)](https://www.curseforge.com/minecraft/mc-mods/armory-rpg-series) | Epische Rüstungssets mit eigenem Aussehen und Set-Boni | beide |
| [Arsenal (RPG Series)](https://www.curseforge.com/minecraft/mc-mods/arsenal-rpg-series) | Legendäre Waffen, die man erbeutet statt herstellt | beide |
| [Better Combat [Fabric & Forge]](https://www.curseforge.com/minecraft/mc-mods/better-combat-by-daedelus) | Nahkampf wie in Minecraft Dungeons: jede Waffe schwingt anders | beide |
| [Combat Roll [Fabric & Forge]](https://www.curseforge.com/minecraft/mc-mods/combat-roll) | Ausweichrolle im Kampf (Taste R) mit Attributen und Verzauberungen | beide |
| [Easy Magic](https://www.curseforge.com/minecraft/mc-mods/easy-magic) | Verzauberungstisch behält die Items und lässt neu würfeln | beide |
| [Enchanting Infuser](https://www.curseforge.com/minecraft/mc-mods/enchanting-infuser) | Neuer Verzauberungstisch: Verzauberungen gezielt zu fairen Preisen wählen | beide |
| [Grind enchantments](https://www.curseforge.com/minecraft/mc-mods/grind-enchantments) | Mit dem Schleifstein Verzauberungen abnehmen und übertragen | beide |
| [Jewelry (RPG Series)](https://www.curseforge.com/minecraft/mc-mods/jewelry) | Edelsteine tief unten finden und zu starkem Schmuck verarbeiten | beide |
| [Paladins & Priests (RPG Series)](https://www.curseforge.com/minecraft/mc-mods/paladins-and-priests) | Klassen Paladin und Priester: Freunde schützen und heilen (Netherite Holy Staff) | beide |
| [Relics (RPG Series)](https://www.curseforge.com/minecraft/mc-mods/relics-rpg) | Mächtige Relikte (Trinkets) mit besonderen Fähigkeiten | beide |
| [Rogues & Warriors (RPG Series)](https://www.curseforge.com/minecraft/mc-mods/rogues-and-warriors) | Klassen Schurke und Krieger: leise Klingen und wuchtige Schläge | beide |
| [Runes](https://www.curseforge.com/minecraft/mc-mods/rune-crafting) | Runen herstellen – die Munition für Zauber | beide |
| [Wizards (RPG Series)](https://www.curseforge.com/minecraft/mc-mods/wizards) | Klasse Magier: Arkan-, Feuer- und Frostmagie mit Stäben (Netherit-Stab = Dream-Star-Zutat) | beide |

#### Technik, Maschinen und Lager (16)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [Additional Enchanted Miner](https://www.curseforge.com/minecraft/mc-mods/additional-enchanted-miner) | Verzauberbare Abbau-Maschinen, u. a. der Steinbruch „Quarry Plus“ | beide |
| [Chunk Loaders](https://www.curseforge.com/minecraft/mc-mods/chunk-loaders) | Chunk-Lader in mehreren Stufen halten Chunks geladen | beide |
| [Copper Hopper](https://www.curseforge.com/minecraft/mc-mods/copper-hopper) | Kupfer-Trichter als einfacher Item-Filter | beide |
| [Dark Utilities](https://www.curseforge.com/minecraft/mc-mods/dark-utilities) | Vielseitiger Inhalts-Mod mit „ein bisschen von allem“ | beide |
| [Item Collectors](https://www.curseforge.com/minecraft/mc-mods/item-collectors) | Sammler, die Items in einem Umkreis aufsammeln | beide |
| [JustHammers](https://www.curseforge.com/minecraft/mc-mods/justhammers) | Hämmer, die 3×3 bis 5×5×5 Blöcke auf einmal abbauen | beide |
| [Moving Elevators](https://www.curseforge.com/minecraft/mc-mods/moving-elevators) | Echte, fahrende Aufzüge | beide |
| [Quarry Reborn](https://www.curseforge.com/minecraft/mc-mods/quarry-reborn) | Steinbruch (Quarry) als Erweiterung für Tech Reborn | beide |
| [Reborn Core](https://www.curseforge.com/minecraft/mc-mods/reborncore) | Kern-Bibliothek von Tech Reborn | beide |
| [Simple Magnets](https://www.curseforge.com/minecraft/mc-mods/simple-magnets) | Magnete, die Items um den Spieler einsammeln | beide |
| [Storage Drawers](https://www.curseforge.com/minecraft/mc-mods/storage-drawers) | Schubladen-Lager für die Werkstatt | beide |
| [Tech Reborn](https://www.curseforge.com/minecraft/mc-mods/techreborn) | Großer Technik-Mod: Maschinen, Strom, Werkzeuge – bis zum Lapotronic Energy Orb | beide |
| [Tesseract](https://www.curseforge.com/minecraft/mc-mods/tesseract) | Items, Flüssigkeiten und Energie drahtlos übertragen | beide |
| [Tom's Simple Storage Mod (Fabric)](https://www.curseforge.com/minecraft/mc-mods/toms-storage-fabric) | Einfaches Lagersystem im Vanilla-Stil mit Terminal und Crafting-Terminal | beide |
| [Traveler's Backpack [Fabric]](https://www.curseforge.com/minecraft/mc-mods/travelers-backpack-fabric) | Aufrüstbare Rucksäcke mit zwei Tanks und Upgrades (Taste B öffnet) | beide |
| [Wireless Chargers](https://www.curseforge.com/minecraft/mc-mods/wireless-chargers) | Ladegeräte, die Blöcke und Spieler in der Nähe kabellos laden | beide |

#### Essen und Landwirtschaft (8)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [Cooking for Blockheads](https://www.curseforge.com/minecraft/mc-mods/cooking-for-blockheads) | Mehrblock-Küche, die zeigt, was du mit deinen Zutaten kochen kannst | beide |
| [Farmer's Delight Refabricated](https://www.curseforge.com/minecraft/mc-mods/farmers-delight-refabricated) | Kochen und Landwirtschaft: Kochtopf, Schneidebrett, neue Pflanzen und Gerichte | beide |
| [Farming for Blockheads](https://www.curseforge.com/minecraft/mc-mods/farming-for-blockheads) | Markt, Sprinkler und weitere Farm-Helfer | beide |
| [More Delight (Fabric)](https://www.curseforge.com/minecraft/mc-mods/more-delight-fabric) | Add-on für Farmer's Delight: mehr Gerichte, Messer und Zutaten | beide |
| [RightClickHarvest](https://www.curseforge.com/minecraft/mc-mods/rightclickharvest) | Pflanzen per Rechtsklick ernten | beide |
| [Rustic Delight](https://www.curseforge.com/minecraft/mc-mods/rustic-delight) | Add-on für Farmer's Delight: Pfannkuchen, Baumwolle, Kaffee, Paprika, Frittiertes und mehr | beide |
| [Storage Delight (Fabric)](https://www.curseforge.com/minecraft/mc-mods/storage-delight-fabric) | Küchenmöbel für Farmer's Delight im Vanilla-Stil | beide |
| [Ube's Delight](https://www.curseforge.com/minecraft/mc-mods/ubes-delight) | Add-on für Farmer's Delight mit philippinisch inspirierten Pflanzen und Gerichten | beide |

#### Bauen und Dekoration (25)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [Additional Lanterns](https://www.curseforge.com/minecraft/mc-mods/additional-lanterns) | Viele neue Laternen in verschiedenen Farben und Materialien | beide |
| [Armor Statues](https://www.curseforge.com/minecraft/mc-mods/armor-statues) | Rüstungsständer frei einstellen (Posen, Arme und mehr) | beide |
| [Beautify: Refabricated](https://www.curseforge.com/minecraft/mc-mods/beautify-refabricated) | Viele Deko-Möglichkeiten im Vanilla-Stil für schönere Bauten | beide |
| [Chalk (Fabric)](https://www.curseforge.com/minecraft/mc-mods/chalk-fabric) | Kreide-Zeichen auf Blöcken, z. B. als Wegmarkierung in Höhlen | beide |
| [Construction Wand (Fabric)](https://www.curseforge.com/minecraft/mc-mods/construction-wand-fabric) | Bau-Zauberstab, der Blöcke flächig an vorhandene Blöcke anbaut | beide |
| [Dawn Of Time](https://www.curseforge.com/minecraft/mc-mods/dawn-of-time) | Über 350 Bau- und Möbelblöcke japanischer, Maya-, römischer und französischer Kultur | beide |
| [Diagonal Fences](https://www.curseforge.com/minecraft/mc-mods/diagonal-fences) | Zäune verbinden sich auch diagonal | beide |
| [Diagonal Walls](https://www.curseforge.com/minecraft/mc-mods/diagonal-walls) | Mauern verbinden sich auch diagonal | beide |
| [Diagonal Windows](https://www.curseforge.com/minecraft/mc-mods/diagonal-windows) | Fenster (Glasscheiben) verbinden sich auch diagonal | beide |
| [Effortless Building](https://www.curseforge.com/minecraft/mc-mods/effortless-building) | Bauhilfen: Spiegel, Reihen, Baumodi und Block-Zufall, in Survival und Kreativ | beide |
| [Macaw's Bridges](https://www.curseforge.com/minecraft/mc-mods/macaws-bridges) | Viele Brücken | beide |
| [Macaw's Doors](https://www.curseforge.com/minecraft/mc-mods/macaws-doors) | Türen in jeder Holzfarbe plus neue besondere Türen | beide |
| [Macaw's Fences and Walls](https://www.curseforge.com/minecraft/mc-mods/macaws-fences-and-walls) | Neue Zäune, Mauern und Tore im Vanilla-Stil | beide |
| [Macaw's Furniture](https://www.curseforge.com/minecraft/mc-mods/macaws-furniture) | Möbel: Schränke, Kommoden, Stühle, Schreibtische, Tische, Sofas, Waschbecken und mehr | beide |
| [Macaw's Lights and Lamps](https://www.curseforge.com/minecraft/mc-mods/macaws-lights-and-lamps) | Lampen, Fackeln, Straßenlaternen, Papierlampen und mehr | beide |
| [Macaw's Paintings](https://www.curseforge.com/minecraft/mc-mods/macaws-paintings) | Viele neue Gemälde | beide |
| [Macaw's Paths and Pavings](https://www.curseforge.com/minecraft/mc-mods/macaws-paths-and-pavings) | Wege und Pflaster im Vanilla-Stil | beide |
| [Macaw's Roofs](https://www.curseforge.com/minecraft/mc-mods/macaws-roofs) | Echte Dachblöcke statt Treppen | beide |
| [Macaw's Stairs](https://www.curseforge.com/minecraft/mc-mods/macaws-stairs) | Neue Treppen, Treppengeländer und Balkone | beide |
| [Macaw's Trapdoors](https://www.curseforge.com/minecraft/mc-mods/macaws-trapdoors) | Falltüren in jeder Holzart plus neue Falltüren | beide |
| [Macaw's Windows](https://www.curseforge.com/minecraft/mc-mods/macaws-windows) | Fenster, Mosaikglas, Jalousien, Fensterläden, Vorhänge und mehr | beide |
| [Magic Vibe Decorations](https://www.curseforge.com/minecraft/mc-mods/magic-vibe-decorations) | Hexen-Deko und Kristalle; manche Kristalle geben Schutz-Effekte | beide |
| [Rechiseled](https://www.curseforge.com/minecraft/mc-mods/rechiseled) | Meißel: Blöcke in viele Deko-Varianten mit verbundenen Texturen umwandeln | beide |
| [Reconnectible Chains](https://www.curseforge.com/minecraft/mc-mods/reconnectible-chains) | Zäune und Mauern mit Deko-Ketten verbinden | beide |
| [Stoneworks](https://www.curseforge.com/minecraft/mc-mods/stoneworks) | Vanilla-Steinarten in vielen zusätzlichen Varianten | beide |

#### Karten, Navigation und Teleport (7)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [Explorer's Compass](https://www.curseforge.com/minecraft/mc-mods/explorers-compass) | Kompass, der Strukturen überall in der Welt findet | beide |
| [Nature's Compass](https://www.curseforge.com/minecraft/mc-mods/natures-compass) | Kompass, der Biome überall in der Welt findet | beide |
| [Ping Wheel](https://www.curseforge.com/minecraft/mc-mods/ping-wheel) | Orte und Mobs für Freunde kurz markieren (Mittelklick) | beide |
| [Waystones](https://www.curseforge.com/minecraft/mc-mods/waystones) | Wegsteine zum Teleportieren und Warp-Schriftrollen | beide |
| [WITS (What Is This Structure?)](https://www.curseforge.com/minecraft/mc-mods/wits) | Befehl /wits zeigt den Namen der Struktur an deiner Stelle | beide |
| [Xaero's Minimap](https://www.curseforge.com/minecraft/mc-mods/xaeros-minimap) | Minikarte mit Wegpunkten (B neuer Wegpunkt, Y Liste) | beide |
| [Xaero's World Map](https://www.curseforge.com/minecraft/mc-mods/xaeros-world-map) | Vollbild-Weltkarte von allem, was du erkundet hast (Taste M) | beide |

#### Komfort, Inventar und Oberfläche (42)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [AppleSkin](https://www.curseforge.com/minecraft/mc-mods/appleskin) | Zeigt Hunger und Sättigung eines Essens direkt in der Hungerleiste | beide |
| [AttributeFix](https://www.curseforge.com/minecraft/mc-mods/attributefix) | Hebt willkürliche Grenzen des Attribut-Systems auf | beide |
| [Better Advancements](https://www.curseforge.com/minecraft/mc-mods/better-advancements) | Größerer, schönerer Fortschritte-Bildschirm | Client |
| [Better Mount HUD](https://www.curseforge.com/minecraft/mc-mods/better-mount-hud) | Besseres HUD beim Reiten | Client |
| [Blur+](https://www.curseforge.com/minecraft/mc-mods/blur-fabric) | Animierte, einstellbare Unschärfe hinter Menüs | Client |
| [Carry On](https://www.curseforge.com/minecraft/mc-mods/carry-on) | Truhen, Öfen samt Inhalt und kleine Tiere hochheben und tragen (schleichen, leere Hände) | beide |
| [Controlling](https://www.curseforge.com/minecraft/mc-mods/controlling) | Suchleiste im Tastenbelegungs-Menü | Client |
| [Crafting Tweaks](https://www.curseforge.com/minecraft/mc-mods/crafting-tweaks) | Werkbank-Raster per Knopf drehen, verteilen oder leeren | beide |
| [Death Backup](https://www.curseforge.com/minecraft/mc-mods/death-backup) | Sichert das Inventar vor dem Tod; per Befehl wiederherstellbar | beide |
| [Double Doors](https://www.curseforge.com/minecraft/mc-mods/double-doors) | Doppeltüren, Falltüren und Tore öffnen sich gemeinsam | beide |
| [Durability Tooltip](https://www.curseforge.com/minecraft/mc-mods/durability-tooltip) | Zeigt die Haltbarkeit eines Items im Tooltip | beide |
| [Easy Anvils](https://www.curseforge.com/minecraft/mc-mods/easy-anvils) | Amboss behält Items, faire Kosten, keine Strafe mehr für wiederholtes Reparieren | beide |
| [Easy Shulker Boxes](https://www.curseforge.com/minecraft/mc-mods/easy-shulker-boxes) | Shulker-Kisten direkt im Inventar durchsuchen, befüllen und leeren | beide |
| [Enchantment Descriptions](https://www.curseforge.com/minecraft/mc-mods/enchantment-descriptions) | Beschreibungen der Verzauberungen im Tooltip | Client |
| [Fabric Capes](https://www.curseforge.com/minecraft/mc-mods/capes) | Zeigt Umhänge (Capes) von OptiFine, LabyMod und anderen Cape-Mods | Client |
| [FallingTree](https://www.curseforge.com/minecraft/mc-mods/falling-tree) | Ganze Bäume mit einem Schlag fällen (schleichen = nur ein Stamm) | beide |
| [Fast Item Frames](https://www.curseforge.com/minecraft/mc-mods/fast-item-frames) | Schnellere Item-Rahmen, färbbar und unsichtbar schaltbar | beide |
| [Forgiving Void](https://www.curseforge.com/minecraft/mc-mods/forgiving-void) | Wer in die Leere fällt, kommt oben wieder heraus | beide |
| [Healing Campfire](https://www.curseforge.com/minecraft/mc-mods/healing-campfire) | Lagerfeuer heilen Spieler und friedliche Tiere in der Nähe | beide |
| [Inventory Profiles Next](https://www.curseforge.com/minecraft/mc-mods/inventory-profiles-next) | Inventar sortieren, Slots sperren, Ausrüstungs-Sets und mehr | Client |
| [Jade 🔍](https://www.curseforge.com/minecraft/mc-mods/jade) | Zeigt oben am Bildschirm, worauf du schaust und welches Werkzeug es braucht | beide |
| [Just Enough Items (JEI)](https://www.curseforge.com/minecraft/mc-mods/jei) | Rezepte und Verwendungen aller Items ansehen (über ein Item: R = Rezept, U = Verwendung) | beide |
| [Just Enough Professions (JEP)](https://www.curseforge.com/minecraft/mc-mods/just-enough-professions-jep) | JEI-Add-on: zeigt die Arbeitsblöcke der Dorfbewohner-Berufe | beide |
| [Magnum Torch](https://www.curseforge.com/minecraft/mc-mods/magnum-torch) | Starke Fackeln, die Mob-Spawns in großem Umkreis verhindern | beide |
| [Mob Lassos](https://www.curseforge.com/minecraft/mc-mods/mob-lassos) | Lassos, um Mobs einzufangen und mitzunehmen | beide |
| [Mod Menu](https://www.curseforge.com/minecraft/mc-mods/modmenu) | Liste aller installierten Mods im Menü | Client |
| [Mouse Tweaks](https://www.curseforge.com/minecraft/mc-mods/mouse-tweaks) | Mehr Funktionen der Maustasten im Inventar | Client |
| [Not Enough Recipe Book [NERB]](https://www.curseforge.com/minecraft/mc-mods/notenoughrecipebook) | Entfernt das Vanilla-Rezeptbuch (spart Spielerdaten); Rezepte zeigt JEI | beide |
| [Overflowing Bars](https://www.curseforge.com/minecraft/mc-mods/overflowing-bars) | Leben-, Rüstungs- und Härteleisten über Vanilla hinaus, kompakt ohne verwirrende Farben | Client |
| [Pick Up Notifier](https://www.curseforge.com/minecraft/mc-mods/pick-up-notifier) | Meldet, was du gerade aufgesammelt hast | Client |
| [Searchables](https://www.curseforge.com/minecraft/mc-mods/searchables) | Such- und Filterhilfen mit Autovervollständigung (Bibliothek) | Client |
| [Shoulder Surfing Reloaded](https://www.curseforge.com/minecraft/mc-mods/shoulder-surfing-reloaded) | Schulterkamera für die dritte Person (F5); Dreamcraft startet seit V1.2 in der Ego-Sicht | Client |
| [Shulker Box Tooltip [Fabric/Forge/NeoForge]](https://www.curseforge.com/minecraft/mc-mods/shulkerboxtooltip) | Zeigt den Inhalt von Shulker-Kisten im Tooltip | beide |
| [Smooth Swapping](https://www.curseforge.com/minecraft/mc-mods/smooth-swapping) | Items gleiten sichtbar durch das Inventar | Client |
| [Starter Kit](https://www.curseforge.com/minecraft/mc-mods/starter-kit) | Startausrüstung für neue Spieler (einstellbar) | beide |
| [Trade Cycling](https://www.curseforge.com/minecraft/mc-mods/trade-cycling) | Handel der Dorfbewohner neu würfeln, ohne den Arbeitsblock abzubauen | beide |
| [Trading Post](https://www.curseforge.com/minecraft/mc-mods/trading-post) | Mit allen Dorfbewohnern in der Nähe auf einmal handeln | beide |
| [Trash Cans](https://www.curseforge.com/minecraft/mc-mods/trash-cans) | Mülleimer für Items, Flüssigkeiten und Energie | beide |
| [Villager In A Bucket](https://www.curseforge.com/minecraft/mc-mods/villager-in-a-bucket) | Dorfbewohner im Eimer mitnehmen | beide |
| [Visual Workbench](https://www.curseforge.com/minecraft/mc-mods/visual-workbench) | Items bleiben auf der Werkbank liegen und sind sichtbar | beide |
| [XP Storage](https://www.curseforge.com/minecraft/mc-mods/xp-storage) | Erfahrung speichern, auf mehrere Arten | beide |
| [Zoomify](https://www.curseforge.com/minecraft/mc-mods/zoomify) | Zoom-Taste, sehr einstellbar | Client |

#### Mehrspieler und Server (8)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [BisectHosting Server Integration Menu [FABRIC]](https://www.curseforge.com/minecraft/mc-mods/bisecthosting-server-integration-menu-fabric) | BisectHosting-Integration im Menü (Knopf „Rent a Server“) | Client |
| [Chat Heads](https://www.curseforge.com/minecraft/mc-mods/chat-heads) | Zeigt den Kopf des Spielers neben seinen Chat-Nachrichten | Client |
| [Chunky (Fabric)](https://www.curseforge.com/minecraft/mc-mods/chunky-pregenerator) | Chunks im Voraus generieren, schnell und sicher | beide |
| [CraftPresence](https://www.curseforge.com/minecraft/mc-mods/craftpresence) | Discord-Status (Rich Presence) frei gestalten | Client |
| [Ledger](https://www.curseforge.com/minecraft/mc-mods/ledger) | Server-Protokoll: wer hat was gemacht (nur Server) | Server |
| [No Chat Reports](https://www.curseforge.com/minecraft/mc-mods/no-chat-reports) | Macht den Chat (wo möglich) nicht meldbar | beide |
| [Simple Voice Chat](https://www.curseforge.com/minecraft/mc-mods/simple-voice-chat) | Sprachchat im Spiel | beide |
| [WorldEdit](https://www.curseforge.com/minecraft/mc-mods/worldedit) | Welt-Editor im Spiel für große Bauvorhaben | beide |

#### Optik und Klang (14)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [[EMF] Entity Model Features [Fabric & Forge]](https://www.curseforge.com/minecraft/mc-mods/entity-model-features) | Eigene Entity-Modelle im OptiFine-Format | Client |
| [[ETF] Entity Texture Features - [Fabric & Forge]](https://www.curseforge.com/minecraft/mc-mods/entity-texture-features-fabric) | Eigene, leuchtende und variierte Mob-Texturen im OptiFine-Format | Client |
| [AmbientSounds 6](https://www.curseforge.com/minecraft/mc-mods/ambientsounds) | Naturgeräusche passend zur Umgebung | Client |
| [Bobby](https://www.curseforge.com/minecraft/mc-mods/bobby) | Größere Sichtweite als der Server erlaubt (Chunk-Cache) | Client |
| [Continuity](https://www.curseforge.com/minecraft/mc-mods/continuity) | Verbundene Texturen, effizient | Client |
| [Falling Leaves (Fabric)](https://www.curseforge.com/minecraft/mc-mods/falling-leaves-fabric) | Blätter fallen als Partikel von den Bäumen | Client |
| [LambDynamicLights](https://www.curseforge.com/minecraft/mc-mods/lambdynamiclights) | Dynamisches Licht, z. B. eine Fackel in der Hand | Client |
| [Not Enough Animations](https://www.curseforge.com/minecraft/mc-mods/not-enough-animations) | Ego-Animationen auch in der dritten Person | beide |
| [Particle Rain](https://www.curseforge.com/minecraft/mc-mods/particle-rain) | Wetter als Partikel-Effekte | Client |
| [Presence Footsteps](https://www.curseforge.com/minecraft/mc-mods/presence-footsteps) | Realistische Schrittgeräusche | Client |
| [Skin Layers 3D](https://www.curseforge.com/minecraft/mc-mods/skin-layers-3d) | Die äußere Skin-Ebene in 3D | beide |
| [Sound Physics Remastered](https://www.curseforge.com/minecraft/mc-mods/sound-physics-remastered) | Realistischer Hall und Dämpfung des Klangs durch Blöcke | beide |
| [Subtle Effects](https://www.curseforge.com/minecraft/mc-mods/subtle-effects) | Viele kleine Partikel- und Klang-Details; am 2. November Partyhüte (Geburtstags-Easter-Egg) | beide |
| [Visuality](https://www.curseforge.com/minecraft/mc-mods/visuality) | Kleine optische Verbesserungen mit neuen Partikeln | Client |

#### Shader (2)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [BSL Shaders](https://www.curseforge.com/minecraft/customization/bsl-shaders) | Shaderpack: hell, farbenfroh, eigenständig (mit Iris, standardmäßig aus) | Shaderpack |
| [Complementary Shaders - Reimagined](https://www.curseforge.com/minecraft/customization/complementary-reimagined) | Shaderpack mit hoher Qualität und Leistung (mit Iris, standardmäßig aus; im TikTok v2 verwendet) | Shaderpack |

#### Hauptmenü und Ladebildschirm (2)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [Drippy Loading Screen](https://www.curseforge.com/minecraft/mc-mods/drippy-loading-screen) | FancyMenu-Add-on für den Ladebildschirm (Dreamcraft-Ladebildschirm mit lila Balken) | beide |
| [FancyMenu](https://www.curseforge.com/minecraft/mc-mods/fancymenu) | Menüs gestalten – das Dreamcraft-Hauptmenü mit acht zufälligen Hintergründen | beide |

#### Leistung und Stabilität (23)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [BadOptimizations](https://www.curseforge.com/minecraft/mc-mods/badoptimizations) | Optimierungen abseits des Renderns | Client |
| [Clumps](https://www.curseforge.com/minecraft/mc-mods/clumps) | Fasst XP-Kugeln zusammen, weniger Lag | beide |
| [Debugify](https://www.curseforge.com/minecraft/mc-mods/debugify) | Behebt bekannte Minecraft-Fehler aus dem Bugtracker | beide |
| [Dynamic FPS](https://www.curseforge.com/minecraft/mc-mods/dynamic-fps) | Spart Leistung, wenn das Spiel im Hintergrund läuft | Client |
| [Entity Culling Fabric/Forge](https://www.curseforge.com/minecraft/mc-mods/entityculling) | Blendet nicht sichtbare Entities und Block-Entities aus | beide |
| [FerriteCore (Fabric)](https://www.curseforge.com/minecraft/mc-mods/ferritecore-fabric) | Weniger Arbeitsspeicher | beide |
| [fix GPU memory leak](https://www.curseforge.com/minecraft/mc-mods/fix-gpu-memory-leak) | Behebt Grafikspeicher-Lecks im Client | beide |
| [ImmediatelyFast](https://www.curseforge.com/minecraft/mc-mods/immediatelyfast) | Beschleunigt das Immediate-Mode-Rendering | Client |
| [Iris Shaders](https://www.curseforge.com/minecraft/mc-mods/irisshaders) | Shader-Mod, kompatibel mit OptiFine-Shadern (Shader sind standardmäßig aus) | Client |
| [Language Reload](https://www.curseforge.com/minecraft/mc-mods/language-reload) | Kürzere Ladezeiten für Sprachen, Ersatz-Sprachen | Client |
| [Lithium (Fabric/NeoForge)](https://www.curseforge.com/minecraft/mc-mods/lithium) | Optimiert die Spiel- und Serverlogik deutlich | beide |
| [Memory Settings](https://www.curseforge.com/minecraft/mc-mods/memory-settings) | Warnt beim Start, wenn zu wenig RAM eingestellt ist | beide |
| [MoreCulling](https://www.curseforge.com/minecraft/mc-mods/moreculling) | Besseres Culling für mehr FPS | Client |
| [Neruina - Ticking Entity Fixer](https://www.curseforge.com/minecraft/mc-mods/neruina) | Verhindert, dass Tick-Abstürze von Entities eine Welt unbrauchbar machen | beide |
| [Not Enough Crashes (Fabric)](https://www.curseforge.com/minecraft/mc-mods/not-enough-crashes) | Nach einem Absturz zurück ins Hauptmenü statt Neustart | beide |
| [Packet Fixer](https://www.curseforge.com/minecraft/mc-mods/packet-fixer) | Behebt Probleme mit Paketen, NBT und Timeouts | beide |
| [Reese's Sodium Options](https://www.curseforge.com/minecraft/mc-mods/reeses-sodium-options) | Übersichtlicheres Optionsmenü für Sodium | Client |
| [ScalableLux](https://www.curseforge.com/minecraft/mc-mods/scalablelux) | Schnellere Lichtberechnung (auf Starlight-Basis) | beide |
| [Server Performance - Smooth Chunk Save](https://www.curseforge.com/minecraft/mc-mods/smooth-chunk-save) | Speichert Chunks laufend ohne Lag-Spitzen, mehr Server-TPS | beide |
| [Sodium](https://www.curseforge.com/minecraft/mc-mods/sodium) | Schnelles Rendering, deutlich mehr FPS | Client |
| [Sodium Extra](https://www.curseforge.com/minecraft/mc-mods/sodium-extra) | Zusätzliche Grafikoptionen für Sodium | Client |
| [spark](https://www.curseforge.com/minecraft/mc-mods/spark) | Leistungs-Profiler für Client und Server | beide |
| [Structure Layout Optimizer](https://www.curseforge.com/minecraft/mc-mods/structure-layout-optimizer) | Schnellere Generierung von Jigsaw-Strukturen | beide |

#### Bibliotheken (Abhängigkeiten anderer Mods) (50)

| Mod | Was sie macht | Seite |
| --- | --- | --- |
| [Architectury API](https://www.curseforge.com/minecraft/mc-mods/architectury-api) | Bibliothek für Mods auf mehreren Loadern (u. a. für Better Archeology) | beide |
| [Armor Model API](https://www.curseforge.com/minecraft/mc-mods/armor-model-api) | Bedrock-/GeckoLib-Rüstungsmodelle (für die RPG Series) | beide |
| [Athena](https://www.curseforge.com/minecraft/mc-mods/athena) | Bibliothek für verbundene Block-Texturen | beide |
| [Balm](https://www.curseforge.com/minecraft/mc-mods/balm) | Bibliothek für Waystones, Cooking/Farming for Blockheads, Crafting Tweaks, Forgiving Void | beide |
| [BCLib](https://www.curseforge.com/minecraft/mc-mods/bclib) | Bibliothek der BetterX-Mods (BetterNether, BetterEnd) | beide |
| [Bookshelf](https://www.curseforge.com/minecraft/mc-mods/bookshelf) | Bibliothek (u. a. für Dark Utilities) | beide |
| [Cloth Config API (Fabric/Forge/NeoForge)](https://www.curseforge.com/minecraft/mc-mods/cloth-config) | Einstellungs-Menüs für viele Mods | beide |
| [Collective](https://www.curseforge.com/minecraft/mc-mods/collective) | Gemeinsamer Code der Serilum-Mods (Death Backup, Double Doors, Healing Campfire, Starter Kit) | beide |
| [Configurable](https://www.curseforge.com/minecraft/mc-mods/configurable) | Einstellungs-Bibliothek (für Neruina) | beide |
| [CraftedCore](https://www.curseforge.com/minecraft/mc-mods/crafted-core) | Bibliothek (u. a. für Woodwalkers) | beide |
| [CreativeCore](https://www.curseforge.com/minecraft/mc-mods/creativecore) | Bibliothek (für AmbientSounds) | beide |
| [Cristel Lib](https://www.curseforge.com/minecraft/mc-mods/cristel-lib) | Struktur-Einstellungen und Laufzeit-Datapacks (für Towns and Towers) | beide |
| [Cupboard](https://www.curseforge.com/minecraft/mc-mods/cupboard) | Bibliothek (für Memory Settings, Smooth Chunk Save, Structure Essentials) | beide |
| [Delight Lib](https://www.curseforge.com/minecraft/mc-mods/delight-lib) | Bibliothek für Farmer's-Delight-Add-ons (für More Delight) | beide |
| [EpheroLib](https://www.curseforge.com/minecraft/mc-mods/epherolib) | Bibliothek für Mods auf Fabric und Forge | beide |
| [Fabric API](https://www.curseforge.com/minecraft/mc-mods/fabric-api) | Die Grund-API aller Fabric-Mods | beide |
| [Fabric Language Kotlin](https://www.curseforge.com/minecraft/mc-mods/fabric-language-kotlin) | Kotlin-Unterstützung (u. a. für Inventory Profiles Next, Zoomify, Ledger, Fzzy Config) | beide |
| [Forge Config API Port](https://www.curseforge.com/minecraft/mc-mods/forge-config-api-port) | Forge-Konfigurationssystem für Fabric (für die Fuzs-Mods wie Easy Anvils oder die Diagonal-Mods) | beide |
| [Fusion (Connected Textures)](https://www.curseforge.com/minecraft/mc-mods/fusion-connected-textures) | Verbundene Texturen und Modelle für Ressourcenpakete (für Rechiseled) | beide |
| [Fzzy Config](https://www.curseforge.com/minecraft/mc-mods/fzzy-config) | Einstellungs-Bibliothek mit automatischen Menüs (für Subtle Effects) | beide |
| [GeckoLib](https://www.curseforge.com/minecraft/mc-mods/geckolib) | 3D-Animationen für Mobs, Blöcke und Items (für The Graveyard) | beide |
| [JamLib](https://www.curseforge.com/minecraft/mc-mods/jamlib) | Bibliothek (für RightClickHarvest) | beide |
| [Konkrete](https://www.curseforge.com/minecraft/mc-mods/konkrete) | Bibliothek für FancyMenu und Drippy Loading Screen | beide |
| [libIPN](https://www.curseforge.com/minecraft/mc-mods/libipn) | Oberflächen-Bibliothek für Inventory Profiles Next | Client |
| [Lithostitched](https://www.curseforge.com/minecraft/mc-mods/lithostitched) | Weltgen-Bibliothek (für Tectonic und Terralith) | beide |
| [Melody](https://www.curseforge.com/minecraft/mc-mods/melody) | Hintergrundmusik-Bibliothek (für FancyMenu) | beide |
| [MidnightLib](https://www.curseforge.com/minecraft/mc-mods/midnightlib) | Bibliothek mit eingebautem Einstellungssystem | beide |
| [Moog's Structure Lib (moogs_structures)](https://www.curseforge.com/minecraft/mc-mods/moogs-structure-lib) | Bibliothek der Moog's-Strukturmods | beide |
| [Nanite Library](https://www.curseforge.com/minecraft/mc-mods/nanite-library) | Bibliothek (für JustHammers) | beide |
| [Player Animation Library](https://www.curseforge.com/minecraft/mc-mods/player-animation-library) | Spieler-Animationen (für Better Combat, Combat Roll, Spell Engine) | beide |
| [Prickle](https://www.curseforge.com/minecraft/mc-mods/prickle) | JSON-Einstellungsformat (für AttributeFix, Enchantment Descriptions) | beide |
| [Puzzles Lib](https://www.curseforge.com/minecraft/mc-mods/puzzles-lib) | Bibliothek der Fuzs-Mods (Easy Anvils, Easy Magic, Easy Shulker Boxes, Diagonal-Mods, Armor Statues …) | beide |
| [Ranged Weapon API](https://www.curseforge.com/minecraft/mc-mods/ranged-weapon-api) | Bögen und Armbrüste als API (für die RPG Series) | beide |
| [Resourceful Config](https://www.curseforge.com/minecraft/mc-mods/resourceful-config) | Einstellungs-Bibliothek von Team Resourceful | beide |
| [Resourceful Lib](https://www.curseforge.com/minecraft/mc-mods/resourceful-lib) | Bibliothek (für Friends&Foes, Variants&Ventures) | beide |
| [Scalable Cat's Force](https://www.curseforge.com/minecraft/mc-mods/scalable-cats-force) | Scala-Unterstützung (für Additional Enchanted Miner) | beide |
| [ShatterLib \| OctoLib](https://www.curseforge.com/minecraft/mc-mods/shatterbyte-lib) | Bibliothek (für Not Enough Recipe Book) | beide |
| [Shogi](https://www.curseforge.com/minecraft/mc-mods/shogi) | Regelbasierte Einstellungen (für Waystones) | beide |
| [Spell Engine](https://www.curseforge.com/minecraft/mc-mods/spell-engine) | Datengetriebene Magie-Engine der RPG Series (Zauber, Zauberbücher) | beide |
| [Spell Power Attributes](https://www.curseforge.com/minecraft/mc-mods/spell-power) | Zauberkraft-Attribute mit Effekten und Verzauberungen | beide |
| [StrawberryLib](https://www.curseforge.com/minecraft/mc-mods/strawberrylib) | Bibliothek (für Lost Relics, Respawnable Pets) | beide |
| [Structure Pool API](https://www.curseforge.com/minecraft/mc-mods/structure-pool-api) | Fügt Strukturen in Struktur-Pools ein (für die RPG Series) | beide |
| [SuperMartijn642's Config Lib](https://www.curseforge.com/minecraft/mc-mods/supermartijn642s-config-lib) | Einstellungs-Bibliothek der SuperMartijn642-Mods | beide |
| [SuperMartijn642's Core Lib](https://www.curseforge.com/minecraft/mc-mods/supermartijn642s-core-lib) | Kern-Bibliothek der SuperMartijn642-Mods (Chunk Loaders, Item Collectors, Moving Elevators, Simple Magnets, Tesseract, Trash Cans, Rechiseled) | beide |
| [TerraBlender (Fabric)](https://www.curseforge.com/minecraft/mc-mods/terrablender-fabric) | Bibliothek zum Hinzufügen von Biomen | beide |
| [Trinkets Updated](https://www.curseforge.com/minecraft/mc-mods/trinkets-updated) | Zubehör-Slots (Trinkets), z. B. für Lost Relics | beide |
| [UniLib](https://www.curseforge.com/minecraft/mc-mods/unilib) | Hilfsbibliothek (u. a. für CraftPresence) | Client |
| [VillagersTradingPlus](https://www.curseforge.com/minecraft/mc-mods/villagerstradingplus) | Dorfbewohner-Handel per Datapack (für The Graveyard) | beide |
| [WorldWeaver](https://www.curseforge.com/minecraft/mc-mods/worldweaver) | Weltgen-Bibliothek der BetterX-Mods | beide |
| [YetAnotherConfigLib](https://www.curseforge.com/minecraft/mc-mods/yacl) | Einstellungs-Bibliothek (für Zoomify, Structurify, Reconnectible Chains) | beide |

---

## 4. Entfernte und fehlende Mods

### Entfernt, weil sie auf 26.3 im Pack nicht liefen (`pack/removed.md`)
| Mod (Projekt) | Grund |
| --- | --- |
| Enhanced Quarries (528338) | schreibt Rezept-JSON um (`item`→`id`) und zerstört BetterEnd/BCLib-Rezepte → der Server startet nicht |
| MCPitanLib (682213) | wandelt Rezept-JSON global um; zerstört BetterEnd- und Farming-for-Blockheads-Daten (keine Mod braucht sie mehr) |
| Display Case (517791) | seine 26.3-Advancements nutzen noch das 1.20-NBT-Format → Registry-Ladefehler |
| Kaleidoscope Cookery Refabricated (1394201) | REI konnte seine Topf-/Teekannen-Rezepte nicht anzeigen (Hunderte Fehler); Farmer's Delight und Add-ons decken das Kochen ab |
| Wakes (884267) | FancyMenu 3.9.14 erklärt sich als inkompatibel |
| Cherished Worlds (308240) | die mitgelieferte SpectreLib lädt `ComponentSerialization` zu früh → CreativeCore-Mixin schlägt fehl, Client startet nicht |
| ModernFix-mVUS (1367508) | lädt Chat-Klassen zu früh → Mixins von Language Reload/CreativeCore schlagen fehl |
| FrozenLib (709773) + Wilder Wild (648511) + Simple Copper Pipes (571336) | FrozenLibs Early-Entrypoint lädt Chat-Klassen zu früh → Client startet nicht |
| Item Highlighter (541578) + Iceberg (539382) | Iceberg bringt eine alte NightConfig mit → jede Fuzs-Mod-Config stürzt ab |
| Roughly Enough Items (310111) + REP (597988) | REI 26.3 kann die datengetriebenen Brau-Rezepte (557) und den Kochtopf (27) nicht anzeigen → **ersetzt durch JEI + Just Enough Professions** |
| Just Enough Resources (240630), **entfernt in V1.2** | sein JEI-Plugin baut eine eigene Weltgen-Registry und scheitert an BetterNethers Biomen („No value registered for key betternether:flooded_deltas“) – es zeigte gar keine Seite |

### Noch nicht für Fabric 26.3 verfügbar (aus der CurseForge-Beschreibung)
Create, Botania, Applied Energistics 2, Spectrum, Ad Astra, Modern Industrialization und The Bumblezone. Sie sollen
zurückkommen, sobald es sie für Fabric 26.3 gibt. Die Beschreibung listet außerdem die getesteten, aber (noch) nicht
lauffähigen Mods: Enhanced Quarries, Display Case, Wakes, Cherished Worlds, ModernFix-mVUS, Wilder Wild, Simple Copper
Pipes, Item Highlighter und Just Enough Resources.

### Bekannte harmlose Log-Meldungen
In Dungeons and Taverns lassen sich zwei Vorlagen nicht laden (Tippfehler in der Mod: `axys`,
`chisled_polished_blackstone`). Die Teile fehlen dann einfach, das Spiel stürzt nicht ab.

---

## 5. Hauptmenü und Ladebildschirm

- **FancyMenu-v3-Layouts** `config/fancymenu/customization/title_screen_dreamcraft_1.txt` … `_8.txt`: acht Layouts,
  eines pro Hintergrund (`assets/dreamcraft/bg1.jpg` … `bg8.jpg`). Zufallsmodus mit `randomonlyfirsttime = true`:
  beim ersten Öffnen des Menüs wird eines der acht gewählt.
- **Knöpfe als Schriftzug-Bilder** (`btn_single`, `btn_multi`, `btn_options`, `btn_mods`, `btn_rent`, `btn_quit`, jeweils
  mit `_hover`), dazu eine **Seitenleiste mit Logo** (`sidebar.png`) und ein Versions-Schild (`version_tag.png`).
  „Mods“ öffnet die Mod-Liste (Mod Menu), „Rent a Server“ öffnet `https://bisecthosting.com/kasax007`.
- **Skalierung (seit V1.2):** `setscale 2` plus `autoscale` mit Basis 1920×1080, damit das Menü in jedes Fenster passt.
- **Drippy Loading Screen:** Hintergrund `loading_bg.jpg`, Logo `loading_logo.png`, **lila Ladebalken #7e0cc9**. Seit
  V1.2 zeichnet ihn Drippys eigenes Balken-Element (`drippy_vanilla_bar` mit Farbe), weil der Vanilla-Balken Farben
  ignoriert und weiß blieb.
- **Ausgeschaltete Willkommens-Fenster:** BetterX (`config/wover/client.json`: `did_present_welcome_screen`,
  `check_for_new_versions: false`) und Terralith (`config/terralith.json`: `intro_message: false`).
- Bilder und Layouts erzeugt `tools/menu_gen.py`. In V1.2 wurde dort `fresh_ids()` repariert: es vergab für dieselbe
  UUID verschiedene neue IDs, dadurch hatten „Mods“ und „Rent a Server“ keine Aktion mehr.

## 6. Configs im Pack (`pack/overrides/config`)

| Datei | Zweck |
| --- | --- |
| `questsicons/quests/**` | das Quest-Buch (vom Generator geschrieben, siehe Abschnitt 9) |
| `fancymenu/**`, `drippyloadingscreen/options.txt` | Hauptmenü und Ladebildschirm |
| `shouldersurfing-client.toml` | `default_perspective = "FIRST_PERSON"`: Start in der Ego-Sicht (seit V1.2; vorher startete man in der Schulterkamera) |
| `terralith.json` | Terralith-Module, Intro-Nachricht aus |
| `wover/client.json` | BetterX: kein Willkommens-Fenster, keine Update-Prüfung, BetterX-Welttyp erzwungen |

Hinweise aus dem Projektgedächtnis: **Subtle Effects** zeigt am 2. November (Geburtstag der Mod) Partyhüte und
kreisende Köpfe – für Aufnahmen `enableEasterEggs = false` setzen. Für Aufnahmen mit HUD wurde die Minikarte im
Testclient abgeschaltet (`display_minimap = false`); im Pack selbst ist sie an.

## 7. Der Server-Pack

`tools/mkpack.py` baut neben dem Client-Zip einen fertigen Server-Ordner:
- alle server-fähigen Mods (ohne reine Client-Mods und ohne `drippyloadingscreen`), dazu Quest Icons, Beach Craft und
  Tamagotchi – in V1.2.1 waren das **209 Mods**;
- `config/` ohne FancyMenu/Drippy, also mit den Quest-Dateien;
- `fabric-server-launch.jar` (lädt beim ersten Start Minecraft 26.3 selbst herunter);
- `start.sh` (Linux/macOS) und `start.bat` (Windows) mit **EULA-Prüfung**: Beim ersten Start entsteht
  `eula.txt` mit `eula=false`; nach dem Lesen auf `true` setzen und neu starten. RAM: `-Xms4G`, `-Xmx` 8 GB
  (bei `start.sh` per `DREAMCRAFT_RAM=10G` änderbar);
- `server.properties`: MOTD „Dreamcraft 26.3 – a dream of a modpack“, normal, Sichtweite 10, Simulationsweite 8,
  kein Spawn-Schutz, Fliegen erlaubt, `max-tick-time=120000`, `sync-chunk-writes=false`;
- `README.txt` (Anleitung, BisectHosting-Code KASAX007) und `server-icon.png`.

**Getestet:** Server-Pack aus dem Zip gestartet (Start in 32 s, Quest-Buch geladen); Chunky in allen Dimensionen ohne
Fehler (Oberwelt 1521 Chunks in 1:43, Raft-Dimension 729 Chunks, früher auch Nether und End).

**Von Hand nötig:** Auf CurseForge muss die Zusatzdatei als **Server Pack markiert** werden – das geht nicht per API.

---

## 8. Versionen und der Produktiv-Installationstest

### Alle Versionen
| Version | Client-Datei | Server-Pack | Inhalt (Changelog `docs/curseforge/changelog-26.3-*.md`) |
| --- | --- | --- | --- |
| **V1** | 9403038 | 9403042 | Dreamcraft auf 26.3: neue Quest-Story (13 Kapitel, über 160 Quests), Quest Icons 1.0, Beach Craft 2.0, neue Mods, neues Menü, JEI mit JEP und JER, Server-Pack |
| **V1.1** | 9408516 | 9408519 | Beach Craft 2.0.1 (über 20 Fehler behoben); Raft-Quests korrigiert: Treibholz-Stümpfe an Stränden, „Land Ho!“ wurde **„Driftwood Ahoy!“** (16 Treibholz-Stämme), Titan-Quest nennt Diamantspitzhacke und Metalldetektor, echter Set-Bonus der Titan-Rüstung |
| **V1.2** | 9409459 | 9409463 | nach dem Test der echten Installation: Menü passt in jedes Fenster, Mods- und Rent-a-Server-Knopf gehen, lila Ladebalken, Start in der Ego-Sicht, Quest Icons 1.0.1 (kein zweites Quest-Buch), Quests nennen JEI statt REI; **Just Enough Resources entfernt** |
| **V1.2.1** | 9415062 | 9415063 | Hotfix: Quest Icons 1.0.2 – das Quest-Buch reagiert wieder auf Klicks (26.3-Maustasten) |
| **V1.3** | 9431378 | 9431379 | Beach Craft 3.0.0 (9431301), Tamagotchi 1.2.0 (9431312), Quest Icons 1.1.0 (9429010) mit Dream Star, Quests 164 → 328 (hochgeladen am 4.11.2026) |
| **V1.4** | 9475197 | 9475219 | Beach Craft 3.1.0 (9474711: eigenes Floß, Menschen der See, Sounds und Musik, Kai in allen Lagern), Upgraded Iron Chests 1.5.1 neu, Kapitel „Quality of Life“, Quests 328 → 348 in 15 Kapiteln (hochgeladen am 6.11.2026) |
| **V1.4.1** | 9487507 | 9487509 | Menü-Fix: Singleplayer, Multiplayer, Options und Quit Game lagen hinter dem lila Seitenbalken (gemeldet vom Nutzer am 6.11. anhand des Trailers); sonst identisch mit V1.4 |

### Was V1.3 bringt (Changelog `changelog-26.3-V1.3.md`)
- **Beach Craft 3.0 „Tides of the Deep“** – Inselwelt, Story, Boss, Expedition Raft, Tauchen ([03](03_beach_craft.md)).
- **Tamagotchi** als neue Mod ([04](04_tamagotchi.md)).
- **Quest Icons 1.1.0 und der Dream Star** ([02](02_quest_icons.md)).
- **Quests 164 → 328:** Kapitel 6 neu (81 Quests), neuer Seitenpfad Tamagotchi (27), Dream-Star-Kette im Epilog,
  mehr vom Pack in jedem Kapitel (Tech-Reborn-Weg zum Lapotronic Energy Orb, Quarry Reborn, Tesseract, Dark Utilities,
  Netherit-Stäbe, Relics, Armory, BetterNether, BetterEnd-Metalle und Portale, Drachenei und -kopf, Küche, Bauen,
  Erkunden, mehr Kreaturen und Bosse). **Master of Dreams** gibt jetzt zwei Quest Crowns; wer die Quest schon hatte,
  kann die zweite Krone abholen. Alle alten Quest-IDs bleiben, Fortschritt bleibt erhalten.
- Loot-Kisten enthalten auch Pet Kibble, Seil, Titan, Tamagotchi Hearts, Ancient Crystals und Netherit-Vorlagen.
- **Korrekturen:** „Let the Machines Dig“ nannte die falsche Mod (es ist Quarry Plus aus Additional Enchanted Miner;
  Quarry Reborn hat eine eigene Quest); Mythic Upgrades nannte falsche Fundorte (Ametrine kommt aus dem End); die
  Tech-Reborn-Batterie heißt Battery Box; der Explorer's Atlas nannte Wilder Wild (nicht im Pack); zwei Belohnungen
  nannten Items, die es in 26.3 nicht gibt („Path of the Wizard“ gibt jetzt einen Arcane Wand, „Chalk Marks“ eine
  Glowing Chalk); „Friendsoes“ statt Friends&Foes (das „&F“ wurde als Farbcode gelesen); Karten aufgeräumt.
- **Bestehende Welten:** Schon erkundete Teile der Endless Sea behalten ihre alte Form – weiter hinausfahren. Alte
  Ankunftsplattformen haben keine Castaway-Truhe: Expedition Journal herstellen (Buch, Kompass, Papier) und auf See
  schleichend benutzen.

### V1.4.1: der Menü-Fix (6.11.2026 abends)
- **Ursache:** Der lila Seitenbalken ist ein eigenes Bild-Element (`sidebar.png`). FancyMenu zeichnet eigene Elemente
  über den Vanilla-Widgets, solange `render_custom_elements_behind_vanilla = false` ist. Singleplayer, Multiplayer,
  Options und Quit Game sind restylte Vanilla-Knöpfe und lagen deshalb unter dem halbdurchsichtigen Balken (lila
  getönt). Mods und Rent a Server sind eigene Knöpfe nach dem Balken und lagen davor.
- **Fix:** `render_custom_elements_behind_vanilla = true` in allen acht `title_screen_dreamcraft_*.txt` (und in
  `tools/menu_gen.py`). Geprüft im echten Client (Produktiv-Test): bei 854×480, 1366×768 und 1920×1080 haben alle
  sechs Knöpfe die Textfarbe der Grafik (255, 251, 206), Hover geht, Quit Game beendet das Spiel. Server-Pack: 364 Mods,
  „Done“ nach 10 s, 15 Kapitel, 348 Quests.
- **Achtung beim Bauen:** `tools/mkpack.py` nimmt die Overrides aus `$SP/pack/overrides`, nicht aus dem Repo. Eine
  Änderung im Repo zuerst dorthin kopieren (der erste V1.4.1-Build enthielt den Fix deshalb nicht; geprüft durch
  Vergleich der Zips mit V1.4: anders sind nur `manifest.json` und die acht Layouts).
- Dazu neu: das Menübild der CurseForge-Seite (`menu_v14.jpg`) und der Menü-Shot des Trailers (`footage/dc/menu_land.mp4`,
  aus dem neuen Screenshot mit derselben langsamen Zoomfahrt).
- Upload am 7.11. um 7:31 Uhr deutscher Zeit (Wunsch des Nutzers: 7:30) per `$SP/upload141.sh`: Client 9487507,
  Server-Pack 9487509 (`parentFileID` 9487507). Den Server-Pack auf CurseForge von Hand als Server Pack markieren.

### So wurde V1.4 gebaut (6.11.2026)
1. Beach Craft 3.1.0 hochgeladen (Datei 9474711), nach rund 15 Minuten freigegeben (Download-Link 307).
2. `python3 tools/mkpack.py V1.4 9429010 9474711` → Client-Pack (253 CurseForge-Mods), Server-Pack (211 Mods, 426 MB).
3. Wie ein Launcher installiert (alle 253 Mods von CurseForge, 0 Fehler), Client bis in eine neue Welt, Quest-Buch
   („0/217“ Pflicht-Quests), Mods geladen: raft 3.1.0+26.3, questsicons 1.1.0, tamagotchi 1.2.0, upgraded-iron-chests
   1.5.1. Server-Pack aus der Zip: 364 Mods, „Done“ nach 12 s, „15 chapters, 348 quests“, Floß-Strukturen per
   `/locate` gefunden. Im Log nur Umgebungs- und Erststart-Meldungen.
4. Client (9475197) und Server-Pack (9475219, `parentFileID`) hochgeladen.

### So wurde V1.3 gebaut (4.11.2026, Reihenfolge ist wichtig)
1. Beach Craft 3.0.0 hochgeladen (Datei 9431301) und die CurseForge-Prüfung abgewartet: Eine neue Datei ist erst nach
   rund 10 Minuten herunterladbar (der öffentliche Download-Link antwortet dann mit 307); erst dann darf ein Pack sie
   referenzieren.
2. Tamagotchi 1.2.0 direkt auf CurseForge hochgeladen (Datei 9431312). Der Weg über den Release-Workflow ging aus der
   Sitzung nicht (Tag-Push bricht ab, `workflow_dispatch` braucht den Workflow auf dem Default-Branch `main`).
   `pack/mods.json` zeigt jetzt auf 9431312.
3. `python3 tools/mkpack.py V1.3 9429010 9431301` – Quest Icons 1.1.0 ist 9429010; Tamagotchi kommt aus
   `pack/mods.json` (ein viertes Argument würde es überschreiben).
4. Wie ein Launcher installiert und getestet (unten), dann Client (9431378) und Server-Pack (9431379, mit
   `parentFileID`) hochgeladen. Ob das Server-Pack als Server Pack markiert ist, muss man auf CurseForge von Hand prüfen.

### Der Produktiv-Installationstest (`tools/prodtest`)
**Warum:** Der Client-Test in `tools/dctest` läuft in Loom, einer Entwicklungsumgebung. Er lässt z. B. Neruina weg
(dessen Test-Mixins in einer Dev-Umgebung werfen) und die reinen Server-Mods. Nur ein echter Launcher-Start zeigt, was
Spieler sehen.

1. **Installieren wie ein Launcher:** `python3 -I cf_install.py <Client-Datei> <Server-Datei>` lädt das Modpack-Zip
   von CurseForge, holt jede Manifest-Datei über Projekt- und Datei-ID, entpackt die Overrides nach `instance/` und
   schreibt `report.json` mit der sha1 jedes Jars. Die zwei Shaderpack-Zips gehören (wie bei der CurseForge-App) von
   `mods/` nach `shaderpacks/`.
2. **Client starten:** `launch.py` startet Minecraft 26.3 + Fabric Loader 0.20.1 produktiv (Classpath aus dem
   Fabric-Profil, Version-JSON und Assets aus dem Loom-Cache), unter Xvfb.
3. **Ansehen und klicken:** `shot.sh` macht Screenshots, `xin.py` sendet Mausbewegungen, Klicks und Tasten (XTEST),
   `xwin.py` ändert die Fenstergröße.
4. **Server-Pack** entpacken, `start.sh` einmal starten (EULA), `eula=true` setzen, neu starten.

**Checkliste vor jedem Pack-Upload** (Projektgedächtnis): installieren wie ein Launcher; Hauptmenü bei 854×480,
1366×768 und 1920×1080 ansehen und jeden Knopf klicken; Welt laden, Quest-Buch (J) öffnen; Server-Pack aus der Zip
starten.

**Was der Test in V1.1 fand (behoben in V1.2):** Menü zu groß für kleine Fenster (bei 854×480 war kein Knopf
klickbar, bei 1366×768 fehlte „Quit Game“); Mods- und Rent-a-Server-Knopf ohne Aktion; Ladebalken weiß; Start in der
Schulterkamera; JER scheitert an BetterNether-Biomen; Quests nannten REI. **Was er nicht fand:** den Klick-Fehler im
Quest-Buch (der Test öffnete das Buch, klickte aber keine Quest an) – den meldeten Spieler im Discord, siehe
[02](02_quest_icons.md#wie-es-zum-hotfix-102-kam).

---

## 9. Die Quests

### Wie die Quests entstehen
- Die Quests werden nicht von Hand geschrieben, sondern **erzeugt**: `python3 tools/dc_quests.py OUT_DIR` schreibt
  `data.snbt`, `chapter_groups.snbt`, `chapters/*.snbt` und `reward_tables/*.snbt`. Kapitel 6 kommt aus
  `dc_quests_raft.py`, der Tamagotchi-Pfad aus `dc_quests_pets.py`; `qlib.py` ist die kleine Bibliothek dazu.
- Ziel im Pack: `pack/overrides/config/questsicons/quests`. Für diese Doku wurde der Generator erneut in einen
  Testordner laufen gelassen – das Ergebnis ist **identisch** mit den Dateien im Repo.
- **Stabile IDs:** Jede Quest-ID ist ein FNV-1a-Hash von „Kapitel:Quest-Schlüssel“. Solange ein Schlüssel bleibt,
  bleibt der Fortschritt der Spieler. Belohnungen sind durchnummeriert; neue Belohnungen kommen ans Ende einer Liste
  (so konnte „Master of Dreams“ eine zweite Krone bekommen, die auch alte Spieler abholen können).
- **Prüfung:** `tools/qcheck.py` prüft jede Item-, Mob-, Advancement-, Struktur-, Biom- und Dimensions-ID gegen einen
  Registry-Dump des laufenden Packs, dazu Abhängigkeiten (keine Zyklen), doppelte IDs, übereinanderliegende Quests,
  Kisten-Tabellen und `&`-Zeichen, die Buchstaben fressen. Lauf für diese Doku gegen den V1.3-Dump
  (`$SP/v13/regdump3.json`): **„checked 328 quests in 14 chapters … 0 problems“**.
- **Erzählstimme:** Der **Dreamkeeper** spricht in lila Kursivschrift, Tipps stehen in Grau. Jede Quest erklärt, wie
  ihre Mod wirklich funktioniert. Zutaten des Dream Star sind mit „✦ Dream Star:“ markiert.
- **Buch-Einstellungen** (`data.snbt`): Titel „Dreamcraft – Quest Book“, Icon Quest Book, Standardform Kreis,
  Belohnungen pro Spieler (`default_reward_team: false`), Buch beim ersten Betreten (`give_book_on_first_join: true`).

### Die 14 Kapitel
| Gruppe | Kapitel | Quests | davon optional |
| --- | --- | --- | --- |
| ✦ The Dream | Prologue: A Strange Dream | 13 | 4 |
| ✦ The Dream | 1. The Settler | 18 | 7 |
| ✦ The Dream | 2. Into the Deep | 20 | 8 |
| ✦ The Dream | 3. Sparks of Industry | 36 | 10 |
| ✦ The Dream | 4. Paths of Power | 23 | 13 |
| ✦ The Dream | 5. Through the Fire | 15 | 5 |
| ✦ The Dream | 6. The Endless Sea | 81 | 16 |
| ✦ The Dream | 7. The End of the Dream | 15 | 6 |
| ✦ The Dream | Epilogue: Lucid Dreamer | 19 | 3 |
| ✦ Side Paths | Kitchen & Farm | 15 | 9 |
| ✦ Side Paths | Builder's Dream | 14 | 7 |
| ✦ Side Paths | Explorer's Atlas | 16 | 10 |
| ✦ Side Paths | Creatures & Companions | 16 | 12 |
| ✦ Side Paths | Tamagotchi | 27 | 15 |
| **Summe** | 14 Kapitel | **328** | 125 |

### Loot-Kisten in Dreamcraft
Die vier Loot Crates von Quest Icons würfeln diese Tabellen aus (Chance = Gewicht / Summe der Gewichte, aus dem
Generator berechnet):

**Common Crate** (`reward_tables/common_crate.snbt`, 16 Einträge):

| Item | Anzahl | Chance |
| --- | --- | --- |
| Bread | 8 | 12.7 % |
| Torch | 32 | 12.7 % |
| Steak | 6 | 9.5 % |
| Iron Ingot | 4 | 9.5 % |
| Coal | 16 | 9.5 % |
| Arrow | 24 | 6.3 % |
| Bone Meal | 16 | 6.3 % |
| Apple | 6 | 6.3 % |
| Leather | 6 | 5.1 % |
| Gold Ingot | 3 | 5.1 % |
| Emerald | 3 | 3.8 % |
| Lantern | 4 | 3.8 % |
| Rope *(Farmer's Delight)* | 12 | 3.2 % |
| Pet Kibble *(Tamagotchi)* | 8 | 2.5 % |
| Rope *(Beach Craft)* | 8 | 2.5 % |
| Name Tag | 1 | 1.3 % |

**Rare Crate** (`reward_tables/rare_crate.snbt`, 16 Einträge):

| Item | Anzahl | Chance |
| --- | --- | --- |
| Diamond | 2 | 11.2 % |
| Emerald | 8 | 11.2 % |
| Golden Apple | 2 | 9.0 % |
| Ender Pearl | 4 | 9.0 % |
| Block of Iron | 2 | 7.5 % |
| Bottle o' Enchanting | 16 | 7.5 % |
| Block of Gold | 1 | 6.0 % |
| Block of Lapis Lazuli | 2 | 6.0 % |
| Obsidian | 8 | 6.0 % |
| Saddle | 1 | 4.5 % |
| Name Tag | 2 | 4.5 % |
| Trial Key | 1 | 4.5 % |
| Ruby *(Jewelry (RPG Series))* | 2 | 3.7 % |
| Sapphire *(Jewelry (RPG Series))* | 2 | 3.7 % |
| Tamagotchi Heart *(Tamagotchi)* | 1 | 3.0 % |
| Titanium Ingot *(Beach Craft)* | 3 | 3.0 % |

**Epic Crate** (`reward_tables/epic_crate.snbt`, 15 Einträge):

| Item | Anzahl | Chance |
| --- | --- | --- |
| Diamond | 5 | 13.9 % |
| Bottle o' Enchanting | 48 | 11.1 % |
| Netherite Scrap | 1 | 9.3 % |
| Block of Emerald | 2 | 9.3 % |
| Totem of Undying | 1 | 7.4 % |
| Block of Diamond | 1 | 7.4 % |
| Shulker Shell | 2 | 7.4 % |
| Ancient Debris | 2 | 7.4 % |
| Nautilus Shell | 3 | 4.6 % |
| Ominous Trial Key | 1 | 4.6 % |
| Heart of the Sea | 1 | 3.7 % |
| Wither Skeleton Skull | 1 | 3.7 % |
| Netherite Upgrade | 1 | 3.7 % |
| Ancient Crystal *(Beach Craft)* | 1 | 3.7 % |
| Enchanted Golden Apple | 1 | 2.8 % |

**Legendary Crate** (`reward_tables/legendary_crate.snbt`, 11 Einträge):

| Item | Anzahl | Chance |
| --- | --- | --- |
| Netherite Ingot | 2 | 14.6 % |
| Totem of Undying | 2 | 14.6 % |
| Block of Diamond | 4 | 14.6 % |
| Enchanted Golden Apple | 2 | 12.2 % |
| Netherite Upgrade | 2 | 9.8 % |
| Elytra | 1 | 7.3 % |
| Nether Star | 1 | 7.3 % |
| Dragon's Breath | 8 | 6.1 % |
| Beacon | 1 | 4.9 % |
| Music Disc | 1 | 4.9 % |
| Heavy Core | 1 | 3.7 % |

### Alle Quests, Kapitel für Kapitel
Die Tabellen sind direkt aus dem Generator erzeugt. Lesehilfe: **Haben** = Items im Inventar haben, **Abgeben** =
Items werden über „Submit“ abgegeben, **Häkchen** = Knopf „Done!“, **Fortschritt** = Advancement, **Ansehen** = einen
Block oder Mob eine Weile anschauen. Kursiv in Klammern steht die Mod des Items. Quests ohne Aufgabe schließen sich
selbst ab, sobald ihre Voraussetzungen erledigt sind. Die Titel sind die englischen Namen aus dem Spiel.

### Prologue: A Strange Dream

*You fell asleep... and woke up somewhere else.* – Gruppe „✦ The Dream“, Datei `chapters/prologue.snbt`, **13 Quests**, davon 4 optional.

Der Einstieg. Der **Dreamkeeper** begrüßt dich und erklärt das Quest-Buch (J, Claim). Danach die ersten Schritte, jeweils mit dem Mod, der dabei hilft: Holz (FallingTree), Werkbank (JEI: R = Rezept, U = Verwendung), Steinzeit (Jade), Essen (AppleSkin), Bett, Lagerfeuer (Healing Campfire), Tragen (Carry On), Karte (Xaero, Ping Wheel), Rucksack (Traveler's Backpack) und Eisen. „The Dream Calls“ schließt sich selbst ab und öffnet die übrigen Kapitel. Die erste Quest („I am ready to dream“) war die, die vor dem Hotfix 1.0.2 nicht anklickbar war.

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | A Strange Dream | Häkchen: „I am ready to dream“ | 25 XP, 6× Bread |
| 2 | Punch a Tree | Haben: 16× beliebige Stämme | 4× Apple |
| 3 | The First Workbench | Haben: Crafting Table | 16× Stick |
| 4 | Stone Age | Haben: 32× Cobblestone + Haben: Stone Pickaxe | 16× Torch |
| 5 | Carry On *(optional)* | Häkchen: „I carried something“ | 30 XP |
| 6 | Hunger Pangs | Haben: 8× beliebiges Essen | Flint Knife |
| 7 | A Place to Sleep | Haben: ein beliebiges Bett | 3× Lantern |
| 8 | A Warm Fire *(optional)* | Haben: Campfire | 4× Cooked Chicken |
| 9 | Survive the Night | Besiegen: 5× Untote (beliebige) | 3× Iron Ingot, 50 XP |
| 10 | Where Am I? *(optional)* | Häkchen setzen | Common Loot Crate |
| 11 | Pack Your Bags *(optional)* | Haben: ein Traveler's Backpack | 60 XP |
| 12 | Iron Will | Haben: 12× Eisenbarren | 2× Common Loot Crate |
| 13 | The Dream Calls | – (fertig, sobald die Voraussetzungen erledigt sind) | Rare Loot Crate, 100 XP |

### 1. The Settler

*A home, a farm and a full belly.* – Gruppe „✦ The Dream“, Datei `chapters/settler.snbt`, **18 Quests**, davon 7 optional.

Haus, Hof und Küche: Farmer's Delight (Schneidebrett, Kochtopf, Herd, Rich Soil), RightClickHarvest, die Gießkanne aus Additional Additions, Farming for Blockheads (Futtertrog, Markt, Hühnernest), Mob Lassos, Villager In A Bucket und Trading Post, neue Berufe (More Villagers), Macaw's-Möbel, Waystones und die Mehrblock-Küche von Cooking for Blockheads.

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | A Home in the Dream | – (fertig, sobald die Voraussetzungen erledigt sind) | 20 XP |
| 2 | Till the Soil | Haben: eine beliebige Hacke + Haben: 16× Wheat | 16× Bone Meal |
| 3 | Watering Can *(optional)* | Haben: Watering Can *(Additional Additions)* | 16× Bone Meal |
| 4 | Wild Crops | Haben: 4× Cabbage *(Farmer's Delight)* + Haben: 4× Onion *(Farmer's Delight)* | 4× Rice |
| 5 | Knife and Board | Haben: Cutting Board *(Farmer's Delight)* + Haben: ein beliebiges Messer | 4× Tomato Seeds |
| 6 | The Cooking Pot | Haben: Cooking Pot *(Farmer's Delight)* + Haben: Stove *(Farmer's Delight)* | 4× Dumplings |
| 7 | Rich Soil *(optional)* | Haben: 4× Organic Compost *(Farmer's Delight)* | 8× Rich Soil |
| 8 | A Feast for Friends *(optional)* | Haben: Roast Chicken *(Farmer's Delight)* | Common Loot Crate |
| 9 | Animal Husbandry | Haben: Feeding Trough *(Farming for Blockheads)* | 2× Lead, 16× Wheat |
| 10 | The Market | Haben: Market *(Farming for Blockheads)* | 6× Emerald |
| 11 | Chicken Nest *(optional)* | Haben: Chicken Nest *(Farming for Blockheads)* | 16× Wheat Seeds |
| 12 | Catch Them All *(optional)* | Haben: Golden Lasso *(Mob Lassos)* | 8× Golden Carrot |
| 13 | A Villager in a Bucket | Haben: Villager In A Bucket *(Villager In A Bucket)* + Haben: Trading Post *(Trading Post)* | 12× Emerald |
| 14 | New Jobs in Town *(optional)* | Häkchen: „A villager took a new job“ | 8× Emerald |
| 15 | Home Sweet Home | Häkchen: „My house is built“ | 6× Lantern, Common Loot Crate |
| 16 | Waystones | Haben: Warp Stone *(Waystones)* | 3× Return Scroll |
| 17 | A Proper Kitchen *(optional)* | Haben: Cooking Table *(Cooking for Blockheads)* | Cooking for Blockheads I |
| 18 | Settled In | Haben: 16× Steak | Rare Loot Crate, 150 XP |

### 2. Into the Deep

*Ores, storage and the magic of enchanting.* – Gruppe „✦ The Dream“, Datei `chapters/deep.snbt`, **20 Quests**, davon 8 optional.

Bergbau, Lager und Verzaubern: Kohle, Kupfer, Gold, Necoium (Mythic Upgrades), Tiefenschiefer, Hämmer (JustHammers), Diamanten, Magnete (Simple Magnets), Magnum Torch, Tom's Simple Storage samt Crafting Terminal, Storage Drawers, Verzaubern mit Easy Magic und dem Enchanting Infuser, Easy Anvils, XP Storage, Better Archeology und Lootr.

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | Into the Deep | Haben: Iron Pickaxe | 32× Torch |
| 2 | Fuel for the Fire | Haben: 32× Coal | 2× Furnace |
| 3 | Copper Shine | Haben: 24× Kupferbarren | 40 XP |
| 4 | Gold Rush | Haben: 12× Goldbarren | 6× Golden Carrot |
| 5 | Necoium *(optional)* | Haben: 4× Necoium Ingot *(Mythic Upgrades)* | 80 XP |
| 6 | Deepslate | Haben: 64× Cobbled Deepslate | 4× Iron Ingot |
| 7 | Smash It | Haben: Iron Hammer *(Just Hammers)* | 3× Iron Ingot |
| 8 | Diamonds! | Haben: 5× Diamanten | Rare Loot Crate |
| 9 | Magnetic Personality *(optional)* | Haben: Magnet *(Simple Magnets)* | 50 XP |
| 10 | Keep the Dark Away *(optional)* | Haben: Diamond Magnum Torch *(Magnum Torch)* | Common Loot Crate |
| 11 | Organized Chaos | Haben: Inventory Connector *(Tom's Simple Storage Mod)* + Haben: Storage Terminal *(Tom's Simple Storage Mod)* | 16× Inventory Cable |
| 12 | Crafting Terminal *(optional)* | Haben: Crafting Terminal *(Tom's Simple Storage Mod)* | 16× Inventory Cable |
| 13 | Drawers *(optional)* | Haben: beliebige Schubladen (Storage Drawers) + Haben: Drawer Controller *(Storage Drawers)* | 2× Storage Upgrade (III) |
| 14 | Enchanted | Haben: Enchanting Table + Haben: 15× Bookshelf | 32× Lapis Lazuli |
| 15 | The Enchanting Infuser | Haben: Enchanting Infuser *(Enchanting Infuser)* | 10 Level |
| 16 | A Kinder Anvil *(optional)* | Haben: Anvil | 8× Bottle o' Enchanting |
| 17 | A Book of Experience *(optional)* | Haben: XP Book *(XP Storage)* | 200 XP |
| 18 | Dig Up the Past *(optional)* | Haben: Brush + Haben: Archeology Table *(Better Archeology)* | Common Loot Crate |
| 19 | Loot for Everyone | Struktur: „Explore a mineshaft“ | Rare Loot Crate |
| 20 | Master of the Deep | Haben: Diamond Pickaxe | 2× Rare Loot Crate, 300 XP |

### 3. Sparks of Industry

*Machines, power and automation.* – Gruppe „✦ The Dream“, Datei `chapters/industry.snbt`, **36 Quests**, davon 10 optional.

Das Technik-Kapitel, seit V1.3 mit 36 Quests der ganze Weg durch **Tech Reborn**: Gummibäume, Refined Iron, Schaltkreise, Maschinenrahmen, Generator und Kabel, Elektroofen, Erzverdopplung, Solarpanel, Battery Box und größere Speicher, Legierungen, Bohrer und Kettensäge, dann die Großmaschinen (Industrial Grinder, Industrial Blast Furnace, Assembling Machine, Chemical Reactor), Iridium, Implosion Compressor, Lapotron Crystal und am Ende der **Lapotronic Energy Orb** (Dream-Star-Zutat). Daneben: Quarry Plus (Additional Enchanted Miner), Quarry Reborn, Item Collectors, Trash Cans, Copper Hopper, Chunk Loaders, Moving Elevators, Tesseract, Wireless Chargers und die Platten von Dark Utilities.

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | Sparks of Industry | Haben: 32× Eisenbarren | Tech Reborn Manual |
| 2 | Rubber Trees | Haben: Treetap *(Tech Reborn)* + Haben: 8× Sap *(Tech Reborn)* | 4× Rubber Sapling |
| 3 | Refined Iron | Haben: 16× Refined Iron Ingot *(Tech Reborn)* | 2× Block of Coal |
| 4 | Electronic Circuits | Haben: 4× Electronic Circuit *(Tech Reborn)* | 32× Redstone Dust |
| 5 | Machine Frame | Haben: 2× Basic Machine Frame *(Tech Reborn)* | 8× Refined Iron Ingot |
| 6 | Let There Be Power | Haben: Generator *(Tech Reborn)* | 16× Insulated Copper Cable |
| 7 | Electric Furnace | Haben: Electric Furnace *(Tech Reborn)* | 80 XP |
| 8 | Ore Doubling | Haben: Grinder *(Tech Reborn)* | 16× Raw Iron |
| 9 | Free Energy | Haben: 2× Basic Solar Panel *(Tech Reborn)* | Red Cell Battery |
| 10 | Battery Bank | Haben: Battery Box *(Tech Reborn)* | 100 XP |
| 11 | Bigger Batteries *(optional)* | Haben: MFE *(Tech Reborn)* | 150 XP |
| 12 | Alloys | Haben: Alloy Smelter *(Tech Reborn)* | 16× Refined Iron Ingot |
| 13 | Power Tools *(optional)* | Haben: Basic Drill *(Tech Reborn)* + Haben: Basic Chainsaw *(Tech Reborn)* | Red Cell Battery |
| 14 | Let the Machines Dig | Haben: Quarry Plus *(QuarryPlus)* + Haben: 4× Marker Plus *(QuarryPlus)* | Rare Loot Crate |
| 15 | Quarry Reborn *(optional)* | Haben: Quarry *(Industrial Quarry Mod)* | 16× Quarry Tube |
| 16 | Item Collectors *(optional)* | Haben: Basic Item Collector *(Item Collectors)* | 2× Hopper |
| 17 | Take Out the Trash *(optional)* | Haben: Item Trash Can *(Trash Cans)* | 60 XP |
| 18 | Copper Hoppers *(optional)* | Haben: 4× Copper Hopper *(Copper Hopper)* | 16× Copper Ingot |
| 19 | Never Sleeping | Haben: Single Chunk Loader *(Chunk Loaders)* | Rare Loot Crate |
| 20 | Going Up *(optional)* | Haben: 2× Elevator Controller *(Moving Elevators)* | 100 XP |
| 21 | Tesseract *(optional)* | Haben: 2× Tesseract *(Tesseract)* | 150 XP |
| 22 | Wireless Charging *(optional)* | Haben: Basic Wireless Player Charger *(Wireless Chargers)* | 120 XP |
| 23 | Plates of Power *(optional)* | Haben: 4× Vector Plate *(DarkUtilities)* | 8× Blank Plate |
| 24 | The Dream Never Sleeps | Haben: Industrial Centrifuge *(Tech Reborn)* | Epic Loot Crate, 400 XP |
| 25 | Squeeze and Extract | Haben: Compressor *(Tech Reborn)* + Haben: Extractor *(Tech Reborn)* | 8× Refined Iron Ingot |
| 26 | Advanced Circuits | Haben: 4× Advanced Circuit *(Tech Reborn)* | 16× Glowstone Dust |
| 27 | Industrial Grinder | Haben: Industrial Grinder *(Tech Reborn)* | 8× Standard Machine Casing |
| 28 | Industrial Blast Furnace | Haben: Industrial Blast Furnace *(Tech Reborn)* | 4× Cupronickel Heating Coil |
| 29 | The Assembling Machine | Haben: Assembling Machine *(Tech Reborn)* | 200 XP |
| 30 | Chemical Reactor | Haben: Chemical Reactor *(Tech Reborn)* + Haben: 2× Synthetic Redstone Crystal *(Tech Reborn)* | 4× Block of Redstone |
| 31 | Energy Crystal | Haben: Energy Crystal *(Tech Reborn)* | 250 XP |
| 32 | Iridium | Haben: 4× Raw Iridium *(Tech Reborn)* | Rare Loot Crate |
| 33 | Implosion Compressor | Haben: Implosion Compressor *(Tech Reborn)* + Haben: Iridium Alloy Plate *(Tech Reborn)* | 16× TNT |
| 34 | Industrial Circuits | Haben: 2× Industrial Circuit *(Tech Reborn)* | 250 XP |
| 35 | Lapotron Crystal | Haben: Lapotron Crystal *(Tech Reborn)* | Epic Loot Crate |
| 36 | Lapotronic Energy Orb | Haben: Lapotronic Energy Orb *(Tech Reborn)* | Legendary Loot Crate, 500 XP |

### 4. Paths of Power

*Wizard, paladin, archer or rogue?* – Gruppe „✦ The Dream“, Datei `chapters/power.snbt`, **23 Quests**, davon 13 optional.

Klassen und Magie der RPG Series: Spell Binding Table und Zauberbücher (Spell Engine), die Wege des Magiers, Paladins, Bogenschützen und Schurken mit Rüstungen, die vier **Netherit-Stäbe** (einer davon ist Dream-Star-Zutat), Runes, Jewelry, Relics, Arsenal und die epischen Rüstungen von Armory.

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | Paths of Power | Häkchen: „Show me the paths“ | 50 XP |
| 2 | The Spell Binding Table | Haben: Spell Binding Table *(Spell Engine)* | 32× Lapis Lazuli, 5 Level |
| 3 | A Book of Spells *(optional)* | Haben: ein beliebiges Zauberbuch | 16× Lapis Lazuli, 5 Level |
| 4 | Path of the Wizard | Haben: Arcane Staff *(Wizards (RPG Series))* | Arcane Wand |
| 5 | Robes of Power *(optional)* | Haben: Arcane Hat *(Wizards (RPG Series))* + Haben: Arcane Robe Top *(Wizards (RPG Series))* + Haben: Arcane Robe Bottom *(Wizards (RPG Series))* + Haben: Arcane Boots *(Wizards (RPG Series))* | 16× Amethyst Shard |
| 6 | Fire and Frost *(optional)* | Haben: Fire Staff *(Wizards (RPG Series))* + Haben: Frost Staff *(Wizards (RPG Series))* | Rare Loot Crate |
| 7 | Path of the Paladin | Haben: Monk Workbench *(Paladins & Priests (RPG Series))* + Haben: Iron Claymore *(Paladins & Priests (RPG Series))* | Golden Apple |
| 8 | Crusader Plate *(optional)* | Haben: Crusader Chestplate *(Paladins & Priests (RPG Series))* | Iron Kite Shield |
| 9 | Path of the Archer | Haben: Archery Artisan Table *(Archers (RPG Series))* + Haben: Composite Longbow *(Archers (RPG Series))* | 64× Arrow |
| 10 | Ranger Gear *(optional)* | Haben: Archer Tunic *(Archers (RPG Series))* | Auto-Fire Hook |
| 11 | Path of the Rogue | Haben: Arms Station *(Rogues & Warriors (RPG Series))* + Haben: Iron Dagger *(Rogues & Warriors (RPG Series))* | 6× Iron Ingot |
| 12 | Assassin or Berserker *(optional)* | Haben: Assassin Tunic *(Rogues & Warriors (RPG Series))* | Iron Sickle |
| 13 | Netherite Mastery | Haben: Netherite Upgrade | 4× Diamond |
| 14 | Netherite Arcane Staff *(optional)* | Haben: Netherite Arcane Staff *(Wizards (RPG Series))* | Rare Loot Crate |
| 15 | Netherite Fire Staff *(optional)* | Haben: Netherite Fire Staff *(Wizards (RPG Series))* | Rare Loot Crate |
| 16 | Netherite Frost Staff *(optional)* | Haben: Netherite Frost Staff *(Wizards (RPG Series))* | Rare Loot Crate |
| 17 | Netherite Holy Staff *(optional)* | Haben: Netherite Holy Staff *(Paladins & Priests (RPG Series))* | Rare Loot Crate |
| 18 | Runes | Haben: Rune Crafting Altar *(Runes)* + Haben: Rune Pouch *(Runes)* | 16× Arcane Rune |
| 19 | Gems and Jewelry | Haben: Jeweler's Kit *(Jewelry (RPG Series))* + Haben: Ruby *(Jewelry (RPG Series))* | Gold Ring |
| 20 | Relics *(optional)* | Haben: ein beliebiges Relikt (Relics) | Rare Loot Crate |
| 21 | Legendary Arsenal *(optional)* | Haben: Cataclysm's Edge *(Arsenal (RPG Series))* | Epic Loot Crate |
| 22 | Epic Armor *(optional)* | Haben: Smithing Template *(Armory (RPG Series))* | Epic Loot Crate |
| 23 | Awakened Power | XP: 20 Level | Epic Loot Crate, Wahl: Ruby Ring / Sapphire Ring / Jade Ring / Citrine Ring |

### 5. Through the Fire

*The burning layer of the Dream.* – Gruppe „✦ The Dream“, Datei `chapters/nether.snbt`, **15 Quests**, davon 5 optional.

Der Nether mit BetterNether: Quarz und Gold, Nether-Rubine, Festung, Tränke, die neuen Bewohner (z. B. Nagas), Bastion, Nether-Stadt, antiker Schrott und Netherit, Advanced Netherite, der Ember Pup aus Tamagotchi und die Wither-Schädel.

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | Through the Fire | Haben: 10× Obsidian + Haben: Flint and Steel | 8× Golden Carrot |
| 2 | Into the Nether | Dimension: „Enter the Nether“ | 100 XP |
| 3 | Quartz and Gold | Haben: 32× Nether Quartz + Haben: Golden Helmet | 8× Gold Ingot |
| 4 | Nether Rubies *(optional)* | Haben: 4× Nether Ruby *(Better Nether)* | 120 XP |
| 5 | The Fortress | Struktur: „Find a nether fortress“ + Haben: 8× Blaze Rod | Rare Loot Crate |
| 6 | Potion Master | Haben: Brewing Stand + Haben: 8× Nether Wart | 16× Glass Bottle |
| 7 | Strange Locals *(optional)* | Besiegen: Naga | Rare Loot Crate |
| 8 | Bastion Remnant | Struktur: „Find a bastion“ | Rare Loot Crate |
| 9 | A City in the Fire *(optional)* | Struktur: „Find a nether city“ | Epic Loot Crate |
| 10 | Ancient Debris | Haben: 4× Ancient Debris | 16× Gold Ingot |
| 11 | Netherite | Haben: Netherite Ingot | Netherite Upgrade |
| 12 | Advanced Netherite *(optional)* | Haben: Netherite-Diamond Ingot *(Advanced Netherite)* | Epic Loot Crate |
| 13 | A Friend in the Flames *(optional)* | Ansehen: „Spot an Ember Pup“ | 4× Ember Jerky |
| 14 | Skulls of the Wither | Haben: 3× Wither Skeleton Skull | Rare Loot Crate |
| 15 | Forged in Fire | Haben: 12× Ender Pearl | Epic Loot Crate, 400 XP |

### 6. The Endless Sea

*A drowned dream: rafts, reefs and wrecks.* – Gruppe „✦ The Dream“, Datei `chapters/sea.snbt`, **81 Quests**, davon 16 optional.

Das Beach-Craft-Kapitel, für Beach Craft 3.0 neu geschrieben (81 Quests): der Weg zum Portal (Ancient Broken Ring, Crystal, Energy, Treibholz, Energy Staff, Rahmen), das Seafarer's Almanac und das Expedition Journal, Überleben auf dem Floß (Seil, Fundamente, Hai, Plastic Hook, Item Catcher, Receiver, Frischwasser, Grill, Floß-Farm, Ananas), die **ganze Story als Fortschritts-Quests** in der Reihenfolge ihrer Kapitel, Bauen, Titan, Energie, Boote und das Expedition Raft mit Upgrades, Tauchen und die Nebenorte und Kreaturen. Das **Heart of the Tide** führt zum Dream Star. Die Quest-Titel sind spoilerarm, die Aufgaben nennen aber die Story-Orte.

> ⚠️ **Spoiler-Warnung:** Die Aufgaben dieses Kapitels nennen die Story-Orte und den Endgegner von Beach Craft 3.0. Wer sich überraschen lassen will, überspringt die Tabelle.

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | The Endless Sea | Haben: Fishing Rod | 6× Raw Cod |
| 2 | Ancient Broken Ring | Haben: Ancient Broken Ring *(Beach Craft)* | 2× Empty Map |
| 3 | Ancient Crystal | Haben: Ancient Crystal *(Beach Craft)* | 80 XP |
| 4 | Ancient Energy | Haben: 3× Ancient Energy *(Beach Craft)* | 80 XP |
| 5 | Driftwood | Haben: 12× Driftwood Log *(Beach Craft)* | 16× Bone Meal |
| 6 | The Energy Staff | Haben: Energy Staff *(Beach Craft)* | 8× Glowstone Dust |
| 7 | Portal Frames | Haben: 10× Driftwood Portal Frame *(Beach Craft)* | 100 XP |
| 8 | Beyond the Horizon | Dimension: „Enter the Endless Sea“ | 8× Rope, 8× Raft Foundation |
| 9 | The Castaway | Fortschritt: „Find the Expedition Journal“ | Seafarer's Almanac, 100 XP |
| 10 | Keeper of the Light | Fortschritt: „Reach the Old Lighthouse“ | Common Loot Crate, 100 XP |
| 11 | Saltmere | Fortschritt: „Visit Saltmere“ | Common Loot Crate, 150 XP |
| 12 | The Coral Sigil | Fortschritt: „Take the Coral Sigil“ | 200 XP |
| 13 | Deep Science | Fortschritt: „Dive to Helix Research Station“ | Rare Loot Crate, 200 XP |
| 14 | The Pearl Sigil | Fortschritt: „Recover the Pearl Sigil“ | 250 XP |
| 15 | The Drowned City | Fortschritt: „Explore Port Solace“ | Rare Loot Crate, 250 XP |
| 16 | The Storm Sigil | Fortschritt: „Claim the Storm Sigil“ | 300 XP |
| 17 | Through Fire | Fortschritt: „Enter the Ashen Forge“ | Rare Loot Crate, 300 XP |
| 18 | The Ember Sigil | Fortschritt: „Carry the Ember Sigil out“ | 350 XP |
| 19 | The Coral Temple | Fortschritt: „Find the Coral Temple“ | Epic Loot Crate, 350 XP |
| 20 | The Tidewarden Key | Fortschritt: „Forge the Tidewarden Key“ | 400 XP |
| 21 | The Abyssal Sanctum | Fortschritt: „Reach the Abyssal Sanctum“ | Epic Loot Crate, 400 XP |
| 22 | The Leviathan | Fortschritt: „Defeat the Leviathan“ | Legendary Loot Crate, 20 Level |
| 23 | Heart of the Tide | Haben: Heart of the Tide *(Beach Craft)* | Epic Loot Crate, 500 XP |
| 24 | Tidebreaker *(optional)* | Haben: Tidebreaker *(Beach Craft)* | Epic Loot Crate |
| 25 | Master of the Sea | Haben: Raft Flag *(Beach Craft)* | Epic Loot Crate, 400 XP |
| 26 | The Seafarer's Almanac | Haben: Seafarer's Almanac *(Beach Craft)* | 50 XP, 3× Fresh Water |
| 27 | Rope | Haben: 8× Rope *(Beach Craft)* | 8× String |
| 28 | Expand the Raft | Haben: 32× Raft Foundation *(Beach Craft)* | 16× Palm Thatch |
| 29 | Shark Proof | Haben: 8× Reinforced Foundation *(Beach Craft)* | 6× Scrap Metal |
| 30 | Bruce | Besiegen: Bruce the Shark | 4× Cooked Shark Meat, Rare Loot Crate |
| 31 | Hammerhead *(optional)* | Besiegen: Hammerhead Shark | Rare Loot Crate |
| 32 | Shark Trophy *(optional)* | Haben: Shark Jaw Trophy *(Beach Craft)* | 100 XP |
| 33 | Plastic Hook | Haben: Plastic Hook *(Beach Craft)* | 6× Scrap Metal |
| 34 | Item Catcher | Haben: Item Catcher *(Beach Craft)* + Haben: Item Catcher Net *(Beach Craft)* | 8× Plastic |
| 35 | Receiver | Haben: Receiver *(Beach Craft)* | 150 XP |
| 36 | Driftwood Ahoy! | Haben: 16× Driftwood Log *(Beach Craft)* | Rare Loot Crate |
| 37 | Fresh Water | Haben: Water Purifier *(Beach Craft)* + Haben: 3× Fresh Water *(Beach Craft)* | 8× Glass Bottle |
| 38 | Simple Grill | Haben: Simple Grill *(Beach Craft)* | 8× Raw Cod |
| 39 | A Floating Farm | Haben: 4× Crop Plot *(Beach Craft)* + Haben: Scarecrow *(Beach Craft)* | 4× Coconut |
| 40 | Pineapples | Haben: 4× Pineapple *(Beach Craft)* | 2× Pineapple Crown |
| 41 | Island Drinks *(optional)* | Haben: Coconut Milk *(Beach Craft)* + Haben: Pina Colada *(Beach Craft)* | Common Loot Crate |
| 42 | Beach Builder | Haben: 16× Weathered Planks *(Beach Craft)* + Haben: 16× Teak Planks *(Beach Craft)* | 16× Bone Meal |
| 43 | Coral and Tidestone | Haben: 16× Coral Stone Bricks *(Beach Craft)* + Haben: 16× Tidestone Bricks *(Beach Craft)* + Haben: 4× Aqua Sea Glass *(Beach Craft)* | 16× Prismarine Shard |
| 44 | Island Lights | Haben: 4× Red Paper Lantern *(Beach Craft)* + Haben: 4× Warm String Lights *(Beach Craft)* + Haben: Hammock *(Beach Craft)* | 8× Rope |
| 45 | Pirate Style *(optional)* | Haben: Ship Cannon *(Beach Craft)* + Haben: 8× Cannonball *(Beach Craft)* + Haben: Treasure Chest *(Beach Craft)* | 8× Gunpowder |
| 46 | Steel and City *(optional)* | Haben: 2× Porthole *(Beach Craft)* + Haben: 4× Catwalk *(Beach Craft)* | 8× Scrap Metal |
| 47 | An Aquarium *(optional)* | Haben: Aquarium *(Beach Craft)* | Common Loot Crate |
| 48 | Titanium | Haben: 12× Titanium Ingot *(Beach Craft)* | Rare Loot Crate |
| 49 | Titanium Armor *(optional)* | Haben: Titanium Helmet *(Beach Craft)* + Haben: Titanium Chestplate *(Beach Craft)* + Haben: Titanium Leggings *(Beach Craft)* + Haben: Titanium Boots *(Beach Craft)* | Epic Loot Crate |
| 50 | Sun Power | Haben: Makeshift Solar Panel *(Beach Craft)* + Haben: Makeshift Battery *(Beach Craft)* | 16× Copper Cable |
| 51 | Wind Turbine | Haben: Wind Turbine *(Beach Craft)* | 2× Circuit Board |
| 52 | Raft Quarry *(optional)* | Haben: Quarry *(Beach Craft)* | Epic Loot Crate |
| 53 | Small Boats | Haben: Paddle *(Beach Craft)* | 60 XP |
| 54 | The Expedition Raft | Haben: Expedition Raft *(Beach Craft)* + Fortschritt: „Take the helm“ | Seafarer's Almanac, 150 XP |
| 55 | Raft Sail | Haben: Raft Sail *(Beach Craft)* | 8× Rope |
| 56 | Raft Engine | Haben: Raft Engine *(Beach Craft)* | 4× Block of Coal |
| 57 | Anchor and Cargo | Haben: Raft Anchor *(Beach Craft)* + Haben: Raft Cargo Crate *(Beach Craft)* | Rare Loot Crate |
| 58 | Raft Lanterns *(optional)* | Haben: Raft Lanterns *(Beach Craft)* | 100 XP |
| 59 | Diving Helmet | Haben: Diving Helmet *(Beach Craft)* | Seafarer's Almanac, 100 XP |
| 60 | Deep Breath | Haben: Oxygen Tank *(Beach Craft)* + Fortschritt: „Wear helmet and tank“ | 150 XP |
| 61 | Wetsuit and Flippers | Haben: Wetsuit *(Beach Craft)* + Haben: Flippers *(Beach Craft)* | 16× Dried Kelp |
| 62 | Air Compressor | Haben: Air Compressor *(Beach Craft)* | 150 XP |
| 63 | Helmet Lamp | Besiegen: Anglerfish + Häkchen: „My helmet has a lamp“ | Rare Loot Crate |
| 64 | Harpoon Gun | Haben: Harpoon Gun *(Beach Craft)* + Haben: 8× Harpoon *(Beach Craft)* | 8× Harpoon |
| 65 | Deep Diver *(optional)* | Haben: Sea Scooter *(Beach Craft)* + Haben: Titanium Oxygen Tank *(Beach Craft)* | Epic Loot Crate |
| 66 | Sunken Ruins | Struktur: „Find sunken ruins“ | Common Loot Crate |
| 67 | The Broken Freighter | Struktur: „Explore a cargo ship wreck“ | Rare Loot Crate |
| 68 | Lost Flight *(optional)* | Struktur: „Find a sunken plane“ | Rare Loot Crate |
| 69 | Ghost Ship | Fortschritt: „Explore a galleon wreck“ + Fortschritt: „Find a pirate gold coin“ | Rare Loot Crate |
| 70 | Saltjaw's Gold | Fortschritt: „Find the pirate cove“ | Epic Loot Crate, 9× Gold Coin |
| 71 | Rusted Giant | Fortschritt: „Climb aboard a rig“ | Rare Loot Crate |
| 72 | Cold Outpost *(optional)* | Struktur: „Find an iceberg outpost“ | Rare Loot Crate |
| 73 | Songs of the Sea *(optional)* | Haben: Lofi Beat Music Disc *(Beach Craft)* + Haben: Crystal Castles Music Disc *(Beach Craft)* + Haben: Some Game Music Disc *(Beach Craft)* | Epic Loot Crate |
| 74 | Crab Dinner | Ansehen: „Watch a crab“ + Fortschritt: „Eat a cooked crab claw“ | Seafarer's Almanac, 4× Cooked Crab Claw |
| 75 | Seagulls | Ansehen: „Watch a seagull“ | 8× Feather |
| 76 | Penguins on Ice *(optional)* | Ansehen: „Watch a penguin“ | 8× Raw Cod |
| 77 | Sea Otters | Ansehen: „Watch a sea otter“ | 4× Seashell |
| 78 | Reef Life | Ansehen: „Watch a manta ray“ + Ansehen: „Spot a moray eel“ | 2× Pearl |
| 79 | Jellyfish *(optional)* | Ansehen: „Watch a jellyfish“ | 4× Slimeball |
| 80 | Whale Watcher | Fortschritt: „Watch a whale through a spyglass“ | Rare Loot Crate |
| 81 | Cursed Crew | Besiegen: 3× Drowned Corsair | 6× Gold Coin |

### 7. The End of the Dream

*Find the stronghold. Face the dragon.* – Gruppe „✦ The Dream“, Datei `chapters/end.snbt`, **15 Quests**, davon 6 optional.

Augen des Enders, Festung, Endportal, der Drache („The Last Nightmare“), das Drachenei, die äußeren Inseln mit BetterEnd (End Stone Smelter, Terminite, Aeternium, ewige Portale), Endstadt, Elytren, der Drachenkopf am End-Schiff, Shulker-Kisten (Easy Shulker Boxes) und das Void Kitten aus Tamagotchi.

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | Eyes of Ender | Haben: 12× Eye of Ender | 4× Ender Pearl |
| 2 | The Stronghold | Struktur: „Find the stronghold“ | Rare Loot Crate |
| 3 | The End Portal | Dimension: „Enter the End“ | 200 XP |
| 4 | The Last Nightmare | Besiegen: Ender Dragon | Legendary Loot Crate, 30 Level |
| 5 | The Dragon Egg *(optional)* | Haben: Dragon Egg | Epic Loot Crate |
| 6 | The Outer Islands | Biom: „Visit the Foggy Mushroomland“ | Rare Loot Crate |
| 7 | Metals of the End | Haben: End Stone Smelter *(Better End)* + Haben: 4× Terminite Ingot *(Better End)* | Rare Loot Crate |
| 8 | Aeternium *(optional)* | Haben: Aeternium Ingot *(Better End)* | Epic Loot Crate |
| 9 | On Eternal Paths *(optional)* | Fortschritt: „Discover an eternal portal“ | Epic Loot Crate |
| 10 | End City | Struktur: „Find an End city“ + Haben: 4× Shulker Shell | Epic Loot Crate |
| 11 | Wings | Haben: Elytra | 32× Firework Rocket |
| 12 | A Dragon's Head *(optional)* | Haben: Dragon Head | Rare Loot Crate |
| 13 | Boxes in Boxes *(optional)* | Haben: Shulker Box | 2× Shulker Shell |
| 14 | A Kitten from the Void *(optional)* | Ansehen: „Spot a Void Kitten“ | 4× Fish Crackers |
| 15 | The Dream Is Free | – (fertig, sobald die Voraussetzungen erledigt sind) | Legendary Loot Crate, 1000 XP |

### Epilogue: Lucid Dreamer

*For those who never want to wake up.* – Gruppe „✦ The Dream“, Datei `chapters/epilogue.snbt`, **19 Quests**, davon 3 optional.

Für alle, die nie aufwachen wollen: Wither, Leuchtfeuer, Mythic Upgrades, Warden, eine legendäre Kiste und **Master of Dreams** (gibt seit V1.3 zwei Quest Crowns). Danach die Dream-Star-Kette: je eine Quest pro Zutat, „Living the Dream“ (Stern herstellen), „A Place of Honour“ (Sockel) und „The Dreamer's Legacy“ als letzte Quest.

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | Lucid Dreamer | – (fertig, sobald die Voraussetzungen erledigt sind) | 100 XP |
| 2 | The Wither | Besiegen: Wither | Epic Loot Crate |
| 3 | A Beacon in the Dream | Haben: Beacon | 2× Block of Diamond |
| 4 | Mythic Upgrades *(optional)* | Haben: Ametrine Ingot *(Mythic Upgrades)* | Epic Loot Crate |
| 5 | The Warden *(optional)* | Besiegen: Warden | Legendary Loot Crate |
| 6 | Crate Collector *(optional)* | Abgeben: Legendary Loot Crate | Legendary Loot Crate |
| 7 | Master of Dreams | Häkchen: „Finish the journey“ | 2× Legendary Loot Crate, Crown Icon, Crown Icon |
| 8 | The Dream Star | – (fertig, sobald die Voraussetzungen erledigt sind) | 500 XP |
| 9 | The Quest Crown | Haben: Crown Icon | 100 XP |
| 10 | Ametrine Ingots | Haben: 2× Ametrine Ingot *(Mythic Upgrades)* | 200 XP |
| 11 | Lapotronic Energy Orb | Haben: Lapotronic Energy Orb *(Tech Reborn)* | 200 XP |
| 12 | Heart of the Tide | Haben: Heart of the Tide *(Beach Craft)* | 200 XP |
| 13 | A Dragon's Treasure | – (fertig, sobald **eine** der Voraussetzungen erledigt ist) | 200 XP |
| 14 | Tamagotchi Heart | Haben: Tamagotchi Heart *(Tamagotchi)* | 100 XP |
| 15 | A Netherite Staff | – (fertig, sobald **eine** der Voraussetzungen erledigt ist) | 200 XP |
| 16 | Nether Star | Haben: Nether Star | 200 XP |
| 17 | ✦ Living the Dream ✦ | Haben: Dream Star | Legendary Loot Crate, 30 Level |
| 18 | A Place of Honour | Haben: Dream Star Pedestal + Ansehen: „Admire your Dream Star on its pedestal“ | Legendary Loot Crate |
| 19 | The Dreamer's Legacy | Häkchen: „Thank you, Dreamkeeper“ | 3× Legendary Loot Crate, 50 Level, 2× Enchanted Golden Apple, 64× Firework Rocket |

### Kitchen & Farm

*Everything about food, farming and cooking.* – Gruppe „✦ Side Paths“, Datei `chapters/kitchen.snbt`, **15 Quests**, davon 9 optional.

Seitenpfad Küche: Pfanne und Reis (Farmer's Delight), More Delight, Rustic Delight und Kaffee, Ube's Delight, Leckereien aus Additional Additions, Ahornsirup (Ecologics), Storage Delight, Dünger und Sprinkler (Farming for Blockheads) und die Küche von Cooking for Blockheads bis zur Kochmütze.

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | Kitchen & Farm | Haben: 32× beliebiges Essen | 30 XP |
| 2 | The Skillet | Haben: Skillet *(Farmer's Delight)* | 8× Egg |
| 3 | Rice Paddies *(optional)* | Haben: 8× Rice Panicle *(Farmer's Delight)* | Bag of Rice |
| 4 | More Delight *(optional)* | Haben: Loaded Hamburger *(More Delight)* | 6× Tomato |
| 5 | Rustic Delight *(optional)* | Haben: Green Bell Pepper *(Rustic Delight)* | Common Loot Crate |
| 6 | Morning Coffee *(optional)* | Haben: Coffee *(Rustic Delight)* | 4× Cabbage |
| 7 | Ube's Delight *(optional)* | Haben: 4× Ube *(Ube's Delight)* | Common Loot Crate |
| 8 | Sweet Little Things *(optional)* | Haben: Sweet Berry Pie *(Additional Additions)* + Haben: Honeyed Apple *(Additional Additions)* | 16× Sweet Berries |
| 9 | Maple Syrup *(optional)* | Haben: Maple Syrup Bottle *(Ecologics)* | 16× Sugar |
| 10 | Crate and Barrel | Haben: Carrot Crate *(Farmer's Delight)* | 4× Canvas |
| 11 | Fertilizer | Haben: 4× Green Fertilizer *(Farming for Blockheads)* | 32× Bone Meal |
| 12 | Sprinkler *(optional)* | Haben: Sprinkler *(Farming for Blockheads)* | Common Loot Crate |
| 13 | Kitchen Multiblock | Haben: Sink *(Cooking for Blockheads)* + Haben: Kitchen Counter *(Cooking for Blockheads)* | Rare Loot Crate |
| 14 | Ovens and Toasters *(optional)* | Haben: Toaster *(Cooking for Blockheads)* + Haben: Milk Jar *(Cooking for Blockheads)* | Milk Bucket |
| 15 | Master Chef | Haben: Chef Hat *(Cooking for Blockheads)* + Häkchen: „I cooked my way through the add-ons“ | Rare Loot Crate, 150 XP |

### Builder's Dream

*Blocks, furniture and the tools to build big.* – Gruppe „✦ Side Paths“, Datei `chapters/builder.snbt`, **14 Quests**, davon 7 optional.

Seitenpfad Bauen: Meißel (Rechiseled), Stoneworks, Bau-Zauberstab, Effortless Building, Kreide, die Macaw's-Mods, Beautify, Additional Lanterns, Magic Vibe Decorations, Dawn of Time, Ketten (Reconnectible Chains) und Armor Statues.

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | Builder's Dream | Haben: 64× beliebige Bretter | 30 XP |
| 2 | The Chisel | Haben: Chisel *(Rechiseled)* | 64× Stone Bricks |
| 3 | Stoneworks *(optional)* | Haben: Stonecutter + Haben: 16× Andesite Tiles *(Stoneworks)* | 64× Andesite |
| 4 | Building Wand | Haben: Iron Wand *(Construction Wand (Fabric))* | 64× Cobblestone |
| 5 | Effortless Building | Häkchen: „I tried a build mode“ | 32× Glass |
| 6 | Chalk Marks *(optional)* | Haben: Chalk *(Chalk)* | Glow Chalk |
| 7 | Macaw's Collection | Haben: Oak Roof *(Macaw's Roofs)* + Haben: Resizeable Oak Window *(Macaw's Windows)* + Haben: Oak Bridge *(Macaw's Bridges)* | Common Loot Crate |
| 8 | Furnish It | Haben: 2× Oak Chair *(Macaw's Furniture)* + Haben: Oak Table *(Macaw's Furniture)* | 32× Oak Planks |
| 9 | In the Details *(optional)* | Haben: Oak Barn Door *(Macaw's Doors)* + Haben: 16× Andesite Flagstone *(Macaw's Paths and Pavings)* + Haben: Oak Blinds *(Beautify)* | Common Loot Crate |
| 10 | Light It Up *(optional)* | Haben: 4× Amethyst Lantern *(Additional Lanterns)* | 32× Torch |
| 11 | Magic Vibes *(optional)* | Haben: Ametrine Crystal Lamp *(Magic Vibe Decorations)* | 16× Amethyst Shard |
| 12 | Dawn of Time *(optional)* | Häkchen: „I found a style I like“ | Common Loot Crate |
| 13 | Hang in There *(optional)* | Haben: 8× Iron Chain + Haben: Armor Stand | 4× Lantern |
| 14 | Master Builder | Häkchen: „My dream build is done“ | Rare Loot Crate, 200 XP |

### Explorer's Atlas

*Biomes, structures and how to find them.* – Gruppe „✦ Side Paths“, Datei `chapters/atlas.snbt`, **16 Quests**, davon 10 optional.

Seitenpfad Erkunden: Nature's Compass, Explorer's Compass, /wits, Hängegleiter, Dörfer, Tavernen, Plünderer-Außenposten, Bryce Canyon (Terralith), Berge (Tectonic), Friedhöfe, Burgen, Himmelsinseln, Trial Chambers, Lost Relics und 10 km Wandern.

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | Explorer's Atlas | Haben: Compass | 4× Empty Map |
| 2 | Nature's Compass | Haben: Nature's Compass *(Nature's Compass)* | 60 XP |
| 3 | Explorer's Compass | Haben: Explorer's Compass *(Explorer's Compass)* | 60 XP |
| 4 | What Is This Place? *(optional)* | Häkchen: „I asked /wits“ | 40 XP |
| 5 | Hang Glider | Haben: Hang Glider *(Hang Glider)* | 16× Feather |
| 6 | A Village | Struktur: „Find a village“ | 8× Emerald |
| 7 | The Tavern *(optional)* | Struktur: „Find a tavern“ | Rare Loot Crate |
| 8 | Pillagers! *(optional)* | Struktur: „Find a pillager outpost“ | Rare Loot Crate |
| 9 | Bryce Canyon *(optional)* | Biom: „Visit a Bryce Canyon“ | Common Loot Crate |
| 10 | Above the Clouds *(optional)* | Biom: „Stand on a mountain“ | Spyglass |
| 11 | A Graveyard *(optional)* | Struktur: „Find a large graveyard“ | Rare Loot Crate |
| 12 | Castles and Keeps *(optional)* | Struktur: „Find a ruined castle“ | Epic Loot Crate |
| 13 | Islands in the Sky *(optional)* | Struktur: „Visit a sky castle tower“ | Epic Loot Crate |
| 14 | Trial Chambers *(optional)* | Struktur: „Find the trial chambers“ + Haben: Trial Key | Epic Loot Crate |
| 15 | Lost Relics *(optional)* | Haben: ein beliebiges Relikt (Lost Relics) | Rare Loot Crate |
| 16 | World Traveller | Statistik: „Walk 10 km“ | Epic Loot Crate, 300 XP |

### Creatures & Companions

*Friends, foes and fearsome mutants.* – Gruppe „✦ Side Paths“, Datei `chapters/creatures.snbt`, **16 Quests**, davon 12 optional.

Seitenpfad Tiere und Monster: Naturalist (Schmetterlinge, Bären, Safari-Tiere, Fangnetz), Friends&Foes (Moobloom, Tuff Golem, Glare, Wildfire), Pinguine (Ecologics), Lovely Snails, Respawnable Pets, Woodwalkers, Variants&Ventures (Gelid und Co.), die ganze Mutant-Familie und der „Lich“ aus The Graveyard (im Spiel heißt er Corrupted Champion).

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | Creatures & Companions | Häkchen setzen | 30 XP |
| 2 | Butterflies | Ansehen: „Watch a butterfly“ | 2× Honey Bottle |
| 3 | Bear Country *(optional)* | Ansehen: „Spot a bear“ | 16× Sweet Berries |
| 4 | Safari *(optional)* | Ansehen: „Spot an elephant“ + Ansehen: „Spot a giraffe“ | 4× Hay Bale |
| 5 | Bug Net *(optional)* | Haben: Capture Net *(Naturalist)* | 4× Glass Bottle |
| 6 | Moobloom *(optional)* | Ansehen: „Find a moobloom“ | 4× Sunflower |
| 7 | Little Helpers *(optional)* | Ansehen: „Find a glare“ | 16× Copper Ingot |
| 8 | Penguins *(optional)* | Ansehen: „Find a penguin“ | 8× Raw Cod |
| 9 | The Slow Lane *(optional)* | Ansehen: „Find a snail“ | Saddle |
| 10 | A Loyal Friend | Haben: 8× Bone | Name Tag |
| 11 | Walk in Their Shoes *(optional)* | Häkchen: „I walked as a mob“ | 100 XP |
| 12 | New Faces in the Dark *(optional)* | Besiegen: Gelid | Common Loot Crate |
| 13 | Mutant Zombie | Besiegen: Mutant Zombie | Epic Loot Crate |
| 14 | The Whole Mutant Family *(optional)* | Besiegen: Mutant Skeleton + Besiegen: Mutant Creeper + Besiegen: Mutant Enderman | Legendary Loot Crate |
| 15 | The Wildfire *(optional)* | Besiegen: Wildfire | Epic Loot Crate |
| 16 | The Lich *(optional)* | Besiegen: Corrupted Champion | Legendary Loot Crate |

### Tamagotchi

*Ten rare pets hide in the world. Find them all!* – Gruppe „✦ Side Paths“, Datei `chapters/pets.snbt`, **27 Quests**, davon 15 optional.

Neuer Seitenpfad für Tamagotchi (27 Quests): Tamagotchi Heart und Tamacon, „Pets in Hiding“ mit den zehn Pets rundherum (je eine optionale Quest „Spot a …“), Zähmen, Pager, Füttern, Spielen, Baden, Schlafen, Rucksack, Talente, Möbel, Gadgets, Plüschtiere und „Gotta Pet 'Em All“ (alle zehn zähmen).

| # | Quest | Aufgabe | Belohnung |
| --- | --- | --- | --- |
| 1 | Tamagotchi | Haben: Tamagotchi Heart *(Tamagotchi)* | 8× Pet Kibble |
| 2 | The Tamacon | Haben: Tamacon *(Tamagotchi)* | 50 XP |
| 3 | Pets in Hiding | – (fertig, sobald die Voraussetzungen erledigt sind) | 50 XP |
| 4 | Desert Dragon *(optional)* | Ansehen: „Spot a Desert Dragon“ | 4× Dragon Fruit |
| 5 | Jungle Dragon *(optional)* | Ansehen: „Spot a Jungle Dragon“ | 4× Dragon Fruit |
| 6 | Tide Dragon *(optional)* | Ansehen: „Spot a Tide Dragon“ | 4× Fish Crackers |
| 7 | Frost Penguin *(optional)* | Ansehen: „Spot a Frost Penguin“ | 4× Fish Crackers |
| 8 | Ember Pup *(optional)* | Ansehen: „Spot an Ember Pup“ | 4× Ember Jerky |
| 9 | Sculk Wisp *(optional)* | Ansehen: „Spot a Sculk Wisp“ | 4× Glow Gummy |
| 10 | Void Kitten *(optional)* | Ansehen: „Spot a Void Kitten“ | 4× Fish Crackers |
| 11 | Pebble Golem *(optional)* | Ansehen: „Spot a Pebble Golem“ | 4× Rock Candy |
| 12 | Hex Toad *(optional)* | Ansehen: „Spot a Hex Toad“ | 4× Glow Gummy |
| 13 | Mimic *(optional)* | Ansehen: „Spot a Mimic“ | 4× Golden Biscuit |
| 14 | A New Best Friend | Fortschritt: „Tame a pet“ | Rare Loot Crate, 16× Pet Kibble |
| 15 | Beep Beep! | Fortschritt: „Get a Tama Pager“ | 100 XP |
| 16 | Feeding Time | Haben: 8× Pet Kibble *(Tamagotchi)* + Haben: Food Bowl *(Tamagotchi)* | 16× Pet Kibble |
| 17 | Favourite Treats *(optional)* | Haben: Dragon Fruit *(Tamagotchi)* + Haben: Fish Crackers *(Tamagotchi)* + Haben: Ember Jerky *(Tamagotchi)* + Haben: Rock Candy *(Tamagotchi)* + Haben: Glow Gummy *(Tamagotchi)* + Haben: Golden Biscuit *(Tamagotchi)* | Rare Loot Crate |
| 18 | Playtime | Haben: Laser Pointer *(Tamagotchi)* + Haben: Squeaky Ball *(Tamagotchi)* + Haben: Feather Wand *(Tamagotchi)* | 150 XP |
| 19 | Squeaky Clean | Haben: Pet Brush *(Tamagotchi)* + Haben: Pet Bath *(Tamagotchi)* | 8× White Wool |
| 20 | Sweet Dreams | Haben: Pet Bed *(Tamagotchi)* | 16× Pet Kibble |
| 21 | A Backpack for Your Pet | Haben: Chest + Häkchen: „My pet wears a backpack“ | 2× Golden Apple |
| 22 | Hidden Talents | Häkchen: „My pet used its talent“ | Rare Loot Crate |
| 23 | Brave Little Friend *(optional)* | Haben: Pet Incubator *(Tamagotchi)* | Rare Loot Crate |
| 24 | Pet Paradise *(optional)* | Haben: Bouncy Mushroom *(Tamagotchi)* + Haben: Running Wheel *(Tamagotchi)* + Haben: Scratching Post *(Tamagotchi)* + Haben: Pet House *(Tamagotchi)* | Rare Loot Crate |
| 25 | Pet Gadgets *(optional)* | Haben: Treat Dispenser *(Tamagotchi)* + Haben: Toy Box *(Tamagotchi)* + Haben: Pet Flap *(Tamagotchi)* | Rare Loot Crate |
| 26 | Plushies and Portraits *(optional)* | Haben: Pet Portrait *(Tamagotchi)* + Haben: Egg Lamp *(Tamagotchi)* | 100 XP |
| 27 | Gotta Pet 'Em All | Fortschritt: „Tame all ten pets“ | 2× Legendary Loot Crate, 1000 XP |

---

## 10. Das Dream-Star-Endgame

Der **Dream Star** ist die End-Trophäe – „Proof that you finished Dreamcraft“, wie der ATM Star der All-The-Mods-Packs.
Die Idee: Das Rezept braucht **einen Schatz aus jeder Ecke des Packs**, deshalb führt jedes Kapitel ein Stück näher.

| Zutat | Woher | Kapitel |
| --- | --- | --- |
| 2× Ametrine Ingot | Mythic Upgrades: Ametrine aus dem End + Necoium Ingots | Epilog, Kapitel 2 (Necoium) |
| Quest Crown | Belohnung von „Master of Dreams“ (gibt zwei) | Epilog |
| Netherite Arcane/Fire/Frost Staff oder Netherite Holy Staff | Wizards / Paladins & Priests, Schmiedetisch + Netherit-Vorlage | 4. Paths of Power |
| Nether Star | Wither | Epilog |
| Lapotronic Energy Orb | Tech Reborn: 8 Lapotron Crystals um eine Iridium Alloy Plate | 3. Sparks of Industry |
| Tamagotchi Heart | 5 rote Farbe um eine Amethystscherbe | Tamagotchi |
| Dragon Egg oder Dragon Head | Drachenei auf dem Ausgangsportal, Kopf am End-Schiff | 7. The End of the Dream |
| Heart of the Tide | Beute des Leviathan in Beach Craft | 6. The Endless Sea |

**Die Quest-Kette im Epilog:** „Master of Dreams“ → „The Dream Star“ (Erklärung, schließt sich selbst ab) → je eine
Quest pro Zutat → **„✦ Living the Dream ✦“** (Stern herstellen: Legendary Crate + 30 Level) → **„A Place of Honour“**
(Sockel herstellen und den Stern darauf 3 s ansehen) → **„The Dreamer's Legacy“** (3 Legendary Crates, 50 Level,
2 verzauberte goldene Äpfel, 64 Feuerwerksraketen). Das Herstellen schaltet zusätzlich die Challenge „Living the
Dream“ frei. Rezepte und Sockel im Detail: [02_quest_icons.md](02_quest_icons.md#9-der-dream-star-und-sein-sockel-neu-in-110).

---

## 11. Testen im Container (`tools/dctest`)

- Ein kleiner Fabric-Mod startet das ganze Pack in einem Client-Game-Test (`./gradlew runPack`); `tools/dc_prepare.py`
  kopiert vorher Mods und Configs nach `build/run/client`. Szenen: `boot`, `smoke` (Welt erstellen, umsehen),
  `quests` (Kapitel-Screenshots `-Pchapters=all`, Fenster/GUI-Skalen `-Pwin`, `-Pgui`, Quests öffnen `-Pquests`,
  Dimension besuchen und `/locate` mit `-Pvisit`/`-Plocate`, Registry-Dump `-Pdump`) und `film`.
- `KeyFix` füllt spät registrierte Tastenbelegungen, `mixin/ScreenshotLeakMixin` behebt ein Speicherleck der
  Fabric-Gametest-API (8 MB pro Bild), `FilmSound` + `SoundLogMixin` protokollieren alle Spielgeräusche für die Videos.
- **V1.3 wurde so geprüft:** Smoke-Lauf und Kapitel-Screenshots (Ordner `$SP/v13/run/`), Registry-Dump mit
  Dream-Star-Rezept-Check (`dream_star` geladen, `dream_star_vanilla` nicht, Sockel geladen), `qcheck.py` ohne Fehler.
  Gelaufen ist das mit den Jars aus `$SP/ownjars` (Quest Icons 1.1.0, Beach Craft 3.0.0, Tamagotchi 1.2.0). Der
  Produktiv-Test folgte am 4.11.: das fertige Zip wie ein Launcher installiert (252 Mods, 0 Fehler), Client bis ins
  Spiel (Hauptmenü, neue Welt, Quest-Buch mit 14 Kapiteln; „0/203“ zählt nur Pflicht-Quests, dazu 125 optionale = 328),
  Server-Pack gestartet (363 Mods, „Done“ nach 33 s, 328 Quests, Raft-Strukturen per `/locate` gefunden). Im Log nur
  Umgebungsfehler (kein Ton, keine Anmeldung, kein Discord).
