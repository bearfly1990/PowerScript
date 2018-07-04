@echo off
net use h: /delete /y
:: net use l: /delete /y
:: net use m: /delete /y

net use h: "\\xxx"
:: net use l: "\\xxx\PAMINV800"
:: net use l: "\\xxx\PFIINV800"
:: net use m: "\\xxx"
IF EXIST "\\xxx\Python36" SET PATH=%PATH%;"xxx\Python36"
pushd %~dp0
python Import.py
pause
