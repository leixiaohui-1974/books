@echo off
chcp 65001 >nul
echo ================================================
echo   T2-CN 水网觉醒 - Gemini 图片生成
echo ================================================
echo.

set NB_API_KEY=AIzaSyC0CWHvn0K0Wk__RtZ2tqa9Safumu-sMRY
set NB_API_BASE=https://generativelanguage.googleapis.com/v1beta
set NB_MODEL=gemini-2.0-flash-preview-image-generation

cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请安装 Python 3.10+
    pause
    exit /b 1
)

echo [1/3] 安装依赖...
pip install google-genai pillow --quiet

echo.
echo [2/3] 检查文件...
if not exist generate_images_api.py (
    echo [错误] 找不到 generate_images_api.py
    pause
    exit /b 1
)
echo       OK

echo.
echo [3/3] 开始生成图片（约15-20分钟）...
echo.

python generate_images_api.py --all --update-md

echo.
echo ================================================
echo 完成！图片在 H\ 目录
echo ================================================
pause
