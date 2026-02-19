#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def update_version_in_file(file_path: Path, version: str) -> bool:
    """更新文件中的版本号"""
    
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    if file_path.name == 'pyproject.toml':
        pattern = r'version\s*=\s*["\']([^"\']+)["\']'
        replacement = f'version = "{version}"'
    elif file_path.name == 'CHANGELOG.md':
        pattern = r'## \[([^\]]+)\]'
        replacement = f'## [{version}]'
    else:
        return False
    
    new_content = re.sub(pattern, replacement, content, count=1)
    
    if new_content != original_content:
        file_path.write_text(new_content, encoding='utf-8')
        return True
    
    return False


def main():
    parser = argparse.ArgumentParser(description='Update project version')
    parser.add_argument('version', help='New version number (e.g., 1.0.0, 1.1.0, 2.0.0)')
    parser.add_argument('--commit', action='store_true', help='Commit the changes')
    parser.add_argument('--tag', action='store_true', help='Create git tag')
    
    args = parser.parse_args()
    
    version = args.version
    
    if not re.match(r'^\d+\.\d+\.\d+', version):
        print(f"Error: Invalid version format '{version}'. Expected format: X.Y.Z")
        return 1
    
    project_root = Path(__file__).parent.parent
    
    files_to_update = [
        project_root / 'pyproject.toml',
        project_root / 'CHANGELOG.md',
    ]
    
    updated_files = []
    
    for file_path in files_to_update:
        if file_path.exists():
            if update_version_in_file(file_path, version):
                updated_files.append(file_path)
                print(f"Updated: {file_path}")
            else:
                print(f"No changes: {file_path}")
    
    if not updated_files:
        print("No files were updated")
        return 0
    
    print(f"\nVersion updated to {version}")
    print(f"Updated {len(updated_files)} file(s)")
    
    if args.commit or args.tag:
        import subprocess
        
        if args.commit:
            commit_msg = f"chore: bump version to {version}"
            subprocess.run(['git', 'add'] + [str(f) for f in updated_files], check=True)
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print(f"\nCommitted: {commit_msg}")
        
        if args.tag:
            tag_name = f"v{version}"
            subprocess.run(['git', 'tag', '-a', tag_name, '-m', f"Release {version}"], check=True)
            print(f"Created tag: {tag_name}")
            print("\nTo push the tag, run:")
            print(f"  git push origin {tag_name}")
    
    return 0


if __name__ == '__main__':
    exit(main())
