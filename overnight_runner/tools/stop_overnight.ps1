Param()

try {
  $procs = Get-CimInstance Win32_Process |
    Where-Object {
      $_.Name -match 'python' -and (
        $_.CommandLine -like '*overnight_runner*runner.py*' -or
        $_.CommandLine -like '*overnight_runner*listener.py*'
      )
    }

  if (-not $procs) {
    Write-Host 'No overnight runner/listener processes found.'
    exit 0
  }

  $ids = @($procs | ForEach-Object { $_.ProcessId })
  foreach ($procId in $ids) {
    try { Stop-Process -Id $procId -Force -ErrorAction Stop } catch {}
  }
  Write-Host ('Stopped PIDs: ' + ($ids -join ', '))
  exit 0
}
catch {
  Write-Error $_
  exit 1
}


