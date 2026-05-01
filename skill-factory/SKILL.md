---
name: skill-factory
version: v9.2.0
author: skill-lifecycle
description: 技能工厂，基于"轻/重/薄/厚"四维分类生成技能；包含研究、分析、规划、生成、验证五个阶段
tags: [skill-factory, skill-family, skill-classification]
dependency:
  parent: skill-lifecycle
  children:
    - skill-factory-researcher
    - skill-factory-analyzer
    - skill-factory-planner
    - skill-factory-generator
    - skill-factory-packager
---

# Skill Factory - 技能工厂

## 任务目标

本 Skill 用于将技术文档或网站转化为结构化的技能族包。

**触发条件**: 当用户提供技术文档/URL 并要求生成技能时使用。

---

## 四维分类体系

```mermaid
flowchart TB
    subgraph 四维分类法
        direction LR
        L1["功能维度<br/>━━━━━━━━━━━━━<br/>轻 单一功能<br/>重 多模块"]
        L2["内容维度<br/>━━━━━━━━━━━━━<br/>厚 内容丰富<br/>薄 内容精简"]
    end
    
    Q1["🟢 轻+薄<br/>简单技能<br/>单文件 SKILL.md"]
    Q2["🔵 重+薄<br/>技能族-薄<br/>skills 子目录"]
    Q3["🟠 轻+厚<br/>复杂单技能<br/>SKILL.md + refs"]
    Q4["🟣 重+厚<br/>技能族-厚<br/>混合模式"]
    
    style Q1 fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    style Q2 fill:#e3f2fd,stroke:#2196f3,color:#0d47a1
    style Q3 fill:#fff3e0,stroke:#ff9800,color:#e65100
    style Q4 fill:#f3e5f5,stroke:#9c27b0,color:#4a148c
```

### 维度定义

| 维度 | 定义 | 判断标准 | 输出结构 |
|------|------|---------|---------|
| **轻** | 功能单一 | 1 个核心能力，逻辑简单 | 单个 SKILL.md |
| **重** | 功能复杂 | 多个模块，可独立使用 | `skills/{子}/SKILL.md` |
| **薄** | 内容精简 | 单文件 <300 行能描述清楚 | 无需额外文件 |
| **厚** | 内容丰富 | 需要详细说明、示例、代码等 | `references/` + 可选 `scripts/` `templates/` |

### 四种组合与输出结构

| 组合 | 类型 | 目录结构 | 典型场景 |
|------|------|---------|---------|
| **轻+薄** | 简单技能 | `{name}/SKILL.md` | 工具类、格式转换 |
| **重+薄** | 技能族(薄) | `{name}-family/SKILL.md` + `skills/{子}/SKILL.md` | CLI工具集、工作流编排器 |
| **轻+厚** | 复杂单技能 | `{name}/SKILL.md` + `references/*.md` | 数据处理管道、详细教程 |
| **重+厚** | 技能族(厚) | `{name}-family/SKILL.md` + `skills/{子}/` (+ 部分 `references/`) | 大型框架学习包 |

---

## 完整工作流程（五阶段）

```mermaid
flowchart LR
    A[用户输入] --> R[researcher 信息研究]
    
    R -->|需求明确| N[需求文档]
    
    N --> AN[analyzer 技术分析]
    AN --> PL[planner 判定类型]
    PL --> GE[generator 按类型生成]
    GE --> PA[packager 结构验证]
    PA --> OUT[输出 技能包]
    
    subgraph researcher 内部
        direction TB
        R1[浏览内容]
        R2[交互确认]
        R3[搜索补充]
    end
    
    style A fill:#f5f5f5,color:#424242
    style R fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px,color:#1a237e
    style N fill:#c5cae9,stroke:#303f9f,color:#1a237e
    style AN fill:#e3f2fd,stroke:#2196f3,color:#0d47a1
    style PL fill:#fff3e0,stroke:#ff9800,color:#e65100
    style GE fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    style PA fill:#fce4ec,stroke:#e91e63,color:#880e4f
    style OUT fill:#f3e5f5,stroke:#9c27b0,color:#4a148c
```

### 阶段职责总览

| 阶段 | 子技能 | 核心职责 | 关键能力 |
|------|--------|----------|---------|
| **① 研究** | **researcher** | 接收输入、交互确认、补充信息 | 用户交互、网络搜索 |
| 分析 | analyzer | 提取技术信息，评估功能数量和内容体量 | 信息完整度 >= 80%？ |
| 规划 | planner | **判定轻重薄厚**，选择输出结构 | 轻/重 + 薄/厚 四维决策 |
| 生成 | generator | **按四种类型**生成对应目录和文件 | 四种输出模板 |
| 打包 | packager | **验证对应结构**的完整性 | 四种验证规则 |

