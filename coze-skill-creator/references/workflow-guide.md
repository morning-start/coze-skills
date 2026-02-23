# 工作流编排指南

## 概览
工作流是 Skill 中多个工具和脚本协同执行的流程定义。本指南说明如何设计和实现工作流。

## 目录
- [节点类型](#节点类型)
- [连接规则](#连接规则)
- [数据流转](#数据流转)
- [条件分支](#条件分支)
- [错误处理](#错误处理)
- [设计示例](#设计示例)

## 节点类型

### 1. 开始节点 (Start)
工作流的唯一入口，接收初始输入数据。

**配置**:
```json
{
  "type": "start",
  "id": "start",
  "outputs": ["input_data"]
}
```

### 2. 工具节点 (Tool)
调用预定义的工具或脚本。

**配置**:
```json
{
  "type": "tool",
  "id": "tool_1",
  "tool_name": "compress",
  "inputs": {
    "file_path": "$.input_data.file",
    "quality": 80
  },
  "outputs": ["result"]
}
```

### 3. 条件节点 (Condition)
根据条件判断执行不同分支。

**配置**:
```json
{
  "type": "condition",
  "id": "check_format",
  "expression": "$.file_type == 'image'",
  "branches": {
    "true": ["process_image"],
    "false": ["process_text"]
  }
}
```

### 4. 循环节点 (Loop)
遍历数组或重复执行。

**配置**:
```json
{
  "type": "loop",
  "id": "process_files",
  "iterable": "$.files",
  "item_var": "file",
  "body": ["process_single"]
}
```

### 5. 结束节点 (End)
工作流的唯一出口，返回最终结果。

**配置**:
```json
{
  "type": "end",
  "id": "end",
  "inputs": ["$.result"]
}
```

## 连接规则

### 基本规则
1. 工作流必须有且仅有一个开始节点和一个结束节点
2. 节点之间的连接形成有向无环图（DAG）
3. 每个节点必须有至少一个前置节点（除了开始节点）
4. 每个节点必须有至少一个后置节点（除了结束节点）

### 数据传递
使用 JSONPath 引用上游节点的输出数据。

**示例**:
```json
{
  "id": "node_b",
  "inputs": {
    "data": "$.node_a.output",
    "timestamp": "$.start.time"
  }
}
```

## 数据流转

### 单向流转
数据从上游节点流向下游节点，不可回溯。

**示例**:
```
[start] → [parse] → [validate] → [process] → [end]
```

### 分支合并
多个分支在条件节点后合并到同一个节点。

**示例**:
```
[start] → [condition]
              ├→ [branch_a] ─┐
              └→ [branch_b] ──┤
                             ↓→ [merge] → [end]
```

## 条件分支

### 简单条件
基于单一布尔表达式。

```json
{
  "expression": "$.size > 1024"
}
```

### 复合条件
使用逻辑运算符组合多个条件。

```json
{
  "expression": "$.type == 'image' AND $.size < 1048576"
}
```

### 多路分支
根据表达式值匹配不同分支。

```json
{
  "type": "switch",
  "expression": "$.status",
  "cases": {
    "200": ["handle_success"],
    "404": ["handle_not_found"],
    "500": ["handle_error"]
  },
  "default": ["handle_unknown"]
}
```

## 错误处理

### Try-Catch 块
捕获工具节点执行过程中的异常。

```json
{
  "type": "try_catch",
  "id": "safe_process",
  "try": ["risky_operation"],
  "catch": {
    "error": ["handle_error"]
  }
}
```

### 重试机制
失败时自动重试指定次数。

```json
{
  "type": "tool",
  "retry": {
    "max_attempts": 3,
    "delay": 1000
  }
}
```

### 超时控制
设置节点执行的超时时间。

```json
{
  "type": "tool",
  "timeout": 30000
}
```

## 设计示例

### 示例 1: 线性流程
**场景**: 图片压缩工作流

```
[start] → [upload] → [compress] → [download] → [end]
```

**配置**:
```json
{
  "name": "image-compress-workflow",
  "nodes": [
    {"type": "start", "id": "start"},
    {"type": "tool", "id": "upload", "tool_name": "upload_image"},
    {"type": "tool", "id": "compress", "tool_name": "compress", "inputs": {"quality": 80}},
    {"type": "tool", "id": "download", "tool_name": "download_image"},
    {"type": "end", "id": "end"}
  ],
  "connections": [
    ["start", "upload"],
    ["upload", "compress"],
    ["compress", "download"],
    ["download", "end"]
  ]
}
```

### 示例 2: 条件分支
**场景**: 根据文件类型处理

```
[start] → [detect_type] → [condition]
                              ├→ [process_image] → [end]
                              └→ [process_text] → [end]
```

**配置**:
```json
{
  "name": "file-processor-workflow",
  "nodes": [
    {"type": "start", "id": "start"},
    {"type": "tool", "id": "detect_type", "tool_name": "detect_type"},
    {
      "type": "condition",
      "id": "check_type",
      "expression": "$.type == 'image'",
      "branches": {
        "true": ["process_image"],
        "false": ["process_text"]
      }
    },
    {"type": "tool", "id": "process_image", "tool_name": "process_image"},
    {"type": "tool", "id": "process_text", "tool_name": "process_text"},
    {"type": "end", "id": "end"}
  ],
  "connections": [
    ["start", "detect_type"],
    ["detect_type", "check_type"],
    ["process_image", "end"],
    ["process_text", "end"]
  ]
}
```

### 示例 3: 循环处理
**场景**: 批量处理多个文件

```
[start] → [list_files] → [loop] → [process] → [end]
                              ↑___|
```

**配置**:
```json
{
  "name": "batch-processor-workflow",
  "nodes": [
    {"type": "start", "id": "start"},
    {"type": "tool", "id": "list_files", "tool_name": "list_files"},
    {
      "type": "loop",
      "id": "process_loop",
      "iterable": "$.files",
      "body": ["process_single"]
    },
    {"type": "tool", "id": "process_single", "tool_name": "process_single"},
    {"type": "end", "id": "end"}
  ],
  "connections": [
    ["start", "list_files"],
    ["list_files", "process_loop"],
    ["process_single", "end"]
  ]
}
```

## 最佳实践

1. **保持简单**: 优先使用线性流程，仅在必要时使用分支和循环
2. **明确命名**: 节点 ID 应清晰表达其功能
3. **错误处理**: 为关键节点添加重试和超时配置
4. **数据验证**: 在条件节点前验证数据格式
5. **性能优化**: 并行执行无依赖关系的节点
6. **文档完善**: 为复杂工作流编写说明文档

## 工作流验证

在生成技能前，使用以下检查清单验证工作流设计:

- [ ] 是否有且仅有一个开始节点和一个结束节点
- [ ] 节点连接是否形成有向无环图（DAG）
- [ ] 所有 JSONPath 引用是否有效
- [ ] 条件表达式语法是否正确
- [ ] 循环节点是否有终止条件
- [ ] 错误处理是否完善
- [ ] 数据流转逻辑是否清晰
