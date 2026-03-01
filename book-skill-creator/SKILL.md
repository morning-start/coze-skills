---
name: book-skill-creator
version: v2.0.0
author: skill-manager
description: 技能工厂母技能，分析官方文档/技术书籍，生成技能拆分计划，支持并行生成多个技术技能（如golang-skill、vue-skill、react-skill），适用于Vue、React、Go、Python等技术栈
tags: [skill-generation, documentation, planning, parallel-execution, web-search, best-practices]
dependency:
  python:
    - pyyaml>=6.0
    - networkx>=3.0
---

# Book Skill Creator - 技能工厂

## 任务目标

**核心能力**
- 本 Skill 用于：分析官方文档/技术书籍，生成技能拆分计划，支持并行生成多个技术技能
- 能力包含：
  - **文档分析**：使用 Read/WebFetch 工具解析文档，提取技术模块和知识点
  - **网络搜索补充**：使用 WebSearch 工具搜索最佳实践，完善分析结果
  - **技能拆分规划**：根据分析结果生成技能拆分计划（哪些技能、每个技能内容）
  - **并行生成执行**：生成可并行执行的技能生成计划，智能体按步骤执行
  - **质量验证**：使用 skill-standards 进行标准化检验
- 触发条件：
  - 用户需要从大型文档生成多个技能（如 React 文档 → react-core-skill、react-hooks-skill、react-router-skill）
  - 用户需要从技术书籍生成技能族（如《Go 语言圣经》→ golang-basic-skill、golang-concurrency-skill、golang-web-skill）
  - 用户需要从规范文档生成相关技能（如 OpenAPI 规范 → api-design-skill、api-testing-skill、api-doc-skill）

**可选能力**
- 技能依赖关系分析和排序
- 批量技能模板复用
- 技能版本协调管理

## 核心工作流程

```
阶段 1：分析规划（Analysis & Planning）
├── 文档解析（Read/WebFetch）
├── 网络搜索补充（WebSearch）
├── 技术模块识别
└── 技能拆分计划生成

阶段 2：并行生成（Parallel Generation）
├── 技能 A 生成（独立执行）
├── 技能 B 生成（独立执行）
├── 技能 C 生成（独立执行）
└── ...（其他技能并行生成）

阶段 3：质量验证（Quality Verification）
├── 各技能独立验证
├── 技能间一致性检查
└── 整体质量报告
```

## 操作步骤

### 阶段 1：分析规划

#### 步骤 1.1：文档解析与初步分析

1. **获取文档来源**
   - 用户提供的文档路径或 URL
   - 支持的格式：Markdown、HTML、在线文档、PDF

2. **解析文档结构**
   - 使用 **Read** 工具读取本地文档
   - 使用 **WebFetch** 工具获取在线文档
   - 提取文档目录结构和章节划分

3. **识别技术模块**
   - 分析文档章节，识别独立的技术模块
   - 每个模块应包含：
     - 核心概念和原理
     - API/函数/配置参考
     - 代码示例
     - 最佳实践
   - 记录模块间的依赖关系

4. **输出初步分析结果**
   ```markdown
   ## 文档分析结果

   ### 文档信息
   - **标题**：{文档标题}
   - **来源**：{文档 URL 或路径}
   - **总章节数**：{N} 章

   ### 识别的技术模块
   | 模块名称 | 章节范围 | 核心内容 | 依赖模块 |
   |---------|---------|---------|---------|
   | {模块1} | 第1-3章 | {核心概念} | 无 |
   | {模块2} | 第4-6章 | {API参考} | 模块1 |
   | {模块3} | 第7-9章 | {高级特性} | 模块1,2 |

   ### 模块依赖图
   ```
   模块1 → 模块2 → 模块3
   ```
   ```

#### 步骤 1.2：网络搜索补充

1. **搜索各模块最佳实践**
   - 对每个技术模块使用 **WebSearch** 搜索：
     - `"{技术名} {模块名} best practices 2025"`
     - `"{技术名} {模块名} production patterns"`
     - `"{技术名} {模块名} common pitfalls"`

2. **补充行业经验**
   - 提取生产环境配置建议
   - 收集性能优化技巧
   - 整理常见问题解决方案

3. **完善模块分析**
   - 补充每个模块的实战场景
   - 添加模块间的关联使用案例

#### 步骤 1.3：生成技能拆分计划

1. **设计技能拆分方案**
   - 根据技术模块划分技能边界
   - 每个技能对应一个或多个相关模块
   - 确保技能间职责清晰、依赖合理

