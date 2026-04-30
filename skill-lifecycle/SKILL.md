***

name: skill-lifecycle
version: v2.0.0
author: skill-lifecycle
description: 高阶技能管理系统，支持技能全生命周期管理、文档规范制定、技能整合拆分及工作流编排；提供三层认知框架（域约束→设计决策→实现机制）和域扩展支持
tags:
\[
skill-management,
documentation-standards,
integration,
decomposition,
workflow,
meta-cognition,
domain-extension,
]
-

# Skill Lifecycle

## 任务目标

本 Skill 用于技能全生命周期管理，所有操作遵循**三层认知框架**：

- **Layer 3: 域约束（WHY）** - 为什么需要这个技能，约束条件是什么
- **Layer 2: 设计决策（HOW）** - 如何设计技能结构和工作流
- **Layer 1: 实现机制（WHAT）** - 具体实现细节和工具

### 核心能力

- **技能生命周期管理**: 创建新技能、修改现有技能、版本控制
- **文档规范制定**: 提供简单/复杂技能文档编写标准，指导文档分层组织
- **技能整合**: 将多个技能合并为一个新技能
- **技能拆分**: 将复杂技能拆分为多个独立技能
- **技能优化**: 应用设计模式提升技能质量

### 可选能力

- **工作流生成**: 根据技能生成标准化 WORKFLOW\.md（仅在需要编排多个技能时使用）
- **域扩展**: 支持按业务领域扩展技能集（FinTech、ML、Cloud-Native等）
- **元认知路由**: 根据问题类型自动路由到合适的技能或工作流

### 触发条件

当需要创建、修改、整合、拆分或优化技能时触发。

***

## 三层认知框架

所有技能操作遵循统一的三步流程，配合三层认知模型：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  第三层：域约束（Domain Constraints）                                         │
│  └── 为什么需要这个技能？目标用户是谁？有什么约束条件？                         │
│      向上追溯：识别问题的本质，而不是表面症状                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  第二层：设计决策（Design Decisions）                                          │
│  └── 如何设计技能结构？选择什么整合模式？工作流如何编排？                       │
│      权衡取舍：在多个方案中选择最适合当前域约束的                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  第一层：实现机制（Implementation Mechanisms）                                 │
│  └── 具体用什么工具？如何编写 SKILL.md？步骤如何执行？                         │
│      执行验证：按照设计决策实现，并通过标准化检验                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  三步流程：查阅信息 → 执行操作 → 检查验收                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 认知追踪示例

**问题**: "我的技能文档超过 500 行了"

```
├── Layer 3: 域约束分析
│   └── 为什么超过 500 行？
│       - 是因为功能确实复杂？还是文档组织混乱？
│       - 目标用户需要一次性阅读全部内容吗？
│       - 约束：需要支持多人协作维护吗？
│
├── Layer 2: 设计决策
│   └── 如果功能复杂 → 使用复杂技能文档结构（SKILL.md + references/）
│   └── 如果需要协作 → 拆分到子文档，按需加载
│   └── 如果只是描述过长 → 优化 description，压缩正文
│
└── Layer 1: 实现机制
    └── 创建 references/ 目录
    └── 编写 references/implementation.md
    └── 更新 SKILL.md 为概览+索引结构
```

***

## 场景操作指南

### 场景 A: 创建新技能

**生命周期**: 设计 → 开发 → 测试 → 发布
**认知层次**: Layer 3（域约束）→ Layer 2（设计）→ Layer 1（实现）
**子技能**: [scenario-create](skills/scenario-create/SKILL.md)

### 场景 B: 修改技能

**生命周期**: 开发 → 测试 → 发布 → 维护
**认知层次**: Layer 1（实现）→ Layer 2（影响分析）→ Layer 3（版本策略）
**子技能**: [scenario-modify](skills/scenario-modify/SKILL.md)

### 场景 C: 优化技能

**生命周期**: 设计 → 开发 → 测试 → 发布
**认知层次**: Layer 3（质量评估）→ Layer 2（优化策略）→ Layer 1（执行）
**子技能**: [scenario-optimize](skills/scenario-optimize/SKILL.md)

### 场景 D: 整合技能

**生命周期**: 设计 → 开发 → 测试 → 发布
**认知层次**: Layer 3（能力边界）→ Layer 2（整合模式）→ Layer 1（接口对接）
**子技能**: [scenario-integrate](skills/scenario-integrate/SKILL.md)

### 场景 E: 拆分技能

**生命周期**: 设计 → 开发 → 测试 → 发布
**认知层次**: Layer 3（职责划分）→ Layer 2（依赖关系）→ Layer 1（独立实现）
**子技能**: [scenario-decompose](skills/scenario-decompose/SKILL.md)

***

## 文档编写规范

### 简单技能 vs 复杂技能

根据技能复杂度选择合适的文档组织方式：

**简单技能**（功能单一、逻辑简单）:

- 直接在 `SKILL.md` 中完整描述所有功能
- 适用于：工具类技能、正文 < 300 行、无需复杂配置

**复杂技能**（多模块、逻辑复杂）:

- `SKILL.md` 仅作为概览和索引
- 详细内容拆分到 `references/` 子文件
- 适用于：多模块协作、需要详细文档、支持多人协作

