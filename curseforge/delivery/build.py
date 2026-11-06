"""Builds the delivery page for the CurseForge descriptions (artifact): copy buttons, the YouTube id field that is
written into the Beach Craft description, and the YouTube texts of the documentary.

python3 build.py <bc.html> <dc.html> <qi.html> <tama.html> <yt_title> <yt_desc.txt> <preview.jpg|-> <out_dir>
"""
import html
import json
import os
import sys

bc, dc, qi, tama, yt_title, yt_desc, preview, out = sys.argv[1:9]


def read(p):
    return open(p, encoding='utf-8').read()


data = {
    'bc': read(bc), 'dc': read(dc), 'qi': read(qi), 'tama': read(tama),
    'ytTitle': yt_title, 'ytDesc': read(yt_desc).strip() + '\n',
}
has_block = '<!-- VIDEO START -->' in data['bc'] and '<!-- VIDEO END -->' in data['bc']
if not has_block or 'VIDEO_ID' not in data['bc']:
    raise SystemExit('Beach Craft description: video block markers or VIDEO_ID placeholder missing')

blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/').replace('<!--', '<\\u0021--')


def kb(s):
    return f"{len(s.encode('utf-8')) / 1024:.0f} KB"


preview_html = ''
if preview != '-':
    preview_html = '''
      <details class="preview">
        <summary>Vorschau der neuen Seite <span class="muted">(Bild, ohne Video)</span></summary>
        <div class="shot"><img src="bc-preview.jpg" alt="Vorschau der neuen Beach-Craft-Beschreibung" loading="lazy"></div>
      </details>'''

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
.card { background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 18px; display: grid; gap: 12px; min-width: 0; }
.card.lead { border-color: color-mix(in srgb, var(--sea) 45%, var(--line)); box-shadow: 0 1px 0 var(--line); }
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
button:focus-visible, .btn:focus-visible, input:focus-visible, summary:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
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
.note { font-size: 13px; color: var(--muted); }
code { font: 12.5px var(--mono); background: var(--line); border-radius: 4px; padding: 1px 4px; }
footer { font-size: 13px; color: var(--muted); display: grid; gap: 6px; }
</style>

<div class="wrap">
  <header>
    <div class="kicker">Stand 6. November 2026</div>
    <h1>CurseForge Beschreibungen</h1>
    <p>Alle vier Projektseiten zum Einfügen. Beach Craft ist neu und kurz, mit Grafiken und der Doku als Video. Dreamcraft ist auf V1.4 gebracht, Quest Icons und Tamagotchi sind gleich geblieben.</p>
    <ol class="steps" aria-label="So fügst du eine Beschreibung ein">
      <li><b>1</b>HTML kopieren</li>
      <li><b>2</b>CurseForge: Projekt → Description</li>
      <li><b>3</b>Editor auf Quellcode (Source)</li>
      <li><b>4</b>alles ersetzen, speichern</li>
    </ol>
  </header>

  <article class="card lead" id="beach-craft">
    <div class="top"><h2>Beach Craft</h2><span class="chip new">neu</span></div>
    <div class="ids">Mod · Projekt 1010922 · Version 3.1.0+26.3 (Datei 9474711, freigegeben)</div>
    <p>Viel weniger Text, dafür Bilder: Kopfbild, die Doku als Video, „Auf einen Blick“ in Zahlen, zwei Ablaufgrafiken (der Weg ins Endlose Meer, das eigene Floß) und Bildcollagen aus den Shader-Aufnahmen. Bisect-Banner bleibt, die Musik-Credits stehen in einem Spoiler.</p>
