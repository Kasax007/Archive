"""Summarise audit reports: per structure the sum over its instances (solid/fluid/deco intrusions, missing,
foreign replacements, loose blocks, items) and the people check."""
import glob, re, sys, collections
def parse(dirs):
    rows = collections.OrderedDict()
    for d in dirs:
        for f in sorted(glob.glob(d + '/audit/*.txt')):
            line = next((l for l in open(f) if l.startswith('AUDIT')), None)
            if not line:
                continue
            m = re.match(r'AUDIT (\S+) raft:(\S+) at', line)
            if not m:
                rows.setdefault(re.match(r'AUDIT \S+ raft:(\S+)', line).group(1), []).append(None); continue
            s = m.group(2)
            def num(key):
                mm = re.search(r'\| ' + key + r' (\d+) \[([^\]]*)\]', line)
                return (int(mm.group(1)), mm.group(2)) if mm else (0, '')
            npc = re.search(r'npc (\d+)/(\d+) ok', line)
            follow = re.search(r'\((\d+) follow the terrain\)', line)
            rows.setdefault(s, []).append(dict(solid=num('solid'), fluid=num('fluid'), deco=num('deco'),
                                               missing=num('missing'), loose=num('loose'),
                                               items=num('items'), npc=(int(npc.group(1)), int(npc.group(2))) if npc else (0, 0),
                                               follow=int(follow.group(1)) if follow else 0))
    return rows
def table(rows):
    out = ['| Struktur | Orte | Fremdblöcke in Räumen | Wasser/Lava in Räumen | Pflanzen in Räumen | NPC in Ordnung | Items |', '|---|---|---|---|---|---|---|']
    for s, inst in rows.items():
        inst = [i for i in inst if i]
        if not inst:
            continue
        sol = sum(i['solid'][0] for i in inst); flu = sum(i['fluid'][0] for i in inst); dec = sum(i['deco'][0] for i in inst)
        no, nt = sum(i['npc'][0] for i in inst), sum(i['npc'][1] for i in inst)
        it = sum(i['items'][0] for i in inst)
        out.append(f'| {s} | {len(inst)} | {sol} | {flu} | {dec} | {f"{no}/{nt}" if nt else "–"} | {it} |')
    return '\n'.join(out)
if __name__ == '__main__':
    print(table(parse(sys.argv[1:])))
