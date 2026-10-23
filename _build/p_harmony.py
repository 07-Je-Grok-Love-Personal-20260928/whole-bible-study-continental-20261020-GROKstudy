"""v8: 四福音合参（Diatessaron 式编辑合参）。经文：新标点和合本（简体），eBible.org cmn-cu89s（标注 Public Domain）。"""
import json,re,os
from lib import *
from v6lib import G
from v5extra import hbar
D=json.load(open(os.path.join(os.path.dirname(__file__),'data','cuv_gospels_acts.json'),encoding='utf-8'))
T=D['text']
AB={'M':('Mt','MAT','太'),'K':('Mk','MAR','可'),'L':('Lk','LUK','路'),'J':('Jn','JOH','约')}
COL=['Mt','Mk','Lk','Jn']; LET=dict(zip(COL,'MKLJ'))
def verses(bk,ref):
    """'26:1-5,14-16' / '7:53-8:11' / '8:18,23-27' -> [(c,v),...] (verified against the CUV file)"""
    out=[];ch=None
    for part in ref.split(','):
        part=part.strip()
        a,_,b=part.partition('-')
        if ':' in a: ch,va=a.split(':')
        else: va=a
        if b:
            if ':' in b: c2,vb=b.split(':')
            else: c2,vb=ch,b
        else: c2,vb=ch,va
        c,v,ce,ve=int(ch),int(va),int(c2),int(vb)
        mx=lambda c_:max(int(x) for x in T[bk][str(c_)])
        if v>mx(c) or ve>mx(ce): raise SystemExit(f'harmony: bad ref {bk} {ref}')
        while (c,v)<=(ce,ve):
            if str(v) in T[bk][str(c)]: out.append((c,v))   # merged/omitted verses (e.g. 路1:2, 太18:11) are skipped
            v+=1
            if v>mx(c): c+=1;v=1
        ch=c2
    return out
def txt(bk,ref):
    vs=verses(bk,ref);o=[];last=None
    for c,v in vs:
        if last and (c!=last[0] or v!=last[1]+1): o.append('<span class="gap">……</span>')
        t=E(T[bk][str(c)][str(v)]).replace('[','<i class="ins">').replace(']','</i>')
        o.append(f'<span class="vv"><sup>{c}:{v}</sup>{t}</span>');last=(c,v)
    return ''.join(o),len(vs)
def load():
    parts=[];cur=None
    for l in open(os.path.join(os.path.dirname(__file__),'data','harmony.txt'),encoding='utf-8'):
        l=l.rstrip('\n')
        if not l or l.startswith('# '): continue
        if l.startswith('## '):
            n,t,dt,ic=l[3:].split('|'); cur={'n':int(n),'t':t,'dt':dt,'ic':ic,'s':[]}; parts.append(cur); continue
        f=l.split('|'); refs=dict(zip(COL,f[1:5]))
        cur['s'].append({'t':f[0],'r':{k:v for k,v in refs.items() if v},'p':f[5],'u':[x.strip() for x in f[6].split(';') if x.strip()]})
    return parts
P=load(); N=sum(len(p['s']) for p in P)
def chip(g,ref,prim=False):
    nm,col,ic=G[g]; return f'<span class="hg{" pr" if prim else ""}" style="--c:{col}">{ic} {AB[LET[g]][2]}{E(ref)}</span>'
def coverage():
    """4-row SVG strip: one column per section, filled where that gospel has the pericope"""
    W=N*6; o=''
    for r,g in enumerate(COL):
        d=''.join(f'M{i*6},{r*16}h5v12h-5z' for i,s in enumerate(x for p in P for x in p['s']) if g in s['r'])
        o+=f'<path d="{d}" fill="{G[g][1]}"/><text x="-6" y="{r*16+10}" text-anchor="end" font-size="11" fill="currentColor">{G[g][2]}{G[g][0]}</text>'
    k=0;mk=''
    for p in P:
        mk+=f'<line x1="{k*6-0.5}" x2="{k*6-0.5}" y1="-4" y2="66" stroke="currentColor" stroke-opacity=".35"/><text x="{k*6+2}" y="76" font-size="9.5" fill="currentColor" opacity=".8">{p["n"]}</text>';k+=len(p['s'])
    return f'<div class="tw cov"><svg viewBox="-62 -6 {W+66} 86" style="min-width:760px;width:100%;color:var(--ink2)" role="img" aria-label="四福音段落覆盖图">{o}{mk}</svg></div>'
