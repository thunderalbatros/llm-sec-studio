#Requires -Version 5.1
param(
    [switch]$OfflineOnly,
    [switch]$NoHeadroom,
    [switch]$SmokeTest,
    [switch]$ForceStart,
    [double]$RemainingCreditsUsd = 73.0
)

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

function Invoke-Step {
    param(
        [string]$Label,
        [scriptblock]$Action
    )
    Write-Host "`n=== $Label ===" -ForegroundColor Cyan
    & $Action
    if ($LASTEXITCODE -ne 0) {
        throw "Fallo '$Label' (exit $LASTEXITCODE)."
    }
}

Push-Location $RepoRoot
try {
    Write-Host ">>> FASE 0: Preflight Local (`$0.00/h, VM apagada) <<<" -ForegroundColor Yellow

    Write-Host "`n--- git status --short ---" -ForegroundColor Gray
    git status --short

    Write-Host "`n--- icm.exe facts list llm-sec-studio ---" -ForegroundColor Gray
    icm.exe facts list llm-sec-studio

    $handoffPath = Join-Path $RepoRoot "memory\session_handoff.md"
    if (Test-Path $handoffPath) {
        Write-Host "`n--- memory/session_handoff.md ---" -ForegroundColor Gray
        Get-Content -Path $handoffPath -Encoding UTF8
    }

    $preflightFailed = $false
    try {
        Invoke-Step "uv run run-gates" { uv run run-gates }
        Invoke-Step "uv run pytest tests/evals/ -m 'not live'" { uv run pytest tests/evals/ -m "not live" -v }
        Invoke-Step "toktoken index:update src" { toktoken index:update src }
    } catch {
        $preflightFailed = $true
        Write-Host "[PREFLIGHT] $($_.Exception.Message)" -ForegroundColor Red
        if (-not $ForceStart) {
            Write-Host "Abortado antes de encender la VM GCP (`$0.00 gastados). Usa -ForceStart para omitir." -ForegroundColor Yellow
            exit 1
        }
        Write-Host "[WARN] Continuando por -ForceStart..." -ForegroundColor DarkYellow
    }

    if ($OfflineOnly) {
        Write-Host "`nLISTO (Modo -OfflineOnly | `$0.00/h GPU). Preflight completo." -ForegroundColor Green
        exit 0
    }

    Write-Host "`n>>> FASE 1: Arranque VM GCP + IAP (:8000) + Headroom (:8787) <<<" -ForegroundColor Yellow
    & (Join-Path $PSScriptRoot "iniciar_llm.ps1")
    if ($LASTEXITCODE -ne 0) {
        throw "iniciar_llm.ps1 fallo (exit $LASTEXITCODE)."
    }

    if (-not $NoHeadroom) {
        $hrAlive = $false
        try {
            $h = Invoke-RestMethod -Uri "http://127.0.0.1:8787/health" -TimeoutSec 2 -ErrorAction Stop
            if ($h.ready -eq $true) { $hrAlive = $true }
        } catch {}

        if (-not $hrAlive) {
            & (Join-Path $PSScriptRoot "iniciar_headroom.ps1") -Background
            for ($i = 1; $i -le 15; $i++) {
                try {
                    $h = Invoke-RestMethod -Uri "http://127.0.0.1:8787/health" -TimeoutSec 2 -ErrorAction Stop
                    if ($h.ready -eq $true) {
                        $hrAlive = $true
                        Write-Host "Headroom /health OK (ready=true, mode=$($h.config.mode), pid=$($h.config.pid))." -ForegroundColor Green
                        break
                    }
                } catch {}
                Start-Sleep -Seconds 1
            }
            if (-not $hrAlive) {
                throw "Headroom no respondio /health en 127.0.0.1:8787 tras 15s."
            }
        } else {
            Write-Host "Headroom ya activo y sano en http://127.0.0.1:8787/v1." -ForegroundColor Green
        }
    }

    & (Join-Path $PSScriptRoot "estado_llm.ps1") -RemainingCreditsUsd $RemainingCreditsUsd

    if ($SmokeTest) {
        Invoke-Step "uv run llm-bench" { uv run llm-bench }
    }

    $activeUrl = if ($NoHeadroom) { "http://127.0.0.1:8000/v1" } else { "http://127.0.0.1:8787/v1" }
    Write-Host "`n=== SESION LISTA PARA CLINE ===" -ForegroundColor Green
    Write-Host "Workspace : $RepoRoot" -ForegroundColor Green
    Write-Host "Endpoint  : $activeUrl" -ForegroundColor Green
    Write-Host "Al cerrar : ~\scripts-gcp-llm\cerrar_sesion.ps1" -ForegroundColor Yellow
} finally {
    Pop-Location
}
