# 个人 Harness Skill / Plugin 跨平台交付方案

## 1. 文档目的

这份文档回答的不是“harness 是什么”，而是更具体的问题：

- 如何把前一份设计文档里的 harness 框架，做成 **可分发、可安装、可复用** 的个人技能仓库
- 如何同时兼容 `Codex`、`Claude Code`、`OpenCode`
- 每个平台到底接受什么格式
- 哪些内容可以共用，哪些内容必须做平台适配
- `caiqiyue-skills` 仓库应该长成什么样，才能长期维护而不失控

结论先说：

**不要试图做一个“单目录、单清单、三端通吃”的神奇插件。**
三种工具的技能 / 插件 / 规则系统并不相同。正确方案是：

**一套共享核心内容 + 三套平台适配层 + 一套构建/同步脚本。**

---

## 2. 调研结论总览

### 2.1 Codex

Codex 侧要区分两类东西：

- **仓库级指导文件**
  - 公开官方文档明确强调 `AGENTS.md`
  - 用于告诉 Codex 如何理解代码库、运行哪些命令、遵守哪些项目实践
- **Skill**
  - 核心是 `SKILL.md`
  - 最小元数据是 `name`、`description`
  - 可带 `agents/openai.yaml`
  - 可带 `scripts/`、`references/`、`assets/`
- **Plugin**
  - 核心清单是 `.codex-plugin/plugin.json`
  - 可包含 `skills/`、`hooks/`、`scripts/`、`assets/`、`.mcp.json`、`.app.json`

从本机 Codex 技能/插件规范可以确认：

- 技能是 **目录级别单元**
- 插件是 **目录级别单元**
- Codex 插件清单与 Claude 插件清单不是一回事
- Codex 公开官方文档更强调 `AGENTS.md` 和使用方式；更细的本地 Skill / Plugin 包结构，需要结合本机可验证约定来设计

### 2.2 Claude Code

Claude Code 官方文档明确支持三层扩展：

- **项目记忆 / 规则**
  - `CLAUDE.md`
  - 可通过 `@AGENTS.md` 引用已有通用规则
- **Skill**
  - `.claude/skills/<skill-name>/SKILL.md`
  - 或插件中的 `skills/<skill-name>/SKILL.md`
- **Plugin**
  - `.claude-plugin/plugin.json`
  - 插件根目录可含 `skills/`、`agents/`、`hooks/`、`.mcp.json`、`.lsp.json`、`settings.json` 等

Claude Code 还原生支持：

- `.claude/agents/*.md` 自定义子智能体
- `hooks`
- 插件 marketplace

这对你的 harness 非常关键，因为你的设计本来就依赖：

- 子智能体角色分工
- 生命周期校验
- 可重复分发

### 2.3 OpenCode

OpenCode 的扩展面与前两者不同，重点是：

- **规则文件**
  - `AGENTS.md`
  - 会优先于 `CLAUDE.md`
- **配置文件**
  - `opencode.json` / `opencode.jsonc`
- **Skill**
  - 官方主路径是 `.opencode/skills/<name>/SKILL.md`
  - 同时兼容 `.claude/skills/<name>/SKILL.md`
  - 也兼容 `.agents/skills/<name>/SKILL.md`
- **自定义命令**
  - `.opencode/commands/*.md`
- **自定义 agent**
  - `.opencode/agents/*.md`
  - 或 `opencode.json` 中的 `agent`
- **插件**
  - `.opencode/plugins/*.js|*.ts`
  - 或 npm 包，通过 `plugin` 字段加载

OpenCode 当前仓库格式和你现有 `caiqiyue-skills` 仓库最接近，因为你的仓库已经有：

- `.agents/skills/content-builder/SKILL.md`
- `package.json` 中的 `opencode.skills`

这说明：

**你现在的仓库本质上已经偏 OpenCode/Agent Skills 兼容风格，还没有真正变成 Codex + Claude + OpenCode 三端统一交付仓库。**

---

## 3. 最重要的工程判断

### 3.1 单一物理格式不可行

三端不能共享一个“原样即装”的目录，原因是：

- Codex plugin 清单是 `.codex-plugin/plugin.json`
- Claude plugin 清单是 `.claude-plugin/plugin.json`
- OpenCode plugin 是 `.opencode/plugins/*.ts` 或 npm plugin，不认上面两种 manifest

