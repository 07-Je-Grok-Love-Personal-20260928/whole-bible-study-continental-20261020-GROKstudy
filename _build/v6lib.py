"""v6 shared helpers: gospel colours, static SVG charts (prerendered, CSS/one-shot animation), filter chips."""
from lib import *
G={'Mt':('马太','var(--g-mt)','👑'),'Mk':('马可','var(--g-mk)','🐂'),'Lk':('路加','var(--g-lk)','🧑'),'Jn':('约翰','var(--g-jn)','🦅')}
GO=['Mt','Mk','Lk','Jn']
def gtag(k,ref=''):
    n,c,i=G[k]
    return f'<span class="gt" style="--c:{c}" title="{n}福音">{i}{n}{(" "+E(ref)) if ref else ""}</span>'
def gset(refs):
    """refs: dict Mt->'3:1–12' ... -> membership key like 'MtMkLk' """
    return ''.join(k for k in GO if refs.get(k))
def gcells(refs):
    o=[]
    for k in GO:
        r=refs.get(k,'')
        o.append(f'<span class="gc" style="--c:{G[k][1]}">{E(r)}</span>' if r else '<span class="gc no">—</span>')
    return o
def gfilter(target,label='按福音筛选'):
    b=''.join(f'<button data-g="{k}" style="--c:{G[k][1]}">{G[k][2]} {G[k][0]}</button>' for k in GO)
    return f'<div class="gfilter" data-target="{target}"><b>🔎 {label}：</b>{b}<label><input type="checkbox" data-only> 只看“恰好这些”</label><button data-reset>全部</button><span class="gcount"></span></div>'
def vbars(rows,h=220,unit='',cap='',maxv=None,lab_every=1,rot=False,id_=''):
    """rows: (label,value,color,tooltip) -> responsive SVG column chart"""
    n=len(rows); W=max(600,n*28); L=46; B=h-(60 if rot else 34); T=14
    mx=maxv or max(v for _,v,_,_ in rows) or 1
    bw=(W-L-10)/n
    import math
    step=10**int(math.log10(mx)) if mx>0 else 1
    ticks=[t for t in range(0,int(mx)+1,max(1,step if mx/step<=6 else step*2))]
    g=''.join(f'<line x1="{L}" x2="{W-6}" y1="{B-(t/mx)*(B-T):.1f}" y2="{B-(t/mx)*(B-T):.1f}" class="gl"/><text x="{L-6}" y="{B-(t/mx)*(B-T)+4:.1f}" text-anchor="end" class="ax">{t}</text>' for t in ticks)
    bars=''
    for i,(lb,v,c,tt) in enumerate(rows):
        x=L+i*bw+bw*.14; hh=(v/mx)*(B-T); y=B-hh
        bars+=f'<g class="bh"><rect x="{x:.1f}" y="{y:.1f}" width="{bw*.72:.1f}" height="{max(hh,0.5):.1f}" rx="3" fill="{c}" style="--d:{i*12}ms"><title>{E(tt or f"{lb}：{v}{unit}")}</title></rect>'
        if i%lab_every==0:
            tx=x+bw*.36
            bars+=(f'<text x="{tx:.1f}" y="{B+12}" class="ax" text-anchor="end" transform="rotate(-55 {tx:.1f} {B+12})">{E(lb)}</text>' if rot else f'<text x="{tx:.1f}" y="{B+16}" class="ax" text-anchor="middle">{E(lb)}</text>')
        bars+='</g>'
    return f'<figure class="v6c rv"{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><div class="v6sc"><svg viewBox="0 0 {W} {h}" style="min-width:{min(W,1100)}px" role="img" aria-label="{E(cap)}">{g}{bars}</svg></div>{f"<figcaption class=srcline>{cap}</figcaption>" if cap else ""}</figure>'
def donut(rows,cap='',size=220):
    """rows: (label,value,color)"""
    import math
    tot=sum(v for _,v,_ in rows); r=80; C=2*math.pi*r; off=0; segs=''; leg=''
    for lb,v,c in rows:
        l=C*v/tot
        segs+=f'<circle r="{r}" cx="110" cy="110" fill="none" stroke="{c}" stroke-width="34" stroke-dasharray="{l:.2f} {C-l:.2f}" stroke-dashoffset="{-off:.2f}"><title>{E(lb)}：{v}（{v/tot*100:.1f}%）</title></circle>'
        off+=l; leg+=f'<span><i style="background:{c}"></i>{E(lb)} <b>{v}</b> · {v/tot*100:.0f}%</span>'
    return f'<figure class="donut rv"><svg viewBox="0 0 220 220" width="{size}" height="{size}" role="img" aria-label="{E(cap)}"><g transform="rotate(-90 110 110)">{segs}</g><text x="110" y="106" text-anchor="middle" class="dn">{tot}</text><text x="110" y="128" text-anchor="middle" class="ax">合计</text></svg><div class="dleg">{leg}</div>{f"<figcaption class=srcline>{cap}</figcaption>" if cap else ""}</figure>'
def stat(n,t,i,c='var(--gold)'):
    return f'<div class="card tile st6" style="--c:{c}"><div class="big">{i}</div><b class="num">{n}</b><span>{t}</span></div>'
def stats(items): return '<div class="grid g6 rv">'+''.join(stat(*x) for x in items)+'</div>'
def hero(chips,title,em_,lead):
    ch=''.join(f'<span class="chip{" g" if i==0 else ""}">{c}</span>' for i,c in enumerate(chips))
    return f'<section class="hero reveal"><div class="chips">{ch}</div><h1>{title}<em>{em_}</em></h1><p class="lead">{lead}</p></section>'
def cmp2(a,b,rows,ca='var(--sky)',cb='var(--gold)'):
    """two-column comparison table with coloured heads"""
    return f'<div class="tw cmp2"><table><thead><tr><th>对照点</th><th style="color:{ca}">{a}</th><th style="color:{cb}">{b}</th></tr></thead><tbody>'+''.join(f'<tr><td><b>{E(k)}</b></td><td>{rich(x,False)}</td><td>{rich(y,False)}</td></tr>' for k,x,y in rows)+'</tbody></table></div>'
