# Crawl of Fame – Projektgedächtnis

Stand 12.11.2026. Auftrag des Nutzers: ein großer Fabric-26.3-Mod im Genre „Dungeon-Crawl als Gameshow“ (Inspiration:
LitRPG-Romane), integrierbar in Modpacks, serverfähig, mit vielen eigenen Kreaturen, Items, Klassen, UI, Sounds.
Eigenständig durcharbeiten bis „publish-ready“; höchstens 2 Subagenten (Opus, high), die Hauptsitzung plant und macht
das Schwierigste. Effizient arbeiten (Wochenlimit).

## Repo und Name

- Repo: `Kasax007/dungeon-crawler-steve`, lokal `/home/user/dungeon-crawler-steve`, Branch `claude/determined-edison-xwiksi`
  (einziger Branch, auf den gepusht werden darf).
- **Mod-Name: „Crawl of Fame“**, Mod-ID `crawloffame`, Paket `net.kasax.crawl`. Der Repo-Name bleibt Arbeitstitel.
- Warum nicht „Dungeon Crawler Steve“: „Dungeon Crawler Carl“ ist eine Marke des Autors (USPTO 97323580, weitere
  Anmeldung 2025) und wird für Spiele lizenziert (Renegade: Rollenspiel und Deckbuilder; TV-Serie bei Peacock). Ein
  Titel nach demselben Muster wäre für eine Veröffentlichung riskant. „Dungeon crawler“ allein ist ein Gattungsbegriff.
- **Inhalt ist eigenständig:** keine Namen, Figuren, Kreaturen, Texte oder Ebenen-Konzepte aus den Büchern. Nur die
  Genre-Mechaniken (Ebenen mit Zeitlimit, Treppen, Lootboxen, Achievements, Publikum, Sponsoren, Klassenwahl).
  Sperrliste `docs/NAMES_NOT_ALLOWED.txt` (836 Namen), Prüfung `tools/dev/check_names.py`.
- Das Buch (Zip des Nutzers) wurde nur als Text ausgewertet (36 Blöcke → Mechanik-Digest); Text und Digest liegen
  nur im Scratchpad, **nicht in einem Repo**.

## Konzept in Kürze (Details: `docs/DESIGN.md` im Mod-Repo)

- Stage Doors in der Oberwelt (roter Teppich, Glühbirnen-Bogen, Treppe, roter Vorhang). Wer durchgeht, ist Kandidat
  der Show CRAWL OF FAME. Gleiche Stage Door binnen 5 Minuten = gleiche Gruppe („Cast“).
- 10 Ebenen als Filmkulissen, jede mit eigener Regel; Sendezeit pro Ebene, danach „Set Strike“ (alle dort sterben).
  Tod = Lauf vorbei, alles bleibt als „Remains“ für die Gruppe liegen; Sieg = goldener Vorhang auf Ebene 10.
- Der Moderator „the Emcee“ spricht alle Systemtexte. Green Rooms (sicher), Prize Crates (Copper … Starlight, nur im
  Green Room zu öffnen), Hype und Fans, Sponsoren ab Ebene 4, Rollen und Makeover in Ebene 3, 5 Werte (Strength,
  Agility, Vitality, Mind, Charm), Fertigkeiten durch Benutzen.

## Technik (Details: `docs/ARCHITECTURE.md`, Stand-Liste `docs/PLAN.md`)

- Minecraft 26.3, Fabric Loader 0.20.1, Fabric API 0.166.2+26.3, Loom 1.17.21, Gradle 9.6, JDK 25 unter
  `/opt/jdk25/jdk-25.0.5+8` (Adoptium-API; `JAVA_HOME` der Umgebung zeigt auf Java 21, Skripte nutzen `CRAWL_JDK`).
- Getrennte Source-Sets (`src/main`, `src/client`, `src/gametest`); Ressourcen je Modul in `src/main/modules/<modul>`.
- Eine Dimension `crawloffame:dungeon`; jede Ebene eines Laufs ist eine Region (32×32 Chunks), 1 Kachel = 1 Chunk.
  Der Grundriss kommt aus `net.kasax.crawl.layout` (reines Java, offline prüfbar: `tools/dev/layout.sh`).
- Werkzeuge: `tools/dev/jc.sh` (Kompilier-Check in Sekunden ohne Gradle), `tools/dev/locked.sh` (Sperre für jeden
  Minecraft-Lauf, nur einer gleichzeitig).
- Referenz-Ordner im Container (nicht im Repo, nach Reset neu anlegen): `/home/user/ref/mcsrc` (dekompilierte
  Minecraft-Quellen, `./gradlew genSources` und Jar entpacken), `/home/user/ref/mcassets`, `/home/user/ref/raft`
  (Beach Craft 26.3), `/home/user/ref/cc` (Challenge Craft 26.3), `/home/user/ref/classpaths.txt`
  (`./gradlew printClasspaths -PcpOut=…`).

## Lehren

- Maven Central antwortet mit 429: Init-Skript `~/.gradle/init.d/central-mirror.gradle` (Google-Spiegel).
- `.gitignore`-Muster ohne führenden Schrägstrich (`run/`) blenden auch Java-Pakete gleichen Namens aus
  (`…/crawl/run/`): immer am Repo-Wurzelverzeichnis verankern (`/run/`).
- Agenten arbeiten in eigenen Worktrees (`/home/user/wt/a`, `/home/user/wt/b`) und liefern per Rebase + Push auf den
  einen Branch; jedes Modul hat eigene Dateien (auch eigene Mixin-Config und Lang-Datei), damit nichts kollidiert.
- Commit-Fußzeile ohne Modellnamen: `Co-Authored-By: Claude <noreply@anthropic.com>` + `Claude-Session: …`.

## Arbeitsweise mit den Agenten

- Zwei Spuren (A und B), je ein Workflow mit einer Kette von zwei Aufgaben (Opus, effort high). Pro Aufgabe etwa
  0,4 Mio. Agenten-Tokens und 35–45 Minuten. Jede Aufgabe liefert einen Bericht `docs/reports/<Aufgabe>.md`.
- Bilder für die Abnahme legen die Agenten nach `/home/user/shots/<Aufgabe>/` (nicht ins Repo). Die Hauptsitzung
  sieht sie an und gibt die Grafik-Richtung für die nächste Aufgabe vor.
- Erst eine Ebene „fertig aussehen“ lassen (Ebene 1), ansehen, dann den Stil auf die anderen Ebenen übertragen.
- Reihenfolge so, dass jede Stufe veröffentlichbar ist: erst 3 Ebenen rund (Grafik, Show, Karte, Stage Door,
  Mehrspieler-Prüfung), dann Rollen, NPCs, Audio, dann Ebenen 4–10, zuletzt Sponsoren/Interviews und Abschluss.

