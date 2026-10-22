"""v5: essence-first TL;DR per page + data-driven visuals (all static SVG/CSS, one-shot reveal animations)."""
import re
from lib import *
C=['var(--gold)','var(--sky)','var(--emer)','var(--rose)','var(--vio)']
TLDR={
'index.html':[('一个故事','创造—堕落—救赎—成全，==中心是基督==（路24:27）。'),('一条约线','[[恩典之约]]从@@创3:15@@贯穿到启21:3，历史之约是它的逐步施行。'),('一套记法','11 个时代色带 + 8 个钉子年份 + 66 卷口诀：**先骨架、再细节、后背诵**。')],
'story.html':[('四幕剧','**创造 · 堕落 · 救赎 · 成全**——整本圣经只讲一个故事。'),('一条红线','@@女人的后裔@@（创3:15）→ 亚伯拉罕的后裔 → 大卫的子孙 → ==基督==。'),('三条读法',';;以经解经;;、基督中心、救赎历史渐进：先问“这段在大故事的哪一幕？”')],
'covenant.html':[('三约框架','[[救赎之约]]（永恒，父与子）· [[行为之约]]（亚当）· [[恩典之约]]（基督为中保）。'),('一条递进链','挪亚 → 亚伯拉罕 → 摩西 → 大卫 → 新约：==一个恩典之约，多次施行==。'),('一个实质','新旧约是;;同一恩典之约的两种施行;;：实质为一，施行有别——这是与!!时代论!!的分水岭。')],
'timeline.html':[('8 个钉子','@@1446@@出埃及 · @@966@@建殿 · @@931@@分裂 · @@722@@北亡 · @@586@@南亡 · @@538@@归回。'),('42 位君王','统一 3 + 以色列 19（**全恶**，9 个王朝）+ 犹大 20（大卫一朝，**8 善**）。'),('最长的时代','两约之间约 425 年、族长约 360 年、士师约 356 年——看下方时代长度图。')],
'geography.html':[('一座陆桥','迦南夹在**埃及与美索不达米亚**之间：==神把子民放在列国的十字路口==。'),('四条纵带','沿海平原 · 中央山地 · 约旦裂谷 · 外约旦高原——由西向东记。'),('地理服务神学','应许之地是预表：亚伯拉罕的后裔要“承受世界”（罗4:13）。')],
'ot.html':[('五类 39 卷','律法 5 · 历史 12 · 诗歌 5 · 大先知 5 · 小先知 12。'),('一条主轴','==应许 · 预表 · 等候==：“这经就是为我作见证的”（约5:39）。'),('读每卷的顺序','⏮️ 前因后果 → ①②③ 核心三要点 → 结构图 → ★ 必背经文 → 易错点。')],
'nt.html':[('五类 27 卷','福音 4 · 历史 1 · 保罗 13 · 普通 8 · 预言 1。'),('一条主轴','==应验 · 实体 · 差遣==：旧约的影儿在基督里成了实体（西2:17）。'),('一种张力','[[已然—未然]]：国度已经降临，尚未完全；教会在两次降临之间生活。')],
'creeds.html':[('三份 · 三个战场','使徒信经＝洗礼告白；尼西亚＝**基督的神性**与圣灵；亚他那修＝==三一与二性==的精确语法。'),('同一副骨架','三份都是**父—子—圣灵**的三一结构；后两份是对异端的精准回答。'),('三天背三份','先背使徒信经（12 句），再尼西亚，最后用遮盖模式分段背亚他那修。')],
'forms.html':[('比利时信条 1561','37 条：**我们相信什么**——从神、圣经到教会与末日。'),('海德堡要理问答 1563','129 问 · 52 主日 · 三部分：==罪与苦难 → 救赎 → 感恩==。'),('多特信经 1618–19','五项教义回应抗辩派：@@无条件拣选@@与**有效的恩典**。')],
'memory.html':[('先挂钩','口诀把内容挂在已知的东西上：66 卷口诀表、钉子年份。'),('再回忆','闪卡、选择题、排序游戏：==主动回忆比重读有效得多==。'),('后间隔','两周计划按 1-2-4-7 天间隔复习，信经用遮盖模式逐句背。')],
'sources.html':[('唯一逐字来源','信经与三项联合信条全部逐字取自 **ccifellowship.org**。'),('构建时校验','每一处短引文都必须是原文子串，否则==构建失败==。'),('经文与年代','经文采用和合本；年代采用保守派 Thiele 式，个别年份 ±1–2 年。')],
}

