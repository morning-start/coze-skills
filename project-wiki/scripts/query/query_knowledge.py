#!/usr/bin/env python3
"""
知识查询接口
功能：语义检索和知识查询
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class KnowledgeQuerier:
    """知识查询器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.references_path = Path(__file__).parent.parent / "references"
        self.project_info = self._load_project_info()
        self.knowledge_index = self._build_knowledge_index()
    
    def _load_project_info(self) -> Dict:
        """加载项目分析信息"""
        analysis_file = self.project_path / "project-analysis.json"
        if analysis_file.exists():
            with open(analysis_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _build_knowledge_index(self) -> Dict:
        """构建知识索引"""
        index = {
            'core': {},
            'document-guides': {},
            'visualization': {},
            'frameworks': {},
            'templates': {}
        }
        
        # 索引核心指南
        core_path = self.references_path / 'core'
        if core_path.exists():
            for file in core_path.glob('*.md'):
                index['core'][file.stem] = {
                    'path': str(file),
                    'title': self._extract_title(file)
                }
        
        # 索引文档规范
        doc_guides_path = self.references_path / 'document-guides'
        if doc_guides_path.exists():
            for file in doc_guides_path.glob('*.md'):
                index['document-guides'][file.stem] = {
                    'path': str(file),
                    'title': self._extract_title(file)
                }
        
        # 索引可视化
        viz_path = self.references_path / 'visualization'
        if viz_path.exists():
            for file in viz_path.glob('*.md'):
                index['visualization'][file.stem] = {
                    'path': str(file),
                    'title': self._extract_title(file)
                }
        
        # 索引框架指引
        frameworks_path = self.references_path / 'frameworks'
        if frameworks_path.exists():
            for file in frameworks_path.glob('*-guide.md'):
                framework_name = file.stem.replace('-guide', '')
                index['frameworks'][framework_name] = {
                    'path': str(file),
                    'title': self._extract_title(file)
                }
        
        return index
    
    def _extract_title(self, file_path: Path) -> str:
        """从文件中提取标题"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line.startswith('# '):
                    return first_line[2:].strip()
        except:
            pass
        return file_path.stem
    
    def _search_by_keywords(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """关键词搜索"""
        results = []
        query_lower = query.lower()
        
        # 确定搜索范围
        search_categories = [category] if category else list(self.knowledge_index.keys())
        
        for cat in search_categories:
            if cat not in self.knowledge_index:
                continue
            
            for name, info in self.knowledge_index[cat].items():
                # 搜索标题
                if query_lower in info['title'].lower():
                    results.append({
                        'category': cat,
                        'name': name,
                        'title': info['title'],
                        'path': info['path'],
                        'relevance': 'high'
                    })
                
                # 搜索文件名
                if query_lower in name.lower():
                    results.append({
                        'category': cat,
                        'name': name,
                        'title': info['title'],
                        'path': info['path'],
                        'relevance': 'medium'
                    })
        
        return results
    
    def _detect_intent(self, query: str) -> Tuple[str, Optional[str]]:
        """检测用户意图"""
        query_lower = query.lower()
        
        # 文档查询意图
        if any(kw in query_lower for kw in ['如何', '规范', '格式', '怎么写']):
            # 进一步分类
            if 'api' in query_lower or '接口' in query_lower:
                return ('query_guide', 'api-doc-guide')
            elif '架构' in query_lower:
                return ('query_guide', 'architecture-guide')
            elif 'changelog' in query_lower or '变更日志' in query_lower:
                return ('query_guide', 'changelog-guide')
            elif 'roadmap' in query_lower or '规划' in query_lower:
                return ('query_guide', 'roadmap-guide')
            elif '结构' in query_lower or '目录' in query_lower:
                return ('query_guide', 'wiki-structure-guide')
            else:
                return ('query_guide', None)
        
        # 框架查询意图
        elif '框架' in query_lower or '技术栈' in query_lower:
            return ('query_framework', None)
        
        # 图表生成意图
        elif any(kw in query_lower for kw in ['流程图', '架构图', '时序图', '类图', '状态图']):
            return ('query_visualization', 'mermaid-syntax')
        
        # 通用搜索
        else:
            return ('search', None)
    
    def query(self, query: str) -> Dict:
        """执行查询"""
        
        print(f"查询: {query}")
        
        # 检测意图
        intent, target = self._detect_intent(query)
        
        result = {
            'query': query,
            'intent': intent,
            'target': target,
            'results': []
        }
        
        if intent == 'query_guide':
            # 查询特定指南
            if target:
                # 搜索所有类别
                for cat, items in self.knowledge_index.items():
                    if target in items:
                        guide = items[target]
                        result['results'].append({
                            'category': cat,
                            'name': target,
                            'title': guide['title'],
                            'path': guide['path'],
                            'relevance': 'exact'
                        })
                        break
            else:
                # 返回所有指南列表
                for name, info in self.knowledge_index['document-guides'].items():
                    result['results'].append({
                        'category': 'document-guides',
                        'name': name,
                        'title': info['title'],
                        'path': info['path']
                    })
        
        elif intent == 'query_framework':
            # 查询框架
            frameworks = self.project_info.get('frameworks', [])
            for fw in frameworks:
                if fw in self.knowledge_index['frameworks']:
                    result['results'].append({
                        'category': 'frameworks',
                        'name': fw,
                        'title': self.knowledge_index['frameworks'][fw]['title'],
                        'path': self.knowledge_index['frameworks'][fw]['path']
                    })
            
            if not result['results']:
                # 返回所有可用框架
                for name, info in self.knowledge_index['frameworks'].items():
                    result['results'].append({
                        'category': 'frameworks',
                        'name': name,
                        'title': info['title'],
                        'path': info['path']
                    })
        
        elif intent == 'query_visualization':
            # 查询可视化指南
            if target and target in self.knowledge_index.get('visualization', {}):
                viz = self.knowledge_index['visualization'][target]
                result['results'].append({
                    'category': 'visualization',
                    'name': target,
                    'title': viz['title'],
                    'path': viz['path']
                })
        
        elif intent == 'search':
            # 关键词搜索
            results = self._search_by_keywords(query)
            result['results'] = results
        
        return result
    
    def get_document_content(self, doc_path: str) -> Optional[str]:
        """获取文档内容"""
        path = Path(doc_path)
        if not path.is_absolute():
            path = self.project_path / doc_path
        
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def list_all_knowledge(self) -> Dict:
        """列出所有知识"""
        return self.knowledge_index


def main():
    parser = argparse.ArgumentParser(description='知识查询接口')
    parser.add_argument('--path', type=str, default='.', help='项目路径')
    parser.add_argument('--query', type=str, help='查询内容')
    parser.add_argument('--list', action='store_true', help='列出所有知识')
    parser.add_argument('--get', type=str, help='获取文档内容')
    
    args = parser.parse_args()
    
    querier = KnowledgeQuerier(args.path)
    
    if args.list:
        # 列出所有知识
        index = querier.list_all_knowledge()
        print(json.dumps(index, indent=2, ensure_ascii=False))
    
    elif args.get:
        # 获取文档内容
        content = querier.get_document_content(args.get)
        if content:
            print(content)
        else:
            print(f"文档不存在: {args.get}")
    
    elif args.query:
        # 执行查询
        result = querier.query(args.query)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        # 交互式查询
        print("ProjectWiki 知识查询接口")
        print("输入 'exit' 退出")
        print("="*50)
        
        while True:
            query = input("\n查询: ").strip()
            if query.lower() == 'exit':
                break
            
            if not query:
                continue
            
            result = querier.query(query)
            print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
