"""Bausteine fuer die Aufnahmen der Doku v2 (Querformat 1920x1080, Shader, freie Kamera, Welt bcdoc2).

Kamera: fuer Landschaft und Orte ist der Spieler Zuschauer (spectator, erste Person, kein HUD): er ist die Kamera und
nie im Bild. Nur fuer Vorfuehrungen steht der Spieler im Bild, die Kamera ist dann frei (cam=..., freecam).
Positionen koennen Skript-Variablen sein ({cx+20}: scout setzt x0 y0 z0 x1 y1 z1 cx cy cz, find fx fy fz,
openloot ... peek ox oy oz, where px py pz, height hy). Augenhoehe = Fusshoehe + 1.62.
"""
import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'tools')))
from film import Script, aim, f1  # noqa: E402

DIM = 'raft:raftdim'
FPS = 30          # Spielzeit-Bilder pro Sekunde einer Aufnahme (im Schnitt auf 60 fps interpoliert)
EYE = 1.62
MAX_SECS = 5.0   # longer clips cost too much render time (3 s per frame with shaders); the edit slows them down


def v(name, off=0.0):
    """placeholder {name+off}"""
    return '{%s%+.2f}' % (name, off) if off else '{%s}' % name


class S2(Script):
    def __init__(self, deadline=55.0, world='bcdoc2', rd=10, new=False):
        self.L = ([f'world beachcraft', f'keep {world}'] if new else [f'open {world}', 'respawn']) + [
            f'deadline {deadline}', 'size 1920 1080', 'gui 2', f'rd {rd}', 'hud off', 'fov 70', 'gamma 0.5',
            'cmd gamerule send_command_feedback false', 'cmd gamerule show_advancement_messages false',
            'cmd gamerule spawn_monsters false', 'cmd advancement grant @p everything', 'cmd recipe give @p *',
            'cmd time set 6000', 'cmd weather clear', 'cmd effect clear @p', 'cmd clear @p', 'esc']
        self.spec()
        self.H = len(self.L)            # header: repeated at the start of every part (see write_parts)

    def spec(self):
        self.cmd('gamemode spectator @p')
        self.L.append('third off')
        return self

    def actor(self, mode='creative'):
        """the player as an actor in the picture (free camera)"""
        self.cmd(f'gamemode {mode} @p')
        self.L.append('third on')
        return self

    def go(self, x, y, z, tx, ty, tz, settle=420, dim=DIM):
        """camera (eye) at x y z, looking at tx ty tz; all values numbers or placeholders"""
        y = y if isinstance(y, str) else y - EYE
        if isinstance(y, str) and y.startswith('{'):
            y = y[:-1] + '%+.2f}' % -EYE if ('+' in y or '-' in y[1:]) else y[:-1] + '-1.62}'
            y = _norm(y)
        self.L.append(f'cmd execute in {dim} run tp @p {f1(x)} {f1(y)} {f1(z)}')
        self.L.append(f'face {f1(tx)} {f1(ty)} {f1(tz)}')
        self.settle(settle)
        self.L.append('wait 8 render')
        return self

    def clip(self, name, secs, **opt):
        secs = min(secs, MAX_SECS)
        if 'look' in opt and 'smooth' not in opt:
            opt['smooth'] = 1
        return self.rec(name, int(round(secs * FPS)), FPS, **opt)

    # ------------------------------------------------------------------ camera moves around a scouted box
    def orbit(self, name, secs, r, h, deg, start=45.0, look_dy=0.0, settle=420):
        """camera on a circle of radius r around the box centre, h above the box top, looking at the centre"""
        a = math.radians(start)
        dx, dz = math.sin(a) * r, -math.cos(a) * r
        self.go(v('cx', dx), v('y1', h), v('cz', dz), v('cx'), v('cy', look_dy), v('cz'), settle)
        return self.clip(name, secs, orbit=f"{v('cx')},{v('cz')},{deg}", look=f"{v('cx')},{v('cy', look_dy)},{v('cz')}")

    def flyin(self, name, secs, r0, r1, h0, h1, ang=45.0, look_dy=0.0, settle=420):
        """straight dolly towards the box centre along one direction, from distance r0/height h0 to r1/h1"""
        a = math.radians(ang)
        sx, sz = math.sin(a), -math.cos(a)
        self.go(v('cx', sx * r0), v('y1', h0), v('cz', sz * r0), v('cx'), v('cy', look_dy), v('cz'), settle)
        return self.clip(name, secs, to=f"{v('cx', sx * r1)},{v('y1', h1 - EYE)},{v('cz', sz * r1)}",
                         look=f"{v('cx')},{v('cy', look_dy)},{v('cz')}")

    def push(self, name, secs, var, d0, d1, dy=1.5, ang=0.0, settle=200, look_dy=0.5):
        """push-in on a point (fx/ox ...): from distance d0 to d1, dy above it"""
        a = math.radians(ang)
        sx, sz = math.sin(a), -math.cos(a)
        X, Y, Z = var
        self.go(v(X, sx * d0), v(Y, dy + EYE), v(Z, sz * d0), v(X), v(Y, look_dy), v(Z), settle)
        return self.clip(name, secs, to=f"{v(X, sx * d1)},{v(Y, dy)},{v(Z, sz * d1)}", look=f"{v(X)},{v(Y, look_dy)},{v(Z)}")

    def lines(self):
        return self.L + ['where']

    def part(self):
        """cut here: the script is written as several shorter runs (other tests can take the build lock between)"""
        self.L.append('#PART')
        return self

    def write_parts(self, prefix):
        """prefix1.txt, prefix2.txt ... : header + one section each"""
        head, body, parts = self.L[:self.H], self.L[self.H:], [[]]
        for l in body:
            if l == '#PART':
                parts.append([])
            else:
                parts[-1].append(l)
        for k, p in enumerate(parts):
            open(f'{prefix}{k + 1}.txt', 'w').write('\n'.join(head + p + ['where']) + '\n')
        return len(parts)


