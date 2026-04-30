---
name: skill-factory-generator
version: v1.0.0
author: skill-factory
parent: skill-factory
description: 技能生成器，根据拆分计划创建母技能和子技能的 SKILL.md，包括正文编写和模板应用
tags: [skill-factory, generator, skill-creation, documentation, template]
dependency:
  parent: skill-factory
  requires: skill-factory-planner
---

# Skill Factory Generator - 技能生成器

## 任务目标

- **本 Skill 用于**：根据拆分计划生成技能文件
- **核心能力**：母技能生成、子技能生成、模板应用
- **触发条件**：获得技能拆分计划后需要生成技能时

## 工作流程

```
技能拆分计划 → 母技能生成 → 子技能生成 → 质量自检
```

## 操作步骤

### 步骤 1：母技能生成

1. 创建母技能目录结构
2. 编写母技能 SKILL.md
3. 设置 `parent` 指向父技能

### 步骤 2：子技能生成

1. 创建子技能目录结构
2. 编写子技能 SKILL.md
3. 设置正确的 parent 和 requires

### 步骤 3：模板应用

根据技能类型应用模板（见下方模板参考）

## 模板参考

### API 技能模板

```yaml
---
name: {{ skill_name }}
description: {{ description }}
---

# {{ skill_title }}

## 任务目标
- 本 Skill 用于：{{ functionality }}
- 核心能力：{{ core_features }}
- 触发条件：{{ trigger_conditions }}

## 操作步骤
1. 准备请求参数
2. 调用 API 接口
3. 处理响应结果
```

### 数据处理技能模板

```yaml
---
name: {{ skill_name }}
description: {{ description }}
---

# {{ skill_title }}

## 任务目标
- 本 Skill 用于：{{ functionality }}
- 核心能力：{{ core_features }}
- 触发条件：{{ trigger_conditions }}

## 操作步骤
1. 数据读取与验证
2. 执行数据处理
3. 结果导出
```

### 工作流技能模板

```yaml
---
name: {{ skill_name }}
description: {{ description }}
---

# {{ skill_title }}

## 任务目标
- 本 Skill 用于：{{ functionality }}
- 核心能力：{{ core_features }}
- 触发条件：{{ trigger_conditions }}

## 操作步骤
1. 流程解析与验证
2. 任务编排与执行
3. 结果汇总与报告
```

## 使用示例

**输入**：Vue 技能拆分计划

**输出**：完整的 Vue 技能族目录结构
