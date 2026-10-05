@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_CMD="
where py >nul 2>nul && set "PYTHON_CMD=py"
if not defined PYTHON_CMD where python >nul 2>nul && set "PYTHON_CMD=python"

if not defined PYTHON_CMD (
  echo Python was not found on this computer.
  echo Install Python to run this website with Excel data.
  pause
  exit /b 1
)

echo Starting AURA Connector Documentation Hub...
echo Local address: http://localhost:8080
echo Save the Excel workbook, then refresh the browser to load the latest data.
echo Press Ctrl+C in this window to stop the server.

start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 1; Start-Process 'http://localhost:8080'"
%PYTHON_CMD% server.py

endlocal
