# 03 – Beach Craft: der Raft-Mod (2.0 und 3.0 „Tides of the Deep“)

**Beach Craft** ist dein Raft-Mod (CurseForge-Name „Beach Craft“, Projekt **1010922**, Mod-ID `raft`, Repo
`Kasax007/Kasax_Raft_Mod`). Er bringt das Hochsee-Überleben aus dem Spiel *Raft* nach Minecraft: Man reist durch ein
Treibholz-Portal in die Dimension **„The Endless Sea“** (`raft:raftdim`), baut ein Floß, fischt Treibgut, reinigt
Wasser und wehrt den Hai Bruce ab. Mit 3.0 wurde daraus eine ganze Inselwelt mit Story und Boss.

## 1. Überblick und Versionen

| Version | CurseForge-Datei | Stand |
| --- | --- | --- |
| 2.0.0+26.3 | 9402661 | veröffentlicht (2.11.2026), Port auf 26.3 mit neuem Überlebens-Inhalt |
| 2.0.1+26.3 | 9408472 | veröffentlicht (2.11.2026), über 20 Fehler aus dem Review-Video behoben |
| **3.0.0+26.3** | – | **fertig, nicht hochgeladen** (Upload hat das Berechtigungssystem blockiert) |

- **Branch:** `26.3` und `3.0-dev` zeigen beide auf Commit `e16c820` („Beach Craft 3.0.0: CurseForge page, changelog and
  images“), lokal und auf GitHub gleich. `gradle.properties`: `mod_version=3.0.0+26.3`.
- **Das fertige Release-Paket** liegt im Scratchpad: `$SP/release_bc3/` mit `raft-3.0.0+26.3.jar` (7,7 MB),
  `changelog-3.0.0+26.3.md`, `description.html` und `beachcraft3_page_preview.png`. **Achtung:** Der Scratchpad ist
  flüchtig. Geht er verloren, baut man das Jar mit `./gradlew build` aus Branch `26.3` neu.
- **Voraussetzungen:** Minecraft 26.3, Fabric Loader 0.19.5 oder neuer, Fabric API (0.165.0+26.3). Team Reborn
  Energy 5 ist eingebaut.
