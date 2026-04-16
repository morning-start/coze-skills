# 优秀执行方案库

## 目录
1. [API 调用类方案](#api-调用类方案)
2. [数据处理类方案](#数据处理类方案)
3. [工作流类方案](#工作流类方案)
4. [文件转换类方案](#文件转换类方案)
5. [自动化构建类方案](#自动化构建类方案)

## 概览
本文档收集了各类问题的优秀执行方案，包含问题场景、解决方案和可复制的代码示例，帮助快速构建高质量技能。

## API 调用类方案

### 方案1：RESTful API 调用（含重试和错误处理）

#### 问题场景
需要调用第三方 REST API，要求：
- 支持自动重试（网络故障）
- 完善的错误处理
- 请求超时控制
- 结果验证

#### 解决方案
```python
import time
from typing import Optional, Dict, Any
from coze_workload_identity import requests

class APIClient:
    """通用 API 客户端，支持重试和错误处理"""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        max_retries: int = 3,
        timeout: int = 30
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.max_retries = max_retries
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """发起请求，支持重试"""
        url = f"{self.base_url}{endpoint}"
        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method,
                    url,
                    headers=self.headers,
                    json=data,
                    timeout=self.timeout
                )

                # 检查 HTTP 状态码
                if response.status_code >= 400:
                    raise Exception(
                        f"HTTP {response.status_code}: {response.text}"
                    )

                result = response.json()

                # 检查业务错误
                if result.get("error"):
                    raise Exception(f"API Error: {result['error']}")

                return result

            except requests.exceptions.Timeout:
                last_error = "请求超时"
                time.sleep(2 ** attempt)  # 指数退避

            except requests.exceptions.RequestException as e:
                last_error = f"网络错误: {str(e)}"
                time.sleep(2 ** attempt)

        raise Exception(f"请求失败（重试 {self.max_retries} 次）: {last_error}")

    def get(self, endpoint: str) -> Dict[str, Any]:
        return self._request("GET", endpoint)

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", endpoint, data)
```

#### 使用示例
```python
client = APIClient(
    base_url="https://api.example.com",
    api_key="your-api-key"
)

result = client.get("/users")
print(result)

new_user = client.post("/users", {"name": "John"})
print(new_user)
```

### 方案2：异步批量 API 调用

#### 问题场景
需要并发调用多个 API 接口，提高效率

#### 解决方案
```python
import asyncio
from typing import List, Dict, Any
from coze_workload_identity import requests

async def async_call_api(
    url: str,
    headers: Dict[str, str],
    payload: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """异步 API 调用"""
    try:
        response = await requests.get(url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

async def batch_call_api(
    urls: List[str],
    headers: Dict[str, str]
) -> List[Dict[str, Any]]:
    """批量并发调用 API"""
    tasks = [async_call_api(url, headers) for url in urls]
    results = await asyncio.gather(*tasks)
    return results
```

## 数据处理类方案

### 方案1：数据清洗管道

#### 问题场景
需要清洗原始数据，包括：
- 缺失值处理
- 重复值处理
- 类型转换
- 异常值处理

#### 解决方案
```python
import pandas as pd
from typing import Dict, Any

class DataCleaningPipeline:
    """数据清洗管道"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """执行清洗流程"""
        # 去重
        if self.config.get("drop_duplicates"):
            df = df.drop_duplicates()

        # 处理缺失值
        if self.config.get("handle_missing") == "drop":
            df = df.dropna()
        elif self.config.get("handle_missing") == "fill":
            df = df.fillna(self.config.get("fill_value", 0))

        # 类型转换
        if self.config.get("type_conversions"):
            for col, dtype in self.config["type_conversions"].items():
                if col in df.columns:
                    df[col] = df[col].astype(dtype)

        # 处理异常值
        if self.config.get("handle_outliers"):
            for col in self.config["handle_outliers"]:
                if col in df.columns:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR
                    df = df[(df[col] >= lower) & (df[col] <= upper)]

        return df
```

#### 使用示例
```python
config = {
    "drop_duplicates": True,
    "handle_missing": "fill",
    "fill_value": 0,
    "type_conversions": {
        "age": "int64",
        "salary": "float64"
    },
    "handle_outliers": ["salary"]
}

pipeline = DataCleaningPipeline(config)
cleaned_df = pipeline.clean(raw_df)
```

### 方案2：数据转换与导出

#### 问题场景
需要将数据从一种格式转换为另一种格式

#### 解决方案
```python
import pandas as pd
import json
from pathlib import Path

class DataConverter:
    """数据格式转换器"""

    @staticmethod
    def csv_to_json(csv_path: str, json_path: str):
        """CSV 转 JSON"""
        df = pd.read_csv(csv_path)
        df.to_json(json_path, orient='records', force_ascii=False)

    @staticmethod
    def json_to_excel(json_path: str, excel_path: str):
        """JSON 转 Excel"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df.to_excel(excel_path, index=False)

    @staticmethod
    def batch_convert(
        input_dir: str,
        output_dir: str,
        input_format: str,
        output_format: str
    ):
        """批量转换"""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for file in input_path.glob(f"*.{input_format}"):
            output_file = output_path / f"{file.stem}.{output_format}"

            if input_format == "csv" and output_format == "json":
                DataConverter.csv_to_json(str(file), str(output_file))
            elif input_format == "json" and output_format == "xlsx":
                DataConverter.json_to_excel(str(file), str(output_file))
```

## 工作流类方案

### 方案1：多步骤任务编排

#### 问题场景
需要按顺序执行多个任务，每个任务可能依赖前一个任务的输出

#### 解决方案
```python
from typing import Dict, Any, Callable
from dataclasses import dataclass

@dataclass
class TaskResult:
    """任务执行结果"""
    success: bool
    data: Any
    error: str = ""

class Workflow:
    """工作流编排器"""

    def __init__(self):
        self.tasks = []
        self.context = {}

    def add_task(
        self,
        name: str,
        func: Callable,
        depends_on: list = None
    ):
        """添加任务"""
        self.tasks.append({
            "name": name,
            "func": func,
            "depends_on": depends_on or []
        })

    def execute(self, initial_data: Dict[str, Any] = None):
        """执行工作流"""
        self.context = initial_data or {}
        results = {}

        for task in self.tasks:
            # 检查依赖
            for dep in task["depends_on"]:
                if not results.get(dep).success:
                    results[task["name"]] = TaskResult(
                        success=False,
                        data=None,
                        error=f"依赖任务 {dep} 失败"
                    )
                    break
            else:
                # 执行任务
                try:
                    result = task["func"](**self.context)
                    results[task["name"]] = TaskResult(
                        success=True,
                        data=result
                    )
                    self.context[task["name"]] = result
                except Exception as e:
                    results[task["name"]] = TaskResult(
                        success=False,
                        data=None,
                        error=str(e)
                    )

        return results
```

#### 使用示例
```python
def step1(input_data):
    print("执行步骤1")
    return {"processed": input_data + "_processed"}

def step2(processed_data):
    print("执行步骤2")
    return {"result": processed_data.upper()}

workflow = Workflow()
workflow.add_task("step1", step1)
workflow.add_task("step2", step2, depends_on=["step1"])

results = workflow.execute({"input_data": "test"})
```

### 方案2：条件分支流程

#### 问题场景
需要根据条件选择不同的执行路径

#### 解决方案
```python
from typing import Callable, Dict, Any

class ConditionalWorkflow:
    """条件分支工作流"""

    def __init__(self):
        self.rules = []

    def add_rule(
        self,
        condition: Callable[[Dict[str, Any]], bool],
        action: Callable[[Dict[str, Any]], Dict[str, Any]]
    ):
        """添加规则"""
        self.rules.append((condition, action))

    def execute(self, context: Dict[str, Any]):
        """执行工作流，匹配第一个满足条件的规则"""
        for condition, action in self.rules:
            if condition(context):
                return action(context)

        raise Exception("没有匹配的规则")
```

## 文件转换类方案

### 方案1：PDF 提取

#### 问题场景
从 PDF 文件中提取文本、表格和图片

#### 解决方案
```python
import PyPDF2
import pdfplumber
from typing import Dict, Any

class PDFExtractor:
    """PDF 内容提取器"""

    def extract_text(self, pdf_path: str) -> str:
        """提取文本"""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def extract_tables(self, pdf_path: str) -> list:
        """提取表格"""
        tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)
        return tables

    def extract_all(self, pdf_path: str) -> Dict[str, Any]:
        """提取所有内容"""
        return {
            "text": self.extract_text(pdf_path),
            "tables": self.extract_tables(pdf_path)
        }
```

### 方案2：Markdown 转 HTML

#### 问题场景
将 Markdown 文档转换为 HTML

#### 解决方案
```python
import markdown
from pathlib import Path

class MarkdownConverter:
    """Markdown 转换器"""

    def __init__(self):
        self.md = markdown.Markdown(
            extensions=['tables', 'fenced_code', 'toc']
        )

    def to_html(self, md_text: str) -> str:
        """Markdown 转 HTML"""
        return self.md.convert(md_text)

    def convert_file(self, md_path: str, html_path: str):
        """文件转换"""
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        html_content = self.to_html(md_content)

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
```

## 自动化构建类方案

### 方案1：批量文件生成

#### 问题场景
根据模板批量生成文件

#### 解决方案
```python
from jinja2 import Template
from pathlib import Path
from typing import Dict, Any

class FileGenerator:
    """批量文件生成器"""

    def __init__(self, template_dir: str):
        self.template_dir = Path(template_dir)

    def generate_from_template(
        self,
        template_name: str,
        output_path: str,
        context: Dict[str, Any]
    ):
        """从模板生成文件"""
        template_path = self.template_dir / template_name
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        template = Template(template_content)
        output_content = template.render(**context)

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_content)

    def batch_generate(
        self,
        template_name: str,
        items: list,
        output_pattern: str
    ):
        """批量生成"""
        for item in items:
            output_path = output_pattern.format(**item)
            self.generate_from_template(template_name, output_path, item)
```

### 方案2：依赖关系分析

#### 问题场景
分析多个组件之间的依赖关系

#### 解决方案
```python
import networkx as nx
from typing import Dict, List, Set

class DependencyAnalyzer:
    """依赖关系分析器"""

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_component(self, name: str, dependencies: List[str] = None):
        """添加组件及其依赖"""
        self.graph.add_node(name)
        for dep in dependencies or []:
            self.graph.add_edge(dep, name)

    def get_build_order(self) -> List[str]:
        """获取构建顺序（拓扑排序）"""
        return list(nx.topological_sort(self.graph))

    def find_circular_dependencies(self) -> List[Set[str]]:
        """查找循环依赖"""
        return list(nx.simple_cycles(self.graph))

    def visualize(self, output_path: str):
        """可视化依赖图"""
        import matplotlib.pyplot as plt

        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=2000)
        plt.savefig(output_path)
```

## 方案选择指南

### API 调用场景
```
需要并发调用？
├─ 是 → 异步批量方案
└─ 否 → 需要重试？
    ├─ 是 → 重试+错误处理方案
    └─ 否 → 简单 requests 调用
```

### 数据处理场景
```
需要清洗数据？
├─ 是 → 数据清洗管道
└─ 否 → 需要转换格式？
    └─ 数据转换与导出
```

### 工作流场景
```
需要条件分支？
├─ 是 → 条件分支流程
└─ 否 → 多步骤编排
```

### 文件操作场景
```
处理 PDF？
├─ 是 → PDF 提取方案
└─ 否 → Markdown 转换？
    └─ Markdown 转 HTML
```