同理，skill 的发现路径也不同：

- Codex：Skill 目录 + `SKILL.md`
- Claude：`.claude/skills/<name>/SKILL.md` 或 plugin `skills/<name>/SKILL.md`
- OpenCode：官方主路径是 `.opencode/skills/`，同时又兼容 `.claude/skills/` 和 `.agents/skills/`，还常与 `.opencode/commands/`、`.opencode/agents/`、`AGENTS.md` 组合实现

所以必须接受这个现实：

**“同一套内容”可以共享，但“同一套包结构”不能共享。**

### 3.2 正确做法是“内容核心统一，分发外壳分叉”

你要维护的真正资产不是某个工具的 manifest，而是这几类东西：

- harness 原则
- 角色定义
- 工作流
- project `.ai/` 模板
- profile 模板
- verify / evals 模板
- 初始化步骤
- 输出要求

这些应该成为 **平台无关的核心资产**。

然后再生成：

- Codex 版本
- Claude Code 版本
- OpenCode 版本

---

## 4. 推荐的仓库目标形态

针对 `caiqiyue/caiqiyue-skills.git`，我建议目标仓库形态如下：

```text
caiqiyue-skills/
├─ docs/
│  ├─ personal-ai-harness-framework-design.md
│  └─ personal-harness-skill-delivery-plan.md
├─ core/
│  ├─ harness-spec/
│  │  ├─ overview.md
│  │  ├─ rules.md
│  │  ├─ workflows.md
│  │  ├─ roles.md
│  │  └─ verification.md
│  ├─ templates/
│  │  └─ project-ai-framework/
│  │     ├─ AGENTS.md
│  │     ├─ CLAUDE.md
│  │     └─ .ai/
│  │        ├─ docs/
│  │        ├─ policies/
│  │        ├─ agents/
│  │        ├─ workflows/
│  │        ├─ state/
│  │        ├─ verify/
│  │        ├─ evals/
│  │        ├─ profiles/
│  │        ├─ templates/
│  │        ├─ scripts/
│  │        └─ hooks/
│  ├─ profiles/
│  │  ├─ langgraph-django-react.md
│  │  └─ langgraph-springboot-vue.md
│  └─ snippets/
│     ├─ definition-of-done.md
│     ├─ feature-list.template.json
│     └─ verify-agent-flow.md
├─ adapters/
│  ├─ codex-skill/
│  │  └─ personal-harness/
│  ├─ codex-plugin/
│  │  └─ personal-harness-plugin/
│  ├─ claude-plugin/
│  │  ├─ .claude-plugin/
│  │  │  └─ marketplace.json
│  │  └─ plugins/
│  │     └─ personal-harness-plugin/
│  └─ opencode/
│     ├─ .agents/
│     │  └─ skills/
│     │     └─ personal-harness/
│     ├─ .opencode/
│     │  ├─ agents/
│     │  ├─ commands/
│     │  └─ plugins/
│     └─ package.json
└─ scripts/
   ├─ sync-core-to-adapters.(js|py)
   ├─ build-codex-skill.(js|py)
   ├─ build-codex-plugin.(js|py)
   ├─ build-claude-plugin.(js|py)
   └─ build-opencode-package.(js|py)
```

这棵树背后的原则是：

- `docs/`：解释方案和设计，不参与安装
- `core/`：唯一事实源，存真正的方法论和模板
- `adapters/`：三端各自能安装的真实产物
- `scripts/`：避免人工复制粘贴导致三端漂移

---

## 5. 三端适配策略

## 5.1 Codex 适配策略

### 目标

给 Codex 提供两种交付形态：

1. **Skill 版**
   - 适合“按流程做事”
   - 重点承载 harness 方法论和项目初始化流程
2. **Plugin 版**
   - 适合需要额外 hooks / 工具 / MCP / 应用集成时扩展

### 推荐目录

```text
adapters/codex-skill/personal-harness/
├─ SKILL.md
├─ agents/
│  └─ openai.yaml
├─ references/
│  ├─ harness-spec.md
│  ├─ roles.md
│  ├─ workflows.md
│  └─ verification.md
└─ assets/
   └─ project-ai-framework/
```

### `SKILL.md` 应承担的职责

- 识别仓库是否已有 `AGENTS.md` / `CLAUDE.md` / `.ai/`
- 自动识别技术栈并要求用户确认 profile
- 初始化项目内 `.ai/` 框架
- 进入任务前先检查：
  - 当前 active task
  - DoD
  - verify 策略
