---
name: project-wiki
version: 3.4.0
description: 智能项目知识助手，自动分析项目、智能推荐文档、渐进式知识搜索，强调数据流动与状态管理
---

# ProjectWiki - 智能项目知识助手

ProjectWiki 是一个智能项目知识助手，从静态文档管理升级为动态智能交互系统。通过自然语言问答、意图识别、上下文感知，结合项目信息提供精准答案。**支持智能自动分析、渐进式文档生成、角色视图推荐、知识自动补充**。

---

## 核心价值

> **让文档生成自动化、智能化、个性化**

- **自动分析**：智能识别项目类型、技术栈和复杂度
- **智能推荐**：自动推荐文档类型、模板和角色视图
- **渐进生成**：从功能到架构的完整文档链
- **知识补全**：自动搜索并补充技术栈知识
- **角色适配**：为不同角色提供专门的文档和视图

---

## 智能工作流程

```mermaid
flowchart LR
    A[项目分析] --> B[智能推荐]
    B --> C[文档生成]
    C --> D[知识补全]
    D --> E[优化迭代]
```

### 三种工作模式

**1. 分析模式**
```bash
python3 scripts/analysis/smart_analyzer.py --path ./your-project
```

**2. 生成模式**
```bash
python3 scripts/generation/generate_doc.py --auto
```

**3. 优化模式**
```bash
python3 scripts/utils/consistency_checker.py --fix
```

---

## 关键特性

### 1. 渐进式文档系统

从功能描述到架构设计的完整文档链，支持自动推断和数据一致性设计。

```
功能文档 → 需求文档 → 架构文档
```

**核心重点**：
- 数据流动（Mermaid 时序图）
- 状态管理（完整的状态机设计）

### 2. 智能推荐引擎

基于项目分析结果，自动推荐最合适的文档类型和模板。

**推荐维度**：
- 项目类型（Django、React、Flutter 等）
- 复杂度（简单、中等、复杂）
- 角色视图（架构师、开发者、测试、运维、产品）

### 3. 渐进式知识搜索

项目级能力，自动搜索并积累不熟悉的技术栈知识。

**知识类型**：库、架构、设计模式、原理、数学公式

### 4. 数据流动设计

强调数据在系统中的流动路径，使用时序图和流程图可视化。

### 5. 状态管理

提供完整的状态机设计框架，强调状态一致性和状态持久化。

---

## 快速开始

### 一键启动

```bash
# 1. 智能分析
python3 scripts/analysis/smart_analyzer.py --path ./your-project

# 2. 自动生成
python3 scripts/generation/generate_doc.py --auto

# 3. 查询知识
python3 scripts/query/query_knowledge.py --query "数据流动设计"
```

---

## 文档规范化

### 核心文档命名

| 文档名 | 用途 | 位置 |
|--------|------|------|
| `TODO.md` | 待办事项 | 项目根目录 |
| `CHANGELOG.md` | 变更日志 | 项目根目录 |
| `ROADMAP.md` | 路线图 | 项目根目录 |
| `ARCHITECTURE.md` | 架构文档 | 项目根目录 |

**命名规范**：
- ✅ 必须使用全大写
- ✅ 必须位于项目根目录
- ✅ 必须使用 `.md` 扩展名

详细规范：[文档命名规范](references/guides/document/naming-conventions.md)

---

## 目录结构

```
project-wiki/
├── SKILL.md                      # 本文件
├── references/
│   ├── core/                     # 核心指南
│   ├── templates/                # ⭐ 文档模板（按类型分类）
│   │   ├── core/                 # 核心文档（TODO、CHANGELOG、ROADMAP、ARCHITECTURE）
│   │   ├── api/                  # API 文档
│   │   ├── architecture/         # 架构文档
│   │   ├── design/               # 设计文档
│   │   ├── functional/           # 功能文档
│   │   ├── requirement/          # 需求文档
│   │   ├── module/               # 模块文档
│   │   ├── service/              # 服务文档
│   │   ├── state/                # 状态文档
│   │   ├── knowledge/            # 知识文档
│   │   ├── wiki/                 # Wiki 文档
│   │   └── changelog/            # 变更日志
│   ├── guides/                   # 指南文档
│   ├── knowledge/                # 知识库
│   └── utils/                    # 工具和可视化
├── scripts/                      # 执行脚本
│   ├── analysis/
│   ├── generation/
│   ├── query/
│   ├── knowledge/
│   ├── structure/
│   └── utils/
└── FEATURE_INDEX.md
```

---

## 资源索引

### 核心脚本

| 脚本 | 功能 |
|------|------|
| [analysis/smart_analyzer.py](scripts/analysis/smart_analyzer.py) | ⭐ 智能分析 |
| [generation/generate_doc.py](scripts/generation/generate_doc.py) | 智能文档生成 |
| [query/query_knowledge.py](scripts/query/query_knowledge.py) | 知识查询 |
| [knowledge/search_knowledge.py](scripts/knowledge/search_knowledge.py) | ⭐ 知识搜索 |
| [knowledge/knowledge_manager.py](scripts/knowledge/knowledge_manager.py) | ⭐ 知识管理器 |

### 参考文档

| 目录 | 内容 |
|------|------|
| [templates/](references/templates/) | ⭐ 所有模板（按类型分类） |
| [guides/document/](references/guides/document/) | 文档指南、命名规范 |
| [knowledge/patterns/](references/knowledge/patterns/) | 23 种设计模式 |
| [knowledge/principles/](references/knowledge/principles/) | SOLID 六大原则 |

---

## 使用技巧

### 1. 从智能分析开始

使用 `smart_analyzer.py` 获取项目分析报告和推荐建议。

### 2. 遵循文档命名规范

使用标准命名确保项目文档的一致性：
- `TODO.md` - 待办事项
- `CHANGELOG.md` - 变更日志
- `ROADMAP.md` - 路线图
- `ARCHITECTURE.md` - 架构文档

### 3. 利用自动生成功能

使用 `--auto` 参数让系统自动选择模板和内容。

### 4. 关注数据流动和状态管理

在架构文档和 API 文档中重点展示数据流动和状态管理。

### 5. 积累知识库

使用知识搜索功能补充技术栈知识，建立项目专属知识库。

---

## 常见问题

**Q: 如何开始使用？**
A: 运行 `python3 scripts/analysis/smart_analyzer.py --path ./your-project`

**Q: 如何生成文档？**
A: 使用 `python3 scripts/generation/generate_doc.py --auto`

**Q: 核心文档如何命名？**
A: 必须使用全大写：`TODO.md`、`CHANGELOG.md`、`ROADMAP.md`、`ARCHITECTURE.md`

**Q: 模板在哪里？**
A: 所有模板在 `references/templates/`，按类型分类

---

## 更新日志

**v2.1 - 模板库优化**
- 重组 templates 目录，按文档类型分类
- 新增 12 个模板分类
- 精简 SKILL.md 到 200 行

**v2.0 - 智能自主性增强**
- 新增智能分析器
- 新增自动推荐功能
- 重组目录结构
- 新增设计原则文档

**v1.0 - 基础版本**
- 项目分析
- 文档生成
- 知识查询
- 角色视图
