Param(
  [Parameter(Mandatory)][string]$ScriptPath,
  [string[]]$Args
)

$ErrorActionPreference='Stop'
if (-not (Test-Path $ScriptPath)) { throw "Script not found: $ScriptPath" }
& pwsh -NoLogo -NoProfile -File $ScriptPath @Args
exit $LASTEXITCODE





