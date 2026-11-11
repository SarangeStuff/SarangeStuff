// Render an exam-style HTML file to an A4 PDF with a running header and page footer.
//   node render.js <in.html> <out.pdf> "<header left>" "<header right>" [<local-mathjax-package-dir>]
const { chromium } = require('playwright');
const path = require('path');
const [,, src, out, left, right, mjdir] = process.argv;
const hdr = `<div style="width:100%;font:10pt 'Liberation Serif','Times New Roman',serif;color:#000;padding:0 12mm;display:flex;justify-content:space-between"><span>${left}</span><span>${right}</span></div>`;
const ftr = `<div style="width:100%;font:10pt 'Liberation Serif','Times New Roman',serif;color:#000;text-align:center">Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ colorScheme: 'light' });
  await p.route(/fonts\.(googleapis|gstatic)\.com/, r => r.fulfill({ status: 200, contentType: 'text/css', body: '' }));
  if (mjdir) await p.route(/cdn\.jsdelivr\.net/, r => r.fulfill({ status: 200, path: path.join(mjdir, r.request().url().split('mathjax@3.2.2/')[1]), contentType: 'application/javascript' }));
  await p.goto('file://' + path.resolve(src));
  const hasMJ = await p.evaluate(() => !!document.querySelector('script[src*="mathjax"]'));
  if (hasMJ) {
    await p.waitForFunction(() => window.MathJax && MathJax.startup && MathJax.startup.promise, null, { timeout: 30000 });
    await p.evaluate(() => MathJax.startup.promise);
  }
  await p.waitForTimeout(400);
  await p.emulateMedia({ media: 'print' });
  await p.pdf({ path: out, format: 'A4', printBackground: true, outline: true, tagged: true,
    displayHeaderFooter: true, headerTemplate: hdr, footerTemplate: ftr,
    margin: { top: '22mm', bottom: '18mm', left: '14mm', right: '14mm' } });
  await b.close();
})();
