import json,re,html
V='v9'; DATE='2026-10-23'
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
GROUPS=[('1','66卷书','📚',[('index.html','📚','66卷书','书架·逐卷13项解读')]),
 ('2','全景总览','🧭',[('overview.html','🏠','全景总览','学习路线·一页纸·标注系统'),('story.html','🧭','救赎大故事','四幕剧·红线·圣经神学'),('covenant.html','🤝','圣约神学','三约·六约·两种施行'),('timeline.html','⏳','时间线·诸王','11时代·8钉子·42王'),('geography.html','🗺️','地理文化','8幅交互地图')]),
 ('3','基督与福音','✝️',[('life-of-christ.html','🌟','基督生平','事件×地图联动'),('gospels.html','📗','四福音对照','四幅肖像·段落对照'),('harmony.html','📖','四福音合参','202段·和合本·独有细节'),('acts.html','🕊️','使徒行传·初代教会','AD30–95·旅程动画')]),
 ('4','文体对比','🧩',[('pentateuch.html','⚖️','摩西五经对照','五经横向×纵向'),('history.html','🏛️','历史书对照','得地→被掳→归回'),('poetry.html','🎼','诗歌智慧书对照','五卷三角度看智慧'),('prophets.html','🔥','先知书对照','17先知×君王×帝国'),('epistles.html','✉️','新约书信对照','21封书信·年代·主题')]),
 ('5','专题','🔍',[('kings-chronicles.html','👑','列王纪×历代志','42王逐王对照'),('compare.html','🔗','跨卷对照','以经解经·引用网络'),('stats.html','📊','圣经统计','章节·类别·引用')]),
 ('6','信条','🕊️',[('creeds.html','🕊️','三大信经','背诵版·深度对比'),('forms.html','📜','三项联合信条','37条·129问·多特'),('memory.html','🧠','记忆·测验','口诀·闪卡·测验')]),
 ('7','资料','🗂️',[('sources.html','🗂️','资料来源','逐字来源·核对')])]
PAGES=[(f,i,t) for _,_,_,ps in GROUPS for f,i,t,_d in ps]
PNUM={f:f'{g}.{k+1}' for g,_,_,ps in GROUPS for k,(f,_i,_t,_d) in enumerate(ps)}
PGRP={f:(g,gn,gi) for g,gn,gi,ps in GROUPS for (f,_i,_t,_d) in ps}
GCIRC='①②③④⑤⑥⑦'
def navhtml(fn):
    o=''
    for g,gn,gi,ps in GROUPS:
        on=any(f==fn for f,*_ in ps)
        links=''.join(f'<a href="{f}" class="{"on" if f==fn else ""}"><span class="pn">{PNUM[f]}</span>{i} {t}<small>{E(d)}</small></a>' for f,i,t,d in ps)
        o+=f'<div class="ng{" on" if on else ""}"><button class="ngb" aria-haspopup="true" aria-expanded="false"><span class="gn">{GCIRC[int(g)-1]}</span><span class="gi">{gi}</span>{gn}<i>▾</i></button><div class="ndd" role="menu"><b class="ndh">{GCIRC[int(g)-1]} {gn}</b>{links}</div></div>'
    return o
def pageshtml(fn):
    o=''
    for g,gn,gi,ps in GROUPS:
        o+=f'<div class="tpg"><b class="tpgh"><span class="gn">{GCIRC[int(g)-1]}</span>{gi} {gn}</b>'+''.join(f'<a href="{f}" class="{"on" if f==fn else ""}"><span class="pn">{PNUM[f]}</span>{i} {t}</a>' for f,i,t,_d in ps)+'</div>'
    return o
