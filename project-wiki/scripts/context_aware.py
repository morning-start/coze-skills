#!/usr/bin/env python3
"""
上下文感知增强器

自动注入环境上下文，使回答更精准
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ContextInfo:
    """上下文信息"""
    project_path: str
    current_file: Optional[str]
    current_function: Optional[str]
    current_class: Optional[str]
    git_branch: Optional[str]
    git_commit: Optional[str]
    environment: str
    timestamp: str
    user_role: Optional[str]


@dataclass
class EnhancedResponse:
    """增强响应"""
    original_query: str
    context: ContextInfo
    enhanced_query: str
    suggested_knowledge: List[str]
    suggested_resources: List[str]
    confidence: float


class ContextAwareness:
    """上下文感知"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.context_cache = {}
    
    def collect_context(self, current_file: str = None, user_role: str = None) -> ContextInfo:
        """收集上下文信息"""
        context = ContextInfo(
            project_path=str(self.project_path),
            current_file=current_file,
            current_function=self._detect_current_function(current_file),
            current_class=self._detect_current_class(current_file),
            git_branch=self._get_git_branch(),
            git_commit=self._get_git_commit(),
            environment=self._detect_environment(),
            timestamp=datetime.now().isoformat(),
            user_role=user_role
        )
        
        self.context_cache['current'] = context
        return context
    
    def _detect_current_function(self, file_path: str = None) -> Optional[str]:
        """检测当前函数"""
        # 这里可以集成代码分析器，获取当前光标所在的函数
        # 暂时返回 None
        return None
    
    def _detect_current_class(self, file_path: str = None) -> Optional[str]:
        """检测当前类"""
        # 这里可以集成代码分析器，获取当前光标所在的类
        # 暂时返回 None
        return None
    
    def _get_git_branch(self) -> Optional[str]:
        """获取 Git 分支"""
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def _get_git_commit(self) -> Optional[str]:
        """获取 Git 提交"""
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()[:7]  # 只取前7位
        except:
            pass
        return None
    
    def _detect_environment(self) -> str:
        """检测环境"""
        # 检查是否有虚拟环境
        if os.getenv('VIRTUAL_ENV') or os.getenv('CONDA_PREFIX'):
            return 'development'
        
        # 检查是否有 Docker
        if os.path.exists('/.dockerenv'):
            return 'docker'
        
        # 检查 CI/CD 环境
        if os.getenv('CI') or os.getenv('JENKINS_URL'):
            return 'ci/cd'
        
        return 'local'
    
    def enhance_query(self, query: str, context: ContextInfo) -> str:
        """增强查询"""
        enhanced_parts = [query]
        
        # 添加文件上下文
        if context.current_file:
            relative_file = Path(context.current_file).relative_to(self.project_path)
            enhanced_parts.append(f"（参考文件: {relative_file}）")
        
        # 添加函数上下文
        if context.current_function:
            enhanced_parts.append(f"（当前函数: {context.current_function}）")
        
        # 添加类上下文
        if context.current_class:
            enhanced_parts.append(f"（当前类: {context.current_class}）")
        
        # 添加 Git 上下文
        if context.git_branch:
            enhanced_parts.append(f"（分支: {context.git_branch}）")
        
        # 添加角色上下文
        if context.user_role:
            enhanced_parts.append(f"（角色: {context.user_role}）")
        
        return " ".join(enhanced_parts)
    
    def suggest_knowledge(self, query: str, context: ContextInfo) -> List[str]:
        """建议相关知识"""
        suggestions = []
        
        # 基于查询关键词建议
        keywords = query.lower().split()
        
        # API 相关
        if any(keyword in keywords for keyword in ['api', '接口', 'endpoint', '接口文档']):
            suggestions.append("wiki/api-docs/")
            if context.current_file:
                module_name = Path(context.current_file).stem
                suggestions.append(f"wiki/modules/{module_name}/")
        
        # 架构相关
        if any(keyword in keywords for keyword in ['架构', 'architecture', '设计', 'design']):
            suggestions.append("wiki/01-架构文档/")
            suggestions.append("references/architecture-principles.md")
        
        # 测试相关
        if any(keyword in keywords for keyword in ['测试', 'test', '单元测试', 'unit test']):
            suggestions.append("wiki/05-测试文档/")
            if context.current_file:
                test_file = f"tests/{Path(context.current_file).stem}_test.py"
                suggestions.append(test_file)
        
        # 部署相关
        if any(keyword in keywords for keyword in ['部署', 'deploy', '运维', 'ops']):
            suggestions.append("wiki/06-运维文档/")
            suggestions.append("references/deployment-guide.md")
        
        # 数据模型相关
        if any(keyword in keywords for keyword in ['模型', 'model', '数据', 'data', 'schema']):
            suggestions.append("wiki/modules/*/models/")
            suggestions.append("references/data-models.md")
        
        return suggestions
    
    def suggest_resources(self, query: str, context: ContextInfo) -> List[str]:
        """建议相关资源"""
        resources = []
        
        # 基于角色建议
        if context.user_role:
            role_resources = {
                'architect': [
                    'references/architecture-principles.md',
                    'references/design-patterns.md',
                    'references/capability-model.md'
                ],
                'developer': [
                    'references/coding-standards.md',
                    'references/api-design.md',
                    'references/testing-guide.md'
                ],
                'tester': [
                    'references/testing-guide.md',
                    'references/quality-assurance.md',
                    'references/bug-reporting.md'
                ],
                'ops': [
                    'references/deployment-guide.md',
                    'references/monitoring-guide.md',
                    'references/operations-runbook.md'
                ],
                'product': [
                    'references/user-flow.md',
                    'references/feature-specification.md',
                    'references/product-roadmap.md'
                ]
            }
            
            if context.user_role in role_resources:
                resources.extend(role_resources[context.user_role])
        
        # 基于查询关键词建议
        keywords = query.lower().split()
        
        if any(keyword in keywords for keyword in ['python', 'django', 'fastapi']):
            resources.append('references/python-best-practices.md')
        elif any(keyword in keywords for keyword in ['javascript', 'react', 'vue']):
            resources.append('references/frontend-guide.md')
        elif any(keyword in keywords for keyword in ['数据库', 'database', 'sql', 'nosql']):
            resources.append('references/database-design.md')
        
        return list(set(resources))  # 去重
    
    def calculate_confidence(self, query: str, context: ContextInfo) -> float:
        """计算置信度"""
        confidence = 0.5  # 基础置信度
        
        # 如果有文件上下文，提升置信度
        if context.current_file:
            confidence += 0.2
        
        # 如果有角色上下文，提升置信度
        if context.user_role:
            confidence += 0.1
        
        # 如果有 Git 上下文，提升置信度
        if context.git_branch:
            confidence += 0.1
        
        # 如果查询包含具体关键词，提升置信度
        specific_keywords = ['函数', '类', '模块', '接口', '数据库', '缓存']
        if any(keyword in query for keyword in specific_keywords):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def process_query(self, query: str, current_file: str = None, user_role: str = None) -> EnhancedResponse:
        """处理查询，返回增强响应"""
        # 收集上下文
        context = self.collect_context(current_file, user_role)
        
        # 增强查询
        enhanced_query = self.enhance_query(query, context)
        
        # 建议知识
        suggested_knowledge = self.suggest_knowledge(query, context)
        
        # 建议资源
        suggested_resources = self.suggest_resources(query, context)
        
        # 计算置信度
        confidence = self.calculate_confidence(query, context)
        
        return EnhancedResponse(
            original_query=query,
            context=context,
            enhanced_query=enhanced_query,
            suggested_knowledge=suggested_knowledge,
            suggested_resources=suggested_resources,
            confidence=confidence
        )


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="上下文感知增强器")
    parser.add_argument("--path", required=True, help="项目路径")
    parser.add_argument("--query", required=True, help="查询内容")
    parser.add_argument("--file", help="当前文件路径")
    parser.add_argument("--role", help="用户角色（architect/developer/tester/ops/product）")
    parser.add_argument("--output", help="输出 JSON 路径")
    
    args = parser.parse_args()
    
    # 处理查询
    awareness = ContextAwareness(args.path)
    response = awareness.process_query(args.query, args.file, args.role)
    
    # 输出结果
    print(f"\n{'='*60}")
    print(f"上下文感知增强结果")
    print(f"{'='*60}\n")
    
    print(f"原始查询: {response.original_query}")
    print(f"增强查询: {response.enhanced_query}")
    print(f"置信度: {response.confidence:.2%}")
    
    print(f"\n上下文信息:")
    print(f"  项目路径: {response.context.project_path}")
    if response.context.current_file:
        print(f"  当前文件: {Path(response.context.current_file).relative_to(args.path)}")
    if response.context.current_function:
        print(f"  当前函数: {response.context.current_function}")
    if response.context.current_class:
        print(f"  当前类: {response.context.current_class}")
    if response.context.git_branch:
        print(f"  Git 分支: {response.context.git_branch}")
    if response.context.user_role:
        print(f"  用户角色: {response.context.user_role}")
    
    if response.suggested_knowledge:
        print(f"\n建议知识 ({len(response.suggested_knowledge)}):")
        for i, knowledge in enumerate(response.suggested_knowledge, 1):
            print(f"  {i}. {knowledge}")
    
    if response.suggested_resources:
        print(f"\n建议资源 ({len(response.suggested_resources)}):")
        for i, resource in enumerate(response.suggested_resources, 1):
            print(f"  {i}. {resource}")
    
    # 导出 JSON
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(asdict(response), f, indent=2, ensure_ascii=False)
        print(f"\n结果已保存到: {args.output}")


if __name__ == "__main__":
    main()
