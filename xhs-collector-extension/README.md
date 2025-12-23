# 🔖 XHS Collector Extension

Chrome extension để thêm link Xiaohongshu vào hàng đợi tải xuống.

## 📦 Cài đặt

### Development
1. Mở Chrome → `chrome://extensions/`
2. Bật "Developer mode"
3. Click "Load unpacked"
4. Chọn thư mục `xhs-collector-extension`

### Production
1. Zip toàn bộ thư mục extension
2. Upload lên Chrome Web Store
3. Hoặc distribute file .crx

## ⚙️ Cấu hình

Cập nhật API endpoint trong `popup.js`:

```javascript
// Development
const API_BASE = 'http://localhost:8080/api';

// Production  
const API_BASE = 'https://your-app.vercel.app/api';
```

## 🚀 Tính năng

- ✅ Thêm link XHS nhanh chóng
- ✅ Chọn category cho phân loại
- ✅ Xem queue và stats real-time
- ✅ Auto refresh mỗi 10 giây
- ✅ Dark theme UI

## 📋 Permissions

```json
{
  "permissions": ["activeTab", "storage"],
  "host_permissions": ["http://localhost:8080/*"]
}
```

## 🔧 Build

```bash
# Zip for distribution
zip -r xhs-collector-extension.zip xhs-collector-extension/

# Exclude development files
zip -r xhs-collector-extension.zip xhs-collector-extension/ -x "*.md" "*.git*"
```