"""Die Film-Laeufe der Doku (je ein bctest-Skript, unter 20 Minuten). Erzeugen: python3 tools/runs.py <lauf> <datei>.
Koordinaten aus den Erkundungslaeufen (scout/chests im Log), Welt bcdoc, Seed beachcraft, Dimension raft:raftdim."""
import sys
from film import Script


def r03():
    """Cluster south-west of spawn: volcanic isle, coral temple, galleon, cargo ship, sunken plane, ruins, sanctum,
    abandoned raft, fishing boat, buoy field - candidate stills (outside, inside) and the loot of their chests."""
    s = Script(deadline=17.5)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    # --- volcanic isle (surface)
    s.effects()
    s.view('b_volcano_a', -380, 112, -270, -400, 105, -300, dist=7, settle=60)
    s.view('b_volcano_b', -430, 118, -330, -400, 108, -300, dist=7)
    s.add('cmd execute in raft:raftdim run locate biome raft:volcanic_isle')
    s.add('find raft:black_sand 40', 'find minecraft:lava 48', 'find raft:pumice 40')
    # --- coral temple (template -336 99 -304 .. -296 121 -257), partly above the sea
    s.add('find raft:tidewarden_altar 48', 'find raft:sigil_pedestal 48')
    s.view('p_temple_a', -316, 108, -226, -316, 108, -280, dist=7)
    s.view('p_temple_b', -262, 112, -270, -316, 106, -280, dist=7)
    s.gear('dive').effects('night_vision', 'conduit_power')
    s.view('p_temple_u0', -316, 94, -238, -316, 96, -280, dist=5)
    s.view('p_temple_u1', -270, 94, -300, -316, 96, -280, dist=5)
    s.chest('p_temple_chest', -316, 104, -301)
    s.chest('p_temple_offer', -326, 103, -292)
    # --- galleon wreck (template -371 42 -256 .. -320 71 -228, rotated 90)
    s.ring('p_galleon_r', (-345, 56, -242), 30, 62, n=4, start=30, dist=6)
    s.chest('p_galleon_chest', -343, 46, -250)
    s.chest('p_galleon_treasure', -324, 53, -250)
    # --- cargo ship (template -320 56 -240 .. -296 84 -178)
    s.ring('p_cargo_r', (-308, 68, -209), 34, 76, n=4, start=60, dist=6)
    s.chest('p_cargo_chest', -304, 70, -224)
    s.chest('p_cargo_barrel', -304, 59, -221)
    # --- sunken plane (seaplane, template -470 53 -272 .. -448 67 -250)
    s.ring('p_plane_r', (-459, 59, -261), 20, 64, n=3, start=20, dist=5)
    s.chest('p_plane_crate', -458, 61, -262)
    # --- sunken ruins (shrine, template -492 43 -237 .. -480 56 -224)
    s.ring('p_ruins_r', (-486, 49, -230), 14, 54, n=2, start=200, dist=5)
    s.chest('p_ruins_chest', -486, 46, -229)
    # --- abyssal sanctum (template -528 56 -368 .. -466 89 -267)
    s.add('find raft:tide_seal 80', 'find raft:sanctum_glass 80')
    s.ring('p_sanctum_r', (-497, 72, -318), 60, 80, n=4, start=150, dist=7)
    s.chest('p_sanctum_reward', -497, 70, -363)
    s.chest('p_sanctum_offer', -502, 69, -357)
    s.view('p_sanctum_dome', -497, 70, -300, -497, 66, -327, dist=6)
    # --- abandoned raft (homestead, -576 98 -320 .. -565 106 -312), fishing boat, buoy field
    s.effects()
    s.view('p_raft_a', -555, 101, -300, -570, 100, -316, dist=6)
    s.chest('p_raft_chest', -572, 101, -317)
    s.gear('dive').effects('night_vision', 'conduit_power')
    s.ring('p_fishing_r', (-586, 45, -358), 16, 50, n=2, start=60, dist=5)
    s.chest('p_fishing_barrel', -580, 43, -361)
    s.effects().gear('none')
    s.view('p_buoy_a', -540, 101, -420, -554, 98, -438, dist=6)
    s.add('chests 30')
    # --- palm isle (-256 -288)
    s.view('b_palm_a', -240, 106, -260, -256, 102, -288, dist=7)
    s.add('cmd execute in raft:raftdim run locate biome raft:palm_isle', 'find raft:hibiscus 40', 'find raft:sea_oats 40',
          'find raft:seashells 40', 'find raft:sea_glass_scatter 40', 'find raft:bird_of_paradise 40', 'find raft:giant_clam 60',
          'find raft:sea_urchin 60', 'find raft:starfish_orange 60', 'find raft:sea_anemone_red 60', 'find raft:pineapple_bush 60')
    return s


def r04():
    """Around spawn: Saltmere, buoy field, fishing boat, iceberg outpost, rusted rig (stills + loot); kelp forest with
    sea otters, coral shallows with mantas, jellyfish and a moray eel, frost floes with penguins, open sea with a shark
    at a raft and a hammerhead (clips)."""
    s = Script(deadline=17.5)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    s.effects()
    # --- Saltmere (deck y 102-103, plaza 160..184 / -24..0, shrine 166..178 / -41..-25, elder hut 141..159 / -19..-5)
    s.view('p_saltmere_a', 222, 110, 42, 172, 104, -8, dist=8, settle=60)
    s.view('p_saltmere_b', 118, 112, -62, 172, 104, -8, dist=8)
    s.view('p_saltmere_c', 230, 104, -60, 172, 106, -8, dist=7)
    s.view('p_saltmere_in_a', 172, 103, 0, 172, 104, -30, dist=5, yaw_off=0)
    s.view('p_saltmere_in_b', 176, 103, -20, 168, 104, 10, dist=5, yaw_off=0)
    s.view('p_saltmere_shrine', 172, 103, -27, 172, 103.5, -39, dist=3, yaw_off=0)
    s.chest('s_saltmere_elder', 146, 103, -8)
    s.chest('s_saltmere_shrine', 172, 102, -39)
    s.chest('p_saltmere_market', 165, 102, -9)
    s.chest('p_saltmere_house', 155, 103, 10)
    # --- buoy field (96..116 / 4..16) with its supply crate
    s.view('p_buoy_a', 92, 101, 34, 106, 99, 10, dist=6)
    s.view('p_buoy_b', 126, 101, -4, 104, 99, 11, dist=6)
    s.chest('p_buoy_crate', 105, 99, 12, stand=(105.5, 101, 14.5))
    # --- coral shallows (64, -32): reef stills, mantas, jellyfish, a moray eel
    s.gear('dive').effects('conduit_power')
    s.add('cmd execute in raft:raftdim positioned 64 0 -32 positioned over ocean_floor run tp @p ~ ~4 ~ 200 15', 'fly on', 'settle 40')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 5', 'still b_shallows_under_a 1.25')
    s.add('cmd execute as @p at @p run tp @p ~ ~ ~ ~120 ~', 'wait 5', 'still b_shallows_under_b 1.25')
    s.add('find raft:giant_clam 40', 'find raft:sea_urchin 40', 'find raft:starfish_red 40', 'find raft:sea_anemone_purple 40',
          'find raft:sea_glass_scatter 40', 'find raft:barnacles 40')
    s.add('pcmd summon raft:manta_ray ^2 ^1 ^9', 'pcmd summon raft:manta_ray ^-3 ^2 ^12', 'pcmd summon raft:manta_ray ^0 ^0 ^15', 'wait 20')
    s.rec('c_manta', 90, 15, look='raft:manta_ray', smooth=0.06)
    s.add('cmd kill @e[type=raft:manta_ray,distance=..40]')
    s.add('pcmd summon raft:jellyfish ^1 ^1 ^5 {Variant:"moon"}', 'pcmd summon raft:jellyfish ^-2 ^2 ^7 {Variant:"moon"}',
          'pcmd summon raft:jellyfish ^2 ^3 ^8 {Variant:"crimson"}', 'pcmd summon raft:jellyfish ^-1 ^0 ^9 {Variant:"crimson"}',
          'pcmd summon raft:jellyfish ^0 ^2 ^11 {Variant:"moon"}', 'wait 10')
    s.rec('c_jelly', 75, 15, by='0,0,0,-14,0')
    s.add('cmd kill @e[type=raft:jellyfish,distance=..40]')
    # moray: summon, let it find a crevice, then swim towards it in survival
    s.add('pcmd summon raft:moray_eel ^ ^ ^6', 'wait 120', 'lookat raft:moray_eel', 'cmd gamemode survival @p',
          'cmd effect give @p minecraft:resistance infinite 4 true', 'cmd effect give @p minecraft:water_breathing infinite 0 true')
    s.rec('c_moray', 90, 15, look='raft:moray_eel', chase='3.5,0.5', smooth=0.05)
    s.add('cmd gamemode creative @p', 'cmd kill @e[type=raft:moray_eel,distance=..40]')
    # --- kelp forest (0, 0): under water, then sea otters at the surface
    s.add('cmd execute in raft:raftdim positioned 4 0 4 positioned over ocean_floor run tp @p ~ ~8 ~ 30 10', 'fly on', 'settle 40')
    s.add('still b_kelp_under_a 1.25', 'cmd execute as @p at @p run tp @p ~ ~ ~ ~150 -5', 'wait 5', 'still b_kelp_under_b 1.25')
    s.add('find raft:glow_kelp 48', 'find raft:barnacles 40')
    s.effects()
    s.add('cmd execute in raft:raftdim run tp @p 2 99.6 2 0 20', 'fly on', 'wait 10',
          'pcmd summon raft:sea_otter ^1 ^ ^5', 'pcmd summon raft:sea_otter ^-2 ^ ^7', 'pcmd summon raft:sea_otter ^2 ^ ^9', 'wait 60')
    s.add('cmd item replace entity @p weapon.mainhand with raft:seashell 8')
    s.rec('c_otter', 105, 15, at=[(60, 'lookat raft:sea_otter'), (61, 'use')], look='raft:sea_otter', smooth=0.08)
    s.hands()
    # --- fishing boat (sloop 16..35 / 52..59 / 48..69, barrel 23 53 52)
    s.gear('dive').effects('night_vision', 'conduit_power')
    s.ring('p_fishing_r', (25, 55, 58), 16, 60, n=2, start=200, dist=5)
    s.chest('p_fishing_barrel', 23, 53, 52)
    # --- frost floes (-96, 96) with penguins, iceberg outpost (18..48 / 89..111 / 240..269)
    s.effects().gear('none')
    s.view('b_frost_a', -70, 104, 70, -96, 100, 96, dist=7, settle=60)
    s.add('cmd execute in raft:raftdim positioned -90 0 90 positioned over motion_blocking run tp @p ~ ~ ~ 45 20', 'wait 20',
          'pcmd summon raft:penguin ^1 ^ ^4', 'pcmd summon raft:penguin ^-2 ^ ^6', 'pcmd summon raft:penguin ^2 ^ ^7',
          'pcmd summon raft:penguin ^0 ^ ^5 {Age:-24000}', 'third on', 'wait 40')
    s.rec('c_penguin', 90, 15, look='raft:penguin', smooth=0.06)
    s.view('p_iceberg_a', 33, 106, 220, 33, 102, 255, dist=7)
    s.add('chests 30', 'find raft:expedition_radio 30')
    s.view('p_iceberg_b', 64, 106, 260, 33, 102, 255, dist=7)
    s.chest('p_iceberg_chest', 34, 102, 257)
    # --- rusted rig (212..256 / 20..144 / 128..175): from the sea and on deck
    s.view('p_rig_a', 280, 104, 196, 234, 120, 152, dist=8)
    s.view('p_rig_b', 196, 112, 100, 234, 120, 152, dist=8)
    s.view('p_rig_deck', 236, 116, 150, 234, 116, 135, dist=5)
    s.chest('p_rig_chest', 239, 115, 157)
    # --- open sea (160, 160): a shark circles a raft with a player on it
    s.r('fill 157 99 157 163 99 163 raft:raft_foundation', 'fill 157 100 157 163 104 163 air')
    s.add('cmd execute in raft:raftdim run tp @p 160.5 100 160.5 30 40', 'cmd gamemode survival @p',
          'cmd effect give @p minecraft:resistance infinite 4 true', 'third on', 'cmd attribute @p minecraft:camera_distance base set 6',
          'pcmd summon raft:shark ^6 ^-3 ^10 {PersistenceRequired:1b}', 'wait 420')
    s.rec('c_shark_bite', 180, 15, look='raft:shark', smooth=0.06, pitch=8)
    s.add('cmd gamemode creative @p', 'cmd kill @e[type=raft:shark,distance=..40]')
    # hammerhead under water
    s.gear('dive').effects('night_vision', 'conduit_power')
    s.add('cmd execute in raft:raftdim run tp @p 175 88 175 0 0', 'fly on', 'wait 10', 'pcmd summon raft:hammerhead_shark ^2 ^ ^10 {PersistenceRequired:1b}', 'wait 20')
    s.rec('c_hammerhead', 75, 15, look='raft:hammerhead_shark', smooth=0.08)
    s.add('cmd kill @e[type=raft:hammerhead_shark,distance=..60]')
    return s


