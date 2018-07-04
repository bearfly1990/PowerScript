@ECHO OFF
vol h: >nul 2>nul
if errorlevel 1 (
    net use h: \\ServerName\c$ "password" /user:"domain\user"
) else (
    :: if not errorlevel 0 echo fail to connnect to remote machine
    :: /s in clude sub directory  /d only copy the updated files(date newer)
    xcopy /s /c /d /y /EXCLUDE:c:\Users\eid\Desktop\uncopy.txt "c:\Users\eid\Desktop\Company" h:\Users\user\Desktop\LocalBK\Company
)
REM net use h: /del 
REM if not errorlevel 0 echo fail to delete machine
