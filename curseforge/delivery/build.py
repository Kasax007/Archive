"""Builds the delivery page for the CurseForge descriptions (artifact): one card per project with a preview picture,
a copy button, and for projects with a video a YouTube field whose id is written into the description (without an id
the block between <!-- VIDEO START --> and <!-- VIDEO END --> is cut out), plus the YouTube title and description of
that video to copy.

python3 build.py config.json out_dir

config.json: {"date": "...", "intro": "...", "projects": [{"key", "name", "chip": ["new"|"upd"|"same", label],
  "ids", "about": [html paragraphs or "- " list items], "html": path, "preview": path or null, "url",
  "video": null or {"label", "yt_title", "yt_desc": path, "hint"}}], "footer": "..."}
Preview pictures are written next to the page as <key>-preview.jpg.
"""
import json
import os
import sys

from PIL import Image

cfg_path, out = sys.argv[1:3]
cfg = json.load(open(cfg_path, encoding='utf-8'))
os.makedirs(out, exist_ok=True)


def read(p):
    return open(p, encoding='utf-8').read()


def kb(s):
    return f"{len(s.encode('utf-8')) / 1024:.0f} KB"


data = {}
cards = []
for p in cfg['projects']:
    k = p['key']
    html = read(p['html'])
    data[k] = html
    video = p.get('video')
    if video:
        if '<!-- VIDEO START -->' not in html or '<!-- VIDEO END -->' not in html or 'VIDEO_ID' not in html:
            raise SystemExit(f'{k}: video block markers or VIDEO_ID placeholder missing')
        data[k + '_ytTitle'] = video['yt_title']
        data[k + '_ytDesc'] = read(video['yt_desc']).strip() + '\n'
    elif 'VIDEO_ID' in html:
        raise SystemExit(f'{k}: VIDEO_ID placeholder but no video configured')

    preview = ''
    if p.get('preview'):
        im = Image.open(p['preview']).convert('RGB')
        if im.width > 1040:
            im = im.resize((1040, round(im.height * 1040 / im.width)), Image.LANCZOS)
        im.save(os.path.join(out, f'{k}-preview.jpg'), quality=80, optimize=True, progressive=True)
        preview = f'''
      <details class="preview">
        <summary>Vorschau der Seite <span class="muted">(Bild{', ohne Video' if video else ''})</span></summary>
        <div class="shot"><img src="{k}-preview.jpg" alt="Vorschau der Beschreibung von {p['name']}" loading="lazy"></div>
      </details>'''

    about = []
    items = [a for a in p['about'] if a.startswith('- ')]
    for a in p['about']:
        if not a.startswith('- '):
            about.append(f'    <p>{a}</p>')
    if items:
        about.append('    <ul class="changes">' + ''.join(f'<li>{a[2:]}</li>' for a in items) + '</ul>')

    yt = ''
    yt_help = ''
    if video:
        yt = f'''
    <div class="yt">
      <label for="yt-{k}">YouTube-Link: {video['label']}</label>
      <input id="yt-{k}" data-yt="{k}" inputmode="url" autocomplete="off" spellcheck="false" placeholder="https://youtu.be/…">
      <p class="state warn" id="yt-state-{k}"></p>
    </div>'''
        yt_help = f'''
    <details>
      <summary>So kommt das Video auf YouTube</summary>
      <ol class="how">
        <li>{video['hint']}</li>
        <li>In YouTube Studio hochladen. Titel und Beschreibung (mit Musik-Credit und Hashtags) hier kopieren:
          <div class="actions" style="margin-top:8px">
            <button data-copy="{k}_ytTitle">Titel kopieren</button>
            <button data-copy="{k}_ytDesc">Beschreibung kopieren</button>
          </div>
          <textarea class="fallback" data-fallback="{k}_ytTitle" readonly hidden></textarea>
          <textarea class="fallback" data-fallback="{k}_ytDesc" readonly hidden></textarea>
        </li>
        <li>Sichtbarkeit „Öffentlich“ oder „Nicht gelistet“, sonst lässt sich das Video nicht einbetten.</li>
        <li>Den Link (zum Beispiel <code>https://youtu.be/…</code>) oben ins Feld einfügen, dann „HTML kopieren“: Das Video steht in der Beschreibung, als eingebetteter Player und als Bild mit Link.</li>
      </ol>
    </details>'''

    chip_cls, chip_label = p['chip']
    cards.append(f'''
  <article class="card{' lead' if chip_cls != 'same' else ''}" id="{k}">
    <div class="top"><h2>{p['name']}</h2><span class="chip {chip_cls}">{chip_label}</span></div>
    <div class="ids">{p['ids']}</div>
{chr(10).join(about)}{preview}{yt}
    <div class="actions">
      <button class="primary" data-copy="{k}">HTML kopieren</button>
      <a class="btn" href="{p['url']}" target="_blank" rel="noopener">Projektseite ↗</a>
      <span class="size" id="size-{k}">{kb(html)}</span>
    </div>
    <textarea class="fallback" data-fallback="{k}" readonly hidden></textarea>{yt_help}
  </article>''')