def r05():
    """East of spawn: old lighthouse, beach shack, jungle isle, the abyssal trench (helmet lamp, anglerfish, trench
    floor), the pirate cove and the glowing lagoon with glow jellyfish."""
    s = Script(deadline=17.5)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    s.effects()
    # --- old lighthouse (compound 425..464 / 103..146 / 64..105, jetty 422..432 / 106..136)
    s.tp(470, 140, 40).add('settle 60', 'find raft:lighthouse_lens 70', 'chests 50')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 8')
    s.add('nearblock raft:lighthouse_lens 80 40 -32 30', 'fly on', 'settle 40', 'faceblock raft:lighthouse_lens 80', 'still p_lighthouse_a 1.25')
    s.add('nearblock raft:lighthouse_lens 80 -12 -34 48', 'fly on', 'settle 30', 'faceblock raft:lighthouse_lens 80', 'still p_lighthouse_b 1.25')
    s.add('nearblock raft:lighthouse_lens 80 -40 -30 -20', 'fly on', 'settle 30', 'faceblock raft:lighthouse_lens 80', 'still p_lighthouse_c 1.25')
    s.add('cmd attribute @p minecraft:camera_distance base set 3')
    s.add('nearblock raft:lighthouse_lens 80 2 -1 2', 'fly on', 'wait 10', 'faceblock raft:lighthouse_lens 80', 'still p_lighthouse_in 1.25')
    s.view('p_lighthouse_cottage', 447.5, 105, 79.5, 447.5, 105.5, 74, dist=3, yaw_off=0)
    s.chest('s_lighthouse', 447, 105, 75)
    s.chest('p_lighthouse_storage', 436, 104, 90)
    s.view('p_lighthouse_jetty', 427, 117, 150, 430, 120, 100, dist=6, yaw_off=0)
    # --- beach shack (tiki bar 432..454 / 99..107 / 160..180)
    s.view('p_shack_a', 443, 103, 146, 443, 102, 172, dist=6, yaw_off=6)
    s.view('p_shack_b', 468, 104, 186, 443, 102, 170, dist=6)
    s.chest('p_shack_crate', 444, 101, 178)
    # --- jungle isle (352, 96)
    s.view('b_jungle_a', 330, 118, 60, 352, 108, 100, dist=8)
    s.add('find raft:pineapple_bush 60', 'find raft:tropical_fern 60', 'find raft:hibiscus 60', 'find raft:bird_of_paradise 60')
    s.add('cmd attribute @p minecraft:camera_distance base set 4')
    s.add('nearblock raft:pineapple_bush 70 2 0 2', 'wait 5', 'faceblock raft:pineapple_bush 70', 'still b_pineapple_bush 1.25')
    s.add('nearblock raft:bird_of_paradise 70 2 0 3', 'wait 5', 'faceblock raft:bird_of_paradise 70', 'still b_flowers 1.25')
    # --- abyssal trench (448, 0): dark without the lamp, then with it; the trench floor; anglerfish
    s.gear('dive').effects('water_breathing')
    s.add('cmd execute in raft:raftdim run tp @p 448 60 0 0 30', 'settle 40',
          'cmd execute in raft:raftdim positioned 448 0 0 positioned over ocean_floor run tp @p ~ ~3 ~ 0 25', 'fly on', 'wait 40', 'settle 30')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 4', 'still f_lamp_off 1.25')
    s.cmd('item replace entity @p armor.head with raft:diving_helmet[raft:diving_lamp={}]')
    s.add('wait 30', 'still f_lamp_on 1.25')
    s.add('find raft:tube_worms 40', 'find raft:bubble_vent 40', 'find raft:sea_anemone_glow 40')
    s.add('cmd attribute @p minecraft:camera_distance base set 4')
    s.add('nearblock raft:tube_worms 50 3 1 3', 'fly on', 'wait 10', 'faceblock raft:tube_worms 50', 'still b_trench_floor 1.25')
    s.add('nearblock raft:bubble_vent 50 3 2 3', 'fly on', 'wait 10', 'faceblock raft:bubble_vent 50', 'still b_vent 1.25')
    s.add('pcmd summon raft:anglerfish ^1 ^1 ^7', 'pcmd summon raft:anglerfish ^-3 ^2 ^10', 'wait 30',
          'cmd gamemode survival @p', 'cmd effect give @p minecraft:resistance infinite 4 true')
    s.rec('c_angler', 90, 15, look='raft:anglerfish', smooth=0.08)
    s.cmd('item replace entity @p armor.head with raft:diving_helmet', 'effect clear @p night_vision')
    s.add('wait 20', 'still c_angler_dark 1.25')
    s.add('cmd gamemode creative @p', 'cmd kill @e[type=raft:anglerfish,distance=..40]')
    s.cmd('item replace entity @p armor.head with raft:diving_helmet[raft:diving_lamp={}]')
    s.view('b_trench_wall', 448, 70, 30, 448, 40, 0, dist=5, yaw_off=0)
    # --- pirate cove (216..272 / 78..135 / 544..599) and the glowing lagoon (256, 512)
    s.effects().gear('none')
    s.view('p_cove_a', 300, 112, 520, 244, 105, 572, dist=8)
    s.add('find raft:gold_coin_pile 60', 'find raft:wanted_poster 60', 'find raft:jolly_roger 60', 'find raft:treasure_chest 60')
    s.add('cmd attribute @p minecraft:camera_distance base set 4')
    s.add('nearblock raft:gold_coin_pile 60 3 1 4', 'fly on', 'wait 10', 'faceblock raft:gold_coin_pile 60', 'still p_cove_treasure 1.25')
    s.add('nearblock raft:wanted_poster 60 0 0 3', 'fly on', 'wait 10', 'faceblock raft:wanted_poster 60', 'still p_cove_quarters 1.25')
    s.add('nearblock raft:jolly_roger 60 6 2 6', 'fly on', 'wait 10', 'faceblock raft:jolly_roger 60', 'still p_cove_ship 1.25')
    s.chest('s_cove_captain', 248, 101, 552)
    s.chest('p_cove_loot', 245, 102, 591)
    s.gear('dive').effects('water_breathing')
    s.add('cmd execute in raft:raftdim positioned 256 0 512 positioned over ocean_floor run tp @p ~ ~4 ~ 0 10', 'fly on', 'settle 40')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 5', 'still b_lagoon_under 1.25')
    s.add('pcmd summon raft:jellyfish ^1 ^1 ^5 {Variant:"glow"}', 'pcmd summon raft:jellyfish ^-2 ^2 ^7 {Variant:"glow"}',
          'pcmd summon raft:jellyfish ^2 ^3 ^8 {Variant:"glow"}', 'pcmd summon raft:jellyfish ^-1 ^0 ^10 {Variant:"glow"}', 'wait 10')
    s.rec('c_jelly_glow', 75, 15, by='0,0,0,12,0')
    s.add('cmd kill @e[type=raft:jellyfish,distance=..40]')
    s.effects().gear('none')
    s.view('b_lagoon_top', 230, 108, 480, 256, 100, 512, dist=7)
    return s


def r09():
    """The exhibition: all 337 blocks and items of the seven creative tabs (17 stills, names added in the edit), and the
    creative tabs themselves."""
    from museum import museum
    s = Script(deadline=17.5)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.effects()
    museum(s)
    s.add('gui 3', 'hud on')
    for tab, short in [('raft:bc_building', 'building'), ('raft:bc_decor', 'decor'), ('raft:bc_nature', 'nature'),
                       ('raft:bc_voyage', 'voyage'), ('raft:bc_creatures', 'creatures'), ('raft:bc_story', 'story'),
                       ('raft:raft', 'raft')]:
        s.add(f'tab {tab}', 'wait 4 render', f'shot i_tab_{short}', 'esc')
    s.add('hud off')
    return s


def r06():
    """South-west again, with the fixed player: coral temple (outside, altar), galleon with drowned corsairs, cargo
    ship, sunken plane, ruins, sanctum (outside, seal), abandoned raft; volcanic isle with ember crabs; palm isle with
    crabs, seagulls and the beach plants; a giant clam giving its pearl."""
    s = Script(deadline=17.5)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    s.effects()
    # --- coral temple: above the water, then under water, the altar room
    s.view('p_temple_a', -316, 108, -226, -316, 108, -280, dist=7)
    s.view('p_temple_b', -262, 112, -270, -316, 106, -280, dist=7)
    s.add('find raft:tidewarden_altar 64', 'find raft:sigil_pedestal 64')
    s.gear('dive').effects('night_vision', 'conduit_power')
    s.clear_kelp(-330, 86, -250, -300, 100, -228)
    s.view('p_temple_u', -316, 93, -236, -316, 97, -270, dist=5, yaw_off=6)
    s.add('cmd attribute @p minecraft:camera_distance base set 4')
    s.add('nearblock raft:tidewarden_altar 70 0 0 5', 'fly on', 'wait 10', 'faceblock raft:tidewarden_altar 70', 'still p_temple_in 1.25')
    s.add('nearblock raft:tidewarden_altar 70 4 1 -4', 'fly on', 'wait 10', 'faceblock raft:tidewarden_altar 70', 'still p_temple_in2 1.25')
    # --- galleon (template -371 42 -256 .. -320 71 -228): clear view from the south-east, corsairs swimming
    s.clear_kelp(-345, 40, -232, -310, 75, -205)
    s.view('p_galleon_a', -322, 62, -212, -345, 56, -242, dist=6)
    s.clear_kelp(-312, 40, -270, -290, 75, -240)
    s.view('p_galleon_b', -300, 64, -252, -345, 56, -242, dist=6)
    s.add('cmd execute in raft:raftdim run summon raft:drowned_corsair -336 52 -238', 'cmd execute in raft:raftdim run summon raft:drowned_corsair -330 50 -244',
          'cmd execute in raft:raftdim run summon raft:drowned_corsair -342 54 -236', 'wait 10')
    s.add('cmd execute in raft:raftdim run tp @p -322 58 -222 160 15', 'fly on', 'wait 10')
    s.rec('c_corsair', 90, 15, look='raft:drowned_corsair', smooth=0.06)
    s.add('cmd kill @e[type=raft:drowned_corsair,distance=..60]')
    # --- cargo ship (template -320 56 -240 .. -296 84 -178)
    s.clear_kelp(-300, 50, -215, -270, 90, -185)
    s.view('p_cargo_a', -276, 76, -196, -308, 68, -209, dist=6)
    s.view('p_cargo_b', -290, 82, -172, -308, 70, -209, dist=6)
    # --- sunken plane (seaplane -470 53 -272 .. -448 67 -250)
    s.clear_kelp(-460, 50, -252, -435, 72, -232)
    s.view('p_plane_a', -444, 63, -238, -459, 59, -261, dist=5)
    s.view('p_plane_b', -470, 66, -240, -459, 59, -261, dist=5)
    # --- ruins (shrine -492 43 -237 .. -480 56 -224)
    s.clear_kelp(-500, 42, -230, -470, 60, -205)
    s.view('p_ruins_a', -478, 51, -214, -486, 48, -230, dist=5)
    # --- abyssal sanctum: outside, the seal, inside the dome
    s.view('p_sanctum_a', -470, 84, -262, -497, 72, -318, dist=7)
    s.view('p_sanctum_b', -540, 86, -280, -497, 74, -318, dist=7)
    s.view('p_sanctum_seal', -497, 69, -294, -497, 71, -303, dist=4, yaw_off=0)
    s.view('p_sanctum_in', -505, 70, -300, -497, 66, -327, dist=5)
    # --- abandoned raft (homestead -576 98 -320 .. -565 106 -312)
    s.effects().gear('none')
    s.view('p_raft_a', -558, 102, -306, -570, 101, -316, dist=5)
    s.view('p_raft_b', -584, 103, -300, -570, 101, -316, dist=5)
    # --- volcanic isle: the island, black sand and pumice, ember crabs
    s.view('b_volcano_a', -380, 112, -270, -400, 105, -300, dist=7)
    s.view('b_volcano_b', -430, 118, -330, -400, 108, -300, dist=7)
    s.add('cmd attribute @p minecraft:camera_distance base set 6')
    s.add('cmd execute in raft:raftdim positioned -402 0 -372 positioned over motion_blocking run tp @p ~ ~ ~ 0 25', 'wait 10',
          'cmd execute as @p at @p run tp @p ~ ~ ~ 180 25', 'wait 5',
          'pcmd summon raft:ember_crab ^1 ^ ^4', 'pcmd summon raft:ember_crab ^-2 ^ ^5', 'pcmd summon raft:ember_crab ^2 ^ ^6', 'wait 20',
          'cmd gamemode survival @p', 'cmd effect give @p minecraft:resistance infinite 4 true', 'cmd effect give @p minecraft:fire_resistance infinite 0 true')
    s.rec('c_ember', 90, 15, look='raft:ember_crab', smooth=0.06, yawoff=14, pitch=4)
    s.add('cmd gamemode creative @p', 'cmd kill @e[type=raft:ember_crab,distance=..40]', 'cmd effect clear @p')
    # --- palm isle (-256 -288): beach plants, crabs, seagulls
    s.view('b_palm_a', -240, 106, -260, -256, 102, -288, dist=7)
    s.add('cmd attribute @p minecraft:camera_distance base set 4')
    s.add('nearblock raft:sea_oats 60 3 0 2', 'wait 5', 'faceblock raft:sea_oats 60', 'still b_palm_close 1.25')
    s.add('nearblock raft:seashells 60 2 0 2', 'wait 5', 'faceblock raft:seashells 60', 'still b_shells 1.25')
    s.add('cmd execute in raft:raftdim positioned -259 0 -281 positioned over motion_blocking run tp @p ~ ~ ~ 90 25', 'wait 10',
          'pcmd summon raft:crab ^1 ^ ^3 {Variant:"red"}', 'pcmd summon raft:crab ^-1.5 ^ ^4 {Variant:"blue"}', 'pcmd summon raft:crab ^0.5 ^ ^5 {Variant:"sand"}', 'wait 20',
          'cmd gamemode survival @p', 'cmd effect give @p minecraft:resistance infinite 4 true', 'cmd attribute @p minecraft:camera_distance base set 5')
    s.rec('c_crab', 60, 15, look='raft:crab', smooth=0.08, yawoff=14, pitch=4)
    s.rec('c_crab_dig', 75, 15, at=[(2, 'press sprint'), (3, 'press forward'), (40, 'release forward'), (41, 'release sprint')])
    s.add('cmd gamemode creative @p', 'cmd kill @e[type=raft:crab,distance=..40]')
    # seagulls over a little wheat field without a scarecrow
    s.add('cmd execute in raft:raftdim positioned -262 0 -279 positioned over motion_blocking run tp @p ~ ~ ~ 0 20', 'wait 5')
    s.add('pcmd fill ^-2 ^-1 ^3 ^2 ^-1 ^6 minecraft:farmland[moisture=7]', 'pcmd fill ^-2 ^ ^3 ^2 ^ ^6 minecraft:wheat[age=6]',
          'pcmd summon raft:seagull ^ ^6 ^5', 'pcmd summon raft:seagull ^2 ^7 ^8', 'pcmd summon raft:seagull ^-3 ^5 ^7', 'pcmd summon raft:seagull ^1 ^8 ^10',
          'cmd attribute @p minecraft:camera_distance base set 6', 'wait 30')
    s.rec('c_gull', 90, 15, look='raft:seagull', smooth=0.05, yawoff=12)
    s.add('wait 200')
    s.rec('c_gull_peck', 90, 15)
    s.add('cmd kill @e[type=raft:seagull,distance=..60]')
    # --- a giant clam under water: open with a pearl, the player takes it
    s.gear('dive').effects('conduit_power')
    s.add('cmd execute in raft:raftdim positioned -295 0 -265 positioned over ocean_floor run tp @p ~ ~1 ~3 180 35', 'fly on', 'wait 10',
          'pcmd setblock ^ ^-1 ^2 raft:giant_clam[facing=south,open=true,pearl=true,waterlogged=true]', 'wait 5',
          'cmd attribute @p minecraft:camera_distance base set 3', 'third on')
    s.rec('b_clam', 75, 15, at=[(30, 'third off'), (31, 'faceblock raft:giant_clam 10'), (40, 'use'), (60, 'third on')])
    return s


