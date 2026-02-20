#!/usr/bin/env python3
"""
CI/CD 文档生成脚本
功能：根据项目类型和特征生成 CI/CD 文档和配置文件
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, Optional, List


class CICDGenerator:
    """CI/CD 生成器"""
    
    def __init__(self, project_path: str, output_path: Optional[str] = None):
        self.project_path = Path(project_path).resolve()
        self.wiki_path = output_path or self.project_path / "wiki" / "05-部署运维"
        self.project_info = self._load_project_info()
    
    def _load_project_info(self) -> Dict:
        """加载项目分析信息"""
        analysis_file = self.project_path / "project-analysis.json"
        if analysis_file.exists():
            with open(analysis_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _detect_platform(self) -> str:
        """检测 CI/CD 平台"""
        # 优先级：GitHub > GitLab > Jenkins
        if (self.project_path / ".github").exists():
            return "github"
        elif (self.project_path / ".gitlab-ci.yml").exists():
            return "gitlab"
        elif (self.project_path / "Jenkinsfile").exists():
            return "jenkins"
        
        # 检测 Git 远程仓库
        git_config = self.project_path / ".git" / "config"
        if git_config.exists():
            with open(git_config, 'r', encoding='utf-8') as f:
                content = f.read()
                if "github.com" in content:
                    return "github"
                elif "gitlab.com" in content:
                    return "gitlab"
        
        # 默认 GitHub
        return "github"
    
    def _detect_language(self) -> str:
        """检测项目主要语言"""
        languages = self.project_info.get('languages', [])
        
        if 'Python' in languages:
            return 'python'
        elif 'JavaScript' in languages or 'TypeScript' in languages:
            return 'javascript'
        elif 'Java' in languages:
            return 'java'
        elif 'Go' in languages:
            return 'go'
        elif 'Rust' in languages:
            return 'rust'
        
        return 'python'  # 默认
    
    def _detect_project_type(self) -> str:
        """检测项目类型"""
        frameworks = self.project_info.get('frameworks', [])
        
        web_frameworks = ['django', 'flask', 'fastapi', 'express', 'react', 'vue', 'angular']
        if any(f in frameworks for f in web_frameworks):
            return "web"
        
        if 'electron' in frameworks or 'tauri' in frameworks:
            return "desktop"
        
        return "generic"
    
    def _generate_github_actions_workflow(self, language: str) -> str:
        """生成 GitHub Actions Workflow"""
        
        if language == 'python':
            return """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Lint
      run: |
        pip install pylint
        pylint src/
    
    - name: Test
      run: |
        pip install pytest pytest-cov
        pytest --cov=src tests/
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build
      run: |
        echo "Building project..."
        # 添加构建命令
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: build-artifacts
        path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy
      run: |
        echo "Deploying to production..."
        # 添加部署命令
"""
        
        elif language == 'javascript':
            return """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Lint
      run: npm run lint
    
    - name: Test
      run: npm test -- --coverage
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build
      run: npm run build
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: build-artifacts
        path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy
      run: |
        echo "Deploying to production..."
        # 添加部署命令
"""
        
        else:  # generic
            return """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Test
      run: |
        echo "Running tests..."
        # 添加测试命令

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build
      run: |
        echo "Building project..."
        # 添加构建命令
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: build-artifacts
        path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy
      run: |
        echo "Deploying to production..."
        # 添加部署命令
"""
    
    def _generate_gitlab_ci_config(self, language: str) -> str:
        """生成 GitLab CI 配置"""
        
        if language == 'python':
            return """stages:
  - lint
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: myapp:$CI_COMMIT_SHA

lint:
  stage: lint
  image: python:3.10
  script:
    - pip install pylint
    - pylint src/
  only:
    - main
    - develop
    - merge_requests

test:
  stage: test
  image: python:3.10
  script:
    - pip install pytest pytest-cov
    - pip install -r requirements.txt
    - pytest --cov=src tests/
  coverage: '/TOTAL.*\\s+(\\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
  only:
    - main
    - develop
    - merge_requests

build:
  stage: build
  image: alpine:latest
  script:
    - echo "Building project..."
    # 添加构建命令
  artifacts:
    paths:
      - dist/
  only:
    - main

deploy_production:
  stage: deploy
  image: alpine:latest
  script:
    - echo "Deploy to production"
    # 添加部署命令
  only:
    - main
  when: manual
"""
        
        else:
            return """stages:
  - lint
  - test
  - build
  - deploy

