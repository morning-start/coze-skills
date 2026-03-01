---
name: book-skill-creator
version: v1.2.0
author: skill-manager
description: 技能工厂母技能，根据官方文档、技术书籍或规范生成技术技能（如golang-skill、vue-skill），支持网络搜索补充最佳实践，适用于Vue、React、Go、Python等技术栈
tags: [skill-generation, documentation, web-search, best-practices, code-generation]
dependency:
  python:
    - pyyaml>=6.0
    - networkx>=3.0
---

# Book Skill Creator - 技能工厂

## 任务目标

**核心能力**
- 本 Skill 用于：根据官方文档、技术书籍或规范性文档生成技术技能
- 能力包含：
  - **文档解析**：使用 Read/WebFetch 工具解析官方文档、技术书籍
  - **网络搜索补充**：使用 WebSearch 工具搜索最佳实践和行业经验
  - **技能生成**：生成符合规范的 SKILL.md 及相关参考文档
  - **质量验证**：使用 skill-standards 进行标准化检验
- 触发条件：
  - 用户需要从官方文档生成技能（如 React 官方文档 → react-skill）
  - 用户需要从技术书籍生成技能（如《Go 语言圣经》→ golang-skill）
  - 用户需要从规范文档生成技能（如 OpenAPI 规范 → api-skill）

**可选能力**
- 批量生成相关技能族
- 技能模板复用和定制
- 技能依赖关系分析

## 核心工作流程

```
文档输入（官方文档/书籍/规范）
    ↓
智能体解析（使用 Read/WebFetch 工具）
    ↓
网络搜索补充（使用 WebSearch 工具）
    ↓
技能生成（输出 SKILL.md 及相关文件）
    ↓
质量验证（使用 skill-standards 检验）
```

## 操作步骤

### 步骤 1：文档解析

1. **获取文档来源**
   - 用户提供的文档路径或 URL
   - 支持的格式：Markdown、HTML、在线文档

2. **解析文档内容**
   - 使用 **Read** 工具读取本地文档
   - 使用 **WebFetch** 工具获取在线文档
   - 提取核心内容：
     - 技术概述和核心概念
     - API 参考和函数列表
     - 配置选项和参数
     - 代码示例和最佳实践
     - 常见问题和解决方案

3. **结构化提取**
   - 整理技术的主要功能点
   - 分类整理 API 或函数
   - 提取配置项和默认值
   - 收集代码示例

### 步骤 2：网络搜索补充

1. **搜索最佳实践**
   - 使用 **WebSearch** 工具搜索：
     - `"{技术名} best practices 2025"`
     - `"{技术名} production ready patterns"`
     - `"{技术名} common pitfalls"`
     - `"{技术名} real world examples"`

2. **筛选高质量内容**
   - 优先官方文档和权威博客
   - 选择近期更新的内容
   - 关注高赞/高星的项目和文章

3. **提取补充内容**
   - 行业最佳实践
   - 生产环境配置建议
   - 性能优化技巧
   - 常见问题解决方案

### 步骤 3：技能生成

1. **创建技能目录**
   ```bash
   mkdir {skill-name}/
   mkdir {skill-name}/references/
   mkdir {skill-name}/assets/
   ```

2. **编写 SKILL.md**
   - 前言区：name、version、author、description、tags
   - 任务目标：核心能力、可选能力、触发条件
   - 操作步骤：详细的使用步骤
   - 资源索引：references 和 assets
   - 使用示例：具体场景示例
   - 注意事项：关键提醒

3. **生成参考文档**
   - 技术概述文档
   - API 参考文档
   - 最佳实践文档
   - 常见问题文档

### 步骤 4：质量验证

1. **标准化检验**
   - 前言区字段完整性（name、version、author、description、tags）
   - description 长度 100-150 字符
   - tags 至少 3 个
   - 正文包含必需章节

2. **内容质量检查**
   - 操作步骤清晰可执行
   - 使用示例完整
   - 资源索引准确

## 资源索引

| 资源 | 路径 | 用途 |
|------|------|------|
| 技能规范 | [references/skill-specs.md](references/skill-specs.md) | SKILL.md 编写规范 |
| 框架指南 | [references/frameworks-guide.md](references/frameworks-guide.md) | 常用框架分类和使用场景 |
| 最佳实践 | [references/best-practices.md](references/best-practices.md) | 方案分类和解决方案 |
| API 技能模板 | [assets/skill-templates/api-skill.md](assets/skill-templates/api-skill.md) | API 类技能模板 |
| 数据处理模板 | [assets/skill-templates/data-process.md](assets/skill-templates/data-process.md) | 数据处理类技能模板 |
| 工作流模板 | [assets/skill-templates/workflow.md](assets/skill-templates/workflow.md) | 工作流类技能模板 |

