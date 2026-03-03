#!/bin/bash

# 综合评审脚本：T1-CN 全书 8 大项检查

REPORT="COMPREHENSIVE_AUDIT_REPORT.md"
> "$REPORT"

echo "# T1-CN 全书深度评审报告" >> "$REPORT"
echo "生成时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT"
echo "" >> "$REPORT"

# ===== 1. 参考文献完整性检查 =====
echo "## 1. 参考文献完整性检查" >> "$REPORT"
echo "" >> "$REPORT"

for ch in {01..15}; do
  file="ch${ch}_final.md"
  [ ! -f "$file" ] && file="ch${ch}.md"
  
  if [ -f "$file" ]; then
    refs=$(grep -o "\[${ch}-[0-9]*\]" "$file" | sort -u)
    ref_list=$(grep "^\[${ch}-" "$file" | wc -l)
    
    echo "### Ch$ch" >> "$REPORT"
    echo "- 正文引用数：$(echo "$refs" | wc -l)" >> "$REPORT"
    echo "- 参考文献条数：$ref_list" >> "$REPORT"
    
    # 检查孤立引用
    orphans=""
    for ref in $refs; do
      ref_num=$(echo "$ref" | sed 's/\[//' | sed 's/\]//' | cut -d'-' -f2)
      if ! grep -q "^\[${ch}-${ref_num}\]" "$file"; then
        orphans="$orphans $ref"
      fi
    done
    
    if [ -n "$orphans" ]; then
      echo "⚠️ 孤立引用：$orphans" >> "$REPORT"
    else
      echo "✅ 无孤立引用" >> "$REPORT"
    fi
    echo "" >> "$REPORT"
  fi
done

# ===== 2. 公式编号连续性检查 =====
echo "## 2. 公式编号连续性检查" >> "$REPORT"
echo "" >> "$REPORT"

for ch in {01..15}; do
  file="ch${ch}_final.md"
  [ ! -f "$file" ] && file="ch${ch}.md"
  
  if [ -f "$file" ]; then
    echo "### Ch$ch" >> "$REPORT"
    
    # 提取公式编号
    formulas=$(grep -o "(${ch}-[0-9]*)" "$file" | sort -u)
    max=$(echo "$formulas" | tail -1 | sed 's/(//' | sed 's/)//' | cut -d'-' -f2)
    
    echo "- 最大公式编号：$max" >> "$REPORT"
    
    # 检查缺失编号
    missing=""
    for ((i=1; i<=max; i++)); do
      if ! echo "$formulas" | grep -q "(${ch}-${i})"; then
        missing="$missing ${ch}-${i}"
      fi
    done
    
    if [ -n "$missing" ]; then
      echo "⚠️ 缺失编号：$missing" >> "$REPORT"
    else
      echo "✅ 编号连续无缺失" >> "$REPORT"
    fi
    echo "" >> "$REPORT"
  fi
done

# ===== 3. 图片链接检查 =====
echo "## 3. 图片链接检查" >> "$REPORT"
echo "" >> "$REPORT"

total_imgs=0
valid_imgs=0
invalid_imgs=0

for ch in {01..15}; do
  file="ch${ch}_final.md"
  [ ! -f "$file" ] && file="ch${ch}.md"
  
  if [ -f "$file" ]; then
    imgs=$(grep -o "!\[.*\](.*)" "$file" | grep -o "https://.*\.png\|H/.*\.png" | sort -u)
    img_count=$(echo "$imgs" | grep -c "")
    
    if [ $img_count -gt 0 ]; then
      echo "### Ch$ch - $img_count 个图片" >> "$REPORT"
      total_imgs=$((total_imgs + img_count))
      
      for img in $imgs; do
        if echo "$img" | grep -q "^https://"; then
          echo "- ✅ $img (raw URL)" >> "$REPORT"
          valid_imgs=$((valid_imgs + 1))
        elif echo "$img" | grep -q "^H/"; then
          echo "- ⚠️ $img (相对路径)" >> "$REPORT"
          invalid_imgs=$((invalid_imgs + 1))
        fi
      done
      echo "" >> "$REPORT"
    fi
  fi
done

echo "**统计**：总数=$total_imgs，有效=$valid_imgs，无效=$invalid_imgs" >> "$REPORT"
echo "" >> "$REPORT"

