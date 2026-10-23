"""v9: 文化与生活 — calendar & feasts, tabernacle/temple, sects, Roman rule, weights/money/measures,
houses/agriculture/marriage, empires × Israel timeline. Core points only; charts are build-time SVG."""
import math
from lib import *
from v6lib import hero,stats,donut
from genre import R,htable,flowsteps,kbox,mnem,rtable,grid,card,spans
from v4extra import feasts
def wheel():
    """12-month calendar wheel: inner ring = months, middle = season (rain/dry), outer = Gezer-calendar farm work; feast markers"""
    M=[('尼散','3–4月','#ff6b6b'),('以珥','4–5月','#ff9f43'),('西弯','5–6月','#ffcb5c'),('搭模斯','6–7月','#f5a623'),('埃波','7–8月','#e8833a'),('以禄','8–9月','#d9a441'),
       ('提斯利','9–10月','#5cc8ff'),('玛西班','10–11月','#4f8bff'),('基斯流','11–12月','#6f7bff'),('提别','12–1月','#8e7bff'),('细罢特','1–2月','#3ee0a1'),('亚达','2–3月','#2dd4bf')]
    FEAST={0:'🐑 逾越·除酵·初熟',2:'🌾 七七（五旬节）',6:'📯 吹角·🩸赎罪·⛺住棚',8:'🕎 修殿节',11:'🎭 普珥节'}
    FARM=[(0,2,'割大麦·收割','#ffcb5c'),(2,3,'割小麦','#f5a623'),(3,5,'修剪葡萄','#b78cff'),(5,6,'夏果','#ff6fa5'),(6,8,'收橄榄','#3ee0a1'),(8,10,'播种','#5cc8ff'),(10,11,'晚播','#4f8bff'),(11,12,'割麻','#9aa3c7')]
    cx=cy=260;o=[]
    def arc(r0,r1,a0,a1,col,cls=''):
        a0r,a1r=math.radians(a0-90),math.radians(a1-90)
        p=lambda r,a:(cx+r*math.cos(a),cy+r*math.sin(a))
        x0,y0=p(r1,a0r);x1,y1=p(r1,a1r);x2,y2=p(r0,a1r);x3,y3=p(r0,a0r);lg=1 if a1-a0>180 else 0
        return f'<path class="{cls}" d="M{x0:.1f},{y0:.1f} A{r1},{r1} 0 {lg} 1 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} A{r0},{r0} 0 {lg} 0 {x3:.1f},{y3:.1f} Z" fill="{col}"/>'
    def tx(r,a,t,cls,rot=True):
        ar=math.radians(a-90);x,y=cx+r*math.cos(ar),cy+r*math.sin(ar);rr=a if a<=90 or a>=270 else a-180
        return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="middle" dominant-baseline="middle"'+(f' transform="rotate({rr:.0f} {x:.1f} {y:.1f})"' if rot else '')+f'>{E(t)}</text>'
    for i,(n,g,c) in enumerate(M):
        a0,a1=i*30,(i+1)*30
        o.append(arc(70,150,a0+.6,a1-.6,c,'wm'));o.append(tx(122,a0+15,n,'wl'));o.append(tx(92,a0+15,g,'wg'))
    # seasons ring: rain (提斯利 6 → 尼散 0 i.e. months 6..11 + 0) vs dry (1..5)
    o.append(arc(152,172,180+.5,360-.5,'#4f8bff','ws'));o.append(arc(152,172,0+.5,30-.5,'#4f8bff','ws'));o.append(arc(152,172,30+.5,180-.5,'#ffb34d','ws'))
    o.append(tx(162,255,'🌧️ 雨季（秋雨→晚雨）','wsl'));o.append(tx(162,105,'☀️ 旱季','wsl'))
    for a,b,t,c in FARM:o.append(arc(174,214,a*30+.6,b*30-.6,c,'wf'));o.append(tx(194,(a+b)*15,t,'wfl'))
    for i,t in FEAST.items():
        ar=math.radians(i*30+15-90);x,y=cx+236*math.cos(ar),cy+236*math.sin(ar)
        o.append(f'<g class="wfe" style="--i:{i}"><circle cx="{x:.1f}" cy="{y:.1f}" r="7"/></g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="66" class="wc"/><text x="{cx}" y="{cy-10}" class="wct" text-anchor="middle">宗教年</text><text x="{cx}" y="{cy+14}" class="wcs" text-anchor="middle">始于尼散月（出12:2）</text><text x="{cx}" y="{cy+34}" class="wcs" text-anchor="middle">民事年始于提斯利</text>')
    leg=''.join(f'<span><b>●</b> {M[i][0]}：{t}</span>' for i,t in FEAST.items())
    return (f'<figure class="wheel rv"><svg viewBox="0 0 520 520" role="img" aria-label="以色列历法转盘：月份、雨季旱季、农事与节期">{"".join(o)}</svg>'
            f'<figcaption><div class="wleg">{leg}</div><p class="srcline">内圈：犹太月名（太阴历，约每3年加闰亚达月）与公历对应；中圈：雨季/旱季；外圈：基色历（Gezer Calendar，约主前10世纪）所记农事；红点＝节期所在月。</p></figcaption></figure>')
