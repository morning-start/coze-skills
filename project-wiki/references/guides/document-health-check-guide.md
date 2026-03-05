# 文档健康度检查指南

## 概述

本文档提供文档健康度检查的方法和工具，确保文档质量、准确性和时效性。

---

## 检查项

### 1. Broken Link 检测

**目标**：检测文档中的失效链接。

**检查方法**：
```bash
# 使用 markdown-link-check
find . -name "*.md" -exec markdown-link-check {} \;

# 或使用 CI 自动检查
# 详见 .github/workflows/link-check.yml
```

**修复建议**：
- 更新失效的外部链接
- 修复错误的内部链接
- 移除无用的参考链接

---

### 2. 过期标记

**目标**：识别超过一定时间未更新的文档。

**检查方法**：
```bash
# 检查超过 90 天未更新的文档
find . -name "*.md" -mtime +90 -type f
```

**标记规则**：
- **新鲜**：< 30 天
- **较新**：30-60 天
- **可能过期**：60-90 天
- **已过期**：> 90 天

**处理建议**：
- 可能过期的文档：通知责任人 review
- 已过期的文档：标记"⚠️ 可能过期"，安排更新

---

### 3. 内容准确性验证

**目标**：验证文档内容的准确性。

**检查方法**：
1. **抽样检查**：随机抽取 20% 的文档
2. **代码对比**：验证文档中的代码示例与实际代码一致
3. **API 验证**：验证 API 文档与实际接口一致
4. **截图验证**：验证截图是否反映当前界面

**工具辅助**：
```bash
# 检查代码示例中的依赖版本
grep -r "version" wiki/ | grep -E "v\d+\.\d+"
```

---

### 4. 格式规范检查

**目标**：确保文档格式符合规范。

**检查方法**：
```bash
# 使用 markdownlint 检查格式
markdownlint **/*.md

# 检查占位符未替换
grep -r "{{" wiki/ || grep -r "\[TODO\]" wiki/
```

**检查项**：
- [ ] Markdown 语法正确
- [ ] 标题层级清晰
- [ ] 代码块语言标注
- [ ] 表格格式规范
- [ ] 无占位符未替换

---

### 5. 更新频率监控

**目标**：监控文档更新频率，确保文档活跃。

**监控指标**：
- **文档更新频率**：每月更新次数
- **文档活跃度**：最近 30 天是否有更新
- **责任人响应时间**：发现问题后多久修复

**监控脚本**：
```bash
#!/bin/bash
# 文档活跃度报告
echo "=== 文档活跃度报告 ==="
echo "总文档数：$(find . -name '*.md' | wc -l)"
echo "最近 30 天更新：$(find . -name '*.md' -mtime -30 | wc -l)"
echo "最近 90 天未更新：$(find . -name '*.md' -mtime +90 | wc -l)"
```

---

## 健康度报告

### 报告模板

```markdown
# 文档健康度报告

**生成时间**：2024-02-20
**检查范围**：所有 Markdown 文档

## 总体评分：85/100

## 指标

| 指标 | 得分 | 说明 |
|------|------|------|
| 链接有效性 | 95/100 | 发现 2 个失效链接 |
| 内容时效性 | 80/100 | 5 篇文档超过 90 天未更新 |
| 格式规范性 | 90/100 | 3 处格式问题 |
| 内容准确性 | 85/100 | 2 处代码示例需更新 |

## 问题列表

### 高优先级
1. API 文档与实际接口不一致
2. 部署文档中的命令已过时

### 中优先级
1. 3 篇文档格式不规范
2. 2 个外部链接失效

### 低优先级
1. 部分文档缺少版本信息

## 改进建议

1. 本周内修复高优先级问题
2. 下周内修复中优先级问题
3. 安排责任人更新过期文档
```

---

## 自动化检查

### CI 集成示例

```yaml
# .github/workflows/doc-health-check.yml
name: Document Health Check

on:
  schedule:
    - cron: '0 9 * * 1'  # 每周一上午 9 点
  workflow_dispatch:

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check links
        run: |
          npm install -g markdown-link-check
          find . -name "*.md" -exec markdown-link-check {} \;
      
      - name: Check format
        run: |
          npm install -g markdownlint-cli
          markdownlint **/*.md
      
      - name: Check stale docs
        run: |
          find . -name "*.md" -mtime +90 -type f
      
      - name: Generate report
        run: |
          echo "# Document Health Report" > report.md
          echo "Generated: $(date)" >> report.md
```

---

## 使用建议

1. **定期检查**：每月运行一次健康度检查
2. **自动化**：在 CI 中集成自动检查
3. **快速修复**：发现问题后尽快修复
4. **趋势分析**：跟踪健康度趋势，持续改进

---

## 参考资料

- [文档管理流程指南](document-management-guide.md)
- [评审 checklist 模板](../templates/document-review-checklist.md)
