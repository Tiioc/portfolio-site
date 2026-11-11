// Renders the three LinkedIn thumbnails (1200x627, saved at 2x) from tools/thumbnails.html.
// Run: node tools/render_thumbnails.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const pg = await (await b.newContext({ viewport: { width: 1300, height: 700 }, deviceScaleFactor: 2 })).newPage();
  await pg.goto('file://' + path.resolve(__dirname, 'thumbnails.html'), { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready);
  for (const id of ['general', 'inboxowner', 'member-billing']) {
    const el = pg.locator('#' + id);
    const box = await el.boundingBox();
    const overflow = await el.evaluate(n => n.scrollHeight > n.clientHeight || n.scrollWidth > n.clientWidth);
    await el.screenshot({ path: path.resolve(__dirname, '../linkedin', `linkedin-${id}.png`) });
    console.log(id, Math.round(box.width) + 'x' + Math.round(box.height), 'overflow', overflow);
  }
  await b.close();
})();
