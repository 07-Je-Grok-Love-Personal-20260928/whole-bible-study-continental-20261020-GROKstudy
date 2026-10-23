import json,random
from lib import *
from v5extra import *
from books import *
from kings import *
def index():
    c=[]
    c.append(f'''<section class="hero img reveal" style="background-image:linear-gradient(90deg,rgba(7,11,26,.85),rgba(7,11,26,.35) 60%,rgba(7,11,26,.1)),url(assets/img/hero.svg);min-height:clamp(380px,58vh,560px);display:flex;flex-direction:column;justify-content:center">
<div class="chips"><span class="chip g">📖 GROKstudy {V}</span><span class="chip">🗓️ {DATE}</span><span class="chip">欧陆改革宗 · 三项联合信条</span><span class="chip">三大普世信经</span></div>
<h1>整本《圣经》<br><em>从伊甸园到新耶路撒冷</em></h1>
<p class="lead">时间线 · 故事线 · 地理 · 真实背景 · 文化区域 · 诸王与时代 · 圣经神学 · 圣约神学 · 66 卷逐卷解读 · 信经背诵 · 记忆测验——以<span class="key">比利时信条、海德堡要理问答、多特信经</span>为认信框架，信条与信经原文逐字取自 ccifellowship.org。</p>
<div class="chips" style="margin-top:8px"><a class="btn on" href="story.html">🧭 从整体开始</a><a class="btn" href="timeline.html">⏳ 时间线·诸王</a><a class="btn" href="ot.html">📜 旧约39卷</a><a class="btn" href="nt.html">✝️ 新约27卷</a><a class="btn" href="creeds.html">🕊️ 背诵信经</a></div></section>''')
    stats=[('66','卷书','📚'),('42','位君王（3+19+20）','👑'),('8','幅交互地图','🗺️'),('6','个历史之约','🤝'),('3+3','信经·信条全文','🕊️'),('60+','测验与闪卡','🧠')]
    c.append('<div class="grid g6 reveal">'+''.join(f'<div class="card tile" style="text-align:center"><div class="big">{i}</div><h4 class="shimmer" style="font-size:26px">{n}</h4><p>{t}</p></div>' for n,t,i in stats)+'</div>')
    c.append(legend_box(True))
    c.append(h2('path','🛤️','学习路线：先整体，再局部，最后记牢'))
    c.append(h3('mods',f'{len(GROUPS)} 组 {len(PAGES)} 个学习模块（编号＝全站导航）'))
    GD={'index.html':'书架总图 + 66 卷逐卷解读（旧约 39 · 新约 27）','overview.html':'学习路线、66 卷色图、一页纸、标注系统','story.html':'四幕剧、十二场景、女人后裔红线、七条圣经神学主题','covenant.html':'救赎之约·行为之约·恩典之约；六个历史之约；律法三用','timeline.html':'11 时代、8 钉子年份、42 位君王全表与年代图','geography.html':'8 幅交互地图：近东、族长、出埃及、王国、帝国、耶稣、保罗',
     'ot.html':'旧约 39 卷逐卷 13 项解读 + 认信连接','nt.html':'新约 27 卷逐卷 13 项解读 + 认信连接','pentateuch.html':'五卷故事线、律法与约的递进、会幕与五祭、托勒多、申命记=条约','history.html':'得地→士师循环→王国→被掳→归回；两种史观','poetry.html':'希伯来平行体、诗篇五卷、敬畏耶和华、伯/箴/传三角度','prophets.html':'17 位先知 × 君王 × 帝国时间轴、弥赛亚预言链、耶和华的日子','gospels.html':'四幅肖像、41 段落对照、神迹比喻、符类问题','epistles.html':'21 封书信 × 使徒行传年代、称义/教会/末世、罗↔加↔雅',
     'life-of-christ.html':'48 事件 × 地图联动、受难周逐日、三职二状态','kings-chronicles.html':'两种眼光、42 王逐王对照、双轨时间线、口诀','compare.html':'10 组以经解经：创↔启、利↔来、雅↔罗……','stats.html':'章节数、类别、作者、旧约引用、文体组统计',
     'creeds.html':'背诵版、遮盖背诵、三份信经深度对比','forms.html':'比利时信条 37 条、海德堡 52 主日 129 问、多特信经','memory.html':'口诀总表、闪卡、选择题、排序游戏','sources.html':'逐字来源、核对报告、推荐网站'}
    for g,gn,gi,ps in GROUPS:
        c.append(f'<div class="modg rv"><b class="modgh"><span class="gn">{GCIRC[int(g)-1]}</span> {gi} {gn}</b><div class="grid g3">'+''.join(f'<a class="card tile" href="{f}"><div class="big">{i}</div><h4><span class="pnb">{PNUM[f]}</span> {t}</h4><p>{GD.get(f,d)}</p></a>' for f,i,t,d in ps)+'</div></div>')
    c.append(h2('canon','🌈','66 卷颜色地图'))
    c.append(h3('canon-grid','色块总图（颜色 = 文体分类，点击进入该卷）'))
    c.append(legend(list(CATS.keys()))+canon_grid())
    c.append(h3('canon-ch','📏 章数比例条：66 卷一眼看出厚薄'))
    c.append(canonbars())
    c.append(h3('canon-bar','比例条：每类各几卷'))
    sizes=[('law',5),('hist',12),('poet',5),('majp',5),('minp',12),('gosp',4),('acts',1),('paul',13),('gen',8),('rev',1)]
    c.append('<div class="bar" style="height:22px;margin-top:14px">'+''.join(f'<span title="{CATS[k][0]} {n}" style="width:{n/66*100:.2f}%;background:{CATS[k][1]}"></span>' for k,n in sizes)+'</div><p class="srcline">比例条：旧约 5+12+5+5+12=39；新约 4+1+13+8+1=27 —— 口诀 <span class="mn">“旧约 5-12-5-5-12，新约 4-1-13-8-1”</span></p>')
    c.append(h2('onepage','📄','整本圣经一页纸'))
    c.append(h3('onepage-t','十一阶段一页表'))
    c.append(table(['阶段','书卷','一句话','圣约','基督'],[['创造与堕落','创1–11','神创造，人堕落，神应许','行为之约→恩典之约宣告（3:15）；挪亚之约','女人的后裔'],['族长','创12–50','神拣选亚伯拉罕一家','亚伯拉罕之约','亚伯拉罕的后裔'],['出埃及与律法','出—申','神救赎并与以色列立约','摩西之约','逾越节羔羊、大祭司'],['得地与士师','书—得','得地、背道、需要王','—','真约书亚、至亲救赎者'],['王国','撒上—代下','大卫之约、圣殿、分裂、灭亡','大卫之约','大卫的子孙'],['先知','赛—玛','审判与新约的应许','新约应许','受苦的仆人、人子'],['归回','拉—斯；该亚玛','余民归回，等候','—','后来的荣耀'],['基督','太—约','应许成就','新约设立','道成肉身、十字架、复活'],['教会','徒—犹','福音到地极','新约施行','升天作王、浇灌圣灵'],['成全','启','羔羊得胜，新天新地','约的完成','阿拉法、俄梅戛']]))
    c.append(h3('comfort','唯一的安慰（海德堡第1问）'))
    c.append(hc(1,open_=True))
    c.append(h2('emsys','🎨','笔记式标注系统（全站通用）'))
    c.append(h3('em-legend','颜色编码图例'))
    c.append(LEGEND_EM)
    c.append(h3('em-demo','六种笔记框示范'))
    c.append('<div class="grid g3">'+co('core','<p>'+rich('整本圣经的中心是==在基督里的恩典之约==：**一位中保、一个应许、一种得救之法**（因信）。',False)+'</p>')+co('xc','<p>'+rich('“于是从摩西和众先知起，凡经上所指着自己的话都给他们讲解明白了”（路24:27）——**每卷书都通向基督**。',False)+'</p>')+co('hardc','<p>'+rich('南北国王年代**加总超出**实际年数：因^^共治^^与**登基年/非登基年**两种计年法（Thiele）。',False)+'</p>')+co('trap','<p>'+rich('!!“旧约讲律法、新约讲恩典”!!——两约都有律法与福音；西奈之约以“我是耶和华你的神，曾将你从埃及地……领出来”开头（出20:2）。',False)+'</p>')+co('mnc','<p class="mn">“一四四六出埃及，九六六年把殿立；九三一年国分裂，七二二北、五八六南”</p>')+co('app','<p>'+rich('%%每读一卷书问三问%%：神在这里**启示了自己什么**？人**需要什么**？**基督**如何成全？',False)+'</p>')+'</div>')
    c.append(h3('em-era','救赎历史年代色带'))
    from p_timeline import ERAS
    c.append('<div class="era rv">'+''.join(f'<a href="timeline.html#eras" style="--c:{col}"><b>{n}</b>{y}</a>' for n,r,col,y in ERAS)+'</div>')
    return page('overview.html','全景总览',''.join(c))
