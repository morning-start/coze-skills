#!/usr/bin/env python3
"""
一致性检查器

检查文档与代码的一致性，防止脱节
"""

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict


@dataclass
class ConsistencyIssue:
    """一致性问题"""
    issue_type: str
    severity: str  # low, medium, high, critical
    location: str
    description: str
    suggestion: str
    code_location: Optional[str]
    doc_location: Optional[str]


@dataclass
class ConsistencyReport:
    """一致性报告"""
    project_path: str
    total_files: int
    checked_files: int
    issues: List[ConsistencyIssue]
    summary: Dict[str, int]
    score: int  # 0-100


class ConsistencyChecker:
    """一致性检查器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.wiki_path = self.project_path / 'wiki'
        self.code_extensions = {'.py', '.js', '.ts', '.java', '.go'}
    
    def check_all(self) -> ConsistencyReport:
        """执行全面一致性检查"""
        issues = []
        
        # 检查 API 文档一致性
        api_issues = self._check_api_consistency()
        issues.extend(api_issues)
        
        # 检查模块文档一致性
        module_issues = self._check_module_consistency()
        issues.extend(module_issues)
        
        # 检查数据模型一致性
        model_issues = self._check_model_consistency()
        issues.extend(model_issues)
        
        # 检查文档时效性
        freshness_issues = self._check_document_freshness()
        issues.extend(freshness_issues)
        
        # 检查链接有效性
        link_issues = self._check_link_validity()
        issues.extend(link_issues)
        
        # 生成摘要
        summary = self._generate_summary(issues)
        
        # 计算得分
        score = self._calculate_score(issues)
        
        return ConsistencyReport(
            project_path=str(self.project_path),
            total_files=self._count_files(),
            checked_files=len(issues),  # 简化处理
            issues=issues,
            summary=summary,
            score=score
        )
    
    def _count_files(self) -> int:
        """统计文件数量"""
        count = 0
        for ext in self.code_extensions:
            count += len(list(self.project_path.rglob(f'*{ext}')))
        return count
    
    def _check_api_consistency(self) -> List[ConsistencyIssue]:
        """检查 API 文档一致性"""
        issues = []
        
        if not self.wiki_path.exists():
            return issues
        
        # 查找 API 文档
        api_docs = list(self.wiki_path.rglob('api*.md')) + list(self.wiki_path.rglob('*api.md'))
        
        for api_doc in api_docs:
            # 提取文档中定义的 API
            doc_apis = self._extract_doc_apis(api_doc)
            
            # 在代码中查找对应的 API 实现
            for doc_api in doc_apis:
                code_api = self._find_code_api(doc_api)
                
                if not code_api:
                    issues.append(ConsistencyIssue(
                        issue_type='api_not_implemented',
                        severity='high',
                        location=str(api_doc.relative_to(self.project_path)),
                        description=f"文档中定义的 API '{doc_api}' 在代码中未找到实现",
                        suggestion=f"检查 API 名称拼写或补充实现代码",
                        doc_location=str(api_doc.relative_to(self.project_path)),
                        code_location=None
                    ))
        
        return issues
    
    def _extract_doc_apis(self, api_doc: Path) -> List[str]:
        """从文档中提取 API 定义"""
        apis = []
        
        try:
            content = api_doc.read_text(encoding='utf-8', errors='ignore')
            
            # 提取 API 路径
            path_matches = re.findall(r'路径[:\s]*([^\n]+)', content, re.IGNORECASE)
            apis.extend(path_matches)
            
            # 提取 API 端点
            endpoint_matches = re.findall(r'端点[:\s]*([^\n]+)', content, re.IGNORECASE)
            apis.extend(endpoint_matches)
            
            # 提取 URL 模式
            url_matches = re.findall(r'/(?:api|v[0-9]+)/[^\s\n]+', content)
            apis.extend(url_matches)
        except:
            pass
        
        return list(set(apis))
    
    def _find_code_api(self, api_path: str) -> Optional[str]:
        """在代码中查找 API 实现"""
        # 查找 Python 文件
        for py_file in self.project_path.rglob('*.py'):
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                if api_path in content or self._normalize_path(api_path) in content:
                    return str(py_file.relative_to(self.project_path))
            except:
                pass
        
        return None
    
    def _normalize_path(self, path: str) -> str:
        """规范化路径"""
        return path.replace('/', '_').replace('-', '_')
    
    def _check_module_consistency(self) -> List[ConsistencyIssue]:
        """检查模块文档一致性"""
        issues = []
        
        if not self.wiki_path.exists():
            return issues
        
        # 查找模块文档
        module_docs = list(self.wiki_path.rglob('module*.md')) + list(self.wiki_path.rglob('*module.md'))
        
        for module_doc in module_docs:
            # 提取模块名称
            module_name = self._extract_module_name(module_doc)
            
            if module_name:
                # 检查代码中是否存在该模块
                module_path = self.project_path / module_name
                if not module_path.exists():
                    # 尝试其他常见的模块位置
                    found = False
                    for ext in self.code_extensions:
                        module_file = self.project_path / f"{module_name}{ext}"
                        if module_file.exists():
                            found = True
                            break
                    
                    if not found:
                        issues.append(ConsistencyIssue(
                            issue_type='module_not_found',
                            severity='medium',
                            location=str(module_doc.relative_to(self.project_path)),
                            description=f"文档中提到的模块 '{module_name}' 在代码中未找到",
                            suggestion=f"检查模块名称拼写或补充模块代码",
                            doc_location=str(module_doc.relative_to(self.project_path)),
                            code_location=None
                        ))
        
        return issues
    
    def _extract_module_name(self, module_doc: Path) -> Optional[str]:
        """从文档中提取模块名称"""
        try:
            content = module_doc.read_text(encoding='utf-8', errors='ignore')
            
            # 查找模块名称
            module_match = re.search(r'模块[:\s]*([^\n]+)', content, re.IGNORECASE)
            if module_match:
                return module_match.group(1).strip()
            
            # 从文件名推断
            filename = module_doc.stem
            if 'module' in filename.lower():
                return filename.replace('module', '').replace('-', '_').strip()
        except:
            pass
        
        return None
    
    def _check_model_consistency(self) -> List[ConsistencyIssue]:
        """检查数据模型一致性"""
        issues = []
        
        if not self.wiki_path.exists():
            return issues
        
        # 查找模型文档
        model_docs = list(self.wiki_path.rglob('model*.md')) + list(self.wiki_path.rglob('*model.md'))
        
        for model_doc in model_docs:
            # 提取模型定义
            models = self._extract_model_definitions(model_doc)
            
            for model in models:
                # 在代码中查找模型定义
                code_model = self._find_code_model(model['name'])
                
                if not code_model:
                    issues.append(ConsistencyIssue(
                        issue_type='model_not_found',
                        severity='medium',
                        location=str(model_doc.relative_to(self.project_path)),
                        description=f"文档中定义的模型 '{model['name']}' 在代码中未找到",
                        suggestion=f"检查模型名称拼写或补充模型代码",
                        doc_location=str(model_doc.relative_to(self.project_path)),
                        code_location=None
                    ))
                else:
                    # 检查字段一致性
                    field_issues = self._check_model_fields(model, code_model)
                    issues.extend(field_issues)
        
        return issues
    
    def _extract_model_definitions(self, model_doc: Path) -> List[Dict]:
        """从文档中提取模型定义"""
        models = []
        
        try:
            content = model_doc.read_text(encoding='utf-8', errors='ignore')
            
            # 查找模型定义
            model_pattern = re.compile(r'(?:模型|Model|类|Class)[:\s]+(\w+).*?字段[:\s]*([^\n]+(?:\n[^\n]+)*?)(?=\n(?:模型|Model|类|Class)|\n\n|\Z)', re.IGNORECASE)
            
            for match in model_pattern.finditer(content):
                model_name = match.group(1)
                fields_text = match.group(2)
                
                # 提取字段
                fields = []
                field_lines = fields_text.strip().split('\n')
                for line in field_lines:
                    if ':' in line and '|' in line:
                        parts = [p.strip() for p in line.split('|')]
                        if len(parts) >= 2:
                            fields.append({
                                'name': parts[0],
                                'type': parts[1],
                                'description': parts[2] if len(parts) > 2 else ''
                            })
                
                models.append({
                    'name': model_name,
                    'fields': fields
                })
        except:
            pass
        
        return models
    
    def _find_code_model(self, model_name: str) -> Optional[Dict]:
        """在代码中查找模型定义"""
        # 查找 Python 类定义
        for py_file in self.project_path.rglob('*.py'):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 使用 AST 解析
                    tree = ast.parse(content)
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef) and node.name.lower() == model_name.lower():
                            # 提取字段
                            fields = []
                            for item in node.body:
                                if isinstance(item, ast.Assign):
                                    for target in item.targets:
                                        if isinstance(target, ast.Name):
                                            fields.append({'name': target.id})
                            
                            return {
                                'file': str(py_file.relative_to(self.project_path)),
                                'fields': fields
                            }
            except:
                pass
        
        return None
    
    def _check_model_fields(self, doc_model: Dict, code_model: Dict) -> List[ConsistencyIssue]:
        """检查模型字段一致性"""
        issues = []
        
        doc_field_names = {f['name'].lower() for f in doc_model['fields']}
        code_field_names = {f['name'].lower() for f in code_model.get('fields', [])}
        
        # 检查文档中定义但代码中不存在的字段
        missing_in_code = doc_field_names - code_field_names
        if missing_in_code:
            issues.append(ConsistencyIssue(
                issue_type='field_missing_in_code',
                severity='low',
                location=code_model['file'],
                description=f"模型 '{doc_model['name']}' 中有 {len(missing_in_code)} 个字段在代码中未找到: {', '.join(missing_in_code)}",
                suggestion=f"检查字段名称或补充字段定义",
                code_location=code_model['file'],
                doc_location=None
            ))
        
        # 检查代码中存在但文档中未记录的字段
        missing_in_doc = code_field_names - doc_field_names
        if missing_in_doc:
            issues.append(ConsistencyIssue(
                issue_type='field_missing_in_doc',
                severity='low',
                location=code_model['file'],
                description=f"模型 '{doc_model['name']}' 中有 {len(missing_in_doc)} 个字段在文档中未记录: {', '.join(missing_in_doc)}",
                suggestion=f"补充文档中的字段定义",
                code_location=code_model['file'],
                doc_location=None
            ))
        
        return issues
    
    def _check_document_freshness(self) -> List[ConsistencyIssue]:
        """检查文档时效性"""
        issues = []
        
        if not self.wiki_path.exists():
            return issues
        
        # 检查是否有最近更新的文档
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=30)
        
        for doc_file in self.wiki_path.rglob('*.md'):
            try:
                doc_mtime = datetime.fromtimestamp(doc_file.stat().st_mtime)
                if doc_mtime < cutoff_date:
                    # 检查对应的代码文件是否有更新
                    doc_stem = doc_file.stem
                    for ext in self.code_extensions:
                        code_file = self.project_path / f"{doc_stem}{ext}"
                        if code_file.exists():
                            code_mtime = datetime.fromtimestamp(code_file.stat().st_mtime)
                            if code_mtime > doc_mtime:
                                issues.append(ConsistencyIssue(
                                    issue_type='document_outdated',
                                    severity='low',
                                    location=str(doc_file.relative_to(self.project_path)),
                                    description=f"文档可能已过期（代码已更新但文档未更新）",
                                    suggestion=f"检查代码变更并更新文档",
                                    doc_location=str(doc_file.relative_to(self.project_path)),
                                    code_location=str(code_file.relative_to(self.project_path))
                                ))
                                break
            except:
                pass
        
        return issues
    
    def _check_link_validity(self) -> List[ConsistencyIssue]:
        """检查链接有效性"""
        issues = []
        
        if not self.wiki_path.exists():
            return issues
        
        for doc_file in self.wiki_path.rglob('*.md'):
            try:
                content = doc_file.read_text(encoding='utf-8', errors='ignore')
                
                # 提取所有链接
                link_matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                
                for link_title, link_url in link_matches:
                    # 跳过外部链接
                    if link_url.startswith(('http://', 'https://', '#')):
                        continue
                    
                    # 检查相对链接
                    target_path = (doc_file.parent / link_url).resolve()
                    if not target_path.exists():
                        # 尝试添加 .md 扩展名
                        if not link_url.endswith('.md'):
                            target_path = (doc_file.parent / f"{link_url}.md").resolve()
                        
                        if not target_path.exists():
                            issues.append(ConsistencyIssue(
                                issue_type='broken_link',
                                severity='low',
                                location=str(doc_file.relative_to(self.project_path)),
                                description=f"链接 '[{link_title}]({link_url}' 指向的文件不存在",
                                suggestion=f"检查链接路径或创建目标文件",
                                doc_location=str(doc_file.relative_to(self.project_path)),
                                code_location=None
                            ))
            except:
                pass
        
        return issues
    
    def _generate_summary(self, issues: List[ConsistencyIssue]) -> Dict[str, int]:
        """生成问题摘要"""
        summary = {
            'total': len(issues),
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for issue in issues:
            summary[issue.severity] += 1
        
        return summary
    
    def _calculate_score(self, issues: List[ConsistencyIssue]) -> int:
        """计算一致性得分"""
        score = 100
        
        # 根据问题严重程度扣分
        severity_penalty = {
            'critical': 30,
            'high': 20,
            'medium': 10,
            'low': 5
        }
        
        for issue in issues:
            score -= severity_penalty.get(issue.severity, 10)
        
        return max(0, score)
    
    def export_report(self, report: ConsistencyReport, output_path: str):
        """导出报告"""
        report_data = {
            "project": {
                "path": report.project_path,
                "total_files": report.total_files,
                "score": report.score
            },
            "summary": report.summary,
            "issues": [
                {
                    "type": issue.issue_type,
                    "severity": issue.severity,
                    "location": issue.location,
                    "description": issue.description,
                    "suggestion": issue.suggestion,
                    "code_location": issue.code_location,
                    "doc_location": issue.doc_location
                }
                for issue in report.issues
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="一致性检查器")
    parser.add_argument("--path", required=True, help="项目路径")
    parser.add_argument("--output", help="输出报告路径", default="consistency-report.json")
    
    args = parser.parse_args()
    
    # 执行检查
    checker = ConsistencyChecker(args.path)
    report = checker.check_all()
    
    # 输出结果
    print(f"\n{'='*60}")
    print(f"一致性检查报告")
    print(f"{'='*60}\n")
    
    print(f"项目路径: {report.project_path}")
    print(f"总文件数: {report.total_files}")
    print(f"问题总数: {report.summary['total']}")
    print(f"一致性得分: {report.score}/100")
    
    if report.summary['total'] > 0:
        print(f"\n问题分布:")
        print(f"  - 严重 (Critical): {report.summary['critical']}")
        print(f"  - 高 (High): {report.summary['high']}")
        print(f"  - 中 (Medium): {report.summary['medium']}")
        print(f"  - 低 (Low): {report.summary['low']}")
        
        print(f"\n详细问题 ({len(report.issues)}):")
        for i, issue in enumerate(report.issues, 1):
            print(f"\n  {i}. [{issue.severity.upper()}] {issue.issue_type}")
            print(f"     位置: {issue.location}")
            print(f"     描述: {issue.description}")
            print(f"     建议: {issue.suggestion}")
            if issue.code_location:
                print(f"     代码: {issue.code_location}")
            if issue.doc_location:
                print(f"     文档: {issue.doc_location}")
    else:
        print(f"\n✓ 未发现一致性问题")
    
    # 导出报告
    checker.export_report(report, args.output)
    print(f"\n报告已保存到: {args.output}")


if __name__ == "__main__":
    main()
