$docxFiles = Get-ChildItem -Path . -Filter *.docx
if ($docxFiles.Count -eq 0) {
    Write-Host "No docx files found."
    exit
}
Write-Host "Found $($docxFiles.Count) files. Starting conversion..."
foreach ($file in $docxFiles) {
    $outName = Join-Path $file.DirectoryName ($file.BaseName + ".md")
    Write-Host "Converting: $($file.Name) -> $($file.BaseName).md"
    try {
        # 使用用户提供的完整路径调用 pandoc
        & "D:\pandoc-3.1.13\pandoc.exe" -f docx -t gfm -o "$outName" "$($file.FullName)" --wrap=none
    } catch {
        Write-Host "Error calling pandoc: $($_.Exception.Message)"
        break
    }
}
Write-Host "Done."
