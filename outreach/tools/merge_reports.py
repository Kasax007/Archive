"""Merges agent reports (JSON WITHOUT e-mail addresses) into creators.csv and targets.csv.

python3 merge_reports.py REPORT.json [REPORT2.json ...]
- creators -> creators.csv (CRLF, same columns), skipped if the id exists or the draft file is missing
- packs    -> targets.csv rows (status draft/hold), skipped if the id exists or the draft file is missing
Prints a summary; never reads or writes addresses (the reports must not contain any).
"""
import csv, json, os, sys, datetime, re

OUT = '/home/user/Archive/outreach'
TODAY = datetime.date.today()
EM = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}')

reports = [json.load(open(p, encoding='utf-8')) for p in sys.argv[1:]]
for p in sys.argv[1:]:
    assert not EM.search(open(p, encoding='utf-8').read().replace('discord.gg', '')), f'{p} contains an address'

cpath = os.path.join(OUT, 'creators.csv')
ccols = next(csv.reader(open(cpath, encoding='utf-8', newline='')))
cexist = {r['id'] for r in csv.DictReader(open(cpath, encoding='utf-8', newline=''))}
tpath = os.path.join(OUT, 'targets.csv')
trows = list(csv.DictReader(open(tpath, encoding='utf-8', newline='')))
tcols = list(trows[0].keys())
texist = {r['id'] for r in trows if not (r['status'] == 'new' and r['notes'].startswith('Lead'))}  # leads may be drafted

added_c, added_p, problems = [], [], []
with open(cpath, 'a', encoding='utf-8', newline='') as fh:
    w = csv.writer(fh)
    for rep in reports:
        for c in rep.get('creators', []):
            if c['id'] in cexist or c['id'] in texist:
                problems.append(f"{c['id']}: already known"); continue
            if not os.path.exists(os.path.join(OUT, c['draft'])):
                problems.append(f"{c['id']}: draft file missing ({c['draft']})"); continue
            row = {'id': c['id'], 'name': c['name'], 'platform': c['platform'], 'url': c['url'],
                   'language': c.get('language', 'en'), 'audience': c.get('audience', ''),
                   'business_route': c.get('business_route', ''), 'focus': c.get('focus', ''), 'fit': c.get('fit', ''),
                   'evidence': c.get('evidence', ''), 'evidence_url': c.get('evidence_url', ''),
                   'evidence_month': c.get('evidence_month', ''), 'last_checked': TODAY.isoformat()}
            w.writerow([row.get(k, '') for k in ccols])
            cexist.add(c['id']); added_c.append(c['id'])

for rep in reports:
    for p in rep.get('packs', []):
        if p['id'] in texist:
            problems.append(f"{p['id']}: already in targets.csv"); continue
        trows = [r for r in trows if r['id'] != p['id']]   # a lead row is replaced by the drafted pack
        if not os.path.exists(os.path.join(OUT, p['draft'])):
            problems.append(f"{p['id']}: draft file missing ({p['draft']})"); continue
        trows.append({'id': p['id'], 'type': 'pack', 'name': p['name'], 'platform': p['platform'], 'url': p['url'],
                      'contact_route': p.get('contact_route', ''), 'score': str(p.get('score', '')),
                      'status': p.get('status', 'draft'), 'first_seen': TODAY.isoformat(), 'sent_on': '',
                      'follow_up_on': '', 'notes': f'Gefunden {TODAY.day}.{TODAY.month}.{TODAY.year} (tägliche Routine, breite Suche: auch 1.21.1/1.20.1, große Packs).',
                      'delete_after': (TODAY + datetime.timedelta(days=182)).isoformat(), 'fit': p.get('fit', ''),
                      'why': p.get('why', '')})
        texist.add(p['id']); added_p.append(p['id'])

w = csv.DictWriter(open(tpath, 'w', encoding='utf-8', newline=''), fieldnames=tcols)
w.writeheader(); w.writerows(trows)
print(f'creators added: {len(added_c)}; packs added: {len(added_p)}')
for x in problems:
    print('  !', x)
