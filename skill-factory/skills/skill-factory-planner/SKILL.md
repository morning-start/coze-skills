---
name: skill-factory-planner
version: v1.0.0
author: skill-factory
parent: skill-factory
description: 技能规划器，基于技术分析结果生成技能拆分计划，确定母技能和子技能结构、依赖关系及生成优先级
tags: [skill-factory, planner, skill-planning, dependency-analysis, architecture-design]
dependency:
  parent: skill-factory
  requires: skill-factory-analyzer
---

# Skill Factory Planner - 技能规划器

## 任务目标

- **本 Skill 用于**：基于分析结果生成技能拆分计划
- **核心能力**：模块识别、技能拆分、依赖分析、执行计划生成
- **触发条件**：完成技术分析后需要规划技能时

## 工作流程

```
分析报告 → 模块识别 → 技能拆分 → 依赖分析 → 执行计划
```

## 操作步骤

### 步骤 1：模块识别

1. 基于分析报告识别独立技术模块
2. 确定每个模块的核心内容
3. 记录模块间的依赖关系

### 步骤 2：技能拆分设计

1. 确定母技能定位（技能族概览）
2. 设计子技能拆分方案
3. 确保每个技能职责单一
4. 评估技能复杂度

### 步骤 3：依赖关系分析

1. 识别无依赖的基础技能
2. 确定有依赖的核心/高级技能
3. 避免循环依赖

### 步骤 4：执行计划生成

1. 确定生成顺序
2. 规划并行执行组
3. 标注每个技能的定位和复杂度

## 输出格式

```markdown
## 技能清单

### 技能 1：{skill-name-1}
- **对应模块**：{模块列表}
- **技能定位**：{基础/核心/高级}
- **依赖技能**：{无/技能 X}
- **预计复杂度**：{低/中/高}

## 执行策略

### 并行执行组
- **第 1 组**（无依赖）：{skill-name-1}
- **第 2 组**（可并行）：{skill-name-2}, {skill-name-3}
```

## 使用示例

**输入**：Vue.js 技术分析报告

**输出**：Vue 技能拆分计划
