@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" goto dependencies

set "PYTHON_CMD="
where.exe py >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD (
    where.exe python >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo Python 3 est requis. Installez-le depuis python.org puis relancez ce fichier.
    pause
    exit /b 1
)

echo Creation de l'environnement Aivora Company...
%PYTHON_CMD% -m venv .venv
if errorlevel 1 goto failed

:dependencies
".venv\Scripts\python.exe" -c "import pygame, tkinterdnd2, PIL, mutagen, imageio_ffmpeg" >nul 2>nul
if errorlevel 1 (
    echo Installation des dependances partagees...
    ".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
    if errorlevel 1 goto failed
)

echo Demarrage d'Aivora V1.1.0 et Aivora Studio V1.0...
start "Aivora" ".venv\Scripts\python.exe" "aivora\app.py"
start "Aivora Studio" /d "aivora studio" "..\.venv\Scripts\python.exe" -m aivora_studio
exit /b 0

:failed
echo.
echo L'installation a echoue. Verifiez Python et votre connexion Internet.
pause
exit /b 1
