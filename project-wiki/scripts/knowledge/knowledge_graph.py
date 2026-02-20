#!/usr/bin/env python3
"""
知识图谱生成脚本
功能：分析项目结构，生成知识图谱节点和关系
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class KnowledgeGraphBuilder:
    """知识图谱构建器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.graph = {
            'nodes': [],
            'edges': [],
            'concepts': []
        }
        self.node_types = {
            'module': '模块',
            'api': 'API',
            'class': '类',
            'function': '函数',
            'database': '数据库',
            'config': '配置',
            'service': '服务'
        }
    
    def build(self) -> Dict:
        """构建知识图谱"""
        print(f"构建知识图谱: {self.project_path}")
        
        if not self.project_path.exists():
            raise FileNotFoundError(f"项目路径不存在: {self.project_path}")
        
        # 分析项目结构
        self._analyze_structure()
        
        # 分析代码文件
        self._analyze_code_files()
        
        # 分析配置文件
        self._analyze_config_files()
        
        # 生成关系
        self._build_relationships()
        
        return self.graph
    
    def _analyze_structure(self):
        """分析项目结构"""
        directories = []
        
        for item in self.project_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                node_id = f"dir:{item.name}"
                directories.append({
                    'id': node_id,
                    'name': item.name,
                    'type': 'module',
                    'description': f"目录: {item.name}",
                    'path': str(item.relative_to(self.project_path))
                })
        
        self.graph['nodes'].extend(directories)
    
    def _analyze_code_files(self):
        """分析代码文件"""
        common_extensions = ['.py', '.js', '.ts', '.go', '.java', '.rs']
        
        for ext in common_extensions:
            files = list(self.project_path.rglob(f'*{ext}'))
            files = [f for f in files if self._is_main_file(f)]
            
            for file in files[:20]:  # 限制数量
                node_id = f"file:{file.stem}"
                self.graph['nodes'].append({
                    'id': node_id,
                    'name': file.stem,
                    'type': 'module',
                    'description': f"文件: {file.name}",
                    'path': str(file.relative_to(self.project_path))
                })
    
    def _analyze_config_files(self):
        """分析配置文件"""
        config_patterns = [
            'package.json', 'tsconfig.json', 'vite.config.js',
            'requirements.txt', 'pyproject.toml', 'setup.py',
            'go.mod', 'Cargo.toml', 'pom.xml', 'build.gradle',
            'pubspec.yaml', '.env', 'config.yml', 'config.yaml'
        ]
        
        for pattern in config_patterns:
            config_files = list(self.project_path.rglob(pattern))
            for config_file in config_files:
                node_id = f"config:{config_file.stem}"
                self.graph['nodes'].append({
                    'id': node_id,
                    'name': config_file.name,
                    'type': 'config',
                    'description': f"配置文件: {config_file.name}",
                    'path': str(config_file.relative_to(self.project_path))
                })
    
    def _is_main_file(self, file: Path) -> bool:
        """判断是否是主文件"""
        main_names = ['main', 'app', 'index', 'server', 'init']
        return any(name in file.stem.lower() for name in main_names)
    
    def _build_relationships(self):
        """构建节点间的关系"""
        relationships = defaultdict(set)
        
        # 文件到目录的关系
        for node in self.graph['nodes']:
            if node['type'] in ['module', 'api', 'function']:
                path_parts = node['path'].split('/')
                if len(path_parts) > 1:
                    parent_dir = '/'.join(path_parts[:-1])
                    parent_node = self._find_node_by_path(parent_dir)
                    if parent_node:
                        relationships[node['id']].add(parent_node['id'])
        
        # 生成边
        for source, targets in relationships.items():
            for target in targets:
                self.graph['edges'].append({
                    'from': source,
                    'to': target,
                    'type': 'contains'
                })
    
    def _find_node_by_path(self, path: str):
        """根据路径查找节点"""
        for node in self.graph['nodes']:
            if node['path'] == path:
                return node
        return None
    
    def generate_mermaid(self) -> str:
        """生成 Mermaid 知识图谱"""
        lines = ['graph TB']
        
        # 添加节点
        for node in self.graph['nodes']:
            node_id = node['id'].replace(':', '_')
            label = node['name'][:30]  # 限制长度
            node_type = node['type']
            
            # 根据类型设置不同样式
            style_map = {
                'module': 'fill:#e1f5ff,stroke:#0277bd',
                'api': 'fill:#fff3e0,stroke:#d81b60',
                'config': 'fill:#fff9c4,stroke:#f57c00',
                'database': 'fill:#fce4ec,stroke:#00695c'
            }
            style = style_map.get(node_type, 'fill:#f9f9f9,stroke:#333')
            
            lines.append(f'    {node_id}["{label}", "{style}"]')
        
        # 添加边
        for edge in self.graph['edges']:
            from_id = edge['from'].replace(':', '_')
            to_id = edge['to'].replace(':', '_')
            lines.append(f'    {from_id} --> {to_id}')
        
        # 添加图例
        lines.append('')
        lines.append('    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px')
        lines.append('    classDef module fill:#e1f5ff,stroke:#0277bd,stroke-width:2px')
        lines.append('    classDef api fill:#fff3e0,stroke:#d81b60,stroke-width:2px')
        lines.append('    classDef config fill:#fff9c4,stroke:#f57c00,stroke-width:2px')
        
        return '\n'.join(lines)
    
    def export_json(self) -> str:
        """导出为 JSON"""
        return json.dumps(self.graph, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='构建项目知识图谱')
    parser.add_argument('--path', type=str, default='.', help='项目路径（默认当前目录）')
    parser.add_argument('--output', type=str, default='knowledge-graph.json', help='输出文件路径')
    parser.add_argument('--format', type=str, default='json', choices=['json', 'mermaid'], help='输出格式')
    
    args = parser.parse_args()
    
    builder = KnowledgeGraphBuilder(args.path)
    graph = builder.build()
    
    # 输出结果
    output_path = Path(args.output)
    
    if args.format == 'mermaid':
        mermaid_path = output_path.with_suffix('.mmd')
        mermaid_content = builder.generate_mermaid()
        mermaid_path.write_text(mermaid_content, encoding='utf-8')
        print(f"Mermaid 知识图谱已保存到: {mermaid_path}")
    
    # 总是导出 JSON
    json_content = builder.export_json()
    output_path.write_text(json_content, encoding='utf-8')
    
    print(f"\n知识图谱构建完成！")
    print(f"节点数: {len(graph['nodes'])}")
    print(f"关系数: {len(graph['edges'])}")
    print(f"JSON 结果已保存到: {output_path}")


if __name__ == '__main__':
    main()
