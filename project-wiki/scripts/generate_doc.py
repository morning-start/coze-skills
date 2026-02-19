#!/usr/bin/env python3
"""
智能文档生成器
功能：根据模板和代码上下文生成符合规范的文档
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, Optional, List


class DocumentGenerator:
    """文档生成器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.templates_path = Path(__file__).parent.parent / "references" / "templates"
        self.project_info = self._load_project_info()
    
    def _load_project_info(self) -> Dict:
        """加载项目分析信息"""
        analysis_file = self.project_path / "project-analysis.json"
        if analysis_file.exists():
            with open(analysis_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _get_template(self, doc_type: str) -> Optional[str]:
        """获取模板内容"""
        template_map = {
            'api': 'api-template.md',
            'module': 'module-template.md',
            'service': 'service-template.md'
        }
        
        template_name = template_map.get(doc_type)
        if not template_name:
            return None
        
        template_path = self.templates_path / template_name
        if not template_path.exists():
            return None
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _extract_code_context(self, target: str) -> Dict:
        """提取代码上下文"""
        # 这里可以调用 extract_docs.py 或其他脚本
        # 简化实现，返回基本结构
        return {
            'functions': [],
            'classes': [],
            'apis': []
        }
    
    def _fill_template(self, template: str, context: Dict) -> str:
        """填充模板"""
        result = template
        
        # 替换占位符
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        
        return result
    
    def generate(self, doc_type: str, name: str, output_path: Optional[str] = None) -> str:
        """生成文档"""
        
        print(f"生成文档: {doc_type} - {name}")
        
        # 获取模板
        template = self._get_template(doc_type)
        if not template:
            raise ValueError(f"不支持的文档类型: {doc_type}")
        
        # 提取代码上下文
        code_context = self._extract_code_context(name)
        
        # 构建上下文
        context = {
            'name': name,
            'service_name': name,
            'module_name': name,
            'api_name': name,
            'version': '1.0.0',
            'date': '2024-02-19',
            'path': f'/api/v1/{name.lower()}',
            'method': 'POST',
            'base_url': 'http://localhost:8080',
            'token': 'YOUR_TOKEN_HERE',
            'request_body': '{\n  "param1": "value1"\n}',
            'success_message': '操作成功',
            'response_data': '{\n    "id": 123,\n    "name": "示例数据"\n  }',
            'field_name': 'example_field',
            'type': 'string',
            'required': '是',
            'description': '示例字段',
            'example': 'example_value',
            'default': 'default_value',
            'param': 'param1',
            'path_param': 'id',
            'query_param': 'page',
            'body_param': 'data',
            'function_name': 'example_function',
            'function_description': '示例函数',
            'component': 'ExampleComponent',
            'dependencies': '依赖A, 依赖B',
            'responsibility_1': '职责 1',
            'responsibility_2': '职责 2',
            'responsibility_3': '职责 3',
            'module_path': f'src/modules/{name.lower()}',
            'model_name': 'ExampleModel',
            'field1': 'field1',
            'field2': 'field2',
            'value1': 'value1',
            'value2': 'value2',
            'env_var': 'SERVICE_PORT',
            'port': '8080',
            'mode': 'production',
            'db_host': 'localhost',
            'db_port': '5432',
            'db_name': 'database',
            'pool_size': '10',
            'redis_host': 'localhost',
            'redis_port': '6379',
            'ttl': '300',
            'log_level': 'INFO',
            'log_output': 'stdout',
            'db_secret': 'db-secret',
            'description': '示例描述',
            'best_practice_1': '最佳实践 1',
            'best_practice_2': '最佳实践 2',
            'best_practice_3': '最佳实践 3',
            'question_1': '问题 1',
            'answer_1': '答案 1',
            'question_2': '问题 2',
            'answer_2': '答案 2',
            'endpoint_1': '获取列表',
            'endpoint_2': '创建资源',
            'endpoint_3': '更新资源',
            'endpoint_4': '删除资源',
            'cache_strategy': 'Redis 缓存',
            'batch_processing': '支持批量操作',
            'async_processing': '支持异步处理',
            'exception': 'ExampleException',
            'condition': '条件描述',
            'handler': '处理方式',
            'note_1': '注意事项 1',
            'note_2': '注意事项 2',
            'note_3': '注意事项 3',
            'rule_1': '业务规则 1',
            'rule_2': '业务规则 2',
            'rule_3': '业务规则 3',
        }
        
        # 填充模板
        content = self._fill_template(template, context)
        
        # 保存文档
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"文档已生成: {output_file}")
        
        return content


def main():
    parser = argparse.ArgumentParser(description='智能文档生成器')
    parser.add_argument('--path', type=str, default='.', help='项目路径')
    parser.add_argument('--type', type=str, required=True,
                        choices=['api', 'module', 'service'],
                        help='文档类型（api/module/service）')
    parser.add_argument('--name', type=str, required=True, help='文档名称')
    parser.add_argument('--output', type=str, help='输出文件路径')
    
    args = parser.parse_args()
    
    generator = DocumentGenerator(args.path)
    content = generator.generate(args.type, args.name, args.output)
    
    if not args.output:
        print("\n" + "="*80)
        print("生成的文档内容:")
        print("="*80)
        print(content)


if __name__ == '__main__':
    main()