def r07():
    """West: Port Solace (above and under the water, the City Hall tower, the vaults), the Ashen Forge on its volcano,
    the wreck graveyard, a castaway camp."""
    s = Script(deadline=17.5)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    s.effects()
    # --- Port Solace (-1103..-919 / 33..135 / 87..315); city hall -1091..-1057 / 45..123 / 183..219
    s.view('p_solace_top', -985, 106, 140, -1060, 112, 205, dist=8, settle=90)
    s.view('p_solace_top2', -1120, 108, 270, -1050, 112, 200, dist=8)
    s.add('chests 110')
    s.add('openloot story/port_solace_vault 150', 'wait 6 render', 'shot s_storm', 'esc',
          'third on', 'cmd attribute @p minecraft:camera_distance base set 4', 'fly on', 'wait 4', 'still s_storm_room 1.25')
    s.add('openloot story/port_solace_hall 150', 'wait 6 render', 'shot s_solace_hall', 'esc')
    s.add('openloot port_solace_office 150', 'wait 6 render', 'shot p_solace_office', 'esc')
    s.gear('dive').effects('night_vision', 'conduit_power')
    s.view('p_solace_street', -1033, 49, 262, -1033, 50, 225, dist=5, yaw_off=0)
    s.view('p_solace_plaza', -1018, 54, 236, -1033, 50, 200, dist=6)
    s.view('p_solace_tower', -1038, 78, 160, -1074, 92, 201, dist=6)
    s.view('b_shelf_under', -960, 52, 120, -1000, 48, 150, dist=5)
    s.add('openloot port_solace_apartment 150', 'wait 6 render', 'shot p_solace_apartment', 'esc')
    # --- Ashen Forge (-1196..-1096 / 150..209 / 476..543): hall -1184..-1139 / 163..197 / 488..528, vault -1138..-1108
    s.effects().gear('none')
    s.add('cmd effect give @p minecraft:fire_resistance infinite 0 true')
    s.view('p_forge_out', -1120, 190, 455, -1150, 180, 510, dist=8, settle=90)
    s.view('p_forge_out2', -1215, 196, 560, -1150, 180, 510, dist=8)
    s.add('find minecraft:lava 50', 'chests 60')
    s.view('p_forge_in', -1178, 170, 508, -1140, 170, 512, dist=4)
    s.add('openloot story/ashen_vault 80', 'wait 6 render', 'shot s_ember', 'esc',
          'third on', 'cmd attribute @p minecraft:camera_distance base set 4', 'fly on', 'wait 4', 'still s_ember_room 1.25')
    s.add('openloot story/ashen_forge 80', 'wait 6 render', 'shot s_forge_chest', 'esc')
    s.add('openloot ashen_storage 80', 'wait 6 render', 'shot p_forge_storage', 'esc')
    # --- wreck graveyard (-1264, 372)
    s.gear('dive').effects('conduit_power')
    s.add('cmd execute in raft:raftdim run tp @p -1264 90 372 0 10', 'settle 60',
          'cmd execute in raft:raftdim positioned -1264 0 372 positioned over ocean_floor run tp @p ~ ~8 ~ 0 10', 'fly on', 'wait 30',
          'third on', 'cmd attribute @p minecraft:camera_distance base set 5', 'still b_graveyard 1.25',
          'cmd execute as @p at @p run tp @p ~ ~ ~ ~140 5', 'wait 5', 'still b_graveyard2 1.25')
    s.effects().gear('none')
    s.view('b_graveyard_top', -1240, 106, 400, -1264, 100, 372, dist=6)
    # --- castaway camp (tent, -1022..-1008 / 120..124 / 863..880)
    s.view('p_camp_a', -1000, 126, 890, -1015, 121, 871, dist=6, settle=90)
    s.view('p_camp_b', -1032, 128, 858, -1015, 121, 871, dist=6)
    s.add('openloot castaway_camp 40', 'wait 6 render', 'shot p_camp_loot', 'esc')
    return s


def r10():
    """The sea creatures, staged closer: sea otters around a little raft, mantas and jellyfish over the reef, a moray,
    penguins on an ice floe, Bruce circling a raft over the shallows (seen from above), a whale surfacing, a hammerhead."""
    s = Script(deadline=17.5)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    s.effects()
    # --- sea otters in the kelp forest, from a little raft
    s.r('fill 0 99 0 2 99 2 raft:raft_foundation', 'fill 0 100 0 2 103 2 air')
    s.add('cmd execute in raft:raftdim run tp @p 1.5 100 1.5 0 30', 'settle 40', 'third on', 'cmd attribute @p minecraft:camera_distance base set 6',
          'cmd execute in raft:raftdim run summon raft:sea_otter 2.5 99.5 6.5', 'cmd execute in raft:raftdim run summon raft:sea_otter -1.5 99.5 7.5',
          'cmd execute in raft:raftdim run summon raft:sea_otter 4.5 99.5 9.5', 'wait 60')
    s.add('cmd item replace entity @p weapon.mainhand with raft:seashell 8')
    s.rec('c_otter', 90, 15, at=[(50, 'lookat raft:sea_otter'), (51, 'use')], look='raft:sea_otter', smooth=0.06, yawoff=22, pitch=8)
    s.hands()
    # --- coral shallows: mantas, jellyfish, a moray
    s.gear('dive').effects('conduit_power')
    s.add('cmd execute in raft:raftdim positioned 70 0 -20 positioned over ocean_floor run tp @p ~ ~5 ~ 180 5', 'fly on', 'settle 40',
          'cmd attribute @p minecraft:camera_distance base set 4')
    s.add('pcmd summon raft:manta_ray ^3 ^1 ^5', 'pcmd summon raft:manta_ray ^-3 ^2 ^7', 'wait 10')
    s.rec('c_manta', 100, 15, look='raft:manta_ray', chase='6,1', smooth=0.07, yawoff=22)
    s.add('cmd kill @e[type=raft:manta_ray,distance=..60]')
    s.add('cmd execute in raft:raftdim positioned 70 0 -20 positioned over ocean_floor run tp @p ~ ~5 ~ 180 -8', 'fly on', 'wait 5',
          'pcmd summon raft:jellyfish ^2 ^1 ^4 {Variant:"moon"}', 'pcmd summon raft:jellyfish ^3 ^2.5 ^6 {Variant:"crimson"}',
          'pcmd summon raft:jellyfish ^1 ^3 ^7 {Variant:"moon"}', 'pcmd summon raft:jellyfish ^4 ^0.5 ^8 {Variant:"crimson"}',
          'pcmd summon raft:jellyfish ^-2 ^2 ^9 {Variant:"moon"}', 'wait 5')
    s.rec('c_jelly', 75, 15, by='0,0,0,10,0')
    s.add('cmd kill @e[type=raft:jellyfish,distance=..40]')
    s.add('pcmd summon raft:moray_eel ^2 ^ ^4', 'wait 5')
    s.rec('c_moray', 90, 15, look='raft:moray_eel', smooth=0.06, yawoff=22, pitch=8)
    s.add('cmd kill @e[type=raft:moray_eel,distance=..40]')
    # --- Bruce circles a raft over the bright shallows: seen from high above the player on it
    s.effects().gear('none')
    s.r('fill 84 99 -44 88 99 -40 raft:raft_foundation', 'fill 84 100 -44 88 106 -40 air')
    s.add('cmd execute in raft:raftdim run tp @p 86.5 100 -42.5 0 75', 'cmd gamemode survival @p', 'cmd effect give @p minecraft:resistance infinite 4 true',
          'third on', 'cmd attribute @p minecraft:camera_distance base set 14',
          'cmd execute in raft:raftdim run summon raft:shark 92 96 -36 {PersistenceRequired:1b}', 'wait 360')
    s.rec('c_shark_bite', 180, 12)
    s.add('cmd gamemode creative @p', 'cmd kill @e[type=raft:shark,distance=..60]')
    # --- penguins on an ice floe in the frost floes
    s.r('fill -100 99 92 -92 99 100 minecraft:packed_ice', 'fill -100 100 92 -92 104 100 air', 'fill -98 100 94 -94 100 98 minecraft:snow')
    s.add('cmd execute in raft:raftdim run tp @p -96.5 101 101.5 180 20', 'settle 40', 'cmd attribute @p minecraft:camera_distance base set 4',
          'cmd execute in raft:raftdim run summon raft:penguin -95.5 101 97.5', 'cmd execute in raft:raftdim run summon raft:penguin -97.5 101 95.5',
          'cmd execute in raft:raftdim run summon raft:penguin -94.5 101 94.5', 'cmd execute in raft:raftdim run summon raft:penguin -96.5 101 96.5 {Age:-24000}', 'wait 30')
    s.rec('c_penguin', 90, 15, look='raft:penguin', smooth=0.05, yawoff=22, pitch=10)
    s.add('cmd kill @e[type=raft:penguin,distance=..40]')
    # --- a whale near a raft on the open sea: wait for it to come up and spout
    s.r('fill 159 99 159 161 99 161 raft:raft_foundation', 'fill 159 100 159 161 104 161 air')
    s.add('cmd execute in raft:raftdim run tp @p 160.5 100 160.5 0 10', 'settle 40', 'cmd attribute @p minecraft:camera_distance base set 7',
          'cmd execute in raft:raftdim run summon raft:whale 160 93 176 {PersistenceRequired:1b}', 'wait 900')
    s.rec('c_whale', 150, 10, look='raft:whale', smooth=0.05, yawoff=10, pitch=4)
    # --- hammerhead under water
    s.gear('dive').effects('night_vision', 'conduit_power')
    s.add('cmd execute in raft:raftdim run tp @p 175 88 175 0 0', 'fly on', 'wait 10', 'pcmd summon raft:hammerhead_shark ^2 ^ ^6 {PersistenceRequired:1b}', 'wait 10',
          'cmd attribute @p minecraft:camera_distance base set 5')
    s.rec('c_hammerhead', 75, 15, look='raft:hammerhead_shark', chase='7,1', smooth=0.07, yawoff=22)
    s.add('cmd kill @e[type=raft:hammerhead_shark,distance=..60]', 'cmd kill @e[type=raft:whale,distance=..80]')
    # --- drowned corsairs at the galleon wreck (-345 56 -242), close
    s.add('cmd execute in raft:raftdim run tp @p -326 58 -226 150 10', 'settle 40', 'fly on', 'cmd attribute @p minecraft:camera_distance base set 4',
          'pcmd summon raft:drowned_corsair ^2 ^ ^5', 'pcmd summon raft:drowned_corsair ^-3 ^1 ^7', 'wait 5')
    s.rec('c_corsair', 90, 15, look='raft:drowned_corsair', chase='6,0.5', smooth=0.07, yawoff=22)
    s.add('cmd kill @e[type=raft:drowned_corsair,distance=..60]')
    return s