- **Spezifikation:** `docs/design/beachcraft3.md` (Abschnitt 14 „Deviations“ gilt vor dem Plan). Spielertexte mit
  geprüften Zahlen: `tools/content/guide/texts.py` (der Seafarer's Almanac).

---

## 2. Beach Craft 2.0 – Port und Floß-Überleben

### 2.1 Was beim Port passierte
- Port vom Branch `1.21.1` auf 26.3 (offizielle Mojang-Namen, Loom 1.17.21, Java 25, Fabric API 0.165, Team Reborn
  Energy 5).
- **Eigenes Portal:** Die Custom Portal API gibt es für 26.3 nicht. Jetzt: Treibholz-Portalrahmen, angezündet mit dem
  Energy Staff.
- **Das Portal ist machbar geworden:** Treibholz wächst als Stümpfe an Oberwelt-Stränden, ein Rezept gibt 4 Rahmen,
  Ancient Broken Rings gibt es in Schiffswrack-, Schatz- und Ruinen-Loot (und beim Angeln).
- Die Raft-Dimension wurde höher; die Ankunftsplattform liegt hoch über den Wellen (y ≈ 209).
- Neu in 2.0.0: Floß-Fundamente, Seil, Strickleiter, Seilrolle, Wasserreiniger, Grill, Pflanzbeet, Vogelscheuche,
  Kokosmilch, Plastikhaken, Paddel, Empfänger, Treibgut, der Hai **Bruce** samt Trophäe, Deko (Palmenstroh, Segeltuch,
  Steuerrad, Flagge, Kokosnuss-Laterne, Schrott- und Plastikblock).

### 2.2 Der Weg ins Meer
1. **Ancient Broken Rings** suchen (Schiffswrack-Schätze, vergrabene Schätze, Ozeanruinen, Angeln) und zu
   **Ancient Energy** schmelzen. Schiffswrack-Schätze haben auch **Ancient Crystals**.
2. **Energy Staff:** Ancient Energy oben, Ancient Crystal in der Mitte, Stock unten – zündet 64-mal.
3. **Rahmen:** kurze dunkle Treibholz-Stümpfe an Sandstränden; 4 Treibholz-Stämme um 1 Ancient Energy = 4 Rahmen.
   Bauen wie ein Netherportal (innen mindestens 2×3 frei) und mit dem Stab anzünden.
4. **Ankunft** auf einer Treibholz-Plattform hoch über dem Meer, mit Rückportal. Seit 3.0 wartet auf einer **neuen**
   Plattform eine Castaway-Truhe.
5. **Ohne Portal:** Raft Dimension Teleporter (5 Titanbarren + 2 Ancient Energy), 64 Nutzungen, hin und zurück.

### 2.3 Überleben auf dem Floß
| Thema | So funktioniert es |
| --- | --- |
| Treibgut | Die Strömung bringt Bretter, Palmblätter, Plastik und Schrott von West nach Ost, ab und zu Beute; seit 3.0 selten Flaschenpost und Vorratsfässer |
| Plastic Hook | Benutzen halten zieht treibende Items aus bis zu 12 Blöcken heran |
| Item Catcher | fängt Treibgut im Wasser (eine Sorte gleichzeitig, Trichter können leeren); mit Netz (32 Fänge) etwa alle 30 s Unrefined Ocean Garbage → Trash Cube → 1–3 Überraschungen |
| Fundamente | 7 Bretter mit Seil oben und unten in der Mitte = 4 Raft Foundations; Seil aus 2 Palmblättern oder 3 Fäden; Fundament + 2 Schrott = Reinforced Foundation |
| Hai | Bruce kreist um Flöße, auf denen jemand steht; alle 15–45 s beißt er ein Randfundament, nach 4 Bissen bricht es (seit 3.0). Verstärkte Fundamente beißt er nie. Treffer verjagen ihn eine Weile. `/gamerule raft:shark_bites false` stellt das Beißen ab |
| Wasser | Water Purifier: Wasserflaschen → Fresh Water, ein Eimer gibt drei; Brennstoff Bretter, Stämme, Kohle |
| Essen | Simple Grill: zwei Speisen, 50 % schneller als ein Lagerfeuer; Kokosnüsse wachsen nach ~20 min nach; Kokosmilch = Regeneration, Piña Colada = Tempo |
| Pflanzen | Crop Plot: immer bewässert, nie zertrampelt, ~50 % schneller; seit 3.0 Ananas aus der Pineapple Crown |
| Vogelscheuche | keine Monster-Spawns in 24 Blöcken, kein Zertrampeln in 8 Blöcken, seit 3.0 keine pickenden Möwen in 16 Blöcken |

### 2.4 Technik (FE, Team Reborn Energy – andere Tech-Mods können andocken)
- Makeshift Solar Panel 10 FE/t (über der Endless Sea geht die Sonne nie unter), seit 3.0 Wind Turbine 20 FE/t.
- Makeshift Battery 1 000 000 FE; Copper Cable 128 FE/t, Titanium Cable 512 FE/t.
- Quarry: 11×11 bis zum Weltboden, 1 000 FE pro Block, Truhe obendrauf; Chunk Destroyer: ganzer Chunk, 100 000 FE pro Säule.
- Brick Furnace 1,5-mal schneller; Titanium Furnace 32-mal schneller und verdoppelt jedes Ergebnis.
- Circuit Board (Kupfer, Schleimball, Plastik) steckt in den meisten Maschinen-Rezepten.

### 2.5 Titan
Titanerz gibt es nur in der Raft-Dimension, unter y 20 unter dem Meeresboden; Diamantspitzhacke. 9 Nuggets = Barren,
9 Barren = Block. Die volle Titanrüstung gibt **Wasseratmung, Gunst des Delfins und Conduit Power**. Der
Metalldetektor meldet die Höhe des ersten Titanerzes unter dir, der Receiver Richtung und Entfernung zum nächsten
treibenden Treibholz. Titan-Werkzeuge gibt es nicht.

### 2.6 Was 2.0.1 behoben hat (Auszug aus `changelog-2.0.1+26.3.md`)
Haie spawnten im immer hellen Meer nie (Licht-Prüfung für Monster) und verschwanden bei Tag; Segeltuch war nicht
herstellbar (Rezept-Konflikt mit der Seilrolle, jetzt 2 Seil über 2 weißer Wolle); Paddel schob das Boot nicht (der
Schub kam nur beim Server an, Boote steuert aber der Client – fiel erst beim Filmen auf); Item Catcher, Wasserreiniger,
Grill und Vogelscheuche repariert; Kokosnüsse wuchsen erst nach ~95 h nach; Treibholz und Palmenholz brennen im Ofen;
Steinbruch und Chunk Destroyer löschen keine Shulker-Inhalte mehr und speichern ihren Fortschritt; kein
Energie-Ping-Pong zwischen Batterien; Tooltips mit echten Zahlen; Portal- und Teleporter-Korrekturen; Musik-Discs
(eine pro Wrack-Truhe), Titanerz gibt XP, Set-Effekte enden nach dem Ablegen. Der Prüfbericht dazu ist
`beachcraft/review/REPORT.md` im Archiv ([06](06_videos_und_beschreibungen.md)).

---

## 3. Beach Craft 3.0 „Tides of the Deep“

Ziel laut Spezifikation: die Raft-Dimension zu einer lebendigen Ozeanwelt machen – Inselgelände mit vielen Biomen,
Riffen und Gräben, Dutzende Strukturen über und unter Wasser, eine Story aus Logbüchern und Orten, viele Deko-Blöcke,
Kreaturen überall, ein Floß, das wirklich segelt, Tauchausrüstung und ein Endboss, der erst nach der Story erreichbar
ist. Inspiriert von Raft-artigen Spielen, aber alle Orte, Namen und Kreaturen sind eigene.

**In Zahlen:** 12 Biome, 7 Story- und 12 Nebenstrukturen, 12 neue Kreaturen plus der überarbeitete Bruce, ein Boss mit
Helfern, das Expedition Raft und 4 Boote, Tauchausrüstung, 84 Bau- und 59 Deko-Blöcke, 22 natürliche Blöcke, 6 neue
Creative-Tabs (Building, Decoration, Nature, Voyage, Creatures, Tides of the Deep), das Handbuch Seafarer's Almanac und
neu gezeichnete Texturen für die 2.0-Blöcke und -Items.

### 3.1 Welt und Gelände
- **Archipel statt Oberwelt-Kopie:** Vorher nutzte die Dimension die Geländeform der Oberwelt mit Meeresspiegel 100 –
  dadurch ragten riesige Steinmassive aus dem „endlosen Meer“ (Design-Frage aus dem 2.0.1-Review). Jetzt eigene
  Dichte-Funktionen und Rauschen (`data/raft/worldgen/density_function/raftdim/*`, `noise/*`, `noise_settings/raftdim.json`).
- Meeresspiegel bleibt **100** (Wasser bis y 99), Welt von y −64, Höhe 384.

| Zone (Zielwerte der Spezifikation) | Boden-/Landhöhe | Anteil |
| --- | --- | --- |
| Abyssal Trench | y 0–15, steile Wände | ~10 % |
| Tiefe offene See | y 35–60 | ~35 % |
| Drowned Shelf | flach y 44–50 (Boden der versunkenen Stadt) | ~10 % |
| Kelp / mittlere See | y 55–75 | ~15 % |
| Flachwasser (Riff, Lagune) | y 82–96 | ~12 % |
| Inseln | Strand y 100–103, innen 104–135 | ~15 % |
| Vulkangipfel | bis y 170–190, Krater mit Lava | wenige % |

- Gemessen in der Offline-Vorschau (Modulbericht `world`): Graben 4,7 % statt ~10 % (das Graben-Biom selbst 7–8 %),
  mittlere See 9 % statt ~15 %; Inseln, Flachwasser, Shelf und Tiefsee nahe am Ziel.
- **Licht wie in der Oberwelt** (Entscheidung bei der Integration): `ambient_light` 0.0 und Farbe #0a0a0a statt 1.0/weiß.
  Die Sonne steht weiterhin fest (Mittag, sie geht nie unter), aber tiefes Wasser, Höhlen und Räume sind dunkel – so
  wirken die leuchtenden Meerespflanzen. Die Tiefsee-Nebelfarben sind ohne Rotanteil, weil Vanilla den Wasser-Nebel
  nach ein paar Sekunden aufhellt.
- **Keine fallenden Blöcke nach der Generierung:** Feature `raft:gravity_support` macht ungestützten Sand, Kies,
  Shell Sand, Black Sand und Vulkanasche stabil.
- Kraterlava bleibt aus Chunks mit oder neben der Ashen Forge heraus.
- Titanerz wird weiter generiert.
- **Bestehende Welten:** Schon erkundete Chunks behalten ihr altes Gelände (harte Kante zum neuen). Weiter hinausfahren
  oder neue Welt.

### 3.2 Die 12 Biome
Die Kreaturen-Gewichte stammen aus `content/world/WorldSpawns.java` (dort werden die 3.0-Kreaturen beim Laden
eingefügt, weil in 26.3 eine unbekannte Entity-ID in einer Biom-Datei das Laden der Welt stoppt). Vanilla-Mobs und Bruce
stehen in den Biom-JSONs.

| Biom (ID `raft:…`) | Wo | Besonderheiten | Kreaturen (Gewicht) |
| --- | --- | --- | --- |
| **Endless Sea** (`raft_ocean_biome`) | tiefe offene See | tiefblau; Kelp, Seegras, Röhrenkorallen, Blasenquellen | Bruce, Wal 1, Qualle 4, Hammerhai 1, Kabeljau, Tintenfisch, Delfin |
| **Kelp Forest** | mittlere See | sehr hoher Kelp, Glow Kelp, Seegras, Seepocken | Seeotter 4, Qualle 2, Muräne 1, Kabeljau, Lachs |
| **Coral Shallows** | warmes Flachwasser | Korallenriffe, Anemonen, Riesenmuscheln, Seesterne, Seeigel, Seeglas | Mantarochen 3, Muräne 2, Schildkröte, Tropenfische, Kugelfisch |
| **Glowing Lagoon** | seltenes Flachwasser | dunkler, voller leuchtendem Leben; Glow-Partikel | Qualle 6 (Leuchtquallen), Manta 1, Leuchttintenfisch |
| **Drowned Shelf** | flacher mittlerer Boden | trüb; Betonschutt; Boden von Port Solace | Muräne 2, Drowned Corsair 1, Ertrunkene, Kabeljau |
| **Abyssal Trench** | am tiefsten | fast schwarz; Röhrenwürmer, Blasenquellen, Basalt | Anglerfisch 4, Qualle 2, Leuchttintenfisch 3 |
| **Wreck Graveyard** | tiefe See, selten | neblig, voller Wracks | Drowned Corsair 3, Bruce 3, Ertrunkene |
| **Frost Floes** | kalte offene See | Eisberge, Eisschollen | Pinguin 6, Wal 1, Eisbär, Lachs |
| **Palm Isle** | Inseln | Sandstrände, Palmen, Muscheln, Seeglas, Treibholz | Krabbe 8, Möwe 6 |
| **Jungle Isle** | warme, feuchte Inseln | Dschungel, Bambus, Ananas, Melonen, Kakao | Möwe 2, Krabbe 3, Papagei, Ozelot |
| **Mangrove Isle** | niedrige, sumpfige Inseln | Mangroven, Schlamm, Seerosen | Krabbe 4, Frosch, (selten) Schleim |
| **Volcanic Isle** | seltene Inseln | schwarzer Sand, Asche, Basaltsäulen, Magma, Lava, Kraterlava | Ember Crab 5, Möwe 1 |

Damit Ertrunkene und Korsaren nicht in einer Minute das ganze Monster-Limit füllen, gibt es **Spawn-Kosten**:
Ertrunkene und Korsaren 0,7/0,12 überall, Ember Crabs im Vulkan-Biom, Wale (Frost Floes, Endless Sea) und Mantas
(Shallows, Lagune). Korsaren spawnen im offenen Wasser nur bei Dunkelheit; Obergrenzen nahe Strukturen: höchstens
6 Korsaren in 32, 5 Ember Crabs in 40, 4 Muränen in 24 Blöcken. Meeres-Monster hindern nicht mehr am Schlafen.

### 3.3 Natürliche Blöcke
22 natürliche Blöcke: Shell Sand, Black Sand, Volcanic Ash, Pumice, Beach Grass, Sea Oats, Hibiscus, Bird of Paradise,
Tropical Fern, Pineapple Bush, Glow Kelp, drei Sea Anemones (rot, lila, leuchtend), Giant Clam, drei Starfish, Sea
Urchin, Barnacles, Tube Worms und Bubble Vent – dazu Seashells und Sea Glass am Strand. Jeder Block mit Beschreibung
steht in Abschnitt 4.

---

### 3.4 ⚠️ SPOILER-WARNUNG: Die Story „Tides of the Deep“

> Dieser Abschnitt verrät die ganze Geschichte, alle Orte und das Ende. Wer selbst spielen will, springt zu 3.5.

**Die Vorgeschichte.** Vor langer Zeit hielten die **Tidewardens**, ein Seevolk, das Meer mit dem **Heart of the Tide**
ruhig, einem Kristall aus Ancient Energy (die Ancient Crystals und Broken Rings von 2.0 sind ihre Relikte). Tief im
Abgrund banden sie **den Leviathan**, eine riesige Seeschlange, hinter dem **Tide Seal**, verschlossen mit vier
**Tide Sigils** (Coral, Pearl, Storm, Ember). Jahrhunderte später fand die **Meridian Expedition** die Relikte, baute
Treibholz-Portale (so kommt der Spieler hierher) und gründete **Port Solace**, eine Stadt mit Kristall-Energie. Ihre
Chef-Wissenschaftlerin **Dr. Imara Voss** erforschte die Siegel in der **Helix Research Station** und bohrte in den
Abgrund. Das Siegel bekam Risse, der Leviathan erwachte, das Meer stieg und verschluckte Port Solace. Die Überlebenden
zerstreuten sich über Inseln und Flöße.

**Die Figuren** (Autoren der Logbücher): Kapitänin **Rhea Marlow** (Expeditionsleiterin, hinterlässt Notizen für den,
der durchs Portal kommt), **Tobias Fenn** (Leuchtturmwärter), **Nana Kalea** (Älteste des Pfahldorfs Saltmere),
**Dr. Imara Voss** (Wissenschaftlerin, von Schuld geplagt), **Bürgermeister Aldous Crane** (Port Solace) und der
Piratenkapitän **„Saltjaw“ Brannigan** (Nebengeschichte um seinen Schatz). Ton: abenteuerlich, etwas melancholisch,
hoffnungsvoll.

**Die Kapitel:**
| # | Kapitel | Ort (Struktur) | Was der Spieler findet | Führt zu |
| --- | --- | --- | --- | --- |
| 1 | The Castaway | Ankunftsplattform | Castaway-Truhe: Marlows erste Notiz, **Expedition Journal**, Karte zum Leuchtturm, Grundausrüstung | Old Lighthouse |
| 2 | Keeper of the Light | `old_lighthouse` | Fenns Logbuch, Karte nach Saltmere, Laternen-Vorräte | Saltmere |
| 3 | Saltmere | `saltmere_village` | Nana Kaleas Briefe, **Diving Helmet**, **Coral Sigil** (Dorfschrein), Karte zur Helix | Helix Station |
| 4 | Deep Science | `helix_station` | Voss' Forschungslogs (Terminals), **Pearl Sigil** (Labortresor), Sauerstofftank, Karte nach Port Solace | Port Solace |
| 5 | The Drowned City | `port_solace` | Cranes letzte Funkmeldung, **Storm Sigil** (Tresor oben im Rathausturm), Karte zur Schmiede | Ashen Forge |
| 6 | Through Fire | `ashen_forge` | Tafeln der Tidewardens, **Ember Sigil**, Karte zum Korallentempel | Coral Temple |
| 7 | The Tidewarden Key | `coral_temple` | Tidewarden-Altar: die 4 Sigils einsetzen → **Tidewarden Key**; Karte zum Sanktum | Abyssal Sanctum |
| 8 | The Leviathan | `abyssal_sanctum` | Schlüssel am **Tide Seal**, in die Kuppel, Leviathan wecken und besiegen | Epilog |
| – | Saltjaw's Gold (Nebenstory) | `pirate_cove`, `wreck_galleon` | Brannigans Logbuch, Piratenschatz, verfluchte Korsaren | – |

**Die Castaway-Truhe** (Loot `raft:chests/story/castaway`): Marlows Notiz (Buch), Expedition Journal, Karte, Brot,
gebratener Kabeljau, Fäden, Kokosnuss, Fresh Water, Paddel, Palmensetzling, Plastikhaken, Seil – und das Seafarer's
Almanac (über einen optionalen Tag-Eintrag). Sie erscheint nur auf **neu gebauten** Ankunftsplattformen (einmal pro
Plattform).

**Gating (harte Regel):** Der Boss ist erst nach der Story erreichbar. Hülle und Siegel des Sanktums sind unzerstörbar
und explosionsfest; das Siegel öffnet sich nur für den Tidewarden Key; den Schlüssel schmiedet nur ein Tidewarden-Altar
aus allen vier Sigils; jedes Sigil liegt nur im Tresor-Loot seines Story-Orts. Der Leviathan spawnt nur am
Leviathan-Altar im Sanktum (kein natürlicher Spawn, im Survival kein Spawn-Ei).

**Keine Sackgassen:** Jede Story-Truhe enthält eine Karte zum nächsten Ort. Das **Expedition Journal** zeigt immer das
aktuelle Ziel samt Hinweis (es liest den Fortschritt aus den `raft:story/*`-Advancements) und zeichnet auf See bei
Schleichen + Benutzen eine frische Karte zum nächsten Ort (alle 5 Minuten, auf dem Item angezeigt). Craftbar aus Buch,
Kompass und Papier – so kommen auch Spieler mit alten Plattformen in die Story.

**Hinweise in der Welt:** 8 Story-Bücher (Marlows Notiz, Fenns Logbuch, Kaleas Briefe, Voss' Journal, Cranes
Funkmeldung, die Schmiede-Tafel, die Prophezeiung der Tidewardens, Saltjaws Logbuch), 14 Briefe der Überlebenden in
**Flaschenposten**, 15 Logs auf **Research Terminals** (`helix_1`–`helix_6`, `solace_1`–`solace_4`, `rig_1`, `rig_2`,
`lab_misc_1`–`lab_misc_3`) und 16 Meldungen der **Expedition Radios**. Story-Items verschwinden nie, wenn man sie fallen
lässt.

### 3.5 Die Strukturen
Alle Strukturen sind Jigsaw-Strukturen (auch einteilige), gebaut mit Python-Vorlagen (`tools/content/structures_*`).
Abstand = `spacing`/`separation` in Chunks aus den `structure_set`-Dateien.

**Die 7 Story-Orte** (Spoiler-Hinweis wie oben):
| Ort | Modul | Biome | Abstand | Was dort ist |
| --- | --- | --- | --- | --- |
| **Old Lighthouse** | surface | Palm Isle, Jungle Isle | 22/8 | rot-weißer Leuchtturm (≥ 28 hoch) auf Felssockel, Wendeltreppe, Laternenraum mit Lighthouse Lens, Wärterhaus, Steg mit Bojen |
| **Saltmere** (Pfahldorf) | surface | Coral Shallows, Glowing Lagoon | 28/10 | verlassenes Fischerdorf auf Pfählen (Decks bei y 101), Platz, Hütten, Seilbrücken, Schrein; Ältesten-Hütte und Schrein-Truhe |
| **Helix Research Station** | deep | Coral Shallows, Glowing Lagoon, Kelp Forest | 28/10 | Forschungsbasis auf dem Meeresboden (57×17×54): Glaskuppeln, Tunnel, Luftschleuse, Labore mit Terminals, Aquarien, teils gefluteter Flügel mit Muränen, Tresor |
| **Port Solace** (versunkene Stadt) | city | Drowned Shelf | 36/14 | Straßenraster mit Asphalt und Laternen, Autowracks, Platz mit Statue, Hochhäuser (manche brechen durch die Oberfläche), Büros, Wohnungen, Läden, **Rathausturm** mit trockenem Tresor oben |
| **Ashen Forge** | surface | Volcanic Isle | 30/12 | Schmiedetempel der Tidewardens im Vulkanhang: Lavakanäle, riesige Esse, Runen, Tresor hinter einer Brücke über Lava, Ember Crabs |
| **Coral Temple** | deep | Coral Shallows, Glowing Lagoon | 32/12 | überwucherter, gefluteter Tempel (41×23×48): Hof, Säulengänge, Statuen, Allerheiligstes mit Tidewarden-Altar und vier Sockeln |
| **Abyssal Sanctum** | deep | Abyssal Trench, Endless Sea | 40/16 | Boss-Arena (63×34×102): 5×5-Siegeltür, unzerstörbare Hülle, Luftkuppel (Radius ~22) mit Ring, Säulen, Becken (Radius 7, ≥ 10 tief), Leviathan-Altar, Belohnungsraum |

**Die 12 Nebenorte** (`structures_side`):
| Ort | Biome | Abstand | Was dort ist |
| --- | --- | --- | --- |
| Galleon Wreck (`wreck_galleon`) | Wreck Graveyard, Endless Sea | 26/9 | große Piraten-Galeone (2 Varianten) schräg am Boden, Masten, Kanonen, Kajüte und Laderaum, Korsaren; manchmal Saltjaws Schatzkarte |
| Cargo Ship Wreck | Wreck Graveyard, Endless Sea, Kelp Forest | 24/8 | rostiger Frachter, in zwei Teile gebrochen, verstreute Container, Brücke mit Control Panel |
| Fishing Boat Wreck | alle tiefen und flachen Meer-Biome | 12/4 | kleine Fischerboot-Wracks (3 Varianten) mit Netzen und Kisten |
| **Pirate Cove** | Jungle Isle, Palm Isle | 34/12 | Saltjaws Versteck in einem eigenen Felshügel: Meereingang, Steg mit Schiff, Schatzraum mit Münzhaufen, Kapitänsquartier, Steckbrief, Korsaren |
| Rusted Rig | Endless Sea, Frost Floes | 30/10 | verlassene Plattform auf Stahlbeinen (Deck y 108–112): Kräne, Container, Helipad, Quartiere, Funkmast mit Radio, Terminals, Windturbine |
| Sunken Plane | Kelp Forest, Endless Sea, Coral Shallows | 28/10 | abgestürztes Flugzeug am Boden (Verkehrsflugzeug und Wasserflugzeug) |
| Sunken Ruins | Coral Shallows, Kelp Forest, Endless Sea, Glowing Lagoon | 10/3 | kleine Tidewarden-Ruinen (5 Varianten): Säulen, Bögen, Statuenkopf, Schrein |
| Castaway Camp | Palm Isle | 16/6 | winziges Lager (3 Varianten): Unterstand, Lagerfeuer, SOS aus Steinen im Sand |
| Abandoned Raft | Endless Sea, Kelp Forest, Coral Shallows | 12/4 | treibendes Floß (Deck y 99, 3 Varianten) mit Segel, Truhe, Pflanzbeet |
| Iceberg Outpost | Frost Floes | 24/8 | Forschungshütte auf einer Eisscholle mit Terminal (`lab_misc_2`) |
| Beach Shack | Palm Isle, Jungle Isle | 18/6 | Strandbar (2 Varianten) mit Liegestühlen, Schirmen, Tiki-Fackeln, Lichterketten |
| Buoy Field | Coral Shallows, Endless Sea | 14/5 | 3–6 Bojen und eine angekettete Vorratskiste (2 Varianten) |

Dazu aus 2.0 die treibenden **Treibholz-Strukturen** (`driftwood`, `driftwoodtwo`) an Stränden und in der Endless Sea –
das Ziel des Receivers. Jede Truhe hat eine eigene Loot-Tabelle (Spezifikation 9.3), z. B. `raft:chests/wreck_galleon`
oder `raft:chests/sunken_plane`; Bojenfelder nutzen die Vorratsfass-Tabelle.

### 3.6 Die Kreaturen
| Kreatur | Leben | Wo | Verhalten | Drops |
| --- | --- | --- | --- | --- |
| **Bruce the Shark** (2.0, überarbeitet) | 26 | Meer | jagt Schwimmer (5 Schaden); kreist um Flöße mit Spielern und beißt Randfundamente; neues Modell, Textur und Schwimmanimation | rohes Haifleisch, Haizähne |
| **Hammerhead Shark** | 40 | tiefe See (6–50 unter der Oberfläche) | stärkerer Hai (7 Schaden), jagt Schwimmer, beißt Flöße | Haizähne, Haifleisch |
| **Whale** | 120 | tief, 5–25 unter der Oberfläche | riesig und friedlich; taucht alle ein, zwei Minuten auf und bläst, singt (eigene Klänge) | nichts – „ein Freund“ |
| **Manta Ray** | 20 | Flachwasser | gleitet in Schleifen, springt manchmal | evtl. Leder |
| **Jellyfish** (Moon, Crimson, Glow) | 6 | fast überall im Wasser | treibt und pulsiert; Berührung = Vergiftung 3 s, außer mit Wetsuit | Jelly Blob bzw. Glow Jelly |
| **Anglerfish** | 18 | Abyssal Trench (45+ unter der Oberfläche) | lauert mit Leuchtköder, schießt vor und beißt (5) | Angler Lure, manchmal Kabeljau |
| **Moray Eel** | 16 | Löcher in Riffen und Ruinen | schnellt auf Spieler in 4 Blöcken zu (4 Schaden), zieht sich zurück | Eel Fillet |
| **Crab** (rot, blau, sand) | 8 | Inselstrände | läuft seitwärts, gräbt sich ein, wenn man heransprintet, kneift zurück (2); vermehrt sich mit Kelp | Crab Claw, selten Muschel |
| **Ember Crab** | 14 | Vulkaninseln | feindlich aus der Nähe, setzt dich in Brand (4 Schaden), feuerfest | Crab Claw, Ember Shell |
| **Seagull** | 6 | Inseln und Flöße | fliegt in Schwärmen, pickt Pflanzen (eine Stufe zurück) ohne Vogelscheuche in 16 Blöcken, klaut Essen vom Boden | Federn |
| **Penguin** | 10 | Frost Floes | watschelt, rutscht auf dem Bauch, taucht; mit Kabeljau Küken | Federn |
| **Sea Otter** | 10 | Kelp Forest | treibt auf dem Rücken, knackt Muscheln; für eine Muschel folgt er dir und bringt Perlen oder Muscheln | – |
| **Drowned Corsair** | 24 | Wrack-Friedhof, Galeonen, Piratenbucht | verfluchter untoter Pirat aus Saltjaws Crew: schwimmt, brennt nicht in der Sonne, Entermesser, klettert auf Flöße | Goldmünzen, Knochen, manchmal Cutlass |

Leben in Lebenspunkten (2 = ein Herz), aus den Attributen im Code. Alle Meereswesen stehen im Tag `raft:sea_creatures`
und in `#minecraft:aquatic` (Bonus von „Impaling“).

### 3.7 ⚠️ SPOILER-WARNUNG: Der Boss – der Leviathan

> Auch das Almanac zeigt dieses Kapitel erst nach einer Warnung (und öffnet es von selbst nach dem Sieg).

- **Werte:** riesige Seeschlange mit **600 Leben** und Rüstung 10, rückstoßfest, immun gegen Ertrinken, Feuer und
  Fallschaden, Bossleiste. Nur der Kopf (Hitbox ~3,0×2,5) nimmt Schaden, der ~14 Blöcke lange Körper ist Optik.
- **Wecken:** Tidewarden Key am **Leviathan-Altar** am Beckenrand benutzen; gekämpft wird auf dem Steinring.
- **Kampfphasen:**
  - **Kreisen** tief im Becken – dabei unverwundbar.
  - **Aufsteigen und spucken:** Brine Bolts, je 5 Schaden plus Langsamkeit.
  - **Sprung:** springt über den Ring und schlägt auf (8 Schaden im Umkreis), liegt dann **4 Sekunden gestrandet** und
    nimmt **50 % mehr Schaden** – der Moment zum Zuschlagen.
  - **Unter halbem Leben:** Brüllen stößt zurück und ruft **Tidelings** (10 Leben, 3 Schaden, hüpfen 10 s an Land,
    dann zappeln sie hilflos; höchstens 5 gleichzeitig), und ein **Strudel** zieht Spieler zum Becken.
  - **Unter einem Viertel:** schneller, Angriffe folgen aufeinander.
- **Regeln:** verschwindet nie, verlässt das Sanktum nicht, heilt sich ganz, wenn 30 s kein Spieler (außer Kreativ)
  in 24 Blöcken ist; nur Tod (oder Friedlich) entfernt ihn.
- **Belohnung:** **Heart of the Tide** (Block: Conduit Power und Gunst des Delfins für Schwimmer in 32 Blöcken;
  in Dreamcraft Zutat des Dream Star), Leviathan Scales, Leviathan Trophy, 500 Erfahrung, Advancement „Calm Seas“.
  Aus 4 Schuppen, einem Titanbarren und einem Dreizack entsteht der **Tidebreaker** (9 Schaden, +50 % gegen
  Meereswesen, Sprint im Wasser oder Regen).
- **Nochmal kämpfen:** Schlüssel und ein Ancient Crystal am Altar – so kommen auch Freunde dran.

### 3.8 Das Expedition Raft und die Boote
- **Rezept:** 6 Raft Foundations, 2 Seil, 1 Paddel.
- Großes **3×3-Floß** mit **vier Sitzen** und **27 Lagerplätzen**; Schleichen + Benutzen öffnet das Lager. Wer zuerst
  einsteigt, sitzt am Steuer.
- **Sinkt nie, kippt nie, Haie können ihm nichts**; Wellen und Regen werfen niemanden ab, Wasser läuft nicht hinein.
  Freunde, die auf dem Deck stehen, fahren mit.
- **Aufheben:** 3 Treffer in 2 Sekunden oder einmal schleichend. Es droppt als Item **mit seinen Upgrades**
  (Item-Komponente `raft:raft_upgrades`), die Ladung fällt daneben.
- **Upgrades** (Item auf das Floß benutzen, jedes ist sichtbar):

| Upgrade | Wirkung | Rezept |
| --- | --- | --- |
| Raft Sail | 50 % schneller geradeaus | 2 Seil, 2 Sail Canvas, 2 Palmenstämme |
| Raft Engine | mehr als doppelt so schnell, verbrennt Ofen-Brennstoff aus dem Slot im Floß-Menü | 2 Schrott, Circuit Board, 3 Titanbarren, Ofen |
| Raft Anchor | mit dem Hebel im Floß-Menü setzen – das Floß bleibt stehen | Seil, 4 Eisen |
| Raft Cargo Crate | 27 weitere Lagerplätze | Truhe, Seil, 6 Bretter |
| Raft Lanterns | Laternenpfosten und Seilgeländer | 2 Laternen, Seil, 4 Stöcke |

- Ohne Upgrades ist das Floß etwas langsamer als ein Boot, mit Segel und Motor mehr als doppelt so schnell.
- **Die vier Boote:** Palm Boat und Palm Boat with Chest (wie Vanilla-Boote), Driftwood Raft und Driftwood Raft with
  Chest (wie das Bambusfloß). Das Paddel gibt im Boot einen Schub.

### 3.9 Tauchausrüstung
| Teil | Slot | Wirkung |
| --- | --- | --- |
| Diving Helmet | Kopf | viel weitere Sicht unter Wasser; mit Tank atmet man aus dem Tank |
| Helmlampe | (Helm + Angler Lure) | unter Wasser Nachtsicht im dunklen Tiefsee und Graben (13 s, bei 11 s aufgefrischt, endet beim Auftauchen); Schaden und Verzauberungen des Helms bleiben |
| Oxygen Tank | Brust | 2 Minuten Luft (2 400 Ticks), Balken am Item und Anzeige unter Wasser |
| Titanium Oxygen Tank | Brust | 6 Minuten Luft (7 200 Ticks), Schutz wie ein Eisenbrustpanzer |
| Wetsuit | Beine | unter Wasser dreimal so schnell abbauen; Quallen stechen nicht |
| Flippers | Füße | viel schneller schwimmen; an Land 25 % langsamer |
| **Volles Set** | – | Gunst des Delfins beim Schwimmen |

- Ein Tank wirkt nur zusammen mit dem Helm. Er füllt sich, wenn der Kopf über Wasser ist oder in einer
  Blasensäule – ein normaler Tank ist in 3 Sekunden voll. Blasensäulen machen Bubble Vents und Seelensand.
- **Air Compressor:** Tank in den Slot, füllt mit FE von einem Nachbarn (Kabel, Batterie, Solarpanel, Windturbine);
  ohne Strom schleichend mit leerer Hand benutzen oder die Kurbel im Menü drücken – jede Drehung gibt 5 Sekunden Luft
  (bzw. 40 FE). Lädt auch den Sea Scooter. Neue Tanks kommen voll, neue Scooter geladen.
- **Harpoon Gun:** 8 Schaden unter Wasser, 4 in der Luft, ein Schuss pro Sekunde; Harpunen wieder aufsammeln.
- **Sea Scooter:** Benutzen halten zieht dich in Blickrichtung; Akku 3 000 FE, etwa 75 Sekunden Fahrt.

### 3.10 Der Seafarer's Almanac
Das Handbuch im Spiel, gestaltet als wasserfestes, geöltes Lederbuch (Vorbild: das Tamacon von Tamagotchi). Man bekommt
es beim **ersten Betreten der Endless Sea** (gemerkt über das Spieler-Attachment `raft:almanac_given`) und in der
Castaway-Truhe; nachbauen aus Buch + Kelp, getrocknetem Kelp, Treibholz-Stamm oder -Brettern. Quests können es auf einer
bestimmten Seite öffnen (Item-Daten `{almanac:"<kapitel>"}`), Dreamcraft nutzt das.

**14 Kapitel:** Welcome Aboard · The Portal · Raft Survival · Building · Technology · Sailing · Diving · The Sea's
Biomes · Islands & Wrecks · Creatures (eine Seite pro Kreatur mit gerendertem Porträt) · The Story (spoilerfrei: wie
Journal und Karten führen) · The Leviathan (mit Spoiler-Warnung, nach dem Sieg offen) · Titanium & Tools · Tips.
Bedienung: Kapitel anklicken, Seiten mit den Pfeilen, Pfeiltasten oder Mausrad, rotes Lesezeichen zurück zum Inhalt,
Mauszeiger über Bilder zeigt Namen, das Buch merkt sich die letzte Seite. Alle Texte wurden gegen Code, Rezepte und
Loot geprüft.

### 3.11 Die Advancements (zwei neue Tabs)
**Tides of the Deep** (Story): Tides of the Deep (durch ein Treibholz-Portal ankommen) → The Castaway (Journal finden) →
Keeper of the Light → Saltmere → The Coral Sigil → Deep Science → The Pearl Sigil → The Drowned City → The Storm Sigil
→ Through Fire → The Ember Sigil → The Coral Temple → The Tidewarden Key → The Abyssal Sanctum → **Calm Seas** (den
Leviathan besiegen).

**Endless Sea Adventures:** Set Sail (ans Steuer eines Expedition Raft), Deep Breath (Helm und Tank tragen), Shark Bait
(von einem Hai gebissen werden), Whale Watcher (Wal durchs Fernrohr ansehen), Pieces of Eight (eine Piraten-Goldmünze),
Crab Dinner (gebratene Krabbenschere essen), Rusted Giant (auf die Bohrinsel klettern), Ghost Ship (Galeonenwrack
erkunden), Saltjaw's Gold (die Piratenbucht finden). Geplant, aber weggelassen: `adventure/full_upgrade` (bräuchte
interne Daten des Floß-Moduls).

