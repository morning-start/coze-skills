#!/usr/bin/env python3
"""
API Scanner - 扫描项目代码，提取API路由和参数信息

支持的框架：
- Flask: @app.route, @bp.route
- FastAPI: @app.get, @app.post, @app.put, @app.delete, @app.patch
- Express: app.get, router.get, router.post, router.put, router.delete

输出格式：
{
    "project_name": "项目名称",
    "framework": "检测到的框架",
    "apis": [
        {
            "path": "/users/{id}",
            "method": "GET",
            "function": "get_user",
            "file": "routes/users.py",
            "line": 10,
            "description": "获取用户信息",
            "path_params": [{"name": "id", "type": "str", "required": true}],
            "query_params": [],
            "body_params": [],
            "returns": {"type": "dict", "description": "用户对象"}
        }
    ]
}
"""

import argparse
import ast
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class APIScanner:
    def __init__(self, project_dir: str, framework: str = "auto"):
        self.project_dir = Path(project_dir)
        self.framework = framework
        self.apis = []
        self.detected_framework = None

    def detect_framework(self) -> str:
        """检测项目使用的Web框架"""
        if self.framework != "auto":
            return self.framework

        # 检测常见的导入和文件特征
        py_files = list(self.project_dir.rglob("*.py"))
        js_files = list(self.project_dir.rglob("*.js"))

        flask_patterns = ["from flask import", "import flask", "Flask("]
        fastapi_patterns = ["from fastapi import", "import fastapi", "FastAPI("]
        express_patterns = ["require('express')", "import express", "express()"]

        for py_file in py_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                if any(p in content for p in fastapi_patterns):
                    return "fastapi"
                if any(p in content for p in flask_patterns):
                    return "flask"
            except Exception:
                continue

        for js_file in js_files:
            try:
                content = js_file.read_text(encoding="utf-8")
                if any(p in content for p in express_patterns):
                    return "express"
            except Exception:
                continue

        return "flask"  # 默认返回flask

    def scan_python_files(self):
        """扫描Python文件"""
        py_files = list(self.project_dir.rglob("*.py"))
        exclude_dirs = {".venv", "venv", "__pycache__", ".git", "node_modules", "tests", "test"}

        for py_file in py_files:
            # 跳过排除的目录
            if any(part in exclude_dirs for part in py_file.parts):
                continue

            try:
                content = py_file.read_text(encoding="utf-8")
                if self.detected_framework == "flask":
                    self._scan_flask_file(content, str(py_file))
                elif self.detected_framework == "fastapi":
                    self._scan_fastapi_file(content, str(py_file))
            except Exception as e:
                print(f"Warning: Failed to scan {py_file}: {e}")

    def scan_javascript_files(self):
        """扫描JavaScript文件"""
        js_files = list(self.project_dir.rglob("*.js"))
        exclude_dirs = {".venv", "venv", "__pycache__", ".git", "node_modules", "tests", "test"}

        for js_file in js_files:
            # 跳过排除的目录
            if any(part in exclude_dirs for part in js_file.parts):
                continue

            try:
                content = js_file.read_text(encoding="utf-8")
                if self.detected_framework == "express":
                    self._scan_express_file(content, str(js_file))
            except Exception as e:
                print(f"Warning: Failed to scan {js_file}: {e}")

    def _scan_flask_file(self, content: str, filepath: str):
        """扫描Flask路由"""
        # 匹配 @app.route 或 @bp.route 装饰器
        pattern = r'@(\w+)\.route\([\'"]([^\'"]+)[\'"][,\)]'
        matches = list(re.finditer(pattern, content))

        for i, match in enumerate(matches):
            app_name = match.group(1)
            path = match.group(2)

            # 查找对应的函数定义
            func_match = re.search(r'def\s+(\w+)\s*\([^)]*\):', content[match.end():])
            if func_match:
                func_name = func_match.group(1)
                line_num = content[:match.start()].count('\n') + 1

                # 提取文档字符串
                doc_match = re.search(r'"""(.*?)"""', content[match.end():match.end()+500], re.DOTALL)
                description = doc_match.group(1).strip() if doc_match else ""

                # 提取参数
                params = self._extract_python_params(content[match.end():match.end()+500])

                self.apis.append({
                    "path": path,
                    "method": "GET",  # Flask默认GET，可通过methods参数修改
                    "function": func_name,
                    "file": filepath,
                    "line": line_num,
                    "description": description,
                    "path_params": self._extract_path_params(path),
                    "query_params": params.get("query", []),
                    "body_params": params.get("body", []),
                    "returns": params.get("returns", {})
                })

    def _scan_fastapi_file(self, content: str, filepath: str):
        """扫描FastAPI路由"""
        # 匹配 @app.get, @app.post, @app.put, @app.delete, @app.patch
        methods = ["get", "post", "put", "delete", "patch"]
        pattern = r'@(\w+)\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]'

        for match in re.finditer(pattern, content):
            app_name = match.group(1)
            method = match.group(2).upper()
            path = match.group(3)

            # 查找对应的函数定义
            func_match = re.search(r'async def\s+(\w+)\s*\([^)]*\):', content[match.end():])
            if not func_match:
                func_match = re.search(r'def\s+(\w+)\s*\([^)]*\):', content[match.end():])

            if func_match:
                func_name = func_match.group(1)
                line_num = content[:match.start()].count('\n') + 1

                # 提取文档字符串
                doc_match = re.search(r'"""(.*?)"""', content[match.end():match.end()+500], re.DOTALL)
                description = doc_match.group(1).strip() if doc_match else ""

                # 提取FastAPI参数（从函数签名）
                params = self._extract_fastapi_params(content[match.end():match.end()+500])

                self.apis.append({
                    "path": path,
                    "method": method,
                    "function": func_name,
                    "file": filepath,
                    "line": line_num,
                    "description": description,
                    "path_params": params.get("path", []),
                    "query_params": params.get("query", []),
                    "body_params": params.get("body", []),
                    "returns": params.get("returns", {})
                })

    def _scan_express_file(self, content: str, filepath: str):
        """扫描Express路由"""
        # 匹配 app.get, router.post 等
        methods = ["get", "post", "put", "delete", "patch"]
        pattern = r'(app|router)\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]'

        for match in re.finditer(pattern, content):
            app_name = match.group(1)
            method = match.group(2).upper()
            path = match.group(3)

            line_num = content[:match.start()].count('\n') + 1

            # 提取回调函数和注释
            func_match = re.search(r',\s*\([^)]*\)\s*=>\s*{', content[match.end():match.end()+300])
            comment_match = re.search(r'//\s*(.*?)\n', content[:match.start()][-200:])

            description = comment_match.group(1).strip() if comment_match else ""

            # 提取路径参数
            path_params = self._extract_express_path_params(path)

            self.apis.append({
                "path": path,
                "method": method,
                "function": f"{app_name}.{method.lower()}",
                "file": filepath,
                "line": line_num,
                "description": description,
                "path_params": path_params,
                "query_params": [],
                "body_params": [],
                "returns": {}
            })

    def _extract_path_params(self, path: str) -> List[Dict]:
        """提取路径参数"""
        # 匹配 {param} 或 <param> 格式
        params = re.findall(r'[<{](\w+)[>}]', path)
        return [{"name": p, "type": "str", "required": True} for p in params]

    def _extract_express_path_params(self, path: str) -> List[Dict]:
        """提取Express路径参数（:id 格式）"""
        params = re.findall(r':(\w+)', path)
        return [{"name": p, "type": "str", "required": True} for p in params]

    def _extract_python_params(self, code: str) -> Dict:
        """提取Python函数参数（简化版）"""
        # 这里做简单提取，实际项目可以更复杂
        params = {
            "query": [],
            "body": [],
            "returns": {}
        }

        # 查找request.args引用（查询参数）
        query_match = re.findall(r'request\.args\.get\([\'"]([^\'"]+)[\'"]', code)
        for q in query_match:
            params["query"].append({
                "name": q,
                "type": "str",
                "required": False,
                "description": ""
            })

        # 查找request.json引用（请求体参数）
        body_match = re.findall(r'request\.json\.get\([\'"]([^\'"]+)[\'"]', code)
        for b in body_match:
            params["body"].append({
                "name": b,
                "type": "any",
                "required": False,
                "description": ""
            })

        return params

    def _extract_fastapi_params(self, code: str) -> Dict:
        """提取FastAPI函数参数（带类型注解）"""
        params = {
            "path": [],
            "query": [],
            "body": [],
            "returns": {}
        }

        # 提取函数签名中的参数
        func_sig_match = re.search(r'def\s+\w+\s*\((.*?)\)', code, re.DOTALL)
        if func_sig_match:
            sig = func_sig_match.group(1)

            # 匹配带类型注解的参数: name: type = default 或 name: type
            param_matches = re.findall(r'(\w+):\s*([^=,\)]+)(?:\s*=\s*([^,\)]+))?', sig)

            for param_name, param_type, default in param_matches:
                if param_name in ["self"]:
                    continue

                # 判断参数类型
                if param_name.endswith("_id") or ":" in param_type:
                    # 可能是路径参数
                    params["path"].append({
                        "name": param_name,
                        "type": param_type.strip(),
                        "required": default is None
                    })
                elif default is not None:
                    # 有默认值，可能是查询参数
                    params["query"].append({
                        "name": param_name,
                        "type": param_type.strip(),
                        "required": False,
                        "default": default.strip(),
                        "description": ""
                    })
                else:
                    # 没有默认值，可能是请求体或路径参数
                    params["body"].append({
                        "name": param_name,
                        "type": param_type.strip(),
                        "required": True,
                        "description": ""
                    })

        return params

    def scan(self) -> Dict:
        """执行扫描"""
        self.detected_framework = self.detect_framework()
        print(f"Detected framework: {self.detected_framework}")

        if self.detected_framework in ["flask", "fastapi"]:
            self.scan_python_files()
        elif self.detected_framework == "express":
            self.scan_javascript_files()

        return {
            "project_name": self.project_dir.name,
            "framework": self.detected_framework,
            "total_apis": len(self.apis),
            "apis": self.apis
        }


def main():
    parser = argparse.ArgumentParser(description="Scan project code for API endpoints")
    parser.add_argument("--project-dir", required=True, help="Project root directory")
    parser.add_argument("--framework", default="auto", choices=["auto", "flask", "fastapi", "express"],
                        help="Web framework type")
    parser.add_argument("--output", default="api_scan_result.json", help="Output JSON file path")

    args = parser.parse_args()

    scanner = APIScanner(args.project_dir, args.framework)
    result = scanner.scan()

    # 写入输出文件
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nScanned {result['total_apis']} API endpoints")
    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()
