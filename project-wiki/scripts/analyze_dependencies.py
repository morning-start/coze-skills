#!/usr/bin/env python3
"""
依赖关系分析脚本
功能：分析模块依赖关系，生成 Mermaid 图表
"""

import os
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict


class DependencyAnalyzer:
    """依赖关系分析器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.dependencies = defaultdict(set)
        self.modules = set()
        self.result = {
            'dependency_graph': {},
            'mermaid_diagram': '',
            'circular_dependencies': [],
            'module_levels': {}
        }
    
    def analyze(self) -> Dict:
        """执行分析"""
        print(f"分析依赖关系: {self.project_path}")
        
        if not self.project_path.exists():
            raise FileNotFoundError(f"项目路径不存在: {self.project_path}")
        
        # 分析 Python 项目
        py_files = list(self.project_path.rglob('*.py'))
        py_files = [
            f for f in py_files
            if 'test' not in f.name.lower()
            and 'venv' not in str(f)
            and '__pycache__' not in str(f)
        ]
        
        print(f"找到 {len(py_files)} 个 Python 文件")
        
        # 构建模块映射
        module_map = self._build_module_map(py_files)
        
        # 分析导入关系
        self._analyze_imports(py_files, module_map)
        
        # 生成 Mermaid 图表
        self._generate_mermaid_diagram()
        
        # 检测循环依赖
        self._detect_circular_dependencies()
        
        # 计算模块层级
        self._calculate_module_levels()
        
        return self.result
    
    def _build_module_map(self, py_files: List[Path]) -> Dict[str, Path]:
        """构建模块映射"""
        module_map = {}
        
        for py_file in py_files:
            try:
                rel_path = py_file.relative_to(self.project_path)
                # 将文件路径转换为模块名
                module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')
                module_map[module_name] = py_file
                self.modules.add(module_name)
            except ValueError:
                continue
        
        return module_map
    
    def _analyze_imports(self, py_files: List[Path], module_map: Dict[str, Path]):
        """分析导入关系"""
        import_patterns = [
            r'^from\s+([a-zA-Z0-9_.]+)\s+import',
            r'^import\s+([a-zA-Z0-9_.]+)'
        ]
        
        for py_file in py_files[:100]:  # 限制处理文件数量
            try:
                source_code = py_file.read_text(encoding='utf-8', errors='ignore')
                rel_path = py_file.relative_to(self.project_path)
                current_module = str(rel_path.with_suffix('')).replace(os.sep, '.')
                
                if current_module not in self.modules:
                    continue
                
                # 查找所有 import 语句
                lines = source_code.split('\n')
                for line in lines:
                    line = line.strip()
                    
                    for pattern in import_patterns:
                        match = re.match(pattern, line)
                        if match:
                            imported_module = match.group(1)
                            
                            # 只记录项目内部的导入
                            if self._is_internal_module(imported_module, module_map):
                                # 标准化模块名
                                normalized = self._normalize_module_name(imported_module, module_map)
                                if normalized and normalized != current_module:
                                    self.dependencies[current_module].add(normalized)
                            
                            break
            
            except Exception as e:
                print(f"分析文件 {py_file} 失败: {e}")
                continue
    
    def _is_internal_module(self, module_name: str, module_map: Dict[str, Path]) -> bool:
        """判断是否是内部模块"""
        # 简单判断：模块名的前缀是否匹配项目中的任何模块
        for existing_module in module_map.keys():
            if module_name == existing_module or existing_module.startswith(module_name + '.'):
                return True
        return False
    
    def _normalize_module_name(self, module_name: str, module_map: Dict[str, Path]) -> Optional[str]:
        """标准化模块名"""
        # 尝试找到完全匹配的模块
        if module_name in module_map:
            return module_name
        
        # 尝试找到父模块
        for existing_module in module_map.keys():
            if existing_module.startswith(module_name + '.'):
                return module_name
        
        # 尝试找到子模块
        for existing_module in module_map.keys():
            if module_name.startswith(existing_module + '.'):
                return existing_module
        
        return None
    
    def _generate_mermaid_diagram(self):
        """生成 Mermaid 图表"""
        # 使用 TD (Top-Down) 布局
        mermaid_lines = ['graph TD']
        
        # 添加节点和边
        added_edges = set()
        
        for module, deps in self.dependencies.items():
            # 简化模块名显示
            short_module = module.split('.')[-1]
            node_id = module.replace('.', '_')
            
            # 添加节点
            mermaid_lines.append(f'    {node_id}[{short_module}]')
            
            # 添加依赖边
            for dep in deps:
                dep_id = dep.replace('.', '_')
                edge = f'{node_id} --> {dep_id}'
                
                if edge not in added_edges:
                    short_dep = dep.split('.')[-1]
                    mermaid_lines.append(f'    {node_id} -->|依赖| {dep_id}')
                    added_edges.add(edge)
        
        # 添加样式
        mermaid_lines.append('')
        mermaid_lines.append('    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px')
        mermaid_lines.append('    classDef module fill:#e1f5ff,stroke:#0277bd,stroke-width:2px')
        
        self.result['mermaid_diagram'] = '\n'.join(mermaid_lines)
        
        # 生成依赖图数据
        self.result['dependency_graph'] = {
            k: list(v) for k, v in sorted(self.dependencies.items())
        }
    
    def _detect_circular_dependencies(self):
        """检测循环依赖"""
        visited = set()
        recursion_stack = set()
        circular_deps = []
        
        def dfs(module, path):
            if module in recursion_stack:
                # 找到循环
                cycle_start = path.index(module)
                cycle = path[cycle_start:] + [module]
                circular_deps.append(cycle)
                return True
            
            if module in visited:
                return False
            
            visited.add(module)
            recursion_stack.add(module)
            
            for dep in self.dependencies[module]:
                if dfs(dep, path + [module]):
                    pass
            
            recursion_stack.remove(module)
            return False
        
        for module in list(self.dependencies.keys()):
            if module not in visited:
                dfs(module, [])
        
        self.result['circular_dependencies'] = circular_deps
    
    def _calculate_module_levels(self):
        """计算模块层级（拓扑排序）"""
        in_degree = defaultdict(int)
        all_modules = set(self.dependencies.keys())
        
        for deps in self.dependencies.values():
            for dep in deps:
                all_modules.add(dep)
                in_degree[dep] += 1
        
        # 初始化入度
        for module in all_modules:
            if module not in in_degree:
                in_degree[module] = 0
        
        # 拓扑排序
        levels = defaultdict(list)
        queue = [m for m in all_modules if in_degree[m] == 0]
        level = 0
        
        while queue:
            current_level = queue
            queue = []
            
            for module in current_level:
                levels[level].append(module.split('.')[-1])
                
                for dep in self.dependencies[module]:
                    in_degree[dep] -= 1
                    if in_degree[dep] == 0:
                        queue.append(dep)
            
            level += 1
        
        self.result['module_levels'] = {k: sorted(v) for k, v in levels.items()}


def main():
    parser = argparse.ArgumentParser(description='分析依赖关系')
    parser.add_argument('--path', type=str, default='.', help='项目路径（默认当前目录）')
    parser.add_argument('--format', type=str, default='mermaid', choices=['mermaid', 'json'], help='输出格式')
    parser.add_argument('--output', type=str, default='dependency-analysis.json', help='输出文件路径')
    
    args = parser.parse_args()
    
    analyzer = DependencyAnalyzer(args.path)
    result = analyzer.analyze()
    
    # 输出结果
    output_path = Path(args.output)
    
    if args.format == 'json':
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    else:
        # 只输出 Mermaid 图表
        output_path.with_suffix('.mmd').write_text(result['mermaid_diagram'], encoding='utf-8')
        print(f"\nMermaid 图表已保存到: {output_path.with_suffix('.mmd')}")
        print(f"完整分析结果已保存到: {output_path}")
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"\n依赖分析完成！")
    print(f"分析的模块数: {len(result['dependency_graph'])}")
    print(f"发现的循环依赖: {len(result['circular_dependencies'])}")
    if result['circular_dependencies']:
        print("警告: 发现循环依赖:")
        for cycle in result['circular_dependencies']:
            print(f"  -> {' -> '.join([m.split('.')[-1] for m in cycle])}")


if __name__ == '__main__':
    main()
