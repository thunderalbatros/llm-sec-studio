#Requires -Version 5.1
param(
    [switch]$RunLiveEvals,
    [switch]$SkipLiveAuto,
    [switch]$SkipFullGates,
    [string]$Milestone = "",
    [double]$RemainingCreditsUsd = 73.0
)

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

function Test-LocalPort8000 {
    try {
        $h = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -TimeoutSec 2 -ErrorAction Stop
        return ($h.status -eq "ok")
    } catch {
        return $false
    }
}

Push-Location $RepoRoot
$liveFailed = $false
try {
    try {
        $shouldRunLive = $RunLiveEvals.IsPresent
        if (-not $shouldRunLive -and -not $SkipLiveAuto -and (Test-LocalPort8000)) {
            $changed = (git status --porcelain 2>$null | Out-String)
            if ($changed -match 'src/llm_sec_studio/(guardrails|tools)/|\.clinerules|skills_library/') {
                Write-Host "[AUTO] Detectados cambios en guardrails/tools/rules/skills con VM activa -> ejecutando evals live..." -ForegroundColor Cyan
                $shouldRunLive = $true
            }
        }

        if ($shouldRunLive) {
            Write-Host "`n>>> FASE 3A: Evals Live (antes de apagar VM) <<<" -ForegroundColor Yellow
            uv run pytest tests/evals/test_llm_live_evals.py -m live -v
            if ($LASTEXITCODE -ne 0) {
                $liveFailed = $true
                Write-Host "[WARN] Evals live devolvieron exit $LASTEXITCODE; apagando VM igualmente (FinOps)." -ForegroundColor Red
            }
        }
    } finally {
        Write-Host "`n>>> FASE 4: Apagado Obligatorio FinOps (`$0.00/h) <<<" -ForegroundColor Yellow
        & (Join-Path $PSScriptRoot "detener_llm.ps1")
    }

    Write-Host "`n>>> FASE 3B: QA Local & Persistencia (`$0.00/h) <<<" -ForegroundColor Yellow
    $qaFailed = $false

    if (-not $SkipFullGates) {
        Write-Host "`n=== uv run run-gates --full ===" -ForegroundColor Cyan
        uv run run-gates --full
        if ($LASTEXITCODE -ne 0) { $qaFailed = $true }

        Write-Host "`n=== uv run pytest tests/evals/ -m 'not live' ===" -ForegroundColor Cyan
        uv run pytest tests/evals/ -m "not live" -v
        if ($LASTEXITCODE -ne 0) { $qaFailed = $true }
    }

    Write-Host "`n=== toktoken index:update src ===" -ForegroundColor Cyan
    toktoken index:update src

    if ($Milestone) {
        Write-Host "`n=== icm.exe facts set last_milestone ===" -ForegroundColor Cyan
        icm.exe facts set llm-sec-studio last_milestone $Milestone
    }

    $handoffPath = Join-Path $RepoRoot "memory\session_handoff.md"
    if (Test-Path $handoffPath) {
        $age = (Get-Date) - (Get-Item $handoffPath).LastWriteTime
        if ($age.TotalHours -gt 4) {
            Write-Host "[RECORDATORIO] memory/session_handoff.md tiene $([math]::Round($age.TotalHours,1))h sin actualizar." -ForegroundColor DarkYellow
        }
    }

    Write-Host "`n--- git status --short ---" -ForegroundColor Gray
    git status --short

    Write-Host ""
    & (Join-Path $PSScriptRoot "estado_llm.ps1") -RemainingCreditsUsd $RemainingCreditsUsd

    if ($liveFailed -or $qaFailed) {
        Write-Host "`nVM APAGADA (`$0.00/h), pero hubo fallos en QA/evals. Revisar arriba." -ForegroundColor Red
        exit 1
    }
    Write-Host "`n=== SESION CERRADA LIMPIA (`$0.00/h GPU) ===" -ForegroundColor Green
} finally {
    Pop-Location
}
