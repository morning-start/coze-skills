# 更新日志 (CHANGELOG)

本文档记录 Coze Skills 技能集合的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-02-18

### 新增 (Added)

#### 项目初始化
- 创建 Coze Skills 技能集合项目
- 添加项目级 README.md 文档，包含所有技能的详细介绍
- 添加 CHANGELOG.md 文档，用于记录项目变更历史

#### 技能列表 (8个核心技能)

1. **api-doc-generator** - API 文档自动生成器
   - 支持 Flask/FastAPI/Express 框架
   - 自动划分功能模块和层级结构
   - 生成完整的 API 文档（概述、认证、端点详情、错误处理等）
   - 包含代码扫描脚本和模块分类脚本

2. **copyright-assist** - 软著申请辅助技能
   - 源代码提取与格式化（符合国家版权局要求）
   - 设计说明书/用户说明书/操作手册撰写指导
   - 资源完整性检查工具
   - 自动打包提交材料
   - 支持多版本申请

3. **project-wiki** - 项目知识库构建工具
   - 智能项目结构分析
   - 隐性知识挖掘
   - 知识图谱构建（Mermaid 可视化）
   - 支持 13+ 主流框架（React/Vue/Django/Spring Boot 等）
   - 包含完整的框架指引文档

4. **python-team** - Python 团队协同开发技能
   - 四角色协同（自主学习/PM/架构师/高级程序员）
   - 从自然语言需求生成完整 Python 项目
   - 支持功能扩展和项目重构
   - 支持数据库设计与实现（SQLite/PostgreSQL/MongoDB/向量数据库/图数据库）
   - 数据层抽象（Repository 模式）
   - 强制使用 Python 3.11+ 特性、UV 包管理、loguru 日志

5. **pythonic-style** - Pythonic 代码风格
   - 代码风格分析与改进建议
   - Pythonic 惯用法指导（列表推导、生成器、装饰器等）
   - 设计模式应用（SOLID 原则）
   - 性能优化建议
   - 重构指导
   - 140+ 实战代码模板
   - 基于 "Friendly Python" 理念

6. **recruitment-processor** - 招聘信息处理技能
   - 批量处理招聘 markdown 文档
   - 图片识别与 OCR
   - 关键信息提取（职位、薪资、截止时间等）
   - 条件筛选功能
   - 生成结构化总结报告

7. **six-layer-architect** - 六层架构全栈生成器
   - 基于六层架构（前端UI/前端服务/前端API/后端API/后端服务/数据层）
   - 逐层代码生成
   - 跨层一致性校验
   - 架构与安全审查
   - 技术栈：Vue 3 + Tailwind + Pinia + TypeScript + FastAPI + Pydantic + SQLAlchemy + PostgreSQL

8. **tech-comparison** - 技术选型对比助手
   - 智能识别技术类型
   - 动态选择对比维度
   - 生成结构化技术选型报告
   - 支持前端框架、后端技术、数据库、部署方案等多维度对比

### 文档结构

每个技能包含标准化的文档结构：
- `SKILL.md` - 技能主文档（任务目标、操作步骤、资源索引、注意事项、使用示例）
- `assets/templates/` - 代码模板
- `references/` - 参考文档和指南
- `scripts/` - Python 辅助脚本（部分技能）
- `config.yaml` - 配置文件（部分技能）

### 技术栈

- **Python** - 主要开发语言
- **Markdown** - 文档格式
- **Jinja2** - 模板引擎（six-layer-architect）
- **PyYAML** - 配置文件解析（copyright-assist）
- **Pydantic** - 数据验证（six-layer-architect）

### 设计原则

- 模块化设计，每个技能独立运行
- 标准化的文档结构
- 清晰的使用说明和示例
- 完整的资源索引和参考文档

---

## 版本说明

### 版本号格式
- **主版本号 (Major)**：不兼容的 API 修改
- **次版本号 (Minor)**：向下兼容的功能新增
- **修订号 (Patch)**：向下兼容的问题修正

### 变更类型
- **新增 (Added)** - 新功能
- **变更 (Changed)** - 功能变更
- **弃用 (Deprecated)** - 即将移除的功能
- **移除 (Removed)** - 已移除的功能
- **修复 (Fixed)** - 问题修复
- **安全 (Security)** - 安全相关的修复

---

## 未来计划

### [1.1.0] - 计划中
- [ ] 添加更多技能
- [ ] 改进现有技能的功能
- [ ] 增加自动化测试
- [ ] 优化文档结构

---

## 链接

- [项目 README](./README.md)
- [技能文档](./)
