---
name: book-skill-creator
version: v3.0.0
author: skill-manager
description: 技能工厂母技能，分析技术文档和网站生成技能拆分计划，支持智能网站分析、迭代学习、技术特点提取，适用于 Vue、React、Go、Python 等技术栈的文档分析和技能生成
tags:
  [
    skill-generation,
    documentation,
    web-analysis,
    iterative-learning,
    planning,
    parallel-execution,
  ]
---

# Book Skill Creator - 技能工厂

## 任务目标

- **本 Skill 用于**：分析技术文档和网站，通过迭代学习提取技术特点，生成技能拆分计划
- **核心能力**：
  - 网站内容读取（WebFetch/Read）
  - 技术特点分析和知识规划
  - 迭代式学习（search 补充）
  - 技能族规划和子技能生成
  - 技能族整体打包和发布
- **技能族概念**：
  - 技能族（Skill Family）是围绕同一技术栈的多个相关技能的集合
  - 例如：Vue 技能族 = vue-skills（母技能）+ vue-core-skill + vue-router-skill + vue-pinia-skill（子技能）
  - 技能族本身也是一个技能，拥有独立的 SKILL.md
  - 子技能可以独立使用，也可以依赖技能族
- **触发条件**：
  - 提供技术网站 URL 需要分析并生成技能族
  - 从大型文档/技术书籍生成技能族
  - 从规范文档生成相关技能族

## 核心工作流程

### 模式 A：智能网站分析

```
网站 URL → 内容读取 → 技术特点分析 → 知识规划 → 迭代学习 → 技能族规划 → 母技能生成 → 子技能生成 → 打包发布
```

**详细流程**：见 [references/web-analysis-flow.md](references/web-analysis-flow.md)

### 模式 B：文档分析

```
文档 → 解析 → 搜索补充 → 模块识别 → 技能族规划 → 母技能生成 → 子技能生成 → 打包发布
```

**详细流程**：见 [references/document-analysis-flow.md](references/document-analysis-flow.md)

### 技能族创建流程（新增）

当需要创建技能族时，需要同时创建母技能和子技能：

```
技能族规划 → 母技能创建 → 子技能创建 → 技能族打包
```

**详细流程**：见 [references/skill-family-flow.md](references/skill-family-flow.md)

## 操作步骤

### 模式 A：智能网站分析流程

**详细步骤**：见 [references/web-analysis-flow.md](references/web-analysis-flow.md)

**核心步骤概览**：

1. **网站内容读取** - 获取 URL，读取内容，提取技术特点
2. **知识规划** - 分析缺口，生成优先级清单
3. **迭代学习** - search 补充，评估完整性，循环学习
4. **技能族规划** - 识别模块，规划母技能和子技能结构

### 模式 B：文档分析流程

**详细步骤**：见 [references/document-analysis-flow.md](references/document-analysis-flow.md)

**核心步骤概览**：

1. **文档解析** - 读取文档，识别模块
2. **搜索补充** - 搜索最佳实践
3. **技能族规划** - 生成母技能和子技能规划
4. **母技能创建** - 创建技能族母技能
5. **子技能创建** - 创建子技能（可并行）
6. **打包发布** - 技能族整体打包和发布

### 技能族创建流程

**详细步骤**：见 [references/skill-family-flow.md](references/skill-family-flow.md)

**核心步骤概览**：

1. **技能族规划** - 确定技能族结构和子技能列表
2. **母技能创建** - 创建技能族母技能（vue-skills）
3. **子技能创建** - 创建子技能（vue-core-skill 等）
4. **打包发布** - 技能族整体打包到一个目录

## 技能族生成与打包

两种模式都支持技能族生成和打包：

- **母技能生成**：创建技能族母技能（如 vue-skills）
- **子技能生成**：创建子技能（如 vue-core-skill）
- **技能族打包**：将母技能和子技能打包到一个目录

**详细流程**：见 [references/skill-family-flow.md](references/skill-family-flow.md)

## 资源索引

