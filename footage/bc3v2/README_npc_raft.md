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

Still coming: `r_sea_chest.mp4` (open the chest at sea and move items; the survival take did not open the chest,
retake planned).

## NPCs (module npc)

World: seed `beachcraft`, survival player (resistance, saturation), first meeting with each person. Dialogue and
trade screens are first-person stills at GUI scale 3 (greeting with the gift line, "What should I do next?",
"Heard any rumours?", trade screen); `_gift` shows the player holding the gift (HUD on). `_talk`: the player walks up,
the person turns to them, the dialogue panel opens at the end (over-the-shoulder camera).

| File | What it shows | s |
| --- | --- | --- |
| n_fenn_work.mp4 | Keeper Tobias Fenn in his cottage at the Old Lighthouse, walking between desk and stove | 4.5 |
| n_fenn_greet.mp4 | Fenn's greeting, "You received: Spyglass" | 2.5 |
| n_fenn_next.mp4 | Hint: sail for Saltmere | 2.5 |
| n_fenn_rumor.mp4 | Rumour: the old Meridian rig | 2.5 |
| n_fenn_trade.mp4 | Fenn's trade screen | 2.5 |
| n_fenn_gift.mp4 | The spyglass in hand, Fenn in front | 2.5 |
| n_nalu_talk.mp4 | The player talks to Nalu on the elder's veranda in Saltmere, dialogue opens | 3.0 |
| n_nalu_greet.mp4 | Nalu's greeting, "You received: Potion of Water Breathing" | 2.5 |
| n_nalu_next.mp4 | Hint: the Coral Sigil in Saltmere's shrine | 2.5 |
| n_nalu_rumor.mp4 | Rumour: a light on the fire island where the old forge stands | 2.5 |
| n_nalu_trade.mp4 | Nalu's trade screen (Saltmere crafts for pearls) | 2.5 |
| n_nalu_gift.mp4 | The water breathing potion in hand, Nalu in front | 2.5 |
| n_tamo_place.mp4 | Orbit over the Saltmere docks (pier, huts, boats) | 4.5 |
| n_tamo_work.mp4 | Old Tamo fishing from the pier (rod, casts) | 4.5 |
| n_tamo_talk.mp4 | The player talks to Tamo on the pier, dialogue opens | 3.0 |
| n_tamo_greet.mp4 | Tamo's greeting, "You received: Cooked Cod" | 2.5 |
| n_tamo_next.mp4 | Hint: the Coral Sigil in the shrine | 2.5 |
| n_tamo_rumor.mp4 | Rumour: Teo's beach bar on the palm isles | 2.5 |
| n_tamo_trade.mp4 | Tamo's trade screen (buys fish, sells a rod and more) | 2.5 |
| n_tamo_gift.mp4 | Cooked cod in hand, Tamo in front | 2.5 |
| n_voss_work.mp4 | Dr. Imara Voss reading her notes in the storeroom of the Ashen Forge (dark: night vision for the camera). Note: in this seed her template spot is inside volcanic rock; for filming she was moved two blocks onto the open floor and a 1×2 gap was cleared for the player | 4.5 |
| n_teo_work.mp4 | Teo at work behind the counter of his tiki bar (beach shack on the palm isles) | 4.5 |

Still coming: n_kai_work, n_lund_work, n_okafor_work (one portrait each), then optional extras
(r_sea_chest, n_fenn_place / n_fenn_talk / n_nalu_place / n_nalu_work / n_voss_place retakes).
