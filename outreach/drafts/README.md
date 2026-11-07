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

## Vorlagen (Stand 7.11.2026)

Fakten für alle Texte: Quest Icons 1.1.0 für 26.3 Fabric, Build für 26.2 und ein Importer für FTB-Quests-Kapitel sind
in Arbeit (nur als „coming“ nennen). FTB Quests gibt es für 26.2/26.3 nicht (letzte Version 26.1.2). Beach Craft 3.1.0
für 26.3 Fabric. Tamagotchi 1.2.0 für 26.3 Fabric. Dreamcraft V1.4.1: 251 Mods, 348 Quests in 15 Kapiteln,
Server-Pack. Discord des Nutzers: Kasax Lounge, `discord.gg/zuZVtVvJaY`. Dreamcraft-Short:
`https://www.youtube.com/watch?v=G-whF3xKTQ4`.

**A: Pack-Autor, Quest Icons** (Vorschlagskanal, Issue-Vorlage oder eingeladene E-Mail)

> Subject: Quest book for {pack_name} on 26.3?
>
> Hi {name}, I'm Kasax, I make the Dreamcraft modpack and the Quest Icons mod. I noticed {pack_name} is on
> {mc_version} Fabric and {specific_observation}. FTB Quests stops at 26.1.2, so I built Quest Icons: an
> FTB-Quests-style quest book with chapters, rewards, loot crates, teams and an in-game editor (a 26.2 build and an
> importer for FTB Quests chapters are coming). If you like, I'll write a free starter chapter for {pack_name}
> ({idea}) so you can try it without work.
>
> https://www.curseforge.com/minecraft/mc-mods/quest-icons
> No reply needed if it's not for you, and I won't follow up more than once. – Kasax (Discord: discord.gg/zuZVtVvJaY)

**B: Pack-Autor, Beach Craft oder Tamagotchi**

> Subject: An ocean dimension for {pack_name}?
>
> Hi {name}, {pack_name} looks great, especially {specific_detail}. I make Beach Craft, a Raft-style ocean dimension
> for 26.3 Fabric: build your own raft, islands, 8 NPCs, diving and a boss, plus a ready quest chapter. It runs in my
> 251-mod pack Dreamcraft and on dedicated servers. If it fits your pack, I'm happy to help with configs or a quest
> chapter. {tamagotchi_line_optional}
>
> https://www.curseforge.com/minecraft/mc-mods/beach-craft · One message only, no follow-up spam. – Kasax

Tamagotchi-Zeile: „I also make Tamagotchi: ten rare tameable pets, built for modpacks since 1.2 with tags for
modded food and ores (https://www.curseforge.com/minecraft/mc-mods/tamagotchi).“

**C: Creator, Dreamcraft-Serie** (nur an die Geschäftsadresse des Kanals)

> Subject: Series idea for {channel_name}: 348-quest modpack on 26.3
>
> Hi {name}, I liked {specific_video} – {specific_detail}. I make Dreamcraft, a free 26.3 Fabric modpack with 251
> mods and a quest story in 15 chapters, a raft ocean with a boss, and ten rare pets to tame. That structure works well
> as an episode series. If you're interested, I can send early access to the next update, B-roll from our trailer and
> documentary, and help setting up a server. No payment involved, no obligations.
>
> Pack: https://www.curseforge.com/minecraft/modpacks/dreamcraft-new · Short: https://www.youtube.com/watch?v=G-whF3xKTQ4
> This is a one-off message. Reply "stop" and you won't hear from me again. Sender: Kasax, {postal_address}

**D: Eine einzige Nachfrage nach 7 Tagen**

> Hi {name}, quick follow-up on my note about {project} for {pack_or_channel}. If now isn't a good time, no worries –
> I won't write again. – Kasax

**Fußzeile für jede E-Mail** (DSGVO Art. 14 und 21, § 7 UWG, CAN-SPAM)

> Why you got this: I found {pack_or_channel} on {platform}, where you list this address for {purpose}. I only keep
> your name, this address and notes for this one request. Reply "stop" and I'll delete them and never write again.
> – Kasax, {postal_address}, {privacy_link}

In Discord-Vorschlagskanälen und GitHub-Issues keine Fußzeile, aber offen sagen, dass der Autor der Mod schreibt.