''' + preview_html + r'''
    <div class="yt">
      <label for="yt">YouTube-Link der Doku</label>
      <input id="yt" inputmode="url" autocomplete="off" spellcheck="false" placeholder="https://youtu.be/…">
      <p class="state warn" id="yt-state">Noch kein Link: Beim Kopieren fehlt der Video-Block, der Rest ist fertig.</p>
    </div>
    <div class="actions">
      <button class="primary" data-copy="bc">HTML kopieren</button>
      <a class="btn" href="https://www.curseforge.com/minecraft/mc-mods/beach-craft" target="_blank" rel="noopener">Projektseite ↗</a>
      <span class="size" id="bc-size"></span>
    </div>
    <textarea class="fallback" data-fallback="bc" readonly hidden></textarea>
    <details>
      <summary>So kommt die Doku auf YouTube</summary>
      <ol class="how">
        <li>Film speichern: die 1080p-Datei mit 60 fps aus dem Chat (640 MB) oder die kleinere 720p-Fassung über „Als MP4 speichern“ auf der Seite der Doku.</li>
        <li>In YouTube Studio hochladen. Titel und Beschreibung mit Kapiteln, Musik-Credits und Hashtags hier kopieren:
          <div class="actions" style="margin-top:8px">
            <button data-copy="ytTitle">Titel kopieren</button>
            <button data-copy="ytDesc">Beschreibung kopieren</button>
          </div>
          <textarea class="fallback" data-fallback="ytTitle" readonly hidden></textarea>
          <textarea class="fallback" data-fallback="ytDesc" readonly hidden></textarea>
        </li>
        <li>Sichtbarkeit „Öffentlich“ oder „Nicht gelistet“, sonst lässt sich das Video nicht einbetten.</li>
        <li>Den Link (zum Beispiel <code>https://youtu.be/…</code>) oben ins Feld einfügen. Dann „HTML kopieren“: Das Video steht jetzt in der Beschreibung, als eingebetteter Player und als Bild mit Link.</li>
      </ol>
    </details>
  </article>

  <article class="card" id="dreamcraft">
    <div class="top"><h2>Dreamcraft</h2><span class="chip upd">aktualisiert</span></div>
    <div class="ids">Modpack · Projekt 545167 · V1.4 (Datei 9475197, Server-Pack 9475219)</div>
    <ul class="changes">
      <li>Neuer Abschnitt für V1.4: Beach Craft 3.1 mit eigenem Floß und den Leuten des Meeres, Upgraded Iron Chests und der Nebenpfad „Quality of Life“.</li>
      <li>348 Quests in 15 Kapiteln (vorher 328 in 14) und ein Hinweis für das Update eines bestehenden Servers.</li>
      <li>Upgraded Iron Chests steht in der Mod-Liste und bei den Credits.</li>
    </ul>
    <div class="actions">
      <button class="primary" data-copy="dc">HTML kopieren</button>
      <a class="btn" href="https://www.curseforge.com/minecraft/modpacks/dreamcraft-new" target="_blank" rel="noopener">Projektseite ↗</a>
      <span class="size">''' + kb(data['dc']) + r'''</span>
    </div>
    <textarea class="fallback" data-fallback="dc" readonly hidden></textarea>
    <p class="note">Modpack und Server-Pack sind freigegeben, beide lassen sich herunterladen (geprüft am 6. November).</p>
  </article>

  <article class="card" id="quest-icons">
    <div class="top"><h2>Quest Icons</h2><span class="chip same">unverändert</span></div>
    <div class="ids">Mod · Projekt 690531 · Version 1.1.0+26.3 (Datei 9429010)</div>
    <p>Gleicher Text wie am 4. November. Musst du nur einfügen, wenn er dort noch nicht steht.</p>
    <div class="actions">
      <button data-copy="qi">HTML kopieren</button>
      <a class="btn" href="https://www.curseforge.com/minecraft/mc-mods/quest-icons" target="_blank" rel="noopener">Projektseite ↗</a>
      <span class="size">''' + kb(data['qi']) + r'''</span>
    </div>
    <textarea class="fallback" data-fallback="qi" readonly hidden></textarea>
  </article>

  <article class="card" id="tamagotchi">
    <div class="top"><h2>Tamagotchi</h2><span class="chip same">unverändert</span></div>
    <div class="ids">Mod · Projekt 1758309 · Version 1.2.0 (Datei 9431312)</div>
    <p>Gleicher Text wie am 4. November (mit den Neuheiten von 1.2). Musst du nur einfügen, wenn er dort noch nicht steht.</p>
    <div class="actions">
      <button data-copy="tama">HTML kopieren</button>
      <a class="btn" href="https://www.curseforge.com/minecraft/mc-mods/tamagotchi" target="_blank" rel="noopener">Projektseite ↗</a>
      <span class="size">''' + kb(data['tama']) + r'''</span>
    </div>
    <textarea class="fallback" data-fallback="tama" readonly hidden></textarea>
  </article>

  <footer>
    <div>Alle Texte liegen auch als HTML-Dateien im Chat und in den Repos unter <code>docs/curseforge/description.html</code>.</div>
  </footer>
</div>

<script type="application/json" id="desc-data">''' + blob + r'''</script>
<script>
(function () {
  var D = JSON.parse(document.getElementById('desc-data').textContent);
  var input = document.getElementById('yt');
  var state = document.getElementById('yt-state');
  var bcSize = document.getElementById('bc-size');

  function ytId(s) {
    s = (s || '').trim();
    var m = s.match(/(?:youtu\.be\/|youtube(?:-nocookie)?\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/|v\/))([A-Za-z0-9_-]{11})/);
    if (m) return m[1];
    return /^[A-Za-z0-9_-]{11}$/.test(s) ? s : null;
  }
  function bcHtml() {
    var id = ytId(input.value);
    if (id) return D.bc.split('VIDEO_ID').join(id);
    return D.bc.replace(/<!-- VIDEO START -->[\s\S]*?<!-- VIDEO END -->\s*/, '');
  }
  function kb(s) { return Math.round(new Blob([s]).size / 1024) + ' KB'; }
  function refresh() {
    var raw = input.value.trim(), id = ytId(raw);
    if (id) { state.className = 'state ok'; state.textContent = 'Video-ID ' + id + ' wird eingesetzt (Player und Bild mit Link).'; }
    else if (raw) { state.className = 'state warn'; state.textContent = 'Das sieht nicht nach einem YouTube-Link aus. Ohne gültigen Link fehlt der Video-Block.'; }
    else { state.className = 'state warn'; state.textContent = 'Noch kein Link: Beim Kopieren fehlt der Video-Block, der Rest ist fertig.'; }
    bcSize.textContent = kb(bcHtml());
  }
  try { var saved = localStorage.getItem('bc-yt'); if (saved) input.value = saved; } catch (e) {}
  input.addEventListener('input', function () {
    try { localStorage.setItem('bc-yt', input.value.trim()); } catch (e) {}
    refresh();
  });
  refresh();

  function text(key) { return key === 'bc' ? bcHtml() : D[key]; }
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

os.makedirs(out, exist_ok=True)
with open(os.path.join(out, 'curseforge-beschreibungen.html'), 'w', encoding='utf-8') as f:
    f.write(page)
print('page', len(page) // 1024, 'KB')
