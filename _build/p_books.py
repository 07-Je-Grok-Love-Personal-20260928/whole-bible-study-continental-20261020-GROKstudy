from lib import *
from books import *
def filters(keys,target):
    return f'<div class="filters" data-target="{target}"><button class="on" data-cat="all">全部</button>'+''.join(f'<button data-cat="{k}">{CATS[k][2]} {CATS[k][0]}</button>' for k in keys)+'<input placeholder="🔍 搜索书卷/主题/经文…" aria-label="搜索书卷"><button data-expand=".bk details" data-state="closed">全部展开</button></div>'
HOW='<div class="grid g3">'+co('core','<p>每卷先看<b class="k">核心三要点</b>与<b class="k">结构图</b>（彩色条按章数比例绘制），再读背景、目的与基督中心。</p>','先抓骨架')+co('trap','<p>每卷都有<span class="uw">易错点</span>：常见误读、异端或断章取义——这是改革宗正统与其他读法分歧最多的地方。</p>','再避陷阱')+co('conf','<p>卷末<span class="cx">认信连接</span>展开三项联合信条原文（逐字引自 ccifellowship.org），把经文与教义连在一起。</p>','后连信条')+'</div>'+legend_box()
GI={'law-h':'**摩西五经**是全本圣经的根基：==创造—堕落—应许—救赎—立约—律法==。主前^^1446^^年出埃及是旧约年代的锚点；五经教导[[圣约]]的基本语法：神先施恩，再赐律法作为感恩生活的规则。',
'hist-h':'从^^1406 BC^^进迦南到^^430 BC^^尼希米：**得地—士师—王国—分裂—被掳—归回**。前先知书以申命记为标准评判历史；历代志从被掳归回者的角度重述，焦点是**大卫之约与圣殿**。',
'poet-h':'不是按年代，而是**约民如何在日常中与神相交**：受苦（伯）、敬拜（诗）、智慧（箴）、虚空中的敬畏（传）、婚姻之爱（歌）。共同钥句：==敬畏耶和华是智慧的开端==。',
'majp-h':'“大”指篇幅不是重要性。主轴：**审判—被掳—安慰—新约**。以赛亚（^^740–680 BC^^）看见受苦的仆人；耶利米（^^627–580 BC^^）宣告新约（31:31）；以西结与但以理在被掳之地看见神的荣耀与国度。',
'minp-h':'希伯来正典中合为一卷“十二先知书”。三组：**亚述时期**（何珥摩俄拿弥）、**巴比伦时期**（鸿哈番）、**波斯归回后**（该亚玛）。共同主题：!!背约!!必受审判，但神为**余民**保留盼望。',
'gosp-h':'四卷福音书是**一位基督的四幅画像**：马太（君王）、马可（仆人）、路加（人子）、约翰（神子）。约^^主后30^^年（或33年）受难复活是新约的中心事件。',
'acts-h':'路加的第二卷：**升天的基督藉圣灵**把福音从耶路撒冷带到罗马（1:8）。记载^^主后30–62^^年；是保罗书信的历史框架。',
'paul-h':'13 卷按篇幅（非年代）排列：先写给教会（罗—帖后），后写给个人（提前—门）。主线：==因信称义、与基督联合、在圣灵里过感恩的生活==。',
'gen-h':'希伯来书至犹大书：面对**逼迫、假教师、退后的试探**，呼召信徒持守信心、真道与爱。',
'rev-h':'以**旧约意象**写成的预言与书信；**七个循环平行**的异象展示从基督升天到再来的整个教会时代，结局是新天新地。'}
GL={'law-h':' <a class="glink" href="pentateuch.html">⚖️ 五经横向×纵向深度对照 →</a>','hist-h':' <a class="glink" href="history.html">🏛️ 历史书深度对照 →</a>','poet-h':' <a class="glink" href="poetry.html">🎼 诗歌智慧书深度对照 →</a>','majp-h':' <a class="glink" href="prophets.html">🔥 先知书 × 君王时间轴 →</a>','minp-h':' <a class="glink" href="prophets.html#r-tl">🔥 小先知 × 君王时间轴 →</a>','gosp-h':' <a class="glink" href="gospels.html">📗 四福音对照 →</a>','paul-h':' <a class="glink" href="epistles.html">✉️ 书信年代与对照 →</a>','gen-h':' <a class="glink" href="epistles.html#e-h">✉️ 21 封书信横向对照 →</a>'}
def ot():
    c=['''<section class="hero reveal"><div class="chips"><span class="chip g">📜 旧约 39 卷</span><span class="chip">律法5 · 历史12 · 诗歌5 · 大先知5 · 小先知12</span></div><h1>旧约：<em>应许、预表与等候</em></h1><p class="lead">“这经就是为我作见证的”（约5:39）。每卷包含：作者·日期·真实背景·为什么写·结构大纲·核心信息·基督中心·圣约位置·关键经文·难点辨析·应用·记忆口诀·认信连接（三项联合信条原文）。</p></section>''']
    c.append(h2('ot-ov','🗂️','旧约总览'));c.append(h3('ot-map','书卷总图（点击跳转）'))
    c.append(legend(['law','hist','poet','majp','minp'])+canon_grid(lambda b:b['n']<=39))
    c.append(h3('ot-cat','五大类速览'));c.append(table(['分类','书卷','时间范围','主题','口诀'],[['⚖️ 律法书（摩西五经）','创—申','创造—1406 BC','根基：创造、拣选、救赎、立约、律法','创出利民申：“起·出·圣·数·重”'],['🏛️ 历史书','书—斯','1406–430 BC','得地、王国、分裂、被掳、归回','书士得 撒撒王王代代 拉尼斯'],['🎼 诗歌智慧书','伯—歌','（跨越各时期）','在约中如何受苦、敬拜、生活、相爱','伯诗箴传歌：“苦·赞·智·虚·爱”'],['🔥 大先知书','赛—但','740–536 BC','审判与安慰、新约、神的国','赛耶哀结但'],['📯 小先知书','何—玛','约800–430 BC','背约的控诉、耶和华的日子、余民的盼望','何珥摩俄拿弥，鸿哈番该亚玛']]))
    c.append(h3('ot-tanak','希伯来正典的排列（TaNaK）'));c.append(note('📜 希伯来正典的排列（TaNaK）','<p>犹太人的圣经（24 卷，内容与新教 39 卷相同）分为：<span class="key">律法（Torah）</span>、<span class="key">先知（Nevi’im，含约书亚—列王纪“前先知”与以赛亚—小先知“后先知”）</span>、<span class="key">圣卷（Ketuvim，诗篇—历代志）</span>。耶稣说“摩西的律法、先知的书和诗篇”（路24:44），正对应这三部分；“从亚伯的血起，直到……撒迦利亚的血为止”（太23:35）则是从创世记到历代志（希伯来正典最后一卷）。</p>','vio'))
    c.append(bc(4))
    c.append(h3('ot-how','如何使用逐卷卡片'));c.append(HOW)
    c.append(filters(['law','hist','poet','majp','minp'],'.bk'))
    groups={1:('law-h','⚖️ 律法书'),6:('hist-h','🏛️ 历史书'),18:('poet-h','🎼 诗歌智慧书'),23:('majp-h','🔥 大先知书'),28:('minp-h','📯 小先知书')}
    for b in BOOKS[:39]:
        if b['n'] in groups: c.append(h2(groups[b['n']][0],groups[b['n']][1].split(' ')[0],groups[b['n']][1].split(' ')[1])+co('info','<p>'+rich(GI[groups[b['n']][0]],False)+GL.get(groups[b['n']][0],'')+'</p>','本组要旨'))
        c.append(card(b))
    return page('ot.html','旧约39卷',''.join(c),cv=False)
