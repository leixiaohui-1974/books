#!/bin/bash
cp ch12_final.md ch12_final.md.backup2

# 从高到低重新编号，避免冲突
sed -i 's/\[12-18\]/[12-11]/g' ch12_final.md
sed -i 's/\[12-16\]/[12-10]/g' ch12_final.md
sed -i 's/\[12-15\]/[12-9]/g' ch12_final.md
sed -i 's/\[12-14\]/[12-8]/g' ch12_final.md
sed -i 's/\[12-12\]/[12-7]/g' ch12_final.md
sed -i 's/\[12-11\]/[12-6]/g' ch12_final.md
sed -i 's/\[12-10\]/[12-5]/g' ch12_final.md
sed -i 's/\[12-9\]/[12-4]/g' ch12_final.md
sed -i 's/\[12-8\]/[12-3]/g' ch12_final.md
sed -i 's/\[12-7\]/[12-2]/g' ch12_final.md

echo "✅ Ch12参考文献重新编号完成"
