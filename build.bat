@echo off
echo ========================================
echo DONG GOI UNG DUNG QUAN LY THUC PHAM
echo ========================================
echo.

echo [1/4] Cai dat dependencies...
py -m pip install -r requirements.txt
if errorlevel 1 (
    echo Loi: Khong the cai dat dependencies!
    pause
    exit /b 1
)
echo.

echo [2/4] Chuyen doi icon PNG sang ICO...
py convert_icon.py
if errorlevel 1 (
    echo Loi: Khong the chuyen doi icon!
    pause
    exit /b 1
)
echo.

echo [3/4] Dong goi ung dung...
py -m PyInstaller build_app.spec --clean --noconfirm
if errorlevel 1 (
    echo Loi: Khong the dong goi ung dung!
    pause
    exit /b 1
)
echo.

echo [4/4] Copy file du lieu va huong dan...
xcopy excel_files dist\excel_files\ /E /I /Y >nul
copy HUONG_DAN_SU_DUNG.txt dist\ >nul
echo.

echo ========================================
echo HOAN THANH DONG GOI!
echo ========================================
echo.
echo Cac file trong thu muc dist:
dir /b dist
echo.
echo Thu muc: dist\
echo File chinh: QuanLyThucPham.exe
echo Du lieu: excel_files\FoodManagement.xlsx
echo Huong dan: HUONG_DAN_SU_DUNG.txt
echo.
echo Copy toan bo thu muc 'dist' sang may khac de su dung!
echo.
echo Nhan phim bat ky de dong cua so...
pause
