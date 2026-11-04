# 04 – Tamagotchi: der Haustier-Mod im Pack und der Bug-Check für 1.2.0

**Tamagotchi** ist dein Fabric-Mod für Minecraft 26.3 (Repo `Kasax007/tamagotchi`, Mod-ID `tamagotchi`,
CurseForge-Projekt **1758309**). Zehn seltene Haustiere verstecken sich in den Strukturen der Welt. Man findet eines,
zähmt es mit einem **Tamagotchi Heart** und kümmert sich darum – füttern, spielen, sauber halten, schlafen lassen.
Dann wird es zum besten Freund: Es folgt dir, trägt einen Rucksack, kämpft mit, bringt dir goldene Äpfel, wenn du
verletzt bist, und hat ein besonderes Talent.

Mit **Dreamcraft V1.3** kommt Tamagotchi ins Pack, samt eigenem Quest-Seitenpfad (27 Quests, siehe
[01_dreamcraft.md](01_dreamcraft.md)) und als Zutat des Dream Star (Tamagotchi Heart).

## 1. Was der Mod kann (aus README und CHANGELOG)

### Die zehn Haustiere
| Pet | Lebt in (Chance pro Struktur) | Talent | Lieblings-Leckerli |
| --- | --- | --- | --- |
| Desert Dragon | Wüstenpyramide (40 %) | **Ember Roast** – röstet rohes Essen, schmilzt Erz | Dragon Fruit |
| Jungle Dragon | Dschungeltempel (40 %) | **Green Thumb** – Pflanzen und Setzlinge in der Nähe wachsen | Dragon Fruit |
| Tide Dragon | Ozeanmonument (50 %) | **Tide Blessing** – Wasseratmung und Gunst des Delfins beim Schwimmen in seiner Nähe | Fish Crackers |
| Frost Penguin | Iglu (45 %) | **Frost Steps** – Wasser gefriert unter deinen Füßen, solange er folgt | Fish Crackers |
| Ember Pup | Netherfestung (30 %) | **Warm Heart** – Feuerresistenz, wenn du brennst; schwimmt in Lava | Ember Jerky |
| Sculk Wisp | Antike Stadt (50 %) | **Echo Sense** – Sonar-Ping lässt feindliche Mobs durch Wände leuchten | Glow Gummy |
| Void Kitten | Endstadt (30 %) | **Item Magnet** – zieht fallengelassene Items in seinen Rucksack oder zu dir | Fish Crackers |
| Pebble Golem | Trail Ruins (35 %), Minen (8 %) | **Ore Sniffer** – erschnüffelt das beste Erz in der Nähe und zeigt den Weg | Rock Candy |
| Hex Toad | Hexenhütte (45 %) | **Brew Buddy** – braut dir einen zufälligen hilfreichen Trank-Effekt | Glow Gummy |
| Mimic | Trial Chambers (30 %), Waldanwesen (60 %) | **Treasure Belly** – 27-Slot-Bauch (54 mit Rucksack), hustet Schätze aus | Golden Biscuit |

Wilde Pets bleiben bei ihrer Struktur und verschwinden nie. Die niedlichen laufen weg, wenn man sie schlägt; Ember Pup,
Sculk Wisp und Mimic beißen zurück. Wer ein Tamagotchi Heart in der Hand hält, lockt sie an.

### Steuerung
| Am eigenen Pet | Wirkung |
| --- | --- |
| Rechtsklick, leere Hand | streicheln ♥ |
| Schleichen + Rechtsklick, leere Hand | Pet-Screen: Bedürfnisse, Stimmung, Bindung, Talent, Rucksack, Sit / Follow / Wander |
| Schleichen + Rechtsklick **mit einer Truhe** | Rucksack an (27 Slots) |
| Schleichen + Rechtsklick **mit einer Schere** | Rucksack ab – **alles darin fällt heraus** |
| Rechtsklick mit dem **Tama Pager** | Sitz/Bleib ↔ Folgen |
| Rechtsklick mit Futter / Leckerli | füttern |
| Rechtsklick mit **goldenem Apfel** | in den Rucksack – das Pet bringt ihn dir bei wenig Leben |
| Rechtsklick mit der Pet Brush | bürsten |

Der **Tama Pager** öffnet in der Luft den Screen des nächsten eigenen Pets (bis 64 Blöcke) und **piept**, wenn ein Pet
hungrig, gelangweilt, müde, schmutzig oder verletzt ist. Beim ersten Zähmen gibt es einen gratis. Das **Tamacon**
(Buch + rosa Farbe + Redstone) ist das Handbuch im Spiel.

