# 技能配置格式参考

## 概览
本文档定义了技能配置 JSON 文件的格式规范，用于通过 `generate_skill.py` 脚本生成完整的 Skill 结构。

## 配置结构

### 根级别字段

| 字段名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| `name` | string | 是 | Skill 名称，必须使用小写字母和连字符，禁止 -skill 后缀 |
| `description` | string | 是 | Skill 描述，100-150 字符，包含核心能力和触发场景 |
| `version` | string | 否 | 技能版本号，格式: x.y.z |
| `author` | string | 否 | 作者信息 |
| `dependency` | object | 否 | 依赖配置 |
| `tools` | array | 否 | 工具列表 |
| `scripts` | array | 否 | 脚本定义 |
| `references` | array | 否 | 参考文档定义 |
| `assets` | array | 否 | 资产文件定义 |

### dependency 字段

```json
{
  "dependency": {
    "python": ["package-name==1.0.0", "other-package>=2.0.0"],
    "system": ["mkdir -p extra-files"]
  }
}
```

### tools 字段

```json
{
  "tools": [
    {
      "name": "tool-name",
      "type": "python|bash|api",
      "description": "工具功能描述",
      "parameters": [
        {
          "name": "param-name",
          "type": "string|integer|boolean|object|array",
          "required": true,
          "description": "参数说明"
        }
      ],
      "returns": {
        "type": "object",
        "description": "返回值结构"
      }
    }
  ]
}
```

### scripts 字段

```json
{
  "scripts": [
    {
      "name": "process.py",
      "description": "脚本功能描述",
      "functions": [
        {
          "name": "main_function",
          "parameters": ["input_data"],
          "description": "函数说明"
        }
      ]
    }
  ]
}
```

### references 字段

```json
{
  "references": [
    {
      "name": "guide.md",
      "content": "# 参考文档内容\n..."
    }
  ]
}
```

### assets 字段

```json
{
  "assets": [
    {
      "path": "templates/config.yaml",
      "content": "模板内容..."
    }
  ]
}
```

## 完整示例

```json
{
  "name": "image-processor",
  "description": "处理图片文件的压缩、裁剪和格式转换",
  "version": "1.0.0",
  "dependency": {
    "python": ["Pillow>=9.0.0", "opencv-python>=4.5.0"],
    "system": ["mkdir -p /tmp/image-cache"]
  },
  "tools": [
    {
      "name": "compress",
      "type": "python",
      "description": "压缩图片文件",
      "parameters": [
        {
          "name": "input_path",
          "type": "string",
          "required": true,
          "description": "输入图片路径"
        },
        {
          "name": "quality",
          "type": "integer",
          "required": false,
          "description": "压缩质量 (1-100)"
        }
      ]
    }
  ],
  "scripts": [
    {
      "name": "compress.py",
      "description": "图片压缩脚本",
      "functions": [
        {
          "name": "compress_image",
          "parameters": ["input_path", "output_path", "quality"],
          "description": "执行图片压缩"
        }
      ]
    }
  ],
  "references": [
    {
      "name": "image-formats.md",
      "content": "# 支持的图片格式\n..."
    }
  ],
  "assets": [
    {
      "path": "examples/sample.jpg",
      "content": "<binary-data>"
    }
  ]
}
```

## 验证规则

1. **命名规范**:
   - `name` 必须使用小写字母和连字符
   - 禁止使用 `-skill` 后缀
   - 长度不超过 50 字符

2. **描述规范**:
   - `description` 长度 100-150 字符
   - 必须包含核心能力说明
   - 建议列举 1-3 个典型触发场景

3. **工具规范**:
   - `type` 仅支持: python、bash、api
   - `parameters.type` 仅支持: string、integer、boolean、object、array
   - 必须指定参数是否必需 (`required`)

4. **依赖规范**:
   - `dependency.python` 遵循 requirements.txt 格式
   - `dependency.system` 为有效的 shell 命令列表

## 常见错误

| 错误类型 | 示例 | 修正 |
|----------|------|------|
| 命名不规范 | `name: "ImageCompressor"` | `name: "image-compressor"` |
| 使用 -skill 后缀 | `name: "my-skill"` | `name: "my-tool"` |
| 描述过长 | 超过 150 字符 | 精简到 100-150 字符 |
| 缺少必需字段 | 缺少 `name` 或 `description` | 添加必需字段 |
| 类型错误 | `parameters.type: "float"` | 使用 `"integer"` 或 `"number"` |

## 生成流程

1. 创建配置 JSON 文件
2. 运行 `validate_schema.py --config config.json` 验证
3. 运行 `generate_skill.py --config config.json --output ./my-skill` 生成
4. 使用 `package_skill` 工具打包
