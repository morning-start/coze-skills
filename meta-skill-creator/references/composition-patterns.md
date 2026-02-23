# 技能组合模式

## 目录
- [组合模式概述](#组合模式概述)
- [顺序组合](#顺序组合)
- [并行组合](#并行组合)
- [嵌套组合](#嵌套组合)
- [流水线组合](#流水线组合)
- [组合最佳实践](#组合最佳实践)

## 概览
本文档定义了技能组合的四种标准模式，用于构建复杂、可维护的技能系统。

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
    ↓
Skill B (数据转换)
    ↓
Skill C (数据验证)
    ↓
输出
```

### 实现要点
1. 定义输入输出映射关系
2. 处理数据格式转换
3. 错误传播机制
4. 中间结果缓存（可选）

### 元数据定义
```yaml
metadata:
  composition_type: sequential
  component_skills: [skill-a, skill-b, skill-c]
  input_mapping:
    skill-b: skill-a.output
    skill-c: skill-b.output
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
输入
    ↓
├─→ Skill A (维度1分析)
├─→ Skill B (维度2分析)
└─→ Skill C (维度3分析)
    ↓
合并输出
```

### 实现要点
1. 定义输出合并策略（merge/concatenate/first）
2. 处理并行执行的依赖隔离
3. 统一错误处理
4. 结果聚合逻辑

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
父技能
  ├─ 步骤1
  ├─ 步骤2 → 调用子技能 A
  ├─ 步骤3
  └─ 步骤4 → 调用子技能 B
```

### 实现要点
1. 定义集成点（在父技能的哪个位置调用）
2. 参数传递机制
3. 子技能结果处理
4. 作用域隔离

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
  sub_skills: [sub-skill-a, sub-skill-b]
  integration_points:
    - step: step2
      skill: sub-skill-a
    - step: step4
      skill: sub-skill-b
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
    ↓ [提取]
Skill A (数据提取)
    ↓ [转换]
Skill B (数据转换)
    ↓ [标准化]
Skill C (数据标准化)
    ↓ [加载]
输出目标
```

### 实现要点
1. 定义数据流图
2. 每个阶段的输入输出契约
3. 阶段间的数据格式验证
4. 流水线监控和日志

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
        transforms:
          - remove_headers
          - filter_empty
      - name: transform
        skill: skill-b
        transforms:
          - normalize_dates
          - encode_categories
      - name: load
        skill: skill-c
        transforms:
          - validate_schema
    output:
      target: database
      format: json
```

## 组合最佳实践

### 接口设计
1. **标准化输入输出**: 使用 JSON 或 YAML 定义清晰的契约
2. **版本化接口**: 支持接口演进和向后兼容
3. **文档化**: 在 references/ 中提供接口规范

### 错误处理
1. **隔离错误**: 单个技能失败不应影响整个组合
2. **优雅降级**: 提供备选方案或默认值
3. **详细日志**: 记录错误上下文，便于调试

### 性能优化
1. **避免重复计算**: 利用缓存机制
2. **并行化**: 对独立的技能使用并行组合
3. **资源管理**: 控制并发数量，避免资源耗尽

### 可维护性
1. **模块化**: 每个技能应独立可测试
2. **文档化**: 记录组合逻辑和决策原因
3. **监控**: 添加性能指标和健康检查

### 组合检查清单
- [ ] 技能接口定义清晰
- [ ] 输入输出格式一致
- [ ] 错误处理机制完善
- [ ] 组合逻辑文档化
- [ ] 独立可测试
- [ ] 性能合理

## 示例场景

### 示例1: 数据分析报告生成
```yaml
组合模式: 流水线

技能列表:
  - data-fetcher (数据获取)
  - data-cleaner (数据清洗)
  - data-analyzer (数据分析)
  - report-generator (报告生成)

数据流:
  数据源 → 获取 → 清洗 → 分析 → 生成 → 报告
```

### 示例2: 多渠道内容分发
```yaml
组合模式: 并行

技能列表:
  - wechat-publisher (微信公众号发布)
  - email-publisher (邮件发送)
  - slack-publisher (Slack 通知)

合并策略: concatenate
说明: 收集所有渠道的发布结果，合并为统一报告
```

### 示例3: 智能客服系统
```yaml
组合模式: 嵌套

父技能: customer-service-router
子技能:
  - faq-matcher (FAQ 匹配)
  - intent-classifier (意图识别)
  - knowledge-retriever (知识检索)

集成点:
  - 用户输入 → 意图识别
  - 匹配 FAQ → 回答
  - 未匹配 → 知识检索
```
