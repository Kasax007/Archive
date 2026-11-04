"""Skript-Bausteine fuer die Aufnahmen der Doku mit tools/bctest (Beach-Craft-Repo, BcScript: rec/still/open/keep ...).
Jeder Lauf ist eine Funktion in shots_runs.py, die eine Liste von Skriptzeilen baut; dieses Modul liefert die Bausteine.
Welt: build/run/bctest/saves/bcdoc (Seed "beachcraft", einmal erzeugt und dann immer wieder geoeffnet).
Koordinaten nie mit "%d.5" formatieren (negative Werte), immer Gleitkomma."""
import math

DIM = 'raft:raftdim'


def f1(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.') if isinstance(v, float) else str(v)


class Script:
    def __init__(self, deadline=17.0, world='bcdoc'):
        self.L = [f'open {world}', f'deadline {deadline}', 'size 1080 1920', 'gui 3', 'rd 6', 'hud off', 'fov 70',
                  'cmd gamerule send_command_feedback false', 'cmd gamerule show_advancement_messages false',
                  'cmd gamerule spawn_monsters false',
                  'cmd advancement grant @p everything', 'cmd recipe give @p *']

    def add(self, *lines):
        self.L.extend(lines)
        return self

    def cmd(self, *cs):
        for c in cs:
            self.L.append('cmd ' + c)
        return self

    def r(self, *cs):
        """command in the raft dimension"""
        for c in cs:
            self.L.append(f'cmd execute in {DIM} run {c}')
        return self

    def tp(self, x, y, z, yaw=None, pitch=None, dim=DIM):
        rot = '' if yaw is None else f' {yaw:.1f} {pitch:.1f}'
        self.L.append(f'cmd execute in {dim} run tp @p {f1(x)} {f1(y)} {f1(z)}{rot}')
        return self

    def look_at(self, x, y, z):
        self.L.append(f'face {f1(x)} {f1(y)} {f1(z)}')
        return self

    def settle(self, s=60):
        self.L.append(f'settle {s}')
        return self

    def still(self, name, scale=1.25):
        self.L.append(f'still {name} {scale}')
        return self

    def shot(self, name):
        self.L.append(f'shot {name}')
        return self

    def rec(self, name, frames, fps, at=None, **opt):
        o = ' '.join(f'{k}={v}' for k, v in opt.items())
        self.L.append(f'rec {name} {frames} {fps} {o}'.rstrip())
        for fr, c in sorted(at or [], key=lambda x: x[0]):
            self.L.append(f'@{fr} {c}')
        self.L.append('end')
        return self

    # ------------------------------------------------------------ player / camera setups

    def gear(self, kind):
        """'dive' = full diving set with the helmet lamp look, 'none' = empty armour slots"""
        if kind == 'dive':
            self.cmd('item replace entity @p armor.head with raft:diving_helmet',
                     'item replace entity @p armor.chest with raft:oxygen_tank',
                     'item replace entity @p armor.legs with raft:wetsuit',
                     'item replace entity @p armor.feet with raft:flippers')
        elif kind == 'none':
            for s in ('head', 'chest', 'legs', 'feet'):
                self.cmd(f'item replace entity @p armor.{s} with air')
        return self

    def hands(self, main='air', off='air'):
        self.cmd(f'item replace entity @p weapon.mainhand with {main}', f'item replace entity @p weapon.offhand with {off}')
        return self

    def mode(self, m):
        self.cmd(f'gamemode {m} @p')
        return self

    def third(self, on=True, dist=None):
        self.L.append('third on' if on else 'third off')
        if dist is not None:
            self.cmd(f'attribute @p minecraft:camera_distance base set {dist}')
        return self

    def effects(self, *names):
        self.cmd('effect clear @p')
        for n in names:
            self.cmd(f'effect give @p minecraft:{n} infinite 0 true')
        return self

    def view(self, name, px, py, pz, tx, ty, tz, dist=5, scale=1.25, settle=40, yaw_off=0.0, pitch_off=0.0, third=True):
        """Player at p, looking at t (plus a small yaw offset so the target is not hidden behind the player), third
        person camera dist behind: one still."""
        yaw, pitch = aim(px, py + 1.62, pz, tx, ty, tz)
        yaw += yaw_off
        pitch += pitch_off
        self.tp(px, py, pz, yaw, pitch)
        self.third(third, dist)
        self.L.append('fly on')
        self.settle(settle)
        self.L.append(f'pose {f1(px)} {f1(py)} {f1(pz)} {yaw:.1f} {pitch:.1f}')
        self.still(name, scale)
        return self

    def ring(self, prefix, center, radius, height, n=4, start=45.0, dist=5, look_dy=0.0, yaw_off=8.0, settle=40):
        """n views around a centre (x, y, z): player on a circle, looking (a little beside) the centre."""
        cx, cy, cz = center
        for k in range(n):
            a = math.radians(start + 360.0 * k / n)
            px, pz = cx + math.sin(a) * radius, cz - math.cos(a) * radius
            self.view(f'{prefix}{k}', round(px, 1), height, round(pz, 1), cx, cy + look_dy, cz, dist=dist, yaw_off=yaw_off, settle=settle)
        return self

    def chest(self, name, x, y, z, stand=None, gui_wait=6):
        """Open the container at x y z (server side, the loot table is rolled like opening it by hand) and take a shot
        of its screen. The player waits next to it (stand, default 2 blocks south, a bit above) in first person."""
        sx, sy, sz = stand if stand else (x + 0.5, y + 1, z + 2.5)
        yaw, pitch = aim(sx, sy + 1.62, sz, x + 0.5, y + 0.5, z + 0.5)
        self.tp(sx, sy, sz, yaw, pitch)
        self.third(False)
        self.L.append('fly on')
        self.L.append('wait 10')
        self.L.append(f'openbe {x} {y} {z}')
        self.L.append(f'wait {gui_wait} render')
        self.shot(name)
        self.L.append('esc')
        return self

    def clear_kelp(self, x1, y1, z1, x2, y2, z2):
        """kelp and sea grass between the camera and a sunken place: water instead (a clear view, like a diver pushing
        the kelp aside). Boxes over 32768 blocks are split along x."""
        xs = sorted((int(x1), int(x2)))
        ys, zs = sorted((int(y1), int(y2))), sorted((int(z1), int(z2)))
        step = max(1, 32000 // ((ys[1] - ys[0] + 1) * (zs[1] - zs[0] + 1)))
        x = xs[0]
        while x <= xs[1]:
            xe = min(xs[1], x + step - 1)
            for b in ('kelp_plant', 'kelp', 'tall_seagrass', 'seagrass'):
                self.r(f'fill {x} {ys[0]} {zs[0]} {xe} {ys[1]} {zs[1]} minecraft:water replace minecraft:{b}')
            x = xe + 1
        return self

    def lines(self):
        return self.L + ['where']

    def write(self, path):
        open(path, 'w').write('\n'.join(self.lines()) + '\n')
        return len(self.L)


def aim(x, eye_y, z, tx, ty, tz):
    dx, dy, dz = tx - x, ty - eye_y, tz - z
    yaw = math.degrees(math.atan2(-dx, dz))
    pitch = -math.degrees(math.atan2(dy, math.hypot(dx, dz)))
    return yaw, pitch
