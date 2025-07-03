@echo off
echo ========================================
echo   Go bo Django Image Crawler Service
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

REM Đường dẫn NSSM
set NSSM_PATH=D:\app\nssm\win64\nssm.exe

REM Kiểm tra NSSM
if not exist "%NSSM_PATH%" (
    echo NSSM khong tim thay tai: %NSSM_PATH%
    echo Kiem tra duong dan NSSM
    echo.
    pause
    exit /b 1
)

REM Kiểm tra service có tồn tại không
"%NSSM_PATH%" status DjangoImageCrawler >nul 2>&1
if %errorlevel% neq 0 (
    echo Service DjangoImageCrawler khong ton tai hoac chua duoc cai dat
    echo.
    pause
    exit /b 0
)

echo Trang thai service hien tai:
"%NSSM_PATH%" status DjangoImageCrawler
echo.

echo Dung service...
"%NSSM_PATH%" stop DjangoImageCrawler
if %errorlevel% equ 0 (
    echo Service da duoc dung
) else (
    echo Service co the da dung tu truoc
)

echo.
echo Go bo service...
"%NSSM_PATH%" remove DjangoImageCrawler confirm
if %errorlevel% equ 0 (
    echo Service da duoc go bo thanh cong!
) else (
    echo Loi khi go bo service
)

echo.
echo ========================================
echo   Hoan tat go bo service
echo
echo   Luu y:
echo   - Project files van con nguyen
echo   - Logs van duoc giu lai
echo   - Co the cai dat lai bang install_service.bat
echo ========================================
echo.
pause
