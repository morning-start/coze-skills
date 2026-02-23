#!/usr/bin/env python3
"""
技能验证器
验证技能是否符合规范，包括命名、结构、格式等
"""

import argparse
import sys
import re
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple


# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='验证技能是否符合规范',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--skill-path',
        type=str,
        required=True,
        help='技能目录路径'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='启用详细日志'
    )

    return parser.parse_args()


def validate_naming(skill_dir: Path) -> Tuple[bool, List[str]]:
    """验证命名规范"""
    errors = []

    # 验证目录名格式
    skill_name = skill_dir.name

    # 检查是否使用小写字母和连字符
    if not re.match(r'^[a-z0-9-]+$', skill_name):
        errors.append(f"目录名格式错误: {skill_name}（应使用小写字母+连字符）")

    # 检查是否包含 -skill 后缀
    if skill_name.endswith('-skill'):
        errors.append(f"目录名不应包含 -skill 后缀: {skill_name}")

    # 检查是否以连字符开头或结尾
    if skill_name.startswith('-') or skill_name.endswith('-'):
        errors.append(f"目录名不应以连字符开头或结尾: {skill_name}")

    return len(errors) == 0, errors


def validate_structure(skill_dir: Path) -> Tuple[bool, List[str]]:
    """验证目录结构"""
    errors = []

    # 检查必需文件
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        errors.append("缺少必需文件: SKILL.md")
    else:
        errors.extend(validate_file_encoding(skill_md))

    # 检查可选目录
    optional_dirs = ['scripts', 'references', 'assets']
    for dir_name in optional_dirs:
        dir_path = skill_dir / dir_name
        if dir_path.exists() and not dir_path.is_dir():
            errors.append(f"{dir_name} 存在但不是目录")

    # 检查是否有空目录
    for dir_path in skill_dir.iterdir():
        if dir_path.is_dir() and dir_path.name not in optional_dirs + ['.', '..']:
            errors.append(f"存在非标准目录: {dir_path.name}")

        # 检查目录是否为空
        if dir_path.is_dir():
            if not any(dir_path.iterdir()):
                errors.append(f"存在空目录: {dir_path.name}")

    return len(errors) == 0, errors


def validate_file_encoding(file_path: Path) -> List[str]:
    """验证文件编码"""
    errors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
    except UnicodeDecodeError:
        errors.append(f"文件编码错误（应为 UTF-8）: {file_path.name}")
    except Exception as e:
        errors.append(f"文件读取错误: {file_path.name} - {e}")
    return errors


def validate_skill_md(skill_dir: Path) -> Tuple[bool, List[str]]:
    """验证 SKILL.md 格式"""
    errors = []

    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        return False, ["SKILL.md 不存在"]

    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查 YAML 前言区
        if not content.startswith('---'):
            errors.append("SKILL.md 缺少 YAML 前言区（应以 --- 开头）")
        else:
            # 提取前言区内容
            end_marker = content.find('\n---\n', 3)
            if end_marker == -1:
                errors.append("SKILL.md YAML 前言区未正确关闭（需要 --- 结束标记）")
            else:
                yaml_content = content[3:end_marker]
                try:
                    front_matter = yaml.safe_load(yaml_content)
                    errors.extend(validate_front_matter(front_matter))
                except yaml.YAMLError as e:
                    errors.append(f"YAML 前言区格式错误: {e}")

        # 检查正文长度
        body_content = content[end_marker + 5:] if end_marker > 0 else content
        body_lines = len(body_content.split('\n'))
        if body_lines > 500:
            errors.append(f"正文过长（{body_lines} 行），应不超过 500 行")

    except Exception as e:
        errors.append(f"读取 SKILL.md 失败: {e}")

    return len(errors) == 0, errors


