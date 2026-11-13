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
