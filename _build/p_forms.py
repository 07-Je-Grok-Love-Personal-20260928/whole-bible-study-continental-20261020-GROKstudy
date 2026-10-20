from lib import *
def ipar(t): return ''.join(f'<p>{E(p.strip())}</p>' for p in t.split('\n\n') if p.strip())
def build():
    c=[]
    c.append('''<section class="hero reveal"><div class="chips"><span class="chip g">📚 三项联合信条</span><span class="chip">比利时信条 37 条</span><span class="chip">海德堡要理问答 52 主日 129 问</span><span class="chip">多特信经 4 部分（5 项教义）</span></div>
<h1>三项联合信条：<em>欧陆改革宗的认信根基</em></h1><p class="lead">全文逐字引自 ccifellowship.org《赞美诗集·信条》栏目（中国改革宗教会），上标数字为原脚注序号，下方为经文出处。本页可作为整本圣经学习的“教义索引”：66 卷书页面中的“认信连接”都链接到这里的条目原文。</p></section>''')
    c.append(legend_box())
    c.append(h2('overview','🧭','三份信条总览'))
    c.append(h3('ov-table','一览对照表'))
    c.append(table(['','比利时信条','海德堡要理问答','多特信经'],[
     ['年代','1561（多特会议1619修订采纳）','1563','1618–1619'],['作者/来源','德布利（Guido de Brès），殉道于1567','乌尔西努、俄利维亚努（腓德烈三世委托）','多特国际总会（含27位外国代表）'],
     ['文体','信仰告白（“我们相信……”）','问答式教理（“你唯一的安慰是什么？”）','教会法规式教义+错谬反驳'],
     ['结构','神论—圣经—三一—创造—罪—基督—救恩—教会—圣礼—政府—末世','愁苦（Q3–11）—拯救（Q12–85）—感恩（Q86–129）','拣选与弃绝｜基督之死｜败坏与归正｜圣徒蒙保守'],
     ['处境','向逼迫的政府表明改革宗信徒是守法的真基督徒','教导青年与会众；每主日讲解','回应阿米念派“抗辩五点”'],
     ['语调','护教的、全面的','温暖的、个人的、敬虔的','精确的、牧养的（多次提醒以安慰教导拣选）'],
     ['与圣经全局','系统神学纲要','福音的“三部曲”','救恩施行的恩典教义']],'cmp'))
    c.append(h3('ov-hc3','海德堡三部曲结构图'))
    c.append(mer('''flowchart LR
subgraph HC["海德堡要理问答：唯一的安慰（Q1–2）"]
direction LR
M["😢 愁苦<br/>Q3–11<br/>律法显明罪"]-->R["✝️ 拯救<br/>Q12–85<br/>中保·信经·称义·圣礼"]-->G["🙏 感恩<br/>Q86–129<br/>归正·十诫·祷告"]
end
style M fill:#4a1d2a,stroke:#ff6b6b
style R fill:#173a5a,stroke:#5ec8ff
style G fill:#173f2f,stroke:#3ee0a1''','海德堡要理问答三部曲——与罗马书结构（1–3罪；3–11救恩；12–16感恩）一致'))
    c.append(h3('ov-mn','口诀与易错'))
    c.append(co('trap','<p>'+rich("!!把 TULIP 当作多特信经的原始结构!!——多特原为**四部分（五项教义）**，顺序是拣选→救赎→败坏与归正→保守；TULIP 是后来英语世界的记忆法。!!以为“有限的救赎”指基督的死价值有限!!——多特第二项教义第3条说基督之死{{DT1_3|具有无限的价值，足以补赎普天下人所犯的一切罪}}；“限定”指**神的意图与果效**（第8条：有效地救赎所有被拣选的人）。",False)+'</p>'))
    c.append(note('🧠 口诀','<p><span class="mn">“比37、海129、多4（5）”</span>；海德堡三部曲 <span class="mn">“罪—救—谢”</span>；多特五点 <span class="mn">“全无限不圣”</span>（全然败坏、无条件拣选、限定的救赎（特定救赎）、不可抗拒的恩典、圣徒蒙保守；英文 TULIP 依多特原顺序则为 U-L-T/I-P）。</p>','gold'))
    # Belgic
    c.append(h2('belgic','📗','比利时信条（全文）'))
    c.append(f'<details class="dx"><summary>📖 网站介绍（逐字）</summary><div class="in"><div class="conf">{ipar(BC["intro"])}</div></div></details>')
    groups=[('神与圣经',1,7),('三位一体',8,11),('创造、护理与罪',12,15),('拣选与拯救：基督',16,21),('称义与成圣',22,26),('教会',27,32),('圣礼',33,35),('政府与末世',36,37)]
    c.append('<div style="margin:8px 0"><button class="btn" data-expand="#belgic-wrap details">全部展开</button></div><div id="belgic-wrap">')
    for g,a,b in groups:
        c.append(h3(f'bc-g{a}',f'比利时信条 第{a}–{b}条 · {g}'))
        for n in range(a,b+1): c.append(bc(n).replace('<summary>📗 比利时信条 '+E(BCA[n]['title'])+'</summary>','<summary><h4 class="h nonum" id="bc-a'+str(n)+'">📗 '+E(BCA[n]['title'])+'</h4></summary>',1))
    c.append('</div>')
    # HC
    c.append(h2('heidelberg','📘','海德堡要理问答（全文，52 主日）'))
    c.append(f'<details class="dx"><summary>📖 网站介绍（逐字）</summary><div class="in"><div class="conf">{ipar(HC["intro"])}</div></div></details>')
    parts={1:'引言：唯一的安慰',2:'第一部分：人的罪恶和愁苦',5:'第二部分：人的得救',32:'第三部分：人的感恩'}
    c.append('<div style="margin:8px 0"><button class="btn" data-expand="#hc-wrap details">全部展开</button></div><div id="hc-wrap">')
    for ld in HC['lordsdays']:
        if ld['number'] in parts: c.append(h3(f'hc-p{ld["number"]}','📘 '+parts[ld['number']]))
        qs=''.join(f'<div class="conf" id="hc-q{q["q"]}"><p><b>{sup(q["question"])}</b></p>{paras(q["answer"])}{refs(q["refs"])}</div>' for q in ld['questions'])
        c.append(f'<details class="dx" id="hc-ld{ld["number"]}"><summary><h4 class="h nonum" id="hc-l{ld["number"]}" data-toc="{E(ld["title"])}（Q{ld["questions"][0]["q"]}–{ld["questions"][-1]["q"]}）">📅 {E(ld["title"])}</h4> <span class="tag">第{ld["questions"][0]["q"]}–{ld["questions"][-1]["q"]}问</span></summary><div class="in"><div class="src srcline">逐字引自 <a href="{ld["url"]}" target="_blank" rel="noopener">{ld["url"]}</a></div>{qs}</div></details>')
    c.append('</div>')
    # Dort
    c.append(h2('dort','📕','多特信经（全文）'))
    c.append(f'<details class="dx"><summary>📖 网站介绍（逐字）</summary><div class="in"><div class="conf">{ipar(DT["intro"])}</div></div></details>')
    c.append('<div style="margin:8px 0"><button class="btn" data-expand="#dort-wrap details">全部展开</button></div><div id="dort-wrap">')
    for i,hd in enumerate(DT['heads']):
        c.append(h3(f'dt-h{i}','📕 '+hd['title']))
        if hd.get('intro'): c.append(f'<div class="conf">{paras(hd["intro"])}</div>')
        for a in hd['articles']:
            c.append(f'<details class="dx"><summary><h4 class="h nonum{" notoc" if "错谬" in a["title"] else ""}">{"⚔️" if "错谬" in a["title"] else "📄"} {E(a["title"])}</h4></summary><div class="in"><div class="conf"><div class="src">逐字引自 <a href="{a["url"]}" target="_blank" rel="noopener">ccifellowship.org</a></div>{paras(a["text"])}{refs(a["refs"])}</div></div></details>')
    c.append('</div>')
    c.append(note('ℹ️ 说明','<p>网站将多特信经呈现为四个页面（第三、四项教义合并），与传统一致；网站未单独提供序言与结语页面。个别脚注号与经文出处数量不一致之处（如海德堡第88、123问有脚注号但网站未列经文），照网站原样保留，详见 <a href="sources.html#verify">资料来源·核对报告</a>。</p>'))
    return page('forms.html','三项联合信条',''.join(c))
