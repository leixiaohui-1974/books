#!/bin/bash

# T1-CN 公式规范检查脚本
# 检查：LaTeX 语法、编号连续、引用准确、块格式

cd "$(dirname "$0")"

echo "========================================"
echo "公式规范检查 - T1-CN 全书"
echo "========================================"
echo ""

REPORT="/tmp/formulas_report.txt"
> "$REPORT"

# 1. 统计公式数量
echo "【检查项 1】：公式分布统计" | tee -a "$REPORT"
total_inline=0
total_blocks=0

for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    inline=$(grep -o '\$[^$]*\$' "$file" | grep -v '^\$\$' | wc -l)
    blocks=$(grep '^\$\$' "$file" | wc -l)
    blocks=$((blocks / 2))  # $$ 成对出现
    printf "  Ch$(printf "%02d" "$ch_num"): 行内公式 %d, 公式块 %d\n" "$inline" "$blocks" | tee -a "$REPORT"
    total_inline=$((total_inline + inline))
    total_blocks=$((total_blocks + blocks))
  fi
done
echo "  【全书总计】：行内公式 $total_inline, 公式块 $total_blocks" | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

# 2. 检查公式编号连续性
echo "【检查项 2】：公式编号连续性" | tee -a "$REPORT"
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 提取所有公式编号 (X-N)
    nums=$(grep -o "($ch_num-[0-9]*)" "$file" | sed "s/($ch_num-//g" | sed 's/)//g' | sort -n | uniq)
    
    if [ -z "$nums" ]; then
      echo "  Ch$(printf "%02d" "$ch_num"): 无编号公式" | tee -a "$REPORT"
      continue
    fi
    
    first=$(echo "$nums" | head -1)
    last=$(echo "$nums" | tail -1)
    expected=$((last - first + 1))
    actual=$(echo "$nums" | wc -w)
    
    if [ "$expected" -eq "$actual" ]; then
      echo "  ✅ Ch$(printf "%02d" "$ch_num"): ($ch_num-$first) ~ ($ch_num-$last) 连续，共 $actual 个" | tee -a "$REPORT"
    else
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): ($ch_num-$first) ~ ($ch_num-$last) 有缺失，期望$expected个，实际$actual个" | tee -a "$REPORT"
    fi
  fi
done
echo "" | tee -a "$REPORT"

# 3. 检查公式块格式规范
echo "【检查项 3】：公式块格式检查（\$\$应独立成行）" | tee -a "$REPORT"
block_format_errors=0
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 检查 $$ 不是独立成行的情况（即不是仅 $$ 的行）
    errors=$(grep '^\$\$' "$file" | grep -v '^\$\$$' | wc -l)
    if [ "$errors" -gt 0 ]; then
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): 发现 $errors 处公式块格式不规范" | tee -a "$REPORT"
      block_format_errors=$((block_format_errors + errors))
    fi
  fi
done
if [ "$block_format_errors" -eq 0 ]; then
  echo "  ✅ 所有公式块格式规范" | tee -a "$REPORT"
fi
echo "" | tee -a "$REPORT"

# 4. 检查过度转义（不应该转义的花括号）
echo "【检查项 4】：LaTeX 命令转义检查（禁止过度转义）" | tee -a "$REPORT"
escape_errors=0
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 搜索不应该转义的模式
    # \dot\{, \hat\{, \text\{, _\{, ^\{, \frac\{
    errors=$(grep -E '\\(dot|hat|text|frac|mathbb|sqrt|sum|int|prod)\\\{' "$file" | wc -l)
    errors=$((errors + $(grep -E '_\\\{|^\^\\\{' "$file" | wc -l)))
    
    if [ "$errors" -gt 0 ]; then
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): 发现 $errors 处过度转义（命令参数不应转义）" | tee -a "$REPORT"
      escape_errors=$((escape_errors + errors))
    fi
  fi
done
if [ "$escape_errors" -eq 0 ]; then
  echo "  ✅ 无过度转义问题" | tee -a "$REPORT"
fi
echo "" | tee -a "$REPORT"

# 5. 检查列表项中的公式格式
echo "【检查项 5】：列表项公式格式（- 后需要空格）" | tee -a "$REPORT"
list_format_errors=0
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 检查 -$ 模式（错误）vs - $ 模式（正确）
    errors=$(grep -E '^-\$' "$file" | wc -l)
    if [ "$errors" -gt 0 ]; then
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): 发现 $errors 处列表项格式错误（-$ 应为 - $）" | tee -a "$REPORT"
      list_format_errors=$((list_format_errors + errors))
    fi
  fi
done
if [ "$list_format_errors" -eq 0 ]; then
  echo "  ✅ 所有列表项格式规范" | tee -a "$REPORT"
fi
echo "" | tee -a "$REPORT"

# 6. 检查公式引用
echo "【检查项 6】：公式引用完整性" | tee -a "$REPORT"
# 统计引用了的公式编号 vs 实际存在的编号
for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    ch_num=$(echo "$file" | sed 's/ch\([0-9]*\)_final.md/\1/')
    # 找到所有被引用的公式编号
    cited=$(grep -o "式($ch_num-[0-9]*)" "$file" | sed "s/式($ch_num-//g" | sed 's/)//g' | sort -u)
    # 找到所有定义的公式编号
    defined=$(grep -o "($ch_num-[0-9]*)" "$file" | sed "s/($ch_num-//g" | sed 's/)//g' | sort -u)
    
    missing=0
    for ref in $cited; do
      if ! echo "$defined" | grep -q "^$ref$"; then
        echo "    公式($ch_num-$ref)被引用但未定义" | tee -a "$REPORT"
        missing=$((missing + 1))
      fi
    done
    
    if [ "$missing" -gt 0 ]; then
      echo "  ⚠️ Ch$(printf "%02d" "$ch_num"): $missing 个被引用的公式未定义" | tee -a "$REPORT"
    fi
  fi
done
echo "" | tee -a "$REPORT"

cat "$REPORT"
