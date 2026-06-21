<#
Set a stable Windows development terminal for this project.

Run from PowerShell before local development. If your execution policy blocks
local scripts, use the first command:

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; . .\scripts\dev-env.ps1

Otherwise:

    . .\scripts\dev-env.ps1

The script keeps Python, pytest and PowerShell output on UTF-8, which prevents
Chinese docs/logs from appearing as mojibake in Windows terminals.
#>

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

try {
    chcp 65001 | Out-Null
} catch {
    Write-Warning "Failed to switch console code page to UTF-8: $($_.Exception.Message)"
}

$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8NoBom
[Console]::OutputEncoding = $utf8NoBom
$global:OutputEncoding = $utf8NoBom

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

if (-not $env:OPENBLAS_NUM_THREADS) {
    $env:OPENBLAS_NUM_THREADS = "1"
}

Write-Host "Dev terminal ready: UTF-8, PYTHONUTF8=1, OPENBLAS_NUM_THREADS=$env:OPENBLAS_NUM_THREADS"
