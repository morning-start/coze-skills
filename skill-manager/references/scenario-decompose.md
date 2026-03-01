---
name: scenario-decompose
description: 拆分技能场景指南，定义将复杂技能拆分为多个独立技能的完整流程，包含拆分策略和迁移指南
tags: [scenario, decompose, split, refactoring, lifecycle]
---

# 场景：拆分技能

本文档定义将复杂技能拆分为多个独立技能的完整流程，包含拆分策略和迁移指南。

---

## 场景概述

**适用场景**: 技能职责过多，需要拆分为更小的独立技能
**生命周期**: 设计(Design) → 开发(Develop) → 测试(Test) → 发布(Release)
**预计耗时**: 60-120 分钟
**输出物**: 多个拆分后的 SKILL.md + 迁移指南

---

## 第一步：查阅信息 (Research)

### 1.1 分析原技能

**能力清单提取**:
```yaml
原技能分析:
  name: data-processor
  capabilities:
    - 数据读取
    - 数据清洗
    - 数据转换
    - 数据分析
    - 数据验证
    - 报告生成
    - 数据导出
  
  dependencies:
    - python
    - pandas
  
  complexity: high  # 复杂度过高
```

### 1.2 识别拆分点

**拆分维度**:

| 维度 | 说明 | 示例 |
|------|------|------|
| **功能** | 按功能模块拆分 | 读取/清洗/分析 |
| **场景** | 按使用场景拆分 | 实时处理/批处理 |
| **复杂度** | 按复杂度拆分 | 简单/复杂任务 |

**拆分分析模板**:
```yaml
拆分分析:
  拆分维度: 功能
  拆分后技能:
    - name: data-reader
      capabilities: [数据读取]
      complexity: low
    - name: data-cleaner
      capabilities: [数据清洗]
      complexity: medium
    - name: data-analyzer
      capabilities: [数据分析]
      complexity: high
```

### 1.3 评估依赖关系

**依赖分析**:
```yaml
依赖关系:
  data-reader:
    depends_on: []
    depended_by: [data-cleaner, data-analyzer]
  
  data-cleaner:
    depends_on: [data-reader]
    depended_by: [data-analyzer]
  
  data-analyzer:
    depends_on: [data-reader, data-cleaner]
    depended_by: []
```

---

## 第二步：执行操作 (Execute)

### 阶段 1: 设计阶段 (Design)

**准入条件**: 原技能已分析，拆分点已识别

**操作步骤**:

1. **设计拆分方案**
   ```yaml
   拆分方案:
     原技能: data-processor
     拆分后:
       - name: data-reader
         description: 数据读取技能
         capabilities: [数据读取]
       
       - name: data-cleaner
         description: 数据清洗技能
         capabilities: [数据清洗]
       
       - name: data-analyzer
         description: 数据分析技能
         capabilities: [数据分析]
       
       - name: data-exporter
         description: 数据导出技能
         capabilities: [数据导出]
   ```

2. **设计技能协作关系**
   ```yaml
   协作关系:
     顺序调用:
       - data-reader → data-cleaner → data-analyzer → data-exporter
     
     接口契约:
       data-reader.output → data-cleaner.input:
         format: cleaned_data_schema
   ```

3. **设计迁移策略**
   ```yaml
   迁移策略:
     阶段1: 创建新技能（并行维护）
     阶段2: 标记原技能为 deprecated
     阶段3: 提供迁移期（30天）
     阶段4: 退役原技能
   ```

**准出条件**:
- [ ] 拆分方案已设计
- [ ] 协作关系已定义
- [ ] 迁移策略已制定

### 阶段 2: 开发阶段 (Develop)

**准入条件**: 设计阶段已完成

**操作步骤**:

1. **创建新技能目录**
   ```bash
   mkdir data-reader data-cleaner data-analyzer data-exporter
   ```

2. **编写新技能 SKILL.md**

   **data-reader/SKILL.md**:
   ```yaml
   ---
   name: data-reader
   version: v1.0.0
   author: skill-manager
   description: 数据读取技能，支持多种数据源读取；当需要从不同来源读取数据时使用
   tags: [data-reading, io, parsing]
   ---
   
   # Data Reader
   
   ## 任务目标
   - 本 Skill 用于: 从多种数据源读取数据
   - 能力包含: CSV读取、JSON读取、数据库读取
   - 触发条件: 当需要读取数据时使用
   
   ## 操作步骤
   1. 识别数据源类型
   2. 配置读取参数
   3. 执行数据读取
   4. 返回结构化数据
   ```

   **data-cleaner/SKILL.md**:
   ```yaml
   ---
   name: data-cleaner
   version: v1.0.0
   author: skill-manager
   description: 数据清洗技能，支持缺失值处理、去重和格式标准化；当需要清洗数据时使用
   tags: [data-cleaning, preprocessing]
   ---
   
   # Data Cleaner
   
   ## 任务目标
   - 本 Skill 用于: 清洗和预处理数据
   - 能力包含: 缺失值处理、去重、格式标准化
   - 触发条件: 当获得原始数据需要清洗时使用
   
   ## 操作步骤
   1. 接收原始数据
   2. 处理缺失值
   3. 去除重复数据
   4. 标准化格式
   ```

