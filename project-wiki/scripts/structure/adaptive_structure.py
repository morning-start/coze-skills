#!/usr/bin/env python3
"""
自适应结构生成器

根据项目复杂度自动生成合适的目录结构
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class StructureConfig:
    """结构配置"""
    structure_type: str  # flat, typed, domain, layered, microservice, nested
    directories: List[Dict]
    file_templates: List[Dict]
    nesting_rules: Dict


class AdaptiveStructureGenerator:
    """自适应结构生成器"""
    
    # 结构类型定义
    STRUCTURE_TYPES = {
        'flat': {
            'description': '扁平结构 - 适用于简单项目',
            'max_modules': 5,
            'max_files': 20
        },
        'typed': {
            'description': '按类型分组 - 适用于中等项目',
            'max_modules': 20,
            'max_files': 100
        },
        'domain': {
            'description': '按领域分组 - 适用于复杂项目',
            'max_modules': 50,
            'max_files': 500
        },
        'layered': {
            'description': '分层结构 - 适用于多层架构项目',
            'max_modules': 30,
            'max_files': 200
        },
        'microservice': {
            'description': '微服务结构 - 适用于微服务架构',
            'max_modules': 100,
            'max_files': 1000
        },
        'nested': {
            'description': '多层嵌套 - 适用于超复杂项目',
            'max_modules': 500,
            'max_files': 5000
        }
    }
    
    def __init__(self, project_path: str, complexity_level: str = None, metrics: Dict = None):
        self.project_path = Path(project_path)
        self.complexity_level = complexity_level
        self.metrics = metrics or {}
    
    def generate_structure(self, structure_type: str = None) -> StructureConfig:
        """生成结构配置"""
        # 如果没有指定结构类型，根据复杂度自动选择
        if not structure_type:
            structure_type = self._auto_select_structure()
        
        # 生成目录结构
        directories = self._generate_directories(structure_type)
        
        # 生成文件模板
        file_templates = self._generate_file_templates(structure_type)
        
        # 生成嵌套规则
        nesting_rules = self._generate_nesting_rules(structure_type)
        
        return StructureConfig(
            structure_type=structure_type,
            directories=directories,
            file_templates=file_templates,
            nesting_rules=nesting_rules
        )
    
    def _auto_select_structure(self) -> str:
        """自动选择结构类型"""
        if self.complexity_level == 'simple':
            return 'flat'
        elif self.complexity_level == 'medium':
            # 如果有多个服务，使用微服务结构
            if self.metrics.get('service_count', 0) >= 5:
                return 'microservice'
            # 如果有多层架构，使用分层结构
            elif self.metrics.get('layer_count', 0) >= 4:
                return 'layered'
            else:
                return 'typed'
        elif self.complexity_level == 'complex':
            # 如果有很多服务，使用微服务结构
            if self.metrics.get('service_count', 0) >= 10:
                return 'microservice'
            else:
                return 'domain'
        elif self.complexity_level == 'ultra-complex':
            return 'nested'
        else:
            return 'typed'
    
    def _generate_directories(self, structure_type: str) -> List[Dict]:
        """生成目录结构"""
        directories = []
        
        if structure_type == 'flat':
            # 扁平结构
            directories = [
                {'name': 'wiki', 'description': 'Wiki 根目录'},
                {'name': 'wiki/api-docs', 'description': 'API 文档'},
                {'name': 'wiki/modules', 'description': '模块文档'},
                {'name': 'wiki/assets', 'description': '资源文件'}
            ]
        
        elif structure_type == 'typed':
            # 按类型分组
            directories = [
                {'name': 'wiki', 'description': 'Wiki 根目录'},
                {'name': 'wiki/01-架构文档', 'description': '架构设计文档'},
                {'name': 'wiki/02-开发指南', 'description': '开发指南'},
                {'name': 'wiki/03-API文档', 'description': 'API 文档'},
                {'name': 'wiki/04-模块文档', 'description': '模块文档'},
                {'name': 'wiki/05-测试文档', 'description': '测试文档'},
                {'name': 'wiki/06-参考文档', 'description': '参考文档'}
            ]
        
        elif structure_type == 'domain':
            # 按领域分组
            domains = self._identify_domains()
            directories = [
                {'name': 'wiki', 'description': 'Wiki 根目录'},
                {'name': 'wiki/shared', 'description': '共享文档'},
            ]
            
            # 为每个领域创建目录
            for domain in domains:
                directories.append({
                    'name': f'wiki/{domain}',
                    'description': f'{domain} 领域文档'
                })
                directories.append({
                    'name': f'wiki/{domain}/architecture',
                    'description': f'{domain} 架构文档'
                })
                directories.append({
                    'name': f'wiki/{domain}/api',
                    'description': f'{domain} API 文档'
                })
                directories.append({
                    'name': f'wiki/{domain}/modules',
                    'description': f'{domain} 模块文档'
                })
        
        elif structure_type == 'layered':
            # 分层结构
            directories = [
                {'name': 'wiki', 'description': 'Wiki 根目录'},
                {'name': 'wiki/presentation', 'description': '表现层文档'},
                {'name': 'wiki/business', 'description': '业务层文档'},
                {'name': 'wiki/persistence', 'description': '持久层文档'},
                {'name': 'wiki/infrastructure', 'description': '基础设施文档'},
                {'name': 'wiki/cross-cutting', 'description': '横切关注点文档'}
            ]
        
        elif structure_type == 'microservice':
            # 微服务结构
            services = self._identify_services()
            directories = [
                {'name': 'wiki', 'description': 'Wiki 根目录'},
                {'name': 'wiki/gateway', 'description': 'API 网关文档'},
                {'name': 'wiki/shared', 'description': '共享服务文档'},
            ]
            
            # 为每个服务创建目录
            for service in services:
                directories.append({
                    'name': f'wiki/services/{service}',
                    'description': f'{service} 服务文档'
                })
                directories.append({
                    'name': f'wiki/services/{service}/api',
                    'description': f'{service} API 文档'
                })
                directories.append({
                    'name': f'wiki/services/{service}/architecture',
                    'description': f'{service} 架构文档'
                })
        
        elif structure_type == 'nested':
            # 多层嵌套结构
            domains = self._identify_domains()
            directories = [
                {'name': 'wiki', 'description': 'Wiki 根目录'},
            ]
            
            # 多层嵌套：domain/service/module/docs
            for domain in domains:
                services = self._identify_services_in_domain(domain)
                for service in services:
                    modules = self._identify_modules_in_service(service)
                    for module in modules:
                        directories.append({
                            'name': f'wiki/{domain}/{service}/{module}/docs',
                            'description': f'{module} 文档'
                        })
                        directories.append({
                            'name': f'wiki/{domain}/{service}/{module}/docs/api',
                            'description': f'{module} API 文档'
                        })
                        directories.append({
                            'name': f'wiki/{domain}/{service}/{module}/docs/design',
                            'description': f'{module} 设计文档'
                        })
        
        return directories
    
    def _generate_file_templates(self, structure_type: str) -> List[Dict]:
        """生成文件模板"""
        templates = []
        
        # 通用文件
        common_templates = [
            {'path': 'README.md', 'description': '项目说明', 'template': 'readme'},
            {'path': 'CHANGELOG.md', 'description': '变更日志', 'template': 'changelog'},
            {'path': 'ROADMAP.md', 'description': '路线图', 'template': 'roadmap'}
        ]
        
        if structure_type == 'flat':
            # 扁平结构文件
            templates = common_templates + [
                {'path': 'wiki/api-docs/README.md', 'description': 'API 文档索引', 'template': 'api-index'},
                {'path': 'wiki/modules/README.md', 'description': '模块文档索引', 'template': 'module-index'}
            ]
        
        elif structure_type == 'typed':
            # 按类型分组文件
            templates = common_templates + [
                {'path': 'wiki/01-架构文档/README.md', 'description': '架构文档索引', 'template': 'architecture-index'},
                {'path': 'wiki/03-API文档/README.md', 'description': 'API 文档索引', 'template': 'api-index'},
                {'path': 'wiki/04-模块文档/README.md', 'description': '模块文档索引', 'template': 'module-index'}
            ]
        
        elif structure_type in ['domain', 'microservice']:
            # 领域/微服务文件
            templates = common_templates + [
                {'path': 'wiki/shared/README.md', 'description': '共享文档索引', 'template': 'shared-index'},
            ]
        
        elif structure_type == 'layered':
            # 分层结构文件
            templates = common_templates + [
                {'path': 'wiki/presentation/README.md', 'description': '表现层文档索引', 'template': 'layer-index'},
                {'path': 'wiki/business/README.md', 'description': '业务层文档索引', 'template': 'layer-index'},
                {'path': 'wiki/persistence/README.md', 'description': '持久层文档索引', 'template': 'layer-index'},
            ]
        
        elif structure_type == 'nested':
            # 嵌套结构文件
            templates = common_templates
        
        return templates
    
    def _generate_nesting_rules(self, structure_type: str) -> Dict:
        """生成嵌套规则"""
        rules = {
            'max_nesting_depth': 1,
            'naming_convention': 'flat',
            'index_files': True,
            'cross_references': False
        }
        
        if structure_type == 'flat':
            rules.update({
                'max_nesting_depth': 1,
                'naming_convention': 'flat',
                'index_files': False,
                'cross_references': False
            })
        
        elif structure_type == 'typed':
            rules.update({
                'max_nesting_depth': 2,
                'naming_convention': 'numbered',
                'index_files': True,
                'cross_references': True
            })
        
        elif structure_type in ['domain', 'microservice']:
            rules.update({
                'max_nesting_depth': 3,
                'naming_convention': 'named',
                'index_files': True,
                'cross_references': True
            })
        
        elif structure_type == 'nested':
            rules.update({
                'max_nesting_depth': 5,
                'naming_convention': 'hierarchical',
                'index_files': True,
                'cross_references': True
            })
        
        return rules
    
    def _identify_domains(self) -> List[str]:
        """识别业务领域"""
        # 常见领域名称
        common_domains = [
            'user', 'order', 'payment', 'product', 'inventory',
            'shipping', 'notification', 'report', 'analytics', 'admin'
        ]
        
        # 扫描项目目录，识别领域
        detected_domains = set()
        project_path = self.project_path
        
        for item in project_path.iterdir():
            if item.is_dir():
                domain_name = item.name.lower()
                for domain in common_domains:
                    if domain in domain_name:
                        detected_domains.add(domain)
                        break
        
        # 如果没有检测到领域，使用默认领域
        if not detected_domains:
            detected_domains = ['core', 'business', 'support']
        
        return sorted(list(detected_domains))
    
    def _identify_services(self) -> List[str]:
        """识别服务"""
        services = []
        project_path = self.project_path
        
        for item in project_path.iterdir():
            if item.is_dir():
                # 检查是否是服务目录
                service_indicators = ['service', 'microservice', 'ms-', 'svc-']
                if any(indicator in item.name.lower() for indicator in service_indicators):
                    services.append(item.name)
                # 检查是否有服务配置文件
                elif (item / 'docker-compose.yml').exists() or (item / 'Dockerfile').exists():
                    services.append(item.name)
        
        # 如果没有检测到服务，返回默认服务列表
        if not services:
            services = ['gateway', 'user-service', 'order-service']
        
        return sorted(services)
    
    def _identify_services_in_domain(self, domain: str) -> List[str]:
        """识别领域内的服务"""
        # 这里简化处理，实际应该扫描 domain 目录
        return [f'{domain}-service']
    
    def _identify_modules_in_service(self, service: str) -> List[str]:
        """识别服务内的模块"""
        # 这里简化处理，实际应该扫描 service 目录
        return ['api', 'core', 'model']
    
    def create_structure(self, config: StructureConfig, output_path: str = None):
        """创建目录结构"""
        if output_path is None:
            output_path = self.project_path / 'wiki'
        else:
            output_path = Path(output_path)
        
        # 创建目录
        for directory in config.directories:
            dir_path = output_path / directory['name']
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ 创建目录: {dir_path}")
        
        # 创建文件（可选）
        for template in config.file_templates:
            file_path = output_path / template['path']
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 创建占位符文件
            if not file_path.exists():
                file_path.write_text(f"# {template['description']}\n\n待填充...\n")
                print(f"✓ 创建文件: {file_path}")
    
    def export_config(self, config: StructureConfig, output_path: str):
        """导出配置"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(config), f, indent=2, ensure_ascii=False)
        print(f"✓ 配置已导出到: {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="自适应结构生成器")
    parser.add_argument("--path", required=True, help="项目路径")
    parser.add_argument("--structure-type", help="结构类型（flat/typed/domain/layered/microservice/nested）")
    parser.add_argument("--complexity", help="复杂度等级（simple/medium/complex/ultra-complex）")
    parser.add_argument("--output", help="输出路径", default="wiki")
    parser.add_argument("--export", help="导出配置文件")
    
    args = parser.parse_args()
    
    # 生成结构
    generator = AdaptiveStructureGenerator(args.path, args.complexity)
    config = generator.generate_structure(args.structure_type)
    
    # 创建目录
    generator.create_structure(config, args.output)
    
    # 导出配置
    if args.export:
        generator.export_config(config, args.export)
    
    # 输出信息
    print(f"\n{'='*60}")
    print(f"结构类型: {config.structure_type}")
    print(f"描述: {AdaptiveStructureGenerator.STRUCTURE_TYPES[config.structure_type]['description']}")
    print(f"{'='*60}")
    print(f"目录数量: {len(config.directories)}")
    print(f"文件模板: {len(config.file_templates)}")
    print(f"最大嵌套深度: {config.nesting_rules['max_nesting_depth']}")


if __name__ == "__main__":
    main()
