# 跨卷连接数据集（编辑精选，非穷尽）+ 弧线网络图
import os,collections
from lib import *
from books import BOOKS,CATS
_D=os.path.dirname(os.path.abspath(__file__))
AB='创 出 利 民 申 书 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 诗 箴 传 歌 赛 耶 哀 结 但 何 珥 摩 俄 拿 弥 鸿 哈 番 该 亚 玛 太 可 路 约 徒 罗 林前 林后 加 弗 腓 西 帖前 帖后 提前 提后 多 门 来 雅 彼前 彼后 约壹 约贰 约叁 犹 启'.split()
BI={b['id']:k for k,b in enumerate(BOOKS)}; BN={b['id']:b['name'] for b in BOOKS}
KIND={'Q':('新约引用旧约','var(--gold)','📜'),'F':('应许→应验','var(--emer)','🎯'),'T':('预表','var(--vio)','🔦'),'P':('平行/姊妹卷','var(--sky)','🪞'),'A':('主题呼应/暗引','var(--rose)','🔗')}
XR=[]
for l in open(os.path.join(_D,'data','xref.txt'),encoding='utf-8'):
    if not l.strip() or l.startswith('#'): continue
    a,b,k,r,n=l.rstrip('\n').split('|'); XR.append((a,b,k,r,n))
def rel(bid):
    return [(b if a==bid else a,k,r,n) for a,b,k,r,n in XR if bid in (a,b)]
def chips(bid,href=lambda o:f'#b-{o}'):
    out=''
    for o,k,r,n in sorted(rel(bid),key=lambda x:BI[x[0]]):
        nm,col,ic=KIND[k]
        out+=f'<a class="xchip" href="{href(o)}" style="--c:{col}" title="{E(nm)}：{E(r)}"><b>{ic} {E(BN[o])}</b><span>{E(r)} · {E(n)}</span></a>'
    return f'<div class="xchips">{out}</div>' if out else ''
def arcs():
    S=20;X=lambda i:16+i*S;Y=300;W=X(65)+16
    p=''
    for j,(a,b,k,r,n) in enumerate(sorted(XR,key=lambda x:-(BI[x[1]]-BI[x[0]]))):
        xa,xb=X(BI[a]),X(BI[b]);d=xb-xa;h=min(560,24+d*0.86)
        p+=f'<path class="xa k{k}" data-a="{a}" data-b="{b}" d="M{xa},{Y}Q{(xa+xb)/2},{Y-h} {xb},{Y}" stroke="{KIND[k][1]}"><title>{E(BN[a])} → {E(BN[b])}｜{KIND[k][0]}｜{E(r)}：{E(n)}</title></path>'
    deg=collections.Counter(x for t in XR for x in t[:2])
    g=''
    for i,bk in enumerate(BOOKS):
        col=CATS[bk['cat']][1]; x=X(i); lab=''.join(f'<tspan x="{x}" dy="{0 if q==0 else 12}">{ch}</tspan>' for q,ch in enumerate(AB[i]))
        g+=f'<g class="xb" data-b="{bk["id"]}" tabindex="0" role="button" aria-label="{E(bk["name"])}：{deg[bk["id"]]} 条连接"><circle cx="{x}" cy="{Y}" r="{3+min(deg[bk["id"]],14)*0.32:.1f}" fill="{col}"/><text x="{x}" y="{Y+20}" text-anchor="middle">{lab}</text></g>'
    sep=f'<line x1="{(X(38)+X(39))/2}" x2="{(X(38)+X(39))/2}" y1="{Y-12}" y2="{Y+46}" class="xsep"/><text x="{X(38)-4}" y="{Y+58}" text-anchor="end" class="xtl">← 旧约 39</text><text x="{X(39)+4}" y="{Y+58}" class="xtl">新约 27 →</text>'
    return f'<div class="tw xarc"><svg viewBox="0 {Y-300} {W} 370" style="min-width:900px;width:100%" role="img" aria-label="66 卷跨卷连接弧线图">{p}{sep}{g}</svg></div>'
