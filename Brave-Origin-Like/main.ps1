# main.ps1
# Makes the normal Windows Brave Browser behave as close as practical to Brave Origin.
# Requires Administrator privileges because Brave managed policies are written to HKLM.
#
# Usage:
#   .\main.ps1 -Install
#   .\main.ps1 -Undo
#   .\main.ps1 -Status
#
# The script backs up existing values under the Brave policy key before changing them.
# It does NOT disable Brave Shields, Chromium Safe Browsing, password manager, sync,
# extensions, JavaScript, cookies, or normal Chromium security features.

[CmdletBinding()]
param(
    [ValidateSet("Install","Undo","Status")]
    [string]$Action = "Install"
)

$ErrorActionPreference = "Stop"

$PolicyPath = "HKLM:\SOFTWARE\Policies\BraveSoftware\Brave"
$BackupDir = Join-Path $env:ProgramData "Brave-Origin-Like"
$BackupFile = Join-Path $BackupDir "policy-backup.json"

$Policies = [ordered]@{
    BraveRewardsDisabled       = 1
    BraveWalletDisabled        = 1
    BraveVPNDisabled           = 1
    BraveAIChatEnabled         = 0
    BraveNewsDisabled          = 1
    BraveTalkDisabled          = 1
    TorDisabled                = 1
    BraveP3AEnabled            = 0
    BraveStatsPingEnabled      = 0
    BraveWebDiscoveryEnabled   = 0
    BraveSpeedreaderEnabled    = 0
    BraveWaybackMachineEnabled = 0
    BravePlaylistEnabled       = 0
    EmailAliasesEnabled        = 0
}

