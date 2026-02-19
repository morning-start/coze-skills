# CI/CD 工作流程详解

本文档详细说明 Coze Skills 项目的 CI/CD 工作流程。

## 目录

- [工作流程概览](#工作流程概览)
- [触发条件](#触发条件)
- [执行流程](#执行流程)
- [发布流程](#发布流程)
- [版本管理](#版本管理)
- [故障排查](#故障排查)

---

## 工作流程概览

```
┌─────────────────────────────────────────────────────────────────┐
│                     CI/CD Workflow                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Trigger   │───▶│    Build    │───▶│   Release   │         │
│  │  (Tag/Manual)│    │   All Skills │    │   & Upload  │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│   • Git Tag           • 安装依赖         • 创建 Release        │
│   • Manual            • 构建所有技能     • 上传技能包          │
│                       • 生成说明         • 上传 Artifacts      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**核心特点**：每次发布构建所有技能，简化管理流程。

---

## 触发条件

### 1. Git Tag 触发（自动）

```bash
# 格式: v{主版本}.{次版本}.{修订号}
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

**行为**：
- 自动触发 workflow
- 构建所有技能（使用各自版本号）
- 创建 GitHub Release

### 2. 手动触发（GitHub Actions 页面）

1. 访问仓库的 Actions 页面
2. 选择 "Build and Release Skills" workflow
3. 点击 "Run workflow" 按钮
4. 可选：输入覆盖版本号
5. 点击 "Run workflow"

### 触发条件对比

| 触发方式 | 适用场景 | 构建范围 | 版本来源 |
|---------|---------|---------|---------|
| Git Tag | 正式发布 | 所有技能 | SKILL.md |
| 手动触发 | 测试/调试 | 所有技能 | SKILL.md / 输入参数 |

---

## 执行流程

### Job: build-and-release（构建和发布）

```yaml
执行步骤:
  1. Checkout code：检出代码
  2. Install uv：安装 uv 包管理器
  3. Set up Python：设置 Python 3.12 环境
  4. Create virtual environment：创建虚拟环境
  5. Create build directory：创建构建目录 dist/
  6. Build all skill packages：构建所有技能
  7. List built packages：列出构建产物
  8. Generate release notes：生成发布说明
  9. Create Release：创建 GitHub Release（仅 tag 触发）
  10. Upload artifacts：上传构建产物
```

### 详细步骤说明

#### 1. 环境准备

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 Python 3.12
uv python install 3.12

# 创建虚拟环境
uv venv
```

#### 2. 构建所有技能

```bash
# 使用各自版本号（默认）
uv run python scripts/build_skills.py --all --output-dir dist

# 或使用统一版本号（手动触发时可选）
uv run python scripts/build_skills.py --all --version 2.0.0 --output-dir dist
```

#### 3. 生成发布说明

自动生成的发布说明包含：
- 构建的技能包列表
- 每个包的文件大小
- 指向 CHANGELOG.md 的链接

#### 4. 创建 Release

仅当触发条件是 Git Tag 时：
- 创建 GitHub Release
- 上传所有 `.skill` 文件
- 使用生成的发布说明

---

## 发布流程

### 标准发布流程

```bash
# 1. 确保所有更改已提交
git status

# 2. 提交代码（如有更改）
git add .
git commit -m "feat: 更新技能"
git push origin master

# 3. 创建版本 tag
git tag -a v1.1.0 -m "Release v1.1.0"

# 4. 推送到远程仓库
git push origin v1.1.0
```

### 发布后检查

1. **查看 Actions 页面**
   - 确认 workflow 已触发
   - 检查构建日志

2. **查看 Release 页面**
   - 确认 Release 已创建
   - 检查所有技能包已上传

3. **下载验证**
   - 下载 `.skill` 文件
   - 验证文件完整性

---

## 版本管理

### 版本号格式

遵循语义化版本规范 (Semantic Versioning)：

```
{主版本号}.{次版本号}.{修订号}
```

- **主版本号 (Major)**：不兼容的 API 修改
- **次版本号 (Minor)**：向下兼容的功能新增
- **修订号 (Patch)**：向下兼容的问题修正

### 版本号存储

每个技能的版本号存储在 `SKILL.md` 文件的 YAML frontmatter 中：

```yaml
---
name: skill-name
version: 1.0.0
description: 技能描述
---
```

### 版本更新流程

#### 更新单个技能版本

```bash
# 1. 修改 SKILL.md 中的版本号
vim skill-name/SKILL.md
# 修改 version: 1.1.0

# 2. 提交修改
git add skill-name/SKILL.md
git commit -m "chore: bump skill-name version to 1.1.0"

# 3. 创建项目 tag
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0
```

#### 批量更新版本

```bash
# 1. 修改多个技能的版本号
vim skill1/SKILL.md skill2/SKILL.md

# 2. 提交修改
git add .
git commit -m "chore: bump versions"

# 3. 创建项目 tag
git tag -a v2.0.0 -m "Release v2.0.0"
git push origin v2.0.0
```

---

## 故障排查

### 常见问题

#### Q1: CI/CD workflow 没有触发

**可能原因**：
- Tag 格式不正确（必须以 `v` 开头）
- 没有写入权限
- Actions 被禁用

**解决方案**：
```bash
# 检查 tag 格式
git tag -l

# 确保 tag 以 v 开头
git tag -a v1.0.0 -m "Release 1.0.0"

# 检查 GitHub 设置
# Settings > Actions > General > Workflow permissions
```

#### Q2: 构建失败

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

#### Q3: 版本号不正确

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

#### Q4: 如何添加新的技能？

1. 创建新技能目录和 SKILL.md
2. 提交代码
3. 创建 tag 触发发布

```bash
# 1. 创建技能
cat > new-skill/SKILL.md << 'EOF'
---
name: new-skill
version: 1.0.0
description: 新技能描述
---

# 新技能文档
EOF

# 2. 提交代码
git add new-skill/
git commit -m "feat: 添加新技能"
git push

# 3. 创建 tag
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

### 调试 CI/CD

#### 本地模拟构建

```bash
# 1. 安装依赖
uv sync

# 2. 创建虚拟环境
uv venv

# 3. 构建所有技能
uv run build-skills --all --output-dir dist

# 4. 检查构建产物
ls -lh dist/
```

#### 查看 CI 日志

1. 访问 GitHub 仓库的 Actions 页面
2. 找到 workflow 运行记录
3. 点击失败的步骤查看详细日志

### 紧急处理

#### 重新运行失败的 workflow

1. 访问 Actions 页面
2. 找到失败的 workflow 运行
3. 点击 "Re-run jobs" 按钮

#### 删除错误的 Release

```bash
# 删除本地 tag
git tag -d v1.0.0

# 删除远程 tag
git push origin :refs/tags/v1.0.0

# 在 GitHub 上手动删除 Release
```

---

## 最佳实践

### 1. 版本号管理

- 每个技能维护自己的版本号
- 修改技能时同步更新 version 字段
- 遵循语义化版本规范

### 2. 提交规范

```bash
# 新技能
feat: 添加新技能 skill-name

# 功能更新
feat: 增强 skill-name 技能

# 问题修复
fix: 修复 skill-name 技能的问题

# 版本更新
chore: bump skill-name version to 1.2.0
```

### 3. 发布流程

```bash
# 1. 本地测试
uv run build-skills --all

# 2. 提交代码
git add .
git commit -m "feat: 更新技能"
git push

# 3. 创建 tag
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0

# 4. 等待 CI/CD 完成
# 5. 检查 Release 页面
```

### 4. 监控和维护

- 定期检查 Actions 运行状态
- 关注失败的构建并及时修复
- 保持 SKILL.md 版本号的准确性

---

## 相关文档

- [CI/CD 使用指南](./CI_CD_GUIDE.md) - 基础使用说明
- [CHANGELOG.md](../CHANGELOG.md) - 版本历史记录
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [语义化版本规范](https://semver.org/lang/zh-CN/)
