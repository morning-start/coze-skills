# Skill 标准规范

## 目录
- [命名规范](#命名规范)
- [目录结构](#目录结构)
- [SKILL.md 格式](#skillmd-格式)
- [参考文档规范](#参考文档规范)
- [资产管理](#资产管理)

## 概览
本规范定义了 Skill 的标准化格式和组织结构，确保所有技能具有一致的质量和可维护性。

## 命名规范

### 目录名规范
- **格式**: 小写字母 + 连字符（如 `data-processor`, `pdf-parser`）
- **禁止**: 使用 `-skill` 后缀（目录名不应与打包文件混淆）
- **示例**:
  - ✅ `exam-grading`
  - ✅ `text-analyzer`
  - ❌ `exam-grading-skill`

### 打包文件名
- **格式**: `<skill-name>.skill`（目录名 + `.skill` 扩展名）
- **示例**: `exam-grading.skill`

## 目录结构

### 固定结构
```
<skill-name>/
├── SKILL.md           # 必需：入口与指南
├── references/        # 可选：参考文档
└── assets/            # 可选：静态资源
```

### 结构规则
1. **必需文件**: SKILL.md 必须存在
2. **可选目录**: references/、assets/ 按需创建，不创建空目录
3. **禁止内容**: 不包含 README.md、tmp/、.cache/、__pycache__/ 等临时文件
4. **层级限制**: 最多两层（固定结构的位置）

## SKILL.md 格式

### 前言区（YAML）

#### 必需字段
```yaml
---
name: <skill-name>
description: <单行描述，100-150字符>
---
```

#### 可选字段
```yaml
dependency:
  python:
    - package==version
    - another-package>=1.2.0
  system:
    - mkdir -p some-dir
metadata:
  capabilities: [能力列表]
  version: "1.0.0"
  changelog: [变更列表]
```

#### 字段说明
- **name**: 技能名称，必须使用英文小写字母和连字符，不以 `-skill` 结尾
- **description**: 单行文本，包含核心价值与触发场景，长度 100-150 字符
- **dependency.python**: Python 依赖包，遵循 requirements.txt 格式
- **dependency.system**: 系统级命令，用于创建非标准文件/文件夹
- **metadata.capabilities**: 技能能力列表
- **metadata.version**: 版本号（语义化版本格式）
- **metadata.changelog**: 版本变更记录

### 正文（Markdown）

#### 标准章节结构
```markdown
# <技能标题>

## 任务目标
- 本 Skill 用于: <一句话场景>
- 能力包含: <核心能力要点>
- 触发条件: <典型用户表达或上下文信号>

## 前置准备
- 依赖说明: 所需的依赖包及版本
  ```
  dependency1==1.0.0
  dependency2==2.0.0
  ```
- 非标准文件/文件夹准备: 前置创建说明
  ```bash
  mkdir -p extra-files/input
  ```

## 操作步骤
- 标准流程:
  1. <步骤 1: 输入/准备>
  2. <步骤 2: 执行/处理>
  3. <步骤 3: 输出/校验>
- 可选分支:
  - 当 <条件 A>: 执行 <分支 A>
  - 当 <条件 B>: 执行 <分支 B>

## 资源索引
- 领域参考: 见 [references/<topic>.md](references/<topic>.md)(何时读取: <触发/场景>)
- 输出资产: 见 [assets/<template-dir>/](assets/<template-dir>/)(直接用于生成/修饰输出)

## 注意事项
- <重要注意事项 1>
- <重要注意事项 2>

## 使用示例(可选)
- <示例 1>
- <示例 2>
```

#### 正文规则
1. **体量限制**: 不超过 500 行
2. **链接层级**: 参考文档为一层链接，禁止嵌套引用
3. **语气**: 使用祈使/不定式表达（如"执行..."、"创建..."）
4. **章节顺序**: 任务目标 → 前置准备 → 操作步骤 → 资源索引 → 注意事项

## 参考文档规范

### 文件命名
- 使用小写字母和连字符（如 `data-formats.md`, `api-reference.md`）

### 结构要求
```markdown
# <Topic>

## 目录(超过100行必需)
- [章节1](#章节1)
- [章节2](#章节2)

## 概览
一句话定义与适用范围

## 核心内容
- 数据结构/格式定义(含完整示例)
- 验证规则
- 常见操作(输入→处理→输出)
- 约束与注意事项

## 示例
2-3 个可复制执行的标准示例
```

### 内容要求
- **超过 100 行**: 必须包含目录（TOC）
- **被依赖时**: 必须提供完整的格式定义、示例和验证规则
- **文件模板**: 如果需要生成文件，必须提供格式模板

## 资产管理

### 资产类型
- **模板文件**: 文档、报告的模板
- **配置文件**: 默认配置样例
- **示例数据**: 测试或演示用数据
- **样式资源**: CSS、样式表等

### 组织方式
```
assets/
├── templates/          # 模板文件
│   ├── report.md
│   └── config.json
├── examples/           # 示例数据
│   └── sample.csv
└── styles/             # 样式资源
    └── format.css
```

### 路径引用
- 在 SKILL.md 中引用时使用相对路径：`assets/templates/report.md`
- 在脚本中引用时使用绝对路径：`/workspace/projects/<skill-name>/assets/...`

## 质量检查清单

### 前言区
- [ ] name 符合命名规范
- [ ] description 为单行文本，长度 100-150 字符
- [ ] dependency 格式正确（若存在）

### 正文
- [ ] 不超过 500 行
- [ ] 包含任务目标、操作步骤章节
- [ ] 链接为一层引用

### 目录结构
- [ ] 仅包含 SKILL.md 和有内容的子目录
- [ ] 无空目录
- [ ] 无临时文件（README.md, tmp/, .cache/ 等）

### 参考文档
- [ ] 超过 100 行包含 TOC
- [ ] 被依赖时提供完整格式定义

## 版本管理

### 语义化版本
- **格式**: `major.minor.patch`（如 1.2.3）
- **递增规则**:
  - major: 破坏性变更（移除能力、接口改变）
  - minor: 新增功能（添加能力、不破坏兼容）
  - patch: 错误修复（Bug 修复、文档更新）

### 变更日志
每次版本更新应记录：
- 版本号
- 变更内容（新增/修改/删除）
- 影响范围
- 作者和时间
