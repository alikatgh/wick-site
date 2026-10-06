const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const script = fs.readFileSync(require('node:path').join(__dirname,'../theme.js'),'utf8');
function page(saved, dark, blocked=false) {
  const handlers = {}, controls=[{value:''}], root={dataset:{},style:{}}, body={dataset:{}};
  const media={matches:dark,addEventListener:(event,fn)=>handlers.os=fn};
  const context={document:{documentElement:root,body,querySelectorAll:()=>controls,addEventListener:(event,fn)=>handlers[event]=fn},window:{matchMedia:()=>media,addEventListener:(event,fn)=>handlers[event]=fn},localStorage:{getItem:()=>{if(blocked)throw Error();return saved;},setItem:(_,value)=>{if(blocked)throw Error();saved=value;}}};
  vm.runInNewContext(script,context);
  return {root,body,media,handlers,controls,select(value){handlers.change({target:{matches:()=>true,value}});}};
}
for(const dark of [false,true]){
  const p=page(null,dark);assert.equal(p.root.dataset.theme,dark?'dark':'light');
  p.media.matches=!dark;p.handlers.os();assert.equal(p.root.dataset.theme,dark?'light':'dark');
  p.select('light');p.media.matches=true;p.handlers.os();assert.equal(p.root.dataset.theme,'light');
  assert.equal(p.root.style.colorScheme,'light');assert.equal(p.body.dataset.mdColorScheme,'default');
  p.handlers.storage({key:'wick-theme',newValue:'dark'});assert.equal(p.root.dataset.theme,'dark');
  p.handlers.storage({key:null,newValue:null});assert.equal(p.controls[0].value,'system');
}
assert.equal(page('garbage',false).root.dataset.theme,'light');
assert.equal(page('light',true).root.dataset.theme,'light');
const blocked=page(null,true,true);blocked.select('light');assert.equal(blocked.root.dataset.theme,'light');
console.log('Theme checks passed: OS changes, overrides, storage sync, invalid and blocked storage.');
