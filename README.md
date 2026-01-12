# Ứng Dụng Quản Lý Thực Phẩm CP BVTV Phú Nông

Ứng dụng quản lý thực phẩm và đăng ký suất ăn cho công nhân viên, được xây dựng bằng Python với giao diện Tkinter.

## 📋 Mục Lục

- [Tính Năng](#-tính-năng)
- [Công Nghệ Sử Dụng](#-công-nghệ-sử-dụng)
- [Yêu Cầu Hệ Thống](#-yêu-cầu-hệ-thống)
- [Cài Đặt](#-cài-đặt)
- [Hướng Dẫn Sử Dụng](#-hướng-dẫn-sử-dụng)
- [Cấu Trúc Dự Án](#-cấu-trúc-dự-án)
- [Build Ứng Dụng](#-build-ứng-dụng)

## ✨ Tính Năng

### 1. **Quản Lý Mặt Hàng Nông Sản - Thực Phẩm**
- Xem danh sách sản phẩm và trái cây
- Thêm, sửa, xóa mặt hàng
- Quản lý đơn vị tính và đơn giá
- Chỉnh sửa tiêu đề trang

### 2. **Danh Sách CNV Đăng Ký Suất Ăn**
- Chọn ngày đăng ký suất ăn
- Quản lý danh sách nhân viên đăng ký
- Đăng ký suất ăn trưa (11h30) và chiều (16h00)
- Lập thực đơn cho từng buổi
- Xuất file Excel theo ngày

### 3. **Cập Nhật Danh Sách Nhân Viên**
- Thêm nhân viên mới
- Sửa thông tin nhân viên (họ tên, bộ phận, suất ăn)
- Xóa nhân viên khỏi danh sách
- Quản lý số suất ăn mặc định của nhân viên

### 4. **Quản Lý Menu**
- Tạo và quản lý thực đơn
- Thêm sản phẩm vào menu
- Chỉnh sửa số lượng và đơn giá

### 5. **Đặt Hàng**
- Tạo đơn đặt hàng thực phẩm
- Xuất đơn hàng ra file Excel theo tháng
- Format: `DatHangTu[MM]-[YYYY].xlsx`

### 6. **Thống Kê**
- Chọn tháng/năm cần thống kê
- Xem trước dữ liệu chi phí
- Xuất báo cáo tổng hợp chi phí ra Excel
- Format: `TongHopChiPhiTrongThangNam[YYYY].xlsx`

## 🛠 Công Nghệ Sử Dụng

- **Python 3.x** - Ngôn ngữ lập trình chính
- **Tkinter** - Framework GUI (có sẵn trong Python)
- **openpyxl 3.1.2** - Thư viện xử lý file Excel
- **Pillow 10.1.0** - Thư viện xử lý hình ảnh
- **PyInstaller 6.3.0** - Công cụ build file thực thi (.exe)

## 💻 Yêu Cầu Hệ Thống

- **Hệ điều hành**: Windows 10/11
- **Python**: 3.8 hoặc cao hơn
- **RAM**: Tối thiểu 2GB
- **Dung lượng ổ cứng**: 100MB trống

## 🚀 Cài Đặt

### Cài Đặt Cho Phát Triển

1. **Clone repository**
```bash
git clone https://github.com/QuiItPner/CPBVTV_Food_Management.git
cd app_thucpham_CP
```

2. **Tạo môi trường ảo Python (khuyến nghị)**
```bash
python -m venv venv
```

3. **Kích hoạt môi trường ảo**
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. **Cài đặt các thư viện cần thiết**
```bash
pip install -r requirements.txt
```

5. **Chạy ứng dụng**
```bash
python main.py
```

### Cài Đặt Cho Người Dùng Cuối

1. Tải file `QuanLyThucPham.exe` từ thư mục `dist/`
2. Copy toàn bộ thư mục sang máy tính cần sử dụng
3. Double-click vào `QuanLyThucPham.exe` để khởi động

**Lưu ý**: Nếu Windows Defender chặn file .exe:
- Chuột phải > Properties > Unblock
- Hoặc chạy với quyền Administrator

## 📖 Hướng Dẫn Sử Dụng

### Khởi Động Ứng Dụng

1. Chạy file `main.py` (cho dev) hoặc `QuanLyThucPham.exe` (cho user)
2. Giao diện menu chính sẽ hiển thị với 6 chức năng chính

### Quản Lý Dữ Liệu

**File Excel chính**: `excel_files/FoodManagement.xlsx`

Cấu trúc các Sheet:
- **Products**: Danh sách sản phẩm
- **Fruits**: Danh sách trái cây
- **Dat hang thuc phẩm**: Danh sách nhân viên
- **Meal_YYYYMMDD**: Database nhân viên đăng ký (tự động tạo)
- **Settings**: Cấu hình ứng dụng
- **Menus**: Danh sách thực đơn

### Xuất File Báo Cáo

Ứng dụng tự động tạo các file Excel:
- `DatHangTu[MM]-[YYYY].xlsx` - Đơn đặt hàng theo tháng
- `TongHopChiPhiTrongThangNam[YYYY].xlsx` - Báo cáo thống kê theo năm

### Lưu Ý Quan Trọng

1. ⚠️ **KHÔNG XÓA** file `FoodManagement.xlsx` - đây là database chính
2. ⚠️ **KHÔNG MỞ** file Excel khi ứng dụng đang chạy
3. 💾 Sao lưu dữ liệu định kỳ bằng cách copy các file `.xlsx`
4. 📁 Giữ file `.exe` cùng thư mục với các file dữ liệu

## 📂 Cấu Trúc Dự Án

```
app_thucpham_CP/
├── main.py                    # File khởi động ứng dụng
├── config.py                  # File cấu hình (màu sắc, font, kích thước)
├── requirements.txt           # Danh sách thư viện cần cài
├── build.bat                  # Script build file .exe
├── HUONG_DAN_SU_DUNG.txt     # Hướng dẫn sử dụng chi tiết
├── DEPLOYMENT_GUIDE.md        # Hướng dẫn triển khai
│
├── models/                    # Module quản lý dữ liệu
│   ├── __init__.py
│   └── data_manager.py        # Class xử lý Excel và business logic
│
├── ui/                        # Module giao diện người dùng
│   ├── __init__.py
│   ├── main_window.py         # Cửa sổ chính và menu
│   ├── products_page.py       # Trang quản lý sản phẩm
│   ├── meal_registration_page.py  # Trang đăng ký suất ăn
│   └── dialogs.py             # Các hộp thoại phụ
│
├── images/                    # Thư mục chứa hình ảnh
│   ├── app_icon.png           # Icon ứng dụng
│   ├── products/              # Hình ảnh sản phẩm
│   └── fruits/                # Hình ảnh trái cây
│
├── excel_files/               # Thư mục chứa dữ liệu Excel
│   └── FoodManagement.xlsx    # Database chính (tự động tạo)
│
└── dist/                      # Thư mục output sau khi build
    └── QuanLyThucPham.exe     # File thực thi
```

## 🔨 Build Ứng Dụng

Để build file `.exe` từ source code:

1. **Đảm bảo đã cài đặt PyInstaller**
```bash
pip install pyinstaller==6.3.0
```

2. **Chạy script build**
```bash
build.bat
```

Hoặc build thủ công:
```bash
pyinstaller --onefile --windowed --icon=images/app_icon.ico --name=QuanLyThucPham main.py
```

3. **Tìm file .exe** trong thư mục `dist/`

### Tham Số Build

- `--onefile`: Đóng gói thành 1 file .exe duy nhất
- `--windowed`: Ẩn console window (chỉ hiện GUI)
- `--icon`: Đặt icon cho ứng dụng
- `--name`: Đặt tên cho file .exe

## 🐛 Xử Lý Lỗi Thường Gặp

### Lỗi: "File đang được mở"
**Nguyên nhân**: File Excel đang được mở bởi Excel hoặc ứng dụng khác
**Giải pháp**: Đóng tất cả file Excel và khởi động lại ứng dụng

### Lỗi: Ứng dụng không chạy
**Nguyên nhân**: Windows Defender/Antivirus chặn file .exe
**Giải pháp**: 
- Chuột phải > Properties > Unblock
- Thêm exception trong antivirus
- Chạy với quyền Administrator

### Lỗi: Thiếu thư viện
**Nguyên nhân**: Chưa cài đặt đầy đủ dependencies
**Giải pháp**: 
```bash
pip install -r requirements.txt
```

### Mất dữ liệu
**Giải pháp**: Khôi phục từ file backup `.xlsx` đã sao lưu trước đó

## 📝 Phiên Bản

**Version**: 1.0  
**Release Date**: 11/12/2025  
**Python Version**: 3.8+  
**Platform**: Windows 10/11

## 👥 Hỗ Trợ

Nếu gặp vấn đề khi sử dụng, vui lòng:
1. Kiểm tra file `HUONG_DAN_SU_DUNG.txt`
2. Xem lại phần Xử Lý Lỗi trong README này
3. Liên hệ bộ phận IT để được hỗ trợ

## 📄 License

Ứng dụng nội bộ của CP BVTV Phú Nông - Không phân phối ra bên ngoài.

---

**Phát triển bởi**: CP BVTV Phú Nông  
**Mục đích**: Quản lý thực phẩm và suất ăn nội bộ
