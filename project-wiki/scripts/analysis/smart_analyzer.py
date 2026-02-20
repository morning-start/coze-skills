#!/usr/bin/env python3
"""
智能分析器 - ProjectWiki 智能决策引擎

功能：
1. 自动检测项目类型和技术栈
2. 自动推荐文档类型和模板
3. 自动补充缺失的知识
4. 自动生成优化建议
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class SmartAnalyzer:
    """智能分析器"""
    
    # 支持的框架映射
    FRAMEWORK_PATTERNS = {
        'backend': {
            'django': ['manage.py', 'settings.py', 'urls.py'],
            'flask': ['app.py', 'requirements.txt'],
            'fastapi': ['main.py', 'dependencies.py'],
            'spring-boot': ['pom.xml', 'application.properties'],
            'gin': ['go.mod', 'main.go']
        },
        'frontend': {
            'react': ['package.json', 'src/App.js', 'public/index.html'],
            'vue': ['package.json', 'src/main.js', 'vue.config.js'],
            'svelte': ['package.json', 'src/App.svelte'],
            'solidjs': ['package.json', 'src/App.jsx']
        },
        'cross-platform': {
            'flutter': ['pubspec.yaml', 'lib/main.dart'],
            'electron': ['package.json', 'main.js', 'renderer/index.html'],
            'tauri': ['src-tauri/tauri.conf.json', 'package.json'],
            'wails': ['wails.json', 'main.go']
        }
    }
    
    # 文档类型推荐映射
    DOC_TYPE_RECOMMENDATIONS = {
        'django': ['api', 'module', 'architecture', 'data-flow'],
        'flask': ['api', 'module', 'service'],
        'fastapi': ['api', 'module', 'data-flow'],
        'react': ['functional', 'module', 'architecture'],
        'vue': ['functional', 'module', 'architecture'],
        'flutter': ['functional', 'module', 'architecture'],
    }
    
    # 角色推荐映射
    ROLE_RECOMMENDATIONS = {
        'api': ['developer', 'tester'],
        'module': ['developer', 'architect'],
        'architecture': ['architect'],
        'data-flow': ['architect', 'developer'],
        'functional': ['product', 'developer'],
    }
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.analysis_result = {
            'project_type': None,
            'frameworks': [],
            'complexity': 'medium',
            'recommended_docs': [],
            'recommended_roles': [],
            'missing_knowledge': [],
            'optimization_suggestions': []
        }
    
    def detect_framework(self) -> Optional[str]:
        """检测项目框架"""
        files = []
        if self.project_path.exists():
            for root, _, filenames in os.walk(self.project_path):
                for filename in filenames:
                    files.append(filename)
        
        detected = []
        for category, frameworks in self.FRAMEWORK_PATTERNS.items():
            for framework, patterns in frameworks.items():
                match_count = sum(1 for pattern in patterns if pattern in files)
                if match_count >= len(patterns) * 0.5:
                    detected.append(framework)
        
        return detected[0] if detected else None
    
    def estimate_complexity(self) -> str:
        """评估项目复杂度"""
        if not self.project_path.exists():
            return 'medium'
        
        # 统计文件数量
        file_count = sum(1 for _ in self.project_path.rglob('*') if _.is_file())
        
        # 统计目录层级
        max_depth = 0
        for path in self.project_path.rglob('*'):
            depth = len(path.relative_to(self.project_path).parts)
            max_depth = max(max_depth, depth)
        
        # 评估复杂度
        if file_count < 50 and max_depth < 4:
            return 'simple'
        elif file_count < 200 and max_depth < 6:
            return 'medium'
        else:
            return 'complex'
    
    def recommend_docs(self, framework: str) -> List[str]:
        """推荐文档类型"""
        if framework in self.DOC_TYPE_RECOMMENDATIONS:
            return self.DOC_TYPE_RECOMMENDATIONS[framework]
        return ['api', 'module', 'architecture']
    
    def recommend_roles(self, doc_types: List[str]) -> List[str]:
        """推荐角色"""
        roles = set()
        for doc_type in doc_types:
            if doc_type in self.ROLE_RECOMMENDATIONS:
                roles.update(self.ROLE_RECOMMENDATIONS[doc_type])
        return list(roles)
    
    def generate_suggestions(self) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        framework = self.analysis_result['frameworks'][0] if self.analysis_result['frameworks'] else 'generic'
        complexity = self.analysis_result['complexity']
        
        # 根据复杂度提供建议
        if complexity == 'simple':
            suggestions.append("项目结构简单，建议使用渐进式文档：功能文档 → 需求文档")
        elif complexity == 'medium':
            suggestions.append("项目复杂度中等，建议创建完整文档链：功能 → 需求 → 架构")
        else:
            suggestions.append("项目复杂度高，建议使用自适应结构和多角色视图")
        
        # 根据框架提供建议
        if framework in ['django', 'flask', 'fastapi']:
            suggestions.append(f"检测到 {framework} 框架，建议重点关注 API 文档和数据流动设计")
        elif framework in ['react', 'vue']:
            suggestions.append(f"检测到 {framework} 框架，建议重点关注模块文档和状态管理")
        
        # 通用建议
        suggestions.append("建议使用知识搜索功能补充技术栈知识")
        suggestions.append("建议创建状态机图展示关键业务流程")
        
        return suggestions
    
    def analyze(self) -> Dict:
        """执行完整分析"""
        # 检测框架
        frameworks = self.detect_framework()
        self.analysis_result['frameworks'] = frameworks if frameworks else ['generic']
        
        # 评估复杂度
        self.analysis_result['complexity'] = self.estimate_complexity()
        
        # 推荐文档
        framework = self.analysis_result['frameworks'][0]
        self.analysis_result['recommended_docs'] = self.recommend_docs(framework)
        
        # 推荐角色
        self.analysis_result['recommended_roles'] = self.recommend_roles(
            self.analysis_result['recommended_docs']
        )
        
        # 生成建议
        self.analysis_result['optimization_suggestions'] = self.generate_suggestions()
        
        return self.analysis_result
    
    def print_report(self):
        """打印分析报告"""
        print("=" * 60)
        print("ProjectWiki 智能分析报告")
        print("=" * 60)
        
        print(f"\n📊 项目分析:")
        print(f"  框架: {', '.join(self.analysis_result['frameworks'])}")
        print(f"  复杂度: {self.analysis_result['complexity']}")
        
        print(f"\n📝 推荐文档类型:")
        for doc_type in self.analysis_result['recommended_docs']:
            print(f"  - {doc_type}")
        
        print(f"\n👥 推荐角色视图:")
        for role in self.analysis_result['recommended_roles']:
            print(f"  - {role}")
        
        print(f"\n💡 优化建议:")
        for i, suggestion in enumerate(self.analysis_result['optimization_suggestions'], 1):
            print(f"  {i}. {suggestion}")
        
        print("\n" + "=" * 60)
        print("✅ 智能分析完成")
        print("=" * 60)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 smart_analyzer.py <项目路径>")
        print("示例: python3 smart_analyzer.py ./my-project")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    analyzer = SmartAnalyzer(project_path)
    result = analyzer.analyze()
    
    # 打印报告
    analyzer.print_report()
    
    # 可选：保存结果
    if len(sys.argv) > 2 and sys.argv[2] == '--save':
        output_file = 'smart-analysis-result.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n📄 分析结果已保存到: {output_file}")


if __name__ == '__main__':
    main()
