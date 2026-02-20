# 框架指引索引

## 📋 目录

1. [快速选择指南](#快速选择指南)
2. [框架分类](#框架分类)
3. [按使用场景搜索](#按使用场景搜索)
4. [框架详情](#框架详情)
5. [框架对比](#框架对比)

---

## 快速选择指南

**三步选择最适合的框架指引**：

### 步骤 1：确定项目类型

| 项目类型 | 推荐框架指引 |
|----------|-------------|
| **Web 后端 API** | Django / Flask / FastAPI / Spring Boot / Gin |
| **前端 Web 应用** | React / Vue / Svelte / SolidJS |
| **桌面应用** | Electron / Tauri / Wails |
| **移动应用** | Flutter |

### 步骤 2：根据语言选择

| 语言 | 可选框架 | 推荐场景 |
|------|----------|----------|
| **Python** | Django / Flask / FastAPI | 快速开发 → Django<br>轻量级 API → Flask<br>高性能异步 → FastAPI |
| **JavaScript** | React / Vue / Electron | 企业级应用 → React<br>渐进式开发 → Vue |
| **Java** | Spring Boot | 企业级应用、微服务 |
| **Go** | Gin / Wails | 高性能 API → Gin<br>桌面应用 → Wails |
| **Rust** | Tauri | 高安全性桌面应用 |
| **Dart** | Flutter | 跨平台移动应用 |

### 步骤 3：根据项目规模选择

| 项目规模 | 推荐框架 |
|----------|----------|
| **小型项目 / MVP** | Flask / Vue / Electron |
| **中型项目 / 团队 5-10 人** | FastAPI / React / Django |
| **大型项目 / 团队 10+ 人** | Spring Boot / Django + React |

---

## 框架分类

### 桌面应用框架（3 个）

| 框架 | 后端语言 | 特点 | 适用场景 | 推荐度 |
|------|---------|------|----------|--------|
| [Electron](#electron-框架) | Node.js | 成熟生态、跨平台、社区活跃 | 企业级桌面应用、需要丰富生态 | ⭐⭐⭐⭐⭐ |
| [Tauri](#tauri-框架) | Rust | 小体积、高安全性、低资源占用 | 对安全性/性能敏感的应用 | ⭐⭐⭐⭐ |
| [Wails](#wails-框架) | Go | 开发友好、配置简单 | Go 团队、快速开发 | ⭐⭐⭐ |

### 前端框架（4 个）

| 框架 | 类型 | 特点 | 适用场景 | 推荐度 |
|------|------|------|----------|--------|
| [React](#react-框架) | 虚拟 DOM | 大型生态、企业级、社区活跃 | 大型企业应用、复杂单页应用 | ⭐⭐⭐⭐⭐ |
| [Vue](#vue-框架) | 响应式 | 渐进式、易上手、模板语法 | 快速开发、中小型项目 | ⭐⭐⭐⭐⭐ |
| [Svelte](#svelte-框架) | 编译型 | 小包体积、高性能、无运行时 | 性能敏感的应用、小型项目 | ⭐⭐⭐⭐ |
| [SolidJS](#solidjs-框架) | 细粒度响应式 | 类似 JSX、无虚拟 DOM、高性能 | 性能优化、从 React 迁移 | ⭐⭐⭐ |

### Web API 框架（5 个）

| 框架 | 语言 | 特点 | 适用场景 | 推荐度 |
|------|------|------|----------|--------|
| [Django](#django-框架) | Python | 全栈、ORM、管理后台、Batteries-included | 企业级应用、快速开发、内容管理系统 | ⭐⭐⭐⭐⭐ |
| [Flask](#flask-框架) | Python | 轻量级、灵活、扩展性强 | 小型 API、微服务、快速原型 | ⭐⭐⭐⭐⭐ |
| [FastAPI](#fastapi-框架) | Python | 现代异步、自动文档、高性能 | 高性能 API、实时应用、微服务 | ⭐⭐⭐⭐⭐ |
| [Spring Boot](#spring-boot-框架) | Java | Spring 生态、企业级、自动配置 | 企业级应用、微服务、金融系统 | ⭐⭐⭐⭐⭐ |
| [Gin](#gin-框架) | Go | 高性能、简单 API、中间件 | 高性能 API、云原生应用 | ⭐⭐⭐⭐ |

### 跨平台 UI 框架（1 个）

| 框架 | 语言 | 特点 | 适用场景 | 推荐度 |
|------|------|------|----------|--------|
| [Flutter](#flutter-框架) | Dart | 单一代码库、多平台、热重载 | 跨平台移动应用、iOS + Android | ⭐⭐⭐⭐⭐ |

---

## 按使用场景搜索

### 🎯 场景 1：构建企业级 Web 应用

**推荐方案**：
- **后端**：Django（Python） / Spring Boot（Java）
- **前端**：React（JavaScript）

**查阅指引**：[Django](#django-框架) + [React](#react-框架)

---

### 🎯 场景 2：快速开发小型 API 服务

**推荐方案**：
- **后端**：Flask（Python） / Gin（Go）
- **前端**：Vue（JavaScript）

**查阅指引**：[Flask](#flask-框架) + [Vue](#vue-框架)

---

### 🎯 场景 3：构建高性能实时应用

**推荐方案**：
- **后端**：FastAPI（Python） / Gin（Go）
- **前端**：Svelte（JavaScript）

**查阅指引**：[FastAPI](#fastapi-框架) + [Svelte](#svelte-框架)

---

### 🎯 场景 4：跨平台移动应用

**推荐方案**：
- **框架**：Flutter（Dart）

**查阅指引**：[Flutter](#flutter-框架)

---

### 🎯 场景 5：桌面应用开发

**推荐方案**：
- **生态优先**：Electron（Node.js）
- **性能优先**：Tauri（Rust）
- **开发效率**：Wails（Go）

**查阅指引**：[Electron](#electron-框架) / [Tauri](#tauri-框架) / [Wails](#wails-框架)

---

### 🎯 场景 6：微服务架构

**推荐方案**：
- **后端**：Spring Boot（Java） / FastAPI（Python） / Gin（Go）

**查阅指引**：[Spring Boot](#spring-boot-框架) / [FastAPI](#fastapi-框架) / [Gin](#gin-框架)

---

### 🎯 场景 7：内容管理系统（CMS）

**推荐方案**：
- **后端**：Django（Python）

**查阅指引**：[Django](#django-框架)

---

## 框架详情

<a id="electron"></a>

### ⭐ Electron 框架

**概述**：使用 Node.js 作为后端、Web 技术作为前端构建跨平台桌面应用的框架。Electron 将 Chromium 和 Node.js 集成在同一个运行时环境中，支持 Windows、macOS 和 Linux 平台。它是目前最流行的跨平台桌面应用开发框架之一。

**关键文件/目录**：
- `main.js` / `main.ts` - 主进程入口
- `preload.js` / `preload.ts` - 预加载脚本
- `src/main/` - 主进程代码
- `src/renderer/` - 渲染进程代码
- `src/preload/` - 预加载脚本
- `package.json` - 项目配置
- `electron-builder.yml` - 打包配置

**版本兼容性**：
- 推荐版本：≥ 22.0
- 已知不兼容：Electron 版本与 Node.js 版本必须匹配

**特征关键词**：webview, nodejs, desktop, cross-platform, multi-process, chromium

**详细指南**：[electron-guide.md](electron-guide.md)

---

<a id="react"></a>

### ⭐ React 框架

**概述**：由 Facebook 开发的 JavaScript 库，用于构建用户界面。采用组件化架构和虚拟 DOM 技术，是目前使用最广泛的前端框架之一。

**关键文件/目录**：
- `*.jsx` / `*.tsx` - React 组件文件
- `src/` - 源代码目录
- `src/App.jsx` / `src/App.tsx` - 根组件
- `src/index.js` / `src/index.tsx` - 应用入口
- `public/` - 静态资源目录

**版本兼容性**：
- 推荐版本：≥ 18
- 已知不兼容：React 18 与某些旧版本 UI 库不兼容

**特征关键词**：virtual-dom, jsx, component-based, hooks, react-native, large-ecosystem

**详细指南**：[react-guide.md](react-guide.md)

---

<a id="vue"></a>

### ⭐ Vue 框架

**概述**：由尤雨溪创建的渐进式 JavaScript 框架，用于构建用户界面。采用模板语法和双向数据绑定，学习曲线平缓，适合初学者和快速开发。Vue 3 引入了 Composition API。

**关键文件/目录**：
- `*.vue` - Vue 单文件组件
- `vue.config.js` / `vue.config.ts` - Vue 配置文件
- `src/` - 源代码目录
- `src/App.vue` - 根组件
- `src/main.js` / `src/main.ts` - 应用入口

**版本兼容性**：
- 推荐版本：≥ 3.0
- 已知不兼容：Vue 2.x 与 Vue 3.x 有重大 breaking changes

**特征关键词**：reactive, component-based, template-syntax, directives, two-way-binding, vue-router

**详细指南**：[vue-guide.md](vue-guide.md)

---

<a id="django"></a>

### ⭐ Django 框架

**概述**：一个高级 Python Web 框架，遵循"约定优于配置"的原则，提供了一套完整的开发工具。Django 内置 ORM、认证、管理后台等功能，适合快速开发企业级应用。

**关键文件/目录**：
- `manage.py` - Django 命令行工具
- `settings.py` - 项目配置文件
- `urls.py` - URL 路由配置
- `models.py` - 数据模型定义
- `views.py` - 视图函数
- `templates/` - 模板目录

**版本兼容性**：
- 推荐版本：≥ 4.2
- 已知不兼容：Django 4.x 不支持 Python 3.7 及以下

**特征关键词**：batteries-included, orm, admin-interface, authentication, mvc, full-stack

**详细指南**：[django-guide.md](django-guide.md)

---

<a id="flask"></a>

### ⭐ Flask 框架

**概述**：一个轻量级 Python Web 框架，以其简洁性和灵活性著称。Flask 只提供核心功能（路由、模板引擎、WSGI），其他功能通过扩展插件实现。Flask 适合快速构建 RESTful API 和小型 Web 应用。

**关键文件/目录**：
- `app.py` / `run.py` - 应用主文件
- `templates/` - 模板目录
- `static/` - 静态资源目录
- `routes.py` / `views.py` - 路由定义

**版本兼容性**：
- 推荐版本：≥ 3.0
- 已知不兼容：Flask 3.0 不支持 Python 3.7 及以下

**特征关键词**：minimal, lightweight, flexible, extensions, wsgi, restful-api

**详细指南**：[flask-guide.md](flask-guide.md)

---

<a id="fastapi"></a>

### ⭐ FastAPI 框架

**概述**：现代、快速的 Python Web 框架，基于标准 Python 类型提示，提供自动 API 文档（Swagger UI）。FastAPI 性能接近 Node.js 和 Go，适合构建高性能 RESTful API。

**关键文件/目录**：
- `fastapi` 依赖 - 框架识别
- `main.py` / `app.py` - 应用主文件
- `routers/` - 路由目录
- `models/` - 数据模型
- `schemas/` - Pydantic 模式
- `dependencies.py` - 依赖注入

**版本兼容性**：
- 推荐版本：≥ 0.100
- 已知不兼容：FastAPI 0.100+ 需要 Python 3.8+

**特征关键词**：async, pydantic, swagger, openapi, high-performance, modern

**详细指南**：[fastapi-guide.md](fastapi-guide.md)

---

<a id="spring-boot"></a>

### ⭐ Spring Boot 框架

**概述**：基于 Spring 框架的快速开发框架，通过约定优于配置和自动配置简化了 Spring 应用的开发。Spring Boot 内置嵌入式服务器，支持快速构建生产级的 Java 应用。

**关键文件/目录**：
- `pom.xml` / `build.gradle` - 包含 `spring-boot-starter` 依赖
- `src/main/java/` - Java 源代码目录
- `src/main/resources/` - 资源文件目录
- `Application.java` - 主启动类
- `@SpringBootApplication` - Spring Boot 注解
- `application.properties` / `application.yml` - 配置文件

**版本兼容性**：
- 推荐版本：≥ 3.0
- 已知不兼容：Spring Boot 3.0 不支持 Java 8 和 11

**特征关键词**：spring-ecosystem, ioc, dependency-injection, aop, auto-configuration, restful-api

**详细指南**：[spring-boot-guide.md](spring-boot-guide.md)

---

<a id="tauri"></a>

### Tauri 框架

**概述**：使用 Rust 作为后端、Web 技术作为前端构建跨平台桌面应用的框架。相比 Electron，它具有更小的体积、更高的安全性和更低的资源占用。

**关键文件/目录**：
- `src-tauri/` - Rust 后端代码目录
- `src-tauri/tauri.conf.json` - Tauri 主配置文件
- `src-tauri/Cargo.toml` - Rust 项目依赖配置
- `src-tauri/src/main.rs` - Rust 入口文件
- `package.json` - 前端依赖配置

**版本兼容性**：
- 推荐版本：≥ 1.5
- 已知不兼容：Tauri v1.x 不兼容 macOS 14+

**特征关键词**：webview, rust, desktop, cross-platform, native, electron-alternative

**详细指南**：[tauri-guide.md](tauri-guide.md)

---

<a id="wails"></a>

### Wails 框架

**概述**：使用 Go 作为后端、Web 技术作为前端构建跨平台桌面应用的框架。相比 Tauri，它对开发者更友好，配置更简单。

**关键文件/目录**：
- `wails.json` - Wails 配置文件
- `go.mod` - Go 模块依赖
- `frontend/` - 前端代码目录
- `main.go` - Go 主入口
- `build/` - 构建输出目录

**版本兼容性**：
- 推荐版本：≥ 2.0
- 已知不兼容：Wails v2 不支持 Windows 7

**特征关键词**：webview, go, desktop, cross-platform, simple-config

**详细指南**：[wails-guide.md](wails-guide.md)

---

<a id="svelte"></a>

### Svelte 框架

**概述**：一个编译型前端框架，它在构建时将组件转换为高效的 JavaScript。相比 React/Vue，它具有更小的包体积和更好的性能。

**关键文件/目录**：
- `svelte.config.js` - Svelte 配置文件
- `*.svelte` - Svelte 组件文件
- `src/routes/` - 路由目录（SvelteKit）
- `vite.config.js` - Vite 构建配置

**版本兼容性**：
- 推荐版本：≥ 4.0
- 已知不兼容：Svelte 3.x 与 4.x 有 breaking changes

**特征关键词**：compile-time, reactive, vite, typescript, no-vdom, lightweight

**详细指南**：[svelte-guide.md](svelte-guide.md)

---

<a id="solidjs"></a>

### SolidJS 框架

**概述**：基于细粒度响应式的响应式 UI 库，语法类似 React JSX，但性能更优。它没有虚拟 DOM，直接响应真实 DOM 的变化。

**关键文件/目录**：
- `solid.config.ts` - Solid 配置文件
- `*.tsx` - Solid TSX 组件文件
- `*.jsx` - Solid JSX 组件文件
- `src/App.tsx` - 根组件

**版本兼容性**：
- 推荐版本：≥ 1.8
- 已知不兼容：某些 React 库可能在 SolidJS 中无法直接使用

**特征关键词**：fine-grained-reactive, jsx, typescript, no-vdom, performance

**详细指南**：[solidjs-guide.md](solidjs-guide.md)

---

<a id="gin"></a>

### Gin 框架

**概述**：高性能 Go Web 框架，类似 Martini 但性能更好。Gin 提供了简单的 API 和中间件机制，适合构建高性能 RESTful API。

**关键文件/目录**：
- `go.mod` - Go 模块依赖
- `gin-gonic/gin` 依赖 - 框架识别
- `main.go` - 应用入口
- `handlers/` - 处理器目录
- `middleware/` - 中间件目录
- `models/` - 数据模型

**版本兼容性**：
- 推荐版本：≥ 1.9
- 已知不兼容：Gin 1.9+ 需要 Go 1.19+

**特征关键词**：http-router, middleware, performance, json-validation, fast

**详细指南**：[gin-guide.md](gin-guide.md)

---

<a id="flutter"></a>

### ⭐ Flutter 框架

**概述**：Google 的跨平台 UI 框架，使用 Dart 语言。Flutter 允许使用单一代码库构建 Web、移动和桌面应用，支持热重载。

**关键文件/目录**：
- `pubspec.yaml` - Flutter 项目配置
- `lib/` - Dart 源代码目录
- `lib/main.dart` - 应用入口
- `lib/widgets/` - 组件目录
- `lib/screens/` - 页面目录

**版本兼容性**：
- 推荐版本：≥ 3.0
- 已知不兼容：Flutter 3.0+ 需要 Dart 2.17+

**特征关键词**：mobile, web, desktop, hot-reload, widgets, dart, cross-platform

**详细指南**：[flutter-guide.md](flutter-guide.md)

---

## 框架对比

### 桌面应用框架对比

| 框架 | 后端语言 | 安装包大小 | 学习曲线 | 适用场景 | 推荐度 |
|------|---------|-----------|----------|----------|--------|
| Electron | Node.js | 大 (~100MB+) | 低 | 跨平台应用、复杂 UI | ⭐⭐⭐⭐⭐ |
| Tauri | Rust | 小 (~5MB) | 高 | 需要小体积和高安全性 | ⭐⭐⭐⭐ |
| Wails | Go | 小 (~10MB) | 中 | 需要 Go 生态 | ⭐⭐⭐ |

### 前端框架对比

| 框架 | 类型 | 包体积 | 学习曲线 | 社区活跃度 | 适用场景 | 推荐度 |
|------|------|--------|----------|------------|----------|--------|
| React | 虚拟 DOM | 中 | 中 | 非常高 | 企业级应用、复杂 SPA | ⭐⭐⭐⭐⭐ |
| Vue | 响应式 | 中 | 低 | 高 | 快速开发、中小型项目 | ⭐⭐⭐⭐⭐ |
| Svelte | 编译型 | 小 | 中 | 中 | 性能敏感的应用 | ⭐⭐⭐⭐ |
| SolidJS | 细粒度响应式 | 小 | 中 | 中 | 性能优化、从 React 迁移 | ⭐⭐⭐ |

### Python Web 框架对比

| 框架 | 类型 | 特点 | 性能 | 适用场景 | 推荐度 |
|------|------|------|------|----------|--------|
| Django | 全栈 | ORM、管理后台、完整性 | 中 | 企业级应用、CMS、快速开发 | ⭐⭐⭐⭐⭐ |
| Flask | 微框架 | 轻量、灵活、扩展性强 | 中 | RESTful API、小型应用 | ⭐⭐⭐⭐⭐ |
| FastAPI | 现代 | 异步、自动文档、高性能 | 高 | 高性能 API、微服务、实时应用 | ⭐⭐⭐⭐⭐ |

### Java Web 框架对比

| 框架 | 特点 | 学习曲线 | 适用场景 | 推荐度 |
|------|------|----------|----------|--------|
| Spring Boot | Spring 生态、自动配置 | 高 | 企业级应用、微服务、金融系统 | ⭐⭐⭐⭐⭐ |

### 选择建议总结

| 项目特征 | 推荐框架 |
|----------|----------|
| 快速开发 MVP | Flask + Vue |
| 企业级应用 | Django + React / Spring Boot + React |
| 高性能 API | FastAPI / Gin |
| 跨平台移动应用 | Flutter |
| 桌面应用 | Electron（生态优先）/ Tauri（性能优先） |