def validate_front_matter(front_matter: Dict[str, Any]) -> List[str]:
    """验证前言区字段"""
    errors = []

    # 检查必需字段
    required_fields = ['name', 'description']
    for field in required_fields:
        if field not in front_matter:
            errors.append(f"前言区缺少必需字段: {field}")

    # 验证 name 字段
    if 'name' in front_matter:
        name = front_matter['name']
        if not isinstance(name, str):
            errors.append("name 字段必须是字符串")
        elif not re.match(r'^[a-z0-9-]+$', name):
            errors.append(f"name 字段格式错误: {name}")

    # 验证 description 字段
    if 'description' in front_matter:
        desc = front_matter['description']
        if not isinstance(desc, str):
            errors.append("description 字段必须是字符串")
        elif len(desc) < 100 or len(desc) > 150:
            errors.append(f"description 长度应为 100-150 字符（当前: {len(desc)}）")
        elif '\n' in desc:
            errors.append("description 应为单行文本（不应包含换行符）")

    return errors


def validate_scripts(skill_dir: Path) -> Tuple[bool, List[str]]:
    """验证脚本文件"""
    errors = []

    scripts_dir = skill_dir / 'scripts'
    if not scripts_dir.exists():
        return True, []  # 脚本目录可选

    for script_file in scripts_dir.glob('*.py'):
        errors.extend(validate_python_script(script_file))

    for script_file in scripts_dir.glob('*.sh'):
        errors.extend(validate_bash_script(script_file))

    return len(errors) == 0, errors


def validate_python_script(script_path: Path) -> List[str]:
    """验证 Python 脚本"""
    errors = []

    try:
        # 检查语法
        import py_compile
        py_compile.compile(str(script_path), doraise=True)
    except py_compile.PyCompileError as e:
        errors.append(f"Python 脚本语法错误: {script_path.name} - {e}")

    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否包含主函数
        if 'def main()' not in content:
            logger.warning(f"{script_path.name}: 建议定义 main() 函数")

        # 检查是否使用 argparse
        if 'import argparse' in content or 'from argparse import' in content:
            logger.debug(f"{script_path.name}: 使用 argparse 参数解析")

    except Exception as e:
        errors.append(f"读取 Python 脚本失败: {script_path.name} - {e}")

    return errors


def validate_bash_script(script_path: Path) -> List[str]:
    """验证 Bash 脚本"""
    errors = []

    try:
        # 检查是否有执行权限
        if not script_path.stat().st_mode & 0o111:
            errors.append(f"Bash 脚本缺少执行权限: {script_path.name}")

        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查 shebang
        if not content.startswith('#!'):
            errors.append(f"Bash 脚本缺少 shebang 行: {script_path.name}")

    except Exception as e:
        errors.append(f"读取 Bash 脚本失败: {script_path.name} - {e}")

    return errors


def validate_skill(skill_path: str) -> bool:
    """验证技能"""
    skill_dir = Path(skill_path)

    if not skill_dir.exists():
        logger.error(f"技能目录不存在: {skill_path}")
        return False

    logger.info(f"验证技能: {skill_dir.name}")
    logger.info("=" * 50)

    all_errors = []

    # 执行各项验证
    checks = [
        ("命名规范", lambda: validate_naming(skill_dir)),
        ("目录结构", lambda: validate_structure(skill_dir)),
        ("SKILL.md 格式", lambda: validate_skill_md(skill_dir)),
        ("脚本验证", lambda: validate_scripts(skill_dir)),
    ]

    for check_name, check_func in checks:
        passed, errors = check_func()
        status = "通过" if passed else "失败"
        logger.info(f"[{status}] {check_name}")

        if errors:
            all_errors.extend(errors)
            for error in errors:
                logger.error(f"  - {error}")

    # 总结
    logger.info("=" * 50)
    if all_errors:
        logger.error(f"验证失败: 发现 {len(all_errors)} 个问题")
        return False
    else:
        logger.info("验证通过: 技能符合规范")
        return True


def main():
    """主函数"""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    success = validate_skill(args.skill_path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
