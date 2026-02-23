---
name: book-skill-creator
version: 1.0.0
description: 技能工厂核心母技能，兼容基础能力并融合官方文档理解、网络搜索辅助、代码框架生成、子技能自动化构建、框架使用规范和优秀执行方案库，为技能开发与管理工作流提供完整支持方案和最佳实践参考，能有效提升开发效率
---

# Book Skill Creator - 技能工厂

## 任务目标
- 本 Skill 用于：工厂化批量创建和管理技能包，提供从需求分析到自动化生成的完整流程
- 能力包含：官方文档理解、网络搜索辅助、代码框架生成、子技能自动化构建、规范指导、方案沉淀
- 触发条件：用户需要创建多个相关技能、理解技术框架生成技能、查找最佳实践方案、批量生成技能包

## 前置准备
- 依赖说明：scripts 脚本所需的依赖包及版本
  ```
  pyyaml>=6.0
  networkx>=3.0
  ```
- 非标准文件/文件夹准备：无额外要求

## 操作步骤

### 标准流程

#### 1. 需求分析与技术选型
- 理解用户需求：明确要创建的技能类型、数量、功能范围
- 技术选型：根据需求选择合适的框架和实现方式
  - 参考 [references/frameworks-guide.md](references/frameworks-guide.md) 了解框架特性
  - 参考 [references/best-practices.md](references/best-practices.md) 选择最佳实践方案
- 能力映射：判断哪些功能由智能体完成，哪些需要脚本实现

#### 2. 官方文档理解与方案设计
- 用户提供官方文档时：
  - 使用 read_file 读取文档内容
  - 提取核心 API、配置项、使用模式
  - 生成基于文档的技能设计方案
- 自动生成方案：
  - 根据文档内容设计 SKILL.md 结构
  - 规划 scripts/ 中的必要脚本
  - 准备 references/ 中的参考文档

#### 3. 网络搜索辅助
- 当需要查找最佳实践或实现方案时：
  - 搜索关键词："<技术栈> best practices"、"<问题> solution"、"<框架> usage examples"
  - 整理搜索结果：提取关键方案、代码示例、配置方法
  - 整合到技能设计中

#### 4. 批量创建与自动化构建
- 单个技能创建：
  1. 基于需求创建 SKILL.md（可使用 assets/skill-templates/ 中的模板）
  2. 创建必要的 scripts/ 文件（可参考 assets/code-scaffolds/）
  3. 添加 references/ 参考文档
  4. 准备 assets/ 静态资源
- 批量技能创建：
  - 调用 `scripts/batch_create.py` 批量生成技能框架
  - 配置文件格式见 references/skill-specs.md 中的配置规范
  - 支持模板化生成和依赖关系管理

#### 5. 质量验收与验证
- 验证技能结构：
  - 调用 `scripts/skill_validator.py` 验证技能符合规范
  - 检查命名规范、目录结构、文件格式
- 分析依赖关系：
  - 调用 `scripts/dependency_analyzer.py` 分析技能间的依赖
  - 生成依赖图，确保构建顺序正确
- 测试执行：
  - 确保所有脚本可执行
  - 验证 SKILL.md 指导清晰完整

### 可选分支

- 当需求包含官方文档理解：执行文档分析流程，基于文档生成技能
- 当需求包含多个相关技能：执行批量创建流程，使用 batch_create.py
- 当需要选择技术框架：查询 frameworks-guide.md 和 best-practices.md
- 当需要验证技能质量：调用 skill_validator.py 进行验证

## 资源索引

### 必要脚本
- [scripts/batch_create.py](scripts/batch_create.py)
  - 用途：批量创建技能包
  - 参数：--config（配置文件）、--output（输出目录）
  - 输入：JSON 格式配置文件，包含技能列表和配置
- [scripts/skill_validator.py](scripts/skill_validator.py)
  - 用途：验证技能是否符合规范
  - 参数：--skill-path（技能目录路径）
  - 输出：验证结果和问题列表
