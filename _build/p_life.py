import json
from lib import *
from v6lib import *
from life_data import *
REFP={'Mt':'太','Mk':'可','Lk':'路','Jn':'约'}
def refs_html(r):
    o=[gtag(k,v) for k,v in r.items() if k in G]
    if 'X' in r: o.append(f'<span class="gt" style="--c:var(--emer)">📜 {E(r["X"])}</span>')
    return ''.join(o)
def mapcfg():
    used=[];seen=set()
    for e in EV:
        if e[5] not in seen: seen.add(e[5]); used.append(e[5])
    route=[list(PL[e[5]]) for e in EV if e[0] not in ('passion','risen')]
    pts=[{'n':n,'ll':list(PL[n]),'d':'；'.join(e[3] for e in EV if e[5]==n)[:120],'k':1 if n in ('耶路撒冷','伯利恒','拿撒勒','迦百农','加利利海','伯大尼','该撒利亚腓立比') else 0} for n in used if n not in ('圣殿','客西马尼','各各他','橄榄山')]
    return {'bounds':[[30.3,31.6],[33.6,36.2]],'color':'#ffcb5c','routes':[{'n':'事工路线（按本页事件先后连线，示意）','path':route,'c':'#ffcb5c','dash':'5 7','arrow':False}],'points':pts,
      'regions':[{'n':'加利利','lab':[32.95,35.33],'c':'#3ee0a1'},{'n':'撒玛利亚','lab':[32.25,35.05],'c':'#ffb34d'},{'n':'犹太','lab':[31.55,34.95],'c':'#5ec8ff'},{'n':'比利亚','lab':[32.05,35.78],'c':'#ff9de2'}],
      'legend':[['#ffcb5c','事件先后（示意连线）'],['#ff5d7a','当前事件']]}
