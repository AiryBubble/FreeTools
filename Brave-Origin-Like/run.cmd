@echo off
setlocal

if /I "%~1"=="/undo" (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0main.ps1" -Action Undo
) else if /I "%~1"=="/status" (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0main.ps1" -Action Status
) else (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0main.ps1" -Action Install
)

echo.
pause
