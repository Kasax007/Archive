# Outreach brief for research agents (Stand 10.11.2026) - read fully before you start

Brief of the big round on 9.11.2026, updated for the daily routine on 10.11.2026. Update the facts (versions,
numbers) before reusing it.

You research outreach targets for Kasax (CurseForge author Kasax007) and write personal draft messages.
You NEVER send, post, comment, DM, follow, subscribe or sign up anywhere. Kasax reads, edits and sends every message
himself from a private approval page. Your output is draft files plus one JSON report (see the end).

Repo: `/home/user/Archive/outreach` (git, branch main). Read these first:
- `drafts/README.md` (tone, templates A-E; the tone rules there are binding)
- `drafts/yt-eldor-devs.md`, `drafts/yt-Kianissohot.md` (format and tone of a creator e-mail draft written today)
- `drafts/cf-1760069-fern-and-feather.md` (pack draft format; its text is the OLD tone - write the new warm tone)
- `README.md` sections "Punkteschema" and "Rechtliche Regeln in Kürze"

Do NOT edit `creators.csv`, `targets.csv`, `suppression.csv`, `config.json` or any script, and do not git commit or
push. Only create new files in `drafts/` (and scratch files under
`/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad/agents/<your name>/`).
Skip every target whose id is already in `targets.csv`, `creators.csv`, `suppression.csv` or `drafts/`.
Several agents work at the same time: before you research a target in depth, claim it with
`mkdir -p .../scratchpad/agents/claims-<today as YYYYMMDD>` once, then
`mkdir /tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad/agents/claims-<YYYYMMDD>/<file stem>`
(e.g. `yt-Handle`, `tt-handle`, `cf-123456`). If mkdir fails, another agent has it: pick a different target.
Never overwrite an existing file in `drafts/`.
Exception to the skip rule: rows in `targets.csv` with status `new` and a note starting with `Lead` are good candidates
an earlier run found but could not draft (e.g. the day's HOLD quota was full). Check those first; if they still fit
(fresh video, invited route), claim and draft them - they count as new. Rows with status `skip` and a note
`Geprüft <date>, verworfen: ...` were checked and rejected; look at them again only if the reason may have changed
(e.g. a channel that was inactive).

## Hard rules

1. E-mail addresses never go into any file (not drafts, not scratch files, not logs you save). They go only into the
   JSON of your final report. Print them to your own console only when you need them.
2. A contact route must be one the person invited: a business/contact e-mail they publish themselves (YouTube channel
   description, About page text, website, linktree/beacons, TikTok or Instagram bio), a "DM for business/collabs"
   line in a bio, a pack page that asks for suggestions/feedback/mod requests (comments, Discord suggestion channel,
   issue tracker with a suggestion template). No invitation = no draft (list it under "skipped" with the reason).
3. YouTube addresses that sit only behind the "View email address" button (captcha) count as a route, but such
   drafts get status HOLD (Status cell starts with `HOLD:`); prefer creators with a public address. At most a third of
   your drafts may be HOLD.
4. Honest praise only: refer to real video titles, real pack features, real mod lists. Never claim you watched a
   specific scene; say "I came across ..." / "I love the idea of ...". Every draft cites its evidence (title + URL +
   age/date) under **Belege**.
5. Challenge Craft has a casino challenge - never mention it (many viewers are kids). Bob is always "an AI rival in an
   early stage of development".
6. Forbidden phrases (sound like AI/mass mail): "No pressure - I won't follow up more than once", "One message only",
   "This is a one-off message", "Reply stop and you won't hear from me again", "No payment involved, no obligations",
   any "Why you got this ..." footer.
7. Tone: warm, friendly, motivating, like a creator who genuinely likes their work. Concrete praise first, then the
   mod in 2-3 sentences, then ALWAYS an offer of help (custom challenge, challenge code for their community, server
   setup, early access, footage/B-roll, a free starter quest chapter, configs/datapack/tags for their pack), then a
   warm close. English, 80-170 words, links on their own lines, no markdown inside the message.
   E-mails: sign "Warm wishes,\nKasax" and a separate footer `{postal_address}, {privacy_link}` (format as in the
   eldor draft). Comments/Discord/DMs: no footer; close with "Kasax (Discord: discord.gg/zuZVtVvJaY)".
8. Follow-up (template D) exactly as in the eldor draft, adapted to the name and project.
9. Be polite to the websites: one request at a time, short pauses, no bulk crawling.

## Facts you may use (all free, all true on 10.11.2026)

- **Challenge Craft** (mod, Fabric 26.3, also older builds for 26.2 and 1.21.5): turns any world into a challenge run.
  51 challenges you can stack (each combination gets a difficulty rating), e.g. Lockout Bingo (up to 4 teams on a
  shared 5x5 board), Force Item Battle, All Biomes, Chunk Hunt, Random Chunk Blocks, Random Item every 30s, Random
  Block Drops, Randomized Crafting, The Floor is Lava, Void Trail (every block you leave takes its whole column),
  Random Mob Spawn every 30s, Trivia (a question every 2 minutes - or die), Hardcore, Skyblock, roll a die to walk.
  Daily Challenge (one ruleset + one seed per day, same for everyone). Challenge Codes: send a code and everyone plays
  the same setup on the same seed. Lifetime XP with levels 1-20 and Infinity Stars, kept across worlds and servers.
  Everything works in co-op. Lockout vs Bob, an AI rival (early stage of development). Kasax builds custom challenges
  on request. Mod: https://www.curseforge.com/minecraft/mc-mods/challenge (also Modrinth:
  https://modrinth.com/mod/challenge_craft). Modpack (the mod + shaders + proximity voice chat + ready menu):
  https://www.curseforge.com/minecraft/modpacks/challenge-craft
- **Dreamcraft V1.6** (modpack, Fabric 26.3): 251 mods, a quest story with 369 quests in 16 chapters, a raft ocean
  with story places and a boss (Beach Craft), ten rare pets to tame (Tamacraft), server pack, BisectHosting order link
  (code KASAX007 = 25% off). https://www.curseforge.com/minecraft/modpacks/dreamcraft-new ; short:
  https://www.youtube.com/watch?v=G-whF3xKTQ4 ; trailer and a 21-minute documentary exist (footage on request).
- **Beach Craft 3.4.2** (mod, Fabric 26.3 and 1.21.1): the open-sea survival of the game Raft in Minecraft. Driftwood
  portal to the Endless Sea; build a raft block by block and sail it like a ship (mast, sails, anchor, motor, wheel);
  hook debris, purify water, farm on deck; Bruce the shark bites your raft. Twelve biomes (palm, jungle, mangrove,
  volcanic isles, reefs, kelp forests, frost floes, trenches), seven story places (castaway, Old Lighthouse, Saltmere,
  Helix Station, Port Solace, Ashen Forge, Coral Temple), guarded places with bosses (Scavenger Chief, Corsair
  Captain, Reef Warden), eight NPCs with trades, diving gear, harpoon gun, sea scooter, 84 building blocks and 59
  decorations, cozy furniture with a "Rested" buff, an island kitchen (crops, cooking pot, fish trap, dishes), gear
  (shark tooth spear, boomerang, machete, armour sets, wreck compass), Seafarer's Almanac guide book, optional JEI and
  Lootr support. https://www.curseforge.com/minecraft/mc-mods/beach-craft (Modrinth page still in review - don't link)
- **Tamacraft 1.3.0** (mod, Fabric 26.3 and 1.21.1; formerly "Tamagotchi"): ten rare pets hide in structures; find,
  tame and look after them; moods on a pet screen and in bubbles; pets dance to jukeboxes, warm up at campfires, hide
  from thunder, play together, carry your things and help in fights, never die (they faint into a Tama Egg); furniture
  like a running wheel (redstone signal), toys, treat dispenser, incubator, pet door; Tamacon guide; JEI/REI info
  pages. For packs: pet homes are structure tags, diets are item tags (easy datapack).
  https://www.curseforge.com/minecraft/mc-mods/tamagotchi (Modrinth still in review - don't link)
- **Quest Icons 1.3.0** (mod): FTB-Quests-style quest book - chapters, quest maps, tasks, rewards, loot crates, teams
  and an in-game editor with forms and pickers (nobody has to write SNBT), 470 icons, 56 quest-map pictures, imports
  FTB Quests books (1.20, 1.21, 26.1). Versions: Fabric 26.3, 26.2, 26.1.2, 1.21.11, 1.21.1, 1.20.1; NeoForge 1.21.1;
  Forge 1.20.1. FTB Quests does not exist for 26.2/26.3. https://www.curseforge.com/minecraft/mc-mods/quest-icons
- Kasax's Discord: Kasax Lounge, discord.gg/zuZVtVvJaY. All mods may be used in modpacks.

## Tools that work from this container

- YouTube (public pages, low volume; run from your own scratch dir, the search writes `yt_results.json` there):
  `python3 /home/user/Archive/outreach/tools/yt_search.py "term" "term2"` = videos uploaded this month with channel
  handle, title, age, views. `python3 /home/user/Archive/outreach/tools/yt_channel.py @handle` = description (e-mails
  masked) + latest 12 videos with age, views, ids. `python3 /home/user/Archive/outreach/tools/yt_about.py @handle` =
  subscribers, video count, masked e-mails; with `--show` it prints them unmasked to your console only (for your
  final report - never redirect that output into a file).
- TikTok profile pages are readable with curl (Chrome user agent): JSON in the HTML has `"signature"` (bio) and
  `"followerCount"`. TikTok search pages need JS; find TikTok creators via the WebSearch tool, via links on their
  YouTube channels, or via linktree/beacons pages.
- Instagram answers curl with a login redirect; try the WebFetch tool or the creator's linktree/website; if nothing
  is readable, skip Instagram.
- CurseForge: curl/Playwright get 403 (Cloudflare), but the WebFetch tool reads project pages (description, sidebar
  links). `https://api.cfwidget.com/minecraft/modpacks/<slug>` gives JSON (total downloads, files with per-file
  downloads and dates, members, links); its "monthly" field is always 0. Modrinth API v2 is open
  (`https://api.modrinth.com/v2/search?facets=...`, `/v2/project/<id>`, `/v2/project/<id>/version`), send a
  User-Agent like `Kasax007-outreach-research/1.0`.
- `discover.py` in the repo has helpers you may import read-only (e.g. pack mod-list reading via range requests):
  run Python from your scratch dir with `sys.path.insert(0, '/home/user/Archive/outreach')`.

## Draft file format (parsed by seed_page.py - keep it exact)

File name = id with ":" and "@" removed: `yt:@Handle` -> `drafts/yt-Handle.md`, `tt:@handle` -> `drafts/tt-handle.md`,
`ig:@handle` -> `drafts/ig-handle.md`, `cf:123456` (+slug) -> `drafts/cf-123456-slug.md`, `mr:AbCdEf12` ->
`drafts/mr-AbCdEf12-slug.md`. Structure (German labels, English message):

```
# <Name>

| Feld | Inhalt |
| --- | --- |
| Ziel | [<Name>](<URL>) · `<id>` · Score <NN> · <audience or downloads> |
| Status | <"Senden per E-Mail, werktags (Di–Do)." / "Senden als Kommentar ..." / "HOLD: ..."> |
| Passt | <Challenge Craft / Dreamcraft / Beach Craft / Tamacraft / Quest Icons, comma separated> |
| Kontaktweg | <exact route, German; never the address itself> |
| Warum eingeladen | <why this route is invited; for e-mails add: "Achtung § 7 UWG: Eine Geschäftsadresse ist keine Einwilligung; einzeln, persönlich und mit Fußzeile senden, Restrisiko bleibt."> |
| Vor dem Senden | <what Kasax should check first, German> |

**Belege** (geprüft am <date of your check, e.g. 10.11.2026>):

- <evidence bullet with title, URL, age/date>
- <...>

## Text (<E-Mail, Englisch | CurseForge-Kommentar, Englisch | Discord, Englisch | TikTok-DM, Englisch | Instagram-DM, Englisch>)

**Subject:** <only for e-mails>

> Hi <name>,
>
> <paragraphs>
>
> Warm wishes,
> Kasax

**Fußzeile:**

> {postal_address}, {privacy_link}

## Nachfrage (Vorlage D, frühestens 7 Tage später, nur einmal)

> Hi <name>! I hope you're doing well. ...
>
> Warm wishes,
> Kasax
```

The "## Text (...)" channel must start with "E-Mail" for e-mail routes (the page sends those through Gmail).
Non-e-mail drafts have no Subject and no Fußzeile block. Score: use the scheme in README.md "Punkteschema"
(creators: modded content 25 / other 10, video in last 2 months 20, 1k-100k followers 15, fitting content 20 else 10,
own business route 15, English or German 5). Kasax re-scores later; be roughly right.

## Final report (your last message = JSON only, no prose)

```
{"creators": [{"id": "yt:@Handle", "name": "...", "platform": "youtube|tiktok|instagram", "url": "...",
               "language": "en", "audience": "~12.3K subscribers", "business_route": "<German or English route
               text, no address>", "focus": "...", "fit": "CC;CCP|DC|BC;TG|...", "evidence": "title; title",
               "evidence_url": "...", "evidence_month": "2026-11", "draft": "drafts/yt-Handle.md",
               "status": "draft|hold", "email": "<address or empty>"}],
 "packs": [{"id": "cf:123456", "name": "...", "platform": "curseforge|modrinth", "url": "...",
            "contact_route": "...", "score": 75, "status": "draft|hold", "fit": "QI+BC", "why": "<score breakdown,
            monthly-download estimate, quest/ocean/pet gap, route quote>", "draft": "drafts/cf-123456-slug.md"}],
 "skipped": ["<id>: <one-line reason>"]}
```
