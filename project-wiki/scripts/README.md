# 脚本工具索引

## 目录

- [核心脚本](#核心脚本)
- [文档生成脚本](#文档生成脚本)
- [使用示例](#使用示例)

---

## 核心脚本

### 1. analyze_project.py

**功能**：分析项目结构，提取项目信息

**用法**：
```bash
python3 scripts/analyze_project.py --path ./your-project
```

**输出**：
- `project-analysis.json` - 项目分析结果

**包含信息**：
- 项目结构
- 框架识别
- 技术栈
- 依赖分析
- 模块关系

---

### 2. knowledge_graph.py

**功能**：构建知识图谱，可视化模块关系

**用法**：
```bash
python3 scripts/knowledge_graph.py --path ./your-project --format mermaid
```

**输出**：
- `knowledge-graph.json` - JSON 格式图谱
- `knowledge-graph.mmd` - Mermaid 格式图谱

**支持格式**：
- `mermaid` - Mermaid 格式
- `json` - JSON 格式
- `graphviz` - Graphviz 格式

---

### 3. knowledge_extractor.py

**功能**：提取隐性知识（设计决策、最佳实践）

**用法**：
```bash
python3 scripts/knowledge_extractor.py --path ./your-project --language python
```

**输出**：
- `implicit-knowledge.json` - 隐性知识

**支持语言**：
- `python`
- `javascript`
- `java`
- `go`
- `typescript`

---

### 4. evaluate_complexity.py

**功能**：评估项目复杂度

**用法**：
```bash
python3 scripts/evaluate_complexity.py --path ./your-project
```

**输出**：
- `complexity-report.json` - 复杂度报告

**评估维度**：
- 代码行数
- 循环复杂度
- 耦合度
- 内聚度
- 依赖复杂度

---

### 5. create_wiki_structure.py

**功能**：创建 Wiki 目录结构

**用法**：
```bash
python3 scripts/create_wiki_structure.py --path ./your-project
```

**输出**：
- `wiki/` - Wiki 目录结构

**目录结构**：
```
wiki/
├── 01-架构文档/
├── 02-开发指南/
├── 03-API文档/
├── 04-模块文档/
├── 05-测试文档/
└── 06-参考文档/
```

---

### 6. generate_doc.py

**功能**：智能文档生成

**用法**：
```bash
# 生成 API 文档
python3 scripts/generate_doc.py --type api --name "用户登录接口" --output wiki/03-API文档/用户登录接口.md

# 生成模块文档
python3 scripts/generate_doc.py --type module --name "认证模块" --output wiki/04-模块文档/认证模块/模块介绍.md

# 生成服务文档
python3 scripts/generate_doc.py --type service --name "用户服务" --output wiki/04-模块文档/用户服务/服务文档.md
```

**支持类型**：
- `api` - API 文档
- `module` - 模块文档
- `service` - 服务文档
- `design` - 设计文档

---

### 7. query_knowledge.py

**功能**：知识查询

**用法**：
```bash
# 交互式查询
python3 scripts/query_knowledge.py

# 单次查询
python3 scripts/query_knowledge.py --query "如何编写 API 文档？"

# 列出所有知识
python3 scripts/query_knowledge.py --list
```

**查询能力**：
- 文档规范查询
- 模板查询
- 框架指引查询
- 角色视图查询

---

### 8. role_view.py

**功能**：角色视图查询

**用法**：
```bash
# 列出所有角色
python3 scripts/role_view.py list-roles

# 查看特定角色的文档
python3 scripts/role_view.py docs --role architect

# 生成角色专属文档
python3 scripts/role_view.py generate --role architect --type architecture --name "用户系统"

# 查看角色映射
python3 scripts/role_view.py mapping
```

**支持角色**：
- `architect` - 架构师
- `developer` - 开发工程师
- `tester` - 测试工程师
- `ops` - 运维/SRE
- `product` - 产品经理

**支持类型**：
- 架构师：`architecture`、`adr`
- 开发工程师：`module`、`api`
- 测试工程师：`test-plan`
- 运维/SRE：`ops-runbook`
- 产品经理：`user-flow`

---

## 文档生成脚本

### 1. generate_changelog.py

**功能**：生成 CHANGELOG

**用法**：
```bash
# 初始化 CHANGELOG
python3 scripts/generate_changelog.py init

# 添加新版本
python3 scripts/generate_changelog.py add --version "1.0.0" --date "2024-02-19"

# 添加变更内容
python3 scripts/generate_changelog.py add --version "1.0.0" --type "Added" --content "添加用户注册功能"
```

**输出**：
- `CHANGELOG.md` - 变更日志

---

### 2. generate_roadmap.py

**功能**：生成 ROADMAP

**用法**：
```bash
python3 scripts/generate_roadmap.py --path ./your-project
```

**输出**：
- `ROADMAP.md` - 路线图

**包含内容**：
- 已完成功能
- 进行中功能
- 计划中功能
- 未来规划

---

### 3. generate_cicd.py

**功能**：生成 CI/CD 配置

**用法**：
```bash
# GitHub Actions
python3 scripts/generate_cicd.py --type github-actions

# GitLab CI
python3 scripts/generate_cicd.py --type gitlab-ci

# Jenkins Pipeline
python3 scripts/generate_cicd.py --type jenkins
```

**输出**：
- `.github/workflows/ci.yml` - GitHub Actions 配置
- `.gitlab-ci.yml` - GitLab CI 配置
- `Jenkinsfile` - Jenkins Pipeline 配置

---

## 使用示例

### 示例 1：完整的项目分析流程

```bash
# 1. 分析项目
python3 scripts/analyze_project.py --path ./your-project

# 2. 构建知识图谱
python3 scripts/knowledge_graph.py --path ./your-project --format mermaid

# 3. 提取隐性知识
python3 scripts/knowledge_extractor.py --path ./your-project --language python

# 4. 评估复杂度
python3 scripts/evaluate_complexity.py --path ./your-project

# 5. 创建 Wiki 结构
python3 scripts/create_wiki_structure.py --path ./your-project
```

---

### 示例 2：生成文档

```bash
# 1. 生成 API 文档
python3 scripts/generate_doc.py --type api --name "用户登录接口"

# 2. 生成模块设计文档
python3 scripts/generate_doc.py --type module --name "认证模块"

# 3. 生成服务文档
python3 scripts/generate_doc.py --type service --name "用户服务"

# 4. 生成设计文档
python3 scripts/generate_doc.py --type design --name "手机号注册功能"
```

---

### 示例 3：角色视图使用

```bash
# 1. 列出所有角色
python3 scripts/role_view.py list-roles

# 2. 生成架构师文档
python3 scripts/role_view.py generate --role architect --type architecture --name "用户系统"

# 3. 生成开发者文档
python3 scripts/role_view.py generate --role developer --type module --name "认证模块"

# 4. 生成测试计划
python3 scripts/role_view.py generate --role tester --type test-plan --name "用户注册功能"

# 5. 生成运维手册
python3 scripts/role_view.py generate --role ops --type ops-runbook --name "生产环境"

# 6. 生成用户旅程图
python3 scripts/role_view.py generate --role product --type user-flow --name "用户注册流程"
```

---

### 示例 4：知识查询

```bash
# 1. 查询 API 文档规范
python3 scripts/query_knowledge.py --query "如何编写 API 文档？"

# 2. 查询设计文档规范
python3 scripts/query_knowledge.py --query "如何编写设计文档？"

# 3. 查询架构师指南
python3 scripts/query_knowledge.py --query "架构师需要关注什么？"

# 4. 列出所有知识
python3 scripts/query_knowledge.py --list
```

---

### 示例 5：生成项目文档

```bash
# 1. 初始化 CHANGELOG
python3 scripts/generate_changelog.py init

# 2. 生成 ROADMAP
python3 scripts/generate_roadmap.py --path ./your-project

# 3. 生成 CI/CD 配置
python3 scripts/generate_cicd.py --type github-actions

# 4. 生成 README
python3 scripts/generate_doc.py --type readme --name "README"
```

---

## 脚本对比

| 脚本 | 用途 | 输入 | 输出 | 适用场景 |
|------|------|------|------|----------|
| analyze_project.py | 项目分析 | 项目路径 | JSON | 项目初始化 |
| knowledge_graph.py | 知识图谱 | 项目路径 | JSON/MD | 可视化关系 |
| knowledge_extractor.py | 隐性知识 | 项目路径 | JSON | 知识挖掘 |
| evaluate_complexity.py | 复杂度评估 | 项目路径 | JSON | 代码审查 |
| create_wiki_structure.py | Wiki 结构 | 项目路径 | 目录 | 文档初始化 |
| generate_doc.py | 文档生成 | 文档类型 | MD | 文档创建 |
| query_knowledge.py | 知识查询 | 查询文本 | 文本 | 知识检索 |
| role_view.py | 角色视图 | 角色/类型 | MD | 角色文档 |
| generate_changelog.py | CHANGELOG | 版本/内容 | MD | 版本管理 |
| generate_roadmap.py | ROADMAP | 项目路径 | MD | 规划管理 |
| generate_cicd.py | CI/CD | CI/CD 类型 | 配置文件 | 自动化 |

---

## 最佳实践

### 1. 项目初始化

```bash
# 分析项目
python3 scripts/analyze_project.py --path ./your-project

# 创建 Wiki 结构
python3 scripts/create_wiki_structure.py --path ./your-project

# 生成基础文档
python3 scripts/generate_changelog.py init
python3 scripts/generate_roadmap.py --path ./your-project
python3 scripts/generate_cicd.py --type github-actions
```

---

### 2. 文档生成

```bash
# 根据角色生成文档
python3 scripts/role_view.py generate --role architect --type architecture --name "用户系统"
python3 scripts/role_view.py generate --role developer --type module --name "认证模块"
python3 scripts/role_view.py generate --role tester --type test-plan --name "用户注册功能"
```

---

### 3. 知识查询

```bash
# 交互式查询
python3 scripts/query_knowledge.py

# 单次查询
python3 scripts/query_knowledge.py --query "如何编写 API 文档？"
```

---

**最后更新**：2024-02-19
