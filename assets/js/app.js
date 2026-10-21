/* GROKstudy whole-Bible v5 — shared UI: 5 themes, IO-only scroll-spy, lazy book bodies, paused off-screen loops */
(function(){
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const root=document.documentElement,body=document.body,LS={g:k=>{try{return localStorage.getItem(k)}catch(e){return null}},s:(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}}};
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches, MOB=()=>innerWidth<=1000;
/* ---------- themes & reading modes ---------- */
const THEMES=['night','dawn','jade','ruby','contrast'],LIGHT={dawn:1,jade:1},TC={night:'#060a1c',dawn:'#f6f3ec',jade:'#edf8f2',ruby:'#16060f',contrast:'#0b0a08'};
const tp=$('#tpanel'),tpb=$('#tpBtn');
function markTheme(){const t=root.dataset.theme||'night';$$('.tsw button').forEach(b=>b.classList.toggle('on',b.dataset.theme===t));const m=$('meta[name=theme-color]');m&&m.setAttribute('content',TC[t]||TC.night)}
function setTheme(t){if(!THEMES.includes(t))t='night';const ap=()=>{root.dataset.theme=t;root.classList.toggle('light',!!LIGHT[t]);markTheme()};LS.s('wb-theme',t);
  if(document.startViewTransition&&!RM)document.startViewTransition(ap);else ap()}
markTheme();
$$('.tsw button').forEach(b=>b.addEventListener('click',()=>setTheme(b.dataset.theme)));
tpb&&tpb.addEventListener('click',e=>{e.stopPropagation();tp.hidden=!tp.hidden;tpb.setAttribute('aria-expanded',String(!tp.hidden))});
document.addEventListener('click',e=>{if(tp&&!tp.hidden&&!e.target.closest('#tpanel,#tpBtn')){tp.hidden=true;tpb.setAttribute('aria-expanded','false')}});
function mode(cls,key,on){root.classList.toggle(cls,on);LS.s(key,on?'1':'0');syncModes()}
function syncModes(){const pl=root.classList.contains('plain'),fo=root.classList.contains('focus');$('#plainChk')&&($('#plainChk').checked=!pl);$('#focusChk')&&($('#focusChk').checked=fo);$('#plainBtn')&&$('#plainBtn').classList.toggle('on',!pl);$('#focusBtn')&&$('#focusBtn').classList.toggle('on',fo)}
syncModes();
$('#plainBtn')&&$('#plainBtn').addEventListener('click',()=>mode('plain','wb-plain',!root.classList.contains('plain')));
$('#focusBtn')&&$('#focusBtn').addEventListener('click',()=>mode('focus','wb-focus',!root.classList.contains('focus')));
$('#plainChk')&&$('#plainChk').addEventListener('change',e=>mode('plain','wb-plain',!e.target.checked));
$('#focusChk')&&$('#focusChk').addEventListener('change',e=>mode('focus','wb-focus',e.target.checked));
window.__setTheme=setTheme;
/* ---------- Lenis (opt-in, loaded on demand) ---------- */
let lenis=null;
function lenisOn(){if(lenis||RM)return;const go=()=>{lenis=new Lenis({lerp:.11,wheelMultiplier:1,smoothWheel:true,anchors:{offset:-(parseInt(getComputedStyle(root).getPropertyValue('--top'))||56)-10},prevent:n=>n.closest&&n.closest('.tocbody,.leaflet-container,.tpanel')});
  const raf=t=>{lenis&&(lenis.raf(t),requestAnimationFrame(raf))};requestAnimationFrame(raf);root.classList.add('wb-smooth')};
  if(window.Lenis)go();else{const s=document.createElement('script');s.src='assets/vendor/lenis.min.js';s.onload=go;document.head.appendChild(s)}}
function lenisOff(){if(lenis){lenis.destroy();lenis=null;root.classList.remove('wb-smooth')}}
const lc=$('#lenisChk');if(LS.g('wb-lenis')==='1'&&matchMedia('(pointer:fine)').matches&&!RM)lenisOn();
lc&&(lc.checked=LS.g('wb-lenis')==='1',lc.addEventListener('change',()=>{if(lc.checked){lenisOn();LS.s('wb-lenis','1')}else{lenisOff();LS.s('wb-lenis','0')}}));
/* ---------- lazy book bodies (template hydration) ---------- */
const lazyQ=[];let lazyT=0;const onHyd=[];
function hydrate(body){if(!body||!body.hasAttribute('data-lazy'))return;const t=body.querySelector(':scope>template');body.removeAttribute('data-lazy');if(t)body.replaceChildren(t.content);onHyd.forEach(f=>f(body))}
function pump(){lazyT=0;const t0=performance.now();while(lazyQ.length&&performance.now()-t0<8){hydrate(lazyQ.shift())}if(lazyQ.length)lazyT=requestAnimationFrame(pump)}
const lazies=$$('.bk>.body[data-lazy]');
if(lazies.length){if('IntersectionObserver' in window){const lo=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){lo.unobserve(en.target);const b=en.target.querySelector(':scope>.body[data-lazy]');if(b){lazyQ.push(b);if(!lazyT)lazyT=requestAnimationFrame(pump)}}}),{rootMargin:'1800px 0px 1800px 0px'});lazies.forEach(b=>lo.observe(b.parentElement))}else lazies.forEach(hydrate)}
function findLazy(id){for(const b of $$('.bk>.body[data-lazy]')){const t=b.querySelector(':scope>template');if(t&&t.content.getElementById(id))return b}return null}
window.__hydrateAll=()=>$$('.bk>.body[data-lazy]').forEach(hydrate);
function goTo(id){let el=document.getElementById(id);if(!el){const lb=findLazy(id);if(lb){hydrate(lb);el=document.getElementById(id)}}if(!el)return;let dd=el.closest('details');while(dd){dd.open=true;dd=dd.parentElement.closest('details')}
  const off=()=>(parseInt(getComputedStyle(root).getPropertyValue('--top'))||56)+10+(el.closest('.bk')&&$('.filters')&&innerWidth>1000?58:0);
  const far=Math.abs(el.getBoundingClientRect().top)>innerHeight*2.5;
  const tgt=()=>Math.max(0,scrollY+el.getBoundingClientRect().top-off());const jump=y=>lenis?lenis.scrollTo(y,{immediate:true,force:true}):scrollTo({top:y,behavior:'instant'});
  if(far)jump(tgt());else if(lenis)lenis.scrollTo(tgt(),{duration:.9});else el.scrollIntoView({behavior:RM?'auto':'smooth',block:'start'});
  history.replaceState(null,'','#'+id);
  let n=0,ly=-1,stop=false;const cancel=()=>{stop=true};['wheel','touchstart','keydown','pointerdown'].forEach(ev=>addEventListener(ev,cancel,{once:true,passive:true}));const fix=()=>{if(stop)return;n++;const y=scrollY,d=el.getBoundingClientRect().top-off();if(y===ly&&Math.abs(d)>8)jump(tgt());ly=y;if(n<14)setTimeout(fix,200)};setTimeout(fix,far?60:400)}
