from lib import *
from v6lib import *
from gospels_data import *
from lib import _plain
from genre import kbox,mnem,cards,quotes,grid,chbars,R
from v5extra import hbar
from p_stats import VERSES
import p_harmony as PH_
V4=[ # key, 象, 作者, 日期, 读者, 基督肖像, 主题, 钥字, 目的经文, 结构, 旧约使用, 结尾, 独有
('Mt','狮子（王）','马太（利未），税吏出身的使徒','约 AD 50–60 年代（圣殿被毁前）','犹太基督徒：熟悉律法与先知','**应许的君王**——大卫的子孙、亚伯拉罕的后裔、新摩西',
 '==天国已经临近==：旧约应许在耶稣身上应验','“天国”（约32次）、“应验”、“义”','太1:1；5:17','五大讲论（5–7、10、13、18、24–25），各以“耶稣讲完了这些话”收尾——像新的“摩西五经”',
 '旧约引用最多的福音书；约十处“这是要应验……”的公式引语','大使命（28:18–20）：“天上地下所有的权柄都赐给我了”','东方博士、逃往埃及、稗子·藏宝·珍珠·撒网、十童女、绵羊山羊、犹大自尽、守墓兵丁、大使命'),
('Mk','牛（仆人）','马可（约翰马可），据早期教会见证（帕皮亚）记录彼得的讲道','约 AD 50–60 年代（多认为最早成书）','外邦人、罗马信徒：解释犹太习俗（可7:3–4），翻译亚兰语','**受苦的仆人**——有权能的神子，却甘愿舍命',
 '==十字架的道路==：人子来是要服事人、舍命作多人的赎价','“立刻／随即”（约40次）、“福音”、“权柄”','可1:1；10:45','前半（1–8:26）他是谁？——权能；转折（8:27–30 彼得认信）；后半（8:31–16）他为何来？——受难。约三分之一篇幅写最后一周',
 '开篇合引玛3:1与赛40:3；较少公式引语','16:8 妇女“害怕”而止；16:9–20 的经文问题（见下）','种子暗暗生长、耳聋舌结者、伯赛大瞎子分两次得医治、赤身逃走的少年人（14:51–52）'),
('Lk','人（人子）','路加，保罗的同工、“亲爱的医生”（西4:14）','约 AD 60–62（早于使徒行传结尾）','提阿非罗及外邦读者：要他“知道所学之道都是确实的”','**完全的人、万人的救主**——寻找拯救失丧的人',
 '==救恩临到万民==：贫穷人、妇女、税吏、撒玛利亚人','“救恩／救主”、“今天”、“祷告”、“圣灵”、“喜乐”','路1:1–4；19:10','序言＋童年（1–2）→加利利（3–9:50）→长篇“往耶路撒冷”旅程（9:51–19:27）→耶路撒冷（19:28–24）',
 '以“经上所记”与应许—应验的叙事框架为主；24:27、44总结全部旧约指向基督','以马忤斯路上解经；升天；“在城里等候”圣灵（续于使徒行传）','施洗约翰与耶稣的童年、尊主颂、12岁在殿里、好撒玛利亚人、浪子、失钱、财主与拉撒路、撒该、十个麻风、以马忤斯'),
('Jn','鹰（神子）','使徒约翰，“耶稣所爱的那门徒”（约21:20–24）','约 AD 85–95（多数保守学者）','全教会与寻求者：已熟悉符类传统，补充更深的启示','**道成肉身的神子**——“我是”，与父原为一',
 '==信耶稣是基督、是神的儿子，就得生命==','“信”（约98次，动词）、“生命”、“真理”、“光”、“荣耀”、“我是”','约20:31','序言（1:1–18）→“神迹之书”（1:19–12:50，七个神迹）→“荣耀之书”（13–20，楼上讲论、受难复活）→后记（21）',
 '以节期与预表为主：逾越节羔羊、吗哪、住棚节的水与光、铜蛇（3:14）','提比哩亚海边：恢复彼得“你喂养我的羊”（21:15–17）','太初有道、迦拿婚筵、尼哥底母、撒玛利亚妇人、毕士大、生来瞎眼、拉撒路复活、洗脚、楼上讲论、大祭司的祷告（17）、多马'),
]
WEST=[('Mk',7,93),('Mt',42,58),('Lk',59,41),('Jn',92,8)]
def venn(items):
    """items: list of refs dicts -> region counts for Mt/Mk/Lk (John shown as count of items incl. Jn)"""
    from collections import Counter
    syn=Counter(); jn=Counter()
    for r in items:
        k=''.join(x for x in ('Mt','Mk','Lk') if r.get(x)) or '—'
        syn[k]+=1
        if r.get('Jn'): jn[k]+=1
    pos={'Mt':(150,120),'Mk':(250,120),'Lk':(200,205),'MtMk':(200,95),'MtLk':(150,180),'MkLk':(250,180),'MtMkLk':(200,148)}
    circ=''.join(f'<circle cx="{x}" cy="{y}" r="88" fill="{G[k][1]}" class="vc"/>' for k,(x,y) in (('Mt',(165,125)),('Mk',(235,125)),('Lk',(200,185))))
    labs=f'<text x="70" y="40" class="vl" fill="{G["Mt"][1]}">👑 马太</text><text x="265" y="40" class="vl" fill="{G["Mk"][1]}">🐂 马可</text><text x="160" y="300" class="vl" fill="{G["Lk"][1]}">🧑 路加</text>'
    reg=''
    for k,(x,y) in pos.items():
        n=syn.get(k,0); j=jn.get(k,0)
        reg+=f'<g class="vr" data-set="{k}" tabindex="0" role="button" aria-label="{k} {n}"><circle cx="{x}" cy="{y}" r="19" class="vh"/><text x="{x}" y="{y+5}" text-anchor="middle" class="vn">{n}</text>{f"<text x={chr(34)}{x}{chr(34)} y={chr(34)}{y+19}{chr(34)} text-anchor={chr(34)}middle{chr(34)} class={chr(34)}vj{chr(34)}>🦅{j}</text>" if j else ""}</g>'
    only_jn=syn.get('—',0)
    return (f'<figure class="venn rv"><svg viewBox="0 0 400 320" role="img" aria-label="符类福音重叠图">{circ}{labs}{reg}'
            f'<g class="vr" data-set="—" tabindex="0" role="button"><rect x="322" y="262" width="74" height="50" rx="12" fill="{G["Jn"][1]}" opacity=".35"/><text x="359" y="283" text-anchor="middle" class="vl" fill="{G["Jn"][1]}">🦅 仅约翰</text><text x="359" y="304" text-anchor="middle" class="vn">{only_jn}</text></g></svg>'
            '<figcaption class="srcline">点击任一区域 → 下方清单只显示该组合。数字＝本页所列段落、神迹、比喻合计；🦅n＝其中约翰也记载的条数。</figcaption></figure>')
