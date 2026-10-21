"""measure real book-card heights (hydrated) at 3 widths -> data/bkh.json (placeholder sizes, avoids scroll jumps)"""
import json,os
from playwright.sync_api import sync_playwright
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for key,w in (('d',1440),('t',820),('m',390)):
        for pg in ('ot.html','nt.html'):
            page=b.new_page(viewport={'width':w,'height':900}); page.goto('file://'+SITE+'/'+pg); page.wait_for_timeout(300)
            page.add_style_tag(content='.bk{content-visibility:visible!important}')
            page.evaluate("window.__hydrateAll()"); page.wait_for_timeout(300)
            r=page.evaluate("Object.fromEntries([...document.querySelectorAll('.bk')].map(c=>[c.id.slice(3),[c.offsetHeight,c.querySelector('.body').offsetHeight]]))")
            for k,(full,body) in r.items(): out.setdefault(k,{})[key]=body; out[k][key.upper()]=full
            page.close()
json.dump(out,open(os.path.join(SITE,'_build','data','bkh.json'),'w'))
print(len(out),'books', out.get('gen'))
