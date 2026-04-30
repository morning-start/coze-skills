---
name: skill-factory
version: v4.0.0
author: skill-lifecycle
description: 技能工厂母技能，分析技术文档和网站生成技能拆分计划，支持智能网站分析、迭代学习、技术特点提取，适用于 Vue、React、Go、Python 等技术栈的文档分析和技能族生成
tags: [skill-factory, skill-family, documentation, web-analysis, iterative-learning, planning]
dependency:
  parent: skill-lifecycle
---

# Skill Factory - 技能工厂

## 技能族概述

Skill Factory 是技能工厂技能族，包含四个子技能：

- **skill-factory-analyzer**：技术内容分析器
- **skill-factory-planner**：技能规划器
- **skill-factory-generator**：技能生成器
- **skill-factory-packager**：技能打包器

## 子技能列表

| 子技能 | 版本 | 描述 | 依赖 |
|--------|------|------|------|
| skill-factory-analyzer | v1.0.0 | 技术内容分析器，通过网站分析和迭代学习提取技术特点 | 无 |
| skill-factory-planner | v1.0.0 | 技能规划器，生成技能拆分计划和依赖关系 | skill-factory-analyzer |
| skill-factory-generator | v1.0.0 | 技能生成器，创建母技能和子技能的 SKILL.md | skill-factory-planner |
| skill-factory-packager | v1.0.0 | 技能打包器，验证和打包技能族 | skill-factory-generator |

## 工作流程

### 模式 A：智能网站分析

```
URL → skill-factory-analyzer → skill-factory-planner → skill-factory-generator → skill-factory-packager
```

### 模式 B：文档分析

```
文档 → skill-factory-analyzer → skill-factory-planner → skill-factory-generator → skill-factory-packager
```

## 使用方式

### 单独使用子技能

```bash
# 使用分析器
/Skill skill-factory-analyzer

# 使用规划器
/Skill skill-factory-planner

# 使用生成器
/Skill skill-factory-generator

# 使用打包器
/Skill skill-factory-packager
```

### 使用完整技能族

```bash
/Skill skill-factory
```

## 技能族结构

```
skill-factory/                          # 母技能
├── SKILL.md                           # 技能族定义
├── metadata.json                      # 技能族元数据
├── index/
│   └── skills-index.md                # 技能索引
└── skills/                            # 子技能目录
    ├── skill-factory-analyzer/       # 分析器
    │   ├── SKILL.md
    │   └── references/
    ├── skill-factory-planner/        # 规划器
    │   ├── SKILL.md
    │   └── references/
    ├── skill-factory-generator/       # 生成器
    │   ├── SKILL.md
    │   └── references/
    │       ├── api-skill-template.md
    │       ├── data-process-template.md
    │       ├── workflow-template.md
    │       └── templates.md
    └── skill-factory-packager/       # 打包器
        ├── SKILL.md
        └── references/
```

## 核心能力

- **网站内容读取**：使用 WebFetch/Read 获取技术网站或文档内容
- **技术特点分析**：提取核心功能、关键概念和应用场景
- **知识规划**：生成带优先级的知识学习清单
- **迭代学习**：通过 search 补充完善技术分析
- **技能族规划**：设计母技能和子技能结构
- **技能生成**：创建完整的 SKILL.md 和参考文档
- **技能打包**：验证并打包技能族

## 触发条件

- 提供技术网站 URL 需要分析并生成技能族
- 从大型文档/技术书籍生成技能族
- 从规范文档生成相关技能族

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v4.0.0 | 2026-04-30 | 重构为技能族结构，包含 4 个子技能 |
| v3.0.0 | 早期版本 | 初始版本，简单技能结构 |
