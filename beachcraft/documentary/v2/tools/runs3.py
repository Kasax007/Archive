"""Retakes after the user's feedback on the v2 cut (6.11.): manta rays with their new voice, a moray eel in its hole
lunging at a diver, a crab digging itself in seen from close by, the seagull flock in formation and gulls pecking
at a wheat field. World bcdoc2, shaders, mod with the 6.11. changes (seagull flock flight, eel, crab, sounds).

Usage: python3 runs3.py <prefix>  ->  <prefix>1.txt (coral shallows), <prefix>2.txt (palm isle)
"""
import sys

from film2 import S2, v


def ruin_with_hole(s, x, z):
    """A broken ruin wall on a sandy patch of the reef floor, with one hole facing north (-z): a moray's home.
    The floor is at hy-1 (height x z sets hy), the hole at (x, hy+1, z)."""
    H = lambda d=0: '{hy%+d:i}' % d if d else '{hy:i}'
    s.r(f'fill {x - 6} {H(-3)} {z - 7} {x + 6} {H(-1)} {z + 5} minecraft:sand',
        f'fill {x - 6} {H()} {z - 7} {x + 6} {H(4)} {z + 5} minecraft:water',
        f'fill {x - 3} {H()} {z} {x + 3} {H(2)} {z + 1} minecraft:mossy_stone_bricks',
        f'fill {x - 2} {H(3)} {z} {x + 1} {H(3)} {z + 1} minecraft:mossy_stone_bricks',
        f'setblock {x - 3} {H(2)} {z} minecraft:water',
        f'setblock {x + 3} {H(2)} {z} minecraft:water',
        f'setblock {x + 2} {H(1)} {z} minecraft:cracked_stone_bricks',
        f'setblock {x - 2} {H()} {z} minecraft:chiseled_stone_bricks',
        f'setblock {x + 1} {H(3)} {z} minecraft:cracked_stone_bricks',
        f'setblock {x - 4} {H()} {z + 1} minecraft:mossy_cobblestone',
        f'setblock {x + 4} {H()} {z} minecraft:mossy_cobblestone_slab[type=bottom,waterlogged=true]',
        f'setblock {x} {H(1)} {z} minecraft:water',
        f'setblock {x - 5} {H()} {z - 3} minecraft:tall_seagrass[half=lower]',
        f'setblock {x - 5} {H(1)} {z - 3} minecraft:tall_seagrass[half=upper]',
        f'setblock {x + 5} {H()} {z - 2} minecraft:seagrass',
        f'setblock {x + 3} {H()} {z - 4} minecraft:seagrass',
        f'setblock {x - 2} {H()} {z - 5} minecraft:brain_coral',
        f'setblock {x + 4} {H()} {z + 3} minecraft:tube_coral_fan',
        f'setblock {x - 4} {H()} {z - 1} minecraft:sea_pickle[pickles=3]')
    return s


