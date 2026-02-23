---
name: {{ skill_name }}
description: {{ description }}
dependency:
  python:
    - pandas>=1.5.0
    - numpy>=1.23.0
---

# {{ skill_title }}

## 任务目标
- 本 Skill 用于：处理 {{ data_type }} 数据，实现 {{ processing_goal }}
- 能力包含：{{ core_features }}
- 触发条件：当用户需要 {{ trigger_conditions }}

## 前置准备
- 依赖说明：scripts 脚本所需的依赖包及版本
  ```
  pandas>=1.5.0
  numpy>=1.23.0
  ```
- 数据准备：确保输入数据符合格式要求

## 操作步骤

### 标准流程
1. 数据读取与验证
   - 读取输入文件（CSV/JSON/Excel）
   - 验证数据格式和完整性
   - 处理缺失值和异常值

2. 数据处理
   - 调用 `scripts/data_processor.py` 执行处理逻辑
   - 应用数据转换规则
   - 执行计算和分析

3. 结果导出
   - 格式化输出结果
   - 导出为目标格式（CSV/JSON/Excel）
   - 生成处理报告

### 可选分支
- 当数据量大：使用分批处理模式
- 当需要清洗：执行数据清洗流程
- 当需要转换：执行格式转换

## 资源索引

### 必要脚本
- [scripts/data_processor.py](scripts/data_processor.py)
  - 用途：处理和分析数据
  - 参数：--input（输入文件）、--output（输出目录）、--config（配置文件）
  - 输入：数据文件（CSV/JSON/Excel）
  - 输出：处理结果文件

### 领域参考
- [references/data-format.md](references/data-format.md)
  - 何时读取：需要了解数据格式规范
  - 内容：输入格式、输出格式、字段说明
- [references/processing-rules.md](references/processing-rules.md)
  - 何时读取：需要了解处理规则
  - 内容：转换规则、计算逻辑、验证规则

## 注意事项

### 数据质量
- 验证输入数据格式
- 处理缺失值策略
- 异常值检测和处理

### 性能优化
- 大数据集使用分批处理
- 向量化操作提高效率
- 内存管理避免溢出

### 错误处理
- 数据格式错误提示
- 处理失败回滚机制
- 详细的错误日志

## 使用示例

### 示例 1：基础处理
- 功能说明：读取 CSV 文件，执行基础转换
- 执行方式：脚本调用
- 关键参数：
  ```python
  python scripts/data_processor.py \
    --input data.csv \
    --output output.csv \
    --transform normalize
  ```

### 示例 2：复杂转换
- 功能说明：执行多步骤数据转换
- 执行方式：脚本调用
- 关键参数：
  ```python
  python scripts/data_processor.py \
    --input data.json \
    --output result.xlsx \
    --config config.json \
    --steps clean,transform,aggregate
  ```
