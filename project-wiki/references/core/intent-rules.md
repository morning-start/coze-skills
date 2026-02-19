# 意图识别规则

## 目录

1. [意图分类体系](#意图分类体系)
2. [关键词匹配规则](#关键词匹配规则)
3. [路由决策逻辑](#路由决策逻辑)
4. [上下文增强](#上下文增强)
5. [处理流程](#处理流程)

---

## 意图分类体系

### 一级分类

| 意图类型 | 优先级 | 处理方式 |
|----------|--------|----------|
| **文档查询** | 高 | 返回参考文档内容 |
| **文档生成** | 高 | 调用生成脚本 + 填充模板 |
| **代码查询** | 中 | 调用提取脚本 |
| **图表生成** | 中 | 生成 Mermaid 代码 |
| **结构查询** | 中 | 返回 Wiki 结构信息 |
| **框架查询** | 低 | 返回框架指引 |
| **版本查询** | 低 | 返回版本相关信息 |

### 二级分类

#### 文档查询（Query Document）

| 子类型 | 关键词 | 目标文档 |
|--------|--------|----------|
| 查询规范 | "如何"、"规范"、"格式" | `document-guides/*.md` |
| 查询结构 | "结构"、"目录"、"组织" | `core/wiki-structure-guide.md` |
| 查询指南 | "指南"、"教程" | `core/*.md` |
| 查询框架 | "框架"、"技术栈" | `frameworks/index.md` |

#### 文档生成（Generate Document）

| 子类型 | 关键词 | 模板 |
|--------|--------|------|
| 生成 API 文档 | "API 文档"、"接口文档" | `templates/api-template.md` |
| 生成模块文档 | "模块文档" | `templates/module-template.md` |
| 生成服务文档 | "服务文档" | `templates/service-template.md` |
| 生成 CHANGELOG | "CHANGELOG"、"变更日志" | `changelog-templates/` |
| 生成 ROADMAP | "ROADMAP"、"发展规划" | （自动生成） |

#### 代码查询（Query Code）

| 子类型 | 关键词 | 操作 |
|--------|--------|------|
| 查询接口 | "接口"、"API"、"endpoint" | 提取 API 信息 |
| 查询函数 | "函数"、"function"、"方法" | 提取函数信息 |
| 查询类 | "类"、"class"、"对象" | 提取类信息 |
| 查询配置 | "配置"、"config"、"设置" | 提取配置信息 |

#### 图表生成（Generate Chart）

| 子类型 | 关键词 | 图表类型 |
|--------|--------|----------|
| 流程图 | "流程图"、"flowchart" | flowchart |
| 架构图 | "架构图"、"系统图" | graph |
| 时序图 | "时序图"、"sequence" | sequenceDiagram |
| 类图 | "类图" | classDiagram |
| 状态图 | "状态图" | stateDiagram |

---

## 关键词匹配规则

### 匹配优先级

```
1. 精确匹配 > 2. 模糊匹配 > 3. 语义推断
```

### 关键词权重

| 关键词 | 权重 | 意图类型 |
|--------|------|----------|
| "如何" | 0.9 | 文档查询 |
| "规范" | 0.9 | 文档查询 |
| "生成" | 0.95 | 文档生成 |
| "创建" | 0.9 | 文档生成 |
| "接口" | 0.8 | 代码查询 |
| "流程图" | 0.95 | 图表生成 |
| "架构" | 0.85 | 文档查询 / 图表生成 |
| "结构" | 0.9 | 结构查询 |

### 组合关键词

| 组合 | 意图类型 | 示例 |
|------|----------|------|
| "生成" + "API" | 文档生成 | "生成用户 API 文档" |
| "如何" + "写" | 文档查询 | "如何写 README" |
| "画出" + "流程图" | 图表生成 | "画出登录流程图" |
| "查询" + "接口" | 代码查询 | "查询登录接口" |

---

## 路由决策逻辑

### 决策树

```python
def route_intent(user_input: str, project_context: dict) -> Intent:
    # 1. 关键词提取
    keywords = extract_keywords(user_input)
    
    # 2. 意图分类
    if contains(keywords, ["生成", "创建"]):
        if contains(keywords, ["API", "接口"]):
            return Intent.GENERATE_API_DOC
        elif contains(keywords, ["模块"]):
            return Intent.GENERATE_MODULE_DOC
        elif contains(keywords, ["服务"]):
            return Intent.GENERATE_SERVICE_DOC
        else:
            return Intent.GENERATE_DOC
    
    elif contains(keywords, ["如何", "规范", "格式"]):
        if contains(keywords, ["API", "接口"]):
            return Intent.QUERY_API_GUIDE
        elif contains(keywords, ["架构"]):
            return Intent.QUERY_ARCHITECTURE_GUIDE
        else:
            return Intent.QUERY_GUIDE
    
    elif contains(keywords, ["流程图", "架构图", "时序图"]):
        return Intent.GENERATE_CHART
    
    elif contains(keywords, ["接口", "函数", "类"]):
        return Intent.QUERY_CODE
    
    elif contains(keywords, ["结构", "目录"]):
        return Intent.QUERY_STRUCTURE
    
    else:
        return Intent.GENERAL_QUERY
```

### 路由表

| 意图 | 处理函数 | 输入参数 | 输出 |
|------|----------|----------|------|
| `QUERY_GUIDE` | `get_guide_content()` | `guide_path` | Markdown 文档内容 |
| `GENERATE_API_DOC` | `generate_api_doc()` | `service_name`, `code_context` | 完整 API 文档 |
| `GENERATE_CHART` | `generate_mermaid_chart()` | `chart_type`, `content` | Mermaid 代码 |
| `QUERY_CODE` | `extract_code_info()` | `target`, `filters` | 代码信息 |
| `QUERY_STRUCTURE` | `get_wiki_structure()` | - | Wiki 结构说明 |

---

## 上下文增强

### 项目上下文

**来源**：`project-analysis.json`

```json
{
  "languages": ["Python"],
  "frameworks": ["fastapi"],
  "documents": {
    "existing": ["README.md"],
    "recommended": ["API.md", "CHANGELOG.md"]
  }
}
```

**用途**：
- 框架相关查询 → 返回对应框架指引
- 文档生成 → 选择合适模板
- 图表生成 → 生成符合技术栈的图表

### 用户上下文

**来源**：历史对话、当前文件、操作记录

**用途**：
- 引用之前讨论的内容
- 结合当前文件上下文回答
- 提供个性化建议

### 文档上下文

**来源**：已生成的文档内容

**用途**：
- 检测文档是否符合规范
- 提供改进建议
- 关联相关文档

---

## 处理流程

### 完整流程

```
用户输入
    ↓
关键词提取
    ↓
意图识别
    ↓
┌─────────┬──────────┬──────────┬──────────┐
│文档查询  │文档生成  │代码查询  │图表生成  │
↓         ↓         ↓         ↓
读取指南  读取模板   提取代码   生成Mermaid
↓         ↓         ↓         ↓
格式化   填充模板   格式化     格式化
↓         ↓         ↓         ↓
返回内容  返回文档  返回信息   返回图表
    └─────────┴──────────┴──────────┘
                    ↓
              附加相关文档链接
                    ↓
              返回最终响应
```

### 响应模板

#### 文档查询响应

```markdown
## [文档标题]

[文档内容]

### 相关文档
- [相关文档1](path/to/doc1.md)
- [相关文档2](path/to/doc2.md)
```

#### 文档生成响应

```markdown
## 生成的文档

### 文档名称
[文档标题]

### 文档内容
```markdown
[完整文档]
```

### 使用说明
1. 保存到指定路径
2. 根据实际情况调整
3. 检查规范要求
```

#### 图表生成响应

```markdown
## [图表类型]

### Mermaid 代码
```mermaid
[mermaid 代码]
```

### 渲染方式
- Typora / GitHub / VS Code
- https://mermaid.live/
```

---

## 示例

### 示例 1：文档查询

**用户输入**：
```
"如何编写 API 文档？"
```

**处理流程**：
1. 关键词：`["如何", "编写", "API", "文档"]`
2. 意图：`QUERY_GUIDE` + 上下文：`"API"`
3. 路由：`document-guides/api-doc-guide.md`
4. 返回：API 文档规范内容

---

### 示例 2：文档生成

**用户输入**：
```
"为用户服务生成 API 文档"
```

**处理流程**：
1. 关键词：`["生成", "用户", "服务", "API", "文档"]`
2. 意图：`GENERATE_API_DOC`
3. 上下文：`service_name = "用户服务"`
4. 模板：`templates/api-template.md`
5. 代码提取：`extract_docs.py`
6. 返回：完整的 API 文档

---

### 示例 3：图表生成

**用户输入**：
```
"画出用户注册流程图"
```

**处理流程**：
1. 关键词：`["画出", "用户", "注册", "流程图"]`
2. 意图：`GENERATE_CHART` + 类型：`flowchart`
3. 上下文：`content = "用户注册"`
4. 语法参考：`visualization/mermaid-syntax.md`
5. 返回：Mermaid flowchart 代码

---

## 扩展规则

### 自定义意图

**添加新意图**：

1. 在 `intent-rules.md` 中定义意图类型
2. 添加关键词匹配规则
3. 实现处理函数
4. 更新路由表

### 上下文扩展

**新增上下文来源**：

1. 分析项目配置文件
2. 读取 Git 历史
3. 解析依赖关系
4. 收集用户偏好

---

**最后更新**：2024-02-19
