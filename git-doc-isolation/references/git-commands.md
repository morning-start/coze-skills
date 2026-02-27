# Git 命令参考

## 目录
- [孤立分支操作](#孤立分支操作)
- [文档提取命令](#文档提取命令)
- [验证命令](#验证命令)
- [分支管理命令](#分支管理命令)
- [故障排除](#故障排除)

## 概览
本文档提供 Git 文档隔离策略中使用的所有命令的详细说明和示例。

## 孤立分支操作

### git checkout --orphan
创建一个新的孤立分支，该分支没有父提交，与现有分支历史完全分离。

**语法**:
```bash
git checkout --orphan <branch-name>
```

**参数**:
- `branch-name`: 新分支的名称

**示例**:
```bash
# 创建名为 docs 的孤立分支
git checkout --orphan docs

# 创建名为 local-docs 的孤立分支
git checkout --orphan local-docs
```

**注意事项**:
- 创建后工作区会保留当前分支的文件
- 需要手动清理不需要的文件
- 新分支的第一个提交将成为该分支的根提交

### git rm -rf
递归强制删除文件，用于清理孤立分支中的残留文件。

**语法**:
```bash
git rm -rf <path>
```

**示例**:
```bash
# 删除所有文件（用于清理孤立分支）
git rm -rf .

# 删除特定目录
git rm -rf src/
```

## 文档提取命令

### git archive
从指定分支或提交中提取文件，不保留 Git 历史。

**语法**:
```bash
git archive <branch-or-commit> <path> | tar -x -C <destination>
```

**参数**:
- `branch-or-commit`: 分支名或提交哈希
- `path`: 要提取的路径
- `destination`: 提取目标目录

**示例**:
```bash
# 从 docs 分支提取 docs/ 目录到当前目录
git archive docs docs/ | tar -x -C .

# 从 docs 分支提取到特定目录
git archive docs docs/ | tar -x -C /tmp/project-docs

# 提取特定文件
git archive docs docs/api.md | tar -x -C .
```

**特点**:
- 提取的文件不带有 Git 跟踪信息
- 文件被视为 untracked
- 不会污染当前分支的历史

## 验证命令

### git log -- docs/
查看 docs/ 目录的提交历史。

**语法**:
```bash
git log <branch> -- docs/
git log --all --full-history -- docs/
```

**示例**:
```bash
# 查看 main 分支中 docs/ 的历史
git log main -- docs/

# 查看所有分支中 docs/ 的完整历史
git log --all --full-history -- docs/

# 查看特定文件的提交历史
git log main -- docs/api.md
```

**输出解读**:
- 返回空: 该分支从未包含 docs/ 目录 ✅
- 返回提交列表: 该分支包含 docs/ 的历史 ❌

### git merge-base
查找两个分支的共同祖先。

**语法**:
```bash
git merge-base <branch1> <branch2>
```

**示例**:
```bash
# 检查 main 和 docs 是否有共同祖先
git merge-base main docs

# 检查 feature 分支和 main 的关系
git merge-base feature-branch main
```

**输出解读**:
- 返回提交哈希: 两个分支有共同祖先
- 返回空: 两个分支无共同祖先（孤立分支）

### git status
查看工作区状态，验证 docs/ 是否被跟踪。

**语法**:
```bash
git status
```

**关键检查点**:
```bash
# docs/ 不应出现在 "Changes to be committed" 中
# docs/ 不应出现在 "Changes not staged for commit" 中
# docs/ 可以出现在 "Untracked files" 中（这是正常的）
```

## 分支管理命令

### 分支创建与切换

**创建并切换到新分支**:
```bash
git checkout -b <branch-name>
```

**示例**:
```bash
# 从当前分支创建功能分支
git checkout -b feat-user-login

# 从 main 创建功能分支
git checkout main
git checkout -b feat-payment-module
```

### 分支合并

**合并分支到当前分支**:
```bash
git merge <branch-name>
```

**示例**:
```bash
# 合并功能分支到 main
git checkout main
git merge feat-user-login
```

**合并孤立分支的预期行为**:
```bash
# 尝试合并 docs（孤立分支）到 main
git checkout main
git merge docs
# 预期结果：报错 "refusing to merge unrelated histories"
# 这是正常且期望的行为，说明隔离有效
```

### 分支删除

**删除已合并的分支**:
```bash
git branch -d <branch-name>
```

**强制删除未合并的分支**:
```bash
git branch -D <branch-name>
```

**示例**:
```bash
# 删除已合并的功能分支
git branch -d feat-user-login

# 强制删除 docs 分支（谨慎使用）
git branch -D docs
```

## 本地排除配置

### .git/info/exclude
本地排除文件，仅对当前仓库有效，不提交到版本控制。

**语法**:
```bash
echo "<pattern>" >> .git/info/exclude
```

**示例**:
```bash
# 排除 docs/ 目录
echo "docs/" >> .git/info/exclude

# 排除特定文件
echo "local-config.json" >> .git/info/exclude

# 排除所有 .log 文件
echo "*.log" >> .git/info/exclude
```

**与 .gitignore 的区别**:
| 特性 | .git/info/exclude | .gitignore |
|-----|-------------------|-----------|
| 提交到版本控制 | 否 | 是 |
| 影响范围 | 仅本地仓库 | 所有克隆者 |
| 适用场景 | 个人开发文件 | 项目通用排除 |

## 故障排除

### 问题 1: 误将 docs/ 提交到 main

**症状**:
```bash
git log main -- docs/
# 返回提交历史
```

**解决方案**:
```bash
# 方法 1: 如果尚未推送到远程
git checkout main
git reset --hard HEAD~1  # 回退到提交前

# 方法 2: 使用 git filter-repo 彻底清除历史
# 安装 git-filter-repo
pip install git-filter-repo

# 清除 docs/ 目录的历史
git filter-repo --path docs/ --invert-paths
```

### 问题 2: 无法提取文档

**症状**:
```bash
git archive docs docs/ | tar -x -C .
# 报错：docs/ 不存在或无法提取
```

**排查步骤**:
```bash
# 1. 确认 docs 分支存在
git branch -a | grep docs

# 2. 确认 docs 分支包含 docs/ 目录
git ls-tree docs docs/

# 3. 检查 tar 是否可用
tar --version
```

### 问题 3: docs/ 出现在 git status 中

**症状**:
```bash
git status
# docs/ 出现在 "Changes to be committed" 或 "Changes not staged"
```

**解决方案**:
```bash
# 1. 从暂存区移除
git reset docs/

# 2. 添加到本地排除
echo "docs/" >> .git/info/exclude

# 3. 验证
git status
# docs/ 应该只出现在 "Untracked files" 中或完全消失
```

### 问题 4: 合并时提示 "unrelated histories"

**症状**:
```bash
git merge docs
# fatal: refusing to merge unrelated histories
```

**说明**:
这是期望的行为！说明 docs 分支是孤立分支，与 main 无共同历史。

**如果确实需要强制合并（不推荐）**:
```bash
git merge docs --allow-unrelated-histories
# ⚠️ 这将破坏文档隔离策略
```

## 常用命令速查表

| 操作 | 命令 |
|-----|------|
| 创建孤立分支 | `git checkout --orphan docs` |
| 清理孤立分支 | `git rm -rf .` |
| 提取文档 | `git archive docs docs/ \| tar -x -C .` |
| 验证 main 干净性 | `git log main -- docs/` |
| 验证分支独立性 | `git merge-base main docs` |
| 本地排除 docs | `echo "docs/" >> .git/info/exclude` |
| 从暂存区移除 | `git reset docs/` |
