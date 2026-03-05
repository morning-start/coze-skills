# 项目类型文档指南

本目录包含针对不同项目类型的文档指南，根据项目类型、技术栈和交付形态提供差异化的文档建议。

## 项目类型分类

| 项目类型 | 技术栈示例 | 交付形态 | 协作模式 |
|---------|-----------|---------|---------|
| [前端项目](frontend-project-guide.md) | Vue, Svelte, SolidJS | Web 应用 | 前端团队协作 |
| [后端项目](backend-project-guide.md) | FastAPI, Gin, Spring Boot | API 服务 | 后端团队协作 |
| [全栈项目](fullstack-project-guide.md) | Next.js, Nuxt, 前后端分离 | 完整应用 | 全栈团队 |
| [移动端项目](mobile-project-guide.md) | Flutter, React Native | 移动应用 | 移动开发团队 |
| [桌面端项目](desktop-project-guide.md) | Tauri, Wails, C#, Electron | 桌面应用 | 桌面开发团队 |
| [CLI/TUI 工具](cli-tui-project-guide.md) | Rust, Go, Python | 命令行工具 | 工具开发团队 |
| [游戏项目](game-project-guide.md) | Godot, Unity | 游戏应用 | 游戏开发团队 |

---

## 最小文档集推荐

根据项目类型，推荐以下最小文档集（必备）：

| 项目类型 | 必备文档（最小集） |
|---------|------------------|
| **前端** | README + 组件 API + 构建部署指南 |
| **后端** | README + OpenAPI + DB 设计 + 部署运维 |
| **全栈** | 前端文档 + 后端文档 + 接口契约 + 联调指南 |
| **移动端** | README + 状态管理说明 + 发布流程 |
| **桌面端** | README + 打包分发 + 系统集成说明 |
| **CLI/TUI** | README + 命令帮助 + 配置文件示例 + 安装方式 |
| **游戏** | README + GDD 摘要 + 场景/脚本结构 + 导出配置 |

---

## 完整文档集推荐

根据项目复杂度和团队规模，可选择以下完整文档集：

### 前端项目（Vue/Svelte/SolidJS）

**核心文档**：
- 架构设计文档（组件分层、状态管理、路由结构）
- 组件 API 文档（Props、Events、Slots）
- 构建与部署说明（Vite/Rollup 配置、环境变量）
- 性能优化指南（懒加载、代码分割、SSR/SSG）
- 国际化策略（如适用）

**推荐工具**：VitePress、Storybook、TypeDoc

---

### 后端项目（FastAPI/Gin/Spring Boot）

**核心文档**：
- API 规范文档（OpenAPI/Swagger、请求/响应结构）
- 领域模型与数据库设计（ER 图、表结构）
- 认证与授权机制（JWT/OAuth2/Session）
- 部署与运维文档（Dockerfile、环境变量、监控）
- 中间件与扩展点说明
- 测试策略（单元测试 vs 集成测试）

**推荐工具**：Swagger UI、Postman Collection、ArchUnit

---

### 全栈项目

**核心文档**：
- 前端和后端所有文档
- 端到端数据流图
- 接口契约文档（前后端字段、格式、错误码约定）
- 联调指南（本地启动、Mock Server）
- 部署拓扑图（CDN、后端服务、DB、缓存）

---

### 移动端项目（Flutter）

**核心文档**：
- 平台适配说明（iOS vs Android 差异）
- 状态管理架构（Provider/Riverpod/Bloc）
- 本地存储策略（SharedPreferences/Hive/SQLite）
- 网络层设计（Dio/http 封装、拦截器）
- 发布流程文档（打包命令、应用签名、提交流程）
- 性能与内存监控（Flutter DevTools）
- 设备兼容性矩阵

---

### 桌面端项目（Tauri/Wails/C#/Python/Go/GPUI）

**核心文档**：
- 打包与分发说明（Windows/macOS/Linux 构建）
- 自动更新机制
- 系统集成能力（托盘、通知、文件关联）
- 安全模型（沙箱限制、权限申请）
- 原生依赖说明（Rust 插件、C++ DLL、Go 编译产物）
- 按框架特定文档

---

### CLI/TUI 工具

**核心文档**：
- 命令行接口规范（子命令、参数/选项）
- 配置文件格式（YAML/JSON/TOML 示例）
- 输出格式控制（--json、--quiet、颜色开关）
- TUI 交互说明（快捷键、导航逻辑）
- 安装方式（Cargo、Go install、pip、npm、Homebrew）
- 脚本集成示例（shell 脚本、CI 调用）

**推荐工具**：clap(Rust)、cobra(Go)、click(Python)、commander(JS)

---

### 游戏项目（Godot）

**核心文档**：
- 游戏设计文档（GDD）摘要（核心玩法、角色、关卡）
- 场景与节点结构说明（场景树组织）
- 信号（Signal）与通信机制
- 资源管理策略（图片/音频/字体加载）
- 导出与发布配置（各平台导出模板、PCK 加密）
- 脚本架构（GDScript 类组织、autoload 单例）

---

## 通用原则

所有项目类型都应包含以下基础文档：

| 文档类型 | 说明 |
|---------|------|
| **README.md** | 项目入口，含简介、快速启动、依赖、贡献指南等 |
| **CHANGELOG.md** | 版本变更记录，便于追踪功能/修复/破坏性变更 |
| **LICENSE.md** | 开源协议或使用条款 |
| **CONTRIBUTING.md** | 贡献规范（代码风格、PR 流程、测试要求等） |
| **配置文件** | .gitignore / .dockerignore 等（虽非文档，但属于"隐式文档"） |

---

## 最佳实践建议

1. **版本化**：所有文档尽量随代码一起提交 Git
2. **自动化生成**：使用 Swagger、TypeDoc、Docusaurus 等工具
3. **PR 检查**：在 PR 模板中加入"是否更新相关文档"检查项
4. **渐进式完善**：从最小文档集开始，根据项目发展逐步完善
5. **定期审查**：定期审查文档的准确性和完整性

---

## 项目类型识别

系统支持基于项目结构自动识别项目类型，识别规则详见 [项目类型识别规则](../knowledge/project-type-recognition.md)。

**识别依据**：
- 基于文件特征（package.json、go.mod、Cargo.toml 等）
- 基于目录结构
- 基于技术栈依赖

---

## 使用说明

1. 确定项目类型
2. 查阅对应的项目类型指南
3. 根据项目复杂度选择最小文档集或完整文档集
4. 使用推荐工具提高文档效率
5. 根据团队需求适当调整

---

## 相关文档

- [文档一致性检查指南](../document/consistency-check-guide.md)
- [基础文档清单](../document/basic-docs-checklist.md)
- [项目类型识别规则](../knowledge/project-type-recognition.md)
