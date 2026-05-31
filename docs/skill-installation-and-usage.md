# 个人 Harness Skill 安装与使用说明

## 1. 这份说明的定位

这份文档回答 3 个问题：

- 这个仓库里的“个人 harness skill”到底是什么
- 现在这个仓库处于什么阶段
- 后续正式做成 `Codex` / `Claude Code` / `OpenCode` 适配器后，应该怎么安装和使用

先把最重要的话说清楚：

**当前仓库已经有设计文档，但还没有把三端都可安装的 harness adapter 全部实现出来。**

所以你现在能“安装”的，主要还是：

- 阅读和复用设计
- 复用现有 OpenCode 风格 skill 资产

而你真正想要的那套：

- `Codex skill`
- `Claude plugin`
- `OpenCode adapter`

是下一阶段要按设计文档实现的内容。

---

## 2. 这个“技能”本质上是什么

它不是一个单独的大 prompt。

它的本质是三层东西：

1. **共享核心内容**
   - harness 原则
   - 角色定义
   - workflow
   - `.ai/` 项目模板
   - verify / evals / profiles

2. **平台适配层**
   - Codex 适配
   - Claude Code 适配
   - OpenCode 适配

3. **项目内落地层**
   - `AGENTS.md`
   - `CLAUDE.md`
   - `.ai/`

安装 skill / plugin 的最终目的，不是为了“多一个命令”，而是为了让 AI 进入仓库后：

- 先识别项目
- 再初始化规则和状态
- 再按 workflow 推进
- 最后按验证证据决定是否完成

---

## 3. 当前仓库里已经有什么

当前仓库已经有：

- `docs/personal-ai-harness-framework-design.md`
- `docs/personal-harness-skill-delivery-plan.md`
- 现有 OpenCode 风格 skill 资产：
  - `.agents/skills/content-builder/SKILL.md`
  - `package.json` 中的 `opencode.skills`

当前仓库还没有完整落地的内容：

- `core/`
- `adapters/codex-skill/`
- `adapters/claude-plugin/`
- `adapters/opencode/`
- `scripts/sync-core-to-adapters.*`

所以这份说明里，“安装”要分：

- 当前阶段安装/使用
- 目标阶段安装/使用

---

## 4. 当前阶段怎么使用

## 4.1 如果你的目标是“理解这套 harness”

按这个顺序阅读：

1. `docs/personal-ai-harness-framework-design.md`
2. `docs/personal-harness-skill-delivery-plan.md`
3. 当前项目里你自己的 `AGENTS.md` / `CLAUDE.md` / `.ai/` 试落一版

## 4.2 如果你的目标是“把它用于真实项目”

当前阶段推荐做法不是直接装 plugin，而是：

1. 选一个真实项目
2. 按设计文档手工落第一版：
   - `AGENTS.md`
   - `CLAUDE.md`
   - `.ai/docs/`
   - `.ai/policies/`
   - `.ai/state/`
   - `.ai/verify/`
3. 把两条硬规则写进去：
   - 未经验证不能说完成
   - 一次只做一个 feature
4. 用这个框架先跑一轮真实需求

这是最稳的路径，因为当前阶段真正成熟的是“方法论”，不是“打包产物”。

---

## 5. 目标阶段的安装方式

等这个仓库按交付方案实现完之后，建议按三端分别安装。

## 5.1 Codex

### 目标产物

- `adapters/codex-skill/personal-harness/`
- 可选：`adapters/codex-plugin/personal-harness-plugin/`

### 安装思路

#### Skill 版

把 `personal-harness/` 放到本机 Codex skills 目录中，例如：

```text
~/.codex/skills/personal-harness/
```

至少包含：

- `SKILL.md`
- `agents/openai.yaml`
- `references/`
- `assets/project-ai-framework/`

#### Plugin 版

把 plugin 放到本机 plugins 目录，并保证含有：

```text
.codex-plugin/plugin.json
```

如果走个人 marketplace，还要把 plugin 条目加入 marketplace 配置。

### 装完后怎么用

典型用法应该是：

1. 在目标项目中触发 `personal-harness`
2. 它先识别仓库是否已有 `.ai/`
3. 如果没有，就初始化：
   - `AGENTS.md`
   - `CLAUDE.md`
   - `.ai/`
4. 然后进入标准工作流：
   - profile 识别
   - active task 检查
   - DoD 检查
   - verify 入口

### 成功标准

- Skill 能被识别
- 能初始化 `.ai/`
- 能把任务推进约束到 WIP=1
- 能把完成判定约束到验证证据

---

## 5.2 Claude Code

### 目标产物

- `adapters/claude-plugin/plugins/personal-harness-plugin/`
- `adapters/claude-plugin/.claude-plugin/marketplace.json`

