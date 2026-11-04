# 07 – Wichtige Entscheidungen und technische Lehren

## 1. Entscheidungen und warum

### Modpack Dreamcraft
| Entscheidung | Warum |
| --- | --- |
| **Quest-System in Quest Icons statt FTB Quests** | FTB Quests gibt es für Fabric nur bis 26.1.2. Quest Icons hatte schon ein CurseForge-Projekt und lässt sich per API hochladen. |
| **Quests per Generator** (`dc_quests*.py`) statt von Hand | 328 Quests bleiben einheitlich, jede ID lässt sich automatisch prüfen (`qcheck.py`), Änderungen sind reproduzierbar. |
| **Quest-IDs als FNV-1a-Hash** von „Kapitel:Schlüssel“, neue Belohnungen nur ans Ende | Der Fortschritt der Spieler bleibt bei jedem Update erhalten; so konnte „Master of Dreams“ eine zweite Krone bekommen, die auch alte Spieler abholen. |
| **REI ersetzt durch JEI + Just Enough Professions** | REI 26.3 konnte die datengetriebenen Brau-Rezepte (557) und den Kochtopf von Farmer's Delight (27) nicht anzeigen – Hunderte Fehler. |
| **Just Enough Resources entfernt** (V1.2) | Sein JEI-Plugin scheitert an BetterNethers Biomen und zeigte keine einzige Seite. |
| **Mods mit frühen Mixin-Konflikten entfernt** (FrozenLib mit Wilder Wild und Simple Copper Pipes, ModernFix-mVUS, Cherished Worlds/SpectreLib) | Sie laden Chat-Klassen schon im preLaunch; dann schlagen die Mixins anderer Mods fehl und der Client startet nicht. |
| **Mods mit Registry-Fehlern entfernt** (MCPitanLib, Enhanced Quarries, Display Case) | Sie schreiben Rezept-JSON global um oder nutzen alte Formate – der Server startet nicht. |
| **Shader eingebaut, aber aus** | Gut für starke PCs, ohne schwache PCs auszubremsen. |
| **Start in der Ego-Sicht** (V1.2) | Shoulder Surfing setzte neue Spieler in die Schulterkamera; F5 geht weiterhin. |
| **Menü mit Autoscale** (V1.2) | Bei 854×480 war kein Knopf klickbar, bei 1366×768 fehlte „Quit Game“. |
| **Jede Version erst wie ein Spieler installieren** (`tools/prodtest`) | Der Loom-Test ist eine Entwicklungsumgebung und zeigt nicht alles, was Spieler sehen (er fand die Menü-Fehler von V1.1). |
| **Reihenfolge: erst Mod hochladen, Freigabe abwarten, dann Pack** | Eine neue CurseForge-Datei ist erst nach rund 10 Minuten Prüfung herunterladbar; ein Pack, das sie früher referenziert, wäre kaputt. |
| **Tamagotchi als normale CurseForge-Datei im Manifest** | Das Pack zieht die veröffentlichte Datei; `mkpack.py` nimmt eine andere Datei-ID als viertes Argument (z. B. 1.2.0). |
| **Dream Star braucht Zutaten aus allen Ecken des Packs**, mit Ladebedingung und Ersatzrezept | Er soll beweisen, dass man das ganze Pack gespielt hat (wie der ATM Star). In anderen Packs fehlen die Mods – dort gilt ein teures Vanilla-Rezept. |
| **„Master of Dreams“ gibt zwei Quest Crowns** | Der Stern verbraucht eine, die andere bleibt als Trophäe. |

### Beach Craft
| Entscheidung | Warum |
| --- | --- |
| **Eigenes Treibholz-Portal** | Die Custom Portal API gibt es für 26.3 nicht. Treibholz an Oberwelt-Stränden, 4 Rahmen pro Rezept und Ringe im Loot machen es überhaupt erreichbar. |
| **Archipel statt Oberwelt-Gelände** (3.0) | Die alte Dimension kopierte die Oberwelt-Form mit Meeresspiegel 100 – riesige Steinmassive im „endlosen Meer“ (Design-Frage aus dem 2.0.1-Review). |
| **Raft-Dimension dunkler** (Umgebungslicht 0 wie die Oberwelt) | Vorher war alles immer voll hell: der Graben, die Tiefsee und Räume waren nie dunkel, Leuchtpflanzen fielen nicht auf. Die Sonne steht weiter fest, deshalb bleibt die Oberfläche hell. Folge: Licht mitnehmen oder Helmlampe – deshalb kam die Helmlampe dazu. |
| **16×16-Texturen im Vanilla-Stil** | Qualität durch gute Pixel-Art statt Auflösung; alles passt zu Vanilla und den anderen Mods. Auch die 2.0-Texturen wurden in diesem Stil neu gezeichnet. |
| **Story mit hartem Gating, aber ohne Sackgassen** | Der Boss soll erst nach der Story kommen (unzerstörbares Sanktum, Schlüssel nur aus vier Sigils). Damit niemand hängen bleibt, hat jede Truhe eine Karte und das Journal zeichnet neue. |
| **Module mit festen Besitzern, Ressourcen per Python** | Mehrere Agenten bauten parallel; jedes Modul ändert nur seine Dateien. Der Resource-Merge bricht bei doppelten Dateien ab, statt still zu überschreiben. Generatoren sind wiederholbar und prüfbar. |
| **Haie beißen Flöße, verstärkte Fundamente nicht; Spielregel zum Abschalten** | Spannung wie in Raft, aber mit Ausweg; Server können es mit `/gamerule raft:shark_bites false` abstellen. |
| **Boss-Infos nur hinter Spoilern** (Almanac, CurseForge, Doku) | Die Überraschung bleibt für die, die sie wollen. |

