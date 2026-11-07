const { chromium } = require('playwright');
const fs = require('fs');
const SP = process.env.SP, SITE = SP + '/descpage/site';
(async () => {
  const body = fs.readFileSync(SITE + '/curseforge-beschreibungen.html', 'utf8');
  const doc = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + body + '</body></html>';
  const browser = await chromium.launch();
  for (const scheme of ['light', 'dark']) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, colorScheme: scheme });
    await ctx.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: 'https://m.test' });
    await ctx.route('https://m.test/**', r => { const f = SITE + new URL(r.request().url()).pathname; r.fulfill({ status: 200, contentType: f.endsWith('.jpg') ? 'image/jpeg' : 'text/html; charset=utf-8', body: f.endsWith('/') ? doc : fs.readFileSync(f) }); });
    const page = await ctx.newPage();
    await page.goto('https://m.test/');
    const n = await page.$$eval('button[data-copytext]', b => b.length);
    if (scheme === 'light') {
      for (const k of ['bc', 'dc', 'tama', 'qi']) {
        await page.click(`#${k} button[data-copytext]`);
        const t = await page.evaluate(() => navigator.clipboard.readText());
        console.log(k, 'summary copied:', t.slice(0, 60) + '…', t.length);
      }
    }
    await page.evaluate(() => document.querySelector('#dc .meta').scrollIntoView());
    await page.screenshot({ path: SP + `/descpage/review/meta_${scheme}.png` });
    console.log(scheme, 'copytext buttons', n);
    await ctx.close();
  }
  await browser.close();
})();
