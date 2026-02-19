# 更新日志 (CHANGELOG)

本文档记录 Coze Skills 技能集合的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.3.0] - 2026-02-19

### 新增 (Added)

#### 新技能
- **flutter-skills** - Flutter 开发完整指南 (v1.0.0)
  - Clean Architecture 架构规范
  - TDD 测试工作流
  - BLoC 状态管理
  - 故障排除指南（构建错误、运行时错误、状态调试、性能分析）
  - 4 个代码生成脚本（generate_feature, generate_model, generate_bloc, generate_test）
  - 4 个智能助手 Agent（TDD Coach, Code Reviewer, Test Writer, Architecture Reviewer）
  - 40+ Flutter 库的选型指南
  - 11 个详细技能文档 + 9 个命令文档

---

## [1.2.1] - 2026-02-19

### 变更 (Changed)

#### 技能升级
- **project-wiki** 升级到 2.2.3 版本
  - 更新 FEATURE_INDEX.md，完善功能索引
  - 更新 scripts/README.md，更新脚本说明
  - 新增 6 个脚本工具：
    - adaptive_structure.py - 自适应结构生成
    - complexity_analyzer.py - 复杂度分析器
    - consistency_checker.py - 一致性检查器
    - context_aware.py - 上下文感知处理
    - multi_hop_qa.py - 多跳问答系统
    - structure_optimizer.py - 结构优化器

---

## [1.2.0] - 2026-02-19

### 新增 (Added)

#### 新技能
- **architecture-design** - 智能技术架构方案生成器
  - 根据业务需求和技术栈生成可实施的架构方案
  - 四步流程：收集信息、梳理需求、迭代完善、输出方案
  - 支持需求分析、技术选型评估、架构设计
  - 提供替代方案建议和方案输出
  - 包含技术选型参考指南

#### 技能升级
- **project-wiki** 升级到 2.0.0 版本
  - 新增 FEATURE_INDEX.md 功能索引
  - 重构 references 目录结构（core/document-guides/roles/templates/visualization）
  - 新增 assets/ 资源目录（changelog 模板、wiki 模板）
  - 新增 8 个脚本工具（create_wiki_structure、evaluate_complexity、generate_changelog、generate_cicd、generate_doc、generate_roadmap、query_knowledge、role_view）
  - 新增角色视图指南（架构师/开发者/测试/运维/产品）

### 变更 (Changed)

#### CI/CD 流程优化
- 简化 CI/CD workflow，删除复杂的多 job 结构
- 每次发布构建所有技能，简化管理流程
- 删除独立版本 tag 支持，统一使用 v* 格式
- 删除变更检测逻辑，避免检测失败问题

---

## [1.1.0] - 2026-02-19

### 新增 (Added)

#### 新技能
- **doc-skill-generator** - 文档技能生成器（母技能）
  - 根据技术官网自动生成 Skill 子技能包
  - 支持 Vue、React、Go 等多种技术栈
  - 智能抓取官网文档内容
  - 自动提取版本号和元数据
  - LLM 内容摘要与核心能力图谱生成
  - 模板化子技能生成（语言类/框架类/工具类）
  - 自动验证技能完整性

### 变更 (Changed)

#### CI/CD 改进
- 实现技能独立版本管理
- 添加智能变更检测脚本
- 支持多种发布场景（新技能/单个更新/多个更新/全部重建）
- 重构 GitHub Actions workflow

---

## [1.0.0] - 2026-02-18

### 新增 (Added)

#### 项目初始化
- 创建 Coze Skills 技能集合项目
- 添加项目级 README.md 文档，包含所有技能的详细介绍
- 添加 CHANGELOG.md 文档，用于记录项目变更历史
- 添加 LICENSE 文件，使用 MIT 许可证

#### CI/CD 自动化
- 添加 GitHub Actions workflow，实现自动化构建和发布
- 创建技能打包脚本 (build_skills.py)，支持打包所有技能为 .skill 格式
- 创建发布说明生成脚本 (generate_release_notes.py)，从 CHANGELOG.md 自动生成发布说明
- 创建版本管理脚本 (bump_version.py)，支持版本号更新和 Git 标签创建
- 支持通过 Git tag 触发自动发布
- 支持手动触发构建流程

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
