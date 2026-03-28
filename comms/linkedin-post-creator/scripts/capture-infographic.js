/**
 * capture-infographic.js
 * 
 * Captures a standalone HTML infographic as a high-res PNG using Puppeteer.
 * 
 * Usage:
 *   node capture-infographic.js <input.html> <output.png> [width] [height]
 * 
 * Defaults: 1080x1350 at 2x device pixel ratio (final image: 2160x2700)
 * 
 * Puppeteer is available via the mermaid-cli global package.
 * Chrome binary is at ~/.cache/puppeteer/chrome/
 */

const path = require('path');
const fs = require('fs');

async function findChrome() {
  const cacheDir = path.join(require('os').homedir(), '.cache', 'puppeteer', 'chrome');
  if (!fs.existsSync(cacheDir)) return null;
  const versions = fs.readdirSync(cacheDir);
  for (const ver of versions.sort().reverse()) {
    const candidate = path.join(cacheDir, ver, 'chrome-linux64', 'chrome');
    if (fs.existsSync(candidate)) return candidate;
  }
  return null;
}

async function capture(htmlPath, outputPath, width = 1080, height = 1350) {
  // Load puppeteer from mermaid-cli's dependency
  let puppeteer;
  const mermaidPuppeteer = path.join(
    require('os').homedir(),
    '.npm-global/lib/node_modules/@mermaid-js/mermaid-cli/node_modules/puppeteer'
  );
  if (fs.existsSync(mermaidPuppeteer)) {
    puppeteer = require(mermaidPuppeteer);
  } else {
    puppeteer = require('puppeteer');
  }

  const chromePath = await findChrome();
  if (!chromePath) throw new Error('Chrome not found in ~/.cache/puppeteer/');

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: chromePath,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 2 });

  const absPath = path.resolve(htmlPath);
  await page.goto(`file://${absPath}`, { waitUntil: 'networkidle0', timeout: 15000 });

  // Wait for any fonts to settle
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 500));

  // Try to screenshot the #root element, fall back to clip
  const rootEl = await page.$('#root');
  if (rootEl) {
    await rootEl.screenshot({ path: outputPath, type: 'png' });
  } else {
    await page.screenshot({ path: outputPath, type: 'png', clip: { x: 0, y: 0, width, height } });
  }

  await browser.close();
  console.log(`PNG saved: ${outputPath}`);
}

// CLI entry point
const [,, htmlArg, outArg, wArg, hArg] = process.argv;
if (!htmlArg || !outArg) {
  console.error('Usage: node capture-infographic.js <input.html> <output.png> [width] [height]');
  process.exit(1);
}

capture(htmlArg, outArg, parseInt(wArg) || 1080, parseInt(hArg) || 1350)
  .catch(err => { console.error(err); process.exit(1); });
