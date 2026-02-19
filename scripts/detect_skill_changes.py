#!/usr/bin/env python3
"""
技能变更检测脚本
用于检测哪些技能在上次发布后有过更新
支持多种发布场景：
1. 新技能添加
2. 单个技能更新
3. 多个技能更新
4. 所有技能统一版本更新
"""
import argparse
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import json


def parse_skill_md(skill_dir: Path) -> Dict:
    """解析 SKILL.md 文件，提取元数据"""
    skill_file = skill_dir / "SKILL.md"
    
    if not skill_file.exists():
        return {}
    
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    info = {
        'name': skill_dir.name,
        'path': skill_dir,
        'has_skill_md': True
    }
    
    # 解析 YAML frontmatter
    yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    
    if yaml_match:
        yaml_content = yaml_match.group(1)
        
        for line in yaml_content.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('#'):
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


def get_all_skills(project_root: Path) -> List[Dict]:
    """获取所有技能目录"""
    skills = []
    
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


def get_last_tag() -> Optional[str]:
    """获取最新的 tag"""
    try:
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_changed_files_since_tag(tag: str) -> List[str]:
    """获取自指定 tag 以来变更的文件"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', f'{tag}..HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        return []


def detect_changed_skills(project_root: Path, changed_files: List[str]) -> List[str]:
    """根据变更文件检测哪些技能有更新"""
    changed_skills = set()
    
    for file_path in changed_files:
        if not file_path:
            continue
        
        # 解析文件路径，确定属于哪个技能
        parts = file_path.split('/')
        if len(parts) > 0:
            skill_name = parts[0]
            # 检查是否是技能目录
            skill_dir = project_root / skill_name
            if skill_dir.exists() and (skill_dir / 'SKILL.md').exists():
                changed_skills.add(skill_name)
    
    return sorted(list(changed_skills))


def detect_new_skills(project_root: Path, tag: str) -> List[str]:
    """检测新增的技能"""
    try:
        # 获取所有技能
        all_skills = get_all_skills(project_root)
        all_skill_names = {s['name'] for s in all_skills}
        
        # 获取 tag 时的文件列表
        result = subprocess.run(
            ['git', 'ls-tree', '-r', '--name-only', tag],
            capture_output=True,
            text=True,
            check=True
        )
        old_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        # 解析 tag 时的技能
        old_skills = set()
        for file_path in old_files:
            parts = file_path.split('/')
            if len(parts) > 0:
                old_skills.add(parts[0])
        
        # 找出新增的技能
        new_skills = all_skill_names - old_skills
        return sorted(list(new_skills))
    
    except subprocess.CalledProcessError:
        return []


def get_skill_version_info(skill_name: str, project_root: Path) -> Dict:
    """获取技能的版本信息"""
    skill_dir = project_root / skill_name
    skill_info = parse_skill_md(skill_dir)
    
    return {
        'name': skill_name,
        'version': skill_info.get('version', '1.0.0'),
        'description': skill_info.get('description', 'No description')[:60]
    }


def main():
    parser = argparse.ArgumentParser(
        description='Detect skill changes since last release',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用场景:
  1. 检测所有变更（包括新增和修改）:
     python detect_skill_changes.py --all
     
  2. 仅检测新增技能:
     python detect_skill_changes.py --new-only
     
  3. 仅检测修改的技能:
     python detect_skill_changes.py --modified-only
     
  4. 输出为 JSON 格式（用于 CI/CD）:
     python detect_skill_changes.py --all --json
     
  5. 指定对比的 tag:
     python detect_skill_changes.py --all --since v1.0.0
        """
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Detect all changes (new and modified skills)'
    )
    parser.add_argument(
        '--new-only',
        action='store_true',
        help='Detect only new skills'
    )
    parser.add_argument(
        '--modified-only',
        action='store_true',
        help='Detect only modified skills'
    )
    parser.add_argument(
        '--since',
        help='Specify tag to compare against (default: latest tag)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON format'
    )
    parser.add_argument(
        '--output',
        help='Output file (default: stdout)'
    )
    
    args = parser.parse_args()
    
    if not (args.all or args.new_only or args.modified_only):
        parser.print_help()
        return 1
    
    project_root = Path(__file__).parent.parent
    
    # 获取对比的 tag
    tag = args.since or get_last_tag()
    
    if not tag:
        print("No tag found to compare against!")
        print("Use --since to specify a tag, or create a tag first.")
        return 1
    
    # 检测结果
    result = {
        'tag': tag,
        'timestamp': datetime.now().isoformat(),
        'new_skills': [],
        'modified_skills': [],
        'all_changed_skills': []
    }
    
    # 检测新增技能
    if args.all or args.new_only:
        new_skills = detect_new_skills(project_root, tag)
        result['new_skills'] = [get_skill_version_info(name, project_root) for name in new_skills]
    
    # 检测修改的技能
    if args.all or args.modified_only:
        changed_files = get_changed_files_since_tag(tag)
        modified_skills = detect_changed_skills(project_root, changed_files)
        
        # 排除新增的技能
        if args.all:
            new_skill_names = {s['name'] for s in result['new_skills']}
            modified_skills = [s for s in modified_skills if s not in new_skill_names]
        
        result['modified_skills'] = [get_skill_version_info(name, project_root) for name in modified_skills]
    
    # 合并所有变更的技能
    if args.all:
        all_names = {s['name'] for s in result['new_skills']} | {s['name'] for s in result['modified_skills']}
        result['all_changed_skills'] = sorted(list(all_names))
    
    # 输出结果
    if args.json:
        output = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        # 文本格式输出
        lines = []
        lines.append(f"Skill Changes Detection")
        lines.append(f"Comparing against: {tag}")
        lines.append(f"Timestamp: {result['timestamp']}")
        lines.append("")
        
        if args.all or args.new_only:
            lines.append(f"New Skills ({len(result['new_skills'])}):")
            if result['new_skills']:
                for skill in result['new_skills']:
                    lines.append(f"  + {skill['name']:<30} v{skill['version']:<10} {skill['description']}...")
            else:
                lines.append("  (none)")
            lines.append("")
        
        if args.all or args.modified_only:
            lines.append(f"Modified Skills ({len(result['modified_skills'])}):")
            if result['modified_skills']:
                for skill in result['modified_skills']:
                    lines.append(f"  ~ {skill['name']:<30} v{skill['version']:<10} {skill['description']}...")
            else:
                lines.append("  (none)")
            lines.append("")
        
        if args.all:
            lines.append(f"Total Changed: {len(result['all_changed_skills'])} skill(s)")
        
        output = '\n'.join(lines)
    
    # 输出到文件或 stdout
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Output written to: {args.output}")
    else:
        print(output)
    
    # 返回码：有变更返回 0，无变更返回 1（用于 CI/CD 判断）
    has_changes = len(result.get('all_changed_skills', [])) > 0
    if args.all:
        return 0 if has_changes else 1
    
    return 0


if __name__ == '__main__':
    exit(main())
