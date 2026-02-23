---
name: {{ config.name }}
description: {{ config.description }}
{% if config.dependency %}
dependency:
{% if config.dependency.python %}
  python:
{% for dep in config.dependency.python %}
    - {{ dep }}
{% endfor %}
{% endif %}
{% if config.dependency.system %}
  system:
{% for cmd in config.dependency.system %}
    - {{ cmd }}
{% endfor %}
{% endif %}
{% endif %}
---

# {{ config.name|capitalize|replace('-', ' ') }}

## 任务目标
- 本 Skill 用于:{{ config.description }}
- 能力包含:{% for tool in config.tools %} {{ tool.description }}{% if not loop.last %},{% endif %}{% endfor %}
- 触发条件:{% if config.triggers %}{% for trigger in config.triggers %} {{ trigger }}{% if not loop.last %},{% endif %}{% endfor %}{% else %}用户请求相关功能{% endif %}

## 前置准备
{% if config.dependency and config.dependency.python %}
- 依赖说明:scripts 脚本所需的依赖包及版本
  ```
{% for dep in config.dependency.python %}
  {{ dep }}
{% endfor %}
  ```
{% endif %}
{% if config.dependency and config.dependency.system %}
- 非标准文件/文件夹准备:
  ```bash
{% for cmd in config.dependency.system %}
  {{ cmd }}
{% endfor %}
  ```
{% else %}
- 非标准文件/文件夹准备:无
{% endif %}

## 操作步骤
- 标准流程:
  1. **输入准备**
     - 接收用户输入:{{ config.inputs|first if config.inputs else '请提供必要参数' }}
  2. **处理执行**
     - {% if config.tools %}调用工具处理:{% for tool in config.tools[:3] %}{{ tool.name }}{% if not loop.last %}、{% endif %}{% endfor %}{% endif %}
     - {% if config.scripts %}执行脚本:{% for script in config.scripts[:3] %}{{ script.name }}{% if not loop.last %}、{% endif %}{% endfor %}{% endif %}
  3. **结果输出**
     - 返回处理结果给用户

- 可选分支:
{% if config.branches %}
  {% for branch in config.branches %}
  - 当 {{ branch.condition }}:执行 {{ branch.action }}
  {% endfor %}
{% else %}
  - 无额外分支
{% endif %}

## 资源索引
{% if config.scripts %}
- 必要脚本:
{% for script in config.scripts %}
  - [scripts/{{ script.name }}](scripts/{{ script.name }})(用途与参数:{{ script.description }})
{% endfor %}
{% endif %}
{% if config.references %}
- 领域参考:
{% for ref in config.references %}
  - [references/{{ ref.name }}](references/{{ ref.name }})(何时读取:{{ ref.usage if ref.usage else '参考配置' }})
{% endfor %}
{% endif %}
{% if config.assets %}
- 输出资产:
{% for asset in config.assets %}
  - [assets/{{ asset.path }}](assets/{{ asset.path }})(用途:{{ asset.usage if asset.usage else '资源文件' }})
{% endfor %}
{% endif %}

## 注意事项
- 确保输入参数格式正确
- 遵循各工具的使用规范
- 处理异常情况并提供友好提示
- 充分利用智能体的理解能力

## 使用示例

### 示例 1:基本使用
- **功能说明**:{{ config.description }}
- **执行方式**:直接调用相关工具
- **关键参数**:{% if config.inputs %}{% for input in config.inputs[:3] %}{{ input.name }}{% if not loop.last %}、{% endif %}{% endfor %}{% else %}见工具配置{% endif %}
- **示例**:根据实际需求提供示例

### 示例 2:高级配置
- **功能说明**:使用工作流编排多个工具
- **执行方式**:按工作流顺序执行
- **关键参数**:见工作流配置
- **示例**:参考工作流指南