lint:
  stage: lint
  script:
    - echo "Running lint..."
    # 添加 lint 命令
  only:
    - main
    - develop
    - merge_requests

test:
  stage: test
  script:
    - echo "Running tests..."
    # 添加测试命令
  only:
    - main
    - develop
    - merge_requests

build:
  stage: build
  script:
    - echo "Building project..."
    # 添加构建命令
  artifacts:
    paths:
      - dist/
  only:
    - main

deploy_production:
  stage: deploy
  script:
    - echo "Deploy to production"
    # 添加部署命令
  only:
    - main
  when: manual
"""
    
    def _generate_cicd_document(self, platform: str, language: str, project_type: str) -> str:
        """生成 CI/CD 文档"""
        
        platform_name = {
            'github': 'GitHub Actions',
            'gitlab': 'GitLab CI',
            'jenkins': 'Jenkins'
        }.get(platform, 'GitHub Actions')
        
        config_file = {
            'github': '.github/workflows/ci.yml',
            'gitlab': '.gitlab-ci.yml',
            'jenkins': 'Jenkinsfile'
        }.get(platform, '.github/workflows/ci.yml')
        
        # 语言特定配置
        lang_config = {
            'python': {
                'test_tool': 'pytest',
                'lint_tool': 'pylint',
                'build_cmd': 'python setup.py build'
            },
            'javascript': {
                'test_tool': 'npm test',
                'lint_tool': 'npm run lint',
                'build_cmd': 'npm run build'
            },
            'java': {
                'test_tool': 'mvn test',
                'lint_tool': 'checkstyle',
                'build_cmd': 'mvn package'
            },
            'go': {
                'test_tool': 'go test ./...',
                'lint_tool': 'golangci-lint run',
                'build_cmd': 'go build'
            },
            'rust': {
                'test_tool': 'cargo test',
                'lint_tool': 'cargo clippy',
                'build_cmd': 'cargo build --release'
            }
        }.get(language, {
            'test_tool': 'test',
            'lint_tool': 'lint',
            'build_cmd': 'build'
        })
        
        return f"""# CI/CD 指南

## 概览

本文档记录项目的持续集成和持续部署流程。

## CI/CD 平台

本项目使用 **{platform_name}** 进行 CI/CD。

- 平台: {platform_name}
- 配置文件: `{config_file}`
- 状态徽章: `![CI Status](...)`

---

## 流程说明

### 持续集成 (CI)

#### 触发条件

- 推送到 `main` 或 `develop` 分支
- 创建 Pull Request / Merge Request
- 手动触发

#### CI 流程

1. **代码检查** (Lint)
   - 工具: {lang_config['lint_tool']}
   - 失败策略: 阻断后续流程

2. **单元测试** (Test)
   - 工具: {lang_config['test_tool']}
   - 覆盖率要求: > 80%
   - 失败策略: 阻断后续流程

3. **构建** (Build)
   - 命令: {lang_config['build_cmd']}
   - 生成构建产物

### 持续部署 (CD)

#### 部署环境

| 环境 | 用途 | 触发条件 | 审批 |
|------|------|----------|------|
| 开发环境 | 日常开发 | 推送 `develop` 分支 | 自动 |
| 测试环境 | 测试验证 | 推送 `main` 分支 | 自动 |
| 生产环境 | 线上发布 | 推送 `main` 分支 | 手动审批 |

#### 部署流程

1. **构建/打包**
   - 生成可部署文件
   - 可选：构建 Docker 镜像

2. **部署到环境**
   - 工具: [根据项目选择]
   - 滚动更新策略
   - 健康检查

3. **部署后验证**
   - 运行集成测试
   - 检查日志
   - 监控指标

---

## 配置说明

### 环境变量

| 变量名 | 说明 | 来源 |
|--------|------|------|
| `DATABASE_URL` | 数据库连接 | Secrets |
| `API_KEY` | API 密钥 | Secrets |
| `DEPLOY_KEY` | 部署密钥 | Secrets |

### Secrets 配置

**{platform_name} 配置步骤**：

{self._get_secrets_config_guide(platform)}

---

## 故障排查

### 常见问题

#### 1. 构建失败

**可能原因**：
- 依赖版本冲突
- 代码检查未通过
- 测试失败

**排查步骤**：
1. 查看构建日志
2. 本地复现问题
3. 修复代码
4. 重新提交

#### 2. 部署失败

