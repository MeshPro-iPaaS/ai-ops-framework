<#
    turn-on-the-machinery.ps1 - optional. Nothing in this vault needs it.

    The vault works with nothing installed: every day-to-day thing is a note. What this turns on is
    the machinery that keeps the generated surfaces true by themselves - the compiled agents, the
    register, the five-page site and the check.

    It needs Python. If this machine has none, it fetches Python's official embeddable package
    (about 10 MB, no installer, no admin rights, nothing added to PATH, nothing registered) into
    C:\AI\python and uses that. Delete that folder any time; nothing else depends on it.

    Run it with no arguments and it finds every vault under C:\AI. Point it at one with -Vault.

    ASCII only, on purpose: Windows PowerShell 5.1 reads a .ps1 with no byte-order mark as ANSI, so
    one em dash in a comment is enough to break the parse thirty lines later. This file also ships
    with a BOM. Keep both.
#>
[CmdletBinding()]
param(
    [string] $Vault,
    [string] $Root       = 'C:\AI',
    [string] $PythonHome = 'C:\AI\python',
    [string] $Url        = 'https://www.python.org/ftp/python/3.13.15/python-3.13.15-embed-amd64.zip'
)

$ErrorActionPreference = 'Stop'

function Find-Python {
    foreach ($c in @('py', 'python', 'python3')) {
        $cmd = Get-Command $c -ErrorAction SilentlyContinue
        if (-not $cmd) { continue }
        try {
            $v = & $c -c "import sys;print('%d.%d' % sys.version_info[:2])" 2>$null
            if ($v -and [version]$v -ge [version]'3.10') { return $cmd.Source }
        } catch { }
    }
    $local = Join-Path $PythonHome 'python.exe'
    if (Test-Path $local) { return $local }
    return $null
}

function Get-EmbeddedPython {
    Write-Host "No Python 3.10+ on this machine. Fetching Python's embeddable package (about 10 MB)."
    Write-Host "  from $Url"
    Write-Host "  into $PythonHome  - no installer, no admin rights, nothing added to PATH."
    try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 } catch { }
    $zip = Join-Path $env:TEMP 'meshpro-python-embed.zip'
    Invoke-WebRequest -Uri $Url -OutFile $zip -UseBasicParsing
    if (Test-Path $PythonHome) { Remove-Item $PythonHome -Recurse -Force }
    Expand-Archive -LiteralPath $zip -DestinationPath $PythonHome -Force
    Remove-Item $zip -Force -ErrorAction SilentlyContinue
    # The embeddable build ships with site imports switched off. The framework's scripts are pure
    # standard library, but turning it back on costs nothing and removes a class of puzzle.
    Get-ChildItem $PythonHome -Filter '*._pth' | ForEach-Object {
        (Get-Content $_.FullName) -replace '^#\s*import site', 'import site' |
            Set-Content $_.FullName -Encoding ASCII
    }
    $exe = Join-Path $PythonHome 'python.exe'
    if (-not (Test-Path $exe)) { throw "the download unpacked but there is no python.exe in $PythonHome" }
    return $exe
}

function Get-Vaults {
    if ($Vault) { return @($Vault) }
    if (-not (Test-Path $Root)) { return @() }
    Get-ChildItem $Root -Directory -ErrorAction SilentlyContinue |
        Where-Object { Test-Path (Join-Path $_.FullName '.ops\scripts\rebuild.py') } |
        ForEach-Object { $_.FullName }
}

$vaults = @(Get-Vaults)
if ($vaults.Count -eq 0) {
    Write-Host "No vault found under $Root. A vault is a folder with .ops\scripts\rebuild.py in it."
    Write-Host 'Point me at yours:  -Vault "C:\AI\Your Folder"'
    exit 1
}

$python = Find-Python
if (-not $python) { $python = Get-EmbeddedPython }
Write-Host ''
Write-Host "Using $python"

$failed = 0
foreach ($v in $vaults) {
    Write-Host ''
    Write-Host "--- $v"
    & $python (Join-Path $v '.ops\scripts\rebuild.py') $v
    if ($LASTEXITCODE -ne 0) { $failed++ }
}

Write-Host ''
if ($failed -eq 0) {
    Write-Host 'Done. The check has run, and your dashboard now says so rather than saying it never has.'
    Write-Host 'Open: 05 - Operations\picture\ai_operations.html'
} else {
    Write-Host "$failed vault(s) reported something untrue. Fix the note each failure names, then run again."
}
exit $failed
