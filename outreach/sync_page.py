"""Carries the user's decisions from the approval page's database back into targets.csv (never the e-mail address).

python3 sync_page.py DB_DIR    (DB_DIR = folder of the page's "targets" documents as JSON, from an ArtifactData list
                                with out_dir; each file is {"data": {...}} or the row itself)
- status, sent_on, follow_up_on and sent_via (into notes) per target id; stop/no also go into suppression.csv
The page is the source of truth for the texts (they were rewritten there in the warm tone on 7.11.2026, the files in
drafts/ keep the first drafts), so texts are not compared.
"""
import csv, glob, json, os, re, subprocess, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
db_dir = sys.argv[1]


def csv_id(doc_id):
    p, rest = doc_id.split('-', 1)
    if p in ('cf', 'mr'):
        return f'{p}:{rest.split("-", 1)[0]}'
    if p in ('yt', 'tt', 'ig'):
        return f'{p}:@{rest}'
    return doc_id


page = {}
for f in glob.glob(os.path.join(db_dir, '*.json')):
    d = json.load(open(f, encoding='utf-8'))
    page[os.path.basename(f)[:-5]] = d.get('data', d)

rows = list(csv.DictReader(open(os.path.join(HERE, 'targets.csv'), encoding='utf-8')))
fields = list(rows[0].keys())
by_id = {r['id']: r for r in rows}
changed, suppress = [], []
for doc_id, row in sorted(page.items()):
    cid = csv_id(doc_id)
    r = by_id.get(cid)
    if not r:
        print('not in targets.csv:', doc_id, '->', cid); continue
    st = row.get('status') or r['status']
    new = {'status': st, 'sent_on': row.get('sent_on') or r['sent_on'], 'follow_up_on': row.get('follow_up_on') or r['follow_up_on']}
    via = row.get('sent_via')
    if via and f'sent_via={via}' not in r['notes']:
        new['notes'] = (r['notes'] + ' | ' if r['notes'] else '') + f'sent_via={via}'
    diff = {k: v for k, v in new.items() if r.get(k, '') != v}
    if diff:
        r.update(diff); changed.append((cid, diff))
    if st in ('stop', 'no'):
        suppress.append((cid, st))

with open(os.path.join(HERE, 'targets.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
if suppress:
    sp = os.path.join(HERE, 'suppression.csv')
    have = {l.split(',', 1)[0] for l in open(sp, encoding='utf-8').read().splitlines()[1:]}
    with open(sp, 'a', encoding='utf-8') as f:
        for cid, st in suppress:
            if cid not in have:
                f.write(f'{cid},{datetime.date.today().isoformat()},{st} on the approval page\n')
for cid, diff in changed:
    print('updated', cid, diff)
print(len(changed), 'rows updated;', len(suppress), 'stop/no')
