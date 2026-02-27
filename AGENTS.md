# Agent 工作流指南

本文档说明 Coze Skills 项目中 Agent 的工作流程和规范，帮助 Agent 更好地理解项目结构、执行自动化任务。

## 项目概述

Coze Skills 是一个技能管理系统，采用模块化设计，每个技能独立维护，通过 GitHub Actions 实现自动化构建和发布。

### 项目结构

```
coze-skills/
├── skill-name/           # 技能目录
│   ├── SKILL.md         # 技能定义文件（含版本信息）
│   ├── references/      # 技能参考文档
│   └── assets/          # 技能资源文件
├── README.md            # 项目主文档
├── CHANGELOG.md         # 变更日志
└── AGENTS.md           # 本文档
```

## Agent 核心职责

### 1. 技能管理

- **新技能处理**：创建技能目录、初始化 SKILL.md、设置版本号（默认 1.0.0）
- **技能更新**：分析变动、自适应更新版本号、更新相关文档
- **版本控制**：遵循语义化版本规范（Major.Minor.Patch）

### 2. 文档维护

- 自动生成/更新 README.md
- 维护 CHANGELOG.md
- 确保文档一致性

### 3. Git 工作流

- 原子化提交（每个技能独立提交）
- 自动生成提交信息
- 管理版本标签

## 工作流程

### 新技能开发流程

```
1. 创建技能目录结构
   └── skill-name/
       ├── SKILL.md (版本: 1.0.0)
       ├── references/
       └── assets/

2. 编写技能定义 (SKILL.md)
   - 技能名称、版本、描述
   - 使用场景和触发条件
   - 输入输出规范

3. 更新项目文档
   - 更新 README.md 技能列表
   - 更新 CHANGELOG.md

4. 提交代码
   git add skill-name/
   git commit -m "feat: 添加 [技能名称] 技能"
   
5. 推送并发布
   git push origin master
   git tag -a v1.x.x -m "Release v1.x.x"
   git push origin v1.x.x
```

### 技能更新流程

```
1. 分析技能变动
   - 识别变更类型（功能新增/修复/重构）
   - 确定版本号更新策略

2. 更新 SKILL.md
   - 更新版本号
   - 更新描述和文档

3. 更新项目文档
   - 同步更新 README.md
   - 追加 CHANGELOG.md

4. 提交代码
   git add skill-name/
   git commit -m "type: 具体描述"
```

### 版本号更新规则

遵循语义化版本规范：

| 变更类型 | 版本更新 | 示例 | 说明 |
|---------|---------|------|------|
| 不兼容 API 修改 | Major +1 | 1.0.0 → 2.0.0 | 破坏性变更 |
| 向下兼容功能新增 | Minor +1 | 1.0.0 → 1.1.0 | 新功能 |
| 向下兼容问题修复 | Patch +1 | 1.0.0 → 1.0.1 | Bug 修复 |

## 提交信息规范

### 格式

```
<type>: <subject>

<body>

<footer>
```

### 类型说明

| 类型 | 说明 | 使用场景 |
|-----|------|---------|
| `feat` | 新功能 | 添加新技能、新增功能 |
| `fix` | 修复 | 修复 Bug、问题修正 |
| `docs` | 文档 | 仅文档变更 |
| `refactor` | 重构 | 代码重构，无功能变更 |
| `chore` | 构建/工具 | 构建流程、依赖更新 |

### 示例

```bash
# 新技能
feat: 添加 project-wiki 技能

# 功能更新
feat(project-wiki): 支持自动生成架构文档

# Bug 修复
fix(skill-manager): 修复版本号解析错误

# 文档更新
docs: 更新 README 技能列表
```

## 自动化构建

### 本地构建命令

```bash
# 构建所有技能
uv run build-skills --all

# 指定版本号构建
uv run build-skills --all --version 2.0.0

# 指定输出目录
uv run build-skills --all --output-dir ./dist
```

### CI/CD 触发方式

1. **Git Tag 触发**（推荐）
   ```bash
   git tag -a v1.0.0 -m "Release 1.0.0"
   git push origin v1.0.0
   ```

2. **手动触发**
   - 访问 GitHub → Actions → "Build and Release Skills"
   - 点击 "Run workflow"

## Agent 操作检查清单

### 新技能创建

- [ ] 创建技能目录结构
- [ ] 初始化 SKILL.md（版本设为 1.0.0）
- [ ] 编写技能描述和使用说明
- [ ] 更新项目 README.md
- [ ] 更新 CHANGELOG.md
- [ ] 提交代码（独立提交，不推送）

### 技能更新

- [ ] 分析变动类型
- [ ] 自适应更新版本号
- [ ] 更新 SKILL.md 内容
- [ ] 同步更新项目文档
- [ ] 提交代码（独立提交，不推送）

### 发布版本

- [ ] 确认所有技能版本已更新
- [ ] 更新 CHANGELOG.md
- [ ] 提交并推送代码
- [ ] 创建版本标签
- [ ] 推送标签触发发布

## 常见问题

### Q1: 如何确定版本号更新？

根据变更的性质判断：
- 破坏性变更 → Major 版本
- 新功能（兼容）→ Minor 版本
- Bug 修复 → Patch 版本

### Q2: 多个技能同时更新如何处理？

每个技能独立提交，遵循原子操作原则：
```bash
git add skill-a/
git commit -m "feat(skill-a): xxx"

git add skill-b/
git commit -m "fix(skill-b): xxx"
```

### Q3: CI/CD 构建失败？

本地测试构建：
```bash
uv run build-skills --all
```

检查 SKILL.md 格式：
```bash
cat skill-name/SKILL.md | head -20
```

## 参考文档

- [SKILL.md 规范](./project-wiki/references/guides/document/README.md)
- [项目规则](./.trae/rules/project_rules.md)
- [CI/CD 详细指南](./.github/CICD.md)
