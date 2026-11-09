# Outreach: Packs und Creator finden, bewerten, anschreiben

Halbautomatische Pipeline nach `research/curseforge-wachstum-2026-11.md`, Teil 3. Die Skripte **finden, bewerten
und entwerfen nur**. Sie senden, posten, kommentieren und schreiben niemandem, auch keine DMs. Jede Nachricht
liest, ändert und verschickt der Nutzer selbst.

Beworben werden Quest Icons (690531), Beach Craft (1010922), Tamagotchi (1758309) bei Pack-Autoren, Dreamcraft
(545167) bei Creatorn und seit 7.11.2026 Challenge Craft (Mod 1508454, Modpack 1653698) bei Creatorn mit
Challenge-, Lockout-/Bingo- oder Koop-Videos (Vorlage E, Suchbegriffe `challenge_creator_terms` in `config.json`).
Gesendet wird auf der Seite selbst: E-Mails mit einem Klick über den Gmail-Connector des Nutzers, Kommentare und
Discord mit „Kopieren & öffnen“. E-Mail-Adressen stehen nur in der privaten Datenbank der Seite, nie in Dateien.

**Erste Runde (7.11.2026):** 1.821 Fabric-Packs für 26.2/26.3 auf Modrinth und 502 CurseForge-Slugs durchsucht, 917 Packs näher angesehen. 15 Pack-Entwürfe (9 jetzt möglich, davon 3 nur über einen Discord-Vorschlagskanal; 6 auf `hold`) und 10 Creator-Entwürfe in `drafts/`. Von Hand verworfene Ziele stehen mit Grund in `targets.csv` (`skip`, Spalte `notes`). Wichtigster Engpass: Unsere Mods fehlen auf Modrinth, deshalb sind fast alle Modrinth-Packs auf `hold`.

**Lauf 9.11.2026:** 1.834 Modrinth-Packs und 502 CurseForge-Slugs durchsucht, 916 Packs bewertet. Zwei Regeln korrigiert: Quest Icons gibt es seit 7.11. auch für 26.2 (dadurch wurden 12 CurseForge-Packs frei; alle von Hand geprüft und mit Grund auf `skip`: keine Links, keine Einladung oder schon ein Quest-System), und Modrinth-Packs bleiben auf `hold`, bis Beach Craft, Quest Icons oder Tamacraft dort freigegeben sind (in Prüfung seit 8.11.; dann `modrinth_id` in `config.json` eintragen). Neue Entwürfe: zwei Creator für Challenge Craft (eldor, KIAN).

**Große Runde 9.11.2026** (Nutzer: „2 reicht nicht“): drei Recherche-Agenten, 49 neue Entwürfe auf der Seite – 20 Creator für Challenge Craft und Dreamcraft (YouTube, davon 4 deutsch), 20 Mod-Showcase-Creator (14 YouTube, 6 TikTok), 9 Pack-Autoren mit geschätzt 750 bis 40.000 Downloads im Monat (auch 1.21.1 und 1.20.1, Forge/NeoForge für Quest Icons). 30 Creator-Adressen stehen in der Datenbank, 10 Creator auf `hold` (Adresse nur hinter dem Captcha), 3 Modrinth-Packs auf `hold` (unsere Mods noch in Prüfung). Instagram war aus dem Container nicht lesbar. Neu: `discover_wide.py` (größere Packs auf allen Versionen unserer Mods, Seeds in `data/wide_cf_seeds.csv`, Ausgabe `data/wide_candidates.json`). Die Routine liefert seitdem 10–20 Entwürfe pro Werktag.

## Wochenablauf

| Schritt | Wer | Wie |
| --- | --- | --- |
| 1. Finden | Skript | `python3 discover.py`: Modrinth, CurseForge, `creators.csv` |
| 2. Bewerten | Skript | `python3 score.py --top 25` schreibt `targets.csv` |
| 3. Entwerfen | Sitzung | Für die besten 5–10 neuen Ziele je eine Datei in `drafts/` (Vorlagen A–C, siehe `drafts/README.md`). Ohne echten Bezug oder echten Kontaktweg: Status `skip`, Grund in `notes` |
| 4. Freigeben | Nutzer | Entwurf lesen, Kontaktweg selbst prüfen, ändern, Status `approved` oder verwerfen |
| 5. Senden | Nutzer | Selbst, über den empfohlenen Kanal. Dann `status` = `sent` und `sent_on` = Datum |
| 6. Verfolgen | Skript | `score.py` setzt `follow_up_on` (+7 Tage) und `delete_after` (+6 Monate) |
| 7. Nachfragen | Nutzer | `python3 score.py --due` zeigt fällige Nachfragen. Text D genau einmal senden, Status `followed_up`. Danach nichts mehr |

