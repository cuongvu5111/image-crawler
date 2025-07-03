@echo off
echo ========================================
echo    Django Image Crawler Deployment
echo ========================================

REM Chuyen ve thu muc chua file bat
cd /d "%~dp0"

echo.
echo Thu muc hien tai: %CD%
echo.

echo [1/5] Kiem tra Python...
py --version
if %errorlevel% neq 0 (
    echo.
    echo Loi: Python khong duoc tim thay!
    echo Vui long cai dat Python hoac them vao PATH
    pause
    exit /b 1
)
echo Python OK!

echo.
echo [2/5] Cai dat dependencies...
py -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo Loi khi cai dat dependencies!
    pause
    exit /b 1
)
echo Dependencies da cai dat!

echo.
echo [3/5] Chay migrations...
py manage.py migrate
if %errorlevel% neq 0 (
    echo Loi khi chay migrations!
    pause
    exit /b 1
)

echo.
echo [4/5] Tao thu muc media...
if not exist "media" mkdir media
if not exist "media\crawled_images" mkdir media\crawled_images
echo Thu muc media da duoc tao

echo.
echo [5/5] Khoi dong server...
echo ========================================
echo   Server dang khoi dong...
echo   URL: http://localhost:8000
echo   URL mang: http://0.0.0.0:8000
echo   Nhan Ctrl+C de dung server
echo ========================================
echo.
py manage.py runserver 0.0.0.0:8000

echo.
echo Server da dung.
pause
