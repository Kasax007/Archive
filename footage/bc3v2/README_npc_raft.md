# Beach Craft 3.1.0 – NPC and raft-building footage (doc v2)

Raw clips for the documentary v2. Landscape 1920×1080, 30 game frames per second (the edit interpolates to 60 fps),
H.264 CRF 17. Shaders: Complementary Reimagined r5.9.3 (Iris 1.11.7, Sodium 0.9.2). HUD off unless noted.
Each clip has `<clip>.sounds.jsonl` (every game sound the client started: time, event, file, position, camera
position) and `<clip>.shot.json`. GUI stills (dialogue and trade screens) are held for 2.5 s; their `.sounds.jsonl`
is empty and their `.shot.json` says `"still": true`.

Worlds: seed `beachcraft`, raft built at x 147..153, z 146..154 on open water south of Saltmere (bow south).
Raft: 63 raft foundations, teak-plank walls at the stern, chest, furnace, 3×3 wheat farm, redstone lamp + lever,
three-high sail, two oars, outboard motor (fuelled), helm, two ship lanterns.

## Raft building (module vessel)

| File | What it shows | s |
| --- | --- | --- |
| r_found_place.mp4 | The player stands on two foundations on open water and places four more straight onto the sea | 4.0 |
| r_found_grow.mp4 | Crane up while the raft grows block by block to 7 × 9 (the player places the near ones, the rest appear in order) | 5.0 |
| r_build_walls.mp4 | The player builds the teak-plank stern walls, two blocks high, gap in the middle for the motor | 4.0 |
| r_build_chest.mp4 | Places the chest and the furnace in front of the walls | 3.0 |
| r_build_farm.mp4 | Sows wheat on the 3×3 farmland (water in a waterlogged slab) | 4.0 |
| r_build_lamp.mp4 | Places a redstone lamp and a lever next to it | 3.0 |
| r_build_sail.mp4 | Sets up the sail (three blocks high, one mast) and the two oars; side camera, player and mast both in view | 4.0 |
| r_build_motor.mp4 | Seen from behind the stern: places the outboard motor and the helm, then holds coal towards the motor | 4.0 |
| r_built_orbit.mp4 | Slow orbit around the finished raft, the player on deck | 5.0 |

## Sailing and using the raft at sea

| File | What it shows | s |
| --- | --- | --- |
| r_setsail.mp4 | The player uses the helm: the raft sets sail and the player sits down at the wheel | 2.5 |
| r_sail_start.mp4 | The raft gets under way; fixed camera ahead and to the side pans with it as it passes | 3.5 |
| r_sail_helm.mp4 | First person at the wheel: over the deck, sail and farm to the bow, the raft sails and turns (the rig swings into view) | 5.0 |
| r_sail_orbit.mp4 | The raft sails a wide circle (player at the helm), the camera keeps its distance: an orbit around the sailing raft, ice floes behind | 5.0 |
| r_sail_wide.mp4 | Wide chase shot behind the raft sailing between ice floes | 5.0 |
| r_sea_furnace.mp4 | At sea, first person: opens the furnace, raw iron smelting, flame burning | 3.0 |
| r_sea_wheat.mp4 | At sea: the wheat grows from sprouts to ripe (random tick speed raised for the shot) | 5.0 |
| r_sea_lever.mp4 | At sea: flips the lever, the redstone lamp lights up | 3.0 |
| r_sea_place.mp4 | At sea: places a teak plank on the deck | 3.0 |
| r_anchor.mp4 | Next to the helm, sneak + use: drop anchor, the raft lines up with the grid and turns back into blocks | 5.0 |
| r_anchored.mp4 | The anchored raft as blocks again among the ice floes (the run timed out: only 2 s) | 2.0 |
| n_lund_place.mp4 | Orbit around the iceberg outpost among the frost floes | 4.5 |
| n_lund_work.mp4 | Dr. Elin Lund at the research terminal in her iceberg outpost hut | 4.5 |
| n_lund_talk.mp4 | The player talks to Lund in the hut, dialogue opens | 3.0 |
| n_lund_greet.mp4 | Lund's greeting, "You received: Honey Bottle" (her "tea") | 2.5 |
| n_lund_next.mp4 | Hint: the Coral Sigil in the shrine | 2.5 |
| n_lund_rumor.mp4 | Rumour: the angry penguins | 2.5 |
| n_lund_trade.mp4 | Lund's trade screen | 2.5 |
| n_lund_gift.mp4 | The honey bottle in hand, Lund in front | 2.5 |
| n_okafor_place.mp4 | Orbit around the rusted rig (Rig Seven) on the open sea | 4.5 |
| n_okafor_work.mp4 | Patience Okafor at the control panels of the rig's control room | 4.5 |
| n_okafor_talk.mp4 | The player talks to Okafor in the control room, dialogue opens | 3.0 |
| n_okafor_greet.mp4 | Okafor's greeting, "You received: Circuit Board" | 2.5 |
| n_okafor_next.mp4 | Hint: the Coral Sigil in the shrine | 2.5 |
| n_okafor_rumor.mp4 | Rumour: the radio picks up singing static at night | 2.5 |
| n_okafor_trade.mp4 | Okafor's trade screen (tech parts) | 2.5 |
| n_okafor_gift.mp4 | The circuit board in hand, Okafor in front | 2.5 |

