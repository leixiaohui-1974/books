#!/bin/bash
echo "=== 检查公式块格式 ==="
for file in ch{01..12}_final.md ch{13..15}_final.md; do
  if [ -f "$file" ]; then
    chapter=$(echo $file | grep -oP 'ch\d+')
    echo "--- $file ---"
    
    # 统计公式块数量
    block_count=$(grep -c '^\$\$' "$file")
    echo "  公式块标记数量: $block_count"
    
    # 提取章节编号
    ch_num=$(echo $chapter | grep -oP '\d+')
    
    # 统计公式编号数量（格式：(X-Y)）
    eq_count=$(grep -oP "\($ch_num-\d+\)" "$file" | sort -u | wc -l)
    echo "  公式编号数量: $eq_count"
    
    # 检查公式块是否成对（应该是偶数）
    if [ $((block_count % 2)) -ne 0 ]; then
      echo "  ⚠️ 警告：公式块标记数量为奇数，可能存在未配对的 \$\$"
    fi
    
    # 检查公式块后是否有空行
    problem_lines=$(grep -n '^\$\$$' "$file" | while read line; do
      linenum=$(echo $line | cut -d: -f1)
      nextline=$((linenum + 1))
      content=$(sed -n "${nextline}p" "$file")
      if [[ "$content" == "<div"* ]]; then
        echo "$linenum"
      fi
    done)
    
    if [ -n "$problem_lines" ]; then
      echo "  ⚠️ 发现公式块后缺少空行的位置："
      echo "$problem_lines" | head -5
    else
      echo "  ✅ 公式块空行格式正确"
    fi
    
    # 如果有公式编号，检查连续性
    if [ $eq_count -gt 0 ]; then
      echo "  公式编号范围: ($ch_num-1) ~ ($ch_num-$eq_count)"
      # 检查是否有缺失
      for i in $(seq 1 $eq_count); do
        if ! grep -q "($ch_num-$i)" "$file"; then
          echo "  ⚠️ 缺失公式编号: ($ch_num-$i)"
        fi
      done
    fi
    
    echo ""
  fi
done
