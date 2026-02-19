# CI/CD 使用指南

本文档说明如何使用 Coze Skills 项目的 CI/CD 流程。

## 概述

项目使用 GitHub Actions 实现自动化构建和发布流程，支持：

- 自动打包所有技能为 `.skill` 格式
- 通过 Git tag 触发自动发布
- 支持手动触发构建流程
- 每次发布构建所有技能（简化管理）

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

### 发布新版本（推荐）

每次发布都会构建所有技能，使用各自 SKILL.md 中的版本号。

#### 步骤 1：更新技能版本号（可选）

如果需要更新技能版本，修改对应技能的 `SKILL.md`：

```bash
# 修改 SKILL.md 中的 version 字段
vim skill-name/SKILL.md
```

#### 步骤 2：提交代码

```bash
git add .
git commit -m "feat: 更新技能"
git push origin master
```

#### 步骤 3：创建 Tag 触发发布

```bash
# 创建版本 tag（使用语义化版本）
git tag -a v1.1.0 -m "Release v1.1.0"

# 推送到远程仓库
git push origin v1.1.0
```

#### 步骤 4：等待自动构建

推送 tag 后，GitHub Actions 会自动：
1. 检出代码
2. 安装 uv 和依赖
3. **构建所有技能**（使用各自版本号）
4. 生成发布说明
5. 创建 GitHub Release
6. 上传构建产物

#### 步骤 5：下载发布包

构建完成后，可以在 GitHub Release 页面下载所有 `.skill` 包。

### 手动触发构建

#### 步骤 1：手动触发 workflow

1. 访问 GitHub 仓库的 Actions 页面
2. 选择 "Build and Release Skills" workflow
3. 点击 "Run workflow" 按钮
4. 可选：输入覆盖版本号（所有技能使用此版本）
5. 点击 "Run workflow"

#### 步骤 2：查看构建结果

1. 在 Actions 页面查看构建进度
2. 构建完成后，可以在 Artifacts 中下载 `.skill` 包

## 本地构建

如果需要在本地构建所有技能：

```bash
# 构建所有技能（使用各自版本号）
uv run build-skills --all

# 构建所有技能（使用统一版本号）
uv run build-skills --all --version 2.0.0

# 构建指定技能
uv run build-skills --skill recruitment-processor

# 指定输出目录
uv run build-skills --all --output-dir ./dist
```

构建产物会保存在 `dist/` 目录下。

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

### 版本号存储

每个技能的版本号存储在 `SKILL.md` 文件的 YAML frontmatter 中：

```yaml
---
name: skill-name
version: 1.0.0
description: 技能描述
---
```

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
4. **Create virtual environment**：创建虚拟环境
5. **Create build directory**：创建构建目录
6. **Build all skill packages**：**构建所有技能**
7. **List built packages**：列出构建产物
8. **Generate release notes**：生成发布说明
9. **Create Release**：创建 GitHub Release（仅 tag 触发时）
10. **Upload artifacts**：上传构建产物

#### 权限要求

workflow 需要 `contents: write` 权限来创建 Release。

## 常见问题

### Q1: CI/CD workflow 没有触发

**可能原因**：
- Tag 格式不正确（必须以 `v` 开头）
- 没有写入权限
- Actions 被禁用

**解决方案**：
```bash
# 检查 tag 格式（必须以 v 开头）
git tag -l

# 确保 tag 格式正确
git tag -a v1.0.0 -m "Release 1.0.0"

# 检查 GitHub 设置
# Settings > Actions > General > Workflow permissions
# 确保选择 "Read and write permissions"
```

### Q2: 构建失败

**可能原因**：
- 依赖安装失败
- 技能目录结构错误
- SKILL.md 格式错误

**解决方案**：
```bash
# 本地测试构建
uv run build-skills --all

# 检查特定技能
uv run build-skills --skill skill-name

# 检查 SKILL.md 格式
cat skill-name/SKILL.md | head -20
```

### Q3: 版本号不正确

**可能原因**：
- SKILL.md 中未定义 version 字段
- YAML frontmatter 格式错误

**解决方案**：
```bash
# 检查 SKILL.md 格式
cat skill-name/SKILL.md

# 确保格式正确
---
name: skill-name
version: 1.0.0
description: 描述
---
```

### Q4: 如何添加新的技能？

1. 在项目根目录创建新的技能目录
2. 添加 `SKILL.md` 文件（包含 version 字段）
3. 提交代码：
   ```bash
   git add new-skill/
   git commit -m "feat: 添加新技能"
   git push
   ```
4. 创建 tag 触发发布：
   ```bash
   git tag -a v1.2.0 -m "Release v1.2.0"
   git push origin v1.2.0
   ```

### Q5: 如何修改现有技能？

1. 修改技能文件
2. 更新 `SKILL.md` 中的版本号（如需要）
3. 提交代码：
   ```bash
   git add skill-name/
   git commit -m "fix: 修复技能问题"
   git push
   ```
4. 创建 tag 触发发布

## 注意事项

1. **版本号维护**：确保 `SKILL.md` 中的版本号正确
2. **Tag 命名**：tag 必须以 `v` 开头（如 `v1.0.0`）
3. **测试验证**：发布前在本地测试构建流程
4. **权限配置**：确保 GitHub Repository Settings 中启用了 Actions 权限

## 相关文档

- [CI/CD 工作流程详解](./CICD_WORKFLOW.md) - 详细的工作流程说明
- [CHANGELOG.md](../CHANGELOG.md) - 版本历史记录
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [语义化版本规范](https://semver.org/lang/zh-CN/)
