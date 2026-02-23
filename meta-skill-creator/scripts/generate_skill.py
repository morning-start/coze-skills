#!/usr/bin/env python3
"""
技能定义生成器
用于生成符合规范的标准化技能定义（SKILL.md 的 YAML 前言区）
"""

import yaml
from typing import Dict, List, Any, Optional


def generate_skill_definition(
    skill_name: str,
    description: str,
    capabilities: List[str],
    dependencies: Optional[Dict[str, List[str]]] = None,
    extra_metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    生成技能定义的 YAML 前言区

    参数:
        skill_name: 技能名称（小写字母+连字符）
        description: 技能描述（100-150字符，单行）
        capabilities: 能力列表
        dependencies: 依赖配置（可选）
            {
                "python": ["package==version"],
                "system": ["command"]
            }
        extra_metadata: 额外元数据（可选）

    返回:
        YAML 格式的技能定义字符串
    """
    # 验证输入
    if not skill_name or not skill_name.replace('-', '').isalnum():
        raise ValueError("skill_name 必须为小写字母、数字和连字符")

    if not description or len(description) > 150:
        raise ValueError("description 长度必须在 1-150 字符之间")

    # 构建基础结构
    skill_def = {
        'name': skill_name,
        'description': description
    }

    # 添加能力（作为注释或 metadata）
    if capabilities:
        if extra_metadata is None:
            extra_metadata = {}
        extra_metadata['capabilities'] = capabilities

    # 添加依赖
    if dependencies:
        skill_def['dependency'] = dependencies

    # 添加额外元数据
    if extra_metadata:
        skill_def['metadata'] = extra_metadata

    # 生成 YAML
    yaml_output = "---\n"
    yaml_output += yaml.dump(skill_def, default_flow_style=False, sort_keys=False, allow_unicode=True)
    yaml_output += "---\n"

    return yaml_output


def validate_skill_name(skill_name: str) -> bool:
    """
    验证技能名称是否符合命名规范

    参数:
        skill_name: 技能名称

    返回:
        是否有效
    """
    if not skill_name:
        return False

    # 禁止 -skill 后缀
    if skill_name.endswith('-skill'):
        return False

    # 只允许小写字母、数字和连字符
    return bool(skill_name.replace('-', '').isalnum()) and skill_name[0].isalpha()


def generate_template(
    skill_name: str,
    description: str,
    template_type: str = "basic"
) -> str:
    """
    生成技能模板（包含 YAML 前言和正文骨架）

    参数:
        skill_name: 技能名称
        description: 技能描述
        template_type: 模板类型（basic/advanced/composable）

    返回:
        完整的 SKILL.md 模板内容
    """
    yaml_header = generate_skill_definition(
        skill_name=skill_name,
        description=description,
        capabilities=[],
        dependencies=None
    )

    if template_type == "basic":
        body = f"""# {skill_name.replace('-', ' ').title()}

## 任务目标
- 本 Skill 用于: [一句话描述用途]
- 能力包含: [核心能力列表]
- 触发条件: [典型触发场景]

## 前置准备
- 依赖说明: 如有 Python 依赖，在此列出

## 操作步骤
- 标准流程:
  1. [步骤 1]
  2. [步骤 2]
  3. [步骤 3]

## 资源索引
- 必要脚本: 如有脚本，列出路径和用途
- 领域参考: 如有参考文档，列出路径和阅读时机

## 注意事项
- [重要注意事项]
"""
    elif template_type == "advanced":
        body = f"""# {skill_name.replace('-', ' ').title()}

## 任务目标
- 本 Skill 用于: [一句话描述用途]
- 能力包含: [核心能力列表]
- 触发条件: [典型触发场景]

## 前置准备
- 依赖说明:
  ```
  package1==1.0.0
  package2>=2.0.0
  ```

## 操作步骤
- 标准流程:
  1. [步骤 1: 输入/准备]
  2. [步骤 2: 执行/处理]
  3. [步骤 3: 输出/校验]
- 可选分支:
  - 当 [条件 A]: 执行 [分支 A]
  - 当 [条件 B]: 执行 [分支 B]

## 资源索引
- 必要脚本:
  - [scripts/script1.py](scripts/script1.py) (用途与参数: [说明])
  - [scripts/script2.py](scripts/script2.py) (用途与参数: [说明])
- 领域参考:
  - [references/guide.md](references/guide.md) (何时读取: [场景])
- 输出资产:
  - [assets/templates/](assets/templates/) (直接用于输出)

## 注意事项
- [注意事项 1]
- [注意事项 2]

## 使用示例
- [示例 1]
- [示例 2]
"""
    elif template_type == "composable":
        body = f"""# {skill_name.replace('-', ' ').title()}

## 任务目标
- 本 Skill 用于: [一句话描述用途]
- 能力包含: [核心能力列表，支持组合]
- 触发条件: [典型触发场景]

## 前置准备
- 依赖说明: [依赖列表]

## 操作步骤
- 标准流程:
  1. [步骤 1]
  2. [步骤 2]
  3. [步骤 3]
- 组合能力:
  - 支持作为子模块被其他技能调用
  - 输入格式标准化: [格式说明]
  - 输出格式标准化: [格式说明]

## 资源索引
- 必要脚本: [脚本列表]
- 领域参考: [参考文档]
- 组合接口: [组合规范]

## 注意事项
- 模块化设计，保持接口清晰
- 避免硬编码，支持配置化

## 使用示例
- [组合示例]
"""
    else:
        body = "# 技能正文待补充\n"

    return yaml_header + body


if __name__ == "__main__":
    # 示例用法
    yaml_def = generate_skill_definition(
        skill_name="data-processor",
        description="数据处理技能，支持清洗、转换和验证",
        capabilities=["数据清洗", "格式转换", "质量验证"],
        dependencies={
            "python": ["pandas>=1.5.0", "pyyaml>=6.0"],
            "system": []
        }
    )
    print("=== 生成的 YAML 前言区 ===")
    print(yaml_def)

    template = generate_template(
        skill_name="data-processor",
        description="数据处理技能，支持清洗、转换和验证",
        template_type="advanced"
    )
    print("\n=== 完整模板 ===")
    print(template)
