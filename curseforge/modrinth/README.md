# Modrinth (seit 8.11.2026)

Alle sechs Projekte des Nutzers (Account Kasax007, id pZ38RE5U) sind auf Modrinth eingerichtet:

| Projekt | Modrinth-Id / Slug | Stand 8.11. | Lizenz |
| --- | --- | --- | --- |
| Beach Craft | 3PmzwJU0 / beach-craft | in Prüfung, 3.3.0 für 26.3 und 1.21.1 | MIT |
| Quest Icons | ohf5LwXu / quest-icons | in Prüfung, 1.3.0 für 8 Versionen/Loader | MIT |
| Tamacraft | lyuVXQEh / tamacraft | in Prüfung, 1.3.0 für 26.3 und 1.21.1 | MIT |
| Challenge Craft (Mod) | 3qs3GQyx / challenge_craft | freigegeben, neu 1.1.3/1.1.2 (26.3), 1.0.1 (1.21.5) | CC-BY-4.0 |
| Challenge Craft Modpack | XVYCqsNs / challenge-craft-modpack | in Prüfung, 26.3-v4.2 (.mrpack) | CC-BY-4.0 |
| Dreamcraft | jRXfjUwW / dreamcraft | erneut in Prüfung, 26.3-V1.5.1 (.mrpack, 244 von 251 Mods) | MIT |

- **Token:** nur in `$SP/.mr_token` der Sitzung, nie in Dateien oder Commits. `tools/mr_api.py` liest ihn zur Laufzeit.
- **Beschreibungen:** `make_modrinth.py descriptions urlmap.json` macht aus den CurseForge-HTMLs Modrinth-Fassungen.
  Modrinth prüft auf dem Server (labrinth `validate/project`): Überschrift höchstens 80 Zeichen (auch HTML-`<h1-6>`),
  keine zwei gleichrangigen Überschriften direkt hintereinander, nicht mit einer Überschrift enden, Alt-Text an jedem
  Bild, kein „Spam“ (z. B. dieselbe Musik-Credit-Zeile pro Titel). `tools/mr_check.py` bildet das lokal nach;
  `GET /v3/project/<id>/validate` liefert die echte Liste. Lizenz, Version und Umgebung (pro Version) sind Pflicht.
- **Versionen:** byte-gleich mit CurseForge hochgeladen (`versions.json`: Modrinth-Version, Datei, sha1/sha512).
  Umgebung `client_and_server`, Abhängigkeit Fabric API (P7dR8mSH) bei Fabric-Versionen.
- **Modpacks:** `.mrpack` aus den CurseForge-Packs (`mrpack/`): jede Datei per Hash auf Modrinth gesucht, Downloads
  nur von cdn.modrinth.com. Server-Umgebung wie im getesteten Server-Pack. Challenge Craft: alle 30 Dateien gefunden;
  `menu_art_source/`, FancyMenu-Buddy-Spielstände und `last_world.fmdata` (privater Server) bleiben draußen.
  Dreamcraft: 7 Mods fehlen (siehe `AUTOREN-ANFRAGE.md`), Quarry Reborn liegt unter CC0 in `overrides/mods`.
  Test 8.11.: Server startet („Done“ nach 21 s, 357 Mods mit Bibliotheken), Client bis ins Dreamcraft-Hauptmenü.
- **Offenlegungen:** KI-Hilfe (Code, Grafiken, Texte) bei allen Projekten; Werbung (Bisect-Knopf) bei den Packs.
