const {chromium} = require('/Users/shaoyikai/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
(async()=>{
  const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
  const page=await browser.newPage();
  const messages=[];
  page.on('pageerror',e=>messages.push(String(e)));
  await page.route('http://**/*',route=>route.abort());
  await page.route('https://**/*',route=>route.abort());
  await page.goto(pathToFileURL(path.join(__dirname,'complete.html')).href,{waitUntil:'load'});
  await page.evaluate(()=>document.fonts.ready);
  const missing=await page.locator('img').evaluateAll(imgs=>imgs.filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src));
  if(missing.length)throw Error('Images missing: '+missing.join(', '));
  if(fs.existsSync(path.join(__dirname,'toc_pages.json'))){
    const toc=JSON.parse(fs.readFileSync(path.join(__dirname,'toc_pages.json'),'utf8'));
    await page.evaluate(toc=>{
      for(const a of document.querySelectorAll('.toc-entry'))a.querySelector('.toc-page').textContent=toc[a.dataset.target]||'';
    },toc);
  }
  const output=path.join(__dirname,'complete_rendered.pdf');
  await page.pdf({path:output,format:'A4',preferCSSPageSize:true,printBackground:true,outline:true,tagged:true,
    displayHeaderFooter:true,
    headerTemplate:'<div style="font-family:PingFang SC,sans-serif;font-size:8px;color:#84909b;width:100%;padding:0 17mm;">26考研政治一页纸整合版</div>',
    footerTemplate:'<div style="font-family:Arial,sans-serif;font-size:8px;color:#84909b;text-align:center;width:100%;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'
  });
  console.log(JSON.stringify({output,images:await page.locator('img').count(),messages}));
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
