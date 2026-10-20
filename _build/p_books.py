from lib import *
from books import *
def filters(keys,target):
    return f'<div class="filters" data-target="{target}"><button class="on" data-cat="all">全部</button>'+''.join(f'<button data-cat="{k}">{CATS[k][2]} {CATS[k][0]}</button>' for k in keys)+'<input placeholder="🔍 搜索书卷/主题/经文…" aria-label="搜索书卷"><button data-expand=".bk details" data-state="closed">全部展开</button></div>'
def ot():
    c=['''<section class="hero reveal"><div class="chips"><span class="chip g">📜 旧约 39 卷</span><span class="chip">律法5 · 历史12 · 诗歌5 · 大先知5 · 小先知12</span></div><h1>旧约：<em>应许、预表与等候</em></h1><p class="lead">“这经就是为我作见证的”（约5:39）。每卷包含：作者·日期·真实背景·为什么写·结构大纲·核心信息·基督中心·圣约位置·关键经文·难点辨析·应用·记忆口诀·认信连接（三项联合信条原文）。</p></section>''']
    c.append(h2('ot-map','🗂️','旧约书卷总图（点击跳转）'))
    c.append(legend(['law','hist','poet','majp','minp'])+canon_grid(lambda b:b['n']<=39))
    c.append(table(['分类','书卷','时间范围','主题','口诀'],[['⚖️ 律法书（摩西五经）','创—申','创造—1406 BC','根基：创造、拣选、救赎、立约、律法','创出利民申：“起·出·圣·数·重”'],['🏛️ 历史书','书—斯','1406–430 BC','得地、王国、分裂、被掳、归回','书士得 撒撒王王代代 拉尼斯'],['🎼 诗歌智慧书','伯—歌','（跨越各时期）','在约中如何受苦、敬拜、生活、相爱','伯诗箴传歌：“苦·赞·智·虚·爱”'],['🔥 大先知书','赛—但','740–536 BC','审判与安慰、新约、神的国','赛耶哀结但'],['📯 小先知书','何—玛','约800–430 BC','背约的控诉、耶和华的日子、余民的盼望','何珥摩俄拿弥，鸿哈番该亚玛']]))
    c.append(note('📜 希伯来正典的排列（TaNaK）','<p>犹太人的圣经（24 卷，内容与新教 39 卷相同）分为：<span class="key">律法（Torah）</span>、<span class="key">先知（Nevi’im，含约书亚—列王纪“前先知”与以赛亚—小先知“后先知”）</span>、<span class="key">圣卷（Ketuvim，诗篇—历代志）</span>。耶稣说“摩西的律法、先知的书和诗篇”（路24:44），正对应这三部分；“从亚伯的血起，直到……撒迦利亚的血为止”（太23:35）则是从创世记到历代志（希伯来正典最后一卷）。</p>','vio'))
    c.append(bc(4))
    c.append(h2('ot-books','📚','逐卷解读（39 卷）'))
    c.append(filters(['law','hist','poet','majp','minp'],'.bk'))
    groups={1:('law-h','⚖️ 律法书'),6:('hist-h','🏛️ 历史书'),18:('poet-h','🎼 诗歌智慧书'),23:('majp-h','🔥 大先知书'),28:('minp-h','📯 小先知书')}
    for b in BOOKS[:39]:
        if b['n'] in groups: c.append(h2(groups[b['n']][0],groups[b['n']][1].split(' ')[0],groups[b['n']][1].split(' ')[1]))
        c.append(card(b))
    return page('ot.html','旧约39卷',''.join(c))
def nt():
    c=['''<section class="hero reveal"><div class="chips"><span class="chip g">✝️ 新约 27 卷</span><span class="chip">福音4 · 历史1 · 保罗13 · 普通8 · 预言1</span></div><h1>新约：<em>应验、实体与差遣</em></h1><p class="lead">“神既在古时藉着众先知多次多方地晓谕列祖，就在这末世藉着他儿子晓谕我们”（来1:1–2）。新约是旧约应许在基督里的成就，也是教会在“已然—未然”之间生活的指南。</p></section>''']
    c.append(h2('nt-map','🗂️','新约书卷总图（点击跳转）'))
    c.append(legend(['gosp','acts','paul','gen','rev'])+canon_grid(lambda b:b['n']>39))
    c.append(table(['分类','书卷','核心','口诀'],[['✝️ 福音书','太 可 路 约','基督是谁、做了什么','君王·仆人·人子·神子'],['🕊️ 历史','徒','升天基督藉圣灵建立教会','耶路撒冷→犹太撒玛利亚→地极'],['✉️ 保罗书信','罗—门（13）','福音的教义与生活','罗林林加，弗腓西，帖帖提提多门'],['📨 普通书信','来—犹（8）','持守信心、真道与爱','来雅彼彼，约约约犹'],['👑 预言','启','羔羊得胜，万有更新','七教会·七印·七号·七碗']]))
    c.append(h3('synoptic','🔭 四福音：四个视角，一位基督'))
    c.append(table(['','马太','马可','路加','约翰'],[['对象','犹太人','罗马人','希腊人/外邦人','普世信徒'],['基督形象','👑 君王（狮子）','🐂 仆人（牛）','🧑 人子（人）','🦅 神子（鹰）'],['开头','家谱（亚伯拉罕）','施洗约翰','序言+出生','太初有道'],['特色','五大讲论、应验','“立刻”、行动','比喻、祷告、圣灵','七记号、七“我是”'],['钥节','太1:1；28:19','可10:45','路19:10','约20:31']],'cmp'))
    c.append(mer('''flowchart LR
G["✝️ 福音书<br/>基督成就救恩"]-->A["🕊️ 使徒行传<br/>圣灵施行"]-->E["✉️ 书信<br/>救恩的解释与生活"]-->R["👑 启示录<br/>救恩的完成"]
style G fill:#173a5a,stroke:#5ec8ff
style R fill:#4a1d2a,stroke:#ff6b6b''','新约的四段结构'))
    c.append(h2('nt-books','📚','逐卷解读（27 卷）'))
    c.append(filters(['gosp','acts','paul','gen','rev'],'.bk'))
    groups={40:('gosp-h','✝️ 福音书'),44:('acts-h','🕊️ 使徒行传'),45:('paul-h','✉️ 保罗书信'),58:('gen-h','📨 普通书信'),66:('rev-h','👑 启示录')}
    for b in BOOKS[39:]:
        if b['n'] in groups: c.append(h2(groups[b['n']][0],groups[b['n']][1].split(' ')[0],groups[b['n']][1].split(' ')[1]))
        c.append(card(b))
    return page('nt.html','新约27卷',''.join(c))
