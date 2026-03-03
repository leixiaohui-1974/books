#!/bin/bash

# T1-CN 图表质量检查脚本
# 检查：链接有效、标题清晰、编号连续、引用准确

cd "$(dirname "$0")"

echo "========================================"
echo "图表质量检查 - T1-CN 全书"
echo "========================================"
echo ""

REPORT="/tmp/images_tables_report.txt"
> "$REPORT"

# 1. 统计图表分布
echo "【检查项 1】：图表分布统计" | tee -a "$REPORT"
total_images=0
total_tables=0

for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    images=$(grep -c '!\[' "$file")
    tables=$(grep -c '^|' "$file")
    tables=$((tables / 2))  # 表格行通常成对（头+分隔）
    if [ "$tables" -lt 0 ]; then tables=0; fi
    
    printf "  Ch$(printf "%02d" "$ch_num"): 图片 %d, 表格 %d\n" "$images" "$tables" | tee -a "$REPORT"
    total_images=$((total_images + images))
    total_tables=$((total_tables + tables))
  fi
done
echo "  【全书总计】：图片 $total_images, 表格 $total_tables" | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

# 2. 检查图片链接有效性
echo "【检查项 2】：图片链接有效性检查" | tee -a "$REPORT"
broken_links=0
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 提取所有图片链接
    images=$(grep -o '!\[[^]]*\]([^)]*)' "$file" | sed 's/!\[.*\](\(.*\))/\1/')
    
    while IFS= read -r img_url; do
      if [ -z "$img_url" ]; then continue; fi
      
      # 检查是否是 GitHub raw URL
      if echo "$img_url" | grep -q "raw.githubusercontent.com"; then
        echo "    ✅ $img_url (GitHub raw URL)" | tee -a "$REPORT"
      elif echo "$img_url" | grep -q "^H/"; then
        echo "    ⚠️ 相对路径: $img_url (应改为 GitHub raw URL)" | tee -a "$REPORT"
        broken_links=$((broken_links + 1))
      elif echo "$img_url" | grep -q "github"; then
        echo "    ✅ $img_url (GitHub URL)" | tee -a "$REPORT"
      else
        echo "    ⚠️ 非 GitHub URL: $img_url" | tee -a "$REPORT"
        broken_links=$((broken_links + 1))
      fi
    done <<< "$images"
  fi
done

if [ "$broken_links" -eq 0 ]; then
  echo "  ✅ 所有图片链接格式正确" | tee -a "$REPORT"
else
  echo "  ⚠️ 发现 $broken_links 个潜在的链接问题" | tee -a "$REPORT"
fi
echo "" | tee -a "$REPORT"

# 3. 检查表格编号连续性
echo "【检查项 3】：表格编号连续性" | tee -a "$REPORT"
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 提取所有表格编号 表X-N 或 Table X-N
    table_nums=$(grep -oE "表$(printf "%02d" "$ch_num")-[0-9]+" "$file" | sed "s/表$(printf "%02d" "$ch_num")-//g" | sort -n | uniq)
    
    if [ -z "$table_nums" ]; then
      continue
    fi
    
    first=$(echo "$table_nums" | head -1)
    last=$(echo "$table_nums" | tail -1)
    expected=$((last - first + 1))
    actual=$(echo "$table_nums" | wc -w)
    
    if [ "$expected" -eq "$actual" ]; then
      echo "  ✅ Ch$(printf "%02d" "$ch_num"): 表$ch_num-$first ~ 表$ch_num-$last 连续，共 $actual 个" | tee -a "$REPORT"
    else
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): 表$ch_num-$first ~ 表$ch_num-$last 有缺失，期望$expected个，实际$actual个" | tee -a "$REPORT"
    fi
  fi
done
echo "" | tee -a "$REPORT"

# 4. 检查图片编号连续性
echo "【检查项 4】：图片编号连续性" | tee -a "$REPORT"
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 提取所有图片编号 图X-N 或 fig_XX_XX
    fig_nums=$(grep -oE "图$(printf "%02d" "$ch_num")-[0-9]+" "$file" | sed "s/图$(printf "%02d" "$ch_num")-//g" | sort -n | uniq)
    
    if [ -z "$fig_nums" ]; then
      continue
    fi
    
    first=$(echo "$fig_nums" | head -1)
    last=$(echo "$fig_nums" | tail -1)
    expected=$((last - first + 1))
    actual=$(echo "$fig_nums" | wc -w)
    
    if [ "$expected" -eq "$actual" ]; then
      echo "  ✅ Ch$(printf "%02d" "$ch_num"): 图$ch_num-$first ~ 图$ch_num-$last 连续，共 $actual 个" | tee -a "$REPORT"
    else
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): 图$ch_num-$first ~ 图$ch_num-$last 有缺失，期望$expected个，实际$actual个" | tee -a "$REPORT"
    fi
  fi
done
echo "" | tee -a "$REPORT"

# 5. 检查图表标题清晰度
echo "【检查项 5】：图表标题清晰度" | tee -a "$REPORT"
missing_captions=0
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 检查有多少图片缺少标题（通常在 ![] 后的括号内）
    images=$(grep '!\[' "$file" | grep -c '\[\]')
    if [ "$images" -gt 0 ]; then
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): $images 个图片缺少标题" | tee -a "$REPORT"
      missing_captions=$((missing_captions + images))
    fi
  fi
done
if [ "$missing_captions" -eq 0 ]; then
  echo "  ✅ 所有图表都有标题" | tee -a "$REPORT"
fi
echo "" | tee -a "$REPORT"

# 6. 检查图表引用
echo "【检查项 6】：图表引用完整性" | tee -a "$REPORT"
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 检查所有被引用的图表编号是否都被定义
    # 这里简化检查：搜索"图X-N"和"表X-N"的引用
    fig_refs=$(grep -oE "图$(printf "%02d" "$ch_num")-[0-9]+" "$file" | sed "s/图$(printf "%02d" "$ch_num")-//g" | sort -u)
    table_refs=$(grep -oE "表$(printf "%02d" "$ch_num")-[0-9]+" "$file" | sed "s/表$(printf "%02d" "$ch_num")-//g" | sort -u)
    
    if [ -n "$fig_refs" ] || [ -n "$table_refs" ]; then
      echo "    Ch$(printf "%02d" "$ch_num"): 引用图$fig_refs 表$table_refs" | tee -a "$REPORT"
    fi
  fi
done
echo "" | tee -a "$REPORT"

cat "$REPORT"
