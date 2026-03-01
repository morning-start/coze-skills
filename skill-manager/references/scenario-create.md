---
name: scenario-create
description: 创建新技能场景指南，定义从设计到发布的完整创建流程，嵌入生命周期管理
tags: [scenario, create, lifecycle, design, develop, test, release]
---

# 场景：创建新技能

本文档定义创建新技能的完整流程，嵌入技能生命周期管理（设计→开发→测试→发布）。

---

## 场景概述

**适用场景**: 从零开始创建一个新技能
**生命周期**: 设计(Design) → 开发(Develop) → 测试(Test) → 发布(Release)
**预计耗时**: 30-60 分钟
**输出物**: 完整的 SKILL.md + 版本标签

---

## 第一步：查阅信息 (Research)

### 1.1 阅读标准化规范

**必读书档**:
- [skill-standards.md](skill-standards.md) - 了解 SKILL.md 格式规范



**关键检查点**:
| 检查项 | 规范要求 |
|--------|---------|
| 命名规范 | 小写字母+连字符，不以 `-skill` 结尾 |
| 前言区字段 | name, version, author, description, tags |
| description 长度 | 100-150 字符 |
| 正文体量 | 不超过 500 行 |

### 1.2 分析技能需求

**需求分析模板**:
```yaml
需求分析:
  核心问题: [技能要解决什么问题？]
  目标用户: [谁将使用这个技能？]
  使用场景: [什么情况下触发？]
  预期输出: [使用后的结果？]
  约束条件: [技术/功能限制？]
```

**示例**:
```yaml
需求分析:
  核心问题: 数据清洗和预处理
  目标用户: 数据分析师
  使用场景: 获得原始数据需要预处理时
  预期输出: 清洗后的数据和清洗报告
  约束条件: 支持 CSV、JSON 格式
```

### 1.3 设计技能架构

**设计输出物**:
```yaml
技能设计:
  名称: data-cleaner
  核心能力:
    - 缺失值处理
    - 重复数据去除
    - 格式标准化
  输入接口:
    - raw_data: 原始数据
    - rules: 清洗规则
  输出格式:
    - cleaned_data: 清洗后数据
    - report: 清洗报告
```

---

## 第二步：执行操作 (Execute)

### 阶段 1: 设计阶段 (Design)

**准入条件**: 需求已明确
**目标**: 完成技能设计文档

**操作步骤**:
1. **能力定义**
   - 列出所有核心能力
   - 定义能力边界
   - 识别依赖关系

2. **接口设计**
   - 设计输入参数
   - 设计输出格式
   - 定义错误处理

3. **创建目录结构**
   ```bash
   mkdir data-cleaner
   cd data-cleaner
   touch SKILL.md
   ```

**元信息初始化**:
```yaml
---
name: data-cleaner
version: v0.1.0  # 开发版本
author: [your-name]
description: [100-150字符描述]
tags: [tag1, tag2, tag3]
---
```

**准出条件**:
- [ ] 能力边界清晰
- [ ] 接口设计完成
- [ ] 目录结构创建

### 阶段 2: 开发阶段 (Develop)

**准入条件**: 设计阶段已完成
**目标**: 完成 SKILL.md 编写

**操作步骤**:
1. **编写前言区**
   ```yaml
   ---
   name: data-cleaner
   version: v0.1.0
   author: skill-manager
   description: 数据清洗技能，支持缺失值处理、去重和格式标准化；当需要清洗原始数据时使用
   tags: [data-cleaning, preprocessing, validation]
   ---
   ```

2. **编写任务目标**
   ```markdown
   ## 任务目标
   - 本 Skill 用于: 清洗和预处理原始数据
   - 能力包含: 
     - **缺失值处理**: 根据策略填充或删除缺失值
     - **重复数据去除**: 识别并删除重复记录
     - **格式标准化**: 统一数据格式
   - 触发条件: 当获得原始数据需要预处理时使用
   ```

3. **编写操作步骤**
   ```markdown
   ## 操作步骤
   1. 接收原始数据和清洗规则
   2. 分析数据质量
   3. 处理缺失值
   4. 去除重复数据
   5. 标准化数据格式
   6. 生成清洗报告
   ```

4. **编写使用示例**
   ```markdown
   ## 使用示例
   
   ### 示例 1: 清洗 CSV 数据
   
   **输入**:
   ```csv
   name,age,city
   Alice,25,New York
   Bob,,Los Angeles
   Alice,25,New York
   ```
   
   **操作**:
   1. 检测缺失值（age 列）
   2. 删除重复记录（Alice 重复）
   3. 标准化城市名称
   
   **输出**:
   ```csv
   name,age,city
   Alice,25,New York
   Bob,0,Los Angeles
   ```
   ```

5. **编写注意事项**
   ```markdown
   ## 注意事项
   - 清洗前建议备份原始数据
   - 缺失值处理策略需根据数据类型选择
   - 标准化规则需提前定义
   ```

**准出条件**:
- [ ] SKILL.md 编写完成
- [ ] 示例完整可运行
- [ ] 元信息配置正确

### 阶段 3: 测试阶段 (Test)

**准入条件**: 开发阶段已完成
**目标**: 验证技能质量

**操作步骤**:
1. **标准化检验**
   ```bash
   # 检查前言区字段
   head -10 SKILL.md
   
   # 检查描述长度
   grep "description:" SKILL.md | wc -c
   
   # 检查正文行数
   tail -n +6 SKILL.md | wc -l
   ```

