#!/bin/bash
echo "=== 表格详细检查 ==="

for file in ch{01..12}_final.md ch{13..15}_final.md; do
  if [ -f "$file" ]; then
    table_count=$(grep -c '^|' "$file")
    
    if [ $table_count -gt 0 ]; then
      echo ""
      echo "--- $file (表格行数: $table_count) ---"
      
      # 提取表格（查看前3行）
      grep -n '^|' "$file" | head -6 | while read line; do
        linenum=$(echo $line | cut -d: -f1)
        content=$(echo $line | cut -d: -f2-)
        
        # 检查该行的上一行（可能是标题）
        prevline=$((linenum - 1))
        prev_content=$(sed -n "${prevline}p" "$file")
        
        # 如果是表格开始（上一行不是表格行）
        if ! echo "$prev_content" | grep -q '^|'; then
          echo "  表格起始行$linenum，前一行: $prev_content"
        fi
      done
    fi
  fi
done
