# 08 – Offen und zu testen (Checkliste)

**Stand 9.11.2026 (Testrunde-Erinnerung vom 5.11. abgearbeitet).** Alles, was am 5.11. zum Hochladen offen war, ist
online und von CurseForge freigegeben: Beach Craft 3.1.0 bis 3.4.0 (26.3 und 1.21.1), Dreamcraft V1.4 bis V1.6
(369 Quests in 16 Kapiteln), Quest Icons 1.3.0 mit allen Ports, Tamacraft 1.3.0 (26.3 und 1.21.1), Challenge-Craft-Modpack
v4.2. Das Challenge-Craft-Modpack v5 ist gestrichen (Pack bleibt Vanilla plus Challenge Craft, Wunsch vom 7.11.). Alle
sechs Projekte sind auch auf Modrinth (Challenge Craft freigegeben, der Rest in Prüfung).

**Getestet seit dem 5.11.:** Dreamcraft V1.5 (neue Quests im Spiel mit `qrun`, neue Welt mit Questbuch, Server-Pack-Start)
und V1.6 (Server aus dem Server-Pack + Client wie aus dem Launcher; neue 26.3-Server haben `white-list=true`, das README
des Server-Packs sagt es). Beach Craft 3.4.0: Look-Tests 11/11 im zusammengeführten Stand, 1.21.1-Port getestet.
Was unten noch offen ist, geht nur von Hand, braucht deine Entscheidung oder ist eine kleine Verbesserung für später.

**Testrunde 5.11. (automatisch im Spiel):** Alle 344 Dreamcraft-Quests lassen sich erfüllen und abholen (Szene `qrun`,
`tools/qrun_plan.py`; 317 im ersten Lauf, die 27 übrigen nach Harness-Fixes im zweiten). Die statische Quellen-Prüfung
(`tools/qsource.py`) findet für 292 von 298 Quest-Items eine Quelle im Überlebensmodus; die 6 übrigen kommen aus
Spielmechaniken oder per Code eingefügter Beute. Die Beach-Craft-Checks (Szene `bccheck`) stehen unten in D.

## Kurz: was jetzt noch bei dir liegt (9.11.)

1. **Von Hand auf CurseForge/Bisect:** Beschreibungen neu einfügen (Beach Craft, Dreamcraft, beide Challenge-Craft-Seiten;
   Übergabeseite), Server-Packs als Server Pack markieren, Bisect-Partnerkonsole (Challenge Craft RAM-Empfehlung 4 GB,
   Dreamcraft-Eintrag 19732 auf 26.3).
2. **Entscheidungen:** Challenge Craft 1.1.4 ja/nein (Crafter-Fix plus Infinite-Chest-Dupe-Fix, Abschnitt G); Beach-Craft-
   Balance-Fragen 1–7 aus 2.0.1 (Abschnitt D, Vorschlag: gesammelt als 3.5; Details im Chat vom 9.11.).
3. **Nur mit echten Spielern:** Quest-Buch mit echten Klicks, Server mit zwei Spielern (`/quests team`), Bosskampf mit
   Freunden, Teams und Edit-Modus von Quest Icons auf einem echten Server.
4. **Modrinth:** Prüfung abwarten; Autoren der 7 fehlenden Dreamcraft-Mods fragen (`curseforge/modrinth/AUTOREN-ANFRAGE.md`).
5. **Outreach:** 76 Entwürfe auf der Freigabeseite (Stand 9.11.), E-Mails in Portionen von 10–15 pro Tag senden.

## A. Deine Entscheidungen (blockieren die nächsten Schritte)

- [x] **Beach Craft 3.0.0 hochgeladen** (4.11., mit deiner Freigabe) – Datei 9431301, freigegeben.
- [x] **Tamagotchi 1.2.0 hochgeladen** (4.11.) – Datei 9431312 direkt über die CurseForge-API, freigegeben.
  - [ ] GitHub-Release/Tag `v1.2.0` fehlt noch (Tag-Push geht aus der Sitzung nicht), siehe [04](04_tamagotchi.md).
- [x] **Dreamcraft V1.3 gebaut, getestet und hochgeladen** (4.11.) – Client 9431378, Server-Pack 9431379.
  - [ ] Auf CurseForge prüfen, ob 9431379 als Server Pack markiert ist (geht nur von Hand).
