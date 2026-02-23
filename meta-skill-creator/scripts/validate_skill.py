#!/usr/bin/env python3
"""
技能验证器
用于验证技能格式合规性和安全规则
"""

import yaml
import re
from typing import Dict, List, Any, Optional


class SkillValidator:
    """技能验证器"""

    def __init__(self):
        self.errors = []
        self.warnings = []

        # 安全规则
        self.security_rules = {
            "forbidden_keywords": ["token", "secret", "password", "api_key", "credential"],
            "safe_domains": [],  # 允许调用的第三方域名白名单
            "max_description_length": 150,
            "max_body_length": 500
        }

    def validate(
        self,
        skill_definition: str,
        check_security: bool = True,
        strict_mode: bool = False
    ) -> Dict[str, Any]:
        """
        验证技能定义

        参数:
            skill_definition: SKILL.md 文件内容
            check_security: 是否检查安全规则
            strict_mode: 严格模式（警告视为错误）

        返回:
            验证结果
        """
        self.errors = []
        self.warnings = []

        # 分离 YAML 前言区和正文
        yaml_section, body_section = self._parse_skill_file(skill_definition)

        if yaml_section is None:
            return {
                "valid": False,
                "errors": ["无法解析 YAML 前言区"],
                "warnings": self.warnings
            }

        # 验证 YAML 前言区
        self._validate_yaml_section(yaml_section)

        # 验证正文
        self._validate_body_section(body_section)

        # 安全检查
        if check_security:
            self._check_security(skill_definition)

        # 判断是否有效
        valid = len(self.errors) == 0
        if strict_mode and self.warnings:
            valid = False
            self.errors.extend(self.warnings)

        return {
            "valid": valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "summary": {
                "error_count": len(self.errors),
                "warning_count": len(self.warnings)
            }
        }

    def _parse_skill_file(self, content: str) -> tuple:
        """解析 SKILL.md 文件，分离 YAML 和正文"""
        lines = content.split('\n')

        # 查找第一个 ---
        yaml_start = -1
        yaml_end = -1

        for i, line in enumerate(lines):
            if line.strip() == '---' and yaml_start == -1:
                yaml_start = i
            elif line.strip() == '---' and yaml_start != -1:
                yaml_end = i
                break

        if yaml_start == -1 or yaml_end == -1:
            self.errors.append("缺少有效的 YAML 前言区（需要用 --- 包裹）")
            return None, content

        yaml_content = '\n'.join(lines[yaml_start+1:yaml_end])
        body_content = '\n'.join(lines[yaml_end+1:])

        try:
            yaml_data = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            self.errors.append(f"YAML 解析失败: {str(e)}")
            return None, body_content

        return yaml_data, body_content

    def _validate_yaml_section(self, yaml_data: Dict[str, Any]):
        """验证 YAML 前言区"""
        # 必需字段
        required_fields = ["name", "description"]
        for field in required_fields:
            if field not in yaml_data:
                self.errors.append(f"YAML 前言区缺少必需字段: {field}")

        # 验证 name
        if "name" in yaml_data:
            name = yaml_data["name"]
            if not isinstance(name, str):
                self.errors.append("name 必须是字符串")
            elif not name.replace('-', '').isalnum() or not name[0].isalpha():
                self.errors.append("name 必须为小写字母、数字和连字符，且以字母开头")
            elif name.endswith('-skill'):
                self.errors.append("name 不应以 -skill 结尾")

        # 验证 description
        if "description" in yaml_data:
            desc = yaml_data["description"]
            if not isinstance(desc, str):
                self.errors.append("description 必须是字符串")
            elif len(desc) > self.security_rules["max_description_length"]:
                self.warnings.append(f"description 长度超过推荐值 ({len(desc)} > {self.security_rules['max_description_length']})")

        # 验证 dependency
        if "dependency" in yaml_data:
            dep = yaml_data["dependency"]
            if not isinstance(dep, dict):
                self.errors.append("dependency 必须是字典")
            else:
                if "python" in dep:
                    if not isinstance(dep["python"], list):
                        self.errors.append("dependency.python 必须是列表")
                    else:
                        for pkg in dep["python"]:
                            if not isinstance(pkg, str):
                                self.warnings.append(f"依赖包格式不正确: {pkg}")

                if "system" in dep:
                    if not isinstance(dep["system"], list):
                        self.errors.append("dependency.system 必须是列表")

    def _validate_body_section(self, body: str):
        """验证正文"""
        if not body or body.strip() == '':
            self.warnings.append("技能正文为空")

        # 检查行数
        line_count = len([line for line in body.split('\n') if line.strip()])
        if line_count > self.security_rules["max_body_length"]:
            self.warnings.append(f"正文体量较大 ({line_count} 行)，建议将细节拆入 references/")

        # 检查是否包含必要的章节
        required_sections = ["任务目标", "操作步骤"]
        for section in required_sections:
            if section not in body:
                self.warnings.append(f"建议包含 '{section}' 章节")

    def _check_security(self, content: str):
        """安全检查"""
        # 检查硬编码凭证
        credential_patterns = [
            r'(?:api[_-]?key|token|secret|password)\s*[:=]\s*["\']?[\w\-]{16,}',
            r'(?:api[_-]?key|token|secret|password)\s*[:=]\s*["\']?sk-[a-zA-Z0-9]{32,}'
        ]

        for pattern in credential_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                self.errors.append(f"安全警告: 检测到可能的硬编码凭证 - {match.group()[:20]}...")

        # 检查危险关键词
        for keyword in self.security_rules["forbidden_keywords"]:
            # 排除注释中的出现
            for line in content.split('\n'):
                if not line.strip().startswith('#') and keyword.lower() in line.lower():
                    # 检查是否在代码上下文中
                    if '=' in line or ':' in line or '"' in line or "'" in line:
                        self.warnings.append(f"检测到敏感关键词 '{keyword}'，请确保未硬编码凭证")

    def check_composition_readiness(self, skill_definition: str) -> Dict[str, Any]:
        """
        检查技能是否准备好用于组合

        参数:
            skill_definition: SKILL.md 文件内容

        返回:
            组合准备度报告
        """
        report = {
            "ready": True,
            "score": 0,
            "issues": [],
            "recommendations": []
        }

        yaml_section, body_section = self._parse_skill_file(skill_definition)
        if yaml_section is None:
            report["ready"] = False
            report["issues"].append("无法解析 YAML 前言区")
            return report

        # 评分标准
        score = 0

        # 1. 有清晰的输入输出定义
        if "input" in body_section.lower() and "output" in body_section.lower():
            score += 20
        else:
            report["recommendations"].append("建议在正文中明确定义输入输出格式")

        # 2. 能力列表完整
        if "metadata" in yaml_section and "capabilities" in yaml_section.get("metadata", {}):
            score += 30
        else:
            report["recommendations"].append("建议在 metadata 中定义 capabilities 列表")

        # 3. 无全局状态依赖
        if "global" not in body_section.lower() and "global" not in str(yaml_section).lower():
            score += 20
        else:
            report["issues"].append("检测到可能的全局状态依赖")

        # 4. 接口标准化
        if "参数" in body_section or "parameter" in body_section.lower():
            score += 30
        else:
            report["recommendations"].append("建议明确参数定义")

        report["score"] = score
        report["ready"] = score >= 70

        return report


if __name__ == "__main__":
    # 示例用法
    validator = SkillValidator()

    # 测试用例
    test_skill = """---
name: test-skill
description: 这是一个测试技能
dependency:
  python:
    - pyyaml>=6.0
---

# Test Skill

## 任务目标
- 本 Skill 用于: 测试
- 能力包含: 测试能力
- 触发条件: 测试触发

## 操作步骤
- 标准流程:
  1. 步骤1
  2. 步骤2
"""

    result = validator.validate(test_skill)
    print("=== 验证结果 ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 组合准备度检查
    readiness = validator.check_composition_readiness(test_skill)
    print("\n=== 组合准备度 ===")
    print(json.dumps(readiness, indent=2, ensure_ascii=False))
