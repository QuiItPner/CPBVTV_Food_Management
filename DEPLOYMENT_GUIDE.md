# Hướng Dẫn Đóng Gói và Triển Khai

## Đóng Gói Ứng Dụng

### Yêu Cầu
- Python 3.10+
- Windows 10/11

### Các Bước Đóng Gói

1. **Chạy script build:**
   ```bash
   build.bat
   ```

2. **Kết quả:**
   - Thư mục `dist/` chứa toàn bộ ứng dụng
   - File `QuanLyThucPham.exe` (33MB)
   - File `FoodManagement.xlsx` (database mẫu)
   - File hướng dẫn sử dụng

## Triển Khai

### Copy sang máy khác

1. **Copy toàn bộ thư mục `dist/`** sang máy đích

2. **Cấu trúc thư mục cần giữ:**
   ```
   dist/
   ├── QuanLyThucPham.exe
   ├── FoodManagement.xlsx
   ├── HUONG_DAN_SU_DUNG.txt
   └── README.txt
   ```

3. **Chạy ứng dụng:**
   - Double-click `QuanLyThucPham.exe`
   - Nếu Windows Defender chặn: Click "More info" → "Run anyway"

### Lưu Ý Khi Triển Khai

#### Icon và Images
- Icon và images đã được **embed vào .exe**
- Không cần copy folder `images/`

#### Database
- File `FoodManagement.xlsx` **BẮT BUỘC** phải cùng thư mục với .exe
- Nếu không có file này, app sẽ tự tạo file mới (rỗng)

#### Files tạo tự động
Khi sử dụng, app sẽ tự tạo các file:
- `DatHangTu{MM}-{YYYY}.xlsx` - Đăng ký suất ăn theo tháng
- `TongHopChiPhiTrongThangNam{YYYY}.xlsx` - Báo cáo thống kê

## Build Script Chi Tiết

### build.bat thực hiện:

1. **Cài đặt dependencies** (openpyxl, Pillow, pyinstaller)
2. **Convert icon** từ PNG → ICO
3. **Đóng gói** với PyInstaller
4. **Copy files** cần thiết vào dist/

### build_app.spec

File cấu hình PyInstaller:
- **One-file mode**: Tất cả trong 1 file .exe
- **Windowed mode**: Không hiện console
- **Icon**: app_icon.ico
- **Data files**: 
  - images/ (embedded)
  - FoodManagement.xlsx (embedded nếu có)

## Xử Lý Lỗi Build

### Lỗi: "pip not found"
```bash
py -m pip install -r requirements.txt
```

### Lỗi: "pyinstaller not found"
```bash
py -m pip install pyinstaller
```

### Lỗi: "Icon conversion failed"
```bash
py convert_icon.py
```

### Rebuild từ đầu
```bash
py -m PyInstaller build_app.spec --clean --noconfirm
```

## Kiểm Tra Sau Khi Build

1. **Kiểm tra file size:**
   - QuanLyThucPham.exe: ~33MB

2. **Test chạy:**
   ```bash
   cd dist
   QuanLyThucPham.exe
   ```

3. **Kiểm tra chức năng:**
   - Mở app → Main menu hiển thị đúng
   - Vào từng chức năng test cơ bản
   - Tạo file Excel xem có lỗi không

## Phân Phối

### Cách 1: Copy trực tiếp
- Copy folder `dist/` vào USB
- Giải nén trên máy đích

### Cách 2: Nén thành ZIP
```bash
# Tạo file ZIP
cd d:\app_thucpham_CP
powershell Compress-Archive -Path dist\* -DestinationPath QuanLyThucPham_v1.0.zip
```

### Cách 3: Tạo installer (Advanced)
- Sử dụng NSIS hoặc Inno Setup
- Tự động tạo shortcut
- Thêm vào Programs & Features

## Bảo Trì

### Update ứng dụng
1. Sửa code
2. Chạy lại `build.bat`
3. Copy file .exe mới thay thế file cũ
4. **KHÔNG** thay thế file .xlsx (giữ nguyên dữ liệu)

### Backup dữ liệu
Copy các file:
- FoodManagement.xlsx
- DatHangTu*.xlsx
- TongHopChiPhi*.xlsx

## Version History

### v1.0 (11/12/2025)
- Phát hành đầu tiên
- Đầy đủ chức năng cơ bản
- Build size: 33MB
- Python 3.10.9
- PyInstaller 6.3.0
