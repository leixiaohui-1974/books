#!/bin/bash

# T1-CN 参考文献检查脚本
# 检查：格式规范、来源真实、编号连续、引用完整

cd "$(dirname "$0")"

echo "========================================"
echo "参考文献完整性检查 - T1-CN 全书"
echo "========================================"
echo ""

REPORT="/tmp/references_report.txt"
> "$REPORT"

# 1. 统计每章的参考文献情况
echo "【检查项 1】：参考文献分布" | tee -a "$REPORT"
total_refs=0
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 统计 [X-N] 格式的参考文献标签
    ref_count=$(grep -o "\[$(printf "%02d" "$ch_num")-[0-9]*\]" "$file" | wc -l)
    ref_list_count=$(grep "^\[$(printf "%02d" "$ch_num")-" "$file" | wc -l)
    printf "  Ch$(printf "%02d" "$ch_num"): 引用%d次, 条目%d条\n" "$ref_count" "$ref_list_count" | tee -a "$REPORT"
    total_refs=$((total_refs + ref_count))
  fi
done
echo "  【全书总计】：引用 $total_refs 次" | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

# 2. 检查孤立引用
echo "【检查项 2】：孤立引用检测" | tee -a "$REPORT"
orphan_count=0
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 找出所有引用的编号
    cited=$(grep -o "\[$(printf "%02d" "$ch_num")-[0-9]*\]" "$file" | sed "s/\[$(printf "%02d" "$ch_num")-//g" | sed 's/\]//g' | sort -u)
    # 找出参考文献列表中存在的编号
    listed=$(grep "^\[$(printf "%02d" "$ch_num")-" "$file" | sed "s/^\[$(printf "%02d" "$ch_num")-//g" | sed 's/\].*//' | sort -u)
    
    # 比对找出孤立的
    for ref_num in $cited; do
      if ! echo "$listed" | grep -q "^$ref_num$"; then
        echo "  ❌ Ch$(printf "%02d" "$ch_num"): [$(printf "%02d" "$ch_num")-$ref_num] 无对应参考文献条目" | tee -a "$REPORT"
        orphan_count=$((orphan_count + 1))
      fi
    done
  fi
done
if [ "$orphan_count" -eq 0 ]; then
  echo "  ✅ 无孤立引用" | tee -a "$REPORT"
fi
echo "" | tee -a "$REPORT"

# 3. 检查参考文献编号连续性
echo "【检查项 3】：参考文献编号连续性" | tee -a "$REPORT"
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 提取该章的参考文献编号
    nums=$(grep "^\[$(printf "%02d" "$ch_num")-" "$file" | sed "s/^\[$(printf "%02d" "$ch_num")-//g" | sed 's/\].*//' | sort -n)
    
    if [ -z "$nums" ]; then
      continue
    fi
    
    # 检查是否连续
    first=$(echo "$nums" | head -1)
    last=$(echo "$nums" | tail -1)
    expected_count=$((last - first + 1))
    actual_count=$(echo "$nums" | wc -w)
    
    if [ "$expected_count" -eq "$actual_count" ]; then
      echo "  ✅ Ch$(printf "%02d" "$ch_num"): [$ch_num-$first] ~ [$ch_num-$last] 连续" | tee -a "$REPORT"
    else
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): [$ch_num-$first] ~ [$ch_num-$last] 有缺失，期望$expected_count条，实际$actual_count条" | tee -a "$REPORT"
    fi
  fi
done
echo "" | tee -a "$REPORT"

# 4. 检查参考文献格式规范
echo "【检查项 4】：参考文献格式规范检查" | tee -a "$REPORT"
format_errors=0
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 检查参考文献行的格式：应为 [X-N] 标题...
    invalid=$(grep "^\[$(printf "%02d" "$ch_num")-" "$file" | grep -v "^\[$(printf "%02d" "$ch_num")-[0-9]*\] " | wc -l)
    if [ "$invalid" -gt 0 ]; then
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): $invalid 条参考文献格式不规范" | tee -a "$REPORT"
      format_errors=$((format_errors + invalid))
    fi
  fi
done
if [ "$format_errors" -eq 0 ]; then
  echo "  ✅ 所有参考文献格式规范" | tee -a "$REPORT"
fi
echo "" | tee -a "$REPORT"

# 5. 检查待发表论文引用（违规检查）
echo "【检查项 5】：待发表论文引用检测（零容忍）" | tee -a "$REPORT"
violation_count=0
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 搜索常见的待发表论文标记
    violations=$(grep -E "待发表|待投|已投|正在审|在审|预印本|arXiv|未发表" "$file" | grep -E "\[[0-9]+-[0-9]+\]" | wc -l)
    if [ "$violations" -gt 0 ]; then
      echo "  ❌ Ch$(printf "%02d" "$ch_num"): 发现 $violations 处可能的待发表论文引用" | tee -a "$REPORT"
      violation_count=$((violation_count + violations))
    fi
  fi
done
if [ "$violation_count" -eq 0 ]; then
  echo "  ✅ 未发现待发表论文引用" | tee -a "$REPORT"
fi
echo "" | tee -a "$REPORT"

cat "$REPORT"
