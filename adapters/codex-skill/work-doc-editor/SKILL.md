---
name: work-doc-editor
description: Use when preparing, revising, or finalizing Markdown workplace documents such as leadership updates, technical summaries, feature design proposals, development plans, project reports, handoff notes, work syncs, retrospectives, diagnosis reports, evaluation reports, review reports, coaching analysis, or experience-sharing docs. Especially use after AI has drafted content and the final output should be concise, readable, human-sounding, easy for leaders or teammates to skim, and visibly grounded in the author's judgment, evidence, root-cause thinking, tradeoffs, risks, and next actions.
---

# Work Doc Editor

Rewrite AI-generated or rough Markdown into a final workplace document that reads like a real employee prepared it for leaders, teammates, or future handoff.

This is a **forced rewrite skill**, not a review-only skill. When it triggers, produce the improved final document directly unless the user explicitly asks only for critique.

## Core Goal

The document should help readers make sense of the work quickly:

- A busy leader can understand the conclusion in about 1 minute.
- A teammate can find the relevant details without reading everything.
- The author can understand the topic better after reading the final version.
- The document shows judgment, tradeoffs, uncertainty, and next steps instead of only AI-style information expansion.
- The reader can tell what is confirmed, what is inferred, and what still needs human follow-up.
- The main body stays light; detailed lists and deep reference material are moved to appendices or follow-up docs.

Use this principle:

> AI can help expand information, but the final document must preserve the author's judgment and responsibility boundaries.

Also use this document-shaping rule:

> The main body explains judgment and direction. Appendices carry detailed lists, raw references, and optional deep dives.

## Reader Pressure Test

Before rewriting, infer the primary reader and the action they need to take.

For a leader, optimize for:

- **Decision**: what needs approval, rejection, prioritization, or awareness.
- **Confidence**: what has been verified and what is still uncertain.
- **Risk**: what could affect schedule, quality, cost, user impact, or cross-team coordination.
- **Accountability**: what the author recommends and what they will do next.

For a teammate, optimize for:

- **Context**: what changed and why it matters.
- **Handoff**: what they need to know to continue work.
- **Details**: where the important implementation, requirement, or process information lives.
- **Open questions**: what should not be assumed yet.

If the draft does not make the reader's expected action clear, add explicit action markers near the top instead of a vague "please pay attention" section.

## Editing Workflow

### 1. Identify Document Intent, Type, and Reader

First classify what job the document is doing. The same Markdown format should be edited differently depending on intent:

- **Inform**: help readers understand status, background, or project shape. Optimize for conclusion, context, and reading path.
- **Decide**: help someone approve, reject, prioritize, or choose. Optimize for options, tradeoffs, recommendation, and decision needed.
- **Diagnose**: explain what is wrong, why it happened, and how to improve. Optimize for evidence, root cause, severity, and corrective action.
- **Review/evaluate**: judge whether another report, plan, diagnosis, or output is reasonable. Optimize for criteria, evidence comparison, disagreements, and revision suggestions.
- **Compare systems/results**: explain why two systems, reports, scores, models, or evaluations disagree. Optimize for scope, numeric summary, discrepancy pattern, scoring-rule difference, root cause, decision impact, and fix path.
- **Handoff**: help someone continue work. Optimize for current state, ownership, dependencies, open issues, and next steps.
- **Teach/share**: help the author or team reuse an experience. Optimize for scenario, mistake, lesson, and checklist.
- **Explain/transfer**: help readers understand a system, mechanism, migration, or design change. Optimize for mental model, what changed, why it matters, key boundaries, and where to look next.

After choosing the intent, pick the closest document type and optimize for that reader need.

Common types:

- **Leadership update**: conclusion, current status, risk, decision needed, next action.
- **Technical summary**: module responsibilities, key paths, important constraints, gotchas, verification status.
- **Feature/design proposal**: recommendation, alternatives considered, tradeoffs, scope boundaries, risks, open questions.
- **Development plan**: target outcome, task breakdown, dependencies, risks, validation, rollout or handoff notes.
- **Handoff/work sync**: what changed, what remains, owner/context, next steps, unresolved points.
- **Diagnosis/report review**: findings, evidence, root cause, whether the original diagnosis is reasonable, what is missing, and what should change.
- **Scoring discrepancy analysis**: sample scope, score gap, gap patterns, rule mismatch, scenario mismatch, examples, priority fixes, and what not to conclude.
- **Experience sharing/retrospective**: situation, mistake or insight, what worked, reusable lesson, next-time checklist.
- **Technical mechanism explanation**: core model, old-vs-new comparison, lifecycle, change impact, stable mental model, and optional deep-dive details.

If the type is mixed, choose the dominant reader goal and keep secondary content in later sections.

### 2. Mark Evidence and Confidence

