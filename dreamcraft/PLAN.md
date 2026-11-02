# Dreamcraft 26.3 – Plan und Stand

Auftrag (2.11.2026): Dreamcraft [FABRIC] (CurseForge 545167, Slug `dreamcraft-new`) und den Server-Pack auf
Minecraft 26.3 bringen. Basis ist die neueste Version **Dreamcraft 1.20.1 V4** (Datei 5042444, 262 Mods).
Ohne Rückfragen arbeiten, höchstens 1 Sonnet-Subagent. Den CurseForge-Token nur als Datei außerhalb der Repos
ablegen (`$SP/.cf_token`), nie committen.

## Bausteine

1. **Modliste:** alle 262 Mods per cfwidget auf 26.3/Fabric prüfen, Ersatz für fehlende Kategorien suchen
   (Bauen, Abenteuer, Magie, Technik, Lager, Essen). Ergebnis: `dreamcraft/modlist-26.3.md`.
2. **Quests:** FTB Quests gibt es für Fabric nur bis 26.1.2 → eigenes Quest-System nach FTB-Quests-Vorbild.
   Es kommt in den Mod **Quest Icons** (Branch `26.3`), weil der Mod schon ein CurseForge-Projekt hat und sich
   per API hochladen lässt.
3. **Quest Icons:** Port 1.21.1 (yarn) → 26.3 (Mojang-Namen, Java 25) plus das Quest-System.
4. **Raft:** Port Branch `1.21.1` → neuer Branch `26.3`. Custom Portal API gibt es für 26.3 nicht → eigenes
   Portal. Neuer Content (Deko und Funktion, Raft-Spiel als Vorbild). Beschreibung im Stil der Tamagotchi-Seite.
5. **Menü:** FancyMenu (v3-Format, siehe Challenge-Craft-Pack) plus Drippy Loading Screen mit den Dreamcraft-
   Bildern (8 Hintergründe, Schriftzug-Buttons, Seitenleiste mit Logo, lila Ladebalken #7e0cc9).
6. **Storyline:** Kapitel mit Erklärungen, wie die Mods funktionieren, und fairen Rewards.
7. **Tests:** Dedicated Server (Welt, Chunk-Generierung), Client (Menü, Ladebildschirm, Welt erstellen,
   Quest-Buch) per Client-Gametest mit Screenshots.
8. **Veröffentlichen:** Quest Icons, Raft, dann Modpack und Server-Pack; Beschreibungen; Archiv; Memory.
9. **TikTok:** schneller Short wie bei Challenge Craft.

## Stand (2.11.2026, fertig)

- [x] 1 **Modliste:** 250 CurseForge-Mods auf 26.3. Liste mit Datei-IDs: `modlist-26.3.md` im Modpack-Repo
  (Branch `26.3`). Entfernte Mods mit Grund: `pack/removed.md`.
- [x] 2/3 **Quest Icons 1.0.0+26.3:** Quest-System im FTB-Quests-Stil. CurseForge 690531, Datei 9402494, freigegeben.
- [x] 4 **Raft → „Beach Craft“ 2.0.0+26.3:** neue Deko und Funktionen, Portal, Hai. Beschreibung und Bilder in
  `docs/curseforge`. CurseForge 1010922, Datei 9402661, freigegeben.
- [x] 5 **Menü:** FancyMenu (8 Hintergründe) und Drippy-Ladebildschirm, im Client getestet.
- [x] 6 **Storyline:** 13 Kapitel, 164 Quests (44 optional), Loot-Kisten in vier Stufen.
- [x] 7 **Tests:**
  - Client: Boot, Menü, Weltgenerierung, Quest-Buch, Filmen in allen Dimensionen.
  - Server-Pack aus dem Zip: Start in 32 s, Quest-Buch geladen.
  - Chunky: Overworld 1521 Chunks in 1:43, Raft-Dimension 729 Chunks; früher auch Nether und End.
- [x] 8 **Veröffentlicht:**
  - Modpack „Dreamcraft 26.3 V1“: CurseForge 545167, Datei 9403038.
  - Server-Pack: Datei 9403042, als Unterdatei.
  - Beschreibungen: `docs/curseforge/description.md` in Modpack-Development und in Kasax_Raft_Mod, jeweils
    Branch `26.3`.
- [x] 9 **TikTok:** `dreamcraft/tiktok/` (44 s, Hook mit Burg-Luftaufnahme).

## Nachtrag (2.11.2026, zweiter Auftrag)

- [x] **TikTok v2:** Shader (Complementary Reimagined), Sichtweite 12. Jeder Shot wartet, bis alle Chunks gezeichnet
  sind. Das Rohmaterial liegt in `footage/dc`.
- [x] **Beach-Craft-Review:** `beachcraft/review/` (5:07). Jedes Feature ist gefilmt und erklärt, Prüfbericht in
  `REPORT.md`, Rohmaterial in `footage/bc`.
- [x] **Beach Craft 2.0.1:** über 20 Fehler behoben, darunter das Paddel, das erst beim Filmen auffiel.
  CurseForge-Datei 9408472.
- [x] **Dreamcraft V1.1:** Beach Craft 2.0.1 und korrigierte Raft-Quests („Driftwood Ahoy!“).
  - Client: Datei 9408516.
  - Server-Pack: Datei 9408519.

- [x] **Dreamcraft V1.2:**
  - Nach einem Test der echten CurseForge-Installation: Menü-Fixes, Ego-Perspektive, JER entfernt, Quest Icons 1.0.1.
  - Client: Datei 9409459, Server-Pack: Datei 9409463.
- [x] **Beschreibungen** im Stil des Nutzers mit Bisect-Bannern und Spoilern, je in `docs/curseforge/description.html`.

Von Hand zu erledigen:
- Beschreibungen auf CurseForge einfügen:
  - Im Editor auf die Quellcode-Ansicht umschalten, den Inhalt der jeweiligen `description.html` einfügen.
  - Die Dateien liegen in Modpack-Development, Kasax_Quests_Items_Mod-1.19.2 und Kasax_Raft_Mod, jeweils `docs/curseforge`.
- Den Server-Pack auf der CurseForge-Seite als Server-Pack markieren; das geht nicht per API.
