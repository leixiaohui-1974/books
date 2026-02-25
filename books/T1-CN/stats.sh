#!/bin/bash
echo "=== T1-CN教材公式统计 ==="
echo ""
printf "%-15s %10s %10s %10s\n" "章节" "行内公式" "公式块" "字符数"
echo "-------------------------------------------------------"

total_inline=0
total_blocks=0
total_chars=0

for file in ch{01..12}_final.md ch{13..15}_final.md; do
  if [ -f "$file" ]; then
    chapter=$(echo $file | sed 's/_final.md//')
    
    # 统计行内公式（$...$配对数）
    inline=$(grep -o '\$[^$]*\$' "$file" | wc -l)
    
    # 统计公式块（$$...$$配对数）
    blocks=$(grep -c '^\$\$$' "$file")
    blocks=$((blocks / 2))
    
    # 统计字符数
    chars=$(wc -c < "$file")
    
    printf "%-15s %10d %10d %10d\n" "$chapter" "$inline" "$blocks" "$chars"
    
    total_inline=$((total_inline + inline))
    total_blocks=$((total_blocks + blocks))
    total_chars=$((total_chars + chars))
  fi
done

echo "-------------------------------------------------------"
printf "%-15s %10d %10d %10d\n" "总计" "$total_inline" "$total_blocks" "$total_chars"
echo ""
echo "字符总数: $(echo $total_chars | numfmt --grouping) 字节"
echo "行内公式总数: $total_inline 个"
echo "公式块总数: $total_blocks 对"
