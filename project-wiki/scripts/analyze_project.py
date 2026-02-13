#!/usr/bin/env python3
"""
项目结构分析脚本
功能：识别语言、框架、构建工具，分析项目结构
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Optional


class ProjectAnalyzer:
    """项目分析器"""
    
    # 语言识别规则
    LANGUAGE_PATTERNS = {
        'Python': ['.py', 'requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
        'JavaScript': ['.js', '.ts', '.jsx', '.tsx', 'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'],
        'Java': ['.java', 'pom.xml', 'build.gradle', 'gradle.properties'],
        'Go': ['.go', 'go.mod', 'go.sum', 'Gopkg.toml'],
        'Rust': ['.rs', 'Cargo.toml', 'Cargo.lock'],
        'C/C++': ['.c', '.cpp', '.h', '.hpp', 'CMakeLists.txt', 'Makefile'],
        'Ruby': ['.rb', 'Gemfile', 'Rakefile'],
        'PHP': ['.php', 'composer.json'],
        'Dart': ['.dart', 'pubspec.yaml'],
    }
    
    # 框架识别规则
    FRAMEWORK_PATTERNS = {
        'Flask': ['requirements.txt:flask', 'app.py:@app.route'],
        'Django': ['requirements.txt:django', 'settings.py:SECRET_KEY', 'manage.py'],
        'FastAPI': ['requirements.txt:fastapi', 'main.py:@app.get', 'main.py:@app.post', 'main.py:@app.route'],
        'React': ['package.json:react', 'src/App.jsx', 'src/App.tsx'],
        'Vue': ['package.json:vue', 'src/App.vue', 'vue.config.js', 'vue.config.ts'],
        'Angular': ['package.json:@angular', 'angular.json'],
        'Svelte': ['package.json:svelte', 'svelte.config.js', 'src/routes', '.svelte'],
        'SolidJS': ['package.json:solid-js', 'solid.config.ts'],
        'Spring Boot': ['pom.xml:spring-boot', 'build.gradle:spring-boot', '@SpringBootApplication'],
        'Express': ['package.json:express', 'app.js:express()'],
        'Next.js': ['package.json:next', 'next.config.js'],
        'Electron': ['package.json:electron', 'main.js', 'main.ts', 'electron-builder.yml'],
        'Tauri': ['src-tauri/tauri.conf.json', 'src-tauri/Cargo.toml'],
        'Wails': ['wails.json', 'go.mod', 'frontend/'],
        'Gin': ['go.mod', 'main.go:router.GET', 'main.go:router.POST', 'gin-gonic/gin'],
        'Flutter': ['pubspec.yaml', 'lib/main.dart', 'android/', 'ios/'],
    }
    
    # 构建工具识别规则
    BUILD_TOOLS = {
        'npm': ['package.json'],
        'pip': ['requirements.txt', 'setup.py', 'pyproject.toml'],
        'maven': ['pom.xml'],
        'gradle': ['build.gradle', 'settings.gradle', 'gradlew'],
        'make': ['Makefile'],
        'cmake': ['CMakeLists.txt'],
        'cargo': ['Cargo.toml'],
        'go modules': ['go.mod'],
    }
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.result = {
            'languages': [],
            'frameworks': [],
            'build_tools': [],
            'project_structure': {},
            'directories': [],
            'configuration_files': []
        }
    
    def analyze(self) -> Dict:
        """执行分析"""
        print(f"分析项目: {self.project_path}")
        
        if not self.project_path.exists():
            raise FileNotFoundError(f"项目路径不存在: {self.project_path}")
        
        # 收集所有文件
        all_files = list(self.project_path.rglob('*'))
        all_files = [f for f in all_files if f.is_file()]
        
        # 识别语言
        self._detect_languages(all_files)
        
        # 识别框架
        self._detect_frameworks(all_files)
        
        # 识别构建工具
        self._detect_build_tools(all_files)
        
        # 分析目录结构
        self._analyze_directory_structure()
        
        # 收集配置文件
        self._collect_config_files(all_files)
        
        return self.result
    
    def _detect_languages(self, files: List[Path]):
        """检测编程语言"""
        file_extensions = set()
        for file in files:
            # 跳过虚拟环境等目录
            if self._should_skip_file(file):
                continue
            file_extensions.add(file.suffix.lower())
        
        detected = []
        for lang, patterns in self.LANGUAGE_PATTERNS.items():
            for pattern in patterns:
                if pattern.startswith('.'):
                    if pattern in file_extensions:
                        detected.append(lang)
                        break
                else:
                    # 检查特定文件
                    config_file = pattern
                    if ':' in config_file:
                        config_file = config_file.split(':')[0]
                    config_path = self.project_path / config_file
                    if config_path.exists() and not self._should_skip_file(config_path):
                        detected.append(lang)
                        break
        
        self.result['languages'] = list(set(detected))
    
    def _detect_frameworks(self, files: List[Path]):
        """检测框架"""
        detected = []
        
        for framework, patterns in self.FRAMEWORK_PATTERNS.items():
            for pattern in patterns:
                if ':' in pattern:
                    # 文件:关键词 模式
                    filename, keyword = pattern.split(':')
                    file_path = self.project_path / filename
                    if file_path.exists() and not self._should_skip_file(file_path):
                        try:
                            content = file_path.read_text(encoding='utf-8', errors='ignore')
                            if keyword in content:
                                detected.append(framework)
                                break
                        except:
                            pass
                elif pattern.startswith('.'):
                    # 文件扩展名模式 (如 .svelte, .tsx)
                    # 检查是否存在该扩展名的文件
                    for file in files:
                        if file.suffix == pattern and not self._should_skip_file(file):
                            detected.append(framework)
                            break
                else:
                    # 路径模式 (如 src-tauri/, src/App.vue)
                    # 先检查是否是目录
                    target_path = self.project_path / pattern
                    if target_path.exists():
                        detected.append(framework)
                        break
                    # 如果不是直接路径，检查文件名
                    for file in files:
                        if pattern in str(file) and not self._should_skip_file(file):
                            detected.append(framework)
                            break
        
        self.result['frameworks'] = list(set(detected))
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """判断是否应该跳过该文件（避免在虚拟环境中检测）"""
        skip_patterns = ['node_modules', 'venv', '__pycache__', '.git', 'dist', 'build', '.tox', '.pytest_cache']
        path_str = str(file_path)
        for pattern in skip_patterns:
            if pattern in path_str:
                return True
        return False
    
    def _detect_build_tools(self, files: List[Path]):
        """检测构建工具"""
        detected = []
        
        for tool, patterns in self.BUILD_TOOLS.items():
            for pattern in patterns:
                config_path = self.project_path / pattern
                if config_path.exists() and not self._should_skip_file(config_path):
                    detected.append(tool)
                    break
        
        self.result['build_tools'] = list(set(detected))
    
    def _analyze_directory_structure(self):
        """分析目录结构"""
        self.result['project_structure'] = self._build_dir_tree(self.project_path, self.project_path)
        
        # 收集主要目录
        directories = [d.name for d in self.project_path.iterdir() if d.is_dir()]
        directories = [d for d in directories if not d.startswith('.')]
        self.result['directories'] = directories
    
    def _build_dir_tree(self, current_path: Path, root_path: Path, max_depth: int = 3) -> Dict:
        """构建目录树"""
        if max_depth <= 0:
            return {
                'type': 'directory',
                'name': current_path.name,
                'children': []
            }
        
        children = []
        try:
            for item in sorted(current_path.iterdir()):
                # 跳过隐藏文件和目录
                if item.name.startswith('.'):
                    continue
                
                # 跳过虚拟环境等目录
                if self._should_skip_file(item):
                    continue
                
                if item.is_file():
                    children.append({
                        'type': 'file',
                        'name': item.name
                    })
                elif item.is_dir():
                    children.append(self._build_dir_tree(item, root_path, max_depth - 1))
        except PermissionError:
            pass
        
        return {
            'type': 'directory',
            'name': current_path.name,
            'children': children
        }
    
    def _collect_config_files(self, files: List[Path]):
        """收集配置文件"""
        config_patterns = [
            'package.json', 'pom.xml', 'build.gradle', 'requirements.txt',
            'setup.py', 'pyproject.toml', 'Cargo.toml', 'go.mod',
            'Gemfile', 'composer.json', 'tsconfig.json', '.babelrc',
            'webpack.config.js', 'vite.config.js', 'vue.config.js',
            'angular.json', 'next.config.js', 'svelte.config.js',
            'solid.config.ts', 'settings.py', 'settings.gradle',
            'application.properties', 'application.yml', 'application.yaml'
        ]
        
        config_files = []
        for file in files:
            if file.name in config_patterns:
                config_files.append(file.name)
        
        self.result['configuration_files'] = list(set(config_files))


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='项目结构分析工具')
    parser.add_argument('--path', type=str, default='.', help='项目路径')
    
    args = parser.parse_args()
    
    analyzer = ProjectAnalyzer(args.path)
    result = analyzer.analyze()
    
    # 保存结果
    output_file = Path(args.path) / 'project-analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n分析完成！结果已保存到: {output_file}")
    print(f"检测到的语言: {', '.join(result['languages']) if result['languages'] else '未检测到'}")
    print(f"检测到的框架: {', '.join(result['frameworks']) if result['frameworks'] else '未检测到'}")
    print(f"检测到的构建工具: {', '.join(result['build_tools']) if result['build_tools'] else '未检测到'}")


if __name__ == '__main__':
    main()