- **Seit 13.11. abends: Aufgaben per Agent-Werkzeug statt Workflow starten.** Der Workflow gibt jedem Agenten nur
  die *letzte* Nutzer-Nachricht als Auftrag mit; ist die eng (z. B. „Im Inventar scrollen“), lehnt der Agent einen
  größeren Auftrag ab. Vorgehen: `python3 briefs/brief.py <ID> <Datei> <a|b>` schreibt den ganzen Auftrag nach
  `wf/out/<ID>.brief.txt`; dann Agent (model opus, Hintergrund) mit kurzem Text „Auftrag der Leitung steht in dieser
  Datei“ und dem Bezug auf den Wunsch des Nutzers. Ein Agent pro Spur.
- Platte: frei halten (Agenten-Läufe brauchen mehrere GB). `tools/crawltest/run.sh` und `tools/dev/gametest.sh`
  löschen ihre Welten jetzt selbst; das Archiv ist als Sparse-Checkout eingerichtet (`memory`, `crawl-of-fame`,
  `dokumentation`, `curseforge`; zurück mit `git sparse-checkout disable`). Seit 14.11. 02:00 UTC ist es zusätzlich ein
  Teil-Klon (`git clone --filter=blob:none --sparse`): `.git` 27 MB statt 5,65 GB; Dateien außerhalb der vier Ordner
  lädt Git erst beim Auschecken nach (für Video-Arbeit dann einzelne Ordner mit `git sparse-checkout add <ordner>`).

## Container und Speicher

- Der Container (16 GB) wurde am 12.11. einmal neu gestartet, als drei Checkouts gleichzeitig bauten und testeten.
  Dateien blieben erhalten, alle Prozesse und Workflows waren weg. Seitdem: `~/.gradle/gradle.properties` mit
  `org.gradle.jvmargs=-Xmx1200m -XX:MaxMetaspaceSize=512m` und `idletimeout=60000`; Test-Server mit `-Xmx2G`
  (build.gradle), Mehrspieler-Test 3G + 2G. Nach einem Reset diese Datei neu anlegen (auch `org.gradle.java.home`).
- Zweiter Neustart am 13.11. kurz nach Mitternacht trotz Speicher-Grenzen (Kernel-Stand der VM wechselte):
  Neustarts kommen von der Infrastruktur und können wieder passieren.
- Vorgehen seitdem: jede Aufgabe beginnt mit dem Hinweis aus `crawl-of-fame/briefs/continue.txt` (frühere Arbeit im
  Worktree suchen: lokale Commits, `git status`, Bericht; dort fortsetzen). Die Agenten committen laufend lokal.
  Nach einem Neustart genügt `Workflow({scriptPath, resumeFromRunId})`: fertige Aufgaben kommen aus dem Cache,
  die unterbrochene setzt an ihren Commits an. Eigene, nicht gepushte Arbeit im Haupt-Checkout zuerst committen.

## Test-Werkzeuge

- `tools/dev/gametest.sh`: Server-Spieltests aller Module (Stand Runde 2: 35 Tests).
- `tools/crawltest/run.sh <skript> <ordner>`: ferngesteuerter Client mit Screenshots (Xvfb + EGL; nach einem
  Container-Reset `apt-get install -y libegl1 libegl-mesa0`).
- `tools/crawltest/mp.sh <host> <gast> <ordner>`: Mehrspieler-Test. Der Host startet einen Dedicated Server im
  eigenen JVM (Skript-Befehl `server`), der Gast ist ein zweiter Client (`join localhost:25599`). Befehle `connect`,
  `disconnect`, `restart`, `signal`/`await`, Prüfungen über `/mpcheck` (Test-Mod). Die Test-API gibt dem Server nur
  10 s zum Starten: der Gast darf erst starten, wenn der Server läuft.

## Stand

- 12.11. spät: Runden 1–3 integriert. Es gibt: Welt mit eigener Grafik für Ebene 1 (Set-Baukasten mit rund 50
  Blöcken und Requisiten, Wegweiser, Loot-Behälter platziert), Lauf-Logik, Charakter mit HUD, 38 Monster und Bosse
  (Ebenen 1–3), Ausrüstung/Affixe/Sets, Tränke, Bomben, Münzen, Loot, Prize Crates mit Unboxing, Stash, Schmuck,
  Show-Modul (Emcee mit 29 Anlässen, 149 Achievements, Hype/Fans, Fan Mail, Staffel-Rückblick, Bestenliste).
- Von der Hauptsitzung: Mehrspieler-Abnahme (`tools/crawltest/mp.sh`, 26 Prüfungen grün: gleiche Stage Door = eine
  Gruppe, Relog, Tod mit Remains, Server-Neustart mitten im Lauf, Set Strike), Schutz für Modpacks (`run.Guard`:
  Spieler ohne Lauf werden hinausgeführt, kein Friendly Fire, `RunEvents.LEFT`, Cash-Out per Config), Prize Trunks
  (Stash, ungeöffnete Crates, Münzen, Finale-Crate gehen beim Sieg als Truhen-Items mit), Tod nur einmal gemeldet.
- 13.11. früh: Runde 4 Spur A fertig (36 Zauber in sechs Schulen mit Zauberleiste; 16 Rollen und 14 Makeovers mit
  Auswahl im Casting Office), Spur B hat Karte (Minimap, Karten-Fenster, Pings) und Stage Door (Oberwelt-Struktur in
  3 Varianten und 3 Biom-Stilen, Casting-Call-Flyer, Advancements, benannte Plätze `world.Spots`/`Stations`)
  geliefert und arbeitet am zweiten Grafik-Durchgang (B7).
- 13.11. morgens: Runde 5 Spur A fertig (A8: Gaffer mit Tutorial, 4 Händler, Verkaufsautomat, Bewohner mit 6
  Quests, Hinweis-Toasts; A9: 12 Sponsoren mit Perks und Aufgaben, Interviews zwischen den Ebenen, Monitore, Fanpost,
  Trophäe, Hall-of-Fame-Tafel). Spur B: B7 (zweiter Grafik-Durchgang: Hallen mit Volumen und Kulissenteilen, Ebene 2
  als Requisitenlager, Ebene 3 als Filmstadt) und B9 (Regel-Baukasten: Meter, Zyklen, Ziele, Kampf-Modifikatoren;
  8 Fallen mit Entschärfen, Schreine, Geheimnisse) fertig; Audio läuft.
- Prüf-Runde läuft auf Spur A (R1 run+show, R2 magic+npc, R3 mob); für Spur B danach R4 item+profile,
  R5 world+map+rules (Skripte `briefs/crawl-review-lane-*.js`). Danach Ebenen 4–10 nach `docs/FLOORS.md` mit der
  Vorlage `briefs/FLOOR.txt` (eine Ebene pro Aufgabe, zwei Spuren parallel, eigene Dateien je Ebene).
