"""Pre-render Mermaid diagrams to inline SVG (dark + light) so no Mermaid runtime is needed in the browser."""
import re,json,hashlib,html,os
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); SITE=os.path.dirname(HERE)
CACHE=os.path.join(HERE,'data','mercache.json')
FONT='"Noto Sans CJK SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif'
DARK={'primaryColor':'#26306a','primaryTextColor':'#eef','lineColor':'#ffcb5c','secondaryColor':'#3a2350','tertiaryColor':'#13324a'}
PRE=re.compile(r'<pre class="mermaid">(.*?)</pre>',re.S)
def run(files):
    cache=json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    srcs={}
    for f in files:
        for m in PRE.finditer(open(os.path.join(SITE,f)).read()): srcs[hashlib.sha1(m.group(1).encode()).hexdigest()[:12]]=html.unescape(m.group(1))
    todo=[h for h in srcs if h not in cache]
    if todo:
        with sync_playwright() as p:
            b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
            pg=b.new_page(viewport={'width':1200,'height':900})
            pg.set_content('<html><body style="width:1100px"><div id="x"></div></body></html>')
            pg.add_script_tag(path=os.path.join(SITE,'assets/vendor/mermaid.min.js'))
            for h in todo:
                out={}
                for th in ('dark','light'):
                    cfg={'startOnLoad':False,'securityLevel':'loose','theme':'dark' if th=='dark' else 'default','fontFamily':FONT,'flowchart':{'htmlLabels':True,'curve':'basis','useMaxWidth':True},'mindmap':{'useMaxWidth':True}}
                    if th=='dark': cfg['themeVariables']=DARK
                    out[th]=pg.evaluate("async ([c,s,id])=>{mermaid.initialize(c);const r=await mermaid.render(id,s);return r.svg}",[cfg,srcs[h],f'm{h}{th[0]}'])
                cache[h]=out; print('rendered',h)
            b.close()
        json.dump(cache,open(CACHE,'w'))
    n=0
    for f in files:
        fp=os.path.join(SITE,f); s=open(fp).read()
        def rep(m):
            nonlocal n; h=hashlib.sha1(m.group(1).encode()).hexdigest()[:12]; n+=1
            vb=re.search(r'viewBox="([-0-9. ]+)"',cache[h]["dark"]); w,hh=(float(x) for x in vb.group(1).split()[2:4]) if vb else (0,1)
            wide=f' mwide" style="--mw:{round(w*.78)}px' if w>1000 and w/hh>6 else ''   # v10: long LR chains keep a readable size and scroll sideways
            return f'<div class="mersvg md{wide}">{cache[h]["dark"]}</div><div class="mersvg ml{wide}">{cache[h]["light"]}</div>'
        s=PRE.sub(rep,s); open(fp,'w').write(s)
    print('mermaid prerendered:',n)
