# 文档管理流程指南

## 概述

本文档提供系统性的文档管理流程，涵盖项目全生命周期中的文档创建、维护、共享和归档。

---

## 一、核心目标

| 目标 | 说明 | 实现方法 |
|------|------|---------|
| **一致性** | 术语、格式、版本统一 | 使用标准模板、术语表 |
| **可追溯性** | 需求→设计→实现→测试文档链完整 | 需求追踪矩阵（RTM） |
| **可访问性** | 团队成员快速找到最新有效文档 | 集中存储、清晰索引 |
| **时效性** | 文档随代码/需求同步更新 | 文档即代码文化 |
| **安全性** | 敏感文档权限可控 | 权限管理、敏感信息脱敏 |

---

## 二、角色与职责

| 角色 | 职责 | 主要文档 |
|------|------|---------|
| **产品经理（PM）** | 编写/维护需求文档、用户故事、PRD | 需求文档、用户故事 |
| **技术负责人** | 主导架构设计、接口规范、技术决策 | 架构文档、API 规范 |
| **开发工程师** | 编写模块设计、API 注释、部署脚本 | 模块设计、API 文档 |
| **测试工程师** | 编写测试计划、用例、缺陷报告 | 测试计划、测试用例 |
| **DevOps/SRE** | 维护部署手册、监控告警文档 | 部署手册、运维文档 |
| **文档管理员** | 推动流程执行、组织评审、归档管理 | 评审记录、归档文档 |

**小团队提示**：角色可合并，但责任必须明确到人。

---

## 三、文档生命周期管理流程

### 阶段 1：规划与创建

**目标**：在项目启动或迭代规划时，明确需要产出的文档。

**关键活动**：
1. 确定文档清单（参考 [项目类型文档指南](../project-types/README.md)）
2. 选择标准模板（参考 [模板库](../templates/README.md)）
3. 创建 wiki/ 目录，与代码同源管理
4. 分配文档责任人

**输出**：
- 文档清单
- 文档目录结构
- 责任人分配表

**示例**：
```markdown
# 项目文档清单

## 必备文档
- [ ] README.md - 项目负责人
- [ ] ARCHITECTURE.md - 技术负责人
- [ ] API.md - 后端开发
- [ ] TEST_PLAN.md - 测试工程师

## 选作文档
- [ ] USER_GUIDE.md - 产品经理
- [ ] DEPLOYMENT.md - DevOps
```

---

### 阶段 2：编写与协作

**目标**：使用合适的工具和协作方式编写文档。

**关键活动**：
1. 选择协作平台（Confluence、Notion、GitBook 等）
2. 使用代码化文档（OpenAPI YAML、PlantUML、Mermaid）
3. 支持评论、@提及、版本对比
4. 定期同步文档进度

**最佳实践**：
- 技术文档优先使用 Markdown
- 图表使用 Mermaid（代码化、可版本控制）
- API 文档使用 OpenAPI/Swagger
- 文档与代码一起提交 Git

---

### 阶段 3：评审与批准

**目标**：确保关键文档质量。

**关键活动**：
1. 选择评审方式：
   - **异步**：PR/MR 中附带文档变更，团队 Review
   - **同步**：设计评审会议（DR Meeting）
2. 使用评审 checklist（详见 [评审 checklist 模板](../templates/document-review-checklist.md)）
3. 记录评审意见和修改
4. 获得批准后发布

**评审 checklist**：
- [ ] 是否覆盖所有需求？
- [ ] 术语是否一致？
- [ ] 是否有歧义或模糊描述？
- [ ] 是否可测试/可实现？
- [ ] 格式是否规范？
- [ ] 链接是否有效？

---

### 阶段 4：发布与同步

**目标**：文档与代码同步发布。

**关键活动**：
1. CI 自动部署文档站点
2. 在 README 或公告中标明文档版本
3. 使用语义化版本（docs-v1.2.0 对应 app-v1.2.0）
4. 通知相关干系人

