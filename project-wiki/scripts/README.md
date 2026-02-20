# ProjectWiki 脚本目录

## 目录结构

```
scripts/
├── analysis/         # 分析类脚本
├── knowledge/        # 知识类脚本
├── generation/       # 生成类脚本
├── query/            # 查询类脚本
├── structure/        # 结构类脚本
└── utils/            # 工具类脚本
```

## 脚本分类

### analysis/ - 分析类脚本

| 脚本 | 功能 | 输出 |
|------|------|------|
| `analyze_project.py` | 项目分析，识别项目类型、技术栈和结构 | project-analysis.json |
| `complexity_analyzer.py` | 复杂度分析，评估项目复杂度 | complexity-report.json |
| `extract_docs.py` | 从代码中提取文档和注释 | extracted-docs/ |
| `structure_optimizer.py` | 结构优化，优化项目目录结构 | optimized-structure.json |

### knowledge/ - 知识类脚本

| 脚本 | 功能 | 输出 |
|------|------|------|
| `knowledge_graph.py` | 构建知识图谱，展示模块依赖关系 | knowledge-graph.json/.mmd |
| `knowledge_extractor.py` | 隐性知识提取，从代码中提取业务逻辑 | extracted-knowledge/ |
| `knowledge_manager.py` | 知识管理器，管理知识索引和统计 | .knowledge-index.json |
| `search_knowledge.py` | 知识搜索，搜索技术栈知识 | wiki/references/[tech]-knowledge.md |

### generation/ - 生成类脚本

| 脚本 | 功能 | 输出 |
|------|------|------|
| `create_wiki_structure.py` | 创建 Wiki 目录结构 | wiki/ |
| `generate_doc.py` | 智能文档生成，支持渐进式文档 | wiki/docs/ |
| `generate_changelog.py` | 生成变更日志 | CHANGELOG.md |
| `generate_cicd.py` | 生成 CI/CD 配置 | .github/workflows/ |
| `generate_roadmap.py` | 生成项目路线图 | ROADMAP.md |

### query/ - 查询类脚本

| 脚本 | 功能 | 输出 |
|------|------|------|
| `query_knowledge.py` | 知识查询，查询文档规范和最佳实践 | 查询结果 |
| `role_view.py` | 角色视图查询，按角色查询文档 | 角色视图 |
| `multi_hop_qa.py` | 多跳问答，支持复杂问题推理 | 答案 |

### structure/ - 结构类脚本

| 脚本 | 功能 | 输出 |
|------|------|------|
| `adaptive_structure.py` | 自适应结构，根据复杂度生成结构 | 结构配置 |
| `context_aware.py` | 上下文感知，结合项目上下文提供建议 | 建议列表 |

### utils/ - 工具类脚本

| 脚本 | 功能 | 输出 |
|------|------|------|
| `consistency_checker.py` | 一致性检查，检查文档一致性 | 检查报告 |

## 使用示例

### 分析项目

```bash
python3 scripts/analysis/analyze_project.py --path ./your-project
```

### 生成文档

```bash
python3 scripts/generation/generate_doc.py --type api --name "用户登录接口"
```

### 查询知识

```bash
python3 scripts/query/query_knowledge.py --query "如何编写 API 文档？"
```

### 搜索技术栈

```bash
python3 scripts/knowledge/search_knowledge.py Redis --type library
```

### 管理知识库

```bash
python3 scripts/knowledge/knowledge_manager.py list
python3 scripts/knowledge/knowledge_manager.py get Redis
python3 scripts/knowledge/knowledge_manager.py stats
```

## 依赖关系

```
analyze_project.py → knowledge_graph.py → create_wiki_structure.py
generate_doc.py → search_knowledge.py → knowledge_manager.py
query_knowledge.py → knowledge_graph.py
role_view.py → generate_doc.py
```
