# CI/CD 使用指南

本文档说明 Coze Skills 项目的 CI/CD 工作流程。

## 概述

项目使用 GitHub Actions 实现自动化构建和发布，支持：
- 自动打包所有技能为 `.skill` 格式
- 通过 Git Tag 触发自动发布
- 支持手动触发构建

## 触发方式

### 1. Git Tag 触发（推荐）

```bash
# 创建版本 tag
git tag -a v1.0.0 -m "Release 1.0.0"

# 推送到远程
git push origin v1.0.0
```

触发后自动执行：安装依赖 → 构建所有技能 → 创建 Release → 上传产物

### 2. 手动触发

1. 访问 GitHub 仓库 → Actions 页面
2. 选择 "Build and Release Skills"
3. 点击 "Run workflow"

## 版本管理

每个技能的版本号存储在 `SKILL.md` 的 YAML frontmatter 中：

```yaml
---
name: skill-name
version: 1.0.0
description: 技能描述
---
```

遵循语义化版本规范：
- **主版本号 (Major)**：不兼容的 API 修改
- **次版本号 (Minor)**：向下兼容的功能新增
- **修订号 (Patch)**：向下兼容的问题修正

## 本地构建

```bash
# 构建所有技能
uv run build-skills --all

# 指定版本号
uv run build-skills --all --version 2.0.0

# 指定输出目录
uv run build-skills --all --output-dir ./dist
```

## 发布流程

```bash
# 1. 更新技能版本号（如需要）
vim skill-name/SKILL.md

# 2. 提交代码
git add .
git commit -m "feat: 更新技能"
git push origin master

# 3. 创建 Tag 触发发布
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

## 常见问题

### Q1: CI/CD 没有触发

- 检查 Tag 格式是否正确（必须以 `v` 开头）
- 确认 GitHub Settings → Actions → Workflow permissions 已启用

### Q2: 构建失败

```bash
# 本地测试
uv run build-skills --all

# 检查 SKILL.md 格式
cat skill-name/SKILL.md | head -20
```

### Q3: 如何添加新技能

1. 创建技能目录和 `SKILL.md`
2. 提交代码
3. 创建 Tag 触发发布

## 工作流配置

工作流文件位于：[`.github/workflows/build-and-release.yml`](./workflows/build-and-release.yml)
