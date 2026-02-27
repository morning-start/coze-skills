---
name: git-doc-isolation
description: Git 文档隔离管理技能，使用孤立分支策略确保 docs/ 目录绝不进入 main 分支历史，支持本地开发文档的安全管理和临时使用
metadata:
  capabilities: [Git分支管理, 文档隔离, 孤立分支创建, 文档安全策略, 分支合并防护, 任务处理工作流]
  version: "1.1.0"
  tags: [git, 文档管理, 分支策略, 开发工作流, 任务处理]
  use_cases:
    - 本地开发文档管理
    - 防止文档污染主干分支
    - 多分支文档共享
    - 安全文档工作流
    - 基于文档的任务处理
  preconditions:
    - Git 仓库已初始化
    - 具有分支管理权限
    - Git 版本 >= 2.0
  posteffects:
    - 创建独立的 docs 孤立分支
    - main 分支历史保持干净（无 docs/）
    - task 分支可获取指定文档执行任务
    - 任务文档更新与代码提交分离
  cost_estimate:
    time: "5-10分钟"
    complexity: "中等"
  reliability_score: 0.98
  author: "skill-manager"
  created_at: "2026-02-27"
  updated_at: "2026-02-27"
  dependencies:
    system:
      - git >= 2.0
      - tar (Unix) 或 tar.exe (Windows)
    env_vars:
      - name: "GIT_AUTHOR_NAME"
        required: false
      - name: "GIT_AUTHOR_EMAIL"
        required: false
  error_codes:
    - code: "BRANCH_EXISTS"
      message: "docs 分支已存在"
      severity: "warning"
      fallback_action: "切换到现有 docs 分支或删除后重建"
    - code: "UNCLEAN_WORKING_DIR"
      message: "工作区有未提交的更改"
      severity: "error"
      fallback_action: "提交或暂存当前更改后再继续"
    - code: "DOCS_IN_HISTORY"
      message: "main 分支历史中发现 docs/ 目录"
      severity: "error"
      fallback_action: "使用 git filter-repo 清除历史，或创建新的干净仓库"
    - code: "MERGE_REJECTED"
      message: "无法合并孤立分支（无共同祖先）"
      severity: "info"
      fallback_action: "这是预期行为，说明隔离有效。如需强制合并，使用 --allow-unrelated-histories（不推荐）"
    - code: "TAR_NOT_FOUND"
      message: "未找到 tar 命令"
      severity: "error"
      fallback_action: "Windows 用户安装 Git Bash 或 WSL，macOS/Linux 通常已预装"
---

# Git 文档隔离管理

## 快速开始

### 5 分钟上手
```bash
# 1. 验证 main 分支干净
git log main -- docs/  # 应返回空

# 2. 创建孤立 docs 分支
git checkout --orphan docs
git rm -rf .
mkdir docs && echo "# Dev Guide" > docs/guide.md
git add docs/ && git commit -m "chore(docs): init"

# 3. 回到 main，开始使用
git checkout main
```

### 日常使用（任务处理流程）

#### 标准任务处理流程（8步法）

```bash
# 步骤 1: 切换到 main 分支
git checkout main

# 步骤 2: 基于 main 创建 task- 分支
git checkout -b task-feature-name

# 步骤 3: 从 docs 分支 show 指定文档
git show docs:docs/task-instruction.md > task-instruction.md

# 步骤 4: 根据文档内容和指令执行任务
# ... 执行任务 ...

# 步骤 5: 对修改的任务逐步提交 git（除了步骤 3 指定的文档）
git add src/ tests/  # 添加修改的文件
git commit -m "feat: 完成任务 xxx"

# 步骤 6: 删除指定文档
rm task-instruction.md

# 步骤 7: 切换到 docs 分支，更新文档，并提交 git
git checkout docs
vim docs/task-instruction.md  # 更新文档
git add docs/
git commit -m "docs: 更新任务文档"

# 步骤 8: 切换 main 分支，合并 task
git checkout main
git merge task-feature-name
git branch -d task-feature-name
```