A strong work document should not make every sentence sound equally certain. When useful, label content with lightweight markers:

- **已确认**: supported by source material, code reading, explicit requirement, meeting note, test result, or other concrete input.
- **我的判断**: reasoned conclusion based on available information.
- **待确认**: missing fact, dependency, stakeholder decision, or unverified assumption.
- **建议**: action the author recommends.
- **需你补充**: a place where the human author needs to add real thinking, firsthand context, examples, or judgment.

Do not over-label every bullet. Use these labels where confusion or overconfidence would create risk.

If a conclusion is based only on the AI draft, avoid presenting it as verified. Write:

```md
基于当前材料，我暂时判断为 xxx；但还需要确认 xxx，避免后续理解偏差。
```

For places that require the user's own confirmation, edits, or personal thinking, mark them directly. Prefer clear inline markers over vague section names:

```md
- 【待你确认】这里是否要按“接手开发”作为后续目标？
- 【需你补充】这里需要补一条你自己的判断或真实案例。
- 【待验证】本地流程尚未跑通，不能直接判断生产可用性。
```

If the output platform supports HTML in Markdown, underline critical human-action markers:

```md
- <u>【待你确认】是否接受先跑通 demo，再评估生产可用性？</u>
```

### 3. Restructure for Skimming

Put the most useful content first. Prefer this shape unless the user provides a required format:

```md
# Clear Specific Title

## 先看结论
- 当前状态：
- 【待你确认】：
- 我的判断：
- 建议动作：
- 主要风险：

## 阅读路径
- 只看结论：看「[先看结论](#先看结论)」
- 评审方案：看「[关键链路](#关键链路)」和「[我的分析](#我的分析)」
- 跟进执行：看「[下一步](#下一步)」
- 查详细清单：看「[附录](#附录)」

## 背景

## 关键链路
- 用 3-6 行说明主流程或核心逻辑。
- 不在正文铺满 API、文件、依赖或配置清单。

## 我的分析
- 为什么我这么判断：
- 我排除了哪些方案：
- 当前风险：
- 不确定点：

## 我的理解与补充
- 我目前真正理解的是：
- 我还没完全想清楚的是：
- 后续我想继续补充的是：

## 下一步

## 附录
```

Omit or rename sections when they do not fit. Do not keep empty sections except `我的理解与补充`, which may contain clear placeholders for the author to fill in.

For long documents, add a short table of contents or reading path near the top. Use Markdown heading links for jump navigation when the target sections exist. Avoid a large nested outline that makes the document feel heavier.

### 3.1 Keep the Main Body Light

Do not solve every reader need in the main body. Keep the main body focused on:

- Conclusion and current status.
- What the reader needs to decide, confirm, or do.
- The shortest useful explanation of the core flow.
- The author's judgment, risk, and next step.
- The author's current understanding and what still needs digestion.

Move these to appendices or follow-up sections when they are useful but not essential to the first read:

- Full API endpoint lists.
- File-by-file responsibility maps.
- Dependency lists.
- Environment variable lists.
- Detailed runbooks.
- Full call chains.
- Raw research notes.
- Glossaries and term explanations.

When adding an appendix, keep it short and clearly optional. If the detail is not needed now, write a follow-up action instead of adding the appendix.

### 4. Remove AI Flavor

Rewrite into direct workplace language:

- Remove pasted rich-text noise from Markdown, such as `<font style=...>`, repeated color spans, and visual styling tags, unless the user explicitly needs HTML.
- Replace vague phrases like "体系化建设", "赋能", "闭环", "抓手", "全链路", "深度融合", "持续优化" with concrete statements.
- Delete generic introductions, repeated summaries, and obvious filler.
- Avoid over-polished parallel lists that sound generated.
- Use "我建议", "我判断", "我担心", "暂不建议", "还需要确认" when the document needs ownership.
- Prefer short paragraphs and practical bullets over dense essay text.
- Keep professional terms only when they are necessary and likely understood by the target reader.
- Remove "correct but useless" content: definitions, broad industry background, generic benefits, or textbook explanations that do not affect this work.
- Explain necessary professional terms the first time they appear, especially in the conclusion or first-screen summary.

Do not make the document casual at the cost of clarity. "Human-sounding" means specific, accountable, and readable.

Watch for phrases that make leaders suspect the author did not digest the content:

- Big claims without an example, owner, risk, or next step.
- Many abstract nouns and no concrete project detail.
- Balanced pros/cons that avoid a recommendation.
- Long background before the actual ask.
- "Everything is important" structure where no priority is visible.

### 4.1 Explain Terms Without Turning the Doc Into a Glossary

When a necessary term may block understanding, translate it into plain language immediately. Do this especially for technical, business, algorithmic, legal, financial, diagnostic, or process terms.

