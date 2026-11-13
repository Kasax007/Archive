# Warm rewrite of all outreach drafts (7.11.2026, wish of the user: friendly, motivating, always offer help,
# no "one message only" / "reply stop" lines). Used by apply.py.
DISCORD = "discord.gg/zuZVtVvJaY"
QI = "https://www.curseforge.com/minecraft/mc-mods/quest-icons"
BC = "https://www.curseforge.com/minecraft/mc-mods/beach-craft"
TG = "https://www.curseforge.com/minecraft/mc-mods/tamagotchi"
DC = "https://www.curseforge.com/minecraft/modpacks/dreamcraft-new"
SHORT = "https://www.youtube.com/watch?v=G-whF3xKTQ4"
SIGN = "Warm wishes,\nKasax"
FOOT = "{postal_address}, {privacy_link}"
NOMAIL = ("Keine öffentliche E-Mail: YouTube zeigt die Adresse nur über „E-Mail-Adresse anzeigen“ mit Captcha, "
          "das geht nicht automatisch. Der Text ist fertig; sobald eine Adresse bekannt ist, kann er raus.")

def pack_close(pack, offer):
    return (f"If you'd like to give it a try, I'm happy to help: {offer} – just tell me what you need. "
            f"It would honestly make my day to see it in {pack}!\n\n"
            f"Thanks for building {pack} – have a great day!\nKasax (Discord: {DISCORD})")

def pack_followup(name, mod, pack):
    return (f"Hi {name}! I just wanted to check whether my suggestion about {mod} reached you. I'd really love to hear "
            f"what you think – and my offer stands: I'm happy to help set it up for {pack}. Have a great day! – Kasax")

def creator_followup(name, what):
    return (f"Hi {name}! I hope you're doing well. I just wanted to make sure my message about {what} didn't get lost – "
            f"I'd really love to hear what you think, and I'm happy to help with anything if you want to try it.\n\n{SIGN}")

T = {}

# ------------------------------------------------------------------ creators (e-mail)
# The addresses are kept only in the page database (field `email`), never in this file.
T['yt-emaiye'] = dict(
  subject="A cozy pet mod for your forever world",
  message=f"""Hi emaiye,

I just watched the first episode of your cozy modded forever world and really enjoyed the slow, comfy pace – it's exactly the kind of world I love making things for!

I make Tamagotchi, a free mod for 26.3 Fabric: ten rare pets hide in structures around the world, and once you find one you can tame it and look after it – with toys, a treat dispenser, an incubator and even a little pet door. It's also part of Dreamcraft, my free modpack with 251 mods and a quest story in 15 chapters, where the pets get their own chapter.

I think it could fit beautifully into a relaxed series, and it would honestly make my day to see one of the pets in your world. If you'd like to try it, I'm happy to help with anything – setting up a server, answering questions, early access to the next update, or footage from our trailer.

Tamagotchi: {TG}
Dreamcraft: {DC}

Thank you for making such calm, lovely videos – I'd love to hear what you think!

{SIGN}""",
  followup=creator_followup('emaiye', 'Tamagotchi'), footer=FOOT)

T['yt-NoxusMods'] = dict(
  subject="Two small mods for a future \"Unknown Mods\" video",
  message=f"""Hi Noxus,

I really like your "15 UNKNOWN Minecraft Mods" videos – they're one of the few places where small mods get a real chance, and I've found some great ones through them myself.

I'd be thrilled if two of mine could make it into one someday, both free for 26.3 Fabric:
- Tamagotchi: ten rare pets hide in the world's structures. You tame them and look after them – with toys, an incubator and a running wheel that even gives off a redstone signal.
- Beach Craft: a Raft-style ocean dimension behind a driftwood portal. You build your own raft block by block, sail between islands, dive, and face the Leviathan.

Both run on servers and play together in my modpack Dreamcraft. If you'd like to try them, I'm happy to help with anything – a quick server setup, early access to the next update, or footage from our trailer and documentary.

Tamagotchi: {TG}
Beach Craft: {BC}

Thanks for all the work you put into showing new mods – I'd love to hear what you think!

{SIGN}""",
  followup=creator_followup('Noxus', 'Tamagotchi and Beach Craft'), footer=FOOT)

