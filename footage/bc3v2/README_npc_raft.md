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

Coming in the next pushes, per person: `n_<npc>_place` (establishing orbit of the place), `n_<npc>_work` (the
person at their activity), `n_<npc>_talk` (the player walks up and talks, the dialogue panel opens at the end),
`n_<npc>_greet` / `_next` / `_rumor` / `_trade` (dialogue and trade screens, stills) and `n_<npc>_gift` (first person
with the gift in hand, HUD on).
