@echo off
echo Stopping Instadeed server...
for /f "tokens=2" %%G in ('tasklist /fi "imagename eq python.exe" /fo list ^| find "PID:"') do (
    echo Killing Python process PID: %%G
    taskkill /PID %%G /F 2>nul
)
echo Server stopped (if running).
