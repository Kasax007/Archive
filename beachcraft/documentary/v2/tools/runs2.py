"""Aufnahme-Laeufe der Doku v2 (Welt bcdoc2, Seed beachcraft: Gelaende und die meisten Orte wie in v1, Koordinaten aus
tools/runs.py; Orte, die 3.0.1 verschoben hat, sucht scout). Aufruf: python3 runs2.py <lauf> <skript.txt>"""
import sys

from film2 import S2, v, EYE


def time_lapse(s, name, frames, t0, step):
    s.cmd(f'time set {t0}')
    return s.rec(name, frames, 30, at=[(i, f'cmd time add {step}') for i in range(frames)])


def run_a():
    """Um den Spawn: Sonnenaufgang, Saltmere, Bojenfeld, Korallen-Flachwasser, Kelpwald, Fischerboot, Eisschollen,
    Eisberg-Station, Bohrinsel, offene See mit Hai und Floss, Hammerhai, Wal, Saltmere bei Nacht."""
    s = S2(deadline=300)
    # sunrise over Saltmere (the sun rises in the east, +x)
    s.go(110, 112, 30, 260, 112, -10, settle=600)
    time_lapse(s, 'o_dawn', 150, 22900, 10)
    s.cmd('time set 6000')
    # Saltmere: aerial, along the plaza to the shrine, the two story chests
    s.orb('p_saltmere_air', 7, (168, 100, -15), 80, 145, 50, start=135)
    s.dolly('p_saltmere_deck', 6, (172, 105.2, 14), (172, 105.2, -12), (172, 104, -36))
    s.dolly('p_saltmere_shrine', 5, (180, 105, -22), (174, 104.6, -30), (172, 103.5, -39), settle=60)
    s.loot('story/saltmere_elder', 60, 's_saltmere_elder')
    s.loot('story/saltmere_shrine', 60, 's_saltmere_shrine')
    # buoy field
    s.orb('p_buoy', 6, (106, 99, 10), 24, 106, 40, start=200)
    s.cmd('gamemode creative @p')
    s.add('cmd execute in raft:raftdim run tp @p 105.5 101 14.5', 'wait 10', 'openbe 105 99 12', 'wait 8 render', 'shot p_buoy_crate', 'esc')
    s.cmd('gamemode spectator @p')
    # coral shallows under water: reef, mantas, jellyfish, moray
    s.fx('night_vision')
    s.add('height 64 -32')
    s.go(52, v('hy', 5), -44, 76, v('hy', 1), -20, settle=300)
    s.clip('b_coral', 6, to=f"70,{v('hy', 4.5 - EYE)},-26", look=f"84,{v('hy', 1)},-12")
    s.summon('raft:manta_ray', 3, spread=5, ahead=9, dy=1)
    s.add('wait 30')
    s.clip('c_manta', 6, look='raft:manta_ray', smooth=0.06)
    s.kill('raft:manta_ray')
    s.summon('raft:jellyfish', 3, spread=3, ahead=6, nbt='{Variant:"moon"}')
    s.summon('raft:jellyfish', 2, spread=3, ahead=8, dy=2, nbt='{Variant:"crimson"}')
    s.add('wait 10')
    s.clip('c_jelly', 5, by='0,0,0,-12,0')
    s.kill('raft:jellyfish')
    s.add('find raft:giant_clam 40')
    s.go(v('fx', 2.2), v('fy', 1.6 + EYE), v('fz', 2.2), v('fx'), v('fy', 0.4), v('fz'), settle=40)
    s.clip('b_clam', 5, to=f"{v('fx', 1.4)},{v('fy', 1.2)},{v('fz', 1.4)}", look=f"{v('fx')},{v('fy', 0.4)},{v('fz')}")
    s.add('find raft:sea_urchin 40')
    s.go(v('fx', 1.8), v('fy', 1.2 + EYE), v('fz', 1.8), v('fx'), v('fy', 0.3), v('fz'), settle=40)
    s.add('still b_urchin 1.25')
    s.add('find raft:bubble_vent 64')
    s.go(v('fx', 6), v('fy', 3 + EYE), v('fz', 6), v('fx'), v('fy', 6), v('fz'), settle=40)
    s.clip('b_vent', 5, to=f"{v('fx', 5)},{v('fy', 9)},{v('fz', 5)}", look=f"{v('fx')},{v('fy', 9)},{v('fz')}")
    # kelp forest: rise through the kelp, then sea otters at the surface
    s.add('height 4 4')
    s.go(4, v('hy', 2.5), 4, 24, v('hy', 8), 14, settle=300)
    s.clip('b_kelp', 6, to=f"8,{v('hy', 14 - EYE)},6", look=f"26,{v('hy', 14)},16")
    s.fx()
    s.go(2, 101.4, 2, 2, 99.6, 10, settle=60)
    s.summon('raft:sea_otter', 3, spread=2.5, ahead=6, dy=-1.8)
    s.add('wait 60')
    s.clip('c_otter', 6, look='raft:sea_otter', smooth=0.06)
    s.kill('raft:sea_otter')
    # fishing boat wreck (sloop 16..35 / 52..59 / 48..69)
    s.fx('night_vision')
    s.orb('p_fishing', 6, (25, 55, 58), 17, 62, 45, start=200)
    s.loot('fishing', 40, 'p_fishing_chest')
    s.fx()
    # frost floes, penguins, iceberg outpost (scouted: the iceberg is new)
    s.orb('b_floes', 7, (-96, 100, 96), 45, 128, 40, start=60)
    s.add('height -90 90')
    s.go(-88, v('hy', 2.2), 86, -92, v('hy', 0.5), 94, settle=60)
    s.summon('raft:penguin', 4, spread=2, ahead=4, dy=0.5)
    s.add('wait 40')
    s.clip('c_penguin', 6, look='raft:penguin', smooth=0.06)
    s.kill('raft:penguin')
    s.add('scout raft:iceberg_outpost')
    s.orbit('p_iceberg_air', 7, 42, 10, 45, start=135, look_dy=-2)
    s.flyin('p_iceberg_hut', 6, 26, 10, 3, 1.5, ang=200, look_dy=-1)
    s.loot('iceberg_outpost', 60, 'p_iceberg_chest')
    # rusted rig (212..256 / 20..144 / 128..175)
    s.orb('p_rig_air', 7, (234, 115, 152), 75, 138, 45, start=300)
    s.dolly('p_rig_deck', 5, (244, 118, 160), (238, 118, 148), (232, 117, 132), settle=60)
    s.loot('rig', 60, 'p_rig_chest')
    # open sea: low over the water, then Bruce circling a raft with a player on it (camera high above)
    s.dolly('b_ocean', 6, (120, 104, 120), (175, 103, 175), (240, 100, 240), settle=300)
    s.r('fill 157 99 157 163 99 163 raft:raft_foundation', 'fill 157 100 157 163 104 163 air')
    s.add('cmd execute in raft:raftdim run tp @p 160.5 100 160.5 30 40')
    s.actor('survival')
    s.cmd('effect give @p minecraft:resistance infinite 4 true')
    s.add('pcmd summon raft:shark ^6 ^-3 ^10 {PersistenceRequired:1b}', 'wait 300')
    s.clip('c_shark', 7, cam='150,116,174,-150,45', look='raft:shark', smooth=0.08)
    s.kill('raft:shark')
    s.spec()
    s.fx('night_vision')
    s.go(175, 90, 175, 175, 89, 190, settle=40)
    s.add('pcmd summon raft:hammerhead_shark ^2 ^ ^10 {PersistenceRequired:1b}', 'wait 20')
    s.clip('c_hammer', 6, look='raft:hammerhead_shark', smooth=0.06)
    s.kill('raft:hammerhead_shark')
    s.fx()
    s.go(150, 101.5, 150, 160, 99, 165, settle=40)
    s.add('pcmd summon raft:whale ^ ^-4 ^14 {PersistenceRequired:1b}', 'wait 200')
    s.clip('c_whale', 8, look='raft:whale', chase='16,4', smooth=0.05)
    s.kill('raft:whale', 120)
    # Saltmere at night: the lights
    s.cmd('time set 18000')
    s.orb('b_night', 7, (168, 103, -15), 34, 112, 35, start=160, settle=60)
    s.cmd('time set 6000')
    return s


