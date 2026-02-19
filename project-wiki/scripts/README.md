# 脚本工具索引

## 目录

- [核心脚本](#核心脚本)
- [智能工具](#智能工具)
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

## 智能工具

### 9. complexity_analyzer.py

**功能**：项目复杂度分析器 - 自主识别项目结构的复杂度

**用法**：
```bash
python3 scripts/complexity_analyzer.py --path ./your-project --output complexity-report.json
```

**输出**：
- `complexity-report.json` - 复杂度分析报告

**分析维度**：
- **基础指标**：文件数量、代码行数、模块数量
- **依赖指标**：依赖数量、循环依赖、依赖深度
- **技术栈指标**：语言数量、框架数量
- **架构指标**：分层数量、服务数量、API 数量
- **代码质量指标**：平均文件行数、最大文件行数

**复杂度等级**：
- `simple` - 简单项目（≤5 模块，≤20 文件，≤5000 行）
- `medium` - 中等项目（≤20 模块，≤100 文件，≤20000 行）
- `complex` - 复杂项目（≤50 模块，≤500 文件，≤100000 行）
- `ultra-complex` - 超复杂项目（>50 模块，>500 文件，>100000 行）

**功能特点**：
- 自主识别项目规模和复杂度
- 推荐合适的目录结构类型
- 提供优化建议
- 计算综合复杂度分数（0-100）

---

### 10. adaptive_structure.py

**功能**：自适应结构生成器 - 根据项目复杂度自动生成合适的目录结构

**用法**：
```bash
# 根据复杂度自动生成结构
python3 scripts/adaptive_structure.py --path ./your-project

# 指定结构类型
python3 scripts/adaptive_structure.py --path ./your-project --structure-type domain

# 指定复杂度等级
python3 scripts/adaptive_structure.py --path ./your-project --complexity complex

# 指定输出路径
python3 scripts/adaptive_structure.py --path ./your-project --output wiki

# 导出配置文件
python3 scripts/adaptive_structure.py --path ./your-project --export structure-config.json
```

**输出**：
- `wiki/` - 自动生成的目录结构
- `structure-config.json` - 结构配置文件（可选）

**支持结构类型**：
- `flat` - 扁平结构（简单项目）
- `typed` - 按类型分组（中等项目）
- `domain` - 按领域分组（复杂项目）
- `layered` - 分层结构（多层架构）
- `microservice` - 微服务结构（微服务架构）
- `nested` - 多层嵌套（超复杂项目）

**功能特点**：
- 根据项目复杂度自动选择最合适的结构类型
- 自动识别业务领域和服务
- 支持多种结构类型和嵌套规则
- 生成目录索引文件

---

### 11. structure_optimizer.py

**功能**：结构优化器 - 分析和优化现有项目结构

**用法**：
```bash
python3 scripts/structure_optimizer.py --path ./your-project --recommended domain --output optimization-report.json
```

**输出**：
- `optimization-report.json` - 优化报告

**检测问题**：
- Wiki 目录缺失
- 目录嵌套过深
- 缺少索引文件（README.md/index.md）
- 空目录检测
- 命名不一致
- 文档完整性检查

**优化建议**：
- 结构重组
- 目录扁平化
- 添加索引文件
- 添加搜索功能
- 改进导航

**功能特点**：
- 分析当前结构类型
- 检测结构问题
- 提供优化建议
- 计算结构得分（0-100）

---

### 12. context_aware.py

**功能**：上下文感知增强器 - 自动注入环境上下文，使回答更精准

**用法**：
```bash
# 基本查询
python3 scripts/context_aware.py --path ./your-project --query "如何设计 API？"

# 指定当前文件
python3 scripts/context_aware.py --path ./your-project --query "这个函数的作用？" --file src/services/user.py

# 指定用户角色
python3 scripts/context_aware.py --path ./your-project --query "如何部署服务？" --role ops

# 组合使用
python3 scripts/context_aware.py --path ./your-project --query "如何测试这个类？" --file src/models/user.py --role tester --output context-result.json
```

**输出**：
- 增强查询
- 上下文信息
- 建议知识列表
- 建议资源列表
- 置信度评分

**上下文信息**：
- 项目路径
- 当前文件
- 当前函数/类
- Git 分支/提交
- 环境（开发/Docker/CI/CD）
- 用户角色

**功能特点**：
- 自动收集环境上下文
- 增强用户查询
- 推荐相关知识和资源
- 计算回答置信度

---

### 13. multi_hop_qa.py

**功能**：多跳问答引擎 - 串联多个文档回答复杂问题

**用法**：
```bash
python3 scripts/multi_hop_qa.py --path ./your-project --query "如何设计并实现用户认证系统？然后如何测试？" --output qa-result.json
```

**输出**：
- `qa-result.json` - 问答结果

**核心能力**：
- **查询分解**：将复杂查询分解为多个子查询
- **知识图谱构建**：自动构建文档知识图谱
- **多步推理**：串联多个文档回答问题
- **执行路径追踪**：记录查询执行路径

**查询分解策略**：
- 连接词分解（然后、之后、接着）
- 关键词分解
- 问题类型分解（如何、为什么、什么）

**功能特点**：
- 支持复杂问题的多跳查询
- 自动构建知识图谱
- 提取文档元数据和链接关系
- 计算总体置信度

---

### 14. consistency_checker.py

**功能**：一致性检查器 - 检查文档与代码的一致性，防止脱节

**用法**：
```bash
python3 scripts/consistency_checker.py --path ./your-project --output consistency-report.json
```

**输出**：
- `consistency-report.json` - 一致性报告

**检查项**：
- **API 文档一致性**：文档中定义的 API 在代码中是否存在
- **模块文档一致性**：文档中提到的模块在代码中是否存在
- **数据模型一致性**：文档中定义的模型和字段与代码是否一致
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

**功能特点**：
- 全面检查文档与代码的一致性
- 支持多种编程语言
- 检测文档时效性
- 计算一致性得分（0-100）

---

## 文档生成脚本

### generate_doc.py

详见[核心脚本 - 6. generate_doc.py](#6-generate_docpy)

---

## 使用示例

### 示例 1：完整的项目文档工作流

```bash
# 1. 分析项目复杂度
python3 scripts/complexity_analyzer.py --path ./your-project --output complexity-report.json

# 2. 根据复杂度生成自适应结构
python3 scripts/adaptive_structure.py --path ./your-project

# 3. 生成 API 文档
python3 scripts/generate_doc.py --type api --name "用户登录" --output wiki/03-API文档/用户登录.md

# 4. 生成模块文档
python3 scripts/generate_doc.py --type module --name "认证模块" --output wiki/04-模块文档/认证模块/模块介绍.md

# 5. 检查一致性
python3 scripts/consistency_checker.py --path ./your-project --output consistency-report.json
```

### 示例 2：智能问答工作流

```bash
# 1. 上下文感知查询
python3 scripts/context_aware.py --path ./your-project --query "如何设计 API？" --role architect

# 2. 多跳复杂查询
python3 scripts/multi_hop_qa.py --path ./your-project --query "如何设计用户系统？然后如何实现？最后如何测试？"

# 3. 知识查询
python3 scripts/query_knowledge.py --query "API 文档规范"
```

### 示例 3：角色视图工作流

```bash
# 1. 列出所有角色
python3 scripts/role_view.py list-roles

# 2. 查看架构师文档
python3 scripts/role_view.py docs --role architect

# 3. 生成架构师专属文档
python3 scripts/role_view.py generate --role architect --type architecture --name "用户系统架构"
```

### 示例 4：结构优化工作流

```bash
# 1. 分析当前结构
python3 scripts/structure_optimizer.py --path ./your-project

# 2. 查看复杂度报告
cat complexity-report.json

# 3. 根据建议重新生成结构
python3 scripts/adaptive_structure.py --path ./your-project --structure-type domain

# 4. 验证一致性
python3 scripts/consistency_checker.py --path ./your-project
```

---

## 工具集成示例

### 与 AI 智能体集成

```python
from scripts.context_aware import ContextAwareness
from scripts.multi_hop_qa import MultiHopQA

# 初始化
awareness = ContextAwareness('./your-project')
qa = MultiHopQA('./your-project')

# 处理用户查询
query = "如何设计并实现用户认证系统？"
enhanced = awareness.process_query(query, user_role='developer')
result = qa.execute_multi_hop(enhanced.enhanced_query)

# 返回增强后的回答
print(f"置信度: {enhanced.confidence:.2%}")
print(f"建议知识: {enhanced.suggested_knowledge}")
print(f"答案: {result.final_answer}")
```

---

## 最佳实践

1. **使用自适应结构**：根据项目复杂度选择最合适的目录结构
2. **定期检查一致性**：使用 `consistency_checker.py` 定期检查文档与代码的一致性
3. **利用上下文感知**：在特定文件或角色下查询时，使用 `context_aware.py` 提升准确性
4. **多跳问答**：对于复杂问题，使用 `multi_hop_qa.py` 进行深度分析
5. **角色视图**：根据用户角色提供定制化的文档和回答

---

## 技术支持

如有问题或建议，请参考：
- [SKILL.md](../SKILL.md) - 主文档
- [references/core/](../references/core/) - 核心指南
- [references/roles/](../references/roles/) - 角色指南