- 13.11. 06:20 UTC: Audio fertig (183 Klänge, 181 per `tools/content/audio/synth.py` erzeugt, 11 Musik-Loops von
  Kevin MacLeod CC BY 4.0, Gelächter CC0 von OpenGameArt, alles in `CREDITS.md`; Jar 18,3 MB). Prüfberichte R1–R3
  ausgewertet: echte Fehler behoben (Remains verschwand bei zwei Betrachtern, statische Zustände über Welten hinweg,
  Rolle ohne Casting Office unterschreibbar, Abklingzeiten durch Relog zurückgesetzt, Boss-Leiste nach Tod);
  Entscheidungen der Leitung stehen am Ende von `docs/reports/R*.md`. Spur B prüft R4 (item+profile) und
  R5 (world+map+rules). Als Nächstes Spur A: Ebene 4 (`briefs/crawl-floors-a1.js`), Spur B danach Ebene 5.
- 13.11. 07:20 UTC: Prüfrunden R4 (item+profile) und R5 (world+map+rules) fertig und ausgewertet (12 weitere
  echte Fehler behoben, u. a. Crates gingen beim Öffnen verloren, Speicherlecks in Stash/Nav/Fallen, entschärfte
  Konfettikanone feuerte weiter). Entscheidungen der Leitung umgesetzt: Crates nur an der Unboxing Booth, Spinde
  schließen bei Entfernung, Bomben/Blitze treffen nur Monster (`item.Blast.canHit`), **Zellen liegen jetzt drei
  Regionen auseinander** (`Cells.STRIDE = 3`; bei Sichtweite 32 wurde sonst die Nachbarzelle vor ihrem Plan als
  Bedrock erzeugt), Casting Call sucht 64 Chunks und merkt sich die Antwort. 128 Server-Tests grün.
- HUD: Die Minimap verdeckte die Vanilla-Effektsymbole; sie stehen jetzt links daneben
  (`tools/crawltest/scripts/hud_effects.txt`).
- Modpack-Verträglichkeit: `tools/dev/compat.sh` (Sätze verbreiteter Mods von Modrinth, statischer Mixin-Abgleich
  `compat_scan.py`, Läufe daneben). Statischer Abgleich mit 37 Jars ohne harte Überschneidung. **Die Läufe mit
  fremden Jars (`compat.sh prod|client`) hat die Sicherheitsprüfung der Sitzung abgelehnt („Code from External“):
  nicht umgehen; der Nutzer muss das freigeben oder selbst starten.**
- Seite: Banner und Logos in `art/` (`tools/page/headers.py`), Entwurf der CurseForge-Beschreibung in
  `crawl-of-fame/curseforge/mod-description.md` (Platzhalter `{{MONSTERS}}`, `{{BOSSES}}`, `{{ACHIEVEMENTS}}`,
  `{{IMG}}` am Ende füllen; Screenshots fehlen noch).
- 13.11. 08:00 UTC: **Ebene 4 (Boiler Room) fertig** (0,68 Mio. Tokens, 90 min; 146 Tests grün; Urteil: gut, Hallen
  etwas dunkel und ähnlich → Hinweis in den Aufträgen der späteren Ebenen). Laufend: Spur A `crawl-floors-a2.js`
  (Ebene 6, dann 8), Lauf `wf_451d6ac5-454`; Spur B `crawl-floors-b1.js` (Ebene 5), Lauf `wf_f23b8e47-dcc`.
  Danach Spur B: `crawl-floors-b2.js` (Ebene 7, dann 9), dann Auftrag `briefs/SIDEKICK.txt` (Tierbegleiter als neues
  Modul; schließt die ungenutzte Fertigkeit Beast Handling). Spur A danach: Ebene 10 aus `briefs/F10.txt` (mit
  Abschnitt zum Finale: Siegessequenz, Abspann). `briefs/common.txt` enthält die Lehren aus den Prüfrunden.
- **Leistung gemessen** (`tools/dev/load.sh <läufe> <ebene>`, Profil mit `CRAWL_JFR=1` und `tools/dev/jfr_top.py`):
  acht gleichzeitige Läufe auf Ebene 1 kosten im Mittel 4,0 ms pro Server-Tick (p95 7,4 ms). Natürliches Spawnen ist
  im Dungeon abgeschaltet. Lehre: `helper.onEachTick` der Testumgebung legt je Tick bis zum Timeout einen Eintrag an
  (bei 2 Mio. Ticks unbrauchbar langsam); eigene Tick-Ereignisse nutzen und den Test über `succeedWhen` beenden.
  `balance.sh` und `load.sh` laufen jetzt allein (`-PtestFilter`).
- 13.11. 08:55 UTC: **Balance, zweiter Durchgang** (Commit `3911d1c`, 147 Tests grün, Mehrspieler-Abnahme 26/26):
  Ausrüstung wuchs nur in drei Materialstufen (Ebenen 1–3, 4–6, 7–10), Monster jede Ebene → Ebene 3 war härter als
  Ebene 4. Jetzt wächst Ausrüstung mit dem Item-Level (`item.Gear.levelScale`, 15 % pro Ebene; Stufe bleibt nur als
  Name im Tooltip). „Shock" setzte die Treffer-Abklingzeit des Opfers zurück → Rudel machten ein Vielfaches an Schaden
  (Raum 509 %, Boss Merrybolt bis 1500 %); behoben (Funke vor dem Schlag, Abklingzeit bleibt). Bosse halten höchstens
  vier Helfer. `tools/dev/balance.sh` zeigt jetzt je Kampf den Boss und **wer den Schaden gemacht hat** (danach
  abstimmen). Gemessen: Räume Ebenen 1–4 bei 0–82 %, Bosse meist 144–250 %. Offen: Ebene 5 wurde von Spur B noch
  gegen die alte Ausrüstungskurve abgestimmt (Ausrüstung dort jetzt rund 10 % stärker) → nach Lieferung nachmessen;
  am Schluss alle Ebenen mit `balance.sh` und `load.sh` durchmessen.
- 13.11. 09:35 UTC: **Ebene 5 (Sunken Archive) fertig** (0,77 Mio. Tokens, 141 min; 190 Tests grün; Urteil: gut, eigener
  Ort, Gezeiten klar lesbar; nachgemessen: Räume 0–40 %, Bosse 103–203 %, Last 3,0 ms pro Tick bei vier Läufen).
  Ebene 6 ist inhaltlich gepusht (Spur A stimmt ab, dann Ebene 8). Laufend: Spur A `crawl-floors-a2.js`, Lauf
  `wf_451d6ac5-454`; Spur B `crawl-floors-b2.js` (Ebene 7, dann 9), Lauf `wf_26b12359-f29`. Danach Spur A: Ebene 10
  (`F10.txt`, ID `F10-floor`); Spur B: `SIDEKICK.txt`, dann `GALLERY.txt` (Screenshots der Seite, füllt auch die
  Platzhalter der CurseForge-Beschreibung). Kosten Ebenen bisher: 0,68 + 0,77 Mio.