- 推进中坚持两条硬规则：
  - 未经验证不能说完成
  - 一次只做一个 feature

### Codex plugin 版什么时候需要

如果你后续希望在 Codex 里加入：

- 安装型 UI 展示
- 插件级 skill 打包
- MCP / App / hook 级扩展
- 更正式的个人 marketplace 分发

那就再做：

```text
adapters/codex-plugin/personal-harness-plugin/
├─ .codex-plugin/
│  └─ plugin.json
├─ skills/
│  └─ personal-harness/
├─ hooks/
├─ scripts/
└─ assets/
```

### Codex 侧建议

第一版先交付 **skill**，第二版再补 **plugin**。

原因：

- 你的核心价值首先是流程治理，不是外部系统连接
- harness 的第一价值是“让 AI 按你的规范工作”，skill 已经足够承载这一层
- plugin 更适合第二阶段补 distribution / integration

---

## 5.2 Claude Code 适配策略

### 目标

Claude Code 这边不建议只做 `.claude/skills/` 散文件。
更合适的是直接做成 **plugin + marketplace**。

原因：

- 你要复用到多个项目
- 你需要 skill + agents + hooks 联动
- Claude Code 原生支持 plugin marketplace，适合长期分发

### 推荐目录

```text
adapters/claude-plugin/
├─ .claude-plugin/
│  └─ marketplace.json
└─ plugins/
   └─ personal-harness-plugin/
      ├─ .claude-plugin/
      │  └─ plugin.json
      ├─ skills/
      │  └─ personal-harness/
      │     └─ SKILL.md
      ├─ agents/
      │  ├─ planner.md
      │  ├─ implementer.md
      │  ├─ reviewer.md
      │  └─ verifier.md
      ├─ hooks/
      │  └─ hooks.json
      ├─ settings.json
      └─ assets/
         └─ project-ai-framework/
```

### Claude plugin 中最重要的 4 块

#### 1. `skills/personal-harness/SKILL.md`

承担主入口逻辑：

- 什么时候触发 harness
- 先读什么
- 如何识别 profile
- 如何初始化 `.ai/`
- 如何检查 DoD 和 active task

#### 2. `agents/*.md`

把你设计里的 4 个角色真正落成 Claude subagents：

- `planner`
- `implementer`
- `reviewer`
- `verifier`

这样 Claude 可以：

- 自动委派
- 显式调用
- 并在 plugin 分发中复用

#### 3. `hooks/hooks.json`

这里非常适合落你最关键的硬规则。

例如：

- `PreToolUse`
  - 阻止明显越界的 destructive 操作
- `Stop` / `SubagentStop`
  - 在 agent 声称完成前检查 evidence
- `PostToolUse`
  - 修改文件后自动提醒同步 state artifacts

#### 4. `assets/project-ai-framework/`

作为初始化模板源：

- `AGENTS.md`
- `CLAUDE.md`
- `.ai/` 整棵模板树

### Claude 侧建议

Claude Code 第一版应优先做 **plugin**，而不是只有 skill。

因为 Claude 是三端里对：

- skills
- subagents
- hooks
- marketplace

支持最完整的一端，最适合承载你的个人 harness 体系。

---

## 5.3 OpenCode 适配策略

### 目标

OpenCode 不要强行模仿 Claude plugin 结构。
应该顺着它自己的机制来做：

- `AGENTS.md`
- `opencode.json`
- `.opencode/commands/`
- `.opencode/agents/`
- `.opencode/plugins/`
- `.agents/skills/`

### 推荐目录

```text
adapters/opencode/
├─ .opencode/
│  ├─ skills/
│  │  └─ personal-harness/
│  │     └─ SKILL.md
│  ├─ agents/
│  │  ├─ planner.md
│  │  ├─ implementer.md
│  │  ├─ reviewer.md
│  │  └─ verifier.md
│  ├─ commands/
│  │  ├─ init-harness.md
│  │  ├─ verify-feature.md
│  │  └─ handoff.md
│  └─ plugins/
│     └─ harness-guard.ts
├─ .agents/
│  └─ skills/
│     └─ personal-harness/
│        └─ SKILL.md
├─ AGENTS.md
└─ package.json
```

### OpenCode 中各部分的分工