---

## 4. Jeder Block und jedes Item

Erzeugt aus den Sprachdateien aller Module (`src/main/modules/*/assets/raft/lang/en_us.json`) und der 2.0-Sprachdatei
(`src/main/resources/assets/raft/lang/en_us.json`); ein Skript prüft, dass **jede der 343 Block- und Item-IDs genau
einmal** vorkommt. Namen wie im Spiel (Englisch), Beschreibung auf Deutsch. „Technischer Block“ = ohne eigenes Item
(z. B. Topfpflanzen oder der Portal-Block). Entities ohne Item (Seat, Cannonball-Geschoss, Harpune im Flug, Brine Bolt)
sind nicht aufgeführt.

#### Baublöcke (Modul `building`, Tab „Beach Craft: Building“) – 84 Blöcke

| Im Spiel | ID (`raft:…`) | Beschreibung |
| --- | --- | --- |
| Weathered Planks, Weathered Stairs, Weathered Slab, Weathered Fence, Weathered Fence Gate, Weathered Door, Weathered Hatch | `weathered_planks`, `weathered_stairs`, `weathered_slab`, `weathered_fence`, `weathered_fence_gate`, `weathered_door`, `weathered_trapdoor` | Graues, sonnengebleichtes Holz für Stege, Hütten und Wracks: 4 Treibholz- oder Palmenbretter um Knochenmehl. Mit Treppe, Stufe, Zaun, Tor, Tür und Luke. |
| Teak Planks, Teak Stairs, Teak Slab, Teak Fence, Teak Fence Gate, Teak Door, Teak Hatch Grating | `teak_planks`, `teak_stairs`, `teak_slab`, `teak_fence`, `teak_fence_gate`, `teak_door`, `teak_trapdoor` | Dunkles, edles Schiffsholz (Piratenschiffe, Kapitänskajüten) aus Schwarzeichen- und Palmenbrettern. Mit Treppe, Stufe, Zaun, Tor, Tür und Gitterluke. |
| Aqua Sea Glass, Aqua Sea Glass Pane, Green Sea Glass, Green Sea Glass Pane, Blue Sea Glass, Blue Sea Glass Pane | `aqua_sea_glass`, `aqua_sea_glass_pane`, `green_sea_glass`, `green_sea_glass_pane`, `blue_sea_glass`, `blue_sea_glass_pane` | Mattes, durchscheinendes Seeglas: 4 Sea Glass Shards ergeben Aqua Sea Glass, mit grüner oder blauer Farbe die anderen Farben; jeweils auch als Scheibe. |
| Coral Stone, Coral Stone Stairs, Coral Stone Slab, Coral Stone Wall, Polished Coral Stone, Polished Coral Stone Stairs, Polished Coral Stone Slab, Coral Stone Bricks, Coral Stone Brick Stairs, Coral Stone Brick Slab, Coral Stone Brick Wall, Mossy Coral Stone Bricks, Mossy Coral Stone Brick Stairs, Mossy Coral Stone Brick Slab, Mossy Coral Stone Brick Wall | `coral_stone`, `coral_stone_stairs`, `coral_stone_slab`, `coral_stone_wall`, `polished_coral_stone`, `polished_coral_stone_stairs`, `polished_coral_stone_slab`, `coral_stone_bricks`, `coral_stone_brick_stairs`, `coral_stone_brick_slab`, `coral_stone_brick_wall`, `mossy_coral_stone_bricks`, `mossy_coral_stone_brick_stairs`, `mossy_coral_stone_brick_slab`, `mossy_coral_stone_brick_wall` | Rosa-beiger Kalkstein mit Korallen-Fossilien (Riff-Ruinen, Dörfer) aus Stein und Korallenblöcken: roh, poliert, als Ziegel und bemooste Ziegel, mit Treppen, Stufen und Mauern. Die meisten Varianten gehen im Steinschneider. |
| Tidestone, Tidestone Stairs, Tidestone Slab, Tidestone Wall, Tidestone Bricks, Tidestone Brick Stairs, Tidestone Brick Slab, Tidestone Brick Wall, Cracked Tidestone Bricks, Mossy Tidestone Bricks, Mossy Tidestone Brick Stairs, Mossy Tidestone Brick Slab, Mossy Tidestone Brick Wall, Chiseled Tidestone, Tidestone Pillar | `tidestone`, `tidestone_stairs`, `tidestone_slab`, `tidestone_wall`, `tidestone_bricks`, `tidestone_brick_stairs`, `tidestone_brick_slab`, `tidestone_brick_wall`, `cracked_tidestone_bricks`, `mossy_tidestone_bricks`, `mossy_tidestone_brick_stairs`, `mossy_tidestone_brick_slab`, `mossy_tidestone_brick_wall`, `chiseled_tidestone`, `tidestone_pillar` | Türkiser Stein der Tidewardens (Tempel, Sanktum, Ruinen) aus Stein und Prismarinscherben: roh, als Ziegel, rissig, bemoost, gemeißelt und als Säule. |
| Glowing Tidestone | `glowing_tidestone` | Tidestone mit leuchtenden cyanen Runen (animiert), Lichtstufe 10; mit Glowstone-Staub hergestellt. |
| Cracked Concrete, Cracked Concrete Stairs, Cracked Concrete Slab, Cracked Concrete Wall, Mossy Concrete, Rebar Concrete | `cracked_concrete`, `cracked_concrete_stairs`, `cracked_concrete_slab`, `cracked_concrete_wall`, `mossy_concrete`, `rebar_concrete` | Beton der versunkenen Stadt: rissig, bemoost oder mit herausstehendem Bewehrungsstahl (Beton + Kies, Rebar zusätzlich mit Eisennuggets). |
| Asphalt, Asphalt Stairs, Asphalt Slab, Asphalt Lane Line | `asphalt`, `asphalt_stairs`, `asphalt_slab`, `asphalt_line` | Straßenbelag aus Kies, Kohle und Sand; die Lane Line trägt eine weiße Fahrbahnlinie entlang ihrer Achse. |
| Cracked Glass, Cracked Glass Pane | `cracked_glass`, `cracked_glass_pane` | Zersprungene Bürofenster (Glas + Kies), auch als Scheibe. |
| Riveted Hull, Rusty Hull | `riveted_hull`, `rusty_hull` | Stahl-Rumpfplatten von Schiffen: dunkelblau mit Nieten bzw. verrostet (Eisen + Schrott). |
| Corrugated Metal, Corrugated Metal Stairs, Corrugated Metal Slab | `corrugated_metal`, `corrugated_metal_stairs`, `corrugated_metal_slab` | Welliges verzinktes Blech für Hütten und Bohrinseln. |
| Rusted Plate | `rusted_plate` | Rostige Stahl-Bodenplatte (aus Schrott). |
| Steel Beam | `steel_beam` | Echter Doppel-T-Träger aus Eisenbarren, in jede Richtung drehbar, kann unter Wasser stehen. |
| Catwalk | `catwalk` | Durchsichtiger Stahl-Gitterrost als Stufe (Eisengitter + Schrott). |
| Steel Railing | `steel_railing` | Dünnes Stahlgeländer, verbindet sich wie eine Glasscheibe. |
| Porthole | `porthole` | Vollblock mit Stahlrahmen und rundem Glasfenster (Bullauge). |
| Bulkhead Door | `bulkhead_door` | Stahltür mit Bullauge – öffnet per Hand wie eine Holztür. |
| Metal Hatch | `metal_hatch` | Stahl-Falltür, öffnet per Hand. |
| Rusty Pipe, Rusty Pipe Valve | `rusty_pipe`, `rusty_pipe_valve` | Rostiges Rohr und Rohr mit rotem Handrad („Turn the wheel to let off some steam.“). |
| Red Shipping Container, Blue Shipping Container, Green Shipping Container | `shipping_container_red`, `shipping_container_blue`, `shipping_container_green` | Gerippte Container-Wände in drei Farben (Eisen + Farbe); die lange Seite liegt entlang der Achse. |
| Control Panel | `control_panel` | Expeditions-Konsole mit blinkenden Lichtern, Deko, Lichtstufe 4. |
| Server Rack | `server_rack` | Brummendes Computer-Rack, Deko, Lichtstufe 3. |
| Satellite Dish | `satellite_dish` | Satellitenschüssel, Deko. |
| Wind Turbine | `wind_turbine` | **Funktioniert:** 20 FE pro Tick, wenn die 3×3-Fläche vor dem Rotor frei ist und der Block über y 90 steht; gibt die Energie an Kabel, Batterien und Maschinen daneben ab. |