function Test-Administrator {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Ensure-Admin {
    if (-not (Test-Administrator)) {
        Write-Host "Administrator privileges are required. Re-launching elevated..." -ForegroundColor Yellow

        $argList = @(
            "-NoProfile"
            "-ExecutionPolicy", "Bypass"
            "-File", "`"$PSCommandPath`""
            "-Action", $Action
        )

        Start-Process -FilePath "powershell.exe" -Verb RunAs -ArgumentList $argList
        exit
    }
}

function Get-ExistingPolicyValues {
    $result = [ordered]@{}

    if (-not (Test-Path $PolicyPath)) {
        return $result
    }

    foreach ($name in $Policies.Keys) {
        try {
            $item = Get-ItemProperty -Path $PolicyPath -Name $name -ErrorAction Stop
            $property = $item.PSObject.Properties[$name]

            if ($null -ne $property) {
                $regKey = [Microsoft.Win32.Registry]::LocalMachine.OpenSubKey(
                    "SOFTWARE\Policies\BraveSoftware\Brave",
                    $false
                )

                if ($null -ne $regKey) {
                    try {
                        $value = $regKey.GetValue(
                            $name,
                            $null,
                            [Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames
                        )
                        $kind = $regKey.GetValueKind($name).ToString()
                        $result[$name] = @{
                            Present = $true
                            Value   = $value
                            Kind    = $kind
                        }
                    }
                    finally {
                        $regKey.Dispose()
                    }
                }
            }
        }
        catch {

        }
    }

    return $result
}

function Save-Backup {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null

    $backup = [ordered]@{
        CreatedUtc = [DateTime]::UtcNow.ToString("o")
        PolicyPath = "HKLM\SOFTWARE\Policies\BraveSoftware\Brave"
        Values     = Get-ExistingPolicyValues
    }

    $backup | ConvertTo-Json -Depth 8 | Set-Content -Path $BackupFile -Encoding UTF8
}

function Install-Policies {
    Ensure-Admin

    $braveProcesses = Get-Process -Name "brave" -ErrorAction SilentlyContinue
    if ($braveProcesses) {
        Write-Host ""
        Write-Host "Brave is currently running." -ForegroundColor Yellow
        Write-Host "Please close all Brave windows before applying the policies."
        Write-Host ""
        $answer = Read-Host "Continue anyway? [y/N]"
        if ($answer -notmatch '^(y|yes)$') {
            Write-Host "Cancelled."
            return
        }
    }

    if (-not (Test-Path $BackupFile)) {
        Save-Backup
        Write-Host "Backup saved to: $BackupFile" -ForegroundColor DarkGray
    }
    else {
        Write-Host "Existing backup retained: $BackupFile" -ForegroundColor DarkGray
    }

    New-Item -Path $PolicyPath -Force | Out-Null

    foreach ($entry in $Policies.GetEnumerator()) {
        New-ItemProperty `
            -Path $PolicyPath `
            -Name $entry.Key `
            -PropertyType DWord `
            -Value ([int]$entry.Value) `
            -Force | Out-Null

        Write-Host ("  {0} = {1}" -f $entry.Key, $entry.Value)
    }

    Write-Host ""
    Write-Host "Brave Origin-like policies applied." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Completely close Brave."
    Write-Host "  2. Start Brave again."
    Write-Host "  3. Open brave://policy and click 'Reload policies'."
    Write-Host "  4. Confirm the listed policies are Enabled."
    Write-Host ""
    Write-Host "Note: because these are managed Windows policies, Brave may show"
    Write-Host "'Managed by your organization'. This is expected."
    Write-Host ""
    Write-Host "Undo with: Brave-Origin-Like.cmd /undo"
}

function Restore-OriginalValue($regKey, $name, $data) {
    $kind = $data.Kind
    $value = $data.Value

    switch ($kind) {
        "DWord" {
            $regKey.SetValue($name, [int]$value, [Microsoft.Win32.RegistryValueKind]::DWord)
        }
        "QWord" {
            $regKey.SetValue($name, [long]$value, [Microsoft.Win32.RegistryValueKind]::QWord)
        }
        "String" {
            $regKey.SetValue($name, [string]$value, [Microsoft.Win32.RegistryValueKind]::String)
        }
        "ExpandString" {
            $regKey.SetValue($name, [string]$value, [Microsoft.Win32.RegistryValueKind]::ExpandString)
        }
        "MultiString" {
            $regKey.SetValue($name, [string[]]$value, [Microsoft.Win32.RegistryValueKind]::MultiString)
        }
        "Binary" {
            $regKey.SetValue($name, [byte[]]$value, [Microsoft.Win32.RegistryValueKind]::Binary)
        }
        default {
            throw "Unsupported registry value kind '$kind' for '$name'."
        }
    }
}

function Undo-Policies {
    Ensure-Admin

    if (-not (Test-Path $BackupFile)) {
        Write-Host "No backup was found at:" -ForegroundColor Yellow
        Write-Host "  $BackupFile"
        Write-Host ""
        Write-Host "Nothing was changed."
        return
    }

    $backup = Get-Content -Path $BackupFile -Raw | ConvertFrom-Json

    $regKey = [Microsoft.Win32.Registry]::LocalMachine.CreateSubKey(
        "SOFTWARE\Policies\BraveSoftware\Brave"
    )

    try {
        foreach ($name in $Policies.Keys) {
            $old = $backup.Values.PSObject.Properties[$name]

            if ($null -ne $old -and $old.Value.Present -eq $true) {
                Restore-OriginalValue $regKey $name $old.Value
                Write-Host "Restored: $name"
            }
            else {
                $regKey.DeleteValue($name, $false)
                Write-Host "Removed:  $name"
            }
        }
    }
    finally {
        $regKey.Dispose()
    }

    try {
        $remaining = Get-ItemProperty -Path $PolicyPath -ErrorAction Stop |
            Select-Object -Property * -ExcludeProperty PSPath,PSParentPath,PSChildName,PSDrive,PSProvider

        if ($remaining.PSObject.Properties.Count -eq 0) {
            Remove-Item -Path $PolicyPath -Force -ErrorAction SilentlyContinue
        }
    }
    catch {

    }

    Write-Host ""
    Write-Host "Original policy values restored." -ForegroundColor Green
    Write-Host "Restart Brave completely for the changes to take effect."
    Write-Host ""
    Write-Host "Backup retained at: $BackupFile" -ForegroundColor DarkGray
}

function Show-Status {
    Write-Host ""
    Write-Host "=== Brave Origin-like policy status ===" -ForegroundColor Cyan
    Write-Host "Policy path: $PolicyPath"
    Write-Host ""

    if (-not (Test-Path $PolicyPath)) {
        Write-Host "No Brave managed policy key exists." -ForegroundColor Yellow
        return
    }

    foreach ($entry in $Policies.GetEnumerator()) {
        try {
            $value = (Get-ItemProperty -Path $PolicyPath -Name $entry.Key -ErrorAction Stop).$($entry.Key)
            $state = if ([int]$value -eq [int]$entry.Value) { "OK" } else { "DIFFERENT" }
            $color = if ($state -eq "OK") { "Green" } else { "Yellow" }
            Write-Host ("[{0}] {1} = {2}" -f $state, $entry.Key, $value) -ForegroundColor $color
        }
        catch {
            Write-Host ("[--] {0} = not set" -f $entry.Key) -ForegroundColor DarkGray
        }
    }

    Write-Host ""
    if (Test-Path $BackupFile) {
        Write-Host "Backup: $BackupFile" -ForegroundColor DarkGray
    }
}

switch ($Action) {
    "Install" { Install-Policies }
    "Undo"    { Undo-Policies }
    "Status"  { Show-Status }
}
