"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const engine=require("../experience/lab-engine.js");

test("native migration keeps the original explicit grants",()=>{
 const r=engine.permission({strategy:"native",role:"app_writer"});
 assert.equal(r.pass,true);
 assert.deepEqual(r.expected,["SELECT","INSERT","UPDATE"]);
 assert.deepEqual(r.missing,[]);
 assert.equal(r.checks.length,3);
});
test("toy table replacement loses grants until explicitly restored",()=>{
 const broken=engine.permission({strategy:"swap",role:"app_writer",reapply:false});
 assert.equal(broken.pass,false);
 assert.equal(broken.missing.length,3);
 assert.equal(broken.trace.at(-1).kind,"verify");
 const repaired=engine.permission({strategy:"swap",role:"app_writer",reapply:true});
 assert.equal(repaired.pass,true);
 assert.equal(repaired.missing.length,0);
});
test("reader and writer contracts are independent",()=>{
 const reader=engine.permission({role:"app_reader",strategy:"swap"});
 assert.deepEqual(reader.expected,["SELECT"]);
 assert.equal(reader.checks.length,1);
 assert.equal(reader.pass,false);
 assert.equal(engine.permission({role:"app_reader",strategy:"native"}).pass,true);
});
test("invalid input uses bounded safe defaults without mutation",()=>{
 const first=engine.permission({strategy:"__unknown__",role:"__unknown__",reapply:false});
 assert.equal(first.strategy,"native");
 assert.equal(first.role,"app_writer");
 first.actual.pop();
 const again=engine.permission({strategy:"native",role:"app_writer"});
 assert.equal(again.actual.length,3);
});
test("tenant scope filters documents before lexical ranking",()=>{
 const scoped=engine.retrieval({tenant:"alpha",scoped:true,query:"release version roadmap"});
 assert.equal(scoped.pass,true);
 assert.equal(scoped.leaks,0);
 assert.ok(scoped.hits.some(d=>d.tenant==="alpha"));
 assert.ok(scoped.hits.every(d=>d.tenant==="alpha"||d.tenant==="public"));
 assert.equal(scoped.scanned,4);
 assert.equal(scoped.total,6);
});
test("turning off tenant isolation produces a reproducible counterexample",()=>{
 const unsafe=engine.retrieval({tenant:"alpha",scoped:false,query:"release version roadmap"});
 assert.equal(unsafe.pass,false);
 assert.ok(unsafe.leaks>=1);
 assert.equal(unsafe.hits[0].id,"B-01");
 assert.equal(unsafe.hits[0].unauthorized,true);
 assert.equal(unsafe.scanned,6);
});
test("different tenant changes the safe result",()=>{
 const r=engine.retrieval({tenant:"beta",scoped:true,query:"cost estimation quantities"});
 assert.equal(r.pass,true);
 assert.ok(r.hits.some(d=>d.id==="B-02"));
 assert.ok(r.hits.every(d=>d.tenant==="beta"||d.tenant==="public"));
});
test("unmatched or adversarial query is inert and never grants access",()=>{
 const r=engine.retrieval({tenant:"alpha",scoped:true,query:"<img src=x onerror=alert(1)> !!!"});
 assert.equal(r.pass,true);
 assert.equal(r.leaks,0);
 assert.deepEqual(r.hits,[]);
 assert.ok(r.query.length<=90);
});
test("fixtures are synthetic, immutable and side-effect-free",()=>{
 assert.ok(Object.isFrozen(engine.fixtures));
 assert.ok(engine.fixtures.every(d=>["alpha","beta","public"].includes(d.tenant)));
 assert.equal(engine.fixtures.length,6);
 assert.equal(typeof engine.permission,"function");
 assert.equal(typeof engine.retrieval,"function");
});
