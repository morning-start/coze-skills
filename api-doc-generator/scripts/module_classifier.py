#!/usr/bin/env python3
"""
Module Classifier - 基于路由路径自动划分模块和层级结构

功能：
1. 基于路由路径的第一段作为主模块
2. 识别深层路径作为子模块
3. 构建模块层级树结构
4. 生成模块分组信息

输入格式：
{
    "project_name": "项目名称",
    "framework": "flask",
    "apis": [
        {
            "path": "/users/{id}",
            "method": "GET",
            ...
        }
    ]
}

输出格式：
{
    "project_name": "项目名称",
    "modules": {
        "users": {
            "name": "users",
            "level": 1,
            "description": "用户管理模块",
            "endpoints": [
                {
                    "path": "/users",
                    "method": "GET",
                    ...
                }
            ],
            "submodules": {
                "orders": {
                    "name": "orders",
                    "level": 2,
                    "parent": "users",
                    "description": "订单管理子模块",
                    "endpoints": [...]
                }
            }
        }
    },
    "api_structure": {
        "users": ["/users", "/users/{id}", "/users/{id}/orders"],
        "orders": ["/orders", "/orders/{id}"]
    }
}
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List


class ModuleClassifier:
    def __init__(self, input_file: str):
        self.input_file = Path(input_file)
        self.data = None
        self.modules = {}
        self.api_structure = defaultdict(list)

    def load_data(self):
        """加载API扫描结果"""
        with open(self.input_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def extract_module_from_path(self, path: str) -> List[str]:
        """从路径中提取模块层级
        例如：/users/{id}/orders -> ["users", "orders"]
        """
        # 移除开头的斜杠和路径参数
        clean_path = path.strip("/")
        # 分割路径
        parts = [p for p in clean_path.split("/") if not p.startswith("{") and not p.startswith(":")]

        return parts

    def classify_modules(self):
        """根据API路径划分模块"""
        module_names_map = {
            "user": "users",
            "users": "users",
            "product": "products",
            "products": "products",
            "order": "orders",
            "orders": "orders",
            "auth": "authentication",
            "authentication": "authentication",
            "login": "authentication",
            "register": "authentication",
            "cart": "shopping-cart",
            "shopping-cart": "shopping-cart",
            "payment": "payments",
            "payments": "payments",
        }

        for api in self.data["apis"]:
            path = api["path"]
            module_parts = self.extract_module_from_path(path)

            if not module_parts:
                # 没有模块信息，归类为root
                module_name = "root"
            else:
                # 标准化模块名称
                raw_module = module_parts[0]
                module_name = module_names_map.get(raw_module, raw_module)

                # 记录API结构
                self.api_structure[module_name].append(path)

                # 如果有子模块，记录到子模块
                if len(module_parts) > 1:
                    submodule_name = module_parts[1]
                    full_submodule = f"{module_name}.{submodule_name}"
                    self.api_structure[full_submodule].append(path)

            # 添加到模块
            self._add_endpoint_to_module(module_name, api, level=1)

            # 如果有子模块，也添加到子模块
            if len(module_parts) > 1:
                submodule_name = module_parts[1]
                self._add_endpoint_to_module(
                    f"{module_name}.{submodule_name}",
                    api,
                    level=2,
                    parent=module_name
                )

    def _add_endpoint_to_module(self, module_key: str, api: Dict, level: int, parent: str = None):
        """添加端点到指定模块"""
        parts = module_key.split(".")

        if len(parts) == 1:
            # 主模块
            module_name = parts[0]
            if module_name not in self.modules:
                self.modules[module_name] = {
                    "name": module_name,
                    "level": level,
                    "description": f"{module_name}模块",
                    "endpoints": [],
                    "submodules": {}
                }
            self.modules[module_name]["endpoints"].append(api)
        else:
            # 子模块
            parent_name, submodule_name = parts[0], parts[1]

            if parent_name in self.modules:
                parent_module = self.modules[parent_name]
                if submodule_name not in parent_module["submodules"]:
                    parent_module["submodules"][submodule_name] = {
                        "name": submodule_name,
                        "level": level,
                        "parent": parent,
                        "description": f"{submodule_name}子模块",
                        "endpoints": []
                    }
                parent_module["submodules"][submodule_name]["endpoints"].append(api)

    def generate_module_descriptions(self):
        """为模块生成描述"""
        module_desc_templates = {
            "users": "用户管理模块，包括用户注册、登录、信息修改等功能",
            "products": "产品管理模块，包括产品列表、详情、搜索等功能",
            "orders": "订单管理模块，包括订单创建、查询、状态更新等功能",
            "authentication": "认证授权模块，包括登录、注册、权限验证等功能",
            "shopping-cart": "购物车模块，包括添加商品、删除商品、数量修改等功能",
            "payments": "支付模块，包括支付处理、退款、订单查询等功能",
            "admin": "后台管理模块，包括用户管理、系统配置等功能",
        }

        for module_name, module_data in self.modules.items():
            if module_name in module_desc_templates:
                module_data["description"] = module_desc_templates[module_name]

            # 为子模块生成描述
            for submodule_name, submodule_data in module_data["submodules"].items():
                if submodule_name in module_desc_templates:
                    submodule_data["description"] = module_desc_templates[submodule_name]

    def classify(self) -> Dict:
        """执行模块分类"""
        self.load_data()
        self.classify_modules()
        self.generate_module_descriptions()

        return {
            "project_name": self.data.get("project_name", ""),
            "framework": self.data.get("framework", ""),
            "total_modules": len(self.modules),
            "modules": self.modules,
            "api_structure": dict(self.api_structure)
        }


def main():
    parser = argparse.ArgumentParser(description="Classify APIs into modules and build hierarchy")
    parser.add_argument("--input", required=True, help="Input JSON file path from api_scanner")
    parser.add_argument("--output", default="api_modules.json", help="Output JSON file path")

    args = parser.parse_args()

    classifier = ModuleClassifier(args.input)
    result = classifier.classify()

    # 写入输出文件
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nClassified into {result['total_modules']} modules")
    print(f"Results saved to: {args.output}")

    # 打印模块结构
    print("\nModule Structure:")
    for module_name, module_data in result["modules"].items():
        print(f"  - {module_name} ({len(module_data['endpoints'])} endpoints)")
        for submodule_name, submodule_data in module_data["submodules"].items():
            print(f"    - {submodule_name} ({len(submodule_data['endpoints'])} endpoints)")


if __name__ == "__main__":
    main()
