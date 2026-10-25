// Renderiza cada .slide[data-nome] de um HTML em PNG.
// Uso: node pecas/render-slides.mjs <html> <pasta> [--guia]
//   --guia: marca as zonas do app e a área do sticker (só pra revisão, não postar).
// Chrome: $CHROME, senão /usr/bin/google-chrome, senão o Chromium do Playwright (npx playwright-core install chromium).
import { createRequire } from 'module'; import path from 'path'; import fs from 'fs';
const req = createRequire(import.meta.url);
let pw;
try { pw = req('playwright-core'); }
catch { pw = createRequire('/home/mucida/imaginario/tools/marketing-mcp/package.json')('playwright-core'); }
const { chromium } = pw;
const [html, outDir, flag] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const exe = process.env.CHROME || (fs.existsSync('/usr/bin/google-chrome') ? '/usr/bin/google-chrome' : undefined);
const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto('file://' + path.resolve(html) + (flag === '--guia' ? '#guia' : ''));
await page.evaluate(() => document.fonts.ready);
const slides = await page.$$('.slide');
for (const [i, s] of slides.entries()) {
  const nome = (await s.getAttribute('data-nome')) || String(i + 1).padStart(2, '0');
  await s.screenshot({ path: path.join(outDir, `${nome}.png`) });
}
console.log(`${slides.length} slides em ${outDir}`); await browser.close();
