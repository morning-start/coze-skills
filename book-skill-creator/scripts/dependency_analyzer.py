#!/usr/bin/env python3
"""
依赖关系分析器
分析技能间的依赖关系，生成依赖图和构建顺序
"""

import argparse
import json
import sys
import logging
import networkx as nx
from pathlib import Path
from typing import Dict, List, Set, Any


# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='分析技能间的依赖关系',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--base-dir',
        type=str,
        required=True,
        help='包含多个技能的基础目录'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='./dependency-report.json',
        help='输出报告文件路径（默认: ./dependency-report.json）'
    )

    parser.add_argument(
        '--format',
        type=str,
        choices=['json', 'text'],
        default='text',
        help='输出格式（json/text）'
    )

    parser.add_argument(
        '--visualize',
        type=str,
        help='生成依赖图图片文件（需要 matplotlib）'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='启用详细日志'
    )

    return parser.parse_args()


def extract_dependencies(skill_dir: Path) -> Dict[str, Any]:
    """从技能目录提取依赖信息"""
    skill_md = skill_dir / 'SKILL.md'

    if not skill_md.exists():
        logger.warning(f"SKILL.md 不存在: {skill_dir.name}")
        return {"name": skill_dir.name, "dependencies": []}

    try:
        import yaml
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取 YAML 前言区
        if content.startswith('---'):
            end_marker = content.find('\n---\n', 3)
            if end_marker != -1:
                yaml_content = content[3:end_marker]
                front_matter = yaml.safe_load(yaml_content)
                return {
                    "name": front_matter.get("name", skill_dir.name),
                    "description": front_matter.get("description", ""),
                    "dependencies": front_matter.get("dependencies", [])
                }

    except Exception as e:
        logger.error(f"读取 {skill_dir.name} 的依赖信息失败: {e}")

    return {"name": skill_dir.name, "dependencies": []}


def build_dependency_graph(base_dir: Path) -> nx.DiGraph:
    """构建依赖关系图"""
    graph = nx.DiGraph()

    # 扫描所有技能目录
    skills = []
    for item in base_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            skills.append(item)

    logger.info(f"发现 {len(skills)} 个技能")

    # 提取依赖信息
    skill_deps = {}
    for skill_dir in skills:
        deps_info = extract_dependencies(skill_dir)
        skill_deps[deps_info["name"]] = deps_info

    # 构建图
    for skill_name, deps_info in skill_deps.items():
        graph.add_node(skill_name, description=deps_info["description"])

        for dep in deps_info["dependencies"]:
            if dep in skill_deps:
                graph.add_edge(dep, skill_name)
                logger.debug(f"依赖关系: {skill_name} -> {dep}")
            else:
                logger.warning(f"{skill_name} 依赖的技能不存在: {dep}")

    return graph


def analyze_graph(graph: nx.DiGraph) -> Dict[str, Any]:
    """分析依赖图"""
    analysis = {}

    # 节点数和边数
    analysis["total_skills"] = graph.number_of_nodes()
    analysis["total_dependencies"] = graph.number_of_edges()

    # 拓扑排序（构建顺序）
    try:
        build_order = list(nx.topological_sort(graph))
        analysis["build_order"] = build_order
        analysis["has_cycle"] = False
    except nx.NetworkXUnfeasible:
        analysis["has_cycle"] = True
        analysis["cycles"] = list(nx.simple_cycles(graph))

    # 入度和出度统计
    analysis["dependency_stats"] = {}
    for node in graph.nodes():
        in_degree = graph.in_degree(node)
        out_degree = graph.out_degree(node)
        analysis["dependency_stats"][node] = {
            "depends_on": in_degree,
            "required_by": out_degree
        }

    # 找出无依赖的技能（叶节点）
    no_deps = [node for node in graph.nodes() if graph.in_degree(node) == 0]
    analysis["no_dependencies"] = no_deps

    # 找出被最多技能依赖的技能
    most_required = sorted(
        graph.nodes(),
        key=lambda x: graph.in_degree(x),
        reverse=True
    )
    analysis["most_required"] = most_required

    return analysis