### Arbeitsweise und Veröffentlichen
| Entscheidung | Warum |
| --- | --- |
| **Höchstens 4 Agenten gleichzeitig** (dein Wunsch), Arbeit vorher in WIP-Commits sichern | Nutzungslimit; mehrere Pausen durch das Limit verloren so keine Arbeit (die WIP-Commits sieht man in jedem Repo). In der ersten Dreamcraft-Runde war es höchstens ein Subagent. |
| **CurseForge-Beschreibungen von Hand einfügen** | Für Projektbeschreibungen gibt es keine API. Deshalb liegt jede als fertiges HTML für die Quellcode-Ansicht im Repo. |
| **Server-Pack von Hand markieren** | `isServerPack` wird beim API-Upload ignoriert. |
| **Challenge Craft: Fixes nur auf einem Branch, keine Versionsänderung** | Jede Änderung von `mod_version` auf `26.3`/`26.3-lockout-bot` veröffentlicht automatisch – das braucht dein Go. |
| **Tamagotchi 1.2.0 nicht selbst veröffentlicht** | Release läuft über Tag/Workflow; eine Sitzung darf keine Tags pushen und ein Release ist nach außen sichtbar. |
| **Beach Craft 3.0.0 nicht hochgeladen** | Das Berechtigungssystem hat den Upload blockiert – du entscheidest. |
| **Kein CurseForge-Token in Dateien oder Ausgaben** | Er liegt nur in `$SP/.cf_token` außerhalb der Repos. |
| **Videos mit echten Spielgeräuschen** (Reviews) und Shadern (TikTok v2) | Reviews sollen zeigen, wie es sich wirklich anhört; der TikTok soll so schön wie möglich aussehen. |
| **Bob immer als „early stage of development“** | Deine Vorgabe für alles Öffentliche zu Challenge Craft. |

---

## 2. Technische Lehren

### Minecraft 26.3 und SDL
- **26.3 nutzt SDL statt GLFW für Eingaben.** Maustasten: links = **1**, Mitte = 2, rechts = 3 (GLFW: links 0). Escape ist
  **41** (GLFW 256). Nie feste Zahlen verwenden, immer `InputConstants.MOUSE_BUTTON_LEFT/RIGHT/MIDDLE` bzw. die
  Tasten-Konstanten. Das hat das Quest-Buch (Hotfix 1.0.2), Escape in Quest Icons (1.1.0), das Tamacon von Tamagotchi
  und den Film-Harness von Challenge Craft getroffen.
- **Oberflächen mit echten Klicks testen** (Cursor setzen + `pressMouse(InputConstants.MOUSE_BUTTON_LEFT)`), nicht per
  Methodenaufruf. Im Gametest hat `pressMouse(1)` Blöcke abgebaut (Truhe zerbrochen) – Klicks deshalb über die
  Tastenbelegung auslösen: `pressKey(o -> o.keyUse)` bzw. `holdKey(o -> o.keyAttack)`.
- 26.3-Eigenheiten beim Modden: Blöcke und Items brauchen `properties.setId(key)` vor dem Bau; Item-Modelle sind
  `assets/<ns>/items/<id>.json`; Rüstungen über `assets/<ns>/equipment/<material>.json`; Spawn-Eier über
  `Item.Properties().spawnEgg(TYPE)`; Ofen-Brennstoff über `cookingFuel(...)`; kein `BlockRenderLayerMap` (die
  Render-Schicht kommt aus den Textur-Pixeln); `Identifier` statt `ResourceLocation`; Entity-Renderer mit Render-States.
- **Spielregeln sind Registry-IDs in Kleinbuchstaben** (`raft:shark_bites`, nicht `raftSharkBites`).
- **Eine unbekannte Item-ID in irgendeiner Loot-Tabelle** stoppt das Laden der ganzen Welt; ebenso **eine unbekannte
  Entity-ID in einer Biom-Datei**. Lösung: optionale Ein-Item-Tags in Loot-Tabellen, `fabric:registry_contains` für
  Rezepte, Kreaturen-Spawns per Fabric-Biom-Modifikation.
- 26.3 liest `minecraft:is_ocean`/`is_deep_ocean`/`is_beach` nicht mehr so wie früher – sie würden der Raft-Dimension
  nur Vanilla-Monumente, Ozeanruinen und Ruinenportale bringen.
