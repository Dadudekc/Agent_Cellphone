Param(
  [string]$WebhookUrl = $env:DISCORD_WEBHOOK_URL,
  [string]$Content,
  [string]$Username = 'Overnight Runner',
  [string]$Title,
  [string]$Description,
  [int]$Color = 5814783,
  [switch]$Embed
)

$ErrorActionPreference = 'Stop'
if (-not $WebhookUrl) { throw 'Discord Webhook URL not provided. Set DISCORD_WEBHOOK_URL or pass -WebhookUrl.' }

$payload = @{
  username = $Username
}

if ($Embed) {
  $embed = @{ title = $Title; description = $Description; color = $Color }
  $payload.embeds = @($embed)
} else {
  if (-not $Content) { throw 'Provide -Content or use -Embed with -Title/-Description.' }
  $payload.content = $Content
}

$json = $payload | ConvertTo-Json -Depth 6
Invoke-RestMethod -Method Post -Uri $WebhookUrl -ContentType 'application/json' -Body $json | Out-Null
Write-Host 'Discord notification sent.'
exit 0