# ------------------------------------------------------------------ creators without a public address (hold)
T['yt-Fuzzycub_'] = dict(status='hold', status_note=NOMAIL,
  subject="A 15-chapter questing pack for a series?",
  message=f"""Hi Fuzzycub,

I saw that you started Reclamation as a series – I love watching questing packs unfold episode by episode, so that made me smile!

I make Dreamcraft, a free 26.3 Fabric modpack with 251 mods and a quest story in 15 chapters (348 quests): magic, tech, new biomes, a whole raft ocean with a boss, and ten rare pets to tame. The chapters map nicely onto episodes, and there's a server pack if you'd like to play it with friends.

It would mean a lot to me to see you play it. If you want to give it a go, I'm happy to help with anything – setting up a server, early access to the next update, or footage from our trailer and documentary.

Dreamcraft: {DC}
Trailer: {SHORT}

Thanks for your videos – I'd love to hear what you think!

{SIGN}""",
  followup=creator_followup('Fuzzycub', 'Dreamcraft'), footer=FOOT)

T['yt-MCG-Modding'] = dict(status='hold', status_note=NOMAIL,
  subject="Two new mods people might have missed",
  message=f"""Hi MCG Modding team,

I really like the idea behind your "20 AMAZING & New Minecraft Mods You Missed" video – giving new mods a stage is such a kind thing to do for small creators like me.

Here are two of mine, both free for 26.3 Fabric:
- Beach Craft: a Raft-style ocean dimension – build your own raft block by block, sail between islands, dive, meet 8 NPCs and face the Leviathan.
- Tamagotchi: ten rare pets hidden in structures that you tame and look after.

Both run on servers and play together in my modpack Dreamcraft (251 mods, 15 quest chapters), which could also work as a series.

It would be wonderful to see them in one of your videos. If you'd like to try them, I'm happy to help with anything – early access, a server setup, or footage from our trailer and documentary.

Beach Craft: {BC}
Tamagotchi: {TG}
Dreamcraft: {DC}

Thanks for supporting new mods – I'd love to hear what you think!

{SIGN}""",
  followup=creator_followup('MCG Modding team', 'Beach Craft and Tamagotchi'), footer=FOOT)

T['yt-YahiamiceLIVE'] = dict(status='hold', status_note=NOMAIL,
  subject="A whole ocean dimension for your raft runs",
  message=f"""Hi Yahiamice,

I watched "Can YOU beat MinecRAFT starting off a RAFT?" and had a big grin on my face – starting on a raft in an ocean-only world is exactly the kind of adventure I build mods for!

I make Beach Craft, a free Raft-style ocean dimension for 26.3 Fabric: you build your own raft block by block and sail it like a ship, explore islands, dive, meet 8 NPCs and face the Leviathan as the final boss. It's also part of Dreamcraft, my free 251-mod pack with a quest story in 15 chapters and ten rare pets to tame – so a "beat it from the raft" run has a clear path all the way to the end.

It would make my day to see you sail it. If you'd like to try it, I'm happy to help with anything – a server setup, a custom challenge, early access to the next update, or footage from our trailer.

Beach Craft: {BC}
Dreamcraft: {DC}
Trailer: {SHORT}

Thanks for the fun videos – I'd love to hear what you think!

{SIGN}""",
  followup=creator_followup('Yahiamice', 'Beach Craft'), footer=FOOT)

