---
name: content-builder
description: 基于多智能体协作的学习内容构建系统。通过阶段式智能体工作流，将任意技术主题拆解为企业级知识框架，并生成配套的教学文档、代码示例和实验内容。适用场景：大模型微调、强化学习，或任何需要系统性学习内容的技术主题。
version: 1.0.0
user-invocable: true
---

# 内容构建技能 (Content Builder Skill)

## 概述

一个基于多智能体协作的学习内容构建系统。通过阶段式智能体工作流，将任意技术主题拆解为企业级知识框架，并生成配套的教学文档、代码示例和实验内容。

**适用场景：** 大模型微调、强化学习，或任何需要系统性学习内容的技术主题

**核心价值：**
- 企业级知识框架设计
- 初学者友好的教学内容的生成
- 代码案例 + 文档的双轨输出
- 自动化质量审核与修复

---

## 工作流总览

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           内容构建流程 (9 阶段)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  阶段 1: 需求解析        用户输入 → 主题/受众/时长/技术栈                    │
│       ↓                                                                     │
│  阶段 2: 资料收集        子智能体A: 读取原始资料 + 联网搜索                   │
│       ↓                                                                     │
│  阶段 3: 框架设计        子智能体B: 设计企业级知识框架                       │
│       ↓                                                                     │
│  阶段 4: 结构规划        子智能体C: 划分课程结构 + 知识点清单               │
│       ↓                                                                     │
│  阶段 5: 框架审核        子智能体D: 审核框架 + 内容结构                      │
│       ↓                                                                     │
│  阶段 6: 任务拆分        子智能体E: 制定构建计划 + 任务分配                  │
│       ↓                                                                     │
│  阶段 7: 并行构建  ←→  滚动窗口式并行（窗口=2），6个子智能体同时工作         │
│       ↓                                                                     │
│  阶段 8: 最终审核        子智能体F + G: 交叉审核 + 修复                      │
│       ↓                                                                     │
│  阶段 9: 项目结构        生成raw-material/ + .gitignore                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 阶段详细说明

### 阶段 1: 需求解析

**输入参数（从用户获取）：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `topic` | 学习主题 | "大模型微调 + 强化学习" |
| `audience` | 目标受众 | "初学者" |
| `level` | 深度级别 | "企业级快速入门" |
| `duration` | 学习时长（可选） | "2周" |
| `tech_stack` | 技术栈偏好（可选） | "Python, PyTorch" |
| `source_materials` | 原始资料（可选） | 文档路径/URL列表 |

**输出：**
```
parsed_requirements = {
  topic: string,
  audience: "初学者" | "进阶" | "专家",
  level: "入门" | "进阶" | "企业级",
  duration: string | null,
  tech_stack: string[],
  source_materials: string[]
}
```

**持久化：** 将需求解析结果追加写入 `README.md` 的 `## 需求解析` 章节

---

### 阶段 2: 资料收集

**执行者：** 子智能体 A（Reader Agent）

**职责：**
1. 读取用户提供的原始资料（PDF/MD/TXT/URL）
2. 联网搜索主题相关的知识点和信息（适度，不深入）
3. 整理提炼核心概念、技术要点、关键词汇

**输出：**
```
collected_materials = {
  core_concepts: string[],        // 核心概念列表
  key_technologies: string[],     // 关键技术列表
  important_terms: string[],     // 重要术语表
  raw_notes: string,              // 原始资料笔记
  web_notes: string,              // 联网搜索笔记
  references: string[]           // 参考资料链接
}
```

**持久化：** 将收集的资料笔记追加写入 `README.md` 的 `## 原始资料整理` 章节

---

### 阶段 3: 知识框架设计

**执行者：** 子智能体 B（Framework Designer Agent）

**职责：**
1. 基于 `collected_materials` 设计企业级知识框架
2. 框架要覆盖该主题的核心知识点
3. 框架要向企业级对齐，包含实际应用场景
4. 框架要分层次（基础 → 进阶 → 高级）

