# Pause vom 23.11.2026, 23:15 UTC (auf Wunsch des Nutzers)

Die Entwicklung von Crawl of Fame ruht, bis der Nutzer wieder „Go“ gibt. Die drei Spuren wurden mitten in ihrem
Schritt angehalten (alle drei hingen seit 21:00 in langen Prüfläufen). Hier liegt alles, was nur lokal im Container
war, damit auch ein zurückgesetzter Container nichts verliert.

## Stand der Spuren

| Spur | Aufgabe, Workflow-Lauf | Angehalten in | Lokal, nicht gepusht |
| --- | --- | --- | --- |
| A | ROOMS1, Prüfungen fertig, FIX-Schritt (`wf_1b322ad1-35a`, Skript `crawl-rooms1-a10.js`) | FIX: offene Punkte und eigene Funde L1/L2 abgearbeitet, verglich gerade den Arcade-Test „Kill Screen breaks the floor and takes coins“ auf `8245b2b` (Hilfs-Worktree `$SP/r1fix/main_wt`) | 8 Commits auf `lane-a` (`lane-a.commits.txt`), nicht auf den Branch umgesetzt; Worktree sauber |
| B | CREATURES1B (Understage), FIX-Schritt (`wf_3422d275-a33`, `crawl-creatures1b-b12.js`) | FIX: alle Funde behoben und gepusht (bis `db9f518`), wartete auf den dritten vollen Golden-Lauf | 1 Commit `f780ddd` (Walker: Schritt vor dem Vorhang), Bericht `docs/reports/CREATURES1B.md` geändert (`lane-b.uncommitted.diff`) |
| C | The Toy Chest (W4), BUILD-Schritt (`wf_c303beb1-2a0`, `crawl-toychest-c3.js`) | BUILD: Endkontrolle (volle Spieltests, Hörlauf), Bericht `docs/reports/W4.md` halb geschrieben | 13 Commits auf `lane-c`, Bericht geändert (`lane-c.uncommitted.diff`) |

`journals/` hält die Workflow-Journale (Ergebnisse der fertigen Schritte: Bau und Prüfungen von A und B).

## Fortsetzen nach dem Go

1. Container noch derselbe (Worktrees `/home/user/wt/a|b|c` mit diesen Commits vorhanden): je Spur das Skript
   ergänzen (im FIX- bzw. BUILD-Auftrag ein Satz: „Ein früherer Lauf dieses Schritts wurde am 23.11. 23:15 UTC für
   eine Pause angehalten; seine Commits liegen auf dem Branch der Spur, ungecommittete Änderungen im Worktree sind
   seine unfertige Arbeit: erst ansehen, Richtiges behalten, dann weiter mit dem, was fehlt“) und mit
   `Workflow({scriptPath, resumeFromRunId})` fortsetzen. Der unterbrochene Schritt läuft neu, alles davor kommt aus
   dem Cache.
2. Container zurückgesetzt: Worktree vom Branch `claude/determined-edison-xwiksi` anlegen, dann
   `git fetch <dieser Ordner>/lane-x.bundle lane-x:lane-x` und `git checkout lane-x` (die Bundles setzen nur Commits
   voraus, die auf dem Remote-Branch liegen), dann `git apply lane-x.uncommitted.diff`. Die Workflow-Caches sind dann
   weg: Spur A und B mit einem reinen FIX-Lauf fortsetzen (Funde stehen in `journals/`), Spur C den Bau mit diesen
   Commits als Ausgangspunkt beenden lassen.
3. Stimmen: Der Supervisor läuft, ist aber pausiert (`PAUSE` in `$SP/voice/work`, beim Go löschen). 16 Retakes sind
   veröffentlicht (`3f8a90f`), 31 noch markiert (der alte Take bleibt, bis ein besserer kommt). Sicherung der
   Sprecher-Referenzen und des Zustands: `../voice-pipeline/work-backup-2026-11-23/` (bei einem neuen Container
   nach `$SP/voice/work/` zurückkopieren, sonst entstehen neue Stimmen).
4. Check-in `trig_01YEwa3HuMn2UhjCf6N5bkJV` ist ausgeschaltet: mit neuem `run_once_at` und `enabled` wieder an.
5. Danach wie geplant: A → ORIGIN1 (`crawl-origin1-a11.js`), B → UI2A (`crawl-ui2a-b13.js`), C → nach dem Toy Chest
   Far Lantern erzeugen; Jar 11, sobald ROOMS1 fertig ist.
