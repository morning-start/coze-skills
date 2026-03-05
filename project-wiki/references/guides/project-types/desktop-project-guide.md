# 桌面端项目文档指南

## 概述

本指南适用于桌面端项目（Tauri/Wails/C#/Electron 等），提供跨平台桌面应用开发的文档建议。

### 最小文档集（必备）

1. **README.md** - 项目说明
2. **打包分发说明** - 多平台构建
3. **系统集成说明** - 系统能力

---

## 完整文档集

### 1. 打包与分发

**核心内容**：

```markdown
## 多平台构建

### Windows
- MSI 安装包
- EXE 安装程序
- 构建命令：`npm run build:win`

### macOS
- DMG 镜像
- PKG 安装包
- 构建命令：`npm run build:mac`

### Linux
- AppImage
- DEB/RPM 包
- 构建命令：`npm run build:linux`
```

### 2. 自动更新机制

```markdown
## 自动更新

### Tauri
- 工具：tauri-updater
- 更新服务器配置
- 差分更新

### Electron
- 工具：electron-updater
- autoUpdater API
```

### 3. 系统集成能力

**核心内容**：

```markdown
## 系统集成

### 托盘图标
- 创建系统托盘
- 托盘菜单
- 点击事件

### 系统通知
- 通知 API
- 通知权限

### 文件关联
- 注册文件类型
- 默认打开方式

### 协议注册
- 自定义协议：myapp://
- 深度链接
```

### 4. 安全模型

```markdown
## 安全

### 沙箱限制
- Tauri/Wails: 默认沙箱
- 权限配置

### macOS 权限
- entitlements 配置
- 签名和公证
```

---

## 按框架特定文档

### Tauri

```markdown
## Tauri 特定

### Rust 后端
- invoke 命令
- Command 宏
- 事件系统
```

### Wails

```markdown
## Wails 特定

### Go 后端
- 方法暴露
- 结构体绑定
```

### C# (WinForms/WPF)

```markdown
## C# 特定

### .NET 版本
- 目标框架
- 依赖 NuGet 包

### ClickOnce 部署
- 发布配置
- 自动更新
```

---

## 检查清单

- [ ] 多平台打包说明完整
- [ ] 自动更新机制说明
- [ ] 系统集成能力文档
- [ ] 安全模型说明

---

## 参考资料

- [Tauri 官方文档](https://tauri.app/)
- [Wails 官方文档](https://wails.io/)
- [项目类型总览](README.md)
