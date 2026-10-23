/* GROKstudy v6 — page widgets: gospel filters + Venn, life-of-Christ timeline↔map sync, kings dual-lane hover. All event-driven (no scroll handlers). */
(function(){
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
/* ---------- gospel filters ---------- */
function applyG(f,sel,exact,syn){const t=document.getElementById(f.dataset.target);if(!t)return;let n=0;const rows=$$('tbody tr',t);
  rows.forEach(r=>{const g=r.dataset.g||'';let ok;
    if(syn!=null){const s=['Mt','Mk','Lk'].filter(k=>g.includes(k)).join('')||'—';ok=s===syn}
    else if(!sel.length)ok=true;else ok=exact?sel.join('')===g:sel.every(k=>g.includes(k));
    r.classList.toggle('off',!ok);r.classList.toggle('hit',ok&&(sel.length>0||syn!=null));if(ok)n++});
  const c=$('.gcount',f);if(c)c.textContent=n+' / '+rows.length+' 条'}
$$('.gfilter').forEach(f=>{const st=()=>{const sel=['Mt','Mk','Lk','Jn'].filter(k=>$(`button[data-g="${k}"]`,f).classList.contains('on'));applyG(f,sel,$('[data-only]',f).checked,null)};
  f.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;if(b.hasAttribute('data-reset')){$$('button[data-g]',f).forEach(x=>x.classList.remove('on'));$('[data-only]',f).checked=false}else b.classList.toggle('on');st()});
  $('[data-only]',f).addEventListener('change',st);st()});
$$('.venn').forEach(v=>{const pick=g=>{const on=!g.classList.contains('on');$$('.vr',v).forEach(x=>x.classList.remove('on'));if(on)g.classList.add('on');
    $$('.gfilter').forEach(f=>{$$('button[data-g]',f).forEach(x=>x.classList.remove('on'));applyG(f,[],false,on?g.dataset.set:null)});
    const t=$('#peritab');if(on&&t)t.scrollIntoView({behavior:'smooth',block:'start'})};
  v.addEventListener('click',e=>{const g=e.target.closest('.vr');if(g)pick(g)});
  v.addEventListener('keydown',e=>{const g=e.target.closest('.vr');if(g&&(e.key==='Enter'||e.key===' ')){e.preventDefault();pick(g)}})});
/* ---------- life of Christ: event list ↔ map ---------- */
const lt=$('.lifetl');
if(lt){const mapEl=$('.map[data-map="life"]');
  const fly=(ll,z,name)=>{if(!mapEl)return;const go=()=>{const m=mapEl._map;if(!m)return false;m.flyTo(ll,z||10,{duration:.9});
      if(mapEl._pin)mapEl._pin.remove();mapEl._pin=L.circleMarker(ll,{radius:11,color:'#fff',weight:3,fillColor:'#ff5d7a',fillOpacity:.95,className:'pinpulse'}).addTo(m).bindTooltip(name,{permanent:true,direction:'top',className:'mlabel'});return true};
    const x=mapEl.closest('.mapx');if(x&&x.dataset.v==='c'){const f=x.querySelector('.cmap');f.querySelectorAll('.cm-pt.hi').forEach(g=>g.classList.remove('hi'));const g=[...f.querySelectorAll('.cm-pt')].find(g=>{const t=g.querySelector('title');return t&&t.textContent.split('：')[0]===name});if(g)g.classList.add('hi');return}
    if(!go()){if(window.__mapBuild)window.__mapBuild(mapEl);let n=0;const t=setInterval(()=>{if(go()||++n>40)clearInterval(t)},120)}};
  lt.addEventListener('click',e=>{const b=e.target.closest('[data-ll]');if(!b)return;$$('[data-ll].on',lt).forEach(x=>x.classList.remove('on'));b.classList.add('on');
    const ll=b.dataset.ll.split(',').map(Number);fly(ll,+b.dataset.z||10,b.dataset.place||'');
    const pane=$('.lifemap');if(pane&&innerWidth<1000)pane.scrollIntoView({behavior:'smooth',block:'center'})});
  const ph=$('.lifeph');if(ph)ph.addEventListener('click',e=>{const b=e.target.closest('button[data-ph]');if(!b)return;$$('button',ph).forEach(x=>x.classList.toggle('on',x===b));const p=b.dataset.ph;
    $$('.lev',lt).forEach(x=>x.classList.toggle('off',p!=='all'&&x.dataset.ph!==p))});
  const play=$('#lifePlay');if(play){let tm=0;play.addEventListener('click',()=>{if(tm){clearInterval(tm);tm=0;play.textContent='▶️ 自动播放';return}
    const items=$$('.lev:not(.off) [data-ll]',lt);let i=Math.max(0,items.findIndex(x=>x.classList.contains('on'))+1);play.textContent='⏸️ 暂停';
    const step=()=>{if(i>=items.length){clearInterval(tm);tm=0;play.textContent='▶️ 自动播放';return}items[i].click();items[i].scrollIntoView({block:'nearest',behavior:'smooth'});i++};step();tm=setInterval(step,2200)})}}
/* ---------- Passion week day picker ---------- */
$$('.pweek').forEach(w=>w.addEventListener('click',e=>{const b=e.target.closest('[data-day]');if(!b)return;$$('[data-day]',w).forEach(x=>x.classList.toggle('on',x===b));
  $$('.pday',w).forEach(x=>x.hidden=x.dataset.d!==b.dataset.day)}));
/* ---------- kings dual lane: synchronized hover ---------- */
$$('.dlane').forEach(d=>{const info=$('.dlinfo',d);let last=null;const show=k=>{if(k===last)return;last=k;$$('.dk.hl',d).forEach(x=>x.classList.remove('hl'));if(!k)return;
    const el=$(`.dk[data-k="${k}"]`,d);if(!el)return;const s=+el.dataset.s,e=+el.dataset.e;el.classList.add('hl');
    $$('.dk',d).forEach(x=>{if(x!==el&&+x.dataset.s>=e-0.5&&+x.dataset.e<=s+0.5&&!(+x.dataset.s<e-0.5&&false))0;if(x!==el&&+x.dataset.s>e&&+x.dataset.e<s)0;
      if(x!==el&&Math.max(+x.dataset.e,e)<=Math.min(+x.dataset.s,s))x.classList.add('hl')});
    if(info)info.innerHTML=el.dataset.info};
  d.addEventListener('pointerover',e=>{const k=e.target.closest('.dk');if(k)show(k.dataset.k)});
  d.addEventListener('click',e=>{const k=e.target.closest('.dk');if(k)show(k.dataset.k)});
  d.addEventListener('focusin',e=>{const k=e.target.closest('.dk');if(k)show(k.dataset.k)})});
})();
