#!/bin/bash
echo "=== 参考文献详细检查 ==="

for file in ch02_final.md ch06_final.md ch12_final.md ch15_final.md; do
  echo ""
  echo "=========================================="
  echo "📄 $file"
  echo "=========================================="
  
  # 提取参考文献章节
  sed -n '/^## 参考文献/,/^##[^#]/p' "$file" | sed '/^##[^#]/d' > /tmp/refs_$file
  
  if [ -s /tmp/refs_$file ]; then
    echo "参考文献条目:"
    grep '^\[' /tmp/refs_$file | nl
    
    echo ""
    echo "检查项:"
    
    # 检查编号连续性
    chapter=$(echo $file | grep -oP 'ch\d+')
    ch_num=$(echo $chapter | grep -oP '\d+')
    
    ref_nums=$(grep -oP '^\['$ch_num'-\d+\]' /tmp/refs_$file | grep -oP '\d+$' | sort -n)
    expected=1
    missing=""
    for num in $ref_nums; do
      if [ $num -ne $expected ]; then
        missing="$missing ($ch_num-$expected)"
      fi
      expected=$((num + 1))
    done
    
    if [ -z "$missing" ]; then
      echo "  ✅ 编号连续"
    else
      echo "  ⚠️ 缺失编号: $missing"
    fi
    
    # 检查是否有DOI或URL
    doi_count=$(grep -c 'DOI:' /tmp/refs_$file)
    url_count=$(grep -c 'http' /tmp/refs_$file)
    echo "  - 包含DOI: $doi_count 条"
    echo "  - 包含URL: $url_count 条"
    
    # 检查是否有年份
    year_count=$(grep -c '[12][0-9]\{3\}' /tmp/refs_$file)
    total_count=$(grep -c '^\[' /tmp/refs_$file)
    echo "  - 包含年份: $year_count/$total_count 条"
    
    if [ $year_count -lt $total_count ]; then
      echo "  ⚠️ 部分文献缺少年份"
    fi
  else
    echo "  ⚠️ 未找到参考文献"
  fi
done