#### `.opencode/skills/personal-harness/SKILL.md`

承载大流程说明，作为 OpenCode 官方主路径 skill。

#### `.agents/skills/personal-harness/SKILL.md`

作为兼容层保留，方便复用你现有仓库习惯，也兼容 Agent Skills 风格工具。

#### `.opencode/agents/*.md`

真正把角色拆开，贴近 OpenCode agent 机制。

#### `.opencode/commands/*.md`

特别适合固化几个高频动作：

- `/init-harness`
- `/verify-feature`
- `/handoff`
- `/review-active-task`

#### `.opencode/plugins/harness-guard.ts`

如果你要把“规则”做成更强的执行层，OpenCode 这边非常适合用 plugin：

- 拦截某些高风险工具调用
- 在 session compacting 时注入 current task / decisions
- 对 `.env`、`secrets/`、`k8s/production` 做保护

### OpenCode 侧建议

第一版保留你当前仓库对 OpenCode 的友好性，但升级为：

- 技能 + commands
- skills + agents
- 必要时再加 plugin

这样最稳，不会为了“统一外形”把 OpenCode 的原生能力浪费掉。

---

## 6. 平台无关核心资产应该如何组织

不管哪一端，真正需要共用的是这些：

### 6.1 核心规则

- 未经验证不能说完成
- 一次只做一个 feature
- 涉及 Docker/K8S/Jenkins 默认需要额外确认
- 改 agent 主流程必须做 agent-flow verify

### 6.2 核心角色

- planner
- implementer
- reviewer
- verifier

### 6.3 核心工作流

- single-agent
- feature-delivery
- bugfix-loop
- review-loop

### 6.4 核心模板

- `AGENTS.md`
- `CLAUDE.md`
- `.ai/docs/*`
- `.ai/policies/*`
- `.ai/state/*`
- `.ai/verify/*`
- `.ai/evals/*`
- `.ai/profiles/*`

### 6.5 核心 profile

- `langgraph-django-react`
- `langgraph-springboot-vue`

### 6.6 核心验证逻辑

- dev verify
- integration verify
- agent-flow verify
- ops verify

所以 `core/` 里的内容应该尽量平台无关，避免写：

- “点击 Claude 的这个按钮”
- “在 Codex 的某个面板里做什么”
- “只有 OpenCode 才有的 UI 细节”

这些都应该留给 adapter 层。

---

## 7. 建议的产品拆分

为了让这个仓库不失控，我建议你把目标产品拆成 3 个可独立发布的交付物。

## 7.1 `personal-harness-core`

这是内容核心，不直接安装给某个 agent。

包含：

- harness 方法论
- `.ai/` 项目模板
- rules / roles / workflows / profiles / verify / evals

### 价值

- 作为唯一事实源
- 避免三端重复维护

## 7.2 `personal-harness-skill`

这是轻量级入口层。

主要做：

- 识别项目
- 选 profile
- 初始化 `.ai/`
- 引导进入标准 workflow

它更接近：

- Codex skill
- Claude skill
- OpenCode `.agents/skills`

## 7.3 `personal-harness-plugin`

这是增强层。

主要做：

- subagents
- hooks
- MCP / app / plugin 级能力
- distribution / marketplace

它更接近：

- Codex plugin
- Claude plugin
- OpenCode plugin

### 这个拆分的好处

这样你可以分阶段推进：

1. 先让 skill 好用
2. 再让 plugin 更强
3. 不会第一天就把复杂度打满

---

## 8. 第一版最合理的落地顺序

## 阶段 A：先把核心内容做成单一事实源

先建：

- `core/harness-spec/`
- `core/templates/project-ai-framework/`
- `core/profiles/`
- `core/snippets/`

目标：

- 不管最后生成哪一端，内容都从这里出

## 阶段 B：先做 Codex skill

先交付：

- `adapters/codex-skill/personal-harness/`

目标：

- 最快验证 harness 内容本身是否能驱动项目初始化和任务约束

## 阶段 C：再做 Claude plugin

再交付：

- `adapters/claude-plugin/plugins/personal-harness-plugin/`
- `adapters/claude-plugin/.claude-plugin/marketplace.json`

目标：

- 把 subagents + hooks + plugin distribution 一次补齐

## 阶段 D：再做 OpenCode 适配

再交付：

- `adapters/opencode/`

目标：

