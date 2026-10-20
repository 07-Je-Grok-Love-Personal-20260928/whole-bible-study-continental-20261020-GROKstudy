import re
from lib import *
CATS={'law':('律法书','var(--law)','⚖️'),'hist':('历史书','var(--hist)','🏛️'),'poet':('诗歌智慧书','var(--poet)','🎼'),'majp':('大先知书','var(--majp)','🔥'),'minp':('小先知书','var(--minp)','📯'),'gosp':('福音书','var(--gosp)','✝️'),'acts':('教会历史','var(--acts)','🕊️'),'paul':('保罗书信','var(--paul)','✉️'),'gen':('普通书信','var(--gen)','📨'),'rev':('预言书','var(--rev)','👑')}
def parse(fn):
    out=[]
    for blk in open(fn).read().split('@@')[1:]:
        lines=blk.strip().split('\n'); h=lines[0].split('|')
        b={'n':int(h[0]),'id':h[1],'name':h[2],'en':h[3],'cat':h[4],'ch':int(h[5]),'kv':[]}
        for ln in lines[1:]:
            if ':' not in ln: continue
            k,v=ln.split(':',1); v=v.strip()
            if k=='kv': t,r=v.split('##'); b['kv'].append((t.strip(),r.strip()))
            else: b[k]=v
        for k in ['one','au','dt','bg','why','ol','core','xc','cov','hard','app','mn','cf']: assert k in b,(b['name'],k)
        out.append(b)
    return out
import os
_D=os.path.dirname(os.path.abspath(__file__))
BOOKS=parse(os.path.join(_D,'books_ot1.txt'))+parse(os.path.join(_D,'books_ot2.txt'))+parse(os.path.join(_D,'books_nt.txt'))
assert [b['n'] for b in BOOKS]==list(range(1,67)),[b['n'] for b in BOOKS]
V2={}
for _l in open(os.path.join(_D,'books_v2.txt')):
    _id,_r=_l.rstrip('\n').split('|',1); _k,_t=_r.split('|trap:'); V2[_id]={'key':[x.strip() for x in _k.replace('key:','',1).split(' | ')],'trap':_t.strip()}
def qmark(t,auto=True): return rich(t,auto)
PAL=['#ffcb5c','#ff6fa5','#b78cff','#5cc8ff','#3ee0a1','#ff9f43','#2dd4bf','#f472b6']
RNG=re.compile(r'^\s*(\d+)(?::(\d+))?(?:\s*[–-]\s*(\d+)(?::(\d+))?)?\s*(.*)$')
def sbar(b):
    items=[x.strip() for x in b['ol'].split('|')]; segs=[]
    for it in items:
        m=RNG.match(re.sub(r'^卷\S+\s+','',it))
        if not m: return ''
        c1=int(m.group(1)); v1=int(m.group(2) or 1); e=m.group(3); segs.append([c1+(v1-1)/60,int(e) if e else c1,m.group(5)])
    verse_mode=b['ch']==1
    tot=(max(s_[1] for s_ in segs) if verse_mode else b['ch'])+1
    if not verse_mode and segs[0][0]>1.5: return ''
    w=[]
    for i,sg in enumerate(segs):
        nx=segs[i+1][0] if i+1<len(segs) else tot
        w.append(max(nx-sg[0],.35))
    T=sum(w); sp=''; lg=''
    for i,(sg,ww) in enumerate(zip(segs,w)):
        col=PAL[i%len(PAL)]; lab=re.split(r'[：:（(，,、]',sg[2])[0][:10]
        rng=' '.join(items[i].split(' ')[:2]) if items[i].startswith('卷') else items[i].split(' ')[0]
        sp+=f'<span style="flex:{ww/T*100:.2f} 1 0;background:{col};transition-delay:{i*.08:.2f}s" title="{E(items[i])}">{E(lab) if ww/T>.1 else ""}</span>'
        lg+=f'<span><i style="background:{col}"></i>{E(rng)} {E(lab)}</span>'
    return f'<div class="sbar" role="img" aria-label="{E(b["name"])}结构图">{sp}</div><div class="sleg">{lg}</div>'
