<#
  Track B helper (Windows side, NOT WSL2).

  Adds the lab hostnames to the Windows hosts file so your Windows browser can
  reach the self-hosted GitLab UI and registry by name.

  Run in an ELEVATED PowerShell:
      Start menu -> "PowerShell" -> Run as administrator
      cd <repo>\simulation\scripts
      .\win-hosts-setup.ps1

  NOTE: this only fixes name resolution on the Windows side. Inside WSL2 also run:
      echo "127.0.0.1 gitlab.local registry.local" | sudo tee -a /etc/hosts
#>
$ErrorActionPreference = 'Stop'

$hostsFile = Join-Path $env:SystemRoot 'System32\drivers\etc\hosts'
$entries   = @('127.0.0.1 gitlab.local', '127.0.0.1 registry.local')

$existing = @(Get-Content -Path $hostsFile -ErrorAction SilentlyContinue)
foreach ($entry in $entries) {
    if ($existing -contains $entry) {
        Write-Host "exists: $entry"
    } else {
        Add-Content -Path $hostsFile -Value $entry
        Write-Host "added : $entry"
    }
}

Write-Host ''
Write-Host 'Windows hosts file updated.'
Write-Host 'Reminder: inside WSL2 run ->  echo "127.0.0.1 gitlab.local registry.local" | sudo tee -a /etc/hosts'