### 安装思路

用 Claude Code plugin / marketplace 方式安装。

目标 plugin 目录中至少应包含：

- `.claude-plugin/plugin.json`
- `skills/personal-harness/SKILL.md`
- `agents/*.md`
- `hooks/hooks.json`
- `assets/project-ai-framework/`

### 装完后怎么用

典型用法应该是：

1. 在 Claude Code 中安装 personal harness plugin
2. 在项目里触发 harness skill
3. 根据需要调用子智能体：
   - `planner`
   - `implementer`
   - `reviewer`
   - `verifier`
4. hooks 在关键节点做约束：
   - 修改后提醒同步 state
   - 声称完成前检查证据
   - 高风险操作前触发保护

### 成功标准

- plugin 可加载
- skill 可触发
- subagents 可见
- hooks 生效
- 模板可被用来初始化项目

---

## 5.3 OpenCode

### 目标产物

- `adapters/opencode/`

其中优先包含：

- `.opencode/skills/personal-harness/SKILL.md`
- `.opencode/agents/*.md`
- `.opencode/commands/*.md`
- 可选：`.opencode/plugins/harness-guard.ts`
- `AGENTS.md`

兼容层可保留：

- `.agents/skills/personal-harness/SKILL.md`

### 安装思路

如果是本地仓库型使用，通常是：

1. 把 adapter 内容放进目标仓库或工具可识别位置
2. 确保 `AGENTS.md` 和 `opencode.json` / `.opencode/` 配置可被读取
3. 如有 plugin，再按 OpenCode 的 plugin 机制加载

### 装完后怎么用

典型用法应该是：

1. 进入项目
2. 让 OpenCode 读取 `AGENTS.md`
3. 通过 skill 或 commands 触发：
   - 初始化 harness
   - 验证 active feature
   - 生成 handoff
4. 需要多角色时调用 `.opencode/agents/*.md`

### 成功标准

- rules 被读取
- skill 被识别
- commands 可触发
- agents 可调用
- 如实现 plugin，plugin 可加载

---

## 6. 安装完成后该怎么用

无论三端哪一种，真正推荐的使用方式都一样。

## 6.1 第一次进入一个项目

先做三件事：

1. 识别项目栈
   - LangGraph / LangChain
   - Django / Spring Boot
   - React / Vue
   - Docker / K8S / Jenkins

2. 确认 profile
   - `langgraph-django-react`
   - `langgraph-springboot-vue`
   - 或其他自定义 profile

3. 初始化项目内框架
   - `AGENTS.md`
   - `CLAUDE.md`
   - `.ai/`

## 6.2 开始做一个 feature

标准动作应该是：

1. 读取 `active-task.md`
2. 读取 `feature-list.json`
3. 确认当前只有一个 active feature
4. 读取 `definition-of-done.md`
5. 进入 workflow：
   - `planner -> implementer -> reviewer -> verifier`

## 6.3 做完后怎么判定是否完成

不能只看“代码写完了”。

至少要检查：

- 本地可运行
- 前后端联调通过
- agent-flow 验证通过
- 关键日志正常
- `state` 工件已更新

只有这些满足，才允许把状态推进到 `verified` 或“完成”。

---

## 7. 最常见误用

### 误用 1

把 harness 当成“大 prompt 模板”。

问题：

- 没有状态
- 没有验证
- 没有任务边界
- 没有角色约束

### 误用 2

刚装上 skill 就让 AI 自由写代码。

问题：

- 还没有 `.ai/`
- 还没有 DoD
- 还没有 active task
- 还没有 verify 路径

### 误用 3

把“实现完成”当成“任务完成”。

这直接违反这套 harness 的核心原则：

- 未经验证不能说完成

---

## 8. 最推荐的落地方式

如果你问“安装后怎么用最合理”，我的建议是：

1. 先不要追求三端都全自动
2. 先选一个真实项目
3. 用这套方法把 `.ai/` 框架立起来
4. 先跑一轮真实需求
5. 再把共用内容沉淀进 `core/`
6. 再生成 Codex / Claude / OpenCode 适配器

也就是说：

**先用真实项目验证 harness，再把它打包成 skill / plugin。**

这是最稳的做法。

---

## 9. 本仓库接下来最值得做的事

如果要把这份说明真正变成“可安装”，下一步最值得做的是：

1. 建 `core/`
2. 建 `adapters/codex-skill/`
3. 建 `adapters/claude-plugin/`
4. 建 `adapters/opencode/`
5. 建 `scripts/sync-core-to-adapters.*`

做到这一步，这份说明里的安装步骤就会从“目标方案”变成“真实可执行步骤”。

