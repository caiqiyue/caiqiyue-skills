# 个人 AI 编程规范框架设计稿

## 1. 文档目的

这份文档用于沉淀一套可在真实项目中重复使用的个人 AI 编程规范框架。

目标不是“给某个 AI 工具多写一点提示词”，而是建立一套让 `Codex`、`Claude Code`、`OpenCode` 等编程 agent 在项目里都能被约束、被验证、被接管的工程系统。

这份设计明确回答以下问题：

- 这个框架要解决什么问题
- 为什么不用工具专属目录，而采用中性目录
- 个人母 skill 和项目内框架如何分层
- `.ai/` 目录树应该长什么样
- 每个目录和核心文件分别负责什么
- 多 agent 角色如何分工
- 如何把“未经验证不能说完成”变成系统规则
- 如何围绕 `LangGraph/LangChain + Django/Spring Boot + React/Vue + Docker/K8S/Jenkins` 的多栈项目落地

---

## 2. 核心问题定义

当前最根本的问题不是“AI 不会写代码”，而是：

**一旦让 AI 来写代码，人的掌控感会迅速丢失。**

这种失控通常表现为：

- AI 直接开始改代码，但没有先确认任务范围
- 同时推进多个改动，最后每个都做到一半
- 改动触及前端、后端、agent 编排、运维链路，但没有统一主流程验证
- 代码写完后直接宣告完成，没有严格外部验证
- 多会话之间缺乏连续性，接手时需要重新考古
- 不清楚某个子智能体在做什么，也不清楚它有没有权力做这个动作

因此，第一版框架必须优先解决以下两个问题：

1. **未经验证不能说完成**
2. **一次只做一个 feature，没验证完不能开下一个**

---

## 3. 总体设计原则

### 3.1 事后控制优先

这套框架优先保证：

- AI 可以实现代码
- 但只有在验证证据完整时，才允许把结果视为完成

也就是说：

- “已实现”不等于“已完成”
- “代码可运行”不等于“交付可接受”

### 3.2 WIP=1

默认工作方式是：

- 任意时刻只允许一个活跃 feature
- 没有通过验证前，不允许开启第二个 feature

这是为了降低范围漂移、减少越界修改、压缩返工成本。

### 3.3 规范中立于工具

框架本体不应绑定在 `./codex` 或 `./claude` 这类工具名目录上。

推荐做法是：

- 根目录保留工具入口文件：`AGENTS.md`、`CLAUDE.md`
- 规范本体放在中性目录：`./.ai/`

这样做的原因：

- 项目规范不被厂商名绑死
- 可以同时适配 `Codex`、`Claude Code`、`OpenCode`
- 以后更换 agent 工具时，只需调整入口文件和适配层，不需要推翻整套项目结构

### 3.4 项目内框架优先于个人母 skill

第一版以 **项目内标准框架** 为核心，个人母 skill 作为辅助层。

原因：

- 项目内工件才真正决定 agent 能做什么、不能做什么
- 个人母 skill 适合做识别、初始化、分发和升级，不适合单独承担项目治理

---

## 4. 两层架构

这套体系拆成两层。

### 4.1 个人母 skill

位置建议：

- 全局目录，例如 `~/.codex/skills/<your-skill>/`

职责：

- 识别仓库技术栈
- 识别项目是否已经具备 `.ai/` 框架
- 给当前项目选择 profile
- 生成或修补项目内框架文件
- 强制执行你的通用规则
- 协调不同工具下的适配方式

它像“总教练”，不直接承载项目细节。

### 4.2 项目内标准框架

位置建议：

- 项目根目录下：
  - `AGENTS.md`
  - `CLAUDE.md`
  - `/.ai/`

职责：

- 承载项目具体规则
- 承载项目状态
- 承载项目验证
- 承载项目角色分工
- 承载项目主流程和边界
- 承载多栈 profile

它像“项目内 AI 工程操作系统”。

### 4.3 两层之间的关系

个人母 skill 负责：

- 这是什么项目
- 该用哪套 profile
- 缺哪些 `.ai/` 工件
- 当前建议走哪条 workflow

项目内框架负责：

- 这个项目的 LangGraph/LangChain 主流程是什么
- 后端和前端边界是什么
- 运维链路什么时候必须停下确认
- 当前唯一活跃 feature 是什么
- 什么才算完成

---

## 5. 项目内标准目录结构

第一版推荐目录树如下：