Freitags zusätzlich `python3 score.py --kpi`. Senden werktags, am besten Dienstag bis Donnerstag, 10–15 Erstnachrichten
pro Woche.

## Befehle

```
cd outreach
python3 discover.py              # erster Lauf ca. 20-30 min (Pausen zwischen den Abrufen), danach Caches
python3 discover.py --skip-cf    # nur Modrinth und Creator
python3 discover.py --no-verify  # ohne Prüfung der Discord-Einladungen und GitHub-Vorlagen
python3 score.py --top 25        # Tabelle aktualisieren, beste offene Ziele zeigen
python3 score.py --due           # fällige Nachfragen
python3 score.py --kpi           # Wochenzahlen
```

Nur Python 3.10+ ohne Zusatzpakete. Netz: `api.modrinth.com`, `api.cfwidget.com`, `mediafilez.forgecdn.net`,
`discord.com` (nur die öffentliche Einladungs-Abfrage), `raw.githubusercontent.com`. Das Skript fragt höchstens
etwa drei Mal pro Sekunde bei Modrinth (Grenze 300 pro Minute) und deutlich seltener bei allen anderen.

## Dateien

| Datei | Inhalt |
| --- | --- |
| `config.json` | Unsere Projekte, Listen der Quest-, Ozean- und Pet-Mods, Punkteschema, Grenzen |
| `discover.py` | Sucht Fabric-Packs für 26.2/26.3. Modrinth: alle Packs per Suche, Details, Team, Links, Mod-Liste der neuesten Version. CurseForge: Slugs aus der Recherche-CSV und `data/cf_seeds.csv`, Details über cfwidget, Mod-Liste aus `manifest.json` und `modlist.html` der Pack-Datei (per Range-Abruf, meist unter 600 KB statt der ganzen Datei). Prüft Discord-Einladungen und GitHub-Vorlagen der aussichtsreichen Packs |
| `score.py` | Punkte, Status, Daten, Sperrliste, Löschfristen, Nachfragen, KPIs |
| `targets.csv` | Die Tabelle. Spalten: `id, type, name, platform, url, contact_route, score, status, first_seen, sent_on, follow_up_on, notes, delete_after, fit, why` |
| `suppression.csv` | Sperrliste (`key, added_on, reason`). Schlüssel: Ziel-ID, URL oder `author:<name>`. Beide Skripte beachten sie: Gesperrte Ziele werden weder abgefragt noch in die Tabelle geschrieben |
| `creators.csv` | Von Hand gepflegte Creator-Liste. Nur Kanalname, Plattform, URL, Sprache, ungefähre Reichweite, der vom Kanal selbst genannte Weg für Geschäftsanfragen (ohne Adresse) und das Video, das die Passung belegt |
| `data/cf_seeds.csv` | Zusätzliche CurseForge-Slugs von der Website (26.2-Liste, Seiten 1–4, Stand 7.11.); ergänzt die Recherche-CSV mit allen 26.3-Packs |
| `drafts/` | Ein Entwurf pro Ziel, Dateiname beginnt mit der ID (`cf-677008-…`, `yt-emaiye-…`, `tt-…`, `ig-…`) |
| `tools/` | Hilfen für die Creator-Suche von Hand (seit 9.11.2026): `yt_search.py` (YouTube-Suche, Videos des letzten Monats), `yt_channel.py` (Beschreibung und neueste Videos), `yt_about.py` (Abos und die Adressen, die der Kanal selbst in seine Beschreibung schreibt; maskiert, `--show` nur für die Konsole). Wenige Abrufe pro Lauf, nur öffentliche Seiten |
| `sync_page.py` | Holt Status, Sendedatum und Nachfrage-Datum von der Freigabeseite nach `targets.csv` (`python3 sync_page.py DB_DIR`) |
| `discover_wide.py`, `data/wide_cf_seeds.csv` | Breite Pack-Suche (seit 9.11.2026): größere Packs auf allen Versionen, auf denen unsere Mods laufen, mit geschätzten Monats-Downloads; schreibt `data/wide_candidates.json` (nicht im Repo). Montags und donnerstags nach `discover.py` |
| `cache/`, `data/candidates.json` | Werden bei jedem Lauf neu erzeugt, nicht ins Repo (`.gitignore`) |

