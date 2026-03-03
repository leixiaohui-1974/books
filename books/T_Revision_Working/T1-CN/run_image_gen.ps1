$env:NB_API_BASE = "https://generativelanguage.googleapis.com/v1beta"
$env:NB_MODEL    = "nano-banana-pro"

Write-Host "Model: $env:NB_MODEL"
Write-Host ""
python generate_images_api.py --all --update-md
Write-Host ""
Write-Host "完成！"
Read-Host "按回车退出"
