#!/usr/bin/env python3
"""
批量创建技能包
根据配置文件批量生成技能目录和基础文件
"""

import argparse
import json
import sys
import logging
from pathlib import Path
from typing import Dict, Any, List


# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='批量创建技能包',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='配置文件路径（JSON 格式）'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='/workspace/projects',
        help='输出目录（默认: /workspace/projects）'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='启用详细日志'
    )

    return parser.parse_args()


def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件"""
    config_file = Path(config_path)
    if not config_file.exists():
        logger.error(f"配置文件不存在: {config_path}")
        sys.exit(1)

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"成功加载配置文件: {config_path}")
        return config
    except json.JSONDecodeError as e:
        logger.error(f"配置文件格式错误: {e}")
        sys.exit(1)


def validate_config(config: Dict[str, Any]) -> bool:
    """验证配置文件格式"""
    if 'skills' not in config:
        logger.error("配置文件缺少 'skills' 字段")
        return False

    if not isinstance(config['skills'], list):
        logger.error("'skills' 字段必须是数组")
        return False

    for i, skill in enumerate(config['skills']):
        required_fields = ['name', 'type', 'description']
        for field in required_fields:
            if field not in skill:
                logger.error(f"技能 #{i} 缺少必需字段: {field}")
                return False

        # 验证技能名称格式
        skill_name = skill['name']
        if not skill_name.replace('-', '').isalnum() or '-' in skill_name.strip('-'):
            logger.error(f"技能名称格式错误: {skill_name}（应为小写字母+连字符）")
            return False

    logger.info("配置文件验证通过")
    return True


def create_skill_structure(skill_dir: Path) -> bool:
    """创建技能目录结构"""
    try:
        # 创建主目录
        skill_dir.mkdir(parents=True, exist_ok=True)

        # 创建可选目录
        (skill_dir / 'scripts').mkdir(exist_ok=True)
        (skill_dir / 'references').mkdir(exist_ok=True)
        (skill_dir / 'assets').mkdir(exist_ok=True)

        logger.debug(f"创建目录结构: {skill_dir}")
        return True
    except Exception as e:
        logger.error(f"创建目录结构失败: {e}")
        return False


def generate_skill_md(skill_dir: Path, skill: Dict[str, Any]) -> bool:
    """生成 SKILL.md 文件"""
    try:
        skill_md_content = f"""---
name: {skill['name']}
description: {skill['description']}
---

# {skill['name'].replace('-', ' ').title()}

## 任务目标
- 本 Skill 用于：{skill.get('purpose', '实现特定功能')}
- 能力包含：{skill.get('capabilities', '核心能力')}
- 触发条件：当用户需要 {skill.get('trigger', '使用此技能')}

## 操作步骤

### 标准流程
1. 准备输入数据
2. 执行处理逻辑
3. 输出结果

## 资源索引

### 必要脚本
- [scripts/main.py](scripts/main.py): 主处理脚本

## 注意事项
- 确保输入数据格式正确
- 处理失败时查看日志
"""

        skill_md_path = skill_dir / 'SKILL.md'
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(skill_md_content)

        logger.info(f"生成 SKILL.md: {skill_md_path}")
        return True
    except Exception as e:
        logger.error(f"生成 SKILL.md 失败: {e}")
        return False


def create_placeholder_script(skill_dir: Path) -> bool:
    """创建占位脚本"""
    try:
        script_path = skill_dir / 'scripts' / 'main.py'
        script_content = """#!/usr/bin/env python3
\"\"\"
技能处理脚本
\"\"\"

import argparse

def main():
    parser = argparse.ArgumentParser(description='技能处理脚本')
    parser.add_argument('--input', required=True, help='输入参数')
    args = parser.parse_args()

    print(f"处理输入: {args.input}")

if __name__ == '__main__':
    main()
"""
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)

        logger.debug(f"创建占位脚本: {script_path}")
        return True
    except Exception as e:
        logger.error(f"创建占位脚本失败: {e}")
        return False


def create_skill(output_dir: Path, skill: Dict[str, Any]) -> bool:
    """创建单个技能"""
    skill_name = skill['name']
    skill_dir = output_dir / skill_name

    logger.info(f"创建技能: {skill_name}")

    # 创建目录结构
    if not create_skill_structure(skill_dir):
        return False

    # 生成 SKILL.md
    if not generate_skill_md(skill_dir, skill):
        return False

    # 创建占位脚本
    if not create_placeholder_script(skill_dir):
        return False

    return True


def create_skills(config: Dict[str, Any], output_dir: Path) -> bool:
    """批量创建技能"""
    skills = config.get('skills', [])
    total = len(skills)
    success_count = 0

    logger.info(f"开始创建 {total} 个技能...")

    for i, skill in enumerate(skills, 1):
        logger.info(f"[{i}/{total}] 创建技能: {skill['name']}")

        if create_skill(output_dir, skill):
            success_count += 1
        else:
            logger.error(f"创建技能失败: {skill['name']}")

    logger.info(f"创建完成: 成功 {success_count}/{total}")
    return success_count == total


def main():
    """主函数"""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # 加载配置
    config = load_config(args.config)

    # 验证配置
    if not validate_config(config):
        sys.exit(1)

    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 批量创建技能
    success = create_skills(config, output_dir)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
