---
name: <语言名称>-skills
description: <编程语言>的系统性学习技能。适用于<语言>入门学习、基础语法、并发编程、Web开发等场景。
dependency:
  python:
    - <运行时环境>>=<最低版本>
  system:
    - <版本检查命令>
---

# <编程语言> Skills

## 任务目标
本 Skill 用于系统性学习 <编程语言> 编程。

### 核心能力
- <语言> 基础语法和数据类型
- 函数与模块化编程
- <并发/异步>编程（如适用）
- Web 服务开发（如适用）
- 错误处理与测试

### 触发条件
典型用户表达：
- "我想学习 <语言> 编程"
- "帮我快速上手 <语言>"
- "<语言> 项目开发指导"
- "<语言> 最佳实践"

## 前置准备

### 环境要求
- <运行时环境> >= <版本>
- 开发环境：IDE（推荐 <推荐IDE>）
- 包管理器：<包管理器名称>

### 依赖安装
```bash
# 安装运行时
<安装命令>

# 验证安装
<验证命令>
```

### 配置文件
<配置说明>

## 操作步骤

### 1. 基础语法学习
掌握 <语言> 的核心语法元素：
- 变量与数据类型
- 控制流（if/for/while）
- 函数定义与调用
- 错误处理

参考：[references/language-basics.md](references/language-basics.md)

### 2. 数据结构学习
学习 <语言> 的数据结构：
- <数据结构1>（如数组、切片）
- <数据结构2>（如字典、Map）
- <数据结构3>（如集合、Set）

参考：[references/data-structures.md](references/data-structures.md)

### 3. 并发编程（如适用）
学习 <语言> 的并发特性：
- <并发机制1>（如 Goroutines）
- <并发机制2>（如 Channels）
- <并发机制3>（如 Mutex）

参考：[references/concurrency-guide.md](references/concurrency-guide.md)

### 4. Web 开发（如适用）
使用 <语言> 构建 Web 服务：
- HTTP 服务器
- 路由处理
- 数据库操作

参考：[references/web-development.md](references/web-development.md)

### 5. 最佳实践
掌握 <语言> 的最佳实践：
- 代码风格规范
- 性能优化技巧
- 错误处理模式

参考：[references/best-practices.md](references/best-practices.md)

## 资源索引

### 领域参考
- [references/language-basics.md](references/language-basics.md)
  - 何时读取：学习基础语法时
  - 内容：语法详解、示例代码

- [references/data-structures.md](references/data-structures.md)
  - 何时读取：学习数据结构时
  - 内容：内置数据类型、操作方法

- [references/concurrency-guide.md](references/concurrency-guide.md)
  - 何时读取：学习并发编程时
  - 内容：并发模型、同步原语

- [references/web-development.md](references/web-development.md)
  - 何时读取：Web 开发项目时
  - 内容：Web 框架、HTTP 处理

- [references/best-practices.md](references/best-practices.md)
  - 何时读取：实际项目开发时
  - 内容：编码规范、优化技巧

### 代码示例
- [assets/hello-world.<语言扩展名>](assets/hello-world.<语言扩展名>)
  - 用途：Hello World 示例

- [assets/http-server.<语言扩展名>](assets/http-server.<语言扩展名>)
  - 用途：HTTP 服务器模板

- [assets/concurrent-worker.<语言扩展名>](assets/concurrent-worker.<语言扩展名>)
  - 用途：并发工作器模板

## 注意事项

### 代码风格
- 遵循官方推荐的代码风格
- 使用格式化工具（如适用）
- 添加必要的注释和文档

### 性能优化
- 避免不必要的内存分配
- 合理使用并发特性
- 了解性能分析工具

### 错误处理
- 始终处理可能的错误
- 提供有意义的错误信息
- 避免吞没错误

## 使用示例

### 示例1：Hello World
```<语言>
<Hello World 代码>
```

### 示例2：HTTP 服务器
```<语言>
<HTTP 服务器代码>
```

### 示例3：并发处理
```<语言>
<并发处理代码>
```
