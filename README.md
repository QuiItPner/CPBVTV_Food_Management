# Ứng Dụng Quản Lý Thực Phẩm CP BVTV Phú Nông

Ứng dụng quản lý thực phẩm và đăng ký suất ăn cho công nhân viên, được xây dựng bằng Python với giao diện Tkinter.

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
git clone <repository-url>
cd app_thucpham_CP
