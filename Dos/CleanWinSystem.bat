@echo off    
echo ---------------------------------------
echo start to clean system...
echo ---------------------------------------
del /f /s /q %systemdrive%\*.tmp    
del /f /s /q %systemdrive%\*._mp    
del /f /s /q %systemdrive%\*.log    
del /f /s /q %systemdrive%\*.gid    
del /f /s /q %systemdrive%\*.chk    
del /f /s /q %systemdrive%\*.old
echo -------------Recycle Bin Start--------------------------    
::WinXP
::del /f /s /q %systemdrive%\recycled\*.* 
::Win7/8
for %%a in (C D) do (
    if exist %%a:\ (
    del /f /s /q "%%a:\$recycle.bin\*.*" >nul 2>nul
    )
)  
echo -------------Recycle Bin End---------------------------     
del /f /s /q %windir%\*.bak    
del /f /s /q %windir%\prefetch\*.*    
rd /s /q %windir%\temp & md %windir%\temp    
echo ---------------------------------------
del /f /q %userprofile%\COOKIES s\*.*    
del /f /q %userprofile%\recent\*.*    
echo ---------------------------------------
del /f /s /q "%userprofile%\Local Settings\Temporary Internet Files\*.*"    
del /f /s /q "%userprofile%\Local Settings\Temp\*.*"    
del /f /s /q "%userprofile%\recent\*.*"   
echo --------------------------------------- 
sfc /purgecache   
defrag %systemdrive% -b 
echo ---------------------------------------
echo Finish to clearn Recycle Bin
echo ---------------------------------------
echo clean system finished. 
echo ---------------------------------------
timeout 5    

