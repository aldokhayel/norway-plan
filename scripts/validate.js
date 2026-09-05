const fs=require('node:fs');const vm=require('node:vm');const assert=require('node:assert/strict');
const context={window:{}};vm.createContext(context);vm.runInContext(fs.readFileSync('trip-data.js','utf8'),context);vm.runInContext(fs.readFileSync('routes.js','utf8'),context);
const t=context.window.TRIP,r=context.window.ROUTES;
assert.equal(t.people,3);assert.equal(t.days.length,11);assert.equal(t.camps.length,10);assert.equal(new Set(t.days.filter(d=>d.camp).map(d=>d.camp)).size,10);
assert.equal(t.days[0].date,'2026-09-19');assert.equal(t.days.at(-1).date,'2026-09-29');assert.equal(t.days.at(-1).camp,null);
for(const [i,d] of t.days.entries()){
 assert.equal(d.n,i+1);assert.equal(new Date(d.date+'T12:00:00Z').getUTCDate(),19+i);
 assert.ok(d.schedule.length>0);assert.ok(d.costs.length>0);assert.ok(d.notes.length>0);
 if(i)assert.equal(d.segments[0].points[0],t.days[i-1].camp,'Overnight continuity');
 if(d.camp)assert.ok(t.camps.some(c=>c.id===d.camp));
 for(const k of d.stops)assert.ok(t.points[k],`Missing point ${k}`);
 for(const [j,s] of d.segments.entries()){
  for(const k of s.points)assert.ok(t.points[k]);
  if(['road','bus'].includes(s.mode)){assert.ok(r[`${d.n}-${j}`]?.coords?.length>1,'Missing road geometry');assert.ok(r[`${d.n}-${j}`].km>0)}
 }
 let prev=0;for(const s of d.schedule){const [a,b]=s.time.split('–').map(v=>{const [h,m]=v.split(':').map(Number);return h*60+m});assert.ok(a>=prev&&b>a,`Schedule overlap day ${d.n}`);prev=b}
}
assert.equal(t.days[9].camp,'bredang');assert.ok(t.days[10].schedule.some(s=>s.time==='10:30–12:00'));assert.equal(t.days[10].segments[0].points.at(-1),'depot');
for(const c of t.camps){assert.ok(c.image.startsWith('https://'));assert.ok(c.rating>=0&&c.rating<=5);assert.ok(c.ratingSource.startsWith('https://'));assert.ok(c.price[1]>=c.price[0]);assert.ok(c.seasonSource)}
assert.ok(t.days[5].segments.some(s=>s.mode==='train'));assert.ok(t.days[5].segments.some(s=>s.mode==='bus'));assert.ok(t.days[3].segments.some(s=>s.mode==='ferry'));
console.log('Validated: 11 dates, 10 distinct camps, overnight continuity, schedules, road geometry, ratings and source fields, noon return, passenger and vehicle transport.');
