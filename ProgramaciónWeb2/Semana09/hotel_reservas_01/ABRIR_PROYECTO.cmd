@echo off
if not exist "%~dp0public\index.php" (
    echo No se encontro el proyecto junto a este archivo.
    pause
    exit /b 1
)
start "" "http://localhost/hotel_reservas_01/public/"
