#!/bin/bash

# T1-CN 内容逻辑检查脚本
# 检查：章节递进、概念连贯、论证完整

cd "$(dirname "$0")"

echo "========================================"
echo "内容逻辑检查 - T1-CN 全书"
echo "========================================"
echo ""

# 创建临时文件
REPORT="/tmp/content_logic_report.txt"
> "$REPORT"

# 检查每个章节的核心概念和递进关系
echo "【检查项 1】：章节标题和层级结构" | tee -a "$REPORT"
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    title=$(head -20 "$file" | grep "^# " | head -1)
    echo "  Ch$(printf "%02d" "$ch_num"): $title" | tee -a "$REPORT"
  fi
done
echo "" | tee -a "$REPORT"

# 检查章节长度（字数）
echo "【检查项 2】：章节长度分布" | tee -a "$REPORT"
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    char_count=$(wc -m < "$file")
    char_count=$((char_count / 1000))  # 转换为千字
    printf "  Ch$(printf "%02d" "$ch_num"): %d K字符\n" "$char_count" | tee -a "$REPORT"
  fi
done
echo "" | tee -a "$REPORT"

# 检查关键概念第一次出现的章节
echo "【检查项 3】：关键概念出现位置" | tee -a "$REPORT"

declare -A concepts
concepts["CHS"]="水系统控制论"
concepts["WNAL"]="水网自主等级"
concepts["ODD"]="运行设计域"
concepts["HDC"]="分层分布式控制"
concepts["HydroOS"]="水网操作系统"

for concept in "${!concepts[@]}"; do
  full_name="${concepts[$concept]}"
  for file in ch{01..15}_final.md; do
    if [ -f "$file" ]; then
      ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
      count=$(grep -o "$concept" "$file" | wc -l)
      if [ "$count" -gt 0 ]; then
        echo "  $concept ($full_name): 首现于 Ch$(printf "%02d" "$ch_num")，共$count次" | tee -a "$REPORT"
        break
      fi
    fi
  done
done
echo "" | tee -a "$REPORT"

# 检查章节间的逻辑连接（通过"上一章"、"下一章"、"前面"等关键词）
echo "【检查项 4】：章节间逻辑连接关键词" | tee -a "$REPORT"
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 搜索参考前面章节的关键词
    cross_refs=$(grep -E "第[0-9]+章|前面|上述|如前|基于.*第" "$file" | wc -l)
    if [ "$cross_refs" -gt 0 ]; then
      echo "  Ch$(printf "%02d" "$ch_num"): 发现$cross_refs处章节间引用" | tee -a "$REPORT"
    fi
  fi
done
echo "" | tee -a "$REPORT"

# 检查每章的核心论点清晰度（通过 ## 二级标题数）
echo "【检查项 5】：逻辑段落数（## 二级标题）" | tee -a "$REPORT"
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    sec_count=$(grep "^## " "$file" | wc -l)
    echo "  Ch$(printf "%02d" "$ch_num"): $sec_count 个二级段落" | tee -a "$REPORT"
  fi
done
echo "" | tee -a "$REPORT"

# 检查引言和总结的存在
echo "【检查项 6】：引言和总结完整性" | tee -a "$REPORT"
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    has_intro=$(grep -E "^## .*引言|^## .*概述|^## .*背景" "$file" | wc -l)
    has_summary=$(grep -E "^## .*总结|^## .*结论|^## .*小结" "$file" | wc -l)
    status="❌"
    [ "$has_intro" -gt 0 ] && [ "$has_summary" -gt 0 ] && status="✅"
    printf "  Ch$(printf "%02d" "$ch_num"): %s (引言:%d 总结:%d)\n" "$status" "$has_intro" "$has_summary" | tee -a "$REPORT"
  fi
done
echo "" | tee -a "$REPORT"

cat "$REPORT"
