#!/usr/bin/env python3
"""Score outreach candidates (0-100) and keep targets.csv, the outreach table, up to date.

    python3 score.py              # score data/candidates.json, update targets.csv, print a summary
    python3 score.py --top 25     # also list the 25 best open targets
    python3 score.py --due        # follow-ups due (status sent, follow_up_on reached)
    python3 score.py --kpi        # weekly KPI numbers from targets.csv

Never sends anything. Scheme from research/curseforge-wachstum-2026-11.md, section 3.5:
26.2/26.3 Fabric is required; content pack 25, last update <= 30 days 20, downloads 500-100,000 15,
gap for one of our mods 20, invited contact route 15, English or German 5. Partial points where the
evidence is partial (documented in README.md). Creators use the same weights, mapped in score_creator().

The user edits targets.csv by hand: status, sent_on, notes. score.py keeps those fields, fills
follow_up_on (sent_on + 7 days) and delete_after, moves 'stop' and 'no' to suppression.csv and never
writes a row for anything that matches suppression.csv.
"""
import argparse
import csv
import datetime as dt
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, 'config.json'), encoding='utf-8'))
S, LIM = CFG['score'], CFG['limits']
TODAY = dt.date.today()
TARGETS = os.path.join(HERE, 'targets.csv')
SUPPRESSION = os.path.join(HERE, 'suppression.csv')
CANDIDATES = os.path.join(HERE, 'data', 'candidates.json')
COLUMNS = ['id', 'type', 'name', 'platform', 'url', 'contact_route', 'score', 'status', 'first_seen', 'sent_on',
           'follow_up_on', 'notes', 'delete_after', 'fit', 'why']
SUP_COLUMNS = ['key', 'added_on', 'reason']
STATUSES = ['new', 'hold', 'draft', 'approved', 'sent', 'followed_up', 'replied', 'yes', 'no', 'stop', 'skip']
OPEN = {'new', 'draft', 'approved'}
AUTO = {'new', 'hold', 'draft', 'skip'}          # statuses the script may change on its own
CONTENT_CATS = set(CFG['cf_content_categories']) | set(CFG['mr_content_categories'])


def days_since(iso):
    try:
        return (TODAY - dt.date.fromisoformat(str(iso)[:10])).days
    except ValueError:
        return 9999


def add_days(iso, n):
    return (dt.date.fromisoformat(iso[:10]) + dt.timedelta(days=n)).isoformat()


def read_csv(path, columns):
    try:
        with open(path, encoding='utf-8', newline='') as fh:
            return [{k: (r.get(k) or '').strip() for k in columns} for r in csv.DictReader(fh)]
    except OSError:
        return []


def write_csv(path, columns, rows):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=columns, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, path)


COSMETIC = re.compile(r'actions? ?(?:&|and) ?stuffs?|cosmetic|animations?|visuals?|bedrock|resource ?packs?|realism|client|'
                      r'\bqol\b|quality of life|essentials?\b|utilit', re.I)
STRONG_CATS = {'Adventure and RPG', 'Quests', 'Tech', 'Magic', 'Skyblock', 'Expert', 'Extra Large', 'Sci-Fi',
               'adventure', 'quests', 'technology', 'magic', 'kitchen-sink', 'challenging'}
STRONG_PERF = re.compile(r'\b(fps|pvp|lag)\b|optimi[sz]|performance|boost', re.I)
CONTENT_THEMES = ('structures', 'worldgen', 'dimensions', 'mobs', 'magic', 'tech', 'rpg_combat', 'farming_food')


def perf_hit(name, summary=''):
    """Performance, shader, PvP or cosmetic pack? The name counts fully, the summary only with strong words."""
    low = (name or '').lower()
    return (any(k in low for k in CFG['perf_keywords'] if len(k) > 3) or bool(re.search(r'\b(fps|pvp|hud|lag)\b', low))
            or bool(COSMETIC.search(name or '')) or bool(STRONG_PERF.search(summary or '')))


