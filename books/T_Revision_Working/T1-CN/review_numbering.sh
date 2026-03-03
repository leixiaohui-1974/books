#!/bin/bash

# T1-CN 编号系统检查脚本
# 检查：公式、表格、图表编号独立且连续、无重复

cd "$(dirname "$0")"

echo "========================================"
echo "编号系统一致性检查 - T1-CN 全书"
echo "========================================"
echo ""

REPORT="/tmp/numbering_report.txt"
> "$REPORT"

# 1. 检查编号系统独立性（公式 vs 表格 vs 图片）
echo "【检查项 1】：三类编号独立性" | tee -a "$REPORT"
echo "  检查：公式编号 (X-N)、表格编号 (表X-N)、图片编号 (图X-N) 是否独立" | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    
    # 提取各类编号
    formula_nums=$(grep -o "($ch_num-[0-9]*)" "$file" | sed "s/($ch_num-//g" | sed 's/)//g' | sort -u | wc -l)
    table_nums=$(grep -oE "表$ch_num-[0-9]+" "$file" | sed "s/表$ch_num-//g" | sort -u | wc -l)
    fig_nums=$(grep -oE "图$ch_num-[0-9]+" "$file" | sed "s/图$ch_num-//g" | sort -u | wc -l)
    
    if [ "$formula_nums" -gt 0 ] || [ "$table_nums" -gt 0 ] || [ "$fig_nums" -gt 0 ]; then
      printf "  Ch$(printf "%02d" "$ch_num"): 公式%d 表格%d 图片%d\n" "$formula_nums" "$table_nums" "$fig_nums" | tee -a "$REPORT"
    fi
  fi
done
echo "" | tee -a "$REPORT"

# 2. 检查编号重复
echo "【检查项 2】：编号重复检测" | tee -a "$REPORT"
dup_count=0

for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    
    # 检查公式编号重复
    formula_dups=$(grep -o "($ch_num-[0-9]*)" "$file" | sort | uniq -d | wc -l)
    if [ "$formula_dups" -gt 0 ]; then
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): $formula_dups 个重复的公式编号" | tee -a "$REPORT"
      dup_count=$((dup_count + formula_dups))
    fi
    
    # 检查表格编号重复
    table_dups=$(grep -oE "表$ch_num-[0-9]+" "$file" | sort | uniq -d | wc -l)
    if [ "$table_dups" -gt 0 ]; then
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): $table_dups 个重复的表格编号" | tee -a "$REPORT"
      dup_count=$((dup_count + table_dups))
    fi
    
    # 检查图片编号重复
    fig_dups=$(grep -oE "图$ch_num-[0-9]+" "$file" | sort | uniq -d | wc -l)
    if [ "$fig_dups" -gt 0 ]; then
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): $fig_dups 个重复的图片编号" | tee -a "$REPORT"
      dup_count=$((dup_count + fig_dups))
    fi
  fi
done

if [ "$dup_count" -eq 0 ]; then
  echo "  ✅ 无编号重复" | tee -a "$REPORT"
fi
echo "" | tee -a "$REPORT"

# 3. 检查编号连续性（全面）
echo "【检查项 3】：编号连续性综合检查" | tee -a "$REPORT"

for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    
    # 公式编号
    formula_nums=$(grep -o "($ch_num-[0-9]*)" "$file" | sed "s/($ch_num-//g" | sed 's/)//g' | sort -n | uniq)
    if [ -n "$formula_nums" ]; then
      first=$(echo "$formula_nums" | head -1)
      last=$(echo "$formula_nums" | tail -1)
      expected=$((last - first + 1))
      actual=$(echo "$formula_nums" | wc -w)
      if [ "$expected" -ne "$actual" ]; then
        echo "  ⚠️ Ch$(printf "%02d" "$ch_num") 公式：($ch_num-$first)~($ch_num-$last) 应有$expected个，实际$actual个" | tee -a "$REPORT"
      fi
    fi
    
    # 表格编号
    table_nums=$(grep -oE "表$ch_num-[0-9]+" "$file" | sed "s/表$ch_num-//g" | sort -n | uniq)
    if [ -n "$table_nums" ]; then
      first=$(echo "$table_nums" | head -1)
      last=$(echo "$table_nums" | tail -1)
      expected=$((last - first + 1))
      actual=$(echo "$table_nums" | wc -w)
      if [ "$expected" -ne "$actual" ]; then
        echo "  ⚠️ Ch$(printf "%02d" "$ch_num") 表格：表$ch_num-$first~表$ch_num-$last 应有$expected个，实际$actual个" | tee -a "$REPORT"
      fi
    fi
    
    # 图片编号
    fig_nums=$(grep -oE "图$ch_num-[0-9]+" "$file" | sed "s/图$ch_num-//g" | sort -n | uniq)
    if [ -n "$fig_nums" ]; then
      first=$(echo "$fig_nums" | head -1)
      last=$(echo "$fig_nums" | tail -1)
      expected=$((last - first + 1))
      actual=$(echo "$fig_nums" | wc -w)
      if [ "$expected" -ne "$actual" ]; then
        echo "  ⚠️ Ch$(printf "%02d" "$ch_num") 图片：图$ch_num-$first~图$ch_num-$last 应有$expected个，实际$actual个" | tee -a "$REPORT"
      fi
    fi
  fi
done
echo "" | tee -a "$REPORT"

# 4. 检查编号格式规范
echo "【检查项 4】：编号格式规范" | tee -a "$REPORT"
format_errors=0

for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    
    # 检查非标准编号格式
    # 例如：式(X-N) vs (X-N)、表 X-N vs 表X-N
    bad_formula=$(grep -E '\(0?[0-9]+-[0-9]+\)' "$file" | grep -v "($ch_num-" | wc -l)
    if [ "$bad_formula" -gt 0 ]; then
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): $bad_formula 处公式编号格式非标准" | tee -a "$REPORT"
      format_errors=$((format_errors + bad_formula))
    fi
  fi
done

if [ "$format_errors" -eq 0 ]; then
  echo "  ✅ 所有编号格式规范" | tee -a "$REPORT"
fi
echo "" | tee -a "$REPORT"

# 5. 编号统计总结
echo "【检查项 5】：全书编号统计" | tee -a "$REPORT"
total_formula=0
total_table=0
total_fig=0

for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    total_formula=$((total_formula + $(grep -o '([0-9]*-[0-9]*)' "$file" | wc -l)))
    total_table=$((total_table + $(grep -oE '表[0-9]+-[0-9]+' "$file" | wc -l)))
    total_fig=$((total_fig + $(grep -oE '图[0-9]+-[0-9]+' "$file" | wc -l)))
  fi
done

echo "  公式编号：$total_formula 处" | tee -a "$REPORT"
echo "  表格编号：$total_table 处" | tee -a "$REPORT"
echo "  图片编号：$total_fig 处" | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

cat "$REPORT"
