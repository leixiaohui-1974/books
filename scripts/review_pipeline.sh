#!/bin/bash
# ============================================================
# CHS 一键评审管线 (review_pipeline.sh)
#
# 用法:
#   ./review_pipeline.sh T2-CN              # 对 T2-CN 全书运行自动化检查
#   ./review_pipeline.sh T1-CN ch05         # 对 T1-CN 某章运行检查
#   ./review_pipeline.sh T2-CN --json       # JSON 输出
#   ./review_pipeline.sh T1-CN --pattern "ch*_final.md"  # 指定文件模式
#
# 依赖:
#   - Python 3.6+
#   - termcheck_v2.py（同目录）
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOKS_DIR="$(cd "$SCRIPT_DIR/../books" && pwd)"
REVIEWS_DIR="$(cd "$SCRIPT_DIR/../reviews" 2>/dev/null && pwd || echo "$SCRIPT_DIR/../reviews")"
TERMCHECK="$SCRIPT_DIR/termcheck_v2.py"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认值
BOOK_NAME=""
CHAPTER=""
JSON_OUTPUT=false
FILE_PATTERN=""
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

usage() {
    echo "CHS 一键评审管线"
    echo ""
    echo "用法: $0 <书名> [章节] [选项]"
    echo ""
    echo "参数:"
    echo "  书名          T1-CN, T2-CN, T2a, T2b 等"
    echo "  章节          可选，如 ch05（不指定则检查全书）"
    echo ""
    echo "选项:"
    echo "  --json        输出 JSON 格式"
    echo "  --pattern P   文件匹配模式（如 'ch*_final.md'）"
    echo "  -h, --help    显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 T2-CN"
    echo "  $0 T1-CN ch05"
    echo "  $0 T1-CN --pattern 'ch*_final.md'"
    exit 0
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            usage
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --pattern)
            FILE_PATTERN="$2"
            shift 2
            ;;
        ch*)
            CHAPTER="$1"
            shift
            ;;
        *)
            if [[ -z "$BOOK_NAME" ]]; then
                BOOK_NAME="$1"
            fi
            shift
            ;;
    esac
done

if [[ -z "$BOOK_NAME" ]]; then
    echo -e "${RED}ERROR: 请指定书名 (如 T1-CN, T2-CN)${NC}"
    usage
fi

# 定位书稿目录
BOOK_DIR="$BOOKS_DIR/$BOOK_NAME"
if [[ ! -d "$BOOK_DIR" ]]; then
    echo -e "${RED}ERROR: 目录不存在: $BOOK_DIR${NC}"
    exit 1
fi

# 确保 reviews 目录存在
mkdir -p "$REVIEWS_DIR"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  CHS 评审管线  |  $BOOK_NAME  |  $TIMESTAMP${NC}"
echo -e "${BLUE}================================================${NC}"

# ============================================================
# Step 1: 基本统计
# ============================================================
echo -e "\n${YELLOW}[1/3] 基本统计...${NC}"

total_files=0
total_chars=0
total_lines=0

if [[ -n "$CHAPTER" ]]; then
    # 单章模式
    CHAPTER_FILES=$(find "$BOOK_DIR" -maxdepth 1 -name "${CHAPTER}*.md" ! -name "*_v1*" ! -name "*_backup*" | sort)
else
    # 全书模式
    if [[ -n "$FILE_PATTERN" ]]; then
        CHAPTER_FILES=$(find "$BOOK_DIR" -maxdepth 1 -name "$FILE_PATTERN" ! -name "*_v1*" ! -name "*_backup*" | sort)
    else
        CHAPTER_FILES=$(find "$BOOK_DIR" -maxdepth 1 -name "ch*.md" ! -name "*_v1*" ! -name "*_backup*" | sort)
    fi
fi

# 附加文件（前言、目录、术语表等）
EXTRA_FILES=$(find "$BOOK_DIR" -maxdepth 1 -name "0*.md" -o -name "9*.md" 2>/dev/null | sort)

echo -e "\n  章节文件列表:"
for f in $CHAPTER_FILES; do
    fname=$(basename "$f")
    chars=$(wc -m < "$f" 2>/dev/null || echo 0)
    lines=$(wc -l < "$f" 2>/dev/null || echo 0)
    # 中文字数粗估
    cn_chars=$(grep -oP '[\x{4e00}-\x{9fff}]' "$f" 2>/dev/null | wc -l || echo 0)
    echo -e "  - $fname  |  ${cn_chars}字  |  ${lines}行"
    total_files=$((total_files + 1))
    total_chars=$((total_chars + cn_chars))
    total_lines=$((total_lines + lines))