def build():
    c=[f'''<section class="hero reveal"><div class="chips"><span class="chip g">📖 四福音合参</span><span class="chip">{N} 段 · {len(P)} 个阶段</span><span class="chip">和合本（新标点·简体）</span><span class="chip">编辑合参 · 依 Robertson / Aland 次序</span></div>
<h1>一位基督，<em>四卷见证，合成一个叙事</em></h1><p class="lead">像二世纪他提安的 <b class="k">Diatessaron</b> 那样把四福音“合成一卷”来读：每段以<b class="k">一卷为主文</b>，列出其余福音书的<mark class="hy">平行经文</mark>，并把它们<mark class="hy">独有的细节</mark>并入、逐条标明出处。点开段落才加载经文（按需渲染）。</p></section>''']
    c.append(h2('hm-how','🧭','怎样使用这份合参'))
    c.append('<div class="grid g3">'+co('info','<p>'+rich('**编辑性合参**：段落划分与先后次序是==编者的判断==，大体依 A. T. Robertson《四福音合参》与 K. Aland《Synopsis》的通行次序；圣经本身没有给出逐日的“总时间表”。',False)+'</p>','这是什么')+co('hardc','<p>'+rich('**年代说明**：采用“约翰福音记三至四个逾越节”的通行框架（约2:13；5:1?；6:4；11:55），公开事工约三年半；受难年取 ~~主后30年~~（亦有主张33年）。各阶段年代均为==约数==。',False)+'</p>','年代与次序')+co('core','<p>'+rich('四福音不是“矛盾的四份口供”，而是**圣灵默示的四重见证**（比利时信条第3–5条）：同一事件，各按写作目的取材、排列。合参的目的是==看见更完整的基督==，不是取代四卷各自的信息。',False)+'</p>','认信立场')+'</div>')
    c.append('<div class="legend">'+''.join(f'<span style="--c:{G[g][1]}"><i></i>{G[g][2]} {G[g][0]}福音</span>' for g in COL)+'<span style="--c:var(--gold)"><i></i>★ 主文</span><span style="--c:var(--mut)"><i></i>➕ 他卷独有细节</span></div>')
    c.append(h3('hm-cov','📊 覆盖图：每一列是一段，有色＝该卷记载'))
    c.append(coverage())
    cnt={g:sum(1 for p in P for s in p['s'] if g in s['r']) for g in COL}
    only={g:sum(1 for p in P for s in p['s'] if list(s['r'])==[g]) for g in COL}
    c.append('<div class="grid g2">'+'<div>'+hbar([(f'{G[g][2]} {G[g][0]}',cnt[g],G[g][1]) for g in COL],' 段',f'在本合参 {N} 段中各卷出现的段数。')+'</div><div>'+hbar([(f'{G[g][2]} 仅{G[g][0]}',only[g],G[g][1]) for g in COL],' 段','只有一卷记载的段落数：约翰与路加的“独家材料”最多，马可几乎都有平行。')+'</div></div>')
    c.append(h3('hm-parts','🗺️ 十三个阶段一览'))
    c.append(table(['#','阶段','约年代','段数','主要福音'],[[f'<b>{p["n"]}</b>',f'<a href="#hp-{p["n"]}">{p["ic"]} {E(p["t"])}</a>',E(p['dt']),str(len(p['s'])),' '.join(chip(g,'') for g in COL if sum(1 for s in p['s'] if g in s['r'])>=len(p['s'])/2)] for p in P]))
    c.append('<div class="hfil" id="hfil"><b>筛选：</b><button class="on" data-g="all">全部</button>'+''.join(f'<button data-g="{g}" style="--c:{G[g][1]}">{G[g][2]} 含{G[g][0]}</button>' for g in COL)+'<button data-g="one">⭐ 仅一卷记载</button><button data-g="four">🔷 四卷皆有</button><input id="hq" placeholder="🔍 搜索段落标题或经文出处…" aria-label="搜索合参"><button data-x="open">全部展开</button><button data-x="close">全部收起</button></div>')
    k=0
    for p in P:
        c.append(h2(f'hp-{p["n"]}',p['ic'],f'{E(p["t"])}<small class="hdt">{E(p["dt"])}</small>',toc=p['t']))
        for s in p['s']:
            k+=1; pg=[g for g in COL if LET[g]==s['p']][0]; pref=s['r'][pg]
            body,nv=txt(AB[s['p']][1],pref)
            par=''.join(f'<li>{chip(g,s["r"][g])}<span>平行</span></li>' for g in COL if g in s['r'] and g!=pg)
            un=''
            for u in s['u']:
                L_,ref=u.split(' ',1); g=AB[L_][0]; t_,n_=txt(AB[L_][1],ref)
                un+=f'<div class="hu" style="--c:{G[g][1]}"><b>➕ {G[g][2]} {G[g][0]}独有/补充 · {AB[L_][2]}{E(ref)}</b><p>{t_}</p></div>'
            gs=''.join(s['r'].keys()); flag='one' if len(s['r'])==1 else ('four' if len(s['r'])==4 else '')
            chips=''.join(chip(g,s['r'][g],g==pg) for g in COL if g in s['r'])
            c.append(f'''<details class="hs" data-g="{gs}" data-f="{flag}"><summary><h3 class="h" id="hm-{k}" data-num="§{k}" data-toc="{E(s['t'])}">{E(s['t'])}</h3><span class="hch">{chips}</span></summary><div class="hb"><template><div class="hmain" style="--c:{G[pg][1]}"><b class="hml">★ 主文：{G[pg][2]} {G[pg][0]}福音 {AB[s['p']][2]}{E(pref)} · {nv} 节</b><p class="ht">{body}</p></div>{f'<div class="hus">{un}</div>' if un else ''}{f'<ul class="hpar"><b>📎 平行经文（同一事件，按各卷视角）</b>{par}</ul>' if par else ''}</template></div></details>''')
    c.append(h2('hm-src','📚','经文来源与编辑说明'))
    c.append('<div class="grid g2">'+co('info','<p>'+rich('**经文**：《新标点和合本》简体（Chinese Union Version, simplified），取自 ==eBible.org 的 cmn-cu89s VPL 文件==（eBible.org 标注为 *Public Domain*；文件日期 2021-10-15；2026-10-23 下载）。方括号中的字在原文中为译者补字，此处以浅色斜体显示。**核对**：与另一独立来源（scrollmapper/bible_databases 的 ChiUn 繁体和合本，经 OpenCC 繁→简转换）逐节比对四福音 3768 节，平均字面相似度 98.6%，97% 的经节相似度 > 0.9（差异主要是繁简用字与标点）。',False)+'</p>','和合本来源')+co('trap','<p>'+rich('**经文异文**：约7:53–8:11（行淫时被拿的妇人）与可16:9–20（马可长结尾）不见于最早的几份抄本，和合本以括号或注释标明；本合参照和合本列出，但==不以它们为任何教义的唯一根据==。**次序**：如洁净圣殿（约2 与 符类福音受难周）本合参按两次事件处理；登山宝训与平原宝训（路6）合并呈现——这些都是编辑判断。',False)+'</p>','编辑判断')+'</div>')
    js='''<script>(()=>{const H=d=>{const t=d.querySelector(':scope>.hb>template');if(t)t.replaceWith(t.content)};
document.addEventListener('toggle',e=>{const d=e.target;if(d.classList&&d.classList.contains('hs')&&d.open)H(d)},true);
const op=()=>{const id=decodeURIComponent(location.hash.slice(1));const el=id&&document.getElementById(id);const d=el&&el.closest('details.hs');if(d&&!d.open)d.open=true};addEventListener('hashchange',op);op();
const f=document.getElementById('hfil');if(!f)return;const S=[...document.querySelectorAll('details.hs')];let g='all';const q=f.querySelector('#hq');
const ap=()=>{const v=(q.value||'').trim();S.forEach(d=>{const ok=(g==='all'||(g==='one'||g==='four'?d.dataset.f===g:d.dataset.g.includes(g)))&&(!v||d.querySelector('summary').textContent.includes(v));d.classList.toggle('hidden',!ok)})};
f.querySelectorAll('button[data-g]').forEach(b=>b.onclick=()=>{f.querySelectorAll('button[data-g]').forEach(x=>x.classList.remove('on'));b.classList.add('on');g=b.dataset.g;ap()});
let tq;q.oninput=()=>{clearTimeout(tq);tq=setTimeout(ap,150)};
f.querySelectorAll('button[data-x]').forEach(b=>b.onclick=()=>{const o=b.dataset.x==='open';S.forEach(d=>{if(!d.classList.contains('hidden')){if(o)H(d);d.open=o}})});})()</script>'''
    return page('harmony.html','四福音合参',''.join(c),scripts=js)
