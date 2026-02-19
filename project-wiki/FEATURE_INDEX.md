# ProjectWiki 功能索引

## 目录

- [核心能力](#核心能力)
- [文档体系](#文档体系)
- [脚本工具](#脚本工具)
- [角色视图](#角色视图)
- [框架支持](#框架支持)
- [快速开始](#快速开始)

---

## 核心能力

### 1. 智能问答 🧠

**功能描述**：支持自然语言查询，结合上下文提供精准答案

**能力**：
- 自然语言查询：询问文档规范、结构、示例
- 上下文感知：结合项目信息提供精准答案
- 意图识别：自动识别用户意图并路由到相应处理
- **多跳推理**：串联多个文档回答复杂问题

**使用方式**：
```bash
# 基础查询
python3 scripts/query_knowledge.py --query "如何编写 API 文档？"

# 上下文感知查询
python3 scripts/context_aware.py --path ./your-project --query "如何设计 API？" --role architect

# 多跳复杂查询
python3 scripts/multi_hop_qa.py --path ./your-project --query "如何设计用户系统？然后如何实现？最后如何测试？"
```

**相关文档**：
- [core/agent-guide.md](references/core/agent-guide.md) - Agent 交互指南
- [core/intent-rules.md](references/core/intent-rules.md) - 意图识别规则

---

### 2. 自动文档生成 📚

**功能描述**：基于预定义模板生成合规文档

**能力**：
- 基于模板：使用预定义模板生成合规文档
- 代码上下文：从代码中提取信息填充文档
- 多类型支持：API 文档、模块文档、服务文档、设计文档

**支持类型**：
- API 文档（api-template.md）
- 模块文档（module-template.md）
- 服务文档（service-template.md）
- 设计文档（design-doc-template.md）
- 架构设计文档（architecture-template.md）
- ADR（adr-template.md）
- 模块设计文档（module-design-template.md）
- 测试计划（test-plan-template.md）
- 运维手册（ops-runbook-template.md）
- 用户旅程图（user-flow-template.md）

**使用方式**：
```bash
python3 scripts/generate_doc.py --type api --name "用户登录接口"
```

**相关文档**：
- [templates/](references/templates/) - 文档模板目录

---

### 3. 知识图谱 🔗

**功能描述**：可视化模块/API/配置的关系网络

**能力**：
- 模块关系：可视化模块/API/配置的关系网络
- 隐性知识挖掘：提取设计决策和最佳实践
- Mermaid 可视化：自动生成流程图、架构图、ER 图、时序图

**使用方式**：
```bash
python3 scripts/knowledge_graph.py --path ./your-project --format mermaid
```

**相关文档**：
- [visualization/mermaid-syntax.md](references/visualization/mermaid-syntax.md) - Mermaid 语法指南

---

### 4. 文档管理 📋

**功能描述**：自动识别项目所需的文档类型

**能力**：
- 自动识别：识别项目所需的文档类型
- 版本控制：支持 CHANGELOG 和 ROADMAP
- CI/CD 集成：生成 CI/CD 配置和文档

**使用方式**：
```bash
# 生成 CHANGELOG
python3 scripts/generate_changelog.py init

# 生成 ROADMAP
python3 scripts/generate_roadmap.py --path ./your-project

# 生成 CI/CD
python3 scripts/generate_cicd.py --type github-actions
```

**相关文档**：
- [document-guides/changelog-guide.md](references/document-guides/changelog-guide.md)
- [document-guides/roadmap-guide.md](references/document-guides/roadmap-guide.md)
- [document-guides/cicd-guide.md](references/document-guides/cicd-guide.md)

---

### 5. 角色视图 👥

**功能描述**：为 5 种角色提供专门的文档和模板

**角色**：
- 架构师（Architect）：架构设计、技术决策（ADR）、非功能性需求
- 开发工程师（Developer）：模块设计、API 契约、数据结构
- 测试工程师（Tester）：测试计划、边界条件、异常场景
- 运维/SRE（Ops）：部署架构、资源清单、监控告警
- 产品经理（Product）：用户旅程、业务规则、用户体验

**使用方式**：
```bash
# 列出所有角色
python3 scripts/role_view.py list-roles

# 查看角色文档
python3 scripts/role_view.py docs --role architect

# 生成角色专属文档
python3 scripts/role_view.py generate --role architect --type architecture --name "用户系统"
```

**相关文档**：
- [roles/README.md](references/roles/README.md) - 角色视图总览
- [roles/role-mapping.md](references/roles/role-mapping.md) - 角色与文档映射

---

### 6. 自适应结构管理 🏗️

**功能描述**：根据项目复杂度自动识别并生成合理的层级结构

**能力**：
- **复杂度分析**：自主识别项目规模和复杂度（4 个等级）
- **结构推荐**：根据复杂度推荐最合适的目录结构类型
- **自适应生成**：自动生成符合项目特征的目录结构
- **结构优化**：分析现有结构，提供优化建议和改进方案

**复杂度等级**：
- `simple` - 简单项目（≤5 模块，≤20 文件，≤5000 行）
- `medium` - 中等项目（≤20 模块，≤100 文件，≤20000 行）
- `complex` - 复杂项目（≤50 模块，≤500 文件，≤100000 行）
- `ultra-complex` - 超复杂项目（>50 模块，>500 文件，>100000 行）

**支持结构类型**：
- `flat` - 扁平结构（简单项目）
- `typed` - 按类型分组（中等项目）
- `domain` - 按领域分组（复杂项目）
- `layered` - 分层结构（多层架构）
- `microservice` - 微服务结构（微服务架构）
- `nested` - 多层嵌套（超复杂项目）

**使用方式**：
```bash
# 分析项目复杂度
python3 scripts/complexity_analyzer.py --path ./your-project --output complexity-report.json

# 生成自适应结构
python3 scripts/adaptive_structure.py --path ./your-project

# 优化现有结构
python3 scripts/structure_optimizer.py --path ./your-project --recommended domain --output optimization-report.json
```

**相关文档**：
- [scripts/complexity_analyzer.py](scripts/complexity_analyzer.py) - 复杂度分析器
- [scripts/adaptive_structure.py](scripts/adaptive_structure.py) - 自适应结构生成器
- [scripts/structure_optimizer.py](scripts/structure_optimizer.py) - 结构优化器

---

### 7. 上下文感知增强 🎯

**功能描述**：自动注入环境上下文，使回答更精准

**能力**：
- **环境上下文**：收集项目路径、当前文件、Git 分支等环境信息
- **角色上下文**：根据用户角色推荐相关的知识和资源
- **查询增强**：自动增强用户查询，补充上下文信息
- **置信度评分**：计算回答的置信度，辅助决策

**上下文信息**：
- 项目路径
- 当前文件/函数/类
- Git 分支和提交
- 环境（开发/Docker/CI/CD）
- 用户角色

**使用方式**：
```bash
# 基本查询
python3 scripts/context_aware.py --path ./your-project --query "如何设计 API？"

# 指定当前文件
python3 scripts/context_aware.py --path ./your-project --query "这个函数的作用？" --file src/services/user.py

# 指定用户角色
python3 scripts/context_aware.py --path ./your-project --query "如何部署服务？" --role ops
```

**相关文档**：
- [scripts/context_aware.py](scripts/context_aware.py) - 上下文感知增强器

---

### 8. 一致性检查 ✅

**功能描述**：检查文档与代码的一致性，防止脱节

**能力**：
- **API 一致性**：检查文档中定义的 API 在代码中是否存在
- **模块一致性**：检查文档中提到的模块在代码中是否存在
- **模型一致性**：检查文档中定义的数据模型和字段与代码是否一致
- **文档时效性**：检查文档是否过期（代码已更新但文档未更新）
- **链接有效性**：检查文档中的链接是否有效

**问题类型**：
- `api_not_implemented` - API 未实现
- `module_not_found` - 模块未找到
- `model_not_found` - 模型未找到
- `field_missing_in_code` - 字段在代码中缺失
- `field_missing_in_doc` - 字段在文档中缺失
- `document_outdated` - 文档过期
- `broken_link` - 链接失效

**使用方式**：
```bash
python3 scripts/consistency_checker.py --path ./your-project --output consistency-report.json
```

**相关文档**：
- [scripts/consistency_checker.py](scripts/consistency_checker.py) - 一致性检查器

---

### 9. 多跳问答引擎 🔍

**功能描述**：串联多个文档回答复杂问题

**能力**：
- **查询分解**：将复杂查询分解为多个子查询
- **知识图谱构建**：自动构建文档知识图谱
- **多步推理**：串联多个文档回答问题
- **执行路径追踪**：记录查询执行路径

**查询分解策略**：
- 连接词分解（然后、之后、接着）
- 关键词分解
- 问题类型分解（如何、为什么、什么）

**使用方式**：
```bash
python3 scripts/multi_hop_qa.py --path ./your-project --query "如何设计并实现用户认证系统？然后如何测试？" --output qa-result.json
```

**相关文档**：
- [scripts/multi_hop_qa.py](scripts/multi_hop_qa.py) - 多跳问答引擎

---

## 文档体系

### 核心指南（core/）

| 文档 | 说明 |
|------|------|
| [agent-guide.md](references/core/agent-guide.md) | Agent 交互指南 |
| [intent-rules.md](references/core/intent-rules.md) | 意图识别规则 |
| [wiki-structure-guide.md](references/core/wiki-structure-guide.md) | Wiki 结构指南 |
| [knowledge-base-guide.md](references/core/knowledge-base-guide.md) | 知识库指南 |
| [knowledge-structure.md](references/core/knowledge-structure.md) | 知识结构说明 |

---

### 文档规范（document-guides/）

| 文档 | 说明 |
|------|------|
| [api-doc-guide.md](references/document-guides/api-doc-guide.md) | API 文档指南（重点：数据流动、数据模型） |
| [architecture-guide.md](references/document-guides/architecture-guide.md) | 架构文档指南 |
| [design-doc-guide.md](references/document-guides/design-doc-guide.md) | 设计文档指南（重点：ER 图、时序图） |
| [changelog-guide.md](references/document-guides/changelog-guide.md) | CHANGELOG 指南 |
| [roadmap-guide.md](references/document-guides/roadmap-guide.md) | ROADMAP 指南 |
| [cicd-guide.md](references/document-guides/cicd-guide.md) | CI/CD 指南 |
| [readme-template.md](references/document-guides/readme-template.md) | README 模板 |

---

### 角色视图（roles/）

| 角色 | 指南 | 模板 |
|------|------|------|
| 架构师 | [architect-guide.md](references/roles/architect/architect-guide.md) | [architecture-template.md](references/roles/architect/architecture-template.md), [adr-template.md](references/roles/architect/adr-template.md) |
| 开发工程师 | [developer-guide.md](references/roles/developer/developer-guide.md) | [module-design-template.md](references/roles/developer/module-design-template.md) |
| 测试工程师 | [tester-guide.md](references/roles/tester/tester-guide.md) | [test-plan-template.md](references/roles/tester/test-plan-template.md) |
| 运维/SRE | [ops-guide.md](references/roles/ops/ops-guide.md) | [ops-runbook-template.md](references/roles/ops/ops-runbook-template.md) |
| 产品经理 | [product-guide.md](references/roles/product/product-guide.md) | [user-flow-template.md](references/roles/product/user-flow-template.md) |

---

### 可视化（visualization/）

| 文档 | 说明 |
|------|------|
| [mermaid-syntax.md](references/visualization/mermaid-syntax.md) | Mermaid 语法指南 |

---

### 框架指引（frameworks/）

| 框架 | 说明 |
|------|------|
| [django-guide.md](references/frameworks/django-guide.md) | Django 框架指引 |
| [flask-guide.md](references/frameworks/flask-guide.md) | Flask 框架指引 |
| [fastapi-guide.md](references/frameworks/fastapi-guide.md) | FastAPI 框架指引 |
| [spring-boot-guide.md](references/frameworks/spring-boot-guide.md) | Spring Boot 框架指引 |
| [gin-guide.md](references/frameworks/gin-guide.md) | Gin 框架指引 |
| [react-guide.md](references/frameworks/react-guide.md) | React 框架指引 |

---

## 脚本工具

### 核心脚本

| 脚本 | 功能 |
|------|------|
| [analyze_project.py](scripts/analyze_project.py) | 分析项目结构，提取项目信息 |
| [knowledge_graph.py](scripts/knowledge_graph.py) | 构建知识图谱，可视化模块关系 |
| [knowledge_extractor.py](scripts/knowledge_extractor.py) | 提取隐性知识（设计决策、最佳实践） |
| [evaluate_complexity.py](scripts/evaluate_complexity.py) | 评估项目复杂度 |
| [create_wiki_structure.py](scripts/create_wiki_structure.py) | 创建 Wiki 目录结构 |

---

### 文档生成脚本

| 脚本 | 功能 |
|------|------|
| [generate_doc.py](scripts/generate_doc.py) | 智能文档生成 |
| [query_knowledge.py](scripts/query_knowledge.py) | 知识查询 |
| [role_view.py](scripts/role_view.py) | 角色视图查询 |

---

### 智能工具（新增）

| 脚本 | 功能 | 复杂度支持 |
|------|------|-----------|
| [complexity_analyzer.py](scripts/complexity_analyzer.py) | 项目复杂度分析器 | ✅ 4 个等级 |
| [adaptive_structure.py](scripts/adaptive_structure.py) | 自适应结构生成器 | ✅ 6 种类型 |
| [structure_optimizer.py](scripts/structure_optimizer.py) | 结构优化器 | ✅ 结构评分 |
| [context_aware.py](scripts/context_aware.py) | 上下文感知增强器 | ✅ 环境上下文 |
| [multi_hop_qa.py](scripts/multi_hop_qa.py) | 多跳问答引擎 | ✅ 多步推理 |
| [consistency_checker.py](scripts/consistency_checker.py) | 一致性检查器 | ✅ 7 种检查 |

**详细文档**：[scripts/README.md](scripts/README.md)

---

## 角色视图

### 支持的角色

| 角色 | 关键文档 | 核心关注点 |
|------|---------|-----------|
| 架构师 | 架构设计文档、ADR、技术选型文档 | 系统架构、技术决策、非功能性需求 |
| 开发工程师 | 模块文档、API 文档、代码规范 | 功能实现、接口定义、代码质量 |
| 测试工程师 | 测试计划、测试用例、测试报告 | 功能验证、边界条件、异常场景 |
| 运维/SRE | 运维手册、部署指南、监控配置 | 部署运维、监控告警、故障处理 |
| 产品经理 | 用户旅程图、业务规则文档、产品需求 | 用户体验、业务流程、功能规划 |

---

## 框架支持

### 后端框架

- **Python**: Django, Flask, FastAPI
- **Java**: Spring Boot
- **Go**: Gin
- **JavaScript/TypeScript**: Express, NestJS

### 前端框架

- **React**: react-guide.md
- **Vue**: vue-guide.md
- **Angular**: angular-guide.md

---

## 快速开始

### 场景 1：分析并生成文档

```bash
# 1. 分析项目复杂度
python3 scripts/complexity_analyzer.py --path ./your-project

# 2. 生成自适应结构
python3 scripts/adaptive_structure.py --path ./your-project

# 3. 生成 API 文档
python3 scripts/generate_doc.py --type api --name "用户登录" --output wiki/03-API文档/用户登录.md

# 4. 检查一致性
python3 scripts/consistency_checker.py --path ./your-project
```

### 场景 2：智能问答

```bash
# 上下文感知查询
python3 scripts/context_aware.py --path ./your-project --query "如何设计 API？" --role architect

# 多跳复杂查询
python3 scripts/multi_hop_qa.py --path ./your-project --query "如何设计用户系统？然后如何实现？最后如何测试？"
```

### 场景 3：角色视图

```bash
# 列出所有角色
python3 scripts/role_view.py list-roles

# 查看架构师文档
python3 scripts/role_view.py docs --role architect

# 生成架构师专属文档
python3 scripts/role_view.py generate --role architect --type architecture --name "用户系统架构"
```

---

## 功能亮点

✨ **智能化升级**
- 从静态文档管理升级为动态智能交互系统
- 支持自然语言问答和意图识别
- 上下文感知，提供精准答案

✨ **数据流动与模型**
- API 文档中强制要求使用 Mermaid 时序图展示数据流转
- 完整的数据模型定义（表格/类图/Schema 三种形式）
- 规范的类型系统（基础类型/复杂类型/类型组合）

✨ **自适应结构**
- 根据项目复杂度自动识别并生成合理的层级结构
- 支持 4 个复杂度等级和 6 种结构类型
- 智能推荐最优结构

✨ **角色视图**
- 为 5 种角色提供专门的文档和模板
- 支持角色视图查询和文档生成
- 根据角色推荐相关知识

✨ **一致性保障**
- 自动检查文档与代码的一致性
- 检测文档时效性
- 防止文档与代码脱节

---

## 更多信息

- [SKILL.md](SKILL.md) - ProjectWiki 主文档
- [scripts/README.md](scripts/README.md) - 脚本工具详细说明
- [FEATURE_INDEX.md](FEATURE_INDEX.md) - 功能索引（本文档）
