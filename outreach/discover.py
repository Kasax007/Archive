#!/usr/bin/env python3
"""Find outreach candidates: Fabric modpacks for 26.2/26.3 (Modrinth and CurseForge) and creators.

Reads public data only and never contacts anyone: no messages, posts, comments or DMs.

    python3 discover.py                 # Modrinth + CurseForge + creators.csv
    python3 discover.py --skip-cf       # without CurseForge
    python3 discover.py --skip-mr       # without Modrinth
    python3 discover.py --no-verify     # without Discord invite and GitHub issue template checks

Output: data/candidates.json. Caches (safe to delete): cache/.

Sources and limits:
- Modrinth API (own User-Agent, about 3 requests per second, far below the 300/min limit).
- CurseForge: seeds from research/curseforge-wachstum-2026-11-daten.csv (all 26.3 Fabric packs on 6.11.2026)
  plus data/cf_seeds.csv (slugs copied from the CurseForge website listing by hand or with a fetch tool;
  the website's search API answers 403 from scripts). Details from api.cfwidget.com. The pack's mod list
  comes from manifest.json and modlist.html inside the public pack file on the CurseForge CDN, read with
  HTTP range requests (usually 50-600 KB instead of the whole file).
- Discord: public invite lookup (is the invite valid, server name, member count). No joining, no messages.
- GitHub: raw.githubusercontent.com, checks a few common issue-template file names.
- Creators: creators.csv, curated by hand. No YouTube/Twitch/TikTok scraping.
"""
import argparse
import csv
import datetime as dt
import html
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, 'config.json'), encoding='utf-8'))
LIM = CFG['limits']
UA = CFG['user_agent']
TODAY = dt.date.today()
CACHE = os.path.join(HERE, 'cache')
DATA = os.path.join(HERE, 'data')
RESEARCH_CSV = os.path.join(HERE, '..', 'research', 'curseforge-wachstum-2026-11-daten.csv')
MR = 'https://api.modrinth.com/v2'

# ---------------------------------------------------------------- HTTP, paced per host

PACE = {'api.modrinth.com': 0.35, 'api.cfwidget.com': 0.8, 'mediafilez.forgecdn.net': 0.25,
        'discord.com': 2.5, 'raw.githubusercontent.com': 0.4}
_last, STATS = {}, {}


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def _pace(host):
    wait = _last.get(host, 0) + PACE.get(host, 1.0) - time.time()
    if wait > 0:
        time.sleep(wait)
    _last[host] = time.time()
    STATS[host] = STATS.get(host, 0) + 1


def http(url, headers=None, method='GET', timeout=40, tries=3):
    """(status, headers, body). HTTP errors come back as status codes; 0 = network error."""
    host = urllib.parse.urlsplit(url).hostname
    hdr = {'User-Agent': UA}
    hdr.update(headers or {})
    for attempt in range(tries):
        _pace(host)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=hdr, method=method), timeout=timeout) as r:
                return r.status, r.headers, r.read()
        except urllib.error.HTTPError as e:
            body = e.read() if e.fp else b''
            if e.code == 429 and attempt < tries - 1:
                wait = e.headers.get('Retry-After')
                try:
                    wait = float(wait) if wait else float(json.loads(body).get('retry_after', 10))
                except (ValueError, AttributeError):
                    wait = 10
                time.sleep(min(wait, 60) + 1)
                continue
            if e.code >= 500 and attempt < tries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            return e.code, e.headers, body
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            if attempt < tries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            return 0, {}, str(e).encode()


def get_json(url, **params):
    if params:
        url += '?' + urllib.parse.urlencode(params)
    st, _, body = http(url)
    if st != 200:
        return st, None
    try:
        return st, json.loads(body)
    except ValueError:
        return st, None


class RangeFile(io.RawIOBase):
    """Read-only file over HTTP range requests, so zipfile can read one entry of a large pack file."""

    def __init__(self, url, max_bytes):
        self.url, self.pos, self.fetched, self.max_bytes = url, 0, 0, max_bytes
        st, hdr, _ = http(url, headers={'Range': 'bytes=0-0'})
        if st != 206:
            raise IOError(f'no range support or missing file (HTTP {st})')
        self.size = int(hdr['Content-Range'].split('/')[-1])

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else self.pos + off if whence == 1 else self.size + off
        return self.pos

    def readinto(self, b):
        n = min(len(b), self.size - self.pos)
        if n <= 0:
            return 0
        if self.fetched + n > self.max_bytes:
            raise IOError('byte budget for this pack file exceeded')
        st, _, data = http(self.url, headers={'Range': f'bytes={self.pos}-{self.pos + n - 1}'})
        if st != 206:
            raise IOError(f'range read failed (HTTP {st})')
        b[:len(data)] = data
        self.pos += len(data)
        self.fetched += len(data)
        return len(data)


