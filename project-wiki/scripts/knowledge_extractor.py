#!/usr/bin/env python3
"""
知识提取脚本
功能：提取隐性知识（设计模式、架构决策、最佳实践、代码注释）
"""

import os
import json
import argparse
import ast
from pathlib import Path
from typing import Dict, List, Optional, Set
from collections import defaultdict
import re


class KnowledgeExtractor:
    """隐性知识提取器"""
    
    def __init__(self, project_path: str, language: Optional[str] = None):
        self.project_path = Path(project_path).resolve()
        self.language = language
        self.knowledge = {
            'design_patterns': [],
            'architecture_decisions': [],
            'best_practices': [],
            'code_conventions': [],
            'implicit_knowledge': []
        }
    
    def extract(self) -> Dict:
        """提取隐性知识"""
        print(f"提取隐性知识: {self.project_path}")
        
        if not self.project_path.exists():
            raise FileNotFoundError(f"项目路径不存在: {self.project_path}")
        
        # 自动检测语言
        if not self.language:
            self.language = self._detect_language()
        
        if self.language == 'Python':
            self._extract_python_knowledge()
        elif self.language == 'JavaScript':
            self._extract_js_knowledge()
        else:
            print(f"警告: 不支持的语言 {self.language}，跳过隐性知识提取")
        
        return self.knowledge
    
    def _detect_language(self) -> Optional[str]:
        """检测项目主语言"""
        lang_counts = {}
        
        for ext in ['.py', '.js', '.ts', '.java', '.go', '.rs']:
            files = list(self.project_path.rglob(f'*{ext}'))
            lang_counts[ext] = len(files)
        
        max_ext = max(lang_counts.items(), key=lambda x: x[1], default=('.py', 0))
        lang_map = {'.py': 'Python', '.js': 'JavaScript', '.ts': 'JavaScript', '.go': 'Go', '.rs': 'Rust'}
        return lang_map.get(max_ext[0])
    
    def _extract_python_knowledge(self):
        """提取 Python 隐性知识"""
        py_files = list(self.project_path.rglob('*.py'))
        
        # 跳过测试和缓存文件
        py_files = [
            f for f in py_files
            if 'test' not in f.name.lower()
            and 'venv' not in str(f)
            and '__pycache__' not in str(f)
            and '.tox' not in str(f)
        ]
        
        print(f"分析 {len(py_files)} 个 Python 文件")
        
        for py_file in py_files[:30]:  # 限制数量
            try:
                self._analyze_python_file(py_file)
            except Exception as e:
                print(f"解析文件 {py_file} 失败: {e}")
    
    def _analyze_python_file(self, file: Path):
        """分析单个 Python 文件"""
        source_code = file.read_text(encoding='utf-8', errors='ignore')
        
        try:
            tree = ast.parse(source_code, filename=str(file))
        except SyntaxError:
            return
        
        # 提取设计模式
        self._extract_design_patterns(tree, source_code, file)
        
        # 提取架构决策（通过注释）
        self._extract_architecture_decisions(tree, source_code, file)
        
        # 提取最佳实践
        self._extract_best_practices(tree, source_code, file)
        
        # 提取代码约定
        self._extract_code_conventions(tree, source_code, file)
    
    def _extract_design_patterns(self, tree: ast.AST, source_code: str, file: Path):
        """提取设计模式"""
        # 常见设计模式名称
        pattern_keywords = {
            'Singleton': ['singleton', '_instance', '__new__'],
            'Factory': ['factory', 'create_', 'build_'],
            'Observer': ['observer', 'subject', 'notify', 'subscribe'],
            'Strategy': ['strategy', 'abstract', 'context'],
            'Decorator': ['decorator', '@wraps', 'functools.wraps'],
            'Repository': ['repository', 'Repository'],
            'Service': ['service', 'Service'],
            'Model': ['model', 'Model', 'BaseModel'],
            'Controller': ['controller', 'Controller'],
            'Middleware': ['middleware', 'Middleware']
        }
        
        file_content_lower = source_code.lower()
        
        for pattern_name, keywords in pattern_keywords.items():
            if any(keyword in file_content_lower for keyword in keywords):
                # 查找具体证据
                context = self._find_context(source_code, keywords[0])
                self.knowledge['design_patterns'].append({
                    'pattern': pattern_name,
                    'file': str(file.relative_to(self.project_path)),
                    'evidence': keywords[0],
                    'context': context[:200]
                })
                break  # 每个文件每个模式只记录一次
    
    def _extract_architecture_decisions(self, tree: ast.AST, source_code: str, file: Path):
        """提取架构决策（从注释）"""
        # 提取文档字符串
        docstrings = []
        
        for node in ast.walk(tree):
            doc = ast.get_docstring(node)
            if doc:
                docstrings.append({
                    'type': type(node).__name__,
                    'name': getattr(node, 'name', ''),
                    'docstring': doc,
                    'file': str(file.relative_to(self.project_path))
                })
        
        # 分析文档字符串中的架构决策关键词
        decision_keywords = [
            'why', 'because', 'reason', 'decision', 'chosen',
            'trade-off', 'tradeoff', 'alternative', 'instead of',
            'we use', 'we chose', 'we decided',
            'note:', 'todo:', 'fixme:', 'hack:'
        ]
        
        for doc_info in docstrings:
            doc_lower = doc_info['docstring'].lower()
            if any(keyword in doc_lower for keyword in decision_keywords):
                self.knowledge['architecture_decisions'].append({
                    'context': f"{doc_info['type']} {doc_info['name']}",
                    'file': str(doc_info['file']),
                    'decision': doc_info['docstring'][:300],
                    'type': self._classify_decision(doc_info['docstring'])
                })
    
    def _classify_decision(self, docstring: str) -> str:
        """分类决策类型"""
        if 'why' in docstring.lower() or 'because' in docstring.lower():
            return '设计理由'
        elif 'note:' in docstring.lower():
            return '注意事项'
        elif 'todo:' in docstring.lower():
            return '待办事项'
        elif 'fixme:' in docstring.lower():
            return '需要修复'
        else:
            return '架构决策'
    
    def _extract_best_practices(self, tree: ast.AST, source_code: str, file: Path):
        """提取最佳实践"""
        practices = []
        
        # 检查类型提示使用
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 检查是否有返回类型注解
                if node.returns:
                    practices.append({
                        'practice': '使用类型提示（返回值）',
                        'file': str(file.relative_to(self.project_path)),
                        'function': node.name
                    })
                
                # 检查参数类型提示
                typed_args = [arg for arg in node.args.args if arg.annotation]
                if typed_args:
                    practices.append({
                        'practice': '使用类型提示（参数）',
                        'file': str(file.relative_to(self.project_path)),
                        'function': node.name
                    })
                
                # 检查文档字符串
                if ast.get_docstring(node):
                    practices.append({
                        'practice': '编写文档字符串',
                        'file': str(file.relative_to(self.project_path)),
                        'function': node.name
                    })
        
        self.knowledge['best_practices'].extend(practices[:20])  # 限制数量
    
    def _extract_code_conventions(self, tree: ast.AST, source_code: str, file: Path):
        """提取代码约定"""
        conventions = []
        
        # 分析命名约定
        function_names = []
        class_names = []
        variable_names = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_names.append(node.name)
            elif isinstance(node, ast.ClassDef):
                class_names.append(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variable_names.append(target.id)
        
        # 分析命名模式
        if function_names:
            snake_case_count = sum(1 for name in function_names if '_' in name)
            camel_case_count = sum(1 for name in function_names if name[0].isupper() or any(c.isupper() for c in name))
            
            if snake_case_count > len(function_names) * 0.7:
                conventions.append({
                    'convention': '使用 snake_case 命名函数',
                    'file': str(file.relative_to(self.project_path)),
                    'evidence': f"{snake_case_count}/{len(function_names)} 函数使用 snake_case"
                })
        
        if class_names:
            pascal_case_count = sum(1 for name in class_names if name[0].isupper())
            if pascal_case_count > len(class_names) * 0.8:
                conventions.append({
                    'convention': '使用 PascalCase 命名类',
                    'file': str(file.relative_to(self.project_path)),
                    'evidence': f"{pascal_case_count}/{len(class_names)} 类使用 PascalCase"
                })
        
        self.knowledge['code_conventions'].extend(conventions[:10])
    
    def _extract_js_knowledge(self):
        """提取 JavaScript 隐性知识"""
        js_files = list(self.project_path.rglob('*.js')) + list(self.project_path.rglob('*.jsx'))
        
        js_files = [f for f in js_files if 'test' not in f.name.lower() and 'node_modules' not in str(f)]
        
        print(f"分析 {len(js_files)} 个 JavaScript 文件")
        
        for js_file in js_files[:20]:  # 限制数量
            try:
                self._analyze_js_file(js_file)
            except Exception as e:
                print(f"解析文件 {js_file} 失败: {e}")
    
    def _analyze_js_file(self, file: Path):
        """分析单个 JavaScript 文件"""
        source_code = file.read_text(encoding='utf-8', errors='ignore')
        
        # 提取设计模式（通过正则）
        self._extract_js_design_patterns(source_code, file)
        
        # 提取注释中的知识
        self._extract_js_comments_knowledge(source_code, file)
    
    def _extract_js_design_patterns(self, source_code: str, file: Path):
        """提取 JS 设计模式"""
        pattern_keywords = {
            'Singleton': ['singleton', 'getInstance'],
            'Factory': ['factory', 'create'],
            'Observer': ['on', 'emit', 'subscribe'],
            'Component': ['Component', 'React.Component'],
            'Hook': ['use', 'useState', 'useEffect']
        }
        
        source_lower = source_code.lower()
        
        for pattern_name, keywords in pattern_keywords.items():
            if any(keyword in source_lower for keyword in keywords):
                context = self._find_context(source_code, keywords[0])
                self.knowledge['design_patterns'].append({
                    'pattern': pattern_name,
                    'file': str(file.relative_to(self.project_path)),
                    'evidence': keywords[0],
                    'context': context[:200]
                })
                break
    
    def _extract_js_comments_knowledge(self, source_code: str, file: Path):
        """提取 JS 注释中的知识"""
        # 提取多行注释
        comments = re.findall(r'/\*\*.*?\*/|//.*$', source_code, re.MULTILINE)
        
        for comment in comments:
            comment_clean = comment.strip('/* */')
            if len(comment_clean) > 10:
                self.knowledge['implicit_knowledge'].append({
                    'file': str(file.relative_to(self.project_path)),
                    'content': comment_clean[:200],
                    'type': '注释知识'
                })
    
    def _find_context(self, source_code: str, keyword: str) -> str:
        """查找关键词的上下文"""
        index = source_code.lower().find(keyword.lower())
        if index == -1:
            return ''
        
        start = max(0, index - 50)
        end = min(len(source_code), index + len(keyword) + 50)
        return source_code[start:end]


def main():
    parser = argparse.ArgumentParser(description='提取隐性知识')
    parser.add_argument('--path', type=str, default='.', help='项目路径（默认当前目录）')
    parser.add_argument('--language', type=str, default=None, help='指定语言（Python/JavaScript）')
    parser.add_argument('--output', type=str, default='implicit-knowledge.json', help='输出文件路径')
    
    args = parser.parse_args()
    
    extractor = KnowledgeExtractor(args.path, args.language)
    knowledge = extractor.extract()
    
    # 输出结果
    output_path = Path(args.output)
    output_path.write_text(json.dumps(knowledge, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"\n隐性知识提取完成！")
    print(f"设计模式: {len(knowledge['design_patterns'])}")
    print(f"架构决策: {len(knowledge['architecture_decisions'])}")
    print(f"最佳实践: {len(knowledge['best_practices'])}")
    print(f"代码约定: {len(knowledge['code_conventions'])}")
    print(f"注释知识: {len(knowledge['implicit_knowledge'])}")
    print(f"结果已保存到: {output_path}")


if __name__ == '__main__':
    main()
