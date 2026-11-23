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
    const selected=page.locator('.graph-project[aria-label="Inspect MigrationWitness"]');
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

    // V7 comparison studio: data-driven overlap, real source links and deep-link state.
    await page.locator('#compare').scrollIntoViewIfNeeded();
    assert.equal(await page.locator('#compare-left').inputValue(),'zhixu');
    assert.equal(await page.locator('#compare-right').inputValue(),'migrationwitness');
    assert.equal(await page.locator('#compare-shared-count').innerText(),'02 / 04');
    await page.locator('[data-compare-preset="cardcraft,cost"]').click();
    assert.equal(await page.locator('#compare-shared-count').innerText(),'01 / 04');
    assert.match(await page.locator('#compare-left-title').innerText(),/CardCraft/);
    assert.match(await page.locator('#compare-right-title').innerText(),/Construction Cost Analyzer/);
    let compareUri=new URL(page.url());
    assert.equal(compareUri.searchParams.get('compare'),'cardcraft,cost');
    assert.equal(compareUri.hash,'#compare');
    await page.locator('#compare-swap').click();
    assert.equal(await page.locator('#compare-left').inputValue(),'cost');
    assert.equal(await page.locator('#compare-right').inputValue(),'cardcraft');
    await page.locator('#compare-left').selectOption('zhixu');
    assert.equal(await page.locator('#compare-left').inputValue(),'zhixu');
    await page.goto(ROOT+'?compare=wifiscope,importproof#compare',{waitUntil:'networkidle'});
    assert.equal(await page.locator('#compare-left').inputValue(),'wifiscope');
    assert.equal(await page.locator('#compare-right').inputValue(),'importproof');
    assert.equal(await page.locator('#compare-shared-count').innerText(),'02 / 04');
    assert.ok(await page.locator('#compare-left-links a').count()>=1);
    assert.ok(await page.locator('#compare-right-links a').count()>=1);
    await page.locator('[data-lang="zh"]').click();
    assert.match(await page.locator('#compare-title').innerText(),/不同的系统/);
    assert.match(await page.locator('#compare-explanation').innerText(),/都涉及/);
    await page.locator('[data-lang="en"]').click();
    await page.locator('#compare').screenshot({path:path.join(SHOTS,'comparison-desktop.png'),animations:'disabled'});

    // V8: hands-on invariant lab — interactive, deterministic, bilingual and source-backed.
    await page.locator('#lab').scrollIntoViewIfNeeded();
    assert.equal(await page.locator('#lab-verdict').getAttribute('data-status'),'pass');
    assert.equal(await page.locator('#lab-reapply').isDisabled(),true);
    await page.locator('#lab-strategy').selectOption('swap');
    assert.equal(await page.locator('#lab-reapply').isDisabled(),false);
    await page.locator('#lab-form-permission button[type=submit]').click();
    assert.equal(await page.locator('#lab-verdict').getAttribute('data-status'),'fail');
    assert.equal(await page.locator('.lab-check-status[data-good=false]').count(),3);
    assert.match(await page.locator('#lab-evidence-link').getAttribute('href'),/PG_OSC_197_RESULTS/);
    await page.locator('#lab-reapply').check();
    await page.locator('#lab-form-permission button[type=submit]').click();
    assert.equal(await page.locator('#lab-verdict').getAttribute('data-status'),'pass');
    await page.locator('#lab-tab-retrieval').click();
    assert.equal(await page.locator('#lab-tab-retrieval').getAttribute('aria-selected'),'true');
    assert.equal(await page.locator('#lab-scoped').isChecked(),true);
    assert.equal(await page.locator('#lab-verdict').getAttribute('data-status'),'pass');
    await page.locator('#lab-scoped').uncheck();
    await page.locator('#lab-form-retrieval button[type=submit]').click();
    assert.equal(await page.locator('#lab-verdict').getAttribute('data-status'),'fail');
    assert.match(await page.locator('#lab-checks').innerText(),/B-01/);
    await page.locator('#lab-scoped').check();
    await page.locator('#lab-form-retrieval button[type=submit]').click();
    assert.equal(await page.locator('#lab-verdict').getAttribute('data-status'),'pass');
    assert.equal(await page.locator('#lab-checks .lab-check-status[data-good=false]').count(),0,'Scoped retrieval must exclude all foreign tenant hits');
    await page.locator('[data-lang="zh"]').click();
    assert.match(await page.locator('#lab-title').innerText(),/动手验证/);
    assert.match(await page.locator('#lab-verdict-desc').innerText(),/租户/);
    assert.match(await page.locator('#lab-trace').innerText(),/模拟文档/);
    await page.locator('#lab').screenshot({path:path.join(SHOTS,'lab-desktop.png'),animations:'disabled'});
    await page.locator('[data-lang="en"]').click();
    await page.goto(ROOT+'?lab=retrieval#lab',{waitUntil:'networkidle'});
    assert.equal(await page.locator('#lab-tab-retrieval').getAttribute('aria-selected'),'true');
    await page.locator('#lab-tab-permission').click();
    assert.equal(await page.locator('#lab-tab-permission').getAttribute('aria-selected'),'true');
    assert.equal(new URL(page.url()).searchParams.get('lab'),'permission');

    // V9 editorial guided stories: real project actions, navigation and deep links.
    await page.goto(ROOT,{waitUntil:'networkidle'});
    await page.locator('#journey-launch').click();
    assert.equal(await page.locator('#journey-dialog').evaluate(x=>x.open),true);
    assert.equal(await page.locator('.journey-choice').count(),3);
    await page.locator('[data-journey-choice="verify"]').click();
    assert.match(await page.locator('#journey-title').innerText(),/migration finished/i);
    assert.equal(await page.locator('.journey-rail-stop').count(),4);
    assert.equal(new URL(page.url()).searchParams.get('trail'),'verify');
    await page.locator('#journey-next').click();
    assert.match(await page.locator('#journey-title').innerText(),/Try breaking/);
    assert.equal(new URL(page.url()).searchParams.get('note'),'2');
    assert.match(await page.locator('#journey-evidence-links a').first().getAttribute('href'),/migrationwitness/);
    await page.locator('#journey-action').click();
    assert.equal(await page.locator('#journey-dialog').evaluate(x=>x.open),false);
    assert.equal(await page.locator('#lab-tab-permission').getAttribute('aria-selected'),'true');

    await page.locator('#journey-launch').click();
    await page.locator('[data-journey-choice="ship"]').click();
    assert.match(await page.locator('#journey-title').innerText(),/game must actually ship/i);
    await page.locator('#journey-action').click();
    assert.equal(await page.locator('#casebook-dialog').evaluate(x=>x.open),true);
    assert.match(await page.locator('#casebook-title').innerText(),/CardCraft/);
    await page.locator('#casebook-close').click();

    await page.goto(ROOT+'?trail=bridge&note=3',{waitUntil:'networkidle'});
    assert.equal(await page.locator('#journey-dialog').evaluate(x=>x.open),true);
    assert.equal(await page.locator('#journey-step-counter').innerText(),'03 / 03');
    await page.locator('#journey-action').click();
    assert.equal(await page.locator('#journey-dialog').evaluate(x=>x.open),false);
    assert.equal(await page.locator('#compare-left').inputValue(),'cost');
    assert.equal(await page.locator('#compare-right').inputValue(),'wifiscope');

    await page.goto(ROOT,{waitUntil:'networkidle'});
    await page.locator('[data-lang="zh"]').click();
    await page.locator('#journey-launch').click();
    assert.match(await page.locator('#journey-chooser-label').innerText(),/探索路线/);
    await page.locator('[data-journey-choice="ship"]').click();
    assert.match(await page.locator('#journey-title').innerText(),/游戏需要真正交付/);
    await page.locator('#journey-next').click();
    assert.match(await page.locator('#journey-title').innerText(),/知识系统/);
    await page.screenshot({path:path.join(SHOTS,'guided-reader-desktop.png'),animations:'disabled'});
    await page.locator('#journey-close').click();
    assert.equal(new URL(page.url()).searchParams.has('trail'),false);
    await page.locator('[data-lang="en"]').click();

    // Accessibility: audit the rendered desktop experience (not only markup).
    await page.addScriptTag({path:require.resolve('axe-core')});
    const audit=await page.evaluate(async()=>axe.run(document,{
      runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}
    }));
    const severe=audit.violations.filter(v=>['critical','serious'].includes(v.impact));
    if(severe.length)console.error('AXE serious/critical findings:',JSON.stringify(severe.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target).slice(0,8)}))));
    assert.equal(severe.length,0,'Serious/critical accessibility violations');

    const budget=await page.evaluate(()=>{
      const items=performance.getEntriesByType('resource').filter(x=>x.name.startsWith(location.origin));
      const documentEntry=performance.getEntriesByType('navigation')[0];
      const jsCss=items.reduce((sum,x)=>sum+(x.decodedBodySize||x.encodedBodySize||0),0);
      return jsCss+(documentEntry?.decodedBodySize||documentEntry?.encodedBodySize||0);
    });
    assert.ok(budget<280000,'Static source transfer exceeds 280KB: '+budget);
    console.log('Decoded document and resource bytes:',budget,'bytes; axe violations:',audit.violations.length);
    await page.evaluate(()=>scrollTo(0,0));
    await page.locator('body').click({position:{x:5,y:5},force:true});
    await page.screenshot({path:path.join(SHOTS,'desktop.png'),fullPage:true,animations:'disabled'});
    const mobile=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
    mobile.on('pageerror',e=>failures.push('mobile '+e.message));
    await mobile.goto(ROOT,{waitUntil:'networkidle',timeout:20000});
    await mobile.locator('.archive-row').first().waitFor();
    assert.equal(await mobile.locator('body').evaluate(x=>x.scrollWidth<=innerWidth+2),true,'Mobile horizontal overflow');
    // V7: mobile graph becomes accessible touch cards instead of a wide scrolling canvas.
    assert.equal(await mobile.locator('#graph-frame').evaluate(x=>getComputedStyle(x).display),'none');
    assert.equal(await mobile.locator('.mobile-project-entry').count(),10);
    await mobile.locator('#mobile-project-index .mobile-project-entry').filter({hasText:'WiFiScope'}).click();
    assert.match(await mobile.locator('#inspector-title').innerText(),/WiFiScope/);
    await mobile.locator('#map-filters [data-map-filter="research"]').click();
    assert.equal(await mobile.locator('.mobile-project-entry:visible').count(),4);
    await mobile.locator('#map-filters [data-map-filter="all"]').click();
    assert.equal(await mobile.locator('.mobile-project-entry:visible').count(),10);
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
    await mobile.locator('#compare-left').selectOption('wifiscope');
    await mobile.locator('#compare-right').selectOption('importproof');
    assert.equal(await mobile.locator('#compare-shared-count').innerText(),'02 / 04');
    assert.equal(await mobile.locator('body').evaluate(x=>x.scrollWidth<=innerWidth+2),true,'V7 comparison causes mobile overflow');
    await mobile.locator('#compare').screenshot({path:path.join(SHOTS,'comparison-mobile.png'),animations:'disabled'});
    // V8: 390px touch interaction, two-state verification and no overflow.
    await mobile.locator('#lab-tab-permission').click();
    await mobile.locator('#lab-strategy').selectOption('swap');
    await mobile.locator('#lab-form-permission button[type=submit]').click();
    assert.equal(await mobile.locator('#lab-verdict').getAttribute('data-status'),'fail');
    await mobile.locator('#lab-tab-retrieval').click();
    assert.equal(await mobile.locator('#lab-verdict').getAttribute('data-status'),'pass');
    await mobile.locator('#lab-scoped').uncheck();
    await mobile.locator('#lab-form-retrieval button[type=submit]').click();
    assert.equal(await mobile.locator('#lab-verdict').getAttribute('data-status'),'fail');
    assert.equal(await mobile.locator('body').evaluate(x=>x.scrollWidth<=innerWidth+2),true,'V8 lab causes body overflow');
    await mobile.locator('#lab').screenshot({path:path.join(SHOTS,'lab-mobile.png'),animations:'disabled'});
    // V9 reader on a 390px touch device: choose, navigate, use real source links.
    await mobile.locator('#journey-launch').click();
    assert.equal(await mobile.locator('.journey-choice').count(),3);
    await mobile.locator('[data-journey-choice="verify"]').click();
    assert.match(await mobile.locator('#journey-title').innerText(),/迁移完成/);
    await mobile.locator('#journey-next').click();
    assert.match(await mobile.locator('#journey-title').innerText(),/自己试着/);
    assert.equal(await mobile.locator('#journey-dialog').evaluate(x=>x.scrollWidth<=x.clientWidth+2),true,'Reader dialog overflows 390px');
    assert.ok((await mobile.locator('#journey-evidence-links a').count())>0);
    await mobile.screenshot({path:path.join(SHOTS,'guided-reader-mobile.png'),animations:'disabled'});
    await mobile.locator('#journey-close').click();
    assert.equal(await mobile.locator('body').evaluate(x=>x.scrollWidth<=innerWidth+2),true,'Reader causes body overflow');
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
