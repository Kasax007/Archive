// Checks the delivery page: copy logic (YouTube id in and out), the other copies, both themes, phone width.
const { chromium } = require('playwright');
const fs = require('fs');
const SP = process.env.SP;
const SITE = SP + '/descpage/site';
const ORIGIN = 'https://desc.test';

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
    await page.screenshot({ path: SP + `/descpage/review/page_${scheme}.png`, fullPage: true });
    if (scheme === 'light') {
      const read = () => page.evaluate(() => navigator.clipboard.readText());
      const exp = fs.readFileSync(SP + '/descriptions2/beachcraft_3.1_description.html', 'utf8');
      await page.click('button[data-copy="bc"]');
      let t = await read();
      console.log('no link: VIDEO_ID', t.includes('VIDEO_ID'), 'iframe', t.includes('<iframe'), 'markers', t.includes('VIDEO START'), 'len', t.length, 'orig', exp.length);
      await page.fill('#yt', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=12s');
      console.log('state:', await page.textContent('#yt-state'));
      await page.click('button[data-copy="bc"]');
      t = await read();
      console.log('with link: VIDEO_ID', t.includes('VIDEO_ID'), 'id count', t.split('dQw4w9WgXcQ').length - 1,
        'equals replace', t === exp.split('VIDEO_ID').join('dQw4w9WgXcQ'));
      await page.fill('#yt', 'hello');
      console.log('bad link state:', await page.textContent('#yt-state'));
      await page.fill('#yt', 'https://youtu.be/AbCdEfGhI_-');
      console.log('short link state:', await page.textContent('#yt-state'));
      for (const [k, f] of [['dc', 'dreamcraft_V1.4'], ['qi', 'questicons_1.1'], ['tama', 'tamagotchi_1.2']]) {
        await page.click(`button[data-copy="${k}"]`);
        t = await read();
        console.log(k, 'equal file', t === fs.readFileSync(SP + `/descriptions2/${f}_description.html`, 'utf8'));
      }
      await page.click('details:not(.preview) summary');
      await page.click('button[data-copy="ytTitle"]');
      console.log('ytTitle', JSON.stringify(await read()));
      await page.click('button[data-copy="ytDesc"]');
      t = await read();
      console.log('ytDesc len', t.length, 'chapters', t.includes('18:13 The Story'));
      await page.reload();
      await page.waitForTimeout(300);
      console.log('restored:', await page.inputValue('#yt'));
      await page.click('details.preview summary');
      await page.waitForTimeout(500);
      await page.screenshot({ path: SP + '/descpage/review/page_preview_open.png' });
    }
    console.log(scheme, 'overflow', overflow, 'errors', JSON.stringify(errs));
    await ctx.close();
  }
  await browser.close();
})();