videos = [p['key'] for p in cfg['projects'] if p.get('video')]
blob = json.dumps({'texts': data, 'videos': videos}, ensure_ascii=False).replace('</', '<\\/').replace('<!--', '<\\u0021--')

page = r'''<title>CurseForge Beschreibungen</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
:root {
  --bg: #f6f2ee; --card: #fffdfb; --fg: #2a211c; --muted: #76685f; --line: #e6dbd2;
  --accent: #e8572a; --accent-fg: #ffffff; --accent-soft: #fde6dc;
  --sea: #0f7c86; --sea-soft: #d9f0f1; --ok: #2f7d45; --ok-soft: #dcefe1;
  --warn: #9a5b00; --warn-soft: #fbecd2; --field: #ffffff;
  --display: "Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #171310; --card: #221c18; --fg: #f1e9e2; --muted: #b3a397; --line: #3a302a;
    --accent: #ff7a4d; --accent-fg: #1c120d; --accent-soft: #43261b;
    --sea: #5fc4cc; --sea-soft: #173538; --ok: #7fcf95; --ok-soft: #1d3324;
    --warn: #f0b25a; --warn-soft: #3b2c14; --field: #1b1613; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #171310; --card: #221c18; --fg: #f1e9e2; --muted: #b3a397; --line: #3a302a;
  --accent: #ff7a4d; --accent-fg: #1c120d; --accent-soft: #43261b;
  --sea: #5fc4cc; --sea-soft: #173538; --ok: #7fcf95; --ok-soft: #1d3324;
  --warn: #f0b25a; --warn-soft: #3b2c14; --field: #1b1613; color-scheme: dark;
}
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--fg); font: 15px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif; }
.wrap { max-width: 760px; margin: 0 auto; padding-block: 28px 56px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: grid; gap: 18px; }
header { display: grid; gap: 8px; padding-bottom: 6px; }
.kicker { font: 600 12px/1 var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }
h1 { font: 700 clamp(28px, 7vw, 40px)/1.05 var(--display); margin: 0; text-wrap: balance; letter-spacing: -.01em; }
header p { margin: 0; color: var(--muted); max-width: 62ch; }
.steps { display: flex; flex-wrap: wrap; gap: 6px; margin: 4px 0 0; padding: 0; list-style: none; }
.steps li { font-size: 13px; background: var(--card); border: 1px solid var(--line); border-radius: 999px; padding: 4px 10px; }
.steps b { color: var(--accent); font-family: var(--mono); margin-right: 4px; }
nav.jump { display: flex; flex-wrap: wrap; gap: 4px 14px; }
nav.jump a { font: 600 13px/1 system-ui, sans-serif; color: var(--fg); text-decoration: none; border-bottom: 2px solid var(--accent-soft); padding: 6px 0 4px; }
.card { background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 18px; display: grid; gap: 12px; min-width: 0; scroll-margin-top: 12px; }
.card.lead { border-color: color-mix(in srgb, var(--sea) 45%, var(--line)); }
.top { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 10px; }
h2 { font: 700 24px/1.1 var(--display); margin: 0; }
.chip { font: 600 11px/1 var(--mono); letter-spacing: .06em; text-transform: uppercase; padding: 5px 8px; border-radius: 6px; }
.chip.new { background: var(--sea-soft); color: var(--sea); }
.chip.upd { background: var(--accent-soft); color: var(--accent); }
.chip.same { background: var(--line); color: var(--muted); }
.ids { font: 12px/1.4 var(--mono); color: var(--muted); }
.card p { margin: 0; max-width: 65ch; }
.muted { color: var(--muted); font-weight: 400; }
ul.changes { margin: 0; padding-left: 18px; display: grid; gap: 4px; }
.actions { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
button, .btn { font: 600 14px/1 system-ui, sans-serif; border-radius: 10px; padding: 11px 14px; cursor: pointer;
  border: 1px solid var(--line); background: var(--field); color: var(--fg); text-decoration: none; display: inline-flex; gap: 6px; align-items: center; }
button.primary { background: var(--accent); color: var(--accent-fg); border-color: var(--accent); }
button:focus-visible, .btn:focus-visible, input:focus-visible, summary:focus-visible, nav.jump a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.size { font: 12px var(--mono); color: var(--muted); }
.yt { display: grid; gap: 6px; background: var(--sea-soft); border-radius: 12px; padding: 12px; }
.yt label { font-weight: 600; font-size: 14px; }
.yt input { width: 100%; font: 14px var(--mono); padding: 10px 12px; border-radius: 9px; border: 1px solid var(--line); background: var(--field); color: var(--fg); min-width: 0; }
.state { font-size: 13px; margin: 0; }
.state.ok { color: var(--ok); }
.state.warn { color: var(--warn); }
details { border-top: 1px solid var(--line); padding-top: 10px; }
summary { cursor: pointer; font-weight: 600; }
details > div, details > ol { margin-top: 10px; }
.shot { max-height: 70vh; overflow: auto; border-radius: 10px; border: 1px solid var(--line); background: #10151a; }
.shot img { display: block; width: 100%; height: auto; }
ol.how { margin: 10px 0 0; padding-left: 20px; display: grid; gap: 8px; }
ol.how li { max-width: 62ch; }
textarea.fallback { width: 100%; min-height: 140px; font: 12px/1.4 var(--mono); border-radius: 9px; border: 1px solid var(--accent); background: var(--field); color: var(--fg); padding: 8px; }
code { font: 12.5px var(--mono); background: var(--line); border-radius: 4px; padding: 1px 4px; }
footer { font-size: 13px; color: var(--muted); display: grid; gap: 6px; }
</style>

<div class="wrap">
  <header>
    <div class="kicker">''' + cfg['date'] + r'''</div>
    <h1>CurseForge Beschreibungen</h1>
    <p>''' + cfg['intro'] + r'''</p>
    <ol class="steps" aria-label="So fügst du eine Beschreibung ein">
      <li><b>1</b>HTML kopieren</li>
      <li><b>2</b>CurseForge: Projekt → Description</li>
      <li><b>3</b>Editor auf Quellcode (Source)</li>
      <li><b>4</b>alles ersetzen, speichern</li>
    </ol>
    <nav class="jump" aria-label="Projekte">''' + ''.join(
        f'<a href="#{p["key"]}">{p["name"]}</a>' for p in cfg['projects']) + r'''</nav>
  </header>
''' + ''.join(cards) + r'''

  <footer>
    <div>''' + cfg['footer'] + r'''</div>
  </footer>
</div>

<script type="application/json" id="desc-data">''' + blob + r'''</script>
<script>
(function () {
  var D = JSON.parse(document.getElementById('desc-data').textContent);
  var T = D.texts;

  function ytId(s) {
    s = (s || '').trim();
    var m = s.match(/(?:youtu\.be\/|youtube(?:-nocookie)?\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/|v\/))([A-Za-z0-9_-]{11})/);
    if (m) return m[1];
    return /^[A-Za-z0-9_-]{11}$/.test(s) ? s : null;
  }
  function input(k) { return document.getElementById('yt-' + k); }
  function html(k) {
    if (D.videos.indexOf(k) < 0) return T[k];
    var id = ytId(input(k).value);
    if (id) return T[k].split('VIDEO_ID').join(id);
    return T[k].replace(/<!-- VIDEO START -->[\s\S]*?<!-- VIDEO END -->\s*/, '');
  }
  function kb(s) { return Math.round(new Blob([s]).size / 1024) + ' KB'; }
  function refresh(k) {
    var raw = input(k).value.trim(), id = ytId(raw), st = document.getElementById('yt-state-' + k);
    if (id) { st.className = 'state ok'; st.textContent = 'Video-ID ' + id + ' wird eingesetzt (Player und Bild mit Link).'; }
    else if (raw) { st.className = 'state warn'; st.textContent = 'Das sieht nicht nach einem YouTube-Link aus. Ohne gültigen Link fehlt der Video-Block.'; }
    else { st.className = 'state warn'; st.textContent = 'Noch kein Link: Beim Kopieren fehlt der Video-Block, der Rest ist fertig.'; }
    document.getElementById('size-' + k).textContent = kb(html(k));
  }
  D.videos.forEach(function (k) {
    var el = input(k);
    try { var saved = localStorage.getItem('yt-' + k) || (k === 'bc' ? localStorage.getItem('bc-yt') : null); if (saved) el.value = saved; } catch (e) {}
    el.addEventListener('input', function () {
      try { localStorage.setItem('yt-' + k, el.value.trim()); } catch (e) {}
      refresh(k);
    });
    refresh(k);
  });

  function text(key) { return /_yt(Title|Desc)$/.test(key) ? T[key] : html(key); }
  function flash(btn, msg) {
    var old = btn.dataset.label || btn.textContent;
    btn.dataset.label = old; btn.textContent = msg;
    clearTimeout(btn._t); btn._t = setTimeout(function () { btn.textContent = old; }, 2200);
  }
  function fallback(key, btn) {
    var ta = document.querySelector('textarea[data-fallback="' + key + '"]');
    ta.hidden = false; ta.value = text(key); ta.focus(); ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    flash(btn, ok ? 'Kopiert ✓' : 'Markiert: jetzt kopieren');
  }
  document.querySelectorAll('button[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var key = btn.dataset.copy, t = text(key);
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(t).then(function () { flash(btn, 'Kopiert ✓'); }, function () { fallback(key, btn); });
      } else { fallback(key, btn); }
    });
  });
})();
</script>
'''

with open(os.path.join(out, 'curseforge-beschreibungen.html'), 'w', encoding='utf-8') as f:
    f.write(page)
print('page', len(page) // 1024, 'KB')
