# CLI/TUI 工具文档指南

## 概述

本指南适用于命令行工具（CLI）和终端用户界面（TUI）工具，提供命令行工具的文档建议。

### 最小文档集（必备）

1. **README.md** - 项目说明
2. **命令帮助** - 使用说明
3. **配置文件示例** - 配置说明
4. **安装方式** - 多包管理器支持

---

## 完整文档集

### 1. 命令行接口规范

**核心内容**：

```markdown
## 命令结构

### 子命令
```bash
tool init      # 初始化项目
tool run       # 运行任务
tool build     # 构建项目
tool deploy    # 部署
```

### 参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --config | string | 否 | 配置文件路径 |
| --verbose | flag | 否 | 详细输出 |
| --output | string | 否 | 输出目录 |

### 选项
- `-h, --help`: 显示帮助
- `-v, --version`: 显示版本
- `-q, --quiet`: 安静模式
```

### 2. 配置文件格式

**核心内容**：

```markdown
## 配置文件

### YAML 示例
```yaml
name: my-project
version: 1.0.0
settings:
  verbose: true
  output: ./dist
```

### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 项目名称 |
| version | string | 是 | 版本号 |
| settings.verbose | boolean | 否 | 详细模式 |
```

### 3. 输出格式控制

```markdown
## 输出控制

### 支持格式
- 默认：人类可读格式
- `--json`: JSON 格式
- `--quiet`: 仅错误输出

### 颜色控制
- 默认：启用颜色
- `--no-color`: 禁用颜色
```

### 4. TUI 交互说明

**核心内容**：

```markdown
## TUI 交互

### 快捷键
| 快捷键 | 功能 |
|--------|------|
| q | 退出 |
| ↑/↓ | 导航 |
| Enter | 确认 |
| Space | 选择 |

### 导航逻辑
- Tab 切换区域
- 方向键导航
- 快捷键操作
```

### 5. 安装方式

**核心内容**：

```markdown
## 安装方式

### Rust (Cargo)
```bash
cargo install tool-name
```

### Go
```bash
go install github.com/user/tool@latest
```

### Python (pip)
```bash
pip install tool-name
```

### Node.js (npm)
```bash
npm install -g tool-name
```

### Homebrew
```bash
brew install tool-name
```

### Scoop (Windows)
```bash
scoop install tool-name
```
```

### 6. 脚本集成示例

**核心内容**：

```markdown
## 脚本集成

### Shell 脚本
```bash
#!/bin/bash
tool init
tool build
tool deploy
```

### CI/CD (.gitlab-ci.yml)
```yaml
build:
  script:
    - tool build
    - tool test
```
```

---

## 推荐工具

| 工具 | 语言 | 用途 |
|------|------|------|
| **clap** | Rust | CLI 参数解析 |
| **cobra** | Go | CLI 框架 |
| **click** | Python | CLI 框架 |
| **commander** | JS | CLI 框架 |
| **Bubble Tea** | Go | TUI 框架 |
| **tui-rs** | Rust | TUI 框架 |

---

## 检查清单

- [ ] 命令帮助文档完整
- [ ] 配置文件示例清晰
- [ ] 安装方式多样
- [ ] 脚本集成示例实用
- [ ] TUI 快捷键说明

---

## 参考资料

- [CLI 最佳实践](https://clig.dev/)
- [项目类型总览](README.md)