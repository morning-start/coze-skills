---
name: skill-factory
version: v4.1.0
author: skill-lifecycle
description: 技能工厂母技能，分析技术文档或网站生成技能拆分计划与技能族结构。接收 URL 或文档输入，输出完整的技能族包
tags: [skill-factory, skill-family, documentation, web-analysis, iterative-learning, planning]
dependency:
  parent: skill-lifecycle
  children:
    - skill-factory-analyzer
    - skill-factory-planner
    - skill-factory-generator
    - skill-factory-packager
---

# Skill Factory - 技能工厂

## 技能定位

技能工厂是一个**技能族编排器**，不直接处理具体技术内容，而是协调四个子技能完成"技术分析→技能规划→技能生成→打包验证"的完整流程。

**本技能解决什么问题**：将散乱的技术文档或网站，转化为结构化的、可复用的技能族。

## 两种工作模式

| 模式 | 输入 | 输出 | 子技能调用顺序 |
|------|------|------|----------------|
| **网站分析** | 技术网站 URL | 技能族包 | analyzer → planner → generator → packager |
| **文档分析** | 文档路径/内容 | 技能族包 | analyzer → planner → generator → packager |

两种模式调用相同的子技能链，区别在于 analyzer 的输入处理方式。

## 触发条件（使用判断）

**启用本技能的条件**（满足任一）：
- 用户提供一个或多个技术网站 URL，要求生成相关技能
- 用户提供文档路径/内容，要求从中提取技能族
- 用户要求"从 XXX 技术文档生成技能"

**不启用本技能的条件**：
- 用户已有拆分计划，只需生成技能文件 → 直接使用 `skill-factory-generator`
- 用户已有完整技能文件，只需打包 → 直接使用 `skill-factory-packager`
- 用户要分析技术但不需要生成技能 → 使用 `skill-factory-analyzer` 单个技能

## 子技能职责边界

| 子技能 | 输入 | 输出 | 核心判断 |
|--------|------|------|----------|
| **analyzer** | URL 或文档 | 技术分析报告 | 信息完整度是否 ≥80%？否则迭代 |
| **planner** | 分析报告 | 技能拆分计划 | 模块是否独立？依赖是否有环？ |
| **generator** | 拆分计划 | SKILL.md 文件 | 模板选择是否正确？内容是否完整？ |
| **packager** | 技能目录 | 验证报告 + 包 | 目录结构是否完整？版本是否一致？ |

## 串行流水线

```
输入 → analyzer → planner → generator → packager → 输出
```

每个子技能的输出是下一个子技能的输入。如果某个子技能判断不通过，返回上游重新处理。

## 单独使用子技能

```bash
/Skill skill-factory-analyzer    # 仅分析
/Skill skill-factory-planner     # 仅规划
/Skill skill-factory-generator   # 仅生成
/Skill skill-factory-packager    # 仅打包
```

## 完整使用技能族

```bash
/Skill skill-factory
```

---

## 子技能设计规范

### 通用结构

每个子技能必须包含以下章节：

1. **任务目标** - 明确本技能负责什么、不负责什么
2. **输入判断** - 如何判断输入是否有效、是否足够
3. **核心逻辑** - 具体的处理流程
4. **输出标准** - 什么样的输出算合格
5. **失败处理** - 判断不通过时怎么办

### 判断逻辑要求

子技能必须有明确的判断条件：
- **有效/无效判断**：输入是否符合要求
- **完成度判断**：输出是否足够充分
- **失败分支**：不通过时返回上游还是自行补充

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v4.1.0 | 2026-04-30 | 强化母技能定位，添加子技能职责边界和判断逻辑规范 |
| v4.0.0 | 2026-04-30 | 重构为技能族结构，包含 4 个子技能 |
| v3.0.0 | 早期版本 | 初始版本，简单技能结构 |
