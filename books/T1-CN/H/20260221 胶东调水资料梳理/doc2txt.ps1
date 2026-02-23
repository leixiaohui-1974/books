$word = New-Object -ComObject Word.Application
$word.Visible = $false
$files = Get-ChildItem "." -Filter *.doc*
foreach ($file in $files) {
    if ($file.Extension -match "\.docx?$") {
        try {
            $doc = $word.Documents.Open($file.FullName)
            $text = $doc.Content.Text
            $outPath = $file.FullName -replace '\.docx?$', '.txt'
            Set-Content -Path $outPath -Value $text -Encoding UTF8
            $doc.Close($false)
            Write-Host "Processed $($file.Name)"
        }
        catch {
            Write-Host "Error processing $($file.Name): $_"
        }
    }
}
$word.Quit()