- 接回你现有仓库已有的 OpenCode 能力
- 让 skill / agents / commands / plugin 都能跑起来

## 阶段 E：最后补构建脚本

最后再做：

- `scripts/sync-core-to-adapters.*`
- `scripts/build-*`

目标：

- 把重复性同步工作自动化

---

## 9. 每一端的“成功安装并使用”判定

用户要求是三端都能成功安装并使用。

这件事不能只靠“文件存在”，必须有明确验收。

## 9.1 Codex 验收

至少要满足：

- Skill 能被识别
- 能显式触发
- 能读取核心参考文件
- 能初始化 `.ai/` 项目框架
- 触发后会执行 profile 识别 + DoD 约束 + WIP=1 约束

如果做 plugin 版，还要补：

- `.codex-plugin/plugin.json` 能通过校验
- plugin 中的 skill 能被 namespaced 识别

## 9.2 Claude Code 验收

至少要满足：

- plugin manifest 可加载
- `/plugin marketplace add` + `/plugin install` 路径成立
- skill 可被 `/plugin-name:skill-name` 触发
- subagents 能出现在 `/agents`
- hooks 能在预期时机触发
- plugin 中模板可被用来初始化项目

## 9.3 OpenCode 验收

至少要满足：

- `AGENTS.md` 能被规则系统读取
- `.agents/skills/personal-harness/SKILL.md` 能被技能系统识别
- `.opencode/commands/*.md` 能生成命令
- `.opencode/agents/*.md` 或 `opencode.json.agent` 能被识别
- 如实现 plugin，则 `.opencode/plugins/*.ts` 能加载

---

## 10. 强烈建议增加的构建/同步脚本

如果没有同步脚本，这个仓库很快就会变成三套内容慢慢漂移。

至少建议做下面 4 个脚本：

### 10.1 `sync-core-to-adapters`

职责：

- 把 `core/` 中的规范、模板、片段同步到各 adapter
- 例如把 `definition-of-done.md` 注入到：
  - Codex references
  - Claude skill docs
  - OpenCode skill docs

### 10.2 `build-codex-skill`

职责：

- 生成 Codex skill 目录
- 生成或更新 `agents/openai.yaml`

### 10.3 `build-claude-plugin`

职责：

- 生成 Claude plugin 目录
- 生成 `plugin.json`
- 生成 marketplace 条目

### 10.4 `build-opencode-package`

职责：

- 更新 `.agents/skills/`
- 更新 `.opencode/commands/`
- 更新 `.opencode/agents/`
- 更新 `package.json` 的 `opencode.skills`

---

## 11. 建议的仓库发布策略

### 11.1 不建议第一版直接发布成“一个 npm 包解决一切”

原因：

- Codex 和 Claude plugin 都不是单纯 npm 格式
- OpenCode plugin 才天然偏 npm
- 强行统一只会让交付物更怪

### 11.2 推荐发布策略

#### 方案 1：仓库内多产物

- GitHub 仓库里同时放：
  - docs
  - core
  - Codex adapter
  - Claude adapter
  - OpenCode adapter

优点：

- 结构清晰
- 所有内容集中管理

#### 方案 2：后续再拆 release

当你成熟后，再拆：

- `caiqiyue-harness-core`
- `caiqiyue-codex-harness`
- `caiqiyue-claude-harness-plugin`
- `caiqiyue-opencode-harness`

第一阶段不必着急拆仓。

---

## 12. 针对你这个 harness 的最重要落地点

这个个人 harness 不应该只是“写一个大 prompt”。

它至少要帮你做 5 件事：

1. **识别项目**
   - LangGraph / LangChain
   - Django / Spring Boot
   - React / Vue
   - Docker / K8S / Jenkins

2. **选择 profile**
   - 自动检测
   - 再让你确认

3. **初始化项目治理框架**
   - 根目录入口文件
   - `.ai/` 目录
   - state / verify / policy / workflow 模板

4. **约束任务推进**
   - 只能一个 active feature
   - implementer 不能宣布完成
   - verifier 必须看证据

5. **把完成判定变成验证系统**
   - 前后端联调
   - agent-flow verify
   - 关键日志检查
   - state artifact 更新

如果某个适配层不能承载这 5 件事，它就不是合格的 harness 适配。

---

## 13. 对 `caiqiyue-skills` 仓库的直接建议

基于你当前仓库状态，我建议：