def crumbs(fn):
    if fn not in PNUM: return ''
    g,gn,gi=PGRP[fn]; i=[x for x in PAGES if x[0]==fn][0]
    k=[x[0] for x in PAGES].index(fn); pv=PAGES[k-1] if k>0 else None; nx=PAGES[k+1] if k+1<len(PAGES) else None
    top=f'<div class="crumb"><a href="index.html">📖 整本圣经</a><i>›</i><span>{GCIRC[int(g)-1]} {gi} {gn}</span><i>›</i><b>{PNUM[fn]} {i[1]} {i[2]}</b></div>'
    bot='<nav class="pnx">'+(f'<a href="{pv[0]}" class="pv"><small>← 上一页</small><b>{PNUM[pv[0]]} {pv[1]} {pv[2]}</b></a>' if pv else '<span></span>')+(f'<a href="{nx[0]}" class="nx"><small>下一页 →</small><b>{PNUM[nx[0]]} {nx[1]} {nx[2]}</b></a>' if nx else '<span></span>')+'</nav>'
    return top,bot
CN='零一二三四五六七八九十'
def cnum(n):
    if n<=10: return CN[n]
    if n<20: return '十'+CN[n-10]
    return CN[n//10]+'十'+(CN[n%10] if n%10 else '')
def _plain(h):
    h=re.sub(r'<small.*?</small>','',h,flags=re.S); h=re.sub(r'<span class="(ic|sn)">.*?</span>','',h,flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>','',h)).strip()
HRE=re.compile(r'<h([234]) class="h([^"]*)"([^>]*)>(.*?)</h\1>',re.S)
def number(content):
    """number h2/h3/h4.h and return (content, toc entries)"""
    c=[0,0,0]; toc=[]; auto=[0]
    def rep(m):
        lv=int(m.group(1)); cls=m.group(2); at=m.group(3); inner=m.group(4)
        idm=re.search(r'\bid="([^"]+)"',at)
        if not idm: auto[0]+=1; hid=f's{auto[0]}'; at+=f' id="{hid}"'
        else: hid=idm.group(1)
        nm=re.search(r'data-num="([^"]*)"',at); tm=re.search(r'data-toc="([^"]*)"',at)
        if lv==2: c[0]+=1;c[1]=0;c[2]=0; num=cnum(c[0])+'、'
        elif lv==3: c[1]+=1;c[2]=0; num=(nm.group(1) if nm else str(c[1]))+'.'
        else:
            c[2]+=1; num=f'{c[1]}.{c[2]}'
        if lv==3 and nm: c[1]=int(nm.group(1)) if nm.group(1).isdigit() else c[1]
        if lv==4 and nm: num=nm.group(1)
        if 'nonum' in cls: num=''
        txt=html.unescape(tm.group(1)) if tm else _plain(inner)
        icm=re.search(r'<span class="ic">(.*?)</span>',inner,re.S)
        if lv==2 and icm and not tm: txt=_plain(icm.group(1))+' '+txt
        if 'notoc' not in cls: toc.append((lv,hid,num,txt))
        sn=f'<span class="sn">{num}</span>' if num else ''
        if '<span class="ic">' in inner: inner=re.sub(r'(<span class="ic">.*?</span>)',lambda x:x.group(1)+sn,inner,count=1,flags=re.S)
        else: inner=sn+inner
        return f'<h{lv} class="h{cls}"{at}>{inner}</h{lv}>'
    return HRE.sub(rep,content),toc
def toctree(toc):
    roots=[];stack=[]
    for lv,hid,num,txt in toc:
        node={'lv':lv,'id':hid,'num':num,'txt':txt,'ch':[]}
        while stack and stack[-1]['lv']>=lv: stack.pop()
        (stack[-1]['ch'] if stack else roots).append(node); stack.append(node)
    big=len(toc)>60
    def r(nodes,d):
        o=''
        for n in nodes:
            has=bool(n['ch']); closed=' closed' if has and d>=2 and big else ''
            o+=f'<li class="l{min(d,3)}{closed}"><div class="row"><button class="tg{"" if has else " leaf"}" aria-label="展开/收起" tabindex="-1">▾</button><a href="#{n["id"]}"><span class="n">{E(n["num"])}</span>{E(n["txt"])}</a></div>'
            if has: o+=('<template class="tl"><ul>'+r(n['ch'],d+1)+'</ul></template>') if closed else ('<ul>'+r(n['ch'],d+1)+'</ul>')
            o+='</li>'
        return o
    return '<ul class="tree">'+r(roots,1)+'</ul>'
def _strip(t): return re.sub(r'\^\d+','',t)
SRC={}
for _n,(_q,_ld) in HCQ.items(): SRC['HC%d'%_n]=(_strip(_q['answer']),_ld['url'],'海德堡要理问答第%d问'%_n)
for _n,_a in BCA.items(): SRC['BC%d'%_n]=(_strip(_a['text']),_a['url'],'比利时信条第%d条'%_n)
SRC['AP']=(CR['apostles']['text'],CR['apostles']['url'],'使徒信经');SRC['NI']=(CR['nicene']['text'],CR['nicene']['url'],'尼西亚信经');SRC['AT']=(CR['athanasian']['text'],CR['athanasian']['url'],'亚他那修信经')
for _i,_h in enumerate(DT['heads']):
    for _a in _h['articles']:
        if isinstance(_a.get('number'),int): SRC[f'DT{_i}_{_a["number"]}']=(_strip(_a['text']),_a['url'],'多特信经·'+_h['title'][:6]+('·错谬反驳' if _a['title'].startswith('错谬') else '第%d条'%_a['number']))
QUOTES=[]
EMR=[(r'\*\*(.+?)\*\*',r'<b class="k">\1</b>'),(r'==(.+?)==',r'<mark class="hy">\1</mark>'),(r'%%(.+?)%%',r'<mark class="hg">\1</mark>'),
     (r'!!(.+?)!!',r'<span class="uw">\1</span>'),(r'\+\+(.+?)\+\+',r'<span class="ug">\1</span>'),(r'\^\^(.+?)\^\^',r'<span class="ub">\1</span>'),
     (r'\[\[(.+?)\]\]',r'<span class="cx">\1</span>'),(r'~~(.+?)~~',r'<span class="cr">\1</span>'),
     (r'@@(.+?)@@',r'<span class="must">\1</span>'),(r';;(.+?);;',r'<span class="ud">\1</span>'),(r'__(.+?)__',r'<span class="uo">\1</span>'),(r'\$\$(.+?)\$\$',r'<mark class="hb">\1</mark>')]
REFRE=re.compile(r'(?<![\d:新旧立守背盟之圣])((?:撒上|撒下|王上|王下|代上|代下|林前|林后|帖前|帖后|提前|提后|彼前|彼后|约一|约二|约三|[创出利民申书士得拉尼斯伯诗箴传歌赛耶哀结但何珥摩俄拿弥鸿哈番该亚玛太可路约徒罗加弗腓西多门来雅犹启])\d{1,3}:\d{1,3}(?:[–\-]\d{1,3}(?::\d{1,3})?)?)(?![\d])')
TERMS=['恩典之约','行为之约','救赎之约','亚伯拉罕之约','摩西之约','西奈之约','大卫之约','挪亚之约','新约应许','因信称义','代赎','中保','道成肉身','受苦的仆人','预表','护理','拣选','归算','三位一体','神的主权']
DATERE=re.compile(r'(?<![\d\^])((?:约|主前|主后|公元前|AD ?)?\d{2,4}(?:[–\-]\d{2,4})?(?: ?BC| ?AD|年代?))(?![\d\^])')
def em(t,auto=True):
    """escape + emphasis markup (no quote handling)"""
    x=E(t).replace('&#x27;',"'")
    if auto:
        x=DATERE.sub(lambda m:'^^'+m.group(1)+'^^' if re.search(r'BC|AD|主前|主后|公元前|年',m.group(1)) else m.group(1),x)
        seen=set()
        for w in TERMS:
            if w in x and w not in seen and '[['+w not in x:
                i=x.find(w)
                # avoid inside existing markup tokens crudely: skip if preceded by '[[' handled
                x=x[:i]+'[['+w+']]'+x[i+len(w):]; seen.add(w)
    for p,r in EMR: x=re.sub(p,r,x)
    x=x.replace('^^','')
    x=REFRE.sub(r'<span class="rf">\1</span>',x)
    return x
def rich(t,auto=True):
    ph=[]
    def rep(m):
        k,txt=m.group(1),m.group(2); src,url,lab=SRC[k]
        if txt not in src: raise SystemExit('QUOTE NOT VERBATIM: %s %s'%(k,txt))
        QUOTES.append((k,txt))
        ph.append(f'“<span class="key">{E(txt)}</span>”<a class="tag" style="color:var(--vio)" href="{url}" target="_blank" rel="noopener">{lab}·逐字</a>')
        return f'\x00{len(ph)-1}\x00'
    t2=re.sub(r'\{\{(\w+)\|(.+?)\}\}',rep,t)
    out=em(t2,auto)
    return re.sub(r'\x00(\d+)\x00',lambda m:ph[int(m.group(1))],out)
CO={'core':('💎','核心'),'xc':('✝️','基督'),'hardc':('⚠️','难点'),'trap':('🚫','易错'),'mnc':('🧠','口诀'),'app':('🌱','应用'),'info':('ℹ️','背景'),'conf':('📚','认信')}
def co(typ,body,label=None,cls=''):
    ic,lb=CO[typ]
    return f'<div class="co {typ} {cls}"><span class="lb">{ic} {label or lb}</span>{body}</div>'
LEGEND_EM=('<div class="legend-em">'
 '<span class="it"><b class="k">粗体金</b> 关键词</span>'
 '<span class="it"><mark class="hy">黄底</mark> 核心句/必背</span>'
 '<span class="it"><mark class="hg">绿底</mark> 正面应用·正统答案</span>'
 '<span class="it"><span class="ub">蓝虚线</span> 日期·年代</span>'
 '<span class="it"><span class="cx">紫粗体</span> 神学术语</span>'
 '<span class="it"><span class="ug">绿实线</span> 恩典·应许</span>'
 '<span class="it"><span class="uw">红波浪</span> 易错·异端·常见误解</span>'
 '<span class="it"><span class="cr">红字</span> 罪·审判</span>'
 '<span class="it"><span class="key">“金底引文”</span> 信条逐字引文</span>'
 '<span class="it"><span class="must">必背</span> 必须背诵</span>'
 '<span class="it"><span class="ud">金双线</span> 定义 · 原则</span>'
 '<span class="it"><span class="rf">罗8:28</span> 经文出处（自动）</span>'
 '<span class="it"><span class="kpb">1</span> 编号要点徽章</span>'
 '<span class="it"><span class="uo">橙粗线</span> 对比·差异</span>'
 '<span class="it"><mark class="hb">蓝底点线</mark> 人物·地点</span>'
 '<span class="it"><span class="mbadge">★ 必背</span> 必背徽章</span>'
 '<span class="it"><span class="mnf">口诀</span> 记忆口诀</span>'
 '<span class="it"><span class="kbmini">🔑</span> 钥点框（编号必背）</span>'
 '<span class="pills">'+''.join(f'<span class="pill co {k}">{v[0]}{v[1]}框</span>' for k,v in CO.items())+'</span></div>')
def legend_box(open_=False):
    return f'<details class="dx legendbox"{" open" if open_ else ""}><summary>🎨 笔记式标注图例（颜色编码说明）</summary><div class="in">{LEGEND_EM}</div></details>'
def wrap_sections(c):
    parts=re.split(r'(?=<h2 class="h)',c)
    def bal(p): return all(p.count('<'+t)==p.count('</'+t+'>') for t in ('div','section','details','article','figure','table'))
    if not all(bal(p) for p in parts): return c
    return ''.join(p if not p.startswith('<h2') else f'<section class="blk">{p}</section>' for p in parts)
THEMES=[('night','🌌','星空深蓝','#060a1c','#ffcb5c'),('dawn','🌅','晨曦米白','#f6f3ec','#b07000'),('jade','🍃','翡翠清新','#eaf6f0','#04875a'),('ruby','👑','红宝石宫廷','#1c0711','#ffd27a'),('contrast','🔆','高对比护眼','#0b0a08','#ffd400')]
HDR='<button class="ibtn hdx" id="plainBtn" title="笔记模式：显示/隐藏彩色标注" aria-label="笔记模式">🖍️</button><button class="ibtn hdx" id="focusBtn" title="专注模式：淡化非重点文字" aria-label="专注模式">🎯</button><button class="ibtn" id="tpBtn" title="主题配色 · 阅读模式" aria-label="主题与阅读模式" aria-expanded="false">🎨</button><div class="tpanel" id="tpanel" hidden><b class="tpt">🎨 主题配色</b><div class="tsw">{tsw}</div><b class="tpt">📖 阅读模式</b><label class="tgl"><input type="checkbox" id="plainChk"> 🖍️ 笔记模式 <small>关闭 = 隐藏全部彩色标注</small></label><label class="tgl"><input type="checkbox" id="focusChk"> 🎯 专注模式 <small>淡化非重点，只亮关键句</small></label><label class="tgl"><input type="checkbox" id="lenisChk"> 🌊 惯性滚动 <small>默认关闭：原生滚动最顺</small></label></div>'.format(tsw=''.join(f'<button data-theme="{k}" style="--sw:{bg};--sa:{ac}"><i></i>{ic} {n}</button>' for k,ic,n,bg,ac in THEMES))
TAGRE=re.compile(r'(<[^>]+>)')
VOID={'br','img','input','meta','link','hr','wbr','source','col','area'}
SKIPT={'a','cite','svg','script','style','textarea','button','code','pre','title','h2','h3','h4','h5','summary','th'}
SKIPC=re.compile(r'class="[^"]*\b(refs|conf|creed|mersvg|kc|kcheat|rf|tag|chip|sleg|sbar|canon|kt|covflow|map|fc|ord|quiz|era)\b')
def autoref(html_):
    out=[];stack=[];skip=0
    for part in TAGRE.split(html_):
        if part.startswith('<'):
            if part.startswith('<!--') or part.startswith('<!'): out.append(part);continue
            m=re.match(r'</?([a-zA-Z0-9]+)',part)
            if not m: out.append(part);continue
            t=m.group(1).lower()
            if part.startswith('</'):
                while stack:
                    tt,sk=stack.pop()
                    if sk: skip-=1
                    if tt==t: break
            elif t not in VOID and not part.endswith('/>'):
                sk=1 if (t in SKIPT or SKIPC.search(part)) else 0
                skip+=sk; stack.append((t,sk))
            out.append(part)
        else:
            out.append(part if skip or ':' not in part else REFRE.sub(r'<span class="rf">\1</span>',part))
    return ''.join(out)
def page(fn,title,content,extra_head='',scripts='',cv=True):
    content=content.replace(' reveal"',' rv"').replace('"reveal ','"rv ').replace('class="reveal"','class="rv"')
    from v5extra import tldr
    t5=tldr(fn)
    if t5:
        if content.lstrip().startswith('<section class="hero'):
            k=content.index('</section>')+len('</section>'); content=content[:k]+t5+content[k:]
        else: content=t5+content
    content,toc=number(content)
    content=autoref(content)
    if cv: content=wrap_sections(content)
    nav=navhtml(fn); pages=pageshtml(fn); cb=crumbs(fn) or ('','')
    GEN=['pentateuch.html','history.html','poetry.html','prophets.html','gospels.html','epistles.html']
    if fn in GEN:
        gl=[x for g_ in GROUPS for x in g_[3] if x[0] in GEN]
        cb=(cb[0]+'<div class="gsw" role="navigation" aria-label="文体对照页切换"><b>📚 文体对照：</b>'+''.join(f'<a href="{f}" class="{"on" if f==fn else ""}">{i} {t.replace("对照","")}</a>' for f,i,t,d in gl)+'</div>',cb[1])
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)} · 整本圣经 欧陆改革宗研读 {V}</title><meta name="description" content="整本圣经解读：救赎历史、圣约神学、时间线、诸王、地理、66卷逐卷、三大信经与三项联合信条（欧陆改革宗）。GROKstudy {V} {DATE}">
<meta name="theme-color" content="#070b1a"><meta name="wb-version" content="{V}-{DATE}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📖</text></svg>">
<script>try{{var d=document.documentElement,L=localStorage,t=L.getItem('wb-theme');if(t==='light')t='dawn';if(!t||t==='dark'||!/^(night|dawn|jade|ruby|contrast)$/.test(t))t='night';d.dataset.theme=t;if(t==='dawn'||t==='jade')d.classList.add('light');if(L.getItem('wb-plain')==='1')d.classList.add('plain');if(L.getItem('wb-focus')==='1')d.classList.add('focus');var w=L.getItem('wb-tocw');if(w)d.style.setProperty('--toc',w+'px')}}catch(e){{}}</script>
<script type="speculationrules">{{"prerender":[{{"where":{{"href_matches":"*.html"}},"eagerness":"moderate"}}]}}</script>
<link rel="stylesheet" href="assets/css/app.css?v={V}">{extra_head}</head>
<body data-mer="assets/vendor/mermaid.min.js"><div class="aurora"></div><div class="prog"></div>
<header class="top"><button class="ibtn" id="tocBtn" title="目录 显示/隐藏" aria-label="目录">☰</button><a class="brand" href="index.html">📖 <b>整本圣经</b><span class="t">· 欧陆改革宗研读</span><small>GROKstudy {V}</small></a><nav class="nav">{nav}</nav>'''+HDR+f'''</header>
<div class="wrap"><aside class="toc" id="toc"><div class="toch"><b>📑 本页目录</b><button id="tocL2" title="只展开到二级">二级</button><button id="tocAll" title="全部展开">全开</button><button id="tocNone" title="全部收起">全收</button><button id="tocClose" title="隐藏目录" aria-label="隐藏目录">✕</button></div>
<input id="tocq" placeholder="🔍 筛选目录…" aria-label="筛选目录"><div class="tocbody" data-lenis-prevent>{toctree(toc)}<div class="tocpages"><b>🧭 全站页面 · {len(GROUPS)} 组 {len(PAGES)} 页</b>{pages}</div></div><div class="rz" title="拖动调整目录宽度（双击复位）" role="separator" aria-orientation="vertical"><span class="rztip"></span></div><div class="rzhint" hidden>↔ 拖动右边缘调整目录宽度</div></aside><div class="scrim"></div>
<main id="main">{cb[0]}{content}
{cb[1]}<footer class="ft">📖 整本圣经 · 欧陆改革宗研读 — GROKstudy {V}（{DATE}）。信经与信条引文逐字取自 <a href="https://ccifellowship.org" target="_blank" rel="noopener">ccifellowship.org</a>（中国改革宗教会）；经文采用和合本。本站为学习辅助，日期采用保守派（Thiele 式）年代学，个别年份学界有±1–2年差异。<br>{"<br>".join(f'<b>{GCIRC[int(g)-1]} {gn}</b>：'+" · ".join(f'<a href="{f}">{PNUM[f]} {t}</a>' for f,i,t,d in ps) for g,gn,gi,ps in GROUPS)}</footer></main></div>
<button class="ibtn totop" aria-label="回到顶部">↑</button>
{scripts}<script src="assets/js/app.js?v={V}" defer></script></body></html>'''
def h4(id,t,num=None): return f'<h4 class="h" id="{id}"{f" data-num={chr(34)}{num}{chr(34)}" if num else ""}>{t}</h4>'
def h2(id,ic,t,toc=None): return f'<h2 class="h reveal" id="{id}"{f" data-toc={chr(34)}{E(toc)}{chr(34)}" if toc else ""}><span class="ic">{ic}</span>{t}</h2>'
def h3(id,t,toc=None): return f'<h3 class="h" id="{id}"{f" data-toc={chr(34)}{E(toc)}{chr(34)}" if toc else ""}>{t}</h3>'
def mer(src,cap=''): return f'<figure class="mer reveal" style="margin:12px 0"><pre class="mermaid">{E(src.strip())}</pre>{f"<figcaption class=srcline>{cap}</figcaption>" if cap else ""}</figure>'
def table(head,rows,cls=''):
    return f'<div class="tw {cls}"><table><thead><tr>{"".join(f"<th>{h}</th>" for h in head)}</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table></div>'
def note(t,body,cls=''): return f'<div class="note {cls}"><b class="t">{t}</b>{body}</div>'
def verse(t,ref): return f'<blockquote class="v">{t}<cite>— {ref}（和合本）</cite></blockquote>'