if(location.hash.length>1)addEventListener('load',()=>setTimeout(()=>goTo(decodeURIComponent(location.hash.slice(1))),60));
/* ---------- TOC tree ---------- */
const toc=$('#toc'),tree=$('#toc .tree'),tb=$('.tocbody');
if(tree){
  tree.addEventListener('click',e=>{const t=e.target.closest('.tg');if(t){t.closest('li').classList.toggle('closed');return}
    const a=e.target.closest('a');if(a){e.preventDefault();if(MOB())body.classList.remove('tocopen');requestAnimationFrame(()=>goTo(a.getAttribute('href').slice(1)))}});
  $('#tocAll')&&$('#tocAll').addEventListener('click',()=>$$('li',tree).forEach(l=>l.classList.remove('closed')));
  $('#tocNone')&&$('#tocNone').addEventListener('click',()=>$$('li',tree).forEach(l=>{if(l.querySelector('ul'))l.classList.add('closed')}));
  $('#tocL2')&&$('#tocL2').addEventListener('click',()=>$$('li',tree).forEach(l=>{if(l.querySelector('ul'))l.classList.toggle('closed',!l.classList.contains('l1'))}));
  const q=$('#tocq');q&&q.addEventListener('input',()=>{const v=q.value.trim().toLowerCase();
    $$('li',tree).forEach(li=>{li.classList.remove('hidden')});if(!v)return;
    $$('li',tree).forEach(li=>{const own=li.querySelector(':scope>.row>a').textContent.toLowerCase().includes(v);const sub=[...li.querySelectorAll('a')].some(a=>a.textContent.toLowerCase().includes(v));li.classList.toggle('hidden',!sub);if(sub&&!own)li.classList.remove('closed');if(own)li.classList.remove('closed')})});
}
$('#tocBtn')&&$('#tocBtn').addEventListener('click',()=>{if(MOB())body.classList.toggle('tocopen');else{body.classList.toggle('tochide');LS.s('wb-toc',body.classList.contains('tochide')?'0':'1')}});
$('#tocClose')&&$('#tocClose').addEventListener('click',()=>{if(MOB())body.classList.remove('tocopen');else{body.classList.add('tochide');LS.s('wb-toc','0')}});
if(LS.g('wb-toc')==='0'&&!MOB())body.classList.add('tochide');
$('.scrim')&&$('.scrim').addEventListener('click',()=>body.classList.remove('tocopen'));
document.addEventListener('keydown',e=>{if(e.key==='Escape')body.classList.remove('tocopen')});
/* resizable TOC */
const W0=parseInt(LS.g('wb-tocw'));if(W0)root.style.setProperty('--toc',W0+'px');
const rz=$('.rz');
if(rz){let sx=0,sw=0,raf=0,nw=0,ty=0;const tip=$('.rztip',rz),hint=$('.rzhint');
  const show=()=>{tip.textContent=Math.round(nw||toc.getBoundingClientRect().width)+' px';tip.style.transform='translateY('+(ty-toc.getBoundingClientRect().top-14)+'px)'};
  const mv=e=>{nw=Math.max(220,Math.min(MOB()?innerWidth*.96:Math.min(680,innerWidth*.6),sw+e.clientX-sx));ty=e.clientY;if(!raf)raf=requestAnimationFrame(()=>{root.style.setProperty('--toc',nw+'px');show();raf=0})};
  const up=()=>{body.classList.remove('rzing');removeEventListener('pointermove',mv);removeEventListener('pointerup',up);if(nw)LS.s('wb-tocw',Math.round(nw))};
  const hideHint=()=>{if(hint&&!hint.hidden){hint.classList.add('out');setTimeout(()=>hint.hidden=true,400);LS.s('wb-rzhint','1')}};
  rz.addEventListener('pointerdown',e=>{e.preventDefault();hideHint();sx=e.clientX;sw=toc.getBoundingClientRect().width;nw=sw;ty=e.clientY;show();body.classList.add('rzing');addEventListener('pointermove',mv,{passive:true});addEventListener('pointerup',up)});
  rz.addEventListener('pointermove',e=>{if(!body.classList.contains('rzing')){ty=e.clientY;nw=0;show()}},{passive:true});
  if(hint&&!LS.g('wb-rzhint')&&!MOB()&&!body.classList.contains('tochide')){setTimeout(()=>{hint.hidden=false},900);setTimeout(hideHint,8000)}
  rz.addEventListener('dblclick',()=>{root.style.removeProperty('--toc');LS.s('wb-tocw','')});
}
/* ---------- progress (CSS scroll-timeline when supported) / totop ---------- */
const prog=$('.prog'),tt=$('.totop'),CSSPROG=window.CSS&&CSS.supports&&CSS.supports('animation-timeline:scroll()');let maxY=1,tick=false,lastOn=null,mT=0;
const measure=()=>{maxY=Math.max(1,root.scrollHeight-innerHeight)};
const measureSoon=()=>{if(!mT)mT=setTimeout(()=>{mT=0;measure()},200)};measure();
addEventListener('resize',measureSoon,{passive:true});if(!CSSPROG&&'ResizeObserver' in window)new ResizeObserver(measureSoon).observe(body);
function onS(){tick=false;const y=scrollY;if(prog&&!CSSPROG)prog.style.transform='scaleX('+Math.min(1,y/maxY)+')';const on=y>600;if(on!==lastOn){tt&&tt.classList.toggle('on',on);lastOn=on}}
addEventListener('scroll',()=>{if(!tick){tick=true;requestAnimationFrame(onS)}},{passive:true});onS();
tt&&tt.addEventListener('click',()=>lenis?lenis.scrollTo(0):scrollTo({top:0,behavior:'smooth'}));
/* ---------- scroll-spy: IntersectionObserver only (no layout reads while scrolling) ----------
   Band = everything above 28% of the viewport. A heading is "passed" when it is in the band.
   Headings inside skipped content (content-visibility / lazy template) fall back to their container being fully passed. */
