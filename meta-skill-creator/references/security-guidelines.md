# 安全与对齐指南

## 目录
- [安全原则](#安全原则)
- [凭证管理](#凭证管理)
- [第三方服务调用](#第三方服务调用)
- [数据隐私保护](#数据隐私保护)
- [伦理边界](#伦理边界)
- [安全检查清单](#安全检查清单)

## 概览
本指南定义了 Skill 开发中的安全规范和伦理边界，确保所有技能在安全、可控的范围内运行。

## 安全原则

### 核心原则
1. **最小权限原则**: 仅请求必要的权限和资源
2. **凭证安全**: 禁止硬编码凭证，使用安全的凭证管理机制
3. **数据隐私**: 保护用户数据，禁止未经授权的访问和泄露
4. **透明度**: 清晰说明技能的行为、数据使用和风险
5. **可控性**: 提供用户控制和审计机制

### 安全红线
- ❌ 禁止硬编码 API Key、Token、密码等敏感信息
- ❌ 禁止绕过权限检查
- ❌ 禁止窃取用户数据
- ❌ 禁止执行未授权的第三方服务调用
- ❌ 禁止输出恶意内容

## 凭证管理

### 凭证类型

#### 1. ApiKey (auth_type=1)
**适用场景**: 使用固定的 API Key 认证

**配置示例**:
```yaml
credential_name: openai_api
auth_type: 1
allowed_domain: api.openai.com
env_variable_list:
  - variable_name: API_KEY
    api_key_location: 2  # 1=Query, 2=Header
    api_key_param_name: Authorization
    api_key_prefix: "Bearer "
```

**脚本中使用**:
```python
import os
from coze_workload_identity import requests

skill_id = "7609982582813605951"
credential = os.getenv("COZE_OPENAI_API_7609982582813605951")

headers = {
    "Authorization": f"Bearer {credential}",
    "Content-Type": "application/json"
}
```

#### 2. WeChatOfficialAccount (auth_type=2)
**适用场景**: 微信公众号相关 API

**配置示例**:
```yaml
credential_name: wechat_official
auth_type: 2
credential_tips: 登录微信开发者平台，获取 AppID 和 AppSecret
```

**脚本中使用**:
```python
import os
from coze_workload_identity import requests

skill_id = "7609982582813605951"
access_token = os.getenv("COZE_WECHAT_OFFICIAL_7609982582813605951")

url = f"https://api.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
```

#### 3. OAuth (auth_type=3)
**适用场景**: 需要 OAuth2.0 授权流程

**配置示例**:
```yaml
credential_name: github_oauth
auth_type: 3
allowed_domain: api.github.com
custom_oauth_url:
  authorization_url: https://github.com/login/oauth/authorize
  token_url: https://github.com/login/oauth/access_token
credential_purpose: GitHub仓库
```

**脚本中使用**:
```python
import os
from coze_workload_identity import requests

skill_id = "7609982582813605951"
access_token = os.getenv("COZE_GITHUB_OAUTH_7609982582813605951")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/vnd.github.v3+json"
}
```

### 凭证命名规范
- 格式: `<service_name>_<purpose>`
- 示例: `openai_chat`, `github_api`, `wechat_message`
- 唯一性: 同一个 skill 内必须唯一

### 凭证获取规则
**绝对禁止**:
- ❌ 将凭证定义为脚本函数参数
- ❌ 在 main() 中添加 --token 等凭证参数
- ❌ 在脚本中放置占位符让调用方替换

**必须遵守**:
- ✅ 所有凭证通过 `os.getenv()` 从环境变量读取
- ✅ 脚本中添加凭证缺失检查
- ✅ 凭证 Key 格式: `COZE_<credential_name>_<skill_id>`

## 第三方服务调用

### 调用流程

#### 第一步: 确定实现方式
1. 查阅用户提供的接口文档（优先）
2. 使用 web_search 搜索调用方式（次优先）
3. 基于已有知识确定（备选）

#### 第二步: 分析授权类型
- 无需授权 → 跳过凭证配置
- 需要 ApiKey → auth_type=1
- 微信公众号 → auth_type=2
- OAuth 授权 → auth_type=3

#### 第三步: 配置凭证
调用 `skill_credentials` 工具配置凭证

#### 第四步: 生成代码
- 必须使用 `coze_workload_identity.requests`
- 凭证从环境变量读取
- 包含完整的错误处理

### 请求安全
```python
import os
from coze_workload_identity import requests

def call_api():
    skill_id = "7609982582813605951"
    credential = os.getenv("COZE_API_KEY_7609982582813605951")

    if not credential:
        raise ValueError("缺少必要的凭证配置")

    url = "https://api.example.com/endpoint"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json={}, timeout=30)

        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: 状态码 {response.status_code}")

        data = response.json()

        if "error" in data:
            raise Exception(f"API错误: {data}")

        return data

    except requests.exceptions.RequestException as e:
        raise Exception(f"API调用失败: {str(e)}")
```

## 数据隐私保护

### 数据分类
1. **公开数据**: 可自由使用的数据（如公开文档、API 文档）
2. **用户数据**: 用户上传的数据（需要保护隐私）
3. **敏感数据**: 包含个人身份、财务等敏感信息（严格保护）

### 处理原则
1. **最小化收集**: 仅收集必要的数据
2. **本地处理**: 优先在本地处理数据，减少外部传输
3. **脱敏处理**: 输出时隐藏敏感信息
4. **及时清理**: 处理完成后删除临时数据

### 禁止行为
- ❌ 未经授权访问用户文件
- ❌ 窃取用户凭证
- ❌ 向第三方泄露用户数据
- ❌ 长期存储用户数据（除非必要）

## 伦理边界

### 内容生成
1. **禁止输出**:
   - 仇恨言论
   - 暴力内容
   - 色情内容
   - 欺诈信息
   - 恶意软件

2. **谨慎处理**:
   - 政治敏感内容
   - 医疗建议（需声明仅供参考）
   - 法律建议（需建议咨询专业人士）

### 行为规范
1. **诚实透明**: 如实告知技能的能力和限制
2. **尊重用户**: 不欺骗、不误导用户
3. **保护隐私**: 不窥探用户隐私
4. **负责任**: 考虑技能使用的社会影响

### 风险提示
在 SKILL.md 中应包含：
- 潜在风险说明
- 使用限制
- 数据使用声明

## 安全检查清单

### 凭证管理
- [ ] 无硬编码凭证
- [ ] 通过 os.getenv() 读取
- [ ] 凭证 Key 格式正确
- [ ] 包含凭证缺失检查

### 第三方调用
- [ ] 使用 coze_workload_identity.requests
- [ ] 超时设置合理
- [ ] 错误处理完善
- [ ] 授权类型正确

### 数据隐私
- [ ] 最小化数据收集
- [ ] 敏感信息脱敏
- [ ] 临时文件清理
- [ ] 数据传输加密

### 伦理边界
- [ ] 不输出恶意内容
- [ ] 不欺骗用户
- [ ] 包含风险提示
- [ ] 尊重用户隐私

### 代码审查
- [ ] 无安全漏洞
- [ ] 无注入风险
- [ ] 资源使用合理
- [ ] 异常处理完善

## 安全事件响应

### 发现安全问题
1. 立即停止使用相关功能
2. 评估影响范围
3. 记录问题详情
4. 修复并验证
5. 更新文档和日志

### 报告机制
- 内部安全团队
- 用户反馈渠道
- 安全审计日志

## 安全最佳实践

1. **防御编程**: 假设所有输入都可能有问题
2. **最小权限**: 请求最少的权限和资源
3. **透明化**: 清晰说明行为和风险
4. **可审计**: 记录关键操作日志
5. **持续监控**: 关注安全漏洞和威胁情报
