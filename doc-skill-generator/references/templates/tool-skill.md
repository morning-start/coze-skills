---
name: <工具名称>-skills
description: <工具名称>的系统性学习技能。适用于<工具>入门学习、配置管理、插件使用、性能优化等场景。
dependency:
  python:
    - <工具包名>>=<最低版本>
  system:
    - <初始化命令>
---

# <工具名称> Skills

## 任务目标
本 Skill 用于系统性学习 <工具名称> 工具。

### 核心能力
- <工具> 核心概念与工作原理
- 配置文件管理
- 插件系统使用
- 性能优化技巧
- 与开发流程集成

### 触发条件
典型用户表达：
- "我想学习 <工具>"
- "帮我配置 <工具>"
- "<工具> 优化指导"
- "<工具> 与项目集成"

## 前置准备

### 环境要求
- 运行环境：<环境要求>
- 依赖工具：<依赖工具>
- Node.js / Python / 其他：<版本要求>

### 依赖安装
```bash
# 安装工具
<安装命令>

# 初始化配置
<初始化命令>

# 验证安装
<验证命令>
```

### 配置文件
- <配置文件1>：主配置文件
- <配置文件2>：环境配置
- <配置文件3>：插件配置

## 操作步骤

### 1. 基础概念学习
理解 <工具> 的工作原理：
- 核心概念与术语
- 工作流程
- 配置文件结构

参考：[references/core-concepts.md](references/core-concepts.md)

### 2. 快速开始
快速上手 <工具>：
- 最小配置示例
- 常用命令
- 基础任务执行

参考：[references/quick-start.md](references/quick-start.md)

### 3. 配置管理
掌握配置文件的编写：
- 配置选项详解
- 环境变量
- 多环境配置

参考：[references/configuration-guide.md](references/configuration-guide.md)

### 4. 插件系统
使用和开发插件：
- 官方插件列表
- 插件配置方法
- 自定义插件开发

参考：[references/plugin-guide.md](references/plugin-guide.md)

### 5. 性能优化
优化 <工具> 的性能：
- 性能瓶颈分析
- 优化策略
- 监控与调试

参考：[references/optimization-guide.md](references/optimization-guide.md)

### 6. 项目集成
将 <工具> 集成到开发流程：
- 与 CI/CD 集成
- 与其他工具配合
- 自动化工作流

参考：[references/integration-guide.md](references/integration-guide.md)

## 资源索引

### 领域参考
- [references/core-concepts.md](references/core-concepts.md)
  - 何时读取：学习核心概念时
  - 内容：<工具> 原理、架构设计

- [references/quick-start.md](references/quick-start.md)
  - 何时读取：快速上手时
  - 内容：快速配置、常用命令

- [references/configuration-guide.md](references/configuration-guide.md)
  - 何时读取：配置管理时
  - 内容：配置选项、最佳实践

- [references/plugin-guide.md](references/plugin-guide.md)
  - 何时读取：使用插件时
  - 内容：插件API、开发指南

- [references/optimization-guide.md](references/optimization-guide.md)
  - 何时读取：性能优化时
  - 内容：优化技巧、监控方法

- [references/integration-guide.md](references/integration-guide.md)
  - 何时读取：项目集成时
  - 内容：CI/CD、自动化流程

### 配置模板
- [assets/basic-config.<配置扩展名>](assets/basic-config.<配置扩展名>)
  - 用途：基础配置模板

- [assets/production-config.<配置扩展名>](assets/production-config.<配置扩展名>)
  - 用途：生产环境配置

- [assets/plugin-config.<配置扩展名>](assets/plugin-config.<配置扩展名>)
  - 用途：插件配置模板

## 注意事项

### 配置管理
- 使用版本控制管理配置文件
- 敏感信息使用环境变量
- 定期审查和更新配置

### 性能考虑
- 按需加载插件
- 合理设置缓存策略
- 监控性能指标

### 安全性
- 定期更新工具版本
- 使用官方插件
- 审查第三方插件安全性

## 使用示例

### 示例1：最小配置
```<配置语言>
<最小配置代码>
```

### 示例2：生产配置
```<配置语言>
<生产配置代码>
```

### 示例3：插件配置
```<配置语言>
<插件配置代码>
```

### 示例4：集成脚本
```<脚本语言>
<集成脚本代码>
```
