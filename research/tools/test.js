const { chromium } = require('playwright');
const fs = require('fs');
const SP = process.env.SP;
(async () => {
  const body = fs.readFileSync(SP + '/growth/curseforge-wachstumsplan.html', 'utf8');
  const doc = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + body + '</body></html>';
  const browser = await chromium.launch();
  for (const scheme of ['light', 'dark']) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, colorScheme: scheme });
    await ctx.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: 'https://g.test' });
    await ctx.route('https://g.test/**', r => r.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body: doc }));
    const page = await ctx.newPage();
    const errs = []; page.on('pageerror', e => errs.push(String(e)));
    await page.goto('https://g.test/');
    await page.waitForTimeout(600);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    const missing = await page.evaluate(() => [...document.querySelectorAll('nav.jump a, a.src')].map(a => a.getAttribute('href')).filter(h => h.startsWith('#') && !document.getElementById(h.slice(1))));
    if (scheme === 'light') {
      await page.click('button[data-copy="q1"]');
      const t = await page.evaluate(() => navigator.clipboard.readText());
      console.log('copy q1:', JSON.stringify(t.slice(0, 90)));
      await page.screenshot({ path: SP + '/descpage/review/growth_top.png' });
      await page.click('nav.jump a[href="#teil-3-automatisierte-cold-outreach-kampagne"]');
      await page.waitForTimeout(800);
      await page.screenshot({ path: SP + '/descpage/review/growth_outreach.png' });
    } else {
      await page.screenshot({ path: SP + '/descpage/review/growth_dark.png' });
    }
    console.log(scheme, 'overflow', overflow, 'missing anchors', JSON.stringify(missing), 'errors', JSON.stringify(errs));
    await ctx.close();
  }
  await browser.close();
})();
