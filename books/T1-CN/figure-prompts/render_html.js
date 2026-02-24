const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const outDir = '/home/claude/figure_output';

async function renderHTML(htmlFile, outName, width = 900, height = 650) {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none']
    });
    const page = await browser.newPage();
    await page.setViewport({ width, height, deviceScaleFactor: 3 }); // 3x for 300dpi equivalent
    
    const htmlPath = path.resolve(htmlFile);
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0', timeout: 15000 });
    
    // Wait for fonts to load
    await page.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 1000));
    
    const outPath = path.join(outDir, outName);
    await page.screenshot({ path: outPath, fullPage: true, type: 'png' });
    await browser.close();
    
    const stats = fs.statSync(outPath);
    console.log(`✅ ${outName} (${Math.round(stats.size/1024)}KB)`);
}

(async () => {
    console.log('Rendering HTML figures to PNG...\n');
    
    await renderHTML('/home/claude/fig_02_02.html', 'fig_02_02_v2_pyramid.png', 900, 620);
    await renderHTML('/home/claude/fig_01_04.html', 'fig_01_04_v2_hierarchy.png', 900, 670);
    await renderHTML('/home/claude/fig_06_04.html', 'fig_06_04_v2_matrix.png', 900, 500);
    
    console.log('\nDone!');
})();
