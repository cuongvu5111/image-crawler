@echo off
echo ========================================
echo    Django Image Crawler Server
echo ========================================

REM Chuyen ve thu muc chua file bat
cd /d "%~dp0"

echo.
echo Thu muc hien tai: %CD%
echo.

echo Kiem tra Python...
py --version
if %errorlevel% neq 0 (
    echo.
    echo Loi: Python khong duoc tim thay!
    echo Huong dan khac phuc:
    echo    1. Cai dat Python tu https://python.org
    echo    2. Hoac cai tu Microsoft Store
    echo    3. Dam bao Python duoc them vao PATH
    echo.
    pause
    exit /b 1
)

echo.
echo Python da san sang!
echo.

echo Khoi dong Django server...
echo.
echo ========================================
echo   Server URLs:
echo   Local:    http://127.0.0.1:8000
echo   Network:  http://0.0.0.0:8000
echo
echo   Nhan Ctrl+C de dung server
echo ========================================
echo.

py manage.py runserver 0.0.0.0:8000

echo.
echo Server da dung.
echo.
pause
