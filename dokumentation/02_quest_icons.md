# 02 – Quest Icons: das Quest-System von Dreamcraft

**Quest Icons** ist dein Mod, der früher nur Icons für Quest-Bücher geliefert hat (Repo
`Kasax007/Kasax_Quests_Items_Mod-1.19.2`, Branch `26.3`, CurseForge-Projekt **690531**). Für Minecraft 26.3 ist daraus
ein komplettes Quest-Buch im Stil von FTB Quests geworden.

**Warum im eigenen Mod?** FTB Quests gibt es für Fabric nur bis 26.1.2, also nicht für 26.3. Dreamcraft braucht aber
eine Quest-Story. Quest Icons hatte schon ein CurseForge-Projekt und lässt sich per API hochladen, deshalb kam das
Quest-System dort hinein (siehe `dreamcraft/PLAN.md` im Archiv).

| Eckdaten | |
| --- | --- |
| Minecraft / Loader | 26.3, Fabric (Loader 0.19.5 oder neuer), Java 25, braucht Fabric API |
| Aktuelle Version | **1.1.0+26.3** (CurseForge-Datei 9429010) |
| Mod-ID / Paket | `questsicons` / `net.kasax.questsicons` |
| Port | von 1.21.1 (Yarn-Namen) auf 26.3 (offizielle Mojang-Namen) |
| Server | muss auf dem Server **und** auf jedem Client installiert sein |
| Quest-Dateien | `config/questsicons/quests` (SNBT, Aufbau wie bei FTB Quests) |

---

## 1. Das Quest-Buch für Spieler

### Öffnen
- Taste **J** (in den Steuerungs-Einstellungen änderbar; nochmal J schließt das Buch).
- Rechtsklick mit dem Item **Quest Book**. Jeder neue Spieler bekommt beim ersten Betreten eines eine
  (abschaltbar mit `give_book_on_first_join` in `data.snbt`).
- Im Inventar der kleine **✉-Knopf** oben links.
- Befehl `/quests open`.
- Seit 1.1.0 nennt der Tooltip des Quest Book die Taste, mit der es aufgeht.

### Aufbau
- **Links die Kapitelliste**, gruppiert in Kapitelgruppen (in Dreamcraft „✦ The Dream“ und „✦ Side Paths“).
- **Rechts die Quest-Karte** des gewählten Kapitels: ziehen verschiebt sie, das Mausrad zoomt.
  Abhängigkeits-Linien verbinden die Quests, Kapitel können Bilder auf der Karte zeigen.
- **Farben:** gesperrte Quests sind grau, erledigte grün, ein goldenes **!** zeigt Belohnungen, die auf dich warten.
- **Formen:** 10 Quest-Formen – circle, square, rounded square (`rsquare`), diamond, pentagon, hexagon, octagon,
  heart, gear und star. Ein Kapitel kann eine Standardform haben, jede Quest eine eigene Form und Größe.
- **Quest-Fenster:** Klick auf eine Quest öffnet Text, Aufgaben (Tasks) und Belohnungen (Rewards) mit Knöpfen
  *Submit*, *Done!*, *Claim*, *Choose*, *Pin* und *Close*.
- **Claim all (n)** in der oberen Leiste holt alles ab, was wartet – außer Auswahl-Belohnungen und Belohnungen mit
  `exclude_from_claim_all`.
- **Kapitel-Fortschritt:** Prozentanzeige; seit 1.1.0 steht dort 99 % statt eines Hakens, wenn noch eine Quest fehlt.
- **Toasts:** Ein Popup meldet „Quest completed!“ und „Chapter completed!“ (seit 1.1.0 nur von der Quest, die das
  Kapitel wirklich abschließt).

### Pins
- Im Quest-Fenster **Pin** klicken: bis zu 4 angeheftete Quests stehen oben links im Bildschirm, jeweils mit dem
  Fortschritt ihrer Aufgaben. **Unpin** nimmt sie wieder weg.
- Pins werden auf dem eigenen Rechner gespeichert, in `config/questsicons-pinned.txt`.

### Quests ohne Aufgabe
Eine Quest ohne Tasks schließt sich von selbst ab, sobald ihre Voraussetzungen erfüllt sind
(`QuestServer.java`, „tasks.isEmpty() … completeQuest“). Dreamcraft nutzt das z. B. für Kapitel-Starts wie
„The Dream Calls“ oder für „A Dragon's Treasure“ (eine von zwei Voraussetzungen reicht).