def run_reef():
    """Coral shallows near spawn: mantas, then the moray set on the reef floor."""
    s = S2(deadline=120)
    s.fx('night_vision')
    s.add('height 64 -32')
    # manta rays glide over the reef: the camera follows one from behind and above
    s.go(56, v('hy', 6), -40, 70, v('hy', 3), -26, settle=300)
    s.r('kill @e[type=raft:manta_ray,distance=..60]')
    s.summon('raft:manta_ray', 3, spread=4, ahead=8, dy=-1)
    s.add('wait 60')
    s.clip('c_manta', 5, look='raft:manta_ray', chase='6,2', smooth=0.05)
    s.go(58, v('hy', 7), -46, 70, v('hy', 2), -26, settle=40)
    s.clip('c_manta2', 5, look='raft:manta_ray', smooth=0.05)
    s.kill('raft:manta_ray')
    # the moray: a ruin wall with a hole on the reef floor, the eel moves in; a diver swims up and it lunges
    s.add('height 64 -34')
    ruin_with_hole(s, 64, -32)
    s.r('kill @e[type=raft:moray_eel,distance=..40]', 'kill @e[type=minecraft:item,distance=..40]')
    s.r('summon raft:moray_eel 64.5 {hy+1} -34.5 {PersistenceRequired:1b}')
    s.go(70, v('hy', 3.0), -36, 64.5, v('hy', 1.4), -33.5, settle=120)
    s.add('wait 140')
    s.add('freecam 69.5 {hy+2.6} -36.5 59 12', 'wait 8 render', 'shot c_moray_check', 'freecam off')
    s.actor('survival')
    s.cmd('effect give @p minecraft:resistance infinite 4 true', 'effect give @p minecraft:water_breathing infinite 0 true',
          'item replace entity @p armor.head with raft:diving_helmet',
          'item replace entity @p armor.chest with raft:oxygen_tank[raft:stored_air=1030]',
          'item replace entity @p armor.legs with raft:wetsuit', 'item replace entity @p armor.feet with raft:flippers')
    s.r('tp @p 64.5 {hy+1} -41.5 0 5')
    s.add('wait 10', 'freecam 69.5 {hy+2.6} -36.5 59 12', 'wait 8 render', 'freecam off')
    s.clip('c_moray', 5, cam=f"69.5,{v('hy', 2.6)},-36.5,59,12", look=f"64.5,{v('hy', 1.4)},-33.5",
           at=[(1, 'cmd execute in raft:raftdim run tp @p 64.5 {hy+1} -41.5 0 5'), (2, 'press forward'),
               (50, 'release forward')])
    s.add('cmd data get entity @e[type=raft:moray_eel,limit=1] Pos')
    s.cmd('effect clear @p', 'clear @p')
    s.spec()
    s.kill('raft:moray_eel')
    return s


def run_isle():
    """Palm isle (-256 -288): a crab digs itself in, the seagull flock, gulls at a wheat field."""
    s = S2(deadline=120)
    s.fx()
    s.add('height -259 -281')
    s.go(-259, v('hy', 2.0), -284, -259, v('hy', 0.3), -278, settle=420)
    s.r('kill @e[type=raft:crab,distance=..40]', 'kill @e[type=raft:seagull,distance=..60]')
    s.r('fill -262 {hy-1:i} -289 -257 {hy-1:i} -276 minecraft:sand', 'fill -262 {hy:i} -289 -257 {hy+3:i} -276 minecraft:air')
    # a crab digs itself in: low camera next to it, the player sprints in from 8 blocks
    s.actor('survival')
    s.cmd('effect give @p minecraft:resistance infinite 4 true')
    s.r('tp @p -259.5 {hy} -286.5 0 10')
    s.r('summon raft:crab -259.5 {hy} -278.5 {Variant:"blue",PersistenceRequired:1b}')
    s.add('wait 30', 'freecam -256.6 {hy+0.95} -276.6 125 15', 'wait 8 render', 'freecam off')
    s.clip('c_crab_dig', 4, cam=f"-256.6,{v('hy', 0.95)},-276.6,125,15", look=f"-259.8,{v('hy', 0.3)},-279.5",
           at=[(3, 'press sprint'), (4, 'press forward'), (24, 'release forward'), (25, 'release sprint')])
    s.kill('raft:crab')
    s.spec()
    # the flock over the isle
    s.go(-262, v('hy', 2.5), -290, -262, v('hy', 8), -276, settle=60)
    s.summon('raft:seagull', 7, spread=3, ahead=12, dy=9)
    s.add('wait 100')
    # the flock circles over the isle (the camera turns with it), then a second take flying along with it
    s.clip('c_gulls', 5, look='raft:seagull', smooth=0.04)
    s.clip('c_gulls2', 5, look='raft:seagull', chase='10,3', smooth=0.12)
    # gulls at a wheat field (no crabs around)
    s.r('kill @e[type=raft:crab,distance=..60]')
    s.go(-262, v('hy', 2.0), -282, -262, v('hy', -1), -277, settle=30)
    s.add('pcmd fill ^-2 ^-2 ^3 ^2 ^-2 ^6 minecraft:farmland[moisture=7]', 'pcmd fill ^-2 ^-1 ^3 ^2 ^-1 ^6 minecraft:wheat[age=6]',
          'wait 260')
    s.clip('c_gull_peck', 5)
    s.kill('raft:seagull')
    return s


