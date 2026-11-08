# Install the toolkit skills and subagents for each agent on this Windows machine. Safe to run again.
# The Windows version of install.sh. Works in Windows PowerShell 5.1 and PowerShell 7.
#
#   irm https://raw.githubusercontent.com/spinsirr/toolkit/main/install.ps1 | iex
#   & ([scriptblock]::Create((irm https://raw.githubusercontent.com/spinsirr/toolkit/main/install.ps1))) -Personal
#
# -Personal also installs my global instructions (AGENTS.md) and my settings (personal/).
# It does not set up the Lore MCP server: personal/mcp.json needs sh, and Windows runs Lore through its own launcher.
# The Codex AGENTS.md is a symbolic link, so -Personal needs Developer Mode (Settings > System > For developers).
#
# Each agent then updates the plugin by itself. Run this again only after a change to settings/ or personal/.
# TOOLKIT_REPO and TOOLKIT_REF install another repo or branch, for tests. CODEX sets the path of codex.exe.
param([switch]$Personal)
$ErrorActionPreference = 'Stop'

$Repo = if ($env:TOOLKIT_REPO) { $env:TOOLKIT_REPO } else { 'spinsirr/toolkit' }
$Ref = $env:TOOLKIT_REF

# Windows PowerShell 5.1 turns each stderr line of a native command into an error, and 'Stop' then ends the
# script. So the helpers use 'Continue' and judge a native command only by its exit code.
function Invoke-Native([string]$Exe, [string[]]$Arguments) {
  $ErrorActionPreference = 'Continue'
  & $Exe @Arguments 2>&1 | ForEach-Object { "$_" }
  if ($LASTEXITCODE -ne 0) { throw "Failed (exit $LASTEXITCODE): $Exe $($Arguments -join ' ')" }
}

function Test-Native([string]$Exe, [string[]]$Arguments) {
  $ErrorActionPreference = 'Continue'
  & $Exe @Arguments 2>&1 | Out-Null
  return $LASTEXITCODE -eq 0
}

function Find-Command([string[]]$Names) {
  foreach ($name in $Names) {
    # Application: claude.cmd or codex.exe, not an npm .ps1 shim that the execution policy can block.
    $command = Get-Command $name -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($command) { return $command.Source }
  }
  return $null
}

$Claude = Find-Command @('claude')
$Codex = if ($env:CODEX) { $env:CODEX } else { Find-Command @('codex') }
if (-not $Claude -and -not $Codex) { throw 'Found neither Claude Code (claude) nor Codex (codex). Set CODEX to the path of codex.exe.' }

# apply.py needs Python 3.9 or newer. The Microsoft Store stub named python.exe fails this test.
$Python = $null
$candidates = @('python', 'python3', (Join-Path $HOME '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'))
foreach ($candidate in $candidates) {
  $path = Find-Command @($candidate)
  if ($path -and (Test-Native $path @('-c', 'import sys; assert sys.version_info >= (3, 9)'))) { $Python = $path; break }
}
if (-not $Python -and ($Claude -or $Personal)) { throw 'install.ps1 needs Python 3.9 or newer on PATH.' }

# Update first: an add of a marketplace that exists can succeed without a fetch, and leave an old copy.
# An update fails when nothing is installed yet, and then the add runs.
if ($Claude) {
  if (-not (Test-Native $Claude @('plugin', 'marketplace', 'update', 'toolkit'))) {
    $source = if ($Ref) { "$Repo#$Ref" } else { $Repo }
    Invoke-Native $Claude @('plugin', 'marketplace', 'add', $source)
  }
  if (-not (Test-Native $Claude @('plugin', 'update', 'personal@toolkit'))) {
    Invoke-Native $Claude @('plugin', 'install', 'personal@toolkit')
  }
  $copy = Join-Path $HOME '.claude\plugins\marketplaces\toolkit'
  if ($Personal) {
    Invoke-Native $Python @((Join-Path $copy 'scripts\apply.py'), 'claude', '--personal')
    # The instructions come from the marketplace copy, so they update with the plugin. No BOM: Claude Code reads the first line.
    $import = '@' + ((Join-Path $copy 'AGENTS.md') -replace '\\', '/')
    [IO.File]::WriteAllText((Join-Path $HOME '.claude\CLAUDE.md'), "$import`n")
  } else {
    Invoke-Native $Python @((Join-Path $copy 'scripts\apply.py'), 'claude')
  }
  Write-Output 'Claude Code: done.'
}

if ($Codex) {
  if (-not (Test-Native $Codex @('plugin', 'marketplace', 'upgrade', 'toolkit'))) {
    $add = @('plugin', 'marketplace', 'add', $Repo)
    if ($Ref) { $add += @('--ref', $Ref) }
    Invoke-Native $Codex $add
  }
  Invoke-Native $Codex @('plugin', 'add', 'personal@toolkit')
  if ($Personal) {
    $codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
    $copy = Join-Path $codexHome '.tmp\marketplaces\toolkit'
    $link = Join-Path $codexHome 'AGENTS.md'
    if (Test-Path -LiteralPath $link) { Remove-Item -LiteralPath $link -Force }
    try {
      New-Item -ItemType SymbolicLink -Path $link -Target (Join-Path $copy 'AGENTS.md') | Out-Null
    } catch {
      throw "Could not link $link. Turn on Developer Mode (Settings > System > For developers), then run this again. $_"
    }
    if (-not (Test-Path -LiteralPath $link)) { throw "$link does not resolve." }
    $env:CODEX = $Codex
    Invoke-Native $Python @((Join-Path $copy 'scripts\apply.py'), 'codex', '--personal')
  }
  Write-Output 'Codex: done.'
}

Write-Output 'Done. Start a new Claude Code or Codex session.'
