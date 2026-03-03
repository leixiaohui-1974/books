#!/bin/bash
echo "=== T1-CN教材全面评审 ==="
echo ""

for file in ch{01..12}_final.md ch{13..15}_final.md; do
  if [ -f "$file" ]; then
    echo "=========================================="
    echo "📄 $file"
    echo "=========================================="
    
    # 1. 图片检查
    echo "📷 图片检查:"
    img_count=$(grep -c '!\[' "$file")
    echo "  - 图片引用数量: $img_count"
    
    # 检查图片链接格式
    broken_imgs=$(grep '!\[' "$file" | grep -v 'https://raw.githubusercontent.com' | grep -v '^#' | head -3)
    if [ -n "$broken_imgs" ]; then
      echo "  ⚠️ 发现非GitHub链接的图片:"
      echo "$broken_imgs" | head -3
    else
      echo "  ✅ 所有图片使用GitHub链接"
    fi
    
    # 2. 公式检查（已验证过，快速检查）
    echo ""
    echo "🔢 公式检查:"
    inline_count=$(grep -o '\$[^$]*\$' "$file" | wc -l)
    block_count=$(grep -c '^\$\$$' "$file")
    echo "  - 行内公式: $inline_count 个"
    echo "  - 公式块: $((block_count / 2)) 对"
    
    # 检查是否有未配对
    dollar_count=$(grep -o '\$' "$file" | wc -l)
    if [ $((dollar_count % 2)) -ne 0 ]; then
      echo "  ⚠️ 公式符号未配对"
    else
      echo "  ✅ 公式符号配对正确"
    fi
    
    # 3. 表格检查
    echo ""
    echo "📊 表格检查:"
    table_count=$(grep -c '^|' "$file")
    if [ $table_count -gt 0 ]; then
      echo "  - 表格行数: $table_count"
      # 检查表格格式
      table_headers=$(grep '^|' "$file" | grep -c '\-\-')
      echo "  - 表格分隔线: $table_headers"
      
      # 检查是否有表格标题
      table_captions=$(grep -B1 '^|' "$file" | grep -c '^表')
      echo "  - 表格标题: $table_captions"
      
      if [ $table_captions -eq 0 ]; then
        echo "  ⚠️ 可能缺少表格标题"
      fi
    else
      echo "  - 无表格"
    fi
    
    # 4. 参考文献检查
    echo ""
    echo "📚 参考文献检查:"
    
    # 检查是否有参考文献章节
    if grep -q '^## 参考文献' "$file" || grep -q '^### 参考文献' "$file"; then
      ref_count=$(sed -n '/^## 参考文献/,/^##/p' "$file" | grep -c '^\[')
      if [ $ref_count -eq 0 ]; then
        ref_count=$(sed -n '/^### 参考文献/,/^###/p' "$file" | grep -c '^\[')
      fi
      echo "  - 参考文献条目: $ref_count"
      
      # 检查引用格式
      if grep -q '^\[[0-9]\+\]' "$file"; then
        echo "  ✅ 使用数字编号格式"
      else
        echo "  ⚠️ 参考文献格式可能不规范"
      fi
    else
      echo "  - 无参考文献章节"
    fi
    
    # 检查正文中的引用
    citation_count=$(grep -o '\[[0-9]\+\]' "$file" | wc -l)
    if [ $citation_count -gt 0 ]; then
      echo "  - 正文引用次数: $citation_count"
    fi
    
    echo ""
  fi
done

echo "=========================================="
echo "🎯 评审完成"
echo "=========================================="
