@echo off
echo ========================================
echo   Cai dat Django Image Crawler Service
echo ========================================

REM Kiem tra quyen Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Loi: Can chay voi quyen Administrator!
    echo Cach khac phuc:
    echo    1. Click phai vao file nay
    echo    2. Chon "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo.
echo Dang chay voi quyen Administrator
echo.

REM Lấy đường dẫn hiện tại
set PROJECT_PATH=%~dp0
set PROJECT_PATH=%PROJECT_PATH:~0,-1%

echo Duong dan project: %PROJECT_PATH%
echo.

REM Duong dan NSSM - Thu nhieu vi tri
set NSSM_PATH=D:\app\nssm\win64\nssm.exe

REM Neu khong tim thay, thu vi tri khac
if not exist "%NSSM_PATH%" (
    set NSSM_PATH=C:\Windows\System32\nssm.exe
)
if not exist "%NSSM_PATH%" (
    set NSSM_PATH=nssm.exe
)

REM Kiểm tra NSSM
if not exist "%NSSM_PATH%" (
    echo NSSM khong tim thay tai: %NSSM_PATH%
    echo.
    echo Huong dan khac phuc:
    echo    1. Kiem tra duong dan NSSM trong script
    echo    2. Hoac copy nssm.exe vao C:\Windows\System32\
    echo    3. Hoac them D:\app\nssm\win64\ vao PATH
    echo.
    pause
    exit /b 1
)

"%NSSM_PATH%" version >nul 2>&1
if %errorlevel% neq 0 (
    echo NSSM khong the chay!
    echo.
    pause
    exit /b 1
)

echo NSSM da duoc cai dat
echo.

REM Dung service neu dang chay
echo Dung service cu (neu co)...
"%NSSM_PATH%" stop DjangoImageCrawler >nul 2>&1
"%NSSM_PATH%" remove DjangoImageCrawler confirm >nul 2>&1

echo.
echo Cai dat service moi...

REM Cài đặt service
"%NSSM_PATH%" install DjangoImageCrawler "%PROJECT_PATH%\start_production.bat"
if %errorlevel% neq 0 (
    echo Loi khi cai dat service!
    pause
    exit /b 1
)

REM Cấu hình service
"%NSSM_PATH%" set DjangoImageCrawler AppDirectory "%PROJECT_PATH%"
"%NSSM_PATH%" set DjangoImageCrawler DisplayName "Django Image Crawler"
"%NSSM_PATH%" set DjangoImageCrawler Description "Django Image Crawler - Web scraping service for downloading images"
"%NSSM_PATH%" set DjangoImageCrawler Start SERVICE_AUTO_START

REM Cấu hình logging
"%NSSM_PATH%" set DjangoImageCrawler AppStdout "%PROJECT_PATH%\logs\service_output.log"
"%NSSM_PATH%" set DjangoImageCrawler AppStderr "%PROJECT_PATH%\logs\service_error.log"
"%NSSM_PATH%" set DjangoImageCrawler AppRotateFiles 1
"%NSSM_PATH%" set DjangoImageCrawler AppRotateOnline 1
"%NSSM_PATH%" set DjangoImageCrawler AppRotateBytes 1048576

REM Tạo thư mục logs
if not exist "%PROJECT_PATH%\logs" mkdir "%PROJECT_PATH%\logs"

echo.
echo ✅ Service đã được cài đặt thành công!
echo.

echo Khoi dong service...
"%NSSM_PATH%" start DjangoImageCrawler
if %errorlevel% equ 0 (
    echo Service da khoi dong thanh cong!
    echo.
    echo Truy cap ung dung tai: http://localhost:8000
    echo Kiem tra trang thai: services.msc
    echo Xem logs tai: %PROJECT_PATH%\logs\
) else (
    echo Loi khi khoi dong service!
    echo Kiem tra logs de biet chi tiet loi
)

echo.
echo ========================================
echo   Cac lenh quan ly service:
echo   Khoi dong: "%NSSM_PATH%" start DjangoImageCrawler
echo   Dung:      "%NSSM_PATH%" stop DjangoImageCrawler
echo   Restart:   "%NSSM_PATH%" restart DjangoImageCrawler
echo   Go bo:     "%NSSM_PATH%" remove DjangoImageCrawler
echo   Trang thai: "%NSSM_PATH%" status DjangoImageCrawler
echo ========================================
echo.
pause
