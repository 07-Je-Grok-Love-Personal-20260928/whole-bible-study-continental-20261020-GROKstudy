# 整本圣经研读-20261020-v1-GROKstudy

> **主题**：整本《圣经》解读（欧陆改革宗 · 正统神学）｜**时间**：2026-10-20｜**版本号**：v1｜GROKstudy

时间线 · 故事线 · 地理位置 · 真实背景 · 文化区域 · 诸王与时代 · 圣经神学 · 圣约神学 · 66 卷逐卷解读 · 三大普世信经干净背诵版与深度对比 · 三项联合信条全文 · 记忆测验。
信经与信条引文全部**逐字**取自 [ccifellowship.org](https://ccifellowship.org)（中国改革宗教会），经文采用和合本。

## 🔗 在线访问（3 个部署 + 1 个仓库）

| 平台 | 链接 |
|---|---|
| GitHub Pages | https://07-je-grok-love-personal-20260928.github.io/whole-bible-study-continental-20261020-GROKstudy/ |
| Surge | https://whole-bible-study-20261020-v1-grokser.surge.sh/ |
| Netlify | https://whole-bible-study-20261020-v1-grokser.netlify.app/ |
| 源码仓库 | https://github.com/07-Je-Grok-Love-Personal-20260928/whole-bible-study-continental-20261020-GROKstudy |

## 📑 页面结构（11 页）

| 文件 | 内容 |
|---|---|
| `index.html` | 首页：学习路线、66 卷颜色地图、整本圣经一页纸、海德堡第 1 问 |
| `story.html` | 救赎大故事：四幕剧、十二场景、女人后裔红线、七条圣经神学主题、基督中心解经、改革宗读经原则、整本圣经思维导图 |
| `covenant.html` | 圣约神学：救赎之约/行为之约/恩典之约、六个历史之约、两种施行、记号、律法三用、vs 时代论 |
| `timeline.html` | 11 时代、8 钉子年份、主时间线（约 60 个事件）、统一王国 3 王、以色列 19 王、犹大 20 位君王（全表）、南北诸王年代图（SVG）、先知对照、六大帝国、被掳与归回、两约之间、新约年代、信经历史 |
| `geography.html` | 8 幅交互地图（Leaflet + 离线 Natural Earth 海岸线，可切换在线底图）：古代近东文化区、族长、出埃及、十二支派、分裂王国、帝国与被掳归回、耶稣事工、保罗旅程；文化区域与地形对照 |
| `ot.html` / `nt.html` | 66 卷逐卷：作者、日期、真实背景、为什么写、结构大纲、核心信息、基督中心、圣约位置、关键经文、难点辨析、应用、记忆口诀、认信连接（三项联合信条原文） |
| `creeds.html` | 三大普世信经干净阅读/背诵版（遮盖背诵模式）、深度对比、异端对照、为什么三份而不是一份、与三项联合信条的关系 |
| `forms.html` | 比利时信条 37 条、海德堡要理问答 52 主日 129 问、多特信经（4 部分/5 项教义）全文 |
| `memory.html` | 66 卷口诀总表、24 张闪卡、24 道选择题、8 个排序游戏、信经填空、两周记忆计划 |
| `sources.html` | 逐字引用来源、在线核对报告、与 2015《敬拜手册》PDF 交叉比对、参考网站 |

## 🛠️ 开发

```bash
python3 _build/build.py      # 由 _build/*.py 与 _build/books_*.txt 生成全部 HTML
python3 _build/check.py all  # 无头 Chromium 在 390/820/1440 宽度检查溢出、控制台错误、Mermaid、地图、66 卷
```

- 纯静态站点，无需构建工具；第三方库已本地化：`assets/vendor/`（Leaflet 1.9.4、Mermaid 11）。
- 书卷内容数据：`_build/books_ot1.txt`、`_build/books_ot2.txt`、`_build/books_nt.txt`（`@@` 分块格式）。
- 信条数据：`_build/data/cci/*.json`（自 ccifellowship.org 抓取并核对）。正文中的短引用以 `{{HC27|…}}` 标记，构建时自动校验必须是原文子串，否则构建失败。

## 📝 版本说明

### v1 — 2026-10-20（首个版本）
- 全新多页面架构（11 页），毛玻璃 + 极光背景、明/暗主题、可隐藏目录（桌面折叠/手机抽屉）、阅读进度条、滚动高亮、渐显动画。
- 66 卷全部完成，每卷 13 个维度；42 位君王全表（3+19+20）与 SVG 年代图；8 幅离线可用交互地图；10+ Mermaid 流程图/思维导图。
- 三大信经 + 三项联合信条全文逐字引自 ccifellowship.org，并于 2026-10-20 与在线页面重新比对（信经段落 100% 一致；16 个信条页面抽查 100% 一致）。
- 部署：GitHub Pages、Surge（`whole-bible-study-20261020-v1-grokser`）、Netlify（`whole-bible-study-20261020-v1-grokser`）。

### 后续版本命名约定
`whole-bible-study-<YYYYMMDD>-v<N>-grokser`（Surge / Netlify 域名），README 标题 `整本圣经研读-<日期>-v<N>-GROKstudy`。

---
年代采用保守派（Thiele 式）年代学；书卷解读与图表为本站依改革宗正统立场所作综述，凡逐字引文均标注出处并链接原页。
