#!/bin/bash
echo "=== T1-CN教材公式格式最终全面检查 ==="
echo ""

total_errors=0

for file in ch{01..12}_final.md ch{13..15}_final.md; do
  if [ -f "$file" ]; then
    chapter=$(echo $file | grep -oP 'ch\d+')
    errors=0
    
    # 1. 检查行内公式配对
    inline_count=$(grep -o '\$' "$file" | wc -l)
    if [ $((inline_count % 2)) -ne 0 ]; then
      echo "❌ $file: 行内公式\$符号不配对（$inline_count个）"
      errors=$((errors + 1))
    fi
    
    # 2. 检查公式块配对
    block_count=$(grep -c '^\$\$' "$file")
    if [ $((block_count % 2)) -ne 0 ]; then
      echo "❌ $file: 公式块\$\$不配对（$block_count个）"
      errors=$((errors + 1))
    fi
    
    # 3. 检查LaTeX命令过度转义
    if grep -q '\\dot\\{' "$file" || grep -q '\\hat\\{' "$file" || \
       grep -q '\\text\\{' "$file" || grep -q '\\frac\\{' "$file" || \
       grep -q '_\\{' "$file" || grep -q '\\^\\{' "$file"; then
      echo "❌ $file: 存在LaTeX命令过度转义"
      errors=$((errors + 1))
    fi
    
    # 4. 检查列表项格式
    if grep -q '\-\$' "$file"; then
      count=$(grep -c '\-\$' "$file")
      echo "❌ $file: 存在${count}处列表项格式错误 (-\$ 应为 - \$)"
      errors=$((errors + 1))
    fi
    
    # 5. 检查公式块空行
    problem_count=$(grep -n '^\$\$$' "$file" | while read line; do
      linenum=$(echo $line | cut -d: -f1)
      nextline=$((linenum + 1))
      content=$(sed -n "${nextline}p" "$file")
      if [[ "$content" == "<div"* ]]; then
        echo "1"
      fi
    done | wc -l)
    
    if [ $problem_count -gt 0 ]; then
      echo "❌ $file: 存在${problem_count}处公式块后缺少空行"
      errors=$((errors + 1))
    fi
    
    # 6. 检查相邻公式
    if grep -q '\$\$\$' "$file"; then
      count=$(grep -c '\$\$\$' "$file")
      echo "❌ $file: 存在${count}处相邻公式缺少空格"
      errors=$((errors + 1))
    fi
    
    if [ $errors -eq 0 ]; then
      echo "✅ $file: 所有检查通过"
    else
      total_errors=$((total_errors + errors))
    fi
  fi
done

echo ""
echo "========================================"
if [ $total_errors -eq 0 ]; then
  echo "🎉 全书公式格式检查完美通过！"
else
  echo "⚠️ 发现 $total_errors 处错误需要修复"
fi