def build():
    c=[]
    c.append(hero(['📗 四福音','横向对照','纵向肖像','符类问题','和谐原则'],'一位基督，','四幅肖像',
      '马太、马可、路加、约翰不是四个“版本”，而是<span class="key">圣灵默示的四重见证</span>：同一位耶稣——<b class="k">王、仆人、人子、神子</b>。先<b class="k">横向</b>看同一事件在四卷中怎样记，再<b class="k">纵向</b>看每卷书自己的结构、读者与目的。'))
    c.append(legend_box())
    c.append(kbox('四福音五个必背钉子',['**四象**：太＝狮（==王==）· 可＝牛（==仆人==）· 路＝人（==人子==）· 约＝鹰（==神子==）。','**符类 vs 约翰**：太可路“同一眼光”，约翰约 **九成独有**——不重复，而是加深。','**目的经文**：@@可10:45@@（来服事、舍命）；@@路19:10@@（寻找拯救失丧的人）；@@约20:31@@（信而得生）。','**重心在最后一周**：四卷用约 **¼–½ 篇幅**写受难周——福音书是“带着长序言的受难记”。','**四卷都记**：施洗约翰、喂饱五千人、进耶路撒冷、受难、空坟墓。']))
    c.append('<div class="g4leg rv">'+''.join(f'<div class="card tile" style="--c:{G[k][1]}"><div class="big">{G[k][2]}</div><b style="color:{G[k][1]}">{G[k][0]}福音</b><span>{s}</span></div>' for k,s in (('Mt','王 · 给犹太人 · 应验'),('Mk','仆人 · 给罗马人 · 行动'),('Lk','人子 · 给外邦人 · 救恩'),('Jn','神子 · 给全教会 · 信而得生')))+'</div>')
    c.append(h2('whole','🧭','整体：为什么是四卷，而不是一卷？'))
    c.append(h3('why4','四重见证的理由'))
    c.append('<div class="steps rv">'+''.join(f'<div style="--c:{col}"><span class="e">{i}</span><b>{t}</b><span>{d}</span></div>' for i,t,d,col in [
      ('⚖️','法律上的见证','“要凭两三个人的口作见证”（申19:15）：多重独立见证使事实确立。','var(--gold)'),
      ('💎','一颗钻石四个切面','同一位基督太丰富，一幅肖像容不下：王（太）、仆人（可）、人（路）、神（约）。','var(--sky)'),
      ('🌍','不同读者的需要','犹太人问“他是不是应许的弥赛亚？”；罗马人看“他做了什么？”；外邦人问“他与我有关吗？”；教会问“他到底是谁？”','var(--emer)'),
      ('📜','教会的领受，不是发明','早期教会（如爱任纽，约 AD 180）已明确只承认四卷；把四卷合成一卷的《四福音合参》（他提安，约 AD 170）没有取代正典。','var(--vio)')])+'</div>')
    c.append(co('conf','<p>'+rich('比利时信条列出新约正典时，首先就是{{BC4|四福音书，即马太福音、马可福音、路加福音及约翰福音}}。正典的根据不是教会的投票：{{BC5|与其说这是因为教会接受并赞同它们，倒不如说这是因为圣灵在我们心中作见证，证明它们都来自神}}。',False)+'</p>','认信'))
    c.append(bc(4)+bc(5))
    _ss=[x for p_ in PH_.P for x in p_['s']]; _n=lambda m:sum(1 for x in _ss if len(x['r'])==m); _jo=[sum(1 for x in p_['s'] if 'Jn' in x['r'] and len(x['r'])>1) for p_ in PH_.P]
    c.append(h3('hmcov',f'合参覆盖：{PH_.N} 段在四卷中的分布'))
    c.append(PH_.coverage())
    c.append(hbar([('✦ 四卷皆有',_n(4),'var(--gold)'),('三卷',_n(3),'var(--sky)'),('两卷',_n(2),'var(--vio)'),('仅一卷',_n(1),'var(--rose)')],' 段',f'按本站《四福音合参》{PH_.N} 段统计（分段为编辑选择，参 Robertson / Aland 传统）。竖线＝13 个阶段。'))
    c.append(co('info',f'<p>想逐段并排读经文？→ <a href="harmony.html">📖 四福音合参（{PH_.N} 段，和合本原文）</a>；想看耶稣升天之后福音怎样从耶路撒冷到罗马？→ <a href="acts.html">🗺️ 使徒行传与新约历史</a>。</p><p>'+rich(f'**观察**：约翰与符类重叠的 {sum(_jo)} 段中，有 {sum(_jo[9:])} 段落在==受难周到复活==（第 10–13 阶段），加利利事工几乎全由符类记载。',False)+'</p>','延伸'))
    c.append(h3('table4','一表看懂四福音（纵向总表）'))
    rows=[]
    for k,sym,au,dt,rd,po,th,kw,pv,st,ot,en,un in V4:
        rows.append([gtag(k),E(sym),rich(po,False),rich(th,False),E(kw),f'<span class="rf">{E(pv)}</span>',E(rd)])
    c.append(table(['福音','象征','基督肖像','主题','钥字','目的经文','读者'],rows))
    c.append(co('mnc','<p class="mn">'+rich('**王·仆·人·神；狮·牛·人·鹰**——太“应验”、可“立刻”、路“救恩”、约“信”。',False)+'</p>','口诀'))
    c.append(h3('west','重叠与独有：一图看比例'))
    c.append('<div class="hbar rv">'+''.join(f'<div><span>{G[k][2]} {G[k][0]}</span><div class="t"><span style="--v:{u/100:.2f};--c:{G[k][1]}"></span></div><b>独有约{u}%</b></div>' for k,u,s in WEST)+'</div>')
    c.append('<p class="srcline">📐 比例为近似值：B. F. Westcott《福音书研究导论》（1860）对各卷“独有材料”的经典估计（马可约7%、马太约42%、路加约59%、约翰约92%），各家统计口径略有不同。</p>')
    c.append(co('core','<p>'+rich('**符类福音**（太、可、路）＝“用同一眼光看”：大量共同材料、相近次序。**约翰**约九成是独有材料——==他不重复，而是加深==。',False)+'</p>'))
    # ---------------- horizontal
    c.append(h2('horiz','↔️','横向：同一事件，四卷怎样记'))
    c.append(h3('venn','交互重叠图（点击区域筛选）'))
    allitems=[r for _,_,r,_ in PERI]+[r for _,r in MIR]+[r for _,r in PAR]
    c.append(venn(allitems))
    c.append(h3('peri',f'主要段落对照表（{len(PERI)} 段）'))
    c.append(gfilter('peritab'))
    rows=[]
    for ph,t,r,nt in PERI:
        rows.append((gset(r),[f'<span class="chip">{E(ph)}</span>',f'<b>{E(t)}</b>']+gcells(r)+[rich(nt,False) if nt else '']))
    c.append(f'<div class="tw gtab" id="peritab"><table><thead><tr><th>阶段</th><th>段落</th>'+''.join(f'<th style="color:{G[k][1]}">{G[k][2]} {G[k][0]}</th>' for k in GO)+'<th>要点</th></tr></thead><tbody>'+''.join(f'<tr data-g="{g}">'+''.join(f'<td>{x}</td>' for x in cells)+'</tr>' for g,cells in rows)+'</tbody></table></div>')
    n4=sum(1 for _,_,r,_ in PERI if len(r)==4)
    c.append(co('core','<p>'+rich(f'本表 {len(PERI)} 段中，**四卷都记载的有 {n4} 段**——几乎集中在 ==施洗约翰、喂饱五千人、进城与受难、复活==。四福音的“重心”在十字架与空坟墓。',False)+'</p>','观察'))
    c.append(h3('miracles',f'神迹清单（{len(MIR)} 个）'))
    c.append(gfilter('mirtab'))
    c.append(f'<div class="tw gtab" id="mirtab"><table><thead><tr><th>神迹</th>'+''.join(f'<th style="color:{G[k][1]}">{G[k][2]} {G[k][0]}</th>' for k in GO)+'</tr></thead><tbody>'+''.join(f'<tr data-g="{gset(r)}"><td><b>{E(t)}</b></td>'+''.join(f'<td>{x}</td>' for x in gcells(r))+'</tr>' for t,r in MIR)+'</tbody></table></div>')
    cnt={k:sum(1 for _,r in MIR if r.get(k)) for k in GO}
    c.append(vbars([(G[k][0],cnt[k],G[k][1],f'{G[k][0]}：本表 {cnt[k]} 个神迹') for k in GO],h=200,cap='本表所列神迹在各卷中的出现次数（依本页清单计算，非全部统计）'))
    c.append(h3('parables',f'比喻清单（{len(PAR)} 个）'))
    c.append(gfilter('partab'))
    c.append(f'<div class="tw gtab" id="partab"><table><thead><tr><th>比喻</th>'+''.join(f'<th style="color:{G[k][1]}">{G[k][2]} {G[k][0]}</th>' for k in GO)+'</tr></thead><tbody>'+''.join(f'<tr data-g="{gset(r)}"><td><b>{E(t)}</b></td>'+''.join(f'<td>{x}</td>' for x in gcells(r))+'</tr>' for t,r in PAR)+'</tbody></table></div>')
    pl=sum(1 for _,r in PAR if list(r)==['Lk']); pm=sum(1 for _,r in PAR if list(r)==['Mt'])
    c.append(co('info','<p>'+rich(f'本表中 **路加独有 {pl} 个**、**马太独有 {pm} 个**比喻；约翰没有符类式的比喻，而用“我是……”与长篇讲论（如好牧人，约10章）。路加的比喻多写==失丧者被寻回==（路15），马太的比喻多写==天国与审判==（太13、25）。',False)+'</p>','观察'))
    c.append(h3('sayings','十架七言与七个“我是”'))
    c.append(table(['#','十架七言','出处','意义'],[[f'<span class="kpb">{i+1}</span>',f'<b>{E(t)}</b>',' '.join(gtag(k,v) for k,v in r.items()),E(m)] for i,(t,r,m) in enumerate(CROSS)]))
    c.append('<div class="grid rv">'+''.join(f'<div class="card tile" style="--c:var(--g-jn)"><b class="kpb">{i+1}</b> <b>我是{E(t)}</b> <span class="rf">约{v}</span></div>' for i,(t,v) in enumerate(IAM))+'</div>')
    c.append(table(['#','约翰福音七个神迹（“记号”）','经文','指向'],[[f'<span class="kpb">{i+1}</span>',f'<b>{E(t)}</b>',f'<span class="rf">约{v}</span>',E(m)] for i,(t,v,m) in enumerate(SIGNS)]))
    c.append('<p class="srcline">约翰称神迹为“记号”（sēmeion），七个是常见的归纳；有学者把复活后的捕鱼（约21）列为第八个。</p>')
    # ---------------- vertical
    c.append(h2('vert','↕️','纵向：每卷福音自己的面貌'))
    for k,sym,au,dt,rd,po,th,kw,pv,st,ot,en,un in V4:
        n,col,ic=G[k]
        c.append(h3('g-'+k.lower(),f'{ic} {n}福音：{_plain(rich(po,False))}',toc=f'{ic} {n}福音'))
        c.append(f'<div class="facts rv" style="--c:{col}">'+''.join(f'<div class="fact"><b>{a}</b> {E(b)}</div>' for a,b in (('✍️ 作者',au),('🕰️ 日期',dt),('👥 读者',rd),('🦁 象征',sym)))+'</div>')
        c.append(h4(f'g-{k.lower()}-st','🧩 结构'))
        c.append('<p>'+rich(st,False)+'</p>')
        c.append(h4(f'g-{k.lower()}-th','💎 主题 · 钥字 · 目的经文'))
        c.append(co('core','<p>'+rich(th,False)+'</p><p>🔑 '+E(kw)+'</p><p>🎯 <span class="rf">'+E(pv)+'</span></p>'))
        c.append(h4(f'g-{k.lower()}-ot','📜 旧约的使用 · 结尾'))
        c.append('<p>'+rich(ot,False)+'</p><p>🏁 '+rich(en,False)+'</p>')
        c.append(h4(f'g-{k.lower()}-un','✨ 独有材料'))
        c.append('<div class="chips">'+''.join(f'<span class="chip" style="border-color:{col}">{E(x)}</span>' for x in un.split('、'))+'</div>')
    c.append(co('hardc','<p>'+rich('**马可福音16:9–20**：最古老的几份抄本（西乃抄本、梵蒂冈抄本）止于16:8，和合本以括号或注释标明。保守改革宗学者看法不一；==无论哪一种看法，复活、差遣、升天的真理都由其他经文清楚确立==（太28；路24；徒1）。不可据这段经文建立“拿蛇、喝毒”的实践。',False)+'</p>','难点'))
    # ---------------- synoptic problem
    c.append(h2('synoptic','🧩','符类问题与和谐原则（保守改革宗角度）'))
    c.append(h3('sp','符类问题：为什么这么像？'))
    c.append(table(['看法','要点','评估'],[
      ['<b>马可优先说</b>','马太、路加使用马可，另有共同材料（常称 “Q”）','许多福音派学者接受文学关系；但“Q”是假设文献，从未发现抄本'],
      ['<b>马太优先说</b>','早期教会传统（奥古斯丁等）：马太先写','与教父见证一致；文学论证上有争议'],
      ['<b>独立见证／口传</b>','使徒的口传教导高度固定，各卷独立写成','重视目击见证（路1:1–4；约21:24）'],
      ['<b>激进形式批判</b>','福音书是初期教会“创作”的信仰传说','<span class="uw">与圣经自证和默示教义相冲突，应予拒绝</span>']]))
    c.append(co('conf','<p>'+rich('改革宗的出发点是 ;;有机默示;;（巴文克、凯波尔）：圣灵使用作者的研究（路1:3）、记忆（约14:26）与写作风格，所写的却完全是神的话。因此**文学来源问题可以讨论，但不能削弱历史可靠性**。比利时信条说：{{BC5|我们完全相信且毫不怀疑其中所写的一切}}。',False)+'</p>','认信'))
    c.append(h3('harmony','和谐原则：读出差异，不制造矛盾'))
    c.append('<div class="steps rv">'+''.join(f'<div style="--c:{col}"><span class="e">{i}</span><b>{t}</b><span>{d}</span></div>' for i,t,d,col in [
      ('🧭','主题排列≠时间排列','马太常按主题集中（如太8–9十个神迹）；路加“按着次序”（1:3）也不一定是严格的日期次序。','var(--gold)'),
      ('🗣️','意思准确≠逐字相同','福音书常记主的话的准确意思（ipsissima vox），而不总是录音式的原话。','var(--sky)'),
      ('🔢','详略不同≠矛盾','一人或两人（格拉森、耶利哥瞎子）：记两人的包含一人，记一人的突出主要的。','var(--emer)'),
      ('🔁','相似事件可能发生不止一次','洁净圣殿、受膏、比喻在不同场合重讲。','var(--vio)'),
      ('🙇','承认未知，不强求','加尔文《四福音合参注释》（1555）的态度：谦卑地合参，不为“和谐”而扭曲经文。','var(--rose)')])+'</div>')
    c.append(co('trap','<p>'+rich('!!不要把四卷压成一卷!!：合参是为了帮助理解，但每卷书都有自己的神学目的。读马可时问“马可要我看见什么”，而不只是“这件事完整经过如何”。',False)+'</p>','易错'))
    c.append(co('app','<p>'+rich('读福音书的三个问题：① 这一段**说耶稣是谁**？② 这一段在**本卷的结构**中处在哪里？③ 这一段在**其他福音书**怎样记？——先纵后横，再回到基督。',False)+'</p>','应用'))
    c.append(h2('g-chart','📊','数字与图表'))
    c.append(grid([hbar([(f'{G[k][2]} {G[k][0]}',v,G[k][1]) for k,v in zip(GO,(28,16,24,21))],' 章','章数：马太最长（28 章），马可最短（16 章）。'),
      hbar([(f'{G[k][2]} {G[k][0]}',v,G[k][1]) for k,v in zip(GO,VERSES[39:43])],' 节','节数：路加最长（1151 节），马可最短（678 节）。')],2))
    c.append(h3('g-week','受难周占多少篇幅？'))
    c.append(hbar([(f'{G["Mt"][2]} 马太 21–28 章',29,G['Mt'][1]),(f'{G["Mk"][2]} 马可 11–16 章',38,G['Mk'][1]),(f'{G["Lk"][2]} 路加 19:28–24 章',23,G['Lk'][1]),(f'{G["Jn"][2]} 约翰 12–21 章',48,G['Jn'][1])],'%','按章数粗算“进耶路撒冷 → 复活”所占比例（近似值）。约翰用近一半篇幅写最后一周。'))
    c.append(co('core','<p>'+R('一生约 33 年，最后**一周**占去福音书约三分之一——==圣灵要我们看的焦点是十字架与复活==。')+'</p>','观察'))
    c.append(h2('g-mem','🧠','记忆：口诀与闪卡'))
    c.append(mnem([('四象','狮牛人鹰 · 王仆人神','太王、可仆、路人、约神；对应以西结书1:10 的四活物（教父的传统配法）。'),('钥字','太应验 · 可立刻 · 路救恩 · 约信','每卷一个高频词，抓住每卷的“口气”。'),('结构','太五讲 · 可八27转 · 路九51上 · 约二书','马太五大讲论；马可在 8:27 彼得认信处转折；路加 9:51 起“定意向耶路撒冷去”；约翰＝神迹之书 + 荣耀之书。'),('约翰 7+7','七记号 · 七我是','七个神迹（记号）+ 七个“我是”，都为叫人信（约20:31）。')]))
    c.append(cards([('太1:1','亚伯拉罕的后裔，大卫的子孙，耶稣基督的家谱'),('太5:17','我来不是要废掉，乃是要成全'),('太28:18–20','天上地下所有的权柄都赐给我了……'),('可1:15','日期满了，神的国近了。你们当悔改，信福音'),('可10:45','人子来……是要服事人，并且要舍命作多人的赎价'),('路19:10','人子来，为要寻找、拯救失丧的人'),('路24:27','从摩西和众先知起，凡经上所指着自己的话，都给他们讲解明白了'),('约1:14','道成了肉身，住在我们中间，充充满满地有恩典有真理'),('约3:16','神爱世人，甚至将他的独生子赐给他们'),('约14:6','我就是道路、真理、生命'),('约19:30','成了'),('约20:31','叫你们信耶稣是基督，是神的儿子，并且叫你们信了他，可以因他的名得生命')],'gfc'))
    c.append(h2('g-xc','✝️','指向基督 · 改革宗读法'))
    c.append(co('conf','<p>'+R('四福音合起来正是海德堡要理问答所说的三重职分：基督被立为{{HC31|我们的大先知和教师}}（太：登山宝训）、{{HC31|我们唯一的大祭司}}（可：舍命作赎价）、{{HC31|我们永远的君王}}（太、约：王与权柄）。他的一生不只是榜样：{{HC37|基督在地上生活的整个时期，特别是最后阶段，用他的肉体与灵魂担当了神对全人类罪恶的忿怒}}。')+'</p>','认信'))
    c.append(co('conf','<p>'+R('四卷同时见证**真神**（约1:1）与**真人**（路2:52）：{{BC19|正因如此，我们宣告基督是真神，也是真人}}。复活不是附录：{{HC45|基督的复活是我们将来荣耀复活的确据}}。')+'</p>','认信'))
    c.append(quotes('HC31,HC37,BC19,HC45'))
    return page('gospels.html','四福音深度对照',''.join(c),scripts='<script src="assets/js/v6.js?v=v8" defer></script>')