T['yt-lupinminecraftmods'] = dict(status='hold', status_note=NOMAIL,
  subject="A modpack for a future \"new modpacks\" list",
  message=f"""Hi Lupin,

I enjoyed your "TOP NEW Modpacks of 2026 You Need to Try" – it's great to see someone give new packs a chance!

I'd love to introduce mine: Dreamcraft is a free 26.3 Fabric modpack with 251 mods and a quest story in 15 chapters (348 quests), a whole raft ocean with a boss, ten rare pets to tame, and a ready server pack.

It would mean a lot to see it in one of your lists. If you'd like to try it, I'm happy to help with anything – a server setup, early access to the next update, or footage from our trailer and documentary.

Dreamcraft: {DC}
Trailer: {SHORT}

Thanks for your videos – I'd love to hear what you think!

{SIGN}""",
  followup=creator_followup('Lupin', 'Dreamcraft'), footer=FOOT)

T['yt-DaLilRedMC'] = dict(status='hold', status_note=NOMAIL,
  subject="A cozy questing modpack for a long-form series",
  message=f"""Hi Da Lil Red,

I've been enjoying your "Minecraft But It's STARDEW VALLEY" series in Sunlit Valley – that slow, relaxing long-form style is exactly what I had in mind when I built my modpack!

Dreamcraft is a free 26.3 Fabric modpack with 251 mods and a quest story in 15 chapters, ten rare pets to tame and care for, lots of farming and cooking, and a whole raft ocean with islands to sail to. It's made to be played at your own pace.

It would honestly make my day to see you play it. If you'd like to give it a try, I'm happy to help with anything – setting up a server, early access to the next update, or footage from our trailer and documentary.

Dreamcraft: {DC}
Trailer: {SHORT}

Thank you for the cozy videos – I'd love to hear what you think!

{SIGN}""",
  followup=creator_followup('Da Lil Red', 'Dreamcraft'), footer=FOOT)

T['yt-EnderVerseMC'] = dict(status='hold', status_note=NOMAIL,
  subject="Two candidates for your next 26.3 mods list",
  message=f"""Hi EnderVerse,

I enjoyed your "TOP 20+ Minecraft Mods for 26.3/26.2" list from October – it's always exciting to see what's new for the latest versions!

I have two candidates for a future one, both free for 26.3 Fabric:
- Beach Craft: a Raft-style ocean dimension. Build your own raft block by block and sail it like a ship, explore islands, dive, meet 8 NPCs and face the Leviathan.
- Tamagotchi: ten rare pets hidden in structures that you tame and look after.

Both are server-tested. It would be a real joy to see them in one of your videos. If you'd like to try them, I'm happy to help with anything – early access, a server setup, or footage from our trailer and documentary.

Beach Craft: {BC}
Tamagotchi: {TG}

Thanks for keeping everyone up to date – I'd love to hear what you think!

{SIGN}""",
  followup=creator_followup('EnderVerse', 'Beach Craft and Tamagotchi'), footer=FOOT)

T['yt-cirandev'] = dict(status='hold', status_note=NOMAIL,
  subject="A few new Fabric mods for \"Up & Coming\"",
  message=f"""Hi Ciran,

I saw the first episode of your "Up & Coming" series on trending Fabric mods for Minecraft 26 – what a lovely idea for small mods, thank you for making it!

A few candidates from me, all free for 26.3 Fabric:
- Tamagotchi: ten rare pets hidden in structures to tame and care for.
- Beach Craft: a Raft-style ocean dimension with your own raft, islands, diving, 8 NPCs and a boss.
- Quest Icons, if you also cover tools for pack makers: an FTB-Quests-style quest book for 26.2 and 26.3 that can even import existing FTB Quests books.

It would make my day to see one of them in an episode. If you'd like to try them, I'm happy to help with anything – early access, a test server, or footage.

Tamagotchi: {TG}
Beach Craft: {BC}
Quest Icons: {QI}

Thanks for the series – I'd love to hear what you think!

{SIGN}""",
  followup=creator_followup('Ciran', 'Tamagotchi, Beach Craft and Quest Icons'), footer=FOOT)

