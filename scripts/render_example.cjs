// MIT; see ../LICENSE-CODE. Requires Playwright + Chromium and Source Han Sans CN.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
(async () => {
  const folder = path.resolve(__dirname, '../plugins/medical-illustration/skills/medical-illustration/examples/editable-lettering');
  const lettered = fs.readFileSync(path.join(folder, 'lettered.svg'), 'utf8');
  const base = fs.readFileSync(path.join(folder, 'base.svg'), 'utf8');
  const browser = await chromium.launch({headless: true, executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || chromium.executablePath()});
  try {
    const page = await browser.newPage({viewport: {width: 800, height: 1000}, deviceScaleFactor: 1});
    await page.setContent(`<html><head><style>@page{size:800px 1000px;margin:0}body{margin:0}svg{display:block}</style></head><body>${lettered}</body></html>`);
    await page.evaluate(() => document.fonts.ready);
    const issues = await page.evaluate(() => [...document.querySelectorAll('text')].map(t => ({text:t.textContent,b:t.getBBox()})).filter(x=>x.b.x<0||x.b.y<0||x.b.x+x.b.width>800||x.b.y+x.b.height>1000).map(x=>x.text));
    if(issues.length) throw Error('Text outside canvas: '+issues.join(', '));
    await page.pdf({path: path.join(folder, 'review.pdf'), preferCSSPageSize: true, printBackground: true});
    await page.setViewportSize({width: 1200, height: 835});
    await page.setContent(`<html><head><style>body{margin:0;background:#e7ede7;font-family:'Source Han Sans CN',sans-serif;color:#163b3c}.wrap{padding:28px 40px}.label{display:flex;justify-content:space-between;margin-bottom:18px;font-size:18px}.panels{display:flex;gap:28px}.panel{background:#fff;width:546px;box-shadow:0 8px 22px #163b3c15}.panel svg{width:546px;height:auto;display:block}.footer{margin-top:20px;font-size:15px;color:#526c6a}</style></head><body><div class="wrap"><div class="label"><span>01　无字底版 · 图形与文字分离</span><span>02　可编辑排字 · PDF 审阅导出</span></div><div class="panels"><div class="panel">${base}</div><div class="panel">${lettered}</div></div><div class="footer">同一版面，独立文字层。草稿演示，无医学论断。</div></div></body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({path:path.join(folder,'preview.png'),fullPage:true});
    console.log('Rendered editable SVG → PDF and preview; canvas text bounds passed.');
  } finally { await browser.close(); }
})().catch(e => {console.error(e);process.exitCode=1;});