#### Dekoration (Modul `decor`, Tab „Beach Craft: Decoration“) – 59 Blöcke und 2 Items

| Im Spiel | ID (`raft:…`) | Beschreibung |
| --- | --- | --- |
| Warm String Lights, Colorful String Lights | `string_lights_warm`, `string_lights_colorful` | Lichterketten entlang einer Wand, warm oder bunt, Lichtstufe 12. |
| Red and White Bunting, Rainbow Bunting | `bunting_red_white`, `bunting_rainbow` | Wimpelgirlanden an der Wand. |
| White Paper Lantern, Red Paper Lantern, Orange Paper Lantern, Yellow Paper Lantern, Lime Paper Lantern, Cyan Paper Lantern, Blue Paper Lantern, Purple Paper Lantern, Pink Paper Lantern | `paper_lantern_white`, `paper_lantern_red`, `paper_lantern_orange`, `paper_lantern_yellow`, `paper_lantern_lime`, `paper_lantern_cyan`, `paper_lantern_blue`, `paper_lantern_purple`, `paper_lantern_pink` | Runde Papierlaternen in neun Farben, stehend oder hängend, Lichtstufe 14. |
| Ship Lantern | `ship_lantern` | Laterne aus Messing und Glas, Lichtstufe 15. |
| Tiki Torch | `tiki_torch` | Zwei Blöcke hohe Bambusfackel mit Flammen (Lichtstufe 14, wenn sie brennt); mit Feuerzeug anzünden, mit der Schaufel löschen. |
| Jelly Lamp | `jelly_lamp` | Glas mit leuchtendem Gelee, animiert, Lichtstufe 15. |
| Brazier | `brazier` | Eiserne Feuerschale, brennend Lichtstufe 15, verletzt wie ein Lagerfeuer; anzünden mit Feuerzeug, löschen mit Schaufel oder Wasser. |
| Red Buoy, Green Buoy | `buoy_red`, `buoy_green` | Schwimmende Fahrwasser-Bojen mit blinkender Spitze (Lichtstufe 10); direkt auf die Wasseroberfläche setzen. |
| Lighthouse Lens | `lighthouse_lens` | Große Fresnel-Linse des Leuchtturms, leuchtet mit Lichtstufe 15. |
| Cyan Neon Tube, Pink Neon Tube | `neon_tube_cyan`, `neon_tube_pink` | Dünne Leuchtröhren in Cyan und Pink, Lichtstufe 12. |
| Driftwood Lamp | `driftwood_lamp` | Stehlampe aus Treibholz und Segeltuch, Lichtstufe 13. |
| Seashell Lamp | `seashell_lamp` | Lampe aus Muscheln, Lichtstufe 12. |
| Ship Cannon | `ship_cannon` | Deckkanone: mit einer Cannonball benutzen – die Kugel fliegt rund 40 Blöcke, macht 8 Schaden und zerstört keine Blöcke. |
| Ship Anchor | `ship_anchor` | Großer Deko-Anker für Wand oder Boden. |
| Treasure Chest | `treasure_chest` | Eisenbeschlagene Schatztruhe mit 27 Slots, der Deckel öffnet sich. |
| Gold Coin Pile | `gold_coin_pile` | Goldmünzen-Haufen, stapelbar in Schichten wie Schnee (9 Gold Coins pro Schicht); bricht, wenn der Block darunter fehlt. |
| Jolly Roger | `jolly_roger` | Piratenflagge an der Wand. |
| Wanted Poster | `wanted_poster` | Steckbrief „WANTED: Saltjaw“ an der Wand. |
| Rum Bottles | `rum_bottles` | 1 bis 3 Rumflaschen. |
| Rope Railing | `rope_railing` | Seilgeländer wie ein Zaun; verbindet sich auch mit Holzzäunen und hält Leinen. |
| Cargo Net | `cargo_net` | Frachtnetz an der Wand, kletterbar wie eine Leiter. |
| Powder Keg | `powder_keg` | Pulverfass – nur Deko, explodiert nicht. |
| Wooden Crate | `wooden_crate` | Holzkiste mit 27 Slots. |
| Ship Bell | `ship_bell` | Schiffsglocke an einer Wandhalterung, läutet bei Rechtsklick. |
| Chart Table | `chart_table` | Tisch mit Seekarte. |
| Spyglass Stand | `spyglass_stand` | Fernrohr auf einem Dreibein. |
| Mermaid Figurehead | `figurehead` | Geschnitzte Meerjungfrau-Galionsfigur für die Wand. |
| Life Ring | `life_ring` | Rot-weißer Rettungsring an der Wand. |
| Hammock | `hammock` | Zwei Blöcke lange Hängematte – ein echtes Bett: tagsüber ausruhen, nachts schlafen, setzt den Spawnpunkt. |
| Deck Chair | `deck_chair` | Gestreifter Liegestuhl, Rechtsklick zum Sitzen. |
| Red Beach Umbrella, Blue Beach Umbrella, Yellow Beach Umbrella | `beach_umbrella_red`, `beach_umbrella_blue`, `beach_umbrella_yellow` | Zwei Blöcke hohe Sonnenschirme in drei Farben. |
| White Cushion, Red Cushion, Blue Cushion, Yellow Cushion, Green Cushion | `cushion_white`, `cushion_red`, `cushion_blue`, `cushion_yellow`, `cushion_green` | Sitzkissen in fünf Farben, Rechtsklick zum Sitzen. |
| Woven Rug | `woven_rug` | Geflochtener Teppich. |
| Driftwood Table, Palm Table | `driftwood_table`, `palm_table` | Tische aus Treibholz bzw. Palmenholz. |
| Driftwood Chair, Palm Chair | `driftwood_chair`, `palm_chair` | Stühle aus Treibholz bzw. Palmenholz, Rechtsklick zum Sitzen. |
| Driftwood Shelf | `driftwood_shelf` | Wandregal aus Treibholz mit Gläsern. |
| Wind Chime | `wind_chime` | Hängendes Muschel-Windspiel, klingt ab und zu leise. |
| Aquarium | `aquarium` | Glasbecken mit Fischen, animiert, Lichtstufe 6. |
| Hanging Planter | `hanging_planter` | Hängekorb mit Blumen. |
| Cannonball | `cannonball` | Item: Kanonenkugel für die Ship Cannon; ein Eisenbarren und Schießpulver ergeben 4. |
| Gold Coin | `gold_coin` | Item: Goldmünze aus Beute (z. B. von Drowned Corsairs); 9 ergeben eine Schicht Münzhaufen. |

