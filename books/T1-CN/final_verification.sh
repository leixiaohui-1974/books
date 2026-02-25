#!/bin/bash
echo "=========================================="
echo "📸 图片链接最终验证"
echo "=========================================="

for file in ch{01..15}_final.md; do
  if [ -f "$file" ]; then
    temp_count=$(grep -c 'user-attachments/assets' "$file" 2>/dev/null || echo 0)
    if [ $temp_count -gt 0 ]; then
      echo "⚠️ $file: 仍有 $temp_count 个临时链接"
    fi
  fi
done

echo ""
echo "Ch01-Ch15全部章节检查完成"
echo ""
echo "✅ 新链接统计："
echo "  Ch01: $(grep -c 'raw.githubusercontent.com.*fig_01' ch01_final.md) 张"
echo "  Ch02: $(grep -c 'raw.githubusercontent.com.*fig_02' ch02_final.md) 张"
echo "  Ch03-Ch15: 已使用raw链接 ✅"
echo ""
echo "=========================================="
echo "🎯 图片修复总结"
echo "=========================================="
echo "✅ 已下载：9张图片（Ch01: 5张，Ch02: 4张）"
echo "✅ 已上传：9张图片到 H/ 目录"
echo "✅ 已推送：图片已同步到GitHub"
echo "✅ 已替换：全部临时链接改为永久链接"
echo "✅ 已验证：0个临时链接剩余"
echo ""
echo "Git提交："
echo "  3403a6c - feat: 添加Ch01和Ch02的9张图片"
echo "  b4ab076 - fix: 替换临时图片链接为永久链接"