## 任务目标
- 本 Skill 用于: 管理本地开发文档，确保 docs/ 目录绝不进入 main 分支的 Git 历史
- 能力包含: 
  - 创建孤立文档分支
  - 安全提取文档
  - 分支合并防护
  - 文档隔离验证
  - **任务处理工作流（8步法）**: 基于 docs 分支中的指定文档执行任务的完整流程
- 触发条件: 
  - 当用户需要在本地维护开发文档但不想将其提交到主干分支时使用
  - 当用户需要基于 docs 分支中的任务文档执行开发任务时使用

## 核心原则

### 绝对隔离原则
- **main 分支历史干净**: docs/ 目录从未出现在 main 分支的任何提交中
- **docs 分支完全独立**: 使用 orphan 分支创建，与 main 无共同历史
- **无法静默合并**: 由于无共同祖先，误操作 merge 会立即报错
- **本地只读使用**: 功能分支通过 git archive 临时获取文档，不跟踪修改

## 操作步骤

### 步骤 1: 创建孤立文档分支（首次设置）

**前置检查**:
```bash
# 确认 main 分支干净
git checkout main
git status  # 应无未提交更改

# 验证 main 从未包含 docs/
git log main -- docs/
# 若返回空，说明干净 ✅
```

**创建孤立分支**:
```bash
# 创建全新的、无历史的 docs 分支
git checkout --orphan docs

# 清空工作区（orphan 分支会保留当前文件）
git rm -rf .

# 创建 docs 目录和文档
mkdir docs
echo "# Development Guide" > docs/dev-guide.md
# 添加更多文档...

# 提交文档（docs 分支的第一个提交，与 main 无任何关联）
git add docs/
git commit -m "chore(docs): initial local documentation"

# 回到 main，确认 docs/ 不存在
git checkout main
ls -la  # 应看不到 docs/
```

### 步骤 2: 任务处理流程（8步法）

**完整任务处理工作流**:

```bash
# ========== 阶段 1: 准备 ==========

# 1. 切换到 main 分支
git checkout main

# 2. 基于 main 创建 task- 分支
git checkout -b task-feature-name


# ========== 阶段 2: 执行 ==========

# 3. 从 docs 分支 show 指定文档
git show docs:docs/task-instruction.md > task-instruction.md

# 4. 根据指定内容和指令执行任务
# ... 读取 task-instruction.md，按照指令执行任务 ...


# ========== 阶段 3: 提交代码 ==========

# 5. 对修改的任务逐步提交 git（除了步骤 3 指定的文档）
git add src/ tests/ scripts/  # 添加实际修改的文件
git commit -m "feat: 完成任务 xxx"


# ========== 阶段 4: 清理 ==========

# 6. 删除指定文档
rm task-instruction.md


# ========== 阶段 5: 更新文档 ==========

# 7. 切换到 docs 分支，更新文档，并提交 git
git checkout docs
vim docs/task-instruction.md  # 根据执行情况更新文档
git add docs/
git commit -m "docs: 更新任务文档"


# ========== 阶段 6: 合并 ==========

# 8. 切换 main 分支，合并 task
git checkout main
git merge task-feature-name
git branch -d task-feature-name
```

**流程说明**:
- **步骤 1-2**: 准备工作，确保从干净的 main 分支创建 task 分支
- **步骤 3**: 精准获取单个文档，避免提取整个 docs 目录
- **步骤 4**: 根据文档指令执行任务
- **步骤 5**: 只提交代码修改，任务文档不进入代码历史
- **步骤 6**: 清理临时文档
- **步骤 7**: 在 docs 分支更新任务文档，记录执行结果
- **步骤 8**: 合并代码到 main，完成整个流程

### 步骤 3: 验证隔离状态

