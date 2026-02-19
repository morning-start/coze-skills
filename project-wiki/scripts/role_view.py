#!/usr/bin/env python3
"""
角色视图查询脚本

支持按角色查询相关文档、列出所有角色、生成角色专属文档
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 角色定义
ROLES = {
    "architect": {
        "name": "架构师 / 技术负责人",
        "name_en": "Architect",
        "focus": ["整体架构合理性", "技术选型依据", "可扩展性/容灾能力", "跨团队依赖"],
        "docs": ["architecture-guide.md", "adr-template.md", "architecture-template.md"],
        "directory": "architect",
        "template_types": {
            "architecture": "架构设计文档",
            "adr": "ADR"
        }
    },
    "developer": {
        "name": "开发工程师（实现者）",
        "name_en": "Developer",
        "focus": ["模块接口定义", "数据结构", "状态流转", "错误处理规则", "本地调试方式"],
        "docs": ["developer-guide.md", "module-design-template.md"],
        "directory": "developer",
        "template_types": {
            "module": "模块设计文档",
            "api": "API 文档"
        }
    },
    "tester": {
        "name": "测试工程师",
        "name_en": "Tester",
        "focus": ["边界条件", "异常场景", "数据一致性规则", "可观测性埋点"],
        "docs": ["tester-guide.md", "test-plan-template.md"],
        "directory": "tester",
        "template_types": {
            "test-plan": "测试计划"
        }
    },
    "ops": {
        "name": "运维 / SRE",
        "name_en": "Ops / SRE",
        "focus": ["部署拓扑", "资源需求", "扩缩容策略", "监控告警指标"],
        "docs": ["ops-guide.md", "ops-runbook-template.md"],
        "directory": "ops",
        "template_types": {
            "ops-runbook": "运维手册"
        }
    },
    "product": {
        "name": "产品经理 / 业务方",
        "name_en": "Product Manager",
        "focus": ["功能是否覆盖需求", "用户路径是否合理", "是否有体验风险"],
        "docs": ["product-guide.md", "user-flow-template.md"],
        "directory": "product",
        "template_types": {
            "user-flow": "用户旅程图"
        }
    }
}


def list_roles() -> None:
    """列出所有角色"""
    print("\n" + "=" * 80)
    print("角色列表")
    print("=" * 80)
    
    for role_key, role_info in ROLES.items():
        print(f"\n【{role_info['name']}】")
        print(f"  英文名: {role_info['name_en']}")
        print(f"  关注重点:")
        for focus in role_info['focus']:
            print(f"    - {focus}")
        print(f"  相关文档:")
        for doc in role_info['docs']:
            print(f"    - {doc}")
    
    print("\n" + "=" * 80)


def show_role_documents(role_key: str) -> None:
    """显示特定角色的文档"""
    if role_key not in ROLES:
        print(f"错误: 角色 '{role_key}' 不存在")
        print(f"可用角色: {', '.join(ROLES.keys())}")
        sys.exit(1)
    
    role = ROLES[role_key]
    role_dir = PROJECT_ROOT / "references" / "roles" / role["directory"]
    
    print(f"\n【{role['name']}】相关文档")
    print("=" * 80)
    
    # 列出目录中的所有文档
    if role_dir.exists():
        for doc_file in sorted(role_dir.glob("*.md")):
            print(f"\n📄 {doc_file.name}")
            print(f"   路径: {doc_file.relative_to(PROJECT_ROOT)}")
            
            # 读取文档的前几行作为摘要
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines[:10]:
                        if line.strip() and not line.startswith('#'):
                            print(f"   {line.strip()}")
                            break
            except Exception as e:
                print(f"   无法读取文档: {e}")
    else:
        print(f"\n警告: 目录不存在 {role_dir}")
    
    print("\n" + "=" * 80)


def generate_role_document(role_key: str, doc_type: str, name: str = None, output: str = None) -> None:
    """生成角色专属文档"""
    if role_key not in ROLES:
        print(f"错误: 角色 '{role_key}' 不存在")
        print(f"可用角色: {', '.join(ROLES.keys())}")
        sys.exit(1)
    
    role = ROLES[role_key]
    
    if doc_type not in role["template_types"]:
        print(f"错误: 角色 '{role_key}' 不支持文档类型 '{doc_type}'")
        print(f"支持的类型: {', '.join(role['template_types'].keys())}")
        sys.exit(1)
    
    # 确定模板文件
    template_name = f"{doc_type}-template.md" if doc_type else "template.md"
    
    # 查找模板文件
    if doc_type == "api":
        template_path = PROJECT_ROOT / "references" / "templates" / "api-template.md"
    elif doc_type == "design-doc":
        template_path = PROJECT_ROOT / "references" / "templates" / "design-doc-template.md"
    else:
        template_path = PROJECT_ROOT / "references" / "roles" / role["directory"] / template_name
    
    if not template_path.exists():
        print(f"错误: 模板文件不存在 {template_path}")
        sys.exit(1)
    
    # 读取模板
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # 替换占位符
    if name:
        template_content = template_content.replace("<功能名称>", name)
        template_content = template_content.replace("<系统名称>", name)
        template_content = template_content.replace("<模块名称>", name)
    
    # 确定输出路径
    if output:
        output_path = Path(output)
    else:
        output_dir = PROJECT_ROOT / "wiki"
        if doc_type == "architecture":
            output_dir = output_dir / "01-架构文档"
        elif doc_type == "adr":
            output_dir = output_dir / "01-架构文档" / "adr"
        elif doc_type == "module":
            output_dir = output_dir / "04-模块文档"
            if name:
                output_dir = output_dir / name
        elif doc_type == "api":
            output_dir = output_dir / "03-API文档"
        elif doc_type == "test-plan":
            output_dir = output_dir / "05-测试文档"
        elif doc_type == "ops-runbook":
            output_dir = output_dir / "06-参考文档"
        elif doc_type == "user-flow":
            output_dir = output_dir / "02-开发指南"
        
        output_path = output_dir / f"{name or '文档'}.md"
    
    # 创建输出目录
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"\n✅ 文档生成成功!")
    print(f"   角色: {role['name']}")
    print(f"   类型: {role['template_types'][doc_type]}")
    print(f"   路径: {output_path.relative_to(PROJECT_ROOT)}")


def show_mapping() -> None:
    """显示角色与文档的映射关系"""
    mapping_path = PROJECT_ROOT / "references" / "roles" / "role-mapping.md"
    
    if mapping_path.exists():
        with open(mapping_path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print(f"错误: 映射文件不存在 {mapping_path}")


def main():
    parser = argparse.ArgumentParser(description="角色视图查询脚本")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 列出所有角色
    list_parser = subparsers.add_parser("list-roles", help="列出所有角色")
    
    # 查看角色文档
    docs_parser = subparsers.add_parser("docs", help="查看角色的相关文档")
    docs_parser.add_argument("--role", required=True, choices=ROLES.keys(), help="角色名称")
    
    # 生成文档
    generate_parser = subparsers.add_parser("generate", help="生成角色专属文档")
    generate_parser.add_argument("--role", required=True, choices=ROLES.keys(), help="角色名称")
    generate_parser.add_argument("--type", required=True, help="文档类型")
    generate_parser.add_argument("--name", help="文档名称")
    generate_parser.add_argument("--output", help="输出路径")
    
    # 查看映射
    mapping_parser = subparsers.add_parser("mapping", help="查看角色与文档的映射关系")
    
    args = parser.parse_args()
    
    if args.command == "list-roles":
        list_roles()
    elif args.command == "docs":
        show_role_documents(args.role)
    elif args.command == "generate":
        generate_role_document(args.role, args.type, args.name, args.output)
    elif args.command == "mapping":
        show_mapping()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