**示例**：
```yaml
# .github/workflows/docs-deploy.yml
name: Deploy Documentation
on:
  release:
    types: [published]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run docs:build
      - run: npm run docs:deploy
```

---

### 阶段 5：维护与更新

**目标**：保持文档的准确性和时效性。

**关键活动**：
1. 建立"文档即代码"文化
2. 功能变更 PR 必须包含文档更新
3. 设置文档健康度检查（详见 [健康度检查指南](document-health-check-guide.md)）
4. 定期（如每季度）清理废弃文档

**健康度检查项**：
- broken link 检测
- 过期标记
- 内容准确性验证
- 格式规范检查
- 更新频率监控

---

### 阶段 6：归档与退役

**目标**：项目结束或版本 EOL 后，文档安全归档。

**关键活动**：
1. 文档打标签归档（git tag）
2. 保留历史版本供审计或回溯
3. 敏感信息（如密钥、内部链接）在归档前脱敏
4. 更新文档索引，标记已归档

**归档清单**：
- [ ] 所有文档已标记归档版本
- [ ] 敏感信息已脱敏
- [ ] 历史版本已保留
- [ ] 文档索引已更新
- [ ] 相关干系人已通知

---

## 四、推荐工具链

| 功能 | 推荐工具 | 适用场景 |
|------|---------|---------|
| **文档编写** | Markdown + VS Code / Typora / Obsidian | 技术文档、笔记 |
| **协作与知识库** | Confluence / Notion / Wiki.js / DokuWiki | 团队知识库 |
| **API 文档** | Swagger UI / Redoc / Postman | API 接口文档 |
| **静态文档站点** | MkDocs / Docusaurus / VitePress / Docsify | 项目文档站点 |
| **图表绘制** | Mermaid / Draw.io / Excalidraw | 流程图、架构图 |
| **版本与权限** | Git + GitHub/GitLab Pages | 版本文档管理 |
| **自动化检查** | Vale / markdown-link-check / custom CI scripts | 文档质量检查 |

---

## 五、常见反模式

详见 [文档管理反模式指南](document-management-anti-patterns.md)

**快速参考**：
- ❌ "文档最后再写" → 导致缺失或失真
- ❌ 文档散落在微信、邮件、本地电脑 → 知识孤岛
- ❌ 只有 Word/PDF → 无法版本对比、协作困难
- ❌ 无维护责任人 → 文档迅速过期
- ❌ 技术文档与代码脱节 → 开发者不信赖文档

---

## 六、轻量级流程

详见 [轻量级文档管理流程模板](../templates/lightweight-doc-management-process.md)

**快速参考**（适用于中小团队）：
1. 项目初始化 → 创建 wiki/ 目录
2. 每个 Feature PR → 必须包含 wiki/ 更新
3. 主干合并前 → CI 检查文档
4. 发布版本时 → 自动部署文档站点
5. 每月站会 → 快速 review 文档健康度（10 分钟）

---

## 七、使用示例

### 示例 1：新项目文档规划

**场景**：启动一个新的前端项目

**步骤**：
1. 查阅 [项目类型文档指南](../project-types/README.md)，确定文档清单
2. 创建 wiki/ 目录和基础文档
3. 分配责任人（PM 负责需求、Tech Lead 负责架构）
4. 使用标准模板编写文档
5. 组织评审并使用 checklist 检查
6. 发布并部署文档站点

### 示例 2：文档健康度检查

**场景**：每月定期检查

**步骤**：
1. 运行 broken link 检查脚本
2. 检查文档更新频率（超过 3 个月未更新标记为"可能过期"）
3. 验证内容准确性（抽样检查）
4. 生成健康度报告
5. 在月度站会 review 报告（10 分钟）

---

## 参考资料

- [评审 checklist 模板](../templates/document-review-checklist.md)
- [健康度检查指南](document-health-check-guide.md)
- [工具链指南](../knowledge/document-management-tools.md)
- [反模式指南](document-management-anti-patterns.md)
- [轻量级流程模板](../templates/lightweight-doc-management-process.md)
