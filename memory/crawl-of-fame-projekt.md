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
- Runde 4 läuft (nach einem Container-Neustart fortgesetzt): Spur A = Zauber (A6), dann Rollen/Makeovers (A7);
  Spur B = Karte (B6), Stage Door als Oberwelt-Struktur + benannte Plätze (B8), zweiter Grafik-Durchgang (B7).
- Danach: A8 NPCs/Tutorial/Händler/Quests, B9 Fallen/Schreine/Ebenen-Regeln, Audio (numpy + ffmpeg/libvorbis
  vorhanden; incompetech und opengameart erreichbar, kenney und freesound gesperrt), Prüf-Runde (4 Agenten, je
  2 Module), Balance, Ebenen 4–10, README/CREDITS/CurseForge-Text. Stand-Liste: `docs/PLAN.md` im Mod-Repo.
- Urteil zur Grafik nach B5: Flure und Green Rooms gut; große Räume zu gleichförmig (niedrig, braun, Requisiten im
  Raster). Auftrag B7: Raumhöhe nach Größe, Zonen und Blickfang, Licht als Führung, Farbe, Boss-Arenen als Bühne,
  eigene Sprache für Ebene 2 (Lager bei Nacht) und 3 (Filmstadt in der Höhle).
- Beobachtung Balance: nackter Level-1-Spieler verliert im ersten Kampfraum in 3 s 17 von 40 Leben; Boss Ebene 1 tötet
  ihn in Sekunden. Balance-Durchgang mit Auto-Kampf-Bot einplanen.
- Kosten bisher (Agenten-Tokens): Buch-Auswertung 6,2 Mio., Runde 1 1,2 Mio., Runde 2 1,6 Mio., Runde 3 rund 1,5 Mio.