# ---------------------------------------------------------------- small helpers

def days_since(iso):
    if not iso:
        return 9999
    return (TODAY - dt.date.fromisoformat(iso[:10])).days


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def load_json(path, default):
    try:
        return json.load(open(path, encoding='utf-8'))
    except (OSError, ValueError):
        return default


def save_json(path, obj, indent=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=indent, sort_keys=False)
    os.replace(tmp, path)


def load_suppression():
    """Keys from suppression.csv: target ids, URLs and author:<name>. Suppressed targets are not even looked up."""
    try:
        return {r['key'].strip().lower() for r in csv.DictReader(open(os.path.join(HERE, 'suppression.csv'), encoding='utf-8'))
                if r.get('key')}
    except OSError:
        return set()


SUPPRESSED = load_suppression()


def is_suppressed(tid=None, url=None, authors=()):
    keys = [tid, url] + [f'author:{a}' for a in authors]
    return any(k and k.lower() in SUPPRESSED for k in keys)


def tokens(slug):
    return set(re.split(r'[^a-z0-9]+', (slug or '').lower())) - {''}


def html_to_text(s):
    s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s or '')
    s = re.sub(r'(?i)<br\s*/?>|</(p|li|h\d|div|tr)>', '\n', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t\r\f\v]+', ' ', s)
    return re.sub(r'\n\s*\n+', '\n', s).strip()


def md_to_text(s):
    s = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', s or '')          # images
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)              # links -> text
    s = html_to_text(s)                                          # inline HTML
    s = re.sub(r'[*_`#>|]+', ' ', s)
    return re.sub(r'[ \t]+', ' ', s).strip()


# ---------------------------------------------------------------- page text: links, invitations, language

DISCORD_RE = re.compile(r'(?:discord\.gg|discord(?:app)?\.com/invite)/([A-Za-z0-9-]{2,32})', re.I)
DISCORD_SHORT_RE = re.compile(r'(?:dsc\.gg|discord\.io)/([A-Za-z0-9_-]{2,32})', re.I)     # redirect services, not checkable
GITHUB_RE = re.compile(r'https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)', re.I)
MR_LINK_RE = re.compile(r'modrinth\.com/modpack/([A-Za-z0-9_-]+)', re.I)
CF_LINK_RE = re.compile(r'curseforge\.com/minecraft/modpacks/([A-Za-z0-9_-]+)', re.I)
INVITE_STRONG = re.compile(r'\b(suggest(?:ion|ions|ed|ing)?|mod (?:requests?|ideas?)|request (?:a |new )?mods?|'
                           r'recommend (?:a |new |us )?mods?|(?:want|would like|like) (?:me|us) to add|'
                           r'let (?:me|us) know (?:what|which|if)|mods? (?:you\'?d|you would) like to see)\b', re.I)
INVITE_FEEDBACK = re.compile(r'\b(feedback|ideas?)\b', re.I)
ROUTE_WORD = re.compile(r'\b(discord|server|issues?|github|comments?|dms?|message|contact|form|tracker|channel|reach out)\b', re.I)
MOD_WORD = re.compile(r'\b(mods?|additions?|content|features?)\b', re.I)
NOT_INVITE = re.compile(r'\b(ram|gb|memory|java|allocate|shader settings|render distance)\b', re.I)
GH_SKIP_OWNERS = {'sponsors', 'orgs', 'user-attachments', 'features', 'topics', 'marketplace', 'apps', 'settings'}

STOP = {
    'en': 'the and with you your for this that are of to in is it on from all have more be will can our',
    'de': 'und der die das mit ist nicht ein eine für auf du dein ich wir zu den dem von auch sind',
    'es': 'el la los las y con para una es del que en por mas pero como',
    'pt': 'o os as e com para uma é não do da que em por mais mas como',
    'fr': 'le les et avec pour une est des du que dans pas plus sur vous',
    'it': 'il gli e con per una è non del della che di in più',
    'pl': 'i w z na do nie się jest to że jak oraz',
}
STOP = {k: set(v.split()) for k, v in STOP.items()}


def language(text):
    if re.search(r'[Ѐ-ӿ]{20,}', text or ''):
        return 'ru'
    if re.search(r'[぀-ヿ一-鿿가-힯]{10,}', text or ''):
        return 'cjk'
    words = re.findall(r"[a-zà-öø-ÿäöüß]+", (text or '').lower())
    counts = {k: sum(1 for w in words if w in v) for k, v in STOP.items()}
    best = max(counts, key=counts.get)
    return best if counts[best] >= 5 else 'unknown'


