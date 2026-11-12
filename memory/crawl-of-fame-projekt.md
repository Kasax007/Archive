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

## Stand

- 12.11. abends: Phase 0 fertig (Gerüst, Layout-Generator, Design, Schnittstellen). Runde 1 läuft als zwei
  Workflows: Spur A (Welt, dann Lauf-Logik), Spur B (Asset-Werkzeuge und Test-Harness, dann Werte, HUD,
  Charakter-Fenster). Danach laut `docs/PLAN.md`: Monster, Items und Crates, Show-Ebene, Magie und Rollen, NPCs,
  Audio, Ebenen 4–10, Release-Prüfung.
