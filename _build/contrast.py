"""v10 contrast audit: every visible text-bearing element in main/header/toc, WCAG ratio of its colour vs the blended
background stack (gradients approximated by their first colour stop). usage: THEMES=a,b WIDTH=1440 contrast.py page1,page2|all"""
import sys,os,json
from playwright.sync_api import sync_playwright
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages=sys.argv[1].split(',') if len(sys.argv)>1 and sys.argv[1]!='all' else [f for f in sorted(os.listdir(SITE)) if f.endswith('.html')]
themes=os.environ.get('THEMES','night').split(','); W=int(os.environ.get('WIDTH','1440')); MIN=float(os.environ.get('MIN','4.0'))
JS=r"""(MIN)=>{const P=s=>{const m=s.match(/rgba?\(([^)]+)\)/);if(!m)return null;const a=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);return [a[0],a[1],a[2],a.length>3?a[3]:1]};
const col=s=>{if(!s)return null;if(s.startsWith('color(srgb')){const a=s.slice(11,-1).split(/[ \/]+/).map(Number);return [a[0]*255,a[1]*255,a[2]*255,a.length>3?a[3]:1]}return P(s)};
const lum=c=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(c[0])+.7152*f(c[1])+.0722*f(c[2])};
const over=(top,bot)=>{const a=top[3];return [top[0]*a+bot[0]*(1-a),top[1]*a+bot[1]*(1-a),top[2]*a+bot[2]*(1-a),1]};
const bgOf=e=>{const st=[];let n=e;while(n&&n.nodeType===1){const cs=getComputedStyle(n);let c=col(cs.backgroundColor);if((!c||c[3]===0)&&cs.backgroundImage.includes('gradient')){const m=cs.backgroundImage.match(/(rgba?\([^)]+\)|color\(srgb[^)]+\))/);c=m?col(m[1]):null}
  if(c&&c[3]>0)st.push(c);if(c&&c[3]>=.999)break;n=n.parentElement}
  let b=st.length&&st[st.length-1][3]>=.999?st.pop():col(getComputedStyle(document.documentElement).getPropertyValue('--bg').trim().replace(/^#(..)(..)(..)$/,(m,r,g,b)=>`rgb(${parseInt(r,16)},${parseInt(g,16)},${parseInt(b,16)})`))||[0,0,0,1];
  while(st.length)b=over(st.pop(),b);return b};
const bad=[];let n=0;const seen=new Set();
document.querySelectorAll('main *, header *, #toc *').forEach(e=>{if(e instanceof SVGElement||e.closest('svg,.leaflet-container,.mersvg,pre.mermaid,.tsw'))return;
  const t=[...e.childNodes].filter(x=>x.nodeType===3&&x.textContent.trim()).map(x=>x.textContent.trim()).join('');if(!t)return;
  const r=e.getBoundingClientRect();if(!r.width||!r.height)return;const cs=getComputedStyle(e);if(cs.visibility!=='visible'||+cs.opacity<.35)return;
  const fc=col(cs.color);if(!fc||fc[3]<.05)return;if(cs.webkitTextFillColor&&col(cs.webkitTextFillColor)&&col(cs.webkitTextFillColor)[3]===0)return;
  const b=bgOf(e),f=over(fc,b),L1=lum(f),L2=lum(b),cr=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);n++;
  const big=parseFloat(cs.fontSize)>=18.5||(parseFloat(cs.fontSize)>=14&&+cs.fontWeight>=700);
  if(cr<(big?Math.min(3,MIN):MIN)){const k=e.tagName+'.'+(e.className&&e.className.baseVal===undefined?e.className:'');if(!seen.has(k)){seen.add(k);bad.push(k.slice(0,40)+' '+cr.toFixed(2)+' «'+t.slice(0,14)+'»')}}});
return {n,bad}}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for th in themes:
        ctx=b.new_context(viewport={'width':W,'height':900}); ctx.add_init_script(f"localStorage.setItem('wb-theme','{th}');localStorage.setItem('wb-mapbase','off')")
        for pg in pages:
            page=ctx.new_page(); page.goto('file://'+SITE+'/'+pg); page.wait_for_timeout(700)
            page.add_style_tag(content='section.blk,.bk{content-visibility:visible!important}*{transition:none!important;animation-duration:0s!important}')
            page.evaluate("()=>{window.__hydrateAll&&window.__hydrateAll();document.querySelectorAll('.rv,.sbar').forEach(e=>e.classList.add('in','go'))}"); page.wait_for_timeout(600)
            r=page.evaluate(JS,MIN); print(json.dumps(dict(theme=th,page=pg,n=r['n'],nbad=len(r['bad']),bad=r['bad'][:12]),ensure_ascii=False),flush=True); page.close()
        ctx.close()
