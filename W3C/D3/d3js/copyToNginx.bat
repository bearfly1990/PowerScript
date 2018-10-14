@echo off
:start
xcopy * D:\ProgramDev\nginx-1.15.5\html\d3js /SY
timeout 5
goto start