if(tree&&'IntersectionObserver' in window){
  const links=$$('a',tree),n=links.length,ids=links.map(a=>a.getAttribute('href').slice(1));
  const hAbove=new Uint8Array(n),cGone=new Map();let cur=null,raf=0;const idx=new Map(),cont=new Array(n);
  const TOPM=-(parseInt(getComputedStyle(root).getPropertyValue('--top'))||56);
  const hio=new IntersectionObserver(es=>{es.forEach(e=>{const i=idx.get(e.target);if(i!==undefined)hAbove[i]=e.isIntersecting?1:0});sched()},{rootMargin:'100000px 0px -72% 0px'});
  // container fully above the band  <=>  container NOT intersecting the region below the 28% line, and its top is above it
  const cio2=new IntersectionObserver(es=>{es.forEach(e=>{const g=!e.isIntersecting&&e.boundingClientRect.top<(e.rootBounds?e.rootBounds.top:0);cGone.set(e.target,g)});sched()},{rootMargin:'-28% 0px 100000px 0px'});
  function bind(i){const el=document.getElementById(ids[i]);const c=el?el.closest('section.blk,.bk'):null;
    if(el){idx.set(el,i);hio.observe(el)}
    let pc=c;if(!el){const lb=findLazy(ids[i]);pc=lb?lb.closest('.bk'):null}
    cont[i]=pc;if(pc&&!cGone.has(pc)){cGone.set(pc,false);cio2.observe(pc)}}
  for(let i=0;i<n;i++)bind(i);
  onHyd.push(body=>{const card=body.closest('.bk');for(let i=0;i<n;i++){if(cont[i]!==card)continue;const el=document.getElementById(ids[i]);if(el&&!idx.has(el))bind(i)}sched()});
  function sched(){if(!raf)raf=requestAnimationFrame(spy)}
  function spy(){raf=0;let ans=0;for(let i=n-1;i>=0;i--){if(hAbove[i]||(cont[i]&&cGone.get(cont[i]))){ans=i;break}}
    const a=links[ans];if(!a||a===cur)return;cur&&cur.classList.remove('act');$$('a.anc',tree).forEach(x=>x.classList.remove('anc'));cur=a;a.classList.add('act');
    let li=a.closest('li').parentElement.closest('li');while(li){li.classList.remove('closed');li.querySelector(':scope>.row>a').classList.add('anc');li=li.parentElement.closest('li')}
    if(tb&&(!MOB()||body.classList.contains('tocopen'))){const r=a.getBoundingClientRect(),br=tb.getBoundingClientRect();if(r.top<br.top+30||r.bottom>br.bottom-30)tb.scrollTo({top:tb.scrollTop+r.top-br.top-br.height/3})}}
}
/* ---------- reveal + structure bars + charts ---------- */
const ro='IntersectionObserver' in window&&!RM?new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.add('in','go');ro.unobserve(en.target)}}),{rootMargin:'0px 0px -5% 0px'}):null;
const REV='.rv,.sbar,.vchart,.hbar';
function reveal(r){$$(REV,r).forEach(el=>ro?ro.observe(el):el.classList.add('in','go'))}
reveal(document);onHyd.push(reveal);
/* ---------- pause infinite animations when off-screen ---------- */
if('IntersectionObserver' in window){const lo2=new IntersectionObserver(es=>es.forEach(e=>e.target.classList.toggle('run',e.isIntersecting)),{rootMargin:'100px 0px'});$$('.covflow,.floaty,.loop').forEach(el=>lo2.observe(el))}
/* ---------- instant navigation: prefetch on hover / touch (fallback when Speculation Rules are unsupported) ---------- */
if(!(HTMLScriptElement.supports&&HTMLScriptElement.supports('speculationrules'))){const done=new Set();const pf=e=>{const a=e.target.closest&&e.target.closest('a[href$=".html"],a[href*=".html#"]');if(!a)return;const u=a.href.split('#')[0];if(done.has(u)||u===location.href.split('#')[0])return;done.add(u);const l=document.createElement('link');l.rel='prefetch';l.href=u;document.head.appendChild(l)};
  document.addEventListener('pointerover',pf,{passive:true});document.addEventListener('touchstart',pf,{passive:true})}
