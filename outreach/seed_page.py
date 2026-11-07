"""Turns the drafts in drafts/*.md into rows for the approval page's database (collection "targets").

python3 seed_page.py OUT.json            -> JSON {"targets": {id: row}} for ArtifactData batch writes
Each row: name, type, platform, url, score, status, fit, route, why, before, facts[], channel, subject, message,
footer, followup, status_note. Drafts without a "## Text" section (pointer files) are skipped.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1]
rows = {}
for fn in sorted(os.listdir(os.path.join(HERE, 'drafts'))):
    if not fn.endswith('.md') or fn == 'README.md':
        continue
    s = open(os.path.join(HERE, 'drafts', fn), encoding='utf-8').read()
    if '\n## Text' not in s:
        continue
    key = fn[:-3]
    name = re.search(r'^# (.+)$', s, re.M).group(1).strip()
    table = dict(re.findall(r'^\| ([^|]+?) \| (.+?) \|$', s, re.M))
    ziel = table.get('Ziel', '')
    url = (re.search(r'\]\((https?://[^)]+)\)', ziel) or [None, ''])[1]
    score = int((re.search(r'Score (\d+)', ziel) or [None, 0])[1])
    status_note = table.get('Status', '')
    status = 'hold' if status_note.upper().startswith('HOLD') else 'draft'
    facts = []
    m = re.search(r'\*\*Belege\*\*[^\n]*\n\n(.*?)\n\n', s, re.S)
    if m:
        facts = [re.sub(r'^- ', '', l).strip() for l in m.group(1).split('\n') if l.startswith('- ')]
    text_sec = re.search(r'\n## Text \((.*?)\)\n(.*?)(?=\n## |\Z)', s, re.S)
    channel, body = text_sec.group(1), text_sec.group(2)
    subject = (re.search(r'\*\*Subject:\*\* (.+)', body) or [None, ''])[1].strip()
    def quote(block):
        lines = [l[2:] if l.startswith('> ') else ('' if l.strip() == '>' else None) for l in block.split('\n')]
        return '\n'.join(l for l in lines if l is not None).strip()
    parts = re.split(r'\*\*Fußzeile:\*\*', body)
    message = quote(parts[0].split('**Subject:**')[-1] if '**Subject:**' in parts[0] else parts[0])
    message = re.sub(r'^.*?\n(?=Hi |Hello |Hey )', '', message, count=1, flags=re.S) if not message.startswith(('Hi', 'Hello', 'Hey')) and re.search(r'\n(Hi |Hello |Hey )', message) else message
    footer = quote(parts[1]) if len(parts) > 1 else ''
    fu = re.search(r'\n## Nachfrage[^\n]*\n(.*?)(?=\n## |\Z)', s, re.S)
    followup = quote(fu.group(1)) if fu else ''
    prefix = key.split('-')[0]
    rows[key] = dict(
        name=name, type='creator' if prefix == 'yt' else 'pack',
        platform={'cf': 'CurseForge', 'mr': 'Modrinth', 'yt': 'YouTube'}.get(prefix, prefix), url=url, score=score,
        status=status, status_note=status_note, fit=table.get('Passt', ''), route=table.get('Kontaktweg', ''),
        why=table.get('Warum eingeladen', ''), before=table.get('Vor dem Senden', ''), facts=facts,
        channel=channel, subject=subject, message=message, footer=footer, followup=followup,
        sent_on='', follow_up_on='', updated_by='claude')
json.dump({'targets': rows}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(rows), 'rows;', sum(r['status'] == 'hold' for r in rows.values()), 'hold;',
      sum(r['type'] == 'creator' for r in rows.values()), 'creators')
