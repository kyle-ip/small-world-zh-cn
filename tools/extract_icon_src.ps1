Add-Type -AssemblyName System.Drawing
$exe = "C:\Program Files (x86)\Steam\steamapps\common\SmallWorld2\SmallWorld.exe"
$tmpPng = Join-Path $env:TEMP "sw2_icon_src.png"
$icon = [System.Drawing.Icon]::ExtractAssociatedIcon($exe)
$bmp = $icon.ToBitmap()
$bmp.Save($tmpPng, [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
$icon.Dispose()
Write-Output $tmpPng
