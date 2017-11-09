@echo off
set "from1=C:\ProgramData\Microsoft\Windows\Start Menu\Programs\${App}\*.link"
set "to=%userprofile%\DeskTop"
xcopy /c /d /y "%from1%" "%to%"