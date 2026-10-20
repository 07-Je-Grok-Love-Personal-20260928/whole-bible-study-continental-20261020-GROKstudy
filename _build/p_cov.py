from lib import *
from books import qmark
COV=[('🌳 行为之约（创造之约）','亚当（全人类的元首）','神 ↔ 亚当','完全顺服→永生；违背→死（创2:16–17）','生命树（与分别善恶树）','何6:7；罗5:12–21','被亚当违背；由“末后的亚当”基督为选民完全成就（主动顺服+被动顺服）','#ffb34d'),
('🌈 挪亚之约','挪亚及其后裔、一切活物','神 ↔ 全地','不再以洪水灭世；季节保存（创8:22–9:17）','彩虹','创9；赛54:9；彼后3:5–7','普遍恩典的保存之约：为救赎历史保存舞台，直到基督','#5ec8ff'),
('⭐ 亚伯拉罕之约','亚伯拉罕与他的后裔（信者与其子女）','神 ↔ 亚伯拉罕家','地、后裔、祝福万国；“我要作你和你后裔的神”（创17:7）','割礼（因信称义的印证，罗4:11）','创12；15；17；22；加3','“那后裔就是基督”（加3:16）；信的外邦人也是亚伯拉罕的子孙（加3:29）','#ff9f5a'),
('🔥 摩西之约（西奈之约）','以色列国（神权国）','神 ↔ 以色列（摩西为中保）','“我是耶和华你的神……”——律法、献祭、祭司、地中的祝福咒诅','安息日；逾越节；献祭','出19–24；申；耶31:32','恩典之约的施行（附带律法作训蒙的师傅）；影子在基督里成全（来8–10）','#ff7aa8'),
('👑 大卫之约','大卫与他的王朝','神 ↔ 大卫家','永远的家、国、位；父子关系；建殿（撒下7）','（王位、耶路撒冷、圣殿）','撒下7；诗89；132；赛55:3','基督是大卫的子孙，坐在宝座上直到永远（路1:32–33；徒2:30–36）','#5ec8ff'),
('✝️ 新约','新以色列——基督的教会（犹太人与外邦人）','神 ↔ 教会（基督为中保）','律法写在心上；人人认识神；罪得完全赦免（耶31:31–34）；圣灵内住','洗礼；圣餐','耶31；结36；路22:20；来8–10','恩典之约最完全、最终的施行；在新天新地完成（启21:3）','#3ee0a1')]
def covflow():
    N=[(n,a,cnt,s_,r,x,col) for n,a,_,cnt,s_,r,x,col in COV]+[('🌅 新天新地','神的全体子民','“神的帐幕在人间，他要与人同住”（启21:3）——圣约公式的最终实现','（无需记号：面对面）','启21–22','约的目标：神与他的子民永远同住','#3ee0a1')]
    W=1200; xs=[80+i*(W-160)/(len(N)-1) for i in range(len(N))]; ys=[150+(-26 if i%2 else 26) for i in range(len(N))]
    d='M'+' '.join(f'{x:.0f},{y}' for x,y in zip(xs,ys))
    path='M%.0f,%d '%(xs[0],ys[0])+' '.join(f'C{(xs[i]+xs[i+1])/2:.0f},{ys[i]} {(xs[i]+xs[i+1])/2:.0f},{ys[i+1]} {xs[i+1]:.0f},{ys[i+1]}' for i in range(len(N)-1))
    o=[f'<svg viewBox="0 0 {W} 300" role="img" aria-label="圣约递进动画流程图"><defs><linearGradient id="cg" x1="0" x2="1"><stop offset="0" stop-color="#ffb34d"/><stop offset=".5" stop-color="#ff6fa5"/><stop offset="1" stop-color="#3ee0a1"/></linearGradient><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="#b78cff"/></marker></defs>',
       f'<path d="M{xs[0]:.0f},44 L{xs[-1]:.0f},44" stroke="#b78cff" stroke-width="2" stroke-dasharray="3 7" fill="none" opacity=".8"/><text x="{W/2:.0f}" y="30" text-anchor="middle" font-size="15" font-weight="800" fill="#c9b2ff">🕰️ 救赎之约（永恒中：父差子 · 子甘愿 · 灵施行）—— 保证一切历史之约必然成就</text>',
       f'<path d="M{xs[5]:.0f},50 L{xs[5]:.0f},{ys[5]-30}" stroke="#b78cff" stroke-width="2" marker-end="url(#ar)"/>',
       f'<path d="{path}" stroke="url(#cg)" stroke-width="5" fill="none" opacity=".35"/><path class="flow" d="{path}" stroke="url(#cg)" stroke-width="3" fill="none"/>',
       f'<path class="flow" d="M{(xs[0]+xs[1])/2:.0f},250 L{xs[-1]:.0f},250" stroke="#3ee0a1" stroke-width="3" fill="none" style="animation-duration:2.4s"/><text x="{(xs[0]+xs[1])/2:.0f}" y="276" font-size="13.5" fill="#7ff0c2">🎁 恩典之约：从创3:15 原福音起，以同一位中保、同一应许贯穿所有历史之约 →</text>',
       f'<text x="{(xs[0]+xs[1])/2:.0f}" y="{min(ys[0],ys[1])-48}" text-anchor="middle" font-size="12" fill="#ff8f8f">💥 堕落·违约</text>']
    for i,((n,a,cnt,s_,r,x,col),X,Y) in enumerate(zip(N,xs,ys)):
        ic,nm=n.split(' ',1)
        info=f'<div class="co core" style="--cc:{col}"><span class="lb">{E(n)}</span><p><b class="k">对象</b>：{E(a)}</p><p><b class="k">内容</b>：{rich(cnt,False)}</p><p><b class="k">记号</b>：{E(s_)} · <span class="ub">{E(r)}</span></p><p><span class="ug">在基督里成全</span>：{rich(x,False)}</p></div>'
        o.append(f'<g class="nd" data-html="{E(info)}" tabindex="0"><circle cx="{X:.0f}" cy="{Y}" r="34" fill="{col}" fill-opacity=".22" stroke="{col}" stroke-width="2.5"/><text x="{X:.0f}" y="{Y+9}" text-anchor="middle" font-size="26">{ic}</text><text x="{X:.0f}" y="{Y+56 if i%2==0 else Y-44}" text-anchor="middle" font-size="14" font-weight="800">{E(nm.split("（")[0])}</text></g>')
    o.append('</svg>')
    return '<div class="covflow rv" data-info="#cfinfo">'+''.join(o)+'</div><div class="kinfo" id="cfinfo">'+co('info','<p>👆 点击任一圣约节点：查看对象、内容、记号、经文与“在基督里成全”。金→粉→绿的流动线 = 救赎历史的推进；紫色虚线 = 永恒的救赎之约；绿色底线 = 贯穿始终的恩典之约。</p>','圣约动画说明')+'</div>'
