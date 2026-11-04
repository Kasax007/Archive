# 08 – Offen und zu testen (Checkliste)

Stand 4.11.2026. Alle Repos sind gepusht (lokaler Stand = GitHub). Offen ist vor allem, was **deine Freigabe** braucht.

## A. Deine Entscheidungen (blockieren die nächsten Schritte)

- [ ] **Beach Craft 3.0.0 hochladen** – vom Berechtigungssystem blockiert; du musst den Upload freigeben oder selbst
  hochladen.
  - Projekt 1010922, Datei `$SP/release_bc3/raft-3.0.0+26.3.jar` (oder neu bauen: Branch `26.3`, `./gradlew build`),
    Changelog `docs/curseforge/changelog-3.0.0+26.3.md`, Spielversion 26.3, Fabric.
  - Danach rund 10 Minuten auf die CurseForge-Freigabe warten.
- [ ] **Tamagotchi 1.2.0 veröffentlichen** – Tag `v1.2.0` pushen oder den Workflow „Release“ von Hand starten (GitHub
  Actions); braucht deine Freigabe.
  - 1.2.0 liegt auf Branch **`26.3`** (`aa45ba7`, am 4.11. nachgezogen und gepusht). Für das Release nur noch den Tag
    `v1.2.0` pushen oder den Workflow „Release“ auf `26.3` starten.
  - Prüfen, ob das Secret `CURSEFORGE_TOKEN` im Tamagotchi-Repo gesetzt ist (sonst gibt es nur das GitHub-Release).
- [ ] **Dreamcraft V1.3 bauen und hochladen** – erst wenn Beach Craft 3.0.0 (und am besten Tamagotchi 1.2.0) auf
  CurseForge freigegeben ist.
  - `python3 tools/mkpack.py V1.3 9429010 <BC-3.0.0-Datei> <Tamagotchi-1.2.0-Datei>`.
  - Ohne viertes Argument käme Tamagotchi 1.1.0 (9399713) ins Pack – die V1.3-Quests beschreiben aber 1.2.0
    (Look-alike-Strukturen, Mod-Essen, Mod-Erze).
  - Danach Produktiv-Test (Abschnitt C), Upload, Server-Pack hochladen und von Hand als Server Pack markieren.
- [ ] **Neue Beschreibungen einfügen** (Quellcode-Ansicht, siehe [06](06_videos_und_beschreibungen.md#4-die-curseforge-beschreibungen-finale-fassungen)):
  - [ ] Quest Icons – **jetzt** (1.1.0 ist veröffentlicht).
  - [ ] Beach Craft – nach dem Upload von 3.0.0.
  - [ ] Dreamcraft – mit V1.3 (die Datei ist schon auf V1.3).
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
- [ ] Mit zwei Spielern segeln: Der zweite steht auf dem Deck und bleibt drauf, auch bei Kurven (Deck-Ecken!).
- [ ] Hängematte nachts schlafen (im Nether/End passiert nichts).
- [ ] Handkurbel des Air Compressor (schleichen + leere Hand, Kurbel-Knopf im Menü).
- [ ] Ganzer Bosskampf im Überlebensmodus, gern mit Freunden; erneutes Rufen mit Schlüssel + Ancient Crystal; Heilung
  nach 30 s ohne Spieler.
- [ ] Natürliche Piratenbucht auf echten Inseln, Leuchtturm-Steg (zeigt er oft ins Land?), Castaway Camp, Sunken Plane,
  Fishing Boat Wreck in freier Natur.
- [ ] Büro-Etagen und Rathaus-Treppenhaus in Port Solace ohne Nachtsicht (seit der dunkleren Dimension).
- [ ] Ton: Walgesang und Blasen (der Testclient lief ohne Ton).
- [ ] Dedicated Server mit 3.0 allein (ohne Pack) starten.
- [ ] Alte Welt: harte Kante zwischen altem und neuem Gelände, Almanac beim nächsten Betreten, keine Castaway-Truhe auf
  alter Plattform.
- [ ] Im Spiel beobachten: Anglerfische im Graben (Gewicht 4) gegenüber Leuchttintenfischen (Gewicht 3, vorher 10).
- [ ] Offene Design-Fragen aus 2.0.1 entscheiden: Titanofen verdoppelt alles, Energieverlust beim Abbauen, Chunk
  Destroyer kostet leere Säulen, ein Ausgabe-Slot im Item Catcher, seltener Treibholz-Setzling, Haken zieht durch Wände.
- [ ] Optional: ein Video (Short oder Review) zu Beach Craft 3.0.

## E. Quest Icons – zu testen
- [ ] Teams auf einem echten Server: einladen per Klick im Chat, beitreten, Server neu starten – kein leeres Team mehr.
- [ ] Edit-Modus als OP auf einem Server: Quest ziehen, SNBT bearbeiten, „Reload files from disk“.
- [ ] Mystery Reward ein paarmal öffnen (keine Creative-Blöcke).

## F. Tamagotchi – nach dem Release
- [ ] CurseForge-Datei-ID von 1.2.0 notieren und für Dreamcraft V1.3 verwenden.
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
