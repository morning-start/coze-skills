#!/usr/bin/env python3
"""
文档生命周期管理器 - ProjectWiki

功能：
1. 初始化文档生命周期
2. 更新文档状态
3. 记录状态变更
4. 生成生命周期报告
5. 检查过期文档
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class LifecycleManager:
    """文档生命周期管理器"""
    
    # 生命周期状态定义
    STATES = {
        'draft': {
            'name': 'Draft',
            'emoji': '🟡',
            'description': '草稿：文档初始创建阶段',
            'color': 'gray'
        },
        'review': {
            'name': 'Review',
            'emoji': '🟠',
            'description': '审核：文档审查阶段',
            'color': 'orange'
        },
        'published': {
            'name': 'Published',
            'emoji': '🟢',
            'description': '发布：文档已发布',
            'color': 'green'
        },
        'maintenance': {
            'name': 'Maintenance',
            'emoji': '🔵',
            'description': '维护：文档维护阶段',
            'color': 'blue'
        },
        'archived': {
            'name': 'Archived',
            'emoji': '🟣',
            'description': '归档：文档已归档',
            'color': 'purple'
        },
        'deprecated': {
            'name': 'Deprecated',
            'emoji': '🔴',
            'description': '废弃：文档已废弃',
            'color': 'red'
        }
    }
    
    # 状态转换规则
    TRANSITIONS = {
        'draft': ['review'],
        'review': ['draft', 'published'],
        'published': ['maintenance', 'archived'],
        'maintenance': ['published'],
        'archived': ['deprecated'],
        'deprecated': []
    }
    
    def __init__(self, workspace_path: str = '.'):
        self.workspace_path = Path(workspace_path)
        self.lifecycle_file = self.workspace_path / '.doc-lifecycle.json'
        self.lifecycle_data = self._load_lifecycle_data()
    
    def _load_lifecycle_data(self) -> Dict:
        """加载生命周期数据"""
        if self.lifecycle_file.exists():
            with open(self.lifecycle_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'documents': {}}
    
    def _save_lifecycle_data(self):
        """保存生命周期数据"""
        with open(self.lifecycle_file, 'w', encoding='utf-8') as f:
            json.dump(self.lifecycle_data, f, indent=2, ensure_ascii=False)
    
    def init_doc(self, doc_path: str, doc_name: str, author: str) -> Dict:
        """初始化文档生命周期"""
        doc_key = str(Path(doc_path).relative_to(self.workspace_path))
        
        if doc_key in self.lifecycle_data['documents']:
            print(f"⚠️  文档 {doc_key} 的生命周期已存在")
            return self.lifecycle_data['documents'][doc_key]
        
        # 创建生命周期记录
        lifecycle = {
            'name': doc_name,
            'path': doc_path,
            'status': 'draft',
            'version': 'v0.1.0',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'author': author,
            'reviewer': None,
            'owner': author,
            'state_history': [
                {
                    'date': datetime.now().isoformat(),
                    'from_state': None,
                    'to_state': 'draft',
                    'operator': author,
                    'reason': '创建文档'
                }
            ],
            'version_history': []
        }
        
        self.lifecycle_data['documents'][doc_key] = lifecycle
        self._save_lifecycle_data()
        
        print(f"✅ 文档 {doc_key} 的生命周期已初始化")
        print(f"   状态: 🟡 Draft")
        print(f"   版本: v0.1.0")
        
        return lifecycle
    
    def update_status(self, doc_path: str, new_status: str, operator: str, reason: str = '') -> bool:
        """更新文档状态"""
        doc_key = str(Path(doc_path).relative_to(self.workspace_path))
        
        if doc_key not in self.lifecycle_data['documents']:
            print(f"❌ 文档 {doc_key} 不存在，请先初始化")
            return False
        
        lifecycle = self.lifecycle_data['documents'][doc_key]
        current_status = lifecycle['status']
        
        # 检查状态转换是否合法
        if new_status not in self.TRANSITIONS[current_status]:
            print(f"❌ 无法从 {current_status} 转换到 {new_status}")
            print(f"   允许的转换: {', '.join(self.TRANSITIONS[current_status])}")
            return False
        
        if new_status not in self.STATES:
            print(f"❌ 无效的状态: {new_status}")
            return False
        
        # 更新状态
        lifecycle['status'] = new_status
        lifecycle['updated_at'] = datetime.now().isoformat()
        lifecycle['state_history'].append({
            'date': datetime.now().isoformat(),
            'from_state': current_status,
            'to_state': new_status,
            'operator': operator,
            'reason': reason
        })
        
        self._save_lifecycle_data()
        
        state_info = self.STATES[new_status]
        print(f"✅ 文档 {doc_key} 状态已更新")
        print(f"   从: {self.STATES[current_status]['emoji']} {self.STATES[current_status]['name']}")
        print(f"   到: {state_info['emoji']} {state_info['name']}")
        print(f"   操作人: {operator}")
        if reason:
            print(f"   原因: {reason}")
        
        return True
    
    def get_doc_lifecycle(self, doc_path: str) -> Optional[Dict]:
        """获取文档生命周期信息"""
        doc_key = str(Path(doc_path).relative_to(self.workspace_path))
        return self.lifecycle_data['documents'].get(doc_key)
    
    def report(self) -> Dict:
        """生成生命周期报告"""
        report = {
            'total_documents': len(self.lifecycle_data['documents']),
            'status_summary': {},
            'documents': []
        }
        
        # 统计各状态文档数量
        for status in self.STATES:
            count = sum(1 for doc in self.lifecycle_data['documents'].values() if doc['status'] == status)
            if count > 0:
                report['status_summary'][status] = {
                    'count': count,
                    'name': self.STATES[status]['name'],
                    'emoji': self.STATES[status]['emoji']
                }
        
        # 列出所有文档
        for doc_key, lifecycle in self.lifecycle_data['documents'].items():
            status_info = self.STATES[lifecycle['status']]
            report['documents'].append({
                'name': lifecycle['name'],
                'path': doc_key,
                'status': lifecycle['status'],
                'status_display': f"{status_info['emoji']} {status_info['name']}",
                'version': lifecycle['version'],
                'updated_at': lifecycle['updated_at'],
                'author': lifecycle['author']
            })
        
        return report
    
    def print_report(self):
        """打印生命周期报告"""
        report = self.report()
        
        print("=" * 60)
        print("文档生命周期报告")
        print("=" * 60)
        
        print(f"\n📊 总文档数: {report['total_documents']}")
        
        print(f"\n📈 状态分布:")
        for status, info in report['status_summary'].items():
            print(f"  {info['emoji']} {info['name']}: {info['count']}")
        
        print(f"\n📄 文档列表:")
        for doc in report['documents']:
            print(f"  {doc['status_display']} | {doc['name']} | {doc['version']} | {doc['author']}")
        
        print("\n" + "=" * 60)
    
    def check_expired(self, days: int = 90) -> List[Dict]:
        """检查过期文档（未更新的文档）"""
        expired_docs = []
        now = datetime.now()
        
        for doc_key, lifecycle in self.lifecycle_data['documents'].items():
            updated_at = datetime.fromisoformat(lifecycle['updated_at'])
            days_since_update = (now - updated_at).days
            
            if days_since_update > days and lifecycle['status'] not in ['archived', 'deprecated']:
                expired_docs.append({
                    'name': lifecycle['name'],
                    'path': doc_key,
                    'status': lifecycle['status'],
                    'days_since_update': days_since_update,
                    'updated_at': lifecycle['updated_at']
                })
        
        return expired_docs
    
    def print_expired(self, days: int = 90):
        """打印过期文档"""
        expired_docs = self.check_expired(days)
        
        if not expired_docs:
            print(f"✅ 没有超过 {days} 天未更新的文档")
            return
        
        print("=" * 60)
        print(f"⚠️  超过 {days} 天未更新的文档")
        print("=" * 60)
        
        for doc in expired_docs:
            status_info = self.STATES[doc['status']]
            print(f"\n{status_info['emoji']} {doc['name']}")
            print(f"  路径: {doc['path']}")
            print(f"  状态: {status_info['name']}")
            print(f"  未更新天数: {doc['days_since_update']} 天")
            print(f"  最后更新: {doc['updated_at']}")
        
        print("\n" + "=" * 60)
        print("💡 建议: 考虑更新或归档这些文档")
        print("=" * 60)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  初始化文档生命周期:")
        print("    python3 lifecycle_manager.py init <文档路径> --name <文档名称> --author <作者>")
        print()
        print("  更新文档状态:")
        print("    python3 lifecycle_manager.py update <文档路径> --status <状态> --operator <操作人> [--reason <原因>]")
        print()
        print("  生成生命周期报告:")
        print("    python3 lifecycle_manager.py report")
        print()
        print("  检查过期文档:")
        print("    python3 lifecycle_manager.py check-expired [--days <天数>]")
        print()
        print("示例:")
        print("  python3 lifecycle_manager.py init docs/api-doc.md --name 'API 文档' --author '张三'")
        print("  python3 lifecycle_manager.py update docs/api-doc.md --status published --operator '李四' --reason '审核通过'")
        print("  python3 lifecycle_manager.py report")
        print("  python3 lifecycle_manager.py check-expired --days 90")
        sys.exit(1)
    
    command = sys.argv[1]
    manager = LifecycleManager()
    
    if command == 'init':
        if len(sys.argv) < 6:
            print("❌ 缺少必要参数")
            sys.exit(1)
        
        doc_path = sys.argv[2]
        doc_name = ''
        author = ''
        
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == '--name' and i + 1 < len(sys.argv):
                doc_name = sys.argv[i + 1]
            elif sys.argv[i] == '--author' and i + 1 < len(sys.argv):
                author = sys.argv[i + 1]
        
        if not doc_name or not author:
            print("❌ 缺少必要参数: --name 和 --author")
            sys.exit(1)
        
        manager.init_doc(doc_path, doc_name, author)
    
    elif command == 'update':
        if len(sys.argv) < 6:
            print("❌ 缺少必要参数")
            sys.exit(1)
        
        doc_path = sys.argv[2]
        new_status = ''
        operator = ''
        reason = ''
        
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == '--status' and i + 1 < len(sys.argv):
                new_status = sys.argv[i + 1]
            elif sys.argv[i] == '--operator' and i + 1 < len(sys.argv):
                operator = sys.argv[i + 1]
            elif sys.argv[i] == '--reason' and i + 1 < len(sys.argv):
                reason = sys.argv[i + 1]
        
        if not new_status or not operator:
            print("❌ 缺少必要参数: --status 和 --operator")
            sys.exit(1)
        
        manager.update_status(doc_path, new_status, operator, reason)
    
    elif command == 'report':
        manager.print_report()
    
    elif command == 'check-expired':
        days = 90
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == '--days' and i + 1 < len(sys.argv):
                days = int(sys.argv[i + 1])
        
        manager.print_expired(days)
    
    else:
        print(f"❌ 未知命令: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