def content_level(c):
    """25 = content pack, 10 = light or mixed content, 0 = performance, shader, PvP or cosmetic pack."""
    cats = set(c['categories'])
    tagged = bool(cats & CONTENT_CATS)
    perf = perf_hit(c['name'], c.get('summary'))
    cosmetic = bool(COSMETIC.search(c['name'] + ' ' + (c.get('summary') or '')))
    mods = c.get('mods')
    if not mods or mods.get('unknown'):           # mod list not readable: categories and name only
        if perf or cosmetic or not tagged:
            return 0, None
        return (S['content'] if cats & STRONG_CATS else S['content_mixed']), None
    cm = sum(mods.get('theme_counts', {}).get(t, 0) for t in CONTENT_THEMES)
    count = mods.get('count') or 0
    if cosmetic or perf:
        level = S['content'] if cm >= 20 and count >= 150 else S['content_mixed'] if cm >= 8 else 0
    elif cm >= 8:
        level = S['content']
    elif tagged and (cm >= 3 or count >= 80):
        level = S['content_mixed']
    else:
        level = 0
    return level, cm


def short(n):
    return f'{n / 1000:.1f}k' if n >= 1000 else str(n)


# ---------------------------------------------------------------- packs

def gap_and_fit(c, content):
    """Which of our mods fill a real gap, and the points for it (scaled by how much of a content pack it is)."""
    if content == 0:
        return [], 0, 'not a content pack: no gap for gameplay mods'
    mods = c.get('mods')
    vers = set(c['mc_versions'])
    cats = set(c['categories'])
    full = content == S['content']
    has263 = '26.3' in vers
    qi_ok = has263 or '26.2' in vers                     # Quest Icons for 26.2 is being built
    if not mods or mods.get('unknown'):
        ours = (mods or {}).get('ours', [])
        fit = [p for p in (['QI'] if qi_ok else []) + (['BC', 'TG'] if has263 else []) if p not in ours]
        return fit, S['gap_unknown'] if fit else 0, 'mod list not checked'
    ours, tc = mods['ours'], mods.get('theme_counts', {})
    blob = (c['name'] + ' ' + (c.get('summary') or '')).lower()
    qi_gap = qi_ok and not mods['quest'] and not mods.get('quest_dirs') and 'QI' not in ours
    bc_gap = has263 and not mods['raft'] and 'BC' not in ours
    tg_gap = has263 and 'TG' not in ours
    bc_theme = (tc.get('structures', 0) + tc.get('worldgen', 0) + tc.get('dimensions', 0) >= 5
                or (full and bool(cats & set(CFG['bc_theme_categories']))))
    tg_theme = (tc.get('mobs', 0) >= 2 or tc.get('farming_food', 0) >= 3 or bool(mods['pet'])
                or 'cozy' in blob or 'farm' in blob)
    notes = []
    if mods['quest']:
        notes.append('has quest book: ' + ', '.join(mods['quest'][:2]))
    elif mods.get('quest_dirs'):
        notes.append('quest config in overrides: ' + ', '.join(mods['quest_dirs'][:2]))
    elif qi_gap:
        notes.append(f"no quest book in {mods['count']} mods")
    if mods['side_quest']:
        notes.append('side quests: ' + ', '.join(mods['side_quest'][:2]))
    if mods['quest_maybe']:
        notes.append('check: ' + ', '.join(mods['quest_maybe'][:2]))
    if mods['pet']:
        notes.append('pet mods: ' + ', '.join(mods['pet'][:2]))
    if ours:
        notes.append('already uses ' + '+'.join(ours))
    fit = (['QI'] if qi_gap else []) + (['BC'] if bc_gap and bc_theme else []) + (['TG'] if tg_gap and tg_theme else [])
    if qi_gap:
        gap = (S['gap_theme'] if mods['quest_maybe'] else S['gap_qi']) if full else S['gap_other']
    elif fit:
        gap = S['gap_theme'] if full else S['gap_other']
    else:
        gap = 0
    return fit, gap, '; '.join(notes)


