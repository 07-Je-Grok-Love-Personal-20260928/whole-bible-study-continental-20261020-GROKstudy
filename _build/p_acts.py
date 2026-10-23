"""v8: 使徒行传与初代教会史 (AD 30–95+)：动画时间线、书信定位、四段旅程动画地图、徒1:8 结构、彼得×保罗平行、福音扩展、罗马统治者。"""
import json
from lib import *
from v6lib import hero,cmp2,donut
from genre import spans,flowsteps,kbox,mnem,rtable,grid,card
from v5extra import hbar
from p_geo import P as GP
from p_harmony import T as CUV
P=dict(GP); P.update({'约帕':(32.05,34.75),'坚革哩':(37.88,22.99),'拔摩':(37.32,26.55),'亚历山大':(31.2,29.92)})
J=[('第一次旅程 · AD 46–48 · 徒13–14','#3ee0a1',[('叙利亚安提阿','圣灵说：要为我分派巴拿巴和扫罗（13:2）'),('西流基','由此坐船'),('撒拉米','在犹太会堂传道'),('帕弗','方伯士求保罗信主；行法术的以吕马瞎眼'),('别加','约翰马可离开'),('彼西底安提阿','会堂长篇讲道；转向外邦人（13:46）'),('以哥念','信的人很多，也遭逼迫'),('路司得','医治瘸腿的；被当作神，又被石头打'),('特庇','使好些人作门徒'),('路司得','坚固门徒：“我们进入神的国，必须经历许多艰难”（14:22）'),('以哥念',''),('彼西底安提阿','在各教会选立长老'),('别加','讲道'),('亚大利','坐船'),('叙利亚安提阿','述说神怎样为外邦人开了信道的门（14:27）')]),
 ('第二次旅程 · AD 49–52 · 徒15:36–18:22','#5ec8ff',[('叙利亚安提阿','保罗与西拉同行'),('大数','经过基利家'),('特庇',''),('路司得','提摩太加入'),('以哥念',''),('彼西底安提阿','圣灵禁止在亚细亚讲道'),('特罗亚','马其顿的异象：“请你过到马其顿来帮助我们”'),('尼亚坡里','福音进入欧洲'),('腓立比','吕底亚、被鬼附的使女、禁卒全家信主'),('帖撒罗尼迦','三个安息日辩论；“搅乱天下的”'),('庇哩亚','天天考查圣经'),('雅典','亚略巴古讲道：“未识之神”'),('哥林多','住一年零六个月；迦流不受理（18:12）；写帖前后'),('坚革哩','许愿剪发'),('以弗所','短暂停留'),('该撒利亚','登岸'),('耶路撒冷','问教会安'),('叙利亚安提阿','回到差派教会')]),
 ('第三次旅程 · AD 52–57 · 徒18:23–21:16','#ffb34d',[('叙利亚安提阿','出发'),('大数',''),('特庇','坚固加拉太、弗吕家的门徒'),('彼西底安提阿',''),('以弗所','约三年；推喇奴学房；“主的道大大兴旺”（19:20）；写林前'),('特罗亚',''),('腓立比','经马其顿；写林后'),('帖撒罗尼迦',''),('哥林多','住三个月；写罗马书'),('腓立比','守除酵节后起行'),('特罗亚','犹推古坠楼复活'),('亚朔','步行'),('米推利尼',''),('米利都','向以弗所长老告别：“他用自己血所买来的”（20:28）'),('哥士',''),('罗底',''),('帕大喇','换船'),('推罗','门徒劝他不要上耶路撒冷'),('多利买',''),('该撒利亚','亚迦布预言捆绑'),('耶路撒冷','圣殿中被捕（21:27–36）')]),
 ('解往罗马 · AD 59–60 · 徒27–28','#ff6b6b',[('该撒利亚','向凯撒上诉后起解'),('西顿','百夫长宽待保罗'),('每拉','换亚历山大的船'),('佳澳','劝告不可开船'),('高大','遇“友拉革罗”大风'),('米利大','船破上岸；毒蛇；医好部百流的父亲'),('叙拉古','停三天'),('利基翁',''),('部丢利','遇见弟兄'),('罗马','软禁两年，“放胆传讲神国的道”（28:31）')])]
