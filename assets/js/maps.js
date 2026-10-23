/* v9 maps: Leaflet + Natural Earth offline base (assets/data/ne.js) + online tile chains; loaded lazily. Degrades to a text list if Leaflet missing. */
(function(){
addEventListener('scroll',()=>{window.__mLS=performance.now()},{passive:true});
/* v9: tile-provider chains with automatic fallback (tileerror / no-load watchdog) over an always-present
   offline Natural Earth base drawn in its own pane UNDER the tiles — if every host is blocked the base still shows. */
const PROV={
 topo:[['https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}','Esri World Topo','',17],
       ['https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png','© OpenTopoMap (CC-BY-SA) © OSM','abc',15],
       ['https://services.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}','Esri Shaded Relief','',13],
       ['https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png','© CARTO © OpenStreetMap','abcd',18]],
 sat:[['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}','Esri World Imagery','',17],
      ['https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}','Esri World Imagery（备用主机）','',17]],
 street:[['https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png','© CARTO © OpenStreetMap','abcd',18],
         ['https://tile.openstreetmap.org/{z}/{x}/{y}.png','© OpenStreetMap','',18],
         ['https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png','© OSM France · HOT','abc',18]]};
const KIND=[['off','示意'],['topo','地形'],['sat','卫星'],['street','街道']];
const BEST={};/* provider index that worked on this page, shared by all maps */
const SEAS=[['地 中 海',[34.2,25]],['红 海',[21.5,38.3]],['波 斯 湾',[27.3,51]],['黑 海',[43.2,34.5]],['里 海',[41.5,50.6]],['爱 琴 海',[38.6,25.1]],['亚 得 里 亚 海',[42.8,15.6]]];
function tiles(m,kind,note){
  if(m._tl){m.removeLayer(m._tl);m._tl=null}clearTimeout(m._wd);m._kind=kind;m._el&&m._el.classList.remove('mtok');
  if(kind==='off'){note('离线示意底图（Natural Earth）');return}
  const ch=PROV[kind];let i=BEST[kind]||0;
  const next=why=>{if(m._tl){m.removeLayer(m._tl);m._tl=null}clearTimeout(m._wd);
    m._el&&m._el.classList.remove('mtok');
    if(i>=ch.length){note('⚠️ 在线底图均不可达 → 已显示离线底图',1);m._el&&m._el.classList.add('mtfail');return}
    const p=ch[i],t=L.tileLayer(p[0],{subdomains:p[2]||'abc',maxZoom:p[3],maxNativeZoom:p[3],attribution:p[1],crossOrigin:false,keepBuffer:1,updateWhenIdle:true});
    let ok=0,er=0;const adv=()=>{if(m._tl!==t)return;i++;next()};
    t.on('tileload',()=>{if(!ok){BEST[kind]=i;note(KIND.find(k=>k[0]===kind)[1]+' · '+p[1].replace(/^©\s*/,''))}ok++});
    /* v9 perf: once the online layer has fully covered the view, stop painting the offline base under it (it was the main scroll-raster cost) */
    t.on('load',()=>{if(m._tl===t&&ok&&m._el)m._el.classList.add('mtok')});
    t.on('tileerror',()=>{er++;if(er>=3&&ok===0||er>ok*2+8)adv()});
    m._tl=t;t.addTo(m);m._wd=setTimeout(()=>{if(!ok)adv()},4500);note('⏳ 正在连接 '+p[1].replace(/^©\s*/,'')+'…')};
  m._el&&m._el.classList.remove('mtfail');next()}
/* v10: offline Natural Earth base as a local 256-px tile layer (GridLayer of canvas tiles drawn from the vectors on demand,
   in idle slices) — behaves like the online tile layers, which scroll smoothly; no single huge raster surface. */
let NEBB=null;const neBB=()=>NEBB||(NEBB=(()=>{const bb=q=>{let a=1e9,b=1e9,c=-1e9,d=-1e9;q.forEach(p=>{if(p[0]<a)a=p[0];if(p[0]>c)c=p[0];if(p[1]<b)b=p[1];if(p[1]>d)d=p[1]});return [a,b,c,d]};const N=window.NE;
  return {land:N.land.map(pl=>[pl,bb(pl[0])]),lakes:N.lakes.map(l=>[l.c,bb(l.c[0])]),rivers:N.rivers.map(r=>[r.c,bb(r.c),!!r.n])}})());
const idle=window.requestIdleCallback?f=>requestIdleCallback(f,{timeout:400}):f=>setTimeout(f,30);
function neTile(m,cv,co,ts){const g=cv.getContext('2d'),z=co.z,o=co.scaleBy(ts),nw=m.unproject(o,z),se=m.unproject(o.add(ts),z),pad=.3*(nw.lat-se.lat+1e-9);
  const W=nw.lng-pad,E=se.lng+pad,S=se.lat-pad,N=nw.lat+pad,hit=b=>!(b[2]<W||b[0]>E||b[3]<S||b[1]>N),B=neBB();g.lineJoin='round';
  const ring=r=>{for(let i=0;i<r.length;i++){const p=m.project([r[i][1],r[i][0]],z);i?g.lineTo(p.x-o.x,p.y-o.y):g.moveTo(p.x-o.x,p.y-o.y)}};
  g.beginPath();B.land.forEach(([pl,b])=>{if(hit(b))pl.forEach(r=>{ring(r);g.closePath()})});g.fillStyle='#eadcb4';g.fill('evenodd');g.strokeStyle='#b99a5e';g.lineWidth=1;g.stroke();
  g.beginPath();B.lakes.forEach(([c,b])=>{if(hit(b))c.forEach(r=>{ring(r);g.closePath()})});g.fillStyle='#5d97e3';g.fill('evenodd');g.strokeStyle='#3a7bd5';g.stroke();
  g.globalAlpha=.9;[false,true].forEach(nm=>{g.beginPath();B.rivers.forEach(([c,b,n])=>{if(n===nm&&hit(b))ring(c)});g.lineWidth=nm?2.2:1.2;g.stroke()})}
/* tiles are drawn on a scratch canvas, then handed to the layer as blob <img>s (plain decoded images composite far cheaper
   than hundreds of live 2D-canvas surfaces while scrolling) */
function neLayer(m){const NEG=L.GridLayer.extend({createTile(co,done){const im=document.createElement('img'),ts=this.getTileSize();im.alt='';
    im.onload=()=>{URL.revokeObjectURL(im.src);done(null,im)};im.onerror=()=>done(null,im);
    idle(()=>{const cv=document.createElement('canvas');cv.width=ts.x;cv.height=ts.y;try{neTile(m,cv,co,ts)}catch(e){}
      cv.toBlob(b=>{if(b)im.src=URL.createObjectURL(b);else done(null,im)})});return im}});
  return new NEG({pane:'nebase',keepBuffer:1,updateWhenIdle:true,maxZoom:18,className:'netile'}).addTo(m)}
function base(el,cfg,jobs){
  const m=L.map(el,{scrollWheelZoom:false,zoomSnap:.25,worldCopyJump:false,attributionControl:true,preferCanvas:!!cfg.canvas});m._el=el;
  m.createPane('nebase').style.zIndex=150;
  const NE=window.NE;
  /* v10: offline base = local tile layer (see neLayer); named lakes/rivers keep hover tooltips via invisible hit shapes */
  if(NE){jobs.push(()=>{m._ne=neLayer(m)});
    jobs.push(()=>{const B=L.latLngBounds(cfg.bounds).pad(.6);
      /* hover names for lakes/rivers via a pure-JS hit test (no invisible SVG shapes: they made a huge vector layer that cost ~2x paint while scrolling) */
      const lk=NE.lakes.filter(k=>k.n&&B.intersects(L.latLngBounds(k.c[0].map(p=>[p[1],p[0]])))),rv=NE.rivers.filter(r=>r.n&&B.intersects(L.latLngBounds(r.c.map(p=>[p[1],p[0]]))));
      if(lk.length||rv.length){let tt=null,raf=0,ev=null;const inR=(x,y,r)=>{let c=false;for(let i=0,j=r.length-1;i<r.length;j=i++){const a=r[i],b=r[j];if((a[1]>y)!==(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])c=!c}return c};
        const sd=(p,a,b)=>{const dx=b.x-a.x,dy=b.y-a.y,l=dx*dx+dy*dy;let t=l?((p.x-a.x)*dx+(p.y-a.y)*dy)/l:0;t=t<0?0:t>1?1:t;const ex=a.x+t*dx-p.x,ey=a.y+t*dy-p.y;return ex*ex+ey*ey};
        const find=e=>{const x=e.latlng.lng,y=e.latlng.lat;for(const k of lk)if(inR(x,y,k.c[0]))return k.n;const p=e.layerPoint;let best=null,bd=64;
          for(const r of rv){let a=m.latLngToLayerPoint([r.c[0][1],r.c[0][0]]);for(let i=1;i<r.c.length;i++){const b=m.latLngToLayerPoint([r.c[i][1],r.c[i][0]]),d=sd(p,a,b);if(d<bd){bd=d;best=r.n}a=b}}return best};
        m.on('mousemove',e=>{ev=e;if(!raf)raf=requestAnimationFrame(()=>{raf=0;const n=find(ev);if(n){if(!tt)tt=L.tooltip({direction:'top',offset:[0,-6]});tt.setLatLng(ev.latlng).setContent(n);if(!m.hasLayer(tt))tt.addTo(m)}else if(tt&&m.hasLayer(tt))m.removeLayer(tt)})});
        m.on('mouseout',()=>{if(tt&&m.hasLayer(tt))m.removeLayer(tt)})}
      SEAS.forEach(s=>{if(B.contains(s[1]))L.marker(s[1],{pane:'nebase',interactive:false,icon:L.divIcon({className:'',html:'<span class="mlabel sea">'+s[0]+'</span>',iconSize:null})}).addTo(m)})})}
  /* status chip + switcher 示意/地形/卫星/街道 */
  const st=L.control({position:'bottomright'});let stEl;st.onAdd=()=>{stEl=L.DomUtil.create('div','mlnote');return stEl};st.addTo(m);
  const note=(t,bad)=>{if(stEl){stEl.textContent=t;stEl.classList.toggle('bad',!!bad)}};
  const sw=L.control({position:'topright'});sw.onAdd=()=>{const d=L.DomUtil.create('div','mlsw');d.setAttribute('role','group');d.setAttribute('aria-label','底图');
    d.innerHTML=KIND.map(k=>'<button type="button" data-k="'+k[0]+'" aria-pressed="false">'+k[1]+'</button>').join('');L.DomEvent.disableClickPropagation(d);
    d.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;set(b.dataset.k);try{localStorage.setItem('wb-mapbase',b.dataset.k)}catch(_){}});return d};sw.addTo(m);
  const set=k=>{sw.getContainer().querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.k===k));tiles(m,k,note)};
  let k0='topo';try{k0=localStorage.getItem('wb-mapbase')||'topo'}catch(_){}if(navigator.onLine===false)k0='off';if(!PROV[k0])k0='off';
  jobs.push(()=>set(k0));
  m.attributionControl.setPrefix('Leaflet · 离线底图 Natural Earth（公有领域）');
  m.fitBounds(cfg.bounds);
  return m;
}
function lab(m,ll,t,cls){return L.marker(ll,{icon:L.divIcon({className:'',html:'<span class="mlabel '+(cls||'')+'">'+t+'</span>',iconSize:null})}).addTo(m)}
function pt(m,p,color){
  const c=L.circleMarker(p.ll,{radius:p.r||6,color:'#fff',weight:1.5,fillColor:p.c||color||'#ff6b6b',fillOpacity:1}).addTo(m);
  const small=innerWidth<640;c.bindTooltip(p.n,{permanent:p.perm!==false&&(!small||p.k),direction:p.dir||'right',className:'mlabel',offset:[6,0]});
  if(p.d)c.bindPopup('<b>'+p.n+'</b><br>'+p.d);
  c._prio=p.n==='耶路撒冷'?3:p.k?2:0;(m._pts||(m._pts=[])).push(c);
  c.on('mouseover',()=>{const e=c.getTooltip()&&c.getTooltip().getElement();e&&e.classList.add('mlpeek')});c.on('mouseout',()=>{const e=c.getTooltip()&&c.getTooltip().getElement();e&&e.classList.remove('mlpeek')});
  return c;
}
/* v7: label collision handling — key places (k=1) first, then in order; overlapped labels hide and reappear on hover or zoom-in */
function declutter(m){const pts=(m._pts||[]).slice().sort((a,b)=>b._prio-a._prio);const kept=[],regs=[...m.getContainer().querySelectorAll('.leaflet-marker-pane .mlabel.reg')].map(e=>e.getBoundingClientRect());
  const rs=pts.map(c=>{const e=c.getTooltip()&&c.getTooltip().getElement();if(!e)return null;e.classList.remove('mlhide');return [c,e,e.getBoundingClientRect()]}).filter(Boolean);
  rs.forEach(([c,e,r])=>{if(!r.width)return;const ov=k=>!(r.right<k.left-2||r.left>k.right+2||r.bottom<k.top-1||r.top>k.bottom+1);const hit=(c._prio<2&&regs.some(ov))||kept.some(k=>!(r.right<k.left-2||r.left>k.right+2||r.bottom<k.top-1||r.top>k.bottom+1));if(hit)e.classList.add('mlhide');else kept.push(r)})}