- 13.11. 12:27 UTC: **Container-Neustart Nr. 3** (gleicher Kernel, nichts verloren: Agenten hatten lokal committet).
  Ebene 6 (Overgrowth) war fertig und abgenommen (hell, drei Raumcharaktere). Neu gestartet mit frischen Skripten
  (aktuelle Aufträge inkl. Klangprüfung und gefilterten Testläufen): Spur A `crawl-floors-a3.js` (Ebene 8 fortsetzen,
  dann Ebene 10 mit Finale), Lauf `wf_8e70e974-bce`; Spur B `crawl-floors-b3.js` (Ebene 7 fortsetzen, dann Ebene 9),
  Lauf `wf_b46bbb44-bc7`. Danach Spur B: `SIDEKICK.txt`, dann `GALLERY.txt`.
- Seit 10:00 UTC zusätzlich: Stellhebel je Ebene (`health_scale`, `damage_scale` im Roster) für die Schlussabstimmung;
  Ebene 5 nachgebessert (drei Klangnamen, ein Test hing vom gewürfelten Grundriss ab; gefunden durch `prod.sh` und
  einen vollen `./gradlew build`, der alle Tests ausführt); Mehrspieler-Abnahme zeigt jetzt auch Rolle und Makeover
  am zweiten Client (26/26). Gefilterte Tests: `tools/dev/gametest.sh "-PtestFilter=*:floor5game_tests_*"`.
- Gefunden beim eigenen Durchlauf (`tools/crawltest/scripts/journey.txt`): eine Stage Door entstand in einem Dorf und
  war von einem Haus versperrt → Türen halten jetzt 10 Chunks Abstand zu Dörfern (`exclusion_zone`).
- 106 Server-Tests grün auf frischer Testwelt (`tools/dev/gametest.sh` löscht die Testwelt vor jedem Lauf; Tests mit
  Test-Spielern müssen auf geladene Chunks warten: `managedBlock`).
- Von der Hauptsitzung zusätzlich: Balance-Modell und Simulation (`docs/BALANCE.md`, `tools/dev/balance.sh`: ein
  Test-Spieler kämpft Räume und Bosse durch; Monster wuchsen pro Level viel schneller als der Spieler, Formeln und
  Boss-Werte angepasst), Design der Ebenen 4–10 (`docs/FLOORS.md`), README/LICENSE/CREDITS, Doku für Pack-Macher
  (`docs/DATAPACKS.md`), Mehrspieler-Abnahme auf dem integrierten Stand erneut grün (26/26), 73 Server-Tests.
- Danach: Prüf-Runde (4 Agenten, je 2 Module, `briefs/review.txt`), Balance nachmessen, Ebenen 4–10 nach
  `docs/FLOORS.md` (größter verbleibender Posten, grob 5 Mio. Agenten-Tokens), Abschluss.
- Urteil zur Grafik nach B5: Flure und Green Rooms gut; große Räume zu gleichförmig (niedrig, braun, Requisiten im
  Raster). Auftrag B7: Raumhöhe nach Größe, Zonen und Blickfang, Licht als Führung, Farbe, Boss-Arenen als Bühne,
  eigene Sprache für Ebene 2 (Lager bei Nacht) und 3 (Filmstadt in der Höhle).
- Beobachtung Balance: nackter Level-1-Spieler verliert im ersten Kampfraum in 3 s 17 von 40 Leben; Boss Ebene 1 tötet
  ihn in Sekunden. Balance-Durchgang mit Auto-Kampf-Bot einplanen.
- Kosten bisher (Agenten-Tokens): Buch-Auswertung 6,2 Mio., Runde 1 1,2 Mio., Runde 2 1,6 Mio., Runde 3 rund 1,5 Mio.,
  Runde 4 je Spur 0,9 und 1,1 Mio., Runde 5 je Spur 1,0 und 0,9 Mio. Summe bis hier rund 14 Mio.
- **13.11. abends: Zehn Ebenen fertig** (281 Tests), Zwischenstand-Jar Nr. 2 in `crawl-of-fame/builds/`. Der Nutzer
  hat gespielt. **Seine Rückmeldung bestimmt Phase 3b** (Reihenfolge = Gewicht): mehr 3D-Modelle für Items und
  Rüstungen (Schild in der Hand!), feinere Texturen überall, Item-Animationen; Waffen und Inventar-Filter schwer zu
  verstehen, unklar was man anlegen soll, bessere Sortierung, **im Inventar scrollen**; UI nicht überall richtig
  skaliert; **Tutorial im Dungeon** (geführte Einweisung auf Ebene 1, eigene Figuren und Texte); Musik nicht
  dauernd, vor allem nicht außerhalb von Kämpfen; funktionale Blöcke, Dinge zum Plündern, interaktive Räume statt
  nur Monster; viele Dinge zum Ausprobieren und Builds über den Lauf; **Ansager und NPCs als echte Sprachausgabe**
  (Englisch, gute Emotion, genaue Regie); **die Show automatisch erzeugt auf einem großen Fernseher** in Green Rooms
  oder Küchen, wo NPCs Essen geben. Erledigt: Tooltips auf dem Crate-Ergebnis (`unbox_hover.txt`).
- Aufträge dafür (alle in `crawl-of-fame/briefs/`): Spur A: `UI1` (läuft, Bausatz + Hauptschirme) → `ITEMS`
  (Power-Wert, Item-Karte mit Vergleich, scrollender Stash mit Filtern/Suche/Sortierung, Loadout, Armoury) →
  `TUTORIAL` (Rehearsal Wing mit dem Gaffer) → `ROOMS1` (Durchsuchen, Requisiten, das Set als Waffe, Gefangene,
  Kopfgeld) → `ROOMS2` (Bonus Rounds: zehn Spiele, Publikums-Aufgaben) → `BROADCAST` (Fernseher, Kantine, Köchin)
  → `UI2`. Spur B: `SIDEKICK` (fertig, 296 Tests) → `VOICE` (läuft: Sprechtext, Wiedergabe, Musik nur in Kämpfen)
  → `MODELS` (3D-Waffen, Schilde, Rüstungsformen, Item-Leben, Icons neu) → `BUILDS1` (Technik je Waffentyp, zehn
  neue Waffentypen, Zustände/Kombos, Übungspuppe mit DPS, zwei Loadouts) → `BUILDS2` (Rewrites: 1 aus 3, 90 Perks,
  regelbrechende Uniques, Script Doctor) → `CREATURES1–3` → `GALLERY`.