3. **更新原技能状态**
   ```yaml
   ---
   name: data-processor
   version: v2.0.0
   description: [已拆分，请使用新的独立技能]
   tags: [deprecated]
   ---
   ```

**准出条件**:
- [ ] 新技能已创建
- [ ] 原技能已标记为 deprecated

### 阶段 3: 测试阶段 (Test)

**准入条件**: 开发阶段已完成

**操作步骤**:

1. **单一职责验证**
   - [ ] 每个技能职责单一
   - [ ] 技能间无重复能力
   - [ ] 技能边界清晰

2. **协作关系验证**
   - [ ] 数据传递正确
   - [ ] 接口契约满足
   - [ ] 依赖关系无循环

3. **功能等价验证**
   - [ ] 新技能组合 = 原技能能力
   - [ ] 无能力丢失
   - [ ] 无新增不必要能力

**准出条件**:
- [ ] 单一职责验证通过
- [ ] 协作关系验证通过
- [ ] 功能等价验证通过

### 阶段 4: 发布阶段 (Release)

**准入条件**: 测试阶段已完成

**操作步骤**:

1. **发布新技能**
   ```bash
   git add data-reader data-cleaner data-analyzer data-exporter
   git commit -m "feat: 拆分 data-processor 为独立技能"
   
   git tag -a data-reader-v1.0.0 -m "Release data-reader v1.0.0"
   git tag -a data-cleaner-v1.0.0 -m "Release data-cleaner v1.0.0"
   git tag -a data-analyzer-v1.0.0 -m "Release data-analyzer v1.0.0"
   git tag -a data-exporter-v1.0.0 -m "Release data-exporter v1.0.0"
   ```

2. **创建迁移指南**
   ```markdown
   # 迁移指南: data-processor v1 → v2
   
   ## 概述
   data-processor v1 已拆分为多个独立技能。
   
   ## 替代方案
   | 原用法 | 新用法 |
   |--------|--------|
   | data-processor (完整流程) | 使用 data-analysis-suite |
   | data-processor (仅读取) | 使用 data-reader |
   | data-processor (仅清洗) | 使用 data-cleaner |
   
   ## 迁移步骤
   1. 识别当前使用的 data-processor 功能
   2. 选择对应的新技能
   3. 更新调用代码
   4. 测试验证
   
   ## 时间线
   - 2024-03-01: data-processor v1 标记为 deprecated
   - 2024-04-01: data-processor v1 退役
   ```

3. **更新原技能（标记退役）**
   ```yaml
   ---
   name: data-processor
   version: v2.0.0
   description: [已退役，请使用新的独立技能]
   tags: [deprecated]
   ---
   ```

**准出条件**:
- [ ] 新技能已发布
- [ ] 原技能已标记为退役

---

## 第三步：检查验收 (Validate)

### 3.1 拆分质量检查

```yaml
检查清单:
  单一职责:
    - [ ] 每个技能职责单一
    - [ ] 技能数量合理（3-5个）
    - [ ] 技能粒度适中
  
  协作关系:
    - [ ] 依赖关系清晰
    - [ ] 无循环依赖
    - [ ] 接口契约明确
  
  迁移友好:
    - [ ] 迁移指南完整
    - [ ] 替代方案明确
    - [ ] 迁移期合理（30天）
```

### 3.2 最终验证

```bash
# 验证新技能创建
ls data-reader data-cleaner data-analyzer data-exporter

# 验证版本标签
git tag | grep "data-reader-v1.0.0"

# 验证原技能状态
grep "status: deprecated" data-processor/SKILL.md
```

---

## 拆分策略详解

### 策略 1: 按功能拆分

**适用场景**: 技能包含多个独立功能模块

**示例**:
```yaml
# 拆分前
data-processor: [读取, 清洗, 分析, 导出]

# 拆分后
data-reader: [读取]
data-cleaner: [清洗]
data-analyzer: [分析]
data-exporter: [导出]
```

### 策略 2: 按场景拆分

**适用场景**: 技能在不同场景下使用不同

**示例**:
```yaml
# 拆分前
data-processor: [实时处理, 批处理]

# 拆分后
data-stream-processor: [实时处理]
data-batch-processor: [批处理]
```

### 策略 3: 按复杂度拆分

**适用场景**: 技能包含简单和复杂任务

**示例**:
```yaml
# 拆分前
data-validator: [简单验证, 复杂验证, 规则引擎]

# 拆分后
data-simple-validator: [简单验证]
data-advanced-validator: [复杂验证, 规则引擎]
```

---

## 迁移期管理

### 迁移期时间线

```
Day 0:   发布新技能，标记原技能 deprecated
Day 7:   发送迁移提醒
Day 14:  发送迁移提醒
Day 21:  发送迁移提醒
Day 30:  退役原技能
```

### 迁移检查清单

```yaml
迁移检查:
  发布阶段:
    - [ ] 新技能已发布
    - [ ] 原技能已标记 deprecated
    - [ ] 迁移指南已发布
  
  提醒阶段:
    - [ ] Day 7 提醒已发送
    - [ ] Day 14 提醒已发送
    - [ ] Day 21 提醒已发送
  
  退役阶段:
    - [ ] Day 30 退役已执行
    - [ ] 原技能已归档
```

---

## 参考文档

- [skill-standards.md](skill-standards.md) - 标准化规范

- [scenario-create.md](scenario-create.md) - 创建新技能
