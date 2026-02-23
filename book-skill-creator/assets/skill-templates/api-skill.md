---
name: {{ skill_name }}
description: {{ description }}
dependency:
  python:
    - requests>=2.28.0
---

# {{ skill_title }}

## 任务目标
- 本 Skill 用于：调用 {{ service_name }} API 实现 {{ functionality }}
- 能力包含：{{ core_features }}
- 触发条件：当用户需要 {{ trigger_conditions }}

## 前置准备
- 依赖说明：scripts 脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  ```
- 凭证配置：需要配置 API 密钥
  - 访问 {{ api_doc_url }} 获取 API Key
  - 调用 skill_credentials 工具配置凭证

## 操作步骤

### 标准流程
1. 准备请求参数
   - 根据接口文档准备必要的参数
   - 验证参数格式和完整性

2. 调用 API 接口
   - 调用 `scripts/api_client.py` 发起请求
   - 处理 API 响应结果

3. 结果处理与输出
   - 解析返回数据
   - 格式化输出结果
   - 错误处理和重试

### 可选分支
- 当请求失败：执行自动重试机制
- 当需要批量调用：使用批量接口

## 资源索引

### 必要脚本
- [scripts/api_client.py](scripts/api_client.py)
  - 用途：调用 {{ service_name }} API
  - 参数：--endpoint（接口路径）、--params（请求参数）
  - 输入：API 参数（JSON 格式）
  - 输出：API 响应结果

### 领域参考
- [references/api-doc.md](references/api-doc.md)
  - 何时读取：需要了解 API 详细文档
  - 内容：接口列表、参数说明、返回格式

## 注意事项

### 授权与凭证
- API 密钥通过环境变量获取
- 不要在脚本中硬编码密钥
- 定期更新密钥保证安全

### 错误处理
- 网络错误自动重试（最多 3 次）
- 业务错误需要处理错误码
- 超时设置（默认 30 秒）

### 性能优化
- 批量请求使用批量接口
- 异步调用提高效率
- 缓存机制减少重复请求

## 使用示例

### 示例 1：基础调用
- 功能说明：调用基础 API 接口
- 执行方式：脚本调用
- 关键参数：
  ```python
  python scripts/api_client.py \
    --endpoint /api/resource \
    --params '{"id": 123}'
  ```

### 示例 2：批量操作
- 功能说明：批量处理多个请求
- 执行方式：脚本调用
- 关键参数：
  ```python
  python scripts/api_client.py \
    --endpoint /api/batch \
    --params '{"items": [...]}' \
    --batch
  ```
