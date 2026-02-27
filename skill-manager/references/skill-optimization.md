# 技能优化

## 目录
- [概述](#概述)
- [优化策略](#优化策略)
  - [技能原子化](#1-技能原子化)
  - [标准化接口](#2-标准化输入输出接口)
  - [元数据增强](#3-技能元数据增强)
  - [分层抽象](#4-技能分层抽象)
  - [组合模板](#5-预定义技能组合模板)
  - [版本控制](#6-技能版本控制)
  - [错误处理标准化](#7-错误处理标准化)
  - [依赖显式声明](#8-技能依赖显式声明)
  - [性能标注](#9-性能与资源标注)
  - [文档内嵌](#10-文档与示例内嵌)
- [优化流程](#优化流程)
- [最佳实践](#最佳实践)

## 概述
技能优化是应用设计模式和最佳实践，提升技能的设计质量、复用性、可组合性和可维护性的过程。

### 优化目标
1. **提升复用性**: 通过原子化和标准化接口，使技能易于复用
2. **增强可组合性**: 通过清晰的接口和分层设计，支持灵活组合
3. **改善可维护性**: 通过元数据、版本控制和文档，降低维护成本
4. **提高可靠性**: 通过标准化错误处理和依赖声明，减少运行时失败

### 核心原则
1. **静态定义**: 所有优化信息在技能注册时确定，不依赖运行时反馈
2. **结构清晰**: 通过规范化的结构提升系统可预测性
3. **人机协同友好**: 既便于程序解析，也便于开发者理解

## 优化策略

### 1. 技能原子化

#### 定义
将每个技能拆解为最小、不可再分的功能单元。每个原子技能只做一件事，做好一件事。

#### 优点
- **提高复用性**: 原子技能可被多种场景复用
- **降低耦合**: 技能间依赖最小化
- **便于测试**: 单一职责易于单元测试
- **灵活组合**: 通过组合原子技能构建复杂功能

#### 反模式 vs 优化示例

❌ **不好的设计**:
```yaml
name: order-processor
description: 处理用户订单，包括解析、验证、支付等
capabilities: [订单处理]
# 问题：职责过多，难以复用
```

✅ **优化后的原子技能**:
```yaml
name: parse-order
description: 解析订单内容，提取订单字段
capabilities: [订单解析]

---

name: validate-inventory
description: 验证库存是否满足订单需求
capabilities: [库存验证]

---

name: generate-payment-link
description: 生成支付链接
capabilities: [支付链接生成]
```

#### 实施步骤
1. 识别技能中的多个职责
2. 评估每个职责的独立性
3. 将独立职责提取为原子技能
4. 设计原子技能间的协作接口
5. 创建组合技能（如需保留原功能）

### 2. 标准化输入输出接口

#### 定义
为所有技能定义统一的输入格式和输出格式，使用 JSON Schema 显式声明接口契约。

#### 优点
- **便于串联**: 技能间输入输出格式统一，易于串联
- **自动化调度**: 支持自动化的技能发现和调度
- **类型安全**: 明确的类型定义，减少运行时错误
- **文档清晰**: 接口即文档，降低使用门槛

#### 实施规范

**输入接口声明**:
```yaml
metadata:
  input_schema:
    type: object
    required: [order_id, items]
    properties:
      order_id:
        type: string
        description: "订单唯一标识"
      items:
        type: array
        description: "订单项列表"
        items:
          type: object
          properties:
            product_id:
              type: string
            quantity:
              type: integer
              minimum: 1
      options:
        type: object
        description: "可选配置"
        properties:
          priority:
            type: string
            enum: [high, normal, low]
            default: "normal"
```

**输出接口声明**:
```yaml
metadata:
  output_schema:
    type: object
    required: [success, data]
    properties:
      success:
        type: boolean
        description: "操作是否成功"
      data:
        type: object
        description: "输出数据（成功时）"
      error:
        type: object
        description: "错误信息（失败时）"
        properties:
          code:
            type: string
          message:
            type: string
          details:
            type: object
```

#### 验证规则
- 所有必需字段必须提供
- 字段类型必须匹配
- 枚举值必须在允许范围内
- 数值必须在约束范围内

### 3. 技能元数据增强

#### 定义
为每个技能附加丰富的描述性元数据，支持智能规划器更智能地选择技能。

#### 元数据字段

```yaml
metadata:
  # 基础信息
  description: "技能功能描述"
  version: "1.0.0"
  
  # 使用场景
  use_cases:
    - "电商订单处理"
    - "库存管理系统"
    - "供应链自动化"
  
  # 前置条件
  preconditions:
    - "订单数据格式正确"
    - "库存系统可访问"
    - "用户已认证"
  
  # 后置效果
  posteffects:
    - "库存数量减少"
    - "订单状态更新"
    - "通知邮件发送"
  
  # 成本估计
  cost_estimate:
    time: "2-5秒"
    tokens: "500-1000"
    api_calls: 3
  
  # 可靠性等级
  reliability_score: 0.95  # 0-1
  
  # 能力标签
  tags: [电商, 订单, 库存, 支付]
  
  # 作者信息
  author: "team-commerce"
  created_at: "2024-01-15"
  updated_at: "2024-02-20"
```

#### 元数据用途
- **技能发现**: 通过 use_cases 和 tags 快速定位技能
- **前置检查**: 验证 preconditions 是否满足
- **成本预估**: 评估 cost_estimate 决定是否使用
- **可靠性评估**: 根据 reliability_score 选择最优技能
- **影响分析**: 通过 posteffects 评估副作用

### 4. 技能分层抽象

#### 定义
构建技能层级结构，兼顾灵活性与高层语义表达。

#### 三层架构

```
高层：任务导向技能（面向具体业务目标）
  ├─ order-management-suite（订单管理套件）
  ├─ customer-service-bot（客服机器人）
  └─ data-analysis-pipeline（数据分析管道）

中层：复合技能（由多个原子技能按固定流程组成）
  ├─ composite-order-processor（订单处理复合技能）
  ├─ inventory-checker（库存检查器）
  └─ payment-workflow（支付工作流）

底层：原子操作（基础功能单元）
  ├─ parse-order（解析订单）
  ├─ validate-inventory（验证库存）
  ├─ generate-payment-link（生成支付链接）
  ├─ call-api（调用 API）
  └─ read-file（读取文件）
```

#### 分层原则

**底层（原子技能）**:
- 最小功能单元
- 无状态，幂等
- 高度可复用
- 接口简单明确

**中层（复合技能）**:
- 组合原子技能
- 定义固定流程
- 处理特定场景
- 可配置参数

**高层（任务技能）**:
- 面向业务目标
- 集成多个复合技能
- 提供完整解决方案
- 易于使用

#### 实施示例

```yaml
# 底层原子技能
name: parse-order
description: 解析订单内容
layer: atomic

# 中层复合技能
name: composite-order-processor
description: 订单处理复合技能
capabilities: [订单解析, 库存验证, 支付生成]
layer: composite
composition:
  type: sequential
  steps:
    - skill: parse-order
    - skill: validate-inventory
    - skill: generate-payment-link

# 高层任务技能
name: order-management-suite
description: 订单管理套件
capabilities: [订单处理, 订单查询, 订单取消]
layer: task
```

### 5. 预定义技能组合模板

#### 定义
预先定义常见技能组合模式，避免重复编写逻辑，提升开发效率。

#### 常用组合模板

**模板1: 顺序执行**
```yaml
template: sequential
structure: A → B → C
usage: 前一个技能的输出作为后一个技能的输入
example: 数据清洗 → 数据分析 → 报告生成
```

**模板2: 并行执行**
```yaml
template: parallel
structure: 
  input → [A, B, C] → merge → output
usage: 同时执行多个独立技能，合并结果
example: 同时分析情感、主题、关键词
```

**模板3: 条件分支**
```yaml
template: conditional
structure:
  input → condition
    ├─ [case A] → path A → output
    └─ [case B] → path B → output
usage: 根据条件选择执行路径
example: 根据内容类型选择处理器
```

**模板4: 故障转移**
```yaml
template: fallback
structure:
  try: primary-skill
  except: fallback-skill
usage: 主技能失败时使用备用技能
example: 主模型失败时使用简化模型
```

**模板5: 重试机制**
```yaml
template: retry
structure:
  attempt: skill
  max_retries: 3
  backoff: exponential
usage: 失败时自动重试
example: API 调用失败重试
```

#### DAG 表示
使用有向无环图描述复杂组合：
```yaml
composition:
  type: dag
  nodes:
    - id: A
      skill: parse-input
    - id: B
      skill: validate-data
    - id: C
      skill: process-data
    - id: D
      skill: generate-output
  edges:
    - from: A
      to: B
    - from: B
      to: C
    - from: C
      to: D
```

### 6. 技能版本控制

#### 定义
为每个技能打上版本号，记录变更日志，支持回滚和兼容性管理。

#### 语义化版本
```yaml
metadata:
  version: "2.1.3"
  # major.minor.patch
  # major: 破坏性变更
  # minor: 新增功能（向后兼容）
  # patch: 错误修复
```

#### 变更日志
```yaml
metadata:
  changelog:
    - version: "2.1.3"
      date: "2024-02-20"
      changes:
        - "修复：库存验证时的边界条件错误"
    - version: "2.1.0"
      date: "2024-02-15"
      changes:
        - "新增：支持批量订单处理"
        - "优化：提升验证速度 30%"
    - version: "2.0.0"
      date: "2024-01-20"
      changes:
        - "破坏性变更：接口字段重命名"
        - "迁移指南：参见 migration-guide.md"
```

#### 兼容性标记
```yaml
metadata:
  compatibility:
    backward_compatible: true  # 是否向后兼容
    deprecated: false          # 是否废弃
    replaced_by: null          # 替代技能
    sunset_date: null          # 停用日期
```

### 7. 错误处理标准化

#### 定义
每个技能明确声明可能的错误类型及恢复建议。

#### 错误声明
```yaml
metadata:
  error_codes:
    - code: "INVALID_INPUT"
      message: "输入数据格式错误"
      severity: "error"
      fallback_action: "返回错误提示，要求重新输入"
      
    - code: "INVENTORY_INSUFFICIENT"
      message: "库存不足"
      severity: "warning"
      fallback_action: "返回缺货信息，提供备选方案"
      
    - code: "API_TIMEOUT"
      message: "API 调用超时"
      severity: "error"
      fallback_action: "重试3次，仍失败则使用缓存数据"
      
    - code: "PAYMENT_FAILED"
      message: "支付失败"
      severity: "error"
      fallback_action: "提示用户检查支付方式，保留订单15分钟"
```

#### 严重级别定义
- **critical**: 系统级错误，必须立即处理
- **error**: 业务错误，操作失败
- **warning**: 警告，操作完成但有异常
- **info**: 信息性提示

#### 恢复策略类型
- **retry**: 重试（指定次数和间隔）
- **fallback**: 使用备用方案
- **skip**: 跳过此步骤，继续执行
- **abort**: 终止工作流
- **manual**: 转人工处理

### 8. 技能依赖显式声明

#### 定义
列出技能运行所依赖的外部资源，便于部署前校验环境完整性。

#### 依赖类型
```yaml
metadata:
  dependencies:
    # 外部服务
    services:
      - name: "inventory-api"
        endpoint: "https://api.inventory.com/v1"
        required: true
        
      - name: "payment-gateway"
        endpoint: "https://payment.example.com"
        required: true
    
    # 数据库
    databases:
      - name: "order-db"
        type: "postgresql"
        connection_string: "${ORDER_DB_URL}"
        required: true
    
    # 模型/API Key
    models:
      - name: "gpt-4"
        provider: "openai"
        api_key: "${OPENAI_API_KEY}"
        required: false
        fallback: "gpt-3.5-turbo"
    
    # 文件/目录
    filesystem:
      - path: "/data/orders"
        permission: "read/write"
        required: true
    
    # 环境变量
    env_vars:
      - name: "ORDER_SERVICE_URL"
        required: true
        
      - name: "MAX_RETRY_COUNT"
        default: "3"
```

#### 依赖检查
部署前自动检查：
- 服务是否可达
- 数据库连接是否正常
- API Key 是否有效
- 文件权限是否正确
- 环境变量是否设置

### 9. 性能与资源标注

#### 定义
静态标注技能的典型资源消耗，用于资源调度和负载均衡。

#### 性能指标
```yaml
metadata:
  performance:
    # 时间
    latency:
      typical: "2s"
      p50: "1.5s"
      p95: "5s"
      p99: "10s"
    
    # 计算资源
    compute:
      cpu: "0.5 cores"
      memory: "512MB"
      gpu: "none"
    
    # 网络
    network:
      bandwidth: "1MB/s"
      connections: 3
    
    # 成本
    cost:
      tokens: "500-1000"
      api_calls: 2
      price_estimate: "$0.02"
    
    # 并发
    concurrency:
      max_parallel: 10
      queue_size: 100
```

#### 资源调度用途
- **负载均衡**: 根据资源消耗分配任务
- **容量规划**: 预估系统承载能力
- **成本估算**: 计算运行成本
- **低功耗适配**: 为资源受限设备选择合适的技能

### 10. 文档与示例内嵌

#### 定义
每个技能包含使用示例和简明文档，降低使用门槛。

#### 示例内容
```yaml
metadata:
  examples:
    - title: "基本用法"
      description: "处理单个订单"
      input:
        order_id: "ORD-12345"
        items:
          - product_id: "SKU-001"
            quantity: 2
      output:
        success: true
        data:
          order_id: "ORD-12345"
          status: "confirmed"
          total: 199.98
    
    - title: "批量处理"
      description: "处理多个订单"
      input:
        orders:
          - order_id: "ORD-001"
            items: [...]
          - order_id: "ORD-002"
            items: [...]
      output:
        success: true
        data:
          processed: 2
          failed: 0
    
    - title: "错误处理"
      description: "库存不足的情况"
      input:
        order_id: "ORD-99999"
        items:
          - product_id: "SKU-OUT"
            quantity: 1000
      output:
        success: false
        error:
          code: "INVENTORY_INSUFFICIENT"
          message: "SKU-OUT 库存不足，当前库存：5"
```

#### 文档章节
```markdown
# Skill Name

## 快速开始
一句话描述 + 最简单的使用示例

## 功能说明
详细的功能描述和边界

## 参数说明
输入参数表格（名称、类型、必填、描述）

## 返回值
输出字段说明

## 错误处理
可能的错误和解决方案

## 使用示例
多个场景的完整示例

## 注意事项
重要提示和限制

## 更新日志
版本历史
```

## 优化流程

### 流程概览
```
评估现状 → 选择策略 → 设计优化方案 → 执行优化 → 验证效果
```

### 详细步骤

#### 步骤 1: 评估现状
1. **分析当前技能设计**
   - 检查是否遵循单一职责原则
   - 评估接口清晰度
   - 检查元数据完整性
   - 评估文档质量

2. **识别问题**
   - 职责过多？→ 需要原子化
   - 接口不清晰？→ 需要标准化
   - 元数据缺失？→ 需要增强
   - 文档不足？→ 需要补充示例

#### 步骤 2: 选择优化策略
根据问题选择合适的策略：
- 复杂度过高 → 原子化 + 分层抽象
- 接口不统一 → 标准化接口
- 难以理解 → 元数据增强 + 文档内嵌
- 难以组合 → 组合模板 + 分层抽象
- 可靠性问题 → 错误处理标准化 + 依赖显式声明

#### 步骤 3: 设计优化方案
1. 规划优化范围（哪些技能需要优化）
2. 确定优化顺序（先底层后高层）
3. 设计新接口（如需变更）
4. 规划迁移路径（如何平滑过渡）

#### 步骤 4: 执行优化
1. 更新技能定义（添加元数据、标准化接口）
2. 重构技能结构（原子化、分层）
3. 补充文档和示例
4. 更新版本和变更日志

#### 步骤 5: 验证效果
- [ ] 接口是否符合标准
- [ ] 元数据是否完整
- [ ] 示例是否可运行
- [ ] 文档是否清晰
- [ ] 向后兼容性（如适用）

## 最佳实践

### 组合使用策略
多种优化策略可以组合使用：

**新技能创建**:
- 原子化设计
- 标准化接口
- 元数据增强
- 文档内嵌

**复杂技能重构**:
- 原子化拆分
- 分层抽象
- 组合模板
- 依赖显式声明

**生产环境技能**:
- 版本控制
- 错误处理标准化
- 性能标注
- 依赖检查

### 优化检查清单
- [ ] 技能是否原子化？（单一职责）
- [ ] 接口是否标准化？（JSON Schema）
- [ ] 元数据是否完整？（场景、条件、成本、可靠性）
- [ ] 是否分层设计？（原子/复合/任务）
- [ ] 是否有组合模板？（顺序、并行、条件等）
- [ ] 版本是否管理？（语义化版本 + 变更日志）
- [ ] 错误是否标准化？（错误码 + 恢复策略）
- [ ] 依赖是否显式声明？（服务、数据库、API Key）
- [ ] 性能是否标注？（延迟、资源、成本）
- [ ] 文档是否内嵌？（示例、说明、注意事项）

### 关键原则总结
1. **静态定义**: 所有优化信息在技能注册时确定
2. **结构清晰**: 通过规范化结构提升可预测性
3. **人机协同**: 既便于程序解析，也便于开发者理解
4. **渐进优化**: 根据实际需求逐步应用优化策略
5. **向后兼容**: 优化时尽量保持向后兼容