def mapcfg():
    pts={};
    for _,c,st in J:
        for n,d in st:
            if n not in pts: pts[n]={'n':n,'ll':list(P[n]),'d':d,'k':1 if n in ('耶路撒冷','叙利亚安提阿','以弗所','哥林多','罗马','腓立比','雅典') else 0}
            elif d and not pts[n]['d']: pts[n]['d']=d
    for n,d in [('约帕','彼得见异象（徒10）'),('撒玛利亚','腓利传道（徒8）'),('大马士革','扫罗归主（徒9）'),('亚历山大','亚波罗的家乡（徒18:24）'),('拔摩','约翰得启示（启1:9）')]:
        pts[n]={'n':n,'ll':list(P[n]),'d':d,'perm':False}
    return {'bounds':[[30.5,12],[42.5,37]],'color':'#8ea2ff','routes':[{'n':n,'path':[list(P[s]) for s,_ in st],'c':c,'w':2.5,'dash':'4 6','arrow':False} for n,c,st in J],'points':list(pts.values()),'legend':[[c,n.split(' · ')[0]] for n,c,_ in J]}
def cuv(ref):
    c,v=ref.split(':'); return CUV['ACT'][c][v]
def axis_events(ev,y0,y1,W=1000):
    """milestone strip: dots on an AD axis; labels placed greedily on alternating levels so none overlap; animated pop-in"""
    X=lambda y:40+(y-y0)/(y1-y0)*(W-80); LV=34; ends={}; place=[]
    order=[1,-1,2,-2,3,-3,4,-4,5,-5]
    for y,lb,ref,col in ev:
        w=max(len(lb)+3,len(ref))*12.2+8; x0=min(max(X(y)-w/2,4),W-4-w); x1=x0+w
        lv=next(l for l in order if ends.get(l,-1e9)<x0-6); ends[lv]=x1; place.append((y,lb,ref,col,lv,x0+w/2))
    up=max([l for *_,l,_x in place if l>0]+[1]); dn=-min([l for *_,l,_x in place if l<0]+[-1])
    A=up*LV+22; H=A+dn*LV+40; o=f'<line x1="20" x2="{W-20}" y1="{A}" y2="{A}" class="gl" style="stroke-width:2"/>'
    for t in range(y0+2,y1+1,5): o+=f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{A-5}" y2="{A+5}" class="gl"/><text x="{X(t):.1f}" y="{A+17}" text-anchor="middle" class="ax">AD {t}</text>'
    for i,(y,lb,ref,col,lv,cx) in enumerate(place):
        ly=A-lv*LV+(4 if lv>0 else 20)
        o+=f'<g class="evp" style="--d:{i*60}ms"><path d="M{X(y):.1f},{A} L{X(y):.1f},{A-lv*LV*0.55:.1f} L{cx:.1f},{ly+(6 if lv>0 else -14):.1f}" fill="none" stroke="{col}" stroke-opacity=".55"/><circle cx="{X(y):.1f}" cy="{A}" r="6" fill="{col}" stroke="#fff" stroke-width="1.5"><title>AD {y} · {E(lb)} · {E(ref)}</title></circle><text x="{cx:.1f}" y="{ly}" text-anchor="middle" class="evt" fill="currentColor"><tspan font-weight="800" fill="{col}">{y}</tspan> {E(lb)}</text><text x="{cx:.1f}" y="{ly+13}" text-anchor="middle" class="evr">{E(ref)}</text></g>'
    return f'<figure class="v6c rv evfig"><div class="v6sc"><svg viewBox="0 0 {W} {H}" style="min-width:860px;color:var(--ink)" role="img" aria-label="初代教会大事年表">{o}</svg></div><figcaption class="srcline">年份为保守派学者常用的约数（±1–2 年）；悬停圆点看出处；折线把标签连到它的年份。</figcaption></figure>'