- Vanilla lädt den Zustand „Sitting“ ohne `setOrderedToSit` (der Pet-Screen von Tamagotchi zeigte nach dem Laden
  nicht „Sit“);
  `minecraft:chain` heißt in 26.3 `minecraft:iron_chain` (Challenge Craft).

### Strukturen
- **Blöcke ohne `rotate()`/`mirror()`** (z. B. `BaseEntityBlock` mit FACING) drehen sich bei gedrehten Jigsaw-Starts
  nicht mit – der Leviathan-Altar zeigte in 3 von 4 Drehungen ins Leere. Behoben für Altar und Research Terminal.
- Ein Jigsaw-Start mit fester Höhe liegt **einen Block unter** `start_height` (Ground-Level-Delta) – feste Höhen deshalb
  um eins höher schreiben.
- **Teppiche und Fackeln in gefluteten Strukturen** werden weggespült (Items liegen herum) – Wolle statt Teppich.
- Große Bauten über 48 Blöcke gehen als einzelne Jigsaw-Vorlage; trockene Räume unter Wasser müssen ganz geschlossen
  sein und Luft enthalten; `ignore_waterlogging` mit selbst gesetzten `waterlogged`-Flags hält sie trocken.
- `beard_box` schnitt rechteckige Gräben in Nachbarinseln – die Piratenbucht nutzt deshalb `none` mit eigenem
  Felshügel.
- Strukturdateien mit gzip-mtime 0 schreiben, dann ergeben gleiche Builds gleiche Dateien.

### Licht, Spawns, Items
- **Dimension-Licht:** `ambient_light` 0.0 und `ambient_light_color` #0a0a0a wie die Oberwelt, sonst ist alles immer hell.
  Vanilla hellt Wasser-Nebel nach ein paar Sekunden auf (Kanal-Skalierung) – Tiefsee-Nebel ohne Rotanteil wählen.
- **Spawn-Limits:** Kreaturen-Dichte über Spawn-Kosten (Fabric `addMobCharge`), sonst füllen Korsaren, Wale oder Mantas
  die Caps; das gemeinsame Limit unter Wasser ist schnell voll (Leuchttintenfische im Graben).
- In einer immer hellen Dimension lehnt die Monster-Lichtprüfung jeden natürlichen Spawn ab (Hai in 2.0.0).
- **`/give` erzeugt zuerst ein Fake-Item** (Alter 5999). Ein Despawn-Schutz im ENTITY_LOAD-Event muss es auslassen, sonst
  schwebt ein Geister-Stern bzw. Geister-Sigil für immer am Boden.
- Was der Client steuert, muss auf dem Client passieren: Der Paddel-Schub kam nur beim Server an, Boote steuert aber
  der Client.

### Testen und Filmen im Container
- **Speicherleck der Fabric-Gametest-API 6.0.11:** `takeScreenshot` gibt das `NativeImage` nie frei (8 MB pro Bild bei
  1080×1920); nach ~600 Bildern beendete der OOM-Killer den Client. Behoben mit `mixin/ScreenshotLeakMixin`;
  trotzdem in Batches zu 5–7 Shots filmen.
- Der integrierte Server tickt in Echtzeit weiter, während ein Bild 0,5–2 s braucht – Öfen, Wachstum, Treibgut und
  Portale laufen pro Filmsekunde 3–5-mal schneller. Sichtbare Abläufe erst im Shot starten.
- Koordinaten nie als `"%d.5"` formatieren (bei negativen Werten einen halben Block daneben), sondern `%.1f` mit `+0.5`.
- `tp … facing <Ziel>` setzt das Ziel genau hinter die Figur – Kamera seitlich versetzen. Luftaufnahmen: Spieler auf
  einen Barriere-Block stellen (Fliegen hielt nicht).
- Shader auf llvmpipe: 5–7 s pro Bild, Client braucht 10–13 GB; das End mit Shadern hing; mehr als 6 GB Heap führte
  einmal zum SIGKILL.
- Der Testrechner ist langsam (neues Gebiet 3–5 min bei Sichtweite 8): `rd 5`, Läufe bündeln; höchstens 2 JVMs
  gleichzeitig, nie `pkill -f` mit einem Muster aus dem eigenen Befehl.

### Mods im Pack
- Mods, die im preLaunch Chat-Klassen laden, zerstören die Mixins anderer Mods (FrozenLib, ModernFix-mVUS, SpectreLib).
- Iceberg bringt eine alte NightConfig mit, die jede Fuzs-Config zum Absturz bringt.
- Mods, die Rezept-JSON global umschreiben (`item`→`id`), zerstören die Daten anderer Mods.
- FancyMenu: Beim Neuvergeben von IDs muss dieselbe UUID immer dieselbe neue ID bekommen, sonst verlieren Knöpfe ihre
  Aktion; der Vanilla-Ladebalken ignoriert Farben.
- CurseForge ersetzt Leerzeichen in Dateinamen durch Bindestriche; der Anzeigename behält sie.
