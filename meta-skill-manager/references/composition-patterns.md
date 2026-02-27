# 技能组合模式

## 目录
- [组合模式概述](#组合模式概述)
- [顺序组合](#顺序组合)
- [并行组合](#并行组合)
- [嵌套组合](#嵌套组合)
- [流水线组合](#流水线组合)
- [整合与拆分原则](#整合与拆分原则)

## 概览
本文档定义了技能组合的四种标准模式，用于构建复杂、可维护的技能系统，以及技能拆分的原则和方法。

## 组合模式概述

### 组合目标
1. **模块化复用**: 将通用能力封装为独立技能，支持重复使用
2. **能力增强**: 通过组合多个技能实现更强大的功能
3. **灵活性**: 支持动态组合，适应不同场景需求
4. **可维护性**: 降低系统复杂度，便于迭代优化

### 组合原则
1. **单一职责**: 每个技能聚焦一个核心能力
2. **接口清晰**: 定义明确的输入输出格式
3. **低耦合**: 技能间最小化依赖
4. **可测试**: 每个技能可独立验证

## 顺序组合

### 模式定义
按固定顺序执行多个技能，前一个技能的输出作为后一个技能的输入。

### 适用场景
- 数据处理流程（清洗 → 转换 → 验证）
- 文档生成流程（收集 → 组织 → 生成）
- 报告处理流程（读取 → 分析 → 格式化）

### 结构示例
```
Skill A (数据清洗)
    ↓ [清洗后的数据]
Skill B (数据转换)
    ↓ [转换后的数据]
Skill C (数据验证)
    ↓ [验证结果]
输出
```

### 设计要点
1. 定义输入输出映射关系
2. 处理数据格式转换
3. 错误传播机制
4. 中间结果传递

### 元数据定义
```yaml
metadata:
  composition_type: sequential
  component_skills: [skill-a, skill-b, skill-c]
  input_mapping:
    skill-b: skill-a.output
    skill-c: skill-b.output
  data_flow:
    - from: skill-a
      to: skill-b
      format: json
    - from: skill-b
      to: skill-c
      format: csv
```

## 并行组合

### 模式定义
同时执行多个技能，收集所有技能的输出并合并。

### 适用场景
- 多维度数据分析（同时分析不同维度）
- 批量文件处理（并行处理多个文件）
- 多源数据采集（同时从多个来源获取数据）

### 结构示例
```
输入数据
    ↓
├─→ Skill A (维度1分析)
│     ↓
│   [分析结果A]
│
├─→ Skill B (维度2分析)
│     ↓
│   [分析结果B]
│
└─→ Skill C (维度3分析)
      ↓
    [分析结果C]
    ↓
合并输出 [综合报告]
```

### 合并策略
- **merge**: 智能合并（去重、去冲突）
- **concatenate**: 直接拼接
- **first**: 使用第一个成功的输出

### 元数据定义
```yaml
metadata:
  composition_type: parallel
  component_skills: [skill-a, skill-b, skill-c]
  output_merge_strategy: merge
  merge_rules:
    - strategy: deduplicate
      fields: [id, timestamp]
    - strategy: append
      fields: [results]
```

## 嵌套组合

### 模式定义
将一个或多个子技能嵌入到父技能的特定执行位置。

### 适用场景
- 复杂任务的分步实现
- 条件性能力调用
- 可选功能模块

### 结构示例
```
父技能 (主流程)
  ├─ 步骤1: 准备阶段
  │     ↓
  ├─ 步骤2: 核心处理 → 调用子技能 A
  │     ↓          [处理结果A]
  ├─ 步骤3: 中间整理
  │     ↓
  └─ 步骤4: 最终输出 → 调用子技能 B
            [输出结果B]
```

### 集成点类型
- **前置**: 在主流程之前执行
- **中置**: 在主流程中间执行
- **后置**: 在主流程之后执行
- **条件**: 满足特定条件时执行

### 元数据定义
```yaml
metadata:
  composition_type: nested
  parent_skill: parent-skill
  sub_skills:
    - name: sub-skill-a
      integration_point: step2
      condition: always
    - name: sub-skill-b
      integration_point: step4
      condition: on_success
```

## 流水线组合

### 模式定义
定义清晰的数据流向和转换规则，每个技能负责特定阶段的处理。

### 适用场景
- ETL 流程（提取 → 转换 → 加载）
- 数据清洗管道
- 内容生成流水线

### 结构示例
```
输入源
    ↓ [原始数据 - CSV格式]
Skill A (数据提取)
    ↓ [提取结果 - JSON格式]
    [转换: 解析CSV → 结构化JSON]
Skill B (数据转换)
    ↓ [转换结果 - 标准化数据]
    [转换: 字段映射、类型转换]
Skill C (数据标准化)
    ↓ [标准化结果]
    [转换: 格式统一、缺失值处理]
输出目标
```

### 元数据定义
```yaml
metadata:
  composition_type: pipeline
  component_skills: [skill-a, skill-b, skill-c]
  data_flow:
    input:
      source: file
      format: csv
    stages:
      - name: extract
        skill: skill-a
        input_format: csv
        output_format: json
        transforms:
          - parse_csv
          - structure_data
      - name: transform
        skill: skill-b
        input_format: json
        output_format: json
        transforms:
          - field_mapping
          - type_conversion
      - name: normalize
        skill: skill-c
        input_format: json
        output_format: json
        transforms:
          - standardize_format
          - handle_missing
```

## 整合与拆分原则

### 技能整合原则

#### 何时整合
1. **常用组合**: 多个技能经常被一起使用
2. **简化入口**: 降低用户使用复杂度
3. **增强能力**: 组合后产生新能力
4. **效率提升**: 减少重复操作和上下文切换

#### 整合策略选择

| 场景 | 推荐模式 | 说明 |
|------|---------|------|
| 数据依赖 | 顺序组合 | A 的输出是 B 的输入 |
| 多维度处理 | 并行组合 | 同时处理不同维度 |
| 主流程+子任务 | 嵌套组合 | 主流程中嵌入特定功能 |
| 数据管道 | 流水线组合 | 清晰的数据流转 |
| 复杂场景 | 混合组合 | 组合多种模式 |

#### 整合后技能定义
```yaml
# 整合技能元数据示例
metadata:
  composition_type: sequential
  component_skills: [data-cleaner, data-analyzer, report-generator]
  integrated_from:
    - skill: data-cleaner
      version: "1.2.0"
      capabilities_used: [数据清洗, 缺失值处理]
    - skill: data-analyzer
      version: "2.0.0"
      capabilities_used: [统计分析, 趋势识别]
    - skill: report-generator
      version: "1.5.0"
      capabilities_used: [报告生成, 可视化]
  new_capabilities:
    - 端到端数据分析
    - 自动化报告生成
```

### 技能拆分原则

#### 何时拆分
1. **复杂度过高**: 单技能包含过多能力
2. **场景分化**: 不同用户使用不同子集
3. **复用需求**: 部分能力需要独立复用
4. **维护成本**: 单技能难以维护和迭代

#### 拆分策略

##### 按功能模块拆分
```
原技能: data-processor (数据处理)
  ├─ 拆分为: data-cleaner (数据清洗)
  │           - 能力: 缺失值处理、去重、格式标准化
  ├─ 拆分为: data-transformer (数据转换)
  │           - 能力: 字段映射、类型转换、聚合计算
  └─ 拆分为: data-validator (数据验证)
              - 能力: 格式检查、规则验证、质量评分
```

##### 按使用场景拆分
```
原技能: content-processor (内容处理)
  ├─ 拆分为: batch-processor (批处理模式)
  │           - 场景: 大批量文件处理
  │           - 特点: 异步、可恢复、资源优化
  └─ 拆分为: real-time-processor (实时处理模式)
              - 场景: 实时流处理
              - 特点: 低延迟、流式、事件驱动
```

##### 按复杂度拆分
```
原技能: image-editor (图像编辑)
  ├─ 拆分为: image-basic-editor (基础编辑)
  │           - 能力: 裁剪、旋转、调整亮度
  │           - 复杂度: 低
  └─ 拆分为: image-advanced-editor (高级编辑)
              - 能力: 滤镜、图层、特效
              - 复杂度: 高
```

#### 拆分后协作关系

##### 松耦合协作
```
data-cleaner 和 data-analyzer 独立存在
用户可单独使用 data-cleaner
也可先使用 data-cleaner，再使用 data-analyzer
```

##### 紧耦合协作
```
data-cleaner 的输出格式与 data-analyzer 的输入格式匹配
data-analyzer 依赖 data-cleaner 的特定输出字段
需要在文档中明确接口契约
```

### 组合与拆分最佳实践

#### 组合时
1. **能力去重**: 识别并合并重复能力
2. **接口统一**: 设计统一的输入输出接口
3. **错误处理**: 设计整体的错误传播机制
4. **文档完整**: 说明组合逻辑和各技能角色

#### 拆分时
1. **单一职责**: 每个新技能聚焦一个核心能力
2. **独立可用**: 确保每个技能有独立使用价值
3. **接口清晰**: 定义技能间的调用接口
4. **依赖明确**: 明确技能间的依赖关系

#### 检查清单
- [ ] 整合后技能能力互补，无重大冲突
- [ ] 拆分后每个技能有独立使用价值
- [ ] 接口定义清晰，数据格式一致
- [ ] 组合/拆分逻辑文档化
- [ ] 版本管理策略明确
