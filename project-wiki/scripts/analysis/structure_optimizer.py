#!/usr/bin/env python3
"""
结构优化器

分析和优化现有项目结构，提供改进建议
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class StructureIssue:
    """结构问题"""
    issue_type: str
    severity: str  # low, medium, high, critical
    location: str
    description: str
    suggestion: str


@dataclass
class OptimizationReport:
    """优化报告"""
    project_path: str
    current_structure_type: str
    recommended_structure_type: str
    issues: List[StructureIssue]
    optimizations: List[Dict]
    score: int  # 0-100


class StructureOptimizer:
    """结构优化器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.wiki_path = self.project_path / 'wiki'
    
    def analyze_current_structure(self) -> Dict:
        """分析当前结构"""
        if not self.wiki_path.exists():
            return {'type': 'none', 'depth': 0, 'directories': 0}
        
        structure = {
            'type': 'unknown',
            'depth': 0,
            'directories': 0,
            'files': 0,
            'index_files': 0
        }
        
        # 扫描目录结构
        for root, dirs, files in os.walk(self.wiki_path):
            depth = root.replace(str(self.wiki_path), '').count(os.sep)
            structure['depth'] = max(structure['depth'], depth)
            structure['directories'] += len(dirs)
            structure['files'] += len(files)
            
            # 统计索引文件
            for file in files:
                if file.lower() in ['readme.md', 'index.md']:
                    structure['index_files'] += 1
        
        # 判断结构类型
        if structure['depth'] <= 1:
            structure['type'] = 'flat'
        elif structure['depth'] <= 3:
            structure['type'] = 'typed'
        elif structure['depth'] <= 4:
            structure['type'] = 'domain'
        else:
            structure['type'] = 'nested'
        
        return structure
    
    def detect_issues(self, current_structure: Dict) -> List[StructureIssue]:
        """检测结构问题"""
        issues = []
        
        if not self.wiki_path.exists():
            issues.append(StructureIssue(
                issue_type='missing_wiki',
                severity='critical',
                location='project_root',
                description='Wiki 目录不存在',
                suggestion='创建 wiki/ 目录并初始化文档结构'
            ))
            return issues
        
        # 检查深度是否合理
        if current_structure['depth'] > 5:
            issues.append(StructureIssue(
                issue_type='too_deep',
                severity='medium',
                location='wiki/',
                description=f'目录嵌套过深（{current_structure["depth"]} 层）',
                suggestion='考虑简化结构或使用更好的命名约定'
            ))
        
        # 检查是否有索引文件
        if current_structure['index_files'] < current_structure['directories'] // 5:
            issues.append(StructureIssue(
                issue_type='missing_index',
                severity='low',
                location='wiki/',
                description='缺少 README.md 或 index.md 索引文件',
                suggestion='为主要目录添加索引文件'
            ))
        
        # 检查是否有空目录
        empty_dirs = []
        for root, dirs, files in os.walk(self.wiki_path):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                if not list(dir_path.iterdir()):
                    empty_dirs.append(dir_path)
        
        if empty_dirs:
            issues.append(StructureIssue(
                issue_type='empty_dirs',
                severity='low',
                location='wiki/',
                description=f'发现 {len(empty_dirs)} 个空目录',
                suggestion=f'删除空目录或添加内容: {", ".join(str(d.relative_to(self.wiki_path)) for d in empty_dirs[:3])}'
            ))
        
        # 检查文件命名一致性
        file_names = []
        for root, dirs, files in os.walk(self.wiki_path):
            for file in files:
                file_names.append(file)
        
        inconsistent_names = [f for f in file_names if ' ' in f or not f.lower().replace('-', '').replace('_', '').isalnum()]
        if inconsistent_names:
            issues.append(StructureIssue(
                issue_type='inconsistent_naming',
                severity='medium',
                location='wiki/',
                description=f'发现 {len(inconsistent_names)} 个命名不一致的文件',
                suggestion='使用统一的命名约定（小写字母、连字符、下划线）'
            ))
        
        # 检查文档完整性
        missing_docs = self._check_documentation_completeness()
        if missing_docs:
            for doc_type, locations in missing_docs.items():
                issues.append(StructureIssue(
                    issue_type='missing_docs',
                    severity='medium',
                    location='wiki/',
                    description=f'缺少 {doc_type} 文档',
                    suggestion=f'在以下位置创建 {doc_type}: {", ".join(locations)}'
                ))
        
        return issues
    
    def _check_documentation_completeness(self) -> Dict[str, List[str]]:
        """检查文档完整性"""
        missing = {}
        
        # 检查是否有 README
        if not (self.wiki_path / 'README.md').exists():
            missing['README'] = ['wiki/']
        
        # 检查是否有架构文档
        if not (self.wiki_path / 'architecture').exists() and not any('architecture' in str(p) for p in self.wiki_path.rglob('*.md')):
            missing['架构文档'] = ['wiki/']
        
        # 检查是否有 API 文档
        if not (self.wiki_path / 'api').exists() and not any('api' in str(p) for p in self.wiki_path.rglob('*.md')):
            missing['API 文档'] = ['wiki/']
        
        return missing
    
    def generate_optimizations(self, current_structure: Dict, recommended_type: str) -> List[Dict]:
        """生成优化建议"""
        optimizations = []
        
        # 如果当前结构与推荐不匹配
        if current_structure['type'] != recommended_type:
            optimizations.append({
                'type': 'restructure',
                'priority': 'high',
                'description': f'当前结构类型为 {current_structure["type"]}，推荐类型为 {recommended_type}',
                'action': '建议重新组织目录结构',
                'effort': 'medium'
            })
        
        # 如果目录过深
        if current_structure['depth'] > 4:
            optimizations.append({
                'type': 'flatten',
                'priority': 'medium',
                'description': '目录嵌套过深，影响导航',
                'action': '考虑扁平化部分目录',
                'effort': 'low'
            })
        
        # 如果缺少索引文件
        if current_structure['index_files'] < current_structure['directories'] // 5:
            optimizations.append({
                'type': 'add_indexes',
                'priority': 'low',
                'description': '为主要目录添加索引文件',
                'action': '创建 README.md 或 index.md',
                'effort': 'low'
            })
        
        # 通用优化建议
        optimizations.append({
            'type': 'add_search',
            'priority': 'low',
            'description': '添加文档搜索功能',
            'action': '配置全文搜索或生成索引',
            'effort': 'medium'
        })
        
        optimizations.append({
            'type': 'add_navigation',
            'priority': 'low',
            'description': '改进文档导航',
            'action': '添加面包屑导航或侧边栏',
            'effort': 'low'
        })
        
        return optimizations
    
    def calculate_score(self, issues: List[StructureIssue], current_structure: Dict) -> int:
        """计算结构得分"""
        score = 100
        
        # 根据问题严重程度扣分
        severity_penalty = {
            'critical': 50,
            'high': 30,
            'medium': 15,
            'low': 5
        }
        
        for issue in issues:
            score -= severity_penalty.get(issue.severity, 10)
        
        # 根据结构深度扣分
        if current_structure['depth'] > 5:
            score -= (current_structure['depth'] - 5) * 5
        
        # 确保分数在 0-100 范围内
        score = max(0, min(100, score))
        
        return score
    
    def optimize(self, recommended_type: str = None) -> OptimizationReport:
        """执行优化分析"""
        # 分析当前结构
        current_structure = self.analyze_current_structure()
        
        # 检测问题
        issues = self.detect_issues(current_structure)
        
        # 生成优化建议
        if recommended_type is None:
            # 根据当前问题推断推荐类型
            if current_structure['depth'] > 4:
                recommended_type = 'typed'
            else:
                recommended_type = current_structure['type']
        
        optimizations = self.generate_optimizations(current_structure, recommended_type)
        
        # 计算得分
        score = self.calculate_score(issues, current_structure)
        
        return OptimizationReport(
            project_path=str(self.project_path),
            current_structure_type=current_structure['type'],
            recommended_structure_type=recommended_type,
            issues=issues,
            optimizations=optimizations,
            score=score
        )
    
    def export_report(self, report: OptimizationReport, output_path: str):
        """导出报告"""
        report_data = {
            "project": {
                "path": report.project_path,
                "current_structure": report.current_structure_type,
                "recommended_structure": report.recommended_structure_type,
                "score": report.score
            },
            "issues": [
                {
                    "type": issue.issue_type,
                    "severity": issue.severity,
                    "location": issue.location,
                    "description": issue.description,
                    "suggestion": issue.suggestion
                }
                for issue in report.issues
            ],
            "optimizations": report.optimizations
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="结构优化器")
    parser.add_argument("--path", required=True, help="项目路径")
    parser.add_argument("--recommended", help="推荐结构类型")
    parser.add_argument("--output", help="输出报告路径", default="optimization-report.json")
    
    args = parser.parse_args()
    
    # 执行优化分析
    optimizer = StructureOptimizer(args.path)
    report = optimizer.optimize(args.recommended)
    
    # 输出结果
    print(f"\n{'='*60}")
    print(f"结构优化报告")
    print(f"{'='*60}\n")
    
    print(f"项目路径: {report.project_path}")
    print(f"当前结构: {report.current_structure_type}")
    print(f"推荐结构: {report.recommended_structure_type}")
    print(f"结构得分: {report.score}/100")
    
    if report.issues:
        print(f"\n检测到的问题 ({len(report.issues)}):")
        for i, issue in enumerate(report.issues, 1):
            print(f"\n  {i}. [{issue.severity.upper()}] {issue.issue_type}")
            print(f"     位置: {issue.location}")
            print(f"     描述: {issue.description}")
            print(f"     建议: {issue.suggestion}")
    else:
        print(f"\n✓ 未检测到问题")
    
    if report.optimizations:
        print(f"\n优化建议 ({len(report.optimizations)}):")
        for i, opt in enumerate(report.optimizations, 1):
            print(f"\n  {i}. [{opt['priority'].upper()}] {opt['type']}")
            print(f"     描述: {opt['description']}")
            print(f"     操作: {opt['action']}")
            print(f"     工作量: {opt['effort']}")
    
    # 导出报告
    optimizer.export_report(report, args.output)
    print(f"\n报告已保存到: {args.output}")


if __name__ == "__main__":
    main()
