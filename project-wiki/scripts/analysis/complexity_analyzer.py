#!/usr/bin/env python3
"""
项目复杂度分析器

自主识别项目结构的复杂度，支持多维度评估
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class ComplexityMetrics:
    """复杂度指标"""
    # 基础指标
    total_files: int
    total_lines: int
    module_count: int
    
    # 依赖指标
    dependency_count: int
    circular_dependency_count: int
    max_dependency_depth: int
    
    # 技术栈指标
    language_count: int
    framework_count: int
    
    # 架构指标
    layer_count: int  # 分层数量
    service_count: int  # 服务数量
    api_count: int  # API 数量
    
    # 代码质量指标
    avg_file_lines: int
    max_file_lines: int
    complexity_score: float  # 综合复杂度分数


@dataclass
class ComplexityAnalysis:
    """复杂度分析结果"""
    project_path: str
    metrics: ComplexityMetrics
    complexity_level: str  # simple, medium, complex, ultra-complex
    structure_recommendation: str
    reason: str
    suggestions: List[str]


class ComplexityAnalyzer:
    """复杂度分析器"""
    
    # 复杂度阈值
    THRESHOLDS = {
        "simple": {
            "max_modules": 5,
            "max_files": 20,
            "max_total_lines": 5000,
            "max_dependencies": 10,
            "max_languages": 1,
            "max_frameworks": 1
        },
        "medium": {
            "max_modules": 20,
            "max_files": 100,
            "max_total_lines": 20000,
            "max_dependencies": 50,
            "max_languages": 2,
            "max_frameworks": 2
        },
        "complex": {
            "max_modules": 50,
            "max_files": 500,
            "max_total_lines": 100000,
            "max_dependencies": 200,
            "max_languages": 3,
            "max_frameworks": 3
        }
    }
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.exclude_dirs = {'.git', '.idea', '.vscode', '__pycache__', 'node_modules', 'venv', 'env', 'dist', 'build', '.cache'}
        self.exclude_files = {'.pyc', '.class', '.jar', '.dll', '.exe', '.log'}
    
    def analyze(self) -> ComplexityAnalysis:
        """分析项目复杂度"""
        # 计算指标
        metrics = self._calculate_metrics()
        
        # 判断复杂度等级
        complexity_level = self._determine_complexity_level(metrics)
        
        # 生成结构推荐
        structure_recommendation, reason = self._recommend_structure(complexity_level, metrics)
        
        # 生成建议
        suggestions = self._generate_suggestions(complexity_level, metrics)
        
        return ComplexityAnalysis(
            project_path=str(self.project_path),
            metrics=metrics,
            complexity_level=complexity_level,
            structure_recommendation=structure_recommendation,
            reason=reason,
            suggestions=suggestions
        )
    
    def _calculate_metrics(self) -> ComplexityMetrics:
        """计算复杂度指标"""
        # 基础指标
        total_files = 0
        total_lines = 0
        module_count = 0
        file_lines_list = []
        
        # 依赖指标
        dependencies = set()
        max_dependency_depth = 0
        circular_dependencies = 0
        
        # 技术栈指标
        languages = set()
        frameworks = set()
        
        # 架构指标
        layers = set()
        services = set()
        apis = set()
        
        # 扫描项目
        for root, dirs, files in os.walk(self.project_path):
            # 排除目录
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            
            root_path = Path(root)
            
            # 识别模块
            if self._is_module_dir(root_path):
                module_count += 1
            
            # 识别层级
            layer = self._identify_layer(root_path)
            if layer:
                layers.add(layer)
            
            # 识别服务
            service = self._identify_service(root_path)
            if service:
                services.add(service)
            
            for file in files:
                file_path = root_path / file
                if file_path.suffix in self.exclude_files:
                    continue
                
                # 统计文件
                total_files += 1
                
                # 统计行数
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                        total_lines += lines
                        file_lines_list.append(lines)
                except:
                    pass
                
                # 识别语言
                language = self._identify_language(file_path)
                if language:
                    languages.add(language)
                
                # 识别框架
                framework = self._identify_framework(file_path)
                if framework:
                    frameworks.add(framework)
                
                # 识别 API
                if self._is_api_file(file_path):
                    apis.add(file_path.stem)
                
                # 分析依赖
                file_deps = self._analyze_dependencies(file_path)
                dependencies.update(file_deps)
        
        # 计算平均和最大文件行数
        avg_file_lines = sum(file_lines_list) / len(file_lines_list) if file_lines_list else 0
        max_file_lines = max(file_lines_list) if file_lines_list else 0
        
        # 计算综合复杂度分数
        complexity_score = self._calculate_complexity_score(
            total_files, total_lines, module_count, len(dependencies),
            len(languages), len(frameworks), len(layers), len(services), len(apis)
        )
        
        return ComplexityMetrics(
            total_files=total_files,
            total_lines=total_lines,
            module_count=module_count,
            dependency_count=len(dependencies),
            circular_dependency_count=circular_dependencies,
            max_dependency_depth=max_dependency_depth,
            language_count=len(languages),
            framework_count=len(frameworks),
            layer_count=len(layers),
            service_count=len(services),
            api_count=len(apis),
            avg_file_lines=int(avg_file_lines),
            max_file_lines=max_file_lines,
            complexity_score=complexity_score
        )
    
    def _is_module_dir(self, path: Path) -> bool:
        """判断是否是模块目录"""
        # 检查是否有 init 文件（Python）
        if (path / '__init__.py').exists():
            return True
        
        # 检查是否有 package.json（Node.js）
        if (path / 'package.json').exists():
            return True
        
        # 检查是否有 go.mod（Go）
        if (path / 'go.mod').exists():
            return True
        
        # 检查是否是独立的功能目录（包含多个代码文件）
        code_files = [f for f in path.glob('*') if f.is_file() and f.suffix in {'.py', '.js', '.ts', '.java', '.go'}]
        if len(code_files) >= 3:
            return True
        
        return False
    
    def _identify_layer(self, path: Path) -> Optional[str]:
        """识别技术分层"""
        path_str = str(path).lower()
        
        if 'controller' in path_str or 'api' in path_str or 'handler' in path_str:
            return 'controller'
        elif 'service' in path_str or 'business' in path_str:
            return 'service'
        elif 'repository' in path_str or 'dao' in path_str or 'model' in path_str:
            return 'repository'
        elif 'entity' in path_str or 'domain' in path_str:
            return 'domain'
        elif 'util' in path_str or 'helper' in path_str or 'common' in path_str:
            return 'util'
        
        return None
    
    def _identify_service(self, path: Path) -> Optional[str]:
        """识别服务"""
        path_str = str(path).lower()
        
        # 检查是否是微服务目录
        if 'service' in path_str or 'microservice' in path_str:
            return path.name
        
        # 检查是否有服务配置文件
        if (path / 'docker-compose.yml').exists() or (path / 'Dockerfile').exists():
            return path.name
        
        return None
    
    def _identify_language(self, path: Path) -> Optional[str]:
        """识别编程语言"""
        ext_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.cs': 'C#',
            '.cpp': 'C++',
            '.c': 'C',
            '.rs': 'Rust',
            '.kt': 'Kotlin',
            '.swift': 'Swift'
        }
        
        return ext_map.get(path.suffix)
    
    def _identify_framework(self, path: Path) -> Optional[str]:
        """识别框架"""
        content = ""
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            pass
        
        # 检查常见框架
        frameworks = {
            'Django': ['from django', 'import django'],
            'Flask': ['from flask', 'import flask'],
            'FastAPI': ['from fastapi', 'import fastapi'],
            'Spring Boot': ['org.springframework.boot', 'spring-boot'],
            'React': ['import React', 'from "react"'],
            'Vue': ['import Vue', 'from "vue"'],
            'Express': ['require("express")', 'import express'],
            'Gin': ['github.com/gin-gonic/gin', 'import "github.com/gin-gonic/gin"']
        }
        
        for framework, keywords in frameworks.items():
            if any(keyword in content for keyword in keywords):
                return framework
        
        return None
    
    def _is_api_file(self, path: Path) -> bool:
        """判断是否是 API 文件"""
        filename = path.name.lower()
        return 'api' in filename or 'controller' in filename or 'handler' in filename
    
    def _analyze_dependencies(self, path: Path) -> List[str]:
        """分析文件依赖"""
        dependencies = []
        
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # 分析 Python import
                if path.suffix == '.py':
                    import os as _os
                    import re
                    import_pattern = re.compile(r'^\s*(?:from\s+(\S+)|import\s+(\S+))')
                    for line in content.split('\n'):
                        match = import_pattern.match(line)
                        if match:
                            dep = match.group(1) or match.group(2)
                            if dep and not dep.startswith('.'):
                                dependencies.append(dep)
                
                # 分析 JavaScript import
                elif path.suffix in ['.js', '.ts']:
                    import re
                    import_pattern = re.compile(r'(?:require\(["\']([^"\']+)["\']\)|import\s+.*from\s+["\']([^"\']+)["\'])')
                    for line in content.split('\n'):
                        match = import_pattern.search(line)
                        if match:
                            dep = match.group(1) or match.group(2)
                            if dep and not dep.startswith('.'):
                                dependencies.append(dep)
        except:
            pass
        
        return dependencies
    
    def _calculate_complexity_score(self, files, lines, modules, deps, langs, frameworks, layers, services, apis) -> float:
        """计算综合复杂度分数"""
        # 归一化各项指标
        norm_files = min(files / 1000, 1.0)
        norm_lines = min(lines / 100000, 1.0)
        norm_modules = min(modules / 50, 1.0)
        norm_deps = min(deps / 200, 1.0)
        norm_langs = min(langs / 5, 1.0)
        norm_frameworks = min(frameworks / 5, 1.0)
        norm_layers = min(layers / 5, 1.0)
        norm_services = min(services / 20, 1.0)
        norm_apis = min(apis / 50, 1.0)
        
        # 加权计算
        weights = {
            'files': 0.15,
            'lines': 0.10,
            'modules': 0.20,
            'deps': 0.15,
            'langs': 0.05,
            'frameworks': 0.10,
            'layers': 0.10,
            'services': 0.10,
            'apis': 0.05
        }
        
        score = (
            norm_files * weights['files'] +
            norm_lines * weights['lines'] +
            norm_modules * weights['modules'] +
            norm_deps * weights['deps'] +
            norm_langs * weights['langs'] +
            norm_frameworks * weights['frameworks'] +
            norm_layers * weights['layers'] +
            norm_services * weights['services'] +
            norm_apis * weights['apis']
        )
        
        return round(score * 100, 2)
    
    def _determine_complexity_level(self, metrics: ComplexityMetrics) -> str:
        """确定复杂度等级"""
        # 检查是否满足简单项目标准
        if (metrics.module_count <= self.THRESHOLDS['simple']['max_modules'] and
            metrics.total_files <= self.THRESHOLDS['simple']['max_files'] and
            metrics.total_lines <= self.THRESHOLDS['simple']['max_total_lines']):
            return 'simple'
        
        # 检查是否满足中等项目标准
        elif (metrics.module_count <= self.THRESHOLDS['medium']['max_modules'] and
              metrics.total_files <= self.THRESHOLDS['medium']['max_files'] and
              metrics.total_lines <= self.THRESHOLDS['medium']['max_total_lines']):
            return 'medium'
        
        # 检查是否满足复杂项目标准
        elif (metrics.module_count <= self.THRESHOLDS['complex']['max_modules'] and
              metrics.total_files <= self.THRESHOLDS['complex']['max_files'] and
              metrics.total_lines <= self.THRESHOLDS['complex']['max_total_lines']):
            return 'complex'
        
        # 超复杂项目
        else:
            return 'ultra-complex'
    
    def _recommend_structure(self, complexity_level: str, metrics: ComplexityMetrics) -> Tuple[str, str]:
        """推荐结构类型"""
        recommendations = {
            'simple': ('flat', '项目规模较小，采用扁平结构更简单直接'),
            'medium': ('typed', '项目规模中等，按文档类型分组便于管理'),
            'complex': ('domain', '项目规模较大，按业务领域分组更清晰'),
            'ultra-complex': ('nested', '项目规模极大，需要多层嵌套结构')
        }
        
        structure, reason = recommendations.get(complexity_level, ('typed', ''))
        
        # 根据特定特征调整推荐
        if metrics.service_count >= 10:
            structure = 'microservice'
            reason = f'检测到 {metrics.service_count} 个服务，推荐微服务结构'
        elif metrics.layer_count >= 4:
            structure = 'layered'
            reason = f'检测到 {metrics.layer_count} 个技术分层，推荐分层结构'
        
        return structure, reason
    
    def _generate_suggestions(self, complexity_level: str, metrics: ComplexityMetrics) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        if complexity_level == 'simple':
            suggestions.append("项目结构简单，保持扁平化即可")
            suggestions.append("建议使用简单的文档目录：wiki/api-docs/、wiki/modules/")
        
        elif complexity_level == 'medium':
            suggestions.append("项目规模中等，建议按文档类型分组")
            suggestions.append("推荐目录：wiki/01-架构/、wiki/02-开发/、wiki/03-API/")
            if metrics.module_count > 10:
                suggestions.append(f"检测到 {metrics.module_count} 个模块，建议为每个模块创建独立文档")
        
        elif complexity_level == 'complex':
            suggestions.append("项目规模较大，建议按业务领域分组")
            suggestions.append("推荐结构：wiki/user-system/、wiki/order-system/、wiki/payment-system/")
            if metrics.service_count > 5:
                suggestions.append(f"检测到 {metrics.service_count} 个服务，建议为每个服务创建独立文档")
            if metrics.dependency_count > 100:
                suggestions.append(f"依赖关系复杂（{metrics.dependency_count} 个依赖），建议生成依赖关系图")
        
        elif complexity_level == 'ultra-complex':
            suggestions.append("项目规模极大，需要多层嵌套结构")
            suggestions.append("推荐结构：domain/service/module/docs/")
            suggestions.append("建议使用知识图谱来管理文档关系")
            if metrics.api_count > 20:
                suggestions.append(f"检测到 {metrics.api_count} 个 API，建议使用 API 文档生成器")
        
        # 通用建议
        if metrics.language_count > 2:
            suggestions.append(f"检测到 {metrics.language_count} 种编程语言，建议按语言分类文档")
        
        if metrics.max_file_lines > 1000:
            suggestions.append(f"检测到大文件（{metrics.max_file_lines} 行），建议拆分或提供详细注释")
        
        return suggestions
    
    def export_report(self, analysis: ComplexityAnalysis, output_path: str):
        """导出分析报告"""
        report = {
            "project": {
                "path": analysis.project_path,
                "complexity_level": analysis.complexity_level,
                "complexity_score": analysis.metrics.complexity_score
            },
            "metrics": asdict(analysis.metrics),
            "recommendation": {
                "structure_type": analysis.structure_recommendation,
                "reason": analysis.reason,
                "suggestions": analysis.suggestions
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="项目复杂度分析器")
    parser.add_argument("--path", required=True, help="项目路径")
    parser.add_argument("--output", help="输出报告路径", default="complexity-report.json")
    
    args = parser.parse_args()
    
    # 分析项目
    analyzer = ComplexityAnalyzer(args.path)
    analysis = analyzer.analyze()
    
    # 输出结果
    print(f"\n{'='*60}")
    print(f"项目复杂度分析报告")
    print(f"{'='*60}\n")
    
    print(f"项目路径: {analysis.project_path}")
    print(f"复杂度等级: {analysis.complexity_level}")
    print(f"复杂度分数: {analysis.metrics.complexity_score}/100")
    
    print(f"\n主要指标:")
    print(f"  - 模块数量: {analysis.metrics.module_count}")
    print(f"  - 文件数量: {analysis.metrics.total_files}")
    print(f"  - 代码行数: {analysis.metrics.total_lines:,}")
    print(f"  - 依赖数量: {analysis.metrics.dependency_count}")
    print(f"  - 语言数量: {analysis.metrics.language_count}")
    print(f"  - 框架数量: {analysis.metrics.framework_count}")
    print(f"  - 服务数量: {analysis.metrics.service_count}")
    print(f"  - API 数量: {analysis.metrics.api_count}")
    
    print(f"\n结构推荐:")
    print(f"  - 类型: {analysis.structure_recommendation}")
    print(f"  - 原因: {analysis.reason}")
    
    print(f"\n优化建议:")
    for i, suggestion in enumerate(analysis.suggestions, 1):
        print(f"  {i}. {suggestion}")
    
    # 导出报告
    analyzer.export_report(analysis, args.output)
    print(f"\n报告已保存到: {args.output}")


if __name__ == "__main__":
    main()