def page_signals(raw, text):
    """Links and suggestion invitations found on the project page (raw = HTML or Markdown)."""
    discord = sorted({m.group(1) for m in DISCORD_RE.finditer(raw or '')})
    github = []
    for m in GITHUB_RE.finditer(raw or ''):
        owner, repo = m.group(1), re.sub(r'\.git$', '', m.group(2))
        if owner.lower() not in GH_SKIP_OWNERS and f'{owner}/{repo}' not in github:
            github.append(f'{owner}/{repo}')
    invites = []
    sents = [x.strip() for x in re.split(r'(?<=[.!?])\s+|\n+', text or '') if x.strip()]
    for i, sent in enumerate(sents):
        if not (8 <= len(sent) <= 300) or NOT_INVITE.search(sent):
            continue
        # "Bug or idea? Leave a comment below." - the route often sits in the next sentence
        pair = (sent + ' ' + sents[i + 1]) if i + 1 < len(sents) and len(sents[i + 1]) <= 200 else sent
        if INVITE_STRONG.search(sent) and (ROUTE_WORD.search(sent) or MOD_WORD.search(sent)):
            invites.append({'kind': 'suggestions', 'text': sent})
        elif INVITE_STRONG.search(sent) and ROUTE_WORD.search(pair):
            invites.append({'kind': 'suggestions', 'text': pair})
        elif INVITE_FEEDBACK.search(sent) and ROUTE_WORD.search(pair):
            invites.append({'kind': 'feedback', 'text': pair if not ROUTE_WORD.search(sent) else sent})
    short = sorted({m.group(0) for m in DISCORD_SHORT_RE.finditer(raw or '')})
    return {'discord_codes': discord, 'discord_short': short[:2], 'github': github[:3], 'invites': invites[:4],
            'modrinth_slugs': sorted({m.group(1).lower() for m in MR_LINK_RE.finditer(raw or '')}),
            'curseforge_slugs': sorted({m.group(1).lower() for m in CF_LINK_RE.finditer(raw or '')})}


# ---------------------------------------------------------------- mod list analysis

QUEST = set(CFG['quest_book_mods'])
SIDE = set(CFG['side_quest_mods'])
GUIDE = set(CFG['guide_mods'])
OURS = {p['slug']: k for k, p in CFG['projects'].items()}
OURS_CF = {p['cf_id']: k for k, p in CFG['projects'].items()}


def analyze_mods(mods, project_ids=()):
    """mods: list of {'slug', 'name', 'cats'?}. Returns compact flags for scoring and drafting."""
    out = {'count': len(mods) or len(project_ids), 'quest': [], 'quest_maybe': [], 'side_quest': [], 'guide': [],
           'raft': [], 'ocean': [], 'pet': [], 'ours': [], 'themes': {}}
    for pid in project_ids:
        if pid in OURS_CF and OURS_CF[pid] not in out['ours']:
            out['ours'].append(OURS_CF[pid])
    for m in mods:
        slug, name = (m.get('slug') or '').lower(), m.get('name') or m.get('slug')
        tk = tokens(slug) | tokens(name)
        if slug in OURS and OURS[slug] not in out['ours']:
            out['ours'].append(OURS[slug])
        if slug in QUEST:
            out['quest'].append(name)
        elif slug in SIDE:
            out['side_quest'].append(name)
        elif tk & set(CFG['quest_tokens']):
            out['quest_maybe'].append(name)
        if slug in GUIDE:
            out['guide'].append(name)
        if tk & set(CFG['raft_tokens']) and slug != 'beach-craft':
            out['raft'].append(name)
        elif tk & set(CFG['ocean_tokens']):
            out['ocean'].append(name)
        if tk & set(CFG['pet_tokens']) and slug not in CFG['pet_exclude'] and slug != 'tamagotchi':
            out['pet'].append(name)
        for theme, words in CFG['themes'].items():
            if tk & set(words):
                out['themes'].setdefault(theme, []).append(name)
    for k in ('quest', 'quest_maybe', 'side_quest', 'guide', 'raft', 'ocean', 'pet'):
        out[k] = out[k][:12]
    out['theme_counts'] = {k: len(v) for k, v in out['themes'].items()}
    out['themes'] = {k: v[:8] for k, v in out['themes'].items()}
    return out


# ---------------------------------------------------------------- Modrinth

