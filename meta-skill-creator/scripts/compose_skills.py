#!/usr/bin/env python3
"""
技能组合处理器
用于组合、嵌套和拼接多个技能
"""

import json
import copy
from typing import Dict, List, Any, Optional, Literal


class SkillComposer:
    """技能组合器"""

    def __init__(self):
        self.composition_modes = {
            "sequential": "顺序组合",
            "parallel": "并行组合",
            "nested": "嵌套组合",
            "pipeline": "流水线组合"
        }

    def validate_skills(self, skills: List[Dict[str, Any]]) -> List[str]:
        """
        验证技能列表的有效性

        参数:
            skills: 技能定义列表

        返回:
            验证错误列表（空列表表示验证通过）
        """
        errors = []

        for idx, skill in enumerate(skills):
            if not isinstance(skill, dict):
                errors.append(f"技能 {idx} 不是字典类型")
                continue

            if "name" not in skill:
                errors.append(f"技能 {idx} 缺少 name 字段")

            if "capabilities" not in skill and "description" not in skill:
                errors.append(f"技能 {idx} 缺少描述信息")

        return errors

    def compose_sequential(
        self,
        skills: List[Dict[str, Any]],
        input_mapping: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        顺序组合多个技能

        参数:
            skills: 技能列表（按执行顺序）
            input_mapping: 技能间输入输出映射（可选）

        返回:
            组合后的技能定义
        """
        if len(skills) < 2:
            raise ValueError("顺序组合至少需要2个技能")

        errors = self.validate_skills(skills)
        if errors:
            raise ValueError(f"技能验证失败: {errors}")

        # 提取所有技能名称
        skill_names = [skill.get("name", f"skill_{i}") for i, skill in enumerate(skills)]

        # 构建组合技能的元数据
        composed_skill = {
            "name": "-".join(skill_names[:3]) + "-composed",  # 避免名称过长
            "description": f"组合技能: 顺序执行 {' -> '.join(skill_names)}",
            "metadata": {
                "composition_type": "sequential",
                "component_skills": skill_names,
                "input_mapping": input_mapping or {},
                "capabilities": self._merge_capabilities(skills)
            }
        }

        return composed_skill

    def compose_parallel(
        self,
        skills: List[Dict[str, Any]],
        output_merge_strategy: Literal["merge", "concatenate", "first"] = "merge"
    ) -> Dict[str, Any]:
        """
        并行组合多个技能

        参数:
            skills: 技能列表
            output_merge_strategy: 输出合并策略

        返回:
            组合后的技能定义
        """
        if len(skills) < 2:
            raise ValueError("并行组合至少需要2个技能")

        errors = self.validate_skills(skills)
        if errors:
            raise ValueError(f"技能验证失败: {errors}")

        skill_names = [skill.get("name", f"skill_{i}") for i, skill in enumerate(skills)]

        composed_skill = {
            "name": "-".join(skill_names[:3]) + "-parallel",
            "description": f"组合技能: 并行执行 {' + '.join(skill_names)}",
            "metadata": {
                "composition_type": "parallel",
                "component_skills": skill_names,
                "output_merge_strategy": output_merge_strategy,
                "capabilities": self._merge_capabilities(skills)
            }
        }

        return composed_skill

    def compose_nested(
        self,
        parent_skill: Dict[str, Any],
        sub_skills: List[Dict[str, Any]],
        integration_points: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        嵌套组合：将子技能嵌入父技能

        参数:
            parent_skill: 父技能定义
            sub_skills: 子技能列表
            integration_points: 集成点列表（父技能中调用子技能的位置）

        返回:
            嵌套后的技能定义
        """
        if not sub_skills:
            raise ValueError("嵌套组合至少需要1个子技能")

        sub_skill_names = [skill.get("name", f"sub_skill_{i}") for i, skill in enumerate(sub_skills)]

        # 深度复制父技能
        nested_skill = copy.deepcopy(parent_skill)

        # 添加嵌套元数据
        if "metadata" not in nested_skill:
            nested_skill["metadata"] = {}

        nested_skill["metadata"].update({
            "composition_type": "nested",
            "sub_skills": sub_skill_names,
            "integration_points": integration_points or []
        })

        # 合并能力
        parent_caps = parent_skill.get("metadata", {}).get("capabilities", [])
        sub_caps = []
        for skill in sub_skills:
            sub_caps.extend(skill.get("metadata", {}).get("capabilities", []))

        nested_skill["metadata"]["capabilities"] = list(set(parent_caps + sub_caps))

        return nested_skill

    def compose_pipeline(
        self,
        skills: List[Dict[str, Any]],
        data_flow: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        流水线组合：定义数据流向和转换规则

        参数:
            skills: 技能列表
            data_flow: 数据流定义（输入 -> 转换 -> 输出）

        返回:
            流水线技能定义
        """
        if len(skills) < 2:
            raise ValueError("流水线组合至少需要2个技能")

        skill_names = [skill.get("name", f"skill_{i}") for i, skill in enumerate(skills)]

        composed_skill = {
            "name": "-".join(skill_names[:3]) + "-pipeline",
            "description": f"流水线技能: {' | '.join(skill_names)}",
            "metadata": {
                "composition_type": "pipeline",
                "component_skills": skill_names,
                "data_flow": data_flow or {},
                "capabilities": self._merge_capabilities(skills)
            }
        }

        return composed_skill

    def _merge_capabilities(self, skills: List[Dict[str, Any]]) -> List[str]:
        """合并多个技能的能力列表"""
        all_caps = []
        for skill in skills:
            caps = skill.get("metadata", {}).get("capabilities", [])
            all_caps.extend(caps)
        return list(set(all_caps))  # 去重

    def generate_composition_plan(
        self,
        composition_mode: str,
        skills: List[Dict[str, Any]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        生成组合方案

        参数:
            composition_mode: 组合模式（sequential/parallel/nested/pipeline）
            skills: 技能列表
            **kwargs: 组合参数

        返回:
            组合方案
        """
        if composition_mode not in self.composition_modes:
            raise ValueError(f"不支持的组合模式: {composition_mode}")

        if composition_mode == "sequential":
            return self.compose_sequential(skills, kwargs.get("input_mapping"))
        elif composition_mode == "parallel":
            return self.compose_parallel(skills, kwargs.get("output_merge_strategy", "merge"))
        elif composition_mode == "nested":
            return self.compose_nested(kwargs["parent_skill"], skills, kwargs.get("integration_points"))
        elif composition_mode == "pipeline":
            return self.compose_pipeline(skills, kwargs.get("data_flow"))

    def analyze_compatibility(
        self,
        skill1: Dict[str, Any],
        skill2: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        分析两个技能的兼容性

        参数:
            skill1: 技能1定义
            skill2: 技能2定义

        返回:
            兼容性分析结果
        """
        analysis = {
            "compatible": True,
            "warnings": [],
            "recommendations": []
        }

        # 检查依赖冲突
        deps1 = skill1.get("dependency", {}).get("python", [])
        deps2 = skill2.get("dependency", {}).get("python", [])

        # 简单检查（实际场景需要更复杂的依赖解析）
        for dep1 in deps1:
            for dep2 in deps2:
                pkg1 = dep1.split("==")[0].split(">=")[0]
                pkg2 = dep2.split("==")[0].split(">=")[0]
                if pkg1 == pkg2 and dep1 != dep2:
                    analysis["warnings"].append(f"依赖冲突: {pkg1} 版本不一致 ({dep1} vs {dep2})")
                    analysis["compatible"] = False

        # 能力重复检查
        caps1 = set(skill1.get("metadata", {}).get("capabilities", []))
        caps2 = set(skill2.get("metadata", {}).get("capabilities", []))
        overlap = caps1 & caps2

        if overlap:
            analysis["recommendations"].append(f"能力重叠: {', '.join(overlap)}")

        return analysis


if __name__ == "__main__":
    # 示例用法
    composer = SkillComposer()

    # 示例技能
    skill1 = {
        "name": "data-cleaner",
        "description": "数据清洗",
        "metadata": {"capabilities": ["数据清洗", "去重"]},
        "dependency": {"python": ["pandas>=1.5.0"]}
    }

    skill2 = {
        "name": "data-validator",
        "description": "数据验证",
        "metadata": {"capabilities": ["数据验证", "格式检查"]},
        "dependency": {"python": ["pyyaml>=6.0"]}
    }

    # 顺序组合
    sequential = composer.compose_sequential([skill1, skill2])
    print("=== 顺序组合 ===")
    print(json.dumps(sequential, indent=2, ensure_ascii=False))

    # 兼容性分析
    compatibility = composer.analyze_compatibility(skill1, skill2)
    print("\n=== 兼容性分析 ===")
    print(json.dumps(compatibility, indent=2, ensure_ascii=False))
