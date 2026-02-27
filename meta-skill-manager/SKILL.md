---
name: meta-skill-manager
description: 高阶技能管理系统，支持技能生命周期管理、整合拆分、工作流编排与技能优化；当用户需要创建、修改、更新技能，整合多个技能，拆分技能能力，生成工作流，或优化技能设计时使用
---

# Meta Skill Manager

## 任务目标
- 本 Skill 用于: 全生命周期技能管理，包括创建、修改、更新、版本控制，技能整合、拆分、工作流编排，以及技能设计优化
- 能力包含: 
  - **技能生命周期管理**: 创建新技能、修改现有技能、更新技能、版本控制
  - **技能整合**: 将 2+ 技能合并为一个新技能
  - **技能拆分**: 将技能拆分为多个独立技能
  - **工作流生成**: 根据技能和目标生成标准化 WORKFLOW.md
  - **技能优化**: 应用设计模式提升技能质量
- 触发条件: 需要管理、整合、拆分、生成或优化技能时

## 核心能力速查

| 能力 | 用途 | 参考文档 |
|------|------|---------|
| **生命周期管理** | 创建、修改、更新、版本控制 | [skill-lifecycle.md](references/skill-lifecycle.md) |
| **技能整合** | 2+ 技能合并为新技能 | [skill-integration.md](references/skill-integration.md) |
| **技能拆分** | 将技能拆分为多个独立技能 | [skill-decomposition.md](references/skill-decomposition.md) |
| **工作流生成** | 生成标准化 WORKFLOW.md | [workflow-generation.md](references/workflow-generation.md) |
| **技能优化** | 应用10大优化策略 | [skill-optimization.md](references/skill-optimization.md) |

## 快速开始

### 场景 A: 创建新技能
1. 阅读 [skill-standards.md](references/skill-standards.md) 了解规范
2. 按照 [skill-lifecycle.md](references/skill-lifecycle.md) 创建
3. 参考 [skill-optimization.md](references/skill-optimization.md) 应用优化策略

### 场景 B: 整合技能
1. 阅读 [skill-integration.md](references/skill-integration.md)
2. 分析技能能力和接口
3. 选择整合策略（顺序/并行/嵌套/流水线）
4. 生成整合技能

### 场景 C: 拆分技能
1. 阅读 [skill-decomposition.md](references/skill-decomposition.md)
2. 分析能力清单和依赖
3. 设计拆分方案（功能/场景/复杂度）
4. 生成新技能

### 场景 D: 生成工作流
1. 阅读 [workflow-generation.md](references/workflow-generation.md)
2. 明确目标和可用技能
3. 选择工作流模式
4. 生成 WORKFLOW.md

### 场景 E: 优化技能
1. 阅读 [skill-optimization.md](references/skill-optimization.md)
2. 评估当前设计质量
3. 选择优化策略（原子化/标准化/元数据等）
4. 执行优化

## 参考文档索引

| 文档 | 内容 | 何时阅读 |
|------|------|---------|
| [skill-standards.md](references/skill-standards.md) | Skill/Workflow 格式规范、命名规则 | 创建或修改技能前 |
| [skill-lifecycle.md](references/skill-lifecycle.md) | 创建、修改、更新、版本控制 | 管理单个技能时 |
| [skill-integration.md](references/skill-integration.md) | 整合策略和操作流程，含组合模式 | 合并多个技能时 |
| [skill-decomposition.md](references/skill-decomposition.md) | 拆分策略和操作流程 | 分解复杂技能时 |
| [workflow-generation.md](references/workflow-generation.md) | 工作流生成步骤和模式 | 编排工作流时 |
| [skill-optimization.md](references/skill-optimization.md) | 10大优化策略 | 优化技能设计时 |

## 注意事项
- 所有操作均为纯自然语言指导，无脚本依赖
- 技能生命周期管理注重规范性
- 技能整合注重能力互补和接口兼容性
- 技能拆分注重单一职责原则
- 工作流生成注重可操作性
- **技能优化注重设计质量，应用原子化、标准化、元数据增强等策略**

## 使用示例

### 示例1: 创建技能
```
需求: 创建数据清洗技能

流程:
1. 阅读 skill-standards.md 了解规范
2. 按照 skill-lifecycle.md 创建 data-cleaner
   - name: data-cleaner
   - capabilities: [数据清洗, 缺失值处理]
3. 应用 skill-optimization.md 优化策略
   - 标准化接口: 定义 JSON Schema
   - 元数据增强: 添加 use_cases、cost_estimate
```

### 示例2: 整合技能
```
需求: 整合数据清洗、分析、报告生成

流程:
1. 阅读 skill-integration.md
2. 选择顺序整合策略（清洗 → 分析 → 报告）
3. 生成 data-analysis-suite
```

### 示例3: 拆分技能
```
需求: 拆分复杂的数据处理技能

流程:
1. 阅读 skill-decomposition.md
2. 按功能模块拆分
   - data-cleaner（清洗）
   - data-analyzer（分析）
3. 生成两个独立技能
```

### 示例4: 生成工作流
```
需求: 生成市场分析报告工作流

流程:
1. 阅读 workflow-generation.md
2. 选择线性模式
3. 编排: 获取 → 清洗 → 分析 → 报告
4. 生成 WORKFLOW.md
```

### 示例5: 优化技能
```
需求: 优化"处理用户订单"技能

流程:
1. 阅读 skill-optimization.md
2. 原子化拆分: parse-order、validate-inventory、generate-payment
3. 标准化接口: JSON Schema
4. 元数据增强: use_cases、reliability_score
5. 分层抽象: 原子 → 复合 → 任务
6. 错误处理: error_codes、fallback_actions
```
