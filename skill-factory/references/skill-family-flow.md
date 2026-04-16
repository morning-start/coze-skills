---
name: skill-family-flow
description: 技能族创建流程指南，定义从规划到打包的完整流程，包括母技能和子技能的创建规范
tags: [skill-family, parent-skill, child-skill, planning, packaging, workflow]
---

# 技能族创建流程

## 概述

技能族（Skill Family）是围绕同一技术栈的多个相关技能的集合。本文档定义技能族的创建流程，确保母技能和子技能都能独立存在并协同工作。

## 核心概念

### 技能族结构

```
vue-skills/                          # 技能族目录（母技能）
├── SKILL.md                        # 母技能定义
├── references/                     # 母技能参考文档
│   └── overview.md                 # 技能族概述
└── skills/                         # 子技能目录
    ├── vue-core-skill/             # 核心技能
    │   ├── SKILL.md
    │   └── references/
    ├── vue-router-skill/           # 路由技能
    │   ├── SKILL.md
    │   └── references/
    ├── vue-pinia-skill/            # 状态管理技能
    │   ├── SKILL.md
    │   └── references/
    └── vue-testing-skill/          # 测试技能
        ├── SKILL.md
        └── references/
```

### 母技能 vs 子技能

| 特性         | 母技能           | 子技能                   |
| ------------ | ---------------- | ------------------------ |
| **命名**     | `vue-skills`     | `vue-core-skill`         |
| **定位**     | 技能族整体概览   | 单个功能模块             |
| **依赖**     | 无外部依赖       | 可依赖母技能或其他子技能 |
| **独立性**   | 可独立使用       | 可独立使用               |
| **SKILL.md** | 技能族概述和索引 | 单个技能完整定义         |

---

## 完整流程

```
┌─────────────────────────────────────────────────────────────┐
│  技能族创建核心流程                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ① 技能族规划 ──→ ② 母技能创建 ──→ ③ 子技能创建 ──→ ④ 打包  │
│        │              │                │               │    │
│        ▼              ▼                ▼               ▼    │
│  [结构设计]    [母技能 SKILL]   [子技能 SKILL]    [目录结构]  │
│  [子技能列表]  [参考文档]       [独立验证]        [打包验证]  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 关键节点速查

| 节点             | 准入条件   | 核心产出                | 准出条件           |
| ---------------- | ---------- | ----------------------- | ------------------ |
| **① 技能族规划** | 需求明确   | 技能族结构 + 子技能列表 | 规划文档完成       |
| **② 母技能创建** | 规划通过   | 母技能 SKILL.md         | 母技能通过验证     |
| **③ 子技能创建** | 母技能完成 | 子技能 SKILL.md         | 所有子技能通过验证 |
| **④ 打包**       | 子技能完成 | 技能族目录结构          | 打包验证通过       |

---

## 第一步：技能族规划

### 准入条件

✅ 需求已明确（技术栈、应用场景、目标用户）

### 核心操作

#### 1. 设计技能族结构

```markdown
## 技能族结构设计

### 技术栈：Vue.js

### 子技能列表

1. **vue-core-skill**（核心）
   - 对应模块：响应式、组件、模板
   - 依赖：无
   - 定位：基础技能

2. **vue-router-skill**（路由）
   - 对应模块：路由配置、导航守卫
   - 依赖：vue-core-skill
   - 定位：核心技能

3. **vue-pinia-skill**（状态管理）
   - 对应模块：Store、Actions、Getters
   - 依赖：vue-core-skill
   - 定位：核心技能

4. **vue-testing-skill**（测试）
   - 对应模块：单元测试、组件测试
   - 依赖：vue-core-skill
   - 定位：高级技能

### 技能族命名

- 母技能：`vue-skills`
- 子技能：`vue-{module}-skill`
```

#### 2. 确定依赖关系

```markdown
## 依赖关系图

vue-core-skill（基础，无依赖）
├── vue-router-skill
├── vue-pinia-skill
└── vue-testing-skill
```

### 准出条件

- [ ] 技能族结构设计完成
- [ ] 子技能列表明确（名称、定位、依赖）
- [ ] 依赖关系图清晰

---

## 第二步：母技能创建

### 准入条件

✅ 技能族规划准出条件全部满足

### 核心操作

#### 1. 创建母技能目录结构

```bash
mkdir vue-skills
cd vue-skills
touch SKILL.md
mkdir references
mkdir skills
```

#### 2. 编写母技能 SKILL.md

````yaml
---
name: vue-skills
version: v1.0.0
author: skill-factory
description: Vue.js 技术栈技能族，包含核心、路由、状态管理、测试等子技能，适用于 Vue 3 全栈开发
tags: [vue, javascript, frontend, skill-family]
---

# Vue Skills - Vue.js 技能族

## 技能族概述

Vue Skills 是 Vue.js 技术栈的完整技能族，包含以下子技能：

- **vue-core-skill**：Vue 核心技能（响应式、组件、模板）
- **vue-router-skill**：Vue Router 路由技能
- **vue-pinia-skill**：Pinia 状态管理技能
- **vue-testing-skill**：Vue 测试技能

## 子技能列表

| 子技能 | 版本 | 描述 | 依赖 |
|--------|------|------|------|
| vue-core-skill | v1.0.0 | Vue 核心概念和组件开发 | 无 |
| vue-router-skill | v1.0.0 | Vue Router 路由管理 | vue-core-skill |
| vue-pinia-skill | v1.0.0 | Pinia 状态管理 | vue-core-skill |
| vue-testing-skill | v1.0.0 | Vue 组件和单元测试 | vue-core-skill |

## 使用方式

### 单独使用子技能

```bash
# 使用 Vue 核心技能
/ Skill vue-core-skill