def raft_scenes(s):
    """A raft of your own at open sea near spawn (kelp forest edge, like the bctest raft tests): crop plots with ripe
    crops and pineapples, a scarecrow, a motor at the stern. f_crops, then r_motor: the helmsman starts the motor."""
    s.spec()
    s.fx()
    s.go(-7, 104.5, -13, 0, 100, -1, settle=240)
    s.r('kill @e[type=raft:vessel,distance=..80]', 'kill @e[type=minecraft:item,distance=..80]')
    s.r('fill -4 99 -5 4 99 5 raft:raft_foundation', 'fill -4 100 -5 4 104 5 minecraft:air',
        'setblock 0 100 -3 raft:helm[facing=south]', 'setblock 0 100 -5 raft:raft_motor[facing=north]{Fuel:6000}',
        'fill 1 100 0 3 100 3 raft:crop_plot',
        'setblock 1 101 0 minecraft:wheat[age=7]', 'setblock 2 101 0 minecraft:wheat[age=7]', 'setblock 3 101 0 minecraft:wheat[age=6]',
        'setblock 1 101 1 minecraft:carrots[age=7]', 'setblock 2 101 1 raft:pineapple_crop[age=5]',
        'setblock 3 101 1 minecraft:carrots[age=5]', 'setblock 1 101 2 minecraft:potatoes[age=7]',
        'setblock 2 101 2 raft:pineapple_crop[age=3]', 'setblock 3 101 2 minecraft:beetroots[age=3]',
        'setblock 1 101 3 minecraft:wheat[age=5]', 'setblock 2 101 3 minecraft:potatoes[age=5]', 'setblock 3 101 3 minecraft:wheat[age=7]',
        'setblock -1 100 2 raft:scarecrow[half=lower,facing=east]', 'setblock -1 101 2 raft:scarecrow[half=upper,facing=east]',
        'setblock -3 100 3 minecraft:barrel[facing=up]', 'setblock -3 100 -1 minecraft:chest[facing=east]')
    s.add('wait 20')
    s.dolly('f_crops', 4, (6.5, 103.8, 6.5), (4.8, 102.6, 4.8), (1.2, 100.8, 1.8), settle=30)
    s.actor('creative')
    s.add('nearblock raft:helm 48 1.3 0.5 0', 'wait 10', 'use',
          'swaitfor 1500 execute in raft:raftdim if entity @e[type=raft:vessel]', 'wait 30')
    s.add('freecam 0.5 100.9 -9.0 0 8', 'wait 8 render', 'freecam off')
    s.clip('r_motor', 5, cam='0.5,100.9,-9.0,0,8', look='raft:vessel', chase='9,1.4', smooth=0.08, at=[(20, 'press forward')])
    s.add('release forward', 'hold sneak 8')
    s.spec()
    return s


def beach_stump(s):
    """W1: an overworld beach with a short dark driftwood stump (raft:driftwood feature)."""
    O = 'minecraft:overworld'
    s.spec()
    s.add('tpbiome minecraft:beach minecraft:overworld', 'settle 300')
    s.cmd(f'execute in {O} run time set 6000')
    s.add('find raft:driftwood_log 64')
    s.go(v('fx', 5), v('fy', 3.2), v('fz', -5), v('fx'), v('fy', 0.6), v('fz'), settle=200, dim=O)
    s.add('wait 20 render', 'still w_beach_check 1.0')
    s.clip('w_beach', 5, orbit=f"{v('fx')},{v('fz')},45", look=f"{v('fx')},{v('fy', 0.6)},{v('fz')}")
    return s


