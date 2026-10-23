import re
from lib import *
from v6lib import *
from kings import ISRAEL,JUDAH,UNITED
def split_refs(r):
    k=[];ch=[];cur=None
    for part in re.split(r'[；;]',r):
        part=part.strip()
        m=re.match(r'(撒上|撒下|王上|王下|代上|代下|赛|耶)',part)
        if m: cur=m.group(1)
        elif cur: part=cur+part
        (ch if cur and cur.startswith('代') else k).append(part) if cur in ('撒上','撒下','王上','王下','代上','代下') else None
    return '；'.join(k),'；'.join(ch)
VC={'good':('var(--emer)','✅ 善'),'evil':('var(--rose)','❌ 恶'),'mix':('var(--gold)','⚖️ 参半')}
HIGH={'亚撒','约沙法','约阿施','亚玛谢','乌西雅','约坦'}
def verdict(n,v,lane):
    if lane=='U': return '—'
    if lane=='I':
        if n=='耶罗波安一世': return '“使以色列人陷在罪里”（王上14:16）——此后北国诸王评语的源头'
        if n=='亚哈': return '“行耶和华眼中看为恶的事，比他以前的列王更甚”（王上16:30）'
        if n=='沙龙': return '（只作王一个月，无评语）'
        return '“行耶和华眼中看为恶的事”，随从“耶罗波安……使以色列人陷在罪里的那罪”'
    if n=='亚她利雅': return '（篡位者，无评语公式）'
    if n=='希西家': return '“行耶和华眼中看为正的事，效法他祖大卫一切所行的”（王下18:3）'
    if n=='约西亚': return '“行耶和华眼中看为正的事……不偏左右”（王下22:2）'
    if v in ('good','mix'): return '“行耶和华眼中看为正的事”'+('，“只是邱坛还没有废去”' if n in HIGH else '')
    return '“行耶和华眼中看为恶的事”'
def lane(kings,key,y0=935,y1=580,px=4.2):
    rows=[];o=''
    for i,(n,alt,s,e,yrs,v,dy,pr,ref,rm) in enumerate(kings):
        e2=e if e<s else s-0.6
        r=0
        while r<len(rows) and rows[r]>e2+0.01 and rows[r]<s: r+=1
        # place row: first row whose last end >= s (BC decreasing => free if last_end>=s)
        r=next((j for j,last in enumerate(rows) if last>=s),len(rows))
        if r==len(rows): rows.append(e2)
        else: rows[r]=e2
        x=(y0-s)*px; w=max((s-e2)*px,6)
        col=VC[v][0]
        info=f'<b>{"🟥 以色列" if key=="I" else "🟦 犹大"} · {E(n)}{E(alt)}</b> {s}–{e} BC · 在位{yrs if yrs else "<1"}年 · {VC[v][1]}{(" · "+E(dy)) if dy else ""}<br>🗣️ {E(pr or "—")} · 📖 {E(ref)}<br>{E(rm)}'
        o+=f'<button class="dk" data-k="{key}{i}" data-s="{s}" data-e="{e2}" data-info="{E(info)}" style="left:{x:.0f}px;width:{w:.0f}px;top:{r*30}px;--c:{col}" title="{E(n)} {s}–{e} BC">{E(n)}</button>'
    return o,len(rows)