def flower(s, name, block, r=64, secs=4.0, ang=135.0, clip=False):
    """close-up of the nearest such plant: a still (slow zoom in the edit), or a push-in clip"""
    s.add(f'find {block} {r}')
    if clip:
        return s.push(name, secs, ('fx', 'fy', 'fz'), 3.0, 1.5, dy=-0.75, ang=ang, look_dy=0.45, settle=60)
    import math
    a = math.radians(ang)
    s.go(v('fx', math.sin(a) * 1.9), v('fy', 0.9), v('fz', -math.cos(a) * 1.9), v('fx'), v('fy', 0.45), v('fz'), settle=60)
    return s.add(f'still {name} 1.25')


def run_b():
    """Osten (erster Lauf: legt die Welt bcdoc2 an): Leuchtturm (scout), Strandbar (scout) mit Blumen der Palmeninsel,
    Dschungelinsel (352 96), Graben (448 0) mit Anglerfisch, Piratenbucht und Leuchtlagune (Nacht), Mangroveninsel."""
    s = S2(deadline=300, new=True)
    # old lighthouse: aerial, the approach from the sea, the dock, the lantern room, the keeper's cottage + chest
    s.add('scout raft:old_lighthouse')
    s.orbit('p_lighthouse_air', 7, 62, 14, 50, start=150, look_dy=-6)
    s.flyin('s_lighthouse_way', 7, 130, 55, -32, -28, ang=200, look_dy=-12)
    s.flyin('p_lighthouse_dock', 5, 60, 38, -36, -36, ang=110, look_dy=-16)
    s.add('find raft:lighthouse_lens 90')
    s.push('p_lighthouse_lens', 5, ('fx', 'fy', 'fz'), 4.2, 2.4, dy=-0.9, ang=200, look_dy=0.5, settle=60)
    s.add('openloot story/lighthouse 120 peek')
    s.push('s_lighthouse_in', 5, ('ox', 'oy', 'oz'), 4.0, 2.2, dy=0.0, ang=180, look_dy=0.4, settle=60)
    s.loot('story/lighthouse', 120, 's_lighthouse')
    # beach shack and the flowers of the palm isle around it
    s.add('scout raft:beach_shack')
    s.orbit('p_shack', 7, 26, 7, 50, start=200, look_dy=-2)
    s.loot('beach_shack', 60, 'p_shack_crate')
    s.orbit('b_palm_air', 8, 80, 40, 35, start=60, look_dy=-6)
    s.add(f"cmd execute in raft:raftdim run tp @p {v('cx')} {v('y1', 4)} {v('cz')}")
    for name, block in (('b_hibiscus', 'raft:hibiscus'), ('b_plumeria', 'raft:plumeria'), ('b_glory', 'raft:beach_morning_glory'),
                        ('b_aloe', 'raft:aloe_vera'), ('b_seaoats', 'raft:sea_oats'), ('b_shells', 'raft:seashells')):
        flower(s, name, block)
    # jungle isle
    s.orb('b_jungle_air', 8, (352, 112, 96), 75, 168, 40, start=210)
    s.add('cmd execute in raft:raftdim run tp @p 352 150 96')
    for name, block in (('b_orchid', 'raft:tropical_orchid'), ('b_heliconia', 'raft:heliconia'), ('b_bird', 'raft:bird_of_paradise'),
                        ('b_pineapple', 'raft:pineapple_bush')):
        flower(s, name, block)
    # abyssal trench: the descent into the dark, the floor, an anglerfish
    s.add('height 448 0')
    s.dolly('b_trench', 8, (448, 96, 30), (448, 40, 12), (448, 10, -10), settle=420)
    s.go(448, v('hy', 3.5), 6, 448, v('hy', 2), -6, settle=120)
    s.summon('raft:anglerfish', 2, spread=3, ahead=7, dy=0.5)
    s.add('wait 30')
    s.clip('c_angler', 6, look='raft:anglerfish', smooth=0.08)
    s.kill('raft:anglerfish')
    # pirate cove (216..272 / 78..135 / 544..599)
    s.orb('p_cove_air', 8, (244, 104, 571), 80, 150, 45, start=120)
    s.loot('pirate_treasure', 80, 'p_cove_chest')
    s.loot('story/pirate_captain', 80, 's_cove_captain')
    # glowing lagoon at night, glow jellies
    s.cmd('time set 18000')
    s.add('height 256 512')
    s.fx('night_vision')
    s.go(250, v('hy', 4), 500, 262, v('hy', 2), 524, settle=420)
    s.summon('raft:jellyfish', 4, spread=3, ahead=7, dy=1, nbt='{Variant:"glow"}')
    s.add('wait 10')
    s.clip('b_lagoon', 6, to=f"254,{v('hy', 3.6 - EYE)},508", look=f"266,{v('hy', 2.5)},528")
    s.kill('raft:jellyfish')
    s.fx()
    s.cmd('time set 6000')
    # mangrove isle with spider lilies
    s.add('tpbiome raft:mangrove_isle', 'where')
    s.orb('b_mangrove', 7, (v('px'), v('py'), v('pz')), 40, v('py', 22), 40, start=45, settle=420)
    s.add(f"cmd execute in raft:raftdim run tp @p {v('px')} {v('py', 3)} {v('pz')}")
    flower(s, 'b_spiderlily', 'raft:spider_lily')
    return s