def build():
    open(SITE+'assets/data/maps6.js','w').write('window.MAPS=Object.assign(window.MAPS||{},'+json.dumps({'life':mapcfg()},ensure_ascii=False,separators=(',',':'))+');')
    c=[]
    c.append(hero(['🌟 基督生平','保守派年代','四福音出处','地图联动','受难周逐日'],'从伯利恒到橄榄山：','基督生平全景',
      '把四福音放进一条时间线：<span class="must">降生 约6–4 BC</span> · <span class="must">受洗 AD 26/27（或29）</span> · <span class="must">十字架 AD 30（或33）</span>。点击任一事件，右侧地图会<b class="k">飞到那个地方</b>；每个事件都列出四福音出处。'))
    c.append(legend_box())
    c.append(h2('frame','🧭','整体：年代框架与两种主要看法'))
    c.append(h3('pins','五个钉子年份'))
    c.append(stats([('6–4 BC','降生（希律死于 4 BC 前）','🌟','var(--gold)'),('AD 26/27','受洗（AD 30 说）','🕊️','var(--sky)'),('3 个','约翰明记的逾越节','🐑','var(--vio)'),('AD 30','钉十字架（4月7日）','✝️','var(--rose)'),('AD 33','另一主要看法（4月3日）','📅','var(--emer)'),('40 + 10','升天第40天，五旬节第50天','☁️','var(--gold)')]))
    c.append(h3('ad30','AD 30 还是 AD 33？'))
    c.append(table(['','AD 30 说','AD 33 说'],[
      ['<b>受洗</b>','AD 26/27 秋','AD 29'],
      ['<b>事工长度</b>','约3年半（约翰记 3 个逾越节，约5:1可能是第4个）','约3年半（4 个逾越节）'],
      ['<b>主要依据</b>',rich('约2:20“这殿是四十六年才造成的”——希律约 20/19 BC 动工 → 约 AD 27 逾越节',False),rich('路3:1“提庇留在位第十五年”——从 AD 14 独自执政起算 → AD 28/29',False)],
      ['<b>困难</b>','路3:1须按提庇留与奥古斯都共治（AD 11/12）起算','须把约2:20的“四十六年”理解为殿宇（naos）完工年份等'],
      ['<b>受难日</b>','尼散月14/15日为星期五：AD 30年4月7日','AD 33年4月3日'],
      ['<b>代表学者</b>','许多保守派年代学者','Harold Hoehner《基督生平年代》（1977）']]))
    c.append(co('core','<p>'+rich('两种看法都**持守圣经无误**，都同意：==降生在希律死前、事工约三年半、星期五受难、第三天复活==。差别只在于如何对应罗马纪年；不要把年代学的分歧当作信仰问题。',False)+'</p>','核心'))
    c.append(h3('phases','八个阶段（色带）'))
    c.append('<div class="eraband rv lifeband">'+''.join(f'<span style="--c:{col};flex:{w} 1 0"><b>{t}</b><small>{d}</small></span>' for (k,t,d,col),w in zip(PH,(2,1,2,3,1.2,1.6,1.4,1.2)))+'</div>')
    # ----- interactive timeline + map
    c.append(h2('tl','🗺️','时间线 × 地图：点击事件，地图飞过去'))
    c.append(h3('tlmap',f'{len(EV)} 个事件 · 四福音出处'))
    c.append('<div class="lifeph" role="toolbar" aria-label="按阶段筛选"><button data-ph="all" class="on">全部</button>'+''.join(f'<button data-ph="{k}" style="--c:{col}">{t}</button>' for k,t,d,col in PH)+'<button id="lifePlay" class="play">▶️ 自动播放</button></div>')
    evs=''
    for i,(ph,d30,d33,t,r,pl,nt) in enumerate(EV):
        col=[x[3] for x in PH if x[0]==ph][0]; ll=PL[pl]
        z=13 if pl in ('圣殿','客西马尼','各各他','橄榄山','伯大尼') else 10
        evs+=(f'<div class="lev" data-ph="{ph}" style="--c:{col}"><button data-ll="{ll[0]},{ll[1]}" data-z="{z}" data-place="{E(pl)}"><span class="ln">{i+1}</span><span class="ld">{E(d30)}{f" <small>／{E(d33)}</small>" if d33!=d30 else ""}</span>'
              f'<b>{E(t)}</b><span class="lp">📍 {E(pl)}</span></button><div class="lr">{refs_html(r)}</div><div class="lnote">{rich(nt,False)}</div></div>')
    c.append(f'<div class="lifegrid"><div class="lifetl">{evs}</div><div class="lifemap"><div class="map" data-map="life" role="region" aria-label="基督生平地图"><div class="lazyph" style="height:100%">🗺️ 地图加载中…</div></div><p class="srcline">年代：前为 AD 30 说，／后为 AD 33 说。地点为传统或约略位置（如以马忤斯、登山变像之山有争议）。</p></div></div>')
    # ----- feasts
    c.append(h2('feasts','🐑','约翰福音的节期：事工长度的钥匙'))
    c.append(h3('jfeasts','约翰记载的六个节期'))
    c.append('<div class="steps rv">'+''.join(f'<div style="--c:{"var(--rose)" if "逾越" in t else "var(--sky)"}"><span class="e">{"🐑" if "逾越" in t else "🎉"}</span><b>{E(t)}</b><span class="rf">{E(r)}</span><span>{E(d)}</span></div>' for t,r,d in FEASTS)+'</div>')
    c.append(co('xc','<p>'+rich('约翰把耶稣放在节期中：他是==真逾越节的羔羊==（约1:29；19:36），是**住棚节的活水与光**（7:37；8:12），是**真殿**（2:19–21）。节期是影儿，基督是实体（西2:16–17）。',False)+'</p>','基督'))
    # ----- passion week
    c.append(h2('passion','✝️','受难周：逐日看'))
    days=[e for e in EV if e[0]=='passion']+[e for e in EV if e[0]=='risen'][:1]
    dn=['六','日','一','二','三','四','五','六','日']
    btn=''.join(f'<button data-day="{i}" class="{"on" if i==6 else ""}" style="--c:{"var(--rose)" if i==6 else ("var(--gold)" if i==8 else "var(--sky)")}"><b>{E(e[1])}</b><small>{E(e[3][:8])}</small></button>' for i,e in enumerate(days))
    pan=''.join(f'<div class="pday card" data-d="{i}"{"" if i==6 else " hidden"}><h4 class="h notoc">{E(e[1])} · {E(e[3])}</h4><p>📍 {E(e[5])} · {rich(e[6],False)}</p><div class="lr">{refs_html(e[4])}</div></div>' for i,e in enumerate(days))
    c.append(h3('pdays','八天时间带（点击某一天）'))
    c.append(f'<div class="pweek rv"><div class="pwb">{btn}</div>{pan}</div>')
    c.append(h3('friday','星期五：钉十字架的时辰'))
    hrs=[('清晨','公会定案，解交彼拉多','可15:1','var(--sky)'),('第三时（约9点）','钉十字架','可15:25','var(--rose)'),('第六时（正午）','遍地黑暗','可15:33','var(--vio)'),('第九时（约3点）','“以利，以利……”，断气','可15:34–37','var(--rose)'),('傍晚','约瑟、尼哥底母安葬','约19:38–42','var(--gold)')]
    c.append('<div class="hourline rv">'+''.join(f'<div style="--c:{col}"><b>{t}</b><span>{d}</span><span class="rf">{r}</span></div>' for t,d,r,col in hrs)+'</div>')
    c.append(co('hardc','<p>'+rich('约19:14说彼拉多判案“约在午正”（第六时）。常见解释：约翰可能用罗马式从午夜起算（约早上6点），或时间为约数。==这是计时方式的差异，不是矛盾==。',False)+'</p>','难点'))
    # ----- resurrection
    c.append(h2('risen','🌅','复活、显现、升天、五旬节'))
    c.append(h3('appear',f'复活后的 {len(APPEAR)} 次显现（按大致次序）'))
    c.append(table(['#','向谁显现','经文'],[[f'<span class="kpb">{i+1}</span>',f'<b>{E(a)}</b>',E(r)] for i,(a,r) in enumerate(APPEAR)]))
    c.append(co('core','<p>'+rich('保罗列出复活见证人，许多“如今还在”（林前15:6）——==复活是可查证的历史事实==，不是信心的投射。',False)+'</p>'))
    # ----- offices & states
    c.append(h2('offices','👑','基督的三职与二状态'))
    c.append(h3('three','先知 · 祭司 · 君王'))
    c.append(table(['职分','旧约预表','基督的成全','对我的意义'],[
      ['📣 <b>先知</b>','摩西（申18:15）','完全启示神的旨意（约1:18；来1:1–2）','听他的话'],
      ['🩸 <b>祭司</b>','亚伦、麦基洗德（诗110:4）','一次献上自己，又长远代求（来7:25；9:12）','靠他的献祭坦然到神面前'],
      ['👑 <b>君王</b>','大卫（撒下7:12–16）','用道与圣灵统管、保护教会（太28:18）','顺服并依靠他的保守']]))
    c.append(co('conf','<p>'+rich('海德堡要理问答第31问：他{{HC31|作我们的大先知和教师}}；{{HC31|他是我们唯一的大祭司，藉着他一次献上的身体救赎了我们}}；{{HC31|他是我们永远的君王，用他的话语和圣灵统管我们}}。',False)+'</p>','认信'))
    c.append(hc(31,open_=True)+hc(32))
    c.append(h3('states','降卑与升高：一条“V”字线'))
    down=['因圣灵感孕','从童贞女马利亚所生','在本丢·彼拉多手下受难','被钉在十字架上','受死，被埋葬','降在阴间']
    up=['第三天从死里复活','他升天','坐在全能父神的右边','将来必从那里降临，审判活人死人']
    for x in down+up: assert x in CR['apostles']['text'],x
    steps=''.join(f'<div class="vst dn" style="--i:{i}"><span>{E(x)}</span></div>' for i,x in enumerate(down))+''.join(f'<div class="vst up" style="--i:{len(up)-1-i}"><span>{E(x)}</span></div>' for i,x in enumerate(up))
    c.append(f'<div class="vline rv" role="img" aria-label="降卑与升高">{steps}</div><p class="srcline">每一级的文字均逐字取自 <a href="{CR["apostles"]["url"]}" target="_blank" rel="noopener">ccifellowship.org · 使徒信经</a>（构建时校验）。参：腓2:6–11；海德堡要理问答第35–52问；威斯敏斯特小要理问答第27–28问。</p>')
    c.append(hc(44))
    c.append(co('trap','<p>'+rich('!!“降在阴间”不是说基督到地狱再受一次苦或给死人第二次机会!!。海德堡第44问把它解释为基督在一切苦难中，{{HC44|尤其是在十字架上所忍受的}}==无法言表的痛苦==，使我确知主{{HC44|已经拯救我脱离了地狱的痛苦和折磨}}。',False)+'</p>','易错'))
    c.append(co('app','<p>'+rich('读福音书的任何一段，都问：这是他**降卑**的哪一步？还是**升高**的预尝？——十字架之后必有冠冕（来12:2）。',False)+'</p>','应用'))
    return page('life-of-christ.html','基督生平',''.join(c),extra_head='<link rel="stylesheet" href="assets/vendor/leaflet.css">',
      scripts='<script src="assets/vendor/leaflet.js" defer></script><script src="assets/data/land.js" defer></script><script src="assets/data/maps6.js" defer></script><script src="assets/js/maps.js?v=v6" defer></script><script src="assets/js/v6.js?v=v6" defer></script>')
