#!/usr/bin/env python3
"""
技能文件生成工具

功能:根据配置 JSON 生成完整的 Skill 文件结构
输出:SKILL.md、scripts/、references/、assets/ 文件
"""

import json
import sys
import os
from pathlib import Path
from jinja2 import Template


def load_config(config_path: str) -> dict:
    """加载技能配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 配置文件不存在: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: 配置文件格式错误: {e}")
        sys.exit(1)


def load_template(template_path: str) -> Template:
    """加载 Jinja2 模板"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return Template(f.read())
    except FileNotFoundError:
        print(f"错误: 模板文件不存在: {template_path}")
        sys.exit(1)


def create_directory_structure(output_dir: Path, config: dict):
    """创建 Skill 目录结构"""
    # 创建主目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建子目录（按需）
    if config.get('scripts'):
        (output_dir / 'scripts').mkdir(exist_ok=True)
    
    if config.get('references'):
        (output_dir / 'references').mkdir(exist_ok=True)
    
    if config.get('assets'):
        (output_dir / 'assets').mkdir(exist_ok=True)


def generate_skill_md(output_dir: Path, config: dict, template: Template):
    """生成 SKILL.md 文件"""
    skill_md = template.render(config=config)
    
    with open(output_dir / 'SKILL.md', 'w', encoding='utf-8') as f:
        f.write(skill_md)
    
    print(f"已生成: {output_dir / 'SKILL.md'}")


def generate_scripts(output_dir: Path, config: dict, template: Template):
    """生成 scripts/ 文件"""
    if not config.get('scripts'):
        return
    
    for script_config in config['scripts']:
        script_content = template.render(
            name=script_config['name'],
            description=script_config.get('description', ''),
            functions=script_config.get('functions', [])
        )
        
        script_path = output_dir / 'scripts' / script_config['name']
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"已生成: {script_path}")


def generate_references(output_dir: Path, config: dict):
    """生成 references/ 文件"""
    if not config.get('references'):
        return
    
    for ref_config in config['references']:
        ref_path = output_dir / 'references' / ref_config['name']
        with open(ref_path, 'w', encoding='utf-8') as f:
            f.write(ref_config['content'])
        
        print(f"已生成: {ref_path}")


def generate_assets(output_dir: Path, config: dict):
    """生成 assets/ 文件"""
    if not config.get('assets'):
        return
    
    for asset_config in config['assets']:
        asset_path = output_dir / 'assets' / asset_config['path']
        asset_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(asset_path, 'w', encoding='utf-8') as f:
            f.write(asset_config['content'])
        
        print(f"已生成: {asset_path}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='根据配置生成 Skill 文件')
    parser.add_argument('--config', required=True, help='配置文件路径')
    parser.add_argument('--output', required=True, help='输出目录')
    parser.add_argument('--templates', help='模板目录路径（默认: assets/templates）')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 确定模板目录
    if args.templates:
        templates_dir = Path(args.templates)
    else:
        # 假设在 skill-creator 目录下运行
        current_dir = Path(__file__).parent.parent
        templates_dir = current_dir / 'assets' / 'templates'
    
    # 加载模板
    skill_template = load_template(templates_dir / 'skill-template.md')
    script_template = load_template(templates_dir / 'python-script.py')
    
    # 创建输出目录
    output_dir = Path(args.output)
    
    # 生成文件
    print(f"开始生成 Skill 文件到: {output_dir}")
    create_directory_structure(output_dir, config)
    generate_skill_md(output_dir, config, skill_template)
    generate_scripts(output_dir, config, script_template)
    generate_references(output_dir, config)
    generate_assets(output_dir, config)
    
    print(f"\nSkill 文件生成完成!")
    print(f"下一步: 使用 package_skill 工具打包 {output_dir}")


if __name__ == '__main__':
    main()
