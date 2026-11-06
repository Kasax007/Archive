// Local check of the 1080p page: pieces are served from disk under /_blob/<id>, downloads.save is mocked and the
// saved Blob is compared byte for byte (sha256) with the film.
const { chromium } = require('playwright');
const fs = require('fs'), crypto = require('crypto');
const SP = process.env.SP, DIR = SP + '/share1080';
const ids = JSON.parse(fs.readFileSync(DIR + '/chunks.json'));
const files = ['part00','part01','part02','part03','part04','part05','part06b','part07b','part08','part09','part10','part11','part12','part13','part14','part15','part16','part17','part18','part19'];
const FILM = SP + '/yt/Beach Craft 3.1 - Tides of the Deep (1080p60, HEVC).mp4';
(async () => {
  const body = fs.readFileSync(DIR + '/tides-1080p.html', 'utf8');
  const doc = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + body + '</body></html>';
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.route('https://dl.test/**', route => {
    const path = new URL(route.request().url()).pathname;
    if (path === '/') return route.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body: doc });
    if (path === '/poster.jpg') return route.fulfill({ status: 200, contentType: 'image/jpeg', body: fs.readFileSync(DIR + '/poster.jpg') });
    const m = path.match(/^\/_blob\/([0-9a-f]{32})$/);
    if (m) { const i = ids.indexOf(m[1]); return route.fulfill({ status: 200, contentType: 'video/mp4', body: fs.readFileSync(DIR + '/v3/' + files[i] + '.mp4') }); }
    route.fulfill({ status: 404, body: '' });
  });
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  await page.addInitScript(() => {
    window.__saved = null;
    window.claude = { use: async (name) => name === 'downloads' ? { save: async (req) => { window.__saved = req; return { status: 'saved' }; } } : null };
  });
  await page.goto('https://dl.test/');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  await page.click('#load');
  await page.waitForSelector('#save:not([hidden])', { timeout: 120000 });
  await page.screenshot({ path: SP + '/descpage/review/dl_page.png', fullPage: true });
  await page.click('#save');
  await page.waitForFunction(() => window.__saved !== null);
  const info = await page.evaluate(async () => {
    const d = window.__saved.data;
    const buf = await d.arrayBuffer();
    const h = await crypto.subtle.digest('SHA-256', buf);
    return { name: window.__saved.filename, size: d.size, sha: Array.from(new Uint8Array(h)).map(b => b.toString(16).padStart(2, '0')).join('') };
  });
  const want = crypto.createHash('sha256').update(fs.readFileSync(FILM)).digest('hex');
  console.log('overflow', overflow, 'errors', JSON.stringify(errs));
  console.log('saved', info.name, info.size, info.sha === want ? 'sha256 matches the film' : 'SHA MISMATCH');
  console.log('status:', await page.textContent('#status'));
  await browser.close();
})();