**CurseForge-Seeds nachtragen:** Die Such-API der Website antwortet Skripten mit 403. Neue Packs deshalb einmal pro
Woche von Hand (oder mit einem Abruf-Werkzeug) aus der Website-Liste übernehmen:
`https://www.curseforge.com/minecraft/search?page=1&pageSize=50&sortBy=popularity&class=modpacks&version=26.3&gameVersionTypeId=4`
(und `version=26.2`), neue Slugs in `data/cf_seeds.csv` eintragen.

## Status in `targets.csv`

| Status | Bedeutung | Wer setzt ihn |
| --- | --- | --- |
| `new` | Bewertet, noch kein Entwurf | Skript |
| `hold` | Passt, aber noch nicht möglich: Modrinth-Pack (unsere Mods sind nicht auf Modrinth) oder nur 26.2 (Quest Icons 26.2 fehlt noch); Creator, deren Adresse nur hinter YouTubes Knopf „View email address“ (Captcha) steht (seit 9.11.2026) | Skript |
| `draft` | Entwurf liegt in `drafts/` | Skript |
| `approved` | Vom Nutzer freigegeben | Nutzer |
| `sent` | Gesendet, `sent_on` eintragen | Nutzer |
| `followed_up` | Die eine Nachfrage ist raus, danach Schluss | Nutzer |
| `replied`, `yes`, `no` | Antwort, Zusage, Absage | Nutzer |
| `stop` | Widerspruch: `score.py` trägt ID, URL und Autoren in `suppression.csv` ein, löscht die Zeile (auch bei `no`) und nennt Entwürfe, die zu löschen sind | Nutzer |
| `skip` | Kein Kontaktweg, kein echter Bezug oder keine Lücke; Grund in `notes` | beide |

## Punkteschema (0–100, qualifiziert ab 60)

Pflicht: 26.2 oder 26.3, Fabric. Teilpunkte dort, wo der Beleg nur teilweise da ist. Der Score sortiert nur vor: Ob ein Pack wirklich passt und ob der Kontaktweg echt ist, prüft die Sitzung beim Entwerfen auf der Projektseite (bei CurseForge stehen Discord und Issues oft nur in der Seitenleiste, die das Skript nicht sieht).

| Kriterium | Punkte |
| --- | --- |
| Inhalts-Pack (Kategorie Adventure, Quests, Tech, Magic, Exploration …) | 25 bei mindestens 8 Inhalts-Mods (Strukturen, Welt, Mobs, Magie, Technik, RPG, Farm, Dimensionen; nach Mod-Namen); 10 bei leichtem Inhalt; 0 bei Performance-, Shader-, PvP-, QoL- oder Optik-Packs |
| Letztes Update ≤ 30 Tage | 20 |
| Downloads 500–100.000 | 15 |
| Lücke für unsere Mods | 20 kein Quest-Buch (Quest Icons), 15 bei unklarer Quest-Mod; 15 Ozean- oder Pet-Lücke mit passendem Thema (Beach Craft, Tamagotchi); bei leichten Packs 10; Mod-Liste nicht gelesen 5; kein Inhalts-Pack 0 |
| Eingeladener Kontaktweg | 15 Mod-Vorschlags-Vorlage oder Seite lädt zu Vorschlägen ein; 12 Feedback-Aufruf oder Feature-Vorlage; 8 Issue-Tracker; 5 gültige Discord-Einladung; 0 keiner |
| Englisch oder Deutsch | 5 |

