# 常见技术文档模式识别

本参考文档帮助智能体识别和分析技术栈官方文档的组织结构，为子技能生成提供依据。

## 目录
- [前端框架文档模式](#前端框架文档模式)
- [后端语言文档模式](#后端语言文档模式)
- [工具库文档模式](#工具库文档模式)
- [内容提取策略](#内容提取策略)

## 概览
不同类型的技术栈有其独特的文档组织模式，识别这些模式有助于更精准地提取关键内容和设计子技能结构。

## 前端框架文档模式

### Vue.js 模式
**典型结构**：
```
/
├── /guide          # 教程
│   ├── /introduction
│   ├── /essentials    # 基础知识
│   └── /components    # 组件开发
├── /api            # API 参考
│   ├── /built-in-components
│   └── /built-in-directives
├── /examples       # 示例
└── /reference      # 高级参考
```

**核心概念关键词**：
- 响应式系统（Reactivity）
- 组件（Components）
- 指令（Directives）
- 组合式 API（Composition API）
- 生命周期钩子（Lifecycle Hooks）

**学习路径**：
1. Introduction（介绍）
2. Essentials（基础：响应式、计算属性、监听器）
3. Components（组件：Props、Emits、Slots）
4. Built-in Directives（内置指令）
5. Router & State Management（路由和状态管理）

### React 模式
**典型结构**：
```
/
├── /learn          # 学习路径
│   ├── /start-a-new-react-project
│   ├── /adding-interactivity
│   └── /managing-state
├── /reference       # 参考
│   ├── /react
│   ├── /react-dom
│   └── /hooks
└── /apis           # API 文档
```

**核心概念关键词**：
- JSX
- Components（组件）
- Props
- State（状态）
- Effects（副作用）
- Hooks

**学习路径**：
1. Quick Start（快速开始）
2. Describing the UI（描述 UI）
3. Adding Interactivity（添加交互）
4. Managing State（状态管理）
5. Escape Hatches（高级用法）

### Angular 模式
**典型结构**：
```
/
├── /guide          # 指南
│   ├── /glossary
│   ├── /setup-local
│   └── /standalone-components
├── /tutorial       # 教程
└── /api            # API 参考
```

**核心概念关键词**：
- Components（组件）
- Templates（模板）
- Directives（指令）
- Services（服务）
- Dependency Injection（依赖注入）
- Modules（模块）

## 后端语言文档模式

### Go 模式
**典型结构**：
```
/
├── /doc            # 文档
│   ├── /effective_go
│   ├── /go-for-java-programmers
│   └── /go-for-python-programmers
├── /pkg            # 包文档
├── /tour           # 交互式教程
└── /wiki           # 社区Wiki
```

**核心概念关键词**：
- Goroutines（协程）
- Channels（通道）
- Interfaces（接口）
- Structs（结构体）
- Methods（方法）
- Packages（包）

**学习路径**：
1. A Tour of Go（Go 之旅）
2. How to Write Go Code（如何写 Go 代码）
3. Effective Go（有效的 Go）
4. Package Documentation（包文档）
5. Go by Example（实例学习）

### Python 模式
**典型结构**：
```
/
├── /doc            # 文档
│   ├── /tutorial   # 教程
│   ├── /library    # 标准库
│   └── /reference  # 参考
├── /howto          # 操作指南
└── /faq            # 常见问题
```

**核心概念关键词**：
- Modules（模块）
- Classes（类）
- Functions（函数）
- Decorators（装饰器）
- Context Managers（上下文管理器）
- Generators（生成器）

### Node.js 模式
**典型结构**：
```
/
├── /docs           # 文档
│   ├── /guides     # 指南
│   ├── /api        # API 参考
│   └── /es6        # ES6+ 特性
├── /about          # 关于
└── /learn          # 学习资源
```

**核心概念关键词**：
- Event Loop（事件循环）
- Modules（模块系统）
- Streams（流）
- Buffers（缓冲区）
- File System（文件系统）
- HTTP/HTTPS

## 工具库文档模式

### Webpack 模式
**典型结构**：
```
/
├── /concepts       # 概念
├── /configuration  # 配置
├── /api            # API
├── /guides         # 指南
└── /plugins        # 插件
```

**核心概念关键词**：
- Entry（入口）
- Output（输出）
- Loaders（加载器）
- Plugins（插件）
- Mode（模式）
- Optimization（优化）

### Docker 模式
**典型结构**：
```
/
├── /engine         # 引擎文档
├── /compose        # Compose
├── /network        # 网络
├── /storage        # 存储
└── /reference      # 参考
```

**核心概念关键词**：
- Images（镜像）
- Containers（容器）
- Dockerfile
- Volumes（卷）
- Networks（网络）
- Compose

## 内容提取策略

### 1. 识别文档类型
根据 URL 路径和页面标题判断文档类型：

| 关键词 | 文档类型 | 提取策略 |
|--------|----------|----------|
| guide, tutorial, learn, start, introduction | 教程 | 完整提取，保留示例代码 |
| api, reference, docs | 参考 | 提取 API 签名和用法示例 |
| examples, demo, sample | 示例 | 重点提取代码片段 |
| best-practices, tips, tricks | 最佳实践 | 提取规则和建议 |
| faq, troubleshooting | 问题解答 | 提取问题和解决方案 |

### 2. 过滤无关内容
以下内容应过滤掉：
- 导航菜单（如 "Skip to content"）
- 页脚（版权信息、社交媒体链接）
- 侧边栏（目录链接）
- 版本选择器
- 语言切换器
- 广告和推广

### 3. 保留关键元素
以下内容必须保留：
- 标题和子标题（用于构建 TOC）
- 代码示例（用于 assets/ 模板）
- 重要提示（Warning、Note、Tip）
- 链接引用（用于构建 references/）

### 4. 结构化整理
将抓取的内容按以下结构整理：

**基础概念层**
- 技术简介
- 核心概念列表
- 术语表

**API/功能层**
- 功能模块分类
- API 方法签名
- 参数说明

**实践层**
- 代码示例
- 最佳实践
- 常见问题

**进阶层**
- 高级用法
- 性能优化
- 生态工具

## 子技能设计建议

### 前端框架子技能
**核心章节**：
1. 基础概念（响应式/JSX/Template）
2. 组件开发（Props/State/Events）
3. 路由与导航
4. 状态管理
5. 构建与部署

**参考文档**：
- `core-concepts.md` - 核心概念详解
- `component-guide.md` - 组件开发指南
- `api-reference.md` - API 参考
- `best-practices.md` - 最佳实践

**资产模板**：
- 组件模板（`.vue` / `.jsx`）
- 应用模板
- 配置文件模板

### 后端语言子技能
**核心章节**：
1. 语法基础（变量、类型、控制流）
2. 函数与模块
3. 并发编程（如适用）
4. Web 开发
5. 数据库操作（如适用）

**参考文档**：
- `language-basics.md` - 语言基础
- `concurrency-guide.md` - 并发编程
- `web-development.md` - Web 开发
- `standard-library.md` - 标准库

**资产模板**：
- 基础代码模板
- HTTP 服务器模板
- 并发工作器模板

### 工具库子技能
**核心章节**：
1. 安装与配置
2. 基础用法
3. 配置选项详解
4. 插件/扩展
5. 优化技巧

**参考文档**：
- `configuration-guide.md` - 配置指南
- `api-reference.md` - API 参考
- `plugin-guide.md` - 插件指南
- `optimization-tips.md` - 优化技巧

**资产模板**：
- 基础配置文件
- 常用配置模板
- 示例项目

## 识别检查清单

在抓取和分析文档时，使用以下清单确保关键信息不被遗漏：

### 框架/语言特性
- [ ] 核心概念和术语
- [ ] 主要特性列表
- [ ] 版本兼容性信息
- [ ] 支持的平台和环境

### 学习路径
- [ ] 官方推荐的学习顺序
- [ ] 入门教程链接
- [ ] 进阶教程链接
- [ ] 实战项目示例

### API/功能
- [ ] API 方法签名
- [ ] 参数类型和说明
- [ ] 返回值说明
- [ ] 使用示例

### 最佳实践
- [ ] 官方推荐的编码规范
- [ ] 性能优化建议
- [ ] 常见陷阱和解决方案
- [ ] 安全注意事项

### 示例代码
- [ ] Hello World 示例
- [ ] 典型用法示例
- [ ] 完整项目示例
- [ ] 配置文件示例

## 提取优先级

按以下优先级提取内容：
1. **必需**（必须提取）：
   - 快速开始/入门指南
   - 核心概念文档
   - 主要 API 参考

2. **重要**（应提取）：
   - 最佳实践
   - 常见问题
   - 代码示例

3. **可选**（视情况提取）：
   - 高级用法
   - 生态工具
   - 历史变更说明

## 内容质量评估

评估抓取的内容质量：
- ✅ 内容完整，无截断
- ✅ 代码示例可运行
- ✅ 链接引用有效
- ✅ 格式清晰（Markdown 结构正确）
- ❌ 导航/页脚等无关内容未过滤
- ❌ 页面加载错误（超时、404）
- ❌ 内容需要登录才能访问
