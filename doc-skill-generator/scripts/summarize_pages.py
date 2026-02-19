#!/usr/bin/env python3
"""
使用 LLM 对抓取的页面进行摘要，生成核心能力图谱

功能：
- 批量读取抓取的 Markdown 文档
- 使用智能体进行摘要分析
- 生成核心能力图谱（JSON 格式）
- 聚合关键概念和学习路径

使用示例：
python summarize_pages.py --input "./raw_docs" --output "./summary.json"
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict, Set
from datetime import datetime


def read_markdown_files(docs_dir: Path) -> List[Dict[str, str]]:
    """
    读取目录下所有 Markdown 文件

    返回：包含文件路径和内容的字典列表
    """
    files = []
    for md_file in docs_dir.glob("*.md"):
        # 跳过摘要文件本身
        if md_file.name.startswith("_"):
            continue

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取标题（第一行）
            lines = content.split('\n', maxsplit=1)
            title = lines[0].replace('#', '').strip() if lines[0].startswith('#') else md_file.stem

            files.append({
                "filepath": str(md_file),
                "filename": md_file.name,
                "title": title,
                "content": content
            })

        except Exception as e:
            print(f"读取文件失败 {md_file}: {e}")

    return files


def generate_page_summary(page: Dict[str, str]) -> Dict:
    """
    为单个页面生成摘要

    注意：此函数需要由智能体调用或配合 LLM 使用
    这里返回页面基本信息，实际摘要由智能体完成
    """
    return {
        "filename": page["filename"],
        "title": page["title"],
        "filepath": page["filepath"],
        "content_length": len(page["content"]),
        "word_count": len(page["content"].split())
    }


def build_core_concept_graph(pages: List[Dict[str, str]]) -> Dict:
    """
    构建核心概念图谱

    返回：包含核心概念、关联关系的图谱结构
    """
    # 这里提供基础结构，实际内容需要智能体分析
    graph = {
        "concepts": [],
        "relationships": [],
        "learning_paths": [],
        "metadata": {
            "total_pages": len(pages),
            "generated_at": datetime.now().isoformat()
        }
    }

    # 分析每个页面，提取潜在概念（简单启发式）
    concept_keywords = set()
    for page in pages:
        # 从标题和内容中提取大写单词作为潜在概念
        words = page["title"].split()
        for word in words:
            if len(word) > 3 and word[0].isupper():
                concept_keywords.add(word)

    graph["concepts"] = [{"name": concept, "type": "unknown"} for concept in sorted(concept_keywords)]

    return graph


def analyze_document_structure(pages: List[Dict[str, str]]) -> Dict:
    """
    分析文档结构，识别文档类型

    返回：文档类型分析和建议
    """
    analysis = {
        "document_types": {},
        "total_pages": len(pages),
        "content_distribution": {},
        "recommended_skill_type": "framework"
    }

    # 统计文档类型
    for page in pages:
        filename_lower = page["filename"].lower()
        title_lower = page["title"].lower()

        # 识别文档类型
        if "api" in filename_lower or "api" in title_lower:
            analysis["document_types"]["api"] = analysis["document_types"].get("api", 0) + 1
        elif "guide" in filename_lower or "tutorial" in filename_lower:
            analysis["document_types"]["guide"] = analysis["document_types"].get("guide", 0) + 1
        elif "example" in filename_lower or "demo" in filename_lower:
            analysis["document_types"]["example"] = analysis["document_types"].get("example", 0) + 1
        elif "reference" in filename_lower:
            analysis["document_types"]["reference"] = analysis["document_types"].get("reference", 0) + 1
        else:
            analysis["document_types"]["general"] = analysis["document_types"].get("general", 0) + 1

    # 推荐技能类型（简单启发式）
    if analysis["document_types"].get("api", 0) > len(pages) * 0.5:
        analysis["recommended_skill_type"] = "language"
    elif analysis["document_types"].get("guide", 0) > len(pages) * 0.3:
        analysis["recommended_skill_type"] = "framework"

    return analysis


def generate_summary_report(pages: List[Dict[str, str]], output_path: Path):
    """
    生成摘要报告

    报告包含：
    - 页面基本信息
    - 文档结构分析
    - 核心概念图谱（基础版本）
    - 技能类型推荐
    """
    # 生成页面摘要
    page_summaries = [generate_page_summary(page) for page in pages]

    # 分析文档结构
    structure_analysis = analyze_document_structure(pages)

    # 构建概念图谱
    concept_graph = build_core_concept_graph(pages)

    # 合并报告
    report = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_pages": len(pages),
            "input_directory": str(output_path.parent)
        },
        "document_structure": structure_analysis,
        "concept_graph": concept_graph,
        "pages": page_summaries,
        "recommendations": {
            "skill_type": structure_analysis["recommended_skill_type"],
            "priority_pages": sorted(page_summaries, key=lambda x: x["word_count"], reverse=True)[:5]
        }
    }

    # 保存报告
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"摘要报告已生成: {output_path}")
    print(f"  - 总页面数: {len(pages)}")
    print(f"  - 推荐技能类型: {structure_analysis['recommended_skill_type']}")
    print(f"  - 识别概念数: {len(concept_graph['concepts'])}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="使用 LLM 对抓取的页面进行摘要分析",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 对抓取的文档生成摘要
  python summarize_pages.py --input ./raw_docs --output ./summary.json

  # 指定文档类型提示
  python summarize_pages.py --input ./raw_docs --output ./summary.json --type framework
        """
    )

    parser.add_argument(
        '--input',
        required=True,
        help='抓取的文档目录路径'
    )

    parser.add_argument(
        '--output',
        required=True,
        help='摘要报告输出路径（JSON 格式）'
    )

    parser.add_argument(
        '--type',
        choices=['language', 'framework', 'tool'],
        default='framework',
        help='文档类型提示（用于模板选择）'
    )

    args = parser.parse_args()

    # 读取文档
    docs_dir = Path(args.input)
    if not docs_dir.exists():
        print(f"错误: 目录不存在 {args.input}")
        sys.exit(1)

    pages = read_markdown_files(docs_dir)
    if not pages:
        print(f"错误: 未找到 Markdown 文件在 {args.input}")
        sys.exit(1)

    print(f"找到 {len(pages)} 个 Markdown 文件")

    # 生成摘要报告
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    generate_summary_report(pages, output_path)


if __name__ == "__main__":
    main()