def tabernacle():
    """schematic plan of the tabernacle court (100×50 cubits, 出27:18) with furniture"""
    S=8  # px per cubit
    W,H=100*S+40,50*S+40;x0,y0=20,20
    o=[f'<rect x="{x0}" y="{y0}" width="{100*S}" height="{50*S}" class="tbc"/>',
       f'<rect x="{x0+100*S-4}" y="{y0+15*S}" width="8" height="{20*S}" class="tbg"/>',
       # tent: 30×10 cubits at west end (center line), holy place 20, most holy 10
       f'<rect x="{x0+10*S}" y="{y0+20*S}" width="{30*S}" height="{10*S}" class="tbt"/>',
       f'<rect x="{x0+10*S}" y="{y0+20*S}" width="{10*S}" height="{10*S}" class="tbh"/>',
       f'<line x1="{x0+20*S}" x2="{x0+20*S}" y1="{y0+20*S}" y2="{y0+30*S}" class="tbv"/>']
    items=[(15,25,'📦','约柜·施恩座','至圣所（出25:10–22）'),(22.5,24.99,'🔥','香坛','祷告（启8:3–4）'),(30,22,'🕎','金灯台','世界的光（约8:12）'),(30,28,'🍞','陈设饼桌','生命的粮（约6:35）'),(52,25,'🫗','洗濯盆','洁净（多3:5）'),(72,25,'🐂','铜祭坛','代赎（来9:22）'),(97,25,'🚪','院门（东）','“我就是门”（约10:9）')]
    for cxu,cyu,ic,n,d in items:
        x,y=x0+cxu*S,y0+cyu*S
        o.append(f'<g class="tbi"><title>{E(n)}：{E(d)}</title><circle cx="{x}" cy="{y}" r="17"/><text x="{x}" y="{y+6}" text-anchor="middle" class="tbe">{ic}</text><text x="{x}" y="{y+(36 if cyu>=25 else -24)}" text-anchor="middle" class="tbl">{E(n)}</text></g>')
    o.append(f'<text x="{x0+15*S}" y="{y0+20*S-46}" text-anchor="middle" class="tbz">至圣所 10×10</text><text x="{x0+30*S}" y="{y0+20*S-46}" text-anchor="middle" class="tbz">圣所 20×10</text><text x="{x0+60*S}" y="{y0+46*S}" text-anchor="middle" class="tbz">外院 100×50 肘（约45×23 米）</text>')
    o.append(f'<path d="M{x0+92*S},{y0+8*S} L{x0+20*S},{y0+8*S}" class="tbar" marker-end="url(#tba)"/><text x="{x0+56*S}" y="{y0+6*S}" text-anchor="middle" class="tbz">敬拜者自东向西：先祭坛，后进前</text>')
    return (f'<figure class="tabn rv"><div class="tbw"><svg viewBox="0 0 {W} {H}" style="min-width:640px" role="img" aria-label="会幕平面示意"><defs><marker id="tba" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="currentColor"/></marker></defs>{"".join(o)}</svg></div>'
            '<figcaption class="srcline">按出25–27、30章尺寸示意（1 肘≈45 厘米）。路线＝从祭坛到施恩座：先有代赎，后有亲近（来10:19–22）。</figcaption></figure>')