def under(s):
    s.fx('night_vision')
    return s


def run_c():
    """Suedwesten: Korallentempel (scout), Galeone mit Korsaren, Frachter, Flugzeug, Ruinen, Sanktum und Siegel,
    verlassenes Floss mit Korsaren-Kampf, Palmeninsel (-256 -288) mit Krabben und Moewen, Vulkaninsel mit
    Glutkrabben, Riesenmuschel, Helix-Station."""
    s = S2(deadline=330)
    # coral temple (new site: deep enough to stay under water)
    s.add('scout raft:coral_temple')
    under(s)
    s.orbit('p_temple_air', 8, 34, 1, 60, start=160, look_dy=-2)
    s.add('find raft:tidewarden_altar 70')
    s.push('p_temple_in', 6, ('fx', 'fy', 'fz'), 9, 4, dy=0.4, ang=180, look_dy=0.6, settle=120)
    s.go(v('cx', 6), v('cy', 2), v('cz', 14), v('cx'), v('cy'), v('cz'), settle=60)
    s.summon('raft:moray_eel', 1, ahead=5)
    s.add('wait 120')
    s.clip('c_moray', 6, look='raft:moray_eel', chase='4,0.5', smooth=0.05)
    s.kill('raft:moray_eel')
    # galleon (-371 42 -256 .. -320 71 -228) with drowned corsairs swimming
    s.clear_kelp(-385, 40, -275, -305, 80, -205)
    s.orb('p_galleon', 8, (-345, 56, -242), 32, 66, 60, start=150)
    s.loot('wreck_galleon', 60, 'p_galleon_chest')
    s.r('summon raft:drowned_corsair -336 52 -238', 'summon raft:drowned_corsair -330 50 -244', 'summon raft:drowned_corsair -342 54 -236')
    s.go(-322, 60, -222, -336, 53, -238, settle=60)
    s.clip('c_corsair', 6, look='raft:drowned_corsair', smooth=0.06)
    s.kill('raft:drowned_corsair')
    # cargo ship, sunken plane, ruins
    s.clear_kelp(-330, 50, -250, -270, 92, -170)
    s.orb('p_cargo', 8, (-308, 68, -209), 40, 84, 50, start=60)
    s.clear_kelp(-485, 50, -285, -435, 72, -235)
    s.orb('p_plane', 7, (-459, 59, -261), 19, 66, 60, start=30)
    s.clear_kelp(-505, 40, -250, -468, 60, -210)
    s.orb('p_ruins', 7, (-486, 48, -230), 15, 54, 60, start=20)
    # abyssal sanctum, its seal
    s.orb('p_sanctum', 8, (-497, 72, -318), 48, 94, 45, start=30)
    s.dolly('s_seal', 6, (-497, 72.5, -287), (-497, 72, -297), (-497, 71, -303), settle=60)
    s.fx()
    # abandoned raft; a drowned corsair climbs aboard and the player fights it (free camera beside the raft)
    s.orb('p_raft', 7, (-570, 101, -316), 15, 106, 50, start=210)
    s.add('cmd execute in raft:raftdim run tp @p -570.5 101 -316.5 90 10')
    s.actor('survival')
    s.cmd('effect give @p minecraft:resistance infinite 4 true', 'item replace entity @p weapon.mainhand with raft:cutlass')
    s.r('summon raft:drowned_corsair -574.5 101 -316.5 {PersistenceRequired:1b}')
    s.add('wait 10', 'lookat raft:drowned_corsair')
    s.clip('c_corsair_fight', 7, cam='-569,103.2,-310,155,12', look='-572,101.6,-316.5',
           at=[(k, 'lookat raft:drowned_corsair') for k in range(0, 210, 6)] + [(k + 1, 'attack') for k in range(12, 210, 14)])
    s.kill('raft:drowned_corsair')
    s.hands()
    s.spec()
    return s


def run_d():
    """Archipel von oben; Westen: Port Solace (Luft, Strassen, Tuerme, Rathaus, Tresor), versunkener Schelf, Sonnenuntergang,
    Ashen Forge (scout), Wrack-Friedhof, Schiffbruechigen-Lager (scout)."""
    s = S2(deadline=330)
    s.orb('b_archi', 9, (120, 100, 60), 150, 235, 25, start=200, settle=600)
    # Port Solace (-1103..-919 / 33..135 / 87..315), city hall -1091..-1057 / 45..123 / 183..219
    s.orb('p_solace_air', 9, (-1011, 100, 200), 125, 178, 30, start=110, settle=600)
    time_lapse(s.go(-930, 110, 150, -1074, 104, 201, settle=60), 'b_daynight', 180, 11600, 11)
    s.cmd('time set 6000')
    s.orb('p_solace_hall', 7, (-1074, 112, 201), 42, 126, 50, start=135)
    s.add('openloot story/port_solace_vault 160 peek')
    s.push('s_solace_vault_room', 5, ('ox', 'oy', 'oz'), 3.6, 2.2, dy=0.0, ang=180, look_dy=0.4, settle=60)
    s.loot('story/port_solace_vault', 160, 's_solace_vault')
    under(s)
    s.dolly('p_solace_street', 7, (-1033, 51.5, 272), (-1031, 51.5, 238), (-1033, 50, 205), settle=200)
    s.dolly('p_solace_towers', 7, (-1028, 60, 150), (-1028, 96, 152), (-1074, 90, 201), settle=60)
    s.dolly('b_shelf', 6, (-952, 54, 112), (-972, 53, 128), (-1000, 48, 150), settle=120)
    s.fx()
    # Ashen Forge (scouted: island places only stand on land now)
    s.cmd('effect give @p minecraft:fire_resistance infinite 0 true')
    s.add('scout raft:ashen_forge')
    s.orbit('p_forge_air', 8, 75, 18, 40, start=160, look_dy=-8)
    s.add('openloot story/ashen_forge 120 peek')
    s.push('p_forge_in', 6, ('ox', 'oy', 'oz'), 9, 4, dy=1.0, ang=180, look_dy=0.5, settle=60)
    s.add('openloot story/ashen_vault 120 peek')
    s.go(v('ox'), v('oy', 7 + EYE), v('oz', 9), v('ox'), v('oy', 0.5), v('oz'), settle=60)
    s.clip('p_forge_bridge', 6, to=f"{v('ox')},{v('oy', 3.5)},{v('oz', 4.5)}", look=f"{v('ox')},{v('oy', 0.5)},{v('oz')}")
    s.loot('story/ashen_vault', 120, 's_forge_vault')
    s.fx()
    # wreck graveyard (-1264, 372)
    under(s)
    s.add('height -1264 372')
    s.dolly('b_wrecks', 7, (-1248, v('hy', 10), 392), (-1260, v('hy', 8), 378), (-1276, v('hy', 4), 360), settle=420)
    s.fx()
    # castaway camp (scouted)
    s.add('scout raft:castaway_camp')
    s.orbit('p_camp', 7, 15, 5, 60, start=200, look_dy=-1)
    s.loot('castaway_camp', 40, 'p_camp_chest')
    return s