T['yt-BisectHosting'] = dict(
  message=f"""Hi BisectHosting team,

I'm Kasax (partner code KASAX007) – I really enjoyed your "MUST PLAY Minecraft Modpacks of 2026!" video, and I'd love to suggest my modpack Dreamcraft for a future roundup.

It's a free 26.3 Fabric modpack with 251 mods and a quest story in 15 chapters (348 quests), a raft ocean with a boss, ten rare pets to tame, and a server pack that runs great on your servers.

It would mean a lot to me to see it featured. I'm happy to help in any way – I can send B-roll from our trailer and documentary, set up a test server, or answer any questions about the pack.

Dreamcraft: {DC}
Trailer: {SHORT}

Thanks for supporting creators like me!
Kasax""",
  followup="Hi BisectHosting team! I just wanted to check whether my note about Dreamcraft reached you – I'd love to hear what you think, and I'm happy to send anything you need. Thanks a lot! – Kasax")

# ------------------------------------------------------------------ pack authors (comments, Discord, GitHub)
T['cf-1609886-waymarked'] = dict(
  message=f"""Hi blurin7! You asked for mod ideas in the comments, so here's one from a fellow creator who really likes what you built. Waymarked already has so much to find – Structory towers, Towns and Towers, Dungeons and Taverns, Moog's Voyager structures – and a quest book could point players at all of it.

I make Quest Icons, an FTB-Quests-style quest book for 26.3 Fabric (chapters, rewards, loot crates, teams and an in-game editor; FTB Quests itself stops at 26.1.2). And if you ever want to explore further: Beach Craft adds a whole ocean dimension (build your own raft, islands, diving, a boss), and Tamagotchi hides ten rare pets in structures.

{QI} · {BC} · {TG}

""" + pack_close('Waymarked', 'I\'d love to write you a free starter chapter, like "waymarks" for the first tower, tavern and village, or help with configs'),
  followup=pack_followup('blurin7', 'Quest Icons', 'Waymarked'))

T['cf-1136552-chillcraft'] = dict(
  message=f"""Hi Gabriele! ChillCraft does relaxed really well – Waystones, Towns and Towers, Farming and Cooking for Blockheads, and even Shogi, which made me smile.

If you ever want a gentle goal for players: Tamagotchi (26.3 Fabric) hides ten rare pets in structures. You tame them, feed them and look after them – nothing hard or grindy. It's made for modpacks: pet diets and pet homes are tags, so it plays nicely with your other mods.

{TG}

""" + pack_close('ChillCraft', 'I can help with configs or a small datapack so your food feeds the pets'),
  followup=pack_followup('Gabriele', 'Tamagotchi', 'ChillCraft'))

T['cf-1606968-cactus-edition'] = dict(
  message=f"""Hi water_wind_! I love the Four Nations idea – EarthBending, Momo and the dragons are so much fun. You already organized the advancement pages so nicely, and a quest book could take that even further and lead players through each nation step by step.

I make Quest Icons, an FTB-Quests-style quest book for 26.3 Fabric with chapters, rewards, loot crates, teams and an in-game editor.

{QI}

""" + pack_close('Cactus Edition', 'I\'d love to write you a free starter chapter for one of the nations, or help with the setup'),
  followup=pack_followup('water_wind_', 'Quest Icons', 'Cactus Edition'))

T['cf-1722887-farm-explore'] = dict(
  message=f"""Hi ayberk168! Farm&Explore is lovely – more than a dozen farming and cooking mods (Farmer's Delight, Rustic Delight, Ube's Delight …) plus Alex's Mobs and Naturalist for the wildlife.

A suggestion from a fellow creator: Tamagotchi (26.3 Fabric) hides ten rare pets in structures; you tame them, feed them and look after them. Pet diets are item tags (tamagotchi:diet/plant, sweet, …), so your crops and meals can feed them with a small datapack, and pet homes are structure tags, so Moog's structures could host them. For the explore half, Beach Craft adds an ocean dimension with your own raft, islands, diving and a boss.

{TG} · {BC}

""" + pack_close('Farm&Explore', 'I can write that datapack for your crops and meals or help with configs'),
  followup=pack_followup('ayberk168', 'Tamagotchi and Beach Craft', 'Farm&Explore'))