EV=[(30,'五旬节·圣灵降临','徒2','var(--gold)'),(32,'彼得约翰被捕','徒4','var(--sky)'),(34,'司提反殉道','徒7','var(--red)'),(35,'扫罗归主','徒9','var(--vio)'),(37,'保罗首访耶路撒冷','加1:18','var(--vio)'),(39,'哥尼流家·外邦人受圣灵','徒10','var(--emer)'),(43,'安提阿“基督徒”','徒11:26','var(--teal)'),(44,'雅各殉道·希律死','徒12','var(--red)'),(46,'饥荒赈济','徒11:28','var(--teal)'),(49,'耶路撒冷会议','徒15','var(--gold)'),(51,'迦流任方伯（定年锚点）','徒18:12','var(--sky)'),(57,'耶路撒冷被捕','徒21','var(--red)'),(59,'向凯撒上诉','徒25:11','var(--amb)'),(60,'抵达罗马','徒28','var(--rose)'),(62,'主的兄弟雅各殉道','约瑟夫','var(--red)'),(64,'罗马大火·尼禄逼迫','塔西佗','var(--red)'),(67,'彼得、保罗殉道（传统）','教父传统','var(--red)'),(70,'圣殿被毁','太24:2','var(--rose)'),(81,'多米田即位','史料','var(--amb)'),(95,'约翰在拔摩岛','启1:9','var(--vio)')]
def clamp(rows,y0,y1): return [(a,max(b,y0),min(c,y1),d,e) for a,b,c,d,e in rows]
BANDS=[('耶路撒冷 1–7',30,34,'var(--gold)'),('犹太·撒玛利亚 8–12',34,46,'var(--emer)'),('地极 13–28',46,62,'var(--sky)'),('使徒时代末期',62,100,'var(--vio)')]
def build():
    open(SITE+'assets/data/maps8.js','w').write('window.MAPS=Object.assign(window.MAPS||{},'+json.dumps({'acts':mapcfg()},ensure_ascii=False,separators=(',',':'))+');window.ACTSJ='+json.dumps([{'n':n,'c':c,'s':[[s,list(P[s]),d] for s,d in st]} for n,c,st in J],ensure_ascii=False,separators=(',',':'))+';')
    c=[hero(['🕊️ 使徒行传与初代教会','AD 30–95+','动画时间线 · 旅程动画地图','书信定位'],'从耶路撒冷到罗马：','升天的基督藉圣灵建立教会',rich('路加写的是“耶稣**开头**一切所行所教训的”（徒1:1）的续篇：==同一位基督，如今从天上藉圣灵继续工作==。主题经文：“但圣灵降临在你们身上，你们就必得着能力，并要在耶路撒冷、犹太全地，和撒马利亚，直到地极，作我的见证。”（徒1:8）',False))]
    c.append(h2('a18','🎯','徒1:8 结构：三个同心圆'))
    seg=[('耶路撒冷','1–7',7,'var(--gold)'),('犹太与撒玛利亚','8–12',5,'var(--emer)'),('直到地极','13–28',16,'var(--sky)')]
    c.append('<div class="obar rv" style="display:flex;height:40px;border-radius:10px;overflow:hidden;margin:8px 0">'+''.join(f'<span style="flex:{n} 1 0;background:color-mix(in srgb,{col} 55%,transparent);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;min-width:0;overflow:hidden;white-space:nowrap">{t} {r}</span>' for t,r,n,col in seg)+'</div>')
    seg2=[('彼得为主 · 向犹太人','1–12',12,'var(--rose)'),('保罗为主 · 向外邦人','13–28',16,'var(--paul)')]
    c.append('<div class="obar rv" style="display:flex;height:30px;border-radius:10px;overflow:hidden;margin:4px 0 10px">'+''.join(f'<span style="flex:{n} 1 0;background:color-mix(in srgb,{col} 45%,transparent);display:flex;align-items:center;justify-content:center;font-size:12.5px;min-width:0;overflow:hidden;white-space:nowrap">{t} {r}</span>' for t,r,n,col in seg2)+'</div>')
    c.append(h3('a-prog','📈 六次“进展报告”（和合本原文）：路加给的结构钥匙'))
    PR=[('6:7','耶路撒冷'),('9:31','犹太、加利利、撒玛利亚'),('12:24','希律死后'),('16:5','小亚细亚'),('19:20','以弗所'),('28:31','罗马')]
    c.append('<div class="grid g3">'+''.join(f'<div class="card gcard rv" style="--c:var(--emer)"><h4>徒{r} · {t}</h4><p class="ht" style="font-size:15px">“{E(cuv(r))}”</p></div>' for r,t in PR)+'</div><p class="srcline">经文：新标点和合本（eBible.org cmn-cu89s），逐字取自数据文件。</p>')
    c.append(kbox('使徒行传的五个要点',['**主角是升天的基督**：徒1:1“开头”——福音书是开头，使徒行传是续篇。','**圣灵是能力**：五旬节（2）、撒玛利亚（8）、外邦人（10）、以弗所（19）——每道“门”打开都有圣灵的印证。','**福音冲破边界**：犹太人 → 撒玛利亚人 → 外邦人；==神的应许是给万民的==（创12:3）。','**逼迫推动扩展**：司提反殉道后“那些分散的人往各处去传道”（8:4）。','**教会的样式**：使徒的教训、团契、擘饼、祈祷（2:42）；长老治理（14:23；20:28）。']))
    c.append(h2('a-tl','⏳','动画时间线 · AD 30–95+'))
    c.append(h3('a-ev','📍 大事年表'))
    c.append(axis_events(EV,28,98))
    c.append(h3('a-rule','👑 罗马统治者 × 保罗生平'))
    rows=[('👑 提庇留',14,37,'var(--amb)','提庇留 14–37（路3:1）'),('👑 该犹（卡利古拉）',37,41,'var(--amb)','37–41'),('👑 革老丢',41,54,'var(--amb)','41–54：饥荒（11:28）、逐犹太人（18:2）'),('👑 尼禄',54,68,'var(--red)','54–68：保罗上诉的“凯撒”；64年逼迫'),('👑 维斯帕先·提多',69,81,'var(--amb)','69–81：攻陷耶路撒冷（70）'),('👑 多米田',81,96,'var(--red)','81–96：启示录时代'),
      ('🏛️ 希律亚基帕一世',41,44,'var(--rose)','41–44：杀雅各、囚彼得（徒12）'),('🏛️ 腓力斯（巡抚）',52,59,'var(--rose)','52–59：徒23–24'),('🏛️ 非斯都（巡抚）',59,62,'var(--rose)','59–62：徒25–26'),('🏛️ 亚基帕二世',50,93,'var(--rose)','约50–93：“你想少微一劝，便叫我作基督徒”（26:28）'),
      ('🧭 归主后：亚拉伯·大马士革',35,37,'var(--vio)','加1:17–18'),('🧭 大数·基利家',37,43,'var(--vio)','徒9:30；加1:21'),('🧭 安提阿事奉',43,46,'var(--vio)','徒11:25–26'),('🧭 第一次旅程',46,48,'#3ee0a1','徒13–14'),('🧭 第二次旅程',49,52,'#5ec8ff','徒15:36–18:22'),('🧭 第三次旅程',52,57,'#ffb34d','徒18:23–21:16'),('🧭 该撒利亚被囚',57,59,'var(--red)','徒23–26'),('🧭 解往罗马',59,60,'#ff6b6b','徒27–28'),('🧭 罗马软禁',60,62,'var(--rose)','徒28:30'),('🧭 获释再旅行·再被囚',62,67,'var(--mut)','据教牧书信推断')]
    c.append(spans(clamp(rows,28,98),28,98,list(range(30,100,5)),'底色＝徒1:8 的三阶段（约数）。罗马皇帝与犹太地统治者为史学通行年代；保罗年表采保守派常用框架（加拉太书“南加拉太说”）。',bands=BANDS,rowh=26,lw=200))
    c.append(h3('a-ep','✉️ 新约书卷写作定位（同一时间轴）'))
    ep=[('雅各书',45,49,'var(--gen)','约45–49：可能最早的书信'),('加拉太书',48,49,'var(--paul)','约48–49：会议前后'),('帖撒罗尼迦前后书',50,51,'var(--paul)','约50–51：哥林多'),('哥林多前书',54,55,'var(--paul)','约55：以弗所'),('哥林多后书',55,56,'var(--paul)','约56：马其顿'),('罗马书',56,57,'var(--paul)','约57：哥林多'),('马可福音',55,65,'var(--gosp)','约55–65'),('马太福音',55,65,'var(--gosp)','约55–65'),('路加福音·使徒行传',60,62,'var(--acts)','约60–62：行传止于软禁'),('狱中书信（弗腓西门）',60,62,'var(--paul)','约60–62：罗马'),('彼得前书',62,64,'var(--gen)','约62–64：“巴比伦”＝罗马'),('提摩太前书·提多书',62,64,'var(--paul)','约62–64'),('希伯来书',64,69,'var(--gen)','圣殿被毁前'),('提摩太后书',66,67,'var(--paul)','约66–67：殉道前'),('彼得后书',65,67,'var(--gen)','约65–67'),('犹大书',65,80,'var(--gen)','约65–80（有争议）'),('约翰福音',85,95,'var(--gosp)','约85–95：以弗所'),('约翰一二三书',85,95,'var(--gen)','约85–95'),('启示录',95,96,'var(--rev)','约95：多米田晚期')]
    c.append(spans(ep,28,98,list(range(30,100,5)),'约略的保守派年代；彼后、犹大、希伯来书与马太、马可的年代学界争议较大。书信页（epistles.html）有更详细的书信年代与主题对照。',bands=BANDS,rowh=24,lw=200))
    c.append(h2('a-map','🗺️','旅程动画地图：三次宣教旅程 + 解往罗马'))
    c.append('<div class="jyb" role="group" aria-label="选择旅程"><b>▶ 播放：</b>'+''.join(f'<button class="btn" data-jy="{i}" style="--c:{col}"><i style="background:{col}"></i>{n.split(" · ")[0]}</button>' for i,(n,col,_) in enumerate(J))+'<span id="actscap" class="jycap" aria-live="polite">点按钮，路线会一站一站画出来；地图上的虚线为全部路线。</span></div>')
    c.append('<div class="map rv" data-map="acts" role="region" aria-label="保罗旅程动画地图" style="height:clamp(380px,62vh,620px)"><div class="lazyph" style="height:100%">🗺️ 地图将在滚动到此处时加载…</div></div>')
    c.append('<div class="grid g4">'+''.join(f'<div class="card gcard rv" style="--c:{col}"><h4>{E(n)}</h4><ol class="jyl">'+''.join(f'<li><b>{E(s)}</b>{"：" + E(d) if d else ""}</li>' for s,d in st if d)+'</ol></div>' for n,col,st in J)+'</div>')
    c.append(h2('a-pp','⚖️','彼得 × 保罗：路加刻意的平行'))
    c.append(cmp2('彼得（1–12）','保罗（13–28）',[('医治生来瘸腿的','徒3:1–10','徒14:8–10'),('对付行邪术的','行邪术的西门（8:18–24）','以吕马（13:6–12）'),('医病的“媒介”','影儿（5:15）','手巾围裙（19:12）'),('叫死人复活','多加（9:36–41）','犹推古（20:9–12）'),('奇妙出监','天使开门（12:6–11）','地大震动（16:25–26）'),('拒绝被拜','哥尼流俯伏（10:25–26）','路司得人献祭（14:13–15）'),('按手受圣灵','撒玛利亚（8:17）','以弗所（19:6）'),('首篇讲道主题','“神已经立他为主，为基督了”（2:36）','“赦罪的道是由这人传给你们的”（13:38）')],'var(--rose)','var(--paul)'))
    c.append('<div class="grid g2">'+co('core','<p>'+rich('平行不是为了抬高人，而是表明：==向外邦人的使徒与向犹太人的使徒传的是同一福音==（加2:7–9），同一位主在两人身上作工。',False)+'</p>','为什么平行')+co('trap','<p>'+rich('!!使徒行传是“描述”多于“规定”!!：神迹、按手、方言在使徒行传里标记的是**救恩历史的一次性转折**（耶路撒冷→撒玛利亚→外邦），不是每个信徒都必须复制的步骤。',False)+'</p>','易错')+'</div>')
    c.append(h2('a-spread','🌍','福音的扩展'))
    c.append(flowsteps([('🔥','耶路撒冷 AD 30','五旬节三千人（2:41）','var(--gold)'),('🫂','撒玛利亚 ~34','腓利；彼得约翰按手（8）','var(--emer)'),('🐪','埃提阿伯太监','福音向南到非洲（8:26–39）','var(--teal)'),('🏛️','该撒利亚 ~39','哥尼流：外邦人受圣灵（10）','var(--sky)'),('⛪','安提阿 ~43','第一个外邦为主的教会；差派中心（11、13）','var(--vio)'),('⛵','加拉太 46–48','第一次旅程','#3ee0a1'),('🏺','马其顿·亚该亚 49–52','福音进入欧洲','#5ec8ff'),('📜','以弗所 52–55','“一切住在亚细亚的……都听见主的道”（19:10）','#ffb34d'),('🏛️','罗马 60–62','“放胆传讲……并没有人禁止”（28:31）','var(--rose)')]))
    c.append(hbar([('耶路撒冷 1–7',7,'var(--gold)'),('犹太·撒玛利亚 8–12',5,'var(--emer)'),('小亚细亚 13–16',4,'#3ee0a1'),('马其顿·亚该亚 16–18',3,'#5ec8ff'),('以弗所 19–20',2,'#ffb34d'),('耶路撒冷·该撒利亚 21–26',6,'var(--red)'),('往罗马 27–28',2,'var(--rose)')],' 章','路加用多少篇幅写每个区域（约数）：受审与上诉（21–26）占了六章——福音在君王与巡抚面前作见证（9:15）。'))
    c.append(h2('a-sp','🎙️','七篇关键讲道'))
    c.append(rtable(['讲员 · 经文','场合','核心'],[['彼得 · 2:14–40','五旬节','诗16、110：**神已经立他为主，为基督了**'],['司提反 · 7:2–53','公会','从亚伯拉罕到圣殿：==神不住人手所造的=='],['彼得 · 10:34–43','哥尼流家','**神不偏待人**；信他的人必蒙赦罪'],['保罗 · 13:16–41','彼西底安提阿','从以色列史到复活：**因信称义**（13:39）'],['雅各 · 15:13–21','耶路撒冷会议','摩9:11–12：外邦人归主应验先知'],['保罗 · 17:22–31','亚略巴古','创造主 · 审判主 · 复活为凭据'],['保罗 · 20:18–35','米利都','牧者遗言：**他用自己血所买来的**教会']]))
    c.append(h2('a-conf','📚','认信连接：圣灵与教会'))
    c.append(co('conf','<p>'+rich('使徒行传是海德堡第54问的历史画面：神的儿子藉着圣灵和圣言{{HC54|为他自己召聚、护卫、保守，并存留他的子民}}。比利时信条第29条列出真教会的标志：{{BC29|她宣讲纯正的福音；她按照基督当初设立圣礼的样式施行圣礼；她为纠正错误、刑罚罪恶而执行教会纪律}}。下面为原文（逐字引自 ccifellowship.org）。',False)+'</p>','认信')+confref('HC54,BC27,BC29'))
    c.append(mnem([('徒1:8','耶 → 犹撒 → 地极','1–7 / 8–12 / 13–28'),('保罗年表','35 归主 · 46 一 · 49 会 · 49 二 · 52 三 · 57 捕 · 60 罗','“三五四六，四九五二，五七六零”'),('六报告','6:7 · 9:31 · 12:24 · 16:5 · 19:20 · 28:31','每段结尾都有“道兴旺”')]))
    c.append(co('app','<p>'+rich('今天的教会仍活在“徒1:8”与“徒28:31”之间：**同一位圣灵**，**同一个福音**，向着==直到地极==。问自己：我在哪个“同心圆”里作见证？',False)+'</p>','应用'))
    return page('acts.html','使徒行传与初代教会',''.join(c),extra_head='<link rel="stylesheet" href="assets/vendor/leaflet.css">',
      scripts='<script src="assets/vendor/leaflet.js" defer></script><script src="assets/data/land.js" defer></script><script src="assets/data/maps8.js" defer></script><script src="assets/js/maps.js?v=v8" defer></script><script src="assets/js/acts.js?v=v8" defer></script>')