def mr_search_all(version):
    hits, offset = [], 0
    facets = json.dumps([['project_type:modpack'], [f"categories:{CFG['loader']}"], [f'versions:{version}']])
    while True:
        st, d = get_json(MR + '/search', index='newest', limit=100, offset=offset, facets=facets)
        if not d:
            log(f'  modrinth search {version} offset {offset}: HTTP {st}')
            break
        hits += d['hits']
        offset += 100
        if offset >= min(d['total_hits'], 4000):
            break
    return hits


def mr_projects(ids, cache=None):
    """Batch project lookup. With cache: only the compact fields for mod lists."""
    out, todo = {}, []
    for i in ids:
        if cache is not None and i in cache:
            out[i] = cache[i]
        else:
            todo.append(i)
    for part in chunks(todo, 80):
        st, d = get_json(MR + '/projects', ids=json.dumps(part))
        for p in d or []:
            if cache is not None:
                cache[p['id']] = {'slug': p['slug'], 'title': p['title'], 'cats': p.get('categories', []),
                                  'type': p.get('project_type'), 'downloads': p.get('downloads', 0)}
                out[p['id']] = cache[p['id']]
            else:
                out[p['id']] = p
    return out


def discover_modrinth(own_authors):
    log('Modrinth: searching packs ...')
    hits = {}
    for v in CFG['mc_versions']:
        for h in mr_search_all(v):
            hits.setdefault(h['project_id'], h)
            hits[h['project_id']].setdefault('_mc', set()).add(v)
    total = len(hits)
    ranked = sorted(hits.values(), key=lambda h: -h['follows'])
    for i, h in enumerate(ranked):
        h['_follow_rank'] = i + 1
    content_cats = set(CFG['mr_content_categories'])
    pool = [h for h in hits.values()
            if set(h['categories']) & content_cats
            and days_since(h['date_modified']) <= LIM['enrich_max_age_days']
            and h['downloads'] >= LIM['enrich_min_downloads']
            and h['author'] not in own_authors
            and not is_suppressed('mr:' + h['project_id'], f"https://modrinth.com/modpack/{h['slug']}", [h['author']])]
    log(f'Modrinth: {total} packs for {"/".join(CFG["mc_versions"])} Fabric, {len(pool)} content packs to enrich')
    projects = mr_projects([h['project_id'] for h in pool])
    teams = {}
    team_ids = [p['team'] for p in projects.values() if p.get('team')]
    for part in chunks(team_ids, 80):
        st, d = get_json(MR + '/teams', ids=json.dumps(part))
        for members in d or []:
            if members:
                teams[members[0]['team_id']] = [{'user': m['user']['username'], 'role': m.get('role', '')}
                                                for m in members if m.get('accepted', True)]
    versions = {}
    vids = [h['latest_version'] for h in pool if h.get('latest_version')]
    for part in chunks(vids, 80):
        st, d = get_json(MR + '/versions', ids=json.dumps(part))
        for v in d or []:
            versions[v['project_id']] = v
    # packs whose newest version is for another Minecraft version: take the newest 26.x Fabric version
    for h in pool:
        v = versions.get(h['project_id'])
        if v and set(v['game_versions']) & set(CFG['mc_versions']) and CFG['loader'] in v['loaders']:
            continue
        st, d = get_json(f"{MR}/project/{h['project_id']}/version", loaders=json.dumps([CFG['loader']]),
                         game_versions=json.dumps(CFG['mc_versions']))
        if d:
            versions[h['project_id']] = max(d, key=lambda x: x['date_published'])
    mod_cache = load_json(os.path.join(CACHE, 'mr_projects.json'), {})
    dep_ids = sorted({dep['project_id'] for v in versions.values() for dep in v.get('dependencies', [])
                      if dep.get('project_id')})
    mods = mr_projects(dep_ids, cache=mod_cache)
    save_json(os.path.join(CACHE, 'mr_projects.json'), mod_cache)
    out = []
    for h in pool:
        p = projects.get(h['project_id'])
        if not p:
            continue
        v = versions.get(h['project_id'])
        deps = v.get('dependencies', []) if v else []
        mod_list = [{'slug': mods[d['project_id']]['slug'], 'name': mods[d['project_id']]['title'],
                     'cats': mods[d['project_id']]['cats']}
                    for d in deps if d.get('project_id') in mods]
        extra_files = [d['file_name'] for d in deps if not d.get('project_id') and d.get('file_name')]
        body = p.get('body') or ''
        text = md_to_text(body)
        sig = page_signals(body, text)
        if p.get('discord_url'):
            sig['discord_codes'] = sorted(set(sig['discord_codes']) | {m.group(1) for m in DISCORD_RE.finditer(p['discord_url'])})
        team = teams.get(p.get('team'), [])
        c = {
            'id': 'mr:' + p['id'], 'type': 'pack', 'platform': 'modrinth', 'name': p['title'], 'slug': p['slug'],
            'url': f"https://modrinth.com/modpack/{p['slug']}",
            'authors': [h['author']] + [m['user'] for m in team if m['user'] != h['author']][:4],
            'organization': h.get('organization') or None,
            'summary': p.get('description', ''),
            'downloads': p.get('downloads', 0), 'follows': p.get('followers', 0), 'follow_rank': h['_follow_rank'],
            'created': (p.get('published') or '')[:10], 'updated': (p.get('updated') or '')[:10],
            'mc_versions': sorted(set(p.get('game_versions', [])) & set(CFG['mc_versions'])),
            'loaders': p.get('loaders', []),
            'categories': sorted(set(p.get('categories', [])) | set(p.get('additional_categories', []))),
            'links': {'discord': p.get('discord_url'), 'issues': p.get('issues_url'), 'source': p.get('source_url'),
                      'wiki': p.get('wiki_url')},
            'latest_file': {'name': v.get('version_number') if v else None, 'date': (v.get('date_published') or '')[:10] if v else None,
                            'mc': v.get('game_versions') if v else []},
            'mods': analyze_mods(mod_list) if v else None,
            'mods_note': (f'{len(extra_files)} files from outside Modrinth' if extra_files else ''),
            'language': language(text), 'signals': sig, 'text_excerpt': text[:1500],
        }
        save_json(os.path.join(CACHE, 'modlists', c['id'].replace(':', '_') + '.json'),
                  {'id': c['id'], 'file': c['latest_file'], 'mods': [[m['slug'], m['name']] for m in mod_list],
                   'other_files': extra_files})
        out.append(c)
    return out, total


