#!/usr/bin/env python3
"""
六层架构代码生成器
根据指定的层级和上下文信息，生成标准化代码模板
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any


# 代码模板定义（使用双重花括号转义 Python 格式化占位符）
TEMPLATES = {
    "ui": {
        "language": "vue",
        "description": "UI 层（Vue 3 + Tailwind）",
        "template": """<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">{{title}}</h2>
    <form @submit.prevent="handleSubmit" class="space-y-4">
      {{form_fields}}
      <button 
        type="submit" 
        :disabled="loading"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {{{{ loading ? '提交中...' : '提交' }}}}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import {{ ref }} from 'vue'
import Swal from 'sweetalert2'

const loading = ref(false)

{{state_definitions}}

const handleSubmit = async () => {{
  try {{
    loading.value = true
    {{submit_logic}}
    Swal.fire({{
      icon: 'success',
      title: '成功',
      text: '{{success_message}}'
    }})
  }} catch (error) {{
    console.error('操作失败:', error)
    Swal.fire({{
      icon: 'error',
      title: '错误',
      text: error.message || '{{error_message}}'
    }})
  }} finally {{
    loading.value = false
  }}
}}
</script>
"""
    },
    
    "frontend_service": {
        "language": "typescript",
        "description": "前端服务层（Pinia Store）",
        "template": """import {{ defineStore }} from 'pinia'
import {{ ref, computed }} from 'vue'
import {{{{ api_function }}}} from '@/api/{{module}}'

interface {{StateInterface}} {{
  {{state_fields}}
}}

export const use{{StoreName}}Store = defineStore('{{storeName}}', () => {{
  // State
  {{state_initialization}}

  // Actions
  async {{action_name}}({{action_params}}) {{
    try {{
      const response = await {{api_function}}({{api_call_params}})
      {{action_logic}}
      return response
    }} catch (error) {{
      console.error('{{action_name}} 失败:', error)
      throw error
    }}
  }}

  // Getters
  {{getters}}

  return {{
    {{export_fields}}
  }}
}}, {{
  persist: {{persist_option}}  // 是否持久化
}})
"""
    },
    
    "frontend_api": {
        "language": "typescript",
        "description": "前端 API 层（Axios + TypeScript）",
        "template": """import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

// 请求拦截器
axios.interceptors.request.use(
  (config) => {{
    const token = localStorage.getItem('token')
    if (token) {{
      config.headers.Authorization = `Bearer ${{token}}`
    }}
    return config
  }},
  (error) => Promise.reject(error)
)

// 响应拦截器
axios.interceptors.response.use(
  (response) => response.data,
  (error) => {{
    if (error.response?.status === 401) {{
      // Token 过期，跳转登录
      localStorage.removeItem('token')
      window.location.href = '/login'
    }}
    return Promise.reject(error.response?.data || error.message)
  }}
)

// TypeScript 接口定义
export interface {{RequestInterface}} {{
  {{request_fields}}
}}

export interface {{ResponseInterface}} {{
  {{response_fields}}
}}

// API 函数
export async function {{function_name}}(
  {{function_params}}
): Promise<{{ResponseInterface}}> {{
  const url = '{{api_endpoint}}'
  const config = {{
    method: '{{http_method}}',
    url,
    {{request_config}}
  }}
  
  return axios(config)
}}
"""
    },
    
    "backend_api": {
        "language": "python",
        "description": "后端 API 层（FastAPI + Pydantic）",
        "template": """from fastapi import APIRouter, Depends, HTTPException, {form_or_body}, File, UploadFile
from pydantic import BaseModel
{imports}

router = APIRouter(prefix="/{resource}", tags=["{Resource}"])

# Pydantic Models
class {RequestModel}(BaseModel):
    \"\"\"请求模型\"\"\"
    {request_fields}

class {ResponseModel}(BaseModel):
    \"\"\"响应模型\"\"\"
    {response_fields}

# API Routes
@router.{http_method}("/{action}", response_model={ResponseModel})
async def {route_name}(
    {route_params}
) -> {ResponseModel}:
    \"\"\"{route_description}\"\"\"
    try:
        # 参数验证
        {validation_logic}
        
        # 调用服务层
        {service_call}
        
        # 返回标准化响应
        return {ResponseModel}(
            code=200,
            data={response_data},
            message="操作成功"
        )
    except {service_exception} as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务器内部错误")
"""
    },
    
    "backend_service": {
        "language": "python",
        "description": "后端服务层（Service 类）",
        "template": """from typing import Optional