def build():
    c=[]
    c.append('''<section class="hero reveal"><div class="chips"><span class="chip g">🤝 圣约神学</span><span class="chip">行为之约 · 救赎之约 · 恩典之约</span><span class="chip">亚当—挪亚—亚伯拉罕—摩西—大卫—新约</span></div>
<h1>圣约：<em>整本圣经的骨骼与关节</em></h1><p class="lead">“我要作你们的神，你们要作我的子民”——这句圣约公式从创世记贯穿到启示录（创17:7；出6:7；耶31:33；林后6:16；启21:3）。欧陆改革宗（乌尔西努、俄利维亚努、维特修斯、巴文克、霍志恒、斯基德尔）以圣约为钥匙读整本圣经：<span class="key">一位神、一个子民、一个恩典之约、一位中保、一条救赎历史。</span></p></section>''')
    c.append(legend_box())
    c.append(h2('frame','📐','圣约的定义与总架构'))
    c.append(h3('def','什么是“约”？六个要素'))
    c.append(co('core','<p><b class="k">约</b> = 神<mark class="hy">主权设立</mark>、<span class="ub">以血立定</span>的关系，包含<b class="k">应许</b>与<b class="k">要求</b>、<b class="k">元首</b>、<b class="k">记号</b>以及<b class="k">祝福/咒诅</b>。公式：<span class="cx">“我要作你们的神，你们要作我的子民”</span>。</p>','一句话定义'))
    c.append('<div class="grid g3 reveal">'+''.join(f'<div class="card tile"><div class="big">{i}</div><h4>{t}</h4><p>{d}</p></div>' for i,t,d in [('👑','神主权设立','约不是平等双方的谈判，而是伟大的君王恩慈地俯就，单方面设立、双方面承担（应许与要求）。'),('🩸','以血立定','希伯来文“立约”直译为“切约”（创15:10–17：神独自经过肉块之间，自我咒诅担保应许）。'),('👤','有元首/中保','亚当代表全人类；基督代表所有属他的人（罗5）。“联邦神学”（foedus=约）因此得名。'),('💧','有记号与印证','生命树、彩虹、割礼、逾越节、洗礼、圣餐——看得见的记号印证看不见的应许（比利时信条第33条）。'),('⚖️','有祝福与咒诅','守约者蒙福，违约者受咒诅；基督“为我们受了咒诅，就赎出我们脱离律法的咒诅”（加3:13）。'),('🔗','有历史性','约在历史中逐步展开、递进，后约不废前约，而是在前约基础上更加丰满。')])+'</div>')
    c.append(h3('three','三个“大约”：行为之约、救赎之约、恩典之约'))
    c.append(mer('''flowchart TB
P["🕰️ 救赎之约 pactum salutis<br/>永恒中：父差子、子甘愿、灵施行<br/>（约6:38–40；17:4–6；弗1:3–14）"]
W["🌳 行为之约（创造之约）<br/>神 ↔ 亚当<br/>顺服则生"]
F["💥 堕落（创3）<br/>在亚当里众人都死"]
G["🎁 恩典之约<br/>神 ↔ 信者与其儿女<br/>中保：基督"]
P==>G
W-->F-->G
G-->OT["旧约施行<br/>应许·预表·献祭·割礼·逾越节"]
G-->NT["新约施行<br/>实体·基督·圣灵·洗礼·圣餐"]
OT-->C["✝️ 基督一次献上<br/>成就行为之约的要求"]
NT-->C
C-->E["🌅 新天新地<br/>神的帐幕在人间"]
style P fill:#3a2350,stroke:#b18cff
style W fill:#5a3a10,stroke:#ffb34d
style F fill:#4a1d2a,stroke:#ff6b6b
style G fill:#173f2f,stroke:#3ee0a1
style C fill:#5a4614,stroke:#f5c76b''','圣约神学总架构（流程图）'))
    c.append(table(['约','双方','条件/内容','元首/中保','结局'],[['救赎之约','父 ↔ 子（与圣灵）','子取人性、顺服至死；父赐他一群子民','子','必然成就（约17）'],['行为之约','神 ↔ 亚当（与全人类）','完全顺服 → 永生','亚当','被违背：罪与死临到众人（罗5:12）'],['恩典之约','神 ↔ 信者与其儿女','白白赐下基督与救恩；要求以信心与顺服回应（信心本身也是恩赐）','基督','在选民身上必然成全；违约者受更重审判（来10:29）']]))
    c.append(note('🔑 难点：两约的“条件”有何不同？','<p>行为之约中，顺服是<span class="key">得生命的根据</span>；恩典之约中，信心是<span class="key">领受生命的工具</span>，而顺服是<span class="key">感恩的果子</span>。所以海德堡要理问答把十诫放在第三部分“感恩”，而不是放在得救之前。</p>','red'))
    c.append(hc(60))
    c.append(h2('hist','🧬','历史之约：一条递进的链'))
    c.append(h3('flow','动画圣约流：从伊甸到新天新地'))
    c.append(covflow())
    c.append(h3('six','六约对照总表'))
    c.append(table(['约','对象','核心应许/要求','记号','关键经文','在基督里成全'],[[f'<b style="color:{col}">{n}</b>',a,cnt,s,r,x] for n,a,_,cnt,s,r,x,col in COV]))
    c.append('<div class="steps reveal">'+''.join(f'<div style="--c:{col}"><span class="e">{n.split(" ")[0]}</span><b>{n.split(" ",1)[1]}</b><span>{x}</span></div>' for n,a,_,cnt,s,r,x,col in COV)+'</div>')
    c.append(mer('''flowchart LR
A["🌳 亚当<br/>行为之约"]-->|违背·3:15 应许|N["🌈 挪亚<br/>保存"]-->AB["⭐ 亚伯拉罕<br/>应许·后裔"]-->M["🔥 摩西<br/>律法·献祭"]-->D["👑 大卫<br/>君王·国度"]-->X["✝️ 新约<br/>基督的血"]-->R["🌅 新天新地"]
style X fill:#5a4614,stroke:#f5c76b''','从伊甸到新耶路撒冷：圣约链'))
    c.append(h3('six-mn','口诀与易错'))
    c.append(co('trap','<p><span class="uw">把摩西之约当成“行为之约的重新颁布”而与恩典之约对立</span>——改革宗主流：西奈之约是<b class="k">恩典之约的一种施行</b>（出20:2 先救赎），其中“在地上长久”的条款具有预表性。<span class="uw">以为新约废除了旧约的应许</span>——新约是同一应许的<mark class="hg">实体与完成</mark>。</p>'))
    c.append(note('🧠 口诀','<span class="mn">“亚挪亚摩大新”——树、虹、割、安、位、杯</span>（各约记号：生命树、彩虹、割礼、安息日/逾越节、王位、圣餐杯）','gold'))
    c.append(h2('admin','🫱','施行与记号'))
    c.append(h3('one-two','一个恩典之约，两种施行（旧约 / 新约）'))
    c.append(table(['比较','旧约时期的施行','新约时期的施行'],[['实质','同一位中保基督、同一应许、同一因信称义（罗4；加3）','相同'],['方式','应许、预表、献祭、割礼、逾越节——“影儿”','实体：基督已来；洗礼、圣餐'],['范围','主要在以色列一国','普及万国万民'],['圣灵','有限度、多赐给职分者','浇灌凡有血气的（徒2）'],['清晰度','模糊、渐进','清楚、完全（来1:1–2）']]))
    c.append(note('📜 威斯敏斯特信仰告白参照','<p>威斯敏斯特信仰告白第7章（论神与人所立的约）第5–6节，也以“一个恩典之约、两种施行”表述同一真理；全文见 <a href="https://opc.org/wcf.html" target="_blank" rel="noopener">opc.org</a>。（此处只标章节出处，不作引用。）</p>','vio'))
    c.append(h3('signs','约的记号：割礼→洗礼，逾越节→圣餐'))
    c.append(table(['旧约记号','新约记号','共同意义','经文'],[['割礼（第八日，男婴）','洗礼（信徒及其儿女）','进入约的群体；洁净与重生的记号','西2:11–12；创17'],['逾越节','圣餐','羔羊的血、救赎的记念与团契','林前5:7；路22:15–20']]))
    c.append(hc(74)); c.append(bc(34)); c.append(bc(33))
    c.append(h3('dutch','欧陆改革宗内部的圣约侧重'))
    c.append(note('🇳🇱 欧陆改革宗内部的圣约侧重（了解即可）','<p>荷兰改革宗传统内部对“恩典之约与拣选的关系”有不同侧重：如加拿大归正教会（CanRC，<a href="https://canrc.org" target="_blank" rel="noopener">canrc.org</a>）承继斯基德尔（K. Schilder）1944年“解放运动”，强调约的应许与要求真实地临到所有受洗的信徒儿女；更正改革宗（PRCA，<a href="https://www.prca.org" target="_blank" rel="noopener">prca.org</a>）则强调约是神与选民之间的友谊联结。各宗派均以三项联合信条为共同认信基础。本站立足信条本身的表述，并鼓励读者查阅各教会官方资料。</p>','vio'))
    c.append(h2('lawvs','⚖️','约与律法 · 与时代论对照'))
    c.append(h3('law','律法的三种功用'))
    c.append('<div class="grid g3 reveal">'+''.join(f'<div class="card tile" style="border-color:{col}"><div class="big">{i}</div><h4>{t}</h4><p>{d}</p></div>' for i,t,d,col in [('🪞','① 镜子：显明罪','“律法本是叫人知罪”（罗3:20）。海德堡要理问答第3问：从神的律法得知罪恶与愁苦。','#ff6b6b'),('🚧','② 篱笆：约束恶行','在社会中约束罪恶（提前1:9–10），维持普遍恩典下的秩序。','#ffb34d'),('🧭','③ 指南：感恩的规则','对蒙恩者，律法是感恩生活的规范（海德堡第86问之后，十诫列在“感恩”部分）。','#3ee0a1')])+'</div>')
    c.append(hc(3)); c.append(hc(115))
    c.append(h3('vs','圣约神学 vs 时代论（简明对照）'))
    c.append(table(['议题','圣约神学（改革宗）','时代论（达秘、司可福体系）'],[['解经钥匙','圣约；以新约解释旧约','七个时代；“字面”解释预言'],['以色列与教会','一个神的子民，教会是“神的以色列”（加6:16）','两个子民、两个计划'],['律法','道德律永久有效；礼仪律在基督里成全','律法时代已结束'],['旧约圣徒得救','唯独因信基督（预表中）','（各派说法不一）'],['千禧年','多为无千禧年派（欧陆改革宗主流）','灾前被提、前千禧年'],['婴儿洗礼','支持：约的延续性','否认']]))
    c.append(h2('apply','🌱','圣约神学的实际应用'))
    c.append('<div class="grid g3 reveal">'+''.join(f'<div class="card tile"><div class="big">{i}</div><h4>{t}</h4><p>{d}</p></div>' for i,t,d in [('👨‍👩‍👧','家庭','父母以约的应许养育儿女，家庭敬拜、要理问答教导（申6:7）。'),('⛪','教会','教会是约的群体；圣礼、纪律、敬拜都是约的生活（比利时信条第27–35条）。'),('🙏','确据','安慰不在于自己的感受，而在于神信实的应许与基督的血（海德堡第1问）。')])+'</div>')
    c.append(hc(1))
    return page('covenant.html','圣约神学',''.join(c))
