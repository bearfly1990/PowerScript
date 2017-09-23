@echo off
::First check the default format in your system(win)
echo %date%
echo %time%
::Split the default date / time string to generate your own date format
for /f "tokens=1-3 delims=/ " %%1 in ("%date%") do set formatedTime=%%1%%2%%3
for /f "tokens=1-3 delims=.: " %%1 in ("%time%") do set formatedTime=%formatedTime%-%%1%%2%%3
echo %formatedTime%