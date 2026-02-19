#!/usr/bin/env python3
"""
Wiki 结构创建脚本
功能：根据项目复杂度自动创建 Wiki 文件夹结构
"""

import os
import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional


class WikiStructureCreator:
    """Wiki 结构创建器"""
    
    def __init__(self, project_path: str, wiki_path: Optional[str] = None):
        self.project_path = Path(project_path).resolve()
        self.wiki_path = Path(wiki_path) if wiki_path else self.project_path / 'wiki'
        self.skill_path = Path(__file__).parent.parent
        self.templates_path = self.skill_path / 'assets' / 'wiki-templates'
        
        self.result = {
            'wiki_path': str(self.wiki_path),
            'structure_type': '',
            'created_files': [],
            'created_dirs': []
        }
    
    def create(self) -> Dict:
        """创建 Wiki 结构"""
        print(f"创建 Wiki 结构: {self.wiki_path}")
        
        # 读取复杂度分析结果
        complexity_file = self.project_path / 'complexity-analysis.json'
        if not complexity_file.exists():
            print("警告: 未找到复杂度分析结果，请先运行 evaluate_complexity.py")
            print("将使用默认结构（分层结构）")
            structure_type = 'hierarchical'
        else:
            with open(complexity_file, 'r') as f:
                complexity_data = json.load(f)
            structure_type = complexity_data.get('structure_type', 'hierarchical')
        
        print(f"结构类型: {structure_type}")
        
        # 创建 Wiki 目录
        self.wiki_path.mkdir(exist_ok=True)
        
        # 根据结构类型创建文件
        if structure_type == 'flat':
            self._create_flat_structure()
        else:
            self._create_hierarchical_structure()
        
        # 复制模板文件
        self._copy_templates()
        
        self.result['structure_type'] = structure_type
        
        print(f"\nWiki 结构创建完成！")
        print(f"路径: {self.wiki_path}")
        print(f"创建的目录: {len(self.result['created_dirs'])} 个")
        print(f"创建的文件: {len(self.result['created_files'])} 个")
        
        return self.result
    
    def _create_flat_structure(self):
        """创建平铺结构"""
        print("创建平铺结构...")
        
        files = {
            'README.md': 'simple-readme.md',
            '架构.md': 'architecture.md',
            'API.md': None,  # 创建空文件
            '部署.md': None,
            '开发指南.md': None,
            '常见问题.md': None
        }
        
        for filename, template in files.items():
            file_path = self.wiki_path / filename
            if template:
                template_path = self.templates_path / template
                if template_path.exists():
                    shutil.copy(template_path, file_path)
                    print(f"  创建文件: {filename} (从模板)")
                else:
                    file_path.touch()
                    print(f"  创建文件: {filename} (空文件)")
            else:
                file_path.touch()
                print(f"  创建文件: {filename} (空文件)")
            
            self.result['created_files'].append(filename)
    
    def _create_hierarchical_structure(self):
        """创建分层结构"""
        print("创建分层结构...")
        
        # 创建文件夹
        directories = [
            '01-概览',
            '02-开发指南',
            '03-API文档',
            '04-模块文档',
            '05-部署运维',
            '06-常见问题'
        ]
        
        for dirname in directories:
            dir_path = self.wiki_path / dirname
            dir_path.mkdir(exist_ok=True)
            print(f"  创建目录: {dirname}/")
            self.result['created_dirs'].append(dirname)
        
        # 创建 README.md
        readme_path = self.wiki_path / 'README.md'
        template_path = self.templates_path / 'complex-readme.md'
        if template_path.exists():
            shutil.copy(template_path, readme_path)
            print(f"  创建文件: README.md (从模板)")
        else:
            readme_path.touch()
            print(f"  创建文件: README.md (空文件)")
        
        self.result['created_files'].append('README.md')
        
        # 创建各文件夹下的文件
        folder_files = {
            '01-概览': ['项目介绍.md', '架构设计.md', '技术栈.md', '快速开始.md'],
            '02-开发指南': ['开发环境.md', '开发规范.md', '代码贡献.md', '调试技巧.md'],
            '03-API文档': ['用户API.md', '管理API.md', '内部API.md', '数据模型.md'],
            '05-部署运维': ['部署指南.md', '运维手册.md', '监控告警.md'],
            '06-常见问题': ['FAQ.md', '故障排查.md']
        }
        
        for folder, files in folder_files.items():
            for filename in files:
                file_path = self.wiki_path / folder / filename
                file_path.touch()
                print(f"  创建文件: {folder}/{filename}")
                self.result['created_files'].append(f"{folder}/{filename}")
    
    def _copy_templates(self):
        """复制模板文件到 Wiki 目录"""
        # 创建 templates 目录
        templates_dir = self.wiki_path / '.templates'
        templates_dir.mkdir(exist_ok=True)
        
        # 复制模板文件
        if self.templates_path.exists():
            for template_file in self.templates_path.glob('*.md'):
                target = templates_dir / template_file.name
                shutil.copy(template_file, target)
                print(f"  复制模板: {template_file.name}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Wiki 结构创建工具')
    parser.add_argument('--path', type=str, default='.', help='项目路径')
    parser.add_argument('--wiki-path', type=str, default=None, help='Wiki 目录路径（默认为 ./wiki）')
    
    args = parser.parse_args()
    
    creator = WikiStructureCreator(args.path, args.wiki_path)
    result = creator.create()
    
    # 保存结果
    output_file = Path(args.path) / 'wiki-structure.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n创建结果已保存到: {output_file}")


if __name__ == '__main__':
    main()
