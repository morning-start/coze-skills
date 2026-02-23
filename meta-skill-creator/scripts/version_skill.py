#!/usr/bin/env python3
"""
技能版本管理器
用于处理技能版本迭代、差异对比和升级
"""

import json
import difflib
from typing import Dict, List, Any, Optional, Literal
from datetime import datetime


class SkillVersionManager:
    """技能版本管理器"""

    def __init__(self):
        self.version_pattern = r'^\d+\.\d+\.\d+$'

    def parse_version(self, version: str) -> tuple:
        """
        解析版本号

        参数:
            version: 版本号字符串 (如 "1.2.3")

        返回:
            (major, minor, patch) 元组
        """
        parts = version.split('.')
        if len(parts) != 3:
            raise ValueError(f"无效的版本号格式: {version}")

        return (int(parts[0]), int(parts[1]), int(parts[2]))

    def bump_version(
        self,
        current_version: str,
        bump_type: Literal["major", "minor", "patch"]
    ) -> str:
        """
        递增版本号

        参数:
            current_version: 当前版本号
            bump_type: 递增类型 (major/minor/patch)

        返回:
            新版本号
        """
        major, minor, patch = self.parse_version(current_version)

        if bump_type == "major":
            return f"{major + 1}.0.0"
        elif bump_type == "minor":
            return f"{major}.{minor + 1}.0"
        elif bump_type == "patch":
            return f"{major}.{minor}.{patch + 1}"
        else:
            raise ValueError(f"不支持的递增类型: {bump_type}")

    def compare_versions(self, v1: str, v2: str) -> str:
        """
        比较两个版本号

        参数:
            v1: 版本号1
            v2: 版本号2

        返回:
            ">", "<", "="
        """
        v1_tuple = self.parse_version(v1)
        v2_tuple = self.parse_version(v2)

        if v1_tuple > v2_tuple:
            return ">"
        elif v1_tuple < v2_tuple:
            return "<"
        else:
            return "="

    def diff_skills(
        self,
        old_skill: Dict[str, Any],
        new_skill: Dict[str, Any],
        detailed: bool = False
    ) -> Dict[str, Any]:
        """
        对比两个技能版本的差异

        参数:
            old_skill: 旧版本技能定义
            new_skill: 新版本技能定义
            detailed: 是否生成详细差异

        返回:
            差异报告
        """
        diff_report = {
            "version_change": {
                "old": old_skill.get("version", "unknown"),
                "new": new_skill.get("version", "unknown")
            },
            "changes": {
                "added": [],
                "removed": [],
                "modified": []
            },
            "impact": "unknown"
        }

        # 对比能力变化
        old_caps = set(old_skill.get("metadata", {}).get("capabilities", []))
        new_caps = set(new_skill.get("metadata", {}).get("capabilities", []))

        diff_report["changes"]["added"].extend(list(new_caps - old_caps))
        diff_report["changes"]["removed"].extend(list(old_caps - new_caps))

        # 对比依赖变化
        old_deps = old_skill.get("dependency", {})
        new_deps = new_skill.get("dependency", {})

        if old_deps != new_deps:
            diff_report["changes"]["modified"].append("dependency")

        # 判断影响范围
        if diff_report["changes"]["removed"]:
            diff_report["impact"] = "breaking"
        elif diff_report["changes"]["added"]:
            diff_report["impact"] = "feature"
        else:
            diff_report["impact"] = "patch"

        # 详细差异
        if detailed:
            diff_report["detailed_diff"] = self._generate_text_diff(
                json.dumps(old_skill, indent=2, ensure_ascii=False),
                json.dumps(new_skill, indent=2, ensure_ascii=False)
            )

        return diff_report

    def _generate_text_diff(self, old_text: str, new_text: str) -> List[str]:
        """生成文本差异"""
        diff = difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile="old",
            tofile="new",
            lineterm=""
        )
        return list(diff)

    def create_version_log(
        self,
        version: str,
        changes: List[str],
        author: str = "system",
        notes: str = ""
    ) -> Dict[str, Any]:
        """
        创建版本日志

        参数:
            version: 版本号
            changes: 变更列表
            author: 作者
            notes: 备注说明

        返回:
            版本日志条目
        """
        return {
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "author": author,
            "changes": changes,
            "notes": notes
        }

    def generate_changelog(
        self,
        version_logs: List[Dict[str, Any]]
    ) -> str:
        """
        生成变更日志

        参数:
            version_logs: 版本日志列表

        返回:
            格式化的变更日志文本
        """
        lines = ["# Changelog\n"]

        for log in sorted(version_logs, key=lambda x: x["version"], reverse=True):
            lines.append(f"\n## {log['version']} ({log['timestamp'][:10]})")
            lines.append(f"作者: {log['author']}\n")

            for change in log.get("changes", []):
                lines.append(f"- {change}")

            if log.get("notes"):
                lines.append(f"\n备注: {log['notes']}")

        return "\n".join(lines)

    def suggest_version_bump(
        self,
        diff_report: Dict[str, Any]
    ) -> str:
        """
        根据差异报告建议版本递增类型

        参数:
            diff_report: 差异报告

        返回:
            建议的递增类型 (major/minor/patch)
        """
        impact = diff_report.get("impact", "patch")

        if impact == "breaking":
            return "major"
        elif impact == "feature":
            return "minor"
        else:
            return "patch"

    def upgrade_skill(
        self,
        skill_definition: str,
        target_version: str,
        changes: List[str],
        notes: str = ""
    ) -> str:
        """
        升级技能到指定版本

        参数:
            skill_definition: 当前技能定义（SKILL.md 内容）
            target_version: 目标版本号
            changes: 变更列表
            notes: 备注说明

        返回:
            更新后的技能定义（包含版本元数据）
        """
        # 解析当前内容
        lines = skill_definition.split('\n')
        yaml_end = -1

        # 查找 YAML 前言区结束位置
        for i, line in enumerate(lines):
            if line.strip() == '---' and i > 0:
                yaml_end = i
                break

        if yaml_end == -1:
            raise ValueError("无效的技能定义格式")

        # 插入版本信息到 YAML 前言区
        version_line = f'version: "{target_version}"'
        changelog_line = f'changelog: {json.dumps(changes, ensure_ascii=False)}'

        # 在第二个 --- 之前插入版本信息
        new_lines = lines[:yaml_end]
        new_lines.append(version_line)
        new_lines.append(changelog_line)
        new_lines.extend(lines[yaml_end:])

        return '\n'.join(new_lines)

    def analyze_version_history(
        self,
        version_logs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        分析版本历史

        参数:
            version_logs: 版本日志列表

        返回:
            分析报告
        """
        if not version_logs:
            return {
                "total_versions": 0,
                "evolution_trend": "stable"
            }

        total_versions = len(version_logs)
        latest_version = max(version_logs, key=lambda x: x["version"])["version"]

        # 分析变更趋势
        major_changes = sum(1 for log in version_logs if log.get("impact") == "breaking")
        minor_changes = sum(1 for log in version_logs if log.get("impact") == "feature")
        patch_changes = sum(1 for log in version_logs if log.get("impact") == "patch")

        trend = "stable"
        if major_changes > total_versions / 3:
            trend = "volatile"
        elif minor_changes > total_versions / 2:
            trend = "rapid_evolution"

        return {
            "total_versions": total_versions,
            "latest_version": latest_version,
            "breakdown": {
                "major": major_changes,
                "minor": minor_changes,
                "patch": patch_changes
            },
            "evolution_trend": trend
        }


if __name__ == "__main__":
    # 示例用法
    manager = SkillVersionManager()

    # 版本递增
    current_version = "1.2.3"
    print(f"当前版本: {current_version}")
    print(f"Patch 递增: {manager.bump_version(current_version, 'patch')}")
    print(f"Minor 递增: {manager.bump_version(current_version, 'minor')}")
    print(f"Major 递增: {manager.bump_version(current_version, 'major')}")

    # 版本对比
    print(f"\n版本比较: 1.2.3 vs 1.2.4 = {manager.compare_versions('1.2.3', '1.2.4')}")

    # 差异分析
    old_skill = {
        "name": "data-processor",
        "version": "1.0.0",
        "metadata": {"capabilities": ["数据清洗"]},
        "dependency": {"python": ["pandas>=1.0.0"]}
    }

    new_skill = {
        "name": "data-processor",
        "version": "2.0.0",
        "metadata": {"capabilities": ["数据清洗", "数据验证", "格式转换"]},
        "dependency": {"python": ["pandas>=2.0.0"]}
    }

    diff = manager.diff_skills(old_skill, new_skill, detailed=False)
    print("\n=== 差异分析 ===")
    print(json.dumps(diff, indent=2, ensure_ascii=False))