Use one of these patterns:

```md
`content_hash` 可以理解成“资源内容的指纹”。内容没变，指纹就一样，系统就不用重复构建。
```

```md
事务可以理解成“一次打包提交”：要么全部写成功，要么失败回滚，避免只写进去一半。
```

Rules:

- Do not put unexplained jargon in `先看结论`.
- If a term is essential, explain it in the same bullet or add a short `先把几个词说白` section.
- Prefer "term + plain-language explanation + why it matters" over dictionary definitions.
- If the term is not essential to the reader's decision or understanding, remove it or move it to an appendix.
- Replace vague high-level labels with observable behavior or concrete examples.

### 5. Add Human Judgment

If the draft lacks judgment, add clearly marked sections without inventing facts:

- **我的判断**: what the author thinks based on the available information.
- **为什么这么判断**: observable reasons, evidence, code findings, requirement constraints, or experience.
- **取舍**: why one option is preferred and what is not being chosen.
- **风险**: what could go wrong and how serious it is.
- **待确认**: facts that are not yet verified.
- **下一步**: specific actions, owners, or decisions needed when known.
- **我需要补充的个人判断**: a placeholder when the author must add real firsthand thinking.

When the source content does not support a conclusion, write it as uncertainty:

```md
我目前倾向于 A，但这里还缺少 xxx 的验证，所以不能直接定成最终结论。
```

Never fabricate research, validation, stakeholder feedback, code behavior, metrics, or personal experience.

### 5.1 Strengthen Diagnostic and Evaluation Reports

Use this section when the document diagnoses a person, process, product, project, business issue, report quality, coaching record, review record, or any AI-generated analysis.

Do not stop at "发现了哪些问题". A useful diagnostic report should show:

- **问题是什么**: state the issue in plain language.
- **证据是什么**: quote or summarize the relevant behavior, record, data point, requirement, code path, or source material.
- **为什么是问题**: explain the impact on the business, user, team, delivery, quality, or learning goal.
- **可能根因**: identify the likely cause, not only the surface symptom.
- **严重程度/优先级**: say which issue matters most and why.
- **建议动作**: give a concrete next step, owner, practice method, correction, or validation method.
- **待确认**: mark anything the source material does not prove.

Prefer this shape for each important finding:

```md
### 问题 1：一句话说清问题
- 证据：
- 我的判断：
- 可能根因：
- 影响：
- 建议动作：
- 待确认：
```

If the source is "diagnosis report + original record", compare them explicitly:

- **诊断报告说了什么**
- **原始记录是否支持这个判断**
- **我同意/不同意的地方**
- **诊断遗漏了什么**
- **应该如何改写或补充**

Avoid high-level labels unless they are immediately explained. For example, replace or explain terms like "认知偏差", "结构化表达不足", "业务敏感度不够", "需求洞察不足", "缺少闭环意识", "方法论沉淀不足" with observable behavior:

```md
不要只写：业务敏感度不够。
改成：他能复述客户问题，但没有继续追问这个问题影响哪个业务指标，所以后续建议停在表面。
```

For coaching or performance-related reports, keep the tone fair:

- Critique behavior and evidence, not personality.
- Do not exaggerate from one record into a broad character judgment.
- Separate "this record shows" from "I infer".
- Give at least one concrete improvement path.

### 5.1a Strengthen Scoring Discrepancy and System Comparison Reports

Use this section when the document compares two scoring systems, diagnosis systems, model outputs, evaluator reports, human-vs-AI results, or old-vs-new evaluation logic.

The report should not only say "scores differ". It should help readers decide whether the difference is a bug, expected rule mismatch, scenario mismatch, calibration issue, or data/sample issue.

Use this main-body shape:

```md
## 先看结论
- 样本范围：
- 最大偏差结论：
- 我的判断：
- 【待你确认】：
- 建议动作：

## 分数差异概览

## 偏差主要来自哪里

## 典型案例

## 根因判断

## 应该怎么处理

## 不应该得出的结论

## 附录
```

For each major discrepancy pattern, prefer:

```md
### 偏差模式：一句话说清
- 现象：
- 数据证据：
- 典型案例：
- 我的判断：
- 可能根因：
- 影响：
- 建议动作：
- 【待验证】：
```

For scoring reports, always separate:

- **评分对象不同**: one system scores task completion, another scores capability.
- **评分维度不同**: one system has a dimension the other does not.
- **场景目标不同**: one scenario intentionally skips a behavior that another rubric expects.
- **权重/汇总方式不同**: a zero or low dimension may drag down the final score.
- **数据口径不同**: sample size, comparable sessions, missing records, truncated conversations, or person/scenario mix.
- **真正可能的系统问题**: cases where the system contradicts its own rationale, applies irrelevant dimensions, or ignores scenario metadata.

