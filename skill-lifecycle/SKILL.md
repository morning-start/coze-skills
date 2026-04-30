---
name: skill-lifecycle
version: v2.1.0
author: skill-lifecycle
description: 技能全生命周期管理系统，提供创建、修改、优化、整合、拆分五大场景的标准化流程和决策指南
tags: [skill-management, lifecycle, documentation-standards]
---

# Skill Lifecycle

## 任务目标

本 Skill 用于管理技能的全生命周期，提供五大场景的标准化操作指南。

**核心能力**:
- 创建新技能
- 修改现有技能
- 优化技能质量
- 整合多个技能
- 拆分复杂技能

**触发条件**: 当你需要创建、修改、优化、整合或拆分技能时使用。

---

## 快速决策树

```
你需要做什么？
│
├─ 创建新技能 → 用 scenario-create
│
├─ 修改现有技能
│   ├─ 修复错误 → scenario-modify (Fix)
│   ├─ 添加新功能 → scenario-modify (Feature)
│   └─ 破坏性变更 → scenario-modify (Breaking)
│
├─ 提升现有技能质量
│   ├─ 质量问题诊断 → scenario-optimize
│   └─ 应用设计模式 → scenario-optimize
│
├─ 将多个技能合并 → 用 scenario-integrate
│
├─ 将复杂技能拆分 → 用 scenario-decompose
│
└─ 编排多技能工作流 → 用 workflow-generation
```

---

## 三步流程框架

所有操作遵循统一的三步流程：

```
┌─────────────────────────────────────────────────────────────┐
│  第一步：查阅信息 (Research)                                 │
│  ├── 阅读 skill-standards.md 了解格式规范                   │
│  ├── 阅读对应场景指南（如 scenario-create.md）              │
│  └── 理解当前技能状态（如修改现有技能）                      │
├─────────────────────────────────────────────────────────────┤
│  第二步：执行操作 (Execute)                                  │
│  ├── 创建/修改 SKILL.md                                     │
│  ├── 按场景指南执行具体步骤                                  │
│  └── 更新版本号（如需要）                                   │
├─────────────────────────────────────────────────────────────┤
│  第三步：检查验收 (Validate)                                 │
│  ├── 执行标准化检验（使用 skill-standards.md）             │
│  ├── 验证元信息完整性                                       │
│  └── 确认文档质量                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 场景索引

| 场景 | 适用情况 | 生命周期 | 输出物 |
|------|---------|---------|--------|
| [scenario-create](skills/scenario-create/SKILL.md) | 从零创建新技能 | 设计→开发→测试→发布 | 新技能 SKILL.md |
| [scenario-modify](skills/scenario-modify/SKILL.md) | 修改已有技能 | 开发→测试→发布→维护 | 更新后的 SKILL.md |
| [scenario-optimize](skills/scenario-optimize/SKILL.md) | 提升技能质量 | 设计→开发→测试→发布 | 优化后的 SKILL.md |
| [scenario-integrate](skills/scenario-integrate/SKILL.md) | 合并多个技能 | 设计→开发→测试→发布 | 整合后的 SKILL.md |
| [scenario-decompose](skills/scenario-decompose/SKILL.md) | 拆分复杂技能 | 设计→开发→测试→发布 | 多个独立技能 |
| [workflow-generation](skills/workflow-generation/SKILL.md) | 编排工作流 | 设计→开发→测试→发布 | WORKFLOW.md |

---

## 核心规范速查

### SKILL.md 必需结构

```yaml
---
name: <skill-name>           # 小写字母+连字符
version: v1.0.0              # v主.次.补丁
author: <作者>
description: <100-150字符描述>
tags: [tag1, tag2, tag3]    # 至少3个标签
---
```

### 正文必需章节

```markdown
## 任务目标
- 本 Skill 用于: <一句话说明>
- 核心能力: <能力要点>
- 触发条件: <何时使用>

## 操作步骤
1. <步骤1>
2. <步骤2>

## 使用示例
<示例>

## 注意事项
<注意点>
```

### 质量标准

| 检查项 | 标准 |
|-------|------|
| 正文行数 | < 500 行 |
| description | 100-150 字符 |
| tags | ≥ 3 个 |
| 必需章节 | 任务目标、操作步骤、示例 |

---

## 参考文档

| 文档 | 用途 |
|-----|------|
| [skill-standards](skills/skill-standards/SKILL.md) | 格式规范、检验清单（所有操作前必读） |

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v2.1.0 | 2026-04-30 | 简化框架，增加决策树，移除冗余内容 |
| v2.0.0 | 2026-04-30 | 引入子技能结构 |
