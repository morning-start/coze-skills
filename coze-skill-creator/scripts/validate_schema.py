#!/usr/bin/env python3
"""
技能配置 Schema 验证工具

功能:验证技能配置 JSON 文件是否符合预定义的 Schema
输出:验证结果（成功/失败）和详细的错误信息
"""

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError


def load_schema(schema_path: str) -> dict:
    """加载 JSON Schema 定义"""
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: Schema 文件不存在: {schema_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: Schema 文件格式错误: {e}")
        sys.exit(1)


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


def validate_config(config: dict, schema: dict) -> bool:
    """验证配置是否符合 Schema"""
    try:
        validate(instance=config, schema=schema)
        return True
    except ValidationError as e:
        print(f"验证失败:")
        print(f"  错误路径: {' -> '.join(str(p) for p in e.path)}")
        print(f"  错误信息: {e.message}")
        print(f"  Schema 路径: {' -> '.join(str(p) for p in e.schema_path)}")
        return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='验证技能配置 JSON 文件')
    parser.add_argument('--config', required=True, help='配置文件路径')
    parser.add_argument('--schema', help='Schema 文件路径（默认: assets/templates/schema.json）')
    
    args = parser.parse_args()
    
    # 确定默认 Schema 路径
    if args.schema:
        schema_path = args.schema
    else:
        # 假设在 skill-creator 目录下运行
        current_dir = Path(__file__).parent.parent
        schema_path = current_dir / 'assets' / 'templates' / 'schema.json'
    
    # 加载 Schema 和配置
    schema = load_schema(str(schema_path))
    config = load_config(args.config)
    
    # 执行验证
    if validate_config(config, schema):
        print("验证通过:配置文件符合 Schema 要求")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