- [scripts/dependency_analyzer.py](scripts/dependency_analyzer.py)
  - 用途：分析技能间的依赖关系
  - 参数：--base-dir（包含多个技能的基础目录）
  - 输出：依赖关系图和构建顺序

### 领域参考
- [references/skill-specs.md](references/skill-specs.md)
  - 何时读取：需要了解详细规范、配置文件格式、质量门槛
  - 内容：命名规范、目录结构、SKILL.md 格式、验证规则
- [references/frameworks-guide.md](references/frameworks-guide.md)
  - 何时读取：选择技术框架、了解框架使用方法
  - 内容：常用框架分类、使用场景、配置方法、代码模式
- [references/best-practices.md](references/best-practices.md)
  - 何时读取：查找最佳实践方案、参考优秀执行案例
  - 内容：方案分类库、问题场景、解决方案、代码示例

### 输出资产
- [assets/skill-templates/](assets/skill-templates/)
  - api-skill.md：API 调用类技能模板
  - data-process.md：数据处理类技能模板
  - workflow.md：工作流类技能模板
- [assets/code-scaffolds/](assets/code-scaffolds/)
  - python-script.py：Python 脚本脚手架
  - bash-script.sh：Bash 脚本脚手架

## 注意事项

### 实现方式原则
- 充分利用智能体能力：文档理解、代码生成、方案设计由智能体完成
- 合理使用脚本：批量操作、自动化构建、结构验证使用脚本
- 避免过度工程化：简单任务使用自然语言指导，复杂任务编写脚本
- 优先复用模板：使用 assets/ 中的模板和脚手架提高效率

### 质量控制
- 命名规范：小写字母+连字符，禁止 -skill 后缀
- 目录结构：严格遵循固定结构，无额外文件
- 格式规范：SKILL.md 前言区字段完整，正文不超过 500 行
- 脚本质量：参数清晰、错误处理完善、可执行性强
- 文档完整：references/ 提供完整格式定义和示例

### 效率优化
- 批量操作：创建多个技能时使用 batch_create.py
- 模板复用：优先使用 assets/skill-templates/ 中的模板
- 并行执行：多个文件创建、编辑操作并行执行
- 渐进式展示：先展示核心流程，细节放入 references/

## 使用示例

### 示例 1：基于官方文档创建技能
- 功能说明：用户提供官方文档，自动生成技能包
- 执行方式：智能体主导 + 脚本辅助
- 关键步骤：
  1. 读取官方文档
  2. 提取 API 和配置信息
  3. 设计 SKILL.md 结构
  4. 生成必要的 scripts
  5. 使用 skill_validator.py 验证

### 示例 2：批量创建相关技能
- 功能说明：一次创建多个相关联的技能包
- 执行方式：脚本主导
- 关键步骤：
  1. 编写配置文件（JSON 格式）
  2. 调用 batch_create.py 批量生成
  3. 使用 dependency_analyzer.py 分析依赖
  4. 按依赖顺序逐个完善

### 示例 3：查找最佳实践并生成技能
- 功能说明：搜索最佳实践方案，生成符合规范的技能
- 执行方式：智能体主导 + 脚本辅助
- 关键步骤：
  1. 网络搜索最佳实践
  2. 参考 best-practices.md 选择方案
  3. 查询 frameworks-guide.md 了解框架
  4. 使用模板快速生成 SKILL.md
  5. 完善脚本和参考文档

## 框架使用规范速查

### Web 框架
- FastAPI：适用于高性能 API，异步支持好
- Flask：适用于轻量级 Web 应用，生态丰富
- Django：适用于全栈应用，包含 ORM 和管理后台

### 数据处理
- Pandas：数据处理和分析
- NumPy：数值计算
- PyTorch/TensorFlow：深度学习

### 工具库
- Requests：HTTP 请求
- PyYAML：YAML 配置处理
- NetworkX：图结构分析

详细使用方法见 [references/frameworks-guide.md](references/frameworks-guide.md)
