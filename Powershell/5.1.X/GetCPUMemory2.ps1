$CurrentDir = Split-Path $MyInvocation.MyCommand.Path
$file="$CurrentDir/Monitor.csv";

$counter = New-Object Diagnostics.PerformanceCounter

$counter.CategoryName = "Processor"

$counter.CounterName = "% Processor Time"

$counter.InstanceName = "_Total"
Add-Content $file '"Time","CPU","Memory"' #>> $file 

$MyFile = Get-Content $file 
# $MyFile = Get-Content $file
$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False
[System.IO.File]::WriteAllLines($file, $MyFile, $Utf8NoBomEncoding)

while ($true)
{
$TotalM= (Get-WmiObject -Class Win32_PhysicalMemory |measure capacity -sum).Sum / 1024 / 1024   #(gwmi win32_computersystem).TotalPhysicalMemory
$AvalibalM =(get-wmiobject -class Win32_PerfFormattedData_PerfOS_Memory   -namespace "root\cimv2").AvailableMBytes
$CPURate = "{00:F2}" -f $counter.NextValue()

$MRate =  "{00:F2}" -f (($TotalM - $AvalibalM) / $TotalM*100)
$time  = Get-Date -format "MM/dd/yyyy HH:mm:ss"
echo "Time=$time,CPU=$CPURate,Memory=$MRate"
$output = '"{0}","{1}","{2}"' -f $time, $CPURate, $MRate  #>> $file
#[System.IO.File]::WriteAllLines($file, $aa, $Utf8NoBomEncoding)
# [System.IO.File]::AppendAllLines($file, $s1)
Add-Content $file $output #>> $file 
sleep 3
}