2. **生成技能拆分计划文档**

   ```markdown
   # 技能拆分计划：{技术名称}

   ## 计划概述
   - **源文档**：{文档标题}
   - **计划生成时间**：{日期}
   - **预计生成技能数**：{N} 个

   ## 技能清单

   ### 技能 1：{skill-name-1}
   - **对应模块**：{模块1, 模块2}
   - **技能定位**：{基础/核心/高级}
   - **核心内容**：
     - {内容点1}
     - {内容点2}
     - {内容点3}
   - **依赖技能**：{无/技能X}
   - **预计复杂度**：{低/中/高}

   ### 技能 2：{skill-name-2}
   - **对应模块**：{模块3}
   - **技能定位**：{基础/核心/高级}
   - **核心内容**：
     - {内容点1}
     - {内容点2}
   - **依赖技能**：{技能1}
   - **预计复杂度**：{低/中/高}

   ## 执行策略

   ### 并行执行组
   - **第1组**（无依赖，可并行）：
     - [ ] {skill-name-1}
   - **第2组**（依赖第1组，可并行）：
     - [ ] {skill-name-2}
     - [ ] {skill-name-3}
   - **第3组**（依赖前两组，可并行）：
     - [ ] {skill-name-4}

   ### 生成顺序建议
   1. 先生成基础技能（无依赖）
   2. 再并行生成依赖基础技能的核心技能
   3. 最后生成高级技能
   ```

3. **与用户确认计划**
   - 展示技能拆分计划
   - 根据用户反馈调整
   - 确认最终执行方案

### 阶段 2：并行生成

#### 步骤 2.1：准备并行生成环境

1. **创建技能目录结构**
   ```bash
   mkdir -p {tech-name}-skills/
   cd {tech-name}-skills/
   ```

2. **准备共享资源**
   - 创建 `shared/` 目录存放公共资源
   - 提取共享的概念定义
   - 整理共享的代码示例

#### 步骤 2.2：执行并行生成

根据技能拆分计划，**智能体并行执行**各技能的生成：

**并行生成模式**：

```
智能体实例 A ──▶ 生成技能 1 ──▶ 质量验证
智能体实例 B ──▶ 生成技能 2 ──▶ 质量验证
智能体实例 C ──▶ 生成技能 3 ──▶ 质量验证
     ...           ...            ...
```

**每个技能的生成流程**：

1. **读取技能定义**
   - 从技能拆分计划获取该技能的定义
   - 确定对应的文档章节

2. **提取相关内容**
   - 使用 **Read** 提取对应章节内容
   - 整理核心概念、API、示例

3. **搜索补充资料**
   - 使用 **WebSearch** 搜索该技能的专项最佳实践
   - 补充实战案例和常见问题

4. **生成 SKILL.md**
   - 编写前言区（name、version、author、description、tags）
   - 编写任务目标（核心能力、可选能力、触发条件）
   - 编写操作步骤（详细使用步骤）
   - 编写资源索引
   - 编写使用示例
   - 编写注意事项

5. **生成参考文档**
   - 创建 `references/` 目录
   - 生成技术概述文档
   - 生成 API 参考文档
   - 生成最佳实践文档

6. **独立质量验证**
   - 验证前言区字段完整性
   - 验证 description 长度
   - 验证操作步骤清晰
   - 标记为"已完成"

#### 步骤 2.3：并行执行示例

**以 React 文档为例**：

```markdown
## 并行生成执行记录

### 第1组（并行执行）
- [x] **react-core-skill** （智能体 A 执行）
  - 状态：已完成
  - 验证：通过
  - 耗时：15分钟

### 第2组（并行执行）
- [x] **react-hooks-skill** （智能体 B 执行）
  - 状态：已完成
  - 验证：通过
  - 耗时：12分钟

- [x] **react-router-skill** （智能体 C 执行）
  - 状态：已完成
  - 验证：通过
  - 耗时：10分钟

### 第3组（并行执行）
- [x] **react-testing-skill** （智能体 D 执行）
  - 状态：已完成
  - 验证：通过
  - 耗时：8分钟
```

### 阶段 3：质量验证

#### 步骤 3.1：各技能独立验证

每个技能生成后自动执行：
- [ ] 前言区字段完整性检查
- [ ] description 长度检查（100-150 字符）
- [ ] tags 数量检查（至少 3 个）
- [ ] 操作步骤清晰性检查
- [ ] 使用示例完整性检查

#### 步骤 3.2：技能间一致性检查

1. **命名一致性**
   - 检查技能名称风格统一
   - 验证 tags 分类一致

2. **内容一致性**
   - 检查共享概念的描述一致
   - 验证示例代码风格统一

3. **依赖关系验证**
   - 确认依赖的技能已生成
   - 验证依赖关系正确

#### 步骤 3.3：生成质量报告

```markdown
# 技能生成质量报告

## 生成统计
- **计划技能数**：{N} 个
- **成功生成**：{M} 个
- **成功率**：{M/N*100}%
- **总耗时**：{X} 分钟

## 各技能详情
| 技能名称 | 状态 | 验证结果 | 备注 |
|---------|------|---------|------|
| {skill-1} | ✅ 完成 | 通过 | 无 |
| {skill-2} | ✅ 完成 | 通过 | 无 |
| {skill-3} | ⚠️ 完成 | 需优化 | description 过长 |

## 问题与建议
- {问题1}：{解决方案}
- {问题2}：{解决方案}

## 下一步行动
- [ ] 修复验证失败的技能
- [ ] 优化 description 长度
- [ ] 统一代码示例风格
```

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

### 分析规划阶段
- **模块划分原则**：高内聚、低耦合，每个模块职责单一
- **依赖关系识别**：准确识别模块间的依赖，避免循环依赖
- **复杂度评估**：合理评估每个技能的复杂度，便于分配资源

