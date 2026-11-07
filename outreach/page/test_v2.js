// Functional test of the outreach page v2 with a fake claude runtime (db, mcp Gmail, permissions).
const { chromium } = require('playwright');
const fs = require('fs');
const SP = process.env.SP;
const body = fs.readFileSync(SP + '/outreachpage/outreach-freigabe.html', 'utf8');
const rows = JSON.parse(fs.readFileSync(SP + '/outreach_rows.json', 'utf8')).targets;
const fake = `
<script>
window.__calls = []; window.__writes = [];
(function(){
  const rows = ${JSON.stringify(rows)};
  const docs = {}; for (const k in rows) docs['targets/' + k] = rows[k];
  docs['settings/sender'] = { postal_address: 'Musterstr. 1, 12345 Musterstadt', privacy_link: '' };
  const subs = [];
  function snapColl(){ return { metadata:{fromCache:false}, docs: Object.keys(docs).filter(p=>p.startsWith('targets/')).map(p=>({id:p.slice(8), exists:true, data:()=>JSON.parse(JSON.stringify(docs[p]))})) }; }
  function fire(){ subs.forEach(s=>s()); }
  const db = {
    collection(name){ return { onSnapshot(cb){ const f=()=>cb(snapColl()); subs.push(f); setTimeout(f,10); return ()=>{}; } }; },
    doc(path){ return {
      async update(p){ window.__writes.push([path,p]); Object.assign(docs[path], p); setTimeout(fire,5); },
      async set(p){ docs[path]=p; setTimeout(fire,5); },
      onSnapshot(cb){ const f=()=>cb({exists:!!docs[path], data:()=>docs[path]}); subs.push(f); setTimeout(f,10); return ()=>{}; } }; }
  };
  const mcp = {
    async listTools(server){ return { servers: [{ server: 'Gmail', authStatus: 'connected', tools: [{name:'send_message'},{name:'create_draft'}] }] }; },
    async callTool(server, tool, input){ window.__calls.push([server, tool, input]);
      if (tool === 'send_message') return { content: [], payload: { id: 'm1', threadId: 't1', labelIds: ['SENT'] } };
      if (tool === 'create_draft') return { content: [], payload: { id: 'd1', threadId: 't2', viewUrl: 'https://mail.google.com/mail/#drafts/d1' } };
      throw { code: 'bad_request', message: 'unknown' }; }
  };
  const perms = { async state(){ return 'prompt'; }, async request(n){ return { 'mcp:Gmail': 'granted' }; }, async manage(){} };
  window.claude = { use: async (n) => n === 'db' ? db : n === 'mcp' ? mcp : n === 'permissions' ? perms : null };
})();
</script>`;
const doc = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>:root{color-scheme:light}body{margin:0}[hidden]{display:none!important}</style></head><body>' + fake + body + '</body></html>';
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: 'https://o.test' });
  await ctx.route('https://o.test/**', r => r.fulfill({ status: 200, contentType: 'text/html; charset=utf-8', body: doc }));
  const page = await ctx.newPage();
  const errors = []; page.on('pageerror', e => errors.push(e.message));
  await page.goto('https://o.test/');
  await page.waitForTimeout(400);
  console.log('gmail pill:', await page.textContent('#gmailpill'));
  await page.click('#gmailacts button');
  await page.waitForTimeout(100);
  console.log('gmail pill after allow:', await page.textContent('#gmailpill'));
  // approve emaiye
  const card = page.locator('article[data-id="yt-emaiye"]');
  await card.locator('input[type=email]').fill('creator@example.com');
  await card.locator('button', { hasText: 'Freigeben' }).click();
  await page.waitForTimeout(100);
  console.log('write after approve:', JSON.stringify(window_writes = await page.evaluate(() => window.__writes.slice(-1))));
  // approved tab
  await page.click('nav.tabs button:has-text("Freigegeben")');
  await page.waitForTimeout(50);
  const a = page.locator('article[data-id="yt-emaiye"]');
  console.log('approved card visible:', await a.count());
  await a.locator('button', { hasText: /^Senden$/ }).click();
  await page.waitForTimeout(50);
  console.log('confirm shown:', await a.locator('.confirm').count());
  await a.locator('.confirm button', { hasText: 'Ja, senden' }).click();
  await page.waitForTimeout(200);
  const calls = await page.evaluate(() => window.__calls);
  console.log('mcp calls:', JSON.stringify(calls.map(c => [c[1], c[2].to, c[2].subject, c[2].body.slice(-120)])));
  const w = await page.evaluate(() => window.__writes.slice(-1)[0]);
  console.log('write after send:', JSON.stringify(w));
  // non-email approved: waymarked
  await page.click('nav.tabs button:has-text("Bereit")');
  await page.locator('article[data-id="cf-1609886-waymarked"] button', { hasText: 'Freigeben' }).click();
  await page.waitForTimeout(80);
  await page.click('nav.tabs button:has-text("Freigegeben")');
  await page.waitForTimeout(50);
  const hrefs = await page.locator('article[data-id="cf-1609886-waymarked"] a.btn').evaluateAll(as => as.map(a => a.textContent + ' -> ' + a.href));
  console.log('waymarked links:', JSON.stringify(hrefs));
  // discord-only pack
  await page.click('nav.tabs button:has-text("Bereit")');
  await page.locator('article[data-id="cf-1782391-drays-adventuries"] button', { hasText: 'Freigeben' }).click();
  await page.waitForTimeout(80);
  await page.click('nav.tabs button:has-text("Freigegeben")');
  await page.waitForTimeout(50);
  console.log('drays links:', JSON.stringify(await page.locator('article[data-id="cf-1782391-drays-adventuries"] a.btn').evaluateAll(as => as.map(a => a.textContent + ' -> ' + a.href))));
  // bulk: approve two more e-mails with addresses
  await page.click('nav.tabs button:has-text("Bereit")');
  for (const id of ['yt-Fuzzycub_', 'yt-MCG-Modding']) {
    const c = page.locator('article[data-id="' + id + '"]');
    await c.locator('input[type=email]').fill(id.slice(3).toLowerCase().replace(/[^a-z]/g, '') + '@example.com');
    await c.locator('button', { hasText: 'Freigeben' }).click();
    await page.waitForTimeout(80);
  }
  await page.click('nav.tabs button:has-text("Freigegeben")');
  await page.waitForTimeout(50);
  console.log('bulk panel:', (await page.textContent('#bulk')).slice(0, 200));
  await page.locator('#bulk button', { hasText: /^Alle/ }).click();
  await page.locator('#bulk .confirm button', { hasText: 'Ja, alle senden' }).click();
  await page.waitForTimeout(600);
  console.log('bulk after:', (await page.textContent('#bulk')).slice(0, 120));
  console.log('send calls total:', await page.evaluate(() => window.__calls.filter(c => c[1] === 'send_message').map(c => c[2].to[0]).join(', ')));
  // sent tab shows emaiye with gmail
  await page.click('nav.tabs button:has-text("Gesendet")');
  await page.waitForTimeout(50);
  console.log('sent state:', await page.locator('article[data-id="yt-emaiye"] .state').textContent());
  await page.screenshot({ path: SP + '/outreachpage/t2/mobile.png', fullPage: false });
  console.log('page errors:', JSON.stringify(errors));
  await browser.close();
})();