done

echo -e "\n  总计: ${total_files}个文件, ${total_chars}中文字, ${total_lines}行"

# ============================================================
# Step 2: termcheck_v2 质量检查
# ============================================================
echo -e "\n${YELLOW}[2/3] 术语与质量检查 (termcheck_v2)...${NC}"

REPORT_BASE="${BOOK_NAME}_review_v2_${TIMESTAMP}"

if [[ -n "$CHAPTER" ]]; then
    # 单章：对指定文件运行
    TARGET_FILE=$(echo "$CHAPTER_FILES" | head -1)
    if [[ -n "$TARGET_FILE" ]]; then
        if $JSON_OUTPUT; then
            python3 "$TERMCHECK" "$TARGET_FILE" --book "$BOOK_NAME" --json \
                -o "$REVIEWS_DIR/${REPORT_BASE}.json" 2>&1 || true
            echo -e "  JSON报告: $REVIEWS_DIR/${REPORT_BASE}.json"
        else
            python3 "$TERMCHECK" "$TARGET_FILE" --book "$BOOK_NAME" --verbose \
                -o "$REVIEWS_DIR/${REPORT_BASE}.txt" 2>&1 || true
            # 同时生成 JSON 备份
            python3 "$TERMCHECK" "$TARGET_FILE" --book "$BOOK_NAME" --json \
                -o "$REVIEWS_DIR/${REPORT_BASE}.json" 2>&1 || true
            echo -e "  文本报告: $REVIEWS_DIR/${REPORT_BASE}.txt"
            echo -e "  JSON报告: $REVIEWS_DIR/${REPORT_BASE}.json"
        fi
    fi
else
    # 全书：对整个目录运行
    TERMCHECK_ARGS="--book $BOOK_NAME --verbose"
    if [[ -n "$FILE_PATTERN" ]]; then
        TERMCHECK_ARGS="$TERMCHECK_ARGS --pattern $FILE_PATTERN"
    fi

    if $JSON_OUTPUT; then
        python3 "$TERMCHECK" "$BOOK_DIR" $TERMCHECK_ARGS --json \
            -o "$REVIEWS_DIR/${REPORT_BASE}.json" 2>&1 || true
        echo -e "  JSON报告: $REVIEWS_DIR/${REPORT_BASE}.json"
    else
        python3 "$TERMCHECK" "$BOOK_DIR" $TERMCHECK_ARGS \
            -o "$REVIEWS_DIR/${REPORT_BASE}.txt" 2>&1 || true
        python3 "$TERMCHECK" "$BOOK_DIR" $TERMCHECK_ARGS --json \
            -o "$REVIEWS_DIR/${REPORT_BASE}.json" 2>&1 || true
        echo -e "  文本报告: $REVIEWS_DIR/${REPORT_BASE}.txt"
        echo -e "  JSON报告: $REVIEWS_DIR/${REPORT_BASE}.json"
    fi
fi

# ============================================================
# Step 3: 汇总与判定
# ============================================================
echo -e "\n${YELLOW}[3/3] 汇总报告...${NC}"

# 读取 JSON 报告提取关键指标
if [[ -f "$REVIEWS_DIR/${REPORT_BASE}.json" ]]; then
    CRITICAL=$(python3 -c "
import json, sys
with open('$REVIEWS_DIR/${REPORT_BASE}.json') as f:
    r = json.load(f)
o = r.get('overall', {})
print(f\"Critical: {o.get('total_critical', 0)}\")
print(f\"Major: {o.get('total_major', 0)}\")
print(f\"Minor: {o.get('total_minor', 0)}\")
print(f\"Verdict: {o.get('verdict', 'N/A')}\")
print(f\"TotalChars: {o.get('total_cn_chars', 0)}\")
" 2>/dev/null || echo "解析失败")

    echo -e "\n${BLUE}─────────────────────────────────────${NC}"
    echo -e "  $CRITICAL"
    echo -e "${BLUE}─────────────────────────────────────${NC}"

    # 判断是否通过
    crit_count=$(echo "$CRITICAL" | grep "Critical:" | awk '{print $2}')
    if [[ "$crit_count" == "0" ]]; then
        echo -e "\n  ${GREEN}PASS: 无 Critical 问题${NC}"
    else
        echo -e "\n  ${RED}FAIL: 存在 ${crit_count} 个 Critical 问题，须修复${NC}"
    fi
fi

echo -e "\n${BLUE}================================================${NC}"
echo -e "${BLUE}  评审完成  |  报告保存在 reviews/ 目录${NC}"
echo -e "${BLUE}================================================${NC}\n"
