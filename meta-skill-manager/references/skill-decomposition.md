# 技能拆分

## 目录
- [概述](#概述)
- [拆分策略](#拆分策略)
- [拆分流程](#拆分流程)
- [拆分模式详解](#拆分模式详解)
- [接口重构](#接口重构)
- [最佳实践](#最佳实践)

## 概述
技能拆分是将复杂技能分解为多个独立、可复用的单一职责技能的过程。

### 拆分目标
1. **降低复杂度**: 将复杂技能拆分为简单、易理解的单元
2. **提高复用性**: 每个拆分后的技能可独立使用
3. **优化维护**: 独立更新和迭代，降低维护成本
4. **清晰边界**: 明确每个技能的能力边界

### 适用场景
- 技能包含过多能力，职责不清晰
- 不同用户使用技能的不同子集
- 部分能力需要独立复用
- 技能难以维护和迭代

### 拆分原则
1. **单一职责**: 每个新技能聚焦一个核心能力
2. **独立可用**: 每个技能有独立的使用价值
3. **接口清晰**: 定义明确的输入输出接口
4. **低耦合**: 技能间依赖最小化

## 拆分策略

### 何时拆分

| 信号 | 说明 | 建议行动 |
|------|------|---------|
| 能力过多 | 超过 5-7 个核心能力 | 考虑拆分 |
| 场景分化 | 不同用户使用不同功能 | 按场景拆分 |
| 复用需求 | 部分功能被其他技能复用 | 提取为独立技能 |
| 维护困难 | 修改一处影响多处 | 解耦拆分 |
| 测试复杂 | 测试覆盖困难 | 拆分为可独立测试单元 |

### 拆分策略选择

#### 策略 1: 按功能模块拆分
将技能按功能模块分离，每个模块成为一个独立技能。

**适用场景**:
- 技能包含多个独立的功能模块
- 模块间耦合度低
- 模块有独立的使用价值

**示例**:
```
原技能: data-processor（数据处理）
  ├─ 拆分为: data-cleaner（数据清洗）
  │           - 能力: 缺失值处理、去重、格式标准化
  ├─ 拆分为: data-transformer（数据转换）
  │           - 能力: 字段映射、类型转换、聚合计算
  └─ 拆分为: data-validator（数据验证）
              - 能力: 格式检查、规则验证、质量评分
```

#### 策略 2: 按使用场景拆分
将技能按不同的使用场景分离，每种场景成为一个独立技能。

**适用场景**:
- 技能支持多种使用模式
- 不同场景有不同的性能要求
- 场景间差异明显

**示例**:
```
原技能: content-processor（内容处理）
  ├─ 拆分为: batch-processor（批处理模式）
  │           - 场景: 大批量文件处理
  │           - 特点: 异步、可恢复、资源优化
  └─ 拆分为: real-time-processor（实时处理模式）
              - 场景: 实时流处理
              - 特点: 低延迟、流式、事件驱动
```

#### 策略 3: 按复杂度拆分
将技能按复杂度分离，区分基础功能和高级功能。

**适用场景**:
- 技能同时包含简单和复杂功能
- 用户群体差异大（新手 vs 专家）
- 需要渐进式功能暴露

**示例**:
```
原技能: image-editor（图像编辑）
  ├─ 拆分为: image-basic-editor（基础编辑）
  │           - 用户: 普通用户
  │           - 能力: 裁剪、旋转、调整亮度
  │           - 复杂度: 低
  └─ 拆分为: image-advanced-editor（高级编辑）
              - 用户: 专业用户
              - 能力: 滤镜、图层、特效、批处理
              - 复杂度: 高
```

### 策略对比

| 策略 | 拆分维度 | 适用场景 | 优点 | 挑战 |
|------|---------|---------|------|------|
| 功能模块 | 功能边界 | 模块独立 | 职责清晰 | 需要协调接口 |
| 使用场景 | 使用模式 | 场景差异大 | 针对性强 | 可能有重复代码 |
| 复杂度 | 功能难度 | 用户差异大 | 渐进学习 | 能力边界模糊 |

## 拆分流程

### 流程概览
```
分析原技能 → 识别拆分点 → 设计拆分方案 → 重构接口 → 生成新技能
```

### 详细步骤

#### 步骤 1: 分析原技能

**1.1 提取能力清单**

从 SKILL.md 中提取所有能力：
```yaml
原技能: data-processor
核心能力:
  - 数据读取（支持 CSV、JSON、Excel）
  - 数据清洗（缺失值处理、去重）
  - 数据转换（字段映射、类型转换）
  - 数据分析（统计计算、趋势识别）
  - 数据验证（格式检查、规则验证）
  - 报告生成（统计报告、可视化）
  - 数据导出（支持多种格式）
```

**1.2 分析能力依赖关系**

识别能力间的依赖：
```
数据读取 → 数据清洗 → 数据转换 → 数据分析 → 报告生成
                ↓
          数据验证（依赖清洗后的数据）
                ↓
          数据导出（依赖处理后的数据）
```

**1.3 评估拆分可行性**

对于每个能力，评估：
- 是否可以独立运行？
- 是否有独立的使用价值？
- 与其他能力的耦合度？
- 拆分后的维护成本？

#### 步骤 2: 识别拆分点

**2.1 功能模块拆分点识别**

识别独立的功能模块：
```
data-processor 功能模块:
  ├─ 输入模块: 数据读取
  ├─ 处理模块: 数据清洗、数据转换
  ├─ 分析模块: 数据分析
  ├─ 验证模块: 数据验证
  └─ 输出模块: 报告生成、数据导出
```

**2.2 使用场景拆分点识别**

识别不同的使用场景：
```
data-processor 使用场景:
  ├─ 场景 A: 数据预处理（清洗 + 转换）
  ├─ 场景 B: 数据分析（分析 + 报告）
  └─ 场景 C: 数据质量控制（验证 + 报告）
```

**2.3 确定拆分粒度**

粒度选择原则：
- **过小**: 技能过于碎片化，使用复杂
- **过大**: 拆分价值不明显，复杂度未降低
- **适中**: 每个技能有 2-4 个核心能力

#### 步骤 3: 设计拆分方案

**3.1 确定新技能数量和定位**

拆分方案设计：
```
原技能: data-processor

拆分方案:
  ├─ data-reader: 数据读取专家
  │   - 职责: 专注数据读取和解析
  │   - 能力: 支持多种格式的数据读取
  │
  ├─ data-cleaner: 数据清洗专家
  │   - 职责: 专注数据清洗和预处理
  │   - 能力: 缺失值处理、去重、格式标准化
  │
  ├─ data-transformer: 数据转换专家
  │   - 职责: 专注数据转换和映射
  │   - 能力: 字段映射、类型转换、聚合计算
  │
  ├─ data-analyzer: 数据分析专家
  │   - 职责: 专注数据分析和洞察
  │   - 能力: 统计分析、趋势识别、异常检测
  │
  └─ data-exporter: 数据导出专家
      - 职责: 专注数据输出和报告
      - 能力: 报告生成、可视化、多格式导出
```

**3.2 分配能力和资源**

能力分配表：
| 新技能 | 分配能力 | 分配资源 |
|--------|---------|---------|
| data-reader | 数据读取 | 格式解析器、连接驱动 |
| data-cleaner | 数据清洗 | 清洗规则、模板 |
| data-transformer | 数据转换 | 映射表、转换器 |
| data-analyzer | 数据分析 | 分析算法、统计库 |
| data-exporter | 数据导出 | 报告模板、导出器 |

**3.3 设计技能协作关系**

定义技能间的调用关系：
```
data-reader → data-cleaner → data-transformer → data-analyzer → data-exporter
                 ↓
            data-validator（可选）
```

#### 步骤 4: 重构接口

**4.1 设计每个新技能的接口**

为每个新技能设计独立的输入输出接口：

**data-cleaner 接口**:
```yaml
input:
  data: "原始数据"
  cleaning_rules:
    - handle_missing: "策略（drop/fill/mean）"
    - remove_duplicates: true/false
    - standardize_format: true/false

output:
  cleaned_data: "清洗后的数据"
  cleaning_report:
    - removed_duplicates: <数量>
    - filled_missing: <数量>
    - quality_score: <评分>
```

**4.2 定义技能间调用契约**

明确技能间的调用约定：
```yaml
契约:
  reader_to_cleaner:
    caller: data-reader
    callee: data-cleaner
    data_format: json
    required_fields: [data, metadata]
  
  cleaner_to_transformer:
    caller: data-cleaner
    callee: data-transformer
    data_format: json
    required_fields: [cleaned_data, cleaning_report]
```

**4.3 处理数据格式转换**

定义必要的格式转换规则：
```
data-reader 输出格式: {data: [...], metadata: {...}}
data-cleaner 输入格式: {data: [...], rules: {...}}
转换: 提取 data 字段，添加 rules 参数
```

#### 步骤 5: 生成新技能

**5.1 为每个新技能创建 SKILL.md**

data-cleaner 示例：
```markdown
---
name: data-cleaner
description: 数据清洗专家，专注数据预处理和质量问题修复；当用户需要清洗原始数据时使用
metadata:
  capabilities: [数据清洗, 缺失值处理, 去重, 格式标准化]
  split_from: data-processor
  version: "1.0.0"
---

# Data Cleaner

## 任务目标
- 本 Skill 用于: 清洗和预处理原始数据
- 能力包含: 缺失值处理、重复数据去除、格式标准化
- 触发条件: 当用户获得原始数据需要预处理时使用

## 操作步骤
- 标准流程:
  1. 接收原始数据和清洗规则
  2. 处理缺失值（根据策略）
  3. 去除重复数据
  4. 标准化数据格式
  5. 生成清洗报告
- 可选分支:
  - 当 数据量 > 100万条: 使用批处理模式
  - 当 包含敏感数据: 执行脱敏处理

## 资源索引
- 清洗规则参考: [references/cleaning-rules.md](references/cleaning-rules.md)

## 注意事项
- 清洗前建议备份原始数据
- 清洗规则应根据数据特点调整

## 使用示例
- 示例: 清洗销售数据，处理缺失的订单金额和重复记录
```

**5.2 更新原技能（可选）**

保留原技能作为组合入口：
```markdown
---
name: data-processor
description: 数据处理套件（已拆分为独立技能）；当需要端到端处理时使用
metadata:
  deprecated: true
  replaced_by: [data-reader, data-cleaner, data-transformer, data-analyzer, data-exporter]
  migration_guide: references/migration-guide.md
---

# Data Processor (已拆分)

## 说明
本技能已拆分为以下独立技能：
- data-reader: 数据读取
- data-cleaner: 数据清洗
- data-transformer: 数据转换
- data-analyzer: 数据分析
- data-exporter: 数据导出

建议使用独立技能以获得更好的灵活性和可维护性。

## 迁移指南
参见 [references/migration-guide.md](references/migration-guide.md)
```

**5.3 创建迁移指南**

帮助用户从原技能迁移到新技能：
```markdown
# 迁移指南: data-processor → 独立技能

## 原用法
```
data-processor.process(file, options)
```

## 新用法
```
data = data-reader.read(file)
cleaned = data-cleaner.clean(data, cleaning_options)
transformed = data-transformer.transform(cleaned, mapping)
analyzed = data-analyzer.analyze(transformed)
report = data-exporter.export(analyzed, format)
```

## 能力映射表
| 原能力 | 新技能 | 新方法 |
|--------|--------|--------|
| 读取 CSV | data-reader | read_csv() |
| 清洗数据 | data-cleaner | clean() |
| 转换格式 | data-transformer | transform() |
```

## 拆分模式详解

### 模式 1: 完全拆分

**定义**: 将原技能完全拆分为多个独立技能，原技能废弃。

**适用场景**:
- 原技能过于复杂，维护困难
- 各能力间耦合度低
- 需要完全独立的技能

**结构**:
```
原技能 A（废弃）
  ├─ 新技能 A1（独立）
  ├─ 新技能 A2（独立）
  └─ 新技能 A3（独立）
```

**优点**:
- 完全解耦，维护简单
- 清晰的单一职责
- 灵活组合

**挑战**:
- 用户需要学习多个新技能
- 需要迁移指南

### 模式 2: 保留门面

**定义**: 保留原技能作为门面（Facade），内部调用拆分后的新技能。

**适用场景**:
- 原技能有较多现有用户
- 需要向后兼容
- 简化用户使用

**结构**:
```
原技能 A（门面）
  ├─ 调用 新技能 A1
  ├─ 调用 新技能 A2
  └─ 调用 新技能 A3
```

**实现**:
```markdown
# Data Processor（门面模式）

## 说明
本技能现在作为门面，内部调用以下独立技能：
- data-reader
- data-cleaner
- data-transformer
- data-analyzer
- data-exporter

## 使用方式
可以直接使用本技能（保持原有接口），也可以使用独立技能获得更精细的控制。
```

**优点**:
- 向后兼容
- 用户无感知迁移
- 渐进式采用新技能

**挑战**:
- 需要维护门面层
- 可能隐藏新技能的灵活性

### 模式 3: 分层拆分

**定义**: 按层次拆分，底层技能提供基础能力，上层技能提供组合能力。

**适用场景**:
- 技能有明显的高低层次
- 基础能力需要复用
- 需要多种组合方式

**结构**:
```
高层技能（业务层）
  ├─ 调用 底层技能 A
  └─ 调用 底层技能 B

底层技能（基础层）
  ├─ 基础技能 A1
  ├─ 基础技能 A2
  └─ 基础技能 B1
```

**示例**:
```
业务层:
  - sales-report-generator: 销售报告生成
  - marketing-analyzer: 营销分析器

基础层:
  - data-reader: 数据读取
  - data-cleaner: 数据清洗
  - data-visualizer: 数据可视化
```

## 接口重构

### 接口设计原则

1. **单一入口**: 每个技能有清晰的主要入口
2. **参数明确**: 参数命名清晰，有默认值
3. **输出完整**: 输出包含结果和元数据
4. **错误规范**: 统一的错误码和消息

### 接口契约示例

**data-cleaner 完整接口**:
```yaml
技能: data-cleaner

输入接口:
  data:
    type: array/object
    description: "原始数据"
    required: true
  
  options:
    type: object
    description: "清洗选项"
    required: false
    default: {}
    properties:
      missing_value_strategy:
        type: string
        enum: [drop, fill, mean, median, mode]
        default: "drop"
      
      remove_duplicates:
        type: boolean
        default: true
      
      standardize_format:
        type: boolean
        default: true

输出接口:
  cleaned_data:
    type: array/object
    description: "清洗后的数据"
  
  report:
    type: object
    properties:
      original_count: integer
      cleaned_count: integer
      removed_duplicates: integer
      filled_missing: integer
      quality_score: number
  
  errors:
    type: array
    description: "错误列表（如有）"
```

## 最佳实践

### 拆分前
- **充分分析**: 深入理解原技能的能力和依赖
- **明确目标**: 清晰定义拆分后的预期收益
- **评估成本**: 评估拆分和迁移成本

### 拆分中
- **渐进拆分**: 分阶段拆分，降低风险
- **保持兼容**: 尽量保持接口兼容性
- **完整文档**: 详细记录拆分方案和迁移指南

### 拆分后
- **独立验证**: 每个新技能独立测试
- **组合测试**: 测试技能间的协作
- **用户支持**: 提供迁移支持和示例

### 检查清单
- [ ] 充分分析了原技能的能力清单
- [ ] 识别了合适的拆分点和粒度
- [ ] 设计了清晰的拆分方案
- [ ] 为每个新技能定义了独立接口
- [ ] 定义了技能间的调用契约
- [ ] 生成了完整的新技能文档
- [ ] 提供了迁移指南（如需要）
- [ ] 更新了原技能说明（如保留）
