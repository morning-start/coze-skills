---
name: git-doc-isolation
description: Git 文档隔离管理技能，使用孤立分支策略确保 docs/ 目录绝不进入 main 分支历史，支持本地开发文档的安全管理和临时使用
metadata:
  capabilities: [Git分支管理, 文档隔离, 孤立分支创建, 文档安全策略, 分支合并防护]
  version: "1.0.0"
  tags: [git, 文档管理, 分支策略, 开发工作流]
  use_cases:
    - 本地开发文档管理
    - 防止文档污染主干分支
    - 多分支文档共享
    - 安全文档工作流
  preconditions:
    - Git 仓库已初始化
    - 具有分支管理权限
    - Git 版本 >= 2.0
  posteffects:
    - 创建独立的 docs 孤立分支
    - main 分支历史保持干净（无 docs/）
    - 功能分支可临时获取文档用于开发
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

### 日常使用（每次开发）
```bash
# 获取文档进行开发
git checkout -b feat-xxx
git archive docs docs/ | tar -x -C .
echo "docs/" >> .git/info/exclude

# 开发完成后
git add src/ && git commit -m "feat: xxx"
git checkout main && git merge feat-xxx
rm -rf docs/
```

## 任务目标
- 本 Skill 用于: 管理本地开发文档，确保 docs/ 目录绝不进入 main 分支的 Git 历史
- 能力包含: 创建孤立文档分支、安全提取文档、分支合并防护、文档隔离验证
- 触发条件: 当用户需要在本地维护开发文档但不想将其提交到主干分支时使用

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

### 步骤 2: 在功能分支中安全使用文档

**创建功能分支并提取文档**:
```bash
# 1. 从 main 创建功能分支
git checkout main
git checkout -b feat-user-login

# 2. 从 docs 分支提取文档（只读，不跟踪）
git archive docs docs/ | tar -x -C .

# 现在 ./docs/ 存在，但 Git 视为 untracked 文件
```

**配置防护（关键步骤）**:
```bash
# 3. 将 docs/ 加入本地排除列表，防止误提交
echo "docs/" >> .git/info/exclude

# 验证：docs/ 不应出现在 git status 的待提交列表中
git status
```

**开发完成后提交**:
```bash
# 4. 明确添加代码目录（避免 git add . 风险）
git add src/ tests/ scripts/  # 根据项目结构调整

# 或：如果用了 git add .，则移除 docs/
git add .
git reset docs/ 2>/dev/null || true

# 5. 提交代码（docs/ 不会被包含）
git commit -m "feat: implement user login"

# 6. 合并回 main
git checkout main
git merge feat-user-login

# 7. 清理
git branch -d feat-user-login
rm -rf docs/   # 删除临时拷贝
```

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

### 示例 2: 日常开发流程
```bash
# 开始新功能
git checkout -b feat-payment-module

# 获取最新文档
git archive docs docs/ | tar -x -C .
echo "docs/" >> .git/info/exclude

# 开发...
# 参考 docs/api.md 进行开发

# 提交（docs/ 自动被排除）
git add src/
git commit -m "feat: implement payment module"

# 清理
git checkout main
git merge feat-payment-module
git branch -d feat-payment-module
rm -rf docs/
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