def run_gulls():
    """Retakes (6.11., later the same day): the flock over open sea near spawn, where the chasing camera meets no
    palm trees, and gulls pecking at a wheat field seen from close by (crabs kept away)."""
    s = S2(deadline=60)
    s.fx()
    s.go(0, 110, -24, 0, 116, 4, settle=240)
    s.r('kill @e[type=raft:seagull,distance=..100]')
    s.r(*[f'summon raft:seagull {x} {y} {z}' for x, y, z in
          ((0, 117, 6), (2, 118, 8), (-2, 117, 9), (3, 116, 5), (-3, 118, 5), (1, 119, 11), (-1, 116, 3))])
    s.add('wait 100')
    s.clip('c_gulls3', 5, look='raft:seagull', chase='9,2.5', smooth=0.1)
    s.clip('c_gulls4', 5, look='raft:seagull', smooth=0.05)
    s.r('kill @e[type=raft:seagull,distance=..120]')
    # gulls at a wheat field on the palm isle (on the sand patch of the crab scene)
    s.add('height -259 -281')
    s.go(-256.5, v('hy', 3.2), -283.5, -259.5, v('hy', 0.3), -280.5, settle=300)
    s.r('kill @e[type=raft:crab,distance=..60]', 'kill @e[type=raft:seagull,distance=..80]')
    s.r('fill -261 {hy-1:i} -282 -258 {hy-1:i} -279 minecraft:farmland[moisture=7]',
        'fill -261 {hy:i} -282 -258 {hy:i} -279 minecraft:wheat[age=7]',
        'fill -261 {hy+1:i} -282 -258 {hy+4:i} -279 minecraft:air')
    s.r(*[f'summon raft:seagull {x} {{hy+6}} {z}' for x, z in
          ((-262, -284), (-258, -285), (-264, -280), (-256, -279), (-260, -276), (-263, -277))])
    s.add('wait 270')
    s.r('kill @e[type=raft:crab,distance=..60]')
    s.clip('c_gull_peck', 5, at=[(0, 'cmd execute in raft:raftdim run kill @e[type=raft:crab,distance=..60]')])
    s.r('kill @e[type=raft:seagull,distance=..80]')
    return s


def run_peck():
    """Gulls pecking at the wheat field (third try: the rec looks at the field on every frame; with a plain rec the
    spectator camera had turned back to the horizon during the wait)."""
    s = S2(deadline=40)
    s.fx()
    s.add('height -259 -281')
    s.go(-256.5, v('hy', 3.2), -283.5, -259.5, v('hy', 0.3), -280.5, settle=300)
    s.r('kill @e[type=raft:crab,distance=..60]', 'kill @e[type=raft:seagull,distance=..80]')
    s.r('fill -261 {hy-1:i} -282 -258 {hy-1:i} -279 minecraft:farmland[moisture=7]',
        'fill -261 {hy:i} -282 -258 {hy:i} -279 minecraft:wheat[age=7]',
        'fill -261 {hy+1:i} -282 -258 {hy+4:i} -279 minecraft:air')
    s.add('wait 10 render', 'still c_gull_peck_check 1.0')
    s.r(*[f'summon raft:seagull {x} {{hy+6}} {z}' for x, z in
          ((-262, -284), (-258, -285), (-264, -280), (-256, -279), (-260, -276), (-263, -277))])
    s.add('wait 270')
    s.r('kill @e[type=raft:crab,distance=..60]')
    s.clip('c_gull_peck', 5, look=f"-259.5,{v('hy', 0.3)},-280.5",
           at=[(0, 'cmd execute in raft:raftdim run kill @e[type=raft:crab,distance=..60]')])
    s.r('kill @e[type=raft:seagull,distance=..80]')
    return s


# ---------------------------------------------------------------------------------------------------------------------
# Real-time retakes (6.11. evening): since the bctest fix c8da36f a clip shows one second of game time per second
# (before, every frame cost two game ticks and the creatures moved three times too fast). The sets from the takes
# above are still in bcdoc2 (ruin wall at 64 -32, sand patch and wheat field on the palm isle).

