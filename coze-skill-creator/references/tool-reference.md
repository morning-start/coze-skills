# 工具配置参考

## 概览
工具是 Skill 中可被调用的功能单元，包括 API 工具、脚本工具和插件工具。本指南说明如何配置和集成各种类型的工具。

## 目录
- [工具类型](#工具类型)
- [参数定义](#参数定义)
- [返回值定义](#返回值定义)
- [API 工具](#api-工具)
- [Python 脚本工具](#python-脚本工具)
- [Bash 脚本工具](#bash-脚本工具)
- [工具集成](#工具集成)
- [配置示例](#配置示例)

## 工具类型

### 1. API 工具 (api)
调用外部 HTTP API 服务。

**适用场景**:
- 调用第三方服务接口
- 集成 RESTful API
- 使用云服务功能

**配置**:
```json
{
  "name": "call_openai",
  "type": "api",
  "description": "调用 OpenAI GPT API",
  "endpoint": "https://api.openai.com/v1/chat/completions",
  "method": "POST",
  "auth": {
    "type": "bearer",
    "token": "${API_KEY}"
  },
  "headers": {
    "Content-Type": "application/json"
  },
  "parameters": [
    {
      "name": "messages",
      "type": "array",
      "required": true,
      "description": "对话消息列表"
    }
  ]
}
```

### 2. Python 脚本工具 (python)
执行 Python 函数或脚本。

**适用场景**:
- 数据处理和转换
- 文件格式操作
- 算法实现

**配置**:
```json
{
  "name": "process_data",
  "type": "python",
  "description": "处理输入数据",
  "script": "scripts/process.py",
  "function": "main",
  "parameters": [
    {
      "name": "input_data",
      "type": "object",
      "required": true,
      "description": "输入数据"
    }
  ]
}
```

### 3. Bash 脚本工具 (bash)
执行 Shell 命令。

**适用场景**:
- 系统级操作
- 文件管理
- 执行外部程序

**配置**:
```json
{
  "name": "run_command",
  "type": "bash",
  "description": "执行系统命令",
  "command": "python --version",
  "parameters": [
    {
      "name": "args",
      "type": "string",
      "required": false,
      "description": "命令参数"
    }
  ]
}
```

## 参数定义

### 参数类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `string` | 字符串 | `"hello"` |
| `integer` | 整数 | `123` |
| `number` | 浮点数 | `3.14` |
| `boolean` | 布尔值 | `true` |
| `object` | JSON 对象 | `{"key": "value"}` |
| `array` | JSON 数组 | `[1, 2, 3]` |

### 参数属性

```json
{
  "name": "param_name",
  "type": "string",
  "required": true,
  "default": "default_value",
  "description": "参数说明",
  "validation": {
    "pattern": "^[a-z]+$",
    "min_length": 1,
    "max_length": 100
  }
}
```

### 参数验证

- **pattern**: 正则表达式验证
- **min_length**: 最小长度（字符串/数组）
- **max_length**: 最大长度（字符串/数组）
- **minimum**: 最小值（数字）
- **maximum**: 最大值（数字）
- **enum**: 枚举值列表

**示例**:
```json
{
  "name": "format",
  "type": "string",
  "required": false,
  "default": "json",
  "validation": {
    "enum": ["json", "xml", "yaml"]
  }
}
```

## 返回值定义

### 返回值结构

```json
{
  "returns": {
    "type": "object",
    "description": "处理结果",
    "properties": {
      "success": {
        "type": "boolean",
        "description": "是否成功"
      },
      "data": {
        "type": "object",
        "description": "返回数据"
      },
      "error": {
        "type": "string",
        "description": "错误信息"
      }
    }
  }
}
```

### 标准返回格式

**成功响应**:
```json
{
  "success": true,
  "data": {
    "result": "processed_data"
  }
}
```

**错误响应**:
```json
{
  "success": false,
  "error": "处理失败:参数验证错误"
}
```

## API 工具

### 认证方式

#### Bearer Token
```json
{
  "auth": {
    "type": "bearer",
    "token": "${API_KEY}"
  }
}
```

#### API Key
```json
{
  "auth": {
    "type": "api_key",
    "key_name": "X-API-Key",
    "key_value": "${API_KEY}",
    "location": "header"
  }
}
```

#### Basic Auth
```json
{
  "auth": {
    "type": "basic",
    "username": "${USERNAME}",
    "password": "${PASSWORD}"
  }
}
```

### 请求配置

```json
{
  "endpoint": "https://api.example.com/v1/resource",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json",
    "Accept": "application/json"
  },
  "body_template": {
    "query": "${prompt}",
    "max_tokens": 1000
  },
  "timeout": 30000,
  "retry": {
    "max_attempts": 3,
    "delay": 1000
  }
}
```

## Python 脚本工具

### 脚本结构

```python
# scripts/process.py

def main(input_data: dict) -> dict:
    """
    处理输入数据
    
    Args:
        input_data: 输入数据字典
    
    Returns:
        dict: 处理结果
    """
    try:
        # 处理逻辑
        result = process(input_data)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    import sys
    import json
    
    input_data = json.loads(sys.stdin.read())
    result = main(input_data)
    print(json.dumps(result))
```

### 依赖配置

在 Skill 的 `dependency.python` 字段中声明依赖:

```json
{
  "dependency": {
    "python": ["requests>=2.28.0", "pandas>=1.5.0"]
  }
}
```

## Bash 脚本工具

### 命令模板

```json
{
  "command": "python script.py --input ${input} --output ${output}",
  "parameters": [
    {
      "name": "input",
      "type": "string",
      "required": true
    },
    {
      "name": "output",
      "type": "string",
      "required": true
    }
  ]
}
```

### 输出处理

```json
{
  "output_format": "json",
  "output_path": "result.json"
}
```

## 工具集成

### 在工作流中使用

在工作流节点中引用工具:

```json
{
  "type": "tool",
  "id": "process_node",
  "tool_name": "process_data",
  "inputs": {
    "input_data": "$.upstream.output"
  }
}
```

### 工具依赖

如果工具之间存在依赖关系，在配置中声明:

```json
{
  "tools": [
    {
      "name": "tool_a",
      "dependencies": []
    },
    {
      "name": "tool_b",
      "dependencies": ["tool_a"]
    }
  ]
}
```

## 配置示例

### 示例 1: OpenAI API 工具

```json
{
  "name": "gpt_completion",
  "type": "api",
  "description": "调用 GPT 完成文本生成",
  "endpoint": "https://api.openai.com/v1/chat/completions",
  "method": "POST",
  "auth": {
    "type": "bearer",
    "token": "${OPENAI_API_KEY}"
  },
  "headers": {
    "Content-Type": "application/json"
  },
  "parameters": [
    {
      "name": "model",
      "type": "string",
      "required": true,
      "default": "gpt-4"
    },
    {
      "name": "messages",
      "type": "array",
      "required": true
    },
    {
      "name": "temperature",
      "type": "number",
      "required": false,
      "default": 0.7,
      "validation": {
        "minimum": 0,
        "maximum": 2
      }
    }
  ],
  "returns": {
    "type": "object",
    "properties": {
      "id": {"type": "string"},
      "choices": {"type": "array"},
      "usage": {"type": "object"}
    }
  }
}
```

### 示例 2: 图片处理工具

```json
{
  "name": "resize_image",
  "type": "python",
  "description": "调整图片尺寸",
  "script": "scripts/image.py",
  "function": "resize",
  "parameters": [
    {
      "name": "input_path",
      "type": "string",
      "required": true,
      "description": "输入图片路径"
    },
    {
      "name": "width",
      "type": "integer",
      "required": true,
      "description": "目标宽度"
    },
    {
      "name": "height",
      "type": "integer",
      "required": true,
      "description": "目标高度"
    }
  ],
  "returns": {
    "type": "object",
    "properties": {
      "output_path": {"type": "string"},
      "original_size": {"type": "object"},
      "new_size": {"type": "object"}
    }
  }
}
```

### 示例 3: 文件压缩工具

```json
{
  "name": "compress_file",
  "type": "bash",
  "description": "压缩文件为 ZIP 格式",
  "command": "zip -r ${output} ${input}",
  "parameters": [
    {
      "name": "input",
      "type": "string",
      "required": true,
      "description": "输入文件或目录"
    },
    {
      "name": "output",
      "type": "string",
      "required": true,
      "description": "输出 ZIP 文件路径"
    }
  ],
  "returns": {
    "type": "object",
    "properties": {
      "output_size": {"type": "integer"},
      "compression_ratio": {"type": "number"}
    }
  }
}
```

## 最佳实践

1. **明确命名**: 工具名称应清晰表达其功能
2. **完善文档**: 为工具提供详细的描述和示例
3. **参数验证**: 对输入参数进行严格的类型和格式验证
4. **错误处理**: 统一返回错误信息格式
5. **性能优化**: 为耗时操作设置合理的超时时间
6. **安全考虑**: 敏感信息使用环境变量或配置文件
7. **版本控制**: 为 API 工具指定版本号

## 工具测试

在集成工具前，建议进行以下测试:

- [ ] 参数验证测试
- [ ] 正常流程测试
- [ ] 异常情况测试
- [ ] 性能测试
- [ ] 安全测试
