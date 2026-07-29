# ==========================================
# AI Trading Research Platform
# Project Backup Manager v1.0
# ==========================================

$ProjectPath = "C:\Users\anast\scanner-project"
$BackupRoot = "$env:USERPROFILE\OneDrive\AI-Trading-Research-Backup"

# Create backup folder if needed
if (!(Test-Path $BackupRoot)) {
    New-Item -ItemType Directory -Path $BackupRoot | Out-Null
}

# Timestamp
$TimeStamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

# Temporary staging folder
$TempFolder = Join-Path $env:TEMP "AI_Backup_$TimeStamp"

New-Item -ItemType Directory -Path $TempFolder | Out-Null

Write-Host ""
Write-Host "========================================="
Write-Host "Creating Project Backup..."
Write-Host "========================================="
Write-Host ""

# Copy project while excluding unnecessary folders
robocopy `
    $ProjectPath `
    $TempFolder `
    /E `
    /XD venv __pycache__ .git .pytest_cache .mypy_cache `
    /XF *.pyc

# ZIP filename
$ZipFile = Join-Path $BackupRoot "AI_Trading_Backup_$TimeStamp.zip"

Compress-Archive `
    -Path "$TempFolder\*" `
    -DestinationPath $ZipFile `
    -CompressionLevel Optimal

# Remove temporary folder
Remove-Item $TempFolder -Recurse -Force

# Display information
$SizeMB = [math]::Round((Get-Item $ZipFile).Length / 1MB,2)

Write-Host ""
Write-Host "Backup Complete!"
Write-Host ""
Write-Host "Location:"
Write-Host $ZipFile
Write-Host ""
Write-Host "Size:"
Write-Host "$SizeMB MB"
Write-Host ""
Write-Host "========================================="