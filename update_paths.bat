@echo off
echo ========================================
echo   Cap nhat duong dan sau khi chuyen project
echo ========================================

REM Lay duong dan hien tai
set NEW_PROJECT_PATH=%~dp0
set NEW_PROJECT_PATH=%NEW_PROJECT_PATH:~0,-1%

echo.
echo Duong dan project moi: %NEW_PROJECT_PATH%
echo.

echo [1/3] Kiem tra cac file can cap nhat...

REM Kiem tra file nginx.conf
if exist "nginx.conf" (
    echo Tim thay nginx.conf - Can cap nhat thu cong
    echo Sua duong dan trong nginx.conf:
    echo   - Static files: %NEW_PROJECT_PATH%\staticfiles\
    echo   - Media files:  %NEW_PROJECT_PATH%\media\
    echo.
)

REM Kiem tra virtual environment
if exist ".venv" (
    echo [2/3] Tim thay virtual environment
    echo Luu y: Virtual environment co the can tao lai
    echo Neu gap loi, chay: 
    echo   rmdir /s .venv
    echo   python -m venv .venv
    echo   .venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
)

echo [3/3] Kiem tra database
if exist "db.sqlite3" (
    echo Tim thay database - Khong can thay doi
) else (
    echo Khong tim thay database - Can chay migrations:
    echo   py manage.py migrate
)

echo.
echo ========================================
echo   Cac buoc can thuc hien:
echo   
echo   1. Neu dung nginx: Cap nhat nginx.conf
echo   2. Neu gap loi venv: Tao lai virtual environment  
echo   3. Chay: py manage.py runserver
echo   4. Test tai: http://127.0.0.1:8000
echo ========================================
echo.

echo Duong dan NSSM hien tai: D:\app\nssm\win64\nssm.exe
if exist "D:\app\nssm\win64\nssm.exe" (
    echo NSSM OK - Scripts se hoat dong binh thuong
) else (
    echo Canh bao: NSSM khong tim thay
    echo Can cap nhat duong dan NSSM trong cac file .bat
)

echo.
pause