Not filmed: `r_sea_chest` (in this world the chest at sea did not open: a stray second chest from a retake stood
between the player and the chest, and the clean-up commands failed). The furnace, lever and farm clips show using
blocks at sea instead.

## NPCs (module npc)

World: seed `beachcraft`, survival player (resistance, saturation), first meeting with each person. Dialogue and
trade screens are first-person stills at GUI scale 3 (greeting with the gift line, "What should I do next?",
"Heard any rumours?", trade screen); `_gift` shows the player holding the gift (HUD on). `_talk`: the player walks up,
the person turns to them, the dialogue panel opens at the end (over-the-shoulder camera).

| File | What it shows | s |
| --- | --- | --- |
| n_fenn_place.mp4 | Orbit over the Old Lighthouse on its jungle isle, the keeper's cottage below | 4.5 |
| n_fenn_talk.mp4 | The player talks to Fenn in his cottage, he turns to them and the dialogue opens (second meeting: "So you've seen Saltmere" line) | 3.0 |
| n_fenn_work.mp4 | Keeper Tobias Fenn in his cottage at the Old Lighthouse, walking between desk and stove | 4.5 |
| n_fenn_greet.mp4 | Fenn's greeting, "You received: Spyglass" | 2.5 |
| n_fenn_next.mp4 | Hint: sail for Saltmere | 2.5 |
| n_fenn_rumor.mp4 | Rumour: the old Meridian rig | 2.5 |
| n_fenn_trade.mp4 | Fenn's trade screen | 2.5 |
| n_fenn_gift.mp4 | The spyglass in hand, Fenn in front | 2.5 |
| n_nalu_place.mp4 | High orbit over Saltmere, the stilt village on the coral reef | 4.5 |
| n_nalu_work.mp4 | Nalu on the elder's veranda (close, she walks towards the camera) | 4.5 |
| n_nalu_talk.mp4 | The player talks to Nalu on the elder's veranda in Saltmere, dialogue opens | 3.0 |
| n_nalu_greet.mp4 | Nalu's greeting, "You received: Potion of Water Breathing" | 2.5 |
| n_nalu_next.mp4 | Hint: the Coral Sigil in Saltmere's shrine | 2.5 |
| n_nalu_rumor.mp4 | Rumour: a light on the fire island where the old forge stands | 2.5 |
| n_nalu_trade.mp4 | Nalu's trade screen (Saltmere crafts for pearls) | 2.5 |
| n_nalu_gift.mp4 | The water breathing potion in hand, Nalu in front | 2.5 |
| n_voss_talk.mp4 | World `bcnpc4`, hall re-placed as designed (`place template raft:ashen_forge/hall -1184 163 528 counterclockwise_90`), Voss summoned at her spot: the player meets her in the storeroom (chests, anvil, ore blocks), the first-meeting dialogue opens | 3.0 |
| n_voss_greet.mp4 | First meeting: "Stay back, I... oh. You're not crew. ... I'm Imara Voss. Yes, that Voss. I cracked the Tide Seal", "You received: Potion of Fire Resistance" | 2.5 |
| n_voss_next.mp4 | Hint: the Coral Sigil in the shrine | 2.5 |
| n_voss_rumor.mp4 | Rumour: Captain Marlow leaves notes for everyone who comes through the portals | 2.5 |
| n_voss_gift.mp4 | The fire resistance potion in hand, Voss in front (she has no trades) | 2.5 |
| n_voss_place.mp4 | Orbit over the volcanic isle of the Ashen Forge (lava, ash, the forge walls in the middle) | 4.5 |
| n_tamo_place.mp4 | Orbit over the Saltmere docks (pier, huts, boats) | 4.5 |
| n_tamo_work.mp4 | Old Tamo fishing from the pier (rod, casts) | 4.5 |
| n_tamo_talk.mp4 | The player talks to Tamo on the pier, dialogue opens | 3.0 |
| n_tamo_greet.mp4 | Tamo's greeting, "You received: Cooked Cod" | 2.5 |
| n_tamo_next.mp4 | Hint: the Coral Sigil in the shrine | 2.5 |
| n_tamo_rumor.mp4 | Rumour: Teo's beach bar on the palm isles | 2.5 |
| n_tamo_trade.mp4 | Tamo's trade screen (buys fish, sells a rod and more) | 2.5 |
| n_tamo_gift.mp4 | Cooked cod in hand, Tamo in front | 2.5 |
| n_teo_place.mp4 | Orbit over the tiki-bar beach shack on the palm isles | 4.5 |
| n_teo_talk.mp4 | The player talks to Teo across the bar, dialogue opens | 3.0 |
| n_teo_greet.mp4 | Teo's greeting ("the first drink is on the house"), "You received: Pina Colada" | 2.5 |
| n_teo_next.mp4 | Hint: the Coral Sigil in the shrine | 2.5 |
| n_teo_rumor.mp4 | Rumour: seagulls steal anything not nailed down | 2.5 |
| n_teo_trade.mp4 | Teo's trade screen (drinks and island food) | 2.5 |
| n_teo_gift.mp4 | The piña colada in hand, Teo in front | 2.5 |
| n_teo_work.mp4 | Teo at work behind the counter of his tiki bar (beach shack on the palm isles) | 4.5 |
| n_kai_place.mp4 | Low orbit through the palms to the castaway camp (tent, camp fire, crates) | 4.5 |
| n_kai_work.mp4 | Kai, the SOS castaway, sitting at his camp fire; camera beside the fire, smoke clear of his face | 4.5 |
| n_kai_talk.mp4 | The player talks to Kai by the tent (a tiki torch partly in front), dialogue opens | 3.0 |
| n_kai_greet.mp4 | Kai's greeting: "A real person! ... Did you bring biscuits?" (no gift) | 2.5 |
| n_kai_next.mp4 | Hint: the Coral Sigil in the shrine | 2.5 |
| n_kai_rumor.mp4 | Rumour: abandoned rafts drifting out there | 2.5 |
| n_kai_trade.mp4 | Kai's trade screen (cookies for flotsam) | 2.5 |

