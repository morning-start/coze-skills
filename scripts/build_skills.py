#!/usr/bin/env python3
"""
技能打包脚本
支持从 SKILL.md 读取独立版本号，处理多种发布场景
"""
import argparse
import os
import zipfile
from pathlib import Path
from typing import Optional
import re


def parse_skill_md(skill_dir: Path) -> dict:
    """解析 SKILL.md 文件，提取元数据"""
    skill_file = skill_dir / "SKILL.md"
    
    if not skill_file.exists():
        return {}
    
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析 YAML frontmatter
    info = {
        'name': skill_dir.name,
        'path': skill_dir,
        'has_skill_md': True
    }
    
    # 匹配 --- 包裹的 YAML 内容
    yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    
    if yaml_match:
        yaml_content = yaml_match.group(1)
        
        # 解析简单的 key: value 格式
        for line in yaml_content.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                # 处理可能的多行值（简单处理，取第一行）
                key_value = line.split(':', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    key = key.strip()
                    value = value.strip()
                    # 移除引号
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    info[key] = value
    
    return info


def get_skill_version(skill_info: dict, override_version: Optional[str] = None) -> str:
    """获取技能版本号
    
    优先级：
    1. 命令行指定的版本号
    2. SKILL.md 中的 version 字段
    3. 默认版本 1.0.0
    """
    if override_version:
        return override_version
    
    return skill_info.get('version', '1.0.0')


def build_skill_package(skill_info: dict, version: str, output_dir: Path) -> Optional[Path]:
    """构建单个技能包
    
    Args:
        skill_info: 技能信息字典
        version: 版本号（如果为 None，则使用 SKILL.md 中的版本）
        output_dir: 输出目录
    
    Returns:
        打包后的文件路径，失败返回 None
    """
    skill_name = skill_info['name']
    skill_path = skill_info['path']
    
    # 确定最终版本号
    final_version = version if version else get_skill_version(skill_info)
    
    package_name = f"{skill_name}-{final_version}.skill"
    package_path = output_dir / package_name
    
    print(f"Building {skill_name} (v{final_version}) -> {package_name}")
    
    try:
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(skill_path):
                # 排除不需要的文件和目录
                dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'dist', 'venv', '.venv']]
                
                for file in files:
                    # 排除不需要的文件
                    if file.endswith(('.pyc', '.pyo', '.skill')):
                        continue
                    
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(skill_path)
                    zipf.write(file_path, arcname)
        
        size = package_path.stat().st_size
        print(f"  ✓ Created: {package_path} ({size:,} bytes)")
        return package_path
    
    except Exception as e:
        print(f"  ✗ Error building {skill_name}: {e}")
        return None


def get_all_skills(project_root: Path) -> list:
    """获取所有技能目录"""
    skills = []
    
    # 排除的目录
    exclude_dirs = {
        '.git', '.github', 'scripts', 'docs', 'dist', 
        'venv', '.venv', '__pycache__', 'node_modules'
    }
    
    for item in project_root.iterdir():
        if item.is_dir() and item.name not in exclude_dirs:
            skill_info = parse_skill_md(item)
            if skill_info.get('has_skill_md'):
                skills.append(skill_info)
    
    return sorted(skills, key=lambda x: x['name'])


def main():
    parser = argparse.ArgumentParser(
        description='Build skill packages with independent versioning',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用场景:
  1. 发布所有技能（使用各自版本号）:
     python build_skills.py --all
     
  2. 发布所有技能（统一版本号）:
     python build_skills.py --all --version 2.0.0
     
  3. 发布单个技能（使用 SKILL.md 版本）:
     python build_skills.py --skill recruitment-processor
     
  4. 发布单个技能（指定版本）:
     python build_skills.py --skill recruitment-processor --version 1.5.0
     
  5. 发布多个指定技能:
     python build_skills.py --skill skill1 --skill skill2
        """
    )
    
    parser.add_argument(
        '--all', 
        action='store_true',
        help='Build all skills'
    )
    parser.add_argument(
        '--skill', 
        action='append',
        dest='skills',
        help='Build specific skill(s), can be used multiple times'
    )
    parser.add_argument(
        '--version', 
        help='Override version (if not specified, use version from SKILL.md)'
    )
    parser.add_argument(
        '--output-dir', 
        default='dist',
        help='Output directory for packages (default: dist)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available skills and their versions'
    )
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取所有技能
    all_skills = get_all_skills(project_root)
    
    if not all_skills:
        print("No skills found!")
        return 1
    
    # 列出所有技能
    if args.list:
        print("Available skills:")
        print("-" * 60)
        for skill in all_skills:
            version = get_skill_version(skill)
            desc = skill.get('description', 'No description')[:50]
            print(f"  {skill['name']:<30} v{version:<10} {desc}...")
        return 0
    
    # 确定要构建的技能
    skills_to_build = []
    
    if args.all:
        skills_to_build = all_skills
    elif args.skills:
        # 查找指定的技能
        skill_names = {s['name']: s for s in all_skills}
        for skill_name in args.skills:
            if skill_name in skill_names:
                skills_to_build.append(skill_names[skill_name])
            else:
                print(f"Warning: Skill '{skill_name}' not found, skipping")
    else:
        parser.print_help()
        return 1
    
    if not skills_to_build:
        print("No skills to build!")
        return 1
    
    # 构建技能包
    print(f"\nBuilding {len(skills_to_build)} skill(s)...")
    print("=" * 60)
    
    built_packages = []
    failed_builds = []
    
    for skill_info in skills_to_build:
        package_path = build_skill_package(skill_info, args.version, output_dir)
        if package_path:
            built_packages.append(package_path)
        else:
            failed_builds.append(skill_info['name'])
    
    # 输出结果
    print("\n" + "=" * 60)
    print(f"Build complete: {len(built_packages)} succeeded, {len(failed_builds)} failed")
    
    if built_packages:
        print(f"\nBuilt packages:")
        for pkg in built_packages:
            print(f"  ✓ {pkg.name}")
    
    if failed_builds:
        print(f"\nFailed builds:")
        for name in failed_builds:
            print(f"  ✗ {name}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