def build():
    c=[]
    c.append(hero(['👑 列王纪 × 历代志','先知的解释','祭司的盼望','42 位君王','双轨时间线'],'同一段历史，','两种眼光',
      '<b class="k">列王纪</b>站在被掳的废墟上问：<mark class="hy">“我们为什么失去了地和殿？”</mark>——因为违背了约。<b class="k">历代志</b>站在归回的工地上问：<mark class="hg">“神还要我们吗？”</mark>——要！大卫之约与圣殿仍在。'))
    c.append(legend_box())
    c.append(h2('why','🧭','整体：为什么要写两遍？'))
    c.append(h3('cmp','一表对照'))
    c.append(h4('cmp-t','📋 九项对照'))
    c.append(cmp2('📕 列王纪上下','📘 历代志上下',[
      ('成书','约 560–550 BC（被掳巴比伦期间；最后事件：约雅斤出狱 561 BC，王下25:27）','约 450–400 BC（归回后；家谱延至所罗巴伯之后数代，代上3:19–24）'),
      ('读者','被掳的以色列人','归回的余民'),
      ('视角','**先知性**：审判的神学解释——申命记的约（申28）应验','**祭司性**：盼望——圣殿、敬拜、利未人、大卫的约'),
      ('核心问题','“为什么会被掳？”','“我们与过去的应许还有关系吗？”'),
      ('范围','所罗门登基 → 南国灭亡（约 970–561 BC）','亚当 → 古列谕令（代上1:1 → 代下36:23）'),
      ('南北','南北交替叙述，北国 19 王都写','几乎只写犹大与大卫王朝；北国只在与犹大有关时出现'),
      ('结尾','约雅斤出狱——==大卫的灯未灭==（王下25:27–30）','古列谕令“你们中间凡作他子民的，可以上去”——++新的开始++（代下36:23）'),
      ('在希伯来正典','“前先知书”','“圣卷”的最后一卷——希伯来圣经以历代志结尾'),
      ('钥字','“使以色列人陷在罪里”“行耶和华眼中看为恶/正的事”','“寻求耶和华”“自卑”“全以色列”“利未人”')]))
    c.append(h4('cmp-k','💎 一句话'))
    c.append(co('core','<p>'+rich('**列王纪＝诊断书**（为什么生病），**历代志＝康复计划**（怎样重新敬拜）。两卷互补：==审判是真实的，应许也是真实的==——都指向那位更大的大卫之子（太1:1）。',False)+'</p>','核心'))
    c.append(h3('srcs','两卷书引用的史料'))
    c.append(table(['书卷','所引史料（举例）','经文'],[
      ['📕 列王纪','《所罗门记》','王上11:41'],['📕 列王纪','《以色列诸王记》（约17次）','王上14:19 等'],['📕 列王纪','《犹大列王记》（约15次）','王上14:29 等'],
      ['📘 历代志','先见撒母耳、先知拿单、先见迦得的书','代上29:29'],['📘 历代志','先知亚希雅的预言书、先见易多的默示书','代下9:29'],['📘 历代志','先知示玛雅与先见易多的史记','代下12:15'],
      ['📘 历代志','哈拿尼的儿子耶户的书','代下20:34'],['📘 历代志','先知以赛亚所写','代下26:22；32:32'],['📘 历代志','《以色列和犹大列王记》等','代下16:11；27:7']]))
    c.append(co('conf','<p>'+rich('引用史料不削弱默示：圣灵带领作者查考、拣选并写下无误的记录（路1:3同理）。比利时信条说这些书卷“{{BC5|用以规范、证实我们的信仰，作我们信仰的根基}}”。',False)+'</p>','认信'))
    c.append(h3('addomit','历代志的增与略'))
    c.append(table(['','历代志 ➕ 增加','历代志 ➖ 省略'],[
      ['大卫',rich('为建殿预备材料与人手（代上22–29）；利未人与歌唱班的编排（代上15–16；23–26）',False),rich('与拔示巴的罪、杀乌利亚（撒下11–12）；押沙龙叛乱',False)],
      ['所罗门','献殿祷告后火从天降（代下7:1）','晚年拜偶像、娶外邦妃嫔（王上11）'],
      ['北国','—','以利亚、以利沙的大部分事迹；北国诸王的独立叙述'],
      ['亚比雅','洗玛脸山的讲论与得胜（代下13）','—'],
      ['约沙法','派人教导律法（17:7–9）、设立审判官（19:4–11）、唱诗得胜（20）','—'],
      ['希西家','洁净圣殿、守逾越节（代下29–31）占三章','—'],
      ['玛拿西',rich('被掳巴比伦后**自卑悔改**、归回（代下33:11–17）',False),'—'],
      ['结尾','古列谕令（代下36:22–23）','约雅斤出狱（王下25:27–30）']]))
    c.append(co('trap','<p>'+rich('!!历代志不是“美化历史”!!：它不否认罪（如乌西雅、亚撒晚年），而是为归回的余民挑选能建立敬拜与盼望的材料。==选材不同≠记载矛盾==。',False)+'</p>','易错'))
    # ---------------- parallel table
    c.append(h2('par','📋','君王逐一对照：两卷书的经文'))
    def rows(kings,lane_):
        out=[]
        for n,alt,s,e,yrs,v,dy,pr,ref,rm in kings:
            k,ch=split_refs(ref)
            out.append([f'<b>{E(n)}</b><small>{E(alt)}</small>',f'<span class="ub">{s}–{e}</span>',str(yrs) if yrs else '<1',f'<span class="vb" style="--c:{VC[v][0]}">{VC[v][1]}</span>',E(k) or '—',E(ch) or '<span class="mut">（略）</span>',rich(verdict(n,v,lane_),False),E(pr or '—'),E(rm)])
        return out
    H=['王','年代 BC','年数','评语','列王纪／撒母耳记','历代志','评语公式','同期先知','要点']
    c.append(h3('par-u','统一王国（3 王）'))
    c.append(table(H,rows(UNITED,'U'),'kct'))
    c.append(h3('par-j','南国犹大（20 位）'))
    c.append(table(H,rows(JUDAH,'J'),'kct'))
    c.append(h3('par-i','北国以色列（19 王）'))
    c.append(table(H,rows(ISRAEL,'I'),'kct'))
    nI=sum(1 for x in ISRAEL if split_refs(x[8])[1]); 
    c.append(co('info','<p>'+rich(f'数一数：北国 19 王中，历代志另有独立经文段落的只有 **{nI}** 位（其余只在与犹大交往时顺带提到）。年代采用 Thiele 系保守年代，==含共治期==（例如约沙法 872 起与亚撒共治，乌西雅 792 起与亚玛谢共治），所以“在位年数”加起来会长于实际跨度。',False)+'</p>','观察'))
    # ---------------- dual lane
    c.append(h2('lane','🛤️','双轨时间线：悬停一位王，看同期的王'))
    li,ni=lane(ISRAEL,'I'); lj,nj=lane(JUDAH,'J'); W=(935-580)*4.2
    ticks=''.join(f'<span class="dt" style="left:{(935-y)*4.2:.0f}px">{y}</span>' for y in range(930,580,25))
    ev=[(931,'王国分裂'),(853,'夸夸尔之战'),(841,'耶户纳贡'),(722,'撒玛利亚陷落'),(701,'西拿基立围城'),(622,'发现律法书'),(612,'尼尼微陷落'),(605,'第一次被掳'),(597,'第二次被掳'),(586,'圣殿被毁')]
    evh=''.join(f'<span class="de" style="left:{(935-y)*4.2:.0f}px"><b>{y}</b> {t}</span>' for y,t in ev)
    emp=[(935,745,'埃及／亚兰为主要威胁','var(--sky)'),(745,612,'亚述（提革拉毗列色三世起）','var(--rose)'),(612,580,'新巴比伦','var(--gold)')]
    eh=''.join(f'<span class="dm" style="left:{(935-a)*4.2:.0f}px;width:{(a-b)*4.2:.0f}px;--c:{col}">{t}</span>' for a,b,t,col in emp)
    c.append(f'''<div class="dlane rv"><div class="dlinfo card">👆 悬停／点击任一位王：同期的王会一起亮起。</div><div class="dlsc"><div class="dlin" style="width:{W:.0f}px">
<div class="dlt">{ticks}</div><div class="dll"><span class="dln">🟥 以色列</span><div class="dlr" style="height:{ni*30}px">{li}</div></div>
<div class="dll"><span class="dln">🟦 犹大</span><div class="dlr" style="height:{nj*30}px">{lj}</div></div><div class="dlm">{eh}</div><div class="dlev">{evh}</div></div></div>
<p class="srcline">横轴：公元前年份（每格 25 年）。同一轨道上下错开的方块＝共治或对立统治。色：<span style="color:var(--emer)">善</span> · <span style="color:var(--rose)">恶</span> · <span style="color:var(--gold)">参半</span>。</p></div>''')
    # ---------------- memory
    c.append(h2('mem','🧠','记忆系统'))
    c.append(h3('rhyme','首字口诀'))
    def chunks(ks,sz): 
        names=[k[0] for k in ks]; out=[];i=0
        for z in sz: out.append(names[i:i+z]); i+=z
        return out
    jg=chunks(JUDAH,[4,4,4,4,4]); ig=chunks(ISRAEL,[4,4,4,4,3])
    def show(gs,col): return '<div class="rhy">'+''.join(f'<div style="--c:{col}"><b>{"".join(n[0] for n in g)}</b><span>{"、".join(g)}</span></div>' for g in gs)+'</div>'
    c.append(h4('rh-j','🟦 犹大 20 王'))
    c.append('<p><b>🟦 犹大 20 王（四字一组）：</b></p>'+show(jg,'var(--sky)'))
    c.append(co('mnc','<p class="mn">'+'｜'.join(''.join(n[0] for n in g) for g in jg)+'</p>','犹大口诀'))
    c.append(h4('rh-i','🟥 以色列 19 王'))
    c.append('<p><b>🟥 以色列 19 王（四字一组）：</b></p>'+show(ig,'var(--rose)'))
    c.append(co('mnc','<p class="mn">'+'｜'.join(''.join(n[0] for n in g) for g in ig)+'</p>','以色列口诀'))
    c.append(h3('good8','犹大 8 位善王'))
    good=[k for k in JUDAH if k[5] in ('good','mix')]
    c.append('<div class="g8 rv">'+''.join(f'<div style="--c:{VC[k[5]][0]}"><span class="kpb">{i+1}</span><b>{E(k[0])}</b><small>{k[2]}–{k[3]}</small><span>{E(k[9][:26])}</span></div>' for i,k in enumerate(good))+'</div>')
    c.append(co('mnc','<p class="mn">'+rich('**亚约约亚，乌约希约**（亚撒·约沙法·约阿施·亚玛谢｜乌西雅·约坦·希西家·约西亚）——只有 ==希西家、约西亚== 被说成“效法大卫”、除掉邱坛。',False)+'</p>','口诀'))
    c.append(h3('dyn','北国 9 个王朝链'))
    from collections import OrderedDict
    dd=OrderedDict()
    for k in ISRAEL:
        m=re.match(r'第(\d)朝',k[6]); dd.setdefault(int(m.group(1)),[]).append(k[0])
    c.append('<div class="dyn rv">'+''.join(f'<div style="--i:{i}"><span class="kpb">{d}</span><b>{E(v[0])}朝</b><small>{len(v)} 王：{"、".join(v)}</small></div>' for i,(d,v) in enumerate(dd.items()))+'</div>')
    killed=['拿答','以拉','心利','约兰','撒迦利雅','沙龙','比加辖','比加']
    c.append(co('core','<p>'+rich(f'北国 {len(ISRAEL)} 王、{len(dd)} 个王朝，其中 **{len(killed)} 位死于非命**（{"、".join(killed)}；心利为自焚）——==没有大卫之约的王位，只剩篡夺与流血==。南国除篡位的亚她利雅外，19 位君王都出自**大卫家**：神信守大卫之约（撒下7:16），弥赛亚要从这条线而来（太1:1–17）。',False)+'</p>','核心'))
    # ---------------- stats
    c.append(h2('kstats','📊','统计图表'))
    c.append(h3('reign','在位年数（圣经记载）'))
    allk=[('J',k) for k in JUDAH]
    c.append(h4('reign-j','🟦 犹大'))
    c.append(vbars([(k[0],k[4],VC[k[5]][0],f'犹大·{k[0]}：{k[4]}年（{k[2]}–{k[3]} BC）') for k in JUDAH],h=240,rot=True,cap='🟦 犹大 20 王在位年数（含共治；玛拿西 55 年最长）'))
    c.append(h4('reign-i','🟥 以色列'))
    c.append(vbars([(k[0],k[4],VC[k[5]][0],f'以色列·{k[0]}：{k[4]}年（{k[2]}–{k[3]} BC）') for k in ISRAEL],h=240,rot=True,cap='🟥 以色列 19 王在位年数（心利 7 日、撒迦利雅 6 个月、沙龙 1 个月记为 0）'))
    c.append(h4('reign-d','🍩 善恶分布与数字'))
    cnt=lambda ks,v: sum(1 for k in ks if k[5]==v)
    c.append('<div class="grid g2">'+donut([('善',cnt(JUDAH,'good'),'var(--emer)'),('参半',cnt(JUDAH,'mix'),'var(--gold)'),('恶',cnt(JUDAH,'evil'),'var(--rose)')],'🟦 犹大：善恶分布（本站评定）',190)
              +donut([('善',cnt(ISRAEL,'good'),'var(--emer)'),('恶',cnt(ISRAEL,'evil'),'var(--rose)')],'🟥 以色列：19 王全部“行恶”',190)+'</div>')
    span=lambda ks:(ks[0][2]-ks[-1][3])
    avg=lambda ks: sum(k[4] for k in ks)/len(ks)
    c.append(stats([(f'{span(JUDAH)} 年',f'犹大存续（931–586）','🟦','var(--sky)'),(f'{span(ISRAEL)} 年','以色列存续（931–722）','🟥','var(--rose)'),(f'{avg(JUDAH):.1f}','犹大平均在位年数','⏳','var(--sky)'),(f'{avg(ISRAEL):.1f}','以色列平均在位年数','⏳','var(--rose)'),(f'{len(dd)}','北国王朝数','🔗','var(--gold)'),('1','南国王朝（大卫家）','👑','var(--emer)')]))
    c.append(co('app','<p>'+rich('读列王纪时问：这位王对**神的约**怎样回应？读历代志时问：这位王怎样**寻求耶和华、自卑**？——两卷都把我们推向唯一完全的王：耶稣基督。',False)+'</p>','应用'))
    return page('kings-chronicles.html','列王纪 × 历代志',''.join(c),scripts='<script src="assets/js/v6.js?v='+V+'" defer></script>')
