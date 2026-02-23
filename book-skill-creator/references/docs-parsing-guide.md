# 官方文档解析指南

## 目录
1. [文档解析概述](#文档解析概述)
2. [支持的文档格式](#支持的文档格式)
3. [解析能力](#解析能力)
4. [生成内容](#生成内容)
5. [覆盖率保证](#覆盖率保证)
6. [使用示例](#使用示例)

## 概览
本文档说明如何使用文档解析器实现官方文档的 100% 覆盖，自动生成完整的技能包。

## 文档解析概述

### 目标
- **100% API 覆盖**：提取文档中的所有 API 端点
- **完整代码示例**：提取所有代码块和示例
- **配置项提取**：识别所有配置参数
- **结构化生成**：自动生成 SKILL.md、脚本、参考文档

### 工作流程
```
官方文档 → 格式检测 → 解析器选择 → 内容提取 → 技能生成 → 质量验证
```

## 支持的文档格式

### 1. Markdown (.md)
**适用场景**：
- GitHub 文档
- 技术博客
- README 文件

**解析能力**：
- 章节结构（# ## ###）
- API 端点（`GET /api/path`）
- 代码块（```python）
- 配置项（`key` (type) - description）

**示例**：
```bash
python scripts/docs_parser.py \
  --docs-path /path/to/docs.md \
  --output /path/to/skill
```

### 2. HTML (.html, .htm)
**适用场景**：
- 官方网站文档
- 在线文档系统
- API 文档页面

**解析能力**：
- HTML 标题结构（h1-h6）
- 预格式化代码块（pre, code）
- 链接和锚点

**依赖**：
```bash
pip install beautifulsoup4
```

### 3. OpenAPI 规范 (.yaml, .yml, .json)
**适用场景**：
- RESTful API 文档
- Swagger 文档
- API 规范文件

**解析能力**：
- 完整的 API 端点
- 参数定义（路径、查询、请求体）
- 响应结构
- 认证方式

**示例**：
```bash
python scripts/docs_parser.py \
  --docs-path openapi.yaml \
  --output /path/to/skill \
  --format openapi
```

## 解析能力

### API 端点提取

#### Markdown 格式
支持多种格式：
- `GET /api/users`
- `**POST /api/data**`
- `PUT /api/resource/{id}`

#### OpenAPI 格式
自动提取：
- 路径
- HTTP 方法
- 参数（name, in, type, required）
- 响应结构

#### 提取结果
```json
{
  "path": "/api/users",
  "method": "GET",
  "description": "获取用户列表",
  "parameters": [
    {
      "name": "page",
      "in": "query",
      "type": "integer",
      "required": false
    }
  ],
  "response": { ... }
}
```

### 代码示例提取

#### 支持的语言
- Python
- JavaScript
- Bash
- JSON
- YAML
- 其他（通用文本）

#### 提取规则
- 识别代码块标记（```）
- 提取语言标识
- 提取代码内容
- 提取代码块前的描述文字

#### 输出格式
```markdown
## 示例 1

**描述**: 调用用户 API

**语言**: python

```python
import requests

response = requests.get('/api/users')
print(response.json())
```
```

### 配置项提取

#### Markdown 格式
```
`database_url` (string) - 数据库连接字符串
`port` (integer) - 服务器端口
`debug` (boolean) - 启用调试模式
```

#### 提取结果
```json
{
  "key": "database_url",
  "type": "string",
  "description": "数据库连接字符串",
  "required": true
}
```

### 章节结构提取

#### Markdown
```
# 标题 1
## 标题 2
### 标题 3
```

#### HTML
```
<h1>标题 1</h1>
<h2>标题 2</h2>
<h3>标题 3</h3>
```

#### 用途
- 生成 SKILL.md 的章节
- 生成参考文档的目录
- 理解文档结构

## 生成内容

### 1. SKILL.md
**内容**：
- 前言区（YAML）
- 任务目标
- 操作步骤
- 资源索引
- 使用示例

**特点**：
- 100% API 覆盖说明
- 自动生成使用流程
- 包含所有提取的信息

### 2. API 客户端脚本
**内容**：
- 完整的客户端类
- 所有 API 方法
- 请求处理逻辑
- 错误处理

**示例**：
```python
class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get_users(self, **kwargs):
        return self._request("GET", "/api/users", kwargs)

    def create_user(self, data):
        return self._request("POST", "/api/users", data)
```

### 3. API 参考文档
**内容**：
- 所有 API 端点详情
- 参数说明表格
- 响应示例
- 使用注意事项

**格式**：Markdown，包含表格和代码块

### 4. 代码示例文档
**内容**：
- 所有提取的代码示例
- 按语言分类
- 包含描述说明

## 覆盖率保证

### 100% 覆盖定义

#### API 覆盖
- 提取文档中所有 API 端点
- 包含所有 HTTP 方法
- 包含所有参数定义
- 包含所有响应结构

#### 代码覆盖
- 提取所有代码块
- 提取所有示例代码
- 生成可运行的客户端脚本

#### 文档覆盖
- 提取所有章节
- 提取所有配置项
- 生成完整的参考文档

### 质量验证

#### 解析报告
```json
{
  "skill_name": "my-api",
  "apis_found": 25,
  "code_examples": 12,
  "configs": 8,
  "chapters": 15,
  "coverage": "100%"
}
```

#### 验证检查
- [ ] 所有 API 端点已提取
- [ ] 所有代码示例已提取
- [ ] 所有配置项已提取
- [ ] 生成的 SKILL.md 包含所有信息
- [ ] 客户端脚本包含所有方法
- [ ] 参考文档完整

### 不完整情况处理

#### 缺失 API 端点
- 检查文档格式是否正确
- 检查 API 端点格式是否符合规范
- 手动补充缺失的端点

#### 缺失代码示例
- 检查代码块标记是否正确
- 检查语言标识是否正确
- 手动补充示例代码

#### 缺失配置项
- 检查配置格式是否符合规范
- 检查是否有配置章节
- 手动补充配置项

## 使用示例

### 示例 1：解析 Markdown 文档

**文档内容**：
```markdown
# My API Documentation

## Users API

### Get Users

`GET /api/users` - 获取用户列表

```python
import requests

response = requests.get('https://api.example.com/users')
users = response.json()
```

### Create User

`POST /api/users` - 创建新用户

```python
data = {"name": "John", "email": "john@example.com"}
response = requests.post('https://api.example.com/users', json=data)
```

## Configuration

`api_key` (string) - API 密钥
`timeout` (integer) - 请求超时时间
```

**解析命令**：
```bash
python scripts/docs_parser.py \
  --docs-path my-api.md \
  --output ./my-api-skill
```

**生成结果**：
- my-api-skill/SKILL.md
- my-api-skill/scripts/api_client.py
- my-api-skill/references/api-reference.md
- my-api-skill/references/code-examples.md

**解析报告**：
```
============================================================
解析完成报告
============================================================
技能名称: My API Documentation
API 端点: 2
代码示例: 2
配置项: 2
章节结构: 3
覆盖率: 100%
============================================================
```

### 示例 2：解析 OpenAPI 规范

**规范文件**：
```yaml
openapi: 3.0.0
info:
  title: Pet Store API
  version: 1.0.0
paths:
  /pets:
    get:
      summary: List all pets
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Successful response
```

**解析命令**：
```bash
python scripts/docs_parser.py \
  --docs-path petstore.yaml \
  --output ./petstore-skill \
  --format openapi
```

### 示例 3：批量处理多个文档

**Shell 脚本**：
```bash
#!/bin/bash

for doc in docs/*.md; do
    skill_name=$(basename "$doc" .md)
    python scripts/docs_parser.py \
        --docs-path "$doc" \
        --output "skills/$skill_name"
done
```

## 最佳实践

### 文档准备
1. 确保文档格式正确
2. API 端点使用统一格式
3. 代码块包含语言标识
4. 配置项使用标准格式

### 解析后处理
1. 检查解析报告
2. 验证覆盖率是否 100%
3. 测试生成的客户端脚本
4. 完善参考文档

### 质量保证
1. 使用验证工具检查生成的技能
2. 手动补充缺失的内容
3. 更新模板和规范
4. 建立文档解析知识库

## 常见问题

### Q1: 解析器无法识别某些 API 端点？
**A**: 检查 API 端点格式，确保使用标准格式（如 `GET /api/path` 或 `**GET /api/path**`）

### Q2: 代码示例没有提取？
**A**: 确保代码块使用正确的标记（```language），并检查前后是否有空行

### Q3: OpenAPI 规范解析失败？
**A**: 检查 YAML/JSON 格式是否正确，确保符合 OpenAPI 规范

### Q4: 如何补充缺失的内容？
**A**: 解析完成后，手动编辑生成的文件，补充缺失的内容

## 进阶使用

### 自定义解析器
继承 `DocsParser` 基类，实现自定义解析逻辑：

```python
class CustomParser(DocsParser):
    def parse(self, docs_path: str) -> ParseResult:
        # 自定义解析逻辑
        pass
```

### 自定义模板生成
修改 `generate_skill_md`、`generate_api_client` 等函数，自定义生成逻辑。

### 集成到工作流
将文档解析集成到 CI/CD 流程，自动生成和更新技能包。
