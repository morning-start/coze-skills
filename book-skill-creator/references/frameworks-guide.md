# 常用框架使用指南

## 目录
1. [Web 框架](#web-框架)
2. [数据处理框架](#数据处理框架)
3. [AI/ML 框架](#aiml-框架)
4. [工具库](#工具库)
5. [配置与部署](#配置与部署)

## 概览
本文档汇总常用技术框架的使用方法、适用场景和最佳实践，帮助快速选择和集成合适的框架。

## Web 框架

### FastAPI

#### 适用场景
- 高性能 API 服务
- 异步 I/O 密集型应用
- 需要自动生成 API 文档
- 现代 Python 生态系统

#### 安装配置
```bash
pip install fastapi uvicorn
```

#### 核心代码模式
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="My API")

class Item(BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items/")
async def create_item(item: Item):
    return {"name": item.name, "price": item.price}
```

#### 最佳实践
- 使用 pydantic 进行数据验证
- 异步函数处理 I/O 操作
- 依赖注入管理共享资源
- 自动文档：访问 /docs

### Flask

#### 适用场景
- 轻量级 Web 应用
- 快速原型开发
- 中小型 API 服务
- 需要灵活扩展

#### 安装配置
```bash
pip install flask
```

#### 核心代码模式
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({"items": []})

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    return jsonify({"message": "created"}), 201
```

#### 最佳实践
- 使用 Blueprint 组织路由
- 环境变量配置管理
- 错误处理中间件
- 蓝图模式模块化

### Django

#### 适用场景
- 全栈 Web 应用
- 需要 ORM 和管理后台
- 大型企业应用
- 内容管理系统

#### 安装配置
```bash
pip install django
django-admin startproject myproject
```

#### 核心代码模式
```python
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

@require_http_methods(["GET"])
def get_items(request):
    items = Item.objects.all()
    return JsonResponse({"items": list(items.values())})
```

#### 最佳实践
- 使用 Django ORM 处理数据库
- REST framework 构建 API
- 中间件处理跨域和认证
- Admin 管理后台利用

## 数据处理框架

### Pandas

#### 适用场景
- 数据分析和清洗
- 结构化数据处理
- 时间序列分析
- 数据导出导入

#### 安装配置
```bash
pip install pandas openpyxl
```

#### 核心代码模式
```python
import pandas as pd

# 读取数据
df = pd.read_csv('data.csv')

# 数据处理
df['new_column'] = df['column1'] * 2
filtered = df[df['value'] > 100]

# 导出数据
df.to_excel('output.xlsx', index=False)
```

#### 最佳实践
- 使用向量化操作避免循环
- 处理大数据时使用 chunksize
- 类型推断和转换
- 缺失值处理策略

### NumPy

#### 适用场景
- 数值计算
- 矩阵运算
- 科学计算
- 数据预处理

#### 安装配置
```bash
pip install numpy
```

#### 核心代码模式
```python
import numpy as np

# 创建数组
arr = np.array([1, 2, 3, 4])
matrix = np.zeros((3, 3))

# 数组操作
result = np.dot(matrix, arr)
mean = np.mean(arr)
```

#### 最佳实践
- 广播机制优化计算
- 避免不必要的拷贝
- 内存视图使用
- 并行计算利用

## AI/ML 框架

### PyTorch

#### 适用场景
- 深度学习研究
- 神经网络训练
- 计算机视觉
- 自然语言处理

#### 安装配置
```bash
pip install torch torchvision
```

#### 核心代码模式
```python
import torch
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 2)

    def forward(self, x):
        return self.fc(x)

model = MyModel()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

#### 最佳实践
- GPU 加速利用
- 自动微分使用
- 数据加载器优化
- 模型保存与加载

### TensorFlow/Keras

#### 适用场景
- 生产环境部署
- 大规模模型训练
- 移动端部署
- 推荐系统

#### 安装配置
```bash
pip install tensorflow
```

#### 核心代码模式
```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(10)
])

model.compile(optimizer='adam', loss='mse')
model.fit(x_train, y_train, epochs=10)
```

#### 最佳实践
- Keras 高级 API 使用
- 模型导出格式
- TensorBoard 监控
- 分布式训练

## 工具库

### Requests

#### 适用场景
- HTTP 请求发送
- API 调用
- 网页抓取
- 文件下载

#### 安装配置
```bash
pip install requests
```

#### 核心代码模式
```python
import requests

response = requests.get('https://api.example.com/data')
data = response.json()

# POST 请求
response = requests.post(
    'https://api.example.com/submit',
    json={'key': 'value'}
)
```

#### 最佳实践
- 会话管理 keep-alive
- 超时设置
- 错误处理
- 重试机制

### PyYAML

#### 适用场景
- 配置文件读取
- 数据序列化
- 技能包元数据
- 环境配置

#### 安装配置
```bash
pip install pyyaml
```

#### 核心代码模式
```python
import yaml

# 读取 YAML
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 写入 YAML
with open('output.yaml', 'w') as f:
    yaml.dump(config, f)
```

#### 最佳实践
- safe_load 防止代码注入
- 类型转换处理
- 多文档支持
- 格式化输出

### NetworkX

#### 适用场景
- 图结构分析
- 依赖关系管理
- 网络分析
- 路径查找

#### 安装配置
```bash
pip install networkx
```

#### 核心代码模式
```python
import networkx as nx

# 创建图
G = nx.DiGraph()
G.add_node('A')
G.add_edge('A', 'B')

# 图分析
shortest_path = nx.shortest_path(G, 'A', 'C')
topological_order = list(nx.topological_sort(G))
```

#### 最佳实践
- 有向图/无向图选择
- 节点属性管理
- 可视化布局
- 性能优化

## 配置与部署

### 环境变量管理

#### Python-dotenv
```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')
```

### 日志配置
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### 异步编程最佳实践
```python
import asyncio

async def main():
    # 并发执行
    await asyncio.gather(
        task1(),
        task2(),
        task3()
    )

asyncio.run(main())
```

## 框架选择决策树

### Web 框架选择
```
需要高性能和自动文档？
├─ 是 → FastAPI
└─ 否 → 需要全栈和ORM？
    ├─ 是 → Django
    └─ 否 → Flask
```

### 数据处理选择
```
需要数值计算？
├─ 是 → NumPy
└─ 否 → 需要表格分析？
    ├─ 是 → Pandas
    └─ 否 → 原生 Python
```

### ML 框架选择
```
需要研究和灵活性？
├─ 是 → PyTorch
└─ 否 → 需要部署和生态？
    └─ TensorFlow/Keras
```