DECK = [
    'setblock 142 100 136 raft:ship_cannon[facing=north]',
    'fill 135 100 145 135 103 145 raft:steel_beam[axis=y]', 'setblock 135 104 145 raft:wind_turbine[facing=south]',
    'setblock 136 104 145 raft:makeshift_battery', 'setblock 136 103 145 raft:copper_cable',
    'setblock 138 100 138 raft:air_compressor', 'setblock 137 100 138 raft:makeshift_battery{Energy:500000L}',
    'setblock 139 100 143 raft:palm_chair[facing=south]', 'setblock 140 100 143 raft:cushion_red',
    'setblock 141 100 143 raft:deck_chair[facing=south]',
    'setblock 143 100 144 raft:hammock[facing=east,part=foot]', 'setblock 144 100 144 raft:hammock[facing=east,part=head]',
    'setblock 136 100 141 raft:water_purifier[facing=south]', 'setblock 137 100 141 raft:simple_grill[facing=south]',
    'setblock 138 100 141 raft:item_catcher',
    'fill 142 99 139 144 99 140 raft:crop_plot', 'fill 142 100 139 143 100 140 minecraft:wheat[age=7]',
    'fill 144 100 139 144 100 140 raft:pineapple_crop[age=7]',
    'setblock 145 100 139 raft:scarecrow[half=lower,facing=south]', 'setblock 145 101 139 raft:scarecrow[half=upper,facing=south]',
    'setblock 136 100 136 raft:quarry[facing=south]', 'setblock 137 100 136 raft:chunk_destroyer',
    'setblock 138 100 136 raft:brick_furnace[facing=south]', 'setblock 139 100 136 raft:titanium_furnace[facing=south]',
    'fill 136 101 136 139 101 136 raft:makeshift_solar_panel',
    'setblock 141 100 138 raft:research_terminal[facing=south]{LogId:"helix_1"}',
    'setblock 140 100 138 raft:expedition_radio[facing=south]']
LIGHTS = ['setblock 134 100 134 raft:tiki_torch[half=lower,lit=true]', 'setblock 134 101 134 raft:tiki_torch[half=upper,lit=true]',
          'setblock 146 100 134 raft:tiki_torch[half=lower,lit=true]', 'setblock 146 101 134 raft:tiki_torch[half=upper,lit=true]',
          'fill 135 100 146 145 100 146 raft:palm_fence', 'fill 135 101 146 145 101 146 raft:string_lights_warm[facing=north]',
          'setblock 140 100 145 raft:brazier[lit=true]', 'setblock 139 100 145 raft:jelly_lamp', 'setblock 141 100 145 raft:coconut_lantern',
          'setblock 137 100 145 raft:ship_lantern', 'setblock 143 100 145 raft:seashell_lamp', 'setblock 144 100 141 raft:driftwood_lamp']


