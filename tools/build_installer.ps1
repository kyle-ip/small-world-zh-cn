# Build Small World 2 zh-CN installer artifacts
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$python = "C:\Python311\python.exe"
if (-not (Test-Path $python)) { $python = "python" }

Write-Host "==> Wizard images"
& $python installer\make_wizard_images.py

if (-not (Test-Path "installer\ChineseSimplified.isl")) {
  Write-Host "==> Download ChineseSimplified.isl"
  Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/gh/kira-96/Inno-Setup-Chinese-Simplified-Translation@main/ChineseSimplified.isl" -OutFile "installer\ChineseSimplified.isl" -UseBasicParsing
}

Write-Host "==> Extract game icon"
& $python launcher\extract_icon.py

Write-Host "==> Ensure PyInstaller / Pillow"
& $python -m pip install --quiet pyinstaller pillow

Write-Host "==> Build launcher EXE (standalone, no Python at runtime)"
New-Item -ItemType Directory -Force -Path dist\launcher | Out-Null
& $python -m PyInstaller `
  --noconfirm --clean --windowed --onefile `
  --name SmallWorld-cn-Launcher `
  --icon ((Resolve-Path "launcher\app.ico").Path) `
  --distpath dist\launcher `
  --workpath dist\build\launcher `
  --specpath dist\build `
  --paths launcher `
  --hidden-import steam_lang `
  launcher\app.py

if (-not (Test-Path "dist\launcher\SmallWorld-cn-Launcher.exe")) {
  throw "Launcher EXE missing"
}

# Locate Inno Setup Compiler
$isccCandidates = @(
  "${env:LocalAppData}\Programs\Inno Setup 6\ISCC.exe",
  "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
  "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
)
$iscc = $isccCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $iscc) {
  Write-Host "Inno Setup 6 not found. Attempting winget install..."
  winget install --id JRSoftware.InnoSetup -e --accept-package-agreements --accept-source-agreements
  $iscc = $isccCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}

if (-not $iscc) {
  Write-Warning "ISCC.exe still not found. Launcher built; compile .iss manually later."
  exit 0
}

Write-Host "==> Compile installer with $iscc"
& $iscc installer\small-world-zh-cn.iss
Write-Host "Done. See dist\"
Get-ChildItem dist -File | Format-Table Name, Length
