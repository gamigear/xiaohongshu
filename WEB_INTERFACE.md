# 🌐 XHS Queue Manager - Giao diện Web

Giao diện web để quản lý hàng đợi tải xuống Xiaohongshu một cách trực quan và dễ dàng.

## 🚀 Truy cập

- **Giao diện đầy đủ:** http://localhost:8080/
- **Dashboard đơn giản:** http://localhost:8080/dashboard
- **API Documentation:** http://localhost:8080/docs

## 📋 Tính năng

### 1. Dashboard Tổng quan
- Thống kê real-time: Pending, Done, Error, Categories
- Hoạt động gần đây
- Auto refresh mỗi 30 giây

### 2. Quản lý Hàng đợi
- Xem danh sách tất cả items
- Lọc theo trạng thái
- Xóa items pending
- Hiển thị thông tin chi tiết: URL, category, tác giả, thời gian

### 3. Thêm Link
- Form thêm link mới
- Chọn category có sẵn hoặc tạo mới
- Validation URL Xiaohongshu
- Feedback real-time

### 4. Cài đặt
- Cấu hình thư mục lưu
- Điều chỉnh delay time
- Hướng dẫn sử dụng
- API endpoints

### 5. Quản lý Categories
- Xem tất cả categories
- Thống kê số lượng mỗi category
- Tạo thư mục tự động

## 🎨 Giao diện

### Responsive Design
- Desktop: Layout 2 cột, bảng đầy đủ
- Mobile: Layout 1 cột, tối ưu touch
- Dark theme với gradient background

### Color Scheme
- **Primary:** #ff6b6b (Red)
- **Secondary:** #4ecdc4 (Teal) 
- **Info:** #74b9ff (Blue)
- **Warning:** #ffd93d (Yellow)
- **Background:** #1a1a2e → #16213e (Gradient)

### Components
- **Cards:** Rounded corners, subtle borders
- **Buttons:** Hover effects, color coding
- **Tables:** Responsive, sortable
- **Forms:** Validation, real-time feedback
- **Alerts:** Auto-dismiss, color coded

## 🔧 Tính năng kỹ thuật

### Auto Refresh
- Queue data: Mỗi 10 giây
- Dashboard: Mỗi 30 giây
- Categories: Khi cần thiết

### Error Handling
- Network errors
- API validation
- User feedback
- Graceful degradation

### Performance
- Lazy loading
- Minimal API calls
- Efficient DOM updates
- CSS animations

## 📱 Sử dụng

### 1. Thêm link mới
1. Vào tab "Thêm link"
2. Paste URL Xiaohongshu
3. Chọn category (hoặc tạo mới)
4. Click "Thêm vào hàng đợi"

### 2. Quản lý queue
1. Vào tab "Hàng đợi"
2. Xem danh sách items
3. Xóa items không cần thiết
4. Monitor trạng thái

### 3. Cấu hình hệ thống
1. Vào tab "Cài đặt"
2. Điều chỉnh thư mục lưu
3. Thay đổi delay time
4. Lưu cài đặt

### 4. Theo dõi categories
1. Vào tab "Categories"
2. Xem thống kê
3. Tạo thư mục tự động

## 🔗 API Integration

Giao diện web sử dụng REST API:

```javascript
// Get queue
GET /api/queue

// Add link
POST /api/add
{
  "url": "https://...",
  "category": "food"
}

// Update config
POST /api/config
{
  "download_path": "/path",
  "delay_seconds": 120
}

// Get categories
GET /api/categories
```

## 🎯 Shortcuts

- **F5:** Refresh trang
- **Ctrl+R:** Refresh data
- **Tab:** Navigate giữa các tabs
- **Enter:** Submit forms

## 🔧 Customization

### Themes
Có thể tùy chỉnh CSS variables:

```css
:root {
  --primary-color: #ff6b6b;
  --secondary-color: #4ecdc4;
  --background: #1a1a2e;
}
```

### Layout
Responsive breakpoints:
- Mobile: < 768px
- Tablet: 768px - 1024px  
- Desktop: > 1024px

## 🚀 Deployment

Giao diện web được serve tự động khi chạy Docker:

```bash
docker compose up -d
```

Truy cập tại: http://localhost:8080

## 📊 Monitoring

### Health Check
- API status
- Database connection
- Worker status
- Queue statistics

### Logs
- Browser console
- Network requests
- Error tracking
- Performance metrics