def r08():
    """The overworld: a beach with driftwood stumps, the portal built and lit with the energy staff, the trip, the
    arrival platform with the castaway chest, the journal and the almanac; at night, all the lights on a beach deck."""
    s = Script(deadline=17.5)
    s.L = [l for l in s.L if l not in ('cmd advancement grant @p everything',)]
    s.cmd('advancement revoke @p everything', 'clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    s.effects()
    s.add('tpbiome minecraft:beach minecraft:overworld', 'settle 90', 'where', 'find raft:driftwood_log 64')
    s.cmd('execute in minecraft:overworld run time set 6000')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 6')
    s.add('nearblock raft:driftwood_log 64 4 0 4', 'wait 10', 'faceblock raft:driftwood_log 64', 'still w_beach 1.25')
    s.add('nearblock raft:driftwood_log 64 -3 0 5', 'wait 10', 'faceblock raft:driftwood_log 64', 'still w_beach2 1.25')
    # the portal: a frame 4 wide, 5 high, 5 blocks south of the player
    s.cmd('execute as @p at @p run tp @p ~ ~ ~ 0 5')
    s.add('pcmd fill ~-3 ~ ~1 ~4 ~6 ~7 minecraft:air', 'pcmd fill ~-3 ~-1 ~1 ~4 ~-1 ~7 minecraft:sand',
          'pcmd fill ~-1 ~ ~5 ~2 ~4 ~5 raft:driftwood_portal_frame', 'pcmd fill ~ ~1 ~5 ~1 ~3 ~5 minecraft:air')
    s.hands('raft:energy_staff')
    s.add('wait 10')
    s.rec('w_light', 60, 15, at=[(8, 'faceblock raft:driftwood_portal_frame 8'), (10, 'use')])
    s.add('still w_portal_lit 1.25')
    # the trip in survival (the swirl needs the HUD), first person
    s.cmd('gamemode survival @p', 'effect give @p minecraft:resistance infinite 4 true', 'execute as @p at @p run tp @p ~0.5 ~1 ~5.5 0 0')
    s.add('third off', 'hud on')
    s.rec('w_trip', 90, 15)
    s.add('wait 60', 'settle 90', 'hud off', 'where')
    s.cmd('gamemode creative @p')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 7', 'fly on', 'wait 5', 'still w_arrive 1.25')
    s.rec('w_arrive', 90, 15, by='0,0,0,50,6')
    # the castaway chest, the journal, the almanac
    s.add('openloot story/castaway 30', 'wait 6 render', 'shot s_chest', 'esc')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 4', 'fly on', 'wait 3', 'still s_platform 1.25')
    s.hands('raft:expedition_journal')
    s.add('third off', 'hud on', 'wait 5', 'use', 'wait 6 render', 'shot s_journal', 'esc')
    s.hands('raft:seafarers_almanac')
    s.add('use', 'wait 6 render', 'shot f_almanac', 'arrow right', 'wait 3 render', 'shot f_almanac2', 'esc')
    s.hands('raft:seafarers_almanac[custom_data={almanac:"creatures/whale"}]')
    s.add('use', 'wait 6 render', 'shot f_almanac_page', 'esc')
    s.hands('raft:seafarers_almanac[custom_data={almanac:"diving"}]')
    s.add('use', 'wait 6 render', 'shot f_almanac_diving', 'esc')
    s.hands('raft:seafarers_almanac[custom_data={almanac:"sailing"}]')
    s.add('use', 'wait 6 render', 'shot f_almanac_sailing', 'esc', 'hud off')
    s.hands()
    # back on the beach at night: all the lights on a little deck
    s.add('tpbiome minecraft:beach minecraft:overworld', 'settle 60')
    s.cmd('execute in minecraft:overworld run time set 18000', 'execute as @p at @p run tp @p ~ ~ ~ 0 8')
    L = ['pcmd fill ~-6 ~ ~2 ~6 ~7 ~9 minecraft:air', 'pcmd fill ~-6 ~-1 ~3 ~6 ~-1 ~8 raft:driftwood_planks',
         'pcmd fill ~-6 ~-1 ~1 ~6 ~-1 ~2 minecraft:water', 'pcmd fill ~-6 ~ ~9 ~6 ~5 ~9 raft:palm_planks',
         'pcmd fill ~-5 ~3 ~8 ~-1 ~3 ~8 raft:string_lights_warm[facing=north]', 'pcmd fill ~1 ~3 ~8 ~5 ~3 ~8 raft:string_lights_colorful[facing=north]',
         'pcmd fill ~-5 ~4 ~8 ~-1 ~4 ~8 raft:bunting_red_white[facing=north]', 'pcmd fill ~1 ~4 ~8 ~5 ~4 ~8 raft:bunting_rainbow[facing=north]',
         'pcmd fill ~-5 ~2 ~8 ~-3 ~2 ~8 raft:neon_tube_cyan[axis=x]', 'pcmd fill ~3 ~2 ~8 ~5 ~2 ~8 raft:neon_tube_pink[axis=x]',
         'pcmd setblock ~ ~-1 ~7 raft:glowing_tidestone', 'pcmd setblock ~ ~ ~7 raft:lighthouse_lens',
         'pcmd setblock ~-6 ~ ~3 raft:tiki_torch[half=lower,lit=true]', 'pcmd setblock ~-6 ~1 ~3 raft:tiki_torch[half=upper,lit=true]',
         'pcmd setblock ~6 ~ ~3 raft:tiki_torch[half=lower,lit=true]', 'pcmd setblock ~6 ~1 ~3 raft:tiki_torch[half=upper,lit=true]',
         'pcmd setblock ~-4 ~ ~7 raft:brazier[lit=true]', 'pcmd setblock ~-3 ~ ~7 raft:jelly_lamp', 'pcmd setblock ~-2 ~ ~7 raft:coconut_lantern',
         'pcmd setblock ~2 ~ ~7 raft:ship_lantern', 'pcmd setblock ~3 ~ ~7 raft:driftwood_lamp', 'pcmd setblock ~4 ~ ~7 raft:seashell_lamp',
         'pcmd setblock ~-4 ~-1 ~1 raft:buoy_red[waterlogged=true]', 'pcmd setblock ~4 ~-1 ~1 raft:buoy_green[waterlogged=true]']
    cols = ['white', 'red', 'orange', 'yellow', 'lime', 'cyan', 'blue', 'purple', 'pink']
    for i, c in enumerate(cols):
        L.append(f'pcmd setblock ~{i - 4} ~ ~4 raft:paper_lantern_{c}')
    s.add(*L)
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 5', 'wait 20', 'settle 30', 'still f_lights 1.25')
    s.rec('f_lights_pan', 75, 15, by='0,0.6,0,-12,4')
    s.cmd('execute in minecraft:overworld run time set 6000')
    return s


def r11():
    """How things work, on a deck of raft foundations on the open sea (135..145 / 99 / 135..145): the expedition raft
    (placing, riding, upgrades, sailing, menu), boats, diving gear and the air gauge, the air compressor, the harpoon gun,
    the sea scooter, the cannon, the wind turbine and the battery, seats and the hammock, the 2.0 survival blocks, the
    machines, a research terminal and a radio."""
    s = Script(deadline=17.5)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    s.effects()
    s.add('cmd execute in raft:raftdim run tp @p 140.5 112 146.5 0 35', 'fly on', 'settle 60')
    s.r('fill 134 99 134 146 99 146 raft:raft_foundation', 'fill 128 100 128 152 108 152 air', 'kill @e[type=!minecraft:player,distance=..40,x=140,y=100,z=140]')
    s.add('cmd execute in raft:raftdim run tp @p 140.5 100 146.5 0 35', 'wait 20', 'third on', 'cmd attribute @p minecraft:camera_distance base set 6')
    # --- the expedition raft: place it, board it, sail away (no upgrades)
    s.hands('raft:expedition_raft')
    s.add('pose 140.5 100 146.5 0 38')
    s.rec('f_raft_place', 45, 15, at=[(8, 'use')])
    s.add('lookat raft:expedition_raft', 'use', 'wait 10')
    s.rec('f_raft_ride', 90, 15, at=[(4, 'press forward'), (86, 'release forward')])
    s.add('cmd ride @p dismount', 'cmd execute in raft:raftdim run tp @p 140.5 100 146.5 0 30', 'wait 5',
          'cmd execute in raft:raftdim run tp @e[type=raft:expedition_raft,limit=1,sort=nearest] 140.5 99.6 151.5 0 0', 'wait 5')
    # --- the upgrades, one after the other
    s.cmd('item replace entity @p hotbar.0 with raft:raft_sail', 'item replace entity @p hotbar.1 with raft:raft_engine',
          'item replace entity @p hotbar.2 with raft:raft_crate', 'item replace entity @p hotbar.3 with raft:raft_lantern',
          'item replace entity @p hotbar.4 with raft:raft_anchor')
    s.add('lookat raft:expedition_raft')
    s.rec('f_raft_upgrade', 105, 15, at=[(4, 'slot 1'), (6, 'lookat raft:expedition_raft'), (8, 'use'), (24, 'slot 2'), (26, 'lookat raft:expedition_raft'), (28, 'use'),
                                         (44, 'slot 3'), (46, 'lookat raft:expedition_raft'), (48, 'use'), (64, 'slot 4'), (66, 'lookat raft:expedition_raft'), (68, 'use'),
                                         (84, 'slot 5'), (86, 'lookat raft:expedition_raft'), (88, 'use')])
    s.add('lookat raft:expedition_raft', 'sneakuse', 'wait 6 render', 'shot f_raft_menu', 'esc')
    s.add('cmd kill @e[type=raft:expedition_raft]', 'cmd clear @p')
    # --- sailing with sail and engine (fuel in the engine slot 54)
    s.r('summon raft:expedition_raft 140.5 99.6 152.5 {Upgrades:27,Rotation:[0f,0f],Items:[{Slot:54b,id:"minecraft:coal",count:32}]}')
    s.add('wait 5', 'cmd ride @p mount @e[type=raft:expedition_raft,limit=1,sort=nearest]', 'wait 5', 'cmd attribute @p minecraft:camera_distance base set 8')
    s.rec('f_raft_sail', 120, 15, at=[(4, 'press forward'), (60, 'press left'), (75, 'release left'), (116, 'release forward')])
    s.add('cmd ride @p dismount', 'cmd kill @e[type=raft:expedition_raft]', 'cmd execute in raft:raftdim run tp @p 140.5 100 140.5 0 20', 'wait 5')
    # --- the four boats
    s.r('summon raft:palm_boat 147.5 99.6 136.5 {Rotation:[90f,0f]}', 'summon raft:palm_chest_boat 147.5 99.6 139.5 {Rotation:[90f,0f]}',
        'summon raft:driftwood_raft 147.5 99.6 142.5 {Rotation:[90f,0f]}', 'summon raft:driftwood_chest_raft 147.5 99.6 145.5 {Rotation:[90f,0f]}')
    s.view('f_boats', 141.5, 100, 141, 148, 100, 141, dist=4, settle=10, yaw_off=0)
    s.add('cmd kill @e[type=minecraft:boat]', 'cmd kill @e[type=raft:palm_boat]', 'cmd kill @e[type=raft:palm_chest_boat]',
          'cmd kill @e[type=raft:driftwood_raft]', 'cmd kill @e[type=raft:driftwood_chest_raft]')
    # --- deck props: cannon, wind turbine + battery, seats, hammock, purifier, grill, crops, scarecrow, machines, terminal, radio
    s.r('setblock 142 100 136 raft:ship_cannon[facing=north]',
        'fill 135 100 145 135 103 145 raft:steel_beam[axis=y]', 'setblock 135 104 145 raft:wind_turbine[facing=south]', 'setblock 136 104 145 raft:makeshift_battery',
        'setblock 136 103 145 raft:copper_cable',
        'setblock 138 100 138 raft:air_compressor', 'setblock 137 100 138 raft:makeshift_battery{Energy:500000L}',
        'setblock 139 100 143 raft:palm_chair[facing=south]', 'setblock 140 100 143 raft:cushion_red', 'setblock 141 100 143 raft:deck_chair[facing=south]',
        'setblock 143 100 144 raft:hammock[facing=east,part=foot]', 'setblock 144 100 144 raft:hammock[facing=east,part=head]',
        'setblock 136 100 141 raft:water_purifier[facing=south]', 'setblock 137 100 141 raft:simple_grill[facing=south]',
        'fill 142 99 139 144 99 140 raft:crop_plot', 'fill 142 100 139 143 100 140 minecraft:wheat[age=7]', 'fill 144 100 139 144 100 140 raft:pineapple_crop[age=7]',
        'setblock 145 100 139 raft:scarecrow[half=lower,facing=south]', 'setblock 145 101 139 raft:scarecrow[half=upper,facing=south]',
        'setblock 136 100 136 raft:quarry[facing=south]', 'setblock 137 100 136 raft:chunk_destroyer', 'setblock 138 100 136 raft:brick_furnace[facing=south]',
        'setblock 139 100 136 raft:titanium_furnace[facing=south]', 'fill 136 101 136 139 101 136 raft:makeshift_solar_panel',
        'setblock 141 100 138 raft:research_terminal[facing=south]{LogId:"helix_1"}', 'setblock 140 100 138 raft:expedition_radio[facing=south]')
    s.r('item replace block 138 100 138 container.0 with raft:oxygen_tank', 'item replace block 136 100 141 container.0 with minecraft:water_bucket',
        'item replace block 136 100 141 container.1 with minecraft:coal 4')
    # cannon
    s.hands('raft:cannonball 16')
    s.add('cmd execute in raft:raftdim run tp @p 143.5 100 137.5 0 10', 'wait 5', 'faceblock raft:ship_cannon 6', 'cmd attribute @p minecraft:camera_distance base set 5')
    s.rec('f_cannon', 60, 15, at=[(8, 'faceblock raft:ship_cannon 6'), (10, 'use'), (38, 'faceblock raft:ship_cannon 6'), (40, 'use')])
    # wind turbine and battery
    s.hands()
    s.view('f_turbine_still', 133, 102, 151, 135.5, 104.5, 145.5, dist=4, settle=10, yaw_off=8)
    s.rec('f_turbine', 45, 15)
    s.add('openbe 136 104 145', 'wait 6 render', 'shot f_battery', 'esc')
    s.add('openbe 138 100 138', 'wait 6 render', 'shot f_compressor', 'esc')
    s.add('openbe 136 100 141', 'wait 30 render', 'shot f_purifier', 'esc')
    # seats and the hammock
    s.add('cmd execute in raft:raftdim run tp @p 141.5 100 141.5 180 20', 'wait 5', 'third off', 'faceblock raft:deck_chair 4', 'use', 'wait 10',
          'third on', 'cmd attribute @p minecraft:camera_distance base set 4', 'cmd execute as @p at @p run tp @p ~ ~ ~ 160 15', 'wait 3', 'still f_sit 1.25')
    s.add('cmd ride @p dismount', 'cmd execute in raft:raftdim run tp @p 143.5 100 142.5 180 30', 'wait 5', 'third off', 'faceblock raft:hammock 4', 'use', 'wait 20',
          'third on', 'cmd attribute @p minecraft:camera_distance base set 4', 'wait 3', 'still f_hammock 1.25')
    s.add('cmd execute in raft:raftdim run tp @p 140.5 100 140.5 0 20', 'wait 5')
    # grill with fuel and food
    s.cmd('item replace entity @p hotbar.0 with minecraft:oak_planks 4', 'item replace entity @p hotbar.1 with minecraft:beef 1',
          'item replace entity @p hotbar.2 with raft:shark_meat 1')
    s.add('third off', 'cmd execute in raft:raftdim run tp @p 137.5 100 143.5 180 40', 'wait 3', 'faceblock raft:simple_grill 4', 'slot 1', 'use', 'slot 2', 'use', 'slot 3', 'use', 'wait 10')
    s.view('f_grill', 138.5, 100, 144.6, 137.5, 100.5, 141.5, dist=3, settle=10, yaw_off=0)
    s.view('f_crops', 143.5, 100, 136.2, 143.5, 100.5, 140, dist=4, settle=10, yaw_off=0)
    s.view('f_machines', 137.8, 100, 132.2, 137.8, 100.8, 136.5, dist=4, settle=10, yaw_off=0)
    s.view('f_deck', 152, 106, 152, 140, 100, 140, dist=6, settle=10, yaw_off=0)
    # terminal and radio
    s.add('third off', 'hud on', 'cmd execute in raft:raftdim run tp @p 141.5 100 140.5 180 30', 'wait 3', 'faceblock raft:research_terminal 4', 'use',
          'wait 8 render', 'shot f_terminal', 'esc')
    s.add('chat on', 'cmd execute in raft:raftdim run tp @p 140.5 100 140.5 180 30', 'wait 3', 'faceblock raft:expedition_radio 4', 'use',
          'wait 10 render', 'shot f_radio', 'chat off', 'hud off')
    # diving: the air gauge in survival, the harpoon gun, the sea scooter
    s.gear('dive')
    s.cmd('gamemode survival @p', 'effect give @p minecraft:resistance infinite 4 true')
    s.add('cmd execute in raft:raftdim run tp @p 150.5 90 140.5 90 10', 'wait 60', 'hud on', 'third off', 'still f_dive_gauge 1.0', 'hud off')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 4', 'still f_dive 1.25')
    s.cmd('item replace entity @p hotbar.0 with raft:harpoon_gun', 'item replace entity @p hotbar.1 with raft:harpoon 16')
    s.add('slot 1', 'pcmd summon minecraft:cod ^ ^ ^7 {NoAI:1b}', 'wait 3')
    s.rec('f_harpoon', 45, 15, at=[(6, 'use'), (26, 'use')])
    s.cmd('item replace entity @p hotbar.0 with raft:sea_scooter')
    s.add('slot 1', 'cmd execute in raft:raftdim run tp @p 150.5 90 140.5 90 0', 'wait 5')
    s.rec('f_scooter', 75, 15, at=[(3, 'press use'), (70, 'release use')])
    s.add('cmd gamemode creative @p', 'cmd effect clear @p', 'cmd clear @p')
    return s


def r12():
    """The end of the story: the four sigils into the Tidewarden altar of the Coral Temple (the key is forged), the key
    opens the Tide Seal, the dome, the Leviathan woken at its altar, the fight (circling, brine bolts, lunge, roar and
    tidelings, whirlpool, last quarter), its death and the rewards, the journal's last page."""
    s = Script(deadline=18.0)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    # --- the Tidewarden altar (Coral Temple, around -316 -280)
    s.gear('dive').effects('night_vision', 'conduit_power')
    s.add('cmd execute in raft:raftdim run tp @p -316 96 -270 180 10', 'settle 60', 'find raft:tidewarden_altar 64')
    s.cmd('item replace entity @p hotbar.0 with raft:coral_sigil', 'item replace entity @p hotbar.1 with raft:pearl_sigil',
          'item replace entity @p hotbar.2 with raft:storm_sigil', 'item replace entity @p hotbar.3 with raft:ember_sigil')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 3', 'nearblock raft:tidewarden_altar 70 0 0 3', 'fly on', 'wait 5',
          'faceblock raft:tidewarden_altar 70', 'still s_altar_before 1.25')
    at = []
    for k in range(4):
        f0 = 4 + k * 24
        at += [(f0, f'slot {k + 1}'), (f0 + 2, 'faceblock raft:tidewarden_altar 8'), (f0 + 4, 'use')]
    s.rec('s_altar', 130, 15, at=at)
    s.add('still s_altar_after 1.25')
    # --- the Tide Seal (5x5 at -499..-495 / 69..73 / -303), opened with the key
    s.hands('raft:tidewarden_key')
    s.add('cmd execute in raft:raftdim run tp @p -497 70 -293 180 5', 'settle 40', 'fly on', 'cmd attribute @p minecraft:camera_distance base set 4')
    s.add('pose -496.5 69 -296.5 180 3')
    s.rec('s_seal', 75, 15, at=[(10, 'faceblock raft:tide_seal 6'), (12, 'use')])
    # --- inside: the dome and the pool; wake the Leviathan at its altar (-497 69 -318, the pool centre 9 blocks north)
    s.effects('water_breathing', 'resistance', 'regeneration', 'saturation', 'fire_resistance')
    s.cmd('effect give @p minecraft:resistance infinite 4 true')
    s.view('s_dome', -500.5, 69, -306.5, -497, 66, -327, dist=4, settle=20, yaw_off=0)
    s.add('cmd execute in raft:raftdim run tp @p -497.5 69 -315.5 180 15', 'wait 5', 'cmd gamemode survival @p', 'third on',
          'cmd attribute @p minecraft:camera_distance base set 6', 'pose -497.5 69 -315.5 180 12')
    s.rec('s_wake', 120, 15, at=[(6, 'faceblock raft:leviathan_altar 5'), (8, 'use'), (14, 'pose -497.5 69 -315.5 180 -4')])
    s.cmd('effect give @p minecraft:resistance infinite 4 true')
    s.rec('s_fight1', 150, 15, look='raft:leviathan', smooth=0.05, yawoff=8, pitch=6)
    s.rec('s_fight2', 150, 15, look='raft:leviathan', smooth=0.05, yawoff=-8, pitch=6)
    s.add('cmd data merge entity @e[type=raft:leviathan,limit=1] {Health:280f}', 'cmd effect give @p minecraft:resistance infinite 4 true')
    s.rec('s_roar', 150, 15, look='raft:leviathan', smooth=0.05, yawoff=8, pitch=6)
    s.rec('s_whirl', 150, 15, look='raft:leviathan', smooth=0.05, yawoff=-8, pitch=6)
    s.add('cmd data merge entity @e[type=raft:leviathan,limit=1] {Health:120f}')
    s.rec('s_last', 120, 15, look='raft:leviathan', smooth=0.05, yawoff=8, pitch=6)
    s.rec('s_death', 135, 15, at=[(10, 'cmd damage @e[type=raft:leviathan,limit=1] 2000 minecraft:generic_kill by @p')],
          look='raft:leviathan', smooth=0.05, pitch=6)
    s.add('wait 60', 'cmd gamemode creative @p', 'cmd kill @e[type=raft:tideling]')
    s.add('cmd execute as @p at @p run tp @p ~ ~ ~ 180 35', 'wait 5', 'still s_drops 1.25')
    # --- the rewards: the Heart of the Tide in the pool, the trophy, the Tidebreaker
    s.r('setblock -497 66 -327 raft:heart_of_the_tide[waterlogged=true]', 'setblock -500 70 -312 raft:leviathan_trophy[facing=south]')
    s.view('s_heart', -497, 68, -321, -497, 66, -327, dist=4, settle=10, yaw_off=0)
    s.hands('raft:tidebreaker')
    s.view('s_tidebreaker', -494, 69, -314, -497, 69, -327, dist=3, settle=10, yaw_off=20)
    s.view('s_trophy', -500, 69, -309, -500, 70.5, -312, dist=2.5, settle=10, yaw_off=0)
    # --- the last page of the journal
    s.cmd('advancement grant @p everything')
    s.hands('raft:expedition_journal')
    s.add('third off', 'hud on', 'wait 5', 'use', 'wait 6 render', 'shot s_end', 'esc', 'hud off')
    s.hands('raft:seafarers_almanac[custom_data={almanac:"leviathan"}]')
    s.add('hud on', 'use', 'wait 6 render', 'shot s_almanac_lev', 'esc', 'hud off')
    return s


