// Renders a CurseForge description (HTML for the editor's source view) the way the project page shows it, as a
// full-page PNG for the delivery page. Images from the public repos are read from the local checkouts instead.
//
//   node preview.js DESCRIPTION.html OUT.png [URL_PREFIX=LOCAL_DIR ...]
//
// Example prefix: https://raw.githubusercontent.com/Kasax007/Kasax_Raft_Mod/26.3/docs/curseforge/img/=/home/user/Kasax_Raft_Mod/docs/curseforge/img/
// YouTube players (iframes) become a dashed placeholder; spoilers stay closed like on CurseForge.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const [src, out, ...maps] = process.argv.slice(2);
let html = fs.readFileSync(src, 'utf8');
for (const m of maps) {
  const i = m.indexOf('=');
  const from = m.slice(0, i), to = 'file://' + path.resolve(m.slice(i + 1)) + '/';
  html = html.split(from).join(to);
}
html = html.replace(/<iframe[^>]*><\/iframe>/g,
  '<span class="yt" style="width:405px;height:240px">YouTube video</span>');
const page = `<!doctype html><html><head><meta charset="utf-8"><style>
  body { margin: 0; background: #18181b; color: #e4e4e7; font: 16px/1.6 Inter, "Segoe UI", Arial, sans-serif; }
  .col { width: 1000px; margin: 0 auto; padding: 24px 0 40px; }
  img { max-width: 100%; height: auto; }
  a { color: #f16436; }
  h3 { font-size: 20px; line-height: 1.4; margin: 12px 0; }
  p { margin: 8px 0; }
  .yt { display: inline-flex; align-items: center; justify-content: center; max-width: 100%; background: #000;
        color: #aaa; border: 2px dashed #555; box-sizing: border-box; }
  .spoiler { border: 1px solid #3f3f46; border-radius: 6px; padding: 0; background: #202024; }
  .spoiler::before { content: "Spoiler (click to show)"; display: block; padding: 8px 16px; color: #a1a1aa; }
  .spoiler > * { display: none; }
</style></head><body><div class="col">${html}</div></body></html>`;
const tmp = path.join(path.dirname(path.resolve(out)), path.basename(out, '.png') + '.render.html');
fs.writeFileSync(tmp, page);

(async () => {
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1048, height: 900 }, deviceScaleFactor: 1 });
  await p.goto('file://' + tmp, { waitUntil: 'load' });
  await p.waitForTimeout(500);
  const broken = await p.$$eval('img', imgs => imgs.filter(i => i.src.startsWith('file:') && !i.naturalWidth).map(i => i.src));
  await p.screenshot({ path: out, fullPage: true });
  await browser.close();
  fs.unlinkSync(tmp);
  console.log(out, broken.length ? 'MISSING ' + broken.join(' ') : 'all local images loaded');
})();
