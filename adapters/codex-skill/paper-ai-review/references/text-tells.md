# 文字层 AI 痕迹清单（中英双语）

判断"这段文字像不像 AI 写的"。**先读 SKILL.md 的两条铁律**：看聚集不看单点、不误伤。
这份清单里几乎每一条单独出现都不算数——你要找的是**多条在同一段密集扎堆**。

通用原则与词表提炼自
[renwei-writing](https://github.com/orange2ai/renwei-writing)（橘子 & Cola，文字人味儿原则）/
Wikipedia [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) /
[blader/humanizer](https://github.com/blader/humanizer)，并针对学术论文补了双语与学术专属项。

---

## 〇、最常见的两个落点（先看这两个）

这两类是论文里 AI 味最常见、也最该改的：

1. **内容空洞**：语法完美、辞藻漂亮，但通篇没有可验证的信息——没有具体方法、没有数据、
   没有能被反驳的判断。"impeccably phrased text that doesn't contain any insight"。
   - 改法：把空泛句换成一个有出处的具体说法。"本方法显著提升了性能"→给出在哪个数据集、
     相对谁、提升了多少。
2. **为排比而排比**：把观点硬凑成三个一组、连续排比、同义词轮换（同一个东西换着叫，
     因为 AI 怕重复）。一个排比是修辞，连排是模式。
   - 改法：拆成长短不一的句子，只保留真有内容的那条。

---

## 一、中文论文：套话信号

- **格式痕迹**：破折号 `——`（学术正文里几乎不该出现，最可靠的中文 AI 信号之一）。
- **句式套路**：
  - "**不是 X，而是 Y**"及变体（"与其说…不如说…""重要的不是…而是…"）——最高频的假深刻。
  - 排比三连、同义词轮换。
- **意义拔高**：标志着 / 体现了 / 折射出 / 彰显了 / 具有重要意义 / 为…提供了新思路（句尾拔高补尾）。
- **宣传腔**：赋能 / 打造 / 璀璨 / 全方位 / 深层次 / 致力于 / 匠心。
- **填充对冲**（删了句子照样成立）：值得注意的是 / 需要指出的是 / 换言之 / 总的来说 / 综上所述（滥用时）。
- **万能展望结尾**：用"未来可期 / 仍有广阔的研究空间 / 进一步的研究方向"等空泛话收尾，
  落不到一个具体的事实上。
- **签到式过渡 / 机械罗列**："首先…其次…再次…最后…"硬套、"接下来我们深入探讨"。
- **句式套层**："旨在…通过…从而…"层层嵌套；三件套形容词堆叠（"高效、稳定、可扩展"却无实证）。

### 中文「不误伤」白名单（看到不要判、不要删）
- **学术规范套话**：本文提出 / 实验结果表明 / 如表 1 所示 / 综上所述 / 本节介绍 / 受…启发——
  这些是论文惯例，**不是 AI 痕迹**。只有当空泛措辞**取代了**本该有的具体方法/数据/结论时才算问题。
- 一个破折号、一处排比、一个"然而"——单独出现，放行。
- 文风干巴、用词朴素——这往往恰恰是真人，不是 AI。

---

## 二、英文论文：GPT-isms

LLM 高频、人类学术写作前 LLM 时代相对少见的词与句式（Ars Technica / Pangram 实证）：

- **高频词**：delve / delves into、showcasing / showcase、intricate、a testament to、
  plays a pivotal / crucial role、rich tapestry、navigating the (landscape / complexities)、
  underscore(s)、it is worth noting that、leverage、realm、seamless(ly)、comprehensive、
  meticulous、garner、stands as、in the ever-evolving。
- **句式**：句首 `Moreover, / Furthermore, / Additionally, / In conclusion,` 层层串联；
  `not only … but also` 滥用；`From X to Y`（X、Y 不在一条真实的轴上）；一律正面、几乎不批判；
  每段都"总—分—升华"同一节奏。
- **格式**：英文破折号 `—`（em dash）密集；机械加粗"**Keyword**: 后接解释"式列表。
- **句法**：句长趋向均匀的中等偏长（真人忽长忽短）。

### 英文「不误伤」白名单
- underscore / comprehensive / leverage / pivotal / novel 等词在正经学术英文里**本就常用**，
  **单个出现绝不能判**。要看是否"**高密度扎堆 + 配套句式**（总分排比、一律正面、moreover/
  furthermore 串联、句长趋同）"才算聚集。
- **母语非英文作者**论文用词偏正式、句式略生硬，属正常，勿误伤为 AI。

---

## 三、学术专属：tortured phrases（扭曲术语）

标准术语被改写工具替换成的怪词，例如：
- signal-to-noise → "flag to clamor"
- convolutional neural network → "convolutional brain organization"
- artificial intelligence → "counterfeit consciousness"
- big data → "enormous information"

来源：洗稿 / 机器翻译规避查重工具（Problematic Paper Screener 收录 7000+ 条）。

### 重要区分（别张冠李戴）
tortured phrases **不是现代 LLM（ChatGPT/Claude）的典型产物**——LLM 通常输出标准术语。
命中扭曲术语时，结论应偏向"**疑似洗稿 / 机翻规避查重**"，而非"ChatGPT 代写"。两者改法不同：
前者要换回标准术语并核查原创性，后者要补具体内容、去套话。别混为一谈。

---

## 人写的迹象（看到就保住，这是和"不误伤"的交汇点）
- 具体到难以编造的细节（一个真实数据、一个反直觉的反例、一句具体的实验设置）。
- 没有解决的矛盾 / 诚实的局限（"在 X 上有效，但在 Y 上反而下降，原因尚不清楚"）。
- 长短不一的呼吸、自我打断、带领域圈子印记的用词。
- 作者能说出理由的用词选择。