2. **质量检查**
   - [ ] 逻辑一致性检查
   - [ ] 示例可行性验证
   - [ ] 链接有效性检查

3. **更新生命周期状态**
**准出条件**:
- [ ] 所有检查项通过
- [ ] 无阻塞性问题

### 阶段 4: 发布阶段 (Release)

**准入条件**: 测试阶段已完成
**目标**: 正式发布技能

**操作步骤**:
1. **确定版本号**
   - 初始版本: v1.0.0

2. **更新版本号**
   ```yaml
   version: v1.0.0
   ```

3. **创建版本标签**
   ```bash
   git add .
   git commit -m "feat: 添加 data-cleaner 技能"
   git tag -a v1.0.0 -m "Release v1.0.0: 初始版本"
   ```

4. **更新 CHANGELOG.md**（项目级）
   ```markdown
   ## v1.0.0 (2024-03-01)
   
   ### 新增
   - 添加 data-cleaner 技能
   - 支持缺失值处理、去重、格式标准化
   ```

**准出条件**:
- [ ] 版本号确定
- [ ] Tag 已创建
- [ ] 发布说明完成

---

## 第三步：检查验收 (Validate)

### 3.1 元信息完整性检查

```yaml
检查清单:
  基础信息:
    - [ ] name: 符合命名规范
    - [ ] version: v1.0.0
    - [ ] author: 存在
    - [ ] description: 100-150字符
    - [ ] tags: ≥3个
  
  生命周期:
    - [ ] status: active
    - [ ] stage: release
  
  版本历史:
    - [ ] version_history 存在
    - [ ] 包含 v1.0.0 记录
```

### 3.2 内容质量检查

```yaml
检查清单:
  结构:
    - [ ] 包含任务目标
    - [ ] 包含操作步骤
    - [ ] 包含使用示例
    - [ ] 包含注意事项
  
  质量:
    - [ ] 正文体量 < 500行
    - [ ] 步骤清晰可执行
    - [ ] 示例完整可复制
```

### 3.3 最终验证

```bash
# 验证技能完整性
ls -la data-cleaner/
# 应包含: SKILL.md

# 验证元信息
grep -A 20 "^---" data-cleaner/SKILL.md

# 验证版本标签
git tag | grep v1.0.0
```

---

## 完整示例

### 创建 data-cleaner 技能的完整流程

```bash
# ========== 第一步：查阅信息 ==========
# 阅读 skill-standards.md
# 分析需求：需要数据清洗技能
# 设计架构：缺失值处理、去重、格式标准化

# ========== 第二步：执行操作 ==========

# 阶段 1: 设计
mkdir data-cleaner
cd data-cleaner

# 阶段 2: 开发
cat > SKILL.md << 'EOF'
---
name: data-cleaner
version: v0.1.0
author: skill-manager
description: 数据清洗技能，支持缺失值处理、去重和格式标准化；当需要清洗原始数据时使用
tags: [data-cleaning, preprocessing, validation]
---

# Data Cleaner

## 任务目标
- 本 Skill 用于: 清洗和预处理原始数据
- 能力包含: 
  - **缺失值处理**: 根据策略填充或删除缺失值
  - **重复数据去除**: 识别并删除重复记录
  - **格式标准化**: 统一数据格式
- 触发条件: 当获得原始数据需要预处理时使用

## 操作步骤
1. 接收原始数据和清洗规则
2. 分析数据质量
3. 处理缺失值
4. 去除重复数据
5. 标准化数据格式
6. 生成清洗报告

## 使用示例

### 示例 1: 清洗 CSV 数据

**输入**:
```csv
name,age,city
Alice,25,New York
Bob,,Los Angeles
Alice,25,New York
```

**操作**:
1. 检测缺失值（age 列）
2. 删除重复记录（Alice 重复）
3. 标准化城市名称

**输出**:
```csv
name,age,city
Alice,25,New York
Bob,0,Los Angeles
```

## 注意事项
- 清洗前建议备份原始数据
- 缺失值处理策略需根据数据类型选择
EOF

# 阶段 3: 测试
# 执行标准化检验
# 质量评分: completeness=0.95, consistency=0.98, usability=0.92

# 阶段 4: 发布
# 更新 version: v0.1.0 → v1.0.0
# 更新 lifecycle: stage=release, status=active
git add .
git commit -m "feat: 添加 data-cleaner 技能"
git tag -a v1.0.0 -m "Release v1.0.0: 初始版本"

# ========== 第三步：检查验收 ==========
# ✅ 元信息完整
# ✅ 内容质量达标
# ✅ 版本标签创建
# ✅ 技能创建成功
```

---

## 常见问题

**Q1: 如何确定技能名称？**
- 使用动词+名词形式，如 `data-cleaner`
- 避免使用 `-skill` 后缀
- 保持简洁，不超过 3 个单词

**Q2: description 写不到 100 字符怎么办？**
- 补充使用场景
- 添加目标用户
- 扩展功能描述

**Q3: 创建过程中发现设计问题？**
- 回退到设计阶段重新设计
- 重新执行设计阶段

---

## 参考文档

- [skill-standards.md](skill-standards.md) - 标准化规范

- [skill-standards.md](skill-standards.md) - 标准化检验流程（详见"标准化检验流程"和"质量检查清单"章节）
