@echo off
cd /d "%~dp0"
where code >nul 2>&1
if errorlevel 1 (
    echo El comando code no esta disponible. Abre esta carpeta desde VS Code.
    pause
    exit /b 1
)
call code .
