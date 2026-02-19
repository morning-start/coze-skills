#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def parse_changelog(changelog_path: Path, version: str) -> dict:
    """解析 CHANGELOG.md 获取指定版本的信息"""
    
    if not changelog_path.exists():
        return {
            'title': f'Release {version}',
            'body': f'Automated release for version {version}'
        }
    
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    version_pattern = rf'## \[{re.escape(version)}\].*?\n(.*?)(?=## \[|$)'
    match = re.search(version_pattern, content, re.DOTALL)
    
    if not match:
        return {
            'title': f'Release {version}',
            'body': f'Automated release for version {version}'
        }
    
    body = match.group(1).strip()
    
    return {
        'title': f'Release {version}',
        'body': body
    }


def main():
    parser = argparse.ArgumentParser(description='Generate release notes from CHANGELOG.md')
    parser.add_argument('--version', required=True, help='Version number (e.g., 1.0.0)')
    parser.add_argument('--output', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    changelog_path = project_root / 'CHANGELOG.md'
    
    release_info = parse_changelog(changelog_path, args.version)
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(release_info['body'])
    
    print(f"Generated release notes for version {args.version}")
    print(f"Output: {output_path}")
    
    return 0


if __name__ == '__main__':
    exit(main())