---

## 快速决策流程

```mermaid
flowchart TD
    A[输入: 技术文档/URL] --> B{功能维度判断}
    
    B -->|1-2 个核心能力| C[轻: 单一功能]
    B -->|3个以上可独立模块| D[重: 多模块拆分]
    
    C --> E{内容维度判断}
    D --> F{内容维度判断}
    
    E -->|300行内能说清| G[类型1: 轻+薄<br/>简单技能]
    E -->|需要详细说明| H[类型3: 轻+厚<br/>复杂单技能]
    
    F -->|每个都简单| I[类型2: 重+薄<br/>技能族-薄]
    F -->|部分子技能复杂| J[类型4: 重+厚<br/>技能族-厚]
    
    style G fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    style H fill:#fff3e0,stroke:#ff9800,color:#e65100
    style I fill:#e3f2fd,stroke:#2196f3,color:#0d47a1
    style J fill:#f3e5f5,stroke:#9c27b0,color:#4a148c
```

---

## 子技能索引

| 子技能 | 阶段 | 职责 | 核心 |
|--------|------|------|------|
| [**researcher**](skills/skill-factory-researcher/SKILL.md) | ①研究 | 信息研究 | 交互确认、信息补充、需求明确 |
| [analyzer](skills/skill-factory-analyzer/SKILL.md) | ②分析 | 技术分析 | 信息完整度 >= 80%？ |
| [planner](skills/skill-factory-planner/SKILL.md) | ③规划 | 类型判定 | 轻/重 + 薄/厚 四维决策 |
| [generator](skills/skill-factory-generator/SKILL.md) | ④生成 | 文件生成 | 四种输出模板 |
| [packager](skills/skill-factory-packager/SKILL.md) | ⑤验证 | 结构验证 | 四种验证规则 |

---

## 前置研究阶段详解 (researcher)

### 为什么需要前置研究？

```mermaid
flowchart LR
    Old[旧流程: 直接分析] --> P1[问题1: 需求不明确]
    Old --> P2[问题2: 信息缺失]
    Old --> P3[问题3: 方向错误]
    
    New[新流程: 先研究再分析] --> S1[解决1: 明确用户意图]
    New --> S2[解决2: 补充必要资源]
    New --> S3[解决3: 对齐期望]
    
    style Old fill:#ffcdd2,stroke:#d32f2f,color:#b71c1c
    style New fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    style P1 fill:#ffcdd2,stroke:#d32f2f,color:#b71c1c
    style P2 fill:#ffcdd2,stroke:#d32f2f,color:#b71c1c
    style P3 fill:#ffcdd2,stroke:#d32f2f,color:#b71c1c
    style S1 fill:#c8e6c9,stroke:#388e3c,color:#1b5e20
    style S2 fill:#c8e6c9,stroke:#388e3c,color:#1b5e20
    style S3 fill:#c8e6c9,stroke:#388e3c,color:#1b5e20
```

### researcher 六步流程

```mermaid
flowchart TD
    Step1[Step 1: 接收输入] --> Step2[Step 2: 初步浏览]
    Step2 --> Step3[Step 3: 交互确认]
    Step3 --> Step4[Step 4: 缺失检测]
    Step4 --> Step5{Step 5: 补充信息}
    Step5 --> Step6[Step 6: 输出需求文档]
    
    Step5 --> Search[网络搜索]
    Step5 --> Ask[询问用户]
    
    Search --> Step6
    Ask --> Step6
    
    style Step1 fill:#e8eaf6,stroke:#3f51b5,color:#1a237e
    style Step2 fill:#e8eaf6,stroke:#3f51b5,color:#1a237e
    style Step3 fill:#fff3e0,stroke:#ff9800,color:#e65100
    style Step4 fill:#fff3e0,stroke:#ff9800,color:#e65100
    style Step5 fill:#ffe0b2,stroke:#fb8c00,color:#e65100
    style Step6 fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    style Search fill:#c5cae9,stroke:#303f9f,color:#1a237e
    style Ask fill:#ffe0b2,stroke:#fb8c00,color:#e65100
```

### 全程回调机制

在后续任何阶段发现信息不足时，都可以回调 researcher：

```mermaid
sequenceDiagram
    participant User as 用户
    participant Res as researcher
    participant Ana as analyzer
    participant Web as 网络
    
    User->>Res: 输入 URL 或文件夹
    Res->>Res: 浏览加交互加补充
    Res->>Ana: 需求文档
    
    Ana->>Ana: 分析中...
    Ana-->>Res: 缺少 API 文档
    
    Res->>Web: 搜索 API 文档
    Web-->>Res: 找到
    
    Res->>User: 确认使用 REST 还是 GraphQL
    User-->>Res: REST
    
    Res->>Ana: 补充完成
    Ana->>A: 继续分析
```

