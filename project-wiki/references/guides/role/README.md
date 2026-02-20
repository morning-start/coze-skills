# 角色视图总览

## 目录

1. [角色体系](#角色体系)
2. [角色映射](#角色映射)
3. [快速导航](#快速导航)
4. [使用方式](#使用方式)

---

## 角色体系

ProjectWiki 支持从 5 种不同角色的视角查看和管理项目文档，每种角色有专门的指南和模板。

### 角色列表

| 角色 | 英文名 | 关注重点 | 核心文档 |
|------|--------|----------|----------|
| 系统架构师 | Architect | 整体架构、技术选型、可扩展性 | [architect/architect-guide.md](architect/architect-guide.md) |
| 开发工程师 | Developer | 模块接口、数据结构、状态流转 | [developer/developer-guide.md](developer/developer-guide.md) |
| 测试工程师 | Tester | 边界条件、异常场景、数据一致性 | [tester/tester-guide.md](tester/tester-guide.md) |
| 运维 / SRE | Ops | 部署拓扑、资源需求、监控告警 | [ops/ops-guide.md](ops/ops-guide.md) |
| 产品经理 | Product | 功能覆盖、用户路径、体验风险 | [product/product-guide.md](product/product-guide.md) |

---

## 角色映射

### 系统架构师 / 技术负责人

**关注重点**：
- 整体架构合理性
- 技术选型依据
- 可扩展性/容灾能力
- 跨团队依赖

**文档内容需求**：
- 架构图（C4 模型）
- 决策记录（ADR）
- 非功能性需求（性能、安全）
- 演进路线

**适合的文档形式**：
- `architecture-guide.md`
- `tech-decisions/` 目录
- ADR 模板

**相关文件**：
- [architect/architect-guide.md](architect/architect-guide.md) - 架构师指南
- [architect/adr-template.md](architect/adr-template.md) - ADR 模板
- [architect/architecture-template.md](architect/architecture-template.md) - 架构设计模板

---

### 开发工程师（实现者）

**关注重点**：
- 模块接口定义
- 数据结构
- 状态流转
- 错误处理规则
- 本地调试方式

**文档内容需求**：
- 类图/序列图
- API 契约
- 示例代码
- 本地启动步骤

**适合的文档形式**：
- `module-design/*.md`
- 内联 Mermaid 图

**相关文件**：
- [developer/developer-guide.md](developer/developer-guide.md) - 开发者指南
- [developer/module-design-template.md](developer/module-design-template.md) - 模块设计模板
- [../document-guides/api-doc-guide.md](../document-guides/api-doc-guide.md) - API 文档指南
- [../templates/api-template.md](../templates/api-template.md) - API 文档模板

---

### 测试工程师

**关注重点**：
- 边界条件
- 异常场景
- 数据一致性规则
- 可观测性埋点

**文档内容需求**：
- 状态机图
- 错误码列表
- 日志/指标规范

**适合的文档形式**：
- 在模块设计中增加"测试要点"节

**相关文件**：
- [tester/tester-guide.md](tester/tester-guide.md) - 测试工程师指南
- [tester/test-plan-template.md](tester/test-plan-template.md) - 测试计划模板
- [developer/module-design-template.md](developer/module-design-template.md) - 模块设计模板（包含测试要点）

---

### 运维 / SRE

**关注重点**：
- 部署拓扑
- 资源需求
- 扩缩容策略
- 监控告警指标

**文档内容需求**：
- 部署架构图
- 资源清单（CPU/Mem）
- SLA/SLO 定义

**适合的文档形式**：
- `ops-runbook.md`

**相关文件**：
- [ops/ops-guide.md](ops/ops-guide.md) - 运维指南
- [ops/ops-runbook-template.md](ops/ops-runbook-template.md) - 运维手册模板

---

### 产品经理 / 业务方

**关注重点**：
- 功能是否覆盖需求
- 用户路径是否合理
- 是否有体验风险

**文档内容需求**：
- 用户旅程图
- 核心流程图
- 业务规则摘要

**适合的文档形式**：
- `user-flow.md`（轻量版，非技术细节）

**相关文件**：
- [product/product-guide.md](product/product-guide.md) - 产品经理指南
- [product/user-flow-template.md](product/user-flow-template.md) - 用户旅程模板

---

## 快速导航

### 按角色查找文档

**架构师**：
- [架构师指南](architect/architect-guide.md)
- [ADR 模板](architect/adr-template.md)
- [架构设计模板](architect/architecture-template.md)

**开发工程师**：
- [开发者指南](developer/developer-guide.md)
- [模块设计模板](developer/module-design-template.md)
- [API 文档指南](../document-guides/api-doc-guide.md)

**测试工程师**：
- [测试工程师指南](tester/tester-guide.md)
- [测试计划模板](tester/test-plan-template.md)

**运维/SRE**：
- [运维指南](ops/ops-guide.md)
- [运维手册模板](ops/ops-runbook-template.md)

**产品经理**：
- [产品经理指南](product/product-guide.md)
- [用户旅程模板](product/user-flow-template.md)

---

### 按文档类型查找

**架构文档**：
- 架构设计模板 → [architect/architecture-template.md](architect/architecture-template.md)
- ADR 模板 → [architect/adr-template.md](architect/adr-template.md)

**开发文档**：
- 模块设计模板 → [developer/module-design-template.md](developer/module-design-template.md)
- API 文档模板 → [../templates/api-template.md](../templates/api-template.md)
- 设计文档模板 → [../templates/design-doc-template.md](../templates/design-doc-template.md)

**测试文档**：
- 测试计划模板 → [tester/test-plan-template.md](tester/test-plan-template.md)

**运维文档**：
- 运维手册模板 → [ops/ops-runbook-template.md](ops/ops-runbook-template.md)

**产品文档**：
- 用户旅程模板 → [product/user-flow-template.md](product/user-flow-template.md)

---

## 使用方式

### 通过脚本查询

```bash
# 列出所有角色
python3 scripts/role_view.py --list-roles

# 查看特定角色的文档
python3 scripts/role_view.py --role architect

# 生成角色专属文档
python3 scripts/role_view.py --role architect --generate

# 查看角色映射
python3 scripts/role_view.py --mapping
```

### 通过自然语言查询

**架构师视角**：
```
"从架构师的角度，系统设计文档应该包含什么？"
→ 返回 architect-guide.md 的内容
```

**开发者视角**：
```
"从开发者的角度，如何编写模块设计文档？"
→ 返回 module-design-template.md 的内容
```

**测试工程师视角**：
```
"测试工程师需要关注哪些边界条件？"
→ 返回 tester-guide.md 的内容
```

**运维视角**：
```
"运维手册应该包含哪些内容？"
→ 返回 ops-runbook-template.md 的内容
```

**产品经理视角**：
```
"如何编写用户旅程图？"
→ 返回 user-flow-template.md 的内容
```

---

## 角色协作

### 文档协作流程

```mermaid
flowchart LR
    PM[产品经理] -->|需求| AD[架构师]
    AD -->|技术方案| DEV[开发工程师]
    DEV -->|代码实现| TEST[测试工程师]
    TEST -->|上线| OPS[运维/SRE]
    OPS -->|反馈| AD
```

### 角色间文档传递

| 来源角色 | 文档类型 | 目标角色 | 用途 |
|----------|----------|----------|------|
| 产品经理 | 用户旅程图 | 架构师 | 理解业务需求 |
| 架构师 | 架构设计文档 | 开发工程师 | 实现技术方案 |
| 架构师 | ADR | 开发工程师 | 理解技术决策 |
| 开发工程师 | 模块设计文档 | 测试工程师 | 编写测试用例 |
| 开发工程师 | API 文档 | 测试工程师 | 接口测试 |
| 开发工程师 | 模块设计文档 | 运维/SRE | 了解系统依赖 |
| 运维/SRE | 运维手册 | 架构师 | 反馈性能瓶颈 |

---

**最后更新**：2024-02-19
