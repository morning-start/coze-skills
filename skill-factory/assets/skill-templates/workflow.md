---
name: {{ skill_name }}
description: {{ description }}
dependency:
  python:
    - networkx>=3.0
  system:
    - echo "Workflow initialization"
---

# {{ skill_title }}

## 任务目标
- 本 Skill 用于：编排 {{ workflow_type }} 工作流，实现 {{ workflow_goal }}
- 能力包含：{{ core_features }}
- 触发条件：当用户需要 {{ trigger_conditions }}

## 前置准备
- 依赖说明：scripts 脚本所需的依赖包及版本
  ```
  networkx>=3.0
  ```
- 流程配置：准备工作流配置文件

## 操作步骤

### 标准流程
1. 流程解析与验证
   - 读取工作流配置文件
   - 验证任务定义和依赖关系
   - 检查资源可用性

2. 任务编排与执行
   - 调用 `scripts/workflow_executor.py` 执行工作流
   - 按依赖顺序执行任务
   - 处理任务间的数据传递

3. 结果汇总与报告
   - 收集所有任务执行结果
   - 生成执行报告
   - 处理失败任务

### 可选分支
- 当任务失败：执行重试或跳过策略
- 当需要并行：启用并行执行模式
- 当条件分支：执行条件判断逻辑

## 资源索引

### 必要脚本
- [scripts/workflow_executor.py](scripts/workflow_executor.py)
  - 用途：执行工作流任务
  - 参数：--workflow（工作流配置）、--parallel（并行模式）
  - 输入：工作流配置文件（JSON/YAML）
  - 输出：执行结果和报告

### 领域参考
- [references/workflow-spec.md](references/workflow-spec.md)
  - 何时读取：需要了解工作流配置格式
  - 内容：任务定义、依赖配置、参数说明
- [references/task-library.md](references/task-library.md)
  - 何时读取：需要了解可用任务类型
  - 内容：任务类型、参数说明、使用示例

## 注意事项

### 任务依赖
- 明确定义任务依赖关系
- 避免循环依赖
- 合理设置执行顺序

### 错误处理
- 任务失败处理策略（重试/跳过/中止）
- 错误信息收集和报告
- 失败任务的恢复机制

### 性能优化
- 并行执行无依赖任务
- 资源管理和分配
- 执行状态跟踪

## 使用示例

### 示例 1：简单顺序工作流
- 功能说明：执行简单的顺序任务
- 执行方式：脚本调用
- 配置文件：
  ```json
  {
    "tasks": [
      {"name": "task1", "action": "process"},
      {"name": "task2", "action": "validate"}
    ]
  }
  ```

### 示例 2：复杂依赖工作流
- 功能说明：执行复杂的多任务工作流
- 执行方式：脚本调用
- 配置文件：
  ```json
  {
    "tasks": [
      {
        "name": "prepare",
        "action": "download"
      },
      {
        "name": "process",
        "action": "transform",
        "depends_on": ["prepare"]
      },
      {
        "name": "validate",
        "action": "check",
        "depends_on": ["process"]
      }
    ],
    "parallel": true
  }
  ```

### 示例 3：条件分支工作流
- 功能说明：根据条件选择不同路径
- 执行方式：脚本调用
- 配置文件：
  ```json
  {
    "tasks": [
      {
        "name": "check",
        "action": "condition"
      },
      {
        "name": "branch_a",
        "action": "process_a",
        "condition": "${check.result} == 'A'"
      },
      {
        "name": "branch_b",
        "action": "process_b",
        "condition": "${check.result} == 'B'"
      }
    ]
  }
  ```
