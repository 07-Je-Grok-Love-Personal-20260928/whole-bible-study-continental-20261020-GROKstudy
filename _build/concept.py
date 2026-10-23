"""v9: build-time 'hand-drawn' concept maps (inline SVG) from the same MAPS configs + vendored Natural Earth.
No SVG filters (cheap raster); sketch look = jittered double strokes; animation lives in a separate small overlay SVG."""
import json,math,random,os,html,re
from shapely.geometry import Polygon,LineString,box
HERE=os.path.dirname(os.path.abspath(__file__))
_NE=None
def ne():
    global _NE
    if _NE is None:
        s=open(os.path.join(HERE,'..','assets','data','ne.js')).read()
        _NE=json.loads(s[s.index('=')+1:].rstrip(';'))
    return _NE
E_=lambda s:html.escape(str(s),quote=True)
ICON={'耶路撒冷':'🕍','巴比伦':'🏯','尼尼微':'👑','书珊':'👑','波斯波利斯':'👑','孟斐斯':'𓂀','撒玛利亚':'👑','罗马':'🏛️','雅典':'🏛️','哥林多':'🏺','以弗所':'🏛️',
 '西奈山':'⛰️','迦密山':'⛰️','尼波山':'⛰️','何珥山':'⛰️','橄榄山':'⛰️','基利心山':'⛰️','他泊山':'⛰️','黑门山':'🏔️',
 '推罗':'⚓','西顿':'⚓','该撒利亚':'⚓','约帕':'⚓','特罗亚':'⚓','部丢利':'⚓','西流基':'⚓','尼亚坡里':'⚓','帕大喇':'⚓','每拉':'⚓','佳澳':'⚓','多利买':'⚓','米利都':'⚓','坚革哩':'⚓',
 '伯利恒':'⭐','拿撒勒':'🏠','迦百农':'🐟','伯赛大':'🐟','抹大拉':'🐟','迦拿':'🍷','别是巴':'💧','叙加':'💧','以琳':'🌴','玛拉':'💧','利非订':'🪨',
 '示剑':'🔥','伯特利':'🔥','希伯仑':'⛺','吾珥':'🌙','哈兰':'🌙','兰塞':'🧱','耶利哥':'🌴','米吉多':'⚔️','加低斯巴尼亚':'⛺','但':'🐂',
 '士每拿':'⛪','别迦摩':'⛪','推雅推喇':'⛪','撒狄':'⛪','非拉铁非':'⛪','老底嘉':'⛪','拔摩':'📜','大马士革':'🏙️','叙利亚安提阿':'⛪'}
def proj(cfg,W=1000):
    (s,w),(n,e)=cfg['bounds'];
    dl=(n-s)*.04;dw=(e-w)*.04;s-=dl;n+=dl;w-=dw;e+=dw
    k=math.cos(math.radians((s+n)/2))
    asp=(n-s)/((e-w)*k)
    lo,hi=(.5,.95) if not cfg.get('tall') else (.6,1.35)
    if asp<lo: d=((e-w)*k*lo-(n-s))/2;s-=d;n+=d
    if asp>hi: d=((n-s)/hi/k-(e-w))/2;w-=d;e+=d
    H=round(W*(n-s)/((e-w)*k))
    f=lambda la,lo_:(round((lo_-w)/(e-w)*W,1),round((n-la)/(n-s)*H,1))
    return f,W,H,(s,w,n,e),k
def jit(pts,rnd,a):return [(x+rnd.uniform(-a,a),y+rnd.uniform(-a,a)) for x,y in pts]
def dpath(pts,close=False):
    if not pts:return ''
    return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+(' Z' if close else '')
def smooth(pts):
    """Catmull-Rom → cubic Bézier (gentle curves for routes)"""
    if len(pts)<3:return dpath(pts)
    o=[f'M{pts[0][0]:.1f},{pts[0][1]:.1f}']
    P=[pts[0]]+pts+[pts[-1]]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6);c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        o.append(f'C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}')
    return ' '.join(o)
