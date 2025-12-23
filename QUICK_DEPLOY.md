# ⚡ Quick Deploy Guide

Deploy XHS Queue Manager trong 5 phút!

## 🚀 Bước 1: GitHub

```bash
# 1. Tạo repo mới tại: https://github.com/new
# Tên: xhs-queue-manager

# 2. Add remote và push
git remote add origin https://github.com/YOURUSERNAME/xhs-queue-manager.git
git push -u origin main
```

## 🌐 Bước 2: Database (Neon)

1. Vào [neon.tech](https://neon.tech) → Sign up
2. Create new project → Copy connection string
3. Format: `postgresql://user:pass@host:port/db?sslmode=require`

## ☁️ Bước 3: Vercel

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel

# 4. Add environment variable
# Vào Vercel dashboard → Settings → Environment Variables
# DATABASE_URL = your-neon-connection-string

# 5. Redeploy
vercel --prod
```

## 🔧 Bước 4: Update Extension

Sửa file `xhs-collector-extension/popup.js`:

```javascript
// Thay localhost bằng Vercel URL
const API_BASE = 'https://your-app.vercel.app/api';
```

## ✅ Bước 5: Test

1. **Web**: https://your-app.vercel.app
2. **API**: https://your-app.vercel.app/api/queue
3. **Dashboard**: https://your-app.vercel.app/dashboard

## 🎯 Done!

- ✅ GitHub repository
- ✅ PostgreSQL database  
- ✅ Vercel deployment
- ✅ Web interface live
- ✅ Chrome extension ready

## 🔗 URLs

Replace `your-app` với tên Vercel app của bạn:

- **Main**: https://your-app.vercel.app
- **Dashboard**: https://your-app.vercel.app/dashboard  
- **API Docs**: https://your-app.vercel.app/docs
- **GitHub**: https://github.com/yourusername/xhs-queue-manager

## 🆘 Troubleshooting

**Database connection failed?**
- Check connection string format
- Ensure `?sslmode=require` at the end

**API not working?**
- Check Vercel function logs
- Verify environment variables

**Extension not connecting?**
- Update API_BASE URL in popup.js
- Check CORS settings