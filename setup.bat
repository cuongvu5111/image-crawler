@echo off
echo ========================================
echo    Django Image Crawler Setup
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
    echo Vui long cai dat Python truoc khi tiep tuc
    pause
    exit /b 1
)

echo.
echo [2/5] Cai dat dependencies...
py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Loi khi cai dat dependencies!
    pause
    exit /b 1
)

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
echo [5/5] Collect static files...
py manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo Canh bao: Khong the collect static files
)

echo.
echo ========================================
echo Setup hoan tat!
echo.
echo Buoc tiep theo:
echo    1. Chay: run_server.bat
echo    2. Mo browser: http://127.0.0.1:8000
echo    3. Tao superuser (tuy chon):
echo       py manage.py createsuperuser
echo ========================================
echo.
pause