- **Sprachausgabe, Entscheidung nach Test** (Arbeitsordner `$SP/voice`, nichts davon im Repo): Qwen3-TTS
  VoiceDesign 1.7B (Apache 2.0) spricht nach Stimm-Beschreibung plus Regie-Anweisung je Satz, wortgenau (Whisper),
  aber die Klangfarbe schwankt zwischen Sätzen (Sprecher-Ähnlichkeit 0,79). Deshalb zweiter Schritt: Chatterbox-VC
  (MIT, `ResembleAI/chatterbox` `s3gen`) bringt jede Zeile auf die Referenz der Figur (danach 0,92; Wörter und
  Betonung bleiben). Tempo auf der ausgelasteten Maschine: Entwurf im Stapel (8–9 Sätze) ×4 Echtzeit, VC ×4,
  zusammen rund 8 s Rechenzeit je Sekunde Sprache; einzeln ×12. Chatterbox Turbo war langsamer (×20–30) und hat
  keine Regie; Kokoro (×1,5–2) dient nur als Platzhalter (`$SP/voice/draft.sh`). Hörproben für den Nutzer:
  https://claude.ai/artifact/YCniHiBsmdrUSUWPDqLNe6 (Ansager A/B/C; ohne Antwort weiter mit A). Vertrag mit dem
  Agenten steht im Auftrag `VOICE.txt` (Sprechtext `tools/content/voice/script/<sprecher>.json`, `cast.json`,
  Presets, `process.py`); die Aufnahme (`synth.py`: Entwurf → Wörter prüfen → VC → Stimme prüfen → Preset → OGG,
  mit Wiederholung) fährt die Hauptsitzung als Hintergrund-Lauf und committet in Etappen.
- Kosten seit der letzten Summe: R-B 0,56, F4 0,68, F5 0,77, F6 ~0,7, F7+F9 0,90, F8 + F10-Abbruch 1,12,
  SIDEKICK 0,28 + 0,62, F10-Rest 0,27, UI1 läuft. Summe rund 20 Mio.
