---
name: content-builder
description: 基于多智能体协作的学习内容构建系统。通过阶段式智能体工作流，将任意技术主题拆解为企业级知识框架，并生成配套的教学文档、代码示例和实验内容。适用场景：大模型微调、强化学习、RAG，或任何需要系统性学习内容的技术主题。
version: 1.1.0
user-invocable: true
---

# 内容构建技能 (Content Builder Skill)

## 概述

一个基于多智能体协作的学习内容构建系统。通过阶段式智能体工作流，将任意技术主题拆解为企业级知识框架，并生成配套的教学文档、代码示例和实验内容。

**适用场景：** 大模型微调、强化学习、RAG，或任何需要系统性学习内容的技术主题

**核心价值：**
- 企业级知识框架设计
- 初学者友好的教学内容生成
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
│  阶段 9: 项目结构        生成课程目录 + raw-material + .gitignore           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 阶段详细说明

### 阶段 1: 需求解析

**输入参数（从用户获取）：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `topic` | 学习主题 | "RAG检索增强生成" |
| `audience` | 目标受众 | "初学者" |
| `level` | 深度级别 | "企业级快速入门" |
| `duration` | 学习时长（可选） | "2周" |
| `tech_stack` | 技术栈偏好（可选） | "Python, LangChain" |
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
1. 将 `knowledge_framework` 序列化为 JSON 写入 `{course_name}/KNOWLEDGE_FRAMEWORK.json`
2. 将知识框架内容追加写入 `{course_name}/README.md`

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
      content_file: "lessons/01-xxx-slug/content.md",
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
1. 将 `content_structure` 序列化为 JSON 写入 `{course_name}/CONTENT_STRUCTURE.json`
2. 将内容结构追加写入 `{course_name}/README.md`

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
  failed_items: string[],
  final_verdict: "approved" | "needs_revision"
}
```

---

### 阶段 9: 项目结构处理

**执行者：** 主智能体

**职责：**
1. 将所有原始学习资料移动到 `{course_name}/raw-material/` 文件夹
2. 生成 `.gitignore` 文件到课程根目录
3. 整理目录结构，确保符合输出规范

**输出文件：**
- `{course_name}/raw-material/` 文件夹（包含所有原始资料）
- `{course_name}/.gitignore` 文件

**持久化：**
- 将阶段 9 的处理结果追加写入 `{course_name}/README.md`

---

## 输出目录结构

构建完成后，最终目录结构如下（与 rag-learning 项目结构一致）：

```
{project_root}/
│
├── {course_name}/                  # 🎓 课程根目录（与项目名同名）
│   ├── README.md                   # 课程入口文档
│   ├── COURSE_META.json           # 课程元信息（自动生成）
│   ├── KNOWLEDGE_FRAMEWORK.json    # 知识框架JSON
│   ├── CONTENT_STRUCTURE.json      # 内容结构JSON
│   │
│   ├── lessons/                    # 📚 课程内容
│   │   ├── 01-xxx-slug/           # 第1节
│   │   │   └── content.md        # 教学内容（唯一文件）
│   │   ├── 02-xxx-slug/           # 第2节
│   │   │   └── content.md
│   │   ├── 03-xxx-slug/           # 第3节（代码课）
│   │   │   ├── content.md
│   │   │   └── code/              # 代码目录（仅代码课时有）
│   │   │       ├── example_1.py
│   │   │       └── README.md
│   │   └── ...
│   │
│   ├── assets/                    # 🎨 资源文件
│   │   ├── diagrams/              # 架构图/流程图
│   │   └── images/               # 图片资源
│   │
│   └── raw-material/              # 📚 原始资料（不进行 Git 跟踪）
│       ├── source_1.pdf
│       ├── source_2.md
│       └── ...
│
├── .gitignore                      # Git 忽略规则
├── .claude/                        # Claude Code 配置（可选）
│   └── skills/
│       └── content-builder/        # 内容构建技能
│
└── README.md                      # 项目入口（父级README）
```

**目录命名规范：**
- 课程根目录：`{course_name}/`，如"RAG实战课程/"
- 课时目录：`{module:02}-{title-slug}/`，如"01-rag-basics-why-retrieval-augmentation"
- 代码目录：仅在代码课时存在 `code/` 子目录

---

## .gitignore 内容

在项目根目录创建 `.gitignore`，包含以下规则：

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# IDE
.idea/
.vscode/
*.swp
*.swo

# pyenv
.python-version

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Jupyter Notebook
.ipynb_checkpoints

# mypy
.mypy_cache/

# Ruff
.ruff_cache/

# Vector store / embeddings（根据课程类型调整）
vector_store/
chromadb/
pinecone_data/
milvus_data/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# 原始资料（不跟踪）
raw-material/**/
!raw-material/.gitkeep

# 压缩包
*.zip
*.7z
*.tar.gz
```

