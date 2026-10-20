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
def strip(t): return re.sub(r'\^\d+','',t)
SRC={}
for n,(q,ld) in HCQ.items(): SRC['HC%d'%n]=(strip(q['answer']),ld['url'],'海德堡要理问答第%d问'%n)
for n,a in BCA.items(): SRC['BC%d'%n]=(strip(a['text']),a['url'],'比利时信条第%d条'%n)
SRC['AP']=(CR['apostles']['text'],CR['apostles']['url'],'使徒信经');SRC['NI']=(CR['nicene']['text'],CR['nicene']['url'],'尼西亚信经');SRC['AT']=(CR['athanasian']['text'],CR['athanasian']['url'],'亚他那修信经')
QUOTES=[]
def qmark(t):
    def rep(m):
        k,txt=m.group(1),m.group(2); src,url,lab=SRC[k]
        if txt not in src: raise SystemExit('QUOTE NOT VERBATIM: %s %s'%(k,txt))
        QUOTES.append((k,txt))
        return f'“<span class="key">{E(txt)}</span>”<a class="tag" style="color:var(--vio)" href="{url}" target="_blank" rel="noopener">{lab}·逐字</a>'
    return re.sub(r'\{\{(\w+)\|(.+?)\}\}',rep,E(t).replace('&#x27;',"'")) if '{{' in t else E(t)
def card(b):
    cl,col,ic=CATS[b['cat']]
    ol=''.join(f'<li>{E(x.strip())}</li>' for x in b['ol'].split('|'))
    app=''.join(f'<li>{qmark(x.strip())}</li>' for x in b['app'].split('|'))
    kv=''.join(verse(E(t),E(r)) for t,r in b['kv'])
    cf=b['cf'].split(',')
    chips=''.join(f'<span class="tag" style="color:var(--vio)">{conflabel(s)}</span>' for s in cf)
    test='旧约' if b['n']<=39 else '新约'
    return f'''<article class="bk reveal" id="b-{b['id']}" data-cat="{b['cat']}" style="--c:{col}">
<header><div class="no">{b['n']}</div><div style="min-width:0;flex:1"><h3 data-toc="{b['n']}. {b['name']}">{ic} {b['name']}<small>{b['en']} · {b['ch']}章</small></h3>
<div class="chips" style="margin-top:6px"><span class="chip" style="border-color:{col};color:{col}">{cl}</span><span class="chip">{test}第{b['n'] if b['n']<=39 else b['n']-39}卷</span><span class="chip">🕰️ {E(b['dt'].split('；')[0][:30])}</span></div></div>
<div class="one">💡 {qmark(b['one'])}</div></header>
<div class="body">
<div class="facts"><div class="fact"><b>✍️ 作者</b>{E(b['au'])}</div><div class="fact"><b>🕰️ 日期</b>{E(b['dt'])}</div><div class="fact"><b>🧠 记忆口诀</b><span class="mn">{E(b['mn'])}</span></div></div>
<div class="bgrid">
<div class="box"><h5>🏺 真实背景 · 受众 <span class="tag">历史视角</span></h5><p>{qmark(b['bg'])}</p></div>
<div class="box"><h5>🎯 为什么写 <span class="tag">写作目的</span></h5><p>{qmark(b['why'])}</p></div>
<div class="box"><h5>🧩 写了什么 · 结构大纲 <span class="tag">文学视角</span></h5><ol class="outline">{ol}</ol></div>
<div class="box"><h5>💎 核心信息 <span class="tag">神学视角</span></h5><p>{qmark(b['core'])}</p><h5 style="margin-top:10px">✝️ 基督中心</h5><p>{qmark(b['xc'])}</p></div>
<div class="box"><h5>🤝 圣约位置 <span class="tag">圣约神学</span></h5><p>{qmark(b['cov'])}</p></div>
<div class="box"><h5>📖 关键经文</h5>{kv}</div>
<div class="box" style="border-color:rgba(255,107,107,.45);background:rgba(255,107,107,.07)"><h5 style="color:var(--red)">⚠️ 难点辨析 <span class="tag">正统立场</span></h5><p>{qmark(b['hard'])}</p></div>
<div class="box" style="border-color:rgba(62,224,161,.45);background:rgba(62,224,161,.06)"><h5 style="color:var(--emer)">🌱 什么应用 <span class="tag">教牧视角</span></h5><ul>{app}</ul></div>
</div>
<details class="dx" style="margin-top:12px"><summary>📚 认信连接（三项联合信条原文，逐字引自 ccifellowship.org）{chips}</summary><div class="in">{confref(b['cf'])}</div></details>
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