- [ ] **Neue Beschreibungen einfügen** (Quellcode-Ansicht, siehe [06](06_videos_und_beschreibungen.md#4-die-curseforge-beschreibungen-finale-fassungen)):
  - [ ] Quest Icons: Seite für 1.2 (FTB-Import, 26.2) erst einfügen, wenn 1.2.0 freigegeben ist; dazu die neue
    Kurzbeschreibung von der Übergabeseite.
  - [ ] Beach Craft (3.0.0 ist veröffentlicht).
  - [ ] Dreamcraft (V1.3 ist hochgeladen).
  - [ ] Dreamcraft-Kurzbeschreibung (Summary) prüfen: stand am 2.11. noch „800+ quests“.
- [ ] **Challenge Craft: Crafter-Änderung** – der Crafter baut keine Infinite Chest und keine Casino-Geräte mehr
  (Branch `bugcheck-2026-11`). Behalten (dann 1.1.4 veröffentlichen) oder anders lösen? Siehe
  [05](05_challenge_craft.md#die-entscheidung-die-du-treffen-musst-der-crafter).

- [x] **BisectHosting-Partner-ID:** laut Nutzer (8.11.) immer 4395; beide Packs tragen sie (Dreamcraft ab V1.4.2,
  Challenge Craft ab v4.1), seit V1.5.1/v4.2 mit `pack_edit_mode=false`.
- [ ] **BisectHosting RAM-Empfehlung für Challenge Craft (Pack 27138)** steht auf 8 GB für 1–4 Spieler; die
  Beschreibung bestellt 4 GB. In der Partnerkonsole auf 4 GB senken, damit Bestellseite und Menü dasselbe empfehlen.
- [ ] Dreamcraft V1.4.2: Server-Pack 9499399 auf CurseForge als Server Pack markieren (geht nur von Hand).

- [ ] **CurseForge-Beschreibungen neu einfügen** (Übergabeseite Version 20): Dreamcraft, Challenge-Craft-Modpack und
  -Mod haben Bisect-Links ohne eckige Klammern (CurseForge hatte den alten Link geleert).
- [ ] **Bisect-Partnerkonsole:** RAM-Empfehlung für Challenge Craft (Pack 27138) auf 4 GB senken (sonst „Insufficient RAM“
  auf der Bestellseite); Dreamcraft-Eintrag (19732) auf die 26.3-Version stellen (zeigt noch „Dreamcraft 1.20.1“).
- [ ] **Modrinth:** Prüfung abwarten (Stand 9.11.: Challenge Craft freigegeben; Beach Craft, Quest Icons, Tamacraft, Challenge-Craft-Pack, Dreamcraft in Prüfung); Autoren
  der 7 fehlenden Dreamcraft-Mods fragen (Vorlage `curseforge/modrinth/AUTOREN-ANFRAGE.md`).
- [x] **Beach Craft 3.4.0** fertig, 26.3 (9512111) und 1.21.1 (9518456) hochgeladen und freigegeben (8./9.11.).

## B. Risiken und Aufräumen
- [ ] **Die Build-Werkzeuge hängen am flüchtigen Scratchpad.** `mkpack.py` hat den Scratchpad-Pfad dieser Sitzung fest
  eingetragen und braucht dort `packdb.json` (Modliste mit Datei-Pfaden), `jars/` (Mod-Cache), `ownjars/` (Quest Icons
  1.1.0, Beach Craft 3.0.0, Tamagotchi 1.2.0), `pack/overrides` (zurzeit identisch mit dem Repo), `client_only.json`
  und `srv/fabric-server-launch.jar`. Geht der Scratchpad verloren, muss das neu entstehen (`tools/pack.py fetch`,
  Overrides aus dem Repo kopieren, Jars bauen oder von CurseForge laden) und der Pfad `SP` angepasst werden.
- [ ] Server-Packs früherer Versionen: ob V1 bis V1.2.1 auf CurseForge als Server Pack markiert sind, ist **unklar**
  (geht nur von Hand). Für das Challenge-Craft-Modpack v4 war die Markierung am 1.11. noch offen.

## C. Dreamcraft – zu testen
- [ ] **V1.3 wie ein Spieler installieren** (`tools/prodtest`): `cf_install.py <Client> <Server>`, Hauptmenü bei
  854×480, 1366×768 und 1920×1080, jeden Knopf klicken (Mods, Rent a Server, Quit), Welt laden, J drücken.
- [ ] **Quest-Buch mit echten Klicks:** erste Prolog-Quest abhaken, Belohnung abholen, „Claim all“, eine Auswahl-Belohnung
  („Awakened Power“: ein Ring nach Wahl), Pins, Escape, verschiedene GUI-Skalen.
- [ ] **Kapitel 6 in einer neuen Welt:** Portal-Quests, Story-Quests feuern mit den Advancements, Almanac-Lesezeichen
  öffnet die richtige Seite.
- [ ] **Tamagotchi-Pfad:** Pets in Strukturen anderer Mods finden (nur mit 1.2.0), Mod-Essen füttern.
- [ ] **Dream Star:** mit echten Zutaten herstellen, Advancement „Living the Dream“, Sockel mit der 3-Sekunden-Ansehen-
  Aufgabe, Ersatzrezept darf im Pack nicht erscheinen.
- [ ] **Update einer V1.2.1-Welt:** Fortschritt bleibt, „Master of Dreams“ bietet die zweite Krone an, alte Teile der
  Endless Sea bleiben alt (weiter hinausfahren), Journal-Karte per Schleichen + Benutzen.
- [ ] **Server:** V1.3-Server-Pack aus der Zip starten (EULA), Quest-Buch, ein zweiter Spieler, `/quests team`;
  Chunky in der neuen Raft-Dimension (die Welt-Generierung war in allen Tests langsam).
- [ ] Shader an (Iris): Endless Sea und Graben ansehen, ob die neue Dunkelheit gut aussieht.

## D. Beach Craft 3.0 – zu testen (aus den Modulberichten und der Spezifikation)
- [x] Deck trägt einen Mitfahrer auch in Kurven (BcCheck 5.11.). Mit einem echten zweiten Spieler noch offen.
- [x] Selbst gebautes Floß (3.1.0): Wer per Teleport, Login oder Dimensionswechsel auf ein fahrendes Floß kommt, steht
  jetzt auf dem Deck statt darunter (Merge e6b344b, Tests `tools/content/vessel/tests/raft_3.txt`, `raft_4.txt`).
- [x] Hängematte nachts schlafen: Nacht wird übersprungen, im Nether passiert nichts (BcCheck 5.11.).
- [x] Handkurbel des Air Compressor (im Sound-Test 5.11. bedient und gehört).
- [x] Bosskampf im Test durchgespielt (Sound-Test 5.11.).
- [x] Heilung nach 30 s ohne Spieler (bctest 5.11., `tools/content/boss/tests/boss_heal.txt`): mit einem Spieler im
  Überlebensmodus in der Arena bleibt der Leviathan bei 450 von 600, ohne Spieler ist er nach 35 s wieder voll.
- [ ] Bosskampf im Überlebensmodus mit Freunden; erneutes Rufen mit Schlüssel + Ancient Crystal.
- [x] Natürliche Piratenbucht, Castaway Camp, Sunken Plane und Fishing Boat Wreck in freier Natur: in der
  Strukturprüfung 6.11. an je 5 Orten geprüft (siehe unten). Offen bleibt nur der Leuchtturm-Steg (zeigt er oft ins Land?).
- [x] **Strukturprüfung 6.11.** (`bctest audit`, Klasse `src/gametest/.../StructAudit.java`, Skripte im Scratchpad
  `audit/gen.py`): alle 19 Strukturen an je 5 Orten in 2 Welten (Seeds `bcaudit1`, `tides2`) Block für Block mit ihren
  Vorlagen verglichen, dazu jede Person (Füße und Kopf frei, Boden darunter, nicht im Wasser, keine Doppelten) und
  herumliegende Items. Gefunden und behoben (Branch `fix/structure-features`, nach 26.3 gemergt):
  - **Ashen Forge:** Basaltsäulen füllten an allen 5 Orten die Räume (1.645–2.875 Blöcke je Forge). Voss stand zweimal
    im Basalt, die Glutkrabben der Vorlage erstickten (daher die Items am Boden). Asche-Dünen fraßen die Wände, ein
    Lavasee schnitt hinein. Ursache: Features laufen nach der Struktur im selben Schritt und auch aus Nachbar-Chunks.
    Fix: Platzierungsfilter `raft:clear_of_structures` an allen Gelände-Features (Vanilla-Features als `raft:`-Kopien;
    Features ohne Höhe wie Blasenquellen, Trümmer, Eisschollen mit `whole_column`).
  - **Überlappung:** Ein Rusted Rig stand auf dem Abyssal Sanctum (Beine durch die Wände, 615 Wasser im Sanctum),
    fremde Teile in Helix Station und Port Solace. Fix: `StructurePriority` mit Rängen (Story vor Orten mit Bewohner vor
    dem Rest, Tags `raft:priority/story` und `raft:priority/people`), geprüft in `findValidGenerationPoint`, also auch
    für `/locate` und die Karten.
  - **Bewuchs und Erze:** Dschungel- und Mangrovenbäume im Leuchtturm und in Saltmere, Erzflecken in Fundamenten und
    Böden, Seetang im Coral Temple, Blasenquellen im Sanctum. Fix: derselbe Filter.
  - **Strandbar:** scharfes Sand-Rechteck mit Stufe am Hang (die Geländeanpassung `beard_thin` ebnet die Grundfläche).
    Fix: Strandbar und Camp nur auf fast ebenem Boden (9 Punkte, höchstens 3 Blöcke Unterschied).
  - **Port Solace:** In etwa 1 von 6 Städten reichte ein Teil in einen 9. Chunk vom Startchunk. Das Spiel verteilt
    Teile aber nur bis 8 Chunks, der Teil wurde nie gebaut (Fuß eines umgestürzten Turms auf nacktem Kies). Fix:
    `max_distance_from_center` 112 → 104 (Layout-Simulation: 0 von 60 Städten jenseits von 8 Chunks, gleich viele
    Teile, Rathaus mit den Story-Truhen, Glas- und Deko-Turm weiter in jeder Stadt). Der Check meldet solche Teile jetzt.
  - **Sunken Plane** ragte aus flachem Wasser (Pflanzen der Vorlage im Trockenen). Fix: Mindesttiefe 14 Blöcke.
  - **Fischerboot:** Das Meer spülte die Spinnweben-Netze weg (bis 36 Schnüre). Jetzt `cargo_net` (wassergefüllt).
  - **Rusted Rig:** Der Amboss am Kran fiel beim ersten Block-Update. Jetzt ein Heavy Core.
  - **Kontrolle mit dem Fix** (dieselben Seeds und Orte, 95 Strukturen): 0 Fremdblöcke in Räumen, 0 Pflanzen in
    Räumen, alle 36 geprüften Personen frei und auf dem Boden, keine Spinnweben- oder Krabben-Items mehr. Übrig sind
    nur gewollte Effekte (Verwitterung, Magma in der Forge, Seegras auf Wasser der Vorlage, Gras unter Blöcken wird zu
    Erde) und bei der Sunken Plane eine geflutete Lufttasche (3 Blöcke).
  - **Geändert 6.11.:** Kai wohnt jetzt in allen drei Lagerarten (Zelt, Unterstand, Boots-Unterschlupf).
  - **Bewusst so:** Die Galeone kann unter Wasser 2
    Schädel verlieren. Gleichrangige Nebenstrukturen dürfen sich weiter berühren (Ruinen und Frachter).
- [ ] Büro-Etagen und Rathaus-Treppenhaus in Port Solace ohne Nachtsicht (seit der dunkleren Dimension).
- [x] Ton: Walgesang und Blasen (BcCheck 5.11., mit Ton-Protokoll).
- [x] Dedicated Server mit 3.1.0 allein (ohne Pack) gestartet (Smoke-Test 5.11., 15/15).
- [ ] Alte Welt: harte Kante zwischen altem und neuem Gelände, Almanac beim nächsten Betreten, keine Castaway-Truhe auf
  alter Plattform.
- [x] Anglerfische im Graben gegenüber Leuchttintenfischen beobachtet (BcCheck 5.11.): an einer Stelle 5 zu 2, an der
  anderen 1 zu 6. Beides kommt vor.
- [ ] Offene Design-Fragen aus 2.0.1 entscheiden: Titanofen verdoppelt alles, Energieverlust beim Abbauen, Chunk
  Destroyer kostet leere Säulen, ein Ausgabe-Slot im Item Catcher, seltener Treibholz-Setzling, Haken zieht durch Wände.
- [x] Video zu Beach Craft 3.0: Doku „Tides of the Deep“ (18:35, `beachcraft/documentary/`), fertig am 4.11.
- [ ] Beim Filmen aufgefallen (prüfen, ggf. beheben):
  - Der Tresor des Storm Sigil (−1072 89 207) liegt unter dem Meeresspiegel (100). Die Story sagt „high above the
    water line“ (Cranes Funkspruch, Radiozeile 13, Terminal solace_3).
  - Vulkaninsel bei (−400, −300) ohne Lava an der Oberfläche, nur tief unten. Prüfen, ob die Lava-Sperre um die Ashen
    Forge (CraterLavaFeature) zu viel wegnimmt.
  - [x] In der Raft-Dimension ist jetzt Tag und Nacht wie in der Oberwelt (3.1.0).
  - [x] Der alte Leuchtturm steckt in hohen Dschungelbäumen der Nachbarinsel: Bäume halten jetzt 6 Blöcke Abstand
    zu Strukturen (Strukturprüfung 6.11.).
  - [x] Der Coral Temple liegt jetzt immer ganz unter Wasser (3.1.0).
  - Neue Gebiete der Raft-Dimension: Der Server fällt 90–180 s zurück.
  - [x] Log: „Dev warning – Untranslated Item Tags“: in 3.4.1 (9.11.) haben alle 63 Item-Tags einen Namen; JEI zeigt
    keine rohen Tag-IDs mehr. Dreamcraft bekommt 3.4.1 beim nächsten größeren Update.

## E. Quest Icons – zu testen
- [x] Quest Icons 1.2.0 und 1.3.0 hochgeladen und freigegeben (1.3.0: 26.3 = 9501059, 26.2 = 9501060, dazu 6 Ports).
- [ ] FTB-Import mit einem eigenen oder freien FTB-Buch ausprobieren: `/quests import ftbquests` (Vorschau), Bericht
  `config/questsicons/ftbquests-import-report.txt` lesen, dann `run`.
- [ ] Teams auf einem echten Server: einladen per Klick im Chat, beitreten, Server neu starten – kein leeres Team mehr.
- [ ] Edit-Modus als OP auf einem Server: Quest ziehen, SNBT bearbeiten, „Reload files from disk“.
- [ ] Mystery Reward ein paarmal öffnen (keine Creative-Blöcke).

## F. Tamagotchi – nach dem Release (1.2.0 = 9431312)
- [x] CurseForge-Datei-ID von 1.2.0 (9431312) notiert und in Dreamcraft V1.3 verwendet.
- [x] Beschreibung: seit 1.3.0 (Tamacraft) mit Modpack-Abschnitt (Struktur- und Item-Tags).
- [x] Modrinth: Tamacraft ist eingerichtet (8.11.), wartet auf die Prüfung.

## G. Challenge Craft
- [ ] Crafter-Entscheidung (siehe A).
- [ ] Wenn 1.1.4 kommen soll: Branch `bugcheck-2026-11` übernehmen, `mod_version` auf 1.1.4 – das veröffentlicht
  automatisch (Changelog liegt bereit); danach evtl. ein neues Challenge-Craft-Modpack mit 1.1.4.
- [ ] Offene Punkte aus dem Bug-Check entscheiden: Infinite Chest und Trichter/Rohr-Mods (Transfer-API), Inhalt beim
  Abbauen behalten, Update-Tag, XP vom Client, wer Bob in die Lobby holen darf, Trivia-Antwort an den Client,
  `ROULETTE_LEAVE`.
- [ ] Bob: Zielen unter Lag (`sniper_duel`) ansehen.
- [x] Modrinth hat jetzt 1.1.2 und 1.1.3 (8.11., byte-gleich mit CurseForge).
