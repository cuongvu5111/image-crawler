@echo off
echo ========================================
echo   Setup NSSM cho Django Image Crawler
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

REM Duong dan NSSM hien tai
set NSSM_SOURCE=D:\app\nssm\win64\nssm.exe
set NSSM_TARGET=C:\Windows\System32\nssm.exe

echo Kiem tra NSSM...
echo Nguon: %NSSM_SOURCE%
echo Dich:  %NSSM_TARGET%
echo.

REM Kiem tra file nguon
if not exist "%NSSM_SOURCE%" (
    echo Khong tim thay NSSM tai: %NSSM_SOURCE%
    echo.
    echo Huong dan khac phuc:
    echo    1. Kiem tra duong dan NSSM
    echo    2. Hoac tai NSSM tu: https://nssm.cc/download
    echo    3. Giai nen vao thu muc D:\app\nssm\
    echo.
    pause
    exit /b 1
)

echo Tim thay NSSM tai: %NSSM_SOURCE%

REM Kiem tra xem da copy chua
if exist "%NSSM_TARGET%" (
    echo NSSM da ton tai trong System32
    echo.
    echo Ban co muon ghi de khong? (Y/N)
    set /p choice=Nhap lua chon:
    if /i not "%choice%"=="Y" (
        echo Huy bo copy NSSM
        goto :test_nssm
    )
)

echo.
echo Copy NSSM vao System32...
copy "%NSSM_SOURCE%" "%NSSM_TARGET%" >nul
if %errorlevel% equ 0 (
    echo Copy NSSM thanh cong!
) else (
    echo Loi khi copy NSSM!
    pause
    exit /b 1
)

:test_nssm
echo.
echo Test NSSM...
nssm version
if %errorlevel% equ 0 (
    echo NSSM hoat dong binh thuong!
) else (
    echo NSSM khong hoat dong!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Setup NSSM hoan tat!
echo
echo   Buoc tiep theo:
echo   1. Chay install_service.bat de cai service
echo   2. Hoac su dung lenh nssm truc tiep
echo
echo   Lenh NSSM co ban:
echo   - nssm install [servicename] [program]
echo   - nssm start [servicename]
echo   - nssm stop [servicename]
echo   - nssm remove [servicename]
echo ========================================
echo.
pause