# ---------------------------------------------------------------- CurseForge

CONTENT_WORDS = re.compile(r'\b(rpg|adventure|quest|quests|magic|tech|create|skyblock|survival|horror|apocalypse|'
                           r'medieval|dungeon|dungeons|odyssey|journey|exploration|story|cozy|farm|smp)\b', re.I)


def perf_name(name):
    low = (name or '').lower()
    return any(k in low for k in CFG['perf_keywords'] if len(k) > 3) or bool(
        re.search(r'\b(fps|pvp|hud|lag)\b', low))


def cf_seeds():
    seeds = {}
    try:
        for r in csv.DictReader(open(RESEARCH_CSV, encoding='utf-8')):
            if r['liste'] == 'modpacks_26.3_fabric':
                seeds[r['slug']] = {'name': r['name'], 'mc_hint': '26.3', 'cats': r['kategorien'].split(';'),
                                    'source': 'research CSV 6.11.2026'}
    except OSError:
        log('  research CSV not found, only data/cf_seeds.csv is used')
    try:
        for r in csv.DictReader(open(os.path.join(DATA, 'cf_seeds.csv'), encoding='utf-8')):
            s = seeds.setdefault(r['slug'].strip(), {'name': r['name'], 'mc_hint': r['mc_hint'], 'cats': [],
                                                     'source': r['source']})
            if r['mc_hint'] not in s['mc_hint']:
                s['mc_hint'] += ',' + r['mc_hint']
    except OSError:
        pass
    return seeds


def cf_widget(slug, cache):
    hit = cache.get(slug)
    if hit and days_since(hit.get('fetched')) < LIM['cf_refresh_days']:
        if hit.get('status') == 'ok':      # re-read invitations from the cached text (patterns may have changed)
            found = hit['signals']['invites']
            hit['signals']['invites'] = found + [i for i in page_signals('', hit['text'])['invites'] if i not in found]
            hit['signals'].setdefault('discord_short', [])
        return hit
    st, d = get_json(f'https://api.cfwidget.com/minecraft/modpacks/{urllib.parse.quote(slug)}')
    if st == 202 or (d and d.get('error')):
        return {'status': 'queued', 'fetched': None}
    if st != 200 or not d:
        cache[slug] = {'status': f'http {st}', 'fetched': TODAY.isoformat()}
        return cache[slug]
    files = [{'id': f['id'], 'name': f['name'], 'display': f.get('display'), 'type': f.get('type'),
              'versions': f.get('versions', []), 'date': f.get('uploaded_at', '')[:10],
              'size': f.get('filesize')} for f in d.get('files', [])]
    raw = d.get('description') or ''
    text = html_to_text(raw)
    cache[slug] = {
        'status': 'ok', 'fetched': TODAY.isoformat(), 'id': d['id'], 'title': d['title'], 'summary': d.get('summary', ''),
        'url': d['urls'].get('curseforge'), 'created': d.get('created_at', '')[:10],
        'downloads': d.get('downloads', {}).get('total', 0), 'categories': d.get('categories', []),
        'members': [{'user': m['username'], 'role': m.get('title', '')} for m in d.get('members', [])],
        'links': d.get('links') or [], 'files': files, 'text': text[:20000], 'signals': page_signals(raw, text),
        'language': language(text + ' ' + d.get('summary', '')),
    }
    return cache[slug]