---

## 四种类型架构示例

### 类型 1：轻+薄（简单技能）

适用于：单一功能的工具类技能

```mermaid
graph TD
    A[text-formatter] --> B[SKILL.md 全部内容在一个文件中]
    
    style A fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    style B fill:#c8e6c9,stroke:#388e3c,color:#1b5e20
```

### 类型 2：重+薄（技能族-薄）

适用于：多个独立工具，每个都很简单

```mermaid
graph TD
    A[cli-toolkit] --> B[SKILL.md 母技能编排器]
    A --> C[skills 目录]
    C --> D[file-ops SKILL.md]
    C --> E[text-process SKILL.md]
    C --> F[system-mgmt SKILL.md]
    
    style A fill:#e3f2fd,stroke:#2196f3,color:#0d47a1
    style B fill:#bbdefb,stroke:#1976d2,color:#0d47a1
    style C fill:#90caf9,stroke:#1565c0,color:#ffffff
```

### 类型 3：轻+厚（复杂单技能）

适用于：单一主题但内容非常丰富

```mermaid
graph TD
    A[data-pipeline] --> B[SKILL.md 概览加索引]
    A --> C[references 详细文档]
    A --> D[scripts 可选]
    A --> E[templates 可选]
    
    C --> C1[implementation]
    C --> C2[api-reference]
    C --> C3[examples]
    C --> C4[architecture]
    
    style A fill:#fff3e0,stroke:#ff9800,color:#e65100
    style B fill:#ffe0b2,stroke:#f57c00,color:#e65100
    style C fill:#ffcc80,stroke:#ef6c00,color:#e65100
```

### 类型 4：重+厚（技能族-厚）⭐

适用于：大型技术栈，外层拆分，内层补充资料

```mermaid
graph TD
    A[vue-family] --> B[SKILL.md 母技能]
    A --> C[metadata.json]
    A --> D[templates 可选]
    A --> E[skills 目录]
    
    E --> F[vue-core 厚子技能]
    E --> G[vue-router 薄子技能]
    E --> H[vue-state 薄子技能]
    
    F --> F1[SKILL.md 概览]
    F --> F2[references 详细文档]
    F2 --> F2a[reactivity]
    F2 --> F2b[component]
    F2 --> F2c[lifecycle]
    F --> F3[scripts 可选]
    
    G --> G1[SKILL.md 单文件]
    H --> H1[SKILL.md 单文件]
    
    style A fill:#f3e5f5,stroke:#9c27b0,color:#4a148c
    style B fill:#e1bee7,stroke:#7b1fa2,color:#4a148c
    style F fill:#ce93d8,stroke:#8e24aa,color:#4a148c
    style G fill:#e1bee7,stroke:#7b1fa2,color:#4a148c
    style H fill:#e1bee7,stroke:#7b1fa2,color:#4a148c
```

---

## 补充资源说明

当技能为**厚技能**时，除 `references/` 外还可包含：

```mermaid
graph LR
    A[厚技能] --> B[references 参考文档]
    A --> C[scripts 可执行脚本]
    A --> D[templates 模板文件]
    A --> E[assets 静态资源]
    
    style A fill:#fff3e0,stroke:#ff9800,stroke-width:3px,color:#e65100
    style B fill:#ffe0b2,color:#e65100
    style C fill:#ffe0b2,color:#e65100
    style D fill:#ffe0b2,color:#e65100
    style E fill:#ffe0b2,color:#e65100
```

| 目录 | 用途 | 何时创建 |
|------|------|---------|
| `references/` | 参考文档（.md） | 内容 >300 行时 |
| `scripts/` | 可执行脚本 | 有自动化操作时 |
| `templates/` | 模板文件 | 有初始化模板时 |
| `assets/` | 静态资源 | 有图片/图表时 |

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v9.2.0 | 2026-04-30 | 修复 Mermaid 渲染问题，替换不兼容的图表类型 |
| v9.1.0 | 2026-04-30 | 优化 Mermaid 语法和配色方案 |
| v9.0.0 | 2026-04-30 | 新增 researcher 信息研究阶段，支持交互和搜索 |
| v8.0.0 | 2026-04-30 | 添加 Mermaid 图表，图文并茂 |
| v7.0.0 | 2026-04-30 | 引入"轻/重/薄/厚"四维分类体系 |
