#!/usr/bin/env python3
"""
使用 crawl4ai 抓取网站文档并转换为 Markdown 格式（增强版）

功能：
- 抓取单个页面并转换为 Markdown
- 智能路径过滤（仅抓取文档相关路径）
- 自动发现相关文档链接
- 批量抓取多个页面
- 收集元数据（版本号、抓取时间）
- 过滤无关内容（导航、广告等）

使用示例：
python crawl_website.py --url "https://vuejs.org" --depth 2 --output "./docs" --type framework
"""

import os
import sys
import argparse
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
from typing import List, Set, Dict, Optional
import re
from datetime import datetime


def setup_crawl4ai():
    """初始化 crawl4ai"""
    try:
        from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
        from crawl4ai.extraction_strategy import LLMExtractionStrategy
        return AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, LLMExtractionStrategy
    except ImportError:
        print("错误: 未安装 crawl4ai，请运行：pip install crawl4ai>=0.4.0")
        sys.exit(1)


def get_path_filters(doc_type: str) -> Dict[str, List[str]]:
    """
    根据文档类型获取路径过滤规则

    返回：
        - include_paths: 允许的路径前缀
        - exclude_paths: 排除的路径前缀
    """
    filters = {
        "language": {
            "include_paths": [
                "/doc", "/docs", "/reference", "/pkg",
                "/tour", "/tutorial", "/guide", "/learn"
            ],
            "exclude_paths": [
                "/blog", "/news", "/events", "/jobs", "/about",
                "/login", "/register", "/search", "/archive",
                "/forum", "/community", "/talk"
            ]
        },
        "framework": {
            "include_paths": [
                "/guide", "/docs", "/api", "/examples",
                "/tutorial", "/learn", "/reference", "/concepts"
            ],
            "exclude_paths": [
                "/blog", "/news", "/events", "/jobs", "/about",
                "/login", "/register", "/search", "/archive",
                "/marketplace", "/showcase", "/sponsor"
            ]
        },
        "tool": {
            "include_paths": [
                "/docs", "/guide", "/api", "/plugins",
                "/configuration", "/concepts", "/examples"
            ],
            "exclude_paths": [
                "/blog", "/news", "/events", "/jobs", "/about",
                "/login", "/register", "/search", "/archive",
                "/pricing", "/enterprise", "/customers"
            ]
        }
    }

    # 默认使用 framework 规则
    return filters.get(doc_type, filters["framework"])


def should_crawl_url(
    url: str,
    base_url: str,
    crawled_urls: Set[str],
    path_filters: Dict[str, List[str]]
) -> bool:
    """
    判断是否应该抓取该URL（增强版）

    规则：
    - 同域名下
    - 未被抓取过
    - 路径符合文档类型过滤规则
    - 排除锚点链接和媒体文件
    """
    try:
        parsed = urlparse(url)
        base_parsed = urlparse(base_url)

        # 1. 必须是同域名
        if parsed.netloc != base_parsed.netloc:
            return False

        # 2. 避免重复抓取
        if url in crawled_urls:
            return False

        # 3. 排除锚点链接
        if parsed.fragment:
            return False

        # 4. 排除媒体文件
        media_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.pdf', '.zip']
        for ext in media_extensions:
            if parsed.path.lower().endswith(ext):
                return False

        # 5. 路径筛选（基于文档类型）
        path = parsed.path.lower()

        # 检查是否在排除列表中
        for exclude in path_filters["exclude_paths"]:
            if exclude in path:
                return False

        # 检查是否在允许列表中
        for include in path_filters["include_paths"]:
            if include in path:
                return True

        # 6. 首页、根路径也抓取
        if path in ['/', '/index.html', '']:
            return True

        # 7. 其他路径不抓取
        return False

    except Exception as e:
        print(f"URL解析错误: {url}, 错误: {e}")
        return False


