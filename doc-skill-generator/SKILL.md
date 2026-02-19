---
name: doc-skill-generator
description: 根据技术官网自动生成Skill子技能包的母技能。支持Vue、React、Go等技术栈，具备智能抓取、内容摘要、模板填充、验证测试等功能。
dependency:
  python:
    - crawl4ai>=0.4.0
---
# Doc Skill Generator

## 任务目标

本 Skill 用于从技术框架或编程语言的官方网站自动提取文档内容，并通过智能分析生成符合规范的 Skill 子技能包，帮助用户系统性学习该技术栈。

### 核心能力

- 智能抓取官网文档（基于类型过滤路径）
- 自动提取版本号和元数据
- LLM 内容摘要与核心能力图谱生成
- 模板化子技能生成（语言类/框架类/工具类）
- 自动验证技能完整性

### 触发条件

典型用户表达：

- "帮我生成一个 Vue 的学习技能包"
- "根据 React 官网创建对应的技能"
- "我需要一个 Go 语言的技能包"
- "生成基于 TypeScript 官网的技能"

## 前置准备

### 依赖安装

```
crawl4ai>=0.4.0
playwright==1.40.0
```

### Playwright 浏览器初始化（首次使用）

```bash
playwright install chromium
```

## 操作步骤

### 1. 信息收集与准备

从用户请求中提取以下信息：

- 官网 URL（必需）
- 技术栈名称（可选，可从 URL 推断）
- 文档类型（语言类/framework类/tool类，可选，可智能推断）
- 抓取深度（可选，默认 2 层）

### 2. 网站文档抓取（增强版）

调用 `scripts/crawl_website.py` 抓取官网内容：

```bash
python scripts/crawl_website.py \
  --url "https://vuejs.org" \
  --depth 2 \
  --output "/workspace/projects/vue-skills/raw_docs" \
  --type framework
```

参数说明：

- `--url`: 官网地址
- `--depth`: 抓取深度（建议 2-3 层）
- `--output`: 文档输出目录
- `--max-pages`: 最大抓取页面数（默认 50）
- `--type`: 文档类型（language/framework/tool）

**增强功能**：

- 智能路径过滤：仅抓取 /docs/、/guide/、/api/ 等文档路径
- 自动版本检测：从首页提取版本号
- 元数据注入：在文件头部记录来源 URL、抓取时间、版本号

### 3. 内容摘要与分析

调用 `scripts/summarize_pages.py` 生成摘要报告：

```bash
python scripts/summarize_pages.py \
  --input "/workspace/projects/vue-skills/raw_docs" \
  --output "/workspace/projects/vue-skills/summary.json" \
  --type framework
```

**输出内容**：

- 页面基本信息统计
- 文档结构分析（API/指南/示例分布）
- 核心概念图谱（基础版）
- 技能类型推荐
- 优先阅读页面列表

### 4. 子技能模板选择与填充

根据摘要报告，智能体选择合适的模板并填充内容：

#### 4.1 选择模板

根据文档类型从 `references/templates/` 选择：

- `language-skill.md` - 编程语言类（Go、Python、Rust）
- `framework-skill.md` - 前端框架类（Vue、React、Angular）
- `tool-skill.md` - 工具类（Webpack、Docker、ESLint）

#### 4.2 填充元数据

从摘要报告中提取：

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

#### 4.3 填充核心内容

基于摘要报告和原文档，智能体填充：

- **任务目标**：根据核心概念图谱生成
- **核心能力**：从文档结构分析中提取
- **操作步骤**：按学习路径组织
- **资源索引**：链接到对应的参考文档

#### 4.4 生成参考文档

从抓取的文档中提取关键内容：

- `core-concepts.md` - 核心概念详解（>100 行，含 TOC）
- `api-reference.md` - API 参考文档
- `best-practices.md` - 最佳实践指南
- `examples.md` - 实战示例代码

#### 4.5 生成代码模板

从官方文档提取可运行示例：

- `assets/hello-world.*` - Hello World 示例
- `assets/basic-template.*` - 基础模板
- `assets/advanced-example.*` - 进阶示例

### 5. 技能验证（可选）

调用 `scripts/validate_skill.py` 验证生成的技能：

```bash
python scripts/validate_skill.py \
  --skill-path "/workspace/projects/vue-skills" \
  --output "/workspace/projects/vue-skills/validation_report.json"
```

**验证内容**：

- 元数据完整性检查
- 目录结构规范检查
- 内容质量检查（description 长度、行数限制）
- 自动生成测试问题

### 6. 打包交付

调用打包工具生成 `.skill` 文件：

```bash
package_skill(skill_dir_name="<技术栈名称>-skills")
```

## 资源索引

### 必要脚本

- [scripts/crawl_website.py](scripts/crawl_website.py)

  - 用途：抓取官网文档并转换为 Markdown
  - 参数：url（必需）、depth、output、type
  - 增强功能：路径过滤、版本检测、元数据注入
- [scripts/summarize_pages.py](scripts/summarize_pages.py)

  - 用途：生成内容摘要和核心能力图谱
  - 参数：input（必需）、output、type
  - 输出：JSON 格式的摘要报告
