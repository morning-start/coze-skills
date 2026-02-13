# API 文档生成指南

## 文档结构

### 1. API 概览

简要描述 API 的整体架构、设计原则和使用场景。

### 2. 认证与授权

说明 API 的认证方式（如 Bearer Token、API Key、OAuth 等）。

示例：
```markdown
## 认证

所有 API 请求需要在 Header 中包含认证令牌：

\`\`\`http
Authorization: Bearer <your-token>
\`\`\`

获取令牌请参考 [认证文档](#获取访问令牌)
```

### 3. API 端点列表

#### 端点格式

每个 API 端点应包含以下信息：

```markdown
### [方法] [路径]

[简要描述]

**请求参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| param1 | string | 是 | 参数说明 |
| param2 | number | 否 | 参数说明，默认值: 0 |

**请求示例**

\`\`\`http
[METHOD] /api/path
Content-Type: application/json

{
  "param1": "value1",
  "param2": 123
}
\`\`\`

**响应示例**

\`\`\`json
{
  "code": 200,
  "message": "success",
  "data": {
    "result": "..."
  }
}
\`\`\`

**响应字段**

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | number | 状态码 |
| message | string | 响应消息 |
| data | object | 响应数据 |

**错误码**

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 400 | 请求参数错误 | 检查参数格式 |
| 401 | 未授权 | 检查认证令牌 |
| 404 | 资源不存在 | 检查资源ID |
| 500 | 服务器错误 | 联系管理员 |
```

### 4. 数据模型

#### 模型定义

```markdown
### User（用户模型）

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| id | string | 用户ID | "123456" |
| name | string | 用户名 | "张三" |
| email | string | 邮箱 | "user@example.com" |
| createdAt | string | 创建时间（ISO 8601） | "2024-01-01T00:00:00Z" |
```

### 5. 最佳实践

- 提供使用示例代码
- 说明性能限制（如速率限制）
- 提供调试建议

## 文档示例

### 示例：用户管理 API

```markdown
# 用户管理 API

## 获取用户列表

\`\`\`http
GET /api/users
\`\`\`

**查询参数**

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | number | 否 | 页码，默认: 1 |
| pageSize | number | 否 | 每页数量，默认: 10 |
| keyword | string | 否 | 搜索关键词 |

**响应示例**

\`\`\`json
{
  "code": 200,
  "message": "success",
  "data": {
    "users": [
      {
        "id": "123456",
        "name": "张三",
        "email": "zhangsan@example.com"
      }
    ],
    "total": 100,
    "page": 1,
    "pageSize": 10
  }
}
\`\`\`

## 获取用户详情

\`\`\`http
GET /api/users/:id
\`\`\`

**路径参数**

| 参数名 | 类型 | 说明 |
|--------|------|------|
| id | string | 用户ID |

**响应示例**

\`\`\`json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": "123456",
    "name": "张三",
    "email": "zhangsan@example.com",
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
\`\`\`
```

## 注意事项

1. **一致性**: 所有 API 端点保持相同的格式和风格
2. **完整性**: 必须包含所有必要的参数说明
3. **示例性**: 提供真实可运行的请求/响应示例
4. **错误处理**: 详细的错误码和错误信息
5. **版本管理**: 如有多个版本，需明确说明版本差异

---

**注意**: 本指南应智能体根据项目实际情况动态调整内容，支持 OpenAPI/Swagger 风格
