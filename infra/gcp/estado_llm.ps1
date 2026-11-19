#Requires -Version 5.1
param(
    [double]$RemainingCreditsUsd = 73.0
)

$ErrorActionPreference = "Stop"

$RuntimeDir = Join-Path $HOME "scripts-gcp-llm"
$StateFile = Join-Path $RuntimeDir "vm_state.json"
$Project = "project-6565e6dc-f33c-49ff-b22"
$Zone = "us-central1-b"
$Instance = "llm-qwen-abliterated"
$LocalPort = 8000
$IpHourlyUsd = 0.005
$DiskMonthlyUsd = 10.00
$DiskHourlyUsd = [math]::Round($DiskMonthlyUsd / 730.0, 4)

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

$gcloud = Get-GcloudPath
$ErrorActionPreference = "Continue"
$vmJson = & $gcloud compute instances describe $Instance --zone=$Zone --project=$Project --format=json 2>$null
$ErrorActionPreference = "Stop"

if (-not $vmJson) {
    $ErrorActionPreference = "Continue"
    $discZone = ((& $gcloud compute instances list --filter="name=$Instance" --project=$Project --format="value(zone.basename())" 2>$null) | Out-String).Trim().Split("`n")[0].Trim()
    $ErrorActionPreference = "Stop"
    if ($discZone) {
        $Zone = $discZone
        $ErrorActionPreference = "Continue"
        $vmJson = & $gcloud compute instances describe $Instance --zone=$Zone --project=$Project --format=json 2>$null
        $ErrorActionPreference = "Stop"
    }
}

if (-not $vmJson) {
    Write-Error "No se encontro la instancia '$Instance' en '$Zone'."
    exit 1
}
$vm = $vmJson | ConvertFrom-Json

$vmStatus = $vm.status
$machineType = ($vm.machineType -split '/')[-1]
$provModel = $vm.scheduling.provisioningModel
$termAction = $vm.scheduling.instanceTerminationAction

$ComputeHourlyUsd = if ($provModel -eq "STANDARD") { 0.707 } else { 0.423 }
$TotalRunningHourlyUsd = [math]::Round($ComputeHourlyUsd + $IpHourlyUsd + $DiskHourlyUsd, 4)
$modeLabel = if ($termAction) { "$provModel (termination=$termAction)" } else { "$provModel (On-Demand)" }

Write-Host "=== ESTADO DE INFRAESTRUCTURA GCP LLM ===" -ForegroundColor Cyan
Write-Host ("Instancia       : {0} ({1})" -f $Instance, $Zone)
Write-Host ("Maquina / Modo  : {0} | {1}" -f $machineType, $modeLabel)
$statusColor = if ($vmStatus -eq "RUNNING") { "Green" } else { "Yellow" }
Write-Host ("Estado VM       : {0}" -f $vmStatus) -ForegroundColor $statusColor

$listener = Get-NetTCPConnection -LocalAddress "127.0.0.1" -LocalPort $LocalPort -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
if ($listener) {
    Write-Host ("Tunel Local     : ACTIVO en 127.0.0.1:{0} (PID {1})" -f $LocalPort, $listener.OwningProcess) -ForegroundColor Green
} else {
    Write-Host ("Tunel Local     : INACTIVO en 127.0.0.1:{0}" -f $LocalPort) -ForegroundColor DarkYellow
}

try {
    $health = Invoke-RestMethod -Uri "http://127.0.0.1:$LocalPort/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host ("Endpoint /health: OK ({0})" -f $health.status) -ForegroundColor Green

    $secretsPath = Join-Path $HOME ".cline\data\secrets.json"
    if (Test-Path $secretsPath) {
        $sec = Get-Content $secretsPath -Raw | ConvertFrom-Json
        if ($sec.openAiApiKey) {
            $models = Invoke-RestMethod -Uri "http://127.0.0.1:$LocalPort/v1/models" -Headers @{ Authorization = "Bearer $($sec.openAiApiKey)" } -TimeoutSec 3 -ErrorAction Stop
            $modelIds = ($models.data | ForEach-Object { $_.id }) -join ", "
            Write-Host ("Modelos /v1     : {0}" -f $modelIds) -ForegroundColor Green
        }
    }
} catch {
    Write-Host "Endpoint /health: NO RESPONDE" -ForegroundColor DarkYellow
}

Write-Host ""
Write-Host "=== ESTIMACION FINOPS (Base `$73 USD o parametro -RemainingCreditsUsd) ===" -ForegroundColor Cyan
Write-Host ("Costo VM encendida : ~`${0}/h ({1} ~`${2}/h + IP efimera `${3}/h + disco `${4}/h)" -f $TotalRunningHourlyUsd, $provModel, $ComputeHourlyUsd, $IpHourlyUsd, $DiskHourlyUsd)
Write-Host ("Costo VM apagada   : `$0.00/h computo (solo disco 100GB pd-balanced ~`${0}/mes = ~`${1}/dia)" -f $DiskMonthlyUsd, [math]::Round($DiskMonthlyUsd / 30.0, 2))
$hoursLeft = [math]::Round($RemainingCreditsUsd / $TotalRunningHourlyUsd, 1)
Write-Host ("Horas estimadas    : ~{0} h de uso activo con `${1} USD restantes" -f $hoursLeft, $RemainingCreditsUsd) -ForegroundColor Green