---

## 2. Alle Aufgaben-Typen (11)

| Typ (`type`) | Was der Spieler tun muss | Wichtige Felder |
| --- | --- | --- |
| `item` | Items im Inventar haben. Item-Tags gehen auch (`#minecraft:logs`). Mit `consume_items` werden sie über den Knopf **Submit** abgegeben. | `item`, `count`, `consume_items`, `match_components` |
| `checkmark` | Nur ein Häkchen setzen (Knopf **Done!**). | `title` |
| `kill` | Eine Anzahl Mobs eines Typs oder eines Entity-Tags besiegen. | `entity`, `value` |
| `advancement` | Einen Fortschritt (Advancement) erreichen, oder nur eines seiner Kriterien. | `advancement`, `criterion` |
| `dimension` | Eine Dimension betreten. | `dimension` |
| `biome` | Ein Biom oder einen Biom-Tag finden. | `biome` |
| `structure` | In einer Struktur stehen, z. B. einem Dorf (auch Struktur-Tags). | `structure` |
| `xp` | Eine Anzahl Level oder XP-Punkte erreichen, oder per Knopf bezahlen. | `value`, `points`, `consume` |
| `stat` | Einen Statistik-Wert erreichen, z. B. Sprünge oder gelaufene Zentimeter. | `stat`, `value` |
| `observation` | Einen Block oder Mob eine Weile ansehen. | `observe`, `entity`, `timer` (Ticks) |
| `location` | Einen Ort in einer Dimension erreichen (mit Radius). | `dimension`, `x`, `y`, `z`, `radius` |

Seit 1.1.0 gilt: Steht in einer Aufgabe ein Tippfehler (falscher Tag, Mob, Biom, Struktur, Statistik oder
Advancement), wird die Aufgabe mit **einer** Meldung im Log abgeschaltet, statt jeden Tick Fehler zu werfen – bis
`/quests reload`.

## 3. Alle Belohnungs-Typen (8)

| Typ (`type`) | Was der Spieler bekommt |
| --- | --- |
| `item` | Ein beliebiges Item in beliebiger Menge |
| `xp` | XP-Punkte |
| `xp_levels` | XP-Level |
| `command` | Führt einen Befehl für den Spieler aus; Platzhalter `{p}`, `{x}`, `{y}`, `{z}`, `{quest}`. Im Buch steht „Surprise!“ |
| `random` | Ein gewichteter Zufallsgriff aus einer Reward-Tabelle |
| `choice` | Der Spieler wählt eines von mehreren Items (Knopf **Choose**, Auswahlfenster „Pick one reward“) |
| `loot` | Würfelt eine Loot-Tabelle aus (Vanilla oder aus einem Datapack) |
| `advancement` | Vergibt ein Advancement |

- Eine Belohnung kann **pro Spieler** oder **einmal für das ganze Team** gelten (`team_reward`; Standard für das Buch
  über `default_reward_team`) und **automatisch** abgeholt werden (`auto`).
- Seit 1.1.0: Ein Eintrag, der ein nicht existierendes Item nennt (Tippfehler, entfernte Mod), gibt **keinen
  Barrier-Block** mehr aus; die Kiste bleibt zu und das Log nennt den kaputten Eintrag.

## 4. Loot Crates und Mystery Reward

### Loot Crates (vier Stufen)
| Item | Seltenheit | Tabelle |
| --- | --- | --- |
| Common Loot Crate | gewöhnlich | `reward_tables/common_crate.snbt` |
| Rare Loot Crate | ungewöhnlich | `reward_tables/rare_crate.snbt` |
| Epic Loot Crate | selten | `reward_tables/epic_crate.snbt` |
| Legendary Loot Crate | episch | `reward_tables/legendary_crate.snbt` |

- Rechtsklick öffnet die Kiste und gibt einen zufälligen Eintrag ihrer Tabelle („You found 3x …!“).
- Eine Reward-Tabelle ist eine Liste aus Item, Anzahl und Gewicht. Höheres Gewicht = wahrscheinlicher.
- **Das Pack füllt die Tabellen**, deshalb passen die Kisten in jedes Modpack. Fehlt eine Tabelle, sagt die Kiste,
  dass sie leer ist, und bleibt in der Hand.
