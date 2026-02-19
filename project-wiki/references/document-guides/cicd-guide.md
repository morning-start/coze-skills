# CI/CD 文档指南

## 目录

1. [概览](#概览)
2. [CI/CD 流程设计](#cicd-流程设计)
3. [主流 CI/CD 平台](#主流-cicd-平台)
4. [配置文件规范](#配置文件规范)
5. [文档模板](#文档模板)

---

## 概览

### 定义

**CI/CD 文档** 是持续集成和持续部署的配置指南，记录自动化构建、测试、部署的流程和配置。

### 核心价值

- **标准化流程**：统一团队的开发和部署流程
- **自动化效率**：减少手动操作，提升开发效率
- **质量保障**：自动化测试确保代码质量
- **快速迭代**：加速发布周期

### 适用场景

✅ 需要创建 CI/CD 文档的项目：
- 有自动化构建需求的项目
- 需要多环境部署的项目
- 团队协作开发的项目
- 有持续集成测试需求的项目

❌ 可以不创建 CI/CD 文档的项目：
- 纯静态网站项目（使用 GitHub Pages）
- 简单的个人项目
- 无自动化部署需求的项目

### 识别标志

项目可能需要 CI/CD 的信号：
- 存在 Dockerfile 或 docker-compose.yml
- 存在 k8s/ Kubernetes 配置文件
- 存在部署脚本（deploy.sh、Makefile 等）
- 存在测试配置（pytest.ini、jest.config.js 等）
- 使用打包工具（npm、maven、cargo 等）

---

## CI/CD 流程设计

### 标准流程

```
代码提交 → 代码检查 → 依赖安装 → 单元测试 → 构建打包 → 部署环境 → 集成测试 → 发布
```

### 流程详解

#### 1. 代码检查 (Lint)
- 代码风格检查（ESLint、Pylint、Checkstyle）
- 静态分析（SonarQube）
- 安全扫描（Snyk、Trivy）

#### 2. 依赖安装
- 下载项目依赖
- 缓存依赖包（提升构建速度）

#### 3. 单元测试
- 执行单元测试
- 生成测试覆盖率报告
- 测试失败则阻断流程

#### 4. 构建打包
- 编译代码
- 生成可部署文件
- 构建镜像（如使用 Docker）

#### 5. 部署环境
- 部署到测试环境
- 部署到预发布环境
- 部署到生产环境（需要审批）

#### 6. 集成测试
- API 测试
- 端到端测试（E2E）
- 性能测试

---

## 主流 CI/CD 平台

### GitHub Actions

**适用场景**：
- GitHub 托管项目
- 需要 GitHub 集成的项目
- 开源项目

**配置文件位置**：`.github/workflows/`

**配置文件格式**：YAML

**优势**：
- 与 GitHub 无缝集成
- 免费额度充足
- 社区 Action 丰富

---

### GitLab CI

**适用场景**：
- GitLab 托管项目
- 企业内部项目
- 需要 DevOps 工具链的项目

**配置文件位置**：`.gitlab-ci.yml`

**配置文件格式**：YAML

**优势**：
- 内置 Docker Registry
- 完整的 DevOps 工具链
- 企业级功能

---

### Jenkins

**适用场景**：
- 复杂构建流程
- 企业级部署
- 需要自定义插件

**配置文件位置**：`Jenkinsfile`

**配置文件格式**：Groovy DSL

**优势**：
- 高度可定制
- 插件生态丰富
- 支持多节点构建

---

### 其他平台

- **CircleCI**：快速、易用
- **Travis CI**：开源项目友好
- **Drone CI**：轻量级、容器化
- **Azure Pipelines**：微软生态

---

## 配置文件规范

### GitHub Actions 配置示例

```yaml
name: CI/CD Pipeline

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
    
    - name: Build Docker image
      run: |
        docker build -t myapp:${{ github.sha }} .
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Push to Docker Hub
      run: |
        docker push myapp:${{ github.sha }}
        docker tag myapp:${{ github.sha }} myapp:latest
        docker push myapp:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        echo "Deploy to production"
        # 添加部署命令
```

---

### GitLab CI 配置示例

```yaml
stages:
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
  coverage: '/TOTAL.*\s+(\d+%)$/'
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
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker push $DOCKER_IMAGE
  only:
    - main

deploy_production:
  stage: deploy
  image: alpine:latest
  script:
    - echo "Deploy to production"
    - # 添加部署命令
  only:
    - main
  when: manual
```

---

### Jenkins 配置示例

```groovy
pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "myapp:${env.BUILD_ID}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Lint') {
            steps {
                sh 'pip install pylint'
                sh 'pylint src/'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pip install pytest pytest-cov'
                sh 'pytest --cov=src tests/'
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                input 'Deploy to production?'
                sh 'echo "Deploying ${DOCKER_IMAGE}"'
                // 添加部署命令
            }
        }
    }
    
    post {
        always {
            junit 'test-results/*.xml'
            publishHTML([
                reportDir: 'coverage/htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

---

## 文档模板

### CI/CD 文档模板

```markdown
# CI/CD 指南

## 概览

本文档记录项目的持续集成和持续部署流程。

## CI/CD 平台

本项目使用 **[平台名称]** 进行 CI/CD。

- 平台: [GitHub Actions | GitLab CI | Jenkins]
- 配置文件: [配置文件路径]
- 状态徽章: ![CI Status](...)

---

## 流程说明

### 持续集成 (CI)

#### 触发条件

- 推送到 `main` 或 `develop` 分支
- 创建 Pull Request
- 手动触发

#### CI 流程

1. **代码检查** (Lint)
   - 工具: [ESLint | Pylint | Checkstyle]
   - 配置文件: [配置文件路径]
   - 失败策略: 阻断后续流程

2. **单元测试** (Test)
   - 工具: [Jest | Pytest | JUnit]
   - 配置文件: [配置文件路径]
   - 覆盖率要求: > 80%
   - 失败策略: 阻断后续流程

3. **构建** (Build)
   - 编译代码
   - 生成构建产物
   - 构建时间: 约 2-3 分钟

### 持续部署 (CD)

#### 部署环境

| 环境 | 用途 | 触发条件 | 审批 |
|------|------|----------|------|
| 开发环境 | 日常开发 | 推送 `develop` 分支 | 自动 |
| 测试环境 | 测试验证 | 推送 `main` 分支 | 自动 |
| 生产环境 | 线上发布 | 推送 `main` 分支 | 手动审批 |

#### 部署流程

1. **构建镜像**
   - 基于 Docker
   - 镜像仓库: [Docker Hub | Harbor]
   - 标签: `$(git rev-parse --short HEAD)`

2. **部署到环境**
   - 工具: [Kubectl | Docker Compose | Ansible]
   - 滚动更新策略: 逐步替换
   - 健康检查: 等待服务就绪

3. **部署后验证**
   - 运行集成测试
   - 检查日志
   - 监控指标

---

## 配置说明

### 环境变量

| 变量名 | 说明 | 来源 |
|--------|------|------|
| `DOCKER_USERNAME` | Docker Hub 用户名 | Secrets |
| `DOCKER_PASSWORD` | Docker Hub 密码 | Secrets |
| `DATABASE_URL` | 数据库连接 | Secrets |
| `API_KEY` | API 密钥 | Secrets |

### Secrets 配置

**GitHub Actions**：
1. 进入项目 Settings
2. 点击 Secrets and variables → Actions
3. 点击 New repository secret
4. 添加所需 Secrets

**GitLab CI**：
1. 进入项目 Settings → CI/CD
2. 点击 Variables
3. 添加所需 Variables
4. 勾选 Mask variable

**Jenkins**：
1. 进入 Jenkins 系统配置
2. 点击 Configure System
3. 添加 Global credentials
4. 在 Pipeline 中使用

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
3. 重新提交

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
# GitHub Actions: 手动触发
# 进入 Actions 页面 → 选择 Workflow → Run workflow

# GitLab CI: 手动触发
# 进入 CI/CD → Pipelines → Run pipeline

# Jenkins: 手动触发
# 点击 Build Now
```

### 查看构建状态

```bash
# 查看最近 10 次构建
gh run list --limit 10

# 查看构建详情
gh run view <run-id>
```

### 回滚部署

```bash
# 回滚到上一个版本
# Kubernetes
kubectl rollout undo deployment/<deployment-name>

# Docker Compose
docker-compose down
docker-compose up -d --scale app=1
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

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [GitLab CI 文档](https://docs.gitlab.com/ee/ci/)
- [Jenkins 文档](https://www.jenkins.io/doc/)
```

---

## 最佳实践

### ✅ 推荐做法

1. **快速反馈**：
   - CI 流程控制在 5 分钟内
   - 优先运行快速测试
   - 缓存依赖包

2. **测试分层**：
   - 单元测试（快速）
   - 集成测试（中等）
   - E2E 测试（慢，可选）

3. **安全优先**：
   - 使用 Secrets 管理敏感信息
   - 定期更新依赖
   - 进行安全扫描

4. **监控告警**：
   - 部署后验证
   - 监控服务状态
   - 设置告警规则

### ❌ 避免做法

1. **混合职责**：
   - CI 和 CD 分离
   - CI 关注代码质量
   - CD 关注部署流程

2. **缺少回滚**：
   - 始终保留回滚能力
   - 记录部署历史
   - 快速回滚机制

3. **过度复杂**：
   - 简化流程
   - 避免不必要的步骤
   - 保持可维护性
