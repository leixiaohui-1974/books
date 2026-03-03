#!/bin/bash
set -e

echo "=== 备份原文件 ==="
cp ch01_final.md ch01_final.md.backup_img
cp ch02_final.md ch02_final.md.backup_img

echo ""
echo "=== 替换Ch01图片链接 ==="

# Ch01图片替换（5张）
sed -i 's|https://github.com/user-attachments/assets/60634219-ff6b-475c-bbfc-661f8e1f1a6e|https://raw.githubusercontent.com/leixiaohui-1974/books/main/books/T1-CN/H/fig_01_01.png|g' ch01_final.md

sed -i 's|https://github.com/user-attachments/assets/5d2bd595-09de-4a1f-9471-5a3c39ed598f|https://raw.githubusercontent.com/leixiaohui-1974/books/main/books/T1-CN/H/fig_01_02.png|g' ch01_final.md

sed -i 's|https://github.com/user-attachments/assets/0f5df490-0074-4d33-b153-c102e388ed16|https://raw.githubusercontent.com/leixiaohui-1974/books/main/books/T1-CN/H/fig_01_03.png|g' ch01_final.md

sed -i 's|https://github.com/user-attachments/assets/9ecfc64e-736a-4b00-b84c-9f97df000322|https://raw.githubusercontent.com/leixiaohui-1974/books/main/books/T1-CN/H/fig_01_04.png|g' ch01_final.md

sed -i 's|https://github.com/user-attachments/assets/e000893a-3268-42b1-af37-421dd3c83a94|https://raw.githubusercontent.com/leixiaohui-1974/books/main/books/T1-CN/H/fig_01_05.png|g' ch01_final.md

echo "Ch01: 5张图片链接已替换"

echo ""
echo "=== 替换Ch02图片链接 ==="

# Ch02图片替换（4张）
sed -i 's|https://github.com/user-attachments/assets/608d6a0a-9802-46a6-9bcb-3d08fb2e9233|https://raw.githubusercontent.com/leixiaohui-1974/books/main/books/T1-CN/H/fig_02_01.png|g' ch02_final.md

sed -i 's|https://github.com/user-attachments/assets/a658034a-7c2a-4131-8691-051cfb37a4bf|https://raw.githubusercontent.com/leixiaohui-1974/books/main/books/T1-CN/H/fig_02_02.png|g' ch02_final.md

sed -i 's|https://github.com/user-attachments/assets/bc63a63f-ef6b-4e97-b558-99e4a4bde3f9|https://raw.githubusercontent.com/leixiaohui-1974/books/main/books/T1-CN/H/fig_02_03.png|g' ch02_final.md

sed -i 's|https://github.com/user-attachments/assets/40ae4deb-ece2-4cd6-a41c-a7a53b6882ef|https://raw.githubusercontent.com/leixiaohui-1974/books/main/books/T1-CN/H/fig_02_04.png|g' ch02_final.md

echo "Ch02: 4张图片链接已替换"

echo ""
echo "=== 验证替换结果 ==="
echo "Ch01临时链接剩余数量: $(grep -c 'user-attachments/assets' ch01_final.md || echo 0)"
echo "Ch02临时链接剩余数量: $(grep -c 'user-attachments/assets' ch02_final.md || echo 0)"

echo ""
echo "Ch01新链接数量: $(grep -c 'raw.githubusercontent.com/leixiaohui-1974/books/main/books/T1-CN/H/fig_01' ch01_final.md || echo 0)"
echo "Ch02新链接数量: $(grep -c 'raw.githubusercontent.com/leixiaohui-1974/books/main/books/T1-CN/H/fig_02' ch02_final.md || echo 0)"