/* ---------- print a block ---------- */
$$('[data-print]').forEach(b=>b.addEventListener('click',()=>{body.classList.add('pk');addEventListener('afterprint',()=>body.classList.remove('pk'),{once:true});print();setTimeout(()=>body.classList.remove('pk'),1500)}));
/* ---------- era band ---------- */
const eb=$('.eraband');if(eb&&'IntersectionObserver' in window){const sp=$$('span',eb);const eo=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){const i=+en.target.dataset.era;sp.forEach((x,j)=>x.classList.toggle('on',j===i))}}),{rootMargin:'-30% 0px -60% 0px'});$$('[data-era]').forEach(e=>{if(e.dataset.era!=='')eo.observe(e)})}
/* ---------- lazy Mermaid ---------- */
let merP=null;const merQ=[];
function loadMer(){if(merP)return merP;merP=new Promise((res,rej)=>{const s=document.createElement('script');s.src=body.dataset.mer||'assets/vendor/mermaid.min.js';s.onload=()=>{initMer();res()};s.onerror=rej;document.head.appendChild(s)});return merP}
function initMer(){const light=root.classList.contains('light');mermaid.initialize({startOnLoad:false,securityLevel:'loose',theme:light?'default':'dark',fontFamily:'"Noto Sans CJK SC","PingFang SC","Microsoft YaHei",sans-serif',flowchart:{htmlLabels:true,curve:'basis',useMaxWidth:true},mindmap:{useMaxWidth:true},themeVariables:light?{}:{primaryColor:'#26306a',primaryTextColor:'#eef',lineColor:'#ffcb5c',secondaryColor:'#3a2350',tertiaryColor:'#13324a'}})}
function renderMer(p){if(!p.dataset.src)p.dataset.src=p.textContent;loadMer().then(()=>mermaid.run({nodes:[p]})).catch(e=>{p.style.color='inherit';p.style.whiteSpace='pre-wrap';console.warn('mermaid',e)})}
function rerenderMer(){if(!window.mermaid)return;initMer();$$('pre.mermaid[data-processed]').forEach(p=>{p.removeAttribute('data-processed');p.innerHTML='';p.textContent=p.dataset.src;mermaid.run({nodes:[p]})})}
const mers=$$('pre.mermaid');
if(mers.length){if('IntersectionObserver' in window){const mo=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){mo.unobserve(en.target);renderMer(en.target)}}),{rootMargin:'700px 0px'});mers.forEach(p=>mo.observe(p))}else mers.forEach(renderMer)}
window.__merAll=()=>Promise.all(mers.map(p=>{renderMer(p);return loadMer()}));
/* ---------- filters ---------- */
const txt=it=>{if(!it.__t){const t=it.querySelector('template');it.__t=(it.textContent+(t?t.content.textContent:'')).toLowerCase()}return it.__t};
$$('.filters').forEach(f=>{const items=$$(f.dataset.target);const q=$('input',f);let cat='all';
  function apply(){const v=(q&&q.value||'').trim().toLowerCase();items.forEach(it=>{const okc=cat==='all'||it.dataset.cat===cat;const okq=!v||txt(it).includes(v);it.classList.toggle('hidden',!(okc&&okq))});measure()}
  $$('button[data-cat]',f).forEach(b=>b.addEventListener('click',()=>{$$('button[data-cat]',f).forEach(x=>x.classList.remove('on'));b.classList.add('on');cat=b.dataset.cat;apply()}));
  let tq;q&&q.addEventListener('input',()=>{clearTimeout(tq);tq=setTimeout(apply,160)});});
