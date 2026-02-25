#!/bin/bash
set -e

echo "==========================================="
echo "🔍 T1-CN全书全面检查"
echo "==========================================="
echo ""

# 检查1：章节完整性
echo "📖 1. 章节完整性检查"
echo "==========================================="
for file in ch{01..15}_final.md; do
  if [ ! -f "$file" ]; then
    echo "❌ 缺失: $file"
  else
    lines=$(wc -l < "$file")
    refs=$(grep -c '^\[' "$file" || echo 0)
    imgs=$(grep -c '!\[' "$file" || echo 0)
    tables=$(grep -c '^|' "$file" || echo 0)
    printf "✅ %-20s %4d行 %2d引用 %2d图片 %2d表\n" "$file" "$lines" "$refs" "$imgs" "$tables"
  fi
done

echo ""
echo "📊 2. 公式格式检查"
echo "==========================================="
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    dollar=$(grep -o '\$' "$file" | wc -l)
    dblstr=$(grep -o '\$\$' "$file" | wc -l)
    if [ $((dollar % 2)) -ne 0 ]; then
      echo "⚠️ $file: \$符号不配对 (共$dollar个)"
    else
      echo "✅ $file: 公式配对正确"
    fi
  fi
done

echo ""
echo "🏷️ 3. 参考文献编号检查"
echo "==========================================="
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | grep -oP 'ch\d+')
    ch_id=$(echo "$ch_num" | grep -oP '\d+')
    ref_count=$(grep -c "^\[$ch_id-" "$file" || echo 0)
    if [ $ref_count -gt 0 ]; then
      echo "📚 $file: $ref_count条参考文献"
    fi
  fi
done

echo ""
echo "✅ 检查完成"
