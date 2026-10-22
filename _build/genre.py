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