def contact_route(c):
    sig = c.get('signals') or {}
    checks = c.get('discord_check')
    ok = [d for d in checks or [] if d.get('ok')]
    dead = [d for d in checks or [] if d.get('ok') is False]
    unchecked = [d for d in checks or [] if d.get('ok') is None]
    if checks is None:                                    # route check not run for this candidate
        unchecked = [{'code': x} for x in sig.get('discord_codes', [])]
    issues = (c.get('links') or {}).get('issues')
    templates = c.get('github_templates') or {}
    if not issues and templates:
        issues = 'https://github.com/' + next(iter(templates)) + '/issues'
    mod_tpl = [f'{r}: {n}' for r, ns in templates.items() for n in ns if 'mod' in n]
    sug_tpl = [f'{r}: {n}' for r, ns in templates.items() for n in ns if 'mod' not in n]
    strong = [i['text'] for i in sig.get('invites', []) if i['kind'] == 'suggestions']
    feedback = [i['text'] for i in sig.get('invites', []) if i['kind'] == 'feedback']
    # CurseForge pages have a comments tab: an author who asks for mod ideas "in the comments" invites them there
    comment_invite = c.get('platform') == 'curseforge' and any('comment' in t.lower() for t in strong + feedback)
    reachable = bool(ok or unchecked or issues or sig.get('discord_short') or comment_invite)
    routes = []
    if mod_tpl:
        routes.append((S['route_invited'], 'GitHub issue template for mod suggestions (' + mod_tpl[0] + ')'))
    if strong and reachable:
        routes.append((S['route_invited'], 'page invites suggestions: "' + strong[0][:140] + '"'))
    if sug_tpl:
        routes.append((S['route_feedback'], 'GitHub suggestion/feature template (' + sug_tpl[0] + ')'))
    if feedback and reachable:
        routes.append((S['route_feedback'], 'page asks for feedback: "' + feedback[0][:140] + '"'))
    if issues:
        routes.append((S['route_issues'], 'issue tracker ' + issues))
    if ok:
        d = ok[0]
        members = f", ~{d['members']} members" if d.get('members') else ''
        routes.append((S['route_discord'], f"Discord \"{d.get('guild')}\"{members} (discord.gg/{d['code']}): "
                                           "suggestion channel only, if its rules allow"))
    elif unchecked:
        routes.append((S['route_discord'], f"Discord discord.gg/{unchecked[0]['code']} (invite not checked)"))
    elif sig.get('discord_short'):
        routes.append((S['route_discord'], f"Discord {sig['discord_short'][0]} (redirect link, not checked)"))
    if not routes:
        none = 'none found' + (' (Discord invite expired)' if dead else '')
        if c.get('platform') == 'curseforge':
            none += ' in the description: check the CurseForge page sidebar (Discord, Issues) by hand'
        return 0, none
    routes.sort(key=lambda r: -r[0])
    also = '; '.join(r[1] for r in routes[1:3])
    return routes[0][0], routes[0][1] + (f' | also: {also}' if also else '')


def score_pack(c):
    content, cm = content_level(c)
    age = days_since(c['updated'])
    fresh = S['fresh'] if age <= S['fresh_days'] else 0
    dl = S['downloads'] if S['dl_min'] <= c['downloads'] <= S['dl_max'] else 0
    fit, gap, gap_note = gap_and_fit(c, content)
    route_pts, route = contact_route(c)
    lang = S['language'] if c.get('language') in S['languages'] else 0
    total = content + fresh + dl + gap + route_pts + lang
    shown = sorted(set(c['categories']) & CONTENT_CATS)[:3]
    mods = c.get('mods') or {}
    why = [f"content {content} ({', '.join(shown) or 'no content category'}; "
           f"{mods.get('count', '?')} mods, {cm if cm is not None else '?'} content mods)",
           f"fresh {fresh} (updated {c['updated']})",
           f"downloads {dl} ({c['downloads']:,})",
           f"gap {gap} ({gap_note})",
           f"route {route_pts}",
           f"lang {lang} ({c.get('language')})",
           'MC ' + '/'.join(c['mc_versions'])]
    if c.get('twin'):
        why.append('also ' + c['twin'])
    if c.get('mods_note'):
        why.append(c['mods_note'])
    return total, fit, route, ' | '.join(why), route_pts


def pack_status(c, fit, route_pts):
    if not fit:
        return 'skip', 'no gap for our mods'
    if route_pts == 0 and c['platform'] != 'curseforge':   # Modrinth shows all project links; CurseForge hides the sidebar
        return 'skip', 'no contact route found'
    if c['platform'] == 'modrinth' and not any(p.get('modrinth_id') for p in CFG['projects'].values()):
        return 'hold', 'Modrinth only: our mods are not on Modrinth yet (report step 3)'
    if fit == ['QI'] and '26.3' not in c['mc_versions']:
        return 'hold', 'only 26.2: wait for the Quest Icons 26.2 build'
    return 'new', ''


