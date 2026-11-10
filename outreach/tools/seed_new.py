"""Prepares DB rows for drafts that are not in the page database yet (no addresses involved).

python3 seed_new.py EXISTING_IDS.txt
1. Copies the score from targets.csv into each new draft's "Ziel" line (creators are re-scored by score.py).
2. Runs seed_page.py, keeps only ids missing from EXISTING_IDS.txt, adds tone/updated_by, writes one JSON per row to
   $SP/outreach_new/<id>.json and prints the ArtifactData batch entries (chunks of 50) as JSON.
"""
import csv, json, os, re, subprocess, sys

SP = os.environ.get('SP', '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad')  # scratch dir for temp files
OUT = '/home/user/Archive/outreach'
existing = {l.strip() for l in open(sys.argv[1]) if l.strip()}
only = {l.strip() for l in open(sys.argv[2]) if l.strip()} if len(sys.argv) > 2 else None

scores = {r['id']: r['score'] for r in csv.DictReader(open(os.path.join(OUT, 'targets.csv'), encoding='utf-8'))}


def file_to_id(fn):
    key = fn[:-3]
    p, rest = key.split('-', 1)
    if p in ('cf', 'mr'):
        return key, f'{p}:{rest.split("-", 1)[0]}'
    return key, f'{p}:@{rest}'


changed = 0
for fn in sorted(os.listdir(os.path.join(OUT, 'drafts'))):
    if not fn.endswith('.md') or fn == 'README.md':
        continue
    key, tid = file_to_id(fn)
    if key in existing or (only is not None and key not in only) or tid not in scores or not scores[tid]:
        continue
    path = os.path.join(OUT, 'drafts', fn)
    s = open(path, encoding='utf-8').read()
    s2 = re.sub(r'(^\| Ziel \|[^\n]*?· Score )(\d+)', lambda m: m.group(1) + scores[tid], s, count=1, flags=re.M)
    if s2 != s:
        open(path, 'w', encoding='utf-8').write(s2); changed += 1
print(f'scores updated in {changed} drafts', file=sys.stderr)

subprocess.run(['python3', os.path.join(OUT, 'seed_page.py'), f'{SP}/outreach_seed.json'], check=True,
               stdout=sys.stderr)
rows = json.load(open(f'{SP}/outreach_seed.json', encoding='utf-8'))['targets']
os.makedirs(f'{SP}/outreach_new', exist_ok=True)
new = []
for k, r in sorted(rows.items()):
    if k in existing or (only is not None and k not in only):
        continue
    r = dict(r, tone='warm-2026-11-07', updated_by='claude')
    json.dump(r, open(f'{SP}/outreach_new/{k}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    new.append(k)
print(f'{len(new)} new rows: ' + ', '.join(new), file=sys.stderr)
batches = [[{'op': 'set', 'collection': 'targets', 'doc_id': k, 'file_path': f'{SP}/outreach_new/{k}.json'}
            for k in new[i:i + 50]] for i in range(0, len(new), 50)]
print(json.dumps(batches))