Still coming: n_lund_work and n_okafor_work with their screens, n_fenn_place and n_nalu_work
retakes, the screens of Teo and Kai, then optional extras
(r_sea_chest, n_fenn_place / n_fenn_talk / n_nalu_place / n_nalu_work / n_voss_place retakes).

## Worlds and the Ashen Forge (for a structure check)

- NPC footage: world `bcnpc2`, seed `beachcraft`, created 5 Nov 2026 ~14:24 UTC by the bctest harness with the mod at
  `Kasax_Raft_Mod` 26.3 commit `e6b344b` (3.1.0 + deck fix). Calibration world `bcnpc` (same seed) was made at
  `cf5ceb8`.
- Raft footage: world `bcraft`, same seed, built at x 147..153, z 146..154, y 99 (mod at `cf5ceb8`, sailing part at
  `e6b344b`).
- Ashen Forge in this seed (raft dimension): structure start chunk at -1184, 528; bounding box -1196 150 476 ..
  -1096 209 543; piece `ashen_forge/hall` COUNTERCLOCKWISE_90 at -1184 163 488 .. -1139 197 528; piece
  `ashen_forge/vault` at -1138 162 505 .. -1108 183 531. Dr. Voss spawned at -1159.5 168 524.5 (template spot hall
  4.5 5 24.5). Around that spot the storeroom was mostly filled with rock and volcanic ash: only her own column was
  free, a camera or player next to her ended up inside blocks. For the talk shot she was moved to -1157.5 168 524.5 and
  the cells -1158..-1156, 168..169, 524 were cleared.
