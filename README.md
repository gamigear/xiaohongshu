# 🔖 XHS Queue Manager

Hệ thống quản lý hàng đợi tải xuống nội dung Xiaohongshu (小红书) không watermark với giao diện web và Chrome extension.

## ✨ Tính năng

- 🔖 **Chrome Extension**: Thêm link nhanh từ trình duyệt
- 🌐 **Web Interface**: Quản lý hàng đợi trực quan
- 🤖 **Auto Worker**: Tải tự động với delay tùy chỉnh
- 📁 **Category System**: Phân loại nội dung theo thư mục
- ⚙️ **Config Management**: Cài đặt linh hoạt
- 📊 **Real-time Dashboard**: Theo dõi tiến trình

## 🚀 Demo

- **Web Interface**: [https://xhs-queue-manager.vercel.app](https://xhs-queue-manager.vercel.app)
- **API Docs**: [https://xhs-queue-manager.vercel.app/docs](https://xhs-queue-manager.vercel.app/docs)

## 🏗️ Kiến trúc

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Chrome Extension│───▶│   API Server    │───▶│   PostgreSQL    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Download Worker│───▶│ XHS Downloader  │
                       └─────────────────┘    └─────────────────┘
```

## 🛠️ Cài đặt

### 1. Docker (Khuyến nghị)

```bash
# Clone repository
git clone https://github.com/yourusername/xhs-queue-manager.git
cd xhs-queue-manager

# Chạy với Docker Compose
docker compose up -d

# Truy cập
# Web: http://localhost:8080
# XHS API: http://localhost:5556
```

### 2. Manual Setup

```bash
# Backend
cd xhs-queue-server
pip install -r requirements.txt
python server.py

# Worker (terminal khác)
python worker.py
```

### 3. Chrome Extension

1. Mở Chrome → `chrome://extensions/`
2. Bật "Developer mode"
3. Click "Load unpacked" → chọn thư mục `xhs-collector-extension`

## 📋 Sử dụng

### Web Interface

1. **Thêm link**: Paste URL XHS → chọn category → thêm
2. **Quản lý queue**: Xem, xóa, theo dõi trạng thái
3. **Cài đặt**: Điều chỉnh delay, thư mục lưu
4. **Categories**: Quản lý phân loại

### Chrome Extension

1. Vào trang XHS bất kỳ
2. Click icon extension
3. Chọn category → "Thêm link"
4. Worker sẽ tự động tải

### API

```bash
# Thêm link
curl -X POST http://localhost:8080/api/add \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.xiaohongshu.com/explore/...", "category": "food"}'

# Xem queue
curl http://localhost:8080/api/queue

# Cập nhật config
curl -X POST http://localhost:8080/api/config \
  -H "Content-Type: application/json" \
  -d '{"delay_seconds": 180}'
```

## 🔧 Cấu hình

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# XHS API
XHS_API_URL=http://localhost:5556/xhs/detail

# Worker
DELAY_SECONDS=120
```

### Docker Compose

```yaml
services:
  xhs-downloader:
    image: joeanamier/xhs-downloader
    ports: ["5556:5556"]
    
  xhs-queue-server:
    build: ./xhs-queue-server
    ports: ["8080:8080"]
    
  xhs-worker:
    build: ./xhs-queue-server
    command: python worker.py
```

## 📁 Cấu trúc Project

```
xhs-queue-manager/
├── xhs-collector-extension/     # Chrome Extension
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
├── xhs-queue-server/           # Backend API
│   ├── server.py              # FastAPI server
│   ├── worker.py              # Download worker
│   ├── static/                # Web interface
│   └── requirements.txt
├── docker-compose.yml         # Docker setup
└── README.md
```

## 🌐 Deployment

### Vercel (Frontend)

```bash
# Deploy web interface
vercel --prod

# Environment variables
VERCEL_URL=your-app.vercel.app
```

### Railway/Heroku (Backend)

```bash
# Deploy API server
railway deploy
# hoặc
git push heroku main
```

## 🔗 Links

- **Repository**: [GitHub](https://github.com/yourusername/xhs-queue-manager)
- **Issues**: [Bug Reports](https://github.com/yourusername/xhs-queue-manager/issues)
- **Discussions**: [Q&A](https://github.com/yourusername/xhs-queue-manager/discussions)

## 📄 License

MIT License - xem [LICENSE](LICENSE) để biết thêm chi tiết.

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Tạo Pull Request

## ⚠️ Disclaimer

Tool này chỉ dành cho mục đích học tập và nghiên cứu. Vui lòng tuân thủ Terms of Service của Xiaohongshu.

## 🙏 Credits

- [XHS-Downloader](https://github.com/JoeanAmier/XHS-Downloader) - Core download functionality
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [PostgreSQL](https://www.postgresql.org/) - Database