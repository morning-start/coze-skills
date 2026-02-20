#!/usr/bin/env python3
"""
代码文档提取脚本
功能：通过 AST 解析提取函数、类、方法的文档注释和类型信息
"""

import os
import json
import argparse
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional


class DocExtractor:
    """文档提取器"""
    
    SUPPORTED_LANGUAGES = ['Python', 'JavaScript']
    
    def __init__(self, project_path: str, language: Optional[str] = None):
        self.project_path = Path(project_path).resolve()
        self.language = language
        self.result = {
            'language': language,
            'files': [],
            'api_endpoints': [],
            'classes': [],
            'functions': [],
            'modules': []
        }
    
    def extract(self) -> Dict:
        """提取文档"""
        print(f"提取文档: {self.project_path}")
        
        if not self.project_path.exists():
            raise FileNotFoundError(f"项目路径不存在: {self.project_path}")
        
        # 自动检测语言
        if not self.language:
            self.language = self._detect_language()
        
        if self.language == 'Python':
            self._extract_python_docs()
        elif self.language == 'JavaScript':
            print("警告: JavaScript AST 解析暂未实现，跳过文档提取")
        else:
            print(f"警告: 不支持的语言 {self.language}，跳过文档提取")
        
        return self.result
    
    def _detect_language(self) -> Optional[str]:
        """检测编程语言"""
        # 查找 .py 文件
        py_files = list(self.project_path.rglob('*.py'))
        if py_files:
            return 'Python'
        
        # 查找 .js/.ts 文件
        js_files = list(self.project_path.rglob('*.js')) + list(self.project_path.rglob('*.ts'))
        if js_files:
            return 'JavaScript'
        
        return None
    
    def _extract_python_docs(self):
        """提取 Python 文档"""
        print(f"提取 Python 文档...")
        
        # 查找所有 Python 文件
        py_files = list(self.project_path.rglob('*.py'))
        
        for py_file in py_files:
            # 跳过测试文件和虚拟环境
            if any(skip in str(py_file) for skip in ['test', 'venv', '__pycache__', '.egg-info']):
                continue
            
            self._extract_from_python_file(py_file)
    
    def _extract_from_python_file(self, file_path: Path):
        """从 Python 文件中提取文档"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 AST
            tree = ast.parse(content)
            
            # 提取文档字符串
            docstring = ast.get_docstring(tree)
            if docstring:
                self.result['modules'].append({
                    'name': str(file_path.relative_to(self.project_path)),
                    'docstring': docstring,
                    'path': str(file_path)
                })
            
            # 提取函数和类
            for node in ast.walk(tree):
                # 提取函数
                if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    self._extract_function(node, file_path)
                
                # 提取类
                elif isinstance(node, ast.ClassDef):
                    self._extract_class(node, file_path)
        
        except SyntaxError as e:
            print(f"警告: 解析 {file_path} 失败: {e}")
        except Exception as e:
            print(f"警告: 读取 {file_path} 失败: {e}")
    
    def _extract_function(self, node: ast.FunctionDef, file_path: Path):
        """提取函数信息"""
        docstring = ast.get_docstring(node)
        
        # 提取参数
        args_info = []
        if hasattr(node, 'args'):
            for arg in node.args.args:
                arg_info = {
                    'name': arg.arg,
                    'type': None,
                    'default': None
                }
                
                # 提取类型注解
                if arg.annotation:
                    arg_info['type'] = ast.unparse(arg.annotation)
                
                args_info.append(arg_info)
        
        # 提取返回类型
        return_type = None
        if hasattr(node, 'returns') and node.returns:
            return_type = ast.unparse(node.returns)
        
        func_info = {
            'name': node.name,
            'docstring': docstring,
            'path': str(file_path),
            'line': node.lineno,
            'args': args_info,
            'return_type': return_type
        }
        
        self.result['functions'].append(func_info)
    
    def _extract_class(self, node: ast.ClassDef, file_path: Path):
        """提取类信息"""
        docstring = ast.get_docstring(node)
        
        # 提取基类
        base_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_classes.append(ast.unparse(base))
        
        class_info = {
            'name': node.name,
            'docstring': docstring,
            'path': str(file_path),
            'line': node.lineno,
            'base_classes': base_classes,
            'methods': []
        }
        
        # 提取类的方法
        for child in node.body:
            if isinstance(child, ast.FunctionDef) or isinstance(child, ast.AsyncFunctionDef):
                method_info = {
                    'name': child.name,
                    'docstring': ast.get_docstring(child),
                    'line': child.lineno
                }
                class_info['methods'].append(method_info)
        
        self.result['classes'].append(class_info)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='代码文档提取工具')
    parser.add_argument('--path', type=str, default='.', help='项目路径')
    parser.add_argument('--language', type=str, choices=['Python', 'JavaScript'],
                       help='指定编程语言')
    
    args = parser.parse_args()
    
    extractor = DocExtractor(args.path, args.language)
    result = extractor.extract()
    
    # 保存结果
    output_file = Path(args.path) / 'docs-metadata.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n文档提取完成！结果已保存到: {output_file}")
    print(f"提取的 API 端点数: {len(result['api_endpoints'])}")
    print(f"提取的类数: {len(result['classes'])}")
    print(f"提取的函数数: {len(result['functions'])}")


if __name__ == '__main__':
    main()
