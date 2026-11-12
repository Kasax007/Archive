# Crawl of Fame – Ablage

Material zum Mod „Crawl of Fame“ (Repo `Kasax007/dungeon-crawler-steve`), das nicht in den Mod-Code gehört.
Projektwissen: `memory/crawl-of-fame-projekt.md`.

| Ordner | Inhalt |
| --- | --- |
| `briefs/` | Aufträge an die Agenten: `common.txt` (gemeinsame Regeln, Platzhalter `__WT__`, `__BRANCH__`, `__ID__`), `review.txt` (Prüf-Auftrag, Platzhalter für Module), Aufgaben `A7` (Rollen/Makeovers), `A8` (NPCs, Tutorial, Händler, Quests), `B7` (zweiter Grafik-Durchgang Ebenen 1–3), `B8` (Stage Door, Casting Call, Advancements, benannte Plätze); `crawl-round4-lane-*.js` = fertige Workflow-Skripte der Runde 4 |

Ein Workflow-Skript entsteht aus `common.txt` + Aufgabentext: eine Kette von Aufgaben pro Spur (Spur A in
`/home/user/wt/a`, Spur B in `/home/user/wt/b`), jede mit `model: 'opus'`, `effort: 'high'` und einem strukturierten
Bericht (done, summary, commits, tests, open_points, shared_changes).
