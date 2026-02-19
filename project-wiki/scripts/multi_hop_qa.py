#!/usr/bin/env python3
"""
多跳问答引擎

串联多个文档回答复杂问题
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict


@dataclass
class QueryStep:
    """查询步骤"""
    step_id: int
    query: str
    source_doc: str
    answer: str
    confidence: float
    next_steps: List[int]


@dataclass
class MultiHopResult:
    """多跳问答结果"""
    original_query: str
    decomposition: List[str]
    steps: List[QueryStep]
    final_answer: str
    total_confidence: float
    execution_path: List[str]


class MultiHopQA:
    """多跳问答引擎"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.wiki_path = self.project_path / 'wiki'
        self.knowledge_graph = {}
    
    def build_knowledge_graph(self) -> Dict:
        """构建知识图谱"""
        graph = {
            'nodes': {},
            'edges': {}
        }
        
        if not self.wiki_path.exists():
            self.knowledge_graph = graph
            return graph
        
        # 扫描文档，提取节点和关系
        for doc_file in self.wiki_path.rglob('*.md'):
            doc_name = str(doc_file.relative_to(self.wiki_path))
            
            # 提取文档元数据
            metadata = self._extract_metadata(doc_file)
            
            # 添加节点
            graph['nodes'][doc_name] = {
                'path': str(doc_file),
                'metadata': metadata,
                'content': doc_file.read_text(encoding='utf-8', errors='ignore')
            }
            
            # 提取链接关系
            links = self._extract_links(doc_file)
            graph['edges'][doc_name] = links
        
        self.knowledge_graph = graph
        return graph
    
    def _extract_metadata(self, doc_file: Path) -> Dict:
        """提取文档元数据"""
        metadata = {
            'title': '',
            'tags': [],
            'category': '',
            'module': '',
            'api': '',
            'references': []
        }
        
        try:
            content = doc_file.read_text(encoding='utf-8', errors='ignore')
            
            # 提取标题（第一个一级标题）
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                metadata['title'] = title_match.group(1).strip()
            
            # 提取标签
            tag_matches = re.findall(r'tag[s]?:\s*(.+)', content, re.IGNORECASE)
            for match in tag_matches:
                tags = [t.strip() for t in match.split(',')]
                metadata['tags'].extend(tags)
            
            # 提取分类（从路径推断）
            path_parts = doc_file.relative_to(self.wiki_path).parts
            if len(path_parts) > 0:
                metadata['category'] = path_parts[0]
            if len(path_parts) > 1:
                metadata['module'] = path_parts[1]
            
            # 检查是否是 API 文档
            if 'api' in str(doc_file).lower():
                api_match = re.search(r'API[:\s]+(.+)', content, re.IGNORECASE)
                if api_match:
                    metadata['api'] = api_match.group(1).strip()
            
            # 提取引用
            ref_matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            for ref_title, ref_link in ref_matches:
                metadata['references'].append({
                    'title': ref_title,
                    'link': ref_link
                })
        except:
            pass
        
        return metadata
    
    def _extract_links(self, doc_file: Path) -> List[str]:
        """提取文档中的链接"""
        links = []
        
        try:
            content = doc_file.read_text(encoding='utf-8', errors='ignore')
            
            # 提取 Markdown 链接
            link_matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            for ref_title, ref_link in link_matches:
                # 如果是相对链接，转换为绝对路径
                if not ref_link.startswith(('http://', 'https://', '#')):
                    if not ref_link.endswith('.md'):
                        ref_link = ref_link + '.md'
                    links.append(ref_link)
        except:
            pass
        
        return links
    
    def decompose_query(self, query: str) -> List[str]:
        """分解复杂查询"""
        sub_queries = []
        
        # 识别连接词
        connectors = ['然后', '之后', '接着', '其次', '最后', '另外', '以及', '并且']
        
        # 按连接词分割
        parts = [query]
        for connector in connectors:
            new_parts = []
            for part in parts:
                new_parts.extend(part.split(connector))
            parts = new_parts
        
        # 清理并去重
        for part in parts:
            cleaned = part.strip()
            if cleaned and len(cleaned) > 2:
                sub_queries.append(cleaned)
        
        # 如果没有分解出子查询，尝试基于关键词分解
        if len(sub_queries) == 1:
            sub_queries = self._keyword_decompose(query)
        
        # 如果仍然只有一个查询，基于问题类型分解
        if len(sub_queries) == 1:
            sub_queries = self._type_decompose(query)
        
        return sub_queries
    
    def _keyword_decompose(self, query: str) -> List[str]:
        """基于关键词分解"""
        sub_queries = []
        
        # 识别关键实体
        entities = self._extract_entities(query)
        
        # 识别关键动作
        actions = self._extract_actions(query)
        
        # 组合查询
        if entities and actions:
            for action in actions:
                sub_queries.append(f"{action} {entities[0]}")
        elif entities:
            for entity in entities:
                sub_queries.append(f"关于 {entity}")
        elif actions:
            sub_queries = actions
        
        return sub_queries if sub_queries else [query]
    
    def _type_decompose(self, query: str) -> List[str]:
        """基于问题类型分解"""
        sub_queries = []
        
        # 识别问题类型
        if '如何' in query or 'how' in query.lower():
            # 方法类问题
            sub_queries.append(f"实现 {query.replace('如何', '').replace('how', '')}")
            sub_queries.append(f"最佳实践 {query}")
        elif '为什么' in query or 'why' in query.lower():
            # 原因类问题
            sub_queries.append(f"{query} 的原因")
            sub_queries.append(f"{query} 的影响")
        elif '什么' in query or 'what' in query.lower():
            # 定义类问题
            sub_queries.append(f"{query} 的定义")
            sub_queries.append(f"{query} 的示例")
        elif '哪里' in query or 'where' in query.lower():
            # 位置类问题
            sub_queries.append(f"{query} 在代码中的位置")
            sub_queries.append(f"{query} 的文档位置")
        else:
            sub_queries.append(query)
        
        return sub_queries
    
    def _extract_entities(self, query: str) -> List[str]:
        """提取实体"""
        entities = []
        
        # 常见技术关键词
        tech_keywords = ['API', '接口', '数据库', '缓存', '消息队列', '服务', '模块', '类', '函数']
        
        for keyword in tech_keywords:
            if keyword in query:
                entities.append(keyword)
        
        return entities
    
    def _extract_actions(self, query: str) -> List[str]:
        """提取动作"""
        actions = []
        
        # 常见动作关键词
        action_keywords = ['设计', '实现', '测试', '部署', '优化', '调试', '监控', '日志']
        
        for keyword in action_keywords:
            if keyword in query:
                actions.append(keyword)
        
        return actions
    
    def search_documents(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """搜索相关文档"""
        if not self.knowledge_graph.get('nodes'):
            self.build_knowledge_graph()
        
        results = []
        
        # 简单的关键词匹配
        query_keywords = query.lower().split()
        
        for doc_name, node in self.knowledge_graph['nodes'].items():
            content = node['content'].lower()
            title = node['metadata']['title'].lower()
            
            # 计算匹配分数
            score = 0
            
            # 标题匹配权重更高
            for keyword in query_keywords:
                if keyword in title:
                    score += 2
                if keyword in content:
                    score += 1
            
            if score > 0:
                results.append((doc_name, score))
        
        # 按分数排序
        results.sort(key=lambda x: x[1], reverse=True)
        
        # 返回前 K 个结果
        return results[:top_k]
    
    def answer_single_query(self, query: str, source_doc: str = None) -> QueryStep:
        """回答单个查询"""
        step_id = 0
        
        # 如果没有指定源文档，搜索相关文档
        if source_doc is None:
            docs = self.search_documents(query, top_k=1)
            if docs:
                source_doc = docs[0][0]
        
        # 提取答案（简化版，实际应该使用更复杂的 NLP 技术）
        answer = self._extract_answer(query, source_doc)
        
        # 计算置信度
        confidence = self._calculate_confidence(query, source_doc)
        
        # 确定下一步（如果有）
        next_steps = []
        if self.knowledge_graph.get('edges', {}).get(source_doc):
            next_steps = list(range(len(self.knowledge_graph['edges'][source_doc])))
        
        return QueryStep(
            step_id=step_id,
            query=query,
            source_doc=source_doc,
            answer=answer,
            confidence=confidence,
            next_steps=next_steps
        )
    
    def _extract_answer(self, query: str, source_doc: str) -> str:
        """提取答案"""
        if source_doc not in self.knowledge_graph['nodes']:
            return "未找到相关文档"
        
        node = self.knowledge_graph['nodes'][source_doc]
        content = node['content']
        
        # 查找包含关键词的段落
        query_keywords = query.lower().split()
        relevant_paragraphs = []
        
        for paragraph in content.split('\n\n'):
            paragraph_lower = paragraph.lower()
            relevance = sum(1 for keyword in query_keywords if keyword in paragraph_lower)
            if relevance > 0:
                relevant_paragraphs.append((relevance, paragraph))
        
        # 按相关性排序
        relevant_paragraphs.sort(key=lambda x: x[0], reverse=True)
        
        # 返回最相关的段落
        if relevant_paragraphs:
            return relevant_paragraphs[0][1].strip()
        
        return "未找到相关内容"
    
    def _calculate_confidence(self, query: str, source_doc: str) -> float:
        """计算置信度"""
        if source_doc not in self.knowledge_graph['nodes']:
            return 0.0
        
        node = self.knowledge_graph['nodes'][source_doc]
        content = node['content'].lower()
        title = node['metadata']['title'].lower()
        query_lower = query.lower()
        
        # 基础分数
        confidence = 0.5
        
        # 标题匹配
        if any(keyword in title for keyword in query_lower.split()):
            confidence += 0.3
        
        # 内容匹配
        match_count = sum(1 for keyword in query_lower.split() if keyword in content)
        confidence += min(match_count * 0.1, 0.2)
        
        return min(confidence, 1.0)
    
    def execute_multi_hop(self, query: str) -> MultiHopResult:
        """执行多跳查询"""
        # 构建知识图谱
        self.build_knowledge_graph()
        
        # 分解查询
        sub_queries = self.decompose_query(query)
        
        # 执行每个子查询
        steps = []
        total_confidence = 1.0
        execution_path = []
        
        for i, sub_query in enumerate(sub_queries):
            step = self.answer_single_query(sub_query)
            step.step_id = i
            steps.append(step)
            
            total_confidence *= step.confidence
            if step.source_doc:
                execution_path.append(step.source_doc)
        
        # 合并答案
        final_answer = self._merge_answers(steps)
        
        return MultiHopResult(
            original_query=query,
            decomposition=sub_queries,
            steps=steps,
            final_answer=final_answer,
            total_confidence=total_confidence,
            execution_path=execution_path
        )
    
    def _merge_answers(self, steps: List[QueryStep]) -> str:
        """合并多个步骤的答案"""
        if not steps:
            return "未找到答案"
        
        if len(steps) == 1:
            return steps[0].answer
        
        # 合并多个答案
        merged = []
        for i, step in enumerate(steps):
            merged.append(f"{i + 1}. {step.query}\n   {step.answer}\n")
        
        return "\n".join(merged)
    
    def export_result(self, result: MultiHopResult, output_path: str):
        """导出结果"""
        result_data = {
            "original_query": result.original_query,
            "decomposition": result.decomposition,
            "steps": [
                {
                    "step_id": step.step_id,
                    "query": step.query,
                    "source_doc": step.source_doc,
                    "answer": step.answer,
                    "confidence": step.confidence,
                    "next_steps": step.next_steps
                }
                for step in result.steps
            ],
            "final_answer": result.final_answer,
            "total_confidence": result.total_confidence,
            "execution_path": result.execution_path
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="多跳问答引擎")
    parser.add_argument("--path", required=True, help="项目路径")
    parser.add_argument("--query", required=True, help="查询内容")
    parser.add_argument("--output", help="输出 JSON 路径")
    
    args = parser.parse_args()
    
    # 执行多跳查询
    qa = MultiHopQA(args.path)
    result = qa.execute_multi_hop(args.query)
    
    # 输出结果
    print(f"\n{'='*60}")
    print(f"多跳问答结果")
    print(f"{'='*60}\n")
    
    print(f"原始查询: {result.original_query}")
    print(f"分解查询: {len(result.decomposition)} 个子查询")
    
    print(f"\n执行步骤:")
    for i, step in enumerate(result.steps, 1):
        print(f"\n步骤 {i}:")
        print(f"  查询: {step.query}")
        print(f"  来源: {step.source_doc}")
        print(f"  置信度: {step.confidence:.2%}")
        print(f"  答案: {step.answer[:100]}..." if len(step.answer) > 100 else f"  答案: {step.answer}")
    
    print(f"\n执行路径:")
    for i, path in enumerate(result.execution_path, 1):
        print(f"  {i}. {path}")
    
    print(f"\n总置信度: {result.total_confidence:.2%}")
    
    print(f"\n最终答案:")
    print(result.final_answer)
    
    # 导出结果
    if args.output:
        qa.export_result(result, args.output)
        print(f"\n结果已保存到: {args.output}")


if __name__ == "__main__":
    main()
