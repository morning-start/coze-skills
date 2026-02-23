# Skill 规范详解

## 目录
1. [命名规范](#命名规范)
2. [目录结构](#目录结构)
3. [SKILL.md 格式规范](#skillmd-格式规范)
4. [脚本规范](#脚本规范)
5. [参考文档规范](#参考文档规范)
6. [资产规范](#资产规范)
7. [质量门槛](#质量门槛)
8. [配置文件格式](#配置文件格式)

## 概览
本文档定义 Skill 的完整规范，包括命名、结构、格式和质量要求，确保技能包的一致性和可维护性。

## 命名规范

### 目录命名
- 格式：小写字母 + 连字符
- 长度：建议 3-30 个字符
- 禁止：禁止使用 `-skill` 后缀
- 示例：
  - ✅ 正确：`book-skill-creator`、`pdf-parser`、`exam-grading`
  - ❌ 错误：`BookSkillCreator`、`pdf_skill`、`exam-grading-skill`

### 文件命名
- SKILL.md：固定文件名，大小写敏感
- 脚本文件：小写字母 + 连字符 + 扩展名（如 `batch-create.py`）
- 参考文档：小写字母 + 连字符 + `.md`
- 资产文件：根据类型命名，保持简洁

## 目录结构

### 固定结构
```
<skill-name>/
├── SKILL.md           # 必需：入口与指南
├── scripts/           # 可选：可执行代码
├── references/        # 可选：参考文档
└── assets/            # 可选：静态资源
```

### 规则说明
- **必需文件**：SKILL.md 必须存在
- **可选目录**：scripts/、references/、assets/ 可选，存在时必须有内容
- **禁止内容**：禁止包含除固定结构外的任何文件或文件夹
- **清理规则**：打包前清理 README.md、tmp/、.cache/、__pycache__/、.DS_Store 等

## SKILL.md 格式规范

### 前言区（YAML）
```yaml
---
name: <skill-name>              # 必需，符合命名规范
description: <描述>             # 必需，100-150字符，单行格式
dependency:                     # 可选
  python:                       # Python依赖
    - package==version
  system:                       # 系统命令
    - <command>
---
```

### 字段说明

#### name
- 类型：字符串
- 必需：是
- 格式：小写字母 + 连字符
- 示例：`book-skill-creator`

#### description
- 类型：字符串
- 必需：是
- 格式：单行文本
- 长度：100-150 字符
- 内容：包含核心能力和触发场景
- 示例：`技能工厂核心母技能，支持批量创建技能、理解官方文档生成方案、网络搜索辅助、代码框架生成`

#### dependency.python
- 类型：列表
- 必需：否
- 格式：参考 requirements.txt
- 示例：
  ```yaml
  python:
    - requests==2.28.0
    - pyyaml>=6.0
  ```

#### dependency.system
- 类型：列表
- 必需：否
- 格式：命令列表
- 路径：相对于 Skill 目录的父目录
- 注意：禁止包含 Python 包安装命令
- 示例：
  ```yaml
  system:
    - mkdir -p extra-files/input
    - chmod +x scripts/*.sh
  ```

### 正文结构
```markdown
# <技能标题>

## 任务目标
- 本 Skill 用于：<一句话场景>
- 能力包含：<核心能力要点>
- 触发条件：<典型用户表达>

## 前置准备
- 依赖说明：<脚本依赖>
- 非标准文件/文件夹准备：<前置命令>

## 操作步骤
### 标准流程
1. 步骤1：<说明>
2. 步骤2：<说明>

### 可选分支
- 当 <条件A>：执行 <分支A>

## 资源索引
- 必要脚本：<路径>（用途与参数）
- 领域参考：<路径>（何时读取）
- 输出资产：<路径>（用途）

## 注意事项
- <重要提示>

## 使用示例（可选）
- <2-3个典型场景>
```

### 正文要求
- 长度：不超过 500 行
- 语气：祈使/不定式（如"执行..."、"创建..."）
- 链接：仅一层链接到 references/
- 内容：聚焦核心流程，细节放入 references/

## 脚本规范

### 通用要求
- 可执行性：脚本必须能直接执行，无需调用方修改
- 参数设计：动态变量通过参数传入，禁止硬编码占位符
- 错误处理：包含完整的错误处理和日志输出
- 依赖清晰：明确列出所需依赖

### 参数规范
- 使用 argparse 解析参数
- 参数名称清晰，有明确用途
- 支持帮助信息（--help）
- 示例：
  ```python
  import argparse

  parser = argparse.ArgumentParser(description='脚本说明')
  parser.add_argument('--input', required=True, help='输入文件路径')
  parser.add_argument('--output', default='./output', help='输出目录')
  args = parser.parse_args()
  ```

### 输入格式一致性
- 脚本输入解析逻辑必须与 references/ 中定义的格式完全一致
- 包含格式验证和错误处理
- 提供清晰的错误提示

### 第三方服务调用规范
涉及第三方 API 调用时，必须遵循以下流程：
1. 确定授权类型（ApiKey/OAuth/WeChatOfficialAccount）
2. 调用 skill_credentials 工具配置凭证
3. 使用 coze_workload_identity 包的 requests/httpx
4. 通过 os.getenv() 获取凭证
- 禁止：
  - ❌ 将凭证作为函数参数
  - ❌ 在脚本中放置占位符让调用方替换
  - ❌ 使用标准库的 requests 包

## 参考文档规范

### 格式要求
- 长度：超过 100 行必须包含目录（TOC）
- 结构：清晰的组织结构，分章节说明
- 命名：使用描述性名称

### 被依赖时的格式要求
当参考文档被脚本或其他资源依赖时，必须提供：
1. **完整的格式定义**：明确说明数据结构、字段含义、类型
2. **完整示例**：提供至少 2-3 个可复制的示例
3. **验证规则**：说明如何验证输入是否符合格式
4. **错误处理**：说明遇到不符合格式的输入时的处理方式

### 示例模板
```markdown
# <Topic>

## 目录（超过100行必需）
- [概览](#概览)
- [格式定义](#格式定义)
- [示例](#示例)

## 概览
一句话定义与适用范围

## 格式定义
- 字段1：<说明>
- 字段2：<说明>

## 示例
### 示例1
<代码或配置>
```

## 资产规范

### 分类
- 模板：SKILL.md 模板、代码脚手架
- 资源：静态文件、图标、配置样例

### 要求
- 可直接使用：无需额外修改即可使用
- 路径正确：引用路径符合规范
- 格式正确：文件格式符合用途

## 质量门槛

### 必须检查项

#### 前言区
- [ ] name 符合命名规范（小写字母+连字符）
- [ ] description 采用单行格式（含核心能力与触发场景）
- [ ] description 长度在 100-150 字符之间
- [ ] dependency 格式正确（若存在）

#### 正文
- [ ] 不超过 500 行
- [ ] 参考均为一层链接
- [ ] 使用祈使语气
- [ ] 避免与参考重复

#### 目录结构
- [ ] 命名符合规范
- [ ] 无多余文档
- [ ] 引用路径正确
- [ ] 长参考含 TOC
- [ ] 无空目录

#### 实现方式
- [ ] 脚本使用符合选型指南
- [ ] 内容创作类任务未使用脚本
- [ ] 技术性任务使用了脚本
- [ ] 每个脚本都有明确的技术性理由

#### 脚本质量
- [ ] 通过语法校验
- [ ] 试运行通过
- [ ] 架构合规（无 web server、持久化服务等）
- [ ] 依赖清晰
- [ ] 参数规范
- [ ] 直接可执行
- [ ] 涉及第三方 API 时正确处理授权

#### 资源联动
- [ ] 脚本输入解析逻辑与 references 格式完全一致
- [ ] 参考文件提供完整的格式定义、示例和验证规则
- [ ] SKILL.md 中的引用与实际资源一致

#### 打包
- [ ] .skill 为 Zip 格式
- [ ] 包含所有必要文件
- [ ] 相对路径一致
- [ ] 已清理临时文件

#### 内容纯净
- [ ] 不含临时文件
- [ ] 不含生成脚本
- [ ] 不含缓存与日志
- [ ] 无标准结构外的文件

## 配置文件格式

### batch_create.py 配置格式

```json
{
  "skills": [
    {
      "name": "skill-name",
      "type": "api|workflow|data-process",
      "description": "技能描述（100-150字符）",
      "dependencies": [],
      "templates": {
        "skill-md": "api-skill.md",
        "scripts": ["python-script.py"]
      }
    }
  ],
  "output_dir": "/workspace/projects"
}
```

### 字段说明

#### skills
- 类型：数组
- 说明：技能列表

#### skills[].name
- 类型：字符串
- 说明：技能名称，符合命名规范

#### skills[].type
- 类型：字符串
- 说明：技能类型
- 可选值：
  - `api`：API 调用类
  - `workflow`：工作流类
  - `data-process`：数据处理类

#### skills[].description
- 类型：字符串
- 说明：技能描述，100-150 字符

#### skills[].dependencies
- 类型：数组
- 说明：依赖的其他技能名称

#### skills[].templates
- 类型：对象
- 说明：使用的模板文件

#### output_dir
- 类型：字符串
- 说明：输出目录路径

## 示例

### 完整 SKILL.md 示例
```markdown
---
name: pdf-parser
description: 解析PDF文档，提取文本、表格和图片，支持批量处理和格式转换
---

# PDF Parser

## 任务目标
- 本 Skill 用于：解析 PDF 文档，提取结构化内容
- 能力包含：文本提取、表格解析、图片提取、格式转换
- 触发条件：用户需要处理 PDF 文件时

## 操作步骤
1. 读取 PDF 文件
2. 提取内容
3. 格式转换

## 资源索引
- scripts/parse.py：PDF 解析脚本
```

### 完整脚本示例
```python
#!/usr/bin/env python3
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='PDF 解析脚本')
    parser.add_argument('--input', required=True, help='PDF 文件路径')
    parser.add_argument('--output', default='./output', help='输出目录')
    args = parser.parse_args()

    try:
        # 处理逻辑
        print(f"处理 {args.input}")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
```
