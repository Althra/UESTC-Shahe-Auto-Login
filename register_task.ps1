$taskName = "UESTCNetAutoLogin"
$scriptFileName = "always_online.py"

# 检测管理员身份
$currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
$adminCheck = New-Object Security.Principal.WindowsPrincipal($currentIdentity)
if (-not $adminCheck.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "Please run this script as Administrator."
    exit 1
}

# 获取 python 路径
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonPath -or -not (Test-Path $pythonPath)) {
    Write-Error "Python executable not found. Please ensure Python is installed and added to the PATH."
    exit 1
}

# 获取脚本路径
$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Path
$loginScript = Join-Path -Path $scriptDir -ChildPath $scriptFileName
if (-not (Test-Path $loginScript)) {
    Write-Error "Script file '$scriptFileName' not found in the current directory."
    exit 1
}

# 创建计划任务
$trigger = New-ScheduledTaskTrigger -AtStartup
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$loginScript`""
$taskPrincipal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType S4U -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $taskPrincipal -Settings $settings -Force
Start-ScheduledTask -TaskName $taskName
Write-Host "Task '$taskName' has been created and is running." -ForegroundColor Green