def r13():
    """Pick-ups with clean stages: land creatures (crabs digging in, ember crabs, seagulls pecking a field) on flat
    stages in their biomes, a giant clam and a sea urchin on an under-water stage, the lighthouse seen from above the
    jungle, the jungle and mangrove isles, the open Endless Sea, aerial views for the opening."""
    s = Script(deadline=17.5)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    s.effects()
    # --- aerial views over the archipelago (player on a barrier block high up)
    s.add('cmd execute in raft:raftdim run tp @p 120.5 171 60.5 150 32', 'fly on', 'settle 90')
    s.r('setblock 120 170 60 minecraft:barrier')
    s.add('cmd execute in raft:raftdim run tp @p 120.5 171 60.5 150 32', 'wait 10', 'third on', 'cmd attribute @p minecraft:camera_distance base set 8',
          'pose 120.5 171 60.5 150 32', 'still o_aerial 1.25', 'pose 120.5 171 60.5 230 30', 'still o_islands 1.25')
    s.rec('o_aerial_pan', 90, 15, by='0,0,0,-30,0')
    # --- under water stage: a giant clam and a sea urchin on sand (coral shallows, 64 -32)
    s.gear('dive').effects('conduit_power')
    s.add('cmd execute in raft:raftdim run tp @p 64.5 104 -28.5 180 30', 'fly on', 'settle 60')
    s.r('fill 58 86 -38 70 96 -26 minecraft:water', 'fill 58 85 -38 70 85 -26 minecraft:sand',
        'setblock 64 86 -32 raft:giant_clam[facing=south,open=true,pearl=true,waterlogged=true]',
        'setblock 61 86 -33 raft:sea_urchin[waterlogged=true]', 'setblock 67 86 -34 raft:sea_anemone_purple[waterlogged=true]',
        'setblock 66 86 -31 raft:starfish_orange[face=floor,facing=north,waterlogged=true]', 'setblock 62 86 -30 raft:sea_anemone_red[waterlogged=true]',
        'setblock 60 86 -35 raft:sea_anemone_glow[waterlogged=true]', 'setblock 68 86 -30 raft:seashells[shells=3,waterlogged=true]',
        'setblock 66 85 -35 raft:bubble_vent', 'setblock 59 86 -31 raft:barnacles[down=true,waterlogged=true]')
    s.add('cmd execute in raft:raftdim run tp @p 64.5 87 -28.5 180 30', 'fly on', 'settle 30', 'third on', 'cmd attribute @p minecraft:camera_distance base set 3',
          'pose 64.5 87 -28.5 180 30', 'still b_reef_close 1.25')
    s.rec('b_clam', 75, 15, at=[(20, 'third off'), (22, 'faceblock raft:giant_clam 6'), (30, 'use'), (52, 'third on'), (53, 'pose 64.5 87 -28.5 180 30')])
    # --- lighthouse from above the jungle canopy, the lantern room (lens 452 136 93), the cottage
    s.effects().gear('none')
    s.add('cmd execute in raft:raftdim run tp @p 480 152 128 145 20', 'settle 60', 'third on', 'cmd attribute @p minecraft:camera_distance base set 8',
          'fly on', 'faceblock raft:lighthouse_lens 80', 'still p_lighthouse_a 1.25')
    s.add('cmd execute in raft:raftdim run tp @p 452.5 118 150 180 -8', 'fly on', 'wait 10', 'faceblock raft:lighthouse_lens 80', 'still p_lighthouse_b 1.25')
    s.add('cmd execute in raft:raftdim run tp @p 420 140 70 -60 0', 'fly on', 'wait 10', 'faceblock raft:lighthouse_lens 80', 'still p_lighthouse_d 1.25')
    s.effects('night_vision')
    s.add('cmd attribute @p minecraft:camera_distance base set 3', 'nearblock raft:lighthouse_lens 80 0 -1 2.5', 'fly on', 'wait 5',
          'faceblock raft:lighthouse_lens 80', 'still p_lighthouse_in 1.25')
    s.view('p_lighthouse_cottage', 447.5, 105, 78.5, 447.5, 105.5, 74.5, dist=2.5, settle=10, yaw_off=0)
    s.effects()
    # --- jungle isle and mangrove isle, a ripe pineapple bush picked
    s.add('tpbiome raft:jungle_isle', 'settle 60', 'cmd execute as @p at @p run tp @p ~ ~12 ~ ~ 20', 'fly on', 'wait 10',
          'third on', 'cmd attribute @p minecraft:camera_distance base set 8', 'still b_jungle 1.25',
          'cmd execute as @p at @p run tp @p ~ ~ ~ ~120 20', 'wait 5', 'still b_jungle2 1.25')
    s.add('cmd execute as @p at @p run tp @p ~ ~-12 ~ ~ 25', 'wait 10', 'cmd attribute @p minecraft:camera_distance base set 3',
          'pcmd fill ^-1 ^-1 ^2 ^1 ^-1 ^4 minecraft:grass_block', 'pcmd fill ^-1 ^ ^2 ^1 ^2 ^4 minecraft:air',
          'pcmd setblock ^ ^ ^3 raft:pineapple_bush[age=3]', 'pcmd setblock ^-1 ^ ^3 raft:tropical_fern', 'pcmd setblock ^1 ^ ^3 raft:hibiscus', 'wait 5')
    s.rec('b_pineapple', 60, 15, at=[(14, 'third off'), (16, 'faceblock raft:pineapple_bush 6'), (22, 'use'), (44, 'third on')])
    s.add('tpbiome raft:mangrove_isle', 'settle 60', 'cmd execute as @p at @p run tp @p ~ ~10 ~ ~ 20', 'fly on', 'wait 10',
          'third on', 'cmd attribute @p minecraft:camera_distance base set 8', 'still b_mangrove 1.25')
    # --- the open Endless Sea: on the surface and under it
    s.add('cmd execute in raft:raftdim run tp @p 175 99.8 190 200 2', 'settle 40', 'fly on', 'third on', 'cmd attribute @p minecraft:camera_distance base set 6',
          'wait 5', 'still b_ocean_top 1.25')
    s.gear('dive').effects('conduit_power')
    s.add('cmd execute in raft:raftdim run tp @p 175 80 190 200 5', 'fly on', 'wait 30', 'still b_ocean_under 1.25')
    # helmet lamp check deep in the open sea (no conduit power: it brightens like night vision)
    s.effects('water_breathing')
    s.add('cmd execute in raft:raftdim run tp @p 175 52 190 200 10', 'fly on', 'wait 40', 'still x_lamp_off 1.0')
    s.cmd('item replace entity @p armor.head with raft:diving_helmet[raft:diving_lamp={}]')
    s.add('wait 40', 'cmd execute if items entity @p armor.head raft:diving_helmet[raft:diving_lamp] run say LAMP_ITEM_OK',
          'cmd execute as @p if entity @s[nbt={active_effects:[{id:"minecraft:night_vision"}]}] run say LAMP_NV_OK', 'still x_lamp_on 1.0')
    s.cmd('item replace entity @p armor.head with raft:diving_helmet')
    # --- Helix Research Station (template -408 51 -37 .. -352 67 16): outside, inside the domes, the lab and the vault
    s.effects('night_vision', 'conduit_power')
    s.clear_kelp(-372, 48, -10, -330, 80, 40)
    s.add('cmd execute in raft:raftdim run tp @p -350 70 30 220 20', 'settle 60', 'fly on', 'cmd attribute @p minecraft:camera_distance base set 7',
          'face -380 58 -10', 'still p_helix_out 1.25')
    s.add('cmd execute in raft:raftdim run tp @p -330 64 -10 270 10', 'fly on', 'wait 10', 'face -380 58 -10', 'still p_helix_out2 1.25')
    s.add('chests 60')
    s.add('openloot story/helix_lab 80', 'wait 6 render', 'shot s_helix_lab', 'esc', 'third on', 'cmd attribute @p minecraft:camera_distance base set 3',
          'fly on', 'wait 3', 'still p_helix_in 1.25')
    s.add('openloot story/helix_vault 80', 'wait 6 render', 'shot s_pearl', 'esc', 'third on', 'fly on', 'wait 3', 'still p_helix_vault 1.25')
    s.add('openloot helix_storage 80', 'wait 6 render', 'shot p_helix_storage', 'esc')
    s.add('third off', 'hud on', 'faceblock raft:research_terminal 6', 'use', 'wait 8 render', 'shot s_helix_terminal', 'esc', 'hud off')
    return s


