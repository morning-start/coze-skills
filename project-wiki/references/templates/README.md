# ProjectWiki 模板库

## 概述

本目录包含 ProjectWiki 支持的所有文档模板，按文档类型分类组织。

---

## 目录结构

```
templates/
├── core/                   # 核心文档（项目级）
├── api/                    # API 文档
├── architecture/           # 架构文档
├── design/                 # 设计文档
├── functional/             # 功能文档
├── requirement/            # 需求文档
├── module/                 # 模块文档
├── service/                # 服务文档
├── state/                  # 状态文档
├── knowledge/              # 知识文档
├── wiki/                   # Wiki 文档
└── changelog/              # 变更日志
```

---

## 模板分类

### 1. 核心文档（core/）

项目级核心文档，位于项目根目录，必须使用标准命名。

| 模板 | 命名 | 用途 | 优先级 |
|------|------|------|--------|
| README.md | `README.md` | 项目概述 | ⭐⭐⭐ |
| ROADMAP.md | `ROADMAP.md` | 路线图 | ⭐⭐⭐ |
| CHANGELOG.md | `CHANGELOG.md` | 变更日志 | ⭐⭐⭐ |
| ARCHITECTURE.md | `ARCHITECTURE.md` | 架构文档 | ⭐⭐⭐ |

**命名规范**：
- ✅ 必须使用全大写（README、ROADMAP、CHANGELOG、ARCHITECTURE）
- ✅ 必须位于项目根目录
- ✅ 必须使用 `.md` 扩展名

### 2. API 文档（api/）

API 接口文档模板。

| 模板 | 用途 |
|------|------|
| api-template.md | API 接口文档 |

**特点**：
- 强调数据流动设计
- 使用 Mermaid 时序图展示数据流转
- 包含请求/响应示例

### 3. 架构文档（architecture/）

系统架构文档模板。

| 模板 | 用途 |
|------|------|
| architecture-doc-template.md | 架构文档 |
| architecture.md | 简化架构文档 |

**特点**：
- 多角色视图
- 多维度设计
- 技术选型说明

### 4. 设计文档（design/）

技术设计文档模板。

| 模板 | 用途 |
|------|------|
| design-doc-template.md | 设计文档 |

**特点**：
- 详细的技术方案
- 设计决策记录
- 实现计划

### 5. 功能文档（functional/）

功能需求文档模板。

| 模板 | 用途 |
|------|------|
| functional-doc-template.md | 功能文档 |

**特点**：
- 功能描述
- 用户场景
- 验收标准

### 6. 需求文档（requirement/）

需求规格文档模板。

| 模板 | 用途 |
|------|------|
| requirement-doc-template.md | 需求文档 |

**特点**：
- 数据模型设计
- 数据流动设计
- 状态管理设计
- 接口设计

### 7. 模块文档（module/）

模块设计文档模板。

| 模板 | 用途 |
|------|------|
| module-template.md | 模块文档 |

**特点**：
- 模块职责
- 接口定义
- 依赖关系

### 8. 服务文档（service/）

服务设计文档模板。

| 模板 | 用途 |
|------|------|
| service-template.md | 服务文档 |

**特点**：
- 服务职责
- API 定义
- 数据流

### 9. 状态文档（state/）

状态机设计文档模板。

| 模板 | 用途 |
|------|------|
| state-machine-template.md | 状态机文档 |

**特点**：
- 状态定义
- 事件定义
- 转换规则
- Mermaid 状态图

### 10. 知识文档（knowledge/）

技术知识文档模板。

| 模板 | 用途 |
|------|------|
| knowledge-template.md | 知识文档 |

**特点**：
- 技术栈介绍
- 最佳实践
- 示例代码

### 11. Wiki 文档（wiki/）

Wiki 页面模板。

| 模板 | 用途 |
|------|------|
| simple-readme.md | 简单 README |
| complex-readme.md | 复杂 README |

**特点**：
- 快速开始
- 使用指南
- 示例

### 12. 变更日志（changelog/）

变更日志模板。

| 模板 | 用途 |
|------|------|
| changelog-template.md | 完整变更日志 |
| version-entry-template.md | 版本条目 |

**特点**：
- 遵循 Keep a Changelog 标准
- 语义化版本号
- 分类清晰

---

## 使用指南

### 基本使用

```bash
# 1. 复制模板
cp references/templates/core/ROADMAP.md ./ROADMAP.md

# 2. 编辑模板
vim ./ROADMAP.md
```

### 智能生成

使用 `generate_doc.py` 自动生成文档：

```bash
# 生成核心文档
python3 scripts/generation/generate_doc.py --type core --name ROADMAP

# 生成 API 文档
python3 scripts/generation/generate_doc.py --type api --name "用户登录接口"

# 生成架构文档
python3 scripts/generation/generate_doc.py --type architecture --name "支付系统"
```

### 自定义模板

1. 复制对应类型的模板
2. 根据需求修改
3. 保存为新的模板

---

## 模板规范

### 命名规范

- 使用小写字母
- 使用连字符分隔单词
- 使用描述性名称

### 格式规范

- 使用 Markdown 格式
- 使用 Mermaid 图表可视化
- 使用代码块展示示例

### 内容规范

- 结构清晰
- 内容完整
- 示例丰富

---

## 最佳实践

1. **从核心文档开始**：先创建 README.md、ROADMAP.md、CHANGELOG.md、ARCHITECTURE.md
2. **遵循命名规范**：核心文档必须使用全大写命名
3. **使用图表可视化**：在 API 文档和架构文档中使用 Mermaid 图表
4. **保持更新**：定期更新文档，确保与代码同步
5. **使用智能生成**：使用 `generate_doc.py --auto` 自动生成文档

---

## 参考资料

- [文档命名规范](../guides/document/naming-conventions.md)
- [SKILL.md](../../SKILL.md)
- [文档指南](../guides/document/)