#### Natur (Modul `world`, Tab „Beach Craft: Nature“) – 22 natürliche Blöcke, 7 technische Blöcke und 6 Items

| Im Spiel | ID (`raft:…`) | Beschreibung |
| --- | --- | --- |
| Shell Sand | `shell_sand` | Sand mit Muscheln, fällt wie Sand (Schaufel); auch aus Muscheln herstellbar. |
| Black Sand | `black_sand` | Schwarzer Vulkansand; schmilzt zu getöntem Glas. |
| Volcanic Ash | `volcanic_ash` | Weiche graue Vulkanasche, fällt wie Sand. |
| Pumice | `pumice` | Leichter, poröser Bimsstein (Spitzhacke). |
| Beach Grass | `beach_grass` | Kurzes Strandgras auf Sand (nur mit der Schere). |
| Sea Oats | `sea_oats` | Zwei Blöcke hoher Strandhafer (Schere). |
| Hibiscus, Potted Hibiscus | `hibiscus`, `potted_hibiscus` | Rote Hibiskusblüte, ergibt rote Farbe; auch im Blumentopf. |
| Bird of Paradise | `bird_of_paradise` | Zwei Blöcke hohe Paradiesvogelblume, ergibt orange Farbe. |
| Tropical Fern, Potted Tropical Fern | `tropical_fern`, `potted_tropical_fern` | Tropischer Farn der Dschungel- und Mangroveninseln (Schere); auch im Blumentopf. |
| Potted Palm Sapling | `potted_palm_sapling` | Palmensetzling im Blumentopf. |
| Pineapple Bush | `pineapple_bush` | Wilder Ananasbusch: Wenn die Frucht golden ist, per Rechtsklick ernten; er trägt wieder. |
| Pineapples | `pineapple_crop` | Ananas-Feldfrucht (technischer Block): aus der Pineapple Crown auf Ackerland oder einem Crop Plot; gibt Ananas und eine neue Krone. |
| Glow Kelp, Glow Kelp Plant | `glow_kelp`, `glow_kelp_plant` | Leuchtender Seetang (Lichtstufe 8), wächst wie Kelp; Glow Kelp Plant ist der Stängel-Block. |
| Red Sea Anemone, Purple Sea Anemone, Glowing Sea Anemone | `sea_anemone_red`, `sea_anemone_purple`, `sea_anemone_glow` | Seeanemonen unter Wasser (Schere); die leuchtende gibt Lichtstufe 10. |
| Giant Clam | `giant_clam` | Riesenmuschel, öffnet und schließt sich; eine offene Muschel mit Perle per Rechtsklick ernten, eine neue Perle wächst mit der Zeit. |
| Orange Starfish, Purple Starfish, Red Starfish | `starfish_orange`, `starfish_purple`, `starfish_red` | Seesterne für Boden, Wand und Decke. |
| Sea Urchin | `sea_urchin` | Stacheliger Seeigel: Berührung tut weh; droppt Urchin Spines. |
| Barnacles | `barnacles` | Seepocken als dünne Schicht auf Stein, Holz und Metall (Schere oder Behutsamkeit). |
| Tube Worms | `tube_worms` | Röhrenwürmer im Graben, Lichtstufe 6 (Schere). |
| Bubble Vent | `bubble_vent` | Blasenquelle: erzeugt eine Blasensäule nach oben, in der Taucher Luft holen; 4 Basalt um Seelensand. |
| Seashells | `seashells` | Technischer Block: 1 bis 4 Muscheln auf dem Sand, gesetzt mit dem Seashell-Item. |
| Sea Glass | `sea_glass_scatter` | Technischer Block „Sea Glass“: 1 bis 3 Seeglas-Kiesel auf dem Sand, gesetzt mit dem Sea Glass Shard. |
| Pearl | `pearl` | Item: Perle aus der Riesenmuschel (Seeotter bringen auch welche). |
| Pineapple | `pineapple` | Item: Ananas zum Essen. |
| Pineapple Crown | `pineapple_crown` | Item: Ananas-Krone zum Pflanzen auf Ackerland oder Crop Plot. |
| Seashell | `seashell` | Item: Muschel – wird zu Knochenmehl oder Shell Sand; Seeotter folgen dir dafür. |
| Sea Glass Shard | `sea_glass_shard` | Item: Seeglas-Scherbe; 4 ergeben Aqua Sea Glass. |
| Urchin Spine | `urchin_spine` | Item: Seeigel-Stachel; mit Stock und Faden 2 Harpunen. |

#### Boote und Floß (Modul `voyage`, Tab „Beach Craft: Voyage“)