TLDR.update({
'gospels.html':[('四幅肖像','**王 · 仆人 · 人子 · 神子**：太“应验”、可“立刻”、路“救恩”、约“信”。'),('横向','同一事件四卷并排：==详略不同≠矛盾==，交互重叠图一点即筛。'),('为何四卷','两三个见证；比利时信条第4条列出“四福音书”。')],
'life-of-christ.html':[('五个钉子','@@6–4 BC@@ 降生 · @@AD 26/27@@ 受洗 · 3 个逾越节 · @@AD 30@@（或33）十字架 · 40+10 天。'),('地图联动','点击 48 个事件，地图==飞到那个地方==。'),('三职二状态','先知 · 祭司 · 君王；降卑与升高（使徒信经逐字）。')],
'kings-chronicles.html':[('两种眼光','列王纪＝**被掳中的诊断**；历代志＝**归回后的盼望**。'),('双轨时间线','悬停一位王，==同期的王一起亮起==。'),('记忆系统','首字口诀、8 位善王、北国 9 个王朝链。')],
'compare.html':[('以经解经','圣经最好的注释是圣经本身。'),('10 组对照','创↔启、利↔来、但↔启、罗↔加、雅↔罗……'),('核心洞见','每组一句：==相同显出主线，不同显出使命==。')],
'stats.html':[('三个数字','**66 卷 · 1,189 章 · 31,102 节**（KJV 分节）。'),('来源可查','经节数：Bible SuperSearch；旧约引用：Roger Nicole（1958）。'),('之最','正中间的一章是诗篇117篇；路加写的节数多于保罗。')],
})
TLDR.update({
'pentateuch.html':[('一卷一个动词','创＝开端 · 出＝救赎 · 利＝圣洁 · 民＝漂流 · 申＝重申。'),('一个重心','五经约三分之一写在==西奈山下不到一年==：[[救赎的目的是同住]]。'),('一条读法','先恩典后律法（出20:2）；礼仪在基督里成全（比利时信条第25条）。')],
'history.html':[('一条弧线','得地 → 士师 → 王国 → 分裂 → 被掳 → 归回：约 1406–430 BC。'),('两种史观','约书亚记—列王纪＝==为什么亡国==；历代志—尼希米记＝[[我们还有将来]]。'),('一个答案','每种制度都失败了：历史书在等候 @@真大卫@@（结34:23）。')],
'poetry.html':[('一条总纲','==敬畏耶和华是智慧的开端==（箴1:7；伯28:28；传12:13）。'),('三个角度','箴言＝规律；约伯记＝[[规律的例外]]；传道书＝日光之下的界限。'),('两种语言','诗篇＝向神说话；雅歌＝爱的语言——@@全部人生都在神面前@@。')],
})
def tldr(fn):
    it=TLDR.get(fn)
    if not it: return ''
    return '<div class="tldr" role="list" aria-label="本页三要点">'+''.join(f'<div role="listitem" style="--c:{C[i%5]}"><i>{i+1}</i><b>{E(t)}</b>{rich(x,False)}</div>' for i,(t,x) in enumerate(it))+'</div>'
def canonbars():
    from books import BOOKS,CATS
    def bar(sel,lab):
        bs=[b for b in BOOKS if sel(b)]; tot=sum(b['ch'] for b in bs)
        segs=''.join(f'<a href="{"ot" if b["n"]<=39 else "nt"}.html#b-{b["id"]}" style="flex:{b["ch"]} 1 0;--c:{CATS[b["cat"]][1]}" title="{b["name"]} · {b["ch"]}章">{E(b["name"][:1]) if b["ch"]>=20 else ""}</a>' for b in bs)
        return f'<div class="srcline"><b>{lab}</b> · {len(bs)} 卷 · {tot} 章</div><div class="cbar" role="img" aria-label="{lab}按章数比例">{segs}</div>'
    return bar(lambda b:b['n']<=39,'旧约')+bar(lambda b:b['n']>39,'新约')+'<p class="srcline">每格宽度＝章数（全本 1189 章）；点击跳到该卷。诗篇 150 章最宽，俄巴底亚书、腓利门书等一章书最窄。</p>'
