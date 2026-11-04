"""Die Ausstellung: jeder Block und jedes Item der sieben Creative-Tabs, 20 pro Bild (4 Spalten x 5 Reihen), als
item_display vor einer Wand hoch ueber dem Meer, frontal gefilmt (Ego-Perspektive, FOV 70, Blick nach Norden).
Die Namen kommen im Schnitt dazu (doc.py zeichnet sie an die projizierten Positionen, siehe labels.json).
  from museum import museum;  museum(script)            -> fuegt die Skriptzeilen an, schreibt tools/labels.json
Die Item-Listen (Reihenfolge wie im Spiel) stehen in tabs.json, die englischen Namen in names.json (aus den Lang-Dateien)."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
TABS = [('raft:bc_building', 'building'), ('raft:bc_decor', 'decor'), ('raft:bc_nature', 'nature'), ('raft:bc_voyage', 'voyage'),
        ('raft:bc_creatures', 'creatures'), ('raft:bc_story', 'story'), ('raft:raft', 'raft')]
CX, EY, CZ = 8.5, 161.62, 30.5          # eye of the camera
D = 10.5                                 # eye -> display plane
COLS = [-3.0, -1.0, 1.0, 3.0]
ROWS = [5.0, 2.5, 0.0, -2.5, -5.0]
ICON_DY = 0.35
LABEL_DY = -0.62
FOV = 70.0
W, H = 1080, 1920


def project(x, y, z):
    """screen position (0..1) of a world point for the museum camera (facing north, pitch 0)"""
    depth = CZ - z
    t = math.tan(math.radians(FOV / 2))
    sx = 0.5 + (x - CX) / (depth * t * W / H) * 0.5
    sy = 0.5 - (y - EY) / (depth * t) * 0.5
    return round(sx, 4), round(sy, 4)


def museum(s, tabs_file=None, names_file=None, only=None, build=True, write_labels=True):
    """only: set of still names to take again (the wall is already there when build is False)."""
    tabs = json.load(open(tabs_file or os.path.join(HERE, 'tabs.json')))
    names = json.load(open(names_file or os.path.join(HERE, 'names.json')))
    zp = CZ - D
    s.add(f'cmd execute in raft:raftdim run tp @p {CX} {EY - 1.62:.2f} {CZ} 180 0', 'settle 60')
    if build:
        s.r(f'fill {int(CX) - 8} {int(EY) - 9} {int(zp) - 2} {int(CX) + 8} {int(EY) + 9} {int(zp) - 2} minecraft:smooth_sandstone',
            f'fill {int(CX) - 8} {int(EY) - 9} {int(zp) - 1} {int(CX) + 8} {int(EY) + 9} {int(zp) + 12} minecraft:air')
    s.add('settle 20', 'third off', 'fly on', 'fov 70', 'hud off')
    labels = {}
    for tab, short in TABS:
        ids = tabs[tab]
        seen = set()
        pages = [ids[i:i + 20] for i in range(0, len(ids), 20)]
        for pi, page in enumerate(pages):
            name = f'i_{short}_{pi + 1}'
            if only is not None and name not in only:
                continue
            entries = []
            for k, iid in enumerate(page):
                col, row = k % 4, k // 4
                x, y = CX + COLS[col], EY + ROWS[row] + ICON_DY
                item = iid
                comp = ''
                label = names.get(iid.split(':')[1], iid)
                if iid in seen and iid == 'raft:diving_helmet':
                    comp = '"components":{"raft:diving_lamp":{}},'
                    label = 'Diving Helmet with Lamp'
                seen.add(iid)
                s.r(f'summon minecraft:item_display {x:.2f} {y:.2f} {zp:.2f} {{item:{{id:"{item}",count:1{"," + comp[:-1] if comp else ""}}},'
                    f'item_display:"gui",billboard:"center",brightness:{{sky:15,block:15}},Tags:["bcmus"],'
                    f'transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.3f,1.3f,1.3f]}}}}')
                lx, ly = project(x, EY + ROWS[row] + LABEL_DY, zp)
                entries.append(dict(text=label, x=lx, y=ly))
            s.add(f'cmd execute in raft:raftdim run tp @p {CX} {EY - 1.62:.2f} {CZ} 180 0', 'fly on', 'wait 4',
                  f'pose {CX} {EY - 1.62:.2f} {CZ} 180 0', f'still {name} 1.25')
            s.r('kill @e[type=minecraft:item_display,tag=bcmus]')
            labels[name] = entries
    if write_labels:
        json.dump(labels, open(os.path.join(HERE, 'labels.json'), 'w'), indent=0)
    return s