function build(el){
  const cfg=window.MAPS&&window.MAPS[el.dataset.map];if(!cfg)return;
  if(!(window.L&&L.map)){el.innerHTML='<div class="mapfb"><b>地图脚本未加载（离线或被拦截），以下为地点列表：</b><ul>'+(cfg.points||[]).map(p=>'<li>'+p.n+(p.d?'：'+p.d:'')+'</li>').join('')+'</ul></div>';return}
  const jobs=[];const m=base(el,cfg,jobs);
  (cfg.regions||[]).forEach(r=>jobs.push(()=>{if(r.poly)L.polygon(r.poly,{color:r.c,weight:1.5,fillColor:r.c,fillOpacity:.22,dashArray:r.dash||null}).bindPopup('<b>'+r.n+'</b><br>'+(r.d||'')).addTo(m);if(r.circle)L.circle(r.circle,{radius:r.rad,color:r.c,weight:1.5,fillColor:r.c,fillOpacity:.25}).bindPopup('<b>'+r.n+'</b><br>'+(r.d||'')).addTo(m);if(r.lab)lab(m,r.lab,r.n,'reg')}));
  (cfg.routes||[]).forEach(r=>jobs.push(()=>{const pl=L.polyline(r.path,{color:r.c,weight:r.w||4,opacity:.95,dashArray:r.dash||null}).addTo(m);pl.bindTooltip(r.n,{sticky:true});
     if(r.arrow!==false){const a=r.path[r.path.length-1];L.circleMarker(a,{radius:4,color:r.c,fillColor:r.c,fillOpacity:1}).addTo(m)}}));
  (cfg.valleys||[]).forEach(v=>jobs.push(()=>L.polyline(v.path,{color:'#2f7fd8',weight:5,opacity:.5,dashArray:'2 8'}).bindTooltip(v.n,{sticky:true}).addTo(m)));
  (cfg.points||[]).forEach(p=>jobs.push(()=>pt(m,p,cfg.color)));
  (cfg.labels||[]).forEach(l=>jobs.push(()=>lab(m,l.ll,l.n,l.cls||'reg')));
  if(cfg.legend)jobs.push(()=>{const lg=L.control({position:'bottomleft'});lg.onAdd=()=>{const d=L.DomUtil.create('div','mlabel');d.style.whiteSpace='normal';d.style.maxWidth='220px';d.style.lineHeight='1.6';d.innerHTML=cfg.legend.map(x=>'<span style="display:inline-block;width:12px;height:4px;background:'+x[0]+';margin-right:6px;vertical-align:middle"></span>'+x[1]).join('<br>');return d};lg.addTo(m)});
  /* add layers in small time-sliced chunks so no single task is long */
  const run=()=>{const now=performance.now();if(now-(window.__mLS||0)<260){setTimeout(run,200);return}const t0=now;while(jobs.length&&performance.now()-t0<8)jobs.shift()();if(jobs.length)setTimeout(run,24)};setTimeout(run,16);
  el._map=m; setTimeout(()=>m.invalidateSize(),300);
  let dT=0;const dc=()=>{clearTimeout(dT);dT=setTimeout(()=>{if(jobs.length){dc();return}requestAnimationFrame(()=>declutter(m))},120)};m.on('zoomend moveend',dc);dc();
}
/* v9: Leaflet + Natural Earth are fetched only when a real map is first needed */
let ldP=null;const js=u=>new Promise((ok,no)=>{const s=document.createElement('script');s.src=u;s.onload=ok;s.onerror=no;document.head.appendChild(s)});
function need(){const hasL=()=>window.L&&window.L.map;if(hasL()&&window.NE)return Promise.resolve();if(ldP)return ldP;
  if(!document.querySelector('link[href*="leaflet.css"]')){const l=document.createElement('link');l.rel='stylesheet';l.href='assets/vendor/leaflet.css';document.head.appendChild(l)}
  return ldP=Promise.all([hasL()?0:js('assets/vendor/leaflet.js'),window.NE?0:js('assets/data/ne.js')]).catch(()=>{})}
