@echo off
net use h: /delete /y
net use h: "\\xxx"

IF EXIST "\\xxx\Python36" SET PATH=%PATH%;"xxx\Python36"
pushd %~dp0
python Import.py
pause