# 使用 Vue Router 技能
/ Skill vue-router-skill
````

### 使用完整技能族

```bash
# 使用 Vue 全技能族
/ Skill vue-skills
```

## 技能族结构

```
vue-skills/
├── SKILL.md                    # 母技能定义
├── references/
│   └── overview.md            # 技能族概述
└── skills/                     # 子技能目录
    ├── vue-core-skill/
    ├── vue-router-skill/
    ├── vue-pinia-skill/
    └── vue-testing-skill/
```

````

#### 3. 创建技能族概述文档

```markdown
# Vue Skills 概述

## 技术栈

Vue.js 3.x - 渐进式 JavaScript 框架

## 技能族组成

| 子技能 | 定位 | 核心内容 |
|--------|------|---------|
| vue-core-skill | 基础 | 响应式系统、组件开发、模板语法 |
| vue-router-skill | 核心 | 路由配置、导航守卫、路由动画 |
| vue-pinia-skill | 核心 | Store、Actions、Getters、插件 |
| vue-testing-skill | 高级 | 单元测试、组件测试、E2E 测试 |

## 学习路径

1. **vue-core-skill**（先学）
2. **vue-router-skill** 或 **vue-pinia-skill**（并行）
3. **vue-testing-skill**（后学）

## 版本兼容性

- Vue 3.0+
- Vue Router 4.0+
- Pinia 2.0+
````

### 准出条件

- [ ] 母技能 SKILL.md 完整
- [ ] 子技能列表准确
- [ ] 技能族结构清晰
- [ ] 母技能通过标准化验证

---

## 第三步：子技能创建

### 准入条件

✅ 母技能创建准出条件全部满足

### 核心操作

#### 1. 创建子技能目录结构

每个子技能都需要独立的目录：

```bash
cd vue-skills/skills

mkdir vue-core-skill
cd vue-core-skill
touch SKILL.md
mkdir references

mkdir vue-router-skill
cd vue-router-skill
touch SKILL.md
mkdir references

# ... 其他子技能
```

#### 2. 编写子技能 SKILL.md

**vue-core-skill 示例**：

````yaml
---
name: vue-core-skill
version: v1.0.0
author: skill-factory
parent: vue-skills
description: Vue 3 核心技能，掌握响应式系统、组件开发、模板语法等核心概念，是 Vue 技术栈的基础技能
tags: [vue, javascript, reactivity, component, template]
dependency:
  parent: vue-skills
---

# Vue Core Skill - Vue 核心技能

## 任务目标

- **本 Skill 用于**：掌握 Vue 3 核心概念和组件开发基础
- **核心能力**：
  - 响应式系统原理
  - 组件开发模式
  - 模板语法
  - 组合式 API
- **触发条件**：学习 Vue.js 基础或需要深入理解 Vue 响应式原理时

## 使用示例

### 示例：创建响应式组件

**输入**：Vue 3 Composition API 代码

**输出**：具有响应式特性的 Vue 组件

```vue
<script setup>
import { ref, reactive, computed } from 'vue'

// 响应式数据
const count = ref(0)
const state = reactive({
  name: 'Vue'
})

// 计算属性
const doubled = computed(() => count.value * 2)

// 方法
function increment() {
  count.value++
}
</script>

<template>
  <div>
    <h1>{{ state.name }}: {{ count }}</h1>
    <p>Double: {{ doubled }}</p>
    <button @click="increment">+1</button>
  </div>
</template>
````

```

## 依赖关系

- **父技能**：vue-skills
- **依赖技能**：无
- **被依赖**：vue-router-skill, vue-pinia-skill, vue-testing-skill
```

**vue-router-skill 示例**：

