#!/usr/bin/env python3
"""
模板管理器
管理模板版本、分类、评分和检索
"""

import argparse
import json
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TemplateMetadata:
    """模板元数据"""
    name: str
    technology: str
    category: str
    version: str
    description: str
    quality_score: float
    created_at: str
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)
    complexity: str = "medium"  # beginner, intermediate, advanced


class TemplateManager:
    """模板管理器"""

    def __init__(self, template_dir: str):
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.template_dir / "template-index.json"
        self.versions_dir = self.template_dir / ".versions"
        self.versions_dir.mkdir(exist_ok=True)
        self.index = self._load_index()

    def _load_index(self) -> Dict[str, Any]:
        """加载模板索引"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载索引失败: {e}")

        return {
            "templates": [],
            "categories": {},
            "technologies": {},
            "statistics": {
                "total_templates": 0,
                "total_versions": 0
            },
            "last_updated": datetime.now().isoformat()
        }

    def _save_index(self):
        """保存模板索引"""
        self.index["last_updated"] = datetime.now().isoformat()
        self.index["statistics"]["total_templates"] = len(self.index["templates"])
        self.index["statistics"]["total_versions"] = sum(
            len(t.get("versions", [])) for t in self.index["templates"]
        )

        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def add_template(
        self,
        name: str,
        technology: str,
        category: str,
        code: str,
        config: str = "",
        documentation: str = "",
        version: str = "1.0.0",
        tags: List[str] = None,
        complexity: str = "medium"
    ) -> bool:
        """添加新模板"""
        try:
            template_id = f"{technology}/{category}/{name}"

            # 检查是否已存在
            existing = next(
                (t for t in self.index["templates"] if t["id"] == template_id),
                None
            )

            if existing:
                logger.warning(f"模板已存在: {template_id}")
                return False

            # 创建模板文件
            template_path = self.template_dir / technology / category
            template_path.mkdir(parents=True, exist_ok=True)

            template_file = template_path / f"{name}.json"

            template_data = {
                "id": template_id,
                "name": name,
                "technology": technology,
                "category": category,
                "version": version,
                "description": documentation.split('\n\n')[0] if documentation else "",
                "code": code,
                "config": config,
                "documentation": documentation,
                "tags": tags or [],
                "complexity": complexity,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "quality_score": self._calculate_quality_score(code, documentation)
            }

            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)

            # 更新索引
            template_entry = {
                "id": template_id,
                "name": name,
                "technology": technology,
                "category": category,
                "version": version,
                "quality_score": template_data["quality_score"],
                "complexity": complexity,
                "tags": tags or [],
                "path": str(template_file.relative_to(self.template_dir)),
                "created_at": template_data["created_at"],
                "versions": [version]
            }

            self.index["templates"].append(template_entry)

            # 更新分类索引
            if technology not in self.index["technologies"]:
                self.index["technologies"][technology] = []
            if category not in self.index["technologies"][technology]:
                self.index["technologies"][technology].append(category)

            self._save_index()

            logger.info(f"模板已添加: {template_id}")
            return True

        except Exception as e:
            logger.error(f"添加模板失败: {e}")
            return False

    def update_template(
        self,
        template_id: str,
        new_version: str = None,
        code: str = None,
        config: str = None,
        documentation: str = None,
        tags: List[str] = None
    ) -> bool:
        """更新模板"""
        try:
            template_entry = next(
                (t for t in self.index["templates"] if t["id"] == template_id),
                None
            )

            if not template_entry:
                logger.error(f"模板不存在: {template_id}")
                return False

            # 读取当前模板
            template_path = self.template_dir / template_entry["path"]
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)

            # 备份当前版本
            current_version = template_data["version"]
            backup_path = self.versions_dir / f"{template_id.replace('/', '_')}_{current_version}.json"
            shutil.copy2(template_path, backup_path)

            # 更新模板
            if code:
                template_data["code"] = code
            if config:
                template_data["config"] = config
            if documentation:
                template_data["documentation"] = documentation
            if tags:
                template_data["tags"] = tags
            if new_version:
                template_data["version"] = new_version

            template_data["updated_at"] = datetime.now().isoformat()
            template_data["quality_score"] = self._calculate_quality_score(
                template_data["code"],
                template_data["documentation"]
            )

            # 保存更新后的模板
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)

            # 更新索引
            template_entry["version"] = template_data["version"]
            template_entry["quality_score"] = template_data["quality_score"]
            template_entry["updated_at"] = template_data["updated_at"]

            if new_version and new_version not in template_entry["versions"]:
                template_entry["versions"].append(new_version)

            self._save_index()

            logger.info(f"模板已更新: {template_id} -> {new_version or current_version}")
            return True

        except Exception as e:
            logger.error(f"更新模板失败: {e}")
            return False

    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """获取模板详情"""
        template_entry = next(
            (t for t in self.index["templates"] if t["id"] == template_id),
            None
        )

        if not template_entry:
            return None

        template_path = self.template_dir / template_entry["path"]
        with open(template_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_templates(
        self,
        technology: str = None,
        category: str = None,
        min_score: float = 0.0,
        complexity: str = None,
        tags: List[str] = None
    ) -> List[Dict[str, Any]]:
        """列出模板"""
        templates = self.index["templates"].copy()

        # 过滤
        if technology:
            templates = [t for t in templates if t["technology"] == technology]
        if category:
            templates = [t for t in templates if t["category"] == category]
        if complexity:
            templates = [t for t in templates if t["complexity"] == complexity]
        if min_score > 0:
            templates = [t for t in templates if t["quality_score"] >= min_score]
        if tags:
            templates = [
                t for t in templates
                if any(tag in t.get("tags", []) for tag in tags)
            ]

        # 按评分排序
        return sorted(templates, key=lambda x: x["quality_score"], reverse=True)

    def search_templates(self, query: str) -> List[Dict[str, Any]]:
        """搜索模板"""
        query_lower = query.lower()
        results = []

        for template in self.index["templates"]:
            score = 0.0

            # 名称匹配
            if query_lower in template["name"].lower():
                score += 0.5

            # 技术匹配
            if query_lower in template["technology"].lower():
                score += 0.3

            # 分类匹配
            if query_lower in template["category"].lower():
                score += 0.2

            # 标签匹配
            for tag in template.get("tags", []):
                if query_lower in tag.lower():
                    score += 0.2

            if score > 0:
                results.append({
                    **template,
                    "search_score": score
                })

        return sorted(results, key=lambda x: x["search_score"], reverse=True)

    def delete_template(self, template_id: str) -> bool:
        """删除模板"""
        try:
            template_entry = next(
                (t for t in self.index["templates"] if t["id"] == template_id),
                None
            )

            if not template_entry:
                logger.error(f"模板不存在: {template_id}")
                return False

            # 删除模板文件
            template_path = self.template_dir / template_entry["path"]
            template_path.unlink()

            # 从索引中移除
            self.index["templates"].remove(template_entry)
            self._save_index()

            logger.info(f"模板已删除: {template_id}")
            return True

        except Exception as e:
            logger.error(f"删除模板失败: {e}")
            return False

    def _calculate_quality_score(self, code: str, documentation: str) -> float:
        """计算模板质量评分"""
        score = 0.0

        # 代码质量（40分）
        if code:
            score += 0.3
            if len(code) > 100:
                score += 0.1
            if 'def ' in code or 'function' in code or 'class ' in code:
                score += 0.1
            if 'try:' in code or 'except' in code:
                score += 0.1

        # 文档质量（30分）
        if documentation:
            score += 0.2
            if len(documentation) > 50:
                score += 0.1
            if '##' in documentation:
                score += 0.1

        return min(score, 1.0)

    def export_template(self, template_id: str, output_dir: str) -> bool:
        """导出模板"""
        try:
            template = self.get_template(template_id)
            if not template:
                return False

            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # 导出为多个文件
            with open(output_path / "code.py", 'w', encoding='utf-8') as f:
                f.write(template["code"])

            if template["config"]:
                with open(output_path / "config.json", 'w', encoding='utf-8') as f:
                    f.write(template["config"])

            if template["documentation"]:
                with open(output_path / "README.md", 'w', encoding='utf-8') as f:
                    f.write(template["documentation"])

            with open(output_path / "template.json", 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2, ensure_ascii=False)

            logger.info(f"模板已导出到: {output_path}")
            return True

        except Exception as e:
            logger.error(f"导出模板失败: {e}")
            return False


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='模板管理器',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='action', help='操作类型')

    # 添加模板
    add_parser = subparsers.add_parser('add', help='添加模板')
    add_parser.add_argument('--name', required=True, help='模板名称')
    add_parser.add_argument('--tech', required=True, help='技术名称')
    add_parser.add_argument('--category', required=True, help='分类')
    add_parser.add_argument('--code', required=True, help='代码内容')
    add_parser.add_argument('--config', help='配置内容')
    add_parser.add_argument('--doc', help='文档内容')
    add_parser.add_argument('--version', default='1.0.0', help='版本号')
    add_parser.add_argument('--tags', nargs='+', help='标签')
    add_parser.add_argument('--complexity', default='medium', choices=['beginner', 'intermediate', 'advanced'])

    # 更新模板
    update_parser = subparsers.add_parser('update', help='更新模板')
    update_parser.add_argument('--id', required=True, help='模板ID')
    update_parser.add_argument('--version', help='新版本号')
    update_parser.add_argument('--code', help='代码内容')
    update_parser.add_argument('--config', help='配置内容')
    update_parser.add_argument('--doc', help='文档内容')
    update_parser.add_argument('--tags', nargs='+', help='标签')

    # 列出模板
    list_parser = subparsers.add_parser('list', help='列出模板')
    list_parser.add_argument('--tech', help='技术名称')
    list_parser.add_argument('--category', help='分类')
    list_parser.add_argument('--min-score', type=float, default=0.0, help='最小评分')
    list_parser.add_argument('--complexity', help='复杂度')
    list_parser.add_argument('--tags', nargs='+', help='标签')

    # 搜索模板
    search_parser = subparsers.add_parser('search', help='搜索模板')
    search_parser.add_argument('--query', required=True, help='搜索查询')

    # 删除模板
    delete_parser = subparsers.add_parser('delete', help='删除模板')
    delete_parser.add_argument('--id', required=True, help='模板ID')

    # 导出模板
    export_parser = subparsers.add_parser('export', help='导出模板')
    export_parser.add_argument('--id', required=True, help='模板ID')
    export_parser.add_argument('--output', required=True, help='输出目录')

    # 获取模板
    get_parser = subparsers.add_parser('get', help='获取模板详情')
    get_parser.add_argument('--id', required=True, help='模板ID')

    parser.add_argument(
        '--template-dir',
        type=str,
        default='./assets/template-library',
        help='模板库目录'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='启用详细日志'
    )

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.action:
        print("请指定操作类型: add, update, list, search, delete, export, get")
        return

    manager = TemplateManager(args.template_dir)

    if args.action == 'add':
        success = manager.add_template(
            name=args.name,
            technology=args.tech,
            category=args.category,
            code=args.code,
            config=args.config or "",
            documentation=args.doc or "",
            version=args.version,
            tags=args.tags,
            complexity=args.complexity
        )
        print("添加成功" if success else "添加失败")

    elif args.action == 'update':
        success = manager.update_template(
            template_id=args.id,
            new_version=args.version,
            code=args.code,
            config=args.config,
            documentation=args.doc,
            tags=args.tags
        )
        print("更新成功" if success else "更新失败")

    elif args.action == 'list':
        templates = manager.list_templates(
            technology=args.tech,
            category=args.category,
            min_score=args.min_score,
            complexity=args.complexity,
            tags=args.tags
        )

        print("\n" + "=" * 80)
        print("模板列表")
        print("=" * 80)

        if not templates:
            print("没有找到模板")
        else:
            for i, t in enumerate(templates, 1):
                print(f"\n{i}. {t['name']}")
                print(f"   ID: {t['id']}")
                print(f"   技术: {t['technology']}")
                print(f"   分类: {t['category']}")
                print(f"   版本: {t['version']}")
                print(f"   评分: {t['quality_score']:.2f}")
                print(f"   复杂度: {t['complexity']}")
                if t.get('tags'):
                    print(f"   标签: {', '.join(t['tags'])}")

        print("\n" + "=" * 80)

    elif args.action == 'search':
        templates = manager.search_templates(args.query)

        print("\n" + "=" * 80)
        print(f"搜索结果: '{args.query}'")
        print("=" * 80)

        if not templates:
            print("没有找到匹配的模板")
        else:
            for i, t in enumerate(templates, 1):
                print(f"\n{i}. {t['name']} (评分: {t['quality_score']:.2f}, 匹配度: {t['search_score']:.2f})")
                print(f"   {t['id']}")

        print("\n" + "=" * 80)

    elif args.action == 'delete':
        success = manager.delete_template(args.id)
        print("删除成功" if success else "删除失败")

    elif args.action == 'export':
        success = manager.export_template(args.id, args.output)
        print("导出成功" if success else "导出失败")

    elif args.action == 'get':
        template = manager.get_template(args.id)
        if template:
            print(json.dumps(template, indent=2, ensure_ascii=False))
        else:
            print("模板不存在")


if __name__ == '__main__':
    main()
