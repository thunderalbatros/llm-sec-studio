#Requires -Version 5.1
param(
    [int]$TimeoutSeconds = 240,
    [switch]$ForceMigrate,
    [string]$TargetZone = "",
    [switch]$NoTunnel
)

$ErrorActionPreference = "Stop"

$RuntimeDir = Join-Path $HOME "scripts-gcp-llm"
New-Item -ItemType Directory -Force -Path $RuntimeDir | Out-Null
$StateFile = Join-Path $RuntimeDir "vm_state.json"
$LocalPort = 8000
$PidFile = Join-Path $RuntimeDir ".tunnel.pid"
$OutLog = Join-Path $env:TEMP "qwen-iap-tunnel.out.log"
$ErrLog = Join-Path $env:TEMP "qwen-iap-tunnel.err.log"

$DefaultProject = "project-6565e6dc-f33c-49ff-b22"
$DefaultInstance = "llm-qwen-abliterated"
$DefaultZone = "us-central1-b"
$DefaultNetwork = "llm-vpc"
$DefaultServiceAccount = "sa-llm-zero-priv@project-6565e6dc-f33c-49ff-b22.iam.gserviceaccount.com"

$RegionSubnets = @{
    "us-central1"             = @{ Name = "llm-subnet";        Cidr = "10.200.0.0/24" }
    "us-east1"                = @{ Name = "llm-subnet-east1";  Cidr = "10.201.0.0/24" }
    "us-west1"                = @{ Name = "llm-subnet-west1";  Cidr = "10.202.0.0/24" }
    "us-east4"                = @{ Name = "llm-subnet-east4";  Cidr = "10.203.0.0/24" }
    "us-west4"                = @{ Name = "llm-subnet-west4";  Cidr = "10.204.0.0/24" }
    "northamerica-northeast1" = @{ Name = "llm-subnet-na-ne1"; Cidr = "10.205.0.0/24" }
    "northamerica-northeast2" = @{ Name = "llm-subnet-na-ne2"; Cidr = "10.206.0.0/24" }
    "europe-west4"            = @{ Name = "llm-subnet-eu-w4";  Cidr = "10.207.0.0/24" }
}

$FallbackZones = @(
    "us-west1-a", "us-west1-b", "us-west1-c",
    "us-central1-a", "us-central1-c", "us-central1-b",
    "us-east1-b", "us-east1-c", "us-east1-d",
    "us-west4-a", "us-west4-c",
    "us-east4-a", "us-east4-c",
    "northamerica-northeast1-b", "northamerica-northeast1-c",
    "northamerica-northeast2-a", "northamerica-northeast2-b",
    "europe-west4-a", "europe-west4-b", "europe-west4-c"
)

function Get-GcloudPath {
    $cmd = Get-Command "gcloud.cmd" -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $cmd = Get-Command "gcloud" -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    throw "No se encontro gcloud CLI en el PATH."
}

function Get-RegionFromZone([string]$z) {
    return ($z -replace '-[a-z]$', '')
}

function Resolve-RegionSubnet([string]$gcloud, [string]$project, [string]$network, [string]$region) {
    if (-not $RegionSubnets.ContainsKey($region)) { return $null }
    $info = $RegionSubnets[$region]
    $subName = $info.Name
    $cidr = $info.Cidr
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $gcloud compute networks subnets describe $subName --region=$region --project=$project 2>$null | Out-Null
    $exists = ($LASTEXITCODE -eq 0)
    if (-not $exists) {
        Write-Host "[FAILOVER] Creando subnet '$subName' ($cidr) en '$region' dentro de '$network' (`$0/mes)..." -ForegroundColor Gray
        & $gcloud compute networks subnets create $subName --network=$network --region=$region --range=$cidr --project=$project --quiet 2>$null | Out-Null
        $exists = ($LASTEXITCODE -eq 0)
    }
    $ErrorActionPreference = $prev
    if ($exists) { return $subName }
    return $null
}

function Get-VmState {
    if (Test-Path $StateFile) {
        try {
            return (Get-Content $StateFile -Raw | ConvertFrom-Json)
        } catch {}
    }
    $reg = Get-RegionFromZone $DefaultZone
    return [pscustomobject]@{
        project            = $DefaultProject
        instance           = $DefaultInstance
        zone               = $DefaultZone
        region             = $reg
        subnet             = $RegionSubnets[$reg].Name
        network            = $DefaultNetwork
        machine_type       = "g2-standard-4"
        provisioning_model = "STANDARD"
        service_account    = $DefaultServiceAccount
        updated_at         = (Get-Date).ToString("o")
    }
}

