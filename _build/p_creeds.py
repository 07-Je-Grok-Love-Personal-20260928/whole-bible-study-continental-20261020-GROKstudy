import re
from lib import *
from v4extra import *
from books import qmark
def lines_ap(t):
    out=[]
    for p in t.split('\n\n'):
        segs=[x for x in re.split(r'(?<=[；。！])',p.strip()) if x.strip()]
        out.append(segs)
    return out
def lines_ni(t):
    return [[x for x in re.split(r'(?<=[；。！])',p.strip()) if x.strip()] for p in t.split('\n\n')]
def lines_at(t):
    out=[]
    for p in t.split('\n\n'):
        segs=[x.strip() for x in re.split(r'(?=\d+\) )',p.strip()) if x.strip()]
        out.append(segs)
    return out
def render(k,paras):
    # join check: reconstruct must equal original (verbatim guarantee)
    rec='\n\n'.join(''.join(s if k!='athanasian' else s for s in p) if k!='athanasian' else ' '.join(p) for p in paras)
    orig=CR[k]['text'].strip()
    assert re.sub(r'\s','',rec)==re.sub(r'\s','',orig),k
    h=''
    for p in paras:
        h+='<p>'
        for s in p:
            m=re.match(r'(\d+)\) (.*)',s,re.S)
            h+=f'<span class="ln"><span class="num">{m.group(1)})</span> {E(m.group(2))}</span>' if m else f'<span class="ln">{E(s)}</span>'
        h+='</p>'
    return h
