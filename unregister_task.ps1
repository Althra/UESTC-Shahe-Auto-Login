$taskName = "UESTCNetAutoLogin"

$currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
$adminCheck = New-Object Security.Principal.WindowsPrincipal($currentIdentity)
if (-not $adminCheck.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "Please run this script as Administrator."
    exit 1
}

$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($task) {
    Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Task '$taskName' has been stopped and deleted." -ForegroundColor Green
} else {
    Write-Host "Task '$taskName' does not exist. No deletion is necessary." -ForegroundColor Yellow
}
