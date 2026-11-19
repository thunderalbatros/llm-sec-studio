#Requires -Version 5.1
param(
    [int]$Port = 8787,
    [string]$UpstreamUrl = "http://127.0.0.1:8000",
    [switch]$Background
)

$ErrorActionPreference = "Stop"
$LocalBin = Join-Path $HOME ".local\bin"
$HeadroomExe = Join-Path $LocalBin "headroom.exe"
if (-not (Test-Path $HeadroomExe)) {
    $cmd = Get-Command "headroom" -ErrorAction SilentlyContinue
    if ($cmd) { $HeadroomExe = $cmd.Source } else { throw "No se encontro headroom. Instala con: uv tool install 'headroom-ai[proxy]'" }
}

$RuntimeDir = Join-Path $HOME "scripts-gcp-llm"
New-Item -ItemType Directory -Force -Path $RuntimeDir | Out-Null
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$CacheDir = Join-Path $RepoRoot ".cache"
New-Item -ItemType Directory -Force -Path $CacheDir | Out-Null
$LogFile = Join-Path $CacheDir "headroom_proxy.jsonl"
$ArgsList = @(
    "proxy",
    "--host", "127.0.0.1",
    "--port", "$Port",
    "--openai-api-url", $UpstreamUrl,
    "--mode", "cache",
    "--disable-kompress",
    "--no-telemetry",
    "--log-file", $LogFile
)

if ($Background) {
    $PidFile = Join-Path $RuntimeDir ".headroom.pid"
    $OutLog = Join-Path $env:TEMP "headroom-proxy.out.log"
    $ErrLog = Join-Path $env:TEMP "headroom-proxy.err.log"
    $proc = Start-Process -FilePath $HeadroomExe -ArgumentList $ArgsList -WindowStyle Hidden -PassThru -RedirectStandardOutput $OutLog -RedirectStandardError $ErrLog
    Set-Content -Path $PidFile -Value $proc.Id -Encoding Ascii
    Write-Host "Headroom Proxy v0.44 activo en http://127.0.0.1:$Port/v1 -> $UpstreamUrl (PID $($proc.Id), modo=cache, CCR=ON, sin ML pesado)." -ForegroundColor Green
} else {
    Write-Host "Iniciando Headroom Proxy v0.44 en http://127.0.0.1:$Port/v1 -> $UpstreamUrl (Ctrl+C para detener)..." -ForegroundColor Cyan
    & $HeadroomExe @ArgsList
}
