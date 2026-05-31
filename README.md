# caiqiyue-skills

个人 AI engineering skills 仓库，目标不是堆很多 prompt，而是沉淀一套可复用的 AI 编程治理体系，逐步支持：

- `Codex`
- `Claude Code`
- `OpenCode`

当前仓库已经包含两份核心设计文档：

- [docs/personal-ai-harness-framework-design.md](docs/personal-ai-harness-framework-design.md)
- [docs/personal-harness-skill-delivery-plan.md](docs/personal-harness-skill-delivery-plan.md)

它们分别回答：

- 个人 harness 框架本体应该怎么设计
- 这套框架如何做成可分发、可安装、可维护的跨平台 skill / plugin / adapter

## 当前状态

当前仓库是 **设计与方案阶段**，不是完整的三端可安装成品。

也就是说：

- 设计文档已经到位
- OpenCode 风格的现有 skill 资产还在
- `Codex` / `Claude Code` / `OpenCode` 三端统一的 harness adapter 还没有全部实现

这很重要，因为安装和使用方式要分两种情况看：

1. **当前仓库怎么使用**
2. **下一阶段 harness adapter 实现后怎么安装和使用**

## 当前仓库怎么用

如果你现在要理解这套个人 harness，建议按这个顺序读：

1. 先读 [docs/personal-ai-harness-framework-design.md](docs/personal-ai-harness-framework-design.md)  
   理解 `.ai/` 项目框架、角色分工、验证门、workflow。

2. 再读 [docs/personal-harness-skill-delivery-plan.md](docs/personal-harness-skill-delivery-plan.md)  
   理解为什么必须做 `core + adapters + scripts`，以及三端分别怎么适配。

3. 最后读 [docs/skill-installation-and-usage.md](docs/skill-installation-and-usage.md)  
   看当前阶段怎么理解安装/使用，和后续正式落地后的安装路径。

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

1. 先把 `core/` 和项目模板落地
2. 先做 `Codex skill` 的第一版
3. 再做 `Claude plugin`，把 subagents + hooks 加进去
4. 最后做 `OpenCode adapter`

更细的安装和使用说明见：

- [docs/skill-installation-and-usage.md](docs/skill-installation-and-usage.md)

