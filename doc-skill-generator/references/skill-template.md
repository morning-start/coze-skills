# 子技能模板选择指南

本参考文档提供子技能生成时的模板选择和使用说明。

## 目录
- [模板类型](#模板类型)
- [模板选择规则](#模板选择规则)
- [元数据注入规范](#元数据注入规范)
- [模板文件位置](#模板文件位置)

## 概览
生成技术学习子技能时，根据技术栈类型选择合适的预定义模板，动态填充内容。

## 模板类型

### 1. 语言类模板 (language-skill.md)
**适用场景**：
- 编程语言：Go、Python、Rust、TypeScript、Java、C++
- 脚本语言：JavaScript、PHP、Ruby
- 特点：强调语法、数据结构、并发/异步、标准库

**核心章节**：
- 基础语法学习
- 数据结构学习
- 并发编程（如适用）
- Web 开发（如适用）
- 最佳实践

### 2. 框架类模板 (framework-skill.md)
**适用场景**：
- 前端框架：Vue、React、Angular、Svelte
- 后端框架：Django、Flask、Express、Spring Boot
- 特点：强调组件/模块、状态管理、路由、配置

**核心章节**：
- 基础概念学习
- 组件/模块开发
- 状态管理
- 路由与导航
- 构建与部署

### 3. 工具类模板 (tool-skill.md)
**适用场景**：
- 构建工具：Webpack、Vite、Parcel
- 包管理器：npm、yarn、pnpm
- 开发工具：ESLint、Prettier、Docker
- 特点：强调配置、插件、优化、集成

**核心章节**：
- 基础概念学习
- 快速开始
- 配置管理
- 插件系统
- 性能优化
- 项目集成

## 模板选择规则

### 基于文档类型
使用 `scripts/crawl_website.py` 时指定的 `--type` 参数：
- `--type language` → 选择 `language-skill.md`
- `--type framework` → 选择 `framework-skill.md`
- `--type tool` → 选择 `tool-skill.md`

### 基于摘要报告
阅读 `scripts/summarize_pages.py` 生成的 `summary.json`：
```json
{
  "document_structure": {
    "recommended_skill_type": "framework"
  }
}
```

根据 `recommended_skill_type` 字段选择模板。

### 基于关键词识别
如果没有明确类型，根据 URL 和内容关键词推断：

| 关键词 | 推荐类型 |
|--------|----------|
| vuejs.org, react.dev, angular.io | framework |
| go.dev, python.org, rust-lang.org | language |
| webpack.js.org, docker.com, eslint.org | tool |

## 元数据注入规范

### YAML 前言区
在生成的 SKILL.md 中注入以下元数据：

```yaml
---
name: <技术栈名称>-skills
description: <能力描述>
metadata:
  source_url: <官网URL>
  version: <版本号>
  crawled_at: <抓取时间>
  doc_type: <文档类型>
---
```

### 字段说明

**name**
- 格式：`<技术栈名称>-skills`
- 示例：`vue-skills`、`go-skills`、`webpack-skills`

**description**
- 格式：单行文本（100-150 字符）
- 内容：核心能力 + 触发场景
- 示例：
  ```
  Vue.js 框架的系统性学习技能。适用于 Vue 入门学习、组件开发、状态管理、路由配置等场景。
  ```

**metadata.source_url**
- 来源：从用户输入或爬取的 `_crawl_summary.json` 中获取
- 示例：`https://vuejs.org`

**metadata.version**
- 来源：从 `_crawl_summary.json` 中的 `detected_version` 字段获取
- 示例：`v18.3.0`、`3.4.0`、`1.21.5`
- 注意：如果未检测到版本号，此字段可省略

**metadata.crawled_at**
- 来源：从 `_crawl_summary.json` 中的 `crawled_at` 字段获取
- 格式：ISO 8601 时间戳
- 示例：`2025-02-19T05:19:00.000Z`

**metadata.doc_type**
- 来源：从 `_crawl_summary.json` 中的 `doc_type` 字段获取
- 取值：`language`、`framework`、`tool`

### 文档元数据
在每个参考文档的文件头部注入元数据：

```markdown
# 核心概念

<!--
Source URL: https://vuejs.org/guide/essentials/reactivity-fundamentals.html
Crawled at: 2025-02-19T05:19:00.000Z
Version: 3.4.0
-->
```

## 模板文件位置

所有模板文件位于 `references/templates/` 目录：

```
references/templates/
├── language-skill.md    # 语言类模板
├── framework-skill.md   # 框架类模板
└── tool-skill.md        # 工具类模板
```

### 使用方式

1. **读取模板**
```python
from pathlib import Path

doc_type = "framework"  # 从摘要报告获取
template_path = Path(f"references/templates/{doc_type}-skill.md")
template_content = template_path.read_text()
```

2. **动态填充**
使用字符串替换或模板引擎（如 Jinja2）填充占位符：
```python
filled_content = template_content.replace("<框架名称>", "Vue")
filled_content = filled_content.replace("<核心概念>", "响应式系统、组件化")
```

3. **保存文件**
```python
output_path = Path("vue-skills/SKILL.md")
output_path.write_text(filled_content)
```

## 模板填充示例

### 语言类模板填充（Go 语言）

**占位符替换**：
- `<语言名称>` → `Go`
- `<运行时环境>` → `Go`
- `<最低版本>` → `1.21`
- `<版本检查命令>` → `go version`
- `<安装命令>` → `go install golang.org/dl/go1.21.5@latest`
- `<验证命令>` → `go version`
- `<并发机制1>` → `Goroutines`
- `<并发机制2>` → `Channels`

### 框架类模板填充（Vue.js）

**占位符替换**：
- `<框架名称>` → `Vue`
- `<核心概念1>` → `响应式系统`
- `<核心概念2>` → `虚拟DOM`
- `<核心概念3>` → `组件生命周期`
- `<组件扩展名>` → `.vue`
- `<配置文件1>` → `package.json`
- `<配置文件2>` → `vite.config.js`

### 工具类模板填充（Webpack）

**占位符替换**：
- `<工具名称>` → `Webpack`
- `<工具包名>` → `webpack`
- `<最低版本>` → `5.0`
- `<初始化命令>` → `npm init -y && npm install --save-dev webpack webpack-cli`
- `<验证命令>` → `npx webpack --version`
- `<配置扩展名>` → `.js`

## 注意事项

### 模板版本管理
- 模板文件应保持最新状态
- 修改模板时确保向后兼容
- 记录模板的变更历史

### 占位符一致性
- 确保所有占位符格式统一（使用 `<尖括号>`）
- 提供占位符替换指南
- 避免使用歧义的占位符名称

### 元数据完整性
- 确保所有元数据字段都有来源
- 对于缺失的字段，提供默认值或省略
- 保持元数据格式的一致性

### 验证机制
- 填充后的模板应通过 `validate_skill.py` 验证
- 检查所有必填字段是否填充
- 验证格式和内容质量