def run_rt_reef():
    """Mantas, the moray at its ruin wall, the anglerfish in the trench, in real time."""
    s = S2(deadline=120)
    s.cmd('difficulty normal')
    s.fx('night_vision')
    s.add('height 64 -32')
    s.go(56, v('hy', 6), -40, 70, v('hy', 3), -26, settle=300)
    s.r('kill @e[type=raft:manta_ray,distance=..60]')
    s.summon('raft:manta_ray', 3, spread=4, ahead=8, dy=1)
    s.add('wait 60')
    s.clip('c_manta', 5, look='raft:manta_ray', chase='6,2', smooth=0.05)
    s.go(58, v('hy', 7), -46, 70, v('hy', 2), -26, settle=40)
    s.clip('c_manta2', 5, look='raft:manta_ray', smooth=0.05)
    s.kill('raft:manta_ray')
    # the moray: the diver starts 5 blocks closer than in the first take (in real time the lunge must come within 5 s)
    s.add('height 64 -34')
    s.r('kill @e[type=raft:moray_eel,distance=..40]', 'kill @e[type=minecraft:item,distance=..40]')
    s.r('setblock 64 {hy+1:i} -32 minecraft:water')
    s.r('summon raft:moray_eel 64.5 {hy+1} -34.5 {PersistenceRequired:1b}')
    s.go(70, v('hy', 3.0), -36, 64.5, v('hy', 1.4), -33.5, settle=120)
    s.add('wait 140')
    s.actor('survival')
    s.cmd('effect give @p minecraft:resistance infinite 4 true', 'effect give @p minecraft:water_breathing infinite 0 true',
          'item replace entity @p armor.head with raft:diving_helmet',
          'item replace entity @p armor.chest with raft:oxygen_tank[raft:stored_air=1030]',
          'item replace entity @p armor.legs with raft:wetsuit', 'item replace entity @p armor.feet with raft:flippers')
    s.r('tp @p 64.5 {hy+1} -39.5 0 5')
    s.add('wait 10', 'freecam 69.5 {hy+2.6} -36.5 59 12', 'wait 8 render', 'freecam off')
    s.clip('c_moray', 5, cam=f"69.5,{v('hy', 2.6)},-36.5,59,12", look=f"64.5,{v('hy', 1.4)},-33.5",
           at=[(1, 'cmd execute in raft:raftdim run tp @p 64.5 {hy+1} -39.5 0 5'), (2, 'press forward'), (60, 'release forward')])
    s.cmd('effect clear @p', 'clear @p')
    s.spec()
    s.kill('raft:moray_eel')
    # the anglerfish in the abyssal trench: the lure first (the fish held still for 40 frames), then it darts and bites
    s.fx()
    s.add('height 448 0')
    s.go(448, v('hy', 4), 6, 448, v('hy', 2), -4, settle=500)
    s.cmd('effect give @p minecraft:night_vision infinite 0 true', 'effect give @p minecraft:water_breathing infinite 0 true')
    s.actor('survival')
    s.cmd('effect give @p minecraft:resistance infinite 4 true',
          'item replace entity @p armor.head with raft:diving_helmet[raft:diving_lamp={}]')
    s.r('kill @e[type=raft:anglerfish,distance=..40]')
    s.r('tp @p 448.5 {hy} 0.5 180 0')
    s.add('wait 10', 'where')
    s.r('summon raft:anglerfish {px} {py+1} {pz-4.2} {PersistenceRequired:1b,Rotation:[0f,0f],NoAI:1b}')
    s.add('wait 10', 'freecam {px+3.2} {py+1.9} {pz-1.8} 120 15', 'wait 8 render', 'shot c_angler_check', 'freecam off')
    s.clip('c_angler', 5, cam="{px+3.2},{py+1.9},{pz-1.8},120,15", look='raft:anglerfish', smooth=0.15,
           at=[(0, 'cmd execute in raft:raftdim run tp @p {px} {py} {pz} 180 0'),
               (40, 'cmd execute in raft:raftdim run data merge entity @e[type=raft:anglerfish,limit=1,sort=nearest] {NoAI:0b}')])
    s.r('kill @e[type=raft:anglerfish,distance=..40]')
    s.cmd('effect clear @p', 'clear @p')
    s.spec()
    return s


