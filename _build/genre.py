"""v7: shared helpers for the genre-comparison pages (五经/历史/诗歌智慧/先知/书信)."""
from lib import *
from v6lib import vbars,donut,stats,hero,cmp2
from v5extra import hbar
from books import BOOKS,CATS
BK={b['id']:b for b in BOOKS}
BN={b['name']:b for b in BOOKS}
def R(t): return rich(t,False)
def htable(cols,rows,cls='hx',colors=None):
    """horizontal comparison: rows=books. First cell = book label (html). cells pass through rich()."""
    head=''.join(f'<th>{h}</th>' for h in cols)
    body=''
    for i,r in enumerate(rows):
        c=colors[i] if colors else 'var(--gold)'
        body+=f'<tr style="--c:{c}"><th scope="row">{r[0]}</th>'+''.join(f'<td>{R(x)}</td>' for x in r[1:])+'</tr>'
    return f'<div class="tw {cls}"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
def vmatrix(books,themes,colors=None):
    """vertical development: themes (rows) × books (columns)"""
    head='<th>主题 ↓ ／ 书卷 →</th>'+''.join(f'<th style="--c:{colors[i] if colors else "var(--gold)"}">{b}</th>' for i,b in enumerate(books))
    body=''.join(f'<tr><th scope="row">{t}</th>'+''.join(f'<td>{R(x)}</td>' for x in cells)+'</tr>' for t,cells in themes)
    return f'<div class="tw vmx"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
def flowsteps(items):
    """items: (emoji,title,desc,color) -> animated arrow chain"""
    return '<div class="fstep rv">'+''.join(f'<div style="--c:{c};--i:{k}"><span class="e">{e}</span><b>{t}</b><span>{R(d)}</span></div>' for k,(e,t,d,c) in enumerate(items))+'</div>'
def kbox(title,items,badge='必背'):
    """key-point box with numbered points + must-memorize badge"""
    return f'<div class="kbox rv"><div class="kbh"><b>🔑 {title}</b>{f"<span class=mbadge>★ {badge}</span>" if badge else ""}</div><ol>'+''.join(f'<li>{R(x)}</li>' for x in items)+'</ol></div>'
def mnem(items):
    """mnemonics: (label, formula, explanation)"""
    return '<div class="mnx rv">'+''.join(f'<div class="mni"><span class="mbadge">🧠 {E(a)}</span><b class="mnf">{E(f)}</b><span>{R(x)}</span></div>' for a,f,x in items)+'</div>'
def cards(items,id_):
    return f'<div class="grid g3 fcs" id="{id_}">'+''.join(f'<div class="fc"><div class="in"><div class="f">{E(a)}</div><div class="b">{E(b)}</div></div></div>' for a,b in items)+f'</div><p class="srcline">👆 点击卡片翻面；<button class="btn" data-shuffle="#{id_}">🔀 洗牌</button></p>'
def chbars(ids,cap):
    return vbars([(BK[i]['name'][:3] if len(ids)<=12 else BK[i]['name'][:2],BK[i]['ch'],CATS[BK[i]['cat']][1],f'{BK[i]["name"]}：{BK[i]["ch"]} 章') for i in ids],h=220,cap=cap,rot=len(ids)>8)
def booklink(i,label=None):
    b=BK[i]; return f'<a href="{"ot" if b["n"]<=39 else "nt"}.html#b-{i}">{label or b["name"]}</a>'
def quotes(spec):
    return '<div class="confx">'+confref(spec)+'</div>'
def chips(items):
    return '<div class="chips">'+''.join(f'<span class="chip" style="--c:{c}">{t}</span>' for t,c in items)+'</div>'
def grid(htmls,n=3): return f'<div class="grid g{n}">'+''.join(htmls)+'</div>'
def card(title,body,c='var(--gold)'):
    return f'<div class="card gcard rv" style="--c:{c}"><h4>{title}</h4>{R(body) if not body.startswith("<") else body}</div>'
def rtable(head,rows,cls=''): return table(head,[[R(x) if isinstance(x,str) and not x.startswith('<') else x for x in r] for r in rows],cls)
def spans(rows,y0,y1,ticks,cap='',bands=None,rowh=30,lw=150,W=1100,id_=''):
    """BC/AD time-span chart. rows: (label,start,end,color,tip). years as signed ints (BC negative).
    bands: (label,start,end,color) background eras."""
    n=len(rows); T=50 if bands else 34; H=T+n*rowh+30
    X=lambda y: lw+(y-y0)/(y1-y0)*(W-lw-20)
    s=f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{E(cap)}">'
    for k,(lb,a,b,col) in enumerate(bands or []):
        s+=f'<rect x="{X(a):.1f}" y="{T-6}" width="{X(b)-X(a):.1f}" height="{H-T-20}" fill="{col}" opacity=".10"/><text x="{(X(a)+X(b))/2:.1f}" y="{T-12-(k%2)*15}" text-anchor="middle" class="ax" font-weight="800" fill="{col}">{E(lb)}</text>'
    for t in ticks:
        s+=f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{T-4}" y2="{H-22}" class="gl"/><text x="{X(t):.1f}" y="{H-6}" text-anchor="middle" class="ax">{abs(t)}{" BC" if t<0 else (" AD" if t>0 else "")}</text>'
    for i,(lb,a,b,col,tip) in enumerate(rows):
        y=T+i*rowh; w=max(X(b)-X(a),5)
        s+=f'<g class="spr" style="--d:{i*40}ms"><text x="{lw-8}" y="{y+rowh*.62:.1f}" text-anchor="end" class="spl">{E(lb)}</text><rect x="{X(a):.1f}" y="{y+5}" width="{w:.1f}" height="{rowh-10}" rx="5" fill="{col}" class="spb"><title>{E(lb)}：{E(tip)}</title></rect>'
        if w>90: s+=f'<text x="{X(a)+6:.1f}" y="{y+rowh*.62:.1f}" class="spt">{E(tip)}</text>'
        elif (b-y0)/(y1-y0)>.86: s+=f'<text x="{X(a)-6:.1f}" y="{y+rowh*.62:.1f}" text-anchor="end" class="spt2">{E(tip)}</text>'
        else: s+=f'<text x="{X(b)+6:.1f}" y="{y+rowh*.62:.1f}" class="spt2">{E(tip)}</text>'
        s+='</g>'
    s+='</svg>'
    return f'<figure class="v6c spanc rv"{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><div class="v6sc">{s.replace("<svg ",f"<svg style=min-width:{W-200}px ",1)}</div>{f"<figcaption class=srcline>{cap}</figcaption>" if cap else ""}</figure>'
