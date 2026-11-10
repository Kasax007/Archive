"""Adds the candidates a research run rejected to targets.csv: status skip with the reason in notes, or status new with
a "Lead <date>:" note for good candidates that only missed out on the day's HOLD quota. Never touches known ids.
python3 add_skips.py WORKFLOW_OUTPUT.json LEAD_ID [LEAD_ID ...]   (reads only the 'skipped' lists, no addresses)"""
import csv, json, os, re, sys, datetime
OUT = '/home/user/Archive/outreach'
TODAY = datetime.date.today()
D = f'{TODAY.day}.{TODAY.month}.{TODAY.year}'
EM = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}')
IDRE = re.compile(r'(?:yt|tt|ig):@[\w.\-]*\w|cf:\d+|mr:[A-Za-z0-9]{8}')
res = json.load(open(sys.argv[1]))['result']
leads = set(sys.argv[2:])
tpath = os.path.join(OUT, 'targets.csv')
rows = list(csv.DictReader(open(tpath, encoding='utf-8', newline='')))
cols = list(rows[0].keys())
known = {r['id'] for r in rows}
known |= {r['id'] for r in csv.DictReader(open(os.path.join(OUT, 'creators.csv'), encoding='utf-8', newline=''))}
known |= {r['key'] for r in csv.DictReader(open(os.path.join(OUT, 'suppression.csv'), encoding='utf-8', newline=''))}
drafts = os.listdir(os.path.join(OUT, 'drafts'))
def stem(i):
    p, rest = i.split(':', 1)
    return p + '-' + rest.replace('@', '')
wide = {c['id']: c for c in json.load(open(os.path.join(OUT, 'data/wide_candidates.json')))['candidates']}
added = {}
for s in res:
    for line in (s.get('report') or {}).get('skipped', []):
        if line.startswith('NO DRAFTS') or ' note:' in line[:40]:
            continue
        line = EM.sub('<Adresse>', line)
        head, tail = line.split(': ', 1) if ': ' in line else (line, line)
        for i in IDRE.findall(head):
            if i in known or i in added or any(f.startswith(stem(i)) for f in drafts):
                continue
            p = i.split(':')[0]
            plat = {'yt': 'youtube', 'tt': 'tiktok', 'ig': 'instagram', 'cf': 'curseforge', 'mr': 'modrinth'}[p]
            handle = i.split('@', 1)[1] if '@' in i else ''
            w = wide.get(i, {})
            m = re.search(re.escape(i) + r'\s*\(([^,)]+)', line)
            name = handle or w.get('name') or (m.group(1).strip() if m else i)
            url = {'youtube': f'https://www.youtube.com/@{handle}', 'tiktok': f'https://www.tiktok.com/@{handle}',
                   'instagram': f'https://www.instagram.com/{handle}/'}.get(plat) or w.get('url') or (
                   f'https://www.curseforge.com/projects/{i[3:]}' if p == 'cf' else f'https://modrinth.com/modpack/{i[3:]}')
            lead = i in leads
            m2 = re.search(re.escape(i) + r'\s*(\([^)]*\))', head)
            reason = (m2.group(1) + ' ' if m2 else '') + tail
            added[i] = {'id': i, 'type': 'pack' if p in ('cf', 'mr') else 'creator', 'name': name, 'platform': plat,
                        'url': url, 'contact_route': '', 'score': '', 'status': 'new' if lead else 'skip',
                        'first_seen': TODAY.isoformat(), 'sent_on': '', 'follow_up_on': '',
                        'notes': (f'Lead {D}: ' if lead else f'Geprüft {D}, verworfen: ') + reason[:300],
                        'delete_after': '', 'fit': '', 'why': ''}
missing = leads - set(added)
rows += list(added.values())
w = csv.DictWriter(open(tpath, 'w', encoding='utf-8', newline=''), fieldnames=cols)
w.writeheader(); w.writerows(rows)
print(f"{len(added)} rows added: {sum(r['status']=='skip' for r in added.values())} skip, "
      f"{sum(r['status']=='new' for r in added.values())} leads; leads not found: {sorted(missing)}")