def lab(v): return f"1/{round(1/v)}" if v<1 else (f"{v/1e4:g}万" if v>=1e4 else f"{v:g}")
def logbars(rows,unit):
    """log-scale horizontal bars (values span 5 orders of magnitude)"""
    mx=max(math.log10(v) for _,v,_,_ in rows);mn=min(math.log10(v) for _,v,_,_ in rows)
    return '<div class="hbar lg rv">'+''.join(f'<div title="{E(t)}"><span>{n}</span><div class="t"><span style="--v:{(math.log10(v)-mn+.25)/(mx-mn+.25):.3f};--c:{c}"></span></div><b>{lab(v)}{unit}</b></div>' for n,v,c,t in rows)+'</div><p class="srcline">对数刻度（每一格相差10倍）；以“1得拿利＝一天工钱”（太20:2）为单位。</p>'
def build():
    c=[]
    c.append(hero(['🏺 文化与生活','读经背景','图表 + 图标'],'回到经文的日常：','历法、圣殿、派别、罗马与度量衡',
      '圣经不是在真空里写成的。本页只取<b class="k">读懂经文必需的背景</b>：一年怎么过（节期）、神在哪里与人相会（会幕/圣殿）、耶稣时代的派别与罗马统治、钱和尺寸到底有多大、房屋田地与婚俗，以及以色列与周边帝国的时间对照。每一项都落到“这对读经有什么用”。'))
    c.append(legend_box())
    c.append(stats([('12','月·太阴历','📅','var(--gold)'),('7','年度节期','🎺','var(--rose)'),('3','朝圣大节','🛕','var(--sky)'),('4','主要派别','🧑‍⚖️','var(--vio)'),('1','得拿利＝日薪','🪙','var(--emer)'),('45cm','1 肘','📏','var(--amb)')]))
    # 1 calendar
    c.append(h2('calendar','📅','历法与节期：把救赎史写进日历'))
    c.append(co('core','<p>'+R('以色列用**太阴历**（月初见新月），以**尼散月**为正月（出12:2，出埃及之月）；一日从**日落**开始（创1“有晚上，有早晨”）。**安息日**每七日一次，**安息年**每七年，**禧年**每五十年（利25）——==时间本身被神分别为圣==。')+'</p>','要点'))
    c.append('<div class="calx">'+wheel()+'<div>'+feasts()+'</div></div>')
    c.append(kbox('三层“安息”节奏',['**安息日**（出20:8–11）：纪念创造与出埃及的拯救（申5:15）；主日（复活之日）在基督里成全其精意（来4:9–10）。','**安息年**（利25:1–7）：地要休息、免债——神才是地的主人。','**禧年**（利25:8–55）：归还产业、释放奴仆；耶稣在拿撒勒宣告“神悦纳人的禧年”（路4:19）。'],'必懂'))
    # 2 temple
    c.append(h2('temple','🕍','会幕与圣殿：神住在百姓中间'))
    c.append(tabernacle())
    c.append(rtable(['','时间','特点','结局'],[['⛺ **会幕**','^^约1446 BC^^ 起','按“山上指示的样式”（出25:40）；可移动、随营','示罗→挪伯→基遍'],['🏛️ **所罗门圣殿**','^^966–959 BC^^ 建','会幕尺寸加倍；约柜入殿、荣耀充满（王上8）','^^586 BC^^ 被巴比伦焚毁'],['🧱 **第二圣殿**','^^516 BC^^ 完工','所罗巴伯重建，“比先前的荣耀小”（该2:3），但应许“后来的荣耀必大过先前”（该2:9）','希律扩建'],['✨ **希律圣殿**','^^约20 BC^^ 起扩建','外邦人院、妇女院、以色列院；耶稣洁净圣殿、教训','^^AD 70^^ 被罗马焚毁（太24:2）']]))
    c.append(co('xc','<p>'+R('“你们拆毁这殿，我三日内要再建立起来……但耶稣这话是以他的身体为殿。”（约2:19–21）——**基督是真圣殿**；教会在他里面成为“圣灵的殿”（林前3:16），终局是“城内我未见有殿，因主神全能者和羔羊为城的殿”（启21:22）。')+'</p>','圣殿的红线'))
    # 3 sects
    c.append(h2('sects','🧑‍⚖️','耶稣时代的派别'))
    S=[('法利赛人','📜','#5ec8ff','“分别出来的人”；源于马加比时期的哈西典人','守律法与**口传传统**；信复活、天使、灵（徒23:8）','百姓中威望最高；会堂与文士','“假冒为善”之责（太23）；但尼哥底母、保罗出身此派'),
       ('撒都该人','🏛️','#ffcb5c','祭司贵族；与大祭司家族相连','只认**摩西五经**为最高权威；!!不信复活!!、天使（太22:23）','掌控圣殿与公会；亲罗马','复活之辩（太22:23–33）；主导逮捕使徒（徒4–5）'),
       ('爱色尼派','🏜️','#3ee0a1','退隐的洁净团体；常与昆兰社群相连','严格洁净、共产、等候末世；抄写经卷','离开圣殿（认为被玷污）','新约未直接提及；死海古卷印证旧约经文的稳定传承'),
       ('奋锐党','🗡️','#ff6b6b','反罗马的激进民族主义（约 AD 6 犹大起事 徒5:37）','只有神是王，武力驱逐罗马','游击与暴动；AD 66–70 起义主力','门徒“奋锐党的西门”（路6:15）——福音使仇敌同桌')]
    c.append('<div class="sect rv">'+''.join(f'<div class="sc" style="--c:{col}"><div class="sh"><span>{ic}</span><b>{n}</b></div><dl><dt>起源</dt><dd>{R(a)}</dd><dt>信念</dt><dd>{R(b)}</dd><dt>社会</dt><dd>{R(d)}</dd><dt>与福音</dt><dd>{R(e)}</dd></dl></div>' for n,ic,col,a,b,d,e in S)+'</div>')
    Y,N,P='<span class="yes">✓</span>','<span class="no">✗</span>','<span class="mid">△</span>'
    c.append(table(['对比','法利赛','撒都该','爱色尼','奋锐'],[['信死人复活',Y,N,Y,Y],['信天使与灵',Y,N,Y,Y],['口传传统有约束力',Y,N,P,P],['与罗马合作',P,Y,N,N],['掌控圣殿',N,Y,N,N]],'mx'))
    c.append(co('trap','<p>'+R('!!“法利赛人＝坏人”是简化!!。他们的问题不是“太看重圣经”，而是**用人的传统加添、架空神的诫命**（可7:8–13），并以守律法为称义的根据（路18:9–14）。')+'</p>'))
    # 4 rome
    c.append(h2('rome','🦅','罗马统治：福音传开的“道路”'))
    c.append(flowsteps([('👑','皇帝','奥古斯都下旨报名上册（路2:1）；提庇留在位第十五年约翰出来（路3:1）','#ffcb5c'),('🏛️','叙利亚总督','居里扭（路2:2）；统辖东方军团','#ff9f43'),('⚖️','巡抚 / 分封王','彼拉多（犹太）、希律安提帕（加利利）；死刑权在罗马（约18:31）','#ff6b6b'),('🕍','公会与大祭司','71人公会；亚那、该亚法（约18:13）','#b78cff'),('🏘️','地方','税吏、百夫长、会堂','#5cc8ff')]))
    E_=[('奥古斯都','-27',14,'#ffcb5c','耶稣降生（路2:1）'),('提庇留','14',37,'#ff9f43','耶稣事工与受难（路3:1）'),('该犹·加利古拉','37',41,'#ff6b6b','欲在圣殿立像'),('革老丢','41',54,'#ff6fa5','饥荒（徒11:28）；逐犹太人出罗马（徒18:2）'),('尼禄','54',68,'#b78cff','保罗上诉该撒（徒25:11）；64年逼迫'),('维斯帕先 / 提多','69',81,'#5cc8ff','AD 70 圣殿被毁'),('图密善','81',96,'#3ee0a1','约翰被放逐拔摩（启1:9）')]
    c.append(spans([(n,int(a),b,col,t) for n,a,b,col,t in E_],-30,100,[-25,0,25,50,75,100],'罗马皇帝在位年代（史学通行年代）与新约事件。',rowh=28,lw=150))
    c.append(co('info','<p>'+R('**罗马和平**（Pax Romana）、大道与海路、通用**希腊语**、各城的**犹太会堂**——加拉太书说“及至时候满足”（加4:4），这些都成为福音快速传开的管道。另一面：**皇帝崇拜**使“耶稣是主”成为有代价的认信（启2:13）。')+'</p>'))
    # 5 measures
    c.append(h2('measures','⚖️','度量衡与钱币：数字有多大？'))
    c.append(logbars([('小钱（勒普顿）',1/128,'#9aa3c7','寡妇的两个小钱（可12:42）'),('大钱（夸德兰）',1/64,'#8ea2ff','“一文钱也不能剩”（太5:26）'),('得拿利 / 德拉克马',1,'#3ee0a1','一天工钱（太20:2）'),('双德拉克马（殿税）',2,'#5cc8ff','太17:24'),('斯达特',4,'#ffcb5c','鱼口中的钱，二人殿税（太17:27）'),('弥拿',100,'#ff9f43','十锭银子（路19:13）'),('他连得',6000,'#ff6b6b','按才干受托（太25:15）'),('一万他连得',6e7,'#e8517a','约16万年工资的债（太18:24）')],' 日'))
    c.append(table(['类别','单位','约合','读经例子'],[['📏 长度','指 / 掌 / 虎口 / 肘','≈2 / 7.5 / 22 / 45 厘米','歌利亚“六肘零一虎口”≈2.9米（撒上17:4）'],['🛤️ 距离','斯他狄（里）/ 安息日可走的路','≈185 米 / ≈1 公里','以马忤斯离耶路撒冷“约有二十五里”≈11公里（路24:13）'],['🌾 干量','伊法 / 贺梅珥','≈22 升 / ≈220 升','吗哪每人一俄梅珥（≈2升，出16:16）'],['🫒 液量','罢特 / 欣','≈22 升 / ≈3.7 升','迦拿六口缸，每口两三桶（≈80–120升，约2:6）'],['⚖️ 重量','舍客勒 / 他连得','≈11.4 克 / ≈34 公斤','押沙龙的头发每年二百舍客勒（撒下14:26）']]))
    c.append(mnem([('钱','1小钱 × 128 = 1得拿利 = 1天','寡妇投的是“一切养生的”（可12:44）——金额最小，奉献最多'),('债','10,000他连得 ÷ 100得拿利 = 60万倍','比喻的对比是**无法偿还 vs 微不足道**（太18:23–35）')]))
    # 6 daily life
    c.append(h2('life','🏠','房屋·农业·婚俗'))
    c.append(grid([card('🏠 四室房（以色列典型民居）','<p>'+R('石墙泥顶、平屋顶（可晾晒、祷告 徒10:9；拆房顶缒下瘫子 可2:4）；底层常养牲畜，楼上住人。“**楼房**”（上房）是待客与聚会处（徒1:13）。')+'</p>','#ffcb5c'),
      card('🌾 农业三宝：五谷·新酒·油','<p>'+R('“五谷、新酒和油”（申7:13）是立约的祝福指标；靠**秋雨与春雨**（申11:14）。撒种比喻的四种土（太13）、葡萄园比喻（赛5；太21）都是日常景象。')+'</p>','#3ee0a1'),
      card('🐑 牧羊与渔业','<p>'+R('羊圈只有一个门，牧人叫着自己羊的名字（约10:3）；加利利海的拖网与撒网（太4:18；13:47）。==耶稣用最日常的图画讲天国==。')+'</p>','#5cc8ff')],3))
    c.append(h3('marriage','婚俗：从订婚到婚宴'))
    c.append(flowsteps([('🤝','订婚','具法律效力，需休书才能解除（太1:18–19）；付聘礼','#ffcb5c'),('⏳','等候','约一年；新郎“去预备地方”（约14:2–3 的背景）','#ff9f43'),('🪔','迎娶','新郎夜间来接新娘，伴娘持灯（太25:1–13）','#ff6b6b'),('🍷','婚宴','可长达七日；缺酒是大羞辱（约2:3）','#b78cff'),('👑','成全','“羔羊婚娶的时候到了”（启19:7）——教会是新妇（弗5:25–32）','#5cc8ff')]))
    # 7 timeline
    c.append(h2('empires','⏳','帝国时间线 × 以色列'))
    rows=[('埃及新王国',-1550,-1070,'#ff9f5a','出埃及时期'),('赫人帝国',-1650,-1180,'#8ea2ff','宗主条约'),('新亚述',-911,-609,'#ff6b6b','722 灭北国'),('新巴比伦',-626,-539,'#f5c76b','586 毁圣殿'),('波斯',-539,-331,'#b18cff','古列谕旨'),('希腊·托勒密·塞琉古',-331,-63,'#5cc8ff','但11'),('罗马',-63,135,'#e8517a','新约世界'),
          ('族长',-2091,-1876,'#ffd27a','亚伯拉罕—雅各'),('在埃及',-1876,-1446,'#ffb34d','430年（出12:40）'),('旷野·得地·士师',-1446,-1050,'#3ee0a1','约书亚、士师'),('联合王国',-1050,-931,'#ffcb5c','扫罗·大卫·所罗门'),('北国以色列',-931,-722,'#ff6fa5','19王'),('南国犹大',-931,-586,'#4f8bff','20王'),('被掳与归回',-605,-430,'#9aa3c7','但以理、以斯拉、尼希米'),('两约之间',-430,-5,'#8e7bff','“沉默的400年”'),('基督与使徒',-5,96,'#ff6b6b','福音与教会')]
    c.append(spans(rows,-2100,140,[-2000,-1500,-1000,-500,0],'上7行＝周边帝国；下9行＝以色列（保守派年代，约数）。',bands=[('族长',-2091,-1876,'#ffd27a'),('王国',-1050,-586,'#4f8bff'),('新约',-5,96,'#ff6b6b')],rowh=26,lw=170))
    c.append(co('core','<p>'+R('读先知书与历史书时，先问“**此时谁是霸主**”：亚述（以赛亚、约拿、那鸿）、巴比伦（耶利米、哈巴谷、但以理）、波斯（以斯拉、尼希米、以斯帖、哈该、撒迦利亚）。==列国兴衰都在神的护理之下==（但2:21），为要预备“日期满足”时弥赛亚的来临。')+'</p>','读经用法'))
    c.append(note('🧩 资料说明','<p>度量衡为学界常用近似值（肘按45厘米计）；货币换算以新约时代为准。年代采用保守派（Thiele 式）框架，个别年份有±1–2年差异。会幕平面按出埃及记尺寸示意。</p>'))
    return page('culture.html','文化与生活',''.join(c))