---

## README.md 结构

项目根目录的 `README.md` 是项目入口文档：

```markdown
# {项目名称}

基于多智能体协作的 {主题} 学习内容构建系统。

---

## 项目结构

```
{project_name}/
│
├── {course_name}/                 # 🎓 课程根目录
│   ├── README.md                  # 课程详情
│   ├── COURSE_META.json          # 课程元信息
│   ├── KNOWLEDGE_FRAMEWORK.json  # 知识框架
│   ├── CONTENT_STRUCTURE.json    # 内容结构
│   ├── lessons/                   # 课程节次
│   │   ├── 01-xxx/content.md
│   │   └── ...
│   ├── assets/                    # 资源文件
│   │   ├── diagrams/
│   │   └── images/
│   └── raw-material/             # 原始资料
│
├── .gitignore                     # Git 忽略规则
├── .claude/                      # Claude Code 配置
│   └── skills/
│       └── content-builder/       # 内容构建技能
│
└── README.md                     # 本文件
```

---

## 目录说明

### {course_name}/

基于原始课件构建的企业级学习内容，包含：

| 课程 | 主题 | 内容 |
|------|------|------|
| 01   | ...  | ... |
| 02   | ...  | ... |

### raw-material/

原始学习资料（原始课件、notebook、压缩包），**已配置不进行 Git 跟踪**。

### .claude/skills/content-builder/

内容构建技能（Skill），用于自动化构建学习内容。

---

## .gitignore 说明

本项目配置的 `.gitignore` 会忽略以下文件：

| 类型 | 规则 | 原因 |
|------|------|------|
| 压缩包 | `*.zip`, `*.7z`, `*.tar.gz` 等 | 无法直接在 Git 查看 |
| Claude 配置 | `.claude/` | 工作区特定配置 |
| 缓存 | `__pycache__/`, `.ruff_cache/` | 可随时重新生成 |
| Python | `*.pyc`, `venv/`, `*.so` | 构建产物 |
| IDE | `.vscode/`, `.idea/` | 个人配置 |
| 系统文件 | `.DS_Store`, `Thumbs.db` | 操作系统文件 |

---

## 构建状态

| 模块 | 状态 |
|------|------|
| 需求解析 | ✅ 完成 |
| 资料收集 | ✅ 完成 |
| 知识框架设计 | ✅ 完成 |
| 内容结构规划 | ✅ 完成 |
| 框架审核 | ✅ 完成 |
| 任务拆分 | ✅ 完成 |
| 并行构建 | ✅ 完成 |
| 最终审核 | ✅ 完成 |
| 项目结构 | ✅ 完成 |

---

## 技术栈

| 领域 | 技术 |
|------|------|
| 学习内容构建 | Claude Code + Multi-Agent |
| 语言 | Python |

---

## 许可

MIT License
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
7. **最终必须创建 .gitignore**：阶段8审核完成后、阶段9开始时，必须在项目根目录创建符合规范的 .gitignore 文件

---

## 调用方式

```bash
# 基本调用
/skill content-builder "RAG检索增强生成"

# 带参数调用
/skill content-builder "RAG检索增强生成" \
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
4. **目录结构**：最终输出必须符合"输出目录结构"章节规定的格式