def r14():
    """Creature retakes, every stage built only after the player is there (chunks loaded): sea otters around a little
    raft in the kelp forest, penguins on an ice floe, a whale near a raft on the open sea."""
    s = Script(deadline=17.5)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    s.effects()
    # --- sea otters
    s.add('cmd execute in raft:raftdim run tp @p 1.5 112 1.5 0 30', 'fly on', 'settle 60')
    s.r('fill 0 99 0 2 99 2 raft:raft_foundation', 'fill 0 100 0 2 103 2 air', 'fill -6 99 4 8 99 14 minecraft:water replace minecraft:kelp',
        'fill -6 90 4 8 99 14 minecraft:water replace minecraft:kelp_plant')
    s.add('cmd execute in raft:raftdim run tp @p 1.5 100 1.5 0 30', 'wait 20', 'third on', 'cmd attribute @p minecraft:camera_distance base set 5',
          'cmd execute in raft:raftdim run summon raft:sea_otter 2.5 99.6 6.5', 'cmd execute in raft:raftdim run summon raft:sea_otter -1.5 99.6 7.5',
          'cmd execute in raft:raftdim run summon raft:sea_otter 4.5 99.6 9.5', 'wait 80', 'pose 1.5 100 1.5 0 28')
    s.add('cmd item replace entity @p weapon.mainhand with raft:seashell 8')
    s.rec('c_otter', 90, 15, at=[(50, 'lookat raft:sea_otter'), (51, 'use'), (53, 'pose 1.5 100 1.5 0 28')])
    s.hands()
    s.add('cmd kill @e[type=raft:sea_otter,distance=..40]')
    # --- penguins on an ice floe (frost floes)
    s.add('cmd execute in raft:raftdim run tp @p -96.5 112 101.5 180 20', 'fly on', 'settle 60')
    s.r('fill -101 99 91 -91 99 101 minecraft:packed_ice', 'fill -101 100 91 -91 104 101 air', 'fill -99 100 93 -93 100 99 minecraft:snow',
        'fill -101 98 91 -91 98 101 minecraft:packed_ice')
    s.add('cmd execute in raft:raftdim run tp @p -96 101 101.5 180 20', 'wait 20', 'cmd attribute @p minecraft:camera_distance base set 4',
          'cmd execute in raft:raftdim run summon raft:penguin -95.5 101 97.5', 'cmd execute in raft:raftdim run summon raft:penguin -97.5 101 95.5',
          'cmd execute in raft:raftdim run summon raft:penguin -94.5 101 94.5', 'cmd execute in raft:raftdim run summon raft:penguin -96.5 101 96.5 {Age:-24000}',
          'wait 30', 'pose -96 101 101.5 180 22')
    s.rec('c_penguin', 105, 15)
    s.add('still b_frost_floe 1.25')
    s.add('cmd kill @e[type=raft:penguin,distance=..40]')
    # --- a whale near a raft on the open sea: it comes up to breathe and spouts
    s.add('cmd execute in raft:raftdim run tp @p 160.5 112 160.5 0 10', 'fly on', 'settle 60')
    s.r('fill 159 99 159 161 99 161 raft:raft_foundation', 'fill 159 100 159 161 104 161 air')
    s.add('cmd execute in raft:raftdim run tp @p 160.5 100 160.5 0 6', 'wait 20', 'cmd attribute @p minecraft:camera_distance base set 6')
    s.r('summon raft:whale 163 96 172 {NoAI:1b,NoGravity:1b,PersistenceRequired:1b,Silent:1b,Rotation:[90f,0f]}')
    s.add('pose 160.5 100 160.5 10 12', 'wait 5', 'still c_p_whale 1.25')
    s.r('kill @e[type=raft:whale,distance=..60,x=160,y=96,z=165]')
    s.add('cmd execute in raft:raftdim run summon raft:whale 160 92 178 {PersistenceRequired:1b}',
          'cmd execute in raft:raftdim run summon raft:whale 172 90 170 {PersistenceRequired:1b}', 'wait 700')
    s.rec('c_whale', 150, 10, look='raft:whale', smooth=0.04, yawoff=12, pitch=5)
    s.rec('c_whale2', 150, 10, look='raft:whale', smooth=0.04, yawoff=-12, pitch=5)
    s.add('cmd kill @e[type=raft:whale,distance=..80]')
    # --- Bruce circling a raft over the sand stage of the shallows (bright floor: the shark shows dark against it)
    s.add('cmd execute in raft:raftdim run tp @p 62.5 112 -30.5 180 40', 'fly on', 'settle 60')
    s.r('fill 54 86 -46 74 98 -24 minecraft:water', 'fill 54 85 -46 74 85 -24 minecraft:sand', 'fill 60 99 -36 64 99 -32 raft:raft_foundation',
        'fill 60 100 -36 64 104 -32 air')
    s.add('cmd execute in raft:raftdim run tp @p 62.5 100 -32.5 180 42', 'wait 10', 'cmd gamemode survival @p',
          'cmd effect give @p minecraft:resistance infinite 4 true', 'third on', 'cmd attribute @p minecraft:camera_distance base set 6')
    s.r('summon raft:shark 62 95 -40 {PersistenceRequired:1b}')
    s.add('wait 320', 'pose 62.5 100 -32.5 180 42')
    s.rec('c_shark_bite', 180, 12)
    s.add('cmd gamemode creative @p')
    s.r('kill @e[type=raft:shark,distance=..60,x=62,y=95,z=-34]')
    return s