TOOLS='<div class="ctool" data-for="#{id}"><button class="btn" data-act="hide">🙈 遮盖背诵模式</button><button class="btn" data-act="show">👀 全部显示</button><button class="btn" data-act="big">A＋</button><button class="btn" data-act="small">A－</button><button class="btn" data-act="copy">复制全文</button></div>'
def creedcard(k,ic,sub):
    c=CR[k]; f={'apostles':lines_ap,'nicene':lines_ni,'athanasian':lines_at}[k]
    return f'''<div class="card reveal">{TOOLS.replace('{id}','cr-'+k)}<div class="creed" id="cr-{k}">{render(k,f(c['text']))}</div>
<p class="srcline">📌 全文逐字引自 <a href="{c['url']}" target="_blank" rel="noopener">{c['url']}</a>（2026-10-20 已与在线页面重新比对，段落 100% 一致）。{sub}</p>
<details class="dx"><summary>📖 网站对此信经的介绍（逐字）</summary><div class="in"><div class="conf">{''.join('<p>'+E(x)+'</p>' for x in c['intro_text'])}</div></div></details></div>'''
def build():
    c=[]
    c.append('''<section class="hero reveal"><div class="chips"><span class="chip g">🕊️ 三大普世信经</span><span class="chip">干净版 · 背诵版</span><span class="chip">深度对比</span><span class="chip">与三项联合信条的关系</span></div>
<h1>三大普世信经：<em>大公教会共同的“信仰语法”</em></h1><p class="lead">比利时信条第9条明言：改革宗教会“甘愿接受”这三个信经。它们不是圣经之外的新启示，而是教会对圣经核心的<span class="key">总结、防护与认信</span>——使徒信经说“信什么”，尼西亚信经说“基督是谁”，亚他那修信经说“如何正确地说三一与道成肉身”。</p></section>''')
    c.append(note('🧭 使用方法','<p>① 先通读干净版；② 点 <b>🙈 遮盖背诵模式</b>，逐句默背，点击一句即可揭开；③ 用下方“关键词钩子”自测；④ 到 <a href="memory.html">记忆·测验</a> 做信经填空题。</p>','gold'))
    c.append(legend_box())
    c.append(h2('texts','📜','三大信经 · 干净阅读版'))
    c.append(h3('apostles','🌱 使徒信经'))
    c.append(creedcard('apostles','①','传统分为十二条；海德堡要理问答第23问全文载有此信经，第24–58问逐条讲解。'))
    c.append(note('🪝 关键词钩子（12条）','<p><span class="mn">父·创造</span> → <span class="mn">子·独生</span> → <span class="mn">灵孕·童女</span> → <span class="mn">彼拉多·十架·死·葬·阴间</span> → <span class="mn">三日复活</span> → <span class="mn">升天·右边</span> → <span class="mn">再来审判</span> → <span class="mn">圣灵</span> → <span class="mn">教会·相通</span> → <span class="mn">赦罪</span> → <span class="mn">身体复活</span> → <span class="mn">永生·阿们</span></p><p>结构口诀：<span class="key">“三位一体三段落：父造、子救、灵使成圣”</span>（参海德堡第24问）。</p>','emer'))
    c.append(h3('nicene','🔥 尼西亚信经（尼西亚—君士坦丁堡信经）'))
    c.append(creedcard('nicene','②','注意第四段“他从父和子而出”（filioque，西方教会文本）。'))
    c.append(note('🪝 关键词钩子','<p><span class="mn">独一的神·可见不可见</span> → <span class="mn">万世以前为父所生</span> → <span class="mn">神出于神·光出于光·真神出于真神</span> → <span class="mn">受生非被造·与父同质</span> → <span class="mn">为拯救我们降世</span> → <span class="mn">照圣经第三天复活</span> → <span class="mn">国没有穷尽</span> → <span class="mn">圣灵·赐生命的主</span> → <span class="mn">一·圣·公·使徒性</span> → <span class="mn">独一洗礼</span> → <span class="mn">复活·更新的世界</span></p><p>记忆：教会的四个标记 <span class="key">“一、圣、公、使徒”</span>。</p>','emer'))
    c.append(h3('athanasian','🔺 亚他那修信经（42 节）'))
    c.append(creedcard('athanasian','③','网站介绍称第二部分为“第29-43点”，而网站所载正文编号至 42)；本站照录正文，不作改动。'))
    c.append(note('🪝 结构钩子','<p><span class="mn">1–2 序：必须持守</span> → <span class="mn">3–28 三一：位格不紊、本质不分</span> → <span class="mn">29–41 基督：完全的神、完全的人、一位</span> → <span class="mn">42 结语</span></p><p>三一段的“节奏”：<span class="key">“父如何，子就如何，圣灵也如何”</span>——每个属性说三次，然后说“非三位……乃一位……”。</p>','emer'))
    c.append(h2('cmpx','⚖️','深度对比与历史战场'))
    c.append(h3('compare','📊 三大信经对照表'))
    c.append(table(['比较项','使徒信经','尼西亚信经','亚他那修信经'],[
     ['📅 形成时间','古罗马信经（约2世纪）→ 约公元400年形式，8世纪定型','325 尼西亚会议 → 381 君士坦丁堡会议正式采纳','约6世纪上半叶，作者不详（非亚他那修本人）'],
     ['🌍 来源','西方（罗马）洗礼认信','东方教会为主，东西方共同承认','西方（拉丁），东正教不认可'],
     ['🎯 主要对象','慕道者与受洗者：个人认信“我信”','大公会议：教会共同认信“我们信”','教导与防护：精确的教义规范'],
     ['🛡️ 针对的问题','诺斯底主义、幻影说、马吉安（否认创造主即救赎主、否认真实肉身）','亚流主义（子是受造者）；马其顿派（圣灵非神）','撒伯流（形态论）、三神论；亚波利拿留、聂斯脱利、欧迪奇等基督论错误'],
     ['🧱 结构','三段（父、子、圣灵）+ 教会与救恩福分','三段，大幅扩展子与圣灵','两大部分：三一论（3–28）+ 基督论（29–41）'],
     ['🔑 关键词',qmark('{{AP|因圣灵感孕，从童贞女马利亚所生}}'),qmark('{{NI|受生却非被造，与父同质}}'),qmark('{{AT|其位格不紊，其本质不分}}')],
     ['✝️ 基督论','叙事性：生、死、复活、升天、再来','本体性：子的永恒受生与同质','位格合一：两性不混、不变，合于一位'],
     ['🕊️ 圣灵','“我信圣灵”（简述）','“赐生命的主……与父和子同受敬拜和尊崇”','“从父和子而出，非受造，也非受生”'],
     ['⚠️ 咒诅条款','无','无（原325年版有附咒诅）','有（第2、42节）：强调信仰的严肃性'],
     ['⛪ 礼仪用途','欧陆改革宗主日崇拜常用（如下午崇拜认信）','圣餐主日或节期常用','较少在礼拜中诵读，用于教导'],
     ['📏 篇幅','最短，易背','中等','最长（42节）']],'cmp'))
    c.append(h3('matrix','📐 教义覆盖矩阵（逐字短语）'))
    c.append(creedmatrix())
    c.append(h3('heresies','🛡️ 每一句都有“战场”：异端与信经回应对照'))
    c.append(table(['异端/错误','核心错谬','信经如何回应'],[
     ['马吉安（2世纪）','旧约的神（创造者）与新约的神（救赎者）不同',qmark('使徒信经：{{AP|我信神，全能的父，创造天地的主}}——创造主就是父')],
     ['诺斯底/幻影说','物质是恶的；基督只是“看似”有身体',qmark('{{AP|在本丢·彼拉多手下受难，被钉在十字架上，受死，被埋葬}}；{{AP|我相信身体复活}}')],
     ['亚流主义（4世纪）','“曾有一段时间子不存在”，子是最高受造物',qmark('{{NI|出于神且是神，出于光且是光，出于真神且是真神；受生却非被造，与父同质}}')],
     ['马其顿派（圣灵受造论）','圣灵是受造的能力',qmark('{{NI|我们信圣灵，赐生命的主}}；{{NI|与父和子同受敬拜和尊崇}}')],
     ['撒伯流主义（形态论）','父、子、灵只是一位神的三种面具',qmark('{{AT|其位格不紊}}；{{AT|因为父是一位，子是一位，圣灵又是一位}}')],
     ['三神论','三位是三个神',qmark('{{AT|但父、子、圣灵非三位神，乃一位神}}')],
     ['亚波利拿留','基督没有人的理性灵魂（神的逻各斯取代之）',qmark('{{AT|他既是完全的神，又是具有人的灵魂和肉体的完全的人}}')],
     ['聂斯脱利','基督是两个位格（神子与人耶稣并列）',qmark('{{AT|尽管既是神又是人，基督仍是一位，而非两位}}')],
     ['欧迪奇（基督一性论）','两性混合为第三种本质',qmark('{{AT|他是一位，并非因两质相混，乃是因神人二性合于一个位格}}')]]))
    c.append(h3('why3','🧩 为什么需要三份信经，而不是一份？'))
    c.append('<div class="grid g3 reveal">'+''.join(f'<div class="card tile" style="--c:{col}"><div class="big">{i}</div><h4>{t}</h4><p>{d}</p></div>' for i,t,d,col in [
     ('🧒','① 不同的“问题”，不同的“答案”','使徒信经回答“基督徒信什么？”（洗礼认信）；尼西亚信经回答“耶稣究竟是谁？是神吗？”（亚流危机）；亚他那修信经回答“如何同时说一与三、神与人而不自相矛盾？”（教义语法）。一份信经无法同时兼顾简洁可背、会议权威、精密定义。','#5ec8ff'),
     ('🔬','② 越来越高的分辨率','好比同一张地图的三种比例尺：使徒信经是“全国地图”（救恩历史大事），尼西亚是“城市地图”（子与圣灵的神性），亚他那修是“街道图”（位格、本质、两性的精确关系）。不是新增内容，而是在同一圣经真理上提高清晰度。','#b18cff'),
     ('🛡️','③ 历史中逐步出现的异端','异端是一波一波来的：2世纪否认肉身、4世纪否认子与灵的神性、5世纪混淆基督两性。教会在每一个时刻按圣经作出回应——信经是“历史的伤疤，也是教会的盔甲”。','#ff6b6b'),
     ('🌐','④ 东方与西方的大公性','使徒信经代表西方，尼西亚信经代表东西方共同，亚他那修信经代表西方的奥古斯丁传统。三者并列，表明改革宗不是“新宗派”，而是站在历代大公教会之中（比利时信条第9条、第27条）。','#3ee0a1'),
     ('🎼','⑤ 不同的使用场合','敬拜中的认信（使徒信经）、圣餐与节期的颂赞（尼西亚信经）、教理教导与防护（亚他那修信经）。正如诗歌、讲章、教科书各有功用。','#f5c76b'),
     ('📏','⑥ 都在圣经之下','三者都是“被规范的规范”（norma normata），圣经才是“规范一切的规范”（norma normans）。比利时信条第7条：不可将人的著作与圣经同等。所以三份信经彼此印证，又共同降服于圣经。','#ff9f5a')])+'</div>')
    c.append(mer('''flowchart TB
S["📖 圣经（唯一无误的规范）"]
S-->A["① 使徒信经<br/>信什么？<br/>救恩历史大纲"]
S-->N["② 尼西亚信经<br/>子与圣灵是谁？<br/>同质 homoousios"]
S-->T["③ 亚他那修信经<br/>如何正确地说？<br/>三一与两性语法"]
A-->HC["海德堡要理问答 Q23–58<br/>逐条讲解使徒信经"]
N-->BC["比利时信条 8–11, 18–19<br/>三一、基督神人二性"]
T-->BC
BC-.第9条明确接受三信经.->A
HC-->D["多特信经<br/>恩典教义（救恩的施行）"]
style S fill:#5a4614,stroke:#f5c76b
style A fill:#173a5a,stroke:#5ec8ff
style N fill:#3a2350,stroke:#b18cff
style T fill:#4a1d2a,stroke:#ff6b6b''','三大信经与三项联合信条的关系（流程图）'))
    c.append(h2('forms-rel','📚','与三项联合信条的关系：同一信仰的展开'))
    c.append(h3('forms-map','🗺️ 主题对照表'))
    c.append(table(['三大信经主题','比利时信条','海德堡要理问答','多特信经'],[
     ['独一神·三位一体','第1、8–11条','第25问（及第24问的三分）','—（预设）'],
     ['创造与护理（父）','第12–13条','第26–28问','—'],
     ['基督的位格与工作（子）','第10、18–21、26条','第29–52问','第二项教义（基督之死与救赎）'],
     ['圣灵与教会','第11、27–35条','第53–55问','第三、四项教义（重生）'],
     ['罪得赦免·称义','第22–23条','第56、59–64问','第一、二项教义'],
     ['身体复活·永生·审判','第37条','第57–58、52问','第五项教义（圣徒蒙保守）']]))
    c.append(h3('forms-src','📖 信条原文：比利时第9条 · 海德堡第23–25问'))
    c.append(bc(9))
    c.append(hc(23)); c.append(hc(24)); c.append(hc(25))
    c.append(h2('recite','🎯','背诵策略：三天三信经'))
    c.append('<div class="steps reveal">'+''.join(f'<div style="--c:{col}"><span class="e">{i}</span><b>{t}</b><span>{d}</span></div>' for i,t,d,col in [('1️⃣','第1天 使徒信经','分3段（父/子/灵与福分），每段3遍，遮盖默背。','#5ec8ff'),('2️⃣','第2天 尼西亚信经','先抓“三个出于”与“受生非被造”，再接救恩叙事。','#b18cff'),('3️⃣','第3–7天 亚他那修信经','每天6节，按“父如何，子就如何”的节奏。','#ff6b6b'),('🔁','复习','间隔 1-3-7-14 天重复；主日敬拜时同声认信。','#3ee0a1')])+'</div>')
    return page('creeds.html','三大普世信经',''.join(c))
