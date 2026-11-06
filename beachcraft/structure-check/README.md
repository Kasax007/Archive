# Strukturprüfung Beach Craft 3.1 (6.11.2026)

Alle 19 Strukturen der Endless Sea wurden in zwei frischen Welten (Seeds `bcaudit1` und `tides2`) an je fünf Orten
erzeugt und Block für Block mit ihren Vorlagen verglichen. Dazu wurde jede Person geprüft: Füße und Kopf frei, Boden
darunter, nicht im Wasser, keine doppelten. Auch herumliegende Items und lose Blöcke wurden gezählt. Werkzeug:
`bctest audit` im Mod-Repo (`src/gametest/java/net/kasax/raft/gametest/StructAudit.java`), Skripte in `tools/`.

## Vorher (Stand 3.1.0 vor der Prüfung, 95 Strukturen)

| Struktur | Orte | Fremdblöcke in Räumen | Wasser/Lava in Räumen | Pflanzen in Räumen | NPC in Ordnung | Items |
|---|---|---|---|---|---|---|
| abandoned_raft | 5 | 0 | 0 | 0 | – | 0 |
| abyssal_sanctum | 5 | 106 | 615 | 7 | – | 1 |
| ashen_forge | 5 | 11046 | 0 | 1 | 3/5 | 11 |
| beach_shack | 5 | 0 | 0 | 0 | 5/5 | 0 |
| buoy_field | 5 | 0 | 0 | 0 | – | 0 |
| castaway_camp | 5 | 0 | 0 | 0 | 2/2 | 0 |
| coral_temple | 5 | 0 | 0 | 0 | – | 0 |
| helix_station | 5 | 53 | 51 | 2 | – | 1 |
| iceberg_outpost | 5 | 0 | 0 | 0 | 5/5 | 0 |
| old_lighthouse | 5 | 14 | 0 | 22 | 5/5 | 0 |
| pirate_cove | 5 | 0 | 0 | 4 | – | 5 |
| port_solace | 5 | 0 | 0 | 0 | – | 7 |
| rusted_rig | 5 | 0 | 0 | 0 | 5/5 | 2 |
| saltmere_village | 5 | 49 | 0 | 33 | 10/10 | 3 |
| sunken_plane | 5 | 0 | 12 | 0 | – | 0 |
| sunken_ruins | 5 | 0 | 0 | 0 | – | 0 |
| wreck_cargo_ship | 5 | 0 | 0 | 0 | – | 0 |
| wreck_fishing_boat | 5 | 0 | 0 | 0 | – | 42 |
| wreck_galleon | 5 | 0 | 0 | 0 | – | 2 |

„Fremdblöcke in Räumen“ = Blöcke, wo die Vorlage Luft hat (Basalt, Bäume, Teile anderer Strukturen).

## Gefunden und behoben (Branch `fix/structure-features`, in 26.3 = 88ce4aa)

| Fund | Ursache | Fix |
| --- | --- | --- |
| Ashen Forge voll Basalt (1.645–2.875 Blöcke), Voss im Basalt, erstickte Glutkrabben (Items am Boden), Asche in den Wänden, Lava | Features laufen nach der Struktur im selben Schritt und aus Nachbar-Chunks | Filter `raft:clear_of_structures` an allen Gelände-Features |
| Rusted Rig auf dem Abyssal Sanctum (615 Wasser im Sanctum), fremde Teile in Helix und Port Solace | Strukturen werden unabhängig platziert | `StructurePriority`: Story vor Orten mit Bewohner vor dem Rest |
| Dschungel- und Mangrovenbäume im Leuchtturm und in Saltmere, Erzflecken, Seetang, Blasenquellen | wie oben | derselbe Filter (Bäume 6, Erze 3–7 Blöcke Abstand) |
| Sand-Rechteck der Tiki-Bar am Hang | `beard_thin` ebnet die ganze Grundfläche | Strandbar und Camp nur auf fast ebenem Boden |
| Port Solace: Teil eines Turms nie gebaut (1 von 6 Städten) | Teile weiter als 8 Chunks vom Start bekommen keine Referenz | `max_distance_from_center` 112 → 104 |
| Sunken Plane ragt aus flachem Wasser | keine Tiefenprüfung | Mindesttiefe 14 Blöcke |
| Fischerboot: bis 36 Schnüre im Wasser | Wasser spült Spinnweben weg | Netze aus `cargo_net` |
| Amboss am Kran des Rigs fällt | Amboss ist ein fallender Block | Heavy Core |

