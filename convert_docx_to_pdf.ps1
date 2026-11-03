param (
    [string]$DocxPath,
    [string]$PdfPath
)

if (-not $DocxPath -or -not $PdfPath) {
    Write-Error "DocxPath and PdfPath are required parameters."
    exit 1
}

$resolvedDocx = (Resolve-Path $DocxPath).Path
$resolvedPdf = [System.IO.Path]::GetFullPath($PdfPath)

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($resolvedDocx, $false, $true) # read-only
    $doc.ExportAsFixedFormat($resolvedPdf, 17) # 17 = wdExportFormatPDF
    $doc.Close(0)
    Write-Host "SUCCESS: Exported to $resolvedPdf"
} catch {
    Write-Error "Failed to export PDF: $($_.Exception.Message)"
    exit 1
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