def nt():
    c=['''<section class="hero reveal"><div class="chips"><span class="chip g">✝️ 新约 27 卷</span><span class="chip">福音4 · 历史1 · 保罗13 · 普通8 · 预言1</span></div><h1>新约：<em>应验、实体与差遣</em></h1><p class="lead">“神既在古时藉着众先知多次多方地晓谕列祖，就在这末世藉着他儿子晓谕我们”（来1:1–2）。新约是旧约应许在基督里的成就，也是教会在“已然—未然”之间生活的指南。</p></section>''']
    c.append(h2('nt-ov','🗂️','新约总览'));c.append(h3('nt-map','书卷总图（点击跳转）'))
    c.append(legend(['gosp','acts','paul','gen','rev'])+canon_grid(lambda b:b['n']>39))
    c.append(h3('nt-cat','五大类速览'));c.append(table(['分类','书卷','核心','口诀'],[['✝️ 福音书','太 可 路 约','基督是谁、做了什么','君王·仆人·人子·神子'],['🕊️ 历史','徒','升天基督藉圣灵建立教会','耶路撒冷→犹太撒玛利亚→地极'],['✉️ 保罗书信','罗—门（13）','福音的教义与生活','罗林林加，弗腓西，帖帖提提多门'],['📨 普通书信','来—犹（8）','持守信心、真道与爱','来雅彼彼，约约约犹'],['👑 预言','启','羔羊得胜，万有更新','七教会·七印·七号·七碗']]))
    c.append(h3('synoptic','🔭 四福音：四个视角，一位基督'))
    c.append(table(['','马太','马可','路加','约翰'],[['对象','犹太人','罗马人','希腊人/外邦人','普世信徒'],['基督形象','👑 君王（狮子）','🐂 仆人（牛）','🧑 人子（人）','🦅 神子（鹰）'],['开头','家谱（亚伯拉罕）','施洗约翰','序言+出生','太初有道'],['特色','五大讲论、应验','“立刻”、行动','比喻、祷告、圣灵','七记号、七“我是”'],['钥节','太1:1；28:19','可10:45','路19:10','约20:31']],'cmp'))
    c.append(mer('''flowchart LR
G["✝️ 福音书<br/>基督成就救恩"]-->A["🕊️ 使徒行传<br/>圣灵施行"]-->E["✉️ 书信<br/>救恩的解释与生活"]-->R["👑 启示录<br/>救恩的完成"]
style G fill:#173a5a,stroke:#5ec8ff
style R fill:#4a1d2a,stroke:#ff6b6b''','新约的四段结构'))
    c.append(h3('nt-how','如何使用逐卷卡片'));c.append(HOW)
    c.append(filters(['gosp','acts','paul','gen','rev'],'.bk'))
    groups={40:('gosp-h','✝️ 福音书'),44:('acts-h','🕊️ 使徒行传'),45:('paul-h','✉️ 保罗书信'),58:('gen-h','📨 普通书信'),66:('rev-h','👑 启示录')}
    for b in BOOKS[39:]:
        if b['n'] in groups: c.append(h2(groups[b['n']][0],groups[b['n']][1].split(' ')[0],groups[b['n']][1].split(' ')[1])+co('info','<p>'+rich(GI[groups[b['n']][0]],False)+GL.get(groups[b['n']][0],'')+'</p>','本组要旨'))
        c.append(card(b))
    return page('nt.html','新约27卷',''.join(c),cv=False)
