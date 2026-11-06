import sys
STRUCTS = ['old_lighthouse', 'saltmere_village', 'ashen_forge', 'beach_shack', 'castaway_camp', 'iceberg_outpost',
           'rusted_rig', 'port_solace', 'coral_temple', 'helix_station', 'abyssal_sanctum', 'pirate_cove',
           'wreck_galleon', 'wreck_cargo_ship', 'wreck_fishing_boat', 'sunken_plane', 'sunken_ruins',
           'abandoned_raft', 'buoy_field']
def script(seed, points, tag, structs=STRUCTS):
    out = ['rd 2', 'world ' + seed]
    for s in structs:
        for i, (x, z) in enumerate(points):
            label = f'{tag}_{s}_{i}'
            out += [f'log {label}', f'scout raft:{s} {x} {z}',
                    'cmd execute in raft:raftdim run forceload add {x0:i} {z0:i} {x1:i} {z1:i}',
                    'swait 200', f'audit raft:{s} {x} {z} {label}',
                    'cmd execute in raft:raftdim run forceload remove all']
    return '\n'.join(out) + '\n'
if __name__ == '__main__':
    open(sys.argv[1], 'w').write(script('bcaudit1', [(0, 0), (3000, 2000), (-2500, 3500)], 's1'))
    open(sys.argv[2], 'w').write(script('tides2', [(1500, -2500), (-3500, -1000)], 's2'))
