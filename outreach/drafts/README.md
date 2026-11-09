# Entwürfe

Eine Datei pro Ziel. Der Dateiname beginnt mit der ID aus `targets.csv` (`cf:677008` wird `cf-677008-…`,
`yt:@emaiye` wird `yt-emaiye-…`). Sobald eine Datei da ist, setzt `score.py` den Status `new` auf `draft`.

Jede Datei enthält:

1. **Ziel:** Name, Link, Score, was passt (QI = Quest Icons, BC = Beach Craft, TG = Tamagotchi, DC = Dreamcraft).
2. **Kontaktweg:** der empfohlene Kanal und warum er ein eingeladener Weg ist, dazu was der Nutzer vorher prüfen muss.
3. **Belege:** die konkreten, wahren Beobachtungen aus der Projektseite oder Mod-Liste (mit Quelle und Datum),
   auf die sich der Text stützt.
4. **Text:** Englisch, aus den Vorlagen unten. Platzhalter in `{geschweiften Klammern}` füllt der Nutzer.
5. **Nachfrage (D):** nur einmal, frühestens 7 Tage nach dem Senden.

Vor dem Senden prüft der Nutzer: Kontaktweg noch da, Server-Regeln erlauben Vorschläge, Beobachtung noch wahr
(Packs ändern ihre Mod-Liste), Fußzeile vollständig (`{postal_address}`, `{privacy_link}`) bei E-Mails.

**Stand 7.11.2026 abends:** Alle 25 Texte wurden in der Datenbank der Seite im herzlichen Ton neu geschrieben
(`$SP/outreachpage/warm/texts.py`, Kopie in `page/warm_texts.py`). Die `.md`-Dateien hier zeigen noch die erste
Fassung; maßgeblich ist die Datenbank.

## Ton (Wunsch des Nutzers, 7.11.2026, gilt für jeden Entwurf)

- **Herzlich, freundlich, motivierend.** Wie ein Creator, der sich ehrlich über das Pack oder den Kanal freut und sich
  freuen würde, eine Antwort zu bekommen oder seinen Mod im Pack/Video zu sehen. Konkretes Lob mit echtem Bezug
  (Video, Mod-Liste, Idee des Packs) zuerst.
- **Immer Hilfe anbieten:** z. B. eine kostenlose Start-Questkette schreiben, Configs/Datapack/Tags einrichten, einen
  Server aufsetzen, eine eigene Challenge bauen, Early Access oder Footage schicken.
- **Verboten** (klingt nach KI oder Mailverteiler): „No pressure – I won't follow up more than once“, „One message only“,
  „This is a one-off message“, „Reply stop and you won't hear from me again“, „No payment involved, no obligations“,
  „Why you got this …“-Fußzeilen.
- **E-Mails:** Adresse immer direkt ins Feld `email` der Datenbank eintragen (nie in Dateien/Git). Gesucht wird in
  öffentlichen Angaben des Kanals: Kanalbeschreibung (YouTube-Seite `…/about` im Quelltext), Website, Linktree,
  Impressum. Steckt die Adresse nur hinter YouTubes „E-Mail-Adresse anzeigen“ (Captcha), Ziel auf `hold` mit Hinweis;
  lieber Creator mit öffentlicher Adresse wählen. Unterschrift: „Warm wishes, Kasax“, darunter nur die Zeile
  `{postal_address}, {privacy_link}` (Fußzeile; die Seite lässt einen leeren Datenschutz-Link weg).
- Englisch, kurz (80–160 Wörter), Links als eigene Zeilen, keine Markdown-Formatierung in E-Mails.

## Vorlagen (Stand 7.11.2026)