**输出：**
```
knowledge_framework = {
  framework_name: string,
  description: string,
  target_audience: string,
  prerequisites: string[],
  levels: [
    {
      level_name: "基础",
      modules: [
        {
          module_name: string,
          description: string,
          learning_objectives: string[],
          estimated_duration: string
        }
      ]
    },
    // ... 进阶、高级
  ],
  total_modules: number,
  total_duration: string
}
```

**持久化：**
1. 将 `knowledge_framework` 序列化为 JSON 写入 `KNOWLEDGE_FRAMEWORK.json`
2. 将知识框架内容追加写入 `README.md` 的 `## 知识框架` 章节（包含完整层级结构、模块描述、学习目标）

---

### 阶段 4: 内容结构规划

**执行者：** 子智能体 C（Content Planner Agent）

**职责：**
1. 基于 `knowledge_framework` 划分课程结构
2. 设计每节课的：
   - 标题
   - 核心知识点（3-5个）
   - 教学目标
   - 配套文档（`content.md`）
   - 代码案例列表（可能多个）
3. 确定代码案例的语言类型

**输出：**
```
content_structure = {
  course_name: string,
  total_lessons: number,
  lessons: [
    {
      lesson_id: "01",
      title: string,
      core_knowledge_points: string[],
      teaching_objectives: string[],
      content_file: "lessons/01-title/content.md",
      code_examples: [
        {
          filename: string,
          language: "python" | "java" | "javascript" | "typescript" | "go",
          description: string
        }
      ]
    }
  ]
}
```

**持久化：**
1. 将 `content_structure` 序列化为 JSON 写入 `content_structure.json`
2. 将内容结构追加写入 `README.md` 的 `## 内容结构设计` 章节（包含每节课ID、标题、核心知识点、配套文件列表）

---

### 阶段 5: 框架与结构审核

**执行者：** 子智能体 D（Reviewer Agent）

**职责：**
1. 审核知识框架：
   - 覆盖面是否完整
   - 层次划分是否合理
   - 是否符合企业级标准
2. 审核内容结构：
   - 课程划分是否合理
   - 知识点是否遗漏
   - 内容顺序是否逻辑连贯
3. 提出修改建议或直接修复

**输出：**
```
review_result = {
  framework_approved: boolean,
  structure_approved: boolean,
  framework_issues: string[],
  structure_issues: string[],
  framework_fixes: string[],
  structure_fixes: string[]
}
```

---

### 阶段 6: 任务拆分与规划

**执行者：** 子智能体 E（Planner Agent）

**职责：**
1. 将内容结构拆分为独立任务（每节课作为一个任务）
2. 分配任务执行顺序（可并行的任务分组）
3. 确定每个任务的执行智能体配置

**输出：**
```
build_plan = {
  total_tasks: number,
  task_groups: [  // 可并行的任务组
    ["lesson_01", "lesson_02"],  // 组内可并行
    ["lesson_03", "lesson_04"],
    // ...
  ],
  task_details: [
    {
      task_id: "lesson_01",
      title: string,
      assigned_agents: {
        reader: "Agent_A1",
        writer: "Agent_A2",
        reviewer: "Agent_A3"
      },
      status: "pending"
    }
  ]
}
```

---

### 阶段 7: 并行内容构建

**执行方式：** 滚动窗口式并行，最多 2 个任务同时执行（6 个子智能体），一个任务完成后立即关闭其 3 个子智能体并启动新任务

