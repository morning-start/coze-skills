---
name: <框架名称>-skills
description: <框架名称>的系统性学习技能。适用于<框架>入门学习、组件开发、状态管理、路由配置等场景。
dependency:
  python:
    - nodejs>=18.0.0
    - <包管理器>>=<最低版本>
  system:
    - <项目初始化命令>
---

# <框架名称> Skills

## 任务目标
本 Skill 用于系统性学习 <框架名称> 框架。

### 核心能力
- <框架> 核心概念与特性
- 组件化开发
- 状态管理
- 路由与导航
- 构建与部署

### 触发条件
典型用户表达：
- "我想学习 <框架>"
- "帮我快速上手 <框架>"
- "<框架> 项目开发指导"
- "<框架> 最佳实践"

## 前置准备

### 环境要求
- Node.js >= <版本>
- 包管理器：npm / yarn / pnpm
- 开发工具：<推荐IDE>

### 依赖安装
```bash
# 创建新项目
<初始化命令>

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 配置文件
- <配置文件1>：项目配置
- <配置文件2>：构建配置

## 操作步骤

### 1. 基础概念学习
理解 <框架> 的核心概念：
- <核心概念1>（如响应式系统）
- <核心概念2>（如虚拟DOM）
- <核心概念3>（如组件生命周期）

参考：[references/core-concepts.md](references/core-concepts.md)

### 2. 组件开发
学习组件化开发：
- 组件定义与使用
- Props 与数据传递
- 事件处理
- Slots / Children

参考：[references/components-guide.md](references/components-guide.md)

### 3. 状态管理
掌握状态管理方案：
- 本地状态（State）
- 全局状态（如 Vuex、Redux）
- 数据流向

参考：[references/state-management.md](references/state-management.md)

### 4. 路由与导航
实现页面路由：
- 路由配置
- 参数传递
- 导航守卫
- 动态路由

参考：[references/routing-guide.md](references/routing-guide.md)

### 5. 进阶特性
学习 <框架> 的高级特性：
- <高级特性1>（如自定义指令）
- <高级特性2>（如插件系统）
- <高级特性3>（如性能优化）

参考：[references/advanced-features.md](references/advanced-features.md)

### 6. 构建与部署
构建生产版本并部署：
- 生产构建
- 环境配置
- 部署策略

参考：[references/deployment-guide.md](references/deployment-guide.md)

## 资源索引

### 领域参考
- [references/core-concepts.md](references/core-concepts.md)
  - 何时读取：学习核心概念时
  - 内容：<框架> 设计理念、核心原理

- [references/components-guide.md](references/components-guide.md)
  - 何时读取：组件开发时
  - 内容：组件API、最佳实践

- [references/state-management.md](references/state-management.md)
  - 何时读取：状态管理时
  - 内容：状态方案、数据流

- [references/routing-guide.md](references/routing-guide.md)
  - 何时读取：路由配置时
  - 内容：路由API、配置方法

- [references/advanced-features.md](references/advanced-features.md)
  - 何时读取：学习高级特性时
  - 内容：插件、性能优化

- [references/deployment-guide.md](references/deployment-guide.md)
  - 何时读取：项目部署时
  - 内容：构建配置、部署流程

### 代码示例
- [assets/basic-component.<组件扩展名>](assets/basic-component.<组件扩展名>)
  - 用途：基础组件模板

- [assets/app-template.<组件扩展名>](assets/app-template.<组件扩展名>)
  - 用途：应用入口模板

- [assets/config.<配置扩展名>](assets/config.<配置扩展名>)
  - 用途：配置文件模板

## 注意事项

### 组件设计
- 保持组件单一职责
- 合理划分组件粒度
- 遵循命名规范

### 性能优化
- 避免不必要的重新渲染
- 合理使用计算属性
- 懒加载与代码分割

### 最佳实践
- 使用 TypeScript（推荐）
- 遵循官方代码风格
- 编写单元测试

## 使用示例

### 示例1：基础组件
```<组件语言>
<基础组件代码>
```

### 示例2：状态管理
```<组件语言>
<状态管理代码>
```

### 示例3：路由配置
```<组件语言>
<路由配置代码>
```