def visualize_graph(graph: nx.DiGraph, output_path: str):
    """可视化依赖图"""
    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(12, 8))

        # 使用分层布局
        pos = nx.spring_layout(graph, k=2, iterations=50)

        # 绘制节点
        nx.draw_networkx_nodes(
            graph,
            pos,
            node_color='lightblue',
            node_size=2000,
            alpha=0.9
        )

        # 绘制边
        nx.draw_networkx_edges(
            graph,
            pos,
            edge_color='gray',
            arrows=True,
            arrowsize=20,
            alpha=0.6
        )

        # 绘制标签
        nx.draw_networkx_labels(
            graph,
            pos,
            font_size=10,
            font_weight='bold'
        )

        plt.title("技能依赖关系图")
        plt.axis('off')

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"依赖图已保存: {output_path}")

    except ImportError:
        logger.warning("未安装 matplotlib，无法生成可视化图片")
    except Exception as e:
        logger.error(f"生成可视化图片失败: {e}")


def generate_report_text(graph: nx.DiGraph, analysis: Dict[str, Any]) -> str:
    """生成文本格式报告"""
    report = []
    report.append("=" * 60)
    report.append("技能依赖关系分析报告")
    report.append("=" * 60)
    report.append("")

    # 基本统计
    report.append("基本统计:")
    report.append(f"  总技能数: {analysis['total_skills']}")
    report.append(f"  总依赖数: {analysis['total_dependencies']}")
    report.append("")

    # 构建顺序
    if analysis["has_cycle"]:
        report.append("警告: 检测到循环依赖!")
        report.append("循环依赖链:")
        for cycle in analysis["cycles"]:
            report.append(f"  {' -> '.join(cycle)}")
    else:
        report.append("构建顺序（拓扑排序）:")
        for i, skill in enumerate(analysis["build_order"], 1):
            report.append(f"  {i}. {skill}")
    report.append("")

    # 依赖统计
    report.append("依赖统计:")
    report.append("  无依赖的技能（可优先构建）:")
    for skill in analysis["no_dependencies"]:
        report.append(f"    - {skill}")
    report.append("")

    report.append("  被最多技能依赖:")
    for skill in analysis["most_required"][:5]:
        count = analysis["dependency_stats"][skill]["required_by"]
        report.append(f"    - {skill} (被 {count} 个技能依赖)")
    report.append("")

    # 详细依赖信息
    report.append("详细依赖信息:")
    for skill, stats in analysis["dependency_stats"].items():
        if stats["depends_on"] > 0 or stats["required_by"] > 0:
            report.append(f"  {skill}:")
            report.append(f"    依赖: {stats['depends_on']} 个技能")
            report.append(f"    被依赖: {stats['required_by']} 个技能")
    report.append("")

    return "\n".join(report)


def main():
    """主函数"""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    base_dir = Path(args.base_dir)

    if not base_dir.exists():
        logger.error(f"基础目录不存在: {args.base_dir}")
        sys.exit(1)

    # 构建依赖图
    logger.info("构建依赖关系图...")
    graph = build_dependency_graph(base_dir)

    # 分析依赖图
    logger.info("分析依赖关系...")
    analysis = analyze_graph(graph)

    # 生成报告
    if args.format == 'json':
        report_data = {
            "graph": {
                "nodes": list(graph.nodes()),
                "edges": list(graph.edges())
            },
            "analysis": analysis
        }
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        logger.info(f"JSON 报告已保存: {args.output}")
    else:
        report_text = generate_report_text(graph, analysis)
        print(report_text)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report_text)
            logger.info(f"文本报告已保存: {args.output}")

    # 可视化（如果指定）
    if args.visualize:
        visualize_graph(graph, args.visualize)

    # 退出码
    if analysis["has_cycle"]:
        logger.error("检测到循环依赖，构建顺序无法确定")
        sys.exit(1)
    else:
        logger.info("依赖关系分析完成")
        sys.exit(0)


if __name__ == '__main__':
    main()
