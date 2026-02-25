#!/bin/bash
echo "=== 检查LaTeX命令过度转义 ==="
for file in ch{01..12}_final.md ch{13..15}_final.md; do
  if [ -f "$file" ]; then
    echo "--- $file ---"
    found=0
    
    # 检查 \dot\{
    if grep -q '\\dot\\{' "$file"; then
      echo "  ⚠️ 发现 \\dot\\{ 过度转义:"
      grep -n '\\dot\\{' "$file" | head -3
      found=1
    fi
    
    # 检查 \hat\{
    if grep -q '\\hat\\{' "$file"; then
      echo "  ⚠️ 发现 \\hat\\{ 过度转义:"
      grep -n '\\hat\\{' "$file" | head -3
      found=1
    fi
    
    # 检查 \text\{
    if grep -q '\\text\\{' "$file"; then
      echo "  ⚠️ 发现 \\text\\{ 过度转义:"
      grep -n '\\text\\{' "$file" | head -3
      found=1
    fi
    
    # 检查 \frac\{
    if grep -q '\\frac\\{' "$file"; then
      echo "  ⚠️ 发现 \\frac\\{ 过度转义:"
      grep -n '\\frac\\{' "$file" | head -3
      found=1
    fi
    
    # 检查下标 _\{
    if grep -q '_\\{' "$file"; then
      echo "  ⚠️ 发现下标过度转义 _\\{:"
      grep -n '_\\{' "$file" | head -3
      found=1
    fi
    
    # 检查上标 ^\{
    if grep -q '\\^\\{' "$file"; then
      echo "  ⚠️ 发现上标过度转义 ^\\{:"
      grep -n '\\^\\{' "$file" | head -3
      found=1
    fi
    
    if [ $found -eq 0 ]; then
      echo "  ✅ 无过度转义"
    fi
    echo ""
  fi
done
