---
name: skill-factory-packager
version: v1.0.0
author: skill-factory
parent: skill-factory
description: 技能打包器，验证技能族结构完整性，执行打包验证并输出最终的技能族目录
tags: [skill-factory, packager, validation, packaging, quality-assurance]
dependency:
  parent: skill-factory
  requires: skill-factory-generator
---

# Skill Factory Packager - 技能打包器

## 任务目标

- **本 Skill 用于**：验证和打包技能族
- **核心能力**：目录结构验证、完整性检查、质量验证、打包输出
- **触发条件**：技能生成完成后需要验证和打包时

## 工作流程

```
技能目录 → 结构验证 → 完整性检查 → 质量验证 → 打包输出
```

## 操作步骤

### 步骤 1：目录结构验证

1. 验证母技能 SKILL.md 存在
2. 验证所有子技能目录存在
3. 验证每个子技能都有 SKILL.md

### 步骤 2：完整性检查

1. 检查母技能引用所有子技能
2. 检查子技能的 parent 指向正确
3. 检查版本号一致性

### 步骤 3：质量验证

1. 执行标准化检验
2. 验证前言区字段完整性
3. 检查内容质量

### 步骤 4：打包输出

1. 清理临时文件
2. 输出最终技能族

## 打包验证清单

```markdown
## 打包验证清单

- [ ] 母技能 SKILL.md 存在
- [ ] 所有子技能目录存在
- [ ] 每个子技能都有独立的 SKILL.md
- [ ] 母技能引用所有子技能
- [ ] 子技能的 parent 指向正确
- [ ] 版本号一致性
```

## 使用示例

**输入**：完整的 Vue 技能族目录

**输出**：Vue 技能族包
