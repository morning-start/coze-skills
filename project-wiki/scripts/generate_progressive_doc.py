#!/usr/bin/env python3
"""
渐进式文档生成器

根据上一级文档生成下一级文档：
- 功能文档 → 需求文档
- 需求文档 → 架构文档
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class DocumentMetadata:
    """文档元数据"""
    doc_type: str  # functional, requirement, architecture
    name: str
    source: Optional[str]
    created_at: str
    status: str


class ProgressiveDocGenerator:
    """渐进式文档生成器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.templates_path = self.project_path / 'references' / 'templates'
        self.functional_docs_path = self.project_path / 'functional-docs'
        self.requirement_docs_path = self.project_path / 'requirement-docs'
        self.architecture_docs_path = self.project_path / 'architecture-docs'
    
    def generate(self, doc_type: str, source: str, output: str = None) -> str:
        """生成文档
        
        Args:
            doc_type: 文档类型（requirement, architecture）
            source: 源文档路径
            output: 输出路径（可选）
        
        Returns:
            生成文档的路径
        """
        # 确定源文档类型和目标文档类型
        if doc_type == 'requirement':
            source_type = 'functional'
            target_type = 'requirement'
            template_file = 'requirement-doc-template.md'
        elif doc_type == 'architecture':
            source_type = 'requirement'
            target_type = 'architecture'
            template_file = 'architecture-doc-template.md'
        else:
            raise ValueError(f"不支持的文档类型: {doc_type}")
        
        # 读取源文档
        source_path = Path(source)
        if not source_path.exists():
            raise FileNotFoundError(f"源文档不存在: {source}")
        
        source_content = source_path.read_text(encoding='utf-8', errors='ignore')
        
        # 读取模板
        template_path = self.templates_path / template_file
        if not template_path.exists():
            raise FileNotFoundError(f"模板不存在: {template_path}")
        
        template_content = template_path.read_text(encoding='utf-8')
        
        # 提取源文档信息
        source_info = self._extract_source_info(source_content, source_path)
        
        # 填充模板
        generated_content = self._fill_template(template_content, source_info, source, target_type)
        
        # 确定输出路径
        if output is None:
            output = self._generate_output_path(doc_type, source_info['name'])
        else:
            output = Path(output)
        
        # 创建输出目录
        output.parent.mkdir(parents=True, exist_ok=True)
        
        # 写入文档
        output.write_text(generated_content, encoding='utf-8')
        
        return str(output)
    
    def _extract_source_info(self, content: str, source_path: Path) -> Dict:
        """从源文档中提取信息"""
        # 优先从文件路径提取名称
        base_name = source_path.stem.replace('-需求', '').replace('-架构', '')
        info = {
            'name': base_name,
            'description': '',
            'background': '',
            'target_users': '',
            'value': '',
            'scenarios': '',
            'priority': '',
            'expected_outcomes': '',
            'related_features': '',
            'intent': '',
            'key_points': '',
            'summary': ''
        }
        
        # 如果路径提取的名称为空或包含模板，从内容中提取
        if not base_name or '模板' in base_name:
            # 从内容中提取标题
            skip_titles = ['功能文档模板', '需求文档模板', '架构文档模板', '使用说明']
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                name = title_match.group(1).strip()
                # 如果是模板标题，查找第二个一级标题
                if name in skip_titles or '模板' in name:
                    lines = content.split('\n')
                    for line in lines[1:]:  # 跳过第一个
                        if line.startswith('# '):
                            name = line[2:].strip()
                            if name not in skip_titles:
                                break
                # 移除后缀
                name = name.replace('-需求', '').replace('-架构', '')
                info['name'] = name
        
        # 提取功能描述
        desc_match = re.search(r'## 功能描述\s*\n(.*?)\s*##', content, re.DOTALL)
        if desc_match:
            info['description'] = desc_match.group(1).strip()
        
        # 提取功能背景
        bg_match = re.search(r'## 功能背景\s*\n(.*?)\s*##', content, re.DOTALL)
        if bg_match:
            info['background'] = bg_match.group(1).strip()
        
        # 提取目标用户
        users_match = re.search(r'## 目标用户\s*\n(.*?)\s*##', content, re.DOTALL)
        if users_match:
            info['target_users'] = users_match.group(1).strip()
        
        # 提取功能价值
        value_match = re.search(r'## 功能价值\s*\n(.*?)\s*##', content, re.DOTALL)
        if value_match:
            info['value'] = value_match.group(1).strip()
        
        # 提取用户场景
        scenarios_match = re.search(r'## 用户场景\s*\n(.*?)\s*##', content, re.DOTALL)
        if scenarios_match:
            info['scenarios'] = scenarios_match.group(1).strip()
        
        # 提取预期成果
        outcomes_match = re.search(r'## 预期成果\s*\n(.*?)\s*##', content, re.DOTALL)
        if outcomes_match:
            info['expected_outcomes'] = outcomes_match.group(1).strip()
        
        # 提取相关功能
        related_match = re.search(r'## 相关功能\s*\n(.*?)\s*##', content, re.DOTALL)
        if related_match:
            info['related_features'] = related_match.group(1).strip()
        
        # 如果是功能文档，提取智能推断结果
        intent_match = re.search(r'### 意图识别\s*\n(.*?)\s*###', content, re.DOTALL)
        if intent_match:
            info['intent'] = intent_match.group(1).strip()
        
        key_points_match = re.search(r'### 关键信息提取\s*\n(.*?)\s*###', content, re.DOTALL)
        if key_points_match:
            info['key_points'] = key_points_match.group(1).strip()
        
        summary_match = re.search(r'### 功能总结\s*\n(.*?)\s*###', content, re.DOTALL)
        if summary_match:
            info['summary'] = summary_match.group(1).strip()
        
        return info
    
    def _fill_template(self, template: str, source_info: Dict, source_path: str, target_type: str) -> str:
        """填充模板"""
        from datetime import datetime
        
        # 替换占位符
        content = template
        
        # 替换文档名称
        content = content.replace('[需求名称]', source_info['name'] + '-需求')
        content = content.replace('[架构名称]', source_info['name'] + '-架构')
        content = content.replace('[功能名称]', source_info['name'])
        
        # 替换源文档引用
        relative_source = str(Path(source_path).relative_to(self.project_path))
        content = content.replace('[功能文档路径]', relative_source)
        content = content.replace('[需求文档路径]', relative_source)
        
        # 替换内容占位符
        content = content.replace('[用户对功能的详细描述，自由文本]', source_info.get('description', ''))
        content = content.replace('[功能的业务背景和使用场景]', source_info.get('background', ''))
        content = content.replace('[功能的目标用户群体]', source_info.get('target_users', ''))
        content = content.replace('[功能带来的业务价值和收益]', source_info.get('value', ''))
        content = content.replace('[具体的使用场景描述]', source_info.get('scenarios', ''))
        content = content.replace('[功能完成后预期的成果和效果]', source_info.get('expected_outcomes', ''))
        content = content.replace('[与现有功能或其他需求的关系]', source_info.get('related_features', ''))
        
        # 替换意图分析
        content = content.replace('[基于功能文档分析]', '')
        content = content.replace('[基于功能文档的用户意图分析]', source_info.get('intent', ''))
        content = content.replace('[智能体识别的用户意图]', source_info.get('intent', ''))
        content = content.replace('[智能体提取的关键信息]', source_info.get('key_points', ''))
        content = content.replace('[智能体生成的结构化功能总结]', source_info.get('summary', ''))
        
        # 替换日期
        today = datetime.now().strftime('%Y-%m-%d')
        content = content.replace('[YYYY-MM-DD]', today)
        content = content.replace('[姓名]', '待填写')
        content = content.replace('[待填写]', '待填写')
        
        # 替换其他占位符
        replacements = {
            '[要解决的核心问题]': '待填写',
            '[技术解决方向]': '待填写',
            '[需求 1]': '待填写',
            '[需求 2]': '待填写',
            '[性能指标 1]': '待填写',
            '[性能指标 2]': '待填写',
            '[约束条件 1]': '待填写',
            '[约束条件 2]': '待填写',
        }
        
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        
        return content
    
    def _generate_output_path(self, doc_type: str, name: str) -> Path:
        """生成输出路径"""
        if doc_type == 'requirement':
            return self.requirement_docs_path / f"{name}-需求.md"
        elif doc_type == 'architecture':
            return self.architecture_docs_path / f"{name}-架构.md"
        else:
            raise ValueError(f"不支持的文档类型: {doc_type}")
    
    def validate_consistency(self, functional_path: str, requirement_path: str, architecture_path: str = None) -> Dict:
        """验证文档之间的一致性"""
        issues = []
        
        # 读取功能文档
        functional_content = Path(functional_path).read_text(encoding='utf-8', errors='ignore')
        
        # 读取需求文档
        requirement_content = Path(requirement_path).read_text(encoding='utf-8', errors='ignore')
        
        # 检查需求文档是否引用功能文档
        if '[功能文档路径]' in requirement_content or ('[功能文档' not in requirement_content and 'functional-docs' not in requirement_content):
            issues.append({
                'type': 'missing_reference',
                'level': 'warning',
                'message': '需求文档未正确引用功能文档'
            })
        
        # 如果有架构文档，检查是否引用需求文档
        if architecture_path and Path(architecture_path).exists():
            architecture_content = Path(architecture_path).read_text(encoding='utf-8', errors='ignore')
            
            if '[需求文档路径]' in architecture_content or ('[需求文档' not in architecture_content and 'requirement-docs' not in architecture_content):
                issues.append({
                    'type': 'missing_reference',
                    'level': 'warning',
                    'message': '架构文档未正确引用需求文档'
                })
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def list_documents(self, doc_type: str) -> List[str]:
        """列出指定类型的文档"""
        if doc_type == 'functional':
            path = self.functional_docs_path
        elif doc_type == 'requirement':
            path = self.requirement_docs_path
        elif doc_type == 'architecture':
            path = self.architecture_docs_path
        else:
            raise ValueError(f"不支持的文档类型: {doc_type}")
        
        if not path.exists():
            return []
        
        docs = list(path.glob('*.md'))
        return [str(d.relative_to(self.project_path)) for d in docs]
    
    def check_chain_completeness(self, functional_name: str) -> Dict:
        """检查文档链的完整性"""
        chain = {
            'functional': None,
            'requirement': None,
            'architecture': None,
            'complete': False
        }
        
        # 检查功能文档
        functional_path = self.functional_docs_path / f"{functional_name}.md"
        if functional_path.exists():
            chain['functional'] = str(functional_path.relative_to(self.project_path))
        
        # 检查需求文档
        requirement_path = self.requirement_docs_path / f"{functional_name}-需求.md"
        if requirement_path.exists():
            chain['requirement'] = str(requirement_path.relative_to(self.project_path))
        
        # 检查架构文档
        architecture_path = self.architecture_docs_path / f"{functional_name}-架构.md"
        if architecture_path.exists():
            chain['architecture'] = str(architecture_path.relative_to(self.project_path))
        
        # 判断完整性
        chain['complete'] = all([
            chain['functional'] is not None,
            chain['requirement'] is not None,
            chain['architecture'] is not None
        ])
        
        return chain


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="渐进式文档生成器")
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # generate 子命令
    gen_parser = subparsers.add_parser('generate', help='生成文档')
    gen_parser.add_argument("--type", required=True, choices=['requirement', 'architecture'], help="文档类型")
    gen_parser.add_argument("--source", required=True, help="源文档路径")
    gen_parser.add_argument("--output", help="输出路径")
    gen_parser.add_argument("--validate", action="store_true", help="验证文档一致性")
    
    # list 子命令
    list_parser = subparsers.add_parser('list', help='列出文档')
    list_parser.add_argument("--type", required=True, choices=['functional', 'requirement', 'architecture'], help="文档类型")
    
    # check-chain 子命令
    chain_parser = subparsers.add_parser('check-chain', help='检查文档链完整性')
    chain_parser.add_argument("--name", required=True, help="功能名称")
    
    args = parser.parse_args()
    
    generator = ProgressiveDocGenerator('.')
    
    # 列出文档
    if args.command == 'list':
        docs = generator.list_documents(args.type)
        print(f"\n{args.type} 文档列表:")
        if docs:
            for doc in docs:
                print(f"  - {doc}")
        else:
            print("  (无)")
        return
    
    # 检查文档链
    if args.command == 'check-chain':
        chain = generator.check_chain_completeness(args.name)
        print(f"\n文档链完整性检查: {args.name}")
        print(f"  功能文档: {'✓' if chain['functional'] else '✗'} {chain['functional'] or '不存在'}")
        print(f"  需求文档: {'✓' if chain['requirement'] else '✗'} {chain['requirement'] or '不存在'}")
        print(f"  架构文档: {'✓' if chain['architecture'] else '✗'} {chain['architecture'] or '不存在'}")
        print(f"  完整性: {'✓ 完整' if chain['complete'] else '✗ 不完整'}")
        return
    
    # 生成文档
    if args.command == 'generate':
        try:
            output_path = generator.generate(args.type, args.source, args.output)
            print(f"\n✓ {args.type} 文档已生成: {output_path}")

            # 验证一致性
            if args.validate:
                validation = {'valid': True, 'issues': []}
                
                if args.type == 'requirement':
                    validation = generator.validate_consistency(args.source, output_path)
                elif args.type == 'architecture':
                    # 需要传入需求文档路径
                    source_name = Path(args.source).stem
                    # 移除可能的 "-需求" 后缀
                    functional_name = source_name.replace('-需求', '').replace('-架构', '')
                    requirement_path = generator._generate_output_path('requirement', functional_name)
                    if requirement_path.exists():
                        validation = generator.validate_consistency(args.source, str(requirement_path), output_path)

                if validation['valid']:
                    print(f"\n✓ 文档一致性检查通过")
                else:
                    print(f"\n⚠ 发现 {len(validation['issues'])} 个问题:")
                    for issue in validation['issues']:
                        print(f"  - [{issue['level']}] {issue['message']}")

        except Exception as e:
            print(f"\n✗ 生成失败: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
