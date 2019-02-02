$CurrentDir = Split-Path $MyInvocation.MyCommand.Path
$file = "$CurrentDir/Monitor.csv"
$ps_name = "java"
$show_sys_cpu_rate = $false
$show_sys_mem_rate = $false

$memory_sys_total = (Get-WmiObject -Class Win32_PhysicalMemory |measure capacity -sum).Sum  #(gwmi win32_computersystem).TotalPhysicalMemory
$cpu_cores = (Get-WmiObject Win32_ComputerSystem).NumberOfLogicalProcessors
# $memory_sys_total = (Get-Counter "\Memory\System Driver Total Bytes").CounterSamples | Sort-Object Path
# $memory_sys_total = $memory_sys_total[0].CookedValue
"time,CPU(%),Memory(%),CPU_$ps_name(%), Memory_$ps_name(%)" >> $file
while ($True) {
    $cpu_rate_pss = (Get-Counter "\process($ps_name*)\% Processor Time").CounterSamples | Sort-Object Path
    $cpu_rate_sys = (Get-Counter "\processor(_total)\% processor time").CounterSamples | Sort-Object Path
    $cpu_rate_sys = $cpu_rate_sys[0].CookedValue
    if($show_sys_cpu_rate -eq $false){
        $cpu_rate_sys = 0
    }
    
    $memory_pss   = (Get-Counter "\Process($ps_name*)\Working Set - Private").CounterSamples | Sort-Object Path

    if($show_sys_mem_rate){
        $memory_sys_available   = (Get-Counter "\Memory\Available Bytes").CounterSamples | Sort-Object Path
        $memory_sys_available   = $memory_sys_available[0].CookedValue
        $memory_sys = $memory_sys_total - $memory_sys_available
    }else{
        $memory_sys = 0
    }

    $cpu_rate_pss_total = 0
    $memory_pss_total = 0
    $cpu_rate_pss.Count
    try {
        For ($i = 0; $i -lt $cpu_rate_pss.Count; $i++) {
            $cpu_rate_pss_total  = $cpu_rate_pss_total + $cpu_rate_pss[$i].CookedValue
            $memory_pss_total    = $memory_pss_total + $memory_pss[$i].CookedValue 
        }
    }catch{
        
    }

    $cpu_rate_sys           = "{0:F2}" -f $cpu_rate_sys
    $cpu_rate_pss_total     = "{0:F2}" -f $cpu_rate_pss_total / $cpu_cores
    
    $memory_rate_sys        = "{0:F2}" -f ( $memory_sys / $memory_sys_total * 100)
    $memory_rate_pss_total  = "{0:F2}" -f ( $memory_pss_total / $memory_sys_total * 100)

    $time = Get-Date -format "MM/dd/yyyy HH:mm:ss"
    
    Write-Output "Time=$time;CPU=$cpu_rate_sys;Memory=$memory_rate_sys;CPU($ps_name)=$cpu_rate_pss_total;Memory($ps_name)=$memory_rate_pss_total"
    "$time,$cpu_rate_sys,$memory_rate_sys,$cpu_rate_pss_total,$memory_rate_pss_total" >> $file
}
