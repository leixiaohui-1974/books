#!/bin/bash
# 重新编号Ch02参考文献：[2-11]~[2-25] → [2-11]~[2-22]，并插入[2-21]

cp ch02_final.md ch02_final.md.backup_refs

# 重新编号：[2-12]~[2-20] → [2-11]~[2-19]
sed -i 's/\[2-12\]/[2-11]/g' ch02_final.md
sed -i 's/\[2-13\]/[2-12]/g' ch02_final.md
sed -i 's/\[2-14\]/[2-13]/g' ch02_final.md
sed -i 's/\[2-15\]/[2-14]/g' ch02_final.md
sed -i 's/\[2-16\]/[2-15]/g' ch02_final.md
sed -i 's/\[2-17\]/[2-16]/g' ch02_final.md
sed -i 's/\[2-18\]/[2-17]/g' ch02_final.md
sed -i 's/\[2-19\]/[2-18]/g' ch02_final.md
sed -i 's/\[2-20\]/[2-19]/g' ch02_final.md

# [2-22] → [2-20]
sed -i 's/\[2-22\]/[2-20]/g' ch02_final.md

# [2-24] → [2-21]
sed -i 's/\[2-24\]/[2-21]/g' ch02_final.md

# [2-25] → [2-22]
sed -i 's/\[2-25\]/[2-22]/g' ch02_final.md

echo "✅ 已重新编号Ch02参考文献"
