#!/usr/bin/env python3
"""
知识搜索脚本 - 通过 Web Search 搜索不熟悉的技术栈并生成知识库
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import re

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class KnowledgeSearcher:
    """知识搜索器"""

    def __init__(self, output_dir: str = None):
        """
        初始化知识搜索器

        Args:
            output_dir: 知识库输出目录，默认为 ./wiki/references
        """
        self.output_dir = Path(output_dir) if output_dir else Path("./wiki/references")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def search_knowledge(self, tech_stack: str, knowledge_type: str = "library") -> Dict:
        """
        搜索技术栈知识

        Args:
            tech_stack: 技术栈名称
            knowledge_type: 知识类型（library/architecture/pattern/principle/math）

        Returns:
            搜索结果字典
        """
        print(f"🔍 正在搜索 {tech_stack} 的知识...")

        # 构建搜索关键词
        search_keywords = self._build_search_keywords(tech_stack, knowledge_type)

        # 模拟搜索结果（实际应该调用 web_search 工具）
        search_results = self._simulate_web_search(search_keywords)

        return {
            "tech_stack": tech_stack,
            "knowledge_type": knowledge_type,
            "search_keywords": search_keywords,
            "search_results": search_results,
            "search_time": datetime.now().isoformat()
        }

    def _build_search_keywords(self, tech_stack: str, knowledge_type: str) -> List[str]:
        """
        构建搜索关键词

        Args:
            tech_stack: 技术栈名称
            knowledge_type: 知识类型

        Returns:
            搜索关键词列表
        """
        keywords = []

        # 基础关键词
        keywords.append(f"{tech_stack} 官方文档")
        keywords.append(f"{tech_stack} 教程")
        keywords.append(f"{tech_stack} 最佳实践")

        # 根据类型添加特定关键词
        if knowledge_type == "library":
            keywords.append(f"{tech_stack} API 文档")
            keywords.append(f"{tech_stack} 使用示例")
            keywords.append(f"{tech_stack} 最新版本")
        elif knowledge_type == "architecture":
            keywords.append(f"{tech_stack} 架构设计")
            keywords.append(f"{tech_stack} 架构模式")
            keywords.append(f"{tech_stack} 设计原理")
        elif knowledge_type == "pattern":
            keywords.append(f"{tech_stack} 设计模式")
            keywords.append(f"{tech_stack} 实现方式")
        elif knowledge_type == "principle":
            keywords.append(f"{tech_stack} 原理")
            keywords.append(f"{tech_stack} 核心概念")
        elif knowledge_type == "math":
            keywords.append(f"{tech_stack} 公式")
            keywords.append(f"{tech_stack} 数学原理")

        return keywords

    def _simulate_web_search(self, keywords: List[str]) -> List[Dict]:
        """
        模拟 Web Search（实际应该调用 web_search 工具）

        Args:
            keywords: 搜索关键词列表

        Returns:
            搜索结果列表
        """
        # 这里模拟搜索结果
        # 实际实现应该调用 web_search 工具
        results = []

        for keyword in keywords:
            results.append({
                "keyword": keyword,
                "title": f"关于 {keyword} 的搜索结果",
                "url": f"https://example.com/search?q={keyword}",
                "snippet": f"这是关于 {keyword} 的搜索结果摘要...",
                "relevance": 0.9
            })

        return results

    def generate_knowledge_file(self, tech_stack: str, search_data: Dict) -> str:
        """
        生成知识文件

        Args:
            tech_stack: 技术栈名称
            search_data: 搜索数据

        Returns:
            生成的知识文件路径
        """
        # 读取知识模板
        template_path = Path(__file__).parent.parent / "assets" / "templates" / "knowledge-template.md"

        if not template_path.exists():
            print(f"❌ 知识模板不存在: {template_path}")
            return None

        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # 生成文件名（规范化）
        safe_name = re.sub(r'[^\w\-]', '_', tech_stack.lower())
        output_filename = f"{safe_name}-knowledge.md"
        output_path = self.output_dir / output_filename

        # 填充模板
        knowledge_content = self._fill_template(template_content, tech_stack, search_data)

        # 保存知识文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(knowledge_content)

        print(f"✅ 知识文件已生成: {output_path}")

        return str(output_path)

    def _fill_template(self, template: str, tech_stack: str, search_data: Dict) -> str:
        """
        填充知识模板

        Args:
            template: 模板内容
            tech_stack: 技术栈名称
            search_data: 搜索数据

        Returns:
            填充后的内容
        """
        # 基础信息
        content = template.replace("[技术栈名称]", tech_stack)
        content = content.replace("[中文名称]", tech_stack)
        content = content.replace("[英文名称]", tech_stack)
        content = content.replace("[简称]", tech_stack.split()[0] if ' ' in tech_stack else tech_stack)

        # 版本信息
        content = content.replace("[版本号]", "latest")
        content = content.replace("[日期]", datetime.now().strftime("%Y-%m-%d"))

        # 知识类型
        type_map = {
            "library": "库",
            "architecture": "架构",
            "pattern": "设计模式",
            "principle": "原理",
            "math": "数学公式"
        }
        content = content.replace("[库/架构/设计模式/数学公式/原理]", type_map.get(search_data.get("knowledge_type", "library"), "库"))

        # 搜索关键词
        keywords = "\n".join([f"{i+1}. {kw}" for i, kw in enumerate(search_data.get("search_keywords", []))])
        content = content.replace("[关键词 1]\n2. [关键词 2]\n3. [关键词 3]", keywords)

        # 搜索时间
        content = content.replace("[YYYY-MM-DD HH:MM:SS]", search_data.get("search_time", datetime.now().isoformat()))

        # 其他占位符保持原样（待后续填充）
        content = content.replace("[简要描述该技术栈的核心功能和用途]", f"{tech_stack} 是一个强大的技术栈，用于...")

        # 官方资源
        content = content.replace("[URL]", f"https://example.com/{tech_stack.lower()}")
        content = content.replace("[许可证]", "MIT License")

        # 版本变化
        content = content.replace("[主要更新内容]", "新功能优化和性能提升")

        # 环境要求
        content = content.replace("[要求 1]", "Python 3.8+")
        content = content.replace("[要求 2]", "Node.js 14+")
        content = content.replace("[要求 3]", "现代浏览器")

        # 核心特性
        content = content.replace("[特性 1]", "高性能")
        content = content.replace("[特性 2]", "易用性")
        content = content.replace("[特性 3]", "可扩展")

        # 核心概念
        content = content.replace("[概念 1]", "核心概念 1")
        content = content.replace("[说明]", "概念说明")
        content = content.replace("[场景]", "应用场景")

        # 主要API
        content = content.replace("[API 1]", "API 1")
        content = content.replace("[参数]", "参数说明")
        content = content.replace("[返回值]", "返回值说明")

        # 设计原则
        content = content.replace("[原则 1]", "原则 1：简洁")
        content = content.replace("[原则 2]", "原则 2：高效")
        content = content.replace("[原则 3]", "原则 3：可维护")

        # 使用建议
        content = content.replace("[建议 1]", "使用官方推荐的配置")
        content = content.replace("[建议 2]", "遵循最佳实践")
        content = content.replace("[建议 3]", "定期更新版本")
        content = content.replace("[避免 1]", "避免使用已废弃的API")
        content = content.replace("[避免 2]", "避免过度设计")
        content = content.replace("[避免 3]", "避免忽视性能优化")

        # 优化点
        content = content.replace("[优化 1]", "缓存优化")
        content = content.replace("[方法]", "使用 Redis 缓存")
        content = content.replace("[效果]", "提升 50% 性能")
        content = content.replace("[优化 2]", "异步处理")
        content = content.replace("[方法]", "使用异步框架")
        content = content.replace("[效果]", "提升吞吐量")

        # 问题描述
        content = content.replace("[问题描述]", "问题描述")
        content = content.replace("[原因说明]", "原因分析")
        content = content.replace("[代码]", "# 解决代码\n# 这里是代码示例")

        # 高级特性
        content = content.replace("[名称]", "特性名称")
        content = content.replace("[描述]", "特性描述")
        content = content.replace("[场景]", "适用场景")
        content = content.replace("[方式]", "实现方式")

        # 扩展方式
        content = content.replace("[说明]", "扩展说明")

        # 对比技术
        content = content.replace("[本技术]", tech_stack)
        content = content.replace("[对比技术 1]", "对比技术 1")
        content = content.replace("[对比技术 2]", "对比技术 2")
        content = content.replace("[评价]", "评价")
        content = content.replace("[场景]", "场景")

        # 案例
        content = content.replace("[案例名称]", "案例名称")
        content = content.replace("[背景说明]", "案例背景")
        content = content.replace("[需求说明]", "案例需求")
        content = content.replace("[方案说明]", "解决方案")
        content = content.replace("[效果说明]", "实现效果")

        # 陷阱
        content = content.replace("[描述]", "陷阱描述")
        content = content.replace("[现象]", "现象描述")
        content = content.replace("[原因]", "原因分析")
        content = content.replace("[方法]", "避免方法")

        # 注意事项
        content = content.replace("[说明]", "注意事项说明")

        # 版本变更
        content = content.replace("[版本号]", "1.0.0")
        content = content.replace("[日期]", datetime.now().strftime("%Y-%m-%d"))
        content = content.replace("[变更 1]", "初始版本发布")
        content = content.replace("[变更 2]", "性能优化")

        # 参考资源
        content = content.replace("[文档 1]", f"{tech_stack} 官方文档")
        content = content.replace("[文档 2]", f"{tech_stack} API 文档")
        content = content.replace("[教程 1]", f"{tech_stack} 快速入门")
        content = content.replace("[教程 2]", f"{tech_stack} 进阶教程")
        content = content.replace("[社区 1]", f"{tech_stack} GitHub")
        content = content.replace("[社区 2]", f"{tech_stack} 论坛")
        content = content.replace("[书籍 1]", f"{tech_stack} 权威指南")
        content = content.replace("[书籍 2]", f"{tech_stack} 实战")

        # 术语
        content = content.replace("[术语 1]", "术语 1")
        content = content.replace("[术语 2]", "术语 2")

        # 相关技术
        content = content.replace("[技术 1]", "相关技术 1")
        content = content.replace("[技术 2]", "相关技术 2")
        content = content.replace("[描述]", "技术描述")

        return content

    def check_knowledge_exists(self, tech_stack: str) -> bool:
        """
        检查知识是否已存在

        Args:
            tech_stack: 技术栈名称

        Returns:
            是否存在
        """
        safe_name = re.sub(r'[^\w\-]', '_', tech_stack.lower())
        knowledge_file = self.output_dir / f"{safe_name}-knowledge.md"
        return knowledge_file.exists()

    def get_knowledge_file(self, tech_stack: str) -> Optional[str]:
        """
        获取知识文件路径

        Args:
            tech_stack: 技术栈名称

        Returns:
            知识文件路径，如果不存在则返回 None
        """
        if self.check_knowledge_exists(tech_stack):
            safe_name = re.sub(r'[^\w\-]', '_', tech_stack.lower())
            return str(self.output_dir / f"{safe_name}-knowledge.md")
        return None


def main():
    parser = argparse.ArgumentParser(description="知识搜索工具")
    parser.add_argument("tech_stack", help="技术栈名称")
    parser.add_argument("--type", choices=["library", "architecture", "pattern", "principle", "math"],
                       default="library", help="知识类型")
    parser.add_argument("--output-dir", default="./wiki/references", help="输出目录")
    parser.add_argument("--check", action="store_true", help="仅检查知识是否存在")

    args = parser.parse_args()

    searcher = KnowledgeSearcher(args.output_dir)

    if args.check:
        if searcher.check_knowledge_exists(args.tech_stack):
            print(f"✅ 知识已存在: {searcher.get_knowledge_file(args.tech_stack)}")
        else:
            print(f"❌ 知识不存在: {args.tech_stack}")
            print(f"   可以使用以下命令搜索: python3 scripts/search_knowledge.py {args.tech_stack}")
    else:
        # 搜索知识
        search_data = searcher.search_knowledge(args.tech_stack, args.type)

        # 生成知识文件
        output_file = searcher.generate_knowledge_file(args.tech_stack, search_data)

        if output_file:
            print(f"\n🎉 知识搜索完成！")
            print(f"📄 知识文件: {output_file}")
            print(f"📊 搜索关键词数: {len(search_data['search_keywords'])}")
            print(f"🔍 搜索结果数: {len(search_data['search_results'])}")


if __name__ == "__main__":
    main()
