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

## Test-Werkzeuge

- `tools/dev/gametest.sh`: Server-Spieltests aller Module (Stand Runde 2: 35 Tests).
- `tools/crawltest/run.sh <skript> <ordner>`: ferngesteuerter Client mit Screenshots (Xvfb + EGL; nach einem
  Container-Reset `apt-get install -y libegl1 libegl-mesa0`).
- `tools/crawltest/mp.sh <host> <gast> <ordner>`: Mehrspieler-Test. Der Host startet einen Dedicated Server im
  eigenen JVM (Skript-Befehl `server`), der Gast ist ein zweiter Client (`join localhost:25599`). Befehle `connect`,
  `disconnect`, `restart`, `signal`/`await`, Prüfungen über `/mpcheck` (Test-Mod). Die Test-API gibt dem Server nur
  10 s zum Starten: der Gast darf erst starten, wenn der Server läuft.

## Stand

- 12.11. abends: Runde 1 und 2 fertig und integriert. Es gibt: Welt (Dimension, Generator, Ebenen 1–3 aus
  Vanilla-Blöcken), Lauf-Logik (Stage Door, Cast, Sendezeit, Set Strike, Treppen, Remains, Sieg), Charakter (Werte,
  Level, Fertigkeiten, HUD, Fenster), 38 Monster und Bosse für Ebenen 1–3 mit Regisseur und Boss-Arenen, Ausrüstung
  mit Affixen und Sets, Tränke, Bomben, Münzen, Loot, Prize Crates mit Unboxing, Stash, Schmuck.
- Runde 3 läuft: Spur B = Welt-Grafik Ebene 1 (B5), dann Minimap und Karte (B6); Spur A = Show-Modul mit Emcee,
  Achievements, Hype/Fans (A5), dann Zauber (A6). Die Hauptsitzung baut die Mehrspieler-Prüfung.
- Danach: B7 (Ebenen 2–3 im Stil von Ebene 1, Stage Door als Oberwelt-Struktur, benannte Plätze für NPCs und
  Stationen), A7 (Rollen und Makeovers), NPCs/Händler/Tutorial, Audio, Balance, Ebenen 4–10, Sponsoren/Interviews,
  README/CREDITS/CurseForge-Text. Stand-Liste: `docs/PLAN.md` im Mod-Repo.
- Kosten bisher (Agenten-Tokens): Buch-Auswertung 6,2 Mio., Runde 1 1,2 Mio., Runde 2 1,6 Mio.