- Kisten sind normale Items und taugen deshalb selbst als Quest-Belohnung.
- Seit 1.1.0 kommen große Belohnungen in normalen Stapeln.
- Was in Dreamcraft in den vier Tabellen liegt, steht in [01_dreamcraft.md](01_dreamcraft.md#loot-kisten-in-dreamcraft).

### Mystery Reward (`questsicons:quest_reward`)
- Die frühere „Treasure Chest“ heißt in 26.3 **Mystery Reward**.
- **5 Nutzungen**; jeder Rechtsklick gibt 1 bis 3 eines zufälligen Items aus dem ganzen Spiel (jede Mod zählt mit).
- **Keine Preise sind:** Luft, Barriere, Licht, Strukturleere, Debug-Stick, Wissensbuch, Grundgestein,
  Endportalrahmen, verstärkter Tiefenschiefer, Spawner, Trial Spawner, Vault, knospender Amethyst, versteinerte
  Eichenstufe, alle Operator-Blöcke (Befehlsblöcke usw.), Items abgeschalteter Experimente, Quest Icons' eigene Items
  und alles mit `spawn_egg`, `command`, `creative` oder `debug` im Namen. (Die Sperrliste kam mit 1.1.0.)

---

## 5. Teams

- Jeder Spieler startet in einem **eigenen Team**.
- `/quests team create <Name>` gibt dem Team einen Namen; wer in einem geteilten Team ist, startet damit ein neues.
- `/quests team invite <Spieler>` lädt ein; der Eingeladene tritt mit `/quests team join <dein Name>` bei. Seit 1.1.0
  lässt sich die Einladung im Chat **anklicken**.
- Team-Mitglieder teilen Aufgaben-Fortschritt und erledigte Quests. Wer beitritt, **ersetzt seinen eigenen
  Fortschritt durch den des Teams**.
- Belohnungen holt jeder selbst ab – außer Team-Belohnungen, die einmal für alle zählen.
- `/quests team info` zeigt Team, Mitglieder und erledigte Quests; `/quests team leave` verlässt das Team (man
  beginnt mit leerem eigenem Fortschritt).

## 6. Alle Befehle

| Befehl | Wer | Wirkung |
| --- | --- | --- |
| `/quests open` | alle | öffnet das Buch |
| `/quests reload` | OP (Level 2) | lädt die Quest-Dateien neu von der Platte |
| `/quests givebook <Spieler>` | OP | gibt ein Quest Book |
| `/quests complete <Quest\|all> [Spieler]` | OP | erledigt eine Quest oder alle |
| `/quests reset <Quest\|all> [Spieler]` | OP | setzt eine Quest oder den ganzen Fortschritt zurück |
| `/quests team info \| create \| invite \| join \| leave` | alle | Teams (siehe oben) |

`/questbook` funktioniert genauso wie `/quests` (Weiterleitung). Quelle: `server/QuestCommands.java`.

---

## 7. Für Pack-Macher: Editor und SNBT-Dateien

### Dateien (Aufbau wie FTB Quests)
```
config/questsicons/quests/
  data.snbt              Buch-Einstellungen
  chapter_groups.snbt    Kapitelgruppen
  chapters/<name>.snbt   ein Kapitel pro Datei
  reward_tables/<name>.snbt  Reward-Tabellen (auch die der Loot Crates)
```
- Beim ersten Start schreibt der Mod ein kleines Beispielkapitel.
- Kommas zwischen Einträgen sind optional. IDs sind 16-stellige Hex-Zahlen oder ein beliebiger lesbarer Name.
- Texte können `&`-Farbcodes, Übersetzungsschlüssel in geschweiften Klammern (`{mypack.quest.title}`) und JSON-Text.
- Beschreibungen können Bilder zeigen: `{image:namespace:path.png width:120 height:60}`.
- **`data.snbt`:** `title`, `icon`, `default_quest_shape`, `default_reward_team`, `give_book_on_first_join`,
  `background`.
- **Kapitel:** `id`, `filename`, `title`, `subtitle`, `icon`, `group`, `order_index`, `default_quest_shape`,
  `hide_until_startable`, `quests`, `images`.
- **Quest:** `id`, `title`, `subtitle`, `icon`, `x`, `y`, `shape`, `size`, `dependencies`,
  `dependency_requirement` (`all_completed` oder `one_completed`), `optional`, `hide_until_deps_complete`,
  `hide_dependency_lines`, `invisible`, `disable_toast`, `description`, `tasks`, `rewards`.
- Nach Änderungen an den Dateien: `/quests reload`. Jede Änderung geht sofort an alle Spieler.
- Seit 1.1.0 überschreiben sich von Hand geschriebene Quests ohne ID nicht mehr gegenseitig.

### Der Editor im Spiel
- Operatoren (Level 2) sehen oben im Buch den Knopf **Edit**.
- Im Edit-Modus zieht man Quests auf der Karte herum.
- **Rechtsklick auf eine Quest:** als SNBT bearbeiten, Abhängigkeit hinzufügen/entfernen (danach die Quest anklicken,
  die vorher fertig sein muss; Esc bricht ab), alle Abhängigkeiten löschen, Icon = Item in der Hand, Item-Aufgabe
  oder Item-Belohnung aus dem Item in der Hand, Häkchen-Aufgabe, 100-XP-Belohnung, Form wechseln, duplizieren,
  löschen.
- **Rechtsklick auf eine freie Stelle:** neue Quest, Kapitel-Einstellungen (SNBT), „Reload files from disk“.
- **Kapitelliste:** „+ New chapter“; Rechtsklick auf ein Kapitel: verschieben, Einstellungen, Icon, löschen (mit Shift,
  wenn es noch Quests hat).

### Wie Dreamcraft seine Quests schreibt
Dreamcraft schreibt die SNBT-Dateien nicht von Hand, sondern mit einem Generator im Modpack-Repo
(`tools/dc_quests.py`, `dc_quests_raft.py`, `dc_quests_pets.py`, Bibliothek `qlib.py`). Die Quest-IDs sind
FNV-1a-Hashes von „Kapitel:Quest-Schlüssel“ und bleiben deshalb stabil. Details in
[01_dreamcraft.md](01_dreamcraft.md#9-die-quests).

---

## 8. Die 32 Icons

Alle liegen im Creative-Tab **Quest Icons**, stapeln sich nicht (1 pro Slot) und taugen als Icon für Quests und
Kapitel – oder als Belohnung. Die ersten zwölf gab es schon vor 26.3, die zwanzig `icon_*` kamen mit 1.0.0 dazu.

| ID | Name im Spiel | Bedeutung |
| --- | --- | --- |
| `chapter_lock` | Chapter Lock | Schloss für gesperrte Kapitel |
| `end_lock` | End Lock | Schloss im End-Stil |
| `quest_backpack` | Backpack Icon | Rucksack |
| `quest_crown` | Crown Icon | Krone – in Dreamcraft die **Quest Crown**, Zutat des Dream Star |
| `quest_dungeon` | Dungeon Icon | Dungeon |
| `quest_key` | Key Icon | Schlüssel |
| `quest_portal_one` | Green Portal Icon | grünes Portal |
| `quest_portal_two` | Purple Portal Icon | lila Portal |
| `quest_portal_three` | Blue Portal Icon | blaues Portal |
| `quest_portal_four` | Yellow Portal Icon | gelbes Portal |
| `quest_portal_five` | Grey Portal Icon | graues Portal |
| `logo_fabric` | Dreamcraft Logo | das Dreamcraft-Logo |
| `icon_compass` | Compass Icon | Kompass |
| `icon_sword` | Sword Icon | Schwert |
| `icon_shield` | Shield Icon | Schild |
| `icon_pickaxe` | Pickaxe Icon | Spitzhacke |
| `icon_magic` | Magic Orb Icon | Magiekugel |
| `icon_gear` | Gear Icon | Zahnrad |
| `icon_house` | House Icon | Haus |
| `icon_food` | Food Icon | Essen |
| `icon_map` | Map Icon | Karte |
| `icon_star` | Star Icon | Stern |
| `icon_trophy` | Trophy Icon | Pokal |
| `icon_skull` | Skull Icon | Totenkopf |
| `icon_heart` | Heart Icon | Herz |
| `icon_question` | Question Icon | Fragezeichen |
| `icon_exclamation` | Exclamation Icon | Ausrufezeichen |
| `icon_raft` | Raft Icon | Floß |
| `icon_potion` | Potion Icon | Trank |
| `icon_chest` | Chest Icon | Truhe |
| `icon_tree` | Tree Icon | Baum |
| `icon_moon` | Moon Icon | Mond (Icon von Dreamcraft-Prolog und Story-Gruppe) |

Weitere Items des Mods: **Quest Book**, die vier **Loot Crates**, **Mystery Reward**, **Dream Star** und
**Dream Star Pedestal** (siehe nächster Abschnitt). Wer ein eigenes Icon will, kann laut Beschreibung Pixel-Art
schicken („giant collaboration of icons“).

---

## 9. Der Dream Star und sein Sockel (neu in 1.1.0)

Der **Dream Star** ist die End-Trophäe von Dreamcraft – wie der ATM Star der All-The-Mods-Packs. Tooltip: „Proof
that you finished Dreamcraft“.

**Eigenschaften (aus Code und Changelog):**
- stapelt nicht (1), Seltenheit episch, glänzt, animierte leuchtende Textur;
- fallengelassen verbrennt er nicht in Feuer oder Lava, übersteht Explosionen, Kaktus und Blitz
  (Damage-Tag `questsicons:dream_star_immune`) und **verschwindet nie**;
- das Herstellen schaltet die Challenge **„Living the Dream“** frei (Advancement `questsicons:dream_star`).

### Rezept in Dreamcraft
Es gibt das Rezept nur, wenn **alle** Mods `techreborn`, `mythicupgrades`, `wizards`, `paladins`, `raft` und
`tamagotchi` geladen sind und alle Zutaten-IDs existieren (Fabric-Ladebedingung).

```
Ametrine Ingot   | Quest Crown        | Ametrine Ingot
Netherite-Stab   | Nether Star        | Lapotronic Energy Orb
Tamagotchi Heart | Dragon Egg / Head  | Heart of the Tide
```

| Zutat | Mod | Woher in Dreamcraft |
| --- | --- | --- |
| 2× Ametrine Ingot | Mythic Upgrades | 4 Ametrine (End) + 4 Necoium Ingots ergeben 1 Barren |
| Quest Crown | Quest Icons | kein Rezept – Belohnung der Quest „Master of Dreams“ (sie gibt zwei) |
| Netherite Arcane/Fire/Frost Staff **oder** Netherite Holy Staff | Wizards bzw. Paladins & Priests | Kapitel 4 „Paths of Power“ |
| Nether Star | Minecraft | den Wither besiegen |
| Lapotronic Energy Orb | Tech Reborn | Spitze von Tech Reborn, Kapitel 3 |
| Tamagotchi Heart | Tamagotchi | 5 rote Farbe um eine Amethystscherbe |
| Dragon Egg **oder** Dragon Head | Minecraft | Ei nach dem ersten Drachenkampf, Kopf am Bug jedes End-Schiffs |
| Heart of the Tide | Beach Craft | Beute des Bosses Leviathan (Kapitel 6) |

### Rezept überall sonst (ohne diese Mods)
```
Totem of Undying        | Dragon Egg / Head | Totem of Undying
Block of Netherite      | Nether Star       | Block of Netherite
Enchanted Golden Apple  | Heavy Core        | Enchanted Golden Apple
```
Die beiden Rezepte schließen sich gegenseitig aus. Im laufenden Dreamcraft-V1.3-Testclient hat der Registry-Dump
bestätigt: `dream_star` geladen, `dream_star_vanilla` nicht geladen, `dream_star_pedestal` geladen.

### Dream Star Pedestal
```
Gold Ingot          | Amethyst Shard      | Gold Ingot
                    | Quartz Pillar       |
Polished Blackstone | Polished Blackstone | Polished Blackstone
```
- Rechtsklick mit dem Stern legt ihn auf den Sockel: Er **schwebt, dreht sich langsam, funkelt** und der Sockel
  leuchtet mit Lichtstufe 15.
- Mit leerer Hand nimmt man ihn zurück. Wird der Sockel abgebaut, fällt der Stern heraus; der Sockel droppt sich
  selbst. Trichter können den Stern nicht herausziehen, Kolben schieben den Sockel nicht.
- Das Rezept des Sockels wird freigeschaltet, sobald man einen Dream Star hat.

---

## 10. Versionen

| Version | CurseForge-Datei | Datum | Was |
| --- | --- | --- | --- |
| **1.0.0+26.3** | 9402494 | 2.11.2026 | Port auf 26.3 und das komplette Quest-System: Kapitel und Gruppen, Karten mit 10 Formen, Linien und Bildern; 11 Aufgaben- und 8 Belohnungs-Typen; Teams, „Claim all“, Toasts, Pins; SNBT-Dateien; Editor; Quest Book, vier Loot Crates und 20 neue Icons |
| **1.0.1+26.3** | 9409345 | 2.11.2026 | Wer mit `/quests team join` einem Team beitrat, bekam beim nächsten Login ein zweites Quest Book. Das Team merkt sich jetzt, dass der Spieler schon eines hat. |
| **1.0.2+26.3** | 9415031 | 3.11.2026 | **Hotfix:** Klicks im Quest-Buch gingen nicht (siehe unten). |
| **1.1.0+26.3** | 9429010 | 3./4.11.2026 | Dream Star und Pedestal; Escape schließt zuerst das offene Fenster; keine Klicks mehr „durch“ Auswahlfenster und Menüs; weggescrollte Knöpfe reagieren nicht mehr; Team-Reparatur nach Server-Neustart; kaputte Aufgaben werden abgeschaltet statt Log-Spam; Quests ohne ID überschreiben sich nicht; XP-Aufgaben zählen die aktuellen XP; 99 % statt Haken; Mystery Reward ohne Creative-Blöcke; Loot Crates in normalen Stapeln; kein Barrier-Block für unbekannte Items |

Die Changelogs liegen in `docs/curseforge/changelog-<version>.md` im Mod-Repo. Dreamcraft nutzte 1.0.0 (V1, V1.1),
1.0.1 (V1.2), 1.0.2 (V1.2.1); V1.3 (4.11.2026) nutzt 1.1.0.

### Wie es zum Hotfix 1.0.2 kam
1. **Das Symptom:** Spieler meldeten im Discord (Dreamcraft V1.2 mit Quest Icons 1.0.1), dass sie keine Quest öffnen
   konnten.
   Die erste Prolog-Quest („I am ready to dream“) und die Klassenwahl ließen sich nicht abhaken, Belohnungen nicht
   abholen. Ein Linksklick verschob nur die Karte.
2. **Die Ursache:** Minecraft 26.3 nutzt für Eingaben **SDL statt GLFW**. Dort ist die linke Maustaste **1**, die
   mittlere 2 und die rechte 3 (bei GLFW war links 0). Das Buch prüfte noch `button == 0`. Ein Linksklick kam also nie
   als Linksklick an.
3. **Warum es vorher nicht auffiel:** Die automatischen Tests öffneten Quests per Methodenaufruf, nicht mit echten
   Mausklicks. Der Code war deshalb „grün“, obwohl kein Mensch klicken konnte.
4. **Der Fix:** Links-, Rechts- (Edit-Menüs) und Mittelklick (Karte verschieben) nutzen jetzt
   `InputConstants.MOUSE_BUTTON_LEFT/RIGHT/MIDDLE`. Quest-Fortschritt blieb erhalten.
5. **Auslieferung:** Quest Icons 1.0.2 (Datei 9415031), sofort danach **Dreamcraft V1.2.1** (Datei 9415062,
   Server-Pack 9415063) mit Dank an den Discord im Changelog.
6. **Die Lehre:** Eigene Oberflächen immer mit **echten Klicks** testen (Cursor setzen und
   `pressMouse(InputConstants.MOUSE_BUTTON_LEFT)`), nie mit festen GLFW-Zahlen arbeiten. Dieselbe Falle traf in 1.1.0
   die Escape-Taste (GLFW 256, SDL 41) und in Tamagotchi und Challenge Craft weitere Screens. Seit 1.1.0 klickt der
   Selbsttest (`./gradlew runSelftest`, Quelle `src/selftest`) jeden Knopf des Buches wirklich: Aufgabe, Claim,
   Pin/Unpin, Close, Choose, Auswahlfenster, Escape und das Edit-Menü; außerdem Stern und Sockel im Überlebensmodus,
   in Lava, bei TNT, beim Droppen und die Rezepte.

---

## 11. Beschreibung auf CurseForge

`docs/curseforge/description.html` im Mod-Repo (Branch `26.3`), im Stil deiner alten Seite: Logo-Bild,
„Made with love, sweat and tears“, Bisect-Banner und deine Abschnittsbilder (imgur), dazu drei Screenshots
(`docs/curseforge/img/book.png`, `quest.png`, `icons.png`) und **10 Spoiler-Boxen** (Screenshots, Öffnen, Befehle,
Aufgaben- und Belohnungs-Typen, Kisten, Teams, Pins, Dream-Star-Rezepte, Quest-Dateien, Editor). Einfügen von Hand,
siehe [06_videos_und_beschreibungen.md](06_videos_und_beschreibungen.md).
