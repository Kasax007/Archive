// Checks the delivery page: for every project the copy button (with and without a YouTube id where the project has
// a video), the YouTube texts, the saved links after a reload, both themes and the phone width.
//   SP=<scratchpad> node test.js <config.json> <site dir>
const { chromium } = require('playwright');
const fs = require('fs');
const SP = process.env.SP;
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const SITE = process.argv[3];
const ORIGIN = 'https://desc.test';
let failed = 0;
const check = (ok, msg) => { console.log((ok ? 'ok   ' : 'FAIL ') + msg); if (!ok) failed++; };

(async () => {
  const body = fs.readFileSync(SITE + '/curseforge-beschreibungen.html', 'utf8');
  const doc = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    + '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style>'
    + '</head><body>' + body + '</body></html>';
  fs.writeFileSync(SITE + '/_test.html', doc);
  const browser = await chromium.launch();
  for (const scheme of ['light', 'dark']) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, colorScheme: scheme, deviceScaleFactor: 1 });
    await ctx.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: ORIGIN });
    await ctx.route(ORIGIN + '/**', route => {
      const f = SITE + new URL(route.request().url()).pathname;
      route.fulfill({ status: 200, contentType: f.endsWith('.jpg') ? 'image/jpeg' : 'text/html; charset=utf-8', body: fs.readFileSync(f) });
    });
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(String(e)));
    await page.goto(ORIGIN + '/_test.html');
    await page.waitForTimeout(800);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    check(overflow === 0, `${scheme}: no sideways scrolling (${overflow})`);
    await page.screenshot({ path: SP + `/descpage/review/page_${scheme}.png`, fullPage: true });
    if (scheme === 'light') {
      const read = () => page.evaluate(() => navigator.clipboard.readText());
      for (const p of cfg.projects) {
        const k = p.key, exp = fs.readFileSync(p.html, 'utf8').replace(/<p[^>]*>\s*<iframe[^>]*>\s*<\/iframe>\s*<\/p>\s*/g, '');
        if (p.video) await page.fill(`#yt-${k}`, '');
        await page.click(`button[data-copy="${k}"]`);
        let t = await read();
        if (p.video) {
          check(!t.includes('VIDEO_ID') && !t.includes('<iframe') && !t.includes('VIDEO START'), `${k}: without a link the video block is cut out`);
          check(t.length < exp.length && t.length > exp.length * 0.5, `${k}: the rest of the page is there (${t.length} of ${exp.length})`);
          const id = ('AbCdEfGhI' + k + 'xx').slice(0, 11).replace(/[^A-Za-z0-9_-]/g, 'x');
          await page.fill(`#yt-${k}`, `https://youtu.be/${id}`);
          await page.click(`button[data-copy="${k}"]`);
          t = await read();
          const n = exp.split('VIDEO_ID').length - 1;
          check(t === exp.split('VIDEO_ID').join(id) && t.split(id).length - 1 === n, `${k}: with a link the id is in all ${n} places`);
          const details = page.locator(`#${k} details:not(.preview) summary`);
          await details.click();
          await page.click(`button[data-copy="${k}_ytTitle"]`);
          check((await read()) === p.video.yt_title, `${k}: YouTube title copies`);
          await page.click(`button[data-copy="${k}_ytDesc"]`);
          check((await read()).trim() === fs.readFileSync(p.video.yt_desc, 'utf8').trim(), `${k}: YouTube description copies`);
        } else {
          check(t === exp, `${k}: copy equals the file`);
        }
        const img = await page.$(`#${k} details.preview img`);
        check(!p.preview || !!img, `${k}: preview picture present`);
      }
      await page.reload();
      await page.waitForTimeout(300);
      for (const p of cfg.projects.filter(p => p.video)) {
        check((await page.inputValue(`#yt-${p.key}`)).startsWith('https://youtu.be/'), `${p.key}: saved link restored after reload`);
      }
      await page.fill('#yt-bc', 'not a link');
      check((await page.textContent('#yt-state-bc')).includes('nicht nach einem YouTube-Link'), 'bc: a bad link is reported');
      await page.click('#dc details.preview summary');
      await page.waitForTimeout(500);
      await page.locator('#dc').screenshot({ path: SP + '/descpage/review/page_card_dc.png' });
    }
    check(errs.length === 0, `${scheme}: no script errors ${JSON.stringify(errs)}`);
    await ctx.close();
  }
  await browser.close();
  fs.unlinkSync(SITE + '/_test.html');
  console.log(failed ? `${failed} FAILED` : 'all checks passed');
  process.exit(failed ? 1 : 0);
})();