T['cf-1725008-the-sift-enhanced-adventure'] = dict(
  message=f"""Hi Blizer! You invited suggestions, so here's one – I really like the idea behind The Sift. Reaching it is the heart of your pack (the goat horn and the note block sequence at an Ancient City), and right now players have to work it out from the description.

I make Quest Icons, an FTB-Quests-style quest book for 26.3 Fabric (chapters, rewards, loot crates, teams and an in-game editor). A small chapter could walk players from the first Ancient City to the portal and the new ore – or stay a puzzle with just a few hints, whatever you prefer.

{QI}

""" + pack_close('The Sift', 'I\'d love to write you a free "Road to The Sift" chapter, or help with the setup'),
  followup=pack_followup('Blizer', 'Quest Icons', 'The Sift'))

T['cf-1727142-litehearted'] = dict(
  message=f"""Hi Alextwicle! Your FAQ says suggestions are welcome, so here's one. It also says there's no wiki yet and points players to the advancements tab – a quest book could be that friendly guide.

I make Quest Icons, an FTB-Quests-style quest book with chapters, rewards, loot crates, teams and an in-game editor, now for 26.2 and 26.3 Fabric (FTB Quests stops at 26.1.2).

{QI}

""" + pack_close('LiteHearted', 'I\'d love to write you a free starter chapter, like a tour through the Wizards spells, Dungeons and Taverns and End Remastered'),
  followup=pack_followup('Alextwicle', 'Quest Icons', 'LiteHearted'))

T['cf-1739929-emberwild-journey'] = dict(
  message=f"""Hi TihomirDobrev! "Bug or idea?" – here's an idea, from someone who really enjoys what you built. Emberwild already has its own Journey Book and great travel tools (Lodeways, Haversack), and Terralith, Tectonic and Nullscape reshape the land and the End. One frontier it doesn't have yet is the sea.

Beach Craft (26.3 Fabric) adds an ocean dimension behind a driftwood portal: build your own raft block by block, sail between islands, dive, meet 8 NPCs and face the Leviathan. It runs on dedicated servers and in my 251-mod pack Dreamcraft. And if you ever want companions, Tamagotchi hides ten rare pets in structures.

{BC} · {TG}

""" + pack_close('Emberwild Journey', 'I can help with configs or with fitting it into your Journey Book'),
  followup=pack_followup('TihomirDobrev', 'Beach Craft', 'Emberwild Journey'))

T['cf-1760069-fern-and-feather'] = dict(
  message=f"""Hi Metzerhigh! You asked for mod suggestions, and Fern & Feather looks so cozy with the whole Kaleidoscope cooking set (Cookery, Grilling, Tavern).

Tamagotchi might fit right in: ten rare pets hide in structures, and you tame them, feed them and look after them (26.3 Fabric). Their diets are item tags, so your cooked dishes can be added with a small datapack.

{TG}

""" + pack_close('Fern & Feather', 'I can write that datapack for your dishes'),
  followup=pack_followup('Metzerhigh', 'Tamagotchi', 'Fern & Feather'))

T['cf-1782391-drays-adventuries'] = dict(
  message=f"""Hi Dray! You said mod suggestions reach you fastest on Discord, so here's one. Your pack already has Fishing Paradise and Moog's Ocean Structures, plus The Sift and The Rift as new worlds – Beach Craft would add a whole ocean dimension: build your own raft, sail between islands, dive, meet 8 NPCs and fight the Leviathan (26.3 Fabric, server-tested). And since Call Your Cat is in there: Tamagotchi hides ten rare pets in structures to tame and look after.

{BC} · {TG}

""" + pack_close("Dray's Adventuries", 'I can help with configs or answer any questions'),
  followup=pack_followup('Dray', 'Beach Craft', "Dray's Adventuries"))