def cf_pick_file(files):
    best = None
    for f in files:
        vs = set(f['versions'])
        if 'Fabric' not in vs or not vs & set(CFG['mc_versions']) or 'server' in (f['name'] or '').lower():
            continue
        if best is None or f['date'] > best['date']:
            best = f
    return best


MODLIST_RE = re.compile(r'<a href="https?://www\.curseforge\.com/minecraft/mc-mods/([^"/?#]+)[^"]*">(.*?)</a>', re.I | re.S)


def cf_modlist(f, cache):
    key = str(f['id'])
    if key in cache:
        return cache[key]
    fid = f['id']
    url = f"https://mediafilez.forgecdn.net/files/{fid // 1000}/{fid % 1000}/{urllib.parse.quote(f['name'])}"
    res = {'ok': False, 'file': f['name'], 'date': f['date']}
    try:
        rf = RangeFile(url, LIM['zip_max_bytes'])
        z = zipfile.ZipFile(io.BufferedReader(rf, buffer_size=128 * 1024))
        names = z.namelist()
        man = json.loads(z.read('manifest.json')) if 'manifest.json' in names else {}
        mods = []
        if 'modlist.html' in names:
            for m in MODLIST_RE.finditer(z.read('modlist.html').decode('utf-8', 'replace')):
                name = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
                mods.append({'slug': m.group(1).lower(), 'name': re.sub(r'\s*\(by [^)]*\)\s*$', '', name)})
        cfgdirs = sorted({n.split('/')[2] for n in names if n.startswith('overrides/config/') and n.count('/') >= 3})
        res = {'ok': True, 'file': f['name'], 'date': f['date'], 'bytes_read': rf.fetched,
               'project_ids': [x.get('projectID') for x in man.get('files', [])],
               'mods': mods, 'quest_dirs': [d for d in cfgdirs if re.search(r'quest', d, re.I)],
               'has_kubejs': any(n.startswith('overrides/kubejs/') for n in names)}
    except (IOError, OSError, zipfile.BadZipFile, KeyError, ValueError) as e:
        res['error'] = str(e)[:200]
    cache[key] = res
    return res


def discover_curseforge(own_authors):
    seeds = cf_seeds()
    content_cats = set(CFG['cf_content_categories'])
    todo = []
    for slug, s in seeds.items():
        if is_suppressed(url=f'https://www.curseforge.com/minecraft/modpacks/{slug}'):
            continue
        # skip obvious performance/shader/PvP packs by name, unless the name or categories say content
        if perf_name(s['name']) and not CONTENT_WORDS.search(s['name']) and not (set(s['cats']) & content_cats):
            continue
        todo.append(slug)
    log(f'CurseForge: {len(seeds)} seed slugs, {len(todo)} after skipping performance/shader packs by name')
    wcache = load_json(os.path.join(CACHE, 'cfwidget.json'), {})
    mcache = load_json(os.path.join(CACHE, 'cf_modlists.json'), {})
    out, queued, missing = [], 0, 0
    for i, slug in enumerate(todo):
        w = cf_widget(slug, wcache)
        if i % 50 == 49:
            save_json(os.path.join(CACHE, 'cfwidget.json'), wcache)
            log(f'  cfwidget {i + 1}/{len(todo)}')
        if w.get('status') == 'queued':
            queued += 1
            continue
        if w.get('status') != 'ok':
            missing += 1
            continue
        authors = [m['user'] for m in w['members']]
        if set(authors) & set(own_authors) or is_suppressed(f"cf:{w['id']}", w['url'], authors):
            continue
        f = cf_pick_file(w['files'])
        if not f:
            continue          # no 26.2/26.3 Fabric file
        mc = sorted({v for x in w['files'] if 'Fabric' in x['versions'] for v in x['versions']} & set(CFG['mc_versions']))
        updated = max(x['date'] for x in w['files'])
        content = bool(set(w['categories']) & content_cats)
        c = {
            'id': f"cf:{w['id']}", 'type': 'pack', 'platform': 'curseforge', 'name': w['title'], 'slug': slug,
            'url': w['url'], 'authors': authors[:5], 'summary': w['summary'], 'downloads': w['downloads'],
            'follows': None, 'created': w['created'], 'updated': updated, 'mc_versions': mc, 'loaders': ['fabric'],
            'categories': w['categories'], 'links': {'cf_links': w['links']},
            'latest_file': {'name': f['display'] or f['name'], 'date': f['date'], 'mc': [v for v in f['versions'] if v[0].isdigit()]},
            'mods': None, 'mods_note': '', 'language': w['language'], 'signals': w['signals'],
            'text_excerpt': w['text'][:1500],
        }
        # the pack file is only read for packs that can become targets
        if content and days_since(updated) <= LIM['enrich_max_age_days'] and w['downloads'] >= LIM['enrich_min_downloads']:
            ml = cf_modlist(f, mcache)
            if ml.get('ok'):
                c['mods'] = analyze_mods(ml['mods'], ml['project_ids'])
                if not ml['mods']:
                    c['mods_note'] = 'pack file has no modlist.html: only project IDs checked (our mods), quest mods unknown'
                    c['mods']['unknown'] = True
                if ml['quest_dirs']:
                    c['mods']['quest_dirs'] = ml['quest_dirs']
                save_json(os.path.join(CACHE, 'modlists', c['id'].replace(':', '_') + '.json'),
                          {'id': c['id'], 'file': ml['file'], 'mods': [[m['slug'], m['name']] for m in ml['mods']],
                           'project_ids': ml['project_ids'], 'quest_dirs': ml['quest_dirs'], 'kubejs': ml['has_kubejs']})
            else:
                c['mods_note'] = 'pack file not readable: ' + ml.get('error', '?')
        out.append(c)
    save_json(os.path.join(CACHE, 'cfwidget.json'), wcache)
    save_json(os.path.join(CACHE, 'cf_modlists.json'), mcache)
    log(f'CurseForge: {len(out)} packs with a 26.2/26.3 Fabric file; cfwidget queued {queued}, not found {missing}')
    return out, len(seeds)


