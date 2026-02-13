---
name: project-wiki
description: 智能项目知识库构建工具，自动分析代码提取隐性知识，生成结构化文档与架构图谱，支持 13+ 主流框架（React/Vue/Django/Spring Boot 等）
---

# Project Wiki - 项目知识库构建工具

## 📋 目录

- [核心价值](#核心价值)
- [快速开始](#快速开始)
- [操作步骤](#操作步骤)
- [框架支持](#框架支持)
- [资源索引](#资源索引)
- [常见问题](#常见问题)

---

## 核心价值

**与传统文档的区别**：

| 维度 | 传统文档 | 知识库 Wiki |
|------|----------|-------------|
| **更新方式** | 手动维护，易过时 | 代码变更自动增量更新 |
| **组织方式** | 线性目录 | 知识图谱网络 |
| **知识类型** | 显性文档（API/配置） | 显性 + 隐性知识（设计决策/最佳实践） |
| **检索方式** | 文件树浏览 | 多维度标签搜索 + 关联推荐 |

**核心能力**：
- 🏗️ **架构解析**：自动识别项目结构、模块划分、技术栈
- 🧠 **隐性知识挖掘**：提取代码中的设计模式、架构决策、最佳实践
- 🔗 **知识图谱构建**：生成模块/API/概念的关系网络（Mermaid 可视化）
- 📚 **结构化文档生成**：README、API 文档、架构文档自动生成

**适用场景**：
- 新人入职：快速理解项目架构和核心模块
- 代码重构：评估影响范围，识别技术债
- 知识传承：将资深开发者的隐性知识显性化
- 架构评审：可视化展示系统设计

---

## 快速开始

### 最简使用（1 分钟）

```bash
# 1. 分析项目
python3 scripts/analyze_project.py --path ./your-project

# 2. 查看结果
cat project-analysis.json
```

输出示例：
```json
{
  "languages": ["Python", "JavaScript"],
  "frameworks": ["fastapi", "vue"],
  "project_structure": {...}
}
```

### 完整流程（5 分钟）

```bash
# 1. 项目分析
python3 scripts/analyze_project.py --path ./your-project

# 2. 构建知识图谱
python3 scripts/knowledge_graph.py --path ./your-project --format mermaid

# 3. 提取隐性知识
python3 scripts/knowledge_extractor.py --path ./your-project --language python

# 4. 查看结果
# - project-analysis.json: 项目结构分析
# - knowledge-graph.json: 知识图谱数据
# - knowledge-graph.mmd: Mermaid 图表
# - implicit-knowledge.json: 隐性知识提取
```

---

## 操作步骤

### 步骤 1：项目结构分析

**目的**：识别编程语言、框架、构建工具和项目结构

```bash
python3 scripts/analyze_project.py --path ./your-project
```

**输出文件**：`project-analysis.json`

**关键字段**：
- `languages`: 编程语言列表（Python、JavaScript、Java、Go、Rust 等）
- `frameworks`: 框架列表（全小写，与框架指引锚点对应）
- `build_tools`: 构建工具（npm、pip、maven、gradle、cargo 等）
- `project_structure`: 目录树结构

**框架识别说明**：
- 支持识别 13+ 主流框架（见[框架支持](#框架支持)）
- 基于特征关键词和文件模式识别，即使没有明确依赖也能检测
- 返回的框架名可直接用于查阅对应的框架指引

---

### 步骤 2：查阅框架指引

**触发条件**：步骤 1 返回了 `frameworks` 字段

**查找方式**：

**方式 1：直接跳转**
```
# 示例：frameworks: ["fastapi", "vue"]
→ 查看 references/frameworks/index.md 中的 FastAPI 和 Vue 章节
→ 使用锚点跳转：#fastapi、#vue
```

**方式 2：框架选择推荐**
根据 `languages` 和项目特征选择最适合的框架指引：
- **Python Web** → Django（企业级）/Flask（轻量级）/FastAPI（异步）
- **前端** → React（生态丰富）/Vue（易上手）/Svelte（高性能）
- **桌面应用** → Electron（成熟）/Tauri（轻量）

---

### 步骤 3：构建知识图谱

**目的**：生成模块/API/配置的关系网络

```bash
python3 scripts/knowledge_graph.py --path ./your-project --format mermaid
```

**输出文件**：
- `knowledge-graph.json`: 结构化数据（节点和边）
- `knowledge-graph.mmd`: Mermaid 流程图（可直接渲染）

**知识图谱包含**：
- 节点类型：模块、API、配置、数据库、外部服务
- 关系类型：包含、依赖、调用、数据流
- 可视化：目录结构图、模块关系图、API 调用图

---

### 步骤 4：提取隐性知识

**目的**：挖掘代码中的设计决策、最佳实践、代码约定

```bash
python3 scripts/knowledge_extractor.py --path ./your-project --language python
```

**输出文件**：`implicit-knowledge.json`

**提取内容**：
- 设计模式识别（单例、工厂、观察者等）
- 架构决策记录（为什么选择某个方案）
- 最佳实践提取（命名规范、注释风格）
- 代码约定总结（模块划分、接口设计）

---

### 步骤 5：生成文档（智能体主导）

**基于提取的数据，智能体生成以下文档**：

| 文档类型 | 生成方式 | 输出格式 |
|----------|----------|----------|
| **README** | 参考模板 + 项目数据 | Markdown |
| **API 文档** | AST 解析 + 注释提取 | Markdown + JSON |
| **架构文档** | 知识图谱 + 架构决策 | Markdown + Mermaid |
| **知识库首页** | 知识分类 + 时间线 | Markdown |

**智能体职责**：
- 根据框架指引生成特定框架的文档结构
- 将隐性知识转化为可读的自然语言描述
- 生成可视化图表（架构图、时序图、流程图）

---

## 框架支持

### 支持的框架（13 个）

**⭐ 最常用框架**（推荐优先查阅）：
- **React**: 企业级前端，生态最丰富
- **Vue**: 渐进式前端，易上手
- **Django**: Python 全栈，快速开发
- **Spring Boot**: Java 企业级，Spring 生态

**桌面应用**（3 个）：
- [Electron](references/frameworks/index.md#electron-框架) - 成熟生态、跨平台
- [Tauri](references/frameworks/index.md#tauri-框架) - 小体积、高安全性
- [Wails](references/frameworks/index.md#wails-框架) - 开发友好、配置简单

**前端框架**（4 个）：
- [React](references/frameworks/index.md#react-框架) - 虚拟 DOM、大型生态
- [Vue](references/frameworks/index.md#vue-框架) - 响应式、渐进式
- [Svelte](references/frameworks/index.md#svelte-框架) - 编译型、高性能
- [SolidJS](references/frameworks/index.md#solidjs-框架) - 细粒度响应式

**Web API 框架**（5 个）：
- [Django](references/frameworks/index.md#django-框架) - Python 全栈、ORM
- [Flask](references/frameworks/index.md#flask-框架) - Python 轻量级
- [FastAPI](references/frameworks/index.md#fastapi-框架) - Python 现代异步
- [Spring Boot](references/frameworks/index.md#spring-boot-框架) - Java 企业级
- [Gin](references/frameworks/index.md#gin-框架) - Go 高性能

**跨平台 UI 框架**（1 个）：
- [Flutter](references/frameworks/index.md#flutter-框架) - Dart、多平台

**完整索引**：[references/frameworks/index.md](references/frameworks/index.md)

**框架选择指南**：根据 `project-analysis.json` 返回的框架名，直接查阅对应指引即可。

---

## 资源索引

### 核心脚本

| 脚本 | 用途 | 参数 | 输出 |
|------|------|------|------|
| [analyze_project.py](scripts/analyze_project.py) | 项目结构分析 | `--path` 项目路径 | `project-analysis.json` |
| [knowledge_graph.py](scripts/knowledge_graph.py) | 知识图谱构建 | `--path` 项目路径<br>`--format` 输出格式 | `knowledge-graph.json`<br>`knowledge-graph.mmd` |
| [knowledge_extractor.py](scripts/knowledge_extractor.py) | 隐性知识提取 | `--path` 项目路径<br>`--language` 编程语言 | `implicit-knowledge.json` |
| [extract_docs.py](scripts/extract_docs.py) | 文档和 API 提取 | `--path` 项目路径<br>`--language` 编程语言 | `docs-metadata.json` |
| [analyze_dependencies.py](scripts/analyze_dependencies.py) | 依赖关系分析 | `--path` 项目路径<br>`--format` 输出格式 | 依赖图（JSON/Mermaid） |

### 参考文档

| 文档 | 用途 | 何时读取 |
|------|------|----------|
| [frameworks/index.md](references/frameworks/index.md) | **框架指引索引**（最重要） | 检测到框架后查阅 |
| [knowledge-base-guide.md](references/knowledge-base-guide.md) | 知识库构建指南 | 构建知识库时参考 |
| [knowledge-structure.md](references/knowledge-structure.md) | 知识结构组织 | 设计知识分类时参考 |
| [readme-template.md](references/readme-template.md) | README 生成模板 | 生成项目 README |
| [api-doc-guide.md](references/api-doc-guide.md) | API 文档生成规范 | 生成 API 文档 |
| [architecture-guide.md](references/architecture-guide.md) | 架构文档生成指南 | 生成架构文档 |
| [mermaid-syntax.md](references/mermaid-syntax.md) | Mermaid 图表语法 | 生成可视化图表 |

---

## 常见问题

### Q1: 如何快速定位框架指引？

**A**: 步骤 1 执行后，查看 `project-analysis.json` 的 `frameworks` 字段，例如：
```json
{
  "frameworks": ["fastapi", "vue"]
}
```

然后在 `references/frameworks/index.md` 中搜索 `#fastapi` 和 `#vue` 即可跳转到对应章节。

---

### Q2: 支持哪些编程语言？

**A**: 当前支持的语言：
- Python、JavaScript、Java、Go、Rust
- C/C++、Ruby、PHP、Dart

---

### Q3: 框架检测准确吗？

**A**: 基于多维度特征识别：
1. 依赖包检测（package.json、requirements.txt 等）
2. 文件模式检测（*.vue、*.jsx、manage.py 等）
3. 目录结构检测（src-tauri/、android/ 等）
4. 代码模式检测（@app.route、@SpringBootApplication 等）

即使没有明确依赖，也能通过文件和代码特征推断。

---

### Q4: 知识图谱如何可视化？

**A**: 两种方式：

**方式 1：直接渲染 Mermaid**
```bash
# 生成 Mermaid 文件
python3 scripts/knowledge_graph.py --path ./your-project --format mermaid

# 使用支持的 Markdown 编辑器（如 Typora、GitHub）打开 knowledge-graph.mmd
```

**方式 2：在线渲染**
- 复制 `knowledge-graph.mmd` 内容到 https://mermaid.live/
- 或使用 VS Code 的 Mermaid 插件

---

### Q5: 如何增量更新知识库？

**A**: 重新执行受影响的步骤：
- 代码变更 → 重新运行 `analyze_project.py`
- 架构调整 → 重新运行 `knowledge_graph.py`
- 需求更新 → 重新运行 `knowledge_extractor.py`

建议将上述脚本集成到 CI/CD 流程中。

---

### Q6: 隐性知识提取的原理是什么？

**A**: 通过以下方式挖掘隐性知识：
- **注释分析**：提取设计理由和权衡说明
- **代码模式**：识别设计模式（单例、工厂等）
- **命名约定**：分析类名、函数名的设计意图
- **依赖关系**：通过模块依赖推断架构决策

智能体会将这些结构化数据转化为自然语言描述。

---

### Q7: 生成文档的格式可以自定义吗？

**A**: 可以。参考 `references/` 目录下的模板文件：
- [readme-template.md](references/readme-template.md) - README 模板
- [api-doc-guide.md](references/api-doc-guide.md) - API 文档格式
- [architecture-guide.md](references/architecture-guide.md) - 架构文档格式

智能体会根据模板生成文档，你可以修改模板来自定义格式。
