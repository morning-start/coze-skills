#!/usr/bin/env python3
"""
网络搜索与经验总结器
搜索行业最佳实践，提取优秀方案，生成可复用模板
"""

import argparse
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import quote_plus


# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """搜索结果"""
    url: str
    title: str
    snippet: str
    source: str = ""
    quality_score: float = 0.0


@dataclass
class SolutionPattern:
    """解决方案模式"""
    name: str
    description: str
    code_example: str
    config_template: str = ""
    best_practices: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    quality_score: float = 0.0


@dataclass
class Template:
    """可复用模板"""
    name: str
    technology: str
    category: str
    description: str
    code: str
    config: str = ""
    documentation: str = ""
    examples: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    quality_score: float = 0.0


class WebSearcher:
    """网络搜索器"""

    def __init__(self):
        self.results = []

    def search(
        self,
        query: str,
        tech: str = None,
        max_results: int = 20
    ) -> List[SearchResult]:
        """
        执行网络搜索

        注意：此脚本需要智能体提供网络搜索能力
        在实际使用中，智能体会调用 web_search 工具
        """
        logger.info(f"搜索查询: {query}")

        # 构建多维搜索关键词
        keywords = self._build_keywords(query, tech)

        # 这里应该调用 web_search 工具
        # 由于此脚本在沙箱环境，我们返回模拟结果
        # 实际使用时，智能体会调用真实的搜索 API

        simulated_results = self._simulate_search(keywords, max_results)

        # 评分和排序
        scored_results = self._score_results(simulated_results)

        # 去重
        unique_results = self._deduplicate(scored_results)

        return unique_results[:max_results]

    def _build_keywords(self, query: str, tech: str = None) -> List[str]:
        """构建搜索关键词"""
        keywords = []

        if tech:
            keywords.extend([
                f"{tech} {query}",
                f"{tech} best practices",
                f"{tech} production ready",
                f"{tech} implementation patterns",
                f"{tech} examples",
                f"{tech} tutorial"
            ])
        else:
            keywords.extend([
                f"{query} best practices",
                f"{query} implementation",
                f"{query} patterns",
                f"{query} examples"
            ])

        return keywords

    def _simulate_search(self, keywords: List[str], max_results: int) -> List[SearchResult]:
        """模拟搜索结果（实际使用时替换为真实搜索）"""
        logger.warning("使用模拟搜索结果，实际使用时需要集成 web_search 工具")

        results = []
        for keyword in keywords[:3]:  # 限制模拟结果
            results.append(SearchResult(
                url=f"https://example.com/{quote_plus(keyword)}",
                title=f"{keyword.title()} - 最佳实践",
                snippet=f"关于 {keyword} 的详细说明和代码示例...",
                source="example.com",
                quality_score=0.8
            ))

        return results

    def _score_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """对搜索结果评分"""
        for result in results:
            score = 0.0

            # 来源权威性
            权威域名 = ['github.com', 'stackoverflow.com', 'official-docs.com', 'dev.to']
            for domain in 权威域名:
                if domain in result.url:
                    score += 0.3
                    break

            # 标题相关性
            if 'best practices' in result.title.lower():
                score += 0.2
            if 'tutorial' in result.title.lower():
                score += 0.1

            # 内容长度
            if len(result.snippet) > 100:
                score += 0.1

            result.quality_score = min(score, 1.0)

        return sorted(results, key=lambda x: x.quality_score, reverse=True)

    def _deduplicate(self, results: List[SearchResult]) -> List[SearchResult]:
        """去重"""
        seen_urls = set()
        unique_results = []

        for result in results:
            if result.url not in seen_urls:
                seen_urls.add(result.url)
                unique_results.append(result)

        return unique_results


class SolutionExtractor:
    """解决方案提取器"""

    def extract_solutions(
        self,
        results: List[SearchResult],
        tech: str
    ) -> List[SolutionPattern]:
        """从搜索结果中提取解决方案"""
        logger.info(f"从 {len(results)} 个搜索结果中提取解决方案")

        solutions = []

        for result in results:
            # 这里应该实际访问 URL 提取内容
            # 由于沙箱限制，我们使用模拟提取
            solution = self._extract_from_result(result, tech)
            if solution:
                solutions.append(solution)

        return solutions

    def _extract_from_result(
        self,
        result: SearchResult,
        tech: str
    ) -> Optional[SolutionPattern]:
        """从单个结果提取解决方案"""
        # 模拟提取
        return SolutionPattern(
            name=f"{tech} 最佳实践",
            description=result.snippet,
            code_example=f"# {tech} 示例代码\n# 来源: {result.url}\n# TODO: 实际提取代码",
            best_practices=[
                "使用异步处理提高性能",
                "添加错误处理和重试机制",
                "实现日志记录和监控"
            ],
            tags=[tech, "best-practices"],
            quality_score=result.quality_score
        )


class TemplateGenerator:
    """模板生成器"""

    def generate_template(
        self,
        solutions: List[SolutionPattern],
        tech: str,
        category: str
    ) -> Template:
        """从解决方案生成模板"""
        logger.info(f"从 {len(solutions)} 个解决方案生成模板")

        # 选择最佳方案
        best_solution = max(solutions, key=lambda x: x.quality_score)

        # 生成模板
        template = Template(
            name=f"{tech}-{category}-template",
            technology=tech,
            category=category,
            description=f"{tech} {category} 的最佳实践模板",
            code=best_solution.code_example,
            config=best_solution.config_template,
            documentation=self._generate_documentation(best_solution),
            examples=[sol.code_example for sol in solutions[:3]],
            quality_score=best_solution.quality_score
        )

        return template

    def _generate_documentation(self, solution: SolutionPattern) -> str:
        """生成文档"""
        doc = [f"# {solution.name}\n\n"]
        doc.append(f"## 描述\n\n{solution.description}\n\n")

        if solution.best_practices:
            doc.append("## 最佳实践\n\n")
            for practice in solution.best_practices:
                doc.append(f"- {practice}\n")
            doc.append("\n")

        if solution.tags:
            doc.append(f"## 标签\n\n{', '.join(solution.tags)}\n")

        return ''.join(doc)


