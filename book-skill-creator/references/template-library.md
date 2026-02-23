# 模板库索引

## 目录
1. [模板库概述](#模板库概述)
2. [模板分类](#模板分类)
3. [模板评分系统](#模板评分系统)
4. [模板管理](#模板管理)
5. [模板检索](#模板检索)
6. [最佳实践](#最佳实践)

## 概览
模板库存储从行业最佳实践中提取的可复用模板，按技术、场景、复杂度分类，支持版本管理和质量评分。

## 模板库结构

```
template-library/
├── template-index.json          # 模板索引
├── .versions/                   # 版本历史
├── FastAPI/
│   ├── api-client/
│   ├── middleware/
│   └── authentication/
├── React/
│   ├── component/
│   ├── hook/
│   └── state-management/
└── TensorFlow/
    ├── model/
    ├── training/
    └── deployment/
```

## 模板分类

### 按技术分类

#### Web 框架
- FastAPI
- Flask
- Django
- Express
- React
- Vue
- Angular

#### 数据处理
- Pandas
- NumPy
- PyTorch
- TensorFlow
- Scikit-learn

#### 工具库
- Requests
- BeautifulSoup
- Selenium
- Celery

### 按场景分类

#### API 调用
- RESTful API 客户端
- GraphQL 客户端
- WebSocket 客户端

#### 数据处理
- 数据清洗管道
- 数据转换工具
- 数据分析脚本

#### 工作流
- 任务编排
- 数据管道
- 自动化流程

### 按复杂度分类

#### 初级（Beginner）
- 代码简洁
- 功能单一
- 易于理解

#### 中级（Intermediate）
- 功能完整
- 包含错误处理
- 适度复杂

#### 高级（Advanced）
- 功能全面
- 包含优化
- 生产就绪

## 模板评分系统

### 评分维度

#### 1. 完整性（0-100）
- 代码完整性：30分
- 文档完整性：30分
- 配置完整性：20分
- 示例完整性：20分

#### 2. 实用性（0-100）
- 实际应用价值：40分
- 使用频率：30分
- 社区认可度：30分

#### 3. 可复用性（0-100）
- 通用性：40分
- 可定制性：30分
- 易于集成：30分

### 综合评分
```
综合评分 = 完整性 × 0.4 + 实用性 × 0.3 + 可复用性 × 0.3
```

### 评分等级
- **优秀**：90-100分
- **良好**：70-89分
- **中等**：50-69分
- **一般**：30-49分
- **较差**：0-29分

## 模板管理

### 添加模板

#### 使用脚本
```bash
python scripts/template_manager.py add \
  --name "api-client" \
  --tech "FastAPI" \
  --category "api" \
  --code "$(cat code.py)" \
  --doc "$(cat README.md)" \
  --version "1.0.0" \
  --tags "api client http" \
  --complexity "intermediate"
```

#### 使用网络搜索器
```bash
python scripts/web_searcher.py \
  --tech "FastAPI" \
  --query "api client best practices" \
  --category "api" \
  --output ./assets/template-library
```

### 更新模板

#### 升级版本
```bash
python scripts/template_manager.py update \
  --id "FastAPI/api/api-client" \
  --version "1.1.0" \
  --code "$(cat new-code.py)"
```

#### 更新内容
```bash
python scripts/template_manager.py update \
  --id "FastAPI/api/api-client" \
  --doc "$(cat updated-doc.md)"
```

### 删除模板
```bash
python scripts/template_manager.py delete \
  --id "FastAPI/api/api-client"
```

### 导出模板
```bash
python scripts/template_manager.py export \
  --id "FastAPI/api/api-client" \
  --output ./exported-templates/api-client
```

## 模板检索

### 列出所有模板
```bash
python scripts/template_manager.py list
```

### 按技术筛选
```bash
python scripts/template_manager.py list --tech FastAPI
```

### 按分类筛选
```bash
python scripts/template_manager.py list --tech FastAPI --category api
```

### 按评分筛选
```bash
python scripts/template_manager.py list --min-score 0.8
```

### 按复杂度筛选
```bash
python scripts/template_manager.py list --complexity advanced
```

### 按标签筛选
```bash
python scripts/template_manager.py list --tags api http
```

### 搜索模板
```bash
python scripts/template_manager.py search --query "api client"
```

### 获取模板详情
```bash
python scripts/template_manager.py get --id "FastAPI/api/api-client"
```

## 模板库索引

### FastAPI 模板

#### API 客户端
- **ID**: FastAPI/api/api-client
- **版本**: 1.2.0
- **评分**: 0.92
- **复杂度**: intermediate
- **标签**: api, client, http, rest

#### 中间件
- **ID**: FastAPI/middleware/auth
- **版本**: 1.0.0
- **评分**: 0.88
- **复杂度**: intermediate
- **标签**: middleware, auth, jwt

### React 模板

#### 组件
- **ID**: React/component/button
- **版本**: 2.0.0
- **评分**: 0.95
- **复杂度**: beginner
- **标签**: component, button, ui

#### Hook
- **ID**: React/hook/use-fetch
- **版本**: 1.1.0
- **评分**: 0.90
- **复杂度**: intermediate
- **标签**: hook, fetch, async

### Pandas 模板

#### 数据清洗
- **ID**: Pandas/data/clean
- **版本**: 1.3.0
- **评分**: 0.93
- **复杂度**: intermediate
- **标签**: data, clean, preprocessing

#### 数据转换
- **ID**: Pandas/data/transform
- **版本**: 1.0.0
- **评分**: 0.87
- **复杂度**: beginner
- **标签**: data, transform, format

## 使用模板

### 1. 搜索模板
```bash
python scripts/template_manager.py search --query "api client"
```

### 2. 获取模板
```bash
python scripts/template_manager.py get --id "FastAPI/api/api-client"
```

### 3. 导出模板
```bash
python scripts/template_manager.py export \
  --id "FastAPI/api/api-client" \
  --output ./my-project
```

### 4. 集成到项目
```bash
cp ./my-project/code.py ./my-project/
cp ./my-project/config.json ./my-project/
```

## 最佳实践

### 模板创建

#### 1. 确保代码质量
- 遵循编码规范
- 包含错误处理
- 添加类型注解
- 编写文档字符串

#### 2. 提供完整文档
- 功能说明
- 使用示例
- 配置说明
- 注意事项

#### 3. 添加配置示例
- 默认配置
- 环境变量
- 配置选项说明

#### 4. 包含测试用例
- 单元测试
- 集成测试
- 测试示例

### 模板维护

#### 1. 定期更新
- 修复 Bug
- 添加新功能
- 优化性能
- 更新依赖

#### 2. 版本管理
- 使用语义化版本
- 记录变更日志
- 保持向后兼容

#### 3. 质量监控
- 收集用户反馈
- 监控使用情况
- 优化评分

### 模板分享

#### 1. 提交模板
- 确保质量达标
- 完善文档
- 提供示例

#### 2. 社区贡献
- 分享经验
- 审查他人模板
- 改进模板质量

## 模板示例

### FastAPI API 客户端模板

#### 代码
```python
#!/usr/bin/env python3
"""
FastAPI API 客户端模板
支持所有 HTTP 方法，包含重试机制和错误处理
"""

import requests
from typing import Dict, Any, Optional
import time


class APIClient:
    """FastAPI API 客户端"""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """发起请求，支持重试"""
        url = f"{self.base_url}{endpoint}"

        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method,
                    url,
                    headers=self.headers,
                    json=data,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()

            except requests.exceptions.Timeout:
                if attempt == self.max_retries - 1:
                    raise Exception(f"请求超时: {endpoint}")
                time.sleep(2 ** attempt)

            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"请求失败: {str(e)}")
                time.sleep(2 ** attempt)

    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """GET 请求"""
        return self._request("GET", endpoint, params)

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST 请求"""
        return self._request("POST", endpoint, data)

    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """PUT 请求"""
        return self._request("PUT", endpoint, data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE 请求"""
        return self._request("DELETE", endpoint)
```

#### 配置
```json
{
  "base_url": "https://api.example.com",
  "api_key": "your-api-key",
  "timeout": 30,
  "max_retries": 3
}
```

#### 文档
```markdown
# FastAPI API 客户端

## 功能
- 支持 GET、POST、PUT、DELETE 方法
- 自动重试机制
- 错误处理
- 超时控制

## 使用示例

```python
client = APIClient(base_url="https://api.example.com", api_key="your-key")

# GET 请求
users = client.get("/users")

# POST 请求
new_user = client.post("/users", {"name": "John"})

# PUT 请求
updated = client.put("/users/1", {"name": "Jane"})

# DELETE 请求
client.delete("/users/1")
```

## 配置说明
- `base_url`: API 基础 URL
- `api_key`: API 密钥（可选）
- `timeout`: 请求超时时间（秒）
- `max_retries`: 最大重试次数
```

## 模板质量检查清单

### 代码质量
- [ ] 代码格式规范
- [ ] 包含错误处理
- [ ] 包含类型注解
- [ ] 包含文档字符串
- [ ] 代码可读性高

### 文档完整性
- [ ] 功能说明清晰
- [ ] 包含使用示例
- [ ] 配置说明完整
- [ ] 注意事项明确
- [ ] 常见问题解答

### 可复用性
- [ ] 通用性强
- [ ] 易于定制
- [ ] 易于集成
- [ ] 依赖清晰
- [ ] 版本兼容

## 常见问题

### Q1: 如何贡献新模板？
**A**: 使用 `web_searcher.py` 搜索最佳实践，然后使用 `template_manager.py add` 添加模板。

### Q2: 如何更新现有模板？
**A**: 使用 `template_manager.py update` 更新模板内容，升级版本号。

### Q3: 如何查找高质量模板？
**A**: 使用 `--min-score` 参数筛选高评分模板，或按技术/分类筛选。

### Q4: 模板如何保持最新？
**A**: 定期使用 `web_searcher.py` 搜索最新实践，更新模板内容和版本。

## 进阶功能

### 模板继承
基于现有模板创建新模板，继承其结构和配置。

### 模板组合
组合多个模板，形成完整的解决方案。

### 模板自动化
自动化模板生成、测试、部署流程。