# ===== 4. 表格编号检查 =====
echo "## 4. 表格编号检查" >> "$REPORT"
echo "" >> "$REPORT"

for ch in {01..15}; do
  file="ch${ch}_final.md"
  [ ! -f "$file" ] && file="ch${ch}.md"
  
  if [ -f "$file" ]; then
    tables=$(grep -E "^\|.*\|$" "$file" | wc -l)
    if [ $tables -gt 0 ]; then
      echo "### Ch$ch" >> "$REPORT"
      echo "- 表格行数：$tables" >> "$REPORT"
      echo "" >> "$REPORT"
    fi
  fi
done

# ===== 5. 术语一致性检查 =====
echo "## 5. 术语一致性检查" >> "$REPORT"
echo "" >> "$REPORT"

for term in "CHS" "WNAL" "ODD" "HDC" "MPC" "MAS"; do
  echo "### $term" >> "$REPORT"
  count=$(grep -r "$term" . --include="*.md" 2>/dev/null | wc -l)
  echo "- 出现次数：$count" >> "$REPORT"
  echo "" >> "$REPORT"
done

# ===== 6. LaTeX 语法检查 =====
echo "## 6. LaTeX 语法检查" >> "$REPORT"
echo "" >> "$REPORT"

# 检查过度转义
over_escape=0
for file in ch*_final.md ch*.md; do
  [ ! -f "$file" ] && continue
  
  # 检查 \dot\{ 类错误
  if grep -q '\\dot\\{' "$file"; then
    echo "⚠️ $file: 发现 \\dot\\{ 过度转义" >> "$REPORT"
    over_escape=$((over_escape + 1))
  fi
  
  # 检查 _{...} 类转义错误
  if grep -q '_\\{' "$file"; then
    echo "⚠️ $file: 发现下标过度转义" >> "$REPORT"
    over_escape=$((over_escape + 1))
  fi
done

if [ $over_escape -eq 0 ]; then
  echo "✅ 无过度转义问题" >> "$REPORT"
else
  echo "⚠️ 发现 $over_escape 处过度转义" >> "$REPORT"
fi
echo "" >> "$REPORT"

# ===== 7. 列表项格式检查 =====
echo "## 7. 列表项公式格式检查" >> "$REPORT"
echo "" >> "$REPORT"

bad_format=0
for file in ch*_final.md ch*.md; do
  [ ! -f "$file" ] && continue
  
  # 检查 -$ 错误格式
  if grep -q -- '-$' "$file"; then
    echo "⚠️ $file: 发现列表项格式错误 (-$)" >> "$REPORT"
    bad_format=$((bad_format + 1))
  fi
done

if [ $bad_format -eq 0 ]; then
  echo "✅ 所有列表项格式正确" >> "$REPORT"
else
  echo "⚠️ 发现 $bad_format 处列表项格式错误" >> "$REPORT"
fi
echo "" >> "$REPORT"

# ===== 8. 交叉引用检查 =====
echo "## 8. 交叉引用检查（按章节统计）" >> "$REPORT"
echo "" >> "$REPORT"

for ch in {01..15}; do
  file="ch${ch}_final.md"
  [ ! -f "$file" ] && file="ch${ch}.md"
  
  if [ -f "$file" ]; then
    # 检查内部引用（同章）
    internal=$(grep -o "\[${ch}-[0-9]*\]" "$file" | wc -l)
    
    # 检查外部引用（其他章）
    external=$(grep -oE "\[[0-9]{2}-[0-9]+\]" "$file" | grep -v "\[${ch}-" | wc -l)
    
    # 检查章节引用
    chapter_refs=$(grep -c "第.*章\|见第.*章\|如\[0-9\]\+所示" "$file" 2>/dev/null || echo "0")
    
    if [ $internal -gt 0 ] || [ $external -gt 0 ]; then
      echo "### Ch$ch" >> "$REPORT"
      echo "- 内部引用（同章）：$internal" >> "$REPORT"
      echo "- 外部引用（其他章）：$external" >> "$REPORT"
      echo "- 章节引用：$chapter_refs" >> "$REPORT"
      echo "" >> "$REPORT"
    fi
  fi
done

echo "" >> "$REPORT"
echo "**评审完成时间**：$(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT"

echo "✅ 报告已生成：$REPORT"