def r15():
    """Small things that still work as in Beach Craft 2 (on the deck at 140 99 140): drifting debris pulled in with the
    plastic hook, a message in a bottle, a supply barrel, the receiver, the metal detector, titanium armour, a music
    disc, trash cubes."""
    s = Script(deadline=12.0)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    s.effects()
    s.add('cmd execute in raft:raftdim run tp @p 140.5 112 140.5 0 30', 'fly on', 'settle 60')
    s.r('fill 134 99 134 146 99 146 raft:raft_foundation', 'fill 134 100 134 146 108 146 air', 'fill 118 99 130 133 99 150 minecraft:water')
    # debris and the plastic hook (survival: the hook pulls only for players who can pick things up)
    s.add('cmd execute in raft:raftdim run tp @p 134.5 100 140.5 90 25', 'wait 10', 'cmd gamemode survival @p',
          'cmd effect give @p minecraft:resistance infinite 4 true', 'third on', 'cmd attribute @p minecraft:camera_distance base set 5')
    s.hands('raft:plastic_hook')
    items = ['raft:plastic', 'raft:scrap_metal', 'raft:driftwood_planks', 'raft:palm_leaves', 'raft:plastic', 'raft:coconut']
    for k, it in enumerate(items):
        s.r(f'summon minecraft:item {124.5 + (k % 3) * 2.0:.1f} 99.6 {137.5 + k:.1f} {{Item:{{id:"{it}",count:{1 + k % 2}}},Tags:["raft_debris"],PickupDelay:10s}}')
    s.add('wait 5', 'pose 134.5 100 140.5 90 22')
    s.rec('f_hook', 75, 15, at=[(6, 'press use'), (66, 'release use')])
    s.add('cmd gamemode creative @p', 'cmd clear @p', 'cmd kill @e[type=minecraft:item,distance=..40]')
    s.add('cmd execute in raft:raftdim run tp @p 140.5 100 140.5 0 20', 'wait 5')
    # message in a bottle and a supply barrel
    s.hands('raft:message_in_a_bottle')
    s.add('third off', 'hud on', 'use', 'wait 8 render', 'shot f_bottle', 'esc', 'hud off')
    s.hands('raft:supply_barrel')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 4', 'pose 140.5 100 140.5 0 35')
    s.rec('f_barrel', 45, 15, at=[(8, 'use')])
    s.add('cmd kill @e[type=minecraft:item,distance=..40]')
    # receiver and metal detector (messages above the hotbar)
    s.hands('raft:receiver')
    s.add('third off', 'hud on', 'chat on', 'use', 'wait 6 render', 'shot f_receiver')
    s.hands('raft:metal_detector')
    s.add('cmd execute as @p at @p run tp @p ~ ~ ~ 0 70', 'wait 3', 'use', 'wait 6 render', 'shot f_detector', 'chat off', 'hud off')
    # titanium armour, a music disc, trash cubes
    s.cmd('item replace entity @p armor.head with raft:titanium_helmet', 'item replace entity @p armor.chest with raft:titanium_chestplate',
          'item replace entity @p armor.legs with raft:titanium_leggings', 'item replace entity @p armor.feet with raft:titanium_boots')
    s.view('f_titanium', 140.5, 100, 140.5, 140.5, 101, 150, dist=4, settle=10, yaw_off=0)
    s.add('third front', 'wait 3', 'still f_titanium_front 1.25', 'third on')
    s.gear('none')
    s.r('setblock 142 100 143 minecraft:jukebox')
    s.hands('raft:lofi_beat_music_disc')
    s.add('third off', 'hud on', 'cmd execute in raft:raftdim run tp @p 142.5 100 141.5 0 40', 'wait 3', 'faceblock minecraft:jukebox 4', 'use',
          'wait 10 render', 'shot f_disc', 'hud off')
    s.hands('raft:trash_cube 4')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 4', 'cmd gamemode survival @p',
          'cmd execute in raft:raftdim run tp @p 140.5 100 138.5 180 25', 'wait 3', 'pose 140.5 100 138.5 180 25')
    s.cmd('item replace entity @p hotbar.1 with minecraft:stone 64', 'item replace entity @p hotbar.2 with minecraft:stone 64')
    for i in range(27):
        s.cmd(f'item replace entity @p inventory.{i} with minecraft:stone 64')
    s.add('slot 1')
    s.rec('f_trash', 60, 15, at=[(6, 'use'), (24, 'use'), (42, 'use')])
    s.add('cmd gamemode creative @p', 'cmd clear @p', 'cmd kill @e[type=minecraft:item,distance=..40]')
    return s


def r16():
    """Creature portraits: every creature still (NoAI) on a clean stage right in front of the camera, then free
    (AI on) for a short clip with a fixed camera. Under water on a sand stage in the coral shallows; crabs, gulls,
    ember crabs and penguins on land stages; a sea otter on the water; a whale beside a raft."""
    s = Script(deadline=17.0)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    # --- under water stage (sand floor y 85, water 86..99) in the coral shallows
    s.gear('dive').effects('conduit_power')
    s.add('cmd execute in raft:raftdim run tp @p 64.5 104 -26.5 180 20', 'fly on', 'settle 60')
    s.r('fill 54 86 -46 74 98 -24 minecraft:water', 'fill 54 85 -46 74 85 -24 minecraft:sand',
        'setblock 60 86 -42 raft:sea_anemone_purple[waterlogged=true]', 'setblock 68 86 -41 raft:sea_anemone_red[waterlogged=true]',
        'setblock 57 86 -38 raft:giant_clam[facing=south,open=true,pearl=true,waterlogged=true]', 'setblock 71 86 -39 raft:sea_urchin[waterlogged=true]',
        'setblock 63 86 -44 raft:starfish_red[face=floor,facing=north,waterlogged=true]', 'fill 54 86 -46 74 90 -46 raft:coral_stone_bricks')
    s.add('cmd execute in raft:raftdim run tp @p 64.5 88 -27.5 180 8', 'fly on', 'wait 20', 'third on', 'cmd attribute @p minecraft:camera_distance base set 4')
    portraits = [('raft:shark', 'c_p_shark', '{}'), ('raft:hammerhead_shark', 'c_p_hammerhead', '{}'), ('raft:manta_ray', 'c_p_manta', '{}'),
                 ('raft:jellyfish', 'c_p_jelly_moon', '{Variant:"moon"}'), ('raft:jellyfish', 'c_p_jelly_crimson', '{Variant:"crimson"}'),
                 ('raft:jellyfish', 'c_p_jelly_glow', '{Variant:"glow"}'), ('raft:moray_eel', 'c_p_moray', '{}'), ('raft:anglerfish', 'c_p_angler', '{}'),
                 ('raft:drowned_corsair', 'c_p_corsair', '{}'), ('raft:tideling', 'c_p_tideling', '{}')]
    for ent, name, nbt in portraits:
        extra = nbt[1:-1]
        tag = '{NoAI:1b,NoGravity:1b,PersistenceRequired:1b,Silent:1b,Rotation:[60f,0f]' + (',' + extra if extra else '') + '}'
        s.r(f'summon {ent} 66.5 87.5 -34.5 {tag}')
        s.add('pose 64.5 88 -27.5 175 8', 'wait 4', f'still {name} 1.25')
        s.r(f'kill @e[type={ent},distance=..30,x=64,y=88,z=-30]')
    # free swimmers past a fixed camera
    s.r('summon raft:manta_ray 70 90 -40', 'summon raft:manta_ray 58 91 -42')
    s.add('pose 64.5 88 -27.5 180 4', 'wait 5')
    s.rec('c_manta', 90, 15)
    s.r('kill @e[type=raft:manta_ray,distance=..60,x=64,y=88,z=-30]')
    s.r('summon raft:jellyfish 66 89 -33 {Variant:"moon"}', 'summon raft:jellyfish 62 91 -36 {Variant:"crimson"}', 'summon raft:jellyfish 68 92 -38 {Variant:"moon"}',
        'summon raft:jellyfish 61 88 -40 {Variant:"glow"}', 'summon raft:jellyfish 65 93 -41 {Variant:"crimson"}')
    s.add('pose 64.5 88 -27.5 180 -4', 'wait 5')
    s.rec('c_jelly', 75, 15)
    s.r('kill @e[type=raft:jellyfish,distance=..60,x=64,y=88,z=-30]')
    s.r('summon raft:shark 72 90 -42 {PersistenceRequired:1b}', 'summon raft:hammerhead_shark 56 89 -44 {PersistenceRequired:1b}')
    s.add('pose 64.5 88 -27.5 180 4', 'wait 5')
    s.rec('c_sharks', 90, 15)
    s.r('kill @e[type=raft:shark,distance=..60,x=64,y=88,z=-30]', 'kill @e[type=raft:hammerhead_shark,distance=..60,x=64,y=88,z=-30]')
    s.r('summon raft:moray_eel 66 86.2 -36')
    s.add('pose 64.5 88 -27.5 180 14', 'wait 5')
    s.rec('c_moray', 75, 15)
    s.r('kill @e[type=raft:moray_eel,distance=..60,x=64,y=88,z=-30]')
    # --- land: a sand stage (palm isle) for crabs and gulls, black sand for ember crabs, ice for penguins
    s.effects().gear('none')
    s.add('cmd execute in raft:raftdim run tp @p -259 112 -277.5 180 22', 'fly on', 'settle 60')
    s.r('fill -266 100 -292 -252 108 -276 minecraft:air', 'fill -266 99 -292 -252 99 -276 minecraft:sand', 'fill -266 98 -292 -252 98 -276 minecraft:sandstone',
        'setblock -262 100 -287 raft:sea_oats[half=lower]', 'setblock -262 101 -287 raft:sea_oats[half=upper]', 'setblock -255 100 -288 raft:beach_grass',
        'setblock -257 100 -284 raft:seashells[shells=3]')
    s.add('cmd execute in raft:raftdim run tp @p -259 100 -277.5 180 24', 'wait 10', 'cmd attribute @p minecraft:camera_distance base set 4')
    for ent, name, nbt in [('raft:crab', 'c_p_crab_red', 'Variant:"red"'), ('raft:crab', 'c_p_crab_blue', 'Variant:"blue"'),
                           ('raft:crab', 'c_p_crab_sand', 'Variant:"sand"'), ('raft:seagull', 'c_p_gull', ''), ('raft:sea_otter', 'c_p_otter', '')]:
        tag = '{NoAI:1b,PersistenceRequired:1b,Silent:1b,Rotation:[60f,0f]' + (',' + nbt if nbt else '') + '}'
        s.r(f'summon {ent} -258 100 -283 {tag}')
        s.add('pose -259 100 -277.5 178 26', 'wait 4', f'still {name} 1.25')
        s.r(f'kill @e[type={ent},distance=..30,x=-259,y=100,z=-280]')
    s.r('summon raft:crab -258 100 -283 {Variant:"red"}', 'summon raft:crab -261 100 -285 {Variant:"blue"}', 'summon raft:crab -256 100 -286 {Variant:"sand"}')
    s.add('pose -259 100 -277.5 180 24', 'wait 10')
    s.rec('c_crab', 75, 15)
    s.cmd('gamemode survival @p', 'effect give @p minecraft:resistance infinite 4 true')
    s.rec('c_crab_dig', 75, 15, at=[(4, 'press sprint'), (5, 'press forward'), (28, 'release forward'), (29, 'release sprint')])
    s.add('cmd gamemode creative @p')
    s.r('kill @e[type=raft:crab,distance=..40,x=-259,y=100,z=-280]')
    s.add('cmd execute in raft:raftdim run tp @p -402 112 -366.5 180 18', 'fly on', 'settle 60')
    s.r('fill -409 100 -379 -395 106 -365 minecraft:air', 'fill -409 99 -379 -395 99 -365 raft:black_sand', 'fill -409 98 -379 -395 98 -365 minecraft:basalt',
        'setblock -405 99 -376 raft:pumice', 'setblock -398 99 -377 raft:volcanic_ash', 'setblock -400 100 -378 minecraft:basalt[axis=y]')
    s.add('cmd execute in raft:raftdim run tp @p -402 100 -366.5 180 22', 'wait 10')
    s.r('summon raft:ember_crab -401 100 -372 {NoAI:1b,PersistenceRequired:1b,Silent:1b,Rotation:[60f,0f]}')
    s.add('pose -402 100 -366.5 178 24', 'wait 4', 'still c_p_ember 1.25')
    s.r('kill @e[type=raft:ember_crab,distance=..30,x=-402,y=100,z=-370]')
    s.r('summon raft:ember_crab -401 100 -373', 'summon raft:ember_crab -404 100 -375', 'summon raft:ember_crab -398 100 -375')
    s.cmd('gamemode survival @p', 'effect give @p minecraft:resistance infinite 4 true', 'effect give @p minecraft:fire_resistance infinite 0 true')
    s.add('pose -402 100 -366.5 180 22', 'wait 5')
    s.rec('c_ember', 90, 15)
    s.add('cmd gamemode creative @p', 'cmd effect clear @p')
    s.r('kill @e[type=raft:ember_crab,distance=..40,x=-402,y=100,z=-370]')
    return s


