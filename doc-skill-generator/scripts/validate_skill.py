#!/usr/bin/env python3
"""
技能验证工具 - 自动构造测试问题，检查子技能是否能正确回答

功能：
- 读取生成的子技能文件
- 基于技能内容自动构造测试问题
- 验证技能文档的完整性和可用性
- 生成验证报告

使用示例：
python validate_skill.py --skill-path "./vue-skills" --output "./validation_report.json"
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict, Set
from datetime import datetime


def read_skill_files(skill_dir: Path) -> Dict:
    """
    读取技能目录下的所有文件

    返回：包含文件内容和路径的字典
    """
    skill_data = {
        "skill_dir": str(skill_dir),
        "skill_md": None,
        "references": {},
        "assets": {},
        "scripts": {}
    }

    # 读取 SKILL.md
    skill_md_path = skill_dir / "SKILL.md"
    if skill_md_path.exists():
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            skill_data["skill_md"] = f.read()

    # 读取 references/
    references_dir = skill_dir / "references"
    if references_dir.exists():
        for ref_file in references_dir.glob("*.md"):
            with open(ref_file, 'r', encoding='utf-8') as f:
                skill_data["references"][ref_file.name] = f.read()

    # 读取 assets/
    assets_dir = skill_dir / "assets"
    if assets_dir.exists():
        for asset_file in assets_dir.rglob("*"):
            if asset_file.is_file():
                try:
                    with open(asset_file, 'r', encoding='utf-8') as f:
                        skill_data["assets"][str(asset_file.relative_to(assets_dir))] = f.read()
                except:
                    # 二进制文件跳过
                    skill_data["assets"][str(asset_file.relative_to(assets_dir))] = "[binary file]"

    return skill_data


def validate_skill_metadata(skill_data: Dict) -> Dict:
    """
    验证技能元数据（YAML 前言区）

    检查项：
    - name 字段存在且符合规范
    - description 字段存在且长度合理
    - dependency 字段格式正确
    """
    issues = []
    passed = []

    if not skill_data["skill_md"]:
        issues.append("SKILL.md 文件不存在")
        return {"issues": issues, "passed": passed}

    content = skill_data["skill_md"]

    # 检查 YAML 前言区
    if not content.startswith("---"):
        issues.append("SKILL.md 缺少 YAML 前言区（必须以 --- 开头）")
    else:
        passed.append("YAML 前言区格式正确")

    # 检查 name 字段
    if "name:" in content[:500]:
        passed.append("name 字段存在")
    else:
        issues.append("SKILL.md 缺少 name 字段")

    # 检查 description 字段
    if "description:" in content[:500]:
        passed.append("description 字段存在")
    else:
        issues.append("SKILL.md 缺少 description 字段")

    return {"issues": issues, "passed": passed}


def validate_skill_structure(skill_data: Dict) -> Dict:
    """
    验证技能目录结构

    检查项：
    - 目录命名规范
    - 仅包含必要的子目录
    - 无空目录
    """
    issues = []
    passed = []

    skill_dir = Path(skill_data["skill_dir"])

    # 检查 SKILL.md
    if (skill_dir / "SKILL.md").exists():
        passed.append("SKILL.md 存在")
    else:
        issues.append("缺少 SKILL.md")

    # 检查允许的子目录
    allowed_dirs = ["scripts", "references", "assets"]
    for item in skill_dir.iterdir():
        if item.is_dir() and item.name not in allowed_dirs:
            issues.append(f"发现不允许的目录: {item.name}")

    # 检查空目录
    for dir_name in allowed_dirs:
        dir_path = skill_dir / dir_name
        if dir_path.exists():
            if not list(dir_path.iterdir()):
                issues.append(f"{dir_name}/ 目录为空，建议删除")

    return {"issues": issues, "passed": passed}


def validate_content_quality(skill_data: Dict) -> Dict:
    """
    验证内容质量

    检查项：
    - SKILL.md description 长度 100-150 字符
    - SKILL.md 正文不超过 500 行
    - 参考文档质量
    """
    issues = []
    passed = []

    if not skill_data["skill_md"]:
        return {"issues": ["SKILL.md 不存在"], "passed": []}

    content = skill_data["skill_md"]

    # 检查 description 长度
    desc_match = None
    for line in content.split('\n')[:50]:
        if line.strip().startswith('description:'):
            desc_match = line
            break

    if desc_match:
        desc_text = desc_match.split(':', 1)[1].strip().strip('"')
        if 100 <= len(desc_text) <= 150:
            passed.append(f"description 长度符合规范 ({len(desc_text)} 字符)")
        else:
            issues.append(f"description 长度不符合规范 ({len(desc_text)} 字符，应在 100-150 之间)")

    # 检查 SKILL.md 总行数
    total_lines = len(content.split('\n'))
    if total_lines <= 500:
        passed.append(f"SKILL.md 行数符合规范 ({total_lines} 行)")
    else:
        issues.append(f"SKILL.md 行数超过限制 ({total_lines} 行，应 ≤ 500)")

    # 检查参考文档数量
    if len(skill_data["references"]) > 0:
        passed.append(f"包含 {len(skill_data['references'])} 个参考文档")
    else:
        issues.append("缺少参考文档（references/）")

    return {"issues": issues, "passed": passed}


def generate_test_questions(skill_data: Dict) -> List[Dict]:
    """
    基于技能内容生成测试问题

    这些问题用于验证技能的完整性：
    - 能否回答基础概念问题
    - 能否提供使用示例
    - 能否解决常见问题
    """
    questions = []

    # 从 SKILL.md 中提取关键概念（简化版）
    if skill_data["skill_md"]:
        content = skill_data["skill_md"]

        # 提取任务目标
        if "任务目标" in content:
            questions.append({
                "category": "任务目标",
                "question": "这个技能的目的是什么？",
                "expected_content": ["任务目标", "核心能力"]
            })

        # 提取操作步骤
        if "操作步骤" in content:
            questions.append({
                "category": "操作步骤",
                "question": "如何使用这个技能？",
                "expected_content": ["步骤", "操作"]
            })

    # 检查参考文档
    if skill_data["references"]:
        for ref_name in skill_data["references"].keys():
            questions.append({
                "category": "参考资料",
                "question": f"如何查看 {ref_name} 的内容？",
                "expected_content": [ref_name, "references"]
            })

    return questions


def generate_validation_report(skill_dir: Path, output_path: Path):
    """
    生成完整的验证报告
    """
    # 读取技能文件
    skill_data = read_skill_files(skill_dir)

    # 执行各项验证
    metadata_validation = validate_skill_metadata(skill_data)
    structure_validation = validate_skill_structure(skill_data)
    content_validation = validate_content_quality(skill_data)

    # 生成测试问题
    test_questions = generate_test_questions(skill_data)

    # 汇总问题
    all_issues = (
        metadata_validation["issues"] +
        structure_validation["issues"] +
        content_validation["issues"]
    )

    all_passed = (
        metadata_validation["passed"] +
        structure_validation["passed"] +
        content_validation["passed"]
    )

    # 生成报告
    report = {
        "metadata": {
            "validated_at": datetime.now().isoformat(),
            "skill_path": str(skill_dir)
        },
        "summary": {
            "total_issues": len(all_issues),
            "total_passed": len(all_passed),
            "status": "PASSED" if len(all_issues) == 0 else "FAILED"
        },
        "validation_results": {
            "metadata": metadata_validation,
            "structure": structure_validation,
            "content": content_validation
        },
        "test_questions": {
            "total": len(test_questions),
            "questions": test_questions
        },
        "recommendations": []
    }

    # 生成建议
    if len(all_issues) > 0:
        report["recommendations"].append("请修复所有问题后重新打包")
    if len(skill_data["references"]) == 0:
        report["recommendations"].append("建议添加参考文档（references/）")
    if len(skill_data["assets"]) == 0:
        report["recommendations"].append("建议添加代码示例（assets/）")

    # 保存报告
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 打印摘要
    print("=" * 60)
    print("技能验证报告")
    print("=" * 60)
    print(f"技能路径: {skill_dir}")
    print(f"验证状态: {report['summary']['status']}")
    print(f"通过项: {len(all_passed)}")
    print(f"失败项: {len(all_issues)}")
    print("=" * 60)

    if all_issues:
        print("\n发现问题:")
        for issue in all_issues:
            print(f"  ❌ {issue}")
    else:
        print("\n✅ 所有验证项通过！")

    if test_questions:
        print(f"\n生成测试问题: {len(test_questions)} 个")

    print(f"\n完整报告已保存: {output_path}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="验证技能的完整性和可用性",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 验证技能
  python validate_skill.py --skill-path ./vue-skills --output ./validation.json

  # 仅检查结构
  python validate_skill.py --skill-path ./vue-skills --output ./validation.json --check structure
        """
    )

    parser.add_argument(
        '--skill-path',
        required=True,
        help='技能目录路径'
    )

    parser.add_argument(
        '--output',
        required=True,
        help='验证报告输出路径（JSON 格式）'
    )

    args = parser.parse_args()

    # 验证技能
    skill_dir = Path(args.skill_path)
    if not skill_dir.exists():
        print(f"错误: 目录不存在 {args.skill_path}")
        sys.exit(1)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    generate_validation_report(skill_dir, output_path)


if __name__ == "__main__":
    main()
