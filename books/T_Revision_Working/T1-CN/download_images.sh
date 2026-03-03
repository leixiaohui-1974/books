#!/bin/bash
set -e

echo "=== 下载Ch01图片 ==="
mkdir -p H/temp_downloads

# Ch01图片（5张）
curl -L "https://github.com/user-attachments/assets/60634219-ff6b-475c-bbfc-661f8e1f1a6e" -o H/temp_downloads/fig_01_01.png
curl -L "https://github.com/user-attachments/assets/5d2bd595-09de-4a1f-9471-5a3c39ed598f" -o H/temp_downloads/fig_01_02.png
curl -L "https://github.com/user-attachments/assets/0f5df490-0074-4d33-b153-c102e388ed16" -o H/temp_downloads/fig_01_03.png
curl -L "https://github.com/user-attachments/assets/9ecfc64e-736a-4b00-b84c-9f97df000322" -o H/temp_downloads/fig_01_04.png
curl -L "https://github.com/user-attachments/assets/e000893a-3268-42b1-af37-421dd3c83a94" -o H/temp_downloads/fig_01_05.png

echo ""
echo "=== 下载Ch02图片 ==="

# Ch02图片（4张，检查是否有更多）
curl -L "https://github.com/user-attachments/assets/608d6a0a-9802-46a6-9bcb-3d08fb2e9233" -o H/temp_downloads/fig_02_01.png
curl -L "https://github.com/user-attachments/assets/a658034a-7c2a-4131-8691-051cfb37a4bf" -o H/temp_downloads/fig_02_02.png
curl -L "https://github.com/user-attachments/assets/bc63a63f-ef6b-4e97-b558-99e4a4bde3f9" -o H/temp_downloads/fig_02_03.png
curl -L "https://github.com/user-attachments/assets/40ae4deb-ece2-4cd6-a41c-a7a53b6882ef" -o H/temp_downloads/fig_02_04.png

echo ""
echo "=== 检查下载结果 ==="
ls -lh H/temp_downloads/
