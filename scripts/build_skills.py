#!/usr/bin/env python3
import argparse
import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
import yaml


def get_skill_info(skill_dir: Path) -> dict:
    """从 SKILL.md 读取技能信息"""
    skill_file = skill_dir / "SKILL.md"
    
    if not skill_file.exists():
        return None
    
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    info = {
        'name': skill_dir.name,
        'path': skill_dir,
        'has_skill_md': True
    }
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('---'):
            if i == 0:
                continue
            elif line.strip() == '---':
                break
            elif ':' in line:
                key, value = line.split(':', 1)
                info[key.strip().lower()] = value.strip()
    
    return info


def build_skill_package(skill_info: dict, version: str, output_dir: Path) -> Path:
    """构建单个技能包"""
    skill_name = skill_info['name']
    skill_path = skill_info['path']
    
    package_name = f"{skill_name}-{version}.skill"
    package_path = output_dir / package_name
    
    print(f"Building {skill_name} -> {package_name}")
    
    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path)
                zipf.write(file_path, arcname)
    
    print(f"  Created: {package_path} ({package_path.stat().st_size} bytes)")
    return package_path


def main():
    parser = argparse.ArgumentParser(description='Build skill packages')
    parser.add_argument('--version', required=True, help='Version number (e.g., 1.0.0)')
    parser.add_argument('--output-dir', default='dist', help='Output directory for packages')
    parser.add_argument('--skill', help='Build specific skill only')
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    skills_dir = project_root
    
    if args.skill:
        skill_dirs = [skills_dir / args.skill]
    else:
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    built_packages = []
    
    for skill_dir in sorted(skill_dirs):
        if not skill_dir.is_dir():
            continue
        
        skill_info = get_skill_info(skill_dir)
        
        if not skill_info or not skill_info.get('has_skill_md'):
            print(f"Skipping {skill_dir.name}: No SKILL.md found")
            continue
        
        try:
            package_path = build_skill_package(skill_info, args.version, output_dir)
            built_packages.append(package_path)
        except Exception as e:
            print(f"Error building {skill_dir.name}: {e}")
    
    print(f"\nBuilt {len(built_packages)} skill packages:")
    for pkg in built_packages:
        print(f"  - {pkg.name}")
    
    return 0


if __name__ == '__main__':
    exit(main())
