# Remove legacy ja-slot Chinese workflow from the game install.
# Safe: does NOT delete original language packs (en/ja/...).
$ErrorActionPreference = "Stop"
$Game = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path "$Game\SmallWorld.exe")) {
  throw "Not the Small World 2 root: $Game"
}

$Res = Join-Path $Game "Resources"
$remove = @(
  "$Res\ja.lproj.chinese",
  "$Res\ja.lproj.original",
  "$Res\compendium\ja.chinese",
  "$Res\compendium\ja.original",
  "$Res\compendium\ja-short.chinese",
  "$Res\compendium\ja-short.original",
  "$Res\compendium\image\mdpi\ja.chinese",
  "$Res\compendium\image\mdpi\en.backup",
  "$Res\credits\credits.html.original",
  "$Game\启用中文.bat",
  "$Game\恢复原版.bat"
)

# Ensure active ja matches original before deleting original backup
$active = Join-Path $Res "ja.lproj\localizedStrings.xml"
$orig = Join-Path $Res "ja.lproj.original\localizedStrings.xml"
if ((Test-Path $active) -and (Test-Path $orig)) {
  $ha = (Get-FileHash $active -Algorithm MD5).Hash
  $ho = (Get-FileHash $orig -Algorithm MD5).Hash
  if ($ha -ne $ho) {
    Write-Host "Restoring ja.lproj from ja.lproj.original..."
    Remove-Item "$Res\ja.lproj" -Recurse -Force
    Copy-Item "$Res\ja.lproj.original" "$Res\ja.lproj" -Recurse
  }
}

foreach ($p in $remove) {
  if (Test-Path $p) {
    Write-Host "Removing $p"
    Remove-Item $p -Recurse -Force
  }
}

Write-Host "Legacy cleanup done. Original language packs kept."
