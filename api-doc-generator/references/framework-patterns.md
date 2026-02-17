# Web 框架路由识别模式

## 目录
- [Flask](#flask)
- [FastAPI](#fastapi)
- [Express](#express)

## Flask

### 路由定义模式
```python
@app.route('/users', methods=['GET', 'POST'])
def users():
    pass

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    pass

# 使用蓝图
@bp.route('/products', methods=['GET'])
def products():
    pass
```

### 识别规则
- 装饰器：`@app.route` 或 `@bp.route`
- 第一个参数：路由路径
- methods参数：HTTP方法（可选，默认GET）
- 路径参数格式：`<param_name>` 或 `<type:param_name>`

### 参数提取
- 路径参数：从路由装饰器的路径中提取 `<param_name>`
- 查询参数：查找 `request.args.get()` 调用
- 请求体参数：查找 `request.json.get()` 或 `request.form.get()` 调用

## FastAPI

### 路由定义模式
```python
@app.get('/users')
async def get_users(skip: int = 0, limit: int = 100):
    pass

@app.post('/users')
async def create_user(user: UserCreate):
    pass

@app.get('/users/{user_id}')
async def get_user(user_id: int):
    pass
```

### 识别规则
- 装饰器：`@app.get`, `@app.post`, `@app.put`, `@app.delete`, `@app.patch`
- 装饰器名称直接表示HTTP方法
- 第一个参数：路由路径
- 函数签名中的参数：自动识别为查询参数或路径参数

### 参数提取
- 路径参数：路径中的 `{param_name}`
- 查询参数：函数签名中非路径参数且有默认值
- 请求体参数：函数签名中的Pydantic模型参数
- 类型注解：从类型注解中提取参数类型

## Express

### 路由定义模式
```javascript
// 应用级别
app.get('/users', (req, res) => {
  // ...
});

app.post('/users', (req, res) => {
  // ...
});

// 路由器级别
router.get('/products', (req, res) => {
  // ...
});

// 路径参数
app.get('/users/:id', (req, res) => {
  // ...
});
```

### 识别规则
- 方法调用：`app.get`, `app.post`, `app.put`, `app.delete`, `app.patch`
- 或：`router.get`, `router.post` 等
- 第一个参数：路由路径
- 第二个参数：回调函数

### 参数提取
- 路径参数：路径中的 `:param_name` 格式
- 查询参数：`req.query` 属性
- 请求体参数：`req.body` 属性

## 通用识别策略

### 1. 框架检测
优先级：
1. 检测 `from fastapi import` 或 `FastAPI(` → FastAPI
2. 检测 `from flask import` 或 `Flask(` → Flask
3. 检测 `require('express')` 或 `express()` → Express

### 2. 路由提取
- 使用正则表达式匹配路由定义模式
- 提取路径、方法、函数名
- 记录文件名和行号

### 3. 参数提取
- 根据框架特点提取不同类型的参数
- 优先利用类型注解（FastAPI）
- 解析代码中的请求对象调用

### 4. 文档提取
- Python：提取函数的docstring（三引号字符串）
- JavaScript：提取路由定义前的注释（// 或 /* */）

## 限制与建议

### 当前限制
1. 仅识别静态路由，无法完全解析动态路由生成器
2. 参数提取基于简单模式匹配，可能遗漏复杂用法
3. 响应结构无法自动提取，需要手动补充

### 使用建议
1. 在代码中添加清晰的docstring和注释
2. 使用类型注解（FastAPI）
3. 对于复杂路由，手动补充文档信息
4. 生成文档后人工审核和补充