function safe(el){const x=el.closest('.mapx');if(x&&x.dataset.v!=='r')tab(x,'r',1);if(el._built)return;el._built=1;
  need().then(()=>{el.innerHTML='';try{build(el)}catch(e){console.warn(e);el.innerHTML='<div class="mapfb">地图加载失败</div>'}})}
/* 概念图 / 实景地图 tabs */
function tab(x,v,noBuild){x.dataset.v=v;x.querySelectorAll('.mxt [role=tab]').forEach(b=>{const on=b.dataset.v===v;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1});
  const c=x.querySelector('.mxc'),r=x.querySelector('.map');if(c)c.hidden=v!=='c';if(r){r.hidden=v!=='r';if(v==='r'){if(!noBuild)safe(r);else if(r._map)setTimeout(()=>r._map.invalidateSize(),30)}}}
document.addEventListener('click',e=>{const b=e.target.closest('.mxt [role=tab]');if(!b)return;const x=b.closest('.mapx');tab(x,b.dataset.v);try{localStorage.setItem('wb-maptab',b.dataset.v)}catch(_){}});
document.addEventListener('keydown',e=>{const b=e.target.closest&&e.target.closest('.mxt [role=tab]');if(!b||!/^Arrow(Left|Right)$/.test(e.key))return;const o=b.parentNode.querySelector('[role=tab]:not([data-v="'+b.dataset.v+'"])');if(o){o.focus();o.click()}});
/* concept maps animate only while on screen (SMIL paused + CSS class) */
const cio='IntersectionObserver' in window?new IntersectionObserver(es=>es.forEach(en=>{const f=en.target,s=f.querySelector('.cmo');f.classList.toggle('run',en.isIntersecting);if(s&&s.pauseAnimations)en.isIntersecting?s.unpauseAnimations():s.pauseAnimations()}),{rootMargin:'40px 0px'}):null;
function init(){document.querySelectorAll('.cmo').forEach(s=>s.pauseAnimations&&s.pauseAnimations());if(cio)document.querySelectorAll('.cmap').forEach(f=>cio.observe(f));let pref='c';try{pref=localStorage.getItem('wb-maptab')||'c'}catch(_){}
  document.querySelectorAll('.mapx').forEach(x=>{if(!x.dataset.v)tab(x,pref==='r'?'r':'c',1)});
  const els=[...document.querySelectorAll('.map[data-map]')].filter(el=>!el.hidden);
  window.__mapsAll=()=>document.querySelectorAll('.map[data-map]').forEach(el=>{if(!el.hidden||!el.closest('.mapx'))safe(el)});
  if(!('IntersectionObserver' in window)){els.forEach(safe);return}
/* build only while the user is not scrolling (Leaflet init is a long task) */
let lastS=0,qT=0;const q=[];addEventListener('scroll',()=>{lastS=performance.now()},{passive:true});
const pump=()=>{qT=0;if(!q.length)return;const idle=performance.now()-lastS;if(idle<350){qT=setTimeout(pump,380-idle);return}safe(q.shift());if(q.length)qT=setTimeout(pump,120)};
const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){io.unobserve(en.target);q.push(en.target);if(!qT)qT=setTimeout(pump,60)}}),{rootMargin:'300px 0px'});els.forEach(el=>io.observe(el))}
window.__mapBuild=safe;window.__mapTab=tab;
if(document.readyState!=='loading')init();else document.addEventListener('DOMContentLoaded',init);
let rzT=0;addEventListener('resize',()=>{clearTimeout(rzT);rzT=setTimeout(()=>document.querySelectorAll('.map').forEach(el=>el._map&&el._map.invalidateSize()),200)},{passive:true});
})();
