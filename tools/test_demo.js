// Checks the simplified InboxOwner demo: same numbers as before, every view works, no errors.
// Run with the site served at http://localhost:8765/  ->  node tools/test_demo.js
const { chromium } = require('playwright');
const assert = require('assert');
(async () => {
  const b = await chromium.launch();
  const pg = await (await b.newContext({ viewport: { width: 390, height: 900 } })).newPage();
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('http://localhost:8765/inboxowner/demo/', { waitUntil: 'networkidle' });
  await pg.evaluate(() => localStorage.clear()); await pg.reload({ waitUntil: 'networkidle' });
  let n = 0; const ok = (c, m) => { assert(c, m); n++; console.log('PASS ' + m); };
  const has = (txt, s) => txt.includes(s);

  const tabs = await pg.$$eval('#demo-tabs button', bs => bs.map(x => x.textContent));
  ok(tabs.length === 3, 'three tabs: ' + tabs.join(', '));

  const w = await pg.innerText('#p-waits');
  ok(/how long each kind of email waited/i.test(w), 'wait times view has a one-line note at the top');
  ok(has(w, '548') && has(w, 'emails'), 'same 548 emails as before');
  ok(has(w, '4.0 hrs'), 'same typical wait (4.0 hrs)');
  ok(has(w, '25%'), 'same 25% with no reply in 2 days');
  ok(has(w, 'Cancellation emails waited 18.7 hours. Trial questions waited 1.2.'), 'same 18.7 vs 1.2 hours');
  ok(has(w, '67% of cancellation emails'), 'same 67% of cancellations with no reply');
  ok(has(w, 'Maya sent 46%'), 'same 46% of replies from Maya');
  ok(has(w, '51% of emails came in while the gym was closed'), 'same 51% after hours');

  await pg.click('button[data-tab=owners]');
  let o = await pg.innerText('#p-owners');
  ok(/pick a name to claim one/i.test(o), 'owners view has a one-line note at the top');
  const mini = await pg.$$eval('#p-owners .mini b', x => x.map(e => e.textContent));
  ok(mini[0] === '13' && mini[1] === '0' && mini[2] === '11', 'same 13 waiting, 0 claimed, 11 late: ' + mini.join('/'));
  ok(has(o, '54 older emails'), 'same 54 older emails on the cleanup list');
  await pg.selectOption('#p-owners select[data-id]', 'Priya');
  ok((await pg.$$eval('#p-owners .mini b', x => x.map(e => e.textContent)))[1] === '1', 'claiming one email updates the count');
  await pg.click('#q-suggest');
  ok((await pg.$$eval('#p-owners .mini b', x => x.map(e => e.textContent)))[1] === '13', 'claim all gives all 13 an owner');
  await pg.click('#q-reset');
  ok((await pg.$$eval('#p-owners .mini b', x => x.map(e => e.textContent)))[1] === '0', 'start over clears the claims');

  await pg.click('button[data-tab=sorting]');
  const s = await pg.innerText('#p-sorting');
  ok(/guesses what it is about/i.test(s), 'sorting view has a one-line note at the top');
  ok(has(s, '87%') && has(s, '81%') && has(s, '19%'), 'same 87% right, 81% by itself, 19% to a person');
  ok(has(await pg.innerText('#t-out'), 'Membership freezes'), 'first example is sorted as a membership freeze, same as before');
  await pg.fill('#t-text', 'please call me back');
  ok(!has(await pg.innerText('#t-out'), 'Vendors'), '"please" no longer matches "lease" (vendor)');
  await pg.selectOption('#t-sample', '4');
  ok((await pg.innerText('#t-out')).length > 0, 'picking an example shows a result');

  const all = (await pg.innerText('body')).toLowerCase();
  for (const word of ['blind set', 'precision', 'recall', 'threshold', 'escalat', 'flag', 'system', 'automated']) ok(!all.includes(word), `no "${word}" on the demo`);
  ok(errs.length === 0, 'no page errors');
  console.log(`\n${n} demo checks passed`);
  await b.close();
})().catch(e => { console.error('FAIL', e.message); process.exit(1); });