def r17():
    """Story pick-ups: the four sigils going into the Tidewarden altar, seen first person with the hotbar (each gem lights
    up), then the forged key."""
    s = Script(deadline=10.0)
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.add('gamma 0.6')
    s.effects('night_vision')
    s.add('cmd execute in raft:raftdim run tp @p -316 112 -284 180 20', 'fly on', 'settle 60')
    s.cmd('item replace entity @p hotbar.0 with raft:coral_sigil', 'item replace entity @p hotbar.1 with raft:pearl_sigil',
          'item replace entity @p hotbar.2 with raft:storm_sigil', 'item replace entity @p hotbar.3 with raft:ember_sigil')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 3', 'nearblock raft:tidewarden_altar 70 3 0 3', 'fly on', 'wait 10',
          'faceblock raft:tidewarden_altar 70', 'cmd execute as @p at @p run tp @p ~ ~ ~ ~24 ~', 'wait 3', 'still s_altar_side 1.25')
    s.add('third off', 'hud on', 'nearblock raft:tidewarden_altar 70 0 0 2.6', 'fly on', 'wait 5', 'faceblock raft:tidewarden_altar 70')
    at = []
    for k in range(4):
        f0 = 4 + k * 22
        at += [(f0, f'slot {k + 1}'), (f0 + 2, 'faceblock raft:tidewarden_altar 8'), (f0 + 4, 'use')]
    s.rec('s_altar', 112, 15, at=at)
    s.add('hud off', 'third on', 'cmd attribute @p minecraft:camera_distance base set 3', 'nearblock raft:tidewarden_altar 70 3 0 3', 'fly on', 'wait 5',
          'faceblock raft:tidewarden_altar 70', 'cmd execute as @p at @p run tp @p ~ ~ ~ ~24 ~', 'wait 3', 'still s_altar_after 1.25')
    s.add('find raft:tidewarden_altar 20')
    # --- the Tide Seal opened with the key, from close by (within reach)
    s.gear('dive').effects('night_vision', 'conduit_power')
    s.hands('raft:tidewarden_key')
    s.add('cmd execute in raft:raftdim run tp @p -496.5 69 -300.2 180 4', 'settle 60', 'fly on', 'third on', 'cmd attribute @p minecraft:camera_distance base set 4',
          'pose -496.5 69 -300.2 180 4', 'wait 5')
    s.rec('s_seal', 75, 15, at=[(10, 'faceblock raft:tide_seal 5'), (12, 'use'), (16, 'pose -496.5 69 -300.2 180 4')])
    s.add('still s_seal_open 1.25')
    return s


def r18():
    """The Leviathan fight again, calmer: the player stands still on the stone ring (pinned every frame, so the lunge and
    the whirlpool cannot throw the camera into a wall), wide third-person view over the pool (fov 90): the dome, the
    wake, circling, brine bolts, lunge and stranding, roar with tidelings, whirlpool, death; then the Heart of the Tide
    in the pool, the trophy and the almanac page."""
    s = Script(deadline=17.0)
    s.cmd('clear @p').mode('creative').gear('dive').hands()
    s.add('gamma 0.6')
    s.effects('night_vision', 'water_breathing', 'regeneration', 'saturation', 'fire_resistance')
    s.cmd('effect give @p minecraft:resistance infinite 4 true')
    P = (-494.5, 69, -316.5)
    pin = f'{P[0]},{P[1] + 0.001},{P[2]},180,6'
    s.add(f'cmd execute in raft:raftdim run tp @p {P[0]} {P[1]} {P[2]} 180 -10', 'settle 60', 'fly on')
    s.add('cmd execute as @p at @p run kill @e[type=raft:leviathan,distance=..80]', 'cmd execute as @p at @p run kill @e[type=raft:tideling,distance=..80]',
          'cmd execute as @p at @p run kill @e[type=minecraft:item,distance=..80]')
    s.add('fov 90', 'third on', 'cmd attribute @p minecraft:camera_distance base set 7', f'pose {P[0]} {P[1]} {P[2]} 180 -10', 'wait 10',
          'still s_dome 1.25')
    # wake (creative: the altar does not ask for an ancient crystal again), then survival so that it fights. The wake clip
    # is not pinned (the use needs the crosshair on the altar); the pose at frame 12 turns back to the pool.
    s.hands('raft:tidewarden_key')
    s.add(f'pose {P[0]} {P[1]} {P[2]} 180 6', 'wait 3')
    s.rec('s_wake', 120, 15, at=[(6, 'faceblock raft:leviathan_altar 6'), (8, 'use'), (10, 'cmd gamemode survival @p'),
                                  (11, 'cmd effect give @p minecraft:resistance infinite 4 true'), (12, f'pose {P[0]} {P[1]} {P[2]} 180 6')])
    s.add('cmd execute unless entity @e[type=raft:leviathan] in raft:raftdim run summon raft:leviathan -496.5 65 -326.5',
          'cmd gamemode survival @p')
    s.hands('raft:tidebreaker')
    for name, frames, extra in (('s_fight1', 165, None), ('s_fight2', 165, None),
                                ('s_roar', 150, 'cmd data merge entity @e[type=raft:leviathan,limit=1] {Health:280f}'),
                                ('s_whirl', 150, None),
                                ('s_death', 105, 'cmd data merge entity @e[type=raft:leviathan,limit=1] {Health:100f}')):
        if extra:
            s.add(extra)
        s.add(f'pose {P[0]} {P[1]} {P[2]} 180 6')
        at = [(12, 'cmd damage @e[type=raft:leviathan,limit=1] 2000 minecraft:generic_kill by @p')] if name == 's_death' else None
        s.rec(name, frames, 15, at=at, to=pin, ease=0)
    s.add('wait 40', 'cmd gamemode creative @p', 'cmd execute as @p at @p run kill @e[type=raft:tideling,distance=..80]')
    s.add('lookat minecraft:item', 'cmd execute as @p at @p run tp @p ~ ~ ~ ~-14 ~', 'wait 3', 'still s_drops 1.25')
    # the rewards: the Heart of the Tide in the pool, the trophy on the ring
    s.r('setblock -497 66 -327 raft:heart_of_the_tide[waterlogged=true]', 'setblock -492 69 -314 raft:leviathan_trophy[facing=south]')
    s.add('fov 70')
    s.view('s_heart', -494.5, 69, -318.5, -497, 66.5, -326.5, dist=4, settle=10, yaw_off=-14)
    s.view('s_trophy', -490.5, 69, -310.5, -491.5, 69.5, -313.5, dist=3, settle=10, yaw_off=-18)
    s.hands('raft:tidebreaker')
    s.view('s_tidebreaker', -494.5, 69, -316.5, -497, 68, -327, dist=3.5, settle=10, yaw_off=22, pitch_off=-4)
    # the almanac page of the Leviathan (looking up, so the use does not hit a block)
    s.hands('raft:seafarers_almanac[custom_data={almanac:"leviathan"}]')
    s.add('third off', 'hud on', f'pose {P[0]} {P[1]} {P[2]} 180 -75', 'wait 3', 'use', 'wait 8 render', 'shot s_almanac_lev', 'esc', 'hud off')
    return s


def r19():
    """r15 (Beach Craft 2 tools on the deck) and r17 (altar first person, seal from close by) in one run."""
    a, b = r15(), r17()
    a.L = [l if not l.startswith('deadline') else 'deadline 19.0' for l in a.L] + b.L[12:]
    return a


def r20():
    """Last run: r17 (the four sigils into the Tidewarden altar first person, the seal opened from close by), retakes of
    r11 on the same deck (raft menu by the inventory key while riding, the battery, compressor and purifier screens from
    within reach, the cannon from the side and fired first person, the wind turbine from the deck, a seat and the
    hammock at night, the radio), diving in the clear water of the coral shallows (gauge, harpoon gun, sea scooter), and
    three Beach Craft 2 tools from r15 (plastic hook, titanium armour, message in a bottle)."""
    s = r17()
    s.L = [l if not l.startswith('deadline') else 'deadline 18.5' for l in s.L]
    s.cmd('clear @p').mode('creative').gear('none').hands()
    s.effects()
    s.add('cmd execute in raft:raftdim run tp @p 140.5 101 146.5 0 20', 'fly on', 'settle 60')
    s.add('cmd execute as @p at @p run kill @e[type=raft:expedition_raft,distance=..60]')
    # radio first (fresh state), chat visible
    s.add('third off', 'hud on', 'chat on', 'cmd execute in raft:raftdim run tp @p 140.5 100 140.2 180 30', 'wait 10',
          'faceblock raft:expedition_radio 4', 'wait 2', 'use', 'wait 20 render', 'shot f_radio', 'chat off', 'hud off')
    # the raft menu: ride the raft, press the inventory key
    s.r('summon raft:expedition_raft 140.5 99.6 152.5 {Upgrades:27,Rotation:[0f,0f],Items:[{Slot:0b,id:"raft:plastic",count:24},'
        '{Slot:1b,id:"raft:driftwood_planks",count:32},{Slot:2b,id:"raft:rope",count:8},{Slot:3b,id:"raft:fresh_water",count:3},'
        '{Slot:4b,id:"minecraft:cooked_cod",count:6},{Slot:54b,id:"minecraft:coal",count:32}]}')
    s.add('wait 5', 'cmd ride @p mount @e[type=raft:expedition_raft,limit=1,sort=nearest]', 'wait 5', 'third off', 'key inventory', 'wait 8 render',
          'shot f_raft_menu', 'esc', 'wait 2', 'cmd ride @p dismount', 'cmd execute as @p at @p run kill @e[type=raft:expedition_raft,distance=..60]')
    # the energy screens from within reach
    s.chest('f_battery', 136, 104, 145)
    s.chest('f_compressor', 138, 100, 138)
    s.chest('f_purifier', 136, 100, 141, gui_wait=30)
    # the cannon: from the side, then fired first person
    s.hands('raft:cannonball 16')
    s.view('f_cannon_still', 144.5, 100, 138.5, 142.5, 100.5, 136.5, dist=3.5, settle=10, yaw_off=-32)
    s.add('third off', 'cmd execute in raft:raftdim run tp @p 142.5 100 138.6 180 25', 'wait 5', 'faceblock raft:ship_cannon 4')
    s.rec('f_cannon_fp', 50, 15, at=[(8, 'use'), (32, 'use')])
    # the wind turbine (135 104 145) from the deck, the rotor turning
    s.hands()
    s.view('f_turbine_still', 143.5, 100, 145.5, 135.5, 104.5, 145.5, dist=4, settle=10, yaw_off=14, pitch_off=6)
    s.rec('f_turbine', 45, 15, to='143.5,100.001,145.5,~,~', ease=0)
    # a deck chair (141 100 143, facing south), seen from the front
    s.add('third off', 'cmd execute in raft:raftdim run tp @p 141.5 100 141.5 180 30', 'wait 5', 'faceblock raft:deck_chair 4', 'use', 'wait 10',
          'face 141.5 101.4 150', 'cmd attribute @p minecraft:camera_distance base set 3', 'third front', 'wait 3', 'still f_sit 1.25', 'third on')
    s.add('cmd ride @p dismount', 'wait 3')
    # the hammock at night (143..144 100 144): lie down
    s.effects('night_vision')
    s.add('cmd time set 18000', 'cmd execute in raft:raftdim run tp @p 143.5 100 142.5 0 30', 'wait 5', 'third off', 'faceblock raft:hammock 4', 'use', 'wait 25',
          'third on', 'cmd attribute @p minecraft:camera_distance base set 4', 'wait 3', 'still f_hammock 1.25', 'cmd time set 6000', 'wait 5')
    s.effects()
    # diving in the clear water of the coral shallows (stage 54..74 / 85..98 / -46..-24 from r16)
    s.gear('dive')
    s.cmd('gamemode survival @p', 'effect give @p minecraft:resistance infinite 4 true')
    s.add('cmd execute in raft:raftdim run tp @p 64.5 90 -26.5 180 8', 'settle 40', 'wait 40', 'hud on', 'third off', 'still f_dive_gauge 1.0', 'hud off')
    s.add('third on', 'cmd attribute @p minecraft:camera_distance base set 4', 'pose 64.5 90 -26.5 160 10', 'wait 3', 'still f_dive 1.25')
    s.cmd('item replace entity @p hotbar.0 with raft:harpoon_gun', 'item replace entity @p hotbar.1 with raft:harpoon 16')
    s.add('slot 1', 'pose 64.5 90 -26.5 180 4', 'cmd execute in raft:raftdim run summon minecraft:cod 64.5 91.2 -34.5 {NoAI:1b}', 'wait 3')
    s.rec('f_harpoon', 45, 15, at=[(6, 'use'), (26, 'use')])
    s.cmd('item replace entity @p hotbar.0 with raft:sea_scooter')
    s.add('slot 1', 'cmd execute in raft:raftdim run tp @p 64.5 90 -24.5 180 2', 'wait 5')
    s.rec('f_scooter', 75, 15, at=[(3, 'press use'), (70, 'release use')])
    s.add('cmd gamemode creative @p', 'cmd effect clear @p', 'cmd clear @p')
    # Beach Craft 2: the plastic hook pulling debris in, titanium armour, a message in a bottle
    b = r15()
    body = b.L[12:]
    cut = next(i for i, l in enumerate(body) if l.startswith('cmd item replace entity @p weapon.mainhand with raft:supply_barrel'))
    tit = next(i for i, l in enumerate(body) if 'titanium_helmet' in l)
    end = next(i for i, l in enumerate(body) if l.startswith('still f_titanium_front'))
    s.L += body[:cut] + body[tit:end + 1] + ['third on']
    s.gear('none')
    return s


RUNS = {'r20': r20, 'r18': r18, 'r19': r19, 'r17': r17, 'r16': r16, 'r15': r15, 'r14': r14, 'r13': r13, 'r12': r12, 'r11': r11, 'r08': r08, 'r10': r10, 'r07': r07, 'r06': r06, 'r03': r03, 'r04': r04, 'r05': r05, 'r09': r09}

if __name__ == '__main__':
    n = RUNS[sys.argv[1]]().write(sys.argv[2])
    print(sys.argv[2], n, 'lines')
