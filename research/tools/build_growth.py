"""Turns the research report (Markdown) into the artifact page "CurseForge Wachstumsplan".

venv/bin/python build_growth.py REPORT.md OUT.html
"""
import html
import re
import sys

import markdown

src, out = sys.argv[1:3]
md = open(src, encoding='utf-8').read()

# The report's own title block is replaced by the page header.
start = md.index('## Auf einen Blick')
body_md = md[start:]

# Python-Markdown wants 4 spaces per list level; the report indents nested items by 2 or 3.
lines, fence = [], False
for line in body_md.split('\n'):
    if line.lstrip().startswith('```'):
        fence = not fence
    if not fence and line.startswith(' ') and line.strip():
        n = len(line) - len(line.lstrip(' '))
        line = ' ' * (4 * ((n + 2) // 3)) + line.lstrip(' ')
    lines.append(line)
body_md = '\n'.join(lines)

conv = markdown.Markdown(extensions=['tables', 'fenced_code', 'sane_lists', 'toc'],
                         extension_configs={'toc': {'slugify': lambda v, sep: re.sub(r'[^a-z0-9]+', '-', v.lower()).strip('-')}})
body = conv.convert(body_md)

# evidence markers -> chips
LABEL = {'Doku': 'doku', 'Daten': 'daten', 'Ableitung': 'ableitung', 'Sekundärquelle': 'sekundaer'}


def chips(m):
    parts = [p.strip() for p in m.group(1).split('+')]
    if not all(p in LABEL for p in parts):
        return m.group(0)
    return ''.join(f'<span class="tag {LABEL[p]}">{p}</span>' for p in parts)


body = re.sub(r'\[((?:Doku|Daten|Ableitung|Sekundärquelle)(?: \+ (?:Doku|Daten|Ableitung))*)(?:, Passung nur vermutet)?\]', chips, body)
body = body.replace('[Daten, Passung nur vermutet]', '<span class="tag daten">Daten</span> <span class="muted">(Passung nur vermutet)</span>')

# source references -> links; the source list gets anchors
body = re.sub(r'<li>\[S(\d+)\]', lambda m: f'<li id="s{m.group(1)}"><span class="snum">S{m.group(1)}</span>', body)
body = re.sub(r'\[S(\d+)\]', lambda m: f'<a class="src" href="#s{m.group(1)}">S{m.group(1)}</a>', body)

# tables scroll on their own
body = body.replace('<table>', '<div class="tablewrap"><table>').replace('</table>', '</table></div>')

# every quote block (summaries, message templates) gets a copy button
n = [0]


def quote(m):
    n[0] += 1
    inner = m.group(1)
    text = re.sub(r'<br\s*/?>', '\n', inner)
    text = re.sub(r'</p>\s*<p>', '\n\n', text)
    text = html.unescape(re.sub(r'<[^>]+>', '', text)).strip()
    return (f'<figure class="quote"><blockquote id="q{n[0]}">{inner}</blockquote>'
            f'<figcaption><button type="button" data-copy="q{n[0]}" data-text="{html.escape(text, quote=True)}">'
            f'Text kopieren</button></figcaption></figure>')


body = re.sub(r'<blockquote>(.*?)</blockquote>', quote, body, flags=re.S)

# h2 sections become cards with ids for the jump bar
sections = re.split(r'(?=<h2 id=")', body)
cards = []
for s in sections:
    if not s.strip():
        continue
    cards.append(f'<section class="part">{s}</section>')
body = '\n'.join(cards)
body = body.replace('<hr />', '')

page = r'''<title>CurseForge Wachstumsplan</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
:root {
  --bg: #f6f3ef; --card: #fffdfa; --fg: #241d18; --muted: #6f6259; --line: #e5dbd1;
  --accent: #e8572a; --accent-fg: #fff; --accent-soft: #fde6dc;
  --doku: #2d5fa8; --doku-bg: #e2ebf8; --daten: #2f7d45; --daten-bg: #dff0e3;
  --abl: #8a5a00; --abl-bg: #f9ecd2; --sek: #6b4fa0; --sek-bg: #ece5f7;
  --decide: #fff4d6; --decide-line: #e9c46a; --code: #f0e9e2;
  --display: "Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #15110e; --card: #201a16; --fg: #f0e8e1; --muted: #b0a196; --line: #382e27;
    --accent: #ff7a4d; --accent-fg: #1b110c; --accent-soft: #42251a;
    --doku: #8db6f2; --doku-bg: #1c2a40; --daten: #86d39c; --daten-bg: #1b3022;
    --abl: #f0c06a; --abl-bg: #3a2c13; --sek: #c2aef0; --sek-bg: #2c2340;
    --decide: #2e2614; --decide-line: #7d6526; --code: #2a221d; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #15110e; --card: #201a16; --fg: #f0e8e1; --muted: #b0a196; --line: #382e27;
  --accent: #ff7a4d; --accent-fg: #1b110c; --accent-soft: #42251a;
  --doku: #8db6f2; --doku-bg: #1c2a40; --daten: #86d39c; --daten-bg: #1b3022;
  --abl: #f0c06a; --abl-bg: #3a2c13; --sek: #c2aef0; --sek-bg: #2c2340;
  --decide: #2e2614; --decide-line: #7d6526; --code: #2a221d; color-scheme: dark;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { background: var(--bg); color: var(--fg); font: 16px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif; }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--bg); }
.wrap { max-width: 820px; margin: 0 auto; padding-block: 26px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: grid; gap: 18px; }
header { display: grid; gap: 8px; }
.kicker { font: 600 12px/1 var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }
h1 { font: 700 clamp(30px, 7.5vw, 44px)/1.04 var(--display); margin: 0; text-wrap: balance; letter-spacing: -.01em; }
header p { margin: 0; color: var(--muted); max-width: 64ch; }
.legend { display: flex; flex-wrap: wrap; gap: 6px 10px; align-items: center; font-size: 13px; color: var(--muted); }
nav.jump { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--bg); padding-block: 8px;
  display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; border-bottom: 1px solid var(--line); }
nav.jump::-webkit-scrollbar { display: none; }
nav.jump a { flex: none; font: 600 13px/1 system-ui, sans-serif; color: var(--fg); text-decoration: none;
  background: var(--card); border: 1px solid var(--line); border-radius: 999px; padding: 8px 12px; }
nav.jump a:focus-visible, button:focus-visible, a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.decide { background: var(--decide); border: 1px solid var(--decide-line); border-radius: 14px; padding: 16px 18px; display: grid; gap: 10px; }
.decide h2 { margin: 0; font: 700 20px/1.2 var(--display); }
.decide ol { margin: 0; padding-left: 20px; display: grid; gap: 8px; }
.part { background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 18px 18px 8px; min-width: 0; scroll-margin-top: 64px; }
.part h2 { font: 700 clamp(22px, 5vw, 28px)/1.15 var(--display); margin: 0 0 12px; text-wrap: balance; }
.part h3 { font: 700 18px/1.25 var(--display); margin: 22px 0 8px; }
.part p, .part li { max-width: 68ch; }
.part ul, .part ol { padding-left: 22px; }
.part li { margin: 4px 0; }
.part li > ul { margin: 4px 0; }
.tablewrap { overflow-x: auto; margin: 10px 0 14px; border: 1px solid var(--line); border-radius: 10px; }
table { border-collapse: collapse; width: 100%; font-size: 14px; }
th, td { text-align: left; vertical-align: top; padding: 8px 10px; border-bottom: 1px solid var(--line); min-width: 110px; }
th { background: var(--code); font-weight: 600; }
tr:last-child td { border-bottom: 0; }
code { font: 13px var(--mono); background: var(--code); border-radius: 4px; padding: 1px 5px; overflow-wrap: anywhere; }
pre { background: var(--code); border-radius: 10px; padding: 12px; overflow-x: auto; font: 12.5px/1.5 var(--mono); }
pre code { background: none; padding: 0; overflow-wrap: normal; }
.tag { display: inline-block; font: 600 11px/1 var(--mono); letter-spacing: .04em; text-transform: uppercase; border-radius: 5px;
  padding: 4px 6px; margin: 0 2px; vertical-align: 1px; }
.tag.doku { background: var(--doku-bg); color: var(--doku); }
.tag.daten { background: var(--daten-bg); color: var(--daten); }
.tag.ableitung { background: var(--abl-bg); color: var(--abl); }
.tag.sekundaer { background: var(--sek-bg); color: var(--sek); }
a { color: var(--accent); }
a.src { font: 600 11px var(--mono); text-decoration: none; background: var(--accent-soft); border-radius: 4px; padding: 2px 4px; }
.muted { color: var(--muted); }
figure.quote { margin: 12px 0 16px; }
blockquote { margin: 0; border-left: 3px solid var(--accent); background: var(--code); border-radius: 0 10px 10px 0; padding: 10px 14px; }
blockquote p { margin: 6px 0; }
figcaption { margin-top: 6px; }
button { font: 600 13px/1 system-ui, sans-serif; border-radius: 9px; padding: 9px 12px; cursor: pointer;
  border: 1px solid var(--line); background: var(--card); color: var(--fg); }
li[id^="s"] { scroll-margin-top: 64px; overflow-wrap: anywhere; font-size: 14px; }
.snum { font: 600 12px var(--mono); color: var(--accent); margin-right: 6px; }
footer { font-size: 13px; color: var(--muted); }
</style>

<div class="wrap">
  <header>
    <div class="kicker">Stand 7. November 2026 · Dreamcraft, Beach Craft, Quest Icons, Tamagotchi</div>
    <h1>CurseForge Wachstumsplan</h1>
    <p>Wie CurseForge sortiert und sucht, was deine Projekte daraus lernen, welche neuen Projekte sich lohnen und wie eine Outreach-Kampagne an Pack-Autoren und Creator aussehen kann. Mit Daten vom 6./7. November und 47 Quellen.</p>
    <div class="legend">Jede Aussage trägt eine Marke:
      <span class="tag doku">Doku</span> von CurseForge selbst
      <span class="tag daten">Daten</span> eigene Messung
      <span class="tag ableitung">Ableitung</span> Schlussfolgerung</div>
  </header>

  <nav class="jump" aria-label="Abschnitte">
    <a href="#entscheiden">Entscheiden</a>
    <a href="#auf-einen-blick-die-10-wichtigsten-schritte">10 Schritte</a>
    <a href="#deine-projekte-heute">Deine Projekte</a>
    <a href="#teil-1-wie-curseforge-sortiert-und-zeigt">Algorithmus</a>
    <a href="#teil-2-optimierung-und-neue-projekte">Optimierung</a>
    <a href="#2-7-welche-neuen-projekte-rangliste">Neue Projekte</a>
    <a href="#teil-3-automatisierte-cold-outreach-kampagne">Outreach</a>
    <a href="#quellen">Quellen</a>
  </nav>

  <section class="decide" id="entscheiden" style="scroll-margin-top:64px">
    <h2>Drei Dinge, die du entscheiden solltest</h2>
    <ol>
      <li><b>Bisect-Banner oben?</b> Die Moderationsregeln vom 22.10.2026 sagen: Banner von Server-Hostern gehören ans Ende der Seite, „with the exception of the integrated Bisect Hosting banner“. Ich habe den Wortlaut selbst nachgelesen. Ob deine eigenen Bisect-Grafiken mit Code KASAX007 als „integriert“ gelten, sagt die Regel nicht. Wenn du sicher gehen willst, verschiebe ich sie in allen vier neuen Beschreibungen nach unten.</li>
      <li><b>Name „Tamagotchi“:</b> Das ist eine Marke von Bandai. Eine Beschwerde könnte die Mod von CurseForge nehmen. Ein eigener Name mit „Tamagotchi-like pets“ in der Summary wäre sicherer (allgemeine Information, keine Rechtsberatung).</li>
      <li><b>Namen und Summaries ändern:</b> Die Suche liest nur Name und Summary. Die Vorschläge stehen unten bei jedem Projekt zum Kopieren. Name, Summary und Kategorien änderst du in der Author Console; das kann ich nicht per API.</li>
    </ol>
  </section>

''' + body + r'''

  <footer>Der vollständige Bericht liegt im Archiv-Repo unter research/curseforge-wachstum-2026-11.md, die Rohdaten daneben als CSV.</footer>
</div>

<script>
(function () {
  function flash(btn, msg) {
    var old = btn.dataset.label || btn.textContent; btn.dataset.label = old; btn.textContent = msg;
    clearTimeout(btn._t); btn._t = setTimeout(function () { btn.textContent = old; }, 2000);
  }
  function selectText(el) {
    var r = document.createRange(); r.selectNodeContents(el);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  }
  document.querySelectorAll('button[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-text'), q = document.getElementById(btn.getAttribute('data-copy'));
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { flash(btn, 'Kopiert ✓'); },
          function () { selectText(q); flash(btn, 'Markiert: jetzt kopieren'); });
      } else { selectText(q); flash(btn, 'Markiert: jetzt kopieren'); }
    });
  });
})();
</script>
'''
open(out, 'w', encoding='utf-8').write(page)
print('page', len(page) // 1024, 'KB,', n[0], 'quotes')
