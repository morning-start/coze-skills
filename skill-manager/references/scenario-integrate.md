---
name: scenario-integrate
description: 整合技能场景指南，定义将多个技能整合为一个新技能的完整流程，包含整合模式和接口设计
tags: [scenario, integrate, composition, merge, lifecycle]
---

# 场景：整合技能

本文档定义将多个技能整合为一个新技能的完整流程，包含整合模式选择和接口设计。

---

## 场景概述

**适用场景**: 将多个相关技能整合为一个统一的能力集合
**生命周期**: 设计(Design) → 开发(Develop) → 测试(Test) → 发布(Release)
**预计耗时**: 45-90 分钟
**输出物**: 整合后的 SKILL.md + 整合说明文档

---

## 第一步：查阅信息 (Research)

### 1.1 分析源技能

**技能清单模板**:
```yaml
源技能分析:
  skill-a:
    capabilities: [能力1, 能力2]
    interface:
      input: [输入定义]
      output: [输出定义]
    dependencies: [依赖列表]
  
  skill-b:
    capabilities: [能力3, 能力4]
    interface:
      input: [输入定义]
      output: [输出定义]
    dependencies: [依赖列表]
```

### 1.2 评估兼容性

**兼容性检查清单**:
```yaml
兼容性评估:
  命名兼容性:
    - [ ] 无命名冲突
    - [ ] 命名风格一致
  
  接口兼容性:
    - [ ] 输入参数可统一
    - [ ] 输出格式可兼容
    - [ ] 错误处理一致
  
  数据兼容性:
    - [ ] 数据格式可转换
    - [ ] 数据依赖可解决
```

### 1.3 选择整合模式

**整合模式对比**:

| 模式 | 说明 | 适用场景 | 示例 |
|------|------|---------|------|
| **顺序** | 技能按顺序执行 | 流水线处理 | 清洗→分析→报告 |
| **并行** | 技能同时执行 | 独立任务 | 同时验证多个条件 |
| **嵌套** | 一个技能调用另一个 | 分层处理 | 外层控制+内层执行 |
| **流水线** | 数据流式处理 | 数据处理 | 读取→转换→输出 |

---

## 第二步：执行操作 (Execute)

### 阶段 1: 设计阶段 (Design)

**准入条件**: 源技能已分析，兼容性已评估

**操作步骤**:

1. **设计整合架构**
   ```yaml
   整合设计:
     名称: data-analysis-suite
     模式: 顺序
     组件:
       - data-cleaner
       - data-analyzer
       - report-generator
     数据流:
       raw_data → cleaned_data → analysis_result → report
   ```

2. **设计统一接口**
   ```yaml
   统一接口:
     input:
       data: [原始数据]
       config: [整合配置]
     output:
       result: [整合结果]
       reports: [各阶段报告]
       metadata: [处理元信息]
   ```

3. **设计数据映射**
   ```yaml
   数据映射:
     skill-a.output → skill-b.input:
       mapping:
         - from: cleaned_data
           to: input_data
           transform: identity
   ```

**准出条件**:
- [ ] 整合架构已设计
- [ ] 统一接口已定义
- [ ] 数据映射已设计

### 阶段 2: 开发阶段 (Develop)

**准入条件**: 设计阶段已完成

**操作步骤**:

1. **创建整合技能**
   ```bash
   mkdir data-analysis-suite
   cd data-analysis-suite
   touch SKILL.md
   ```

2. **编写 SKILL.md**
   ```yaml
   ---
   name: data-analysis-suite
   version: v1.0.0
   author: skill-manager
   description: 数据分析套件，整合数据清洗、分析和报告生成能力；当需要进行完整数据分析时使用
   tags: [data-analysis, integration, suite]
   ---
   ```

