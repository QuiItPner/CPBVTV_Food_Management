-- Tạo database FoodManagement
CREATE DATABASE FoodManagement;
GO

USE FoodManagement;
GO

-- Tạo bảng Products
CREATE TABLE Products (
    STT INT PRIMARY KEY IDENTITY(1,1),
    TenHang NVARCHAR(255) NOT NULL,
    DVT NVARCHAR(50) NOT NULL,
    DonGia DECIMAL(18,2) NOT NULL
);
GO

-- Tạo bảng Settings
CREATE TABLE Settings (
    SettingKey NVARCHAR(100) PRIMARY KEY,
    SettingValue NVARCHAR(MAX)
);
GO

-- Thêm cấu hình tiêu đề mặc định
INSERT INTO Settings (SettingKey, SettingValue) 
VALUES ('PageTitle', N'CÁC MẶT HÀNG NÔNG SẢN - THỰC PHẨM');
GO

-- Thêm dữ liệu mẫu (tùy chọn)
INSERT INTO Products (TenHang, DVT, DonGia) VALUES
(N'Cải chua', N'Kg', 18000),
(N'Cải ngọt', N'Kg', 34000),
(N'Cải thảo', N'Kg', 26000),
(N'Cải thìa', N'Kg', 43000),
(N'Cải xanh', N'Kg', 36000),
(N'Củ cải mặn', N'Kg', 30000),
(N'Hẹ', N'Kg', 30000),
(N'Mồng tơi', N'Kg', 34000),
(N'Rau dền', N'Kg', 32000),
(N'Rau lang', N'Kg', 25000),
(N'Rau má nhỏ', N'Kg', 45000),
(N'Rau muống hạt', N'Kg', 35000),
(N'Rau muống bào', N'Kg', 30000),
(N'Sả lách gai', N'Kg', 45000),
(N'Tan ô', N'Kg', 45000),
(N'Bạc hà', N'Kg', 20000),
(N'Bắp cải', N'Kg', 26000),
(N'Bầu', N'Kg', 28000),
(N'Bí đỏ hồ lô', N'Kg', 23000),
(N'Bí xanh', N'Kg', 23000),
(N'Khoai lang', N'Kg', 20000),
(N'Cà chua', N'Kg', 45000),
(N'Cà rốt công xanh', N'Kg', 30000),
(N'Cà tím', N'Kg', 23000),
(N'Củ cải trắng', N'Kg', 22000),
(N'Củ dền', N'Kg', 26000);
GO