function Save-VmState($stateObj) {
    $stateObj.updated_at = (Get-Date).ToString("o")
    $json = $stateObj | ConvertTo-Json -Depth 4
    Set-Content -Path $StateFile -Value $json -Encoding UTF8
}

function Find-ActiveInstanceZone([string]$gcloud, [string]$project, [string]$instance) {
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $raw = (& $gcloud compute instances list --filter="name=$instance" --project=$project --format="value(zone.basename(),status)" 2>$null | Out-String).Trim()
    $ErrorActionPreference = $prev
    if (-not $raw) { return $null }
    $lines = $raw -split "`r?`n" | Where-Object { $_.Trim() -ne "" }
    foreach ($ln in $lines) {
        $parts = $ln.Trim() -split "\s+"
        if ($parts.Count -ge 2 -and $parts[1] -eq "RUNNING") {
            return [pscustomobject]@{ Zone = $parts[0]; Status = $parts[1] }
        }
    }
    $first = ($lines[0].Trim() -split "\s+")
    if ($first.Count -ge 2) {
        return [pscustomobject]@{ Zone = $first[0]; Status = $first[1] }
    }
    return $null
}

function Test-HealthEndpoint {
    try {
        $resp = Invoke-RestMethod -Uri "http://127.0.0.1:$LocalPort/health" -TimeoutSec 3 -ErrorAction Stop
        if ($resp.status -eq "ok") { return "ok" }
        return "loading"
    } catch {
        $statusCode = $null
        if ($_.Exception.Response -and $_.Exception.Response.StatusCode) {
            $statusCode = [int]$_.Exception.Response.StatusCode
        }
        if ($statusCode -eq 503) { return "loading" }
        return "down"
    }
}

function Stop-ExistingTunnel {
    $prevEAP = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        if (Test-Path $PidFile) {
            $savedPid = (Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1)
            if ($savedPid -match '^\d+$') {
                if (Get-Process -Id ([int]$savedPid) -ErrorAction SilentlyContinue) {
                    & cmd.exe /c "taskkill /PID $savedPid /T /F >nul 2>&1"
                }
            }
            Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
        }
        $listeners = Get-NetTCPConnection -LocalAddress "127.0.0.1" -LocalPort $LocalPort -State Listen -ErrorAction SilentlyContinue
        foreach ($l in $listeners) {
            $p = Get-Process -Id $l.OwningProcess -ErrorAction SilentlyContinue
            if ($p -and $p.ProcessName -match 'plink|ssh|python') {
                Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
            }
        }
        Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
            Where-Object { $_.CommandLine -match [regex]::Escape($Instance) -and $_.CommandLine -match 'start-iap-tunnel|8000:127\.0\.0\.1:8000' } |
            ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
    } finally {
        $ErrorActionPreference = $prevEAP
    }
}

function Find-AvailableL4Zone {
    param(
        [string]$Gcloud,
        [pscustomobject]$State,
        [string]$SourceZone,
        [string[]]$CandidateZones
    )
    $proj = $State.project
    $net = $State.network
    $probeName = "llm-l4-probe-" + (Get-Date -Format "HHmmss")

    foreach ($candZone in $CandidateZones) {
        if (-not $candZone -or $candZone -eq $SourceZone) { continue }
        $candRegion = Get-RegionFromZone $candZone
        $candSubnet = Resolve-RegionSubnet $Gcloud $proj $net $candRegion
        if (-not $candSubnet) { continue }

        Write-Host "[PROBE] Verificando capacidad real L4 en '$candZone'..." -ForegroundColor Cyan
        $ErrorActionPreference = "Continue"
        $probeOut = (& $Gcloud compute instances create $probeName `
            --zone=$candZone `
            --project=$proj `
            --machine-type=g2-standard-4 `
            --provisioning-model=STANDARD `
            --maintenance-policy=TERMINATE `
            --network=$net `
            --subnet=$candSubnet `
            --no-address `
            --no-service-account `
            --no-scopes `
            --image-family=debian-12 `
            --image-project=debian-cloud `
            --boot-disk-size=10GB `
            --quiet 2>&1 | Out-String)
        $probeExit = $LASTEXITCODE
        $ErrorActionPreference = "Stop"

        if ($probeExit -eq 0) {
            Write-Host "[PROBE] CAPACIDAD CONFIRMADA en '$candZone'! Eliminando sonda..." -ForegroundColor Green
            $ErrorActionPreference = "Continue"
            & $Gcloud compute instances delete $probeName --zone=$candZone --project=$proj --quiet 2>$null | Out-Null
            $ErrorActionPreference = "Stop"
            return [pscustomobject]@{ Zone = $candZone; Region = $candRegion; Subnet = $candSubnet }
        }

        if ($probeOut -match 'ZONE_RESOURCE_POOL_EXHAUSTED|STOCKOUT') {
            Write-Host "[PROBE] '$candZone' sin stock L4." -ForegroundColor DarkYellow
        } else {
            $firstErr = ($probeOut -split "`r?`n" | Where-Object { $_ -match 'ERROR|message:' } | Select-Object -First 2) -join " | "
            Write-Host "[PROBE] '$candZone' rechazada: $firstErr" -ForegroundColor DarkYellow
        }
    }
    return $null
}