**判断标准**:

- 功能数量：单一功能 vs 多个子功能
- 文档体量：< 300 行 vs ≥ 300 行
- 配置复杂度：简单 vs 复杂
- 依赖关系：无依赖 vs 需要编排

**详细规范**: 见 [skill-standards](skills/skill-standards/SKILL.md)

***

## 域扩展（Domain Extensions）

技能可按业务领域进行扩展，形成垂直领域的技能集合。

### 支持的域

| 域            | 描述    | 典型技能             |
| ------------ | ----- | ---------------- |
| FinTech      | 金融科技  | 风险评估、交易分析、合规检查   |
| ML           | 机器学习  | 数据预处理、模型训练、结果可视化 |
| Cloud-Native | 云原生   | 容器编排、服务网格、监控告警   |
| IoT          | 物联网   | 设备管理、数据采集、边缘计算   |
| Embedded     | 嵌入式   | 固件开发、驱动编写、资源优化   |
| Web          | Web开发 | 前端组件、后端API、安全加固  |
| CLI          | 命令行   | 文本处理、文件操作、系统管理   |

### 域扩展机制

```yaml
# 在 SKILL.md 前言区声明域扩展
domain_extension:
  primary: [主要域]
  secondary: [次要域]
  skills_related: [相关技能列表]
```

### 域扩展示例

```yaml
---
name: trading-risk-evaluator
version: v1.0.0
author: fintech-team
description: 交易风险评估技能，实时计算持仓风险暴露和止损建议
tags: [fintech, risk-management, trading, real-time-analysis]
domain_extension:
  primary: FinTech
  secondary: [ML]
  skills_related: [data-analyzer, report-generator]
---
```

***

## 子技能索引

| 子技能                                                        | 描述           | 何时使用     |
| ---------------------------------------------------------- | ------------ | -------- |
| [skill-standards](skills/skill-standards/SKILL.md)         | 标准化规范 + 检验指南 | 所有操作前查阅  |
| [scenario-create](skills/scenario-create/SKILL.md)         | 创建新技能        | 创建技能时    |
| [scenario-modify](skills/scenario-modify/SKILL.md)         | 修改技能         | 修改技能时    |
| [scenario-optimize](skills/scenario-optimize/SKILL.md)     | 优化技能         | 优化技能时    |
| [scenario-integrate](skills/scenario-integrate/SKILL.md)   | 整合技能         | 整合技能时    |
| [scenario-decompose](skills/scenario-decompose/SKILL.md)   | 拆分技能         | 拆分技能时    |
| [workflow-generation](skills/workflow-generation/SKILL.md) | 工作流生成        | 需要编排工作流时 |

***

## 注意事项

- **核心原则**: 所有技能操作必须遵循"查阅-执行-检查"三步流程
- **标准化优先**: 创建/修改技能前务必阅读 skill-standards.md
- **质量保障**: 每个操作完成后必须执行标准化检验
- **版本控制**: 重要修改需更新版本号并记录变更
- **向后兼容**: 修改时尽量保持向后兼容
- **元认知追踪**: 遇到问题时，先追溯到 Layer 3（域约束），不要直接在 Layer 1 给解决方案

***

## 使用示例

### 示例: 创建新技能（完整三步流程 + 三层认知）

**需求**: 创建数据清洗技能

**第一步：查阅信息（Layer 3 → Layer 2）**

```
Layer 3: 域约束分析
├── 核心问题：清洗原始数据
├── 目标用户：数据分析师
├── 触发场景：获得原始数据需要预处理时
└── 约束条件：需要支持多种数据格式

Layer 2: 设计决策
├── 技能类型：简单技能（单一功能）
├── 文档策略：单文件 SKILL.md
└── 关键能力：缺失值处理、去重、格式标准化
```

**第二步：执行操作（Layer 1）**

```bash
# 1. 创建目录
mkdir data-cleaner

# 2. 编写 SKILL.md
```

```yaml
---
name: data-cleaner
version: v1.0.0
author: skill-lifecycle
description: 数据清洗技能，支持缺失值处理、去重和格式标准化
tags: [data-cleaning, preprocessing, validation]
---

# Data Cleaner

## 任务目标
- 本 Skill 用于: 清洗原始数据为分析可用格式
- 能力包含: 缺失值处理、去重、格式标准化
- 触发条件: 获得原始数据需要预处理时
```

**第三步：检查验收**

```
□ 元信息完整性检查
  - name: data-cleaner（符合规范）
  - version: v1.0.0（格式正确）
  - author: skill-lifecycle（存在）
  - description: 符合长度要求（100-150字符）
  - tags: 至少3个标签

□ 内容质量检查
  - 正文体量 < 500行
  - 包含所有必需章节
  - 示例完整可复制

□ 元认知追溯验证
  - Layer 3: 域约束已明确
  - Layer 2: 设计决策已记录
  - Layer 1: 实现符合标准

检验结果: ✅ 通过
```

***

## 版本历史

| 版本     | 日期         | 变更说明                    |
| ------ | ---------- | ----------------------- |
| v2.0.0 | 2026-04-30 | 引入三层认知框架和域扩展机制，重构为子技能结构 |
| v1.5.0 | 早期版本       | 初始版本，基础生命周期管理           |