- Other places in this seed: Old Lighthouse 868 96 716 .. 934 174 812 (Fenn 901.7 121 793.2), Saltmere 141 72 -41 ..
  206 123 39 (Nalu 153.5 103 -11.5, Tamo 201.5 102 -13.5), tiki bar 960 102 2042 .. 980 110 2064 (Teo 977 104 2054.9),
  castaway tent -1022 120 863 .. -1008 124 880 (Kai -1010.5 121 871.5), iceberg outpost 16 81 240 .. 48 115 277
  (Lund 29.75 102.06 261.75), rusted rig 212 20 128 .. 256 144 175 (Okafor 244.5 111 162.5).

## Extra shots for the documentary (world `bcnpc2`, same seed and look)

| File | What it shows | s |
| --- | --- | --- |
| s_lev_strike.mp4 | Abyssal Sanctum, camera high above the pool: the Leviathan circling and surfacing below, the player (survival, Tidebreaker) on the stone ring | 5.0 |
| s_lev_strike3.mp4 | Raised camera outside the ring: the Leviathan rises out of the pool and spits brine bolts at the player | 5.0 |
| s_lev_strike4.mp4 | Close, camera over the pool rim: the Leviathan rears out of the water, then circles below the surface while brine bolts streak past | 5.0 |
| s_lev_strike5.mp4 | Close, same rim camera: it surfaces and dives again near the camera | 5.0 |
| s_lev_strike6.mp4 | Close, from the other side: the Leviathan rises high above the pool and spits brine bolts at the player on the ring (best "rise and spit" take) | 5.0 |
| s_lev_strike7.mp4 | Close: the Leviathan leaps out onto the stone ring and lies stranded, then slithers back (the leap) | 5.0 |
| s_helix_terminal.mp4 | Inside Helix Research Station: a research terminal opened ("Meridian Expedition – Terminal", Helix Log 04 – Drill Order), GUI still | 2.5 |
| b_orchid.mp4 | Jungle isle: slow push towards a tropical orchid (pink) on the shore, a red hibiscus beside it in the foreground | 4.0 |
| b_bird.mp4 | Jungle isle: push in on a bird of paradise; the first ~2 s pass through leaves, from 2 s the flower is clear | 4.0 |
| b_pineapple.mp4 | Palm isle (Kai's island), a ripe wild pineapple bush: the player (survival) picks the fruit and holds it (the bush is small in frame) | 4.0 |
| s_tidebreaker.mp4 | First person with HUD, beach of the jungle isle in rain: the Tidebreaker big in hand, two swings, then the charged throw pose (no surge visible) | 5.0 |
| s_tidebreaker2.mp4 | First person under water: the Tidebreaker swung and charged under the surface | 5.0 |