- **13.11. 21:10 UTC, Antwort des Nutzers auf die Hörproben und neue Wünsche:** (1) „Habe immer einen Plan, was wir
  schon gemacht haben und noch machen müssen“: der Plan steht in `docs/PLAN.md` im Mod-Repo (Phase 3b, in der
  Reihenfolge seiner Liste) und wird nach jedem Schritt nachgeführt; in jeder Antwort kurz den Stand nennen.
  (2) Stimmen: **Ansager = Kandidat C** (sehr tiefe Trailer-Stimme) **mit etwas schnellerem Tempo**; die „eine
  Stimme, sechs Stimmungen“ klingt super; die schnelle Engine gefällt ihm nicht: „Wir investieren die Zeit.“
  Referenz liegt als `$SP/voice/work/ref/emcee.wav` (= `cast/c_trailer_intro.wav`), `cast.json` bekommt für den
  Ansager die Beschreibung C mit zügigem Tempo und `"tempo": 1.06`. (3) **Fliegende Säbel zu schwer und schwer zu
  treffen** → umgebaut zum Duellanten (größer, langsamer, angekündigter Stoß, danach liegt er 2,5 s wehrlos);
  dabei gefunden: der Anlauf eines Sturmangriffs wurde nur im KI-Schritt gezählt, den ein stillstehendes Monster
  nicht bekommt (Monster mit CHARGE froren ein) → Zähler laufen jetzt in `Abilities.held`. (4) **Alles auf Ebene 1
  und 2 ist Show-Thema; er will sehr viele verschiedene Themes, zufällig gewählt, je mit eigenen Mobs, Stil,
  Räumen** → Auftrag `THEMES1` (Ort und Tiefe trennen, Reihenfolge pro Lauf auslosen) und danach neue Welten nach
  `docs/WORLDS.md` (zehn Entwürfe: Hollowmere Manor, Sun Tomb, Arcade Zero, Toy Chest, Halcyon Nine, Idol Steps,
  Sugar Works, Smugglers' Grotto, Pop-Up Kingdom, Deep Seam), Vorlage `briefs/PLACE.txt`
  (`brief.py W1-manor PLACE.txt b NAME="Hollowmere Manor"`). (5) „Setze all das um, gib mir dann eine neue Jar und
  entwickle weiter; alles, was Spieler sehen und tun, muss top sein.“ Das Tutorial bleibt im Dungeon (seine
  Klarstellung; die von ihm zurückkopierte Liste nennt noch die alte Fassung).
- Aufnahme-Pipeline (`$SP/voice/synth/`, noch nicht im Repo): Entwurf in Vierer-Stapeln gleicher Länge mit eigener
  Obergrenze je Zeile, dann Stimm-Angleich mit dem Zwei-Schritt-Decoder (`s3gen_meanflow` aus
  `ResembleAI/chatterbox-turbo`: Echtzeit statt 4- bis 17-fach, gleiche Sprecher-Ähnlichkeit), dann Wortprüfung
  auf dem fertigen Ton (faster-whisper small.en) und Sprecher-Prüfung, dann Preset und Ogg. Wasserzeichen der
  Bibliothek bleibt an. Test mit 7 Zeilen: alle im ersten Versuch gut. Engpass ist der Entwurf (unter Last der
  Agenten bis ×18 Echtzeit).
- **13.11. 23:30 UTC:** UI1 geliefert und abgenommen (Bausatz `client.ui`, `docs/UI.md` bindend; Skalierungsfehler der
  Attribut-Zeilen auf niedrigen Fenstern von der Leitung behoben: `StatsTab.compact`, `ui_small.txt`). VOICE
  geliefert (Modul `voice`: 802 Zeilen, 28 Sprecher, Wiedergabe mit Warteschlange und Ducking, Musik nur in Kämpfen;
  301 Tests). Erste 87 Ansager-Aufnahmen sind im Modul (`tools/content/voice/lead/publish.sh <staging>`), Pipeline
  liegt jetzt im Repo unter `tools/content/voice/lead/` (README dort), Herkunft und Lizenzen in `CREDITS.md`.
  Aufnahme läuft als Dauerläufer (`lead/supervise.sh`, zwei Threads; Steuerdateien im Arbeitsordner
  `$SP/voice/work`: `repo.txt`, `PAUSE`, `STOP`, `QUIT`); bei jedem Check-in: `publish.sh $SP/voice/out_ogg`,
  committen, pushen. Hörproben-Seite hat oben vier echte Aufnahmen (Stimme C, Tempo 1,06).
- **Ultracode ist an** (Meldung des Systems): Aufgaben laufen wieder über das Workflow-Werkzeug, je Spur ein
  Workflow mit Qualitätsschleife aus `briefs/gen2.py`: Bauen → zwei unabhängige Prüfungen nacheinander (Linsen in
  `briefs/lenses_<AUFGABE>.txt`, allgemein `lenses_default.txt`; Prüfer ändern nichts) → Korrekturen (`fix2.txt`).
  Weiter höchstens zwei Agenten gleichzeitig (Maschine: ein Minecraft-Lauf zur Zeit). Der Workflow reicht den
  Agenten die letzte Nutzer-Nachricht als Auftrag weiter: die vom 13.11. 21:10 deckt alles ab; nach einer kurzen
  Nachricht des Nutzers wieder das Agent-Werkzeug mit `brief.py` nehmen. Laufend: Spur A `crawl-themes-a6.js`
  (THEMES1), Spur B `crawl-items-b7.js` (erst Prüfung und Korrektur von VOICE, dann ITEMS).
- Zusammenführen ist Sache der Leitung: THEMES1 hat die Regel-Texte von `show.floor.rule.<n>` auf
  `world.place.<id>.rule` umgestellt (dazu `show.floor.service.casting|coins|sponsors`, `rules.hint.casting_floor`);
  der Sprechtext (`tools/content/voice/lines/emcee_floors.txt`) folgt dem jetzt. Nach jedem Merge
  `python3 tools/content/voice/build.py` laufen lassen: es meldet Schlüssel, die es nicht mehr gibt.
- Zwischenstand-Jar 3 kommt, sobald der Bau-Schritt von THEMES1 „fertig“ meldet (dann voller Testlauf grün):
  `./gradlew assemble`, `tools/dev/prod.sh`, nach `crawl-of-fame/builds/`, Roh-Link an den Nutzer.
- **13.11. 23:46 UTC: Container-Neustart Nr. 4.** Nichts verloren (Scratchpad mit Sprachmodellen, Aufnahmen, Worktrees
  mit lokalen Commits blieben). Wieder gestartet: Aufnahme-Dauerläufer (`nohup tools/content/voice/lead/supervise.sh`
  aus dem Haupt-Checkout; er räumt `STOP`/`QUIT` beim Start weg), beide Workflows per
  `Workflow({scriptPath, resumeFromRunId})` (Spur A `crawl-themes-a6.js` / `wf_fd2adf47-3f4`, Spur B
  `crawl-items-b7.js` / `wf_f8e4cb2a-61a`). Stand der Aufnahmen: 113 Ansager-Zeilen im Modul.

- **14.11. 01:30 UTC:** Zwischenstand-Jar 3 geliefert (`crawl-of-fame/builds/…-zwischenstand-3.jar`, Stand 54a2bbc:
  zufällige Orte, neue Oberfläche, Sidekicks, erste Ansager-Aufnahmen, Säbel- und Sturmangriff-Korrektur). THEMES1
  ist samt zwei Prüfungen und Korrekturen fertig (323 Spieltests; Entscheidungen der Leitung im Bericht). VOICE:
  Prüfung und Korrekturen fertig (Sprechtext jetzt 850 Zeilen, 13 485 Wörter, rund 90 Minuten).
  `tools/content/voice/lead/publish.sh <staging> <work>` veröffentlicht nur Aufnahmen, deren Zeile noch so lautet wie
  aufgenommen (Digest im Zustand), und entfernt überholte. Stand der Aufnahme: 138 von 850.
- Laufend seit 01:30: Spur A `crawl-tutorial-a7.js` / `wf_87ef502a-355` (TUTORIAL: Rehearsal Wing vor dem Ort der
  Tiefe 1, Linsen `lenses_TUTORIAL.txt`), Spur B weiter `crawl-items-b7.js` / `wf_f8e4cb2a-61a` (ITEMS im Bau, dann
  zwei Prüfungen und Korrekturen). Danach: Spur A erste neue Welt (`brief.py W1-manor PLACE.txt a NAME="Hollowmere
  Manor"` bzw. `gen2.py` mit `PLACE.txt`), Spur B MODELS.
- Workflow-Weitergabe geprüft (Sonde): Ein Workflow, der in einem durch eine Benachrichtigung ausgelösten Zug
  startet, gibt den Agenten **keinen** Nutzer-Auftrag mit (sie sehen nur die Aufgabe); auch fortgesetzte Workflows
  liefen. Nach einer kurzen Nutzer-Nachricht trotzdem den ersten Agenten kontrollieren (Transkript im
  Workflow-Ordner: liest er die Unterlagen oder lehnt er ab?).
- **Platzhalter-Aufnahmen** (`*.draft.ogg`, schnelle Engine, vom Nutzer abgelehnt) hört kein Spieler mehr: Der Client
  lässt sie aus dem Index, außer mit `-Dcrawl.voice.drafts=true` (setzt der crawltest-Lauf). Unvertonte Zeilen sind
  nur Text.
- **Das Spiel hören** (neu, Leitung): `CT_AUDIO=1 tools/crawltest/run.sh <skript> <ordner>` lässt den Test-Client den
  Ton über den Wave-Writer von OpenAL Soft (liegt LWJGL bei; `ALSOFT_DRIVERS=wave`, `ALSOFT_CONF`) nach
  `<ordner>/game.wav` schreiben. Skript-Befehle dafür: `pace <ticks>` (Echtzeit, 20 Ticks/s, ohne Bilder; `wait`
  läuft so schnell wie die Maschine kann), `vol <quelle> <0-1>`, `beep` (Ton zum Abgleich von Aufnahme und Log),
  `amark <name>`. Auswertung: `$SP/voice/q312/bin/python tools/crawltest/listen.py <ordner>` (Wörter per
  faster-whisper, Pegel: Ruhe beim Erkunden, Musik im Kampf, Musik unter einer Ansage, Übersteuerung) und
  `game.mp3` als Hörprobe für den Nutzer. Skript: `tools/crawltest/scripts/listen.txt`.
- **14.11. 02:20 UTC, Ton-Mischung nach den ersten Mitschnitten (Leitung):** Gemessen mit `listen.py`: Kampfmusik war
  so laut wie die Stimme → `MusicDirector.LEVEL` 0,5 (vorher 0,8), unter Sprache −11 dB (vorher −8). Jingles/Fanfaren
  (`show.*`, −17,7 dB RMS, 0,7–3,5 s laut) starteten im selben Bild wie die Ansage → `VoiceQueue.hold` +
  `ClientShow.leadMs(cue)` (Stimme setzt nach dem lauten Teil ein, höchstens 1,5 s) und `audio.CueSound` (Jingle −9 dB
  unter Sprache). Boss-Karte spielt über `ClientShow.play` und spricht die Vorstellung selbst (Chat-Zeilen erreichen
  Clients mit ausgeblendetem Chat nicht; im Test-Skript deshalb `chat on`). Ansagen hängen an ihren Einblendungen:
  ein Mitschnitt braucht gezeichnete Bilder (`pace` zeichnet alle 250 ms eins). `process.py`: Lautheit bleibt bei
  Vorbis-Überschwingern erhalten (nur Spitzen werden gedrückt). Übergangsregel: Solange nur ein Teil der Varianten
  eines Anlasses aufgenommen ist, nimmt der Ansager die aufgenommenen (`Emcee.voiced`, gesetzt vom Modul voice aus
  dem Index im Jar). Erster Boss-Sieg entschärft: ein Kisten-Jingle pro Tick (`audio.CrateJingles`), eine Chat-Zeile
  für alle Achievements eines Ticks, eine Level-Zeile. Frachtschalter in Prop Storage ohne Tresor (Tiefe 1) liefern
  jetzt eine Kiste. Offene Frage an den Nutzer: Tempo/Lautstärke des Ansagers und Musik-Pegel (Hörprobe-Seite).
- **14.11. 02:55 UTC:** Alles gepusht (Mod-Repo b2f90fe): ITEMS-Bau von Spur B zusammengeführt (333 Spieltests auf
  dem gemeinsamen Stand), Ton-Mischung, Frachtschalter, 171 von 852 Aufnahmen (Ansager Stufe 1 komplett, Referenzen
  für 23 Sprecher). Hörprobe aus dem Spiel steht oben auf der Hörproben-Seite (Lauf `$SP/listen/run4`, Seite neu
  bauen: `python3 $SP/voice/page/build.py <lauf-ordner>`, dann dieselbe Datei wieder veröffentlichen). Der Nutzer ist
  gefragt: Tempo/Lautstärke des Ansagers, Musik-Pegel. Laufend: Spur A TUTORIAL-Bau (`wf_87ef502a-355`), Spur B
  ITEMS-Prüfungen (`wf_f8e4cb2a-61a`). Vorbereitet, noch nicht gestartet: Spur A danach
  `workflows/scripts/crawl-manor-a8.js` (erst unabhängige Prüfung der Ton-Änderungen der Leitung „AUDIOMIX“ mit
  `lenses_AUDIOMIX.txt`/`delivered_AUDIOMIX.txt`, dann Hollowmere Manor); Spur B danach MODELS (`gen2.py … MODELS
  MODELS.txt … lenses_MODELS.txt`). Entscheidungen zu ITEMS (nach den Prüfungen in den Bericht schreiben): Suche nur
  über IDs und englische Namen ist in Ordnung; Stash rastet zeilenweise; Ausrüsten-Taste `I`; Zweihänder sperren
  künftig die Nebenhand (steht als Punkt 4b im Auftrag BUILDS1). Regel der Leitung für eigene größere Änderungen:
  von einer Spur unabhängig prüfen lassen (PRE-Stufe in `gen2.py`), damit es bei zwei Agenten bleibt.
- **14.11. 03:30 UTC, HUD (Leitung, gepusht als 8eb1658):** Bei 1080p mit Standard-GUI-Skalierung („Auto“ = 480×270
  GUI-Pixel; im Test 1280×720 GUI 3 oder 854×480 GUI 2) lag die Boss-Leiste quer über der Bildmitte. Jetzt stehen
  Boss-Name und Lebensbalken auf schmalen Bildschirmen in der oberen Leiste statt des Ebenen-Namens
  (`CrawlerHud.centreHead`, `BossHud.StripPart`); Monster-Namensschilder schrumpfen unter sechs Blöcken Abstand
  (`MonsterRenderer.submitNameDisplay`; gemessen: auf 1,4 Blöcke nur noch 1,6-mal so breit wie auf 6 statt 4,3-mal).
  Regeln dazu in `docs/UI.md` („The HUD in a fight“). Offen für UI2 (Auftrag ergänzt, Punkt 7): kompaktes HUD von
  selbst bei kleiner GUI-Fläche (die linke Spalte nimmt bei 480×270 rund 45 % der Höhe). Prüf-Skripte der Leitung:
  `$SP/lead_hud3.txt`, `$SP/lead_plate.txt` (mit `tick freeze`; `summon` mit NBT ruft kein `finalizeSpawn` auf, dann
  fehlt das Namensschild). Lehre: bei jedem HUD-Teil auch 427×240 GUI-Pixel ansehen.
- **14.11. 03:45 UTC, Referenzstimmen:** Die Referenz eines Sprechers bestimmt alle seine Zeilen, und niemand hört
  sie. Von den ersten 23 automatisch gewählten passten sechs nicht zur Beschreibung (Männerstimme für Rosalind und
  Odile, Frauenstimme für Fennick, Pip viel zu hoch, Tilda zu hoch, Vesna knapp zu tief). Jetzt: `synth.pitch_band`
  leitet aus der Beschreibung einen erlaubten Bereich der mittleren Tonhöhe ab (Geschlecht aus Pronomen und
  Stimmfach, Lage aus Wörtern wie „bass“, „tenor“, „contralto“), `make_refs` verwirft Kandidaten außerhalb und zieht
  beim nächsten Versuch andere Stimmen (`ref/<sprecher>.tries`), `audit_refs.py --fix` prüft und repariert
  vorhandene Referenzen (nach jedem neuen Referenz-Durchgang laufen lassen). Vor Aufnahmen anderer Sprecher immer
  erst prüfen. Der laufende Durchgang wurde mit `STOP` beendet; der Aufseher startet nach zehn Minuten neu und
  entwirft die fünf fehlenden Referenzen mit der Prüfung. Die Ansager-Referenz (vom Nutzer gewählt) liegt bei 75 Hz.
- Hörproben-Seite (Version 5, 03:55 UTC): neuer Abschnitt „Die Stimmen der Figuren“ mit der Referenz jeder Figur
  (Veto-Möglichkeit für den Nutzer, bevor Zeilen aufgenommen sind). Neu bauen: `python3 $SP/voice/page/make_refs_json.py
  <repo>`, dann `python3 $SP/voice/page/build.py $SP/listen/run4`, dann dieselbe Datei veröffentlichen. Nach dem
  Neuentwurf der fünf verworfenen Referenzen (Fennick, Odile, Rosalind, Vesna, Pip) und sobald Host, Werbesprecher,
  Quill und Vesper Referenzen haben: Seite neu bauen und veröffentlichen. Nennt der Nutzer einen Namen: `ref/<id>.wav`
  und `.desc` löschen, `.tries` erhöhen, ggf. Beschreibung in `cast.json` anpassen, Zeilen des Sprechers aus
  `state.json` nehmen (bei gestopptem Aufseher).
- **14.11. 04:25 UTC:** Spur B: ITEMS fertig (Bau, zwei Prüfungen, neun Befunde: acht behoben, einer entschieden; 348
  Spieltests; Entscheidungen der Leitung im Bericht: Fernkampf-Krits und Waffen-Sets kommen mit BUILDS1 (Punkt 4c),
  Zweihänder sperren die Nebenhand (4b), Rest an UI2). Neu gestartet: `crawl-models-b8.js` / `wf_4c66326c-72b` (MODELS:
  3D-Waffen, Schilde, Rüstungsformen, Beute-Strahlen, Icons; Linsen `lenses_MODELS.txt`). Spur A weiter
  `wf_87ef502a-355` (TUTORIAL: Bau im Repo, zweite Prüfung läuft, dann Korrekturen); danach `crawl-manor-a8.js`.
  Fund der Leitung: der einmal gescheiterte Gezeiten-Test war ein echter seltener Fehler (aus dem Becken gelaufenes
  Wasser blieb bei Ebbe liegen, weil die Regel Blöcke ohne Nachbar-Updates setzt): `Floor5Rule.layer` räumt jetzt
  bei Ebbe jedes Wasser des Raums auf dieser Höhe ab; Test mit „schlafendem“ Wasserblock (`UPDATE_SKIP_ON_PLACE`).
  Lehre: ein „Timing-Fehler unter Last“ im Test ist erst dann einer, wenn die Zahlen dazu passen (hier: 240 Ticks
  gewartet, Wasser blieb).
- **14.11. 05:15 UTC:** TUTORIAL fertig (Bau, zwei Prüfungen, 14 Befunde, alle behoben; 357 Spieltests; Entscheidungen
  der Leitung im Bericht). Spur A neu gestartet: `crawl-manor-a8.js` / `wf_10323761-684` (erst Prüfung „AUDIOMIX“ der
  Ton-Änderungen der Leitung mit zwei Linsen und Korrekturen, dann Hollowmere Manor mit Prüfungen). Spur B weiter
  `wf_4c66326c-72b` (MODELS-Bau). Mod-Repo-Stand eb912ad. Jar 4 in Arbeit (Blick der Leitung auf den Wing bei
  854×480, Produktions-Check, `./gradlew assemble`). Aufnahme: 218 von 941.
- **14.11. 05:35 UTC: Zwischenstand-Jar 4 geliefert** (`crawl-of-fame/builds/crawloffame-0.1.0-mc26.3-zwischenstand-4.jar`,
  32,6 MB, Mod-Stand eb912ad; Jar 3 entfernt): Gegenstände verständlich (Power, Itemkarte, Stash mit Filtern), Tutorial
  im Dungeon, korrigierte Ton-Mischung, HUD bei kleiner GUI-Fläche, 218 vertonte Zeilen, Korrekturen aus vier
  Prüfrunden; 357 Spieltests, Produktions-Check sauber, Wing bei 854×480 von der Leitung angesehen. Bekannt und dem
  Nutzer gesagt: noch keine 3D-Modelle, keine neuen Welten, Nebenfiguren meist nur Text. Jar 5 nach MODELS und
  Hollowmere Manor.
- **14.11. 06:50 UTC:** Mod-Repo e359c50. Leitung: (1) Ansager-Banner: wo der Text neben dem „EMCEE“-Schild schmaler
  als 190 wäre (jede GUI unter ~600 Breite, also auch 1080p mit Standard-Skalierung), steht das Schild als Kopfzeile
  und der Text nutzt die ganze Breite; bis fünf Zeilen bei jeder Breite, sonst „…“. Vorher passten 122 der 468
  Ansager-Zeilen bei 427 GUI-Breite nicht, jetzt 12. Bilder: `/home/user/shots/lead-banner*`. Lehre für Skripte:
  die Uhr des Banners ist Echtzeit, ein Tick des Test-Clients dauert in großen Fenstern länger: nach `voice banner`
  höchstens ~25 Ticks warten. (2) Aufnahmen: `process.py` kürzt Pausen im Satz auf 0,7 s (51 von 290 Aufnahmen hatten
  bis 2,5 s; die Tonprüfung `audio/check.py` lässt höchstens 1,2 s zu und schlug bei Wren an). 277 von 944 Zeilen
  (neu: Gaffer im Rehearsal Wing). Werbesprecher: zwei Kandidaten zu hoch, Beschreibung beginnt jetzt mit „A man …
  deep“. Quill und Vesper bekommen ihre Referenz erst mit ihrer Stufe.
- Prüfung „AUDIOMIX: timing“ (Spur A, 05:52 UTC) fand fünf echte Fehler in der Warteregel der Leitung (Abstieg: Regel
  der Karte vor der Ankunftszeile; ein Halt setzt die 4-s-Lebenszeit wartender Zeilen zurück; die Sammler am
  Tick-Ende laufen vor `ShowFlow.tick`, daher weiter zwei „unlocked“-Zeilen und ein verlorener Gold-Jingle; ein
  Banner verliert seine Stimme an eine höhere Zeile; Ankunftszeilen ignorieren „aufgenommene Variante zuerst“).
  Korrekturen macht Spur A nach der zweiten Linse („ears“). Lehre bestätigt: eigene größere Änderungen der Leitung
  immer unabhängig prüfen lassen.
- MODELS-Bau (Spur B, 06:01 UTC, 359 Tests): 3D-Modelle für alle Waffen/Schilde, 25 Unikate mit eigener Form,
  sechs Rüstungssets als Kostüme, Drops mit Strahl. Vom Bau NICHT geliefert: Schlag-Bögen, Blitz beim Blocken,
  Wurf-Nachschwung, Schimmer beim vollen Schlag, Amulett/Abzeichen am Körper, Münzstapel, Icon-Überarbeitung.
  Blick der Leitung auf die Bögen (`/home/user/shots/MODELS`): Schild beim Blocken in Ego-Sicht nicht im Bild,
  Zweihänder in Ego-Sicht kaum zu sehen, Stab und Hellebarde wie eine Lanze getragen, Strahlen dünn, Unikat-Icons
  passen nicht zu den Modellen. Dafür neuer Auftrag **MODELS2** („the item in action“: Clip-System für gehaltene
  Gegenstände, ein Schlag je Waffenklasse leicht/voll, Bögen und Treffer-Funken, Schild im Bild, Fernkampf, Zaubern,
  Trageposen, Icons, Münzen, Strahlen; Beweis als Bildstreifen pro Tick; Linsen `lenses_MODELS2.txt`): auf Spur B
  direkt nach den MODELS-Korrekturen, vor ROOMS1 (Punkt 4 der Liste des Nutzers nennt Item-Animationen ausdrücklich).
  BUILDS1 soll seine Techniken später als Clips in dieses System hängen.