from fastapi import UploadFile, HTTPException
import os
import uuid
from datetime import datetime

{imports}

class {ServiceName}Service:
    \"\"\"{ServiceName} 服务层\"\"\"
    
    def __init__(self, db_session):
        self.db = db_session
        self.{service_name}_repository = {RepositoryName}(db_session)
    
    async def {method_name}({method_params}):
        \"\"\"{method_description}\"\"\"
        
        # 业务验证
        {business_validation}
        
        # 业务逻辑处理
        {business_logic}
        
        # 返回结果
        {return_statement}
    
    def _validate_file(self, file: UploadFile, allowed_types: list, max_size: int = 5 * 1024 * 1024):
        \"\"\"验证文件类型和大小\"\"\"
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"不支持的文件类型: {{file.content_type}}")
        
        content = file.file.read()
        if len(content) > max_size:
            raise HTTPException(status_code=400, detail=f"文件大小超过限制（{{max_size}} 字节）")
        
        file.file.seek(0)  # 重置文件指针
        return content
    
    def _generate_unique_filename(self, original_filename: str) -> str:
        \"\"\"生成唯一文件名\"\"\"
        ext = os.path.splitext(original_filename)[1]
        return f"{{uuid.uuid4()}}_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}{{ext}}"
"""
    },
    
    "data_layer": {
        "language": "python",
        "description": "数据层（SQLAlchemy + PostgreSQL）",
        "template": """from sqlalchemy import Column, String, Integer, DateTime, {other_types}
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class {ModelName}(Base):
    \"\"\"{ModelName} 数据模型\"\"\"
    __tablename__ = "{table_name}"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # 字段定义
    {model_fields}
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<{ModelName}(id={{self.id}}, {repr_fields})>"

# Alembic 迁移命令
# alembic revision --autogenerate -m "Add {ModelName} model"
# alembic upgrade head

# Repository 模式（可选）
class {RepositoryName}:
    \"\"\"{ModelName} 数据仓库\"\"\"
    
    def __init__(self, db_session):
        self.db = db_session
    
    async def get_by_id(self, id: int) -> Optional[{ModelName}]:
        \"\"\"根据 ID 查询\"\"\"
        return self.db.query({ModelName}).filter({ModelName}.id == id).first()
    
    async def create(self, {create_params}) -> {ModelName}:
        \"\"\"创建记录\"\"\"
        {model_instance} = {ModelName}({model_init})
        self.db.add({model_instance})
        self.db.commit()
        self.db.refresh({model_instance})
        return {model_instance}
    
    async def update(self, {model_instance}: {ModelName}) -> {ModelName}:
        \"\"\"更新记录\"\"\"
        self.db.commit()
        self.db.refresh({model_instance})
        return {model_instance}
    
    async def delete(self, id: int) -> bool:
        \"\"\"删除记录\"\"\"
        {model_instance} = await self.get_by_id(id)
        if {model_instance}:
            self.db.delete({model_instance})
            self.db.commit()
            return True
        return False
"""
    }
}


def load_context(context_file: str) -> Dict[str, Any]:
    """加载上下文信息"""
    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"警告: 上下文文件不存在: {context_file}")
        return {}


def generate_code(layer: str, context: Dict[str, Any]) -> str:
    """
    生成指定层级的代码模板
    
    Args:
        layer: 层级名称 (ui/frontend_service/frontend_api/backend_api/backend_service/data_layer)
        context: 上下文信息字典
    
    Returns:
        生成的代码字符串
    """
    if layer not in TEMPLATES:
        raise ValueError(f"不支持的层级: {layer}. 支持的层级: {', '.join(TEMPLATES.keys())}")
    
    template_info = TEMPLATES[layer]
    template = template_info["template"]
    
    # 替换上下文变量
    try:
        code = template.format(**context)
    except KeyError as e:
        raise ValueError(f"上下文缺少必需的变量: {e}")
    
    return code


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("用法: python generate_code.py <layer> <context_file>")
        print("示例: python generate_code.py ui context.json")
        print("\n支持的层级:")
        for layer, info in TEMPLATES.items():
            print(f"  - {layer}: {info['description']}")
        sys.exit(1)
    
    layer = sys.argv[1]
    context_file = sys.argv[2]
    
    try:
        context = load_context(context_file)
        code = generate_code(layer, context)
        print(f"// {TEMPLATES[layer]['description']} 代码模板\n")
        print(code)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