```text
project/
├─ AGENTS.md
├─ CLAUDE.md
├─ README.md
├─ .ai/
│  ├─ docs/
│  │  ├─ architecture.md
│  │  ├─ product.md
│  │  ├─ agent-flow.md
│  │  └─ boundaries.md
│  ├─ policies/
│  │  ├─ global-rules.md
│  │  ├─ definition-of-done.md
│  │  ├─ scope-policy.md
│  │  └─ change-policy.md
│  ├─ agents/
│  │  ├─ planner.md
│  │  ├─ implementer.md
│  │  ├─ reviewer.md
│  │  └─ verifier.md
│  ├─ workflows/
│  │  ├─ single-agent.md
│  │  ├─ feature-delivery.md
│  │  ├─ bugfix-loop.md
│  │  └─ review-loop.md
│  ├─ state/
│  │  ├─ feature-list.json
│  │  ├─ active-task.md
│  │  ├─ progress.md
│  │  └─ session-handoff.md
│  ├─ verify/
│  │  ├─ verify-dev.md
│  │  ├─ verify-integration.md
│  │  ├─ verify-agent-flow.md
│  │  ├─ verify-ops.md
│  │  └─ checklist.md
│  ├─ evals/
│  │  ├─ smoke-cases.md
│  │  ├─ regression-cases.md
│  │  ├─ failure-patterns.md
│  │  └─ acceptance-cases.md
│  ├─ profiles/
│  │  ├─ profile-selection.md
│  │  ├─ langgraph-django-react.md
│  │  └─ langgraph-springboot-vue.md
│  ├─ templates/
│  │  ├─ feature-list.template.json
│  │  ├─ progress.template.md
│  │  ├─ handoff.template.md
│  │  └─ agent-role.template.md
│  ├─ scripts/
│  │  ├─ verify.sh
│  │  └─ check-structure.sh
│  └─ hooks/
│     ├─ pre-task.md
│     ├─ pre-complete.md
│     └─ post-change.md
```

---

## 6. 每个目录的职责

### 6.1 `docs/`

职责：项目知识层。

放置内容：

- 架构分层
- 产品目标
- agent 主流程
- 代码边界与系统边界

关键文件：

- `architecture.md`
  - 系统分层、模块结构、数据流
- `product.md`
  - 用户价值、关键业务行为
- `agent-flow.md`
  - 典型 agent 主路径
- `boundaries.md`
  - agent 层、后端层、前端层、ops 层不可越界项

### 6.2 `policies/`

职责：硬规则层。

关键文件：

- `global-rules.md`
- `definition-of-done.md`
- `scope-policy.md`
- `change-policy.md`

其中必须写死的核心规则：

- 未经验证不能说完成
- 一次只做一个 feature

### 6.3 `agents/`

职责：子智能体角色层。

第一版角色：

- `planner`
- `implementer`
- `reviewer`
- `verifier`

每个角色文件都应定义：

- 角色使命
- 允许做什么
- 禁止做什么
- 输入契约
- 输出契约

### 6.4 `workflows/`

职责：协作流程层。

第一版流程：

- `single-agent`
- `feature-delivery`
- `bugfix-loop`
- `review-loop`

其中默认主流程是：

`planner -> implementer -> reviewer -> verifier`

### 6.5 `state/`

职责：状态层。

关键文件：

- `feature-list.json`
- `active-task.md`
- `progress.md`
- `session-handoff.md`

重点：

- `feature-list.json` 是结构化状态机
- `active-task.md` 用来强制 WIP=1

### 6.6 `verify/`

职责：验证层。

关键文件：

- `verify-dev.md`
- `verify-integration.md`
- `verify-agent-flow.md`
- `verify-ops.md`
- `checklist.md`

这里是你“事后控制”的主战场。

### 6.7 `evals/`

职责：验证样例层。

关键文件：

- `smoke-cases.md`
- `regression-cases.md`
- `failure-patterns.md`
- `acceptance-cases.md`

验证不是一句“请测试”，而是具体场景集合。

### 6.8 `profiles/`

职责：技术栈 profile 层。

第一版 profile：

- `langgraph-django-react`
- `langgraph-springboot-vue`

再加一份：

- `profile-selection.md`

用于自动识别后再人工确认。

### 6.9 `templates/`

职责：模板复用层。

让新项目可以快速套用统一结构，而不是每次手工重写。

### 6.10 `scripts/`

职责：自动化辅助层。

第一版只需两个脚本：

