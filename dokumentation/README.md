# Dokumentation: Dreamcraft 26.3, Quest Icons, Beach Craft, Tamagotchi und Challenge Craft

Stand: 4. November 2026. Diese Dokumentation fasst das ganze Projekt der letzten Tage zusammen: was gebaut,
entschieden und veröffentlicht wurde, wo jedes Projekt steht und was du noch testen oder entscheiden musst.
Die langen Listen (Mods, Quests, Blöcke, Loot-Kisten) sind mit kleinen Skripten direkt aus den Quelldateien erzeugt,
damit sie exakt stimmen. Wo sich etwas nicht prüfen ließ, steht „unklar“.

## Inhalt

| Datei | Thema |
| --- | --- |
| [01_dreamcraft.md](01_dreamcraft.md) | Das Modpack: Port von 1.20.1 V4, **alle 250 Mods nach Kategorie**, entfernte Mods, Menü, Configs, Server-Pack, Versionen mit Datei-IDs, Produktiv-Test, **alle 328 Quests** Kapitel für Kapitel, Loot-Kisten, Dream Star |
| [02_quest_icons.md](02_quest_icons.md) | Quest Icons: Buch, Karten und Formen, alle Aufgaben- und Belohnungs-Typen, Loot Crates, Mystery Reward, Teams, Befehle, Editor, SNBT-Dateien, die 32 Icons, Dream Star mit beiden Rezepten, Versionen und der Klick-Hotfix |
| [03_beach_craft.md](03_beach_craft.md) | Beach Craft 2.0 und 3.0 „Tides of the Deep“: Welt, 12 Biome, Story (mit Spoiler-Warnung), 19 Strukturen, Kreaturen, Boss, Expedition Raft, Tauchen, **alle 343 Blöcke und Items**, Almanac, Advancements, Architektur, Tests, bekannte Probleme |
| [04_tamagotchi.md](04_tamagotchi.md) | Tamagotchi im Pack, der Bug-Check für 1.2.0 und der Release-Stand |
| [05_challenge_craft.md](05_challenge_craft.md) | Bug-Check von Challenge Craft: was behoben, was offen ist, und die Crafter-Entscheidung |
| [06_videos_und_beschreibungen.md](06_videos_und_beschreibungen.md) | TikTok v1/v2, Beach-Craft-Review mit Prüfbericht, Footage, alle CurseForge-Beschreibungen und wie man sie einfügt |
| [07_entscheidungen_und_lehren.md](07_entscheidungen_und_lehren.md) | Wichtige Entscheidungen mit Begründung und technische Lehren (26.3/SDL, Strukturen, Licht, Tests) |
| [08_offen_und_zu_testen.md](08_offen_und_zu_testen.md) | Checkliste: deine Entscheidungen, Risiken, was zu testen ist |

---

## Wo wir stehen (Kurzfassung)

### Veröffentlicht auf CurseForge
| Projekt | Versionen (Datei-ID) |
| --- | --- |
| **Dreamcraft** (Modpack 545167) | V1 9403038 (Server 9403042) · V1.1 9408516 (Server 9408519) · V1.2 9409459 (Server 9409463) · V1.2.1 9415062 (Server 9415063) · **V1.3 9431378 (Server 9431379)** |
| **Quest Icons** (690531) | 1.0.0 9402494 · 1.0.1 9409345 · 1.0.2 9415031 · **1.1.0 9429010** |
| **Beach Craft** (1010922) | 2.0.0 9402661 · 2.0.1 9408472 · **3.0.0 9431301** |
| **Tamagotchi** (1758309) | 1.0.0 9281396 · 1.1.0 9399713 · **1.2.0 9431312** |

### Fertig, aber noch nicht veröffentlicht
| Was | Wo | Warum noch nicht |
| --- | --- | --- |
| **Challenge Craft 1.1.4** (Bug-Check-Fixes) | Branch `bugcheck-2026-11` (`1474c3d`), Changelog-Entwurf | wartet auf deine Entscheidung zum Crafter und dein Go |

### Was du als Nächstes tun musst
Am 4.11.2026 hochgeladen (mit deiner Freigabe): Beach Craft 3.0.0 (9431301), Tamagotchi 1.2.0 (9431312, direkt auf
CurseForge – ein GitHub-Release mit Tag `v1.2.0` fehlt noch) und Dreamcraft V1.3 (9431378, Server-Pack 9431379).
1. Beschreibungen einfügen: Quest Icons, Beach Craft (3.0), Dreamcraft (V1.3); Tamagotchi optional um 1.2.0 ergänzen.
2. Prüfen, ob das V1.3-Server-Pack auf CurseForge als Server Pack markiert ist (geht nur von Hand).
3. Entscheiden: Crafter in Challenge Craft – und ob 1.1.4 kommt.

### Das Wichtigste in Sätzen
- **Dreamcraft** läuft auf Minecraft 26.3 (Fabric 0.20.1, Java 25) mit 250 CurseForge-Mods, eigenem Menü, Server-Pack
  und einer Quest-Story, die jede Mod erklärt. V1.2 kam nach einem echten Installationstest, V1.2.1 war der Hotfix für
  das Quest-Buch, das auf 26.3 keine Linksklicks erkannte.
- **Quest Icons** ist jetzt ein vollständiges Quest-System im FTB-Quests-Stil (FTB Quests gibt es für 26.3 Fabric
  nicht) und bringt mit 1.1.0 den **Dream Star**, die End-Trophäe von Dreamcraft.
- **Beach Craft 3.0** macht aus dem leeren Raft-Ozean eine Inselwelt mit 12 Biomen, einer Story über acht Kapitel bis
  zum Boss Leviathan, 19 Strukturen, 12 neuen Kreaturen, einem segelbaren Expedition Raft, Tauchausrüstung, 84 Bau- und 59
  Deko-Blöcken und einem Handbuch im Spiel.
- **Tamagotchi 1.2.0** macht die Pets modpack-tauglich (Mod-Essen, Mod-Erze, Look-alike-Strukturen) und behebt viele
  kleine Fehler.
- **Challenge Craft** bekam einen Bug-Check mit 10 Fixes (u. a. ein Dupe der Infinite Chest), ohne neue Version.
- **Videos:** Dreamcraft-TikTok (v2 mit Shadern) und ein 5-Minuten-Review von Beach Craft 2.0.1 mit echten
  Spielgeräuschen liegen im Archiv, samt Footage.

### Wichtiger Hinweis zur Arbeitsumgebung
Viele Werkzeuge (Pack-Build, Testclient, Release-Jars) liegen im **flüchtigen Scratchpad** dieser Sitzung (`$SP` =
`/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad`). Der Quellcode ist in Git sicher, aber
`mkpack.py` braucht Dateien aus dem Scratchpad. Details: [08_offen_und_zu_testen.md](08_offen_und_zu_testen.md).
