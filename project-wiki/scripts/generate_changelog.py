#!/usr/bin/env python3
"""
Changelog 生成脚本
功能：自动生成和管理 Changelog 文件
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class ChangelogGenerator:
    """Changelog 生成器"""
    
    CHANGE_TYPES = ['Added', 'Changed', 'Deprecated', 'Removed', 'Fixed', 'Security']
    
    def __init__(self, project_path: str, changelog_path: Optional[str] = None):
        self.project_path = Path(project_path).resolve()
        self.changelog_path = Path(changelog_path) if changelog_path else self.project_path / 'CHANGELOG.md'
        self.skill_path = Path(__file__).parent.parent
        self.templates_path = self.skill_path / 'assets' / 'changelog-templates'
        
        self.result = {
            'changelog_path': str(self.changelog_path),
            'version': None,
            'changes': {},
            'created': False
        }
    
    def generate(self, version: Optional[str] = None, version_type: Optional[str] = None, 
                 changes: Optional[Dict[str, List[str]]] = None, from_git: bool = False) -> Dict:
        """生成 Changelog"""
        
        # 如果 changelog 不存在，创建初始版本
        if not self.changelog_path.exists():
            self._create_initial_changelog()
            self.result['created'] = True
            print(f"创建初始 Changelog: {self.changelog_path}")
        
        # 如果指定了版本，添加新的版本条目
        if version:
            self._add_version_entry(version, version_type, changes)
        
        # 如果从 git log 生成
        if from_git:
            self._generate_from_git()
        
        return self.result
    
    def _create_initial_changelog(self):
        """创建初始 Changelog"""
        template_path = self.templates_path / 'changelog-template.md'
        
        if template_path.exists():
            content = template_path.read_text(encoding='utf-8')
        else:
            content = self._get_default_template()
        
        self.changelog_path.write_text(content, encoding='utf-8')
        print("创建初始 Changelog 文件")
    
    def _add_version_entry(self, version: str, version_type: Optional[str], 
                          changes: Optional[Dict[str, List[str]]]):
        """添加新的版本条目"""
        
        # 验证版本号格式
        if not self._validate_version(version):
            print(f"警告: 版本号 '{version}' 格式不正确，应为 MAJOR.MINOR.PATCH")
            return
        
        # 获取当前日期
        date = datetime.now().strftime('%Y-%m-%d')
        
        # 生成版本条目
        version_entry = self._generate_version_entry(version, date, changes)
        
        # 读取当前 Changelog
        content = self.changelog_path.read_text(encoding='utf-8')
        
        # 在 Unreleased 部分之后插入新版本
        unreleased_pattern = "## [Unreleased]"
        if unreleased_pattern in content:
            # 在 Unreleased 后面插入
            new_content = content.replace(
                unreleased_pattern,
                f"{unreleased_pattern}\n\n{version_entry}"
            )
        else:
            # 直接添加到开头
            new_content = f"{version_entry}\n\n{content}"
        
        # 写回文件
        self.changelog_path.write_text(new_content, encoding='utf-8')
        
        self.result['version'] = version
        self.result['changes'] = changes or {}
        
        print(f"添加版本条目: {version} ({date})")
        
        # 打印变更摘要
        if changes:
            for change_type, items in changes.items():
                if items:
                    print(f"  {change_type}: {len(items)} 项")
    
    def _generate_from_git(self):
        """从 Git log 生成变更记录"""
        import subprocess
        
        try:
            # 获取最近的 commit 消息
            result = subprocess.run(
                ['git', 'log', '--oneline', '-20'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("警告: 无法获取 Git log")
                return
            
            commits = result.stdout.strip().split('\n')
            
            # 分类变更
            changes = {
                'Added': [],
                'Changed': [],
                'Fixed': [],
                'Security': []
            }
            
            for commit in commits:
                if ':' in commit:
                    commit_type, message = commit.split(':', 1)
                    commit_type = commit_type.strip().lower()
                    message = message.strip()
                    
                    if commit_type in ['feat', 'feature']:
                        changes['Added'].append(message)
                    elif commit_type in ['fix', 'bugfix']:
                        changes['Fixed'].append(message)
                    elif commit_type in ['refactor', 'perf']:
                        changes['Changed'].append(message)
                    elif commit_type in ['security']:
                        changes['Security'].append(message)
            
            # 打印分类结果
            print("\n从 Git log 提取的变更：")
            for change_type, items in changes.items():
                if items:
                    print(f"  {change_type}:")
                    for item in items:
                        print(f"    - {item}")
            
            print("\n请手动将上述变更添加到 Changelog 的 Unreleased 部分")
            
        except FileNotFoundError:
            print("警告: Git 未安装或不在 PATH 中")
    
    def _generate_version_entry(self, version: str, date: str, 
                                changes: Optional[Dict[str, List[str]]]) -> str:
        """生成版本条目"""
        entry = f"## [{version}] - {date}\n\n"
        
        if not changes:
            changes = {
                'Added': [],
                'Changed': [],
                'Deprecated': [],
                'Removed': [],
                'Fixed': [],
                'Security': []
            }
        
        for change_type in self.CHANGE_TYPES:
            items = changes.get(change_type, [])
            if items:
                entry += f"### {change_type}\n"
                for item in items:
                    entry += f"- {item}\n"
                entry += "\n"
        
        return entry.strip() + "\n"
    
    def _validate_version(self, version: str) -> bool:
        """验证版本号格式"""
        parts = version.split('.')
        if len(parts) != 3:
            return False
        
        try:
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
            return major >= 0 and minor >= 0 and patch >= 0
        except ValueError:
            return False
    
    def _get_default_template(self) -> str:
        """获取默认模板"""
        return """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2024-01-15

### Added
- 初始版本发布
- 实现核心功能
- 添加文档

### Changed
- 无

### Deprecated
- 无

### Removed
- 无

### Fixed
- 无

### Security
- 无

[Unreleased]: https://github.com/user/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/user/repo/compare/v0.9.0...v1.0.0
"""


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Changelog 生成工具')
    parser.add_argument('--path', type=str, default='.', help='项目路径')
    parser.add_argument('--changelog-path', type=str, default=None, help='Changelog 文件路径')
    parser.add_argument('--version', type=str, default=None, help='版本号（如 1.0.0）')
    parser.add_argument('--type', type=str, default=None, 
                       choices=['major', 'minor', 'patch'],
                       help='版本类型（自动递增版本号）')
    parser.add_argument('--from-git', action='store_true', help='从 Git log 生成变更记录')
    
    args = parser.parse_args()
    
    generator = ChangelogGenerator(args.path, args.changelog_path)
    
    # 如果指定了版本类型，自动计算新版本号
    if args.type and not args.version:
        args.version = generator._calculate_next_version(args.type)
        print(f"自动计算版本号: {args.version}")
    
    result = generator.generate(
        version=args.version,
        version_type=args.type,
        from_git=args.from_git
    )
    
    print(f"\nChangelog 生成完成！")
    print(f"路径: {result['changelog_path']}")
    if result.get('version'):
        print(f"版本: {result['version']}")


if __name__ == '__main__':
    main()