- `verify.sh`
- `check-structure.sh`

不追求自动化铺满，只做必要支撑。

### 6.11 `hooks/`

职责：hook 协议层。

第一版不要求自动执行，而是先定义：

- `pre-task`
- `pre-complete`
- `post-change`

以后再按工具接入实际 hook 机制。

---

## 7. 根目录入口文件设计

### 7.1 `AGENTS.md`

职责：

- 所有 agent 的总入口
- 路由到 `.ai/` 中的规则和文档

必须包含：

- 项目一句话定义
- 启动顺序
- 默认 workflow
- 两条硬规则
- Definition of Done 入口
- architecture / state / verify / agents 的引用路径

### 7.2 `CLAUDE.md`

职责：

- `Claude Code` 的入口补充
- 保持与 `AGENTS.md` 同一大方向
- 可增加 Claude Code 的工具特性提示，但不能偏离规范本体

---

## 8. 4 个关键文件的推荐写法

### 8.1 `AGENTS.md`

核心要点：

- 它是入口协议，不是知识百科
- 只写“先看什么、先做什么、什么不能做、什么才算完成”

应包含：

- `Project`
- `Startup Workflow`
- `Hard Rules`
- `Default Workflow`
- `Task Entry Rule`
- `Completion Rule`
- `References`

### 8.2 `definition-of-done.md`

核心要点：

- 它是最核心的“事后控制器”
- 把“完成”从主观感觉变成客观门槛

应包含至少 7 类条件：

- 实现完成
- 本地可运行
- 联调通过
- Agent 主流程通过
- 关键日志正常
- 状态已更新
- 满足以上条件后才允许说完成

### 8.3 `feature-list.json`

建议字段：

- `project`
- `activeTaskId`
- `features[]`
  - `id`
  - `name`
  - `description`
  - `scope`
  - `dependencies`
  - `status`
  - `verification`
  - `evidence`
  - `ownerRole`
  - `updatedAt`

推荐状态值：

- `not_started`
- `active`
- `blocked`
- `implemented`
- `verified`
- `failed`

关键设计：

- 把 `implemented` 和 `verified` 分开
- 防止“做出来就等于完成”

### 8.4 `verify-agent-flow.md`

这是最关键的验证文件之一。

它应该围绕你最典型的主流程写：

`用户提交任务 -> LangGraph 编排 -> 调工具 -> 写库 -> Django/Spring Boot 返回结果 -> 前端展示`

应覆盖：

- 输入阶段
- 编排阶段
- 工具调用阶段
- 持久化阶段
- 返回阶段
- 展示阶段
- 日志检查

并明确：

- 只有全链路通过且关键日志正常，才允许把 feature 标记为 `verified`

---

## 9. 多 agent 角色分工设计

### 9.1 `planner`

职责：

- 收敛需求为单一 feature
- 明确 scope / out-of-scope / verification
- 选择 workflow

不负责编码。

### 9.2 `implementer`

职责：

- 只实现当前唯一 active feature
- 不得扩 scope
- 提交 changed files、risks、verification-needed

不得宣布完成。

### 9.3 `reviewer`

职责：

- 独立检查 scope、boundaries、设计适配
- 决定是否准入验证

不得接手实现。

### 9.4 `verifier`

职责：

- 对照 Definition of Done 跑验证链
- 收集证据
- 决定能否将状态推进到 `verified`

不得在无证据的情况下放行。

### 9.5 三条协作铁律

第一版必须明确写进规则：

1. implementer 永远不能宣布完成
2. reviewer 永远不能直接接手实现
3. verifier 永远不能在没有证据时放行

---

## 10. 工作流设计

### 10.1 `single-agent`

适用场景：

- 小改动
- 低风险
- 不跨主要边界

即便如此，也不能跳过验证门。

### 10.2 `feature-delivery`

默认主流程：

`planner -> implementer -> reviewer -> verifier`

适用于：

- 常规 feature
- agent 主流程修改
- 前后端联调改动

### 10.3 `bugfix-loop`

推荐流程：

`planner -> reproducer -> implementer -> verifier`

若第一版不单设 `reproducer`，也必须写死：

- 先复现
- 再定位
- 再修复
- 再验证

### 10.4 `review-loop`

问题发现后的回退规则：

- scope 问题 -> 退回 planner
- 实现问题 -> 退回 implementer
- 验证失败 -> 退回 implementer
- DoD 不清 -> 退回 planner / policy owner

---

