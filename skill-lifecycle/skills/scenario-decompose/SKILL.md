---
name: scenario-decompose
version: v2.0.0
author: skill-lifecycle
description: 拆分技能场景指南，定义将复杂技能拆分为多个独立技能的流程
tags: [scenario, decompose, split, refactoring]
---

# 场景：拆分技能

## 适用场景

将复杂技能拆分为多个独立的简单技能。

---

## 快速决策

```
是否需要拆分？
│
├─ 技能有 >5 个核心能力？
│   └─ 是 → 考虑拆分
│
├─ 不同能力面向不同用户？
│   └─ 是 → 考虑拆分
│
└─ 部分能力可独立复用？
    └─ 是 → 考虑拆分
```

---

## 第一步：分析原技能

### 操作

**1. 提取能力清单**

```yaml
原技能分析:
  name: <原技能名>
  capabilities:
    - <能力1>
    - <能力2>
    - ...
```

**2. 识别拆分点**

| 拆分维度 | 说明 | 示例 |
|---------|------|------|
| 功能 | 按功能模块拆分 | 读取/清洗/分析 |
| 场景 | 按使用场景拆分 | 实时处理/批处理 |
| 复杂度 | 按复杂度拆分 | 简单/复杂任务 |

**3. 评估依赖关系**

```yaml
依赖关系:
  skill-a:
    depends_on: []
    depended_by: [skill-b]
  skill-b:
    depends_on: [skill-a]
    depended_by: []
```

---

## 第二步：设计拆分

### 操作

**1. 设计拆分方案**

```yaml
拆分方案:
  原技能: <原技能名>
  拆分后:
    - name: <新技能1>
      capabilities: [<能力>]
    - name: <新技能2>
      capabilities: [<能力>]
```

**2. 设计协作关系**

```
<新技能1> → <新技能2> → <新技能3>
```

**3. 制定迁移策略**

```yaml
迁移策略:
  阶段1: 创建新技能（并行维护）
  阶段2: 标记原技能为 deprecated
  阶段3: 提供迁移期（30天）
  阶段4: 退役原技能
```

---

## 第三步：执行拆分

### 开发阶段

**准入**: 拆分方案完成

**操作**:

1. 创建新技能目录
   ```bash
   mkdir <skill-1> <skill-2>
   ```

2. 编写新技能 SKILL.md

3. 更新原技能为 deprecated

   ```yaml
   ---
   name: <原技能>
   version: v2.0.0
   description: [已拆分，请使用新的独立技能]
   tags: [deprecated]
   ---
   ```

### 测试阶段

**准入**: 开发阶段完成

**验证**:
- [ ] 每个技能职责单一
- [ ] 技能间无重复能力
- [ ] 技能边界清晰
- [ ] 功能等价（原技能 = 新技能组合）

### 发布阶段

**准入**: 测试阶段完成

```bash
git add .
git commit -m "refactor(<原技能>): 拆分为独立技能"
git tag -a <skill-1>-v1.0.0 -m "Release <skill-1> v1.0.0"
```

---

## 第四步：验收

### 拆分质量检查

- [ ] 每个技能职责单一
- [ ] 技能数量合理（3-5个）
- [ ] 依赖关系无循环
- [ ] 迁移指南完整

---

## 参考文档

- [skill-standards](../skill-standards/SKILL.md) - 格式规范
- [scenario-create](../scenario-create/SKILL.md) - 创建技能