| Im Spiel | ID (`raft:…`) | Beschreibung |
| --- | --- | --- |
| Palm Boat, Palm Boat with Chest | `palm_boat`, `palm_chest_boat` | Boot aus Palmenholz, auch mit Truhe – wie ein Vanilla-Boot. |
| Driftwood Raft, Driftwood Raft with Chest | `driftwood_raft`, `driftwood_chest_raft` | Floß aus Treibholz (wie das Bambusfloß), auch mit Truhe. |
| Expedition Raft | `expedition_raft` | Das große 3×3-Floß mit vier Sitzen und 27 Lagerplätzen; Details in Abschnitt 3.7. |
| Raft Sail | `raft_sail` | Upgrade Mast und Segel: 50 % schneller geradeaus (2 Seil, 2 Sail Canvas, 2 Palmenstämme). |
| Raft Engine | `raft_engine` | Upgrade Außenbordmotor: mehr als doppelt so schnell, verbrennt Ofen-Brennstoff aus dem Brennstoff-Slot (2 Schrott, Circuit Board, 3 Titanbarren, Ofen). |
| Raft Anchor | `raft_anchor` | Upgrade Anker: mit dem Hebel im Floß-Menü setzen, das Floß bleibt stehen (Seil + 4 Eisen). |
| Raft Cargo Crate | `raft_crate` | Upgrade Frachtkiste: 27 weitere Lagerplätze (Truhe, Seil, 6 Bretter). |
| Raft Lanterns | `raft_lantern` | Upgrade Laternen: Laternenpfosten und Seilgeländer (2 Laternen, Seil, 4 Stöcke). |

#### Tauchen (Modul `diving`, im Tab Voyage)

| Im Spiel | ID (`raft:…`) | Beschreibung |
| --- | --- | --- |
| Diving Helmet | `diving_helmet` | Messinghelm mit Bullauge: unter Wasser viel weiter sehen; mit Tank atmet man aus dem Tank. Mit einem Angler Lure gecraftet bekommt er die Helmlampe. |
| Oxygen Tank | `oxygen_tank` | Brustteil: 2 Minuten Luft (2 400 Ticks), Anzeige am Item und als Balken unter Wasser. |
| Titanium Oxygen Tank | `titanium_oxygen_tank` | Brustteil: 6 Minuten Luft (7 200 Ticks) und Schutz wie ein Eisenbrustpanzer. |
| Wetsuit | `wetsuit` | Hose: unter Wasser dreimal so schnell abbauen; Quallen stechen nicht. |
| Flippers | `flippers` | Schuhe: viel schneller schwimmen, an Land 25 % langsamer gehen. |
| Air Compressor | `air_compressor` | Block: füllt Tanks und lädt den Sea Scooter mit FE von einem Nachbarn; ohne Strom per Kurbel. |
| Harpoon Gun | `harpoon_gun` | Harpunengewehr: 8 Schaden unter Wasser, 4 in der Luft, ein Schuss pro Sekunde; braucht Harpoons im Inventar. |
| Harpoon | `harpoon` | Harpune (Munition, wieder aufsammelbar): Eisen, Stock und Faden ergeben 4; Urchin Spine, Stock und Faden ergeben 2. |
| Sea Scooter | `sea_scooter` | Unterwasser-Scooter: Benutzen gedrückt halten zieht dich in Blickrichtung; Akku 3 000 FE, etwa 75 Sekunden Fahrt. |

#### Story (Modul `story`, Tab „Beach Craft: Tides of the Deep“) – Spoiler!

| Im Spiel | ID (`raft:…`) | Beschreibung |
| --- | --- | --- |
| Expedition Journal | `expedition_journal` | Expeditionstagebuch: Benutzen zeigt das aktuelle Ziel und einen Hinweis; schleichend benutzen zeichnet eine Karte zum nächsten Ort (alle 5 Minuten). Buch + Kompass + Papier. |
| Message in a Bottle | `message_in_a_bottle` | Flaschenpost treibt selten auf dem Meer; Benutzen ergibt einen Brief von Überlebenden. |
| Supply Barrel | `supply_barrel` | Vorratsfass treibt selten auf dem Meer; Benutzen bricht es auf und gibt nützliche Beute. |
| Coral Sigil, Pearl Sigil, Storm Sigil, Ember Sigil | `coral_sigil`, `pearl_sigil`, `storm_sigil`, `ember_sigil` | Die vier Tide Sigils (Coral, Pearl, Storm, Ember); jedes liegt nur im Tresor seines Story-Orts. Fallengelassen verschwinden sie nie. |
| Tidewarden Key | `tidewarden_key` | Am Tidewarden Altar aus allen vier Sigils geschmiedet; öffnet das Tide Seal und weckt den Leviathan; wird nicht verbraucht. |
| Tidewarden Altar | `tidewarden_altar` | Altar im Coral Temple: die vier Sigils einzeln einsetzen, dann schmiedet er den Schlüssel. |
| Tide Seal | `tide_seal` | Unzerstörbare, schimmernde Barriere vor dem Sanktum; öffnet sich nur für den Tidewarden Key (alle verbundenen Siegel-Blöcke). Offen ist sie unsichtbar und begehbar, hält aber das Wasser zurück. |
| Sanctum Tidestone, Sanctum Glass | `sanctum_tidestone`, `sanctum_glass` | Unzerstörbare Hülle des Abyssal Sanctum (Stein und dunkles Glas). |
| Leviathan Altar | `leviathan_altar` | Altar am Rand des Boss-Beckens: mit dem Tidewarden Key benutzen, um den Leviathan zu wecken. |
| Research Terminal | `research_terminal` | Computer der Expedition: zeigt ein Logbuch (z. B. von Dr. Voss). |
| Expedition Radio | `expedition_radio` | Funkgerät: knistert und zeigt eine zufällige Funkmeldung mit Hinweisen. |
| Sigil Pedestal | `sigil_pedestal` | Deko-Steinsockel in Tempeln und Sanktum. |

#### Boss-Beute (Modul `boss`) – Spoiler!

| Im Spiel | ID (`raft:…`) | Beschreibung |
| --- | --- | --- |
| Heart of the Tide | `heart_of_the_tide` | Block: gibt allen Schwimmern im Umkreis von 32 Blöcken Conduit Power und Gunst des Delfins; Dream-Star-Zutat in Dreamcraft. |
| Leviathan Trophy | `leviathan_trophy` | Kopf-Trophäe des Leviathan („The sea is calm again“). |
| Leviathan Scale | `leviathan_scale` | Schuppe des Leviathan, Material für den Tidebreaker und seine Reparatur. |
| Tidebreaker | `tidebreaker` | Legendärer Speer: 4 Schuppen, Titanbarren und Dreizack; 9 Schaden, +50 % gegen Meereswesen, im Wasser oder Regen Benutzen halten für einen Sprint. |
| Leviathan Spawn Egg, Tideling Spawn Egg | `leviathan_spawn_egg`, `tideling_spawn_egg` | Spawn-Eier (nur im Kreativmodus, im Story-Tab). |

#### Meereswesen-Drops (Modul `marine`, Tab „Beach Craft: Creatures“)

| Im Spiel | ID (`raft:…`) | Beschreibung |
| --- | --- | --- |
| Jelly Blob | `jelly_blob` | Von Mond- und Feuerquallen; 2 ergeben einen Schleimball. |
| Glow Jelly | `glow_jelly` | Von Leuchtquallen; ergibt einen Leuchttintenbeutel, Zutat der Jelly Lamp. |
| Angler Lure | `angler_lure` | Leuchtköder des Anglerfischs; 4 Prismarinscherben um einen Köder ergeben eine Seelaterne; macht den Taucherhelm zur Helmlampe. |
| Raw Eel Fillet, Cooked Eel Fillet | `eel_fillet`, `cooked_eel_fillet` | Muränenfilet, roh und gebraten (gebraten 3 Keulen). |
| Whale Spawn Egg, Manta Ray Spawn Egg, Jellyfish Spawn Egg, Anglerfish Spawn Egg, Moray Eel Spawn Egg, Hammerhead Shark Spawn Egg | `whale_spawn_egg`, `manta_ray_spawn_egg`, `jellyfish_spawn_egg`, `anglerfish_spawn_egg`, `moray_eel_spawn_egg`, `hammerhead_shark_spawn_egg` | Spawn-Eier der Meereswesen. |

#### Küstenwesen-Drops (Modul `shore`)

| Im Spiel | ID (`raft:…`) | Beschreibung |
| --- | --- | --- |
| Crab Claw, Cooked Crab Claw | `crab_claw`, `cooked_crab_claw` | Krabbenschere, roh und gebraten (gebraten 3 Keulen); „Crab Dinner“-Fortschritt. |
| Ember Shell | `ember_shell` | Warme Panzerschale der Ember Crab. |
| Cutlass | `cutlass` | Entermesser der Korsaren: Eisen und Teakbretter, 6 Schaden, schneller als ein Eisenschwert. |
| Crab Spawn Egg, Ember Crab Spawn Egg, Seagull Spawn Egg, Penguin Spawn Egg, Sea Otter Spawn Egg, Drowned Corsair Spawn Egg | `crab_spawn_egg`, `ember_crab_spawn_egg`, `seagull_spawn_egg`, `penguin_spawn_egg`, `sea_otter_spawn_egg`, `drowned_corsair_spawn_egg` | Spawn-Eier der Küstenwesen. |

#### Handbuch (Modul `guide`)

| Im Spiel | ID (`raft:…`) | Beschreibung |
| --- | --- | --- |
| Seafarer's Almanac | `seafarers_almanac` | Seafarer's Almanac, das Handbuch im Spiel (Abschnitt 3.10); Buch + Kelp, getrockneter Kelp, Treibholz-Stamm oder -Bretter. |

#### Inhalt aus Beach Craft 2.0 (Hauptressourcen, Tab „Raft“)