### Pflege
- Vier Bedürfnisse – **Hunger, Fun, Energy, Hygiene** – ergeben die **Stimmung** (Pager-Screen und kleine Blasen über
  dem Kopf). Glückliche Pets nutzen ihr Talent, traurige nicht, todunglückliche kämpfen nicht.
- **Bond** (Herzen) wächst mit jeder Pflege und lässt Talente schneller wieder aufladen.
- Hunger: Pet Kibble, Lieblings-Leckerli, normales Futter oder ein Food Bowl. Fun: streicheln, Laser Pointer, Squeaky
  Ball (Apportieren), Feather Wand, Bouncy Mushroom, Running Wheel, Scratching Post, Toy Box, Plüschtiere, andere Pets.
  Energy: Schlafen in Pet Bed, Pet Basket oder Dragon Nest (schneller neben einem Plüschtier der eigenen Art).
  Hygiene: Pet Brush oder gefülltes Pet Bath.
- Die drei Drachen fliegen, wenn das schneller ist (oder aus Spaß). Im Kampf hilft ein Pet wie ein Wolf; unter einem
  Drittel Leben zieht es sich zurück und frisst aus dem Rucksack.
- **Gezähmte Pets sterben nie:** Sie fallen in Ohnmacht und werden zu einem **Tama Egg**, das alles behält.
- Pets reagieren auf die Welt: tanzen zur Jukebox, wärmen sich am Lagerfeuer, schnuppern an Blumen, betteln um Kuchen,
  verstecken sich vor Gewittern, schütteln sich, jubeln bei Level-ups, spielen miteinander, schlafen neben deinem Bett.

### Möbel und Gadgets
- Schlafen: Pet Bed, Pet Basket, Dragon Nest · Futter: Food Bowl · Baden: Pet Bath · Spaß: Bouncy Mushroom (alle
  hüpfen), Running Wheel (gibt ein Redstone-Signal, solange ein Pet läuft), Scratching Post · Schutz: Pet House.
- Seit 1.1: **Plüschtiere** aller zehn Pets, **Pet Portrait** (malt dein nächstes Pet samt Namen), **Treat Dispenser**
  (Redstone-Puls schießt ein Leckerli zum hungrigsten Pet), **Pet Incubator** (Tama Egg schlüpft in 30 s),
  **Toy Box**, **Pet Flap** (nur Pets kommen durch), **Egg Lamp**; Pet Bed, Pet Basket, Egg Lamp und Portrait-Hintergrund
  lassen sich in allen 16 Farben färben.
- JEI und REI zeigen alle Rezepte plus Infoseiten, wo jedes Pet lebt.

## 2. Der Bug- und Feature-Check, aus dem 1.2.0 wurde

Ziel der Runde: Tamagotchi **modpack-tauglich** machen, denn in Dreamcraft gibt es viel Essen, Erze und Strukturen
aus anderen Mods. Plan und Stand stehen in `docs/PLAN.md` (Abschnitt „Round 3“).

### Neue Funktionen (1.2.0)
- Pets fressen auch Essen anderer Mods (die `c:foods`-Tags); der Pebble Golem erschnüffelt auch Mod-Erze (`c:ores`).
- Pets leben auch in **Look-alike-Strukturen** anderer Mods: Pyramiden, Hexenhütten, Minen, Anwesen, Monumente und
  mehr von Repurposed Structures, Iglus und Netherfestungen von Moog's Structures; dazu Dungeons and Taverns und
  Explorations. Datapacks können eigene Strukturen über die Struktur-Tags `tamagotchi:pet_home/<regel>` ergänzen.
- Jede Holztruhe (`c:chests/wooden`) setzt den Rucksack auf, jede Schere (`c:tools/shear`) nimmt ihn ab – auch aus
  anderen Mods.
- Möbel zeigen im Tooltip, was die Pets damit machen.
- Rezepte erscheinen im Rezeptbuch, sobald man eine Zutat trägt.
- Äxte, Spitzhacken und Hacken bauen die Möbel schneller ab.
- Der Food Bowl hat jetzt einen Knochen in der Mitte (das alte Rezept kollidierte mit dem Tonbecher einer anderen Mod).
- Für Modpacks: Ernährung als Item-Tags `tamagotchi:diet/meat`, `fish`, `plant`, `sweet`, `mineral` (mit Namen für
  Rezept-Viewer).

