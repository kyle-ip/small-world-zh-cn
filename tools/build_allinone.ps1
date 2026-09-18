# Build the all-in-one Chinese patch EXE (resources + enable/disable + launch)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$python = "C:\Python311\python.exe"
if (-not (Test-Path $python)) { $python = "python" }

Write-Host "==> Extract SmallWorld.exe icon (icoextract)"
& $python -m pip install --quiet icoextract pillow pyinstaller
& $python launcher\extract_icon.py

$icon = (Resolve-Path "launcher\app.ico").Path
$payload = (Resolve-Path "payload\Resources").Path

Write-Host "==> Build all-in-one EXE (icon from SmallWorld.exe + embedded payload)"
New-Item -ItemType Directory -Force -Path dist | Out-Null
& $python -m PyInstaller `
  --noconfirm --clean --windowed --onefile `
  --name "SmallWorld-cn" `
  --icon $icon `
  --distpath dist `
  --workpath dist\build\allinone `
  --specpath dist\build `
  --paths launcher `
  --hidden-import steam_lang `
  --hidden-import payload_install `
  --hidden-import PIL `
  --hidden-import PIL.Image `
  --hidden-import PIL.ImageTk `
  --collect-all PIL `
  --add-data "$payload;payload/Resources" `
  --add-data "$icon;." `
  launcher\app.py

if (-not (Test-Path "dist\SmallWorld-cn.exe")) {
  throw "dist\SmallWorld-cn.exe missing"
}

$GameRoot = Split-Path -Parent $Root
$Dest = Join-Path $GameRoot "SmallWorld-cn.exe"
Write-Host "==> Copy to game root: $Dest"
Copy-Item "dist\SmallWorld-cn.exe" $Dest -Force

Get-Item "dist\SmallWorld-cn.exe", $Dest | Format-List FullName, Length, LastWriteTime
Write-Host "Done. Distribute dist\SmallWorld-cn.exe (also copied to game root)."