def section():
    """compare.html 的跨卷网络段落（返回 HTML 片段列表）"""
    from v5extra import hbar
    c=[]
    cnt=collections.Counter(k for *_,k,_,_ in [(a,b,k,r,n) for a,b,k,r,n in XR])
    c.append(h2('xref','🕸️','跨卷连接网络：66 卷怎样彼此解释'))
    c.append(h3('xref-arc',f'弧线图：{len(XR)} 条精选连接'))
    c.append('<div class="xfil" role="group" aria-label="连接类型"><button class="on" data-xk="all">全部</button>'+''.join(f'<button data-xk="{k}" style="--c:{v[1]}">{v[2]} {v[0]} <small>{cnt[k]}</small></button>' for k,v in KIND.items())+'</div>')
    c.append(arcs())
    c.append(f'<div class="xinfo" id="xinfo" aria-live="polite"><b>👆 点击或聚焦任一书卷</b>，只显示它的连接并列出出处。弧越高＝两卷在正典中相距越远；圆点越大＝连接越多。</div>')
    c.append(co('info','<p>'+rich(f'**数据说明（诚实标注）**：这是本站==编辑精选的 {len(XR)} 条代表性连接==，不是穷尽统计。“新约引用旧约”只收明确引文（多据新约经文自己的引用语如“经上记着说”），“预表”“主题呼应”属解经判断。学者估计新约直接引用旧约约 250–350 处（视引文标准而定），暗引更多。',False)+'</p>','数据来源'))
    deg=collections.Counter(x for t in XR for x in t[:2])
    c.append(h3('xref-top','谁被连得最多？'))
    c.append(hbar([(f'{BN[b]}',v,CATS[BOOKS[BI[b]]['cat']][1]) for b,v in deg.most_common(12)],' 条','按本数据集统计。诗篇、以赛亚、创世记是新约最常引用的三卷旧约书——与学界的引文统计方向一致。'))
    c.append(h3('xref-all','全部连接（按类型）'))
    for k,(nm,col,ic) in KIND.items():
        rows=''.join(f'<tr><td><a href="index.html#b-{a}">{E(BN[a])}</a> → <a href="index.html#b-{b}">{E(BN[b])}</a></td><td>{E(r)}</td><td>{E(n)}</td></tr>' for a,b,k2,r,n in XR if k2==k)
        c.append(f'<details class="dx xk" style="--c:{col}"><summary>{ic} {nm} · {cnt[k]} 条</summary><div class="in tw"><table class="t"><thead><tr><th>书卷</th><th>出处</th><th>要点</th></tr></thead><tbody>{rows}</tbody></table></div></details>')
    c.append('''<script>(()=>{const s=document.querySelector('.xarc svg'),inf=document.getElementById('xinfo');if(!s)return;const P=[...s.querySelectorAll('.xa')];let k='all',b=null;
const ap=()=>{P.forEach(p=>{const okk=k==='all'||p.classList.contains('k'+k),okb=!b||p.dataset.a===b||p.dataset.b===b;p.classList.toggle('off',!(okk&&okb));p.classList.toggle('hi',!!b&&okk&&okb)});s.classList.toggle('sel',!!b);
s.querySelectorAll('.xb').forEach(g=>g.classList.toggle('on',g.dataset.b===b));
if(b){const L=P.filter(p=>!p.classList.contains('off'));inf.innerHTML='<b>'+s.querySelector('.xb[data-b="'+b+'"]').getAttribute('aria-label')+'</b>'+(L.length?'<ul>'+L.map(p=>'<li>'+p.querySelector('title').textContent+'</li>').join('')+'</ul>':'')}};
s.addEventListener('click',e=>{const g=e.target.closest('.xb');if(!g)return;b=b===g.dataset.b?null:g.dataset.b;ap()});
s.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){const g=e.target.closest('.xb');if(g){e.preventDefault();b=b===g.dataset.b?null:g.dataset.b;ap()}}});
document.querySelectorAll('[data-xk]').forEach(x=>x.addEventListener('click',()=>{k=x.dataset.xk;document.querySelectorAll('[data-xk]').forEach(y=>y.classList.toggle('on',y===x));ap()}))})()</script>''')
    return c