def nice_km(kmpx,W):
    target=kmpx*W*.18
    for v in [1,2,5,10,20,50,100,200,300,500,1000]:
        if v>=target*.6:return v
    return 1000
def tw(t,fs):return sum(fs*(1 if ord(ch)>0x2e80 else .56) for ch in t)
def svg(key,cfg,title=''):
    f,W,H,(s,w,n,e),k=proj(cfg)
    rnd=random.Random(key);S=cfg.get('fs',1)
    B=box(w,s,e,n);D=ne();tol=(e-w)/520
    o=[];ov=[]
    city=cfg.get('city')
    # land / water
    if not city:
        for c in D['land']:
            try:g=Polygon(c[0])
            except Exception:continue
            if not g.intersects(B):continue
            g=g.buffer(0).intersection(B).simplify(tol,preserve_topology=True)
            for p in (g.geoms if hasattr(g,'geoms') else [g]):
                if p.geom_type!='Polygon' or p.area<tol*tol*4:continue
                pts=[f(la,lo) for lo,la in p.exterior.coords]
                o.append(dpath(jit(pts,rnd,.5),True))
        land=' '.join(o);o=[]
        o.append(f'<path class="cm-wave" d="{land}"/><path class="cm-land" d="{land}"/><path class="cm-coast2" d="{land}" transform="translate(1.6 1.3)"/>')
        for r in D['rivers']:
            l=LineString(r['c'])
            if not l.intersects(B):continue
            g=l.intersection(B).simplify(tol)
            for q in (g.geoms if hasattr(g,'geoms') else [g]):
                if q.geom_type!='LineString' or q.length<tol*6:continue
                pts=[f(la,lo) for lo,la in q.coords]
                o.append(f'<path class="cm-riv{" n" if r["n"] else ""}" d="{dpath(jit(pts,rnd,.4))}">'+(f'<title>{E_(r["n"])}</title>' if r['n'] else '')+'</path>')
        for lk in D['lakes']:
            g=Polygon(lk['c'][0])
            if not g.intersects(B):continue
            pts=[f(la,lo) for lo,la in g.exterior.coords]
            o.append(f'<path class="cm-lake" d="{dpath(pts,True)}"><title>{E_(lk["n"])}</title></path>')
    else:
        o.append(f'<rect class="cm-land" x="0" y="0" width="{W}" height="{H}"/>')
        for v in cfg.get('valleys',[]):
            pts=[f(la,lo) for la,lo in v['path']]
            o.append(f'<path class="cm-val" d="{smooth(pts)}"><title>{E_(v["n"])}</title></path>')
    base=''.join(o);o=[]
    # regions
    rl=[]
    for r in cfg.get('regions',[]):
        c=r.get('c','#999')
        t=E_(r['n']+('：'+re.sub('<[^>]+>','',r['d']) if r.get('d') else ''))
        if r.get('poly'):
            pts=[f(la,lo) for la,lo in r['poly']]
            o.append(f'<path class="cm-reg" style="--c:{c}" d="{dpath(jit(pts,rnd,.8),True)}"{" stroke-dasharray=%s"%chr(34)+r["dash"]+chr(34) if r.get("dash") else ""}><title>{t}</title></path>')
        if r.get('circle'):
            x,y=f(*r['circle']);rad=r['rad']/111000/(n-s)*H
            o.append(f'<circle class="cm-reg" style="--c:{c}" cx="{x}" cy="{y}" r="{rad:.1f}"><title>{t}</title></circle>')
        if r.get('lab'):rl.append((r['n'],f(*r['lab']),c))
    regs=''.join(o);o=[]
    # routes (static ink + animated overlay)
    defs=[];cols=[]
    for i,r in enumerate(cfg.get('routes',[])):
        c=r.get('c','#f5c76b')
        if c not in cols:cols.append(c)
        mid=cols.index(c)
        pts=[f(la,lo) for la,lo in r['path']]
        d=smooth(pts)
        o.append(f'<path class="cm-rt" style="--c:{c}" d="{d}" marker-end="url(#ar-{key}-{mid})"{" stroke-dasharray=%s"%chr(34)+r["dash"]+chr(34) if r.get("dash") else ""}><title>{E_(r["n"])}</title></path>')
        dur=max(4,min(14,len(pts)*1.1))
        ov.append(f'<path class="cm-flow" style="--c:{c};animation-duration:{dur*.35:.1f}s" d="{d}"/><circle class="cm-mv" r="6" style="--c:{c}"><animateMotion dur="{dur:.1f}s" repeatCount="indefinite" path="{d}" rotate="auto"/></circle>')
    for j,c in enumerate(cols):
        defs.append(f'<marker id="ar-{key}-{j}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" fill="{c}"/></marker>')
    rts=''.join(o);o=[]
    # labels: regions first (big, letter-spaced), then points greedily
    boxes=[]
    def free(b):return all(b[2]<q[0] or b[0]>q[2] or b[3]<q[1] or b[1]>q[3] for q in boxes)
    lab=[]
    for t,(x,y),c in rl:
        fs=(24 if len(t)<=5 else 20)*S
        wdt=tw(t,fs)+len(t)*3;b=(x-wdt/2,y-fs*.8,x+wdt/2,y+fs*.3)
        boxes.append(b)
        lab.append(f'<text class="cm-rl" x="{x}" y="{y}" style="--c:{c};font-size:{fs:.0f}px">{E_(t)}</text>')
    for l in cfg.get('labels',[]):
        x,y=f(*l['ll']);t=re.sub(r'^\W+\s*','',l['n']) if not l['n'][0].isalnum() and ord(l['n'][0])<0x2e80 else l['n']
        lab.append(f'<text class="cm-sl" x="{x}" y="{y}">{E_(l["n"])}</text>')
    pts=sorted(cfg.get('points',[]),key=lambda p:-(3 if p['n']=='耶路撒冷' else 2 if p.get('k') else 0))
    dots=[]
    for p in pts:
        x,y=f(*p['ll'])
        if not(0<=x<=W and 0<=y<=H):continue
        kk=p.get('k') or p['n']=='耶路撒冷';c=p.get('c') or cfg.get('color','#ff6b6b')
        ic=p.get('i') or ICON.get(p['n'],'')
        t=E_(p['n']+('：'+re.sub('<[^>]+>','',p['d']) if p.get('d') else ''))
        dots.append(f'<g class="cm-pt{" k" if kk else ""}" style="--c:{c}"><title>{t}</title><circle cx="{x}" cy="{y}" r="{(7 if kk else 4.6)*S:.1f}"/>'+(f'<text class="cm-ic" x="{x}" y="{y-11*S:.1f}">{ic}</text>' if ic else '')+'</g>')
        fs=(17 if kk else 14)*S;wdt=tw(p['n'],fs)
        for dx,dy,anc in [(10*S,5*S,'start'),(-10*S,5*S,'end'),(0,(-14 if not ic else -30)*S,'middle'),(0,22*S,'middle')]:
            x0=x+dx if anc=='start' else x+dx-wdt if anc=='end' else x-wdt/2
            b=(x0-2,y+dy-fs*.85,x0+wdt+2,y+dy+3)
            if b[0]>=0 and b[2]<=W and b[1]>=0 and b[3]<=H and free(b):
                boxes.append(b);lab.append(f'<text class="cm-pl{" k" if kk else ""}" x="{x+dx}" y="{y+dy}" text-anchor="{anc}">{E_(p["n"])}</text>');break
    # compass + scale + cartouche
    kmpx=(e-w)*111.32*k/W;km=nice_km(kmpx,W);L_=km/kmpx
    deco=(f'<g class="cm-deco" transform="translate({W-58} 62)"><circle r="30"/><path d="M0,-34 L7,0 L0,34 L-7,0 Z"/><path class="n" d="M0,-34 L7,0 L-7,0 Z"/><text y="-40">N</text></g>'
          f'<g class="cm-scale" transform="translate(24 {H-26})"><path d="M0,0 h{L_:.1f} M0,-6 v12 M{L_/2:.1f},-4 v8 M{L_:.1f},-6 v12"/><text x="{L_/2:.1f}" y="-10">{km} 公里</text></g>')
    hdr=f'<desc>{E_(title)}——概念示意图（地形、疆界、路线均为大致示意）</desc>'
    svgm=(f'<svg class="cm" viewBox="0 0 {W} {H}"{f' style="--fs:{S}"' if S!=1 else ''} role="img" aria-label="{E_(title)} · 概念图" preserveAspectRatio="xMidYMid meet">{hdr}<defs>{"".join(defs)}</defs>'
          f'<rect class="cm-sea" width="{W}" height="{H}"/>{base}{regs}{rts}{"".join(dots)}{"".join(lab)}{deco}</svg>')
    svgo=f'<svg class="cmo" viewBox="0 0 {W} {H}" aria-hidden="true" preserveAspectRatio="xMidYMid meet">{"".join(ov)}</svg>' if ov else ''
    # legend
    lg=[]
    for r in cfg.get('regions',[]):
        if r.get('poly') or r.get('circle'):lg.append(f'<span class="lgr" style="--c:{r.get("c")}"><i></i>{E_(r["n"])}</span>')
    for r in cfg.get('routes',[]):lg.append(f'<span class="lgt{" d" if r.get("dash") else ""}" style="--c:{r.get("c")}"><i></i>{E_(r["n"])}</span>')
    used=sorted({ICON.get(p['n']) or p.get('i') for p in pts}-{None,''})
    IK={'🕍':'圣殿/圣城','👑':'京城','⚓':'港口','⛰️':'山','🏔️':'高山','🔥':'筑坛/敬拜','⛪':'教会','💧':'水泉/井','🌴':'绿洲','🐟':'湖边渔村','⭐':'降生','🏛️':'希腊罗马名城','🏯':'巴比伦','🌙':'月神城','⚔️':'战场','⛺':'帐棚/营地','🐂':'金牛犊','🍷':'神迹','🏠':'家乡','🧱':'为奴之城','🪨':'磐石','📜':'异象','🏙️':'都市','🏺':'商都','𓂀':'埃及古都'}
    lg+= [f'<span class="lgi">{i} {IK.get(i,"")}</span>' for i in used if i in IK]
    return (f'<figure class="cmap" data-k="{key}"><div class="cmw" style="aspect-ratio:{W}/{H}">{svgm}{svgo}</div>'
            f'<figcaption class="cmleg">{"".join(lg)}<span class="lgn">✍️ 概念示意 · 疆界与路线为近似</span></figcaption></figure>')
def block(key,cfg,title,height=None,cls=''):
    """概念图 / 实景地图 tabs. The real (Leaflet) map is only built on first switch."""
    st=f' style="height:{height}"' if height else ''
    return (f'<div class="mapx rv {cls}" data-k="{key}"><div class="mxt" role="tablist" aria-label="{E_(title)} 视图"><button type="button" role="tab" data-v="c" aria-selected="true">🎨 概念图</button><button type="button" role="tab" data-v="r" aria-selected="false" tabindex="-1">🛰️ 实景地图</button><span class="mxh">示意 · 地形 · 卫星 · 街道；在线底图不可达时自动退回离线底图</span></div>'
            f'<div class="mxc" role="tabpanel">{svg(key,cfg,title)}</div><div class="map" data-map="{key}" role="tabpanel" aria-label="{E_(title)} · 实景地图" hidden{st}><div class="lazyph" style="height:100%">🗺️ 实景地图加载中…</div></div></div>')
