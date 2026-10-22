from lib import *
from v6lib import *
from books import BOOKS,CATS
from kings import ISRAEL,JUDAH
# KJV 版本的经节数（与和合本绝大多数相同）。来源：Bible SuperSearch《The Number of Verses in the Bible》(2019)；与 renniemaharaj/kjv-bible 审核表一致。
VERSES=[1533,1213,859,1288,959,658,618,85,810,695,816,719,942,822,280,406,167,1070,2461,915,222,117,1292,1364,154,1273,357,197,73,146,21,48,105,47,56,53,38,211,55,
1071,678,1151,879,1007,433,437,257,149,155,104,95,89,47,113,83,46,25,303,108,105,61,105,13,14,25,404]
SRC_V='https://www.biblesupersearch.com/2019/02/the-number-of-verses-in-the-bible/'
SRC_N='https://thirdmill.org/articles/rog_nicole/rog_nicole.NT_OT.html'
assert len(VERSES)==66 and sum(VERSES)==31102 and sum(VERSES[:39])==23145
# 成书世纪（保守派，约略）
EC={'15–14c BC':'创 出 利 民 申 书','11–10c BC':'士 得 撒上 撒下 诗 箴 传 歌','8c BC':'何 摩 拿 弥 赛','7c BC':'鸿 番 哈','6c BC':'王上 王下 耶 哀 结 但 该 亚','5c BC':'代上 代下 拉 尼 斯 玛','1c AD':'新约27卷','年代不详':'伯 珥 俄'}
AUTH=[('保罗',13,'罗—门'),('摩西',5,'创—申（另诗90）'),('约翰',5,'约、约一二三、启'),('所罗门',3,'箴（大部分）、传、歌'),('路加',2,'路、徒'),('彼得',2,'彼前、彼后'),('耶利米',2,'耶、哀（传统）'),('其他已知作者',23,'各一卷：约书亚、以斯拉、尼希米、诗篇（大卫等多人）、以赛亚、以西结、但以理、十二小先知、马太、马可、雅各、犹大'),('作者不详／有争议',11,'士、得、撒上下、王上下、代上下（传统归以斯拉）、斯、伯、来')]
def build():
    c=[]
    tot=sum(VERSES); ot=sum(VERSES[:39]); nt=tot-ot
    c.append(hero(['📊 圣经统计','可查证的数字','交互图表','标明来源'],'数字里的圣经：','66 卷 · 1,189 章 · 31,102 节',
      '本页所有数字都<b class="k">由可引用的数据计算</b>：章数来自本站 66 卷资料，经节数采用 <a href="'+SRC_V+'" target="_blank" rel="noopener">KJV 通行分节（Bible SuperSearch）</a>，旧约引用统计采用改革宗学者 <a href="'+SRC_N+'" target="_blank" rel="noopener">Roger Nicole（1958）</a>。<span class="uw">约略值都会标明</span>。'))
    c.append(legend_box())
    c.append(stats([('66','卷书（旧约39＋新约27）','📚','var(--gold)'),(f'{sum(b["ch"] for b in BOOKS):,}','章（旧约929＋新约260）','📖','var(--sky)'),(f'{tot:,}','节（KJV 分节）','🔢','var(--emer)'),(f'{ot:,}','旧约节数','📜','var(--vio)'),(f'{nt:,}','新约节数','✝️','var(--rose)'),('约1,500年','成书跨度（约1446 BC–AD 95）','⏳','var(--gold)')]))
    c.append(co('info','<p>'+rich(f'和合本的章节划分沿用 KJV 系统，章数同为 1,189；个别经节分界可能略有差异，本页节数以 KJV 为准。旧约占全本节数的 **{ot/tot*100:.1f}%**，新约占 **{nt/tot*100:.1f}%**。',False)+'</p>','说明'))
    # chapters & verses
    c.append(h2('size','📏','篇幅：每卷多少章、多少节'))
    c.append(h3('chap','66 卷章数'))
    c.append(vbars([(b['name'][:2],b['ch'],CATS[b['cat']][1],f'{b["name"]}：{b["ch"]} 章') for b in BOOKS],h=240,rot=True,cap='颜色＝书卷类别；悬停看书名与章数。诗篇 150 章最多。',id_='chchart'))
    c.append(h3('vers','66 卷节数'))
    c.append(vbars([(b['name'][:2],v,CATS[b['cat']][1],f'{b["name"]}：{v:,} 节') for b,v in zip(BOOKS,VERSES)],h=240,rot=True,cap='KJV 分节。诗篇 2,461 节最多，约翰二书 13 节最少。'))
    # extremes
    cum=0;mid=None
    for b in BOOKS:
        if cum+b['ch']>=595 and mid is None: mid=(b['name'],595-cum)
        cum+=b['ch']
    srt=sorted(zip(BOOKS,VERSES),key=lambda x:-x[1])
    c.append(h3('ext','之最'))
    c.append(table(['项目','结果','依据'],[
      ['📚 章数最多',f'{max(BOOKS,key=lambda b:b["ch"])["name"]}（150 章）','本站章数'],
      ['🔢 节数最多',f'{srt[0][0]["name"]}（{srt[0][1]:,} 节），其次 {srt[1][0]["name"]}（{srt[1][1]:,}）、{srt[2][0]["name"]}（{srt[2][1]:,}）','KJV 分节'],
      ['🪶 节数最少',f'{srt[-1][0]["name"]}（{srt[-1][1]} 节）、{srt[-2][0]["name"]}（{srt[-2][1]} 节）；旧约最短：俄巴底亚书（21 节）','KJV 分节'],
      ['📍 正中间的一章',f'第 595 章＝{mid[0]}第 {mid[1]} 篇（前后各 594 章）','由 1,189 章计算'],
      ['📏 最长的一章','诗篇 119 篇（176 节）','和合本／KJV'],['🤏 最短的一章','诗篇 117 篇（2 节）','和合本／KJV'],
      ['🧑‍🏫 写得最多的作者（按节数）',f'路加（路加福音＋使徒行传 {VERSES[41]+VERSES[43]:,} 节）多于保罗 13 卷书信（{sum(VERSES[44:57]):,} 节）','由经节数计算']]))
    # genre
    c.append(h2('genre','🎨','类别分布'))
    cats=list(CATS)
    by=lambda f:[(CATS[k][0],sum(f(b,v) for b,v in zip(BOOKS,VERSES) if b['cat']==k),CATS[k][1]) for k in cats]
    c.append(h3('g-books','按卷数 · 按章数 · 按节数'))
    c.append('<div class="grid g3">'+donut(by(lambda b,v:1),'按卷数',200)+donut(by(lambda b,v:b['ch']),'按章数',200)+donut(by(lambda b,v:v),'按节数（KJV）',200)+'</div>')
    c.append(co('core','<p>'+rich('按卷数看，**小先知书与保罗书信各 12–13 卷**最多；按篇幅看，==历史书与诗歌智慧书==占全本最大比重——圣经首先是一部**历史**：神在时间中的作为。',False)+'</p>','观察'))
    # authors
    c.append(h2('auth','✍️','作者与成书年代'))
    c.append(h3('a-who','谁写了几卷？（传统归属）'))
    c.append(vbars([(a,n,['var(--paul)','var(--law)','var(--rev)','var(--poet)','var(--acts)','var(--gen)','var(--majp)','var(--sky)','var(--mut)'][i],f'{a}：{n} 卷（{d}）') for i,(a,n,d) in enumerate(AUTH)],h=220,cap='保守派传统归属；“作者不详”包括圣经本身未署名、教会传统看法不一的书卷。合计 66 卷。'))
    assert sum(n for _,n,_ in AUTH)==66
    c.append(table(['作者','卷数','书卷'],[[f'<b>{E(a)}</b>',str(n),E(d)] for a,n,d in AUTH]))
    c.append(h3('a-era','按成书世纪'))
    def cnt(v): return 27 if v=='新约27卷' else len(v.split())
    c.append(vbars([(k,cnt(v),'var(--gold)' if 'AD' in k else ('var(--mut)' if '不详' in k else 'var(--sky)'),f'{k}：{v}') for k,v in EC.items()],h=200,cap='约略的保守派成书年代（例如摩西五经约 1446–1406 BC；列王纪约 560 BC；新约约 AD 45–95）。约伯记、约珥书、俄巴底亚书的年代各家不一。'))
    assert sum(cnt(v) for v in EC.values())==66
    c.append(co('xc','<p>'+rich('约 40 位作者、跨越约 1,500 年、三种语言（希伯来文、亚兰文、希腊文）、三大洲，却只有**一个主题**：==神在基督里的救赎==（路24:27）。这正是比利时信条所说圣经“{{BC5|这些经卷本身也证明它们是从神而来的}}”。',False)+'</p>','基督'))
    # OT in NT
    c.append(h2('otnt','🔗','旧约在新约中的引用'))
    c.append(h3('nicole','Roger Nicole 的保守统计（1958）'))
    c.append(vbars([('有引言公式的直接引用',224,'var(--gold)','224 处：有明确引言公式'),('以“又”接续的第二处引用',7,'var(--sky)','7 处'),('引言公式后的意译/概括',19,'var(--vio)','19 处'),('无公式但明确的引用',45,'var(--emer)','至少 45 处')],h=220,cap='合计至少 295 处，占新约约 352 节（4.4%）＝约每 22.5 节就有一节是引用。'))
    c.append('<div class="grid g2">'+donut([('摩西五经',94,'var(--law)'),('先知书',99,'var(--majp)'),('圣卷',85,'var(--poet)')],'被引用的 278 节旧约经文（按希伯来正典三部分）',200)
             +'<div>'+'<div class="hbar rv">'+''.join(f'<div><span>{a}</span><div class="t"><span style="--v:{n/4105:.3f};--c:{col}"></span></div><b>{n:,}</b></div>' for a,n,col in [('Nicole：引用',295,'var(--gold)'),('C. H. Toy：引用＋明确暗引',613,'var(--sky)'),('W. Dittmar',1640,'var(--vio)'),('E. Hühn：所有“令人想起”的经文',4105,'var(--rose)')])+'</div><p class="srcline">计数口径越宽，数字越大：从严格引用到一切暗引。</p></div></div>')
    c.append(co('core','<p>'+rich('Nicole 指出：新约**没有一次明确引用旧约次经**；在希伯来正典 22 卷（合并计）中只有六卷（士—得、歌、传、斯、拉—尼、代）未被明确引用。==新约作者把旧约当作神的话来引用==，从未质疑。',False)+'</p>','观察'))
    c.append(f'<p class="srcline">来源：Roger Nicole, “New Testament Use of the Old Testament,” in Carl F. H. Henry ed., <i>Revelation and the Bible</i> (Grand Rapids: Baker, 1958), pp. 137–151；网络版：<a href="{SRC_N}" target="_blank" rel="noopener">thirdmill.org</a>。</p>')
    # kings stats
    c.append(h2('kst','👑','诸王统计'))
    c.append(h3('k-num','数字速览'))
    L=max(JUDAH,key=lambda k:k[4]); LI=max(ISRAEL,key=lambda k:k[4])
    good=sum(1 for k in JUDAH if k[5] in('good','mix'))
    c.append(stats([(f'{len(JUDAH)}','犹大君王（含亚她利雅）','🟦','var(--sky)'),(f'{len(ISRAEL)}','以色列王','🟥','var(--rose)'),(f'{good}','犹大善王（含参半）','✅','var(--emer)'),('0','以色列善王','❌','var(--rose)'),(f'{L[4]} 年',f'最长：{L[0]}','⏳','var(--gold)'),(f'{LI[4]} 年',f'北国最长：{LI[0]}','⏳','var(--vio)')]))
    c.append('<p>详细的在位年数图、善恶分布和双轨时间线见 <a href="kings-chronicles.html">👑 列王纪 × 历代志</a>。</p>')
    c.append(co('app','<p>'+rich('数字的用处是**挂钩**：记住“929 + 260 = 1189”“39 + 27 = 66”“1446 · 966 · 931 · 722 · 586 · 538”，其他内容就有地方挂。',False)+'</p>','应用'))
    return page('stats.html','圣经统计',''.join(c),scripts='<script src="assets/js/v6.js?v=v6" defer></script>')
