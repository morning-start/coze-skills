---
name: skill-standards
version: v2.0.0
author: skill-lifecycle
description: Skill 和 Workflow 标准化规范，定义格式标准、检验流程和质量要求
tags: [standards, skill-format, workflow-format, naming, validation]
---

# Skill 标准规范

## SKILL.md 格式

### 前言区（必需）

```yaml
---
name: <skill-name>              # 小写+连字符，不含-skill后缀
version: v1.0.0                 # v主.次.补丁
author: <作者>
description: <100-150字符>
tags: [tag1, tag2, tag3]       # 至少3个标签
---
```

### 正文结构（必需章节）

```markdown
## 任务目标
- 本 Skill 用于: <一句话>
- 核心能力: <要点列表>
- 触发条件: <何时使用>

## 操作步骤
1. <步骤1>
2. <步骤2>

## 使用示例
<完整示例>

## 注意事项
<注意点>
```

### 可选章节

```markdown
## 资源索引
- 参考: [references/xxx.md](references/xxx.md)
```

---

## 命名规范

| 类型 | 规则 | 示例 |
|------|------|------|
| 目录名 | 小写字母+连字符 | `data-cleaner` |
| 禁止 | 不以 -skill 结尾 | ❌ `data-cleaner-skill` |

---

## 目录结构

```
<skill-name>/
├── SKILL.md              # 必需
├── references/           # 可选：参考文档
│   └── *.md
├── scripts/              # 可选：可执行代码
└── assets/               # 可选：静态资源
```

**规则**:
- 最多两层目录
- 不包含 README.md、tmp/、__pycache__/
- 空目录不创建

---

## WORKFLOW.md 格式

### 前言区（必需）

```yaml
---
name: <workflow-name>
description: <描述>
target: <目标>
skills_required: [skill-1, skill-2]
---
```

### 正文结构

```markdown
## 目标
<工作流目标>

## 前置条件
- <条件>

## 技能清单
- <skill>: <用途>

## 执行流程
### 步骤 1: <名称>
- **使用技能**: <skill>
- **输入**: <描述>
- **操作**: <说明>
- **输出**: <描述>
- **下一步**: <下一步>

## 异常处理
- <异常>: <处理>

## 输出交付物
- <交付物>
```

---

## 质量检查清单

### 前言区检查

- [ ] name: 小写+连字符，无 -skill 后缀
- [ ] version: v主.次.补丁 格式
- [ ] author: 存在且非空
- [ ] description: 100-150 字符
- [ ] tags: ≥ 3 个标签

### 正文检查

- [ ] 包含必需章节（任务目标、操作步骤、示例）
- [ ] 正文 < 500 行
- [ ] 示例完整可执行
- [ ] 正文内链接为一层引用

### WORKFLOW.md 特定检查

- [ ] 包含目标、前置条件、技能清单
- [ ] 执行流程步骤包含完整信息
- [ ] 包含异常处理

---

## 标准化检验流程

### 步骤 1: 自动化检查

```bash
# 检查前言区
head -10 SKILL.md

# 检查描述长度（应为100-150字符）
grep "description:" SKILL.md | wc -c

# 统计正文行数
tail -n +6 SKILL.md | wc -l

# 检查标签数量
grep "tags:" SKILL.md
```

### 步骤 2: 内容审核

- 阅读全文验证逻辑一致性
- 检查示例可行性
- 确认触发条件合理性

### 步骤 3: 交叉验证

- 对比参考文档链接
- 验证能力描述完整性
- 确认与规范一致性

---

## 版本管理

### 版本号规则

| 变更类型 | 版本递增 | 示例 |
|---------|---------|------|
| 破坏性变更 | major +1 | v1.0.0 → v2.0.0 |
| 新增功能 | minor +1 | v1.0.0 → v1.1.0 |
| 错误修复 | patch +1 | v1.0.0 → v1.0.1 |

### 变更记录

每次版本更新应记录：
- 版本号
- 变更类型
- 变更内容
- 影响范围
