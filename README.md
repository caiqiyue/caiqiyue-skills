# caiqiyue-skills

个人 AI engineering skills 仓库，目标不是堆很多 prompt，而是沉淀一套可复用的 AI 编程治理体系，逐步支持：

- `Codex`
- `Claude Code`
- `OpenCode`

当前仓库已经包含两份核心设计文档，以及三端适配中的第一批真实 skill / plugin 入口。

核心设计文档：

- [docs/personal-ai-harness-framework-design.md](docs/personal-ai-harness-framework-design.md)
- [docs/personal-harness-skill-delivery-plan.md](docs/personal-harness-skill-delivery-plan.md)

它们分别回答：

- 个人 harness 框架本体应该怎么设计
- 这套框架如何做成可分发、可安装、可维护的跨平台 skill / plugin / adapter

## 当前状态

当前仓库已经进入 **设计 + 第一版实现** 阶段，已经具备三端真实入口，但还不是完全成熟的三端成品。

也就是说：

- 设计文档已经到位
- `Codex skill` MVP 已经落地
- `Claude Code plugin` MVP 已经落地
- `OpenCode adapter` MVP 已经落地
- OpenCode 风格的现有 skill 资产还在
- 三端适配已经都有入口，但细分 profile 和同步脚本还没补齐

当前已经可直接查看和复用的真实产物：

- [core/harness-spec](core/harness-spec)
- [core/templates/project-ai-framework](core/templates/project-ai-framework)
- [adapters/codex-skill/personal-harness](adapters/codex-skill/personal-harness)
- [adapters/codex-skill/work-doc-editor](adapters/codex-skill/work-doc-editor)
- [adapters/claude-plugin/personal-harness-plugin](adapters/claude-plugin/personal-harness-plugin)
- [adapters/opencode](adapters/opencode)

这很重要，因为安装和使用方式要分两种情况看：

1. **当前仓库怎么使用**
2. **下一阶段 harness adapter 实现后怎么安装和使用**

## 当前仓库怎么用

如果你现在要理解这套个人 harness，建议按这个顺序读：

1. 先读 [docs/personal-ai-harness-framework-design.md](docs/personal-ai-harness-framework-design.md)  
   理解 `.ai/` 项目框架、角色分工、验证门、workflow。

2. 再读 [docs/personal-harness-skill-delivery-plan.md](docs/personal-harness-skill-delivery-plan.md)  
   理解为什么必须做 `core + adapters + scripts`，以及三端分别怎么适配。

3. 然后读 [adapters/codex-skill/personal-harness/SKILL.md](adapters/codex-skill/personal-harness/SKILL.md)  
   这是第一版真实 `Codex skill`。

4. 再看 [adapters/claude-plugin/personal-harness-plugin](adapters/claude-plugin/personal-harness-plugin) 和 [adapters/opencode](adapters/opencode)  
   这是 `Claude Code` 和 `OpenCode` 的第一版真实 adapter。

5. 最后读 [docs/skill-installation-and-usage.md](docs/skill-installation-and-usage.md)  
   看当前已实现的安装/使用方式，以及后续三端完整落地后的路径。

## 计划中的仓库形态

后续这个仓库会逐步演进成下面的结构：

```text
caiqiyue-skills/
├─ docs/
├─ core/
├─ adapters/
│  ├─ codex-skill/
│  ├─ codex-plugin/
│  ├─ claude-plugin/
│  └─ opencode/
└─ scripts/
```

含义是：

- `core/`：唯一事实源，放规则、模板、workflow、verify、profiles
- `adapters/`：三端各自可安装的真实产物
- `scripts/`：把 core 同步/生成到各 adapter，避免三套内容漂移

## 这套 harness 最核心的两条规则

- 未经验证不能说完成
- 一次只做一个 feature，没验证完不能开下一个

## 下一步建议

如果你要继续推进这个仓库，推荐顺序是：

1. 在真实项目里分别试跑 `Codex` / `Claude Code` / `OpenCode` 的当前入口
2. 把细分 profile 从通用版补成 `langgraph-django-react` / `springboot-vue`
3. 加上跨端安装验证脚本或手册
4. 最后补 `scripts/sync-core-to-adapters.*`

更细的安装和使用说明见：

- [docs/skill-installation-and-usage.md](docs/skill-installation-and-usage.md)
