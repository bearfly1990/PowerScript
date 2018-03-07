@echo off

timeout 5

schtasks.exe /Run /S ServerName /TN "Restore Task"

timeout 120

echo Stop the services in ServerName

sc \\ServerName stop "Service Name [TESTAUTO]" 

timeout 60

echo start the services in pfs-pamrepqa01 

sc \\ServerName start "Service Name [TESTAUTO]" 

timeout 60