```yaml
---
name: vue-router-skill
version: v1.0.0
author: skill-factory
parent: vue-skills
description: Vue Router 4 路由技能，掌握路由配置、导航守卫、路由动画等，适用于单页应用路由管理
tags: [vue, vue-router, spa, navigation]
dependency:
  parent: vue-skills
  requires: vue-core-skill
---

# Vue Router Skill - Vue 路由技能

## 任务目标

- **本 Skill 用于**：掌握 Vue Router 4 路由管理
- **核心能力**：
  - 路由配置
  - 导航守卫
  - 路由动画
- **触发条件**：开发 Vue 单页应用需要路由管理时
- **依赖**：vue-core-skill
```

#### 3. 独立验证每个子技能

```bash
# 验证 vue-core-skill
head -10 vue-skills/skills/vue-core-skill/SKILL.md

# 验证 vue-router-skill
head -10 vue-skills/skills/vue-router-skill/SKILL.md

# ... 验证所有子技能
```

### 准出条件

- [ ] 所有子技能 SKILL.md 完整
- [ ] 每个子技能独立通过标准化验证
- [ ] 依赖关系正确（parent 和 requires 字段）
- [ ] 子技能间依赖无循环

---

## 第四步：打包

### 准入条件

✅ 所有子技能创建准出条件全部满足

### 核心操作

#### 1. 验证技能族目录结构

```bash
# 检查目录结构
tree vue-skills/

# 预期结构
vue-skills/
├── SKILL.md
├── references/
│   └── overview.md
└── skills/
    ├── vue-core-skill/
    │   └── SKILL.md
    ├── vue-router-skill/
    │   └── SKILL.md
    ├── vue-pinia-skill/
    │   └── SKILL.md
    └── vue-testing-skill/
        └── SKILL.md
```

#### 2. 验证打包完整性

```markdown
## 打包验证清单

- [ ] 母技能 SKILL.md 存在
- [ ] 所有子技能目录存在
- [ ] 每个子技能都有独立的 SKILL.md
- [ ] 母技能引用所有子技能
- [ ] 子技能的 parent 指向正确
- [ ] 版本号一致性（建议统一）
```

#### 3. 创建打包说明

````markdown
# Vue Skills 打包说明

## 打包内容

- 母技能：vue-skills
- 子技能：vue-core-skill, vue-router-skill, vue-pinia-skill, vue-testing-skill

## 使用方式

### 安装完整技能族

```bash
# 克隆技能族
git clone <repo>/vue-skills

# 安装依赖（如有）
cd vue-skills
npm install
```
````

### 单独使用某个子技能

```bash
# 进入子技能目录
cd vue-skills/skills/vue-core-skill

# 使用该技能
/ Skill vue-core-skill
```

```

### 准出条件
- [ ] 目录结构完整
- [ ] 所有 SKILL.md 存在
- [ ] 打包验证清单全部通过

---

## 快速执行清单

### 创建技能族时执行

```

□ 1. 技能族规划
□ 明确技术栈
□ 设计子技能列表
□ 确定依赖关系

□ 2. 母技能创建
□ 创建母技能目录
□ 编写母技能 SKILL.md
□ 创建技能族概述文档
□ 母技能通过验证

□ 3. 子技能创建
□ 创建所有子技能目录
□ 编写每个子技能的 SKILL.md
□ 设置正确的 parent 和 requires
□ 每个子技能通过验证

□ 4. 打包
□ 验证目录结构
□ 执行打包验证清单
□ 创建打包说明

````

---

## 命名规范

### 母技能命名

- 格式：`{tech}-skills`（小写字母 + 连字符）
- 示例：`vue-skills`、`react-skills`、`golang-skills`
- **不以 -skill 结尾**

### 子技能命名

- 格式：`{tech}-{module}-skill`（小写字母 + 连字符）
- 示例：`vue-core-skill`、`vue-router-skill`、`react-hooks-skill`
- **必须以 -skill 结尾**

### parent 和 requires 字段

```yaml
# 子技能 SKILL.md
---
parent: {parent-skill-name}    # 必填，指向母技能
dependency:
  requires:                     # 可选，指向依赖的子技能
    - {skill-name-1}
    - {skill-name-2}
---
````

---

## 常见问题

### Q1: 子技能可以独立使用吗？

**答**：可以。每个子技能都是独立的技能，拥有完整的 SKILL.md，可以单独使用。

### Q2: 子技能之间的依赖关系？

**答**：子技能之间可以有依赖关系，通过 SKILL.md 的 `dependency.requires` 字段声明。避免循环依赖。

### Q3: 技能族和子技能的版本号？

**答**：建议保持一致，但非强制。母技能版本代表技能族整体版本，子技能可以独立更新。

### Q4: 多个技术栈的技能族？

**答**：每个技术栈对应一个技能族。例如：

- `frontend-skills/`（前端技能族）
  - `react-skills/`
  - `vue-skills/`
  - `angular-skills/`

---

## 参考文档

- [主文档](../SKILL.md) - 技能概览
- [web-analysis-flow.md](web-analysis-flow.md) - 网站分析流程
- [document-analysis-flow.md](document-analysis-flow.md) - 文档分析流程
