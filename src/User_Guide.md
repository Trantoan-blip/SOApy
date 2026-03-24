# Hướng Dẫn Sử Dụng - My Integration App (Python)

## 📋 Mục lục

1. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
2. [Cài Đặt](#cài-đặt)
3. [Cấu Hình](#cấu-hình)
4. [Chạy Ứng Dụng](#chạy-ứng-dụng)
5. [Sử Dụng API](#sử-dụng-api)
6. [Cài Đặt Dịch Vụ Windows](#cài-đặt-dịch-vụ-windows)
7. [Khắc Phục Sự Cố](#khắc-phục-sự-cố)

---

## Yêu Cầu Hệ Thống

- **Python**: 3.8 hoặc cao hơn
- **pip**: Python package manager
- **Git**: Để clone repository
- **Windows**: Để cài đặt dịch vụ Windows
- **API Keys**:
  - Google Client ID & Secret (từ Google Cloud Console)
  - LinkedIn Client ID & Secret (từ LinkedIn Developer)

---

## Cài Đặt

### Bước 1: Clone Repository

```bash
git clone https://github.com/Trantoan-blip/SOA.git
cd SOA/src
```

### Bước 2: Tạo Virtual Environment (Khuyến khích)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
```

### Bước 3: Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

---

## Cấu Hình

### Bước 1: Tạo File `.env.example`

### Bước 2: Thêm API Credentials

Mở file `.env.example` và cập nhật:

```env
# Google API Credentials
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# LinkedIn API Credentials
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret

# Server Port
PORT=3000
```

### Bước 3: Setup Google Credentials File

1. Truy cập [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo OAuth 2.0 Client ID (Desktop application)
3. Download `credentials.json`
4. Đặt vào thư mục `src/`

---

## Chạy Ứng Dụng

### Mode Development

```bash
cd C:\SOA\src
python server.py
```

Server sẽ khởi động trên `http://127.0.0.1:3000`

### Mode Production (với Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 server:app
```

### Kiểm Tra Server

Truy cập trong browser hoặc dùng curl:

```bash
curl http://127.0.0.1:3000/health
```

---

## Sử Dụng API

### 1. Health Check

```bash
GET http://127.0.0.1:3000/health
```

**Response:**

```json
{
  "status": "ok",
  "message": "Server is running"
}
```

### 2. LinkedIn Integration

#### Lấy URL Xác Thực

```bash
GET http://127.0.0.1:3000/linkedin/auth-url
```

**Response:**

```json
{
  "url": "https://www.linkedin.com/oauth/v2/authorization?..."
}
```

#### Callback (Tự động sau xác thực)

```bash
GET http://127.0.0.1:3000/callback?code=AUTH_CODE
```

#### Xem Profile

```bash
GET http://127.0.0.1:3000/linkedin/profile
```

#### Đăng Bài

```bash
POST http://127.0.0.1:3000/linkedin/post
Content-Type: application/json

{
  "text": "Hello LinkedIn!"
}
```

### 3. Gmail Integration

#### Xác Thực Google

```bash
GET http://127.0.0.1:3000/google/auth-url
```

#### Danh Sách Email

```bash
GET http://127.0.0.1:3000/gmail/list
```

#### Gửi Email

```bash
POST http://127.0.0.1:3000/gmail/send
Content-Type: application/json

{
  "to": "recipient@example.com",
  "subject": "Test Email",
  "body": "This is a test email"
}
```

### 4. Google Calendar Integration

#### Danh Sách Sự Kiện

```bash
GET http://127.0.0.1:3000/calendar/events
```

#### Tạo Sự Kiện

```bash
POST http://127.0.0.1:3000/calendar/create
Content-Type: application/json

{
  "summary": "Team Meeting",
  "description": "Weekly sync",
  "start": "2026-03-24T10:00:00",
  "end": "2026-03-24T11:00:00"
}
```

---

## Cài Đặt Dịch Vụ Windows

### Cài Đặt (Yêu Cầu Administrator)

Mở **Command Prompt** hoặc **PowerShell** dưới quyền Administrator:

```bash
cd C:\SOA\src
python install_service.py install
```

### Khởi Động Dịch Vụ

```bash
python install_service.py start
```

### Dừng Dịch Vụ

```bash
python install_service.py stop
```

### Gỡ Bỏ Dịch Vụ

```bash
python install_service.py remove
```

### Quản Lý Dịch Vụ

- Mở **Services** (services.msc)
- Tìm **My Integration App**
- Right-click để khởi động/dừng

---

## Khắc Phục Sự Cố

### 1. "ModuleNotFoundError: No module named 'dotenv'"

**Giải pháp:**

```bash
pip install -r requirements.txt
```

### 2. "Port 3000 already in use"

**Giải pháp:**
Thay đổi PORT trong `.env.example`:

```env
PORT=5000
```

Hoặc kill process:

```bash
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### 3. "Google credentials not found"

**Giải pháp:**

- Đảm bảo `credentials.json` trong thư mục `src/`
- Kiểm tra file có quyền đọc không

### 4. Service không khởi động

**Giải pháp:**

```bash
# Kiểm tra logs
python install_service.py stop
# Xóa và cài đặt lại
python install_service.py remove
python install_service.py install
```

### 5. Virtual Environment không activate

**Giải pháp:**

```bash
# Windows
C:\SOA\venv\Scripts\activate

# Hoặc chạy python trực tiếp từ venv
C:\SOA\.venv\Scripts\python.exe server.py
```

---

## Structure File

```
SOA/
├── src/
│   ├── server.py              # Flask application chính
│   ├── calendar_service.py    # Google Calendar service
│   ├── gmail_service.py       # Gmail service
│   ├── linkedin_service.py    # LinkedIn service
│   ├── windows_service.py     # Windows service wrapper
│   ├── install_service.py     # Service installer
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── .env                  # Local config (not committed)
│   ├── credentials.json      # Google API credentials
│   ├── README.md             # Project documentation
│   ├── User_Guide.md         # This file
│   └── daemon/               # Legacy Windows service files
├── .gitignore
└── README.md
```

---

## Tips & Best Practices

### Bảo Mật

- ✅ **KHÔNG** commit `.env.example` hoặc `credentials.json`
- ✅ Kiểm tra `.gitignore` đã bao gồm các file nhạy cảm
- ✅ Sử dụng environment variables cho secrets

### Performance

- Sử dụng **Gunicorn** cho production
- Cân nhắc **reverse proxy** (Nginx)
- Monitor system resources

### Development

- Sử dụng **virtual environment**
- Cập nhật dependencies thường xuyên
- Test các endpoints trước deploy

---

## Contact & Support

Nếu gặp vấn đề:

1. Kiểm tra **[README.md](README.md)** trong repository
2. Xem **[Khắc Phục Sự Cố](#khắc-phục-sự-cố)** phía trên
3. Tạo Issue trên GitHub

---

**Happy coding! 🚀**