### 13.1 保留现有 OpenCode 资产，但不要继续把仓库只当 OpenCode skill 仓库

当前仓库已经有：

- `.agents/skills/content-builder/SKILL.md`
- `package.json` 里的 `opencode.skills`

这部分可以保留，但仓库定位要升级为：

**跨平台 AI engineering skills repository**

### 13.2 第一批新增内容

优先新增：

- `docs/`
- `core/`
- `adapters/codex-skill/`
- `adapters/claude-plugin/`
- `adapters/opencode/`

### 13.3 第一批不要急着做的内容

先不要急着做：

- 太多花哨插件 UI
- 太重的 marketplace 元数据装饰
- 太复杂的自动发布流水线

先把：

- 核心内容
- 平台适配
- 安装路径
- 验证路径

这四件事跑通。

---

## 14. 建议的第一版实施清单

### P0

- 建 `docs/`
- 建 `core/`
- 把前一份设计文档内容拆进 `core/`
- 建 Codex skill adapter

### P1

- 建 Claude plugin adapter
- 建 Claude marketplace 文件
- 建 4 个 Claude subagents

### P2

- 建 OpenCode adapter
- 把现有 skill 仓库升级到多产物结构

### P3

- 建同步脚本
- 增加跨平台 smoke checklist

---

## 15. 最终推荐方案

如果只保留一句最终方案，那就是：

**把你的个人 harness 做成“一个跨平台仓库里的三端适配产品族”，而不是做成一个巨大的单平台 prompt。**

具体来说：

- 用 `core/` 保存真正的方法论和模板
- 用 `adapters/codex-skill/` 交付 Codex skill
- 用 `adapters/claude-plugin/` 交付 Claude plugin + marketplace
- 用 `adapters/opencode/` 交付 OpenCode skills / commands / agents / plugin
- 用 `scripts/` 保持三端内容同步

这条路线最符合你的目标：

- 保持掌控感
- 让 harness 具体化
- 适配多工具而不被某个工具绑死
- 可以长期迭代，而不是写一次大 prompt 后持续腐烂

---

## 16. 本方案引用的关键资料

### OpenAI / Codex

- OpenAI Developers, *Codex*  
  https://developers.openai.com/codex
- OpenAI Developers, *Codex CLI*  
  https://developers.openai.com/codex/cli
- OpenAI Developers, *Codex CLI / AGENTS.md*  
  https://developers.openai.com/codex/cli#agentsmd
- OpenAI Academy, *Plugins and skills*  
  https://openai.com/academy/codex-plugins-and-skills/
- OpenAI Academy, *Using skills*  
  https://openai.com/academy/skills/
- OpenAI, *Introducing Codex*  
  https://openai.com/index/introducing-codex/

### Claude Code

- Claude Code Docs, *Extend Claude with skills*  
  https://code.claude.com/docs/en/slash-commands
- Claude Code Docs, *Create custom subagents*  
  https://code.claude.com/docs/en/sub-agents
- Claude Code Docs, *Hooks reference*  
  https://code.claude.com/docs/en/hooks
- Claude Code Docs, *Create plugins*  
  https://code.claude.com/docs/en/plugins
- Claude Code Docs, *Plugins reference*  
  https://code.claude.com/docs/en/plugins-reference
- Claude Code Docs, *Create and distribute a plugin marketplace*  
  https://code.claude.com/docs/en/plugin-marketplaces
- Claude Code Docs, *Memory / CLAUDE.md*  
  https://code.claude.com/docs/en/memory

### OpenCode

- OpenCode Docs, *Skills*  
  https://dev.opencode.ai/docs/skills/
- OpenCode Docs, *Rules*  
  https://dev.opencode.ai/docs/rules/
- OpenCode Docs, *Config*  
  https://dev.opencode.ai/docs/config
- OpenCode Docs, *Commands*  
  https://dev.opencode.ai/docs/commands
- OpenCode Docs, *Agents*  
  https://dev.opencode.ai/docs/agents/
- OpenCode Docs, *Hooks*  
  https://dev.opencode.ai/docs/hooks/
- OpenCode Docs, *Plugins*  
  https://dev.opencode.ai/docs/plugins/

### 本机可验证的 Codex 本地规范

- `C:\Users\Administrator\.codex\skills\.system\skill-creator\SKILL.md`
- `C:\Users\Administrator\.codex\skills\.system\plugin-creator\SKILL.md`
