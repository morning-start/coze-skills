#!/usr/bin/env python3
"""
通用 Python 脚本脚手架
适用于各类技术性任务，提供参数解析、日志记录、错误处理等基础设施
"""

import argparse
import logging
import sys
from typing import Any, Dict, Optional
from pathlib import Path


def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    设置日志记录

    Args:
        verbose: 是否启用详细日志

    Returns:
        配置好的 logger 实例
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """
    解析命令行参数

    Returns:
        解析后的参数对象
    """
    parser = argparse.ArgumentParser(
        description='脚本功能描述',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --input data.csv --output result.csv
  %(prog)s --input data.csv --output result.csv --verbose
        """
    )

    # 基础参数
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='输入文件路径'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='./output',
        help='输出目录路径（默认: ./output）'
    )

    parser.add_argument(
        '--config',
        type=str,
        help='配置文件路径（JSON/YAML）'
    )

    # 选项参数
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='启用详细日志输出'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='模拟运行，不实际执行'
    )

    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> bool:
    """
    验证参数有效性

    Args:
        args: 解析后的参数对象

    Returns:
        验证是否通过
    """
    # 检查输入文件是否存在
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        return False

    # 检查输出目录是否可创建
    output_path = Path(args.output)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"错误: 无法创建输出目录: {e}", file=sys.stderr)
        return False

    # 检查配置文件是否存在（如果指定）
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"错误: 配置文件不存在: {args.config}", file=sys.stderr)
            return False

    return True


def load_config(config_path: Optional[str]) -> Dict[str, Any]:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径

    Returns:
        配置字典
    """
    if not config_path:
        return {}

    import json
    import yaml

    config_file = Path(config_path)
    suffix = config_file.suffix.lower()

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            if suffix == '.json':
                return json.load(f)
            elif suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {suffix}")
    except Exception as e:
        print(f"错误: 加载配置文件失败: {e}", file=sys.stderr)
        sys.exit(1)


def process(args: argparse.Namespace, config: Dict[str, Any], logger: logging.Logger) -> bool:
    """
    执行主要处理逻辑

    Args:
        args: 命令行参数
        config: 配置字典
        logger: 日志记录器

    Returns:
        处理是否成功
    """
    try:
        logger.info(f"开始处理: {args.input}")
        logger.debug(f"配置参数: {config}")

        # TODO: 在此处实现具体的处理逻辑
        # 示例：读取输入文件
        logger.info("读取输入文件...")
        input_path = Path(args.input)
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.debug(f"读取到 {len(content)} 字符")

        # TODO: 执行数据处理或业务逻辑
        logger.info("执行处理逻辑...")

        # TODO: 写入输出文件
        if not args.dry_run:
            output_path = Path(args.output) / f"{input_path.stem}_processed{input_path.suffix}"
            logger.info(f"写入输出文件: {output_path}")
            # with open(output_path, 'w', encoding='utf-8') as f:
            #     f.write(processed_content)

        logger.info("处理完成")
        return True

    except Exception as e:
        logger.error(f"处理失败: {e}", exc_info=True)
        return False


def main():
    """
    主函数
    """
    # 解析参数
    args = parse_args()

    # 设置日志
    logger = setup_logging(args.verbose)

    # 验证参数
    if not validate_args(args):
        sys.exit(1)

    # 加载配置
    config = load_config(args.config)

    # 执行处理
    success = process(args, config, logger)

    # 退出
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
