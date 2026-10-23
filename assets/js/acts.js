/* v8: animated journey drawing on the Acts map (rAF, one polyline + one marker; respects reduced motion) */
(()=>{const el=document.querySelector('.map[data-map="acts"]');const J=window.ACTSJ;if(!el||!J)return;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;let layer=null,raf=0;const cap=document.getElementById('actscap');
const ready=cb=>{if(el._map)return cb(el._map);window.__mapBuild&&window.__mapBuild(el);let n=0;const t=setInterval(()=>{if(el._map){clearInterval(t);setTimeout(()=>cb(el._map),250)}else if(++n>60)clearInterval(t)},120)};
function play(i){ready(m=>{if(!window.L)return;cancelAnimationFrame(raf);if(layer)layer.remove();layer=L.layerGroup().addTo(m);const j=J[i],pts=j.s.map(s=>s[1]);
 m.flyToBounds(L.latLngBounds(pts).pad(.12),{duration:.8});
 const line=L.polyline([pts[0]],{color:j.c,weight:5,opacity:.95}).addTo(layer);const dot=L.circleMarker(pts[0],{radius:8,color:'#fff',weight:2,fillColor:j.c,fillOpacity:1}).addTo(layer);
 const seg=[];let tot=0;for(let k=1;k<pts.length;k++){const d=Math.hypot(pts[k][0]-pts[k-1][0],pts[k][1]-pts[k-1][1]);seg.push(d);tot+=d}
 const dur=RM?1:Math.min(15000,Math.max(6000,tot*420));let t0=null,last=-1;
 const show=k=>{const s=j.s[k];if(!s)return;L.circleMarker(s[1],{radius:4.5,color:j.c,fillColor:'#fff',fillOpacity:1,weight:2}).addTo(layer);if(cap)cap.innerHTML='<b style="color:'+j.c+'">'+j.n.split(' · ')[0]+'</b> · 第 '+(k+1)+'/'+pts.length+' 站：<b>'+s[0]+'</b>'+(s[2]?' — '+s[2]:'')};
 const step=ts=>{if(t0===null)t0=ts+(RM?0:850);const f=Math.max(0,Math.min(1,(ts-t0)/dur));let dist=f*tot,k=0;while(k<seg.length-1&&dist>seg[k]){dist-=seg[k];k++}
  const r=seg[k]?Math.min(1,dist/seg[k]):1,a=pts[k],b=pts[k+1]||a,cur=[a[0]+(b[0]-a[0])*r,a[1]+(b[1]-a[1])*r];
  line.setLatLngs(pts.slice(0,k+1).concat([cur]));dot.setLatLng(cur);const reached=f>=1?pts.length-1:(r>=.999?k+1:k);while(last<reached){last++;show(last)}
  if(f<1)raf=requestAnimationFrame(step)};raf=requestAnimationFrame(step)})}
document.querySelectorAll('[data-jy]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-jy]').forEach(x=>x.classList.toggle('on',x===b));play(+b.dataset.jy)}));
})();
