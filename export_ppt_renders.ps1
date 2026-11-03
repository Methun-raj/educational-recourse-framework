$pptFile = "C:\Users\Methunraj A\Downloads\bro\PROJECT_REVIEW_PRESENTATION.pptx"
$pdfFile = "C:\Users\Methunraj A\Downloads\bro\PROJECT_REVIEW_PRESENTATION.pdf"
$exportDir = "C:\Users\Methunraj A\Downloads\bro\slide_renders"

try {
    $pptApp = New-Object -ComObject PowerPoint.Application
    $pres = $pptApp.Presentations.Open($pptFile, 1, 0, 0) # ReadOnly=1, Untitled=0, WithWindow=0
    if (!(Test-Path $exportDir)) {
        New-Item -ItemType Directory -Path $exportDir | Out-Null
    }
    
    $pres.SaveAs($pdfFile, 32) # 32 = ppSaveAsPDF
    Write-Host "[OK] PDF Export Success: $pdfFile"
    
    $slideIdx = 1
    foreach ($slide in $pres.Slides) {
        $outImg = "$exportDir\slide_$slideIdx.png"
        $slide.Export($outImg, "PNG", 1920, 1080)
        $slideIdx++
    }
    Write-Host "[OK] Exported $($slideIdx - 1) slides as PNG to $exportDir"
    $pres.Close()
    $pptApp.Quit()
} catch {
    Write-Host "Error: $_"
}