def run_rt_isle():
    """The crab digging in, the flock over open sea and the gulls at the wheat field, in real time."""
    s = S2(deadline=120)
    s.fx()
    s.add('height -259 -281')
    s.go(-259, v('hy', 2.0), -284, -259, v('hy', 0.3), -278, settle=420)
    s.r('kill @e[type=raft:crab,distance=..40]', 'kill @e[type=raft:seagull,distance=..60]')
    s.actor('survival')
    s.cmd('effect give @p minecraft:resistance infinite 4 true')
    s.r('tp @p -259.5 {hy} -286.5 0 10')
    s.r('summon raft:crab -259.5 {hy} -278.5 {Variant:"blue",PersistenceRequired:1b}')
    s.add('wait 30', 'freecam -256.6 {hy+0.95} -276.6 125 15', 'wait 8 render', 'freecam off')
    s.clip('c_crab_dig', 4, cam=f"-256.6,{v('hy', 0.95)},-276.6,125,15", look=f"-259.8,{v('hy', 0.3)},-279.5",
           at=[(0, 'cmd execute in raft:raftdim run kill @e[type=raft:seagull,distance=..60]'),
               (3, 'press sprint'), (4, 'press forward'), (40, 'release forward'), (41, 'release sprint')])
    s.kill('raft:crab')
    s.spec()
    # gulls at the wheat field (the field from the earlier take, replanted)
    s.go(-256.5, v('hy', 3.2), -283.5, -259.5, v('hy', 0.3), -280.5, settle=60)
    s.r('kill @e[type=raft:crab,distance=..60]', 'kill @e[type=raft:seagull,distance=..80]')
    s.r('fill -261 {hy-1:i} -282 -258 {hy-1:i} -279 minecraft:farmland[moisture=7]',
        'fill -261 {hy:i} -282 -258 {hy:i} -279 minecraft:wheat[age=7]',
        'fill -261 {hy+1:i} -282 -258 {hy+4:i} -279 minecraft:air')
    s.r(*[f'summon raft:seagull {x} {{hy+6}} {z}' for x, z in
          ((-262, -284), (-258, -285), (-264, -280), (-256, -279), (-260, -276), (-263, -277))])
    s.add('wait 270')
    s.r('kill @e[type=raft:crab,distance=..60]')
    s.clip('c_gull_peck', 5, look=f"-259.5,{v('hy', 0.3)},-280.5",
           at=[(0, 'cmd execute in raft:raftdim run kill @e[type=raft:crab,distance=..60]')])
    s.r('kill @e[type=raft:seagull,distance=..80]')
    # the flock over open sea near spawn, the camera flying along
    s.go(0, 110, -24, 0, 116, 4, settle=240)
    s.r('kill @e[type=raft:seagull,distance=..100]')
    s.r(*[f'summon raft:seagull {x} {y} {z}' for x, y, z in
          ((0, 117, 6), (2, 118, 8), (-2, 117, 9), (3, 116, 5), (-3, 118, 5), (1, 119, 11), (-1, 116, 3))])
    s.add('wait 100')
    s.clip('c_gulls3', 5, look='raft:seagull', chase='9,2.5', smooth=0.1)
    s.clip('c_gulls4', 5, look='raft:seagull', smooth=0.05)
    s.r('kill @e[type=raft:seagull,distance=..120]')
    return s


def run_rt_crab():
    """The crab digging in, real time, third try: the wheat field of the gull scenes is turned back into sand, and the
    leftover gulls and crabs are killed around the player (pcmd: the earlier kills never reached the raft dimension)."""
    s = S2(deadline=60)
    s.fx()
    s.add('height -259 -281')
    s.go(-259, v('hy', 2.0), -284, -259, v('hy', 0.3), -278, settle=420)
    s.add('pcmd kill @e[type=raft:crab,distance=..80]', 'pcmd kill @e[type=raft:seagull,distance=..160]')
    s.r('fill -262 {hy-1:i} -289 -257 {hy-1:i} -276 minecraft:sand', 'fill -262 {hy:i} -289 -257 {hy+3:i} -276 minecraft:air')
    s.actor('survival')
    s.cmd('effect give @p minecraft:resistance infinite 4 true')
    s.r('tp @p -259.5 {hy} -286.5 0 10')
    s.r('summon raft:crab -259.5 {hy} -278.5 {Variant:"blue",PersistenceRequired:1b}')
    s.add('wait 30', 'pcmd kill @e[type=raft:seagull,distance=..160]', 'freecam -256.6 {hy+0.95} -276.6 125 15',
          'wait 8 render', 'still c_crab_dig_check 1.0', 'freecam off')
    s.clip('c_crab_dig', 4, cam=f"-256.6,{v('hy', 0.95)},-276.6,125,15", look=f"-259.8,{v('hy', 0.3)},-279.5",
           at=[(0, 'pcmd kill @e[type=raft:seagull,distance=..160]'),
               (3, 'press sprint'), (4, 'press forward'), (40, 'release forward'), (41, 'release sprint')])
    s.add('pcmd kill @e[type=raft:crab,distance=..80]')
    s.spec()
    return s


if __name__ == '__main__':
    prefix = sys.argv[1]
    for k, run in enumerate((run_reef, run_isle)):
        L = run().lines()
        open(f'{prefix}{k + 1}.txt', 'w').write('\n'.join(L) + '\n')
        print(f'{prefix}{k + 1}.txt', len(L))
