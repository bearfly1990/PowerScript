# Get Command
$CurrentDir = Split-Path $MyInvocation.MyCommand.Path
Write-Host $CurrentDir
#write-output $CurrentDir | out-file -filepath C:\temp\a.txt