def memory():
    c=['''<section class="hero reveal"><div class="chips"><span class="chip g">🧠 记忆·测验</span><span class="chip">口诀 · 闪卡 · 选择题 · 排序游戏</span></div><h1>把学到的<em>钉牢在心里</em></h1><p class="lead">记忆科学：<span class="key">提取练习</span>（自测）比重复阅读有效得多；<span class="key">间隔重复</span>（1-3-7-14 天）；<span class="key">颜色与图像编码</span>；<span class="key">串联故事</span>。</p></section>''']
    c.append(h2('mn','🪝','口诀：先挂钩'))
    c.append(h3('quick66','📋 66 卷一句话 + 必背经文'))
    c.append(bookquick())
    c.append(h3('mn-all','66 卷记忆口诀总表'))
    c.append(table(['#','书卷','一句话','口诀'],[[str(b['n']),f'<a href="{"ot" if b["n"]<=39 else "nt"}.html#b-{b["id"]}" style="color:{CATS[b["cat"]][1]}">{b["name"]}</a>',E(b['one']),f'<span class="mn">{E(b["mn"])}</span>'] for b in BOOKS]))
    cards=[('1446','出埃及（王上6:1：966建殿前480年）'),('931','国分为二：罗波安 vs 耶罗波安'),('722','北国撒玛利亚亡于亚述'),('586','耶路撒冷与圣殿毁于巴比伦'),('538','古列谕令，第一批归回'),('516','第二圣殿完成'),('444','尼希米修城墙（52天）'),('605','第一次被掳（但以理）'),('597','第二次被掳（以西结、约雅斤）'),('行为之约','神与亚当：顺服得生（何6:7；罗5）'),('恩典之约','神与信者及其儿女，中保基督；创3:15首次宣告'),('挪亚之约记号','彩虹'),('亚伯拉罕之约记号','割礼 → 新约：洗礼'),('大卫之约','永远的家、国、位（撒下7）'),('新约','律法写在心上（耶31:31–34；路22:20）'),('homoousios','“与父同质”——尼西亚驳亚流'),('filioque','“和子”——圣灵从父和子而出'),('亚他那修信经两部分','3–28 三一；29–41 基督两性'),('海德堡三部曲','愁苦 Q3–11 · 拯救 Q12–85 · 感恩 Q86–129'),('比利时信条','1561，德布利，37条'),('多特信经','1618–19，驳抗辩派五点'),('犹大八善王','亚撒、约沙法、约阿施、亚玛谢、乌西雅、约坦、希西家、约西亚'),('北国九朝代','耶罗波安、巴沙、心利、暗利、耶户、沙龙、米拿现、比加、何细亚'),('旧约 5-12-5-5-12','律法、历史、诗歌、大先知、小先知')]
    c.append(h2('recall','🃏','主动回忆：闪卡与自测'))
    c.append(h3('cards','闪卡（点击翻面）'))
    c.append('<p><button class="btn" data-shuffle="#fcg">🔀 洗牌</button></p><div class="grid" id="fcg">'+''.join(f'<div class="fc"><div class="in"><div class="f">{E(a)}</div><div class="b">{E(b)}</div></div></div>' for a,b in cards)+'</div>')
    Q=[('出埃及的保守年代是？',['1446 BC','1260 BC','1876 BC','966 BC'],0,'王上6:1：所罗门第四年（966）前480年。'),('国分裂的年份是？',['931 BC','722 BC','1010 BC','586 BC'],0,'罗波安与耶罗波安（王上12）。'),('北国以色列亡于哪个帝国？',['亚述','巴比伦','波斯','埃及'],0,'722年撒玛利亚陷落（王下17）。'),('哪位犹大王发现律法书并推行改革？',['约西亚','希西家','亚撒','约沙法'],0,'622年（王下22–23）。'),('北国有几位王是“善王”？',['0','2','8','19'],0,'全部“行耶和华眼中看为恶的事”。'),('哪位是唯一统治犹大的女王（篡位者）？',['亚她利雅','耶洗别','以斯帖','底波拉'],0,'王下11。'),('以赛亚在哪位王崩的那年蒙召？',['乌西雅','希西家','亚哈斯','约坦'],0,'赛6:1。'),('“义人必因信得生”出自哪位先知？',['哈巴谷','阿摩司','约珥','玛拉基'],0,'哈2:4 → 罗1:17；加3:11。'),('“新约”的应许最明确在哪卷？',['耶利米书31章','以西结书40章','但以理书9章','以赛亚书7章'],0,'耶31:31–34；来8:8–12。'),('第二圣殿完成于？',['516 BC','538 BC','586 BC','444 BC'],0,'拉6:15。'),('尼西亚信经驳斥的主要异端是？',['亚流主义','诺斯底主义','伯拉纠主义','阿米念主义'],0,'子“受生却非被造，与父同质”。'),('哪个信经包含“其位格不紊，其本质不分”？',['亚他那修信经','使徒信经','尼西亚信经','比利时信条'],0,'第4节。'),('比利时信条第几条明确接受三大信经？',['第9条','第1条','第27条','第37条'],0,'论三位一体的圣经依据。'),('海德堡要理问答第1问的主题是？',['唯一的安慰','神的律法','圣礼','祷告'],0,'或生或死，我属于信实的救主耶稣基督。'),('多特信经回应的是？',['阿米念派（抗辩派）','罗马天主教','重洗派','路德宗'],0,'1618–1619 多特大会。'),('亚伯拉罕之约的记号是？',['割礼','彩虹','安息日','圣餐'],0,'创17；罗4:11。'),('“耶和华是我的牧者”出自？',['诗篇23篇','以赛亚书40章','约翰福音10章','以西结书34章'],0,'诗23:1。'),('保罗在哪城写了罗马书？',['哥林多','以弗所','罗马','安提阿'],0,'约主后57年（罗16:23）。'),('“我的恩典够你用的”出自？',['哥林多后书12:9','腓立比书4:13','罗马书8:28','加拉太书2:20'],0,'软弱中的能力。'),('启示录写于哪位皇帝时期（保守观点）？',['多米田','尼禄','奥古斯都','提庇留'],0,'约主后95年。'),('哪卷书全书没有出现“神”字？',['以斯帖记','路得记','雅歌','约拿书'],0,'隐藏的护理。'),('“人子”驾云而来得国度出自？',['但以理书7章','以西结书1章','撒迦利亚书14章','玛拉基书3章'],0,'但7:13–14；可14:62。'),('统一王国三王各作王多少年？',['各40年','各20年','各33年','各52年'],0,'徒13:21；王上2:11；11:42。'),('哪位犹大王在位最久（55年）？',['玛拿西','乌西雅','亚撒','约阿施'],0,'王下21:1。')]
    for q in Q: pass
    qs=''
    for i,(q,opts,a,ex) in enumerate(Q):
        order=list(range(4)); random.Random(i*7+3).shuffle(order)
        btn=''.join(f'<button data-k="{k}">{"ABCD"[j]}. {E(opts[k])}</button>' for j,k in enumerate(order))
        qs+=f'<div class="q card" data-a="{a}"><b>Q{i+1}. {E(q)}</b><div class="opts">{btn}</div><p class="ex hidden srcline">💡 {E(ex)}</p></div>'
    c.append(h3('quiz','选择题自测（24 题）'))
    c.append(f'<div class="quiz"><p><span class="score">得分 0 / {len(Q)}</span> <button class="btn" data-reset>🔄 重来</button></p><div class="grid g2">{qs}</div></div>')
    c.append(h2('games','🎮','游戏与填空'))
    c.append(h3('q-kings','排序小游戏（按正确次序点击）'))
    games=[('犹大八位善王（按年代）',['亚撒','约沙法','约阿施','亚玛谢','乌西雅','约坦','希西家','约西亚']),('统一王国与分裂（按年代）',['扫罗','大卫','所罗门','罗波安','亚比央','亚撒']),('八个钉子年份（由早到晚）',['2091','1446','1010','966','931','722','586','538']),('六个历史之约',['亚当（行为之约）','挪亚','亚伯拉罕','摩西','大卫','新约']),('摩西五经',['创世记','出埃及记','利未记','民数记','申命记']),('保罗书信（正典次序）',['罗马书','哥林多前书','哥林多后书','加拉太书','以弗所书','腓立比书','歌罗西书','帖撒罗尼迦前书','帖撒罗尼迦后书','提摩太前书','提摩太后书','提多书','腓利门书']),('小先知书（正典次序）',['何西阿书','约珥书','阿摩司书','俄巴底亚书','约拿书','弥迦书','那鸿书','哈巴谷书','西番雅书','哈该书','撒迦利亚书','玛拉基书']),('北国最后五王',['米拿现','比加辖','比加','何细亚','（722 亡国）'])]
    c.append('<div class="grid g2">'+''.join(f'''<div class="card ordgame" data-seq='{json.dumps(seq,ensure_ascii=False)}'><h4>🎯 {t} <button class="btn" data-restart style="float:right">↻</button></h4><div class="ord"></div><p class="ans" style="color:var(--emer);min-height:1.6em"></p><p class="msg srcline"></p></div>''' for t,seq in games)+'</div>')
    c.append(h3('fill','信经填空（先想，再点开）'))
    fills=[('使徒信经','我信神，全能的父，____的主。','创造天地'),('使徒信经','因圣灵感孕，从____所生','童贞女马利亚'),('尼西亚信经','受生却非被造，与父____','同质'),('尼西亚信经','我们信圣灵，____的主','赐生命'),('亚他那修信经','其位格不紊，其本质____','不分'),('亚他那修信经','他是一位，并非因两质相混，乃是因神人二性合于一个____','位格')]
    c.append('<div class="grid g3">'+''.join(f'<details class="dx"><summary>🕊️ {t}：{E(q)}</summary><div class="in"><p class="key">{E(a)}</p></div></details>' for t,q,a in fills)+'</div>')
    for t,q,a in fills: assert q.replace('____',a).replace('……','') in {'使徒信经':CR['apostles']['text'],'尼西亚信经':CR['nicene']['text'],'亚他那修信经':CR['athanasian']['text']}[t], q
    c.append(h2('plan','📅','计划：两周记忆计划'))
    c.append(table(['天','内容','方法'],[['1','整体：四幕剧 + 11 时代','画出来，讲给别人听'],['2','8 个钉子年份','闪卡 + 排序游戏'],['3','统一王国 + 北国 9 朝代','口诀 + 年代图'],['4','犹大 8 善王 + 两大复兴','排序游戏'],['5','六个历史之约','圣约链流程图'],['6','律法书 + 历史书','口诀表'],['7','复习 1–6 天','选择题'],['8','诗歌书 + 大先知','关键经文'],['9','小先知（与诸王对照）','先知—君王表'],['10','福音书 + 使徒行传','四福音对照'],['11','书信 + 启示录','口诀表'],['12','使徒信经背诵','遮盖模式'],['13','尼西亚信经背诵','遮盖模式'],['14','亚他那修信经（前半）+ 总复习','填空 + 测验']]))
    return page('memory.html','记忆·测验',''.join(c))