**并行策略：**
```
任务池: [lesson_01, lesson_02, lesson_03, lesson_04, ...]
          ↑
      窗口大小=2，同时最多2个任务

  时间线 ──────────────────────────────────────────────────────→

  [Task1(R+W+C)] [Task2(R+W+C)] 
       ↓              ↓
  任务1完成 → 关闭Task1的3个智能体 → 启动Task3
       ↓              ↓
  [Task1(R+W+C)] [Task2(R+W+C)]   ← Task2 还在执行
                    ↓
               任务2完成 → 关闭Task2的3个智能体 → 启动Task4
                    ↓
  [Task3(R+W+C)] [Task2(R+W+C)]   ← Task2 还在执行，Task3 替代Task1
                         ↓
                    任务2完成 → 关闭Task2的3个智能体 → 启动Task4
                         ↓
  [Task3(R+W+C)] [Task4(R+W+C)]   ← Task3 和 Task4 并行
       ...以此类推...
```

**每组 3 个子智能体职责：**

| 智能体 | 职责 | 输入 | 输出 |
|--------|------|------|------|
| 子智能体 R (Reader) | 读取/搜索资料 | 任务ID、知识点 | 相关资料笔记 |
| 子智能体 W (Writer) | 编写教学内容 | 资料笔记 + 知识点 | content.md + 代码案例 |
| 子智能体 C (Checker) | 审核内容 | 编写的内容 | 审核报告 + 修复意见 |

**执行流程（每组）：**
```
Reader(R) ──→ Writer(W) ──→ Checker(C)
   ↓              ↓             ↓
获取资料    编写内容      审核内容
   │              │             │
   └──→ 传递给 W ──┴──→ 传递给 C ─┘
                          │
                          ↓ (有问题的修复循环)
                     最多 3 次修复
                          │
                          ↓ (仍失败则列入失败清单)
                     标记为 failed
                         │
                         ↓ (通知主智能体)
                   主智能体分配新任务
                   关闭当前3个智能体
```

**内容编写要求：**

1. **content.md 文档：**
   - 知识点要讲清楚（专业角度）
   - 用通俗易懂的表达方式
   - 包含生活化例子
   - 结构清晰（引言/正文/总结）
   - 关键概念用加粗/高亮

2. **代码案例：**
   - 详细的中文注释解释每一行代码
   - 代码要完整可运行
   - 注释要解释"为什么这样做"
   - 多个代码案例分散到不同文件

---

### 阶段 8: 最终审核

**执行者：** 子智能体 F + G（交叉审核）

**职责：**
1. 全面审核所有构建内容
2. 检查内容正确性、完整性、一致性
3. 检查代码可运行性
4. 发现问题交给对方修复

**输出：**
```
final_review = {
  all_content_verified: boolean,
  issues_found: [
    {
      file: string,
      issue_type: "content" | "code" | "structure",
      description: string,
      severity: "high" | "medium" | "low",
      assigned_to: "Agent_F" | "Agent_G"
    }
  ],
  fixes_applied: string[],
  failed_items: string[],  // 修复3次仍失败的任务列表
  final_verdict: "approved" | "needs_revision"
}
```

---

### 阶段 9: 项目结构处理

**执行者：** 主智能体（或阶段 8 审核后自动执行）

**职责：**
1. 将所有原始学习资料移动到 `raw-material/` 文件夹
2. 生成 `.gitignore` 文件（包含压缩包、临时文件、操作系统文件等）
3. 整理目录结构，确保符合输出规范

**输出文件：**
- `raw-material/` 文件夹（包含所有原始资料）
- `.gitignore` 文件

**持久化：**
- 将阶段 9 的处理结果追加写入 `README.md` 的 `## 项目结构` 章节

---

## 输出目录结构

```
output/
└── {course_name}/
    ├── README.md                    # 知识框架 + 内容结构总览
    ├── COURSE_META.json              # 课程元信息
    ├── KNOWLEDGE_FRAMEWORK.json      # 知识框架JSON
    ├── content_structure.json        # 内容结构JSON
    ├── .gitignore                    # Git 忽略文件
    ├── raw-material/                 # 原始学习资料（用户提供的）
    │   ├── source_1.pdf
    │   ├── source_2.md
    │   └── ...
    ├── lessons/
    │   ├── 01-{lesson_slug}/
    │   │   ├── content.md           # 教学内容
    │   │   ├── overview.md          # 本节概述
    │   │   └── code/
    │   │       ├── example_1.py     # 代码案例1
    │   │       ├── example_2.js     # 代码案例2
    │   │       └── README.md        # 代码说明
    │   ├── 02-{lesson_slug}/
    │   │   └── ...
    └── assets/
        ├── diagrams/                # 架构图/流程图
        └── images/
```