$$('[data-expand]').forEach(b=>b.addEventListener('click',()=>{const open=b.dataset.state!=='open';if(open&&/\.bk/.test(b.dataset.expand))window.__hydrateAll();$$(b.dataset.expand).forEach(d=>d.open=open);b.dataset.state=open?'open':'closed';b.textContent=open?'全部收起':'全部展开';measure()}));
/* ---------- creed tools ---------- */
$$('.ctool').forEach(t=>{const c=$(t.dataset.for);if(!c)return;
  $$('button',t).forEach(b=>b.addEventListener('click',()=>{const a=b.dataset.act;
    if(a==='hide'){c.classList.toggle('hidemode');$$('.ln',c).forEach(l=>l.classList.remove('show'));b.classList.toggle('on')}
    if(a==='show')$$('.ln',c).forEach(l=>l.classList.add('show'));
    if(a==='next'){const n=$$('.ln:not(.show)',c)[0];n&&n.classList.add('show')}
    if(a==='big'||a==='small'){const s=parseFloat(getComputedStyle(c).fontSize);c.style.fontSize=Math.max(14,Math.min(32,s+(a==='big'?2:-2)))+'px'}
    if(a==='copy'&&navigator.clipboard)navigator.clipboard.writeText(c.innerText).then(()=>{b.textContent='已复制 ✓';setTimeout(()=>b.textContent='复制全文',1500)}).catch(()=>{})}));
  c.addEventListener('click',e=>{const l=e.target.closest('.ln');if(l&&c.classList.contains('hidemode'))l.classList.toggle('show')})});