**检查 main 分支干净性**:
```bash
# 检查 main 是否 ever 包含 docs/
git log --all --full-history -- docs/

# 更严格地，只查 main：
git log main -- docs/

# 如果返回空，说明 main 完全干净 ✅
```

**验证 docs 分支独立性**:
```bash
# 确认 docs 与 main 无共同祖先
git merge-base main docs
# 应返回空（无共同祖先）
```

## 资源索引
- Git 命令参考: 见 [references/git-commands.md](references/git-commands.md)(何时读取: 需要具体命令语法时)
- 分支策略详解: 见 [references/branch-strategy.md](references/branch-strategy.md)(何时读取: 需要理解策略原理时)

## 安全机制说明

### 为什么这样绝对安全？

| 风险场景 | 如何被规避 |
|---------|-----------|
| docs/ 被提交到 main | main 从未有 docs/，且 .git/info/exclude 阻止 git add . |
| docs/ 通过 merge 进入 main | docs 是 orphan 分支，与 main 无共同祖先，merge 会报错 |
| 智能体误改文档导致丢失 | 原始文档始终在独立的 docs 分支中，本地副本可随意丢弃 |
| 历史污染 | main 的整个提交历史都不含 docs/，满足"不能保存"的要求 |

### 分支结构可视化

```
main       → [A] — [B] — [C]          (无 docs/)
               ↑
               └─ 所有 feat-* 从此分出，临时拷贝 docs/，用完即删

docs       → [D]                      (孤立分支，只有 docs/，与 A/B/C 无关联)
```

## 注意事项
- **不要在 main 上创建过 docs/ 再删除**: 那仍会留在历史中
- **如果项目早期已在 main 提交过 docs/**: 建议用 git filter-repo 彻底清除历史
- **对于新项目**: 用 --orphan 创建 docs 分支是最简单、最安全的起点
- **定期验证**: 使用验证命令定期检查 main 分支的干净性

## 使用示例

### 示例 1: 新项目初始化
```bash
# 新项目，main 分支已存在
git checkout main

# 创建孤立 docs 分支
git checkout --orphan docs
git rm -rf .
mkdir docs
echo "# API Documentation" > docs/api.md
git add docs/
git commit -m "chore(docs): add API documentation"

# 回到 main
git checkout main
```

### 示例 2: 任务处理流程（8步法）
```bash
# ========== 阶段 1: 准备 ==========

# 1. 切换到 main 分支
git checkout main

# 2. 基于 main 创建 task- 分支
git checkout -b task-user-auth


# ========== 阶段 2: 执行 ==========

# 3. 从 docs 分支 show 指定文档
git show docs:docs/auth-requirements.md > auth-requirements.md

# 4. 根据指定内容和指令执行任务
# ... 读取 auth-requirements.md，实现用户认证功能 ...


# ========== 阶段 3: 提交代码 ==========

# 5. 对修改的任务逐步提交 git（除了步骤 3 指定的文档）
git add src/auth/
git commit -m "feat: 实现用户登录功能"

git add src/middleware/
git commit -m "feat: 添加认证中间件"


# ========== 阶段 4: 清理 ==========

# 6. 删除指定文档
rm auth-requirements.md


# ========== 阶段 5: 更新文档 ==========

# 7. 切换到 docs 分支，更新文档，并提交 git
git checkout docs
vim docs/auth-requirements.md  # 标记已完成的需求
git add docs/
git commit -m "docs: 更新认证需求文档，标记已完成项"


# ========== 阶段 6: 合并 ==========

# 8. 切换 main 分支，合并 task
git checkout main
git merge task-user-auth
git branch -d task-user-auth
```

### 示例 3: 更新文档
```bash
# 切换到 docs 分支更新文档
git checkout docs
vim docs/api.md  # 修改文档
git add docs/
git commit -m "docs: update API documentation"

# 回到 main
git checkout main
```