## 11. `profiles + verify + evals` 三层协同

### 11.1 `profiles/`

负责判断：

- 当前仓库是什么技术栈
- 应该套用哪套默认命令和验证门

### 11.2 `verify/`

负责定义：

- dev 验证
- integration 验证
- agent-flow 验证
- ops 验证

### 11.3 `evals/`

负责沉淀：

- smoke cases
- regression cases
- failure patterns
- acceptance cases

### 11.4 三者关系

- `profiles` 决定“你是谁”
- `verify` 决定“你该怎么验”
- `evals` 决定“你到底验哪些场景”

---

## 12. 典型主流程验证标准

你的项目最典型的主流程定义为：

`用户提交任务 -> LangGraph 编排 -> 调工具 -> 写库 -> Django/Spring Boot 返回结果 -> 前端展示`

因此，默认接受条件应至少同时满足：

- 代码能跑
- 前后端联调通过
- agent 流程验证通过
- 关键日志正常

这也是为什么你选择的是 `C` 型完成门，而不是简单的“单测通过即可”。

---

## 13. 初始化顺序

不要一开始把所有目录都写满。

推荐分三阶段落地。

### 阶段 1：先立入口、状态、完成门

优先创建：

- `AGENTS.md`
- `CLAUDE.md`
- `.ai/policies/definition-of-done.md`
- `.ai/policies/global-rules.md`
- `.ai/state/feature-list.json`
- `.ai/state/active-task.md`
- `.ai/verify/verify-agent-flow.md`
- `.ai/verify/checklist.md`

这一阶段先把掌控权拿回来。

### 阶段 2：补项目知识和协作流程

再创建：

- `.ai/docs/architecture.md`
- `.ai/docs/agent-flow.md`
- `.ai/docs/boundaries.md`
- `.ai/workflows/feature-delivery.md`
- `.ai/agents/implementer.md`
- `.ai/agents/reviewer.md`
- `.ai/agents/verifier.md`
- `.ai/profiles/profile-selection.md`

### 阶段 3：补治理层和复用层

最后创建：

- `.ai/evals/*`
- `.ai/templates/*`
- `.ai/scripts/*`
- `.ai/hooks/*`
- 其他 profiles
- 其他 workflows

---

## 14. 落地优先级

### P0：绝对优先

- `AGENTS.md`
- `definition-of-done.md`
- `feature-list.json`
- `active-task.md`
- `verify-agent-flow.md`

### P1：高优先

- `architecture.md`
- `boundaries.md`
- `feature-delivery.md`
- `reviewer.md`
- `verifier.md`
- `checklist.md`

### P2：中优先

- `profile-selection.md`
- `verify-integration.md`
- `verify-ops.md`
- `session-handoff.md`
- `progress.md`

### P3：后续增强

- `evals/`
- `templates/`
- `scripts/`
- `hooks/`
- profile 扩展

---

## 15. 运行方式

一条标准任务应按以下顺序推进：

1. agent 读取 `AGENTS.md`
2. 读取 `.ai/state/active-task.md`
3. 读取 `.ai/state/feature-list.json`
4. 读取 `.ai/policies/definition-of-done.md`
5. 根据 profile 和 workflow 确定推进方式
6. implementer 只实现一个 feature
7. reviewer 决定能否进入验证
8. verifier 按 `verify-agent-flow` 和 checklist 跑验证
9. 只有证据完整，才允许将任务状态改为 `verified`

---

## 16. 第一版的最终目标

第一版不追求：

- 全部自动化
- 全目录填满
- 完整平台化治理

第一版只追求 5 件事：

1. 入口清晰
2. 状态唯一
3. 完成可证
4. 协作可控
5. 主流程可验

也就是说：

**第一版先做“掌控系统”，第二版再做“自动化系统”。**

---

## 17. 最终结论

这套设计的本质不是“给 AI 多一点文档”，而是：

**把 AI 编程从聊天行为，升级为仓库内有入口、有状态、有规则、有验证、有交接的制度化行为。**

对你的项目类型来说，这一点尤其重要，因为你的工程天然跨越：

- agent orchestration
- backend service
- frontend UI
- ops chain

任何一层没有被纳入规则和验证，AI 的“完成”都不可信。

因此，第一版项目内标准框架必须优先围绕以下两个原则建立：

1. **未经验证不能说完成**
2. **一次只做一个 feature**

这两个原则一旦落成工件，而不只是聊天要求，你的掌控感才会真正回来。