## 注意事项

- **文档来源可靠**：优先使用官方文档和权威技术书籍
- **网络搜索策略**：使用多个关键词组合，确保覆盖全面
- **内容去重**：避免重复提取相同内容
- **标准化优先**：生成后必须执行标准化检验
- **版本管理**：技能版本遵循语义化版本规范
- **向后兼容**：修改时尽量保持向后兼容

## 使用示例

### 示例 1：从 React 官方文档生成 react-skill

**用户需求**：根据 React 官方文档生成一个完整的 react-skill

**执行流程**：

1. **文档解析**
   - 使用 WebFetch 获取 React 官方文档（https://react.dev/）
   - 提取核心概念：组件、Props、State、Hooks、生命周期
   - 提取 API 参考：useState、useEffect、useContext 等
   - 提取代码示例和最佳实践

2. **网络搜索补充**
   - 搜索 "React best practices 2025"
   - 搜索 "React production patterns"
   - 搜索 "React performance optimization"
   - 提取社区最佳实践

3. **技能生成**
   - 创建 react-skill/ 目录
   - 编写 SKILL.md：
     - 核心能力：组件开发、Hooks 使用、状态管理
     - 操作步骤：创建组件、使用 Hooks、性能优化
     - 使用示例：计数器、Todo 列表、数据获取
   - 生成 references/react-hooks-guide.md
   - 生成 references/react-patterns.md

4. **质量验证**
   - 验证前言区字段完整性
   - 验证 description 长度
   - 验证操作步骤清晰

### 示例 2：从 Go 语言规范生成 golang-skill

**用户需求**：根据 Go 语言规范生成 golang-skill

**执行流程**：

1. **文档解析**
   - 使用 WebFetch 获取 Go 官方文档（https://go.dev/doc/）
   - 提取核心概念：Goroutine、Channel、Interface、Struct
   - 提取标准库：net/http、database/sql、encoding/json 等
   - 提取代码示例

2. **网络搜索补充**
   - 搜索 "Go best practices 2025"
   - 搜索 "Go project structure"
   - 搜索 "Go error handling patterns"
   - 提取 Go 语言惯用法

3. **技能生成**
   - 创建 golang-skill/ 目录
   - 编写 SKILL.md：
     - 核心能力：并发编程、标准库使用、项目结构
     - 操作步骤：编写函数、使用 Goroutine、错误处理
     - 使用示例：HTTP 服务、数据库操作、并发处理
   - 生成 references/go-concurrency.md
   - 生成 references/go-stdlib.md

4. **质量验证**
   - 执行标准化检验
   - 确保所有必需章节存在

### 示例 3：网络搜索补充最佳实践

**场景**：用户提供了某技术的文档，但需要补充最佳实践

**执行流程**：

1. **分析已有文档**
   - 识别文档中缺少的内容（如性能优化、安全建议）

2. **针对性搜索**
   - 搜索 "{技术名} performance tips"
   - 搜索 "{技术名} security best practices"
   - 搜索 "{技术名} common mistakes"

3. **整合补充**
   - 将搜索到的最佳实践整合到 SKILL.md
   - 生成专门的 best-practices.md 参考文档

## 质量门槛

### 生成前检查
- [ ] 文档来源可靠（官方/权威）
- [ ] 网络搜索覆盖全面
- [ ] 内容去重完成

### 生成后检查
- [ ] 前言区字段完整
- [ ] description 长度 100-150 字符
- [ ] tags 至少 3 个
- [ ] 操作步骤清晰
- [ ] 使用示例完整
- [ ] 资源索引准确

## 框架速查

### Web 框架
- **React**：组件化 UI 库，虚拟 DOM
- **Vue**：渐进式框架，响应式数据
- **FastAPI**：高性能 Python API 框架
- **Express**：Node.js Web 框架

### 后端语言
- **Go**：高性能并发，静态类型
- **Python**：简洁易读，生态丰富
- **Rust**：内存安全，高性能

### 数据库
- **PostgreSQL**：关系型数据库
- **MongoDB**：文档型数据库
- **Redis**：内存数据库

详细使用方法见 [references/frameworks-guide.md](references/frameworks-guide.md)