Do not overstate conclusions from aggregate gaps alone. A useful report says what the gap proves and what it does not prove:

```md
这说明两个系统的评分口径不一致；暂时不能直接说明哪个系统更准确。
```

When the report includes people, avoid turning score gaps into personality judgments. Tie interpretations to scenarios and scoring rules:

```md
不要只写：产品脚本执行强，顾问式销售能力弱。
改成：在产品专项场景里陪练分较高，但诊断系统因 D2 需求澄清低分拉低总分；这更像评分口径差异，需要结合原始对话再判断个人能力短板。
```

Recommendations should be decision-oriented:

- Align whether the score is measuring "scenario task completion" or "general sales capability".
- Add scenario-aware scoring exemptions or weight adjustments.
- Split product专项、快速促成、异议专项、全流程对练 into separate calibration buckets.
- Review high-gap cases manually before changing model/rubric logic.
- Define which system is the reference for which business decision.

### 5.2 Strengthen Retrospective, Sharing, and Mechanism Explanation Docs

Use this section when the document explains a technical mechanism, migration, lifecycle, architecture change, old-vs-new comparison, or lessons learned.

Do not turn the main body into a complete encyclopedia. A good sharing document should first give readers a reusable mental model:

- **一句话模型**: the simplest accurate way to understand the mechanism.
- **为什么要看**: why this matters to the reader, team, project, or future work.
- **核心变化/核心经验**: what changed, what was learned, or what should be remembered.
- **主链路**: 3-8 lines that show the important flow, not every implementation detail.
- **边界和例外**: what is not fully implemented, not verified, or easy to misunderstand.
- **下一步入口**: where to read code, what to verify, or what follow-up doc/runbook is needed.

For old-vs-new or migration documents, prefer this structure:

```md
## 先看结论
- 旧版核心：
- 新版核心：
- 我的判断：
- 【待验证/待确认】：

## 一句话模型

## 旧版和新版最大的区别

## 新版主链路

## 为什么这个变化重要

## 边界和后续要补的内容

## 附录
```

If the draft is already long and mostly correct, do not rewrite it into another long document. Instead:

- Keep the main body lighter.
- Move exhaustive node/relationship/API/code lists into appendices.
- Add a "最值得记住的 3 句话" section near the top or near the end.
- Add clear reading paths for "只想理解", "要接手开发", and "要查细节".
- Replace broad technical labels with concrete explanation when a non-owner reader may not understand them.

For retrospective or experience-sharing documents, add the author's learning:

- **我之前容易怎么误解**
- **现在我怎么理解**
- **以后遇到类似问题怎么判断**
- **这次经验对后续工作的影响**

### 6. Preserve Author Learning

Always make the document useful to the author, not only the audience.

Include a section named `我的理解与补充` when the topic is complex, AI-generated, or likely to be reused later. This section should help the author convert AI output into their own understanding.

Use one of these patterns:

```md
## 我的理解与补充
- 我目前真正理解的是：
- 这件事容易误解的地方是：
- 我还需要继续确认的是：
```

or:

```md
## 我的理解与补充
这里先保留给我补充自己的判断、疑问和后续理解。当前我需要重点补充：
- 
```

Do not pretend the author has already added personal reflections. If personal content is missing, leave honest placeholders.

### 7. Control Length

Make the document shorter unless the user explicitly needs a comprehensive reference.

- Put details after conclusions.
- Merge repeated points.
- Remove background that does not affect the decision or understanding.
- Use appendices only for large technical details, logs, raw analysis, or exhaustive comparisons.
- Keep each section focused on one job.
- Prefer one useful concrete example over three generic explanations.
- Prefer "入口 + priority" over exhaustive coverage. For example, say "先看 `/extract` 链路" instead of listing every related function.
- If adding detail would make a busy reader stop reading, move it to an appendix or turn it into a next-step task.

### 8. Final Quality Check

Before answering, check:

- Does the first screen explain what the document is about and what conclusion matters?
- Does the first screen show what the reader is expected to decide, confirm, or do?
- Can a leader or teammate skip to the relevant part?
- Are facts, judgments, assumptions, and recommendations distinguishable?
- Are risks and uncertain points visible?
- Is there a place for the author to add their own thinking?
- Did the rewrite remove AI-style filler without removing important meaning?
- Would a skeptical leader think the author has personally understood the topic, or only pasted a polished AI answer?
- Is the main body short enough to read without opening every detail section?

## Output Rules

- Output the final Markdown document directly.
- If the user asks to modify an existing file, update the file instead of only showing text.
- If you changed an existing draft, optionally add a brief note after the document only when useful: "已按结论前置、去套话、补判断和下一步重排。"
- Do not add a long explanation of the editing process unless requested.