def card(b):
    cl,col,ic=CATS[b['cat']]; x=V2[b['id']]; i=b['id']
    ol=''.join(f'<li>{qmark(re.sub(r"^(\S+)",r"**\1**",x_.strip(),count=1),False)}</li>' for x_ in b['ol'].split('|'))
    app=''.join(f'<li>{qmark(x_.strip())}</li>' for x_ in b['app'].split('|'))
    kv=''.join(verse(E(t),E(r)) for t,r in b['kv'])
    cf=b['cf'].split(',')
    chips=''.join(f'<span class="tag" style="color:var(--vio)">{conflabel(s_)}</span>' for s_ in cf)
    test='旧约' if b['n']<=39 else '新约'
    one=re.sub(r'^([^：]{2,14})：',r'**\1**：',b['one'],count=1)
    core=re.sub(r'(“[^”{}]{4,60}”)',r'==\1==',b['core'],count=1)
    keys=''.join(f'<li>{qmark(k,False)}</li>' for k in x['key'])
    H=lambda k,t:f'<h4 class="h" id="b-{i}-{k}">{t}</h4>'
    return f'''<article class="bk rv" id="bk-{i}" data-cat="{b['cat']}" style="--c:{col}">
<header><div class="no">{b['n']}</div><div style="min-width:0;flex:1"><h3 class="h" id="b-{i}" data-num="{b['n']}" data-toc="{E(b['name'])}">{ic} {b['name']}<small>{b['en']} · {b['ch']}章</small></h3>
<div class="chips" style="margin-top:6px"><span class="chip" style="border-color:{col};color:{col}">{cl}</span><span class="chip">{test}第{b['n'] if b['n']<=39 else b['n']-39}卷</span><span class="chip">✍️ {E(b['au'][:22])}</span><span class="chip">🕰️ {E(b['dt'].split('；')[0][:30])}</span></div></div>
<div class="one">💡 {qmark(one)}</div></header>
<div class="body">
<div class="bgrid btop">
<div class="box span2">{H('ol','🧩 结构大纲 · 结构图')}{sbar(b)}<ol class="outline">{ol}</ol></div>
<div class="box">{co('core','<ol>'+keys+'</ol>','核心三要点')}{co('mnc','<p class="mn">'+E(b['mn'])+'</p>','记忆口诀')}<div class="srcline">✍️ 作者：{E(b['au'])}<br>🕰️ 日期：{qmark(b['dt'])}</div></div>
</div>
<div class="bgrid">
<div class="box">{H('bg','🏺 真实背景 · 受众')}<p>{qmark(b['bg'])}</p></div>
<div class="box">{H('why','🎯 为什么写')}<p>{qmark(b['why'])}</p></div>
<div class="box">{H('core','💎 核心信息 · 基督中心')}<p>{qmark(core)}</p>{co('xc','<p>'+qmark(b['xc'])+'</p>','基督')}</div>
<div class="box">{H('cov','🤝 圣约位置')}<p>{qmark(b['cov'])}</p></div>
<div class="box">{H('kv','📖 关键经文')}{kv}</div>
<div class="box">{H('hard','⚠️ 难点 · 易错')}{co('hardc','<p>'+qmark(b['hard'])+'</p>','难点辨析')}{co('trap','<p>'+qmark(x['trap'],False)+'</p>','易错点')}</div>
<div class="box">{H('app','🌱 应用')}{co('app','<ul>'+app+'</ul>','教牧应用')}</div>
</div>
<details class="dx" style="margin-top:10px"><summary>📚 认信连接（三项联合信条原文，逐字引自 ccifellowship.org）{chips}</summary><div class="in">{confref(b['cf'])}</div></details>
</div></article>'''
def canon_grid(sel=None):
    out=[]
    for b in BOOKS:
        if sel and not sel(b): continue
        cl,col,ic=CATS[b['cat']]; pg='ot.html' if b['n']<=39 else 'nt.html'
        out.append(f'<a href="{pg}#b-{b["id"]}" style="--c:{col}" title="{b["name"]}：{E(b["one"][:40])}">{b["name"].replace("书","") if len(b["name"])>4 else b["name"]}<small>{b["ch"]}章</small></a>')
    return '<div class="canon">'+''.join(out)+'</div>'
def legend(keys):
    return '<div class="legend">'+''.join(f'<span style="--c:{CATS[k][1]}"><i></i>{CATS[k][2]} {CATS[k][0]}</span>' for k in keys)+'</div>'