### .gitignore 内容

```
# 压缩包
*.zip
*.rar
*.7z
*.tar
*.gz

# 临时文件
*.tmp
*.temp
*.swp
*~

# 操作系统
.DS_Store
Thumbs.db

# 依赖目录
node_modules/
__pycache__/
*.pyc
*.pyo

# 构建产物
dist/
build/
*.class
*.o
*.so

# 日志
*.log

# IDE
.vscode/
.idea/
*.iml

# 其他
*.pdf
!raw-material/*.pdf
```

### README.md 结构

`README.md` 是整个课程的知识框架 + 内容结构总览文档，包含以下章节：

```markdown
# {课程名称}

## 需求解析
- 主题：...
- 受众：...
- 级别：...

## 原始资料整理
### 核心概念
### 关键技术
### 术语表
### 参考资料

## 知识框架
### 框架概述
### 基础阶段
- 模块 1.1: ...
- 模块 1.2: ...
### 进阶阶段
### 高级阶段
### 学习路径

## 内容结构设计
### 课程列表
| 课ID | 标题 | 核心知识点 | 配套文件 |
|------|------|-----------|---------|
| 01   | ...  | ...       | content.md, code/*.py |

### 详细内容
（每节课的详细内容链接）

## 构建状态
- [x] 阶段1: 需求解析
- [x] 阶段2: 资料收集
- [x] 阶段3: 框架设计
- [x] 阶段4: 结构规划
- [x] 阶段5: 框架审核
- [ ] 阶段6: 任务拆分
- [ ] 阶段7: 并行构建
- [ ] 阶段8: 最终审核
- [ ] 阶段9: 项目结构

## 项目结构
（阶段9完成后生成）

## 失败任务清单
（构建失败的课程列表）
```

---

## 质量标准

### 内容质量
- [ ] 知识点覆盖完整，无遗漏
- [ ] 表述专业且通俗易懂
- [ ] 例子生活化，易于理解
- [ ] 结构清晰，层次分明

### 代码质量
- [ ] 代码完整可运行
- [ ] 中文注释详细，解释"为什么"
- [ ] 代码风格规范
- [ ] 多个案例分散不集中

### 审核标准
- [ ] 知识框架审核通过
- [ ] 内容结构审核通过
- [ ] 每节课内容审核通过
- [ ] 最终交叉审核通过

---

## 关键约束

1. **原始资料仅作借鉴**：内容不需要和原始资料保持一致，可以自由发挥
2. **联网搜索适度**：主要用于补充知识点，不需要深入研究
3. **修复循环限制**：每个 Checker 最多触发 3 次修复，仍失败则列入失败清单
4. **多文件分散**：不要把所有内容放在同一个文件
5. **代码语言混合**：同节课允许混合 Python/Java/JavaScript/TypeScript/Go 等
6. **全自动执行**：所有阶段全自动执行，无需用户确认（除非主动暂停）

---

## 调用方式

```bash
# 基本调用
/skill content-builder "大模型微调 + 强化学习"

# 带参数调用
/skill content-builder "大模型微调 + 强化学习" \
  --audience "初学者" \
  --level "企业级" \
  --duration "2周" \
  --source "./my-notes.md"
```

---

## 注意事项

1. **执行模式**：此 Skill 需要多智能体环境支持，确保子智能体调度系统可用
2. **进度追踪**：每个阶段完成后输出状态报告
3. **错误处理**：某节课构建失败不影响其他课程继续执行，构建失败的课程列入 `failed_items` 清单供后续处理