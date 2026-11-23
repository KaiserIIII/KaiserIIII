"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const engine=require("../experience/search-engine.js");
const src=fs.readFileSync(require("node:path").resolve(__dirname,"../experience/data.js"),"utf8");
const ctx={window:{}};vm.runInNewContext(src,ctx);
const projects=ctx.window.KAISER_DATA.projects;
const query=(text,language="en")=>engine.inspect(text,projects,language,6);
test("search is grounded in exactly ten public project records",()=>{
  assert.equal(projects.length,10);
  assert.ok(query("").results.length>0);
  assert.ok(query("").results.every(x=>projects.includes(x.project)));
});
test("direct project names stay on top",()=>{
  assert.equal(query("WiFiScope").results[0].project.id,"wifiscope");
  assert.equal(query("MigrationWitness").results[0].project.id,"migrationwitness");
});
test("bilingual natural questions rank relevant public work",()=>{
  assert.equal(query("你做过哪些数据库可靠性研究？","zh").results[0].project.id,"migrationwitness");
  assert.equal(query("有没有真正发布过的产品？","zh").results[0].project.id,"cardcraft");
  assert.equal(query("knowledge retrieval and tenant isolation").results[0].project.id,"zhixu");
  assert.equal(query("工程造价计算","zh").results[0].project.id,"cost");
});
test("the result carries original evidence and known limitations",()=>{
  const results=query("PostgreSQL migration");
  assert.ok(results.results.length>=1);
  const m=results.results.find(r=>r.project.id==="migrationwitness");
  assert.ok(m);
  assert.match(m.evidence,/PostgreSQL/);
  assert.match(m.limitation,/specific|migration/i);
  assert.ok(m.reasons.length>=1);
  assert.ok(m.project.links.some(l=>l.url.includes("github.com/KaiserIIII/")));
});
test("unrelated query reports nothing instead of hallucinating",()=>{
  const q=query("unobtanium dancing telescope zyxwvu");
  assert.equal(q.results.length,0);
  assert.equal(q.mode,"lexical");
});
test("Chinese and English variants share ids, not fabricated projects",()=>{
  const a=query("network privacy").results.map(r=>r.project.id);
  const b=query("网络隐私","zh").results.map(r=>r.project.id);
  assert.ok(a.includes("wifiscope")&&b.includes("wifiscope"));
  assert.ok(engine.conceptDefinitions.length>=6);
});
test("search bounds untrusted text, tokens and returned results",()=>{
  const q=query("x".repeat(400)+" database", "en");
  assert.ok(q.query.length<=180);
  assert.ok(q.results.length<=6);
  assert.ok(q.tokens.length<=20);
});
test("relevance is only query matching, never a personal quality score",()=>{
  const q=query("database");
  assert.ok(q.results.every(r=>r.project&&typeof r.score==="number"&&r.score>=0));
  assert.ok(q.results.every(r=>!("skill" in r)&&!("competence" in r)));
});
test("the engine does not mutate original source records",()=>{
  const original=projects[0].en.proof;
  query("Steam game");
  query("测试 实验","zh");
  assert.equal(projects[0].en.proof,original);
});
