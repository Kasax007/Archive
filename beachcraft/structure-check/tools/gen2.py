import sys
sys.path.insert(0, '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad/audit')
from gen import script
SP = '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad/audit/'
open(SP + 'verify1.txt', 'w').write(script('bcaudit1', [(0, 0), (3000, 2000), (-2500, 3500)], 'v1'))
open(SP + 'verify2.txt', 'w').write(script('tides2', [(1500, -2500), (-3500, -1000)], 'v2'))

NPC = [('old_lighthouse', ['keeper_fenn']), ('saltmere_village', ['nalu', 'old_tamo']), ('ashen_forge', ['dr_voss']),
       ('beach_shack', ['teo']), ('castaway_camp', ['kai']), ('iceberg_outpost', ['dr_lund']), ('rusted_rig', ['okafor'])]
POINTS = {'castaway_camp': [(3000, 2000), (1500, -2500), (-4000, 0)]}
out = ['rd 6', 'clouds off', 'world bcaudit1', 'hud off', 'cmd gamemode spectator @p']
def place(s, x, z, label, npcs, over=True):
    global out
    out += [f'log {label}', f'scout raft:{s} {x} {z}',
            'cmd execute in raft:raftdim run forceload add {x0:i} {z0:i} {x1:i} {z1:i}', 'swait 100',
            f'audit raft:{s} {x} {z} {label}', 'cmd tick freeze']
    for n in npcs:
        out += [f'npcview raft:{n}', 'cmd execute in raft:raftdim run tp @p {camx} {camy} {camz} {camyaw} {campitch}',
                'settle 90', 'pose {camx} {camy} {camz} {camyaw} {campitch}', 'wait 3', f'shotif camx {label}_{n}']
    if over:
        out += ['overview 1', 'cmd execute in raft:raftdim run tp @p {ovx} {ovy} {ovz} {ovyaw} {ovpitch}', 'settle 90',
                'pose {ovx} {ovy} {ovz} {ovyaw} {ovpitch}', 'wait 3', f'shot {label}_over']
    out += ['cmd tick unfreeze', 'cmd execute in raft:raftdim run forceload remove all']
for s, npcs in NPC:
    for i, (x, z) in enumerate(POINTS.get(s, [(0, 0), (3000, 2000)])):
        place(s, x, z, f'p_{s}_{i}', npcs)
for s in ['port_solace', 'pirate_cove', 'abandoned_raft', 'buoy_field', 'wreck_galleon', 'wreck_cargo_ship']:
    place(s, 0, 0, f'p_{s}_0', [])
open(SP + 'pics.txt', 'w').write('\n'.join(out) + '\n')
