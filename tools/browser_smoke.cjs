/* Real Chromium smoke tests of the production HTML, CSS and JS. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const ROOT='http://127.0.0.1:8765/';
const SHOTS=path.resolve('qa-shots');fs.mkdirSync(SHOTS,{recursive:true});
async function check(){
  const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
  const failures=[];
  try{
    const page=await browser.newPage({viewport:{width:1440,height:950},deviceScaleFactor:1});
    page.on('pageerror',e=>failures.push('desktop '+e.message));
    const response=await page.goto(ROOT,{waitUntil:'networkidle',timeout:20000});
    assert.equal(response.status(),200);
    await page.locator('.archive-row').first().waitFor();
    assert.equal(await page.locator('.archive-row').count(),10);
    assert.match(await page.locator('h1').innerText(),/I like making things/);
    assert.match(await page.locator('#inspector-title').innerText(),/Zhixu/);
    assert.equal(await page.locator('body').evaluate(x=>x.scrollWidth<=innerWidth+2),true,'Desktop horizontal overflow');
    await page.locator('[data-lang="zh"]').click();
    assert.match(await page.locator('h1').innerText(),/喜欢做点东西/);
    assert.match(await page.locator('#inspector-focus').innerText(),/后端|数据隔离/);
    await page.locator('[data-lang="en"]').click();
    await page.locator('[data-archive-filter="research"]').click();
    assert.equal(await page.locator('.archive-row').count(),4);
    await page.locator('[data-archive-filter="all"]').click();
    await page.locator('#archive-query').fill('PostgreSQL');
    assert.ok((await page.locator('.archive-row').count())>=1);
    assert.ok((await page.locator('.archive-row').count())<10);
    await page.locator('#archive-query').fill('');
    const selected=page.locator('[aria-label="Inspect MigrationWitness"]');
    await selected.scrollIntoViewIfNeeded();
    await selected.click();
    assert.match(await page.locator('#inspector-title').innerText(),/MigrationWitness/);
    const from=await selected.getAttribute('transform'),box=await selected.boundingBox();
    assert.ok(box);
    const sx=box.x+box.width/2,sy=box.y+box.height/2;
    await page.mouse.move(sx,sy);await page.mouse.down();
    await page.mouse.move(sx-25,sy+29,{steps:10});await page.mouse.up();
    const after=await selected.getAttribute('transform');
    assert.notEqual(after,from,'SVG node should respond to pointer drag');
    await page.locator('#map-reset').click();
    assert.equal(await selected.getAttribute('transform'),from);
    await page.keyboard.press('Control+k');
    assert.equal(await page.locator('#command-dialog').evaluate(x=>x.open),true);
    await page.locator('#command-input').fill('WiFiScope');
    assert.equal(await page.locator('.command-result').count(),1);
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('#command-dialog').evaluate(x=>x.open),false);
    assert.match(await page.locator('#inspector-title').innerText(),/WiFiScope/);
    // V6: every featured project leads to an actual inspectable casebook.
    await page.locator('#casebook-from-inspector').click();
    assert.equal(await page.locator('#casebook-dialog').evaluate(x=>x.open),true);
    assert.match(await page.locator('#casebook-title').innerText(),/WiFiScope/);
    assert.equal(await page.locator('.casebook-stage-pill').count(),5);
    await page.locator('.casebook-stage-pill').nth(2).click();
    assert.match(await page.locator('#casebook-detail').innerText(),/capture|flow|PCAP/i);
    assert.match(page.url(),/case=wifiscope/);
    await page.screenshot({path:path.join(SHOTS,'casebook-desktop.png'),animations:'disabled'});
    await page.locator('#casebook-close').click();
    assert.equal(await page.locator('#casebook-dialog').evaluate(x=>x.open),false);
    assert.equal(new URL(page.url()).searchParams.has('case'),false);

    // Deep links work independently of the interactive graph.
    await page.goto(ROOT+'?case=migrationwitness',{waitUntil:'networkidle'});
    assert.equal(await page.locator('#casebook-dialog').evaluate(x=>x.open),true);
    assert.match(await page.locator('#casebook-title').innerText(),/MigrationWitness/);
    await page.locator('#casebook-close').click();
    await page.locator('[data-lang="zh"]').click();
    await page.locator('[data-open-case="cardcraft"]').click();
    assert.match(await page.locator('#casebook-stage-name').innerText(),/玩家操作/);
    await page.locator('.casebook-stage-pill').nth(1).click();
    assert.match(await page.locator('#casebook-stage-name').innerText(),/房间生命周期/);
    await page.locator('#casebook-close').click();
    await page.locator('[data-lang="en"]').click();

    // Fallback summaries for the four remaining public projects.
    const row=page.locator('.archive-row').filter({hasText:'ImportProof'});
    await row.locator('button').click();
    assert.equal(await page.locator('.casebook-stage-pill').count(),3);
    assert.match(await page.locator('#casebook-title').innerText(),/ImportProof/);
    await page.locator('#casebook-close').click();

    // Accessibility: audit the rendered desktop experience (not only markup).
    await page.addScriptTag({path:require.resolve('axe-core')});
    const audit=await page.evaluate(async()=>axe.run(document,{
      runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}
    }));
    const severe=audit.violations.filter(v=>['critical','serious'].includes(v.impact));
    if(severe.length)console.error('AXE serious/critical findings:',JSON.stringify(severe.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target).slice(0,8)}))));
    assert.equal(severe.length,0,'Serious/critical accessibility violations');

    const budget=await page.evaluate(()=>performance.getEntriesByType('resource')
      .filter(x=>x.name.startsWith(location.origin)).reduce((sum,x)=>sum+(x.transferSize||x.encodedBodySize||0),0));
    assert.ok(budget<280000,'Static source transfer exceeds 280KB: '+budget);
    console.log('Local resource transfer budget:',budget,'bytes; axe violations:',audit.violations.length);
    await page.evaluate(()=>scrollTo(0,0));
    await page.locator('body').click({position:{x:5,y:5},force:true});
    await page.screenshot({path:path.join(SHOTS,'desktop.png'),fullPage:true,animations:'disabled'});
    const mobile=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
    mobile.on('pageerror',e=>failures.push('mobile '+e.message));
    await mobile.goto(ROOT,{waitUntil:'networkidle',timeout:20000});
    await mobile.locator('.archive-row').first().waitFor();
    assert.equal(await mobile.locator('body').evaluate(x=>x.scrollWidth<=innerWidth+2),true,'Mobile horizontal overflow');
    await mobile.locator('[data-lang="zh"]').click();
    assert.match(await mobile.locator('h1').innerText(),/喜欢做点东西/);
    await mobile.locator('#archive-query').fill('CardCraft');
    assert.equal(await mobile.locator('.archive-row').count(),1);
    await mobile.locator('#archive-query').fill('');
    // Modal and stage controls are also usable on a 390px touch layout.
    await mobile.locator('.archive-row').filter({hasText:'Zhixu'}).locator('button').click();
    assert.equal(await mobile.locator('#casebook-dialog').evaluate(x=>x.open),true);
    assert.match(await mobile.locator('#casebook-title').innerText(),/Zhixu/);
    await mobile.locator('.casebook-stage-pill').nth(3).click();
    assert.match(await mobile.locator('#casebook-stage-name').innerText(),/回答/);
    await mobile.screenshot({path:path.join(SHOTS,'casebook-mobile.png'),animations:'disabled'});
    assert.equal(await mobile.locator('#casebook-dialog').evaluate(x=>x.scrollWidth<=x.clientWidth+2),true,'Case modal horizontal overflow');
    await mobile.locator('#casebook-close').click();
    await mobile.evaluate(()=>scrollTo(0,0));
    await mobile.screenshot({path:path.join(SHOTS,'mobile.png'),fullPage:true,animations:'disabled'});
    const reduced=await browser.newPage({viewport:{width:1280,height:800},reducedMotion:'reduce'});
    reduced.on('pageerror',e=>failures.push('reduced '+e.message));
    await reduced.goto(ROOT,{waitUntil:'networkidle',timeout:20000});
    const duration=await reduced.locator('.hero-rings').evaluate(x=>parseFloat(getComputedStyle(x).animationDuration));
    assert.ok(duration<0.001,'Reduced-motion CSS should disable orbital rotation');
    await reduced.locator('[data-lang="zh"]').click();
    assert.equal(await reduced.locator('.archive-row').count(),10);
    await reduced.screenshot({path:path.join(SHOTS,'reduced-motion.png'),animations:'disabled'});
    assert.deepEqual(failures,[]);
    console.log('Chromium smoke passed: desktop, mobile, reduced motion, localization, graph dragging and palette.');
  } finally {await browser.close();}
}
check().catch(error=>{console.error(error);process.exitCode=1;});