# ---------------------------------------------------------------- verification of contact routes

TEMPLATE_NAMES = ['mod_suggestion.yml', 'mod-suggestion.yml', 'mod_suggestion.md', 'mod-suggestion.md',
                  'mod_request.yml', 'mod-request.yml', 'mod_request.md', 'suggestion.yml', 'suggestion.md',
                  'feature_request.yml', 'feature_request.md']


MODRINTH_LIVE = any(p.get('modrinth_id') for p in CFG['projects'].values())


def worth_verifying(c):
    if c['platform'] == 'modrinth' and not MODRINTH_LIVE and not c.get('twin'):
        return False      # our mods are not on Modrinth yet: such packs stay on hold, no route checks needed
    cats = set(c['categories'])
    content = bool(cats & (set(CFG['cf_content_categories']) | set(CFG['mr_content_categories'])))
    return content and days_since(c['updated']) <= 60 and c['downloads'] >= LIM['enrich_min_downloads']


def verify_routes(cands):
    dcache = load_json(os.path.join(CACHE, 'discord.json'), {})
    gcache = load_json(os.path.join(CACHE, 'github_templates.json'), {})
    gh_budget = LIM['github_repos_per_run']
    for c in cands:
        if not worth_verifying(c):
            continue
        checks = []
        for code in c['signals']['discord_codes'][:3]:
            hit = dcache.get(code)
            if not hit or days_since(hit.get('checked')) >= LIM['discord_refresh_days']:
                st, d = get_json(f'https://discord.com/api/v10/invites/{code}', with_counts='true')
                if st == 200 and d:
                    hit = {'ok': True, 'guild': (d.get('guild') or {}).get('name'),
                           'members': d.get('approximate_member_count'), 'checked': TODAY.isoformat()}
                elif st in (404, 400):
                    hit = {'ok': False, 'reason': 'invite invalid or expired', 'checked': TODAY.isoformat()}
                else:
                    hit = {'ok': None, 'reason': f'HTTP {st}', 'checked': TODAY.isoformat()}
                dcache[code] = hit
            checks.append(dict(hit, code=code))
        c['discord_check'] = checks
        # GitHub links in a description often point to the repos of included mods: keep only the pack's own
        owners = {a.lower() for a in c.get('authors', [])}
        repos = [r for r in c['signals']['github']
                 if r.split('/')[0].lower() in owners or norm(r.split('/')[1]) in norm(c['slug'])
                 or norm(c['slug']) in norm(r.split('/')[1])]
        for key in ('issues', 'source'):
            m = GITHUB_RE.search(c['links'].get(key) or '')
            if m and f'{m.group(1)}/{re.sub(r".git$", "", m.group(2))}' not in repos:
                repos.insert(0, f'{m.group(1)}/{re.sub(r".git$", "", m.group(2))}')
        c['github_templates'] = {}
        for repo in repos[:2]:
            hit = gcache.get(repo)
            if (not hit or days_since(hit.get('checked')) >= 30) and gh_budget > 0:
                gh_budget -= 1
                found = []
                for name in TEMPLATE_NAMES:
                    st, _, _ = http(f'https://raw.githubusercontent.com/{repo}/HEAD/.github/ISSUE_TEMPLATE/{name}')
                    if st == 200:
                        found.append(name)
                hit = {'found': found, 'checked': TODAY.isoformat()}
                gcache[repo] = hit
            if hit:
                c['github_templates'][repo] = hit['found']
    save_json(os.path.join(CACHE, 'discord.json'), dcache)
    save_json(os.path.join(CACHE, 'github_templates.json'), gcache)


