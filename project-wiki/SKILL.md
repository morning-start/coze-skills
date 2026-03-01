---
name: project-wiki
version: 5.0.0
description: 智能项目知识助手，支持基础文档生成（README/ROADMAP/CHANGELOG/ARCHITECTURE）、文档流程管理和知识库查询
tags: [project-wiki, documentation, knowledge-base, templates]
---

# ProjectWiki - 智能项目知识助手

ProjectWiki 是一个智能项目知识助手，支持基础文档生成、文档流程管理和知识库查询。

---

## 核心能力

1. **基础文档生成**: README、ROADMAP、CHANGELOG、ARCHITECTURE
2. **文档流程管理**: 生成、更新、修改、完善文档
3. **知识库查询**: 技术框架、设计模式、最佳实践速查

---

## 三步工作流程

### 第一步：查阅信息

1. 阅读项目结构和现有文档
2. 查询知识库获取技术信息
3. 确定需要生成的文档类型

### 第二步：执行操作

1. 选择合适的文档模板
2. 根据指南编写文档内容
3. 使用 Mermaid 绘制图表

### 第三步：检查验收

1. 验证文档完整性
2. 检查数据一致性
3. 确认格式规范

---

## 参考文档

| 文档 | 用途 | 何时使用 |
|------|------|---------|
| [guides/document/README.md](references/guides/document/README.md) | 文档编写指南 | 编写任何文档前 |
| [guides/document/architecture-doc-guide.md](references/guides/document/architecture-doc-guide.md) | 架构文档指南 | 编写 ARCHITECTURE.md |
| [guides/document/design-doc-guide.md](references/guides/document/design-doc-guide.md) | 设计文档指南 | 编写设计文档 |
| [guides/document/functional-doc-guide.md](references/guides/document/functional-doc-guide.md) | 功能文档指南 | 编写功能文档 |
| [guides/document/cicd-guide.md](references/guides/document/cicd-guide.md) | CI/CD 文档指南 | 编写部署文档 |
| [guides/document/changelog-guide.md](references/guides/document/changelog-guide.md) | 变更日志指南 | 编写 CHANGELOG |
| [guides/document/roadmap-guide.md](references/guides/document/roadmap-guide.md) | 路线图指南 | 编写 ROADMAP |
| [templates/README.md](references/templates/README.md) | 文档模板索引 | 选择模板时 |
| [knowledge/frameworks.md](references/knowledge/frameworks.md) | 框架速查 | 技术选型时 |
| [knowledge/patterns.md](references/knowledge/patterns.md) | 设计模式速查 | 架构设计时 |

---

## 文档类型速查

| 文档 | 文件名 | 用途 |
|------|--------|------|
| README | `README.md` | 项目介绍和快速开始 |
| ROADMAP | `ROADMAP.md` | 项目规划和里程碑 |
| CHANGELOG | `CHANGELOG.md` | 版本变更记录 |
| ARCHITECTURE | `ARCHITECTURE.md` | 系统架构设计 |
| API文档 | `docs/api.md` | API接口说明 |
| 设计文档 | `docs/design.md` | 详细设计说明 |

---

## 使用示例

### 示例：生成项目文档

**需求**: 为新项目生成完整文档

**第一步：查阅信息**
```
1. 分析项目结构
   - 项目类型: Web应用
   - 技术栈: React + FastAPI
   - 复杂度: 中等

2. 查询知识库
   - 阅读 [knowledge/frameworks.md](references/knowledge/frameworks.md)
   - 了解 React 和 FastAPI 最佳实践
```

**第二步：执行操作**
```
1. 生成 README.md
   - 使用 [templates/basic/README.md](references/templates/basic/README.md)
   - 填写项目信息

2. 生成 ARCHITECTURE.md
   - 使用 [templates/architecture/architecture.md](references/templates/architecture/architecture.md)
   - 绘制系统架构图

3. 生成 ROADMAP.md
   - 使用 [templates/core/ROADMAP.md](references/templates/core/ROADMAP.md)
   - 规划开发里程碑
```

**第三步：检查验收**
```
□ 所有必需文档已生成
□ 文档格式符合规范
□ 图表清晰可读
□ 链接全部有效

检验结果: ✅ 通过
```

---

## 注意事项

- **标准化优先**: 所有文档遵循项目规范
- **渐进式完善**: 从核心文档开始，逐步完善
- **保持一致性**: 确保术语、版本、配置在各文档间一致
- **及时更新**: 代码变更时同步更新文档
