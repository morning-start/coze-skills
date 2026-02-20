#!/usr/bin/env python3
"""
知识管理器 - 管理渐进式知识搜索和缓存
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Set
from datetime import datetime
import re

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from search_knowledge import KnowledgeSearcher


class KnowledgeManager:
    """知识管理器"""

    def __init__(self, wiki_dir: str = "./wiki", references_dir: str = "./wiki/references"):
        """
        初始化知识管理器

        Args:
            wiki_dir: Wiki 目录
            references_dir: 知识库目录
        """
        self.wiki_dir = Path(wiki_dir)
        self.references_dir = Path(references_dir)
        self.references_dir.mkdir(parents=True, exist_ok=True)

        self.searcher = KnowledgeSearcher(str(self.references_dir))

        # 知识索引
        self.knowledge_index_file = self.references_dir / ".knowledge-index.json"
        self.knowledge_index = self._load_knowledge_index()

        # 缓存
        self.cache = {}

    def _load_knowledge_index(self) -> Dict:
        """加载知识索引"""
        if self.knowledge_index_file.exists():
            with open(self.knowledge_index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_knowledge_index(self):
        """保存知识索引"""
        with open(self.knowledge_index_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_index, f, indent=2, ensure_ascii=False)

    def register_knowledge(self, tech_stack: str, knowledge_type: str = "library", metadata: Dict = None):
        """
        注册知识

        Args:
            tech_stack: 技术栈名称
            knowledge_type: 知识类型
            metadata: 元数据
        """
        safe_name = re.sub(r'[^\w\-]', '_', tech_stack.lower())

        self.knowledge_index[safe_name] = {
            "tech_stack": tech_stack,
            "knowledge_type": knowledge_type,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        self._save_knowledge_index()

    def update_knowledge(self, tech_stack: str, metadata: Dict = None):
        """
        更新知识

        Args:
            tech_stack: 技术栈名称
            metadata: 元数据
        """
        safe_name = re.sub(r'[^\w\-]', '_', tech_stack.lower())

        if safe_name in self.knowledge_index:
            self.knowledge_index[safe_name]["metadata"].update(metadata or {})
            self.knowledge_index[safe_name]["updated_at"] = datetime.now().isoformat()
            self._save_knowledge_index()

    def get_knowledge_info(self, tech_stack: str) -> Optional[Dict]:
        """
        获取知识信息

        Args:
            tech_stack: 技术栈名称

        Returns:
            知识信息
        """
        safe_name = re.sub(r'[^\w\-]', '_', tech_stack.lower())
        return self.knowledge_index.get(safe_name)

    def list_knowledge(self, knowledge_type: str = None) -> List[Dict]:
        """
        列出所有知识

        Args:
            knowledge_type: 知识类型过滤器

        Returns:
            知识列表
        """
        knowledge_list = list(self.knowledge_index.values())

        if knowledge_type:
            knowledge_list = [k for k in knowledge_list if k["knowledge_type"] == knowledge_type]

        return knowledge_list

    def search_and_cache(self, tech_stack: str, knowledge_type: str = "library", force_refresh: bool = False) -> str:
        """
        搜索并缓存知识

        Args:
            tech_stack: 技术栈名称
            knowledge_type: 知识类型
            force_refresh: 是否强制刷新

        Returns:
            知识文件路径
        """
        # 检查缓存
        if not force_refresh and tech_stack in self.cache:
            return self.cache[tech_stack]

        # 检查知识是否存在
        if self.searcher.check_knowledge_exists(tech_stack) and not force_refresh:
            knowledge_file = self.searcher.get_knowledge_file(tech_stack)
            self.cache[tech_stack] = knowledge_file
            return knowledge_file

        # 搜索知识
        print(f"🔍 知识不存在，正在搜索: {tech_stack}")
        search_data = self.searcher.search_knowledge(tech_stack, knowledge_type)
        knowledge_file = self.searcher.generate_knowledge_file(tech_stack, search_data)

        # 注册知识
        self.register_knowledge(tech_stack, knowledge_type, {
            "search_keywords": search_data["search_keywords"],
            "search_results_count": len(search_data["search_results"])
        })

        # 缓存
        self.cache[tech_stack] = knowledge_file

        return knowledge_file

    def get_knowledge(self, tech_stack: str, auto_search: bool = True) -> Optional[str]:
        """
        获取知识

        Args:
            tech_stack: 技术栈名称
            auto_search: 是否自动搜索

        Returns:
            知识文件路径
        """
        # 检查缓存
        if tech_stack in self.cache:
            return self.cache[tech_stack]

        # 检查知识是否存在
        knowledge_file = self.searcher.get_knowledge_file(tech_stack)

        if knowledge_file:
            self.cache[tech_stack] = knowledge_file
            return knowledge_file

        # 自动搜索
        if auto_search:
            return self.search_and_cache(tech_stack)

        return None

    def extract_unknown_tech_stacks(self, text: str, known_stacks: Set[str] = None) -> List[str]:
        """
        从文本中提取未知的技术栈

        Args:
            text: 文本内容
            known_stacks: 已知技术栈集合

        Returns:
            未知技术栈列表
        """
        if known_stacks is None:
            known_stacks = set()

        # 常见技术栈关键词模式
        patterns = [
            r'\b[A-Z][a-zA-Z]+\.(js|py|java|go|rb|ts)\b',  # 文件扩展名
            r'\b[A-Z][a-zA-Z]+\b',  # 大写开头的词（可能是库名）
            r'\b[a-z]+-[a-z]+\b',  # 连字符连接的词（可能是库名）
        ]

        tech_stacks = set()

        for pattern in patterns:
            matches = re.findall(pattern, text)
            tech_stacks.update(matches)

        # 过滤已知技术栈
        unknown_stacks = [ts for ts in tech_stacks if ts not in known_stacks]

        return list(unknown_stacks)

    def batch_search(self, tech_stacks: List[str], knowledge_type: str = "library") -> Dict[str, str]:
        """
        批量搜索知识

        Args:
            tech_stacks: 技术栈列表
            knowledge_type: 知识类型

        Returns:
            技术栈到知识文件的映射
        """
        results = {}

        for tech_stack in tech_stacks:
            try:
                knowledge_file = self.search_and_cache(tech_stack, knowledge_type)
                results[tech_stack] = knowledge_file
            except Exception as e:
                print(f"❌ 搜索 {tech_stack} 失败: {e}")
                results[tech_stack] = None

        return results

    def get_statistics(self) -> Dict:
        """
        获取统计信息

        Returns:
            统计信息
        """
        knowledge_list = self.list_knowledge()

        type_counts = {}
        for k in knowledge_list:
            t = k["knowledge_type"]
            type_counts[t] = type_counts.get(t, 0) + 1

        return {
            "total_knowledge": len(knowledge_list),
            "type_distribution": type_counts,
            "cache_size": len(self.cache),
            "oldest_knowledge": min(k["created_at"] for k in knowledge_list) if knowledge_list else None,
            "newest_knowledge": max(k["updated_at"] for k in knowledge_list) if knowledge_list else None
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="知识管理器")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # 搜索命令
    search_parser = subparsers.add_parser("search", help="搜索知识")
    search_parser.add_argument("tech_stack", help="技术栈名称")
    search_parser.add_argument("--type", choices=["library", "architecture", "pattern", "principle", "math"],
                              default="library", help="知识类型")
    search_parser.add_argument("--force", action="store_true", help="强制刷新")

    # 列出命令
    list_parser = subparsers.add_parser("list", help="列出知识")
    list_parser.add_argument("--type", help="知识类型过滤")

    # 获取命令
    get_parser = subparsers.add_parser("get", help="获取知识")
    get_parser.add_argument("tech_stack", help="技术栈名称")
    get_parser.add_argument("--no-search", action="store_true", help="不自动搜索")

    # 统计命令
    subparsers.add_parser("stats", help="统计信息")

    args = parser.parse_args()

    manager = KnowledgeManager()

    if args.command == "search":
        knowledge_file = manager.search_and_cache(args.tech_stack, args.type, args.force)
        print(f"✅ 知识文件: {knowledge_file}")

    elif args.command == "list":
        knowledge_list = manager.list_knowledge(args.type)
        print(f"\n📚 知识库列表 ({len(knowledge_list)} 项):\n")
        for k in knowledge_list:
            print(f"  • {k['tech_stack']} ({k['knowledge_type']})")
            print(f"    创建时间: {k['created_at']}")
            if k.get('metadata'):
                print(f"    元数据: {k['metadata']}")
            print()

    elif args.command == "get":
        knowledge_file = manager.get_knowledge(args.tech_stack, not args.no_search)
        if knowledge_file:
            print(f"✅ 知识文件: {knowledge_file}")
        else:
            print(f"❌ 知识不存在: {args.tech_stack}")

    elif args.command == "stats":
        stats = manager.get_statistics()
        print(f"\n📊 知识库统计:\n")
        print(f"  总知识数: {stats['total_knowledge']}")
        print(f"  缓存大小: {stats['cache_size']}")
        print(f"  类型分布:")
        for t, count in stats['type_distribution'].items():
            print(f"    {t}: {count}")
        if stats['oldest_knowledge']:
            print(f"  最早知识: {stats['oldest_knowledge']}")
        if stats['newest_knowledge']:
            print(f"  最新知识: {stats['newest_knowledge']}")
        print()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
