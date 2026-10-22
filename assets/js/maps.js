/* Leaflet maps: offline vector base (assets/data/land.js) + optional online tiles. Degrades to text list if Leaflet missing. */
(function(){
const RIVERS={
 '尼罗河':[[24.09,32.9],[25.7,32.64],[27.18,31.18],[29.0,30.85],[30.04,31.23],[30.6,31.0],[31.45,30.4]],
 '尼罗河东支':[[30.04,31.23],[30.8,31.6],[31.4,31.85]],
 '幼发拉底河':[[39.0,39.4],[38.4,38.6],[36.83,38.01],[35.95,39.0],[35.3,40.15],[34.55,40.89],[33.4,43.3],[32.54,44.42],[31.3,45.6],[30.96,46.1],[30.6,47.4],[29.95,48.5]],
 '底格里斯河':[[38.0,40.4],[37.5,42.0],[36.36,43.15],[35.45,43.26],[34.2,43.9],[33.3,44.4],[32.4,45.7],[31.1,47.4],[30.6,47.6]],
 '约旦河':[[33.25,35.62],[32.9,35.62],[32.71,35.57],[32.35,35.56],[32.0,35.53],[31.77,35.55]]
};
const LAKES={
 '死海':[[31.78,35.55],[31.72,35.6],[31.5,35.6],[31.25,35.53],[31.05,35.45],[31.12,35.38],[31.4,35.45],[31.65,35.47]],
 '加利利海':[[32.9,35.59],[32.86,35.65],[32.8,35.65],[32.71,35.6],[32.75,35.53],[32.84,35.52]]
};
function base(el,cfg,jobs){
  const m=L.map(el,{scrollWheelZoom:false,zoomSnap:.25,worldCopyJump:false,attributionControl:true,preferCanvas:false});
  const off=L.layerGroup();
  if(window.LAND){const gj=L.geoJSON(null,{style:{color:'#c9a96a',weight:1,fillColor:'#e8d9b0',fillOpacity:.92},interactive:false}).addTo(off);
    let fs=window.LAND.features||[window.LAND];fs=fs.flatMap(f=>f.geometry&&f.geometry.type==='MultiPolygon'?f.geometry.coordinates.map(c=>({type:'Feature',properties:{},geometry:{type:'Polygon',coordinates:c}})):[f]);
    for(let i=0;i<fs.length;i+=8){const ch=fs.slice(i,i+8);jobs.push(()=>gj.addData({type:'FeatureCollection',features:ch}))}}
  const wat=L.layerGroup();
  for(const k in LAKES)L.polygon(LAKES[k],{color:'#3a7bd5',weight:1,fillColor:'#4f8ee0',fillOpacity:.9,interactive:false}).addTo(wat);
  for(const k in RIVERS)L.polyline(RIVERS[k],{color:'#3a7bd5',weight:2.2,opacity:.9}).bindTooltip(k,{sticky:true}).addTo(wat);
  off.addTo(m);jobs.push(()=>wat.addTo(m));
  jobs.push(()=>{
  const osm=L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:12,attribution:'© OpenStreetMap'});
  const topo=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}',{maxZoom:13,attribution:'Esri Shaded Relief'});
  L.control.layers({'离线矢量底图（默认）':off,'OpenStreetMap 在线':osm,'地形晕渲 在线':topo},{'河流湖泊':wat},{collapsed:true}).addTo(m);
  m.attributionControl.setPrefix('Leaflet · 离线海岸线 Natural Earth');
  });
  m.fitBounds(cfg.bounds);
  return m;
}
function lab(m,ll,t,cls){return L.marker(ll,{icon:L.divIcon({className:'',html:'<span class="mlabel '+(cls||'')+'">'+t+'</span>',iconSize:null})}).addTo(m)}
function pt(m,p,color){
  const c=L.circleMarker(p.ll,{radius:p.r||6,color:'#fff',weight:1.5,fillColor:p.c||color||'#ff6b6b',fillOpacity:1}).addTo(m);
  const small=innerWidth<640;c.bindTooltip(p.n,{permanent:p.perm!==false&&(!small||p.k),direction:p.dir||'right',className:'mlabel',offset:[6,0]});
  if(p.d)c.bindPopup('<b>'+p.n+'</b><br>'+p.d);
  return c;
}
function build(el){
  const cfg=window.MAPS&&window.MAPS[el.dataset.map];if(!cfg)return;
  if(!window.L){el.innerHTML='<div class="mapfb"><b>地图脚本未加载，以下为地点列表：</b><ul>'+(cfg.points||[]).map(p=>'<li>'+p.n+(p.d?'：'+p.d:'')+'</li>').join('')+'</ul></div>';return}
  const jobs=[];const m=base(el,cfg,jobs);
  (cfg.regions||[]).forEach(r=>jobs.push(()=>{if(r.poly)L.polygon(r.poly,{color:r.c,weight:1.5,fillColor:r.c,fillOpacity:.22,dashArray:r.dash||null}).bindPopup('<b>'+r.n+'</b><br>'+(r.d||'')).addTo(m);if(r.circle)L.circle(r.circle,{radius:r.rad,color:r.c,weight:1.5,fillColor:r.c,fillOpacity:.25}).bindPopup('<b>'+r.n+'</b><br>'+(r.d||'')).addTo(m);if(r.lab)lab(m,r.lab,r.n,'reg')}));
  (cfg.routes||[]).forEach(r=>jobs.push(()=>{const pl=L.polyline(r.path,{color:r.c,weight:r.w||4,opacity:.95,dashArray:r.dash||null}).addTo(m);pl.bindTooltip(r.n,{sticky:true});
     if(r.arrow!==false){const a=r.path[r.path.length-1];L.circleMarker(a,{radius:4,color:r.c,fillColor:r.c,fillOpacity:1}).addTo(m)}}));
  (cfg.points||[]).forEach(p=>jobs.push(()=>pt(m,p,cfg.color)));
  (cfg.labels||[]).forEach(l=>jobs.push(()=>lab(m,l.ll,l.n,l.cls||'reg')));
  if(cfg.legend)jobs.push(()=>{const lg=L.control({position:'bottomleft'});lg.onAdd=()=>{const d=L.DomUtil.create('div','mlabel');d.style.whiteSpace='normal';d.style.maxWidth='220px';d.style.lineHeight='1.6';d.innerHTML=cfg.legend.map(x=>'<span style="display:inline-block;width:12px;height:4px;background:'+x[0]+';margin-right:6px;vertical-align:middle"></span>'+x[1]).join('<br>');return d};lg.addTo(m)});
  /* add layers in small time-sliced chunks so no single task is long */
  const run=()=>{const t0=performance.now();while(jobs.length&&performance.now()-t0<12)jobs.shift()();if(jobs.length)setTimeout(run,16)};setTimeout(run,16);
  el._map=m; setTimeout(()=>m.invalidateSize(),300);
}
function safe(el){if(el._built)return;el._built=1;el.innerHTML='';try{build(el)}catch(e){console.warn(e);el.innerHTML='<div class="mapfb">地图加载失败</div>'}}
function init(){const els=[...document.querySelectorAll('.map[data-map]')];if(!('IntersectionObserver' in window)){els.forEach(safe);return}
/* build only while the user is not scrolling (Leaflet init is a long task) */
let lastS=0,qT=0;const q=[];addEventListener('scroll',()=>{lastS=performance.now()},{passive:true});
const pump=()=>{qT=0;if(!q.length)return;const idle=performance.now()-lastS;if(idle<350){qT=setTimeout(pump,380-idle);return}safe(q.shift());if(q.length)qT=setTimeout(pump,120)};
const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){io.unobserve(en.target);q.push(en.target);if(!qT)qT=setTimeout(pump,60)}}),{rootMargin:'300px 0px'});els.forEach(el=>io.observe(el));window.__mapsAll=()=>els.forEach(safe)}
window.__mapBuild=safe;
if(document.readyState!=='loading')init();else document.addEventListener('DOMContentLoaded',init);
let rzT=0;addEventListener('resize',()=>{clearTimeout(rzT);rzT=setTimeout(()=>document.querySelectorAll('.map').forEach(el=>el._map&&el._map.invalidateSize()),200)},{passive:true});
})();