class TemplateManager:
    """模板管理器"""

    def __init__(self, template_dir: str):
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.template_dir / "template-index.json"
        self.index = self._load_index()

    def _load_index(self) -> Dict[str, Any]:
        """加载模板索引"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"templates": [], "last_updated": datetime.now().isoformat()}

    def _save_index(self):
        """保存模板索引"""
        self.index["last_updated"] = datetime.now().isoformat()
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def save_template(self, template: Template) -> bool:
        """保存模板"""
        try:
            # 创建模板目录
            template_path = self.template_dir / template.technology / template.category
            template_path.mkdir(parents=True, exist_ok=True)

            # 保存模板文件
            template_file = template_path / f"{template.name}.json"

            template_data = {
                "name": template.name,
                "technology": template.technology,
                "category": template.category,
                "description": template.description,
                "code": template.code,
                "config": template.config,
                "documentation": template.documentation,
                "examples": template.examples,
                "version": template.version,
                "created_at": template.created_at,
                "quality_score": template.quality_score
            }

            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)

            # 更新索引
            template_entry = {
                "name": template.name,
                "technology": template.technology,
                "category": template.category,
                "quality_score": template.quality_score,
                "version": template.version,
                "path": str(template_file.relative_to(self.template_dir))
            }

            # 检查是否已存在
            existing = next(
                (t for t in self.index["templates"] if t["name"] == template.name),
                None
            )

            if existing:
                existing.update(template_entry)
            else:
                self.index["templates"].append(template_entry)

            self._save_index()

            logger.info(f"模板已保存: {template_file}")
            return True

        except Exception as e:
            logger.error(f"保存模板失败: {e}")
            return False

    def list_templates(
        self,
        tech: str = None,
        category: str = None,
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """列出模板"""
        templates = self.index["templates"]

        # 过滤
        if tech:
            templates = [t for t in templates if t["technology"] == tech]
        if category:
            templates = [t for t in templates if t["category"] == category]
        if min_score > 0:
            templates = [t for t in templates if t["quality_score"] >= min_score]

        # 按评分排序
        return sorted(templates, key=lambda x: x["quality_score"], reverse=True)


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='网络搜索与经验总结器，生成可复用模板',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--tech',
        type=str,
        required=True,
        help='技术名称（如 FastAPI, React, TensorFlow）'
    )

    parser.add_argument(
        '--query',
        type=str,
        default='best practices',
        help='搜索查询（默认: best practices）'
    )

    parser.add_argument(
        '--category',
        type=str,
        default='general',
        help='模板分类（默认: general）'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='./assets/template-library',
        help='模板库目录（默认: ./assets/template-library）'
    )

    parser.add_argument(
        '--max-results',
        type=int,
        default=20,
        help='最大搜索结果数（默认: 20）'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='列出已有模板'
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

    # 初始化组件
    template_manager = TemplateManager(args.output)

    # 列出模板模式
    if args.list:
        templates = template_manager.list_templates(
            tech=args.tech,
            category=args.category
        )

        print("\n" + "=" * 60)
        print(f"模板列表 ({args.tech}/{args.category})")
        print("=" * 60)

        if not templates:
            print("没有找到模板")
        else:
            for i, t in enumerate(templates, 1):
                print(f"\n{i}. {t['name']}")
                print(f"   评分: {t['quality_score']:.2f}")
                print(f"   版本: {t['version']}")

        print("\n" + "=" * 60)
        return

    # 搜索和生成模式
    logger.info(f"开始搜索 {args.tech} 的 {args.query}...")

    # 1. 执行网络搜索
    searcher = WebSearcher()
    results = searcher.search(args.query, args.tech, args.max_results)

    if not results:
        logger.error("未找到搜索结果")
        return

    logger.info(f"找到 {len(results)} 个搜索结果")

    # 2. 提取解决方案
    extractor = SolutionExtractor()
    solutions = extractor.extract_solutions(results, args.tech)

    if not solutions:
        logger.error("未提取到解决方案")
        return

    logger.info(f"提取到 {len(solutions)} 个解决方案")

    # 3. 生成模板
    generator = TemplateGenerator()
    template = generator.generate_template(solutions, args.tech, args.category)

    logger.info(f"生成模板: {template.name} (评分: {template.quality_score:.2f})")

    # 4. 保存模板
    success = template_manager.save_template(template)

    if success:
        # 生成报告
        report = {
            "technology": args.tech,
            "query": args.query,
            "search_results": len(results),
            "solutions_extracted": len(solutions),
            "template_name": template.name,
            "template_quality": template.quality_score,
            "timestamp": datetime.now().isoformat()
        }

        print("\n" + "=" * 60)
        print("模板生成完成")
        print("=" * 60)
        print(f"技术: {report['technology']}")
        print(f"查询: {report['query']}")
        print(f"搜索结果: {report['search_results']}")
        print(f"解决方案: {report['solutions_extracted']}")
        print(f"模板名称: {report['template_name']}")
        print(f"模板评分: {report['template_quality']:.2f}")
        print("=" * 60)


if __name__ == '__main__':
    main()