def presence():
    P=[('伊甸','创2:8',92,'神与人同行'),('被逐','创3:24',18,'基路伯把守'),('族长的坛','创12–50',38,'显现·立坛'),('会幕荣耀','出40:34',70,'云彩充满会幕'),('圣殿荣耀','王上8:11',80,'荣光充满殿'),('荣耀离殿','结10:18',12,'被掳 586 BC'),('第二圣殿','拉6:15',42,'无约柜·无荣云'),('以马内利','约1:14',90,'道“住在”人间'),('圣灵内住','林前3:16',93,'教会是殿'),('新耶路撒冷','启21:3',100,'帐幕在人间')]
    W,H,L,T,B=1000,300,80,34,250; n=len(P); xs=[L+i*(W-L-40)/(n-1) for i in range(n)]; ys=[B-(v/100)*(B-T) for _,_,v,_ in P]
    d='M'+' '.join(f'{x:.0f},{y:.0f}' for x,y in zip(xs,ys))
    pts=''.join(f'<g><circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="var(--gold)" stroke="var(--bg)" stroke-width="2"/><text x="{x:.0f}" y="{y-14:.0f}" text-anchor="middle" font-size="14" font-weight="800">{E(a)}</text><text x="{x:.0f}" y="{B+22}" text-anchor="middle" font-size="12" class="mut">{E(r)}</text><text x="{x:.0f}" y="{B+38}" text-anchor="middle" font-size="11" class="mut">{E(s)}</text></g>' for (a,r,v,s),x,y in zip(P,xs,ys))
    return (f'<figure class="vchart" style="margin:10px 0"><svg viewBox="0 0 {W} {H+10}" role="img" aria-label="神与人同在的曲线"><defs><linearGradient id="pg" x1="0" x2="1"><stop offset="0" stop-color="var(--emer)"/><stop offset=".5" stop-color="var(--rose)"/><stop offset="1" stop-color="var(--gold)"/></linearGradient></defs>'
            f'<line x1="{L}" y1="{B}" x2="{W-20}" y2="{B}" stroke="var(--line2)"/><text x="{L-70}" y="{T+4}" font-size="11" class="mut">同在</text><text x="{L-70}" y="{B}" font-size="11" class="mut">远离</text>'
            f'<path d="{d}" fill="none" stroke="url(#pg)" stroke-width="4" stroke-linejoin="round" class="draw" style="--len:2600"/>{pts}</svg>'
            '<figcaption class="srcline">📈 示意图：“神的同在”这条主题线（圣殿神学）——伊甸是第一座“圣所”，新耶路撒冷是它的成全；高低表示同在的亲近程度，非数据。</figcaption></figure>')
def hbar(rows,unit='',note_=''):
    mx=max(v for _,v,_ in rows)
    return '<div class="hbar">'+''.join(f'<div><span>{t}</span><div class="t"><span style="--v:{v/mx:.3f};--c:{c}"></span></div><b>{v}{unit}</b></div>' for t,v,c in rows)+'</div>'+(f'<p class="srcline">{note_}</p>' if note_ else '')
def eralen():
    R=[('🐑 族长',2166-1805,'#ff9f5a'),('🔥 出埃及与旷野',40,'#ff7aa8'),('⚔️ 征服与士师',1406-1050,'#3ee0a1'),('👑 统一王国',1050-931,'#5ec8ff'),('💔 分裂王国',931-586,'#8ea2ff'),('⛓️ 被掳',605-538,'#b18cff'),('🏗️ 归回',538-430,'#34d6d0'),('🤫 两约之间',430-5,'#9aa3c7'),('✝️ 基督',35,'#f5c76b'),('🕊️ 使徒教会',65,'#ff6b6b')]
    return hbar(R,' 年','按保守派年代约数（族长自亚伯拉罕出生 2166 BC 起）。一眼看出：两约之间、族长、士师、分裂王国是四段最长的时期。')
def _n(t): return len(re.sub(r'[\s，。；：、“”‘’（）？！,.;:()\-—–]','',t))
def creedlen():
    R=[('🌱 使徒信经',_n(SRC['AP'][0]),'var(--emer)'),('🔥 尼西亚信经',_n(SRC['NI'][0]),'var(--gold)'),('🔺 亚他那修信经',_n(SRC['AT'][0]),'var(--vio)')]
    return hbar(R,' 字','按 ccifellowship.org 中文本计数（不含标点）。越晚的信经越长：异端越精细，回答越精确。')
def hcparts():
    R=[('🫶 引言 Q1–2',2,'var(--sky)'),('😢 罪与苦难 Q3–11',9,'var(--red)'),('✝️ 救赎 Q12–85',74,'var(--gold)'),('🙏 感恩 Q86–129',44,'var(--emer)')]
    return hbar(R,' 问','海德堡要理问答 129 问的篇幅分布：一半以上在讲“救赎”——福音是主体，律法是镜子，感恩是回应。')
def dortbar():
    rows=[];LB=['🌱 第一项 · 拣选与弃绝','✝️ 第二项 · 基督的死','🔥 第三四项 · 败坏与归正','🛡️ 第五项 · 圣徒持守']
    for i,h in enumerate(DT['heads']):
        a=sum(1 for x in h['articles'] if x['title'].startswith('第')); rows.append((LB[i],a,C[i%5]))
    return hbar(rows,' 条','多特信经各部分正面条文数（不含错谬驳斥），按 ccifellowship.org 数据自动统计。')

def bookquick():
    from books import BOOKS,CATS
    rows=[]
    for b in BOOKS:
        t,r=b['kv'][0]; one=b['one'].split('：')
        rows.append([f'<b style="color:{CATS[b["cat"]][1]}">{b["n"]}</b>',f'<a href="{"ot" if b["n"]<=39 else "nt"}.html#b-{b["id"]}">{E(b["name"])}</a>',rich(f'**{one[0]}**' + ('：'+one[1] if len(one)>1 else ''),False),f'<span class="must">{E(r)}</span>'])
    return '<details class="dx"><summary>📋 66 卷速查：一句话精髓 + ★ 必背经文（点开）</summary><div class="in">'+table(['#','书卷','一句话精髓','★ 必背'],rows)+'</div></details>'
