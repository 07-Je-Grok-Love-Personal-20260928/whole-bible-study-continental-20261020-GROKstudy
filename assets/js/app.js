/* GROKstudy whole-Bible v1 — shared UI */
(function(){
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const root=document.documentElement,body=document.body;
// theme
try{if(localStorage.getItem('wb-theme')==='light')root.classList.add('light')}catch(e){}
$('#themeBtn')&&$('#themeBtn').addEventListener('click',()=>{root.classList.toggle('light');try{localStorage.setItem('wb-theme',root.classList.contains('light')?'light':'dark')}catch(e){}; if(window.__remer)window.__remer();});
// TOC build
const toc=$('#toc ol'),heads=$$('main h2.h[id], main h3.h[id], main .bk[id] h3');
if(toc){
  let lastL2=null;
  heads.forEach(h=>{
    const id=h.id||h.closest('[id]').id; const li=document.createElement('li');
    const isL3=h.tagName==='H3'; li.className=isL3?'l3':'l2';
    const a=document.createElement('a'); a.href='#'+id; a.textContent=(h.dataset.toc||h.textContent).replace(/\s+/g,' ').trim(); a.dataset.id=id;
    li.appendChild(a); toc.appendChild(li); if(!isL3)lastL2=li;
  });
  $('#tocq')&&$('#tocq').addEventListener('input',e=>{const v=e.target.value.trim().toLowerCase();$$('li',toc).forEach(li=>{li.classList.toggle('hidden',v&&!li.textContent.toLowerCase().includes(v))})});
  toc.addEventListener('click',e=>{if(e.target.tagName==='A'&&innerWidth<=1000)body.classList.remove('tocopen')});
}
const tb=$('#tocBtn');
tb&&tb.addEventListener('click',()=>{if(innerWidth<=1000)body.classList.toggle('tocopen');else{body.classList.toggle('tochide');try{localStorage.setItem('wb-toc',body.classList.contains('tochide')?'0':'1')}catch(e){}}});
try{if(localStorage.getItem('wb-toc')==='0'&&innerWidth>1000)body.classList.add('tochide')}catch(e){}
$('.scrim')&&$('.scrim').addEventListener('click',()=>body.classList.remove('tocopen'));
document.addEventListener('keydown',e=>{if(e.key==='Escape')body.classList.remove('tocopen')});
// progress + totop + spy
const prog=$('.prog'),tt=$('.totop');const links=toc?$$('a',toc):[];
let ticking=false;
function onScroll(){const h=root.scrollHeight-innerHeight;prog&&(prog.style.width=(h>0?scrollY/h*100:0)+'%');tt&&tt.classList.toggle('on',scrollY>600);ticking=false;}
addEventListener('scroll',()=>{if(!ticking){requestAnimationFrame(onScroll);ticking=true}},{passive:true});
tt&&tt.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));
if('IntersectionObserver' in window){
  const map=new Map(links.map(a=>[a.dataset.id,a]));
  const so=new IntersectionObserver(es=>{es.forEach(en=>{if(en.isIntersecting){const a=map.get(en.target.id||en.target.closest('[id]').id);if(a){links.forEach(l=>l.classList.remove('act'));a.classList.add('act');if(toc&&!body.classList.contains('tocopen')){const r=a.getBoundingClientRect(),tr=$('#toc').getBoundingClientRect();if(r.top<tr.top+40||r.bottom>tr.bottom-20)a.scrollIntoView({block:'nearest'})}}}})},{rootMargin:'-15% 0px -75% 0px'});
  heads.forEach(h=>so.observe(h.id?h:h.closest('[id]')));
  const ro=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.add('in');ro.unobserve(en.target)}}),{rootMargin:'0px 0px -6% 0px'});
  $$('.reveal').forEach(el=>ro.observe(el));
}else $$('.reveal').forEach(el=>el.classList.add('in'));
// mermaid
function mer(){
  if(!window.mermaid){$$('pre.mermaid').forEach(p=>{p.style.color='inherit';p.style.textAlign='left';p.style.whiteSpace='pre-wrap'});return}
  const light=root.classList.contains('light');
  try{
    mermaid.initialize({startOnLoad:false,securityLevel:'loose',theme:light?'default':'dark',fontFamily:'"Noto Sans CJK SC","PingFang SC","Microsoft YaHei",sans-serif',flowchart:{htmlLabels:true,curve:'basis',useMaxWidth:true},mindmap:{useMaxWidth:true},themeVariables:light?{}:{primaryColor:'#26306a',primaryTextColor:'#eef',lineColor:'#f5c76b',secondaryColor:'#3a2350',tertiaryColor:'#13324a'}});
    $$('pre.mermaid').forEach(p=>{if(!p.dataset.src)p.dataset.src=p.textContent;});
    mermaid.run({querySelector:'pre.mermaid'}).catch(err=>{console.warn('mermaid',err);});
  }catch(e){console.warn(e)}
}
window.__remer=function(){$$('pre.mermaid').forEach(p=>{if(p.dataset.src){p.removeAttribute('data-processed');p.innerHTML='';p.textContent=p.dataset.src}});mer()};
if(document.readyState==='complete')mer();else addEventListener('load',mer);
// filters (books)
$$('.filters').forEach(f=>{
  const items=$$(f.dataset.target);const q=$('input',f);let cat='all';
  function apply(){const v=(q&&q.value||'').trim().toLowerCase();items.forEach(it=>{const okc=cat==='all'||it.dataset.cat===cat;const okq=!v||it.textContent.toLowerCase().includes(v);it.classList.toggle('hidden',!(okc&&okq))})}
  $$('button[data-cat]',f).forEach(b=>b.addEventListener('click',()=>{$$('button[data-cat]',f).forEach(x=>x.classList.remove('on'));b.classList.add('on');cat=b.dataset.cat;apply()}));
  q&&q.addEventListener('input',apply);
});
// expand/collapse all
$$('[data-expand]').forEach(b=>b.addEventListener('click',()=>{const open=b.dataset.state!=='open';$$(b.dataset.expand).forEach(d=>d.open=open);b.dataset.state=open?'open':'closed';b.textContent=open?'全部收起':'全部展开'}));
// creed recite tools
$$('.ctool').forEach(t=>{const c=$(t.dataset.for);if(!c)return;
  $$('button',t).forEach(b=>b.addEventListener('click',()=>{
    const a=b.dataset.act;
    if(a==='hide'){c.classList.toggle('hidemode');$$('.ln',c).forEach(l=>l.classList.remove('show'));b.classList.toggle('on')}
    if(a==='show'){$$('.ln',c).forEach(l=>l.classList.add('show'))}
    if(a==='big'){const s=parseFloat(getComputedStyle(c).fontSize);c.style.fontSize=Math.min(s+2,32)+'px'}
    if(a==='small'){const s=parseFloat(getComputedStyle(c).fontSize);c.style.fontSize=Math.max(s-2,14)+'px'}
    if(a==='copy'){navigator.clipboard&&navigator.clipboard.writeText(c.innerText).then(()=>{b.textContent='已复制 ✓';setTimeout(()=>b.textContent='复制全文',1500)}).catch(()=>{})}
  }));
  c.addEventListener('click',e=>{const l=e.target.closest('.ln');if(l&&c.classList.contains('hidemode'))l.classList.toggle('show')});
});
// flashcards
$$('.fc').forEach(f=>f.addEventListener('click',()=>f.classList.toggle('flip')));
$$('[data-shuffle]').forEach(b=>b.addEventListener('click',()=>{const g=$(b.dataset.shuffle);[...g.children].sort(()=>Math.random()-.5).forEach(c=>{c.classList.remove('flip');g.appendChild(c)})}));
// quiz
$$('.quiz').forEach(qz=>{let sc=0,done=0;const tot=$$('.q',qz).length;const out=$('.score',qz);
  $$('.q',qz).forEach(q=>{const ans=q.dataset.a;$$('.opts button',q).forEach(b=>b.addEventListener('click',()=>{if(q.dataset.done)return;q.dataset.done=1;done++;
    if(b.dataset.k===ans){b.classList.add('ok');sc++}else{b.classList.add('no');$$('.opts button',q).find(x=>x.dataset.k===ans).classList.add('ok')}
    const ex=$('.ex',q);ex&&ex.classList.remove('hidden');out&&(out.textContent=`得分 ${sc} / ${tot}（已答 ${done}）`)}))});
  const rs=$('[data-reset]',qz);rs&&rs.addEventListener('click',()=>{sc=0;done=0;$$('.q',qz).forEach(q=>{delete q.dataset.done;$$('.opts button',q).forEach(b=>b.classList.remove('ok','no'));const ex=$('.ex',q);ex&&ex.classList.add('hidden')});out&&(out.textContent='得分 0 / '+tot)});
});
// order game
$$('.ordgame').forEach(g=>{const seq=JSON.parse(g.dataset.seq);const pool=$('.ord',g),ans=$('.ans',g),msg=$('.msg',g);let i=0;
  function init(){i=0;ans.textContent='';msg.textContent='';pool.innerHTML='';[...seq].sort(()=>Math.random()-.5).forEach(s=>{const b=document.createElement('button');b.textContent=s;b.onclick=()=>{if(s===seq[i]){b.classList.add('done');ans.textContent+=(i?' → ':'')+s;i++;if(i===seq.length)msg.textContent='🎉 全部正确！'}else{msg.textContent='✗ 下一个应是第 '+(i+1)+' 个，再想想';b.animate([{transform:'translateX(-4px)'},{transform:'translateX(4px)'},{transform:'none'}],{duration:240})}};pool.appendChild(b)})}
  init();$('[data-restart]',g)&&$('[data-restart]',g).addEventListener('click',init)});
onScroll();
})();
