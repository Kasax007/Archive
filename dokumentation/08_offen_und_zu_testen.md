# 08 – Offen und zu testen (Checkliste)

Stand 5.11.2026. Alle Repos sind gepusht (lokaler Stand = GitHub). Seit dem 4.11. sind Beach Craft 3.0.0, Tamagotchi 1.2.0 und Dreamcraft V1.3 hochgeladen.

**Testrunde 5.11. (automatisch im Spiel):** Alle 344 Dreamcraft-Quests lassen sich erfüllen und abholen (Szene `qrun`,
`tools/qrun_plan.py`; 317 im ersten Lauf, die 27 übrigen nach Harness-Fixes im zweiten). Die statische Quellen-Prüfung
(`tools/qsource.py`) findet für 292 von 298 Quest-Items eine Quelle im Überlebensmodus; die 6 übrigen kommen aus
Spielmechaniken oder per Code eingefügter Beute. Die Beach-Craft-Checks (Szene `bccheck`) stehen unten in D.

**Noch nicht hochgeladen (wartet auf deine Freigabe):** Beach Craft 3.1.0 (Floß selbst bauen, NPCs, Sounds und Musik,
Welt-Fixes), Dreamcraft V1.4 (Upgraded Iron Chests, Kapitel „Quality of Life“, Beach Craft 3.1.0) und das
Challenge-Craft-Modpack v5 (erst nach deiner Testrunde, falls Quests sich noch ändern).

## A. Deine Entscheidungen (blockieren die nächsten Schritte)

- [x] **Beach Craft 3.0.0 hochgeladen** (4.11., mit deiner Freigabe) – Datei 9431301, freigegeben.
- [x] **Tamagotchi 1.2.0 hochgeladen** (4.11.) – Datei 9431312 direkt über die CurseForge-API, freigegeben.
  - [ ] GitHub-Release/Tag `v1.2.0` fehlt noch (Tag-Push geht aus der Sitzung nicht), siehe [04](04_tamagotchi.md).
- [x] **Dreamcraft V1.3 gebaut, getestet und hochgeladen** (4.11.) – Client 9431378, Server-Pack 9431379.
  - [ ] Auf CurseForge prüfen, ob 9431379 als Server Pack markiert ist (geht nur von Hand).
- [ ] **Neue Beschreibungen einfügen** (Quellcode-Ansicht, siehe [06](06_videos_und_beschreibungen.md#4-die-curseforge-beschreibungen-finale-fassungen)):
  - [ ] Quest Icons (1.1.0 ist veröffentlicht).
  - [ ] Beach Craft (3.0.0 ist veröffentlicht).
  - [ ] Dreamcraft (V1.3 ist hochgeladen).
  - [ ] Dreamcraft-Kurzbeschreibung (Summary) prüfen: stand am 2.11. noch „800+ quests“.
- [ ] **Challenge Craft: Crafter-Änderung** – der Crafter baut keine Infinite Chest und keine Casino-Geräte mehr
  (Branch `bugcheck-2026-11`). Behalten (dann 1.1.4 veröffentlichen) oder anders lösen? Siehe
  [05](05_challenge_craft.md#die-entscheidung-die-du-treffen-musst-der-crafter).

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
- [ ] Bosskampf im Überlebensmodus mit Freunden; erneutes Rufen mit Schlüssel + Ancient Crystal; Heilung nach 30 s
  ohne Spieler (bisher nur im Code geprüft).
- [ ] Natürliche Piratenbucht auf echten Inseln, Leuchtturm-Steg (zeigt er oft ins Land?), Castaway Camp, Sunken Plane,
  Fishing Boat Wreck in freier Natur.
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
  - Der alte Leuchtturm steckt in hohen Dschungelbäumen der Nachbarinsel.
  - [x] Der Coral Temple liegt jetzt immer ganz unter Wasser (3.1.0).
  - Neue Gebiete der Raft-Dimension: Der Server fällt 90–180 s zurück.
  - Log: „Dev warning – Untranslated Item Tags“.

## E. Quest Icons – zu testen
- [ ] Teams auf einem echten Server: einladen per Klick im Chat, beitreten, Server neu starten – kein leeres Team mehr.
- [ ] Edit-Modus als OP auf einem Server: Quest ziehen, SNBT bearbeiten, „Reload files from disk“.
- [ ] Mystery Reward ein paarmal öffnen (keine Creative-Blöcke).

## F. Tamagotchi – nach dem Release (1.2.0 = 9431312)
- [x] CurseForge-Datei-ID von 1.2.0 (9431312) notiert und in Dreamcraft V1.3 verwendet.
- [ ] Optional: CurseForge-Beschreibung um die Modpack-Funktionen von 1.2.0 ergänzen (sie ist noch auf 1.1.0).
- [ ] Modrinth: nur wenn `MODRINTH_TOKEN` und `modrinth_id` gesetzt sind.

## G. Challenge Craft
- [ ] Crafter-Entscheidung (siehe A).
- [ ] Wenn 1.1.4 kommen soll: Branch `bugcheck-2026-11` übernehmen, `mod_version` auf 1.1.4 – das veröffentlicht
  automatisch (Changelog liegt bereit); danach evtl. ein neues Challenge-Craft-Modpack mit 1.1.4.
- [ ] Offene Punkte aus dem Bug-Check entscheiden: Infinite Chest und Trichter/Rohr-Mods (Transfer-API), Inhalt beim
  Abbauen behalten, Update-Tag, XP vom Client, wer Bob in die Lobby holen darf, Trivia-Antwort an den Client,
  `ROULETTE_LEAVE`.
- [ ] Bob: Zielen unter Lag (`sniper_duel`) ansehen.
- [ ] Alt, aber offen: Modrinth hat noch 1.1.1 (1.1.2 und 1.1.3 fehlen; es fehlt der Modrinth-Token).
