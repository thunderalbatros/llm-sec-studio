#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$RuntimeDir = Join-Path $HOME "scripts-gcp-llm"
$StateFile = Join-Path $RuntimeDir "vm_state.json"
$Project = "project-6565e6dc-f33c-49ff-b22"
$Zone = "us-central1-b"
$Instance = "llm-qwen-abliterated"
$LocalPort = 8000
$PidFile = Join-Path $RuntimeDir ".tunnel.pid"
$HeadroomPidFile = Join-Path $RuntimeDir ".headroom.pid"

if (Test-Path $StateFile) {
    try {
        $st = Get-Content $StateFile -Raw | ConvertFrom-Json
        if ($st.project) { $Project = $st.project }
        if ($st.instance) { $Instance = $st.instance }
        if ($st.zone) { $Zone = $st.zone }
    } catch {}
}

function Get-GcloudPath {
    $cmd = Get-Command "gcloud.cmd" -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $cmd = Get-Command "gcloud" -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    throw "No se encontro gcloud CLI en el PATH."
}

Write-Host "[1/2] Cerrando tunel SSH/IAP local (127.0.0.1:$LocalPort) y Headroom proxy..." -ForegroundColor Cyan
$ErrorActionPreference = "Continue"
foreach ($pf in @($PidFile, $HeadroomPidFile)) {
    if (Test-Path $pf) {
        $savedPid = (Get-Content $pf -ErrorAction SilentlyContinue | Select-Object -First 1)
        if ($savedPid -match '^\d+$') {
            if (Get-Process -Id ([int]$savedPid) -ErrorAction SilentlyContinue) {
                & cmd.exe /c "taskkill /PID $savedPid /T /F >nul 2>&1"
            }
        }
        Remove-Item $pf -Force -ErrorAction SilentlyContinue
    }
}

Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
    Where-Object {
        $_.ProcessId -ne $PID -and
        $_.CommandLine -match 'proxy' -and
        ($_.Name -match '^headroom' -or ($_.Name -match '^python' -and $_.CommandLine -match 'headroom\.exe'))
    } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

$listeners = Get-NetTCPConnection -LocalAddress "127.0.0.1" -LocalPort $LocalPort -State Listen -ErrorAction SilentlyContinue
foreach ($l in $listeners) {
    $p = Get-Process -Id $l.OwningProcess -ErrorAction SilentlyContinue
    if ($p -and $p.ProcessName -match 'plink|ssh|python') {
        Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
    }
}

$headroomListeners = Get-NetTCPConnection -LocalAddress "127.0.0.1" -LocalPort 8787 -State Listen -ErrorAction SilentlyContinue
foreach ($hl in $headroomListeners) {
    $hp = Get-Process -Id $hl.OwningProcess -ErrorAction SilentlyContinue
    if ($hp -and $hp.ProcessName -match 'headroom|python') {
        Stop-Process -Id $hp.Id -Force -ErrorAction SilentlyContinue
    }
}

Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match [regex]::Escape($Instance) -and $_.CommandLine -match 'start-iap-tunnel|8000:127\.0\.0\.1:8000' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

$ErrorActionPreference = "Stop"
$gcloud = Get-GcloudPath
$ErrorActionPreference = "Continue"
$status = ((& $gcloud compute instances describe $Instance --zone=$Zone --project=$Project --format="value(status)" 2>$null) | Out-String).Trim()
$ErrorActionPreference = "Stop"

if (-not $status) {
    $ErrorActionPreference = "Continue"
    $discZone = ((& $gcloud compute instances list --filter="name=$Instance" --project=$Project --format="value(zone.basename())" 2>$null) | Out-String).Trim().Split("`n")[0].Trim()
    $ErrorActionPreference = "Stop"
    if ($discZone) {
        $Zone = $discZone
        $ErrorActionPreference = "Continue"
        $status = ((& $gcloud compute instances describe $Instance --zone=$Zone --project=$Project --format="value(status)" 2>$null) | Out-String).Trim()
        $ErrorActionPreference = "Stop"
    }
}

if ($status -eq "TERMINATED") {
    Write-Host "[2/2] La VM '$Instance' ($Zone) ya esta detenida (TERMINATED). Gasto de computo: `$0.00/h." -ForegroundColor Green
    exit 0
}

Write-Host "[2/2] Deteniendo VM '$Instance' ($Zone)..." -ForegroundColor Yellow
$ErrorActionPreference = "Continue"
& $gcloud compute instances stop $Instance --zone=$Zone --project=$Project --quiet
$stopExit = $LASTEXITCODE
$ErrorActionPreference = "Stop"
if ($stopExit -ne 0) {
    Write-Error "Fallo al detener la VM '$Instance' en '$Zone'."
    exit 1
}

$ErrorActionPreference = "Continue"
$finalStatus = ((& $gcloud compute instances describe $Instance --zone=$Zone --project=$Project --format="value(status)" 2>$null) | Out-String).Trim()
$ErrorActionPreference = "Stop"
Write-Host "VM '$Instance' ($Zone) en estado: $finalStatus. Gasto de GPU/vCPU: `$0.00/h (solo almacenamiento pd-balanced 100GB ~`$0.33/dia)." -ForegroundColor Green