**可能原因**：
- 环境变量缺失
- 网络问题
- 服务启动失败

**排查步骤**：
1. 检查部署日志
2. 验证 Secrets 配置
3. 检查服务健康状态
4. 回滚到上一个版本

#### 3. 测试超时

**可能原因**：
- 测试用例过多
- 依赖服务响应慢

**排查步骤**：
1. 优化测试用例
2. 使用并行测试
3. 增加超时时间

---

## 快速参考

### 触发构建

```bash
# {platform_name}: 手动触发
# 参考平台文档执行手动触发操作
```

### 查看构建状态

```bash
# 查看最近的构建
# 参考平台文档使用 CLI 工具
```

### 回滚部署

```bash
# 回滚到上一个版本
# 参考部署工具文档
```

---

## 最佳实践

1. **快速反馈**：CI 流程控制在 5 分钟内
2. **测试覆盖**：单元测试覆盖率 > 80%
3. **安全扫描**：定期进行依赖漏洞扫描
4. **环境隔离**：开发、测试、生产环境隔离
5. **监控告警**：部署后监控服务状态
6. **版本标记**：使用语义化版本号

---

## 参考资源

- [{platform_name} 文档](https://docs.example.com)

---

**最后更新**: 自动生成
"""
    
    def _get_secrets_config_guide(self, platform: str) -> str:
        """获取 Secrets 配置指南"""
        
        if platform == 'github':
            return """
1. 进入项目 Settings
2. 点击 Secrets and variables → Actions
3. 点击 New repository secret
4. 添加所需 Secrets
"""
        
        elif platform == 'gitlab':
            return """
1. 进入项目 Settings → CI/CD
2. 点击 Variables
3. 添加所需 Variables
4. 勾选 Mask variable
"""
        
        elif platform == 'jenkins':
            return """
1. 进入 Jenkins 系统配置
2. 点击 Configure System
3. 添加 Global credentials
4. 在 Pipeline 中使用
"""
        
        return "参考平台文档进行配置"
    
    def generate(self, platform: Optional[str] = None):
        """生成 CI/CD 文档和配置"""
        
        platform = platform or self._detect_platform()
        language = self._detect_language()
        project_type = self._detect_project_type()
        
        print(f"检测到 CI/CD 平台: {platform}")
        print(f"检测到项目语言: {language}")
        print(f"检测到项目类型: {project_type}")
        
        # 生成配置文件
        config_content = ""
        config_path = ""
        
        if platform == 'github':
            config_content = self._generate_github_actions_workflow(language)
            config_path = self.project_path / ".github" / "workflows" / "ci.yml"
        elif platform == 'gitlab':
            config_content = self._generate_gitlab_ci_config(language)
            config_path = self.project_path / ".gitlab-ci.yml"
        elif platform == 'jenkins':
            # Jenkinsfile 较复杂，这里生成简化版
            config_content = """pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'echo "Running tests..."'
            }
        }
        stage('Build') {
            steps {
                sh 'echo "Building..."'
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'echo "Deploying..."'
            }
        }
    }
}
"""
            config_path = self.project_path / "Jenkinsfile"
        
        # 保存配置文件
        if config_content and config_path:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(config_content)
            print(f"配置文件已生成: {config_path}")
        
        # 生成文档
        doc_content = self._generate_cicd_document(platform, language, project_type)
        doc_path = Path(self.wiki_path) / "CI-CD.md"
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        print(f"CI/CD 文档已生成: {doc_path}")
        
        return {
            'config_path': str(config_path) if config_path else None,
            'doc_path': str(doc_path),
            'platform': platform,
            'language': language
        }


def main():
    parser = argparse.ArgumentParser(description='生成 CI/CD 配置和文档')
    parser.add_argument('--path', type=str, default='.', help='项目路径')
    parser.add_argument('--platform', type=str, choices=['github', 'gitlab', 'jenkins'],
                        help='指定 CI/CD 平台（自动检测）')
    parser.add_argument('--wiki-path', type=str, help='Wiki 文档输出路径')
    
    args = parser.parse_args()
    
    generator = CICDGenerator(args.path, args.wiki_path)
    result = generator.generate(args.platform)
    
    print(f"\n生成完成:")
    print(f"  平台: {result['platform']}")
    print(f"  语言: {result['language']}")
    if result['config_path']:
        print(f"  配置: {result['config_path']}")
    print(f"  文档: {result['doc_path']}")


if __name__ == '__main__':
    main()