def _norm(s):
    """{y1+20.00-1.62} -> {y1+18.38}"""
    import re
    m = re.match(r'\{([a-z][a-z0-9]*)([+-][0-9.]+)?([+-][0-9.]+)\}$', s)
    if not m:
        return s
    off = float(m.group(2) or 0) + float(m.group(3))
    return v(m.group(1), off)


def _orb(self, name, secs, c, r, ey, deg, start=45.0, settle=420):
    """orbit around the fixed point c=(x, y, z): camera eye at height ey on radius r, starting at angle start"""
    cx, cy, cz = c
    a = math.radians(start)
    self.go(_add(cx, math.sin(a) * r), ey, _add(cz, -math.cos(a) * r), cx, cy, cz, settle)
    return self.clip(name, secs, orbit=f'{f1(cx)},{f1(cz)},{deg}', look=f'{f1(cx)},{f1(cy)},{f1(cz)}')


def _add(p, off):
    """number + off, or placeholder {name+o} + off"""
    if isinstance(p, str):
        import re
        m = re.match(r'\{([a-z][a-z0-9]*)([+-][0-9.]+)?\}$', p)
        return v(m.group(1), float(m.group(2) or 0) + off)
    return round(p + off, 2)


def _dolly(self, name, secs, p0, p1, look, settle=420):
    """camera eye from p0 to p1, always looking at look (fixed point)"""
    self.go(*p0, *look, settle)
    return self.clip(name, secs, to=f'{f1(p1[0])},{f1(_add(p1[1], -EYE))},{f1(p1[2])}', look=','.join(f1(x) for x in look))


def _hold(self, name, secs, **opt):
    return self.clip(name, secs, **opt)


def _summon(self, typ, n, spread=4.0, dy=0.0, nbt='', ahead=6.0):
    for k in range(n):
        a = k * 2.399
        self.L.append(f'pcmd summon {typ} ^{math.sin(a) * spread * (k > 0):.1f} ^{dy + (k % 3) * 0.6:.1f} '
                      f'^{ahead + math.cos(a) * spread * (k > 0):.1f} {nbt}'.rstrip())
    return self


def _kill(self, typ, r=80):
    # around the player: a server "kill ...distance" is measured from the world spawn in the overworld and never reached
    # the creatures summoned in the raft dimension (they piled up in bcdoc2 until 6.11.)
    self.L.append(f'pcmd kill @e[type={typ},distance=..{r}]')
    return self


def _fx(self, *names):
    """effects; night vision means under water: render distance 6 there (the water fog hides more anyway), else 10"""
    self.cmd('effect clear @p')
    for n in names:
        self.cmd(f'effect give @p minecraft:{n} infinite 0 true')
    self.L.append('rd 6' if 'night_vision' in names else 'rd 10')
    return self


def _loot(self, table, r, name, back='spectator'):
    """open the nearest container with that loot table and take its screen (spectators cannot open containers)"""
    self.cmd('gamemode creative @p')
    self.add(f'openloot {table} {r}', 'wait 8 render', f'shot {name}', 'esc')
    if back:
        self.cmd(f'gamemode {back} @p')
    return self


S2.loot = _loot
S2.orb = _orb
S2.dolly = _dolly
S2.hold = _hold
S2.summon = _summon
S2.kill = _kill
S2.fx = _fx
