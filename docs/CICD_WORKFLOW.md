# CI/CD 工作流程详解

本文档详细说明 Coze Skills 项目的 CI/CD 工作流程，包括触发条件、执行流程、发布场景和故障排查。

## 目录

- [工作流程概览](#工作流程概览)
- [触发条件](#触发条件)
- [执行流程](#执行流程)
- [发布场景](#发布场景)
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
│  │   Trigger   │───▶│   Detect    │───▶│    Build    │         │
│  │  (多种方式)  │    │   Changes   │    │   & Release │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│   • Git Tag         • 检测新增技能      • 安装依赖              │
│   • Manual          • 检测修改技能      • 构建技能包            │
│   • Auto-detect     • 判断发布类型      • 生成发布说明          │
│                                          • 创建 Release         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 触发条件

### 1. Git Tag 触发（自动）

#### 统一版本 Tag
```bash
# 格式: v{主版本}.{次版本}.{修订号}
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

**行为**：
- 检测自上次 tag 以来的所有变更
- 自动识别新增和修改的技能
- 仅构建有变更的技能（使用各自版本号）

#### 独立版本 Tag
```bash
# 格式: {技能名}-v{版本号}
git tag -a recruitment-processor-v1.2.0 -m "Update recruitment-processor"
git push origin recruitment-processor-v1.2.0
```

**行为**：
- 仅构建指定的技能
- 使用 SKILL.md 中的版本号或 tag 中的版本号

### 2. 手动触发（GitHub Actions 页面）

1. 访问仓库的 Actions 页面
2. 选择 "Build and Release Skills" workflow
3. 点击 "Run workflow" 按钮
4. 选择参数：
   - **Release type**: `changed` / `all` / `specific`
   - **Skill name**: （仅 specific 类型需要）
   - **Version**: （可选，覆盖默认版本）

### 3. 触发条件对比

| 触发方式 | 适用场景 | 构建范围 | 版本来源 |
|---------|---------|---------|---------|
| 统一版本 Tag | 批量发布 | 所有变更的技能 | SKILL.md |
| 独立版本 Tag | 单个技能更新 | 指定技能 | SKILL.md / Tag |
| 手动触发 | 灵活控制 | 根据选择 | SKILL.md / 输入参数 |

---

## 执行流程

### Job 1: detect-changes（变更检测）

```yaml
检测步骤:
  1. 检出代码 (fetch-depth: 0，获取完整历史)
  2. 安装 uv 和 Python 3.12
  3. 创建虚拟环境
  4. 执行 detect_skill_changes.py 脚本
  5. 输出变更技能列表
```

**输出变量**：
- `changed_skills`: 变更的技能列表（逗号分隔）
- `has_changes`: 是否有变更（true/false）
- `release_type`: 发布类型（changed/all/specific）

### Job 2: build-and-release（构建和发布）

**条件**: `needs.detect-changes.outputs.has_changes == 'true'`

```yaml
构建步骤:
  1. 检出代码
  2. 安装 uv 和 Python 3.12
  3. 创建虚拟环境
  4. 创建构建目录 (dist/)
  5. 根据发布类型构建技能包:
     - all: 构建所有技能
     - changed/specific: 构建指定技能
  6. 列出构建产物
  7. 生成发布说明
  8. 创建 GitHub Release（仅 tag 触发）
  9. 上传构建产物到 Artifacts
```

### Job 3: no-changes（无变更处理）

**条件**: `needs.detect-changes.outputs.has_changes == 'false'`

```yaml
执行步骤:
  1. 输出提示信息
  2. 跳过构建流程
```

---

## 发布场景

### 场景 1: 新技能添加

**场景描述**：向仓库添加全新的技能

**操作流程**：

```bash
# 1. 创建新技能目录和文件
mkdir new-skill
cat > new-skill/SKILL.md << 'EOF'
---
name: new-skill
version: 1.0.0
description: 新技能描述
---

# 新技能文档
...
EOF

# 2. 提交代码
git add new-skill/
git commit -m "feat: 添加新技能 new-skill"
git push origin master

# 3. 创建 tag 触发发布
git tag -a v1.1.0 -m "Release 1.1.0 - 添加新技能"
git push origin v1.1.0
```

**CI/CD 行为**：
1. 检测到新增技能 `new-skill`
2. 读取 SKILL.md 中的版本号 (1.0.0)
3. 构建 `new-skill-1.0.0.skill`
4. 创建 Release，包含新技能包

### 场景 2: 单个技能更新

**场景描述**：修改现有技能的代码或文档

**操作流程（方式 1 - 独立版本 Tag）**：

```bash
# 1. 修改技能文件
vim recruitment-processor/SKILL.md
# 更新 version: 1.1.0

# 2. 提交代码
git add recruitment-processor/
git commit -m "feat: 增强 recruitment-processor 技能"
git push origin master

# 3. 创建独立版本 tag
git tag -a recruitment-processor-v1.1.0 -m "Update recruitment-processor"
git push origin recruitment-processor-v1.1.0
```

**操作流程（方式 2 - 手动触发）**：

1. 修改并提交代码
2. 访问 GitHub Actions 页面
3. 选择 "Build and Release Skills"
4. 点击 "Run workflow"
5. 选择参数：
   - Release type: `specific`
   - Skill name: `recruitment-processor`
   - Version: （可选）

**CI/CD 行为**：
1. 识别到特定技能需要更新
2. 构建 `recruitment-processor-1.1.0.skill`
3. 创建 Release 或上传 Artifacts

### 场景 3: 多个技能更新

**场景描述**：同时修改多个技能

**操作流程**：

```bash
# 1. 修改多个技能
vim skill1/SKILL.md
vim skill2/scripts/helper.py

# 2. 提交代码
git add skill1/ skill2/
git commit -m "fix: 修复多个技能的问题"
git push origin master

# 3. 创建 tag 触发批量发布
git tag -a v1.2.1 -m "Release 1.2.1 - 修复多个技能"
git push origin v1.2.1
```

**CI/CD 行为**：
1. 检测所有变更的技能（skill1, skill2）
2. 分别读取各自的版本号
3. 构建多个技能包：
   - `skill1-{version}.skill`
   - `skill2-{version}.skill`
4. 创建 Release，包含所有更新的技能包

### 场景 4: 所有技能重新发布

**场景描述**：需要重新构建所有技能（如修改了构建脚本）

**操作流程**：

```bash
# 方式 1: 手动触发
# 在 GitHub Actions 页面选择 "all" 类型

# 方式 2: 修改所有技能的版本号后统一发布
# （不推荐，除非有特殊需求）
```

**CI/CD 行为**：
1. 构建所有技能（忽略变更检测）
2. 每个技能使用各自的版本号
3. 创建 Release 包含所有技能包

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

### 版本号存储位置

每个技能的版本号存储在 `SKILL.md` 文件的 YAML frontmatter 中：

```yaml
---
name: skill-name
version: 1.2.3
description: 技能描述
---
```

### 版本更新策略

#### 独立版本（推荐）

```bash
# 1. 更新 SKILL.md 中的版本号
vim skill-name/SKILL.md
# 修改 version: 1.2.3

# 2. 提交修改
git add skill-name/SKILL.md
git commit -m "chore: bump skill-name version to 1.2.3"

# 3. 创建独立版本 tag
git tag -a skill-name-v1.2.3 -m "Release skill-name v1.2.3"
git push origin skill-name-v1.2.3
```

#### 统一版本（项目级别）

```bash
# 1. 使用 bump-version 脚本
uv run bump-version 2.0.0 --commit

# 2. 创建项目级别 tag
git tag -a v2.0.0 -m "Release v2.0.0"
git push origin v2.0.0
```

### 版本检测命令

```bash
# 列出所有技能及其版本
uv run build-skills --list

# 检测自上次 tag 以来的变更
uv run detect-changes --all

# 检测新增技能
uv run detect-changes --new-only

# 检测修改的技能
uv run detect-changes --modified-only

# JSON 格式输出（用于脚本处理）
uv run detect-changes --all --json
```

---

## 故障排查

### 常见问题

#### Q1: CI/CD  workflow 没有触发

**可能原因**：
- Tag 格式不正确
- 没有写入权限
- Actions 被禁用

**解决方案**：
```bash
# 检查 tag 格式
git tag -l

# 确保 tag 以 v 开头或符合 {skill}-v{version} 格式

# 检查 GitHub 设置
# Settings > Actions > General > Workflow permissions
# 确保选择 "Read and write permissions"
```

#### Q2: 变更检测失败

**可能原因**：
- 没有历史 tag
- Git 历史不完整

**解决方案**：
```bash
# 检查是否有 tag
git tag -l

# 如果没有，创建初始 tag
git tag -a v0.0.0 -m "Initial release"
git push origin v0.0.0

# 确保 CI 检出完整历史
# actions/checkout@v4 with fetch-depth: 0
```

#### Q3: 构建失败

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

#### Q4: 版本号不正确

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

### 调试 CI/CD

#### 本地模拟 CI 环境

```bash
# 1. 安装依赖
uv sync

# 2. 创建虚拟环境
uv venv

# 3. 检测变更
uv run detect-changes --all

# 4. 构建技能
uv run build-skills --all --output-dir dist

# 5. 检查构建产物
ls -lh dist/
```

#### 查看 CI 日志

1. 访问 GitHub 仓库的 Actions 页面
2. 找到失败的 workflow 运行
3. 点击失败的 job 查看详细日志
4. 展开失败的步骤查看错误信息

### 紧急处理

#### 重新运行失败的 workflow

1. 访问 Actions 页面
2. 找到失败的 workflow 运行
3. 点击 "Re-run jobs" 按钮
4. 选择 "Re-run failed jobs" 或 "Re-run all jobs"

#### 跳过 CI 检测强制构建

```bash
# 手动触发 workflow
# 在 GitHub Actions 页面选择 "all" 类型
# 这会构建所有技能，忽略变更检测
```

#### 删除错误的 Release

```bash
# 删除本地 tag
git tag -d v1.0.0

# 删除远程 tag
git push origin :refs/tags/v1.0.0

# 在 GitHub 上手动删除 Release
# 访问 Releases 页面，点击删除按钮
```

---

## 最佳实践

### 1. 版本号管理

- **独立版本**：每个技能维护自己的版本号
- **更新 SKILL.md**：修改技能时同步更新 version 字段
- **遵循语义化版本**：明确区分 major/minor/patch 更新

### 2. 提交规范

```bash
# 新技能
feat: 添加新技能 skill-name

# 功能更新
feat: 增强 skill-name 技能，添加 xxx 功能

# 问题修复
fix: 修复 skill-name 技能的 xxx 问题

# 版本更新
chore: bump skill-name version to 1.2.0
```

### 3. 发布流程

```bash
# 1. 本地测试
uv run build-skills --skill skill-name

# 2. 提交代码
git add .
git commit -m "feat: 更新技能"
git push

# 3. 创建 tag（独立版本）
git tag -a skill-name-v1.2.0 -m "Release skill-name v1.2.0"
git push origin skill-name-v1.2.0

# 4. 等待 CI/CD 完成
# 5. 检查 Release 页面
```

### 4. 监控和维护

- 定期检查 Actions 运行状态
- 关注失败的构建并及时修复
- 保持 SKILL.md 版本号的准确性
- 及时清理过期的 Artifacts

---

## 相关文档

- [CI/CD 使用指南](./CI_CD_GUIDE.md) - 基础使用说明
- [CHANGELOG.md](../CHANGELOG.md) - 版本历史记录
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [语义化版本规范](https://semver.org/lang/zh-CN/)