def extract_version_from_html(html: str, url: str) -> Optional[str]:
    """
    从HTML中提取版本号

    查找常见的版本号模式
    """
    # 常见版本号模式
    version_patterns = [
        r'version[:\s]+["\']?([0-9]+\.[0-9]+(?:\.[0-9]+)?)["\']?',
        r'v([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
        r'<span[^>]*class="[^"]*version[^"]*"[^>]*>([0-9]+\.[0-9]+(?:\.[0-9]+)?)</span>',
    ]

    for pattern in version_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def extract_links_from_content(html: str, base_url: str) -> List[str]:
    """
    从HTML内容中提取链接

    返回：去重后的URL列表
    """
    links = set()

    # 提取 href 属性
    href_pattern = r'href=["\']([^"\']+)["\']'
    for match in re.finditer(href_pattern, html):
        link = match.group(1)
        # 转换为绝对URL
        absolute_url = urljoin(base_url, link)
        links.add(absolute_url)

    return list(links)


async def crawl_single_page(
    crawler,
    url: str,
    output_dir: Path,
    page_number: int,
    base_url: str
) -> Dict:
    """
    抓取单个页面并保存为 Markdown（增强版）

    返回：包含元数据和链接的字典
    """
    print(f"正在抓取页面 {page_number}: {url}")

    try:
        result = await crawler.arun(
            url=url,
            config={
                "extract_markdown": True,
                "remove_forms": True,
                "remove_scripts": True,
                "remove_comments": True,
            }
        )

        if not result.success:
            print(f"  抓取失败: {result.error_message}")
            return {
                "url": url,
                "success": False,
                "error": result.error_message,
                "links": []
            }

        # 提取 Markdown 内容
        markdown_content = result.markdown

        # 清理内容（移除导航、页脚等）
        markdown_content = clean_markdown(markdown_content)

        # 提取版本号（仅对首页）
        version = None
        if page_number == 1:
            version = extract_version_from_html(result.html, url)

        # 生成文件名
        parsed_url = urlparse(url)
        filename = parsed_url.path.strip('/') or 'index'
        filename = filename.replace('/', '_') or 'index'
        if filename.endswith('.html'):
            filename = filename[:-5]
        filename = f"{page_number:03d}_{filename}.md"
        filepath = output_dir / filename

        # 保存文件（包含元数据）
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {url}\n\n")
            f.write(f"<!--\n")
            f.write(f"Source URL: {url}\n")
            f.write(f"Crawled at: {datetime.now().isoformat()}\n")
            if version:
                f.write(f"Version: {version}\n")
            f.write(f"-->\n\n")
            f.write(markdown_content)

        print(f"  保存成功: {filepath}")
        if version:
            print(f"  检测到版本: {version}")

        # 提取链接
        links = extract_links_from_content(result.html, url)

        return {
            "url": url,
            "success": True,
            "filepath": str(filepath),
            "links": links,
            "title": result.metadata.get("title", url),
            "version": version,
            "crawled_at": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"  抓取异常: {e}")
        return {
            "url": url,
            "success": False,
            "error": str(e),
            "links": []
        }


def clean_markdown(content: str) -> str:
    """
    清理 Markdown 内容，移除无关元素
    """
    lines = content.split('\n')
    cleaned_lines = []

    skip_patterns = [
        r'^\s*<nav',
        r'^\s*<footer',
        r'^\s*<aside',
        r'^\s*<script',
        r'^\s*Skip to',
        r'^\s*Menu',
        r'^\s*Navigation',
        r'^\s*Search',
        r'^\s*Language',
        r'^\s*GitHub',
        r'^\s*Twitter',
    ]

    for line in lines:
        skip = False
        for pattern in skip_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                skip = True
                break

        if not skip:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