## Nachher (dieselben Seeds und Orte, 95 Strukturen)

| Struktur | Orte | Fremdblöcke in Räumen | Wasser/Lava in Räumen | Pflanzen in Räumen | NPC in Ordnung | Items |
|---|---|---|---|---|---|---|
| abandoned_raft | 5 | 0 | 0 | 0 | – | 1 |
| abyssal_sanctum | 5 | 0 | 0 | 0 | – | 0 |
| ashen_forge | 5 | 0 | 0 | 0 | 5/5 | 0 |
| beach_shack | 5 | 0 | 0 | 0 | 3/3 | 0 |
| buoy_field | 5 | 0 | 0 | 0 | – | 0 |
| castaway_camp | 5 | 0 | 0 | 0 | 3/3 | 0 |
| coral_temple | 5 | 0 | 0 | 0 | – | 0 |
| helix_station | 5 | 0 | 0 | 0 | – | 0 |
| iceberg_outpost | 5 | 0 | 0 | 0 | 5/5 | 0 |
| old_lighthouse | 5 | 0 | 0 | 0 | 5/5 | 0 |
| pirate_cove | 5 | 0 | 0 | 1 | – | 2 |
| port_solace | 5 | 0 | 0 | 0 | – | 4 |
| rusted_rig | 5 | 0 | 0 | 0 | 5/5 | 0 |
| saltmere_village | 5 | 0 | 0 | 0 | 10/10 | 0 |
| sunken_plane | 5 | 0 | 9 | 0 | – | 0 |
| sunken_ruins | 5 | 0 | 0 | 0 | – | 1 |
| wreck_cargo_ship | 5 | 0 | 0 | 0 | – | 0 |
| wreck_fishing_boat | 5 | 0 | 0 | 0 | – | 0 |
| wreck_galleon | 5 | 0 | 0 | 0 | – | 2 |

Dazu Schlussläufe: 6 Städte Port Solace ohne Teil jenseits von 8 Chunks, Teo in zwei Tiki-Bars, Sanctum, Helix,
Coral Temple und Iceberg Outpost ohne Blasenquellen oder Eisschollen. Übrig sind nur gewollte Effekte: Verwitterung
und Moos aus den Prozessoren, Magma in der Forge, Seegras auf dem Wasser der Vorlagen, Gras unter Blöcken wird zu Erde,
Kupfer oxidiert, und bei der Sunken Plane eine geflutete Lufttasche (3 Blöcke).

## Bilder

- `images/npc_sheet.jpg`: alle Personen aus freier Luft aufgenommen (Kamera vorher auf Luft und freie Sicht geprüft).
- `images/teo_sheet.jpg`: Teo in zwei Tiki-Bars und die Bars von oben.
- `images/over_sheet.jpg`: Übersichten. Bei der Forge fehlt teils das Gelände (nicht geladen), Unterwasser-Orte sind von
  oben kaum zu sehen.

## Bewusst so gelassen

- (Seit 6.11. geändert: Kai wohnt jetzt in allen drei Lagerarten.)
- Die Galeone kann unter Wasser zwei Schädel verlieren (Items).
- Gleichrangige Nebenstrukturen dürfen sich weiter berühren (z. B. Ruinen und Frachter).
- Ältere Welten: Strukturen in schon erzeugten Chunks bleiben, wie sie sind.