/* ---------- flashcards / quiz / order ---------- */
document.addEventListener('click',e=>{const f=e.target.closest('.fc');if(f)f.classList.toggle('flip')});
$$('[data-shuffle]').forEach(b=>b.addEventListener('click',()=>{const g=$(b.dataset.shuffle);[...g.children].sort(()=>Math.random()-.5).forEach(c=>{c.classList.remove('flip');g.appendChild(c)})}));
$$('.quiz').forEach(qz=>{let sc=0,done=0;const tot=$$('.q',qz).length,out=$('.score',qz);
  $$('.q',qz).forEach(q=>{const ans=q.dataset.a;$$('.opts button',q).forEach(b=>b.addEventListener('click',()=>{if(q.dataset.done)return;q.dataset.done=1;done++;
    if(b.dataset.k===ans){b.classList.add('ok');sc++}else{b.classList.add('no');$$('.opts button',q).find(x=>x.dataset.k===ans).classList.add('ok')}
    const ex=$('.ex',q);ex&&ex.classList.remove('hidden');out&&(out.textContent=`得分 ${sc} / ${tot}（已答 ${done}）`)}))});
  const rs=$('[data-reset]',qz);rs&&rs.addEventListener('click',()=>{sc=0;done=0;$$('.q',qz).forEach(q=>{delete q.dataset.done;$$('.opts button',q).forEach(b=>b.classList.remove('ok','no'));const ex=$('.ex',q);ex&&ex.classList.add('hidden')});out&&(out.textContent='得分 0 / '+tot)})});
$$('.ordgame').forEach(g=>{const seq=JSON.parse(g.dataset.seq),pool=$('.ord',g),ans=$('.ans',g),msg=$('.msg',g);let i=0;
  function init(){i=0;ans.textContent='';msg.textContent='';pool.innerHTML='';[...seq].sort(()=>Math.random()-.5).forEach(s=>{const b=document.createElement('button');b.textContent=s;b.onclick=()=>{if(s===seq[i]){b.classList.add('done');ans.textContent+=(i?' → ':'')+s;i++;if(i===seq.length)msg.textContent='🎉 全部正确！'}else{msg.textContent='✗ 下一个应是第 '+(i+1)+' 个';b.animate([{transform:'translateX(-4px)'},{transform:'translateX(4px)'},{transform:'none'}],{duration:220})}};pool.appendChild(b)})}
  init();$('[data-restart]',g)&&$('[data-restart]',g).addEventListener('click',init)});
/* ---------- kings interactive timeline ---------- */
$$('.kt').forEach(k=>{const info=$(k.dataset.info);
  k.addEventListener('click',e=>{const b=e.target.closest('.kb');if(!b)return;$$('.kb.sel',k).forEach(x=>x.classList.remove('sel'));b.classList.add('sel');
    info&&(info.innerHTML=b.dataset.html)});
  k.addEventListener('mouseover',e=>{const b=e.target.closest('.kb');if(b&&info&&!$('.kb.sel',k))info.innerHTML=b.dataset.html},{passive:true})});
$$('[data-kfilter]').forEach(btn=>btn.addEventListener('click',()=>{const k=$(btn.dataset.kt),v=btn.dataset.kfilter;$$('[data-kt="'+btn.dataset.kt+'"]').forEach(x=>x.classList.remove('on'));btn.classList.add('on');
  $$('.kb',k).forEach(b=>b.classList.toggle('dim',v!=='all'&&!b.classList.contains(v)))}));
/* ---------- covenant flow ---------- */
$$('.covflow').forEach(cf=>{const info=$(cf.dataset.info);cf.addEventListener('click',e=>{const n=e.target.closest('.nd');if(n&&info){info.innerHTML=n.dataset.html;$$('.nd',cf).forEach(x=>x.style.opacity=x===n?1:.55)}})});
})();
