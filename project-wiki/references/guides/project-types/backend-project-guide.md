# 后端项目文档指南

## 概述

本指南适用于后端项目（FastAPI/Gin/Spring Boot），提供 API 服务开发的文档建议和最佳实践。

### 适用项目

- **FastAPI** (Python)
- **Gin** (Go)
- **Spring Boot** (Java)
- 其他后端框架项目

### 最小文档集（必备）

1. **README.md** - 项目说明
2. **OpenAPI 文档** - API 规范
3. **DB 设计文档** - 数据库设计
4. **部署运维文档** - 部署和监控

---

## 完整文档集

### 1. API 规范文档

**目的**：详细说明 API 接口定义。

**核心内容**：

#### 1.1 OpenAPI/Swagger

```markdown
## API 文档

### 自动生成
- FastAPI: 访问 /docs
- Spring Boot: 访问 /swagger-ui.html
- Gin: 使用 swag 生成

### 请求/响应结构
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 资源 ID |
| name | string | 是 | 名称 |
```

#### 1.2 错误格式

```markdown
## 错误响应

### 统一错误格式
```json
{
  "code": "ERROR_CODE",
  "message": "错误描述",
  "details": {}
}
```

### 状态码说明
- 200: 成功
- 400: 请求参数错误
- 401: 未授权
- 403: 禁止访问
- 404: 资源不存在
- 500: 服务器内部错误
```

---

### 2. 数据库设计

**目的**：说明数据库结构和关系。

**核心内容**：

#### 2.1 ER 图

```markdown
## 实体关系图

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : included_in
```
```

#### 2.2 表结构

```markdown
## 表结构

### users 表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 用户 ID |
| username | VARCHAR(50) | NOT NULL, UNIQUE | 用户名 |
| email | VARCHAR(100) | NOT NULL, UNIQUE | 邮箱 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

### 索引
- idx_username (username)
- idx_email (email)
```

---

### 3. 认证与授权

**目的**：说明安全机制。

**核心内容**：

```markdown
## 认证方案

### JWT Token
- Access Token: 有效期 2 小时
- Refresh Token: 有效期 7 天

### OAuth2 集成
- 支持 Google 登录
- 支持 GitHub 登录

## 授权机制

### RBAC 模型
- 角色：admin, user, guest
- 权限：read, write, delete

### 权限控制
- 基于角色的路由
- 基于权限的 API 访问
```

---

### 4. 部署与运维

**目的**：说明部署流程和运维要点。

**核心内容**：

#### 4.1 Dockerfile

```markdown
## Docker 部署

### Dockerfile 说明
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### 环境变量
| 变量 | 说明 | 示例 |
|------|------|------|
| DATABASE_URL | 数据库连接 | postgresql://user:pass@localhost/db |
| SECRET_KEY | JWT 密钥 | your-secret-key |
| DEBUG | 调试模式 | true/false |
```

#### 4.2 健康检查

```markdown
## 健康检查

### 健康检查端点
- GET /health - 基础健康检查
- GET /health/ready - 就绪检查

### 检查项
- 数据库连接
- Redis 连接
- 外部服务连接
```

#### 4.3 日志与监控

```markdown
## 日志

### 日志格式
```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "level": "INFO",
  "message": "Request processed",
  "trace_id": "abc123"
}
```

## 监控指标
- QPS (每秒查询数)
- 响应时间 (P50, P95, P99)
- 错误率
- CPU/内存使用率
```

---

### 5. 中间件说明

**目的**：说明自定义中间件和扩展点。

**核心内容**：

```markdown
## 中间件

### 内置中间件
- CORS 中间件
- 日志中间件
- 错误处理中间件

### 自定义中间件
- 认证中间件
- 限流中间件
- 请求追踪中间件

## 扩展点

### 生命周期钩子
- on_startup: 应用启动时
- on_shutdown: 应用关闭时
```

---

### 6. 测试策略

**目的**：说明测试方案。

**核心内容**：

```markdown
## 测试策略

### 单元测试
- 工具：pytest (Python), junit (Java), testing (Go)
- 范围：业务逻辑、工具函数

### 集成测试
- 工具：TestClient, Postman
- 范围：API 接口、数据库交互

### Mock 策略
- Mock 外部服务
- Mock 数据库
- 使用测试数据库
```

---

## 推荐工具

| 工具 | 用途 | 适用场景 |
|------|------|---------|
| **Swagger UI** | API 文档 | API 接口说明 |
| **Postman** | API 测试 | 接口调试、集合分享 |
| **ArchUnit** | 架构测试 | Java 架构约束验证 |
| **Docker** | 容器化 | 部署打包 |
| **Prometheus** | 监控 | 指标收集 |
| **Grafana** | 可视化 | 监控面板 |

---

## 检查清单

- [ ] API 文档完整（OpenAPI/Swagger）
- [ ] 数据库设计文档（ER 图、表结构）
- [ ] 认证授权机制说明
- [ ] 部署文档（Dockerfile、环境变量）
- [ ] 健康检查端点
- [ ] 日志格式说明
- [ ] 测试策略文档

---

## 参考资料

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Gin 官方文档](https://gin-gonic.com/)
- [Spring Boot 官方文档](https://spring.io/projects/spring-boot)
- [项目类型总览](README.md)
