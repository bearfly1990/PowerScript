@echo off
cls
setlocal EnableDelayedExpansion
set "cmd=findstr /R /N "^^" Trade_15Ports.csv | find /C ":""

for /f %%a in ('!cmd!') do set number=%%a
echo %number%
