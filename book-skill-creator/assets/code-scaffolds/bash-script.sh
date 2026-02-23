#!/bin/bash
###############################################################################
# 通用 Bash 脚本脚手架
# 适用于各类系统级任务，提供参数解析、日志记录、错误处理等基础设施
###############################################################################

set -euo pipefail  # 严格模式：遇到错误立即退出

###############################################################################
# 配置和变量
###############################################################################

# 脚本名称
SCRIPT_NAME="$(basename "$0")"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 默认值
INPUT_FILE=""
OUTPUT_DIR="./output"
CONFIG_FILE=""
VERBOSE=false
DRY_RUN=false

# 颜色定义（如果终端支持）
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

###############################################################################
# 工具函数
###############################################################################

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

log_debug() {
    if [ "$VERBOSE" = true ]; then
        echo -e "[DEBUG] $*" >&2
    fi
}

# 显示帮助信息
show_help() {
    cat << EOF
使用方法: $SCRIPT_NAME [选项]

选项:
  -i, --input FILE      输入文件路径（必需）
  -o, --output DIR      输出目录路径（默认: ./output）
  -c, --config FILE     配置文件路径
  -v, --verbose         启用详细日志
  -d, --dry-run         模拟运行，不实际执行
  -h, --help            显示此帮助信息

示例:
  $SCRIPT_NAME --input data.csv --output result.csv
  $SCRIPT_NAME -i data.txt -o output/ --verbose
  $SCRIPT_NAME -i data.json -c config.yaml --dry-run

EOF
}

# 解析命令行参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -i|--input)
                INPUT_FILE="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            -c|--config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# 验证参数
validate_args() {
    # 检查必需参数
    if [ -z "$INPUT_FILE" ]; then
        log_error "缺少必需参数: --input"
        show_help
        exit 1
    fi

    # 检查输入文件是否存在
    if [ ! -f "$INPUT_FILE" ]; then
        log_error "输入文件不存在: $INPUT_FILE"
        exit 1
    fi

    # 检查配置文件是否存在（如果指定）
    if [ -n "$CONFIG_FILE" ] && [ ! -f "$CONFIG_FILE" ]; then
        log_error "配置文件不存在: $CONFIG_FILE"
        exit 1
    fi

    log_info "参数验证通过"
}

# 创建输出目录
create_output_dir() {
    if [ "$DRY_RUN" = false ]; then
        mkdir -p "$OUTPUT_DIR"
        log_info "创建输出目录: $OUTPUT_DIR"
    else
        log_debug "（模拟）创建输出目录: $OUTPUT_DIR"
    fi
}

# 加载配置文件
load_config() {
    if [ -n "$CONFIG_FILE" ]; then
        log_info "加载配置文件: $CONFIG_FILE"
        # 根据文件扩展名选择加载方式
        case "$CONFIG_FILE" in
            *.json)
                # JSON 配置需要 jq 工具
                if command -v jq &> /dev/null; then
                    log_debug "配置内容: $(jq '.' "$CONFIG_FILE")"
                else
                    log_warn "未安装 jq，无法解析 JSON 配置"
                fi
                ;;
            *.yaml|*.yml)
                # YAML 配置需要 yq 工具
                if command -v yq &> /dev/null; then
                    log_debug "配置内容: $(yq eval '.' "$CONFIG_FILE")"
                else
                    log_warn "未安装 yq，无法解析 YAML 配置"
                fi
                ;;
        esac
    fi
}

# 主处理逻辑
process() {
    log_info "开始处理: $INPUT_FILE"
    log_debug "输出目录: $OUTPUT_DIR"
    log_debug "配置文件: ${CONFIG_FILE:-未指定}"

    # TODO: 在此处实现具体的处理逻辑

    # 示例：读取输入文件
    log_info "读取输入文件..."
    INPUT_SIZE=$(stat -f%z "$INPUT_FILE" 2>/dev/null || stat -c%s "$INPUT_FILE")
    log_debug "文件大小: $INPUT_SIZE 字节"

    # 示例：执行处理
    log_info "执行处理逻辑..."
    if [ "$DRY_RUN" = true ]; then
        log_warn "（模拟运行）跳过实际处理"
    else
        # 实际处理代码
        # OUTPUT_FILE="$OUTPUT_DIR/$(basename "$INPUT_FILE")"
        # cp "$INPUT_FILE" "$OUTPUT_FILE"
        # log_info "处理完成: $OUTPUT_FILE"
        log_debug "（占位）实际处理代码在此处"
    fi

    log_info "处理完成"
    return 0
}

# 清理函数（脚本退出时调用）
cleanup() {
    log_debug "执行清理..."
    # TODO: 添加清理逻辑（如临时文件删除等）
}

###############################################################################
# 主执行流程
###############################################################################

main() {
    # 设置退出时的清理函数
    trap cleanup EXIT

    # 显示启动信息
    log_info "启动脚本: $SCRIPT_NAME"

    # 解析和验证参数
    parse_args "$@"
    validate_args

    # 准备环境
    create_output_dir
    load_config

    # 执行处理
    process

    log_info "脚本执行完成"
}

# 执行主函数
main "$@"