T['cf-486451-space-fight-and-simulation'] = dict(
  message=f"""Hi JD_Virk! Your page asks for favorite mods and suggestions, so here's one. The description mentions a main questline and side quests, and the 26.3 Fabric version (55 mods) doesn't have a quest mod yet – FTB Quests stops at 26.1.2.

I make Quest Icons, an FTB-Quests-style quest book for 26.3 Fabric with chapters, rewards, loot crates, teams and an in-game editor. If you want more ocean content too, Beach Craft adds a whole ocean dimension with your own raft, islands, diving and a boss.

{QI} · {BC}

""" + pack_close('your packs', 'I\'d love to write you a free starter chapter, for example a questline through the Dungeons and Taverns overhauls you already have, for this pack and for Fungle flavour'),
  followup=pack_followup('JD_Virk', 'Quest Icons', 'your packs'))

T['cf-690828-the-solar-apocalypse'] = dict(
  message=f"""Hi SeriousFreezing! The escalating sun is such a great hook – fires around day 5, burning blocks by day 10, then the world collapsing layer by layer. A quest book could turn that timeline into goals ("get underground before day 15") and guide new players through it.

I make Quest Icons, an FTB-Quests-style quest book with chapters, rewards, loot crates, teams and an in-game editor, now for 26.2 and 26.3 Fabric.

{QI}

""" + pack_close('The Solar Apocalypse', 'I\'d love to write you a free starter chapter for the first days of the catastrophe'),
  followup=pack_followup('SeriousFreezing', 'Quest Icons', 'The Solar Apocalypse'))

T['mr-aEksfxM8-the-long-haul'] = dict(
  message=f"""Hi rEiLLy! The Long Haul is built around slow, rewarding progression – which is exactly what a quest book is good at. You already have a wiki, and Quest Icons could bring that roadmap into the game: an FTB-Quests-style quest book for 26.3 Fabric with chapters, rewards, loot crates, teams and an in-game editor (FTB Quests stops at 26.1.2). I also make Tamagotchi (ten rare pets hidden in structures) if you want a long-term companion goal.

{QI} (Modrinth: {{modrinth_url}})

""" + pack_close('The Long Haul', 'I\'d love to write you a free starter chapter, like the first steps through your skill progression and Towns and Towers'),
  followup=pack_followup('rEiLLy', 'Quest Icons', 'The Long Haul'))

T['mr-j9Btp1fF-wildworld'] = dict(
  message=f"""Hi ChongYu668! WildWorld has such a great animal lineup – the whole Animal Garden series plus Alex's Mobs – and the moon events make the nights wonderfully tense.

A suggestion from a fellow creator: Tamagotchi (26.3 Fabric) hides ten rare pets in structures; you tame them and look after them, and they grow with you. Pet homes are structure tags and diets are item tags, so you can tune where pets appear and what they eat with a small datapack.

{TG} (Modrinth: {{modrinth_url}})

""" + pack_close('WildWorld', 'I can write that datapack or help with configs'),
  followup=pack_followup('ChongYu668', 'Tamagotchi', 'WildWorld'))

T['mr-kUSmramu-ultimate-vanilla-plus'] = dict(
  message=f"""Hi Superduash! You invited suggestions on Discord, so here's one that keeps the vanilla feel: Tamagotchi (26.3 Fabric) hides ten rare pets in structures – a lovely extra reward for exploring your ten Dungeons and Taverns overhauls. You tame the pets and look after them, and pet homes are structure tags, so you can choose which structures hold them.

{TG} (Modrinth: {{modrinth_url}})

""" + pack_close('Ultimate Vanilla+', 'I can help pick the structures and set up the tags'),
  followup=pack_followup('Superduash', 'Tamagotchi', 'Ultimate Vanilla+'))

T['mr-tVX2TBKb-sensible-mc'] = dict(
  message=f"""Hi Stackelyy! Sensible MC already takes such good care of pets – Respawnable Pets and Perfected Pet are in the list – so here's a suggestion that adds new ones without changing the basic gameplay: Tamagotchi hides ten rare pets in structures that you tame and look after. Diets and pet homes are tags, so it's easy to tune.

{TG} (Modrinth: {{modrinth_url}})

""" + pack_close('Sensible MC', 'I can help with configs or the tags'),
  followup=pack_followup('Stackelyy', 'Tamagotchi', 'Sensible MC'))
