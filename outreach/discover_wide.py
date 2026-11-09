#!/usr/bin/env python3
"""Wide pack discovery: bigger modpacks (about 1,000+ downloads a month) on every version our mods exist for.

discover.py covers 26.2/26.3 Fabric packs with 500-100,000 total downloads. This script looks wider, at packs
that are big enough to matter and that could add one of our mods:

    Quest Icons:            Fabric 26.3, 26.2, 26.1.2, 1.21.11, 1.21.1, 1.20.1; NeoForge 1.21.1; Forge 1.20.1
    Beach Craft, Tamacraft: Fabric 26.3 and 1.21.1

Usage (from the outreach folder):

    python3 discover_wide.py                       # Modrinth search + CurseForge seeds
    python3 discover_wide.py --skip-cf             # Modrinth only
    python3 discover_wide.py --skip-mr             # CurseForge only
    python3 discover_wide.py --mr-depth 200        # look at the top 200 packs per (loader, version) on Modrinth
    python3 discover_wide.py --min-monthly 1000    # keep packs with an estimated 1,000+ downloads a month
    python3 discover_wide.py --no-verify           # skip the Discord invite and GitHub template checks
    python3 discover_wide.py --cf-seeds FILE.csv   # other seed file (columns: slug,name,source)

Output: data/wide_candidates.json (sorted by estimated monthly downloads), caches in cache/wide_*.json.
Packs already in targets.csv, creators.csv (by author), suppression.csv or drafts/ are skipped.

Monthly downloads are not public on either site, so they are estimated:
- CurseForge (api.cfwidget.com): downloads of the pack files uploaded in the last 45 days, scaled to 30 days by the
  age of the oldest of those files (at least 10 days); with no file that new, the newest file's downloads per day times 30.
- Modrinth (API v2): the same with the per-version downloads of /project/<id>/version.
Both undercount packs whose players stay on older files, and overcount right after a big release. Treat them as
an order of magnitude, and say "estimate" in drafts.

CurseForge has no open search API (the website answers scripts with 403). Seeds therefore come from a CSV
(default data/wide_cf_seeds.csv, columns slug,name,source) that a session fills from the website listing, e.g.
    https://www.curseforge.com/minecraft/search?page=1&pageSize=50&sortBy=popularity&class=modpacks
        &version=1.21.1&gameVersionTypeId=4        (4 = Fabric, 6 = NeoForge, 1 = Forge)
read with a fetch tool. The pack's mod list comes from manifest.json/modlist.html inside the public pack file,
read with HTTP range requests (helpers from discover.py).

Politeness: reads only public APIs, one request at a time with per-host pauses (Modrinth 0.35 s, cfwidget 0.8 s,
CurseForge CDN 0.25 s, Discord 2.5 s, GitHub raw 0.4 s). It never contacts anyone: no messages, posts, comments, joins
or sign-ups. Contact routes are only *found* here; whether a route is really invited is checked by hand on the
project page before a draft is written. The output never contains e-mail addresses (they are stripped from texts).
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
sys.path.insert(0, HERE)
import discover as D  # noqa: E402  (read-only helpers: paced HTTP, range reads, page signals, mod analysis)

TODAY = dt.date.today()
MR = D.MR
CACHE = D.CACHE
DATA = D.DATA

# where each of our mods exists (loader -> versions)
SUPPORT = {
    'QI': {'fabric': ['26.3', '26.2', '26.1.2', '1.21.11', '1.21.1', '1.20.1'], 'neoforge': ['1.21.1'],
           'forge': ['1.20.1']},
    'BC': {'fabric': ['26.3', '1.21.1']},
    'TG': {'fabric': ['26.3', '1.21.1']},
}
PAIRS = sorted({(l, v) for p in SUPPORT.values() for l, vs in p.items() for v in vs})
CF_LOADER = {'Fabric': 'fabric', 'NeoForge': 'neoforge', 'Forge': 'forge', 'Quilt': 'quilt'}

# quest books that make Quest Icons pointless (config list + a few more slugs seen on older versions)
QUEST_EXTRA = {'ftb-quests-forge', 'ftb-quests-neoforge', 'ftb-quests-fabric', 'heracles', 'odyssey',
               'better-questing-unofficial', 'questbook', 'simple-progression', 'vanilla-progression',
               'hqm', 'hardcore-questing-mode', 'questing-mode'}
OCEAN_THEME = re.compile(r'\b(ocean|oceans|sea|seas|island|islands|raft|pirates?|sail(?:ing)?|ships?|boats?|beach|'
                         r'tropical|castaway|shipwrecked|archipelago|survival island)\b', re.I)
ADVENTURE_THEME = re.compile(r'\b(exploration|explore|adventure|adventures|voyage|journey)\b', re.I)
CONTENT_CATS = {'Adventure and RPG', 'Quests', 'Tech', 'Magic', 'Exploration', 'Skyblock', 'Hardcore', 'Extra Large',
                'Expert', 'Horror', 'Sci-Fi', 'Map Based', 'adventure', 'challenging', 'combat', 'kitchen-sink', 'magic',
                'quests', 'technology'}
COZY_THEME = re.compile(r'\b(cozy|cosy|comfy|wholesome|farm(?:ing)?|cottage|cottagecore|pets?|animals?|homestead|'
                        r'relax(?:ing)?|chill|peaceful|calm|village life)\b', re.I)
EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
PERF_ONLY = re.compile(r'\b(fps|optimi[sz]ed|optimi[sz]ation|performance|boost(?:ed)?|potato|xray|x-ray|pvp|client|'
                       r'shaders?|vulkan|voxy|distant horizons|lag)\b', re.I)


def log(*a):
    D.log(*a)


def no_mail(s):
    return EMAIL_RE.sub('[address removed]', s or '')


# ---------------------------------------------------------------- known ids (skip list)

def known():
    ids, authors = set(), set()
    for name in ('targets.csv', 'creators.csv'):
        try:
            for r in csv.DictReader(open(os.path.join(HERE, name), encoding='utf-8')):
                ids.add((r.get('id') or '').strip().lower())
                if name == 'creators.csv':
                    authors.add(re.sub(r'^@', '', (r.get('id') or '').split(':')[-1]).lower())
        except OSError:
            pass
    for path in glob.glob(os.path.join(HERE, 'drafts', '*.md')):
        base = os.path.basename(path)
        m = re.match(r'(cf|mr|yt|tt|ig)-([A-Za-z0-9_]+)', base)
        if m:
            ids.add(f'{m.group(1)}:{m.group(2)}'.lower())
    return ids, authors


# ---------------------------------------------------------------- monthly estimate

def monthly_estimate(files):
    """files: [{'date': 'YYYY-MM-DD', 'downloads': n}]. Returns (estimate, basis text)."""
    dated = [f for f in files if f.get('date')]
    if not dated:
        return 0, 'no dated files'
    recent = [f for f in dated if D.days_since(f['date']) <= 45]
    if recent:
        oldest = max(D.days_since(f['date']) for f in recent)
        total = sum(f['downloads'] for f in recent)
        span = max(oldest, 10)            # very new files would inflate the rate
        est = int(total * 30 / span)
        return est, f'{total} downloads on {len(recent)} files from the last {oldest} days'
    newest = max(dated, key=lambda f: f['date'])
    age = max(D.days_since(newest['date']), 1)
    return int(newest['downloads'] * 30 / age), f"newest file {newest['date']} ({newest['downloads']} downloads in {age} days)"


# ---------------------------------------------------------------- fit analysis

def fits(pairs, mods, text, cats):
    """pairs: {(loader, version)} the pack ships. mods: analyze_mods() result or None."""
    out, notes = [], []
    blob = ' '.join([text or ''] + list(cats or []))
    can = {k for k, p in SUPPORT.items() if any(v in p.get(l, []) for l, v in pairs)}
    if mods is None or mods.get('unknown'):
        return [], ['mod list not read']
    content_mods = sum(mods.get('theme_counts', {}).values())
    if not (set(cats or []) & CONTENT_CATS) and content_mods < 8:
        return [], ['no content pack (categories/mod themes)']
    if PERF_ONLY.search(text[:120] if text else '') and content_mods < 8:
        return [], ['performance/shader pack']
    quest = list(mods['quest']) + [n for n in mods.get('quest_maybe', []) if 'quest' in n.lower()]
    quest_dirs = mods.get('quest_dirs') or []
    if 'QI' in can:
        if quest or quest_dirs:
            notes.append('quest book present: ' + ', '.join((quest + quest_dirs)[:3]))
        elif 'QI' not in mods['ours']:
            out.append('QI')
    if 'BC' in can and 'BC' not in mods['ours']:
        if mods['raft']:
            notes.append('raft mod present: ' + ', '.join(mods['raft'][:3]))
        elif OCEAN_THEME.search(blob):
            out.append('BC')
        elif ADVENTURE_THEME.search(blob):
            out.append('BC?')          # adventure/exploration pack without an ocean theme: weaker fit
    if 'TG' in can and 'TG' not in mods['ours']:
        if mods['pet']:
            notes.append('pet mod present: ' + ', '.join(mods['pet'][:3]))
        elif COZY_THEME.search(blob):
            out.append('TG')
    return out, notes


def mark_quest_slugs(mods_list, analysis):
    for m in mods_list:
        if (m.get('slug') or '').lower() in QUEST_EXTRA and m.get('name') not in analysis['quest']:
            analysis['quest'].append(m.get('name') or m['slug'])
    return analysis


# ---------------------------------------------------------------- Modrinth

def mr_discover(depth, min_monthly, skip_ids, skip_authors):
    hits = {}
    for loader, version in PAIRS:
        facets = json.dumps([['project_type:modpack'], [f'categories:{loader}'], [f'versions:{version}']])
        for offset in range(0, depth, 100):
            st, d = D.get_json(MR + '/search', index='downloads', limit=min(100, depth - offset), offset=offset,
                               facets=facets)
            if not d:
                log(f'  modrinth search {loader} {version}: HTTP {st}')
                break
            for h in d['hits']:
                hits.setdefault(h['project_id'], h).setdefault('_pairs', set()).add((loader, version))
            if offset + 100 >= d['total_hits']:
                break
    log(f'Modrinth: {len(hits)} packs in the top {depth} per loader/version')
    pool = [h for h in hits.values()
            if D.days_since(h['date_modified']) <= 60 and f"mr:{h['project_id']}".lower() not in skip_ids
            and h['author'].lower() not in skip_authors
            and not D.is_suppressed('mr:' + h['project_id'], f"https://modrinth.com/modpack/{h['slug']}", [h['author']])
            and not (PERF_ONLY.search(h['title']) and not set(h['categories']) & {'adventure', 'quests', 'magic', 'technology'})]
    log(f'Modrinth: {len(pool)} updated in the last 60 days and not known yet; reading versions ...')
    out, vcache = [], D.load_json(os.path.join(CACHE, 'wide_mr_versions.json'), {})
    for h in pool:
        pid = h['project_id']
        hit = vcache.get(pid)
        if not hit or D.days_since(hit.get('fetched')) >= 3:
            st, vs = D.get_json(f'{MR}/project/{pid}/version')
            if not vs:
                continue
            hit = {'fetched': TODAY.isoformat(), 'versions': [
                {'id': v['id'], 'name': v.get('version_number'), 'date': v['date_published'][:10],
                 'downloads': v.get('downloads', 0), 'loaders': v.get('loaders', []), 'mc': v.get('game_versions', []),
                 'deps': [x['project_id'] for x in v.get('dependencies', []) if x.get('project_id')]} for v in vs]}
            vcache[pid] = hit
        est, basis = monthly_estimate(hit['versions'])
        if est < min_monthly:
            continue
        match = [v for v in hit['versions'] if any(v2 in v['mc'] and l in v['loaders'] for l, v2 in PAIRS)]
        if not match:
            continue
        newest = max(match, key=lambda v: v['date'])
        pairs = {(l, v2) for l, v2 in PAIRS if v2 in newest['mc'] and l in newest['loaders']}
        out.append({'h': h, 'est': est, 'basis': basis, 'newest': newest, 'pairs': pairs})
    D.save_json(os.path.join(CACHE, 'wide_mr_versions.json'), vcache)
    pcache = D.load_json(os.path.join(CACHE, 'mr_projects.json'), {})
    D.mr_projects(sorted({d for c in out for d in c['newest']['deps']}), cache=pcache)
    D.save_json(os.path.join(CACHE, 'mr_projects.json'), pcache)
    full = D.mr_projects([c['h']['project_id'] for c in out])
    res = []
    for c in out:
        h, p = c['h'], full.get(c['h']['project_id'], {})
        mods_list = [{'slug': pcache[d]['slug'], 'name': pcache[d]['title'], 'cats': pcache[d]['cats']}
                     for d in c['newest']['deps'] if d in pcache]
        mods = D.analyze_mods(mods_list) if mods_list else None
        if mods:
            mark_quest_slugs(mods_list, mods)
        body = p.get('body') or ''
        text = D.md_to_text(body)
        sig = D.page_signals(body, text)
        if p.get('discord_url'):
            sig['discord_codes'] = sorted(set(sig['discord_codes']) |
                                          {m.group(1) for m in D.DISCORD_RE.finditer(p['discord_url'])})
        cats = sorted(set(p.get('categories', [])) | set(p.get('additional_categories', [])))
        fit, notes = fits(c['pairs'], mods, h['title'] + ' ' + p.get('description', '') + ' ' + text[:3000], cats)
        res.append({
            'id': 'mr:' + h['project_id'], 'platform': 'modrinth', 'name': h['title'], 'slug': h['slug'],
            'url': f"https://modrinth.com/modpack/{h['slug']}", 'authors': [h['author']],
            'summary': no_mail(p.get('description', '')), 'downloads_total': h['downloads'],
            'monthly_estimate': c['est'], 'monthly_basis': c['basis'], 'updated': h['date_modified'][:10],
            'pairs': sorted(f'{l} {v}' for l, v in c['pairs']), 'categories': cats,
            'latest_file': {'name': c['newest']['name'], 'date': c['newest']['date']},
            'mods_count': len(mods_list), 'mods': mods, 'fit': fit, 'fit_notes': notes,
            'links': {'discord': p.get('discord_url'), 'issues': p.get('issues_url'), 'source': p.get('source_url')},
            'signals': sig, 'language': D.language(text), 'text_excerpt': no_mail(text[:1500]),
            'note': 'Modrinth only: our mods are still in Modrinth review, draft = HOLD unless the pack is also on CurseForge',
        })
    return res


# ---------------------------------------------------------------- CurseForge

def cf_seeds(path):
    try:
        return list(csv.DictReader(open(path, encoding='utf-8')))
    except OSError:
        log(f'  no seed file {path}: CurseForge skipped')
        return []


def cf_discover(seed_path, min_monthly, skip_ids, skip_authors):
    seeds = cf_seeds(seed_path)
    wcache = D.load_json(os.path.join(CACHE, 'wide_cfwidget.json'), {})
    mcache = D.load_json(os.path.join(CACHE, 'cf_modlists.json'), {})
    res = []
    for i, s in enumerate(seeds):
        slug = s['slug'].strip()
        if D.is_suppressed(url=f'https://www.curseforge.com/minecraft/modpacks/{slug}'):
            continue
        hit = wcache.get(slug)
        if not hit or D.days_since(hit.get('fetched')) >= 3:
            st, d = D.get_json(f'https://api.cfwidget.com/minecraft/modpacks/{slug}')
            if not d or d.get('error') or st != 200:
                log(f'  cfwidget {slug}: HTTP {st} (202 = queued, try again later)')
                continue
            raw = d.get('description') or ''
            text = D.html_to_text(raw)
            hit = {'fetched': TODAY.isoformat(), 'id': d['id'], 'title': d['title'], 'summary': d.get('summary', ''),
                   'url': d['urls'].get('curseforge'), 'downloads': d.get('downloads', {}).get('total', 0),
                   'created': d.get('created_at', '')[:10], 'categories': d.get('categories', []),
                   'members': [m['username'] for m in d.get('members', [])], 'links': d.get('links') or [],
                   'files': [{'id': f['id'], 'name': f['name'], 'display': f.get('display'), 'versions': f.get('versions', []),
                              'date': f.get('uploaded_at', '')[:10], 'downloads': f.get('downloads', 0)}
                             for f in d.get('files', [])],
                   'text': text[:20000], 'signals': D.page_signals(raw, text), 'language': D.language(text)}
            wcache[slug] = hit
            if i % 20 == 19:
                D.save_json(os.path.join(CACHE, 'wide_cfwidget.json'), wcache)
        cid = f"cf:{hit['id']}"
        if cid.lower() in skip_ids or {m.lower() for m in hit['members']} & skip_authors \
                or D.is_suppressed(cid, hit['url'], hit['members']):
            continue
        est, basis = monthly_estimate(hit['files'])
        if est < min_monthly:
            continue

        def pairs_of(f):
            ls = {CF_LOADER[x] for x in f['versions'] if x in CF_LOADER}
            return {(l, v) for l in ls for v in f['versions'] if (l, v) in PAIRS}
        match = [f for f in hit['files'] if pairs_of(f) and 'server' not in (f['name'] or '').lower()]
        if not match:
            continue
        newest = max(match, key=lambda f: f['date'])
        pairs = pairs_of(newest)
        mods, mods_list = None, []
        ml = D.cf_modlist({'id': newest['id'], 'name': newest['name'], 'date': newest['date']}, mcache)
        if ml.get('ok'):
            mods_list = ml['mods']
            mods = D.analyze_mods(mods_list, ml['project_ids'])
            mark_quest_slugs(mods_list, mods)
            if not mods_list:
                mods['unknown'] = True
            if ml['quest_dirs']:
                mods['quest_dirs'] = ml['quest_dirs']
        fit, notes = fits(pairs, mods, hit['title'] + ' ' + hit['summary'] + ' ' + hit['text'][:3000], hit['categories'])
        res.append({
            'id': cid, 'platform': 'curseforge', 'name': hit['title'], 'slug': slug, 'url': hit['url'],
            'authors': hit['members'][:5], 'summary': no_mail(hit['summary']), 'downloads_total': hit['downloads'],
            'monthly_estimate': est, 'monthly_basis': basis, 'updated': max(f['date'] for f in hit['files']),
            'pairs': sorted(f'{l} {v}' for l, v in pairs), 'categories': hit['categories'],
            'latest_file': {'name': newest['display'] or newest['name'], 'date': newest['date']},
            'mods_count': len(mods_list), 'mods': mods, 'fit': fit,
            'fit_notes': notes + ([] if ml.get('ok') else ['pack file not readable: ' + ml.get('error', '?')]),
            'links': {'cf_links': hit['links']}, 'signals': hit['signals'], 'language': hit['language'],
            'text_excerpt': no_mail(hit['text'][:1500]), 'seed_source': s.get('source', ''),
        })
    D.save_json(os.path.join(CACHE, 'wide_cfwidget.json'), wcache)
    D.save_json(os.path.join(CACHE, 'cf_modlists.json'), mcache)
    return res


# ---------------------------------------------------------------- routes

def check_discord(cands):
    dcache = D.load_json(os.path.join(CACHE, 'discord.json'), {})
    for c in cands:
        if not c['fit']:
            continue
        codes = list(c['signals']['discord_codes'])
        for l in (c['links'].get('cf_links') or []):
            m = D.DISCORD_RE.search(l.get('link', '') if isinstance(l, dict) else str(l))
            if m and m.group(1) not in codes:
                codes.append(m.group(1))
        checks = []
        for code in codes[:3]:
            hit = dcache.get(code)
            if not hit or D.days_since(hit.get('checked')) >= 14:
                st, d = D.get_json(f'https://discord.com/api/v10/invites/{code}', with_counts='true')
                if st == 200 and d:
                    hit = {'ok': True, 'guild': (d.get('guild') or {}).get('name'),
                           'members': d.get('approximate_member_count'), 'checked': TODAY.isoformat()}
                elif st in (400, 404):
                    hit = {'ok': False, 'reason': 'invite invalid or expired', 'checked': TODAY.isoformat()}
                else:
                    hit = {'ok': None, 'reason': f'HTTP {st}', 'checked': TODAY.isoformat()}
                dcache[code] = hit
            checks.append(dict(hit, code=code))
        c['discord_check'] = checks
        repos = []
        for key in ('issues', 'source'):
            m = D.GITHUB_RE.search(c['links'].get(key) or '')
            if m:
                repos.append(f'{m.group(1)}/{re.sub(r".git$", "", m.group(2))}')
        c['github_templates'] = {}
        for repo in repos[:1]:
            found = []
            for name in D.TEMPLATE_NAMES:
                st, _, _ = D.http(f'https://raw.githubusercontent.com/{repo}/HEAD/.github/ISSUE_TEMPLATE/{name}')
                if st == 200:
                    found.append(name)
            c['github_templates'][repo] = found
    D.save_json(os.path.join(CACHE, 'discord.json'), dcache)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--skip-mr', action='store_true')
    ap.add_argument('--skip-cf', action='store_true')
    ap.add_argument('--no-verify', action='store_true')
    ap.add_argument('--mr-depth', type=int, default=100)
    ap.add_argument('--min-monthly', type=int, default=1000)
    ap.add_argument('--cf-seeds', default=os.path.join(DATA, 'wide_cf_seeds.csv'))
    args = ap.parse_args()
    skip_ids, skip_authors = known()
    cands = []
    if not args.skip_mr:
        cands += mr_discover(args.mr_depth, args.min_monthly, skip_ids, skip_authors)
    if not args.skip_cf:
        cands += cf_discover(args.cf_seeds, args.min_monthly, skip_ids, skip_authors)
    # a Modrinth pack that is also on CurseForge is pitched there (our mods are live on CurseForge)
    cf_by = {D.norm(c['name']): c for c in cands if c['platform'] == 'curseforge'}
    cf_slugs = {c['slug']: c for c in cands if c['platform'] == 'curseforge'}
    for c in cands:
        if c['platform'] == 'modrinth':
            twin = next((cf_slugs[s] for s in c['signals']['curseforge_slugs'] if s in cf_slugs), None) \
                or cf_by.get(D.norm(c['name']))
            if twin:
                c['twin'], twin['twin'] = twin['id'], c['id']
            elif c['signals']['curseforge_slugs']:
                c['twin_hint'] = c['signals']['curseforge_slugs'][:2]
    if not args.no_verify:
        log('Checking Discord invites and GitHub issue templates of fitting packs ...')
        check_discord(cands)
    cands.sort(key=lambda c: (-len([f for f in c['fit'] if '?' not in f]), -c['monthly_estimate']))
    D.save_json(os.path.join(DATA, 'wide_candidates.json'),
                {'generated': TODAY.isoformat(), 'min_monthly': args.min_monthly, 'requests': D.STATS,
                 'candidates': cands}, indent=1)
    fitting = [c for c in cands if c['fit']]
    log(f'Wrote data/wide_candidates.json: {len(cands)} packs, {len(fitting)} with a gap for our mods.')
    for c in fitting[:40]:
        log(f"  {c['id']:<14} {c['monthly_estimate']:>7}/mo  {'+'.join(c['fit']):<9} {', '.join(c['pairs'])[:40]:<40} {c['name'][:50]}")


if __name__ == '__main__':
    main()