- [scripts/validate_skill.py](scripts/validate_skill.py)

  - 用途：验证技能完整性和可用性
  - 参数：skill-path（必需）、output
  - 输出：JSON 格式的验证报告

### 领域参考

- [references/common-doc-patterns.md](references/common-doc-patterns.md)
  - 何时读取：分析技术文档结构时
  - 内容：常见技术栈文档的组织模式

### 技能模板

- [references/templates/language-skill.md](references/templates/language-skill.md)

  - 适用场景：编程语言类技能（Go、Python、Rust）
  - 内容：基础语法、数据结构、并发编程、Web 开发
- [references/templates/framework-skill.md](references/templates/framework-skill.md)

  - 适用场景：前端框架类技能（Vue、React、Angular）
  - 内容：核心概念、组件开发、状态管理、路由配置
- [references/templates/tool-skill.md](references/templates/tool-skill.md)

  - 适用场景：工具类技能（Webpack、Docker、ESLint）
  - 内容：配置管理、插件系统、性能优化、项目集成

## 注意事项

### 爬取策略优化

- 根据文档类型自动过滤路径，避免抓取无关页面
- 控制抓取深度和页面数，避免对目标网站造成压力
- 遵守网站 robots.txt 规则

### 内容提炼

- 智能体应优先阅读摘要报告，快速了解文档结构
- 核心能力图谱有助于设计子技能的学习路径
- 重点关注教程、API 参考、最佳实践等核心文档

### 技能模板化

- 根据文档类型自动选择合适的模板
- 动态填充元数据（来源 URL、版本号、抓取时间）
- 保持模板的一致性和规范性

### 验证机制

- 建议在打包前运行验证脚本
- 检查所有验证项是否通过
- 根据验证报告修复问题

### 智能体职责边界

- ✅ 智能体负责：内容分析、模板选择、文档生成、示例创作
- ✅ 智能体负责：根据摘要报告设计子技能结构
- ❌ 智能体不负责：HTML 解析、链接发现、文件格式转换
- ❌ 智能体不负责：元数据提取（由脚本完成）

## 使用示例

### 示例 1：生成 Vue 学习技能（框架类）

```bash
# 1. 抓取 Vue 官网
python scripts/crawl_website.py \
  --url "https://vuejs.org" \
  --depth 2 \
  --output "./vue-skills/raw_docs" \
  --type framework

# 2. 生成摘要
python scripts/summarize_pages.py \
  --input "./vue-skills/raw_docs" \
  --output "./vue-skills/summary.json" \
  --type framework

# 3. 智能体选择 framework-skill.md 模板并填充内容
# 4. 生成参考文档和代码模板
# 5. 验证技能
python scripts/validate_skill.py \
  --skill-path "./vue-skills" \
  --output "./vue-skills/validation.json"

# 6. 打包交付
package_skill(skill_dir_name="vue-skills")
```

### 示例 2：生成 Go 语言技能（语言类）

```bash
# 1. 抓取 Go 官网
python scripts/crawl_website.py \
  --url "https://go.dev/doc" \
  --depth 3 \
  --max-pages 100 \
  --output "./go-skills/raw_docs" \
  --type language

# 2. 生成摘要
python scripts/summarize_pages.py \
  --input "./go-skills/raw_docs" \
  --output "./go-skills/summary.json" \
  --type language

# 3. 智能体选择 language-skill.md 模板并填充内容
# 4. 重点关注并发编程、Web 开发等内容
# 5. 打包交付
```

### 示例 3：生成 Webpack 技能（工具类）

```bash
# 1. 抓取 Webpack 官网
python scripts/crawl_website.py \
  --url "https://webpack.js.org" \
  --depth 2 \
  --output "./webpack-skills/raw_docs" \
  --type tool

# 2. 生成摘要
python scripts/summarize_pages.py \
  --input "./webpack-skills/raw_docs" \
  --output "./webpack-skills/summary.json" \
  --type tool

# 3. 智能体选择 tool-skill.md 模板并填充内容
# 4. 重点关注配置管理、插件系统、优化技巧
# 5. 打包交付
```

## 技术架构说明

### 抓取策略优化

- **路径过滤**：根据文档类型（language/framework/tool）预设不同的路径过滤规则
- **版本检测**：从首页 HTML 中自动提取版本号
- **元数据注入**：在每个 Markdown 文件头部注入来源 URL、抓取时间、版本号

### 内容提炼

- **摘要生成**：使用脚本统计页面基本信息（字数、文档类型）
- **文档结构分析**：识别 API、指南、示例等不同类型的文档
- **核心能力图谱**：基于标题和内容提取潜在概念（基础版）

### 技能模板化

- **三种模板**：语言类、框架类、工具类，覆盖常见技术栈
- **动态填充**：根据摘要报告自动填充元数据和核心内容
- **一致性保证**：确保生成的子技能符合统一的格式规范

### 验证机制

- **元数据检查**：验证 YAML 前言区的完整性
- **结构检查**：验证目录结构符合规范
- **内容质量检查**：验证 description 长度、行数限制等
- **测试问题生成**：自动生成测试问题，验证技能可用性