async def crawl_website(
    url: str,
    output_dir: str,
    max_depth: int = 2,
    max_pages: int = 50,
    doc_type: str = "framework"
):
    """
    抓取网站主函数（增强版）

    参数：
        url: 起始URL
        output_dir: 输出目录
        max_depth: 最大抓取深度
        max_pages: 最大抓取页面数
        doc_type: 文档类型（language/framework/tool）
    """
    # 初始化依赖
    AsyncWebCrawler = setup_crawl4ai()[0]

    # 获取路径过滤规则
    path_filters = get_path_filters(doc_type)

    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"开始抓取网站: {url}")
    print(f"输出目录: {output_path}")
    print(f"最大深度: {max_depth}")
    print(f"最大页面数: {max_pages}")
    print(f"文档类型: {doc_type}")
    print(f"允许路径: {', '.join(path_filters['include_paths'])}")
    print(f"排除路径: {', '.join(path_filters['exclude_paths'])}")
    print("-" * 60)

    # 记录已抓取的URL
    crawled_urls: Set[str] = set()
    results = []
    detected_version = None

    # 使用 AsyncWebCrawler
    async with AsyncWebCrawler(verbose=True) as crawler:
        # 按深度抓取
        current_level_urls = [url]
        page_count = 0

        for depth in range(max_depth + 1):
            if not current_level_urls or page_count >= max_pages:
                break

            print(f"\n抓取深度 {depth}，待抓取URL数: {len(current_level_urls)}")
            print("-" * 60)

            next_level_urls = set()

            for current_url in current_level_urls:
                if page_count >= max_pages:
                    print(f"已达到最大页面数限制 ({max_pages})")
                    break

                # 抓取页面
                result = await crawl_single_page(
                    crawler,
                    current_url,
                    output_path,
                    page_number=page_count + 1,
                    base_url=url
                )

                crawled_urls.add(current_url)
                results.append(result)

                # 记录版本号
                if result.get("version"):
                    detected_version = result["version"]

                page_count += 1

                # 提取下一层URL
                if result["success"] and depth < max_depth:
                    for link in result["links"]:
                        if should_crawl_url(link, url, crawled_urls, path_filters):
                            next_level_urls.add(link)

            current_level_urls = list(next_level_urls)

    # 保存抓取摘要（包含元数据）
    summary = {
        "base_url": url,
        "doc_type": doc_type,
        "total_pages": page_count,
        "max_depth": max_depth,
        "detected_version": detected_version,
        "crawled_at": datetime.now().isoformat(),
        "path_filters": path_filters,
        "results": results
    }

    summary_file = output_path / "_crawl_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"抓取完成！")
    print(f"总页面数: {page_count}")
    print(f"输出目录: {output_path}")
    print(f"摘要文件: {summary_file}")
    if detected_version:
        print(f"检测到版本: {detected_version}")
    print("=" * 60)

    # 统计信息
    success_count = sum(1 for r in results if r["success"])
    print(f"\n统计:")
    print(f"  成功: {success_count}")
    print(f"  失败: {page_count - success_count}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="使用 crawl4ai 抓取网站文档（增强版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 抓取 Vue 官网（框架类型）
  python crawl_website.py --url https://vuejs.org --depth 2 --output ./vue-docs --type framework

  # 抓取 Go 文档（语言类型）
  python crawl_website.py --url https://go.dev/doc --depth 3 --max-pages 100 --output ./go-docs --type language

  # 抓取 Webpack 文档（工具类型）
  python crawl_website.py --url https://webpack.js.org --depth 2 --output ./webpack-docs --type tool
        """
    )

    parser.add_argument(
        '--url',
        required=True,
        help='要抓取的网站URL'
    )

    parser.add_argument(
        '--output',
        required=True,
        help='输出目录路径'
    )

    parser.add_argument(
        '--depth',
        type=int,
        default=2,
        help='抓取深度（默认: 2）'
    )

    parser.add_argument(
        '--max-pages',
        type=int,
        default=50,
        help='最大抓取页面数（默认: 50）'
    )

    parser.add_argument(
        '--type',
        choices=['language', 'framework', 'tool'],
        default='framework',
        help='文档类型，用于路径过滤（默认: framework）'
    )

    args = parser.parse_args()

    # 执行抓取
    import asyncio
    asyncio.run(crawl_website(
        url=args.url,
        output_dir=args.output,
        max_depth=args.depth,
        max_pages=args.max_pages,
        doc_type=args.type
    ))


if __name__ == "__main__":
    main()
