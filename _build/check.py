import sys,os,json
from playwright.sync_api import sync_playwright
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); pages=sys.argv[1].split(',') if len(sys.argv)>1 and sys.argv[1]!='all' else [f for f in sorted(os.listdir(SITE)) if f.endswith('.html')]
widths=[int(x) for x in os.environ.get("WIDTHS","390,820,1440").split(",")]; shots=len(sys.argv)>2; themes=os.environ.get('THEMES','night').split(',')
res=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for th in themes:
     for w in widths:
        ctx=b.new_context(viewport={'width':w,'height':900},device_scale_factor=1); ctx.add_init_script(f"localStorage.setItem('wb-theme','{th}')")
        for pg in pages:
            page=ctx.new_page(); errs=[]
            page.on('console',lambda m,errs=errs: errs.append(m.text) if m.type=='error' else None)
            page.on('pageerror',lambda e,errs=errs: errs.append('PAGEERR '+str(e)))
            page.goto('file://'+SITE+'/'+pg); page.wait_for_timeout(800)
            page.add_style_tag(content='section.blk,.bk{content-visibility:visible!important}')
            page.evaluate("()=>{window.__hydrateAll&&window.__hydrateAll();window.__merAll&&window.__merAll();window.__mapsAll&&window.__mapsAll();document.querySelectorAll('.rv,.sbar').forEach(e=>e.classList.add('in','go'))}")
            page.wait_for_timeout(4500 if pg in ('story.html','covenant.html','timeline.html','creeds.html','forms.html','nt.html') else 1500)
            r=page.evaluate("""()=>{const d=document.documentElement;const over=[];const clipped=e=>{if(e instanceof SVGElement&&e.ownerSVGElement){let o=e;while(o.ownerSVGElement)o=o.ownerSVGElement;e=o}let a=e.parentElement;while(a&&a!==d){const o=getComputedStyle(a).overflowX;if(o!=='visible'){return a.getBoundingClientRect().right<=d.clientWidth+1}a=a.parentElement}return false};
            document.querySelectorAll('main *').forEach(e=>{const r=e.getBoundingClientRect();if(r.right>d.clientWidth+1&&r.width>0&&!e.closest('.nav,.toc,.leaflet-container')&&!clipped(e))over.push(e.tagName+'.'+(e.getAttribute('class')||'')+':'+Math.round(r.right))});
            return {sw:d.scrollWidth,cw:d.clientWidth,over:over.slice(0,8),mer:document.querySelectorAll('.mersvg.md svg').length,merTot:document.querySelectorAll('pre.mermaid').length,merErr:[...document.querySelectorAll('pre.mermaid')].filter(p=>/Syntax error|error/i.test(p.textContent)&&!p.querySelector('svg')).length,maps:document.querySelectorAll('.leaflet-container').length,books:document.querySelectorAll('.bk').length,toc:document.querySelectorAll('#toc .tree a').length,tocOverlap:(()=>{const t=document.getElementById('toc').getBoundingClientRect(),m=document.getElementById('main').getBoundingClientRect();return innerWidth>1000&&t.width>0&&t.right>m.left+1})()}}""")
            r.update(theme=th,page=pg,w=w,errs=[e for e in errs if 'tile' not in e.lower() and 'net::' not in e][:5])
            res.append(r); print(json.dumps(r,ensure_ascii=False))
            if shots: page.screenshot(path=f'/workspace/wb/shots/{pg[:-5]}_{w}.png')
            page.close()
        ctx.close()