function Invoke-ZeroTrustFailover {
    param(
        [string]$Gcloud,
        [pscustomobject]$State,
        [string]$SourceZone,
        [string[]]$CandidateZones
    )

    $proj = $State.project
    $inst = $State.instance
    $net = $State.network
    $sa = $State.service_account

    $chosen = Find-AvailableL4Zone -Gcloud $Gcloud -State $State -SourceZone $SourceZone -CandidateZones $CandidateZones
    if (-not $chosen) {
        throw "Ninguna de las $($CandidateZones.Count) zonas candidatas tiene stock L4 disponible en este momento."
    }

    $targetZone = $chosen.Zone
    $targetSubnet = $chosen.Subnet
    $snap = "llm-failover-" + (Get-Date -Format "yyyyMMddHHmmss")

    Write-Host "[FAILOVER] Creando snapshot temporal '$snap' desde '$SourceZone' para migrar a '$targetZone'..." -ForegroundColor Yellow
    $ErrorActionPreference = "Continue"
    & $Gcloud compute snapshots create $snap --source-disk=$inst --source-disk-zone=$SourceZone --storage-location=us --project=$proj --quiet 2>&1 | Out-Host
    $snapExit = $LASTEXITCODE
    $ErrorActionPreference = "Stop"
    if ($snapExit -ne 0) {
        throw "Fallo la creacion del snapshot temporal '$snap' desde '$SourceZone'."
    }

    try {
        Write-Host "[FAILOVER] Clonando disco 100GB en '$targetZone'..." -ForegroundColor Cyan
        $ErrorActionPreference = "Continue"
        & $Gcloud compute disks create $inst --source-snapshot=$snap --type=pd-balanced --size=100GB --zone=$targetZone --project=$proj --quiet 2>&1 | Out-Host
        $diskExit = $LASTEXITCODE
        $ErrorActionPreference = "Stop"
        if ($diskExit -ne 0) {
            throw "Fallo al crear disco '$inst' en '$targetZone'."
        }

        Write-Host "[FAILOVER] Creando VM Zero-Trust '$inst' en '$targetZone' (subnet '$targetSubnet')..." -ForegroundColor Cyan
        $ErrorActionPreference = "Continue"
        $createOut = (& $Gcloud compute instances create $inst `
            --zone=$targetZone `
            --project=$proj `
            --machine-type=g2-standard-4 `
            --provisioning-model=STANDARD `
            --maintenance-policy=TERMINATE `
            --restart-on-failure `
            --network=$net `
            --subnet=$targetSubnet `
            --service-account=$sa `
            --no-scopes `
            --shielded-secure-boot `
            --shielded-vtpm `
            --shielded-integrity-monitoring `
            --disk="name=$inst,boot=yes,auto-delete=yes" `
            --quiet 2>&1 | Out-String)
        $createExit = $LASTEXITCODE
        $ErrorActionPreference = "Stop"

        if ($createExit -ne 0) {
            Write-Host "[FAILOVER] Error al levantar VM en '$targetZone': $createOut" -ForegroundColor Red
            $ErrorActionPreference = "Continue"
            & $Gcloud compute disks delete $inst --zone=$targetZone --project=$proj --quiet 2>$null | Out-Null
            $ErrorActionPreference = "Stop"
            throw "No se pudo crear la VM en '$targetZone' tras el snapshot."
        }

        Write-Host "[FAILOVER] Eliminando instancia y disco viejo en '$SourceZone' (cero almacenamiento duplicado)..." -ForegroundColor Yellow
        $ErrorActionPreference = "Continue"
        & $Gcloud compute instances delete $inst --zone=$SourceZone --project=$proj --quiet 2>&1 | Out-Host
        $ErrorActionPreference = "Stop"

        $State.zone = $targetZone
        $State.region = $chosen.Region
        $State.subnet = $targetSubnet
        Save-VmState $State
        Write-Host "[FAILOVER] EXITO! Migrada a '$targetZone' con blindaje Zero-Trust intacto y vm_state.json actualizado." -ForegroundColor Green
        return $targetZone
    } finally {
        Write-Host "[FAILOVER] Limpiando snapshot temporal '$snap'..." -ForegroundColor Gray
        $ErrorActionPreference = "Continue"
        & $Gcloud compute snapshots delete $snap --project=$proj --quiet 2>$null | Out-Null
        $ErrorActionPreference = "Stop"
    }
}

$gcloud = Get-GcloudPath
$vmState = Get-VmState
$Project = $vmState.project
$Instance = $vmState.instance
$Zone = $vmState.zone

Write-Host "[1/4] Verificando estado de VM '$Instance' (zona registrada: $Zone)..." -ForegroundColor Cyan
$ErrorActionPreference = "Continue"
$status = ((& $gcloud compute instances describe $Instance --zone=$Zone --project=$Project --format="value(status)" 2>$null) | Out-String).Trim()
$ErrorActionPreference = "Stop"

if (-not $status) {
    Write-Host "Instancia no encontrada en '$Zone'; buscando zona activa en GCP..." -ForegroundColor Yellow
    $found = Find-ActiveInstanceZone $gcloud $Project $Instance
    if (-not $found) {
        Write-Error "No se encontro ninguna instancia llamada '$Instance' en el proyecto '$Project'."
        exit 1
    }
    $Zone = $found.Zone
    $status = $found.Status
    $vmState.zone = $Zone
    $vmState.region = (Get-RegionFromZone $Zone)
    if ($RegionSubnets.ContainsKey($vmState.region)) { $vmState.subnet = $RegionSubnets[$vmState.region].Name }
    Save-VmState $vmState
    Write-Host "Sincronizado vm_state.json -> zona '$Zone' (estado: $status)." -ForegroundColor Green
}

if ($ForceMigrate -and $status -ne "RUNNING") {
    $candidates = @()
    if ($TargetZone) { $candidates += $TargetZone }
    $candidates += ($FallbackZones | Where-Object { $_ -ne $Zone -and $_ -ne $TargetZone })
    $Zone = Invoke-ZeroTrustFailover -Gcloud $gcloud -State $vmState -SourceZone $Zone -CandidateZones $candidates
    $status = "RUNNING"
} elseif ($status -ne "RUNNING") {
    Write-Host "[2/4] Encendiendo VM '$Instance' en '$Zone' (estado actual: $status)..." -ForegroundColor Yellow
    $ErrorActionPreference = "Continue"
    $startOut = (& $gcloud compute instances start $Instance --zone=$Zone --project=$Project --quiet 2>&1 | Out-String)
    $startExit = $LASTEXITCODE
    $ErrorActionPreference = "Stop"

    if ($startExit -ne 0) {
        if ($startOut -match 'ZONE_RESOURCE_POOL_EXHAUSTED|STOCKOUT|does not have enough resources') {
            Write-Host "[2/4] STOCKOUT detectado en '$Zone'. Activando Auto-Failover Zero-Trust..." -ForegroundColor Yellow
            $candidates = @()
            if ($TargetZone) { $candidates += $TargetZone }
            if ($startOut -match 'zonesAvailable:\s*([a-z0-9,-]+)') {
                $availList = $Matches[1] -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" -and $_ -ne "''" }
                foreach ($az in $availList) {
                    if ($candidates -notcontains $az -and $az -ne $Zone) { $candidates += $az }
                }
            }
            foreach ($fz in $FallbackZones) {
                if ($candidates -notcontains $fz -and $fz -ne $Zone) { $candidates += $fz }
            }
            Write-Host "[FAILOVER] Zonas candidatas ($($candidates.Count)): $($candidates -join ', ')" -ForegroundColor Cyan
            $Zone = Invoke-ZeroTrustFailover -Gcloud $gcloud -State $vmState -SourceZone $Zone -CandidateZones $candidates
        } else {
            Write-Error "Error al iniciar la VM '$Instance' en '$Zone': $startOut"
            exit 1
        }
    }
} else {
    Write-Host "[2/4] La VM ya estaba RUNNING en '$Zone'." -ForegroundColor Green
}

$healthNow = Test-HealthEndpoint
if ($healthNow -eq "ok" -and -not $NoTunnel) {
    Write-Host "[3/4] Tunel IAP y qwen-server ya estan activos en http://127.0.0.1:$LocalPort ($Zone)" -ForegroundColor Green
    exit 0
}

Write-Host "[3/4] Esperando SSH por IAP ($Zone) y validando 'qwen-server' Zero-Trust + firewall..." -ForegroundColor Cyan
$remoteEnsureScript = @'
set -euo pipefail
sudo systemctl is-active --quiet zero-trust-firewall.service || sudo systemctl start zero-trust-firewall.service || true
API_KEY="$(cat "/home/$USER/.qwen_api_key" | tr -d '\r\n')"
MODEL_FILE="/modelos/Huihui-Qwen3.8-27B-Coder390-EfficientThink-abliterated.i1-Q4_K_M.gguf"
ARGS="$(sudo docker inspect qwen-server --format '{{join .Args " "}}' 2>/dev/null || true)"
HEALTH_TEST="$(sudo docker inspect qwen-server --format '{{join .Config.Healthcheck.Test " "}}' 2>/dev/null || true)"
SEC_STATE="$(sudo docker inspect qwen-server --format 'user={{.Config.User}} ro={{.HostConfig.ReadonlyRootfs}} cap={{.HostConfig.CapDrop}} sec={{.HostConfig.SecurityOpt}} net={{.HostConfig.NetworkMode}}' 2>/dev/null || true)"

if echo "$ARGS" | grep -q -- "$MODEL_FILE" && \
   (echo "$ARGS" | grep -q -- "-c 131072" || echo "$ARGS" | grep -q -- "-c 98304" || echo "$ARGS" | grep -q -- "-c 65536") && \
   echo "$ARGS" | grep -q -- "-np 1" && \
   echo "$ARGS" | grep -q -- "-fa on" && \
   echo "$ARGS" | grep -q -- "--cache-type-k q8_0" && \
   echo "$ARGS" | grep -q -- "--cache-type-v q8_0" && \
   echo "$ARGS" | grep -q -- "--top-k 20" && \
   echo "$ARGS" | grep -q -- "--min-p 0.0" && \
   echo "$ARGS" | grep -q -- "--presence-penalty 0.0" && \
   echo "$ARGS" | grep -q -- "--spec-type ngram-cache" && \
   echo "$ARGS" | grep -q -- "--spec-draft-n-max 3" && \
   echo "$ARGS" | grep -q -- "--reasoning-budget 512" && \
   echo "$ARGS" | grep -q -- "--cache-reuse 256" && \
   echo "$HEALTH_TEST" | grep -q -- "8000/health" && \
   echo "$SEC_STATE" | grep -q -- "user=65534:65534" && \
   echo "$SEC_STATE" | grep -q -- "ro=true" && \
   echo "$SEC_STATE" | grep -q -- "net=llm-noegress"; then
  sudo docker ps -q --filter name=^/qwen-server$ | grep -q . || sudo docker start qwen-server >/dev/null
  exit 0
fi

if ! sudo docker network inspect llm-noegress >/dev/null 2>&1; then
  sudo docker network create --driver bridge --subnet=172.28.0.0/24 -o com.docker.network.bridge.name=br-llm-noegress llm-noegress >/dev/null
fi

MMPROJ_FLAG=""
if sudo docker run --rm ghcr.io/ggml-org/llama.cpp:server-cuda --help 2>/dev/null | grep -q -- "--no-mmproj"; then
  MMPROJ_FLAG="--no-mmproj"
fi

run_container() {
  local ctx="$1"
  sudo docker stop qwen-server >/dev/null 2>&1 || true
  sudo docker rm qwen-server >/dev/null 2>&1 || true
  sudo docker run -d \
    --name qwen-server \
    --restart unless-stopped \
    --gpus all \
    --user 65534:65534 \
    --cap-drop=ALL \
    --security-opt=no-new-privileges:true \
    --read-only \
    --tmpfs /tmp:rw,noexec,nosuid,size=256m \
    --network llm-noegress \
    --health-cmd="curl -fsS http://127.0.0.1:8000/health || exit 1" \
    --health-interval=15s \
    --health-timeout=5s \
    --health-retries=5 \
    -v "/home/$USER/modelos:/modelos:ro" \
    -p 127.0.0.1:8000:8000 \
    ghcr.io/ggml-org/llama.cpp:server-cuda \
    -m "$MODEL_FILE" \
    --alias huihui-qwen3.8-27b-abliterated \
    --jinja \
    $MMPROJ_FLAG \
    --host 0.0.0.0 --port 8000 \
    -ngl 99 -c "$ctx" -np 1 -fa on \
    --cache-type-k q8_0 --cache-type-v q8_0 \
    --cache-reuse 256 \
    --top-k 20 --min-p 0.0 --repeat-penalty 1.0 --presence-penalty 0.0 \
    --reasoning-budget 512 \
    --reasoning-budget-message "Thinking budget reached. Provide final answer:" \
    --spec-type ngram-cache --spec-draft-n-max 3 \
    --api-key "$API_KEY" >/dev/null

  for j in $(seq 1 110); do
    if ! sudo docker ps --filter "name=^/qwen-server$" --format "{{.Status}}" | grep -q "Up"; then
      return 1
    fi
    if sudo docker logs qwen-server 2>&1 | grep -qiE "out of memory|cudaMalloc failed|failed to allocate"; then
      return 1
    fi
    if curl -fsS http://127.0.0.1:8000/health >/dev/null 2>&1; then
      return 0
    fi
    sleep 2
  done
  return 1
}

if ! run_container 131072; then
  if ! run_container 98304; then
    run_container 65536
  fi
fi
'@
$remoteB64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes(($remoteEnsureScript -replace "`r`n", "`n")))

$sshReady = $false
for ($i = 1; $i -le 24; $i++) {
    $ErrorActionPreference = "Continue"
    & $gcloud compute ssh $Instance --zone=$Zone --project=$Project --tunnel-through-iap --quiet --command="echo $remoteB64 | base64 -d | bash" 2>$null | Out-Null
    $sshExit = $LASTEXITCODE
    $ErrorActionPreference = "Stop"
    if ($sshExit -eq 0) {
        $sshReady = $true
        break
    }
    Start-Sleep -Seconds 5
}

if (-not $sshReady) {
    Write-Error "No se pudo conectar por SSH/IAP a '$Instance' ($Zone) tras 120s."
    exit 1
}

if ($NoTunnel) {
    Write-Host "[4/4] Modo -NoTunnel: VM RUNNING y qwen-server validado en '$Zone'." -ForegroundColor Green
    exit 0
}

Stop-ExistingTunnel

Write-Host "[4/4] Abriendo tunel SSH cifrado (IAP) hacia 127.0.0.1:$LocalPort en segundo plano ($Zone)..." -ForegroundColor Cyan
$proc = Start-Process -FilePath $gcloud `
    -ArgumentList @("compute", "ssh", $Instance, "--zone=$Zone", "--project=$Project", "--tunnel-through-iap", "--quiet", "--", "-N", "-L", "${LocalPort}:127.0.0.1:${LocalPort}") `
    -WindowStyle Hidden `
    -PassThru `
    -RedirectStandardOutput $OutLog `
    -RedirectStandardError $ErrLog

Set-Content -Path $PidFile -Value $proc.Id -Encoding Ascii

$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
$ready = $false
Write-Host "Esperando a que llama-server cargue Qwen3.8-27B en VRAM (~90-120s en arranque en frio)..." -ForegroundColor Gray

while ((Get-Date) -lt $deadline) {
    if ($proc.HasExited) {
        $errTxt = if (Test-Path $ErrLog) { Get-Content $ErrLog -Raw } else { "" }
        Write-Error "El tunel SSH salio inesperadamente (exit $($proc.ExitCode)). Log: $errTxt"
        exit 1
    }
    $state = Test-HealthEndpoint
    if ($state -eq "ok") {
        $ready = $true
        break
    }
    Start-Sleep -Seconds 3
}

if ($ready) {
    Write-Host "LISTO! Servidor OpenAI-compatible operativo en http://127.0.0.1:$LocalPort/v1 (Zona: $Zone | PID tunel: $($proc.Id))." -ForegroundColor Green
    Write-Host "Recorda ejecutar detener_llm.ps1 cuando termines de programar para llevar el gasto de computo a `$0.00/h." -ForegroundColor Yellow
} else {
    Write-Warning "El tunel SSH esta activo (PID $($proc.Id)), pero /health no respondio 'ok' en ${TimeoutSeconds}s. Revisa estado_llm.ps1."
    exit 1
}
