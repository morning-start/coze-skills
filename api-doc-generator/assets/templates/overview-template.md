# API 概述模板

## 项目名称

{{PROJECT_NAME}}

## API 用途和目标

{{API_PURPOSE}}

本 API 提供了 {{PROJECT_NAME}} 的完整接口服务，支持 {{USE_CASES}}。

## 支持的使用场景

1. {{SCENARIO_1}} - {{SCENARIO_1_DESC}}
2. {{SCENARIO_2}} - {{SCENARIO_2_DESC}}
3. {{SCENARIO_3}} - {{SCENARIO_3_DESC}}

## 前提条件

在使用本 API 之前，您需要：

1. **注册账号**：访问 {{REGISTRATION_URL}} 注册开发者账号
2. **获取 API Key**：在控制台创建应用并获取 API Key
3. **配置环境**：确保您的开发环境支持 {{FRAMEWORK}} 协议

## 支持的协议

- **协议类型**：REST
- **数据格式**：JSON
- **字符编码**：UTF-8

## 快速开始

### 基础 URL

```
{{BASE_URL}}
```

### 简单示例

```bash
# 获取用户列表
curl -X GET {{BASE_URL}}/users \
  -H "Authorization: Bearer YOUR_API_KEY"

# 创建新用户
curl -X POST {{BASE_URL}}/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

## 版本信息

- **当前版本**：v{{VERSION}}
- **版本策略**：URL路径版本控制（如 /v1/）
- **兼容性**：保持向后兼容，废弃接口提前通知

## 模块概览

本 API 包含以下主要模块：

| 模块名称 | 端点数量 | 功能描述 |
|----------|----------|----------|
{{MODULE_TABLE}}

## 相关文档

- [认证方式](authentication.md) - 了解如何获取和使用认证凭证
- [基础信息](base-info.md) - 查看 API 基础配置和端点列表
- [端点详情](endpoints/) - 查看所有 API 端点的详细文档
- [错误处理](error-handling.md) - 了解错误代码和处理方法