| Im Spiel | ID (`raft:…`) | Beschreibung |
| --- | --- | --- |
| Ancient Broken Ring | `ancient_broken_ring` | Antiker zerbrochener Ring: in Schiffswrack-Schätzen, vergrabenen Schätzen und Ozeanruinen, manchmal beim Angeln; schmilzt zu Ancient Energy. |
| Ancient Energy | `ancient_energy` | Antike Energie: Zutat für Energy Staff, Portalrahmen und Teleporter. |
| Ancient Crystal | `ancient_crystal` | Antiker Kristall aus Schiffswrack-Schätzen; Zutat des Energy Staff (und Kosten für einen zweiten Leviathan-Kampf). |
| Energy Staff | `energy_staff` | Ancient Energy oben, Ancient Crystal in der Mitte, Stock unten; zündet 64-mal ein Portal an. |
| Driftwood Portal Frame | `driftwood_portal_frame` | Portalrahmen: 4 Treibholz-Stämme um 1 Ancient Energy ergeben 4; Rahmen wie ein Netherportal, innen mindestens 2×3 frei. |
| Raft Portal | `raft_portal` | Der Portal-Block selbst (technisch). |
| Raft Dimension Teleporter | `raft_teleporter` | Raft Dimension Teleporter: 5 Titanbarren und 2 Ancient Energy; bringt dich ohne Portal zum Meer und zurück, 64 Nutzungen. |
| Driftwood Log, Driftwood Wood, Stripped Driftwood Log, Stripped Driftwood Wood, Driftwood Planks, Driftwood Leaves, Driftwood Sapling, Driftwood Stairs, Driftwood Slab, Driftwood Button, Driftwood Pressure Plate, Driftwood Fence, Driftwood Fence Gate, Driftwood Door, Driftwood Trapdoor | `driftwood_log`, `driftwood_wood`, `stripped_driftwood_log`, `stripped_driftwood_wood`, `driftwood_planks`, `driftwood_leaves`, `driftwood_sapling`, `driftwood_stairs`, `driftwood_slab`, `driftwood_button`, `driftwood_pressure_plate`, `driftwood_fence`, `driftwood_fence_gate`, `driftwood_door`, `driftwood_trapdoor` | Treibholz: kurze, dunkle Stümpfe an Sandstränden der Oberwelt und treibende Treibholz-Strukturen; komplette Holzfamilie. Brennt im Ofen. |
| Palm Log, Palm Wood, Stripped Palm Log, Stripped Palm Wood, Palm Planks, Palm Leaves, Palm Coconut Leaves, Palm Sapling, Palm Stairs, Palm Slab, Palm Button, Palm Pressure Plate, Palm Fence, Palm Fence Gate, Palm Door, Palm Trapdoor | `palm_log`, `palm_wood`, `stripped_palm_log`, `stripped_palm_wood`, `palm_planks`, `palm_leaves`, `palm_coconut_leaves`, `palm_sapling`, `palm_stairs`, `palm_slab`, `palm_button`, `palm_pressure_plate`, `palm_fence`, `palm_fence_gate`, `palm_door`, `palm_trapdoor` | Palmenholz der Inseln, komplette Holzfamilie; an Palmblättern mit Kokosnüssen wachsen die Nüsse nach etwa 20 Minuten nach. |
| Raft Foundation | `raft_foundation` | Floß-Fundament: 7 Bretter mit Seil oben und unten in der Mitte ergeben 4. |
| Reinforced Foundation | `reinforced_foundation` | Verstärktes Fundament: Fundament + 2 Schrott; Haie beißen es nie an. |
| Rope | `rope` | Seil aus 2 Palmblättern oder 3 Fäden. |
| Rope Ladder, Rope Coil | `rope_ladder`, `rope_coil` | Strickleiter (kletterbar) und Seilrolle (Deko). |
| Palm Thatch, Palm Thatch Stairs, Palm Thatch Slab | `palm_thatch`, `palm_thatch_stairs`, `palm_thatch_slab` | Palmenstroh-Dach als Block, Treppe und Stufe. |
| Sail Canvas, Red Striped Sail Canvas | `sail_canvas`, `sail_canvas_red_striped` | Segeltuch: 2 Seil über 2 weißer Wolle ergeben 2; auch rot gestreift. |
| Scrap Metal, Scrap Metal Block | `scrap_metal`, `scrap_metal_block` | Schrott aus dem Treibgut, auch als Block. |
| Plastic, Plastic Block | `plastic`, `plastic_block` | Plastik aus dem Treibgut, auch als Block; Zutat des Circuit Board. |
| Ship Wheel, Raft Flag, Coconut Lantern | `ship_wheel`, `raft_flag`, `coconut_lantern` | Deko: Steuerrad, Floß-Flagge und Kokosnuss-Laterne. |
| Shark Jaw Trophy | `shark_jaw_trophy` | Hai-Kiefer-Trophäe: 3 Bretter auf 3 Haizähnen, sitzt bündig an der Wand. |
| Item Catcher, Item Catcher Net | `item_catcher`, `net` | Item Catcher fängt im Wasser treibende Items (eine Sorte gleichzeitig, Trichter können leeren); mit Item Catcher Net (hält 32 Fänge) fischt er etwa alle 30 Sekunden Unrefined Ocean Garbage. |
| Unrefined Ocean Garbage, Trash Cube | `unrefined_ocean_garbage`, `trash_cube` | Meeresmüll schmilzt zum Trash Cube; der Würfel gibt 1 bis 3 Überraschungen. |
| Water Purifier, Fresh Water | `water_purifier`, `fresh_water` | Wasserreiniger: Wasserflaschen werden zu Fresh Water (ein Eimer gibt drei); Brennstoff Bretter, Stämme, Kohle oder Holzkohle. Fresh Water füllt eine Keule. |
| Simple Grill | `simple_grill` | Einfacher Grill: zwei Speisen gleichzeitig, 50 % schneller als ein Lagerfeuer; erst mit Brennstoff, dann mit rohem Essen benutzen. |
| Crop Plot | `crop_plot` | Pflanzbeet: immer bewässert, nie zertrampelt, Pflanzen wachsen etwa 50 % schneller. |
| Scarecrow | `scarecrow` | Vogelscheuche: keine Monster-Spawns im Umkreis von 24 Blöcken, kein Zertrampeln in 8 Blöcken, Möwen picken in 16 Blöcken nicht. |
| Plastic Hook | `plastic_hook` | Plastikhaken: Benutzen halten zieht treibende Items aus bis zu 12 Blöcken heran. |
| Paddle | `paddle` | Paddel: im Boot ein Schub nach vorn. |
| Receiver | `receiver` | Empfänger: Richtung und Entfernung zum nächsten treibenden Treibholz. |
| Coconut, Coconut Milk, Pina Colada | `coconut`, `coconut_milk`, `pina_colada` | Kokosnuss, Kokosmilch (Regeneration I für 5 Sekunden) und Piña Colada (Tempo; gibt die Schüssel zurück). |
| Raw Shark Meat, Cooked Shark Meat, Shark Tooth | `shark_meat`, `cooked_shark_meat`, `shark_tooth` | Drops von Bruce: rohes und gebratenes Haifleisch, Haizähne. |
| Bruce the Shark Spawn Egg | `shark_spawn_egg` | Spawn-Ei von Bruce the Shark. |
| Titanium Ore, Deepslate Titanium Ore, Raw Titanium, Raw Titanium Block, Titanium Ingot, Titanium Nugget, Titanium Block, Titanium Grates | `titanium_ore`, `deepslate_titanium_ore`, `raw_titanium`, `raw_titanium_block`, `titanium_ingot`, `titanium_nugget`, `titanium_block`, `titanium_grates` | Titan: Erz nur in der Raft-Dimension unter y 20 unter dem Meeresboden, Diamantspitzhacke, gibt XP; 9 Nuggets = Barren, 9 Barren = Block; Titangitter als Deko. |
| Titanium Helmet, Titanium Chestplate, Titanium Leggings, Titanium Boots | `titanium_helmet`, `titanium_chestplate`, `titanium_leggings`, `titanium_boots` | Titanrüstung; das volle Set gibt Wasseratmung, Gunst des Delfins und Conduit Power. Titan-Werkzeuge gibt es nicht. |
| Metal Detector | `metal_detector` | Metalldetektor: auf den Boden benutzen, meldet die Höhe des ersten Titanerzes darunter (Aktionsleiste). |
| Makeshift Solar Panel | `makeshift_solar_panel` | Behelfs-Solarpanel: 10 FE pro Tick in der Sonne (über der Endless Sea geht sie nie unter). |
| Makeshift Battery | `makeshift_battery` | Behelfs-Batterie: speichert 1 000 000 FE, bis 10 000 FE pro Tick rein und raus. |
| Copper Cable, Titanium Cable | `copper_cable`, `titanium_cable` | Kabel: Kupfer 128 FE pro Tick, Titan 512 FE pro Tick. |
| Quarry | `quarry` | Steinbruch: gräbt ein 11×11-Loch bis zum Weltboden, 1 000 FE pro Block; eine Truhe obendrauf sammelt die Drops. |
| Chunk Destroyer | `chunk_destroyer` | Baut seinen ganzen Chunk ab, 100 000 FE pro Säule. |
| Brick Furnace, Titanium Furnace | `brick_furnace`, `titanium_furnace` | Ziegelofen 1,5-mal schneller; Titanofen 32-mal schneller und verdoppelt jedes Ergebnis. |
| Circuit Board | `circuit_board` | Schaltkreis aus Kupfer, Schleimball und Plastik; in den meisten Maschinen-Rezepten. |
| Some Game Music Disc, Lofi Beat Music Disc, Crystal Castles Music Disc | `some_game_music_music_disc`, `lofi_beat_music_disc`, `crystal_castles_music_disc` | Drei eigene Musik-Discs; eine pro Schiffswrack-Truhe. |

---

## 5. Technische Architektur

### Module
Jeder Inhaltsbereich ist ein **Modul** mit eigenem Java-Paket, eigenem Ressourcen-Ordner, eigener Mixin-Config und
eigenen Python-Generatoren. Ein Modul darf nur seine eigenen Stellen ändern; Verweise zwischen Modulen laufen in Java
über IDs zur Laufzeit (`BuiltInRegistries.BLOCK.getValue(Raft.id("tide_seal"))`), in JSON über ID-Strings.

| Modul | Inhalt |
| --- | --- |
| `world` | Gelände, Biome, natürliche Blöcke, `WorldSpawns` |
| `building` | Baublöcke, Expeditions-Technik, Windturbine |
| `decor` | Deko, Sitz-Entity `raft:seat`, Kanone |
| `shore` | Krabben, Ember Crab, Möwe, Pinguin, Seeotter, Korsar |
| `marine` | Hai (überarbeitet), Hammerhai, Wal, Manta, Qualle, Anglerfisch, Muräne |
| `voyage` | Boote, Expedition Raft, Upgrades |
| `diving` | Tauchausrüstung, Air Compressor, Harpune, Scooter |
| `story` | Story-Items und -Blöcke, Loot-Tabellen, Advancements, Journal, Castaway-Truhe, Treibgut-Ergänzungen |
| `boss` | Leviathan, Tideling, Brine Bolt, Beute |
| `guide` | Seafarer's Almanac |
| `structures_surface`, `structures_deep`, `structures_city`, `structures_side` | nur Daten: Strukturvorlagen, Pools, Sets |
| `polish` | Überarbeitung der 2.0-Texturen (nur Werkzeug) |

- Java: `net.kasax.raft.content.<modul>`, je Modul eine Klasse `…Module implements ContentModule` mit `init()` und
  `initClient()`; Client-Code nur unter `content/<modul>/client/`.
- Ressourcen: `src/main/modules/<modul>/{assets,data}`, Mixins: `raft-<modul>.mixins.json` (Paket `…content.<modul>.mixin`).
- Registrierung über `BcReg` (`block`, `blockWithItem`, `item`, `entity`, `blockEntity`, `sound`), Creative-Tabs über
  `BcTabs` (BUILDING, DECOR, NATURE, VOYAGE, CREATURES, STORY).
- Der alte 2.0-Code (`net.kasax.raft.*` außerhalb von `content`) blieb: Holz, Fundamente, Portal, Hai, Titan,
  Maschinen, Öfen, Item Catcher, Wasserreiniger, Grill, Pflanzbeet, Vogelscheuche, Treibgut.

### Generatoren und Resource-Merge
- **Alle JSON-Dateien und Texturen** eines Moduls entstehen durch wiederholbare Python-Skripte
  `tools/content/<modul>/gen.py` (Aufruf `cd tools && python3 -m content.<modul>.gen`), kein Fabric-Datagen.
- Gradle-Task **`mergeResources`** fügt `src/main/resources`, `src/main/generated` und alle Modul-Ordner zusammen. Nur
  **Sprachdateien, Tags und `sounds.json`** dürfen mehrfach vorkommen und werden zusammengeführt (derselbe
  Sprachschlüssel mit anderem Text = Build-Fehler). Jede andere doppelte Datei bricht den Build ab – so können sich
  Module nicht still überschreiben.

### `tools/bclib` – die Werkzeugkiste
| Datei | Zweck |
| --- | --- |
| `assets.py` | 26.3-JSON: Blockstates, Modelle, Item-Definitionen, Loot, Rezepte, Tags, Familien (Treppe, Stufe, Mauer, Zaun, Tor) |
| `tex.py` | Pixel-Art: Farbrampen (4–6 Töne), Umrisse, Kachel-Vorschau, Kontaktbögen, animierte Texturen |
| `nbt.py` | Strukturvorlagen im 26.3-Format (`id`/`properties`), Truhen mit Loot; seit der Integration mit gzip-mtime 0, damit gleiche Builds gleiche Dateien ergeben |
| `preview.py` | isometrische Vorschau und Schnitte von Strukturen, Prüfung auf unbekannte Blöcke |
| `paths.py` | Pfade der Module |