| 资源             | 路径                                                                             | 用途                         |
| ---------------- | -------------------------------------------------------------------------------- | ---------------------------- |
| 技能规范         | [references/skill-specs.md](references/skill-specs.md)                           | SKILL.md 编写规范            |
| 框架指南         | [references/frameworks-guide.md](references/frameworks-guide.md)                 | 常用框架分类和使用场景       |
| 最佳实践         | [references/best-practices.md](references/best-practices.md)                     | 方案分类和解决方案           |
| **技能族流程**   | [references/skill-family-flow.md](references/skill-family-flow.md)               | **技能族创建完整流程**       |
| 网站分析指南     | [references/web-analysis-guide.md](references/web-analysis-guide.md)             | 智能网站分析模式完整指南     |
| API 技能模板     | [assets/skill-templates/api-skill.md](assets/skill-templates/api-skill.md)       | API 类技能模板               |
| 数据处理模板     | [assets/skill-templates/data-process.md](assets/skill-templates/data-process.md) | 数据处理类技能模板           |
| 工作流模板       | [assets/skill-templates/workflow.md](assets/skill-templates/workflow.md)         | 工作流类技能模板             |

## 注意事项

### 分析规划阶段

- **模块划分原则**：高内聚、低耦合，每个模块职责单一
- **依赖关系识别**：准确识别模块间的依赖，避免循环依赖
- **复杂度评估**：合理评估每个技能的复杂度，便于分配资源

### 并行生成阶段

- **独立执行**：每个技能生成应独立，避免相互干扰
- **资源共享**：共享的概念和代码放在 `shared/` 目录
- **进度跟踪**：实时跟踪各技能的生成进度

### 质量验证阶段

- **独立验证**：每个技能先生成后独立验证
- **一致性检查**：最后统一检查技能间的一致性
- **问题修复**：发现问题及时修复，重新验证

## 使用示例

### 示例 1：智能网站分析模式 - 创建 Vue 技能族

**输入**：https://vuejs.org

**输出**：Vue 技能族

```
vue-skills/                          # 母技能
├── SKILL.md                        # 技能族定义
├── references/
│   └── overview.md                 # 技能族概述
└── skills/                         # 子技能目录
    ├── vue-core-skill/             # 核心技能
    ├── vue-composition-api-skill/  # 组合式 API 技能
    ├── vue-router-skill/           # 路由技能
    ├── vue-pinia-skill/           # 状态管理技能
    └── vue-testing-skill/          # 测试技能
```

**详细流程**：见 [references/skill-family-flow.md](references/skill-family-flow.md)

### 示例 2：文档分析模式 - 创建 React 技能族

**输入**：React 官方文档

**输出**：React 技能族

```
react-skills/                        # 母技能
├── SKILL.md                        # 技能族定义
├── references/
│   └── overview.md                 # 技能族概述
└── skills/                         # 子技能目录
    ├── react-core-skill/          # 核心技能
    ├── react-hooks-skill/         # Hooks 技能
    ├── react-router-skill/         # 路由技能
    └── react-testing-skill/        # 测试技能
```

**详细流程**：见 [references/skill-family-flow.md](references/skill-family-flow.md)

## 质量门槛

### 模式 A：智能网站分析

- [ ] 网站 URL 可访问性验证通过
- [ ] 核心功能提取完整（至少 3 个）
- [ ] 关键概念提取完整（至少 5 个）
- [ ] 信息完整性达到 80% 以上
- [ ] 技能拆分合理，依赖关系正确

### 模式 B：文档分析

- [ ] 文档结构解析完整
- [ ] 技术模块识别准确
- [ ] 技能拆分合理
- [ ] 各技能通过独立验证

**详细检验标准**：见 [references/skill-standards.md](../skill-manager/references/skill-standards.md)

## 框架速查

支持分析以下技术栈：

- **Web 框架**：React, Vue, Angular, Svelte, FastAPI, Express, Django, Flask
- **后端语言**：Go, Python, Rust, Java, Node.js, TypeScript
- **数据库**：PostgreSQL, MongoDB, Redis, MySQL, SQLite
- **AI/ML 框架**：PyTorch, TensorFlow, Scikit-learn, LangChain

**详细使用指南**：见 [references/frameworks-guide.md](references/frameworks-guide.md)
