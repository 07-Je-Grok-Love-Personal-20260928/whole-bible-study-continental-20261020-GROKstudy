"""v7: static internal link + anchor checker (includes ids inside lazy <template>s)."""
import os,re,sys,html
SITE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages=[f for f in os.listdir(SITE) if f.endswith('.html')]
ids={p:set(re.findall(r'\sid="([^"]+)"',open(os.path.join(SITE,p),encoding='utf-8').read())) for p in pages}
bad=[];n=0
for p in pages:
    s=open(os.path.join(SITE,p),encoding='utf-8').read()
    for h in re.findall(r'\shref="([^"]+)"',s):
        h=html.unescape(h)
        if re.match(r'^(https?:|mailto:|tel:|data:|javascript:)',h): continue
        n+=1; f,_,a=h.partition('#'); f=f or p
        if f.endswith(('.css','.js','.png','.svg','.ico','.json','.webmanifest','.xml','.txt')) or '?' in f:
            if not os.path.exists(os.path.join(SITE,f.split('?')[0])): bad.append((p,h,'missing file'))
            continue
        if f not in ids: bad.append((p,h,'missing page')); continue
        if a and a not in ids[f]: bad.append((p,h,'missing anchor'))
    for h in re.findall(r'\ssrc="([^"]+)"',s):
        if re.match(r'^(https?:|data:|//)',h): continue
        n+=1
        if not os.path.exists(os.path.join(SITE,h.split('?')[0].split('#')[0])): bad.append((p,h,'missing src'))
for b in bad: print('BAD',*b)
print(f'links checked: {n}, broken: {len(bad)}')
sys.exit(1 if bad else 0)