### 并行生成阶段
- **独立执行**：每个技能生成应独立，避免相互干扰
- **资源共享**：共享的概念和代码放在 `shared/` 目录
- **进度跟踪**：实时跟踪各技能的生成进度

### 质量验证阶段
- **独立验证**：每个技能先生成后独立验证
- **一致性检查**：最后统一检查技能间的一致性
- **问题修复**：发现问题及时修复，重新验证

## 使用示例

### 示例 1：从 React 文档生成技能族

**用户需求**：根据 React 官方文档生成多个相关技能

**阶段 1：分析规划**

1. **文档解析**
   - 使用 WebFetch 获取 React 文档结构
   - 识别模块：核心概念、Hooks、Router、Testing、Performance

2. **网络搜索补充**
   - 搜索 "React 技能拆分 best practices"
   - 搜索 "React Hooks vs Class Components"

3. **生成技能拆分计划**

   ```markdown
   # 技能拆分计划：React

   ## 技能清单
   ### 技能 1：react-core-skill
   - 对应模块：第1-4章（核心概念、JSX、组件、Props、State）
   - 依赖：无
   - 复杂度：中

   ### 技能 2：react-hooks-skill
   - 对应模块：第5-7章（useState、useEffect、useContext 等）
   - 依赖：react-core-skill
   - 复杂度：中

   ### 技能 3：react-router-skill
   - 对应模块：第8-9章（路由、导航）
   - 依赖：react-core-skill
   - 复杂度：低

   ### 技能 4：react-testing-skill
   - 对应模块：第10章（测试）
   - 依赖：react-core-skill、react-hooks-skill
   - 复杂度：高

   ## 执行策略
   - 第1组：react-core-skill
   - 第2组：react-hooks-skill、react-router-skill（并行）
   - 第3组：react-testing-skill
   ```

**阶段 2：并行生成**

- **智能体 A**：生成 react-core-skill（15分钟）✅
- **智能体 B**：生成 react-hooks-skill（12分钟）✅
- **智能体 C**：生成 react-router-skill（10分钟）✅
- **智能体 D**：生成 react-testing-skill（8分钟）✅

**阶段 3：质量验证**

- 各技能独立验证通过
- 技能间一致性检查通过
- 生成质量报告

### 示例 2：从 Go 语言规范生成技能族

**用户需求**：根据 Go 语言规范生成多个技能

**阶段 1：分析规划**

1. **文档解析**
   - 识别模块：基础语法、并发编程、标准库、Web开发、测试

2. **生成技能拆分计划**

   ```markdown
   # 技能拆分计划：Go

   ## 技能清单
   ### 技能 1：golang-basic-skill
   - 对应模块：基础语法、数据类型、控制流、函数
   - 依赖：无

   ### 技能 2：golang-concurrency-skill
   - 对应模块：Goroutine、Channel、Sync、Context
   - 依赖：golang-basic-skill

   ### 技能 3：golang-stdlib-skill
   - 对应模块：net/http、database/sql、encoding/json
   - 依赖：golang-basic-skill

   ### 技能 4：golang-web-skill
   - 对应模块：Web框架、中间件、路由、模板
   - 依赖：golang-basic-skill、golang-stdlib-skill

   ## 执行策略
   - 第1组：golang-basic-skill
   - 第2组：golang-concurrency-skill、golang-stdlib-skill（并行）
   - 第3组：golang-web-skill
   ```

**阶段 2：并行生成**

- **智能体 A**：生成 golang-basic-skill ✅
- **智能体 B**：生成 golang-concurrency-skill ✅
- **智能体 C**：生成 golang-stdlib-skill ✅
- **智能体 D**：生成 golang-web-skill ✅

### 示例 3：大型框架的技能拆分

**场景**：用户提供了一个大型框架的完整文档，需要拆分为多个技能

**执行流程**：

1. **分析阶段**（30分钟）
   - 解析文档结构（50+ 章节）
   - 识别 8 个技术模块
   - 设计 5 个技能

2. **规划阶段**（15分钟）
   - 生成技能拆分计划
   - 确定并行执行组
   - 分配智能体资源

3. **并行生成阶段**（40分钟）
   - 第1组（1个技能）：15分钟
   - 第2组（2个技能）：12分钟
   - 第3组（2个技能）：13分钟

4. **验证阶段**（10分钟）
   - 各技能独立验证
   - 一致性检查
   - 生成报告

**总耗时**：约 95 分钟生成 5 个高质量技能

## 质量门槛

### 分析规划阶段
- [ ] 文档结构解析完整
- [ ] 技术模块识别准确
- [ ] 依赖关系分析正确
- [ ] 技能拆分合理

### 并行生成阶段
- [ ] 各技能独立生成成功
- [ ] 每个技能通过独立验证
- [ ] 资源共享正确

### 最终验证阶段
- [ ] 所有技能前言区字段完整
- [ ] 所有技能 description 长度符合要求
- [ ] 技能间命名风格一致
- [ ] 共享概念描述一致

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