Creator: Modded-Inhalt 25, passendes Video in den letzten 2 Monaten 20 (6 Monate: 10), 1.000–100.000 Abos 15,
26.x-, Floß-, Quest-, Cozy- oder Challenge-Inhalt (Lockout, Bingo, „Minecraft, but…“, Force Item, Manhunt) 20 (sonst 10),
selbst genannter Weg für Geschäftsanfragen 15, Englisch oder Deutsch 5. Steht die Adresse nur hinter YouTubes Knopf
„View email address“ (Captcha), kommt der Creator auf `hold` (seit 9.11.2026).

## Rechtliche Regeln in Kürze (allgemeine Information, keine Rechtsberatung)

- **§ 7 Abs. 2 Nr. 2 UWG:** Werbung per E-Mail ohne vorherige ausdrückliche Einwilligung ist eine unzumutbare
  Belästigung, auch zwischen Unternehmen. Eine öffentlich angegebene Geschäftsadresse ist keine Einwilligung.
  Deshalb zuerst eingeladene Wege: Vorschlagskanal, Issue-Vorlage, Formular, öffentlicher Aufruf. E-Mail nur an
  Adressen, die ausdrücklich für Geschäftsanfragen genannt sind, einzeln und persönlich. Ein Restrisiko bleibt.
- **§ 7 Abs. 2 Nr. 3 UWG, § 6 DDG:** Absender nie verschleiern, Werbung erkennbar machen, eine gültige Adresse zum
  Abbestellen nennen.
- **DSGVO Art. 14:** spätestens in der ersten Nachricht sagen, wer schreibt, wozu, woher die Daten stammen und welche
  Rechte bestehen (Fußzeile in `drafts/README.md`). **Art. 21:** auf das Widerspruchsrecht ausdrücklich hinweisen.
  Nach „stop“ sofort Status `stop`; `score.py` sperrt und löscht. Nur Name, Kanal, Kontaktweg, Projekt und Status
  speichern. Ohne Antwort nach 6 Monaten löschen (`delete_after`).
- **CAN-SPAM (Empfänger in den USA):** richtige Absenderdaten, keine irreführende Betreffzeile, Postanschrift
  (Postfach genügt), Abmeldungen binnen 10 Werktagen umsetzen.
- **Discord:** keine DMs, keine Massen- oder Bot-Nachrichten. Nur Vorschlagskanäle, und nur, wenn die Server-Regeln
  Mod-Vorschläge dort erlauben.
- **YouTube:** keine Werbe-Kommentare. Geschäfts-Mail nur von Hand über „View email address“ auf der About-Seite.
- **GitHub:** ein einzelnes Issue nur, wenn das Repo Vorschläge per Vorlage oder Discussions erbittet.
- **CurseForge-Kommentare:** nur, wenn die Projektseite ausdrücklich um Vorschläge in den Kommentaren bittet. Ein
  Kommentar, offen als Autor der Mod, keine Wiederholung außer der einen Nachfrage.
- **X, TikTok:** keine automatisierten Erwähnungen oder DMs; TikTok-Creator nur von Hand suchen.
- **Immer:** eine einzige Nachfrage nach 7 Tagen, dann Schluss. Kein Geld für die Aufnahme in ein Pack.

## Wöchentliche Kennzahlen

| Kennzahl | Ziel pro Woche | Quelle |
| --- | --- | --- |
| Neue qualifizierte Ziele (Score ≥ 60) | 15–30 | `score.py --kpi` |
| Gesendete Erstnachrichten | 10–15 | `score.py --kpi` |
| Antwortquote, rollierend 4 Wochen | Packs ≥ 15 %, Creator ≥ 3 % | `score.py --kpi` |
| Zusagen bzw. neue Dependents | ≥ 1 | `yes` in der Tabelle, CurseForge „Dependents“ von Hand |
| Creator-Videos oder Streams mit unseren Projekten | ≥ 1 pro Monat | von Hand |
| Eindeutige Downloads pro Projekt, Veränderung zur Vorwoche | steigend | Autoren-Dashboard |
| Popularity-Rang Dreamcraft in 26.3 Fabric und „Quests“ | steigend | CurseForge-Suche |
| Widersprüche, Beschwerden, gemeldete Nachrichten | 0, sonst sofort stoppen und Texte prüfen | `score.py --kpi` |
| Zeit für Outreach | ≤ 3 h | von Hand |
