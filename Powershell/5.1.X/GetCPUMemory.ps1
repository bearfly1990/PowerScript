$totalMemory = (Get-WmiObject -Class Win32_PhysicalMemory | measure capacity -sum).Sum
$totalMemory = $totalMemory/1024/1024
$CPU_Counter = New-Object Diagnostics.PerformanceCounter
$CPU_Counter.CategoryName = "Processor"
$CPU_Counter.CounterName = "% Processor Time" 
$CPU_Counter.InstanceName = "_Total"

$MEM_Counter = New-Object Diagnostics.PerformanceCounter
$MEM_Counter.CategoryName = "Memory"
$MEM_Counter.CounterName = "Available MBytes" 

While ($true)
{
    $CPURate = $CPU_Counter.NextValue().ToString("0.00")
    $MemAvailable = $MEM_Counter.NextValue()
    $MemUsed = $totalMemory - $MemAvailable
    $MemUsedRate =  ($MemUsed / $totalMemory * 100).ToString("0.00")
    
    $Time = Get-Date -format "yyyy-MM-ddTHH:mm:ss"
    "Time=$Time;CPURate=$CPURate;MemRate=$MemUsedRate"
    "Time=$Time;CPURate=$CPURate;MemRate=$MemUsedRate" >> Monitor.txt
    
    Start-Sleep -Seconds 2
}