Fakten für alle Texte (Stand 9.11.2026): Quest Icons 1.3.0 für 26.3 und 26.2 Fabric mit Icon-Bibliothek, Ingame-Editor
und Import von FTB-Quests-Büchern, dazu Ports für Fabric 1.21.1, 1.21.11, 26.1.2 und 1.20.1, NeoForge 1.21.1 und Forge 1.20.1.
FTB Quests gibt es für 26.2/26.3 nicht (letzte Version 26.1.2). Beach Craft 3.4.0 für 26.3 und 1.21.1 Fabric. Tamacraft
(früher Tamagotchi) 1.3.0 für 26.3 und 1.21.1 Fabric. Dreamcraft V1.6: 251 Mods, 369 Quests in 16 Kapiteln, Server-Pack.
Alle Projekte auch auf Modrinth (seit 8.11., teils noch in Prüfung). Die Zahlen in den Vorlagen unten sind älter; neue
Entwürfe nehmen diese hier. Discord des Nutzers: Kasax Lounge, `discord.gg/zuZVtVvJaY`. Challenge Craft (Mod, seit 7.11. im Outreach für Creator):
1.1.3 für 26.3 Fabric, 51 Challenges, stapelbar mit Schwierigkeit, Daily Challenge (gleicher Seed für alle),
Challenge-Codes zum Teilen, Lifetime XP mit Level 1–20, alles koop-fähig, Lockout gegen den KI-Gegner Bob (immer
„early stage of development“ nennen). Challenge-Craft-Modpack: der Mod plus Shader, Proximity-Voice-Chat und
fertiges Menü. Dreamcraft-Short:
`https://www.youtube.com/watch?v=G-whF3xKTQ4`.

**A: Pack-Autor, Quest Icons** (Kommentar, Vorschlagskanal, Issue)

> Hi {name}! {konkretes Lob zum Pack}. {Beobachtung: was ein Questbuch hier leisten könnte}. I make Quest Icons, an
> FTB-Quests-style quest book for 26.2/26.3 Fabric (chapters, rewards, loot crates, teams, in-game editor, and it can
> import FTB Quests books). If you'd like to give it a try, I'm happy to help: I'd love to write you a free starter
> chapter ({idee}) – just tell me what you need. It would honestly make my day to see it in {pack}!
>
> Thanks for building {pack} – have a great day! Kasax (Discord: discord.gg/zuZVtVvJaY)

**B: Pack-Autor, Beach Craft oder Tamagotchi** – wie A, mit konkretem Bezug (Ozean-/Pet-Mods im Pack) und
Hilfsangebot (Configs, Datapack für Diäten/Tags, Strukturen wählen).

**C: Creator, Dreamcraft-Serie** (E-Mail an die öffentliche Geschäftsadresse)

> Subject: {freundlicher, konkreter Betreff}
>
> Hi {name}, I just watched {video} and {was gefallen hat} – {warum es passt}! I make Dreamcraft, a free 26.3 Fabric
> modpack with 251 mods and a quest story in 15 chapters (348 quests), a raft ocean with a boss and ten rare pets to
> tame. It would honestly make my day to see you play it. If you'd like to give it a try, I'm happy to help with
> anything – a server setup, early access to the next update, or footage from our trailer and documentary.
> {Links}. Thank you for your videos – I'd love to hear what you think! Warm wishes, Kasax

**D: Nachfrage (frühestens nach 7 Tagen, einmal)**

> Hi {name}! I hope you're doing well. I just wanted to make sure my message about {X} didn't get lost – I'd really
> love to hear what you think, and I'm happy to help with anything if you want to try it. Warm wishes, Kasax

**E: Creator, Challenge Craft** (Challenge-, Lockout-/Bingo-, „Minecraft but…“- oder Koop-Kanäle; das Casino nicht
als Aufhänger, junge Zuschauer; Bob immer „early stage of development“)

> Subject: 51 stackable challenges for your next challenge video
>
> Hi {name}, I loved {video} – {konkreter Moment}! I make Challenge Craft, a free 26.3 Fabric mod that turns any world
> into a challenge run: 51 challenges you can stack (Lockout Bingo, Force Item Battle, All Biomes, Chunk Hunt …), a
> Daily Challenge with the same seed for everyone, and short codes to share an exact setup with your viewers.
> Everything works in co-op, and there's an early-stage AI rival, Bob, to play Lockout against. The Challenge Craft
> modpack adds shaders and proximity voice chat, ready to stream. I'd love to build a custom challenge for your format
> or set up a code for your community – just tell me! Mod: https://www.curseforge.com/minecraft/mc-mods/challenge ·
> Modpack: https://www.curseforge.com/minecraft/modpacks/challenge-craft. I'd be so happy to hear what you think!
> Warm wishes, Kasax