### `tools/bctest` – skriptbarer Test im Spiel
`tools/bctest/run.sh <skript> <ausgabe>` baut den Mod, startet einen Client (Xvfb, ohne Ton) mit dem Test-Mod aus
`src/gametest`, führt das Skript aus und schreibt Screenshots, `latest.log` und `gradle.log`. Befehle: `world [seed]`,
`cmd`, `pcmd`, `wait`, `settle`, `shot`, `size`, `hud`, `third`, `gui`, `rd`, `use`, `attack`, `sneak`, `hold`,
`sneakuse`, `esc`, `slot`, `tab` (Creative-Tab öffnen und Items loggen), `count` (Entities zählen), `log`.
`BC_JFR=` zeichnet ein Profil auf. Ein gemeinsames Build-Lock sorgt dafür, dass nur ein Test oder Compile gleichzeitig
läuft; ein schneller javac-Check lief über `$SP/ref/jc.sh`.

### Kunst-Richtlinie
16×16-Texturen im Vanilla-Stil: eine farbverschobene Rampe aus 4–6 Tönen pro Material, Licht von oben links, klare
Silhouetten, kein reines Schwarz, kein Zufallsrauschen. Items mit 1 Pixel dunklerem Umriss. Entities in Vanilla-Maßstab
(64×64, 128×128, Boss 256×256), Modelle aus Boxen mit Animation. Paletten-Themen: Tidewardens türkis mit cyanen Runen und
Gold, Meridian-Expedition lackierter Stahl und Messing im 50er-Jahre-Forschungs-Look, Piraten dunkles Teak und rotes
Tuch, Inseln warmer Sand und Palmengrün, Tiefsee Navy mit Biolumineszenz, Vulkan Basalt und Glut.

---

## 6. Testergebnisse

**Pro Modul (Berichte vom 3.11., vor der Integration, `$SP/work/reports.md`):** Jedes Modul wurde mit bctest im Spiel
geprüft (Screenshots angesehen). Nicht im Spiel gesehen wurden damals u. a.: Schlafen in der Hängematte bei Nacht, das
Kartenzeichnen per Schleichen + Benutzen (bctest konnte das noch nicht), die Castaway-Truhe auf einer neuen Plattform,
die Handkurbel des Kompressors, einige Struktur-Varianten mit zufälliger Lage (nur in Vorschauen), Walgesang (Testclient
ohne Ton) und die letzten Modell-Feinheiten des Bosses.

**Integration und Spielablauf (Commits vom 3.11.):**
- `bctest` bekam `sneakuse`, `esc`, `slot`, `count` und Zeitmessung.
- **Story-Weg** im Spiel (`$SP/work/storypath`, 8 Läufe): Karten aus jeder Story-Truhe, Besuch und `/locate` jedes
  Orts, das Journal in Oberwelt und Meer. Fixes daraus: Castaway-Truhe gibt das Almanac, keine Geister-Sigils durch
  `/give`, Nebenstrukturen mit fester Höhe einen Block höher (Floß-Decks bei y 99), Piratenbucht ohne Gräben,
  Tidewarden-Altar wasserfest, beleuchteter Beckenrand im Sanktum und Säle im Rathaus, Belohnungstruhen mit Loot.
- **Spielablauf** (`$SP/work/gameplay2`): Platzieren an Wand/Decke/Boden, Sitzen, Hängematte, Kanone, Turbine,
  Kompressor, Boote, Floß fahren, stehen, Menü, Upgrades, Abbauen, Hai am Floß, Tauch-Anzeige, Münzen, Absteigen.
  Fixes: Kompressor speichert seinen Slot (Tank/Scooter verschwand beim Chunk-Speichern), Absteigen vom Steuer bei
  Fahrt wirft nicht mehr ins Meer, Münzhaufen brechen ohne Stütze, Turbinen-Item-Modell, Helmlampe im Voyage-Tab.
- **Integrations-Fixes:** Kraterlava nicht in der Schmiede, höchstens 5 Tidelings (8 überrannten Spieler), Leuchttintenfisch
  im Graben seltener (füllte das gemeinsame Limit), Wrack-Segel und -Teppich aus Wolle (Teppiche wurden unter Wasser
  weggespült), reproduzierbare NBT-Dateien.
- Vorher (Commit `fa1124b`): Leviathan-Altar und Research Terminal drehen sich mit gedrehten Strukturen mit.
- Weitere Prüfungen laut Spezifikation 13: `/locate` und `/place` für jede Struktur, Screenshots jedes Bioms, jeder
  Kreatur, jedes Creative-Tabs, Bosskampf, Floß mit allen Upgrades, Tauchen, Möwe gegen Vogelscheuche, Haibisse,
  Start eines Dedicated Servers ohne Client-Klassen. Ein Protokoll mit Häkchen pro Punkt habe ich in den Repos und im
  Scratchpad nicht gefunden – welche Punkte am Ende alle wirklich gelaufen sind, ist im Einzelnen **unklar**.
- In Dreamcraft lief 3.0.0 im V1.3-Testclient (Smoke-Test, Quest-Kapitel, Registry-Dump).

---

## 7. Bekannte Probleme und Design-Entscheidungen

### Abweichungen von der Spezifikation (Abschnitt 14, gekürzt)
- **IDs:** Holzfamilien nach Vanilla-Schema (`weathered_stairs`, `teak_slab` …), Korallenziegel `coral_stone_brick_*`;
  zusätzliche Blöcke wie `weathered_door`, Tidestone- und Beton-Varianten.
- **Doppel-T-Träger** ist eine echte Form und wasserfest.
- **Boote und Flöße** haben keine Entity-Loot-Tabellen, sie droppen ihr Item; Anker über den Hebel im Floß-Menü;
  Upgrade-Rezepte siehe 3.8.
- **Tide Seal** offen = unsichtbar und begehbar, hält aber Wasser zurück; die geschnitzte Fratze des Leviathan-Altars
  zeigt zum Spieler.
- **26.3-Fallen:** Eine einzige unbekannte Item-ID in irgendeiner Loot-Tabelle stoppt das Laden der Welt – deshalb
  nennen Story-Tabellen Items anderer Module über optionale Ein-Item-Tags; Rezepte mit Fremd-Items haben
  `fabric:registry_contains`. Karten sind `minecraft:filled_map`. Ebenso stoppt eine unbekannte Entity-ID in einer
  Biom-Datei die Welt – deshalb `WorldSpawns`.
- **Biom-Tags:** Die Biome stehen nicht in `minecraft:is_ocean`/`is_deep_ocean`/`is_beach` (26.3 liest sie nicht mehr;
  sie würden nur Vanilla-Monumente, Ozeanruinen und Ruinenportale hinzufügen). Stattdessen gezielte Tags (Shipwrecks,
  Tropenfische, Korallen, Eisbären, warme Frösche, Oberflächen-Schleim).
- **Hängematte** ist ein echtes Bett (Zustand `occupied`); zusätzliche Entity `raft:cannonball`.
- **Große Strukturen** sind einzelne Vorlagen über 48 Blöcke (Helix 57×17×54, Tempel 41×23×48, Sanktum 63×34×102,
  Galeone 31×34×53, Frachter 25×29×63, Piratenbucht 56×49×54, Bohrinsel 48×125×45); Story-Bauten mit
  `ignore_waterlogging`, Nebenorte mit `apply_waterlogging`. Feste Starthöhen einen Block höher (Jigsaw-Start liegt
  einen Block unter `start_height`).
- **Tauchen:** Komponente `raft:stored_air`, Scooter-Energie in `team_reborn_energy:energy`; Extra-Rezept Harpunen aus
  Seeigelstacheln; Flossen −25 % an Land; Helmlampe (nicht im Plan) als Komponente `raft:diving_lamp`.
- **Hai-Spielregel** heißt `raft:shark_bites` (26.3-Spielregeln sind kleingeschriebene Registry-IDs, `raftSharkBites`
  ging nicht). Haie kreisen trotzdem, Beißen stoppt bei Treffern (~7 s Flucht).
- **Spawn-Kategorien:** Hai, Hammerhai, Wal, Manta = `water_creature`; Qualle, Muräne = `water_ambient`; Anglerfisch =
  `underground_water_creature`. Die Muränen-Hitbox ist 0,6×0,4 (Modell 1,2 lang), damit sie in ein Block große
  Spalten passt.
- **Boss:** Der Leviathan braucht keinen Altar-Aufbau – er misst sein Becken beim ersten Tick, heilt nach 30 s ohne
  Spieler, max. 5 Tidelings.
- **Licht, Schwerkraft, Krater, Almanac, Wolle** wie in 3.1/3.10/6 beschrieben.

### Bekannte Probleme (aus den Modulberichten, nicht behoben)
- Sonnenschirm: Klicks treffen nur den Schirm im eigenen Block, das Dach ist reine Optik. Stuhllehnen sind etwas höher
  als ein Block.
- Windturbine: Steht ein Block vor dem Rotor, stoppt er, wird aber trotzdem gezeichnet (gewollt).
- Leviathan: frisch gespawnt hängt der Körper kurz senkrecht durch den Boden, bis er sich bewegt (~2 s); der Tidebreaker
  ist ein 2D-Sprite.
- Harpunengewehr: in der dritten Person keine Armbrust-Zielhaltung. Der Tank füllt sich auch an Land, sobald der Kopf
  aus dem Wasser ist (so in der Spezifikation). Mobs mit Taucherausrüstung bekommen nur die Optik.
- Expedition Raft: die Hitbox ist achsenparallel – wer beim Drehen genau an der Deck-Ecke steht, kann ins Wasser
  fallen. Mobs, die ans Floß stoßen, können sich auf freie Sitze setzen (wie bei Vanilla-Booten).
- Wal: an Land erstickt er wie ein Vanilla-Wassertier; unter einem Überhang „atmet“ er am ersten festen Block und bläst
  unter Wasser.
- Krabben-Kneifen ist nur 0,5 s zu sehen; Möwen mit Beute stehlen erst nach dem Fressen wieder; untätige Korsaren
  laufen über den Meeresboden.
- Old Lighthouse: die Drehung ist zufällig, der Steg kann ins Land zeigen (dann wird er zum Holzweg ohne Boot und Bojen).
  Die Plattform unter dem Gelände wirkt am Ufer wie ein Kai.
- In den Coral Shallows können Helix-Station und Tempel-Turm aus dem Wasser ragen; Wracks und Ruinen im Flachwasser
  ebenfalls (gewollt). Schräge Wracks zeigen Treppen-Kanten an Diagonalen.
- Landstrukturen am Strandrand können auf Wasser starten und eine Bodenplatte bei y 99 bekommen.
- Spawns im Abyssal Trench: Der Anglerfisch kommt aus `WorldSpawns.java` mit Gewicht **4**, der Leuchttintenfisch aus
  der Biom-Datei mit Gewicht **3** (vorher 10). So überwiegt der Anglerfisch, wie beabsichtigt. Die Integrations-Commit-
  Nachricht nennt für den Anglerfisch fälschlich 6; der wirksame Wert ist 4.
- Langsame Welt-Generierung in der Raft-Dimension fiel in allen Testläufen auf (auf dem langsamen Testrechner 3–5 min
  pro neuem Gebiet); nicht profiliert.

### Offene Design-Fragen aus dem 2.0.1-Review (`REPORT.md`, bewusst nicht geändert)
Titanofen verdoppelt jedes Ergebnis (auch Ancient Energy); Maschinen verlieren beim Abbauen ihre Energie; Chunk
Destroyer kostet auch für leere Säulen 100 000 FE; Item Catcher hat nur einen Ausgabe-Slot; der Treibholz-Setzling ist
fast nur über Treibgut-Beute zu bekommen; wer von der Plattform (y 209) fällt, landet im Meer; der Plastic Hook zieht
durch Wände. Die Frage nach den Steinmassiven hat 3.0 mit dem Archipel beantwortet.

---

## 8. CurseForge-Seite
`docs/curseforge/description.html` (Branch `26.3`) mit neuem Header `img/header_3.png`, deinem Bisect-Banner
`img/bisect.png`, Abschnitts-Streifen `strip_*.png`, Collagen aus Screenshots (`make_images3.py`) und **23
Spoiler-Boxen**; der Boss steht nur hinter einem Spoiler. Einfügen von Hand, siehe
[06_videos_und_beschreibungen.md](06_videos_und_beschreibungen.md).
