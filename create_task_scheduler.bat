@echo off
echo ========================================
echo   Tao Windows Task cho Django Service
echo   (Thay the cho NSSM)
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

REM Lay duong dan hien tai
set PROJECT_PATH=%~dp0
set PROJECT_PATH=%PROJECT_PATH:~0,-1%

echo Duong dan project: %PROJECT_PATH%
echo.

echo Tao Windows Scheduled Task...

REM Xoa task cu neu co
schtasks /delete /tn "DjangoImageCrawler" /f >nul 2>&1

REM Tao task moi
schtasks /create /tn "DjangoImageCrawler" /tr "%PROJECT_PATH%\start_production_service.bat" /sc onstart /ru "SYSTEM" /rl highest /f

if %errorlevel% equ 0 (
    echo Task da duoc tao thanh cong!
    echo.
    echo Thong tin task:
    echo - Ten: DjangoImageCrawler
    echo - Chay khi: Windows khoi dong
    echo - Quyen: SYSTEM
    echo.
    
    echo Ban co muon khoi dong task ngay bay gio? (Y/N)
    set /p choice=Nhap lua chon: 
    if /i "%choice%"=="Y" (
        echo Khoi dong task...
        schtasks /run /tn "DjangoImageCrawler"
        echo Task da duoc khoi dong!
        echo.
        echo Kiem tra trang thai:
        schtasks /query /tn "DjangoImageCrawler"
    )
) else (
    echo Loi khi tao task!
)

echo.
echo ========================================
echo   Cac lenh quan ly task:
echo   
echo   Khoi dong:    schtasks /run /tn "DjangoImageCrawler"
echo   Dung:         schtasks /end /tn "DjangoImageCrawler"
echo   Xoa:          schtasks /delete /tn "DjangoImageCrawler" /f
echo   Trang thai:   schtasks /query /tn "DjangoImageCrawler"
echo   
echo   Hoac mo Task Scheduler: taskschd.msc
echo ========================================
echo.
pause
