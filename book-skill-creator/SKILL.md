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
  - 技能拆分和并行生成
  - 质量验证
- **触发条件**：
  - 提供技术网站 URL 需要分析并生成技能
  - 从大型文档/技术书籍生成多个技能
  - 从规范文档生成相关技能族
- **可选能力**：依赖分析、模板复用、版本协调

## 核心工作流程

### 模式 A：智能网站分析

```
网站 URL → 内容读取 → 技术特点分析 → 知识规划 → 迭代学习 → 技能规划 → 并行生成
```

**详细流程**：见 [references/web-analysis-flow.md](references/web-analysis-flow.md)

### 模式 B：文档分析

```
文档 → 解析 → 搜索补充 → 模块识别 → 技能拆分 → 并行生成 → 验证
```

**详细流程**：见 [references/document-analysis-flow.md](references/document-analysis-flow.md)

## 操作步骤

### 模式 A：智能网站分析流程

**详细步骤**：见 [references/web-analysis-flow.md](references/web-analysis-flow.md)

**核心步骤概览**：

1. **网站内容读取** - 获取 URL，读取内容，提取技术特点
2. **知识规划** - 分析缺口，生成优先级清单
3. **迭代学习** - search 补充，评估完整性，循环学习
4. **技能规划** - 识别模块，生成拆分计划

### 模式 B：文档分析流程

**详细步骤**：见 [references/document-analysis-flow.md](references/document-analysis-flow.md)

**核心步骤概览**：

1. **文档解析** - 读取文档，识别模块
2. **搜索补充** - 搜索最佳实践
3. **技能拆分** - 生成拆分计划
4. **并行生成** - 多智能体执行
5. **质量验证** - 独立验证，一致性检查

## 并行生成与质量验证

两种模式都支持并行生成和质量验证：

- **并行生成**：多个智能体同时生成不同技能
- **质量验证**：每个技能独立验证，然后进行一致性检查

**详细流程**：见 [references/document-analysis-flow.md#步骤-b4 并行生成](references/document-analysis-flow.md) 和 [references/document-analysis-flow.md#步骤-b5 质量验证](references/document-analysis-flow.md)

## 资源索引

| 资源             | 路径                                                                             | 用途                         |
| ---------------- | -------------------------------------------------------------------------------- | ---------------------------- |
| 技能规范         | [references/skill-specs.md](references/skill-specs.md)                           | SKILL.md 编写规范            |
| 框架指南         | [references/frameworks-guide.md](references/frameworks-guide.md)                 | 常用框架分类和使用场景       |
| 最佳实践         | [references/best-practices.md](references/best-practices.md)                     | 方案分类和解决方案           |
| **网站分析指南** | [references/web-analysis-guide.md](references/web-analysis-guide.md)             | **智能网站分析模式完整指南** |
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

### 示例 1：智能网站分析模式

**输入**：https://vuejs.org

**输出**：生成 5 个相关技能

- vue-core-skill（基础）
- vue-composition-api-skill（核心）
- vue-router-skill（核心）
- vue-pinia-skill（核心）
- vue-testing-skill（高级）

**详细流程**：见 [references/web-analysis-flow.md](references/web-analysis-flow.md)

### 示例 2：文档分析模式

**输入**：React 官方文档

**输出**：生成 4 个相关技能

- react-core-skill（基础）
- react-hooks-skill（核心）
- react-router-skill（核心）
- react-testing-skill（高级）

**详细流程**：见 [references/document-analysis-flow.md](references/document-analysis-flow.md)

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
