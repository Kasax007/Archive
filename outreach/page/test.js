// Local check of the approval page with an in-memory stand-in for the db capability.
const { chromium } = require('playwright');
const fs = require('fs');
const SP = process.env.SP, DIR = SP + '/outreachpage';
const seed = JSON.parse(fs.readFileSync(DIR + '/seed.json')).targets;
(async () => {
  const body = fs.readFileSync(DIR + '/outreach-freigabe.html', 'utf8');
  const doc = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0}[hidden]{display:none!important}</style></head><body>' + body + '</body></html>';
  const browser = await chromium.launch();
  let fail = 0; const check = (ok, m) => { console.log((ok ? 'ok   ' : 'FAIL ') + m); if (!ok) fail++; };
  for (const scheme of ['light', 'dark']) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, colorScheme: scheme });
    await ctx.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: 'https://o.test' });
    await ctx.route('https://o.test/**', r => r.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body: doc }));
    const page = await ctx.newPage();
    const errs = []; page.on('pageerror', e => errs.push(String(e)));
    await page.addInitScript(seed => {
      const store = { targets: JSON.parse(JSON.stringify(seed)), settings: {} };
      const subs = [];
      const notify = () => subs.forEach(f => f());
      const snapDoc = (coll, id) => ({ id, exists: !!store[coll][id], data: () => store[coll][id], metadata: { fromCache: false, hasPendingWrites: false } });
      const db = {
        collection: c => ({ onSnapshot: (next) => { const f = () => next({ docs: Object.keys(store[c]).map(id => snapDoc(c, id)), metadata: { fromCache: false } }); subs.push(f); setTimeout(f, 50); return () => {}; } }),
        doc: p => { const [c, id] = p.split('/'); return {
          update: async patch => { Object.assign(store[c][id], patch); window.__writes = (window.__writes || 0) + 1; setTimeout(notify, 10); },
          set: async data => { store[c][id] = data; setTimeout(notify, 10); },
          onSnapshot: next => { const f = () => next(snapDoc(c, id)); subs.push(f); setTimeout(f, 60); return () => {}; } }; }
      };
      window.__store = store;
      window.claude = { use: async n => n === 'db' ? db : null };
    }, seed);
    await page.goto('https://o.test/');
    await page.waitForTimeout(400);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    check(overflow === 0, `${scheme}: no sideways scrolling (${overflow})`);
    const ready = await page.$$eval('#list .card', c => c.length);
    const nReady = Object.values(seed).filter(r => r.status === 'draft').length;
    check(ready === nReady, `${scheme}: ${ready} cards in "Bereit" (expected ${nReady})`);
    if (scheme === 'light') {
      await page.screenshot({ path: SP + '/descpage/review/outreach_ready.png' });
      // edit survives a live update
      const ta = page.locator('#list .card').first().locator('textarea');
      await ta.fill('EDITED TEXT {postal_address}');
      await page.evaluate(() => { const k = Object.keys(window.__store.targets).pop(); window.__store.targets[k].score += 0; });
      await page.locator('#list .card').nth(1).locator('button', { hasText: 'Nicht senden' }).click();
      await page.waitForTimeout(200);
      check((await page.locator('#list .card').first().locator('textarea').inputValue()).startsWith('EDITED TEXT'), 'unsaved edit survives a live update');
      // copy warns about the missing address
      await page.locator('#list .card').first().locator('button', { hasText: 'Text kopieren' }).click();
      check((await page.locator('#list .card').first().locator('.warn').textContent()).includes('Postanschrift'), 'copy warns when the postal address is missing');
      // sender settings fill the placeholder
      await page.click('#senderbox summary');
      await page.fill('#postal', 'Musterweg 1, 12345 Musterstadt');
      await page.click('#savesender');
      await page.waitForTimeout(200);
      await page.locator('#list .card').first().locator('button', { hasText: 'Text kopieren' }).click();
      const clip = await page.evaluate(() => navigator.clipboard.readText());
      check(clip.includes('Musterweg 1') && !clip.includes('{postal_address}'), 'copied text has the address filled in');
      // mark as sent
      await page.locator('#list .card').first().locator('button', { hasText: 'Gesendet' }).click();
      await page.waitForTimeout(200);
      await page.click('nav.tabs button[data-tab="sent"]');
      const sent = await page.$$eval('#list .card', c => c.length);
      check(sent === 1, `one card in "Gesendet" (${sent})`);
      check((await page.locator('#list .card .state').first().textContent()).includes('Nachfrage ab'), 'sent card shows the follow-up date');
      await page.click('nav.tabs button[data-tab="hold"]');
      const hold = await page.$$eval('#list .card', c => c.length);
      check(hold === Object.values(seed).filter(r => r.status === 'hold').length, `"Warten" shows the hold cards (${hold})`);
      await page.click('nav.tabs button[data-tab="done"]');
      check((await page.$$eval('#list .card', c => c.length)) === 1, '"Erledigt" shows the skipped card');
    } else {
      await page.screenshot({ path: SP + '/descpage/review/outreach_dark.png' });
    }
    check(errs.length === 0, `${scheme}: no script errors ${JSON.stringify(errs)}`);
    await ctx.close();
  }
  await browser.close();
  console.log(fail ? fail + ' FAILED' : 'all checks passed');
})();