# ---------------------------------------------------------------- creators

def audience(text):
    m = re.search(r'([\d.]+)\s*([KkMm]?)', text or '')
    if not m:
        return None
    return float(m.group(1)) * {'': 1, 'k': 1e3, 'm': 1e6}[m.group(2).lower()]


def score_creator(c):
    focus = (c.get('focus') or '').lower()
    content = S['content'] if re.search(r'mod|modpack|modded', focus) else S['content_mixed']
    month = c.get('evidence_month') or ''
    if re.fullmatch(r'\d{4}-\d{2}', month):
        age = days_since(month + '-01')
        fresh = S['fresh'] if age <= 62 else (S['fresh'] // 2 if age <= 183 else 0)
    else:
        fresh = 0
    aud = audience(c.get('audience'))
    dl = S['downloads'] if aud and S['creator_audience_min'] <= aud <= S['creator_audience_max'] else 0
    ev = (c.get('evidence') or '') + ' ' + focus
    gap = S['gap_qi'] if re.search(r'26\.[123]|raft|ocean|quest|cozy|stardew|modpacks? of 2026', ev, re.I) else S['gap_other']
    route = c.get('route') or ''
    route_pts = 0 if route.lower().startswith('none') or not route else S['route_invited']
    lang = S['language'] if (c.get('language') or '')[:2] in S['languages'] else 0
    total = content + fresh + dl + gap + route_pts + lang
    why = (f"content {content} ({c.get('focus')}) | fresh {fresh} (evidence {month or '?'}) | audience {dl} "
           f"({c.get('audience') or '?'}) | fit {gap} | route {route_pts} | lang {lang} ({c.get('language')}) | "
           f"evidence: {c.get('evidence')}")
    # address only behind YouTube's "View email address" button (captcha): hold, prefer creators with a public address
    captcha_only = bool(re.search(r'view email address|captcha', route, re.I)
                        and not re.search(r'description (lists|gives|names)|in the description', route, re.I))
    if captcha_only:
        why = "hold: address only behind YouTube's View email address button (captcha) | " + why
    status = ('hold' if captcha_only else 'new') if route_pts else 'skip'
    return total, c.get('fit', '').replace(';', '+'), route or 'none found', why, status


# ---------------------------------------------------------------- table upkeep

def draft_prefix(tid):
    return re.sub(r'[^A-Za-z0-9_-]+', '-', tid.replace('@', '')).strip('-')


def has_draft(tid):
    return bool(glob.glob(os.path.join(HERE, 'drafts', draft_prefix(tid) + '*.md')))


def suppressed(row, cand, keys):
    if row['id'].lower() in keys or row['url'].lower() in keys:
        return True
    return any(f'author:{a}'.lower() in keys for a in (cand or {}).get('authors', []))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--top', type=int, default=10)
    ap.add_argument('--due', action='store_true')
    ap.add_argument('--kpi', action='store_true')
    args = ap.parse_args()

    data = json.load(open(CANDIDATES, encoding='utf-8')) if os.path.exists(CANDIDATES) else {'candidates': []}
    cands = {c['id']: c for c in data['candidates']}
    old = {r['id']: r for r in read_csv(TARGETS, COLUMNS)}
    sup = read_csv(SUPPRESSION, SUP_COLUMNS)
    if not os.path.exists(SUPPRESSION):
        write_csv(SUPPRESSION, SUP_COLUMNS, [])

    # 1. 'stop' and 'no' go to the suppression list and leave the table (GDPR Art. 21, UWG)
    added = []
    for r in list(old.values()):
        if r['status'] in ('stop', 'no'):
            reason = 'objection (stop)' if r['status'] == 'stop' else 'declined'
            keys = [r['id'], r['url']] + [f'author:{a}' for a in cands.get(r['id'], {}).get('authors', [])]
            for k in keys:
                if k and k.lower() not in {s['key'].lower() for s in sup + added}:
                    added.append({'key': k, 'added_on': TODAY.isoformat(), 'reason': reason})
            del old[r['id']]
    if added:
        write_csv(SUPPRESSION, SUP_COLUMNS, sup + added)
        sup += added
    keys = {s['key'].lower() for s in sup if s['key']}

    # 2. score every candidate; a pack listed on both platforms appears once (as the CurseForge project)
    rows, seen = {}, set()
    for cid, c in cands.items():
        if c['type'] == 'pack':
            if c['platform'] == 'modrinth' and c.get('twin', '').startswith('cf:') and c['twin'] in cands:
                continue
            total, fit, route, why, route_pts = score_pack(c)
            status, status_why = pack_status(c, fit, route_pts)
            if status_why:
                why = status_why + ' | ' + why
        else:
            total, fit, route, why, status = score_creator(c)
            fit = fit.split('+') if fit else []
        row = {'id': cid, 'type': c['type'], 'name': c['name'], 'platform': c['platform'], 'url': c['url'],
               'contact_route': route, 'score': str(total), 'status': status,
               'first_seen': c.get('first_seen') or c.get('last_checked') or TODAY.isoformat(),
               'sent_on': '', 'follow_up_on': '', 'notes': '', 'delete_after': '',
               'fit': '+'.join(fit) if isinstance(fit, list) else fit, 'why': why}
        prev = old.get(cid)
        manual_skip = bool(prev and prev['status'] == 'skip' and prev['notes'])
        if prev:
            for k in ('sent_on', 'follow_up_on', 'notes', 'delete_after'):
                row[k] = prev[k]
            row['first_seen'] = prev['first_seen'] or row['first_seen']
            if prev['status'] not in AUTO:
                row['status'] = prev['status']
                row['contact_route'] = prev['contact_route'] or route
            elif manual_skip:
                row['status'] = 'skip'                     # skipped by hand (reason in notes) stays skipped
        if row['status'] in AUTO and not manual_skip and has_draft(cid):
            row['status'] = 'hold' if row['status'] == 'hold' else 'draft'   # a draft file means someone chose it
        seen.add(cid)
        if suppressed(row, c, keys):
            continue
        rows[cid] = row
    # rows that discovery no longer returns (pack left 26.x, fell below the limits) stay only while someone
    # works with them (status set by the user, a note or a draft); untouched rows are dropped (data minimisation)
    for cid, r in old.items():
        if cid in seen or suppressed(r, cands.get(cid), keys):
            continue
        if r['status'] not in AUTO or r['notes'] or has_draft(cid):
            rows[cid] = r

    # one owner with several packs gets one message, not several
    by_owner = {}
    for cid, r in rows.items():
        owner = (cands.get(cid, {}).get('authors') or [''])[0].lower()
        if owner and r['type'] == 'pack':
            by_owner.setdefault(owner, []).append(cid)
    for ids in by_owner.values():
        if len(ids) > 1:
            for cid in ids:
                others = [rows[o]['name'].strip() for o in ids if o != cid]
                note = f"same owner as {', '.join(others[:3])}{' …' if len(others) > 3 else ''}: send one message"
                if not rows[cid]['why'].startswith('same owner'):
                    rows[cid]['why'] = note + ' | ' + rows[cid]['why']

    # 3. dates: follow-up 7 days after sending; delete after 6 months (data minimisation)
    removed = []
    for cid, r in list(rows.items()):
        if r['sent_on'] and not r['follow_up_on']:
            r['follow_up_on'] = add_days(r['sent_on'], LIM['follow_up_days'])
        if r['status'] == 'yes':
            r['delete_after'] = ''
        elif r['sent_on']:
            r['delete_after'] = add_days(r['sent_on'], LIM['delete_after_days'])
        elif not r['delete_after']:
            r['delete_after'] = add_days(r['first_seen'] or TODAY.isoformat(), LIM['delete_after_days'])
        if r['delete_after'] and days_since(r['delete_after']) > 0:
            removed.append(r)
            del rows[cid]

    order = {s: i for i, s in enumerate(['approved', 'draft', 'new', 'sent', 'followed_up', 'replied', 'yes', 'hold', 'skip'])}
    scored = sorted(rows.values(), key=lambda r: (order.get(r['status'], 9), -int(r['score'] or 0), r['name'].lower()))
    # the table keeps qualified targets and everything someone works with; the rest is rebuilt on every run
    out = [r for r in scored if (int(r['score'] or 0) >= S['qualified'] and r['status'] != 'skip')
           or r['status'] not in AUTO or r['notes'] or has_draft(r['id'])]
    write_csv(TARGETS, COLUMNS, out)

    # 4. summary
    packs = [r for r in scored if r['type'] == 'pack']
    creators = [r for r in scored if r['type'] == 'creator']
    q = lambda rs: [r for r in rs if int(r['score'] or 0) >= S['qualified']]
    counts = data.get('counts', {})
    print(f"Candidates: {counts}")
    act = lambda rs: [r for r in q(rs) if r['status'] not in ('hold', 'skip')]
    print(f"Scored {len(packs)} packs: {len(q(packs))} with score >= {S['qualified']} "
          f"({len(act(packs))} actionable now, {sum(1 for r in q(packs) if r['status'] == 'hold')} on hold, "
          f"{sum(1 for r in q(packs) if r['status'] == 'skip')} skipped: no route, no gap or checked by hand); "
          f"{len(creators)} creators, {len(q(creators))} with score >= {S['qualified']}. targets.csv: {len(out)} rows")
    for plat in ('curseforge', 'modrinth', 'youtube'):
        rs = [r for r in out if r['platform'] == plat]
        if rs:
            st = {s: sum(1 for r in rs if r['status'] == s) for s in STATUSES if any(r['status'] == s for r in rs)}
            print(f"  {plat}: {len(rs)} rows in targets.csv, qualified {len(q(rs))}, status {st}")
    if added:
        print(f'Moved to suppression.csv: {len(added)} keys')
    stale = [f for f in glob.glob(os.path.join(HERE, 'drafts', '*-*.md'))
             if any(os.path.basename(f).startswith(draft_prefix(k['key']) + '-') for k in sup if re.match(r'(cf|mr|yt):', k['key']))]
    if stale:
        print('Drafts of suppressed targets, delete them (GDPR Art. 21): ' + ', '.join(os.path.basename(f) for f in stale))
    if removed:
        print(f'Deleted after the 6-month limit: {len(removed)} rows')
    top = [r for r in out if r['status'] in OPEN][:args.top]
    print(f'\nTop {len(top)} open targets (status new/draft/approved):')
    for r in top:
        print(f"  {r['score']:>3}  {r['type']:<7} {r['name'][:38]:<38} fit {r['fit']:<9} {r['contact_route'][:70]}")
    due = [r for r in out if r['status'] == 'sent' and r['follow_up_on'] and days_since(r['follow_up_on']) >= 0]
    if due or args.due:
        print(f'\nFollow-ups due ({len(due)}): send template D once, then set status followed_up')
        for r in due:
            print(f"  {r['follow_up_on']}  {r['name']}  {r['url']}  drafts/{draft_prefix(r['id'])}*.md")
    if args.kpi:
        kpi(out, sup)


def kpi(rows, sup):
    week = [r for r in rows if r['sent_on'] and days_since(r['sent_on']) <= 7]
    new_q = [r for r in rows if days_since(r['first_seen']) <= 7 and int(r['score'] or 0) >= S['qualified']]
    print('\nWeekly KPIs (targets from research report 3.7):')
    print(f'  New qualified targets (score >= 60), last 7 days: {len(new_q)}   target 15-30')
    print(f'  First messages sent, last 7 days: {len(week)}   target 10-15')
    for typ, goal in (('pack', '>= 15 %'), ('creator', '>= 3 %')):
        sent = [r for r in rows if r['type'] == typ and r['sent_on'] and days_since(r['sent_on']) <= 28]
        replied = [r for r in sent if r['status'] in ('replied', 'yes', 'no', 'stop')]
        rate = f'{100 * len(replied) / len(sent):.0f} %' if sent else 'n/a'
        print(f'  Reply rate {typ}s, rolling 4 weeks: {rate} ({len(replied)}/{len(sent)})   target {goal}')
    print(f"  Yes / new dependents: {sum(1 for r in rows if r['status'] == 'yes')} marked yes   target >= 1 per week "
          '(check CurseForge "Dependents" by hand)')
    stops = [s for s in sup if days_since(s['added_on']) <= 7 and s['reason'].startswith('objection')
             and re.match(r'(cf|mr|yt):', s['key'])]
    print(f'  Objections / complaints, last 7 days: {len(stops)}   target 0 (otherwise stop and review the texts)')
    print('  By hand: creator videos/streams (>= 1 per month), unique downloads per project, popularity rank '
          'of Dreamcraft, time spent (<= 3 h)')


if __name__ == '__main__':
    sys.exit(main())
