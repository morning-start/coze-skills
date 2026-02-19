#!/usr/bin/env python3
"""
项目复杂度评估脚本
功能：分析项目复杂度，推荐 Wiki 文件夹结构
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple


class ComplexityEvaluator:
    """项目复杂度评估器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.result = {
            'complexity_score': 0,
            'complexity_level': '',
            'dimensions': {},
            'recommendation': '',
            'structure_type': ''
        }
    
    def evaluate(self) -> Dict:
        """执行复杂度评估"""
        print(f"评估项目复杂度: {self.project_path}")
        
        if not self.project_path.exists():
            raise FileNotFoundError(f"项目路径不存在: {self.project_path}")
        
        # 评估各个维度
        self._evaluate_file_count()
        self._evaluate_module_count()
        self._evaluate_dependency_complexity()
        self._evaluate_framework_count()
        self._evaluate_directory_depth()
        
        # 计算总分
        self._calculate_score()
        
        # 生成推荐
        self._generate_recommendation()
        
        return self.result
    
    def _evaluate_file_count(self):
        """评估文件数量"""
        all_files = list(self.project_path.rglob('*'))
        all_files = [f for f in all_files if f.is_file()]
        
        # 过滤掉虚拟环境和临时文件
        skip_patterns = ['node_modules', 'venv', '__pycache__', '.git', 'dist', 'build', '.tox', '.pytest_cache']
        filtered_files = [f for f in all_files if not any(p in str(f) for p in skip_patterns)]
        
        file_count = len(filtered_files)
        
        if file_count < 50:
            score = 0
            level = "低"
        elif file_count < 200:
            score = 1
            level = "中"
        else:
            score = 2
            level = "高"
        
        self.result['dimensions']['file_count'] = {
            'value': file_count,
            'score': score,
            'level': level
        }
        
        print(f"  文件数量: {file_count} ({level}) - {score} 分")
    
    def _evaluate_module_count(self):
        """评估模块数量"""
        # 统计主要目录作为模块数量
        directories = [d for d in self.project_path.iterdir() if d.is_dir()]
        skip_dirs = ['.', '..', '.git', 'node_modules', 'venv', '__pycache__', 'dist', 'build']
        
        modules = [d for d in directories if d.name not in skip_dirs and not d.name.startswith('.')]
        module_count = len(modules)
        
        if module_count < 5:
            score = 0
            level = "低"
        elif module_count < 15:
            score = 1
            level = "中"
        else:
            score = 2
            level = "高"
        
        self.result['dimensions']['module_count'] = {
            'value': module_count,
            'score': score,
            'level': level
        }
        
        print(f"  模块数量: {module_count} ({level}) - {score} 分")
    
    def _evaluate_dependency_complexity(self):
        """评估依赖复杂度"""
        dependency_count = 0
        
        # 检查常见的依赖文件
        dep_files = {
            'package.json': 'node_modules',
            'requirements.txt': 'pip',
            'pom.xml': 'maven',
            'build.gradle': 'gradle',
            'go.mod': 'go modules',
            'Cargo.toml': 'cargo'
        }
        
        for dep_file, tool in dep_files.items():
            file_path = self.project_path / dep_file
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    # 简单统计行数作为依赖数量的估算
                    lines = [line for line in content.split('\n') if line.strip() and not line.startswith('#')]
                    dependency_count += len(lines)
                except:
                    pass
        
        if dependency_count < 10:
            score = 0
            level = "低"
        elif dependency_count < 30:
            score = 1
            level = "中"
        else:
            score = 2
            level = "高"
        
        self.result['dimensions']['dependency_complexity'] = {
            'value': dependency_count,
            'score': score,
            'level': level
        }
        
        print(f"  依赖复杂度: {dependency_count} 个依赖 ({level}) - {score} 分")
    
    def _evaluate_framework_count(self):
        """评估框架数量"""
        framework_count = 0
        
        # 读取项目分析结果（如果存在）
        analysis_file = self.project_path / 'project-analysis.json'
        if analysis_file.exists():
            try:
                with open(analysis_file, 'r') as f:
                    analysis = json.load(f)
                framework_count = len(analysis.get('frameworks', []))
            except:
                pass
        else:
            # 简单推断
            frameworks = ['Flask', 'Django', 'FastAPI', 'React', 'Vue', 'Svelte', 'Spring Boot', 'Electron', 'Flutter']
            for framework in frameworks:
                for file in self.project_path.rglob('*'):
                    if file.is_file() and framework.lower() in file.read_text(encoding='utf-8', errors='ignore').lower():
                        framework_count += 1
                        break
        
        if framework_count <= 1:
            score = 0
            level = "低"
        elif framework_count <= 3:
            score = 1
            level = "中"
        else:
            score = 2
            level = "高"
        
        self.result['dimensions']['framework_count'] = {
            'value': framework_count,
            'score': score,
            'level': level
        }
        
        print(f"  框架数量: {framework_count} ({level}) - {score} 分")
    
    def _evaluate_directory_depth(self):
        """评估目录深度"""
        max_depth = 0
        
        for root, dirs, files in os.walk(self.project_path):
            # 过滤掉虚拟环境
            if any(skip in root for skip in ['node_modules', 'venv', '__pycache__', '.git', 'dist', 'build']):
                continue
            
            depth = root.count(os.sep) - str(self.project_path).count(os.sep)
            if depth > max_depth:
                max_depth = depth
        
        if max_depth < 3:
            score = 0
            level = "浅"
        elif max_depth < 5:
            score = 1
            level = "中"
        else:
            score = 2
            level = "深"
        
        self.result['dimensions']['directory_depth'] = {
            'value': max_depth,
            'score': score,
            'level': level
        }
        
        print(f"  目录深度: {max_depth} 层 ({level}) - {score} 分")
    
    def _calculate_score(self):
        """计算总分"""
        total_score = 0
        for dim_name, dim_data in self.result['dimensions'].items():
            total_score += dim_data['score']
        
        self.result['complexity_score'] = total_score
        
        print(f"\n  总分: {total_score} / 10 分")
    
    def _generate_recommendation(self):
        """生成推荐"""
        score = self.result['complexity_score']
        
        if score <= 3:
            level = "简单"
            structure_type = "flat"
            recommendation = (
                "项目复杂度较低，建议使用**平铺结构**。\n"
                "所有文档放在 wiki/ 目录下，不创建子文件夹。"
            )
        elif score <= 7:
            level = "中等"
            structure_type = "hierarchical"
            recommendation = (
                "项目复杂度中等，建议使用**分层结构**。\n"
                "按文档类型分类（概览、开发指南、API、部署等），每个类别一个子文件夹。"
            )
        else:
            level = "复杂"
            structure_type = "hierarchical_with_modules"
            recommendation = (
                "项目复杂度较高，建议使用**分层结构 + 模块文件夹**。\n"
                "按文档类型分类，同时为复杂模块创建独立的文件夹。"
            )
        
        self.result['complexity_level'] = level
        self.result['structure_type'] = structure_type
        self.result['recommendation'] = recommendation
        
        print(f"  复杂度等级: {level}")
        print(f"  推荐结构: {structure_type}")
        print(f"\n  推荐建议:\n  {recommendation}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='项目复杂度评估工具')
    parser.add_argument('--path', type=str, default='.', help='项目路径')
    
    args = parser.parse_args()
    
    evaluator = ComplexityEvaluator(args.path)
    result = evaluator.evaluate()
    
    # 保存结果
    output_file = Path(args.path) / 'complexity-analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n评估完成！结果已保存到: {output_file}")


if __name__ == '__main__':
    main()
