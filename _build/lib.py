import json,re,html
V='v1'; DATE='2026-10-20'
import os
HERE=os.path.dirname(os.path.abspath(__file__))
CCI=os.path.join(HERE,'data','cci')+'/'
SITE=os.path.dirname(HERE)+'/'
CR=json.load(open(CCI+'creeds.json')); BC=json.load(open(CCI+'belgic.json')); HC=json.load(open(CCI+'heidelberg.json')); DT=json.load(open(CCI+'dort.json'))
HCQ={q['q']:(q,ld) for ld in HC['lordsdays'] for q in ld['questions']}
BCA={a['number']:a for a in BC['articles']}
E=html.escape
def sup(t): return re.sub(r'\^(\d+)',r'<sup>\1</sup>',E(t))
def paras(t): return ''.join('<p>'+sup(p.strip()).replace('\n','<br>')+'</p>' for p in t.strip().split('\n\n') if p.strip() and not p.strip().startswith('- '))
def refs(r): return '<ol class="refs">'+''.join(f'<li>{E(x)}</li>' for x in r)+'</ol>' if r else ''
def hc(n,open_=False,show_refs=True):
    q,ld=HCQ[n]
    return f'<details class="dx conf-d"{" open" if open_ else ""}><summary>📘 海德堡要理问答 第{n}问 <span class="tag" style="color:var(--vio)">{E(ld["title"])}</span></summary><div class="in"><div class="conf"><div class="src">逐字引自 <a href="{ld["url"]}" target="_blank" rel="noopener">ccifellowship.org · {E(ld["title"])}</a></div><p><b>{sup(q["question"])}</b></p>{paras(q["answer"])}{refs(q["refs"]) if show_refs else ""}</div></div></details>'
def bc(n,open_=False):
    a=BCA[n]
    return f'<details class="dx conf-d"{" open" if open_ else ""}><summary>📗 比利时信条 {E(a["title"])}</summary><div class="in"><div class="conf"><div class="src">逐字引自 <a href="{a["url"]}" target="_blank" rel="noopener">ccifellowship.org · 比利时信条</a></div>{paras(a["text"])}{refs(a["refs"])}</div></div></details>'
def dort(h,n,open_=False):
    hd=DT['heads'][h]; a=[x for x in hd['articles'] if x['number']==n][0]
    return f'<details class="dx conf-d"{" open" if open_ else ""}><summary>📕 多特信经 · {E(hd["title"])} · {E(a["title"])}</summary><div class="in"><div class="conf"><div class="src">逐字引自 <a href="{a["url"]}" target="_blank" rel="noopener">ccifellowship.org · 多特信经</a></div>{paras(a["text"])}{refs(a["refs"])}</div></div></details>'
def confref(spec):
    """spec like 'HC1,BC12,DT0.7' -> html"""
    out=[]
    for s in [x.strip() for x in spec.split(',') if x.strip()]:
        if s.startswith('HC'): out.append(hc(int(s[2:])))
        elif s.startswith('BC'): out.append(bc(int(s[2:])))
        elif s.startswith('DT'): h,n=s[2:].split('.'); out.append(dort(int(h),int(n)))
    return ''.join(out)
def conflabel(s):
    if s.startswith('HC'): return f'海德堡{s[2:]}问'
    if s.startswith('BC'): return f'比利时{s[2:]}条'
    h,n=s[2:].split('.'); return f'多特{["一","二","三四","五"][int(h)]}·{n}'
PAGES=[('index.html','🏠','首页总览'),('story.html','🧭','救赎大故事'),('covenant.html','🤝','圣约神学'),('timeline.html','⏳','时间线·诸王'),('geography.html','🗺️','地理文化'),('ot.html','📜','旧约39卷'),('nt.html','✝️','新约27卷'),('creeds.html','🕊️','三大信经'),('forms.html','📚','三项联合信条'),('memory.html','🧠','记忆·测验'),('sources.html','🔗','资料来源')]
def page(fn,title,content,extra_head='',scripts=''):
    nav=''.join(f'<a href="{f}" class="{"on" if f==fn else ""}">{i} {t}</a>' for f,i,t in PAGES)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)} · 整本圣经 欧陆改革宗研读 {V}</title><meta name="description" content="整本圣经解读：救赎历史、圣约神学、时间线、诸王、地理、66卷逐卷、三大信经与三项联合信条（欧陆改革宗）。GROKstudy {V} {DATE}">
<meta name="theme-color" content="#070b1a"><meta name="wb-version" content="{V}-{DATE}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📖</text></svg>">
<link rel="stylesheet" href="assets/css/app.css?v={V}">{extra_head}</head>
<body><div class="aurora"><i></i><i></i><i></i></div><div class="prog"></div>
<header class="top"><button class="ibtn" id="tocBtn" title="目录 显示/隐藏" aria-label="目录">☰</button><a class="brand" href="index.html">📖 <b>整本圣经</b><span class="t">· 欧陆改革宗研读</span><small>GROKstudy {V}</small></a><nav class="nav">{nav}</nav><button class="ibtn" id="themeBtn" title="明/暗主题" aria-label="主题">◐</button></header>
<div class="wrap"><aside class="toc" id="toc"><h4>📑 本页目录</h4><input id="tocq" placeholder="🔍 筛选目录…" aria-label="筛选目录"><ol></ol><h4 style="margin-top:18px">🧭 全站页面</h4><div class="tocpages">{"".join(f'<a href="{f}" class="{"on" if f==fn else ""}">{i} {t}</a>' for f,i,t in PAGES)}</div></aside><div class="scrim"></div>
<main id="main">{content}
<footer class="ft">📖 整本圣经 · 欧陆改革宗研读 — GROKstudy {V}（{DATE}）。信经与信条引文逐字取自 <a href="https://ccifellowship.org" target="_blank" rel="noopener">ccifellowship.org</a>（中国改革宗教会）；经文采用和合本。本站为学习辅助，日期采用保守派（Thiele 式）年代学，个别年份学界有±1–2年差异。<br>页面：{" · ".join(f'<a href="{f}">{t}</a>' for f,i,t in PAGES)}</footer></main></div>
<button class="ibtn totop" aria-label="回到顶部">↑</button>
<script src="assets/vendor/mermaid.min.js"></script>{scripts}<script src="assets/js/app.js?v={V}"></script></body></html>'''
def h2(id,ic,t,toc=None): return f'<h2 class="h reveal" id="{id}"{f" data-toc={chr(34)}{E(toc)}{chr(34)}" if toc else ""}><span class="ic">{ic}</span>{t}</h2>'
def h3(id,t): return f'<h3 class="h" id="{id}">{t}</h3>'
def mer(src,cap=''): return f'<figure class="mer reveal" style="margin:12px 0"><pre class="mermaid">{E(src.strip())}</pre>{f"<figcaption class=srcline>{cap}</figcaption>" if cap else ""}</figure>'
def table(head,rows,cls=''):
    return f'<div class="tw {cls}"><table><thead><tr>{"".join(f"<th>{h}</th>" for h in head)}</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table></div>'
def note(t,body,cls=''): return f'<div class="note {cls}"><b class="t">{t}</b>{body}</div>'
def verse(t,ref): return f'<blockquote class="v">{t}<cite>— {ref}（和合本）</cite></blockquote>'