def sources():
    import os
    lv=json.load(open(HERE+'/data/verify/creeds_live_verify.json')); sp=json.load(open(HERE+'/data/verify/forms_live_spotcheck.json'))
    pdf=json.load(open(HERE+'/data/verify/pdf2015.json'))
    c=['''<section class="hero reveal"><div class="chips"><span class="chip g">🔗 资料来源</span><span class="chip">引用核对报告</span></div><h1>资料来源与<em>核对报告</em></h1><p class="lead">诚实标注：本站哪些是逐字引用、哪些是作者综述，以及如何核对。</p></section>''']
    c.append(h2('primary','📌','逐字引用来源（唯一来源）'))
    c.append(table(['文献','网址','本站处理'],[['使徒信经',f'<a href="{CR["apostles"]["url"]}" target="_blank" rel="noopener">{CR["apostles"]["url"]}</a>','全文逐字'],['尼西亚信经',f'<a href="{CR["nicene"]["url"]}" target="_blank" rel="noopener">{CR["nicene"]["url"]}</a>','全文逐字'],['亚他那修信经',f'<a href="{CR["athanasian"]["url"]}" target="_blank" rel="noopener">{CR["athanasian"]["url"]}</a>','全文逐字'],['比利时信条',f'<a href="https://ccifellowship.org/books/book-of-praise/confessions/the-belgic-confession" target="_blank" rel="noopener">ccifellowship.org/…/the-belgic-confession</a>','37 条全文逐字（含脚注号与经文）'],['海德堡要理问答',f'<a href="{HC["url"]}" target="_blank" rel="noopener">{HC["url"]}</a>','52 主日 129 问全文逐字'],['多特信经',f'<a href="{DT["url"]}" target="_blank" rel="noopener">{DT["url"]}</a>','4 部分全部条文及错谬反驳逐字']]))
    c.append(h2('verify','🔬','核对报告（2026-10-20）'))
    c.append(table(['项目','结果'],[[f'三大信经 vs 在线页面（{k}）',f'段落 {v["found_live"]}/{v["paragraphs"]} 一致 {"✅" if v["all"] else "⚠️"}'] for k,v in lv.items()]+[[f'抽查 {x["kind"]} · {x["url"].split("/")[-1]}',f'句段 {x["found"]}/{x["segments"]} 一致 {"✅" if x["found"]==x["segments"] else "⚠️"}'] for x in sp]+[['正文中的短引用',f'构建时自动校验：{len(QUOTES)} 处短引用均为原文子串（否则构建失败）'],['计数','比利时信条 37 条；海德堡 52 主日 129 问；多特信经 4 部分（第一项 18 条+驳斥，第二项 9 条+驳斥，第三四项 17 条+驳斥，第五项 15 条+驳斥）']]))
    c.append(note('ℹ️ 网站原貌说明（照录不改）','<ul><li>网站将亚他那修信经正文编号至 42)，而网站介绍文字称第二部分为“第29-43点”。</li><li>比利时信条第9条写作《亚他拿修信经》，信经页面标题为《亚他那修信经》——两种译名并存，本站各按原处照录。</li><li>海德堡第88、123问在网站上有脚注号但无经文列表；第25、47、63问经文条目比脚注号多一条；第23、24、71、77问无脚注。</li><li>多特信经网站无单独序言/结语页面。</li></ul>'))
    rows=[[d['label'],str(d['page']),E(d['cci']),E(d['pdf']),d['kind']] for d in pdf['diffs'] if d['doc']=='creeds']
    c.append(h3('pdf','📕 与用户附件《中国改革宗教会敬拜手册》（2015版）交叉比对：三大信经差异'))
    c.append(f'<p>整体相似度：信经 {pdf["ratio"]["creeds"]}，比利时信条 {pdf["ratio"]["bc"]}，海德堡 {pdf["ratio"]["hc"]}，多特 {pdf["ratio"]["dort"]}。差异多为写法（如“400年/四百年”、“·”间隔号）或个别用词；本站一律以 ccifellowship.org 为准。</p>')
    c.append(table(['信经','PDF页','ccifellowship.org（本站采用）','2015 手册','类型'],rows))
    c.append(h2('refs','📚','参考网站（供延伸学习；本站未从中作逐字引用）'))
    R=[('https://ccifellowship.org','中国改革宗教会（CCI）','信经、信条、海德堡讲道（52主日）、经文证道、疑难解答'),('https://www.ccreformed.org','洛杉矶改革宗·恩约教会','中文改革宗讲道与教导'),('https://www.reformedbeginner.net','改革宗初学者','入门文章与信条导读'),('https://canrc.org','Canadian Reformed Churches','欧陆改革宗（荷兰解放派传统），Book of Praise'),('https://www.urcna.org','United Reformed Churches in North America','三项联合信条'),('https://heritagereformed.com','Heritage Reformed Congregations','荷兰第二次改教（Nadere Reformatie）传统'),('https://www.prca.org','Protestant Reformed Churches in America','三项联合信条；圣约论述'),('https://opc.org','Orthodox Presbyterian Church','威斯敏斯特信仰准则（opc.org/wcf.html 等）'),('https://canadianreformedseminary.ca','Canadian Reformed Theological Seminary','欧陆改革宗神学教育'),('https://crts.edu','CRTS','神学院资源'),('https://www.wts.edu','Westminster Theological Seminary','霍志恒圣经神学传统')]
    c.append('<div class="grid g3">'+''.join(f'<a class="card tile" href="{u}" target="_blank" rel="noopener"><div class="big">🔗</div><h4>{n}</h4><p>{d}<br><small>{u}</small></p></a>' for u,n,d in R)+'</div>')
    c.append(h2('method','🧪','年代与资料方法'))
    c.append('<ul><li>旧约诸王年代：Edwin R. Thiele 系统（及 McFall 修订），与保守派研读本（如 ESV/改革宗研读本）一致；个别年份 ±1 年。</li><li>出埃及采“早期说”1446年（王上6:1）。</li><li>耶稣受难年取 AD 30 或 33 两说并列。</li><li>地图：Natural Earth 海岸线（公有领域）+ 手工标注；古代地点坐标为通行考古识别，部分存争议（已标注）。</li><li>经文：和合本。</li><li>书卷解读、口诀、图表为本站作者依改革宗正统立场综述，不属逐字引文；凡逐字引文均以紫色框/“逐字”标签标出并链接原页。</li></ul>')
    c.append(h3('v6src','v6 统计与学术资料'))
    c.append(table(['用途','来源','用在'],[['经节数（66 卷，31,102 节）','<a href="https://www.biblesupersearch.com/2019/02/the-number-of-verses-in-the-bible/" target="_blank" rel="noopener">Bible SuperSearch：The Number of Verses in the Bible（2019，KJV 分节）</a>','<a href="stats.html">圣经统计</a>'],
      ['旧约在新约中的引用（224 / 295 / 352 节 / 278 节）','<a href="https://thirdmill.org/articles/rog_nicole/rog_nicole.NT_OT.html" target="_blank" rel="noopener">Roger Nicole, “New Testament Use of the Old Testament” (1958)</a>','<a href="stats.html">圣经统计</a>'],
      ['四福音独有材料比例（约值）','B. F. Westcott, <i>An Introduction to the Study of the Gospels</i> (1860)','<a href="gospels.html">四福音对照</a>'],
      ['基督生平年代（AD 30 / AD 33）','保守派年代学；Harold W. Hoehner, <i>Chronological Aspects of the Life of Christ</i> (1977)','<a href="life-of-christ.html">基督生平</a>']]))
    return page('sources.html','资料来源',''.join(c))