def run_e():
    """Overworld (Strand mit Treibholz, Portal, Reise), Ankunftsplattform mit Kiste und Journal, Almanach, Tabs; Deck auf
    offener See (134..146 / 99): Expedition-Floss, Boote, Kanone, Windturbine, Sitze, Haengematte, Grill, Beete,
    Maschinen, Terminal, Funk; Tauchen (Anzeige, Lampe, Harpune, Scooter); Lichter bei Nacht."""
    s = S2(deadline=330)
    O = 'minecraft:overworld'
    s.add('tpbiome minecraft:beach minecraft:overworld', 'settle 400', 'find raft:driftwood_log 64')
    s.cmd('execute in minecraft:overworld run time set 6000')
    s.go(v('fx', 7), v('fy', 4), v('fz', 7), v('fx'), v('fy', 0.5), v('fz'), settle=200, dim=O)
    s.clip('w_beach', 6, orbit=f"{v('fx')},{v('fz')},50", look=f"{v('fx')},{v('fy', 0.5)},{v('fz')}")
    s.push('w_stump', 5, ('fx', 'fy', 'fz'), 4.5, 2.4, dy=-0.4, ang=200, look_dy=0.5, settle=30)
    # the portal: a frame 4 wide, 5 high, built on cleared sand south of the player; lit with the energy staff
    s.add(f"cmd execute in {O} run tp @p {v('fx', 6)} {v('fy', 1)} {v('fz', 6)} 0 5")
    s.actor('creative')
    s.add('pcmd fill ~-3 ~ ~1 ~4 ~6 ~7 minecraft:air', 'pcmd fill ~-3 ~-1 ~1 ~4 ~-1 ~7 minecraft:sand',
          'pcmd fill ~-1 ~ ~5 ~2 ~4 ~5 raft:driftwood_portal_frame', 'pcmd fill ~ ~1 ~5 ~1 ~3 ~5 minecraft:air', 'where')
    s.hands('raft:energy_staff')
    s.add('settle 60')
    s.go(v('px', 4.5), v('py', 2.8), v('pz', 2.0), v('px', 0.5), v('py', 2), v('pz', 5), settle=10, dim=O) if False else None
    s.add(f"freecam {v('px', 5)} {v('py', 3.0)} {v('pz', 1.5)} 60 12", 'wait 6 render', 'shot w_frame', 'freecam off')
    s.clip('w_light', 5, cam=f"{v('px', 5)},{v('py', 3.0)},{v('pz', 1.5)},60,12", look=f"{v('px', 0.5)},{v('py', 2.2)},{v('pz', 5)}",
           at=[(10, 'faceblock raft:driftwood_portal_frame 8'), (12, 'use')])
    # the trip (survival, first person with the HUD: the swirl)
    s.cmd('gamemode survival @p', 'effect give @p minecraft:resistance infinite 4 true',
          'execute as @p at @p run tp @p ~0.5 ~1 ~5.5 0 0')
    s.add('third off', 'hud on')
    s.clip('w_trip', 5)
    s.add('wait 60', 'hud off', 'settle 400', 'where')
    s.cmd('gamemode spectator @p')
    s.orb('w_arrive', 7, (v('px'), v('py'), v('pz')), 14, v('py', 7), 60, start=150, settle=200)
    s.orb('s_platform', 6, (v('px'), v('py'), v('pz')), 6, v('py', 3), 40, start=300, settle=20)
    s.cmd('gamemode creative @p')
    s.loot('story/castaway', 30, 's_chest', back=None)
    s.hands('raft:expedition_journal')
    s.add('hud on', 'use', 'wait 8 render', 'shot s_journal', 'esc')
    s.hands('raft:seafarers_almanac')
    s.add('use', 'wait 8 render', 'shot f_almanac', 'esc')
    s.hands('raft:seafarers_almanac[custom_data={almanac:"creatures/whale"}]')
    s.add('use', 'wait 8 render', 'shot f_almanac_page', 'esc', 'hud off')
    s.hands()
    for tab, rows, name in (('raft:bc_building', 0, 'i_tab_building'), ('raft:bc_building', 6, 'i_tab_building2'),
                            ('raft:bc_decor', 0, 'i_tab_decor'), ('raft:bc_decor', 6, 'i_tab_decor2'),
                            ('raft:bc_nature', 0, 'i_tab_nature'), ('raft:bc_voyage', 0, 'i_tab_voyage'),
                            ('raft:bc_creatures', 0, 'i_tab_creatures'), ('raft:bc_story', 0, 'i_tab_story'),
                            ('raft:raft', 0, 'i_tab_raft')):
        s.add(f'tab {tab} {rows}', 'wait 4 render', f'shot {name}', 'esc')
    # the deck on the open sea
    s.cmd('gamemode spectator @p')
    s.go(140.5, 114, 152, 140.5, 100, 140, settle=420)
    s.r('fill 134 99 134 146 99 146 raft:raft_foundation', 'fill 128 100 128 152 108 152 air',
        'kill @e[type=!minecraft:player,distance=..40,x=140,y=100,z=140]', *DECK)
    s.r('item replace block 138 100 138 container.0 with raft:oxygen_tank', 'item replace block 136 100 141 container.0 with minecraft:water_bucket',
        'item replace block 136 100 141 container.1 with minecraft:coal 4')
    s.add('cmd execute in raft:raftdim run tp @p 140.5 100 146.5 0 35')
    s.actor('creative')
    s.hands('raft:expedition_raft')
    s.add('wait 10')
    s.clip('f_raft_place', 4, cam='146,104.5,151,135,30', look='140.5,99.8,150', at=[(10, 'use')])
    s.add('cmd kill @e[type=raft:expedition_raft]', 'cmd clear @p')
    s.r('summon raft:expedition_raft 140.5 99.6 153.5 {Upgrades:27,Rotation:[0f,0f],Items:[{Slot:54b,id:"minecraft:coal",count:32}]}')
    s.add('wait 5', 'orbit_dummy') if False else None
    s.go(148, 104, 158, 140.5, 100, 153.5, settle=10)
    s.clip('f_raft_upgrades', 6, orbit='140.5,153.5,70', look='140.5,100,153.5')
    s.add('cmd execute in raft:raftdim run tp @p 140.5 100 153.5 0 10', 'wait 5', 'cmd ride @p mount @e[type=raft:expedition_raft,limit=1,sort=nearest]', 'wait 5')
    s.add('third on')
    s.clip('f_raft_sail', 8, cam='128,106,150,-120,18', look='raft:expedition_raft', chase='14,5', smooth=0.08,
           at=[(4, 'press forward'), (110, 'press left'), (140, 'release left'), (236, 'release forward')])
    s.add('cmd ride @p dismount', 'cmd kill @e[type=raft:expedition_raft]', 'cmd execute in raft:raftdim run tp @p 140.5 100 140.5 0 20', 'wait 5')
    s.r('summon raft:palm_boat 147.5 99.6 136.5 {Rotation:[90f,0f]}', 'summon raft:palm_chest_boat 147.5 99.6 139.5 {Rotation:[90f,0f]}',
        'summon raft:driftwood_raft 147.5 99.6 142.5 {Rotation:[90f,0f]}', 'summon raft:driftwood_chest_raft 147.5 99.6 145.5 {Rotation:[90f,0f]}')
    s.spec()
    s.go(153.5, 102, 139, 147.5, 99.8, 141, settle=10)
    s.add('still f_boats 1.25')
    for e in ('palm_boat', 'palm_chest_boat', 'driftwood_raft', 'driftwood_chest_raft'):
        s.cmd(f'kill @e[type=raft:{e}]')
    # cannon (fired twice), turbine, compressor and battery screens, seats, hammock
    s.add('cmd execute in raft:raftdim run tp @p 143.5 100 137.5 0 10')
    s.actor('creative')
    s.hands('raft:cannonball 16')
    s.add('wait 5', 'faceblock raft:ship_cannon 6')
    s.clip('f_cannon', 5, cam='147,102,132,40,12', look='142.5,100.6,135', at=[(8, 'faceblock raft:ship_cannon 6'), (10, 'use'),
                                                                               (80, 'faceblock raft:ship_cannon 6'), (82, 'use')])
    s.hands()
    s.spec()
    s.dolly('f_turbine', 5, (131, 103, 151), (131.5, 105, 150), (135.5, 104.5, 145.5), settle=10)
    s.cmd('gamemode creative @p')
    s.add('openbe 138 100 138', 'wait 8 render', 'shot f_compressor', 'esc')
    s.cmd('gamemode spectator @p')
    s.add('cmd execute in raft:raftdim run tp @p 141.5 100 141.5 180 20')
    s.actor('creative')
    s.add('third off', 'wait 5', 'faceblock raft:deck_chair 4', 'use', 'wait 10', 'third on',
          'freecam 141.5 101.6 147 180 12', 'wait 6 render', 'still f_seats 1.25', 'freecam off')
    s.add('cmd ride @p dismount', 'cmd execute in raft:raftdim run tp @p 143.5 100 142.5 180 30', 'wait 5', 'third off',
          'faceblock raft:hammock 4', 'use', 'wait 20', 'third on',
          'freecam 143.8 102.4 147.5 170 30', 'wait 6 render', 'still f_hammock 1.25', 'freecam off')
    s.add('cmd execute in raft:raftdim run tp @p 140.5 100 140.5 0 20', 'wait 5')
    # grill with food, crops, machines, the whole deck
    s.cmd('item replace entity @p hotbar.0 with minecraft:oak_planks 4', 'item replace entity @p hotbar.1 with minecraft:beef 1',
          'item replace entity @p hotbar.2 with raft:shark_meat 1')
    s.add('third off', 'cmd execute in raft:raftdim run tp @p 137.5 100 143.5 180 40', 'wait 3', 'faceblock raft:simple_grill 4',
          'slot 1', 'use', 'slot 2', 'use', 'slot 3', 'use', 'wait 10')
    s.spec()
    s.go(138.2, 101.5, 143.2, 137.5, 100.5, 141.5, settle=10)
    s.add('still f_grill 1.25')
    s.go(143.5, 101.8, 136.4, 143.5, 100.5, 140, settle=10)
    s.add('still f_crops 1.25')
    s.go(137.8, 102.0, 133.0, 137.8, 100.8, 136.5, settle=10)
    s.add('still f_machines 1.25')
    s.dolly('f_deck', 6, (154, 108, 154), (151, 106, 151), (140, 100, 140), settle=10)
    # terminal and radio (first person; the radio broadcast shows in the chat)
    s.cmd('gamemode creative @p')
    s.add('third off', 'hud on', 'chat on', 'cmd execute in raft:raftdim run tp @p 141.5 100 140.5 180 30', 'wait 3',
          'faceblock raft:research_terminal 4', 'use', 'wait 8 render', 'shot f_terminal', 'esc')
    s.add('cmd execute in raft:raftdim run tp @p 140.5 100 140.5 180 30', 'wait 3', 'faceblock raft:expedition_radio 4', 'use',
          'wait 30 render', 'shot f_radio', 'hud off')
    # diving: gauge (first person), the diver (free camera), lamp, harpoon, scooter
    s.gear('dive')
    s.cmd('gamemode survival @p', 'effect give @p minecraft:resistance infinite 4 true')
    s.add('cmd execute in raft:raftdim run tp @p 150.5 90 140.5 90 10', 'wait 60', 'hud on', 'third off', 'shot f_gauge', 'hud off')
    s.add('third on')
    s.clip('f_dive', 5, cam='154,91.5,136,40,10', look='150.5,91,140.5')
    s.cmd('execute in raft:raftdim run tp @p 150.5 90 140.5 90 10')
    s.cmd('item replace entity @p hotbar.0 with raft:harpoon_gun', 'item replace entity @p hotbar.1 with raft:harpoon 16')
    s.add('slot 1', 'pcmd summon minecraft:cod ^ ^ ^7 {NoAI:1b}', 'wait 3')
    s.clip('f_harpoon', 4, cam='151.5,92,135.5,60,12', look='147,90.8,140.5', at=[(8, 'use'), (60, 'use')])
    s.cmd('item replace entity @p hotbar.0 with raft:sea_scooter')
    s.add('slot 1', 'cmd execute in raft:raftdim run tp @p 150.5 90 140.5 90 0', 'wait 5')
    s.clip('f_scooter', 6, cam='155,92,137,60,10', look='150.5,90.8,140.5', chase='6,1', smooth=0.08,
           at=[(3, 'press use'), (176, 'release use')])
    s.add('cmd execute in raft:raftdim run tp @p 448 30 0 0 30', 'settle 300')
    s.cmd('execute in raft:raftdim positioned 448 0 0 positioned over ocean_floor run tp @p ~ ~3 ~ 0 25',
          'item replace entity @p armor.head with raft:diving_helmet', 'effect clear @p night_vision')
    s.add('third off', 'wait 40')
    s.clip('f_lamp', 6, at=[(70, 'cmd item replace entity @p armor.head with raft:diving_helmet[raft:diving_lamp={}]')])
    s.cmd('gamemode creative @p', 'effect clear @p', 'clear @p')
    s.gear('none')
    # the deck at night: all the lights
    s.r(*LIGHTS)
    s.cmd('time set 18000')
    s.spec()
    s.orb('f_lights', 7, (140.5, 100.5, 140.5), 13, 105, 50, start=160, settle=60)
    s.cmd('time set 6000')
    return s


