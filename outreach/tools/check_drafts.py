"""Quality check for new drafts: parse like seed_page.py, forbidden phrases, casino, Bob wording, length, addresses."""
import json, os, re, subprocess, sys
SP = os.environ.get('SP', '/tmp/claude-0/-home-user/4ca9508b-4f8c-5a8e-91dc-6059d6cc887c/scratchpad')  # scratch dir for temp files
OUT = '/home/user/Archive/outreach'
keys = sys.argv[1:]
TMP = f'{SP}/check_seed_{os.getpid()}.json'   # one file per run: several agents may check at the same time
subprocess.run(['python3', f'{OUT}/seed_page.py', TMP], check=True, stdout=subprocess.DEVNULL)
rows = json.load(open(TMP, encoding='utf-8'))['targets']
os.remove(TMP)
EM = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}')
FORBID = ["no pressure", "one message only", "one-off message", "reply stop", "no payment", "no obligations",
          "why you got this", "won't follow up", "i won't write again"]
for k in keys:
    r = rows.get(k)
    raw = open(f'{OUT}/drafts/{k}.md', encoding='utf-8').read()
    probs = []
    if not r: print(f'{k:28} NOT PARSED'); continue
    msg = r['message']; low = (msg + ' ' + r['followup'] + ' ' + r['subject']).lower()
    words = len(msg.split())
    if EM.search(raw.replace('discord.gg', '')): probs.append('ADDRESS IN FILE')
    for f in FORBID:
        if f in low: probs.append('forbidden:' + f)
    if 'casino' in low or 'gambl' in low or 'house always wins' in low: probs.append('CASINO')
    if re.search(r'\bbob\b', low) and not re.search(r'early[ -]stage|frühe[nm]? (entwicklungs|stadium|phase)|early development|noch ganz am anfang|frühen phase|frühes stadium', low): probs.append('BOB without early-stage')
    if not (60 <= words <= 200): probs.append(f'words={words}')
    if r['channel'].lower().startswith('e-mail'):
        if not r['subject']: probs.append('no subject')
        if '{postal_address}' not in r['footer']: probs.append('no footer')
        if not re.search(r'(warm wishes|herzliche grüße|liebe grüße|viele grüße)', msg.lower()): probs.append('no warm sign-off')
    if not r['followup']: probs.append('no followup')
    if not r['facts']: probs.append('no facts')
    print(f"{k:28} {r['status']:5} score={r['score']:<3} {r['channel'][:22]:22} words={words:<3} {'OK' if not probs else ' | '.join(probs)}")