# ---------------------------------------------------------------- creators (curated by hand)

def load_creators():
    path = os.path.join(HERE, 'creators.csv')
    out = []
    try:
        rows = list(csv.DictReader(open(path, encoding='utf-8')))
    except OSError:
        return out
    for r in rows:
        if not r.get('id') or is_suppressed(r['id'], r.get('url')):
            continue
        out.append({'id': r['id'], 'type': 'creator', 'platform': r['platform'], 'name': r['name'], 'url': r['url'],
                    'language': r['language'], 'audience': r.get('audience', ''), 'route': r.get('business_route', ''),
                    'focus': r.get('focus', ''), 'fit': r.get('fit', ''), 'evidence': r.get('evidence', ''),
                    'evidence_url': r.get('evidence_url', ''), 'evidence_month': r.get('evidence_month', ''),
                    'last_checked': r.get('last_checked', '')})
    return out


# ---------------------------------------------------------------- main

def norm(s):
    return re.sub(r'[^a-z0-9]+', '', (s or '').lower())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--skip-mr', action='store_true')
    ap.add_argument('--skip-cf', action='store_true')
    ap.add_argument('--no-verify', action='store_true', help='no Discord invite / GitHub template checks')
    args = ap.parse_args()
    own = set(CFG['own_authors'])
    prev = load_json(os.path.join(DATA, 'candidates.json'), {})
    prev_by_id = {c['id']: c for c in prev.get('candidates', [])}
    cands, counts = [], dict(prev.get('counts', {}))     # counts of a skipped source stay from the last run
    if not args.skip_mr:
        mr, total = discover_modrinth(own)
        cands += mr
        counts['modrinth_packs_26x_fabric'] = total
        counts['modrinth_enriched'] = len(mr)
    else:
        cands += [c for c in prev_by_id.values() if c['platform'] == 'modrinth']
    if not args.skip_cf:
        cf, seeds = discover_curseforge(own)
        cands += cf
        counts['curseforge_seeds'] = seeds
        counts['curseforge_packs_26x_fabric'] = len(cf)
    else:
        cands += [c for c in prev_by_id.values() if c['platform'] == 'curseforge']
    # link the same pack on both platforms
    by_cf_slug = {c['slug']: c for c in cands if c['platform'] == 'curseforge'}
    by_name = {norm(c['name']): c for c in cands if c['platform'] == 'curseforge'}
    by_mr_slug = {c['slug']: c for c in cands if c['platform'] == 'modrinth'}
    for c in cands:
        if c['platform'] != 'modrinth':
            continue
        twin = next((by_cf_slug[s] for s in c['signals']['curseforge_slugs'] if s in by_cf_slug), None) \
            or by_cf_slug.get(c['slug']) or by_name.get(norm(c['name']))
        if twin:
            c['twin'] = twin['id']
            twin['twin'] = c['id']
    for c in cands:
        if c['platform'] == 'curseforge' and 'twin' not in c:
            twin = next((by_mr_slug[s] for s in c['signals']['modrinth_slugs'] if s in by_mr_slug), None)
            if twin:
                c['twin'], twin['twin'] = twin['id'], c['id']
    if not args.no_verify:
        log('Checking contact routes (Discord invites, GitHub issue templates) ...')
        verify_routes(cands)
    creators = load_creators()
    counts['creators_curated'] = len(creators)
    for c in cands:
        c['first_seen'] = prev_by_id.get(c['id'], {}).get('first_seen') or TODAY.isoformat()
    save_json(os.path.join(DATA, 'candidates.json'),
              {'generated': TODAY.isoformat(), 'counts': counts, 'requests': STATS,
               'candidates': cands + creators}, indent=1)
    log(f'Wrote data/candidates.json: {len(cands)} packs, {len(creators)} creators. Requests per host: {STATS}')


if __name__ == '__main__':
    main()