def run_f():
    """Ende der Story: die vier Siegel in den Altar des Korallentempels (scout), das Gezeitensiegel, die Kuppel, der
    Leviathan (freie Kamera, Spieler kaempft auf dem Steinring), Belohnungen, Tidebreaker, letzte Journalseite."""
    s = S2(deadline=300)
    s.add('scout raft:coral_temple', 'find raft:tidewarden_altar 90')
    s.fx('night_vision', 'water_breathing')
    s.go(v('fx'), v('fy', 3), v('fz', 4), v('fx'), v('fy'), v('fz'), settle=420)
    s.add(f"cmd execute in raft:raftdim run tp @p {v('fx')} {v('fy')} {v('fz', 2.5)} 180 20")
    s.actor('creative')
    s.cmd('item replace entity @p hotbar.0 with raft:coral_sigil', 'item replace entity @p hotbar.1 with raft:pearl_sigil',
          'item replace entity @p hotbar.2 with raft:storm_sigil', 'item replace entity @p hotbar.3 with raft:ember_sigil')
    at = []
    for k in range(4):
        f0 = 6 + k * 34
        at += [(f0, f'slot {k + 1}'), (f0 + 2, 'faceblock raft:tidewarden_altar 8'), (f0 + 4, 'use')]
    s.clip('s_altar', 5.5, cam=f"{v('fx', 3.2)},{v('fy', 2.4)},{v('fz', 3.2)},135,25", look=f"{v('fx')},{v('fy', 0.8)},{v('fz', 1)}", at=at)
    s.add(f"freecam {v('fx', 2)} {v('fy', 2.2)} {v('fz', 2)} 135 30", 'wait 6 render', 'still s_altar_after 1.25', 'freecam off')
    # the Tide Seal (5x5 at -499..-495 / 69..73 / -303), opened with the key
    s.hands('raft:tidewarden_key')
    s.add('cmd execute in raft:raftdim run tp @p -496.5 69 -296.5 180 3', 'settle 420')
    s.clip('s_seal_open', 5, cam='-491.5,72.5,-293,130,15', look='-497,71,-302', at=[(10, 'faceblock raft:tide_seal 6'), (12, 'use')])
    # the dome
    s.spec()
    s.fx('night_vision', 'water_breathing')
    s.dolly('s_dome', 6, (-497, 75, -305), (-497, 74, -311), (-497, 66, -327), settle=60)
    # the Leviathan: the player stands on the stone ring, the camera is free
    s.cmd('kill @e[type=raft:leviathan]', 'kill @e[type=raft:tideling]')
    P = (-494.5, 69, -316.5)
    s.add(f'cmd execute in raft:raftdim run tp @p {P[0]} {P[1]} {P[2]} 180 6')
    s.actor('creative')
    s.fx('night_vision', 'water_breathing', 'regeneration', 'saturation', 'fire_resistance')
    s.cmd('effect give @p minecraft:resistance infinite 4 true')
    s.hands('raft:tidewarden_key')
    cam = '-484,76,-306,140,20'
    hold = [(k, f'cmd execute in raft:raftdim run tp @p {P[0]} {P[1]} {P[2]} ~ ~') for k in range(0, 300, 20)]
    s.clip('s_wake', 6, cam=cam, look='-497,66,-327', at=[(6, 'faceblock raft:leviathan_altar 6'), (8, 'use'),
                                                          (10, 'cmd gamemode survival @p'),
                                                          (11, 'cmd effect give @p minecraft:resistance infinite 4 true')])
    s.add('cmd execute unless entity @e[type=raft:leviathan] in raft:raftdim run summon raft:leviathan -496.5 65 -326.5')
    s.hands('raft:tidebreaker')
    s.clip('s_lev_wide', 6, cam='-480,80,-303,140,25', look='raft:leviathan', smooth=0.05, at=hold)
    s.clip('s_lev_circle', 6, cam=cam, look='raft:leviathan', smooth=0.05, at=hold)
    s.clip('s_lev_leap', 7, cam=cam, look='raft:leviathan', smooth=0.06, at=hold)
    s.clip('s_lev_strike', 5, cam='-490,72,-311,150,10', look='raft:leviathan', smooth=0.08,
           at=hold + [(k, 'lookat raft:leviathan') for k in range(5, 150, 10)] + [(k + 1, 'attack') for k in range(5, 150, 10)])
    s.add('cmd data merge entity @e[type=raft:leviathan,limit=1] {Health:280f}')
    s.clip('s_lev_roar', 6, cam=cam, look='raft:leviathan', smooth=0.05, at=hold)
    s.add('cmd data merge entity @e[type=raft:leviathan,limit=1] {Health:120f}')
    s.clip('s_lev_death', 5, cam=cam, look='raft:leviathan', smooth=0.05,
           at=[(12, 'cmd damage @e[type=raft:leviathan,limit=1] 2000 minecraft:generic_kill by @p')])
    s.add('wait 60', 'cmd gamemode creative @p', 'cmd kill @e[type=raft:tideling]')
    s.spec()
    s.add('lookat minecraft:item', 'wait 6 render', 'still s_rewards 1.25')
    s.r('setblock -497 66 -327 raft:heart_of_the_tide[waterlogged=true]')
    s.dolly('s_heart', 5, (-496, 71, -319), (-496.5, 69.5, -322), (-497, 66.4, -327), settle=20)
    # the Tidebreaker, big, turning slowly over the ring
    s.r('summon minecraft:item_display -494.5 70.6 -321.5 {item:{id:"raft:tidebreaker",count:1},item_display:"fixed",'
        'transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.2f,2.2f,2.2f]}}')
    s.orb('s_tidebreaker', 6, (-494.5, 70.6, -321.5), 3.4, 71.4, 120, start=20, settle=20)
    s.cmd('kill @e[type=minecraft:item_display]')
    # the last page of the journal
    s.cmd('gamemode creative @p', 'advancement grant @p everything')
    s.hands('raft:expedition_journal')
    s.add('third off', 'hud on', f'pose {P[0]} {P[1]} {P[2]} 180 -70', 'wait 5', 'use', 'wait 8 render', 'shot s_end', 'esc', 'hud off')
    return s


