# Ứng dụng Tích hợp của Tôi (Python)

Một ứng dụng Python tích hợp với các dịch vụ khác nhau bao gồm Google Calendar, Gmail và LinkedIn. Ứng dụng này cung cấp giải pháp dựa trên server để quản lý tích hợp và có thể chạy như một dịch vụ Windows.

## Tính năng

- **Tích hợp Google Calendar**: Quản lý sự kiện lịch qua `calendar_service.py`
- **Tích hợp Gmail**: Xử lý các thao tác email qua `gmail_service.py`
- **Tích hợp LinkedIn**: Kết nối với các dịch vụ LinkedIn qua `linkedin_service.py`
- **Máy chủ Flask**: Máy chủ API RESTful chạy trên cổng 3000 (có thể cấu hình)
- **Hỗ trợ dịch vụ Windows**: Có thể cài đặt như một dịch vụ Windows bằng `pywin32`

## Yêu cầu tiên quyết

- Python 3.8 trở lên
- pip (Python package manager)
- Thông tin xác thực Google API (cho các dịch vụ Google)
- Hệ điều hành Windows (để cài đặt dịch vụ)

## Cài đặt

1. Sao chép kho lưu trữ:

   ```bash
   git clone https://github.com/Trantoan-blip/SOA.git
   cd SOA/src
   ```

2. Tạo môi trường ảo (khuyến khích):

   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. Cài đặt các phụ thuộc:

   ```bash
   pip install -r requirements.txt
   ```

4. Thiết lập biến môi trường:
   - Thêm các khóa API và cấu hình của bạn:
     ```
     GOOGLE_CLIENT_ID=your_google_client_id
     GOOGLE_CLIENT_SECRET=your_google_client_secret
     LINKEDIN_CLIENT_ID=your_linkedin_client_id
     LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
     PORT=3000
     ```

5. Đặt file `credentials.json` từ Google API:
   - Download file từ [Google Cloud Console](https://console.cloud.google.com)
   - Đặt vào thư mục `src/`

## Sử dụng

### Phát triển

```bash
python server.py
```

### Sản xuất (với Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 server:app
```

Máy chủ sẽ khởi động trên cổng đã cấu hình (mặc định: 3000).

## Điểm cuối API

### Kiểm tra sức khỏe

- `GET /health` - Kiểm tra trạng thái server

### LinkedIn

- `GET /linkedin/auth-url` - Lấy URL xác thực LinkedIn
- `GET /callback` - Callback sau khi LinkedIn redirect
- `GET /linkedin/profile` - Xem profile LinkedIn
- `POST /linkedin/post` - Đăng bài mới trên LinkedIn

### Gmail

- `GET /google/auth-url` - Lấy URL xác thực Google
- `GET /google/callback` - Callback sau khi Google redirect
- `GET /gmail/list` - Danh sách email
- `POST /gmail/send` - Gửi email

### Google Calendar

- `GET /calendar/events` - Danh sách sự kiện
- `POST /calendar/create` - Tạo sự kiện mới

## Cài đặt dịch vụ Windows

Để cài đặt như một dịch vụ Windows:

1. Mở Command Prompt hoặc PowerShell **dưới quyền Administrator**

2. Điều hướng tới thư mục `src`:

   ```bash
   cd SOA\src
   ```

3. Cài đặt dịch vụ:

   ```bash
   python install_service.py install
   ```

4. Khởi động dịch vụ:

   ```bash
   python install_service.py start
   ```

5. Để dừng dịch vụ:

   ```bash
   python install_service.py stop
   ```

6. Để xóa dịch vụ:

   ```bash
   python install_service.py remove
   ```

Dịch vụ sẽ được cài đặt và có thể được quản lý qua **Services** (services.msc) trên Windows.

## Cấu trúc dự án

```
src/
├── server.py              # Máy chủ Flask chính
├── calendar_service.py    # Tích hợp Google Calendar
├── gmail_service.py       # Tích hợp Gmail
├── linkedin_service.py    # Tích hợp LinkedIn
├── windows_service.py     # Windows service wrapper
├── install_service.py     # Trình cài đặt dịch vụ Windows
├── requirements.txt       # Phụ thuộc Python
├── .env.example           # Ví dụ file biến môi trường
├── .env                   # Biến môi trường (không commit)
├── .gitignore             # Quy tắc git ignore
├── credentials.json       # Google API credentials (không commit)
└── daemon/                # File dịch vụ Windows (legacy)
    ├── myintegrationapp.exe.config
    └── myintegrationapp.xml
```

## Cấu hình

Cấu hình ứng dụng bằng biến môi trường trong `.env`:

- `PORT`: Cổng máy chủ (mặc định: 3000)
- `GOOGLE_CLIENT_ID`: ID khách hàng Google API
- `GOOGLE_CLIENT_SECRET`: Bí mật khách hàng Google API
- `LINKEDIN_CLIENT_ID`: ID ứng dụng LinkedIn
- `LINKEDIN_CLIENT_SECRET`: Bí mật ứng dụng LinkedIn

## Khắc phục sự cố

### "Module not found" errors

```bash
pip install -r requirements.txt
```

### Google credentials error

Đảm bảo file `credentials.json` nằm trong thư mục `src/` và chứa thông tin Google OAuth của bạn.

### Port already in use

```bash
# Thay đổi PORT trong file .env hoặc sử dụng:
PORT=5000 python server.py
```

## Đóng góp

1. Fork kho lưu trữ
2. Tạo nhánh tính năng (`git checkout -b feature/AmazingFeature`)
3. Commit các thay đổi của bạn (`git commit -m 'Add some AmazingFeature'`)
4. Push lên nhánh (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## Giấy phép

Dự án này được cấp phép theo Giấy phép MIT.
