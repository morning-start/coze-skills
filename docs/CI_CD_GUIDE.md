# CI/CD 使用指南

本文档说明如何使用 Coze Skills 项目的 CI/CD 流程。

## 概述

项目使用 GitHub Actions 实现自动化构建和发布流程，支持：

- 自动打包所有技能为 `.skill` 格式
- 从 CHANGELOG.md 自动生成发布说明
- 通过 Git tag 触发自动发布
- 支持手动触发构建流程

## 前置要求

### 1. 安装 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 验证安装
uv --version
```

### 2. 安装项目依赖

```bash
uv sync
```

## 使用流程

### 方式一：发布新版本（推荐）

#### 步骤 1：更新版本号

使用 `bump-version` 脚本更新版本号：

```bash
# 更新版本号（会自动更新 pyproject.toml 和 CHANGELOG.md）
uv run bump-version 1.1.0

# 更新版本号并创建 Git commit
uv run bump-version 1.1.0 --commit

# 更新版本号、创建 Git commit 和 tag
uv run bump-version 1.1.0 --commit --tag
```

#### 步骤 2：推送 tag 到远程仓库

```bash
git push origin master
git push origin v1.1.0
```

#### 步骤 3：自动触发构建

推送 tag 后，GitHub Actions 会自动：
1. 检出代码
2. 安装 uv 和依赖
3. 构建所有技能包
4. 生成发布说明
5. 创建 GitHub Release
6. 上传构建产物

#### 步骤 4：下载发布包

构建完成后，可以在 GitHub Release 页面下载：
- 所有技能的 `.skill` 包
- 自动生成的发布说明

### 方式二：手动触发构建

#### 步骤 1：手动触发 workflow

1. 访问 GitHub 仓库的 Actions 页面
2. 选择 "Build and Release Skills" workflow
3. 点击 "Run workflow" 按钮
4. 选择分支（默认为 master）
5. 点击 "Run workflow"

#### 步骤 2：查看构建结果

1. 在 Actions 页面查看构建进度
2. 构建完成后，可以在 Artifacts 中下载 `.skill` 包
3. 注意：手动触发不会创建 GitHub Release

## 本地构建

如果需要在本地构建技能包：

```bash
# 构建所有技能（使用当前版本号）
uv run build-skills --version 1.0.0

# 构建指定技能
uv run build-skills --version 1.0.0 --skill recruitment-processor

# 指定输出目录
uv run build-skills --version 1.0.0 --output-dir ./dist
```

构建产物会保存在 `dist/` 目录下。

## 生成发布说明

从 CHANGELOG.md 生成指定版本的发布说明：

```bash
uv run generate-notes --version 1.0.0 --output dist/release_notes.md
```

## 技能包格式

`.skill` 包是一个 ZIP 压缩包，包含技能的所有文件：

```
skill-name/
├── SKILL.md              # 技能主文档
├── assets/               # 模板和资源文件
│   └── templates/
├── references/            # 参考文档
│   └── *.md
├── scripts/              # Python 脚本（如有）
│   └── *.py
└── config.yaml           # 配置文件（如有）
```

## 版本号规范

遵循语义化版本 (Semantic Versioning)：

- **主版本号 (Major)**：不兼容的 API 修改
- **次版本号 (Minor)**：向下兼容的功能新增
- **修订号 (Patch)**：向下兼容的问题修正

示例：
- `1.0.0` - 初始版本
- `1.1.0` - 新增功能
- `1.1.1` - 修复问题
- `2.0.0` - 重大更新

## 工作流说明

### build-and-release.yml

GitHub Actions workflow 文件：`.github/workflows/build-and-release.yml`

#### 触发条件

1. **自动触发**：推送以 `v` 开头的 tag（如 `v1.0.0`）
2. **手动触发**：在 GitHub Actions 页面手动运行

#### 构建步骤

1. **Checkout code**：检出代码
2. **Install uv**：安装 uv 包管理器
3. **Set up Python**：设置 Python 3.12 环境
4. **Install dependencies**：安装 PyYAML 依赖
5. **Get version from tag**：从 tag 提取版本号
6. **Create build directory**：创建构建目录
7. **Build skill packages**：构建所有技能包
8. **Generate release notes**：生成发布说明
9. **Create Release**：创建 GitHub Release（仅 tag 触发时）
10. **Upload artifacts**：上传构建产物

#### 权限要求

workflow 需要 `contents: write` 权限来创建 Release。

## 常见问题

### Q1: 如何回滚到之前的版本？

```bash
# 删除本地 tag
git tag -d v1.1.0

# 删除远程 tag
git push origin :refs/tags/v1.1.0

# 重新创建 tag
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

### Q2: 如何调试构建失败？

1. 在 GitHub Actions 页面查看详细日志
2. 检查脚本输出和错误信息
3. 本地运行脚本复现问题：
   ```bash
   uv run build-skills --version 1.0.0
   ```

### Q3: 如何添加新的技能？

1. 在项目根目录创建新的技能目录
2. 添加 `SKILL.md` 文件
3. 提交代码：
   ```bash
   git add new-skill/
   git commit -m "feat: 添加新技能"
   git push
   ```
4. 发布新版本（参考"方式一"）

### Q4: 如何修改现有技能？

1. 修改技能文件
2. 提交代码：
   ```bash
   git add modified-skill/
   git commit -m "fix: 修复技能问题"
   git push
   ```
3. 发布新版本（参考"方式一"）

## 注意事项

1. **版本号一致性**：确保 `pyproject.toml` 和 `CHANGELOG.md` 中的版本号一致
2. **CHANGELOG 维护**：每次发布前更新 CHANGELOG.md，记录所有变更
3. **tag 命名**：tag 必须以 `v` 开头（如 `v1.0.0`）
4. **测试验证**：发布前在本地测试构建流程
5. **权限配置**：确保 GitHub Repository Settings 中启用了 Actions 权限

## 相关文档

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [语义化版本规范](https://semver.org/lang/zh-CN/)
- [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