def c_rest(s):
    """Rest of run C (there the player fell out of the world after a height query in an unloaded chunk)."""
    # palm isle (-256 -288): crabs, one digs in when the player sprints at it; seagulls
    s.add('height -259 -281')
    s.go(-259, v('hy', 1.4), -281, -259, v('hy', 0.2), -276, settle=420)
    s.summon('raft:crab', 3, spread=1.5, ahead=4, nbt='{Variant:"red"}')
    s.add('wait 20')
    s.clip('c_crab', 5, look='raft:crab', smooth=0.08)
    s.kill('raft:crab')
    s.add(f"cmd execute in raft:raftdim run tp @p -259 {v('hy')} -281 0 10")
    s.actor('survival')
    s.cmd('effect give @p minecraft:resistance infinite 4 true')
    s.summon('raft:crab', 1, ahead=7, nbt='{Variant:"blue"}')
    s.add('wait 10')
    s.clip('c_crab_dig', 5, cam=f"-254,{v('hy', 2.6)},-275,135,18", look=f"-259,{v('hy', 0.5)},-278",
           at=[(4, 'press sprint'), (5, 'press forward'), (70, 'release forward'), (71, 'release sprint')])
    s.kill('raft:crab')
    s.spec()
    s.go(-262, v('hy', 2.5), -282, -262, v('hy', 7), -270, settle=60)
    s.summon('raft:seagull', 7, spread=4, ahead=10, dy=8)
    s.add('wait 40')
    s.clip('c_gulls', 7, look='raft:seagull', smooth=0.04)
    s.add('pcmd fill ^-2 ^-2 ^3 ^2 ^-2 ^6 minecraft:farmland[moisture=7]', 'pcmd fill ^-2 ^-1 ^3 ^2 ^-1 ^6 minecraft:wheat[age=6]',
          'wait 200')
    s.go(-262, v('hy', 2.0), -282, -262, v('hy', -1), -277, settle=30)
    s.clip('c_gull_peck', 6)
    s.kill('raft:seagull')
    for name, block in (('b_glory', 'raft:beach_morning_glory'), ('b_aloe', 'raft:aloe_vera'), ('b_hibiscus', 'raft:hibiscus'),
                        ('b_plumeria', 'raft:plumeria'), ('b_seaoats', 'raft:sea_oats'), ('b_bird', 'raft:bird_of_paradise')):
        flower(s, name, block, r=128)
    # volcanic isle and ember crabs
    s.orb('b_volcano', 8, (-400, 108, -300), 75, 152, 40, start=330)
    s.add('height -402 -372')
    s.go(-402, v('hy', 1.5), -368, -402, v('hy', 0.3), -374, settle=200)
    s.summon('raft:ember_crab', 3, spread=1.5, ahead=4)
    s.add('wait 20')
    s.clip('c_ember', 5, look='raft:ember_crab', smooth=0.08)
    s.kill('raft:ember_crab')
    # a giant clam with a pearl: the pearl is taken (first person, creative)
    under(s)
    s.add('height -295 -265')
    s.go(-295, v('hy', 1.8), -262, -295, v('hy', 0.2), -265, settle=200)
    s.r(f"setblock -295 {v('hy')} -265 raft:giant_clam[facing=south,open=true,pearl=true,waterlogged=true]")
    s.cmd('gamemode creative @p')
    s.add('wait 10', 'faceblock raft:giant_clam 8')
    s.clip('b_clam_open', 4, at=[(40, 'faceblock raft:giant_clam 8'), (41, 'use')])
    s.spec()
    # Helix Research Station (-408 51 -37 .. -352 67 16)
    s.clear_kelp(-420, 48, -50, -330, 80, 40)
    s.orb('p_helix_air', 8, (-380, 59, -10), 42, 72, 50, start=60)
    s.add('openloot story/helix_lab 90 peek')
    s.push('p_helix_in', 5, ('ox', 'oy', 'oz'), 5, 2.5, dy=0.0, ang=180, look_dy=0.6, settle=60)
    s.loot('story/helix_lab', 90, 's_helix_lab')
    s.loot('story/helix_vault', 90, 's_helix_vault')
    s.cmd('gamemode creative @p')
    s.add('hud on', 'faceblock raft:research_terminal 8', 'use', 'wait 8 render', 'shot s_helix_terminal', 'esc', 'hud off')
    s.spec()
    s.fx()
    return s


def run_g():
    """Nachholen: Kisten-Bildschirme aus A und B (dort noch als Zuschauer, der keine Kisten oeffnen kann), Blumen der
    Dschungel- und Mangroveninseln in neu erzeugtem Gelaende (mit der neuen Blumen-Verteilung)."""
    s = S2(deadline=200)
    s.go(172, 112, 10, 172, 104, -15, settle=300)
    s.loot('story/saltmere_elder', 80, 's_saltmere_elder')
    s.loot('story/saltmere_shrine', 80, 's_saltmere_shrine')
    s.cmd('gamemode creative @p')
    s.add('cmd execute in raft:raftdim run tp @p 105.5 101 14.5', 'wait 10', 'openbe 105 99 12', 'wait 8 render', 'shot p_buoy_crate', 'esc')
    s.add('cmd execute in raft:raftdim run tp @p 25 62 58', 'settle 200')
    s.loot('wreck_fishing', 60, 'p_fishing_chest')
    s.add('cmd execute in raft:raftdim run tp @p 234 125 152', 'settle 200')
    s.loot('rusted_rig', 80, 'p_rig_chest')
    s.add('scout raft:iceberg_outpost', f"cmd execute in raft:raftdim run tp @p {v('cx')} {v('y1', 3)} {v('cz')}", 'settle 200')
    s.loot('iceberg_outpost', 60, 'p_iceberg_chest')
    s.add('scout raft:old_lighthouse', f"cmd execute in raft:raftdim run tp @p {v('cx')} {v('y1', 3)} {v('cz')}", 'settle 200')
    s.loot('story/lighthouse', 120, 's_lighthouse')
    s.add('scout raft:beach_shack', f"cmd execute in raft:raftdim run tp @p {v('cx')} {v('y1', 3)} {v('cz')}", 'settle 200')
    s.loot('beach_shack', 60, 'p_shack_crate')
    s.add('cmd execute in raft:raftdim run tp @p 244 110 571', 'settle 200')
    s.loot('pirate_treasure', 80, 'p_cove_chest')
    s.loot('story/pirate_captain', 80, 's_cove_captain')
    # the coral temple from under water (its box reaches the surface only with the kelp growing on it)
    s.add('scout raft:coral_temple')
    under(s)
    s.orb('p_temple_air', 6, (v('cx'), v('y0', 11), v('cz')), 30, v('y0', 19), 55, start=160, settle=300)
    s.fx()
    # penguins on a natural ice floe of the frost floes
    s.add('cmd execute in raft:raftdim run tp @p -96 105 96', 'settle 200', 'find minecraft:snow_block 48')
    s.go(v('fx', 5), v('fy', 3.2), v('fz', 5), v('fx'), v('fy', 1), v('fz'), settle=60)
    s.r(*(f"summon raft:penguin {v('fx', dx)} {v('fy', 1)} {v('fz', dz)}" for dx, dz in ((0, 0), (1, -1), (-1, 1), (1, 1))))
    s.add('wait 40')
    s.clip('c_penguin', 5, look='raft:penguin', smooth=0.06)
    s.kill('raft:penguin')
    # jungle and mangrove flowers in new terrain (far from everything filmed so far)
    s.add('cmd execute in raft:raftdim run tp @p 2400 160 -2400', 'tpbiome raft:jungle_isle', 'where', 'settle 300')
    for name, block in (('b_orchid', 'raft:tropical_orchid'), ('b_heliconia', 'raft:heliconia'), ('b_pineapple', 'raft:pineapple_bush')):
        flower(s, name, block, r=128)
    s.add('tpbiome raft:mangrove_isle', 'where', 'settle 300')
    flower(s, 'b_spiderlily', 'raft:spider_lily', r=128)
    c_rest(s)
    return s


RUNS = {'a': run_a, 'b': run_b, 'c': run_c, 'd': run_d, 'e': run_e, 'f': run_f, 'g': run_g}

if __name__ == '__main__':
    n = RUNS[sys.argv[1]]().write(sys.argv[2])
    print(sys.argv[1], n, 'lines')