3. **定义整合流程**
   ```markdown
   ## 任务目标
   - 本 Skill 用于: 执行完整的数据分析流程
   - 能力包含: 
     - **数据清洗**: 调用 data-cleaner
     - **数据分析**: 调用 data-analyzer
     - **报告生成**: 调用 report-generator
   - 触发条件: 当需要进行完整数据分析时使用
   
   ## 操作步骤
   1. 接收原始数据和配置
   2. 调用 data-cleaner 清洗数据
   3. 调用 data-analyzer 分析数据
   4. 调用 report-generator 生成报告
   5. 整合各阶段结果
   6. 输出完整分析报告
   ```

**准出条件**:
- [ ] 整合技能已创建
- [ ] 依赖关系已声明
- [ ] 整合流程已定义

### 阶段 3: 测试阶段 (Test)

**准入条件**: 开发阶段已完成

**操作步骤**:

1. **接口契约测试**
   - [ ] 输入参数验证
   - [ ] 输出格式验证
   - [ ] 数据映射验证

2. **整合流程测试**
   - [ ] 各阶段执行验证
   - [ ] 数据传递验证
   - [ ] 错误处理验证

3. **兼容性测试**
   - [ ] 与源技能兼容
   - [ ] 版本兼容性
   - [ ] 依赖完整性

**准出条件**:
- [ ] 接口契约验证通过
- [ ] 整合流程验证通过
- [ ] 兼容性验证通过

### 阶段 4: 发布阶段 (Release)

**准入条件**: 测试阶段已完成

**操作步骤**:

1. **创建版本标签**
   ```bash
   git add .
   git commit -m "feat: 添加 data-analysis-suite 整合技能"
   git tag -a v1.0.0 -m "Release v1.0.0: 初始版本"
   ```

2. **创建整合说明文档**
   ```markdown
   # 整合说明
   
   ## 整合概览
   - **整合技能**: data-analysis-suite
   - **源技能**: data-cleaner, data-analyzer, report-generator
   - **整合模式**: 顺序执行
   
   ## 数据流
   ```
   raw_data → [data-cleaner] → cleaned_data
   cleaned_data → [data-analyzer] → analysis_result
   analysis_result → [report-generator] → report
   ```
   
   ## 使用方式
   直接调用 data-analysis-suite，自动执行完整流程。
   ```

**准出条件**:
- [ ] 版本标签已创建
- [ ] 整合说明已编写

---

## 第三步：检查验收 (Validate)

### 3.1 整合质量检查

```yaml
检查清单:
  架构:
    - [ ] 整合模式选择合理
    - [ ] 数据流设计清晰
    - [ ] 接口契约明确
  
  实现:
    - [ ] 依赖声明完整
    - [ ] 整合流程可执行
    - [ ] 错误处理完善
  
  文档:
    - [ ] 整合说明清晰
    - [ ] 使用示例完整
    - [ ] 迁移指南提供（如需要）
```

### 3.2 最终验证

```bash
# 验证依赖关系
grep -A 10 "dependencies:" SKILL.md

# 验证整合流程
grep -A 5 "操作步骤" SKILL.md

# 验证版本标签
git tag | grep v1.0.0
```

---

## 整合模式详解

### 模式 1: 顺序整合

**适用场景**: 任务有明确的先后顺序

**示例**:
```
数据清洗 → 数据分析 → 报告生成
```

**特点**:
- 数据单向流动
- 前一个输出是后一个输入
- 易于理解和调试

### 模式 2: 并行整合

**适用场景**: 多个独立任务可同时执行

**示例**:
```
          ┌→ 验证A →┐
输入数据 → ┼→ 验证B →┼→ 汇总结果
          └→ 验证C →┘
```

**特点**:
- 提高效率
- 需要结果合并
- 复杂度较高

### 模式 3: 嵌套整合

**适用场景**: 分层处理，外层控制内层

**示例**:
```
数据处理 (外层)
  ├── 数据清洗 (内层)
  ├── 数据转换 (内层)
  └── 数据验证 (内层)
```

**特点**:
- 层次清晰
- 易于扩展
- 需要良好的接口设计

---

## 参考文档

- [skill-standards.md](skill-standards.md) - 标准化规范

- [scenario-create.md](scenario-create.md) - 创建新技能