### Behobene Fehler (1.2.0)
- Ein müdes Pet, das dich nicht erreicht, schläft nicht mehr ständig ein und wacht wieder auf.
- Pets bleiben neben deinem Bett eingerollt, bis du aufstehst.
- Ein unterbrochenes Füttern mit goldenem Apfel erzeugt keinen Gratis-Apfel mehr (Dupe).
- Verletzte Pets essen ihr Futter aus dem Rucksack, nicht die goldenen Äpfel für dich.
- Ein Pet, das in der Leere ohnmächtig wird, landet als Ei in deinem Inventar, statt ewig zu fallen.
- Tama Eggs auf dem Boden überstehen Feuer, Lava, Kakteen und Explosionen.
- Ein in der Luft gespeicherter Drache schwebt nach dem Laden nicht mehr ewig.
- Das Void Kitten zieht Items nur noch, wenn du in der Nähe bist, und lässt Items liegen, die Spieler wegwerfen.
- Pets versuchen nicht mehr, einem Besitzer in einer anderen Dimension zu folgen, von ihm zu betteln oder ihm einen
  Ball zu bringen (auch Möbel und Level-up-Jubel nur in der eigenen Dimension).
- Der Pet-Screen zeigt „Sit“ richtig, auch nach dem Laden der Welt; das Tamacon-Inhaltsverzeichnis reagiert nur auf die
  linke Maustaste (26.3/SDL: links = 1).

### Wie geprüft wurde
- Client-Game-Tests mit **echten Klicks** (`./gradlew runClientGameTest`, `-Ptests=checks` nur Funktions-Checks,
  `-Ptests=blocks,checks` mit der Möbel-Galerie); die Tests wurden dafür an 26.3 angepasst (Screen-Zugriff
  `mc.gui.screen()`, Pet-Screen schließen wie mit Esc). Ergebnis-Zeilen `[TamaTest] PASS/FAIL` im Log.
- Dedicated Server mit platzierten Strukturen.
- Im Dreamcraft-V1.3-Testclient lief bereits das 1.2.0-Jar (`$SP/ownjars/tamagotchi-1.2.0.jar`).

## 3. Release-Stand

| Version | CurseForge-Datei | Stand |
| --- | --- | --- |
| 1.0.0 | 9281396 | veröffentlicht |
| 1.1.0 | 9399713 | veröffentlicht |
| 1.2.0 | 9431312 | veröffentlicht (4.11.2026), **aktuell**; in Dreamcraft ab V1.3 (`pack/mods.json`) |

**Wo 1.2.0 liegt:** auf dem Branch **`26.3`** (Commit `aa45ba7`, `mod_version=1.2.0`, am 4.11. per Fast-Forward von
`bugcheck-wip` nachgezogen und auf GitHub gepusht).

**Wie 1.2.0 veröffentlicht wurde:** Mit deiner Freigabe habe ich das Jar (`tamagotchi-1.2.0.jar`, gebaut aus `26.3`)
direkt über die CurseForge-API hochgeladen; Changelog ist der Abschnitt `## 1.2.0` aus `CHANGELOG.md`. Der
eigentliche Release-Weg (README, „Releasing“, `.github/workflows/release.yml`) ging aus der Sitzung nicht: Das
Pushen des Tags `v1.2.0` bricht am Proxy ab, und „Run workflow“ per API findet den Workflow nicht, weil der
Default-Branch `main` nur eine README hat. **Noch offen:** ein GitHub-Release/Tag `v1.2.0` – das kannst du selbst
anlegen (Tag `v1.2.0` auf `26.3`). Achtung: Der Workflow würde dann auch noch einmal auf CurseForge hochladen, falls das
Secret `CURSEFORGE_TOKEN` gesetzt ist; dann die doppelte Datei auf CurseForge löschen oder nur das GitHub-Release von
Hand anlegen.

**Zusammenhang mit Dreamcraft V1.3:** Der V1.3-Quest-Seitenpfad beschreibt 1.2.0-Verhalten („In Dreamcraft they also
live in the look-alikes … of Repurposed Structures“, „modded ores too“, „Pets eat modded food too“). V1.3 enthält
deshalb genau die CurseForge-Datei 9431312.

## 4. Videos zu Tamagotchi

Short (ca. 43 s), 2-Minuten-Showcase und ein Review-Schnitt (ca. 3:05, nur für dich) mit echten Spielgeräuschen
liegen im Archiv unter `tamagotchi/` – siehe [06_videos_und_beschreibungen.md](06_videos_und_beschreibungen.md).
Sie zeigen Version 1.1; für 1.2.0 gibt es kein neues Video.
