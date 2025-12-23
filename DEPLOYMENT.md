# 🚀 Deployment Guide

Hướng dẫn deploy XHS Queue Manager lên GitHub và Vercel.

## 📋 Chuẩn bị

### 1. Tài khoản cần thiết
- [GitHub](https://github.com) account
- [Vercel](https://vercel.com) account  
- [Neon](https://neon.tech) hoặc PostgreSQL database

### 2. Tools cần cài
```bash
# Git
git --version

# Node.js (cho Vercel CLI)
node --version
npm --version

# Vercel CLI
npm i -g vercel
```

## 🔧 Setup Database

### Option 1: Neon (Khuyến nghị)
1. Tạo account tại [neon.tech](https://neon.tech)
2. Tạo database mới
3. Copy connection string
4. Format: `postgresql://user:pass@host:port/db?sslmode=require`

### Option 2: Railway
1. Tạo account tại [railway.app](https://railway.app)
2. Deploy PostgreSQL service
3. Copy connection string

### Option 3: Supabase
1. Tạo project tại [supabase.com](https://supabase.com)
2. Vào Settings → Database
3. Copy connection string

## 📤 Deploy lên GitHub

### 1. Tạo Repository
```bash
# Tạo repo trên GitHub với tên: xhs-queue-manager
# Sau đó clone về local hoặc init git

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/xhs-queue-manager.git
git push -u origin main
```

### 2. Cấu trúc files
```
xhs-queue-manager/
├── .github/workflows/deploy.yml
├── api/index.py
├── xhs-queue-server/
├── xhs-collector-extension/
├── vercel.json
├── requirements.txt
├── package.json
├── README.md
└── LICENSE
```

## 🌐 Deploy lên Vercel

### Method 1: Vercel CLI (Khuyến nghị)

```bash
# Login Vercel
vercel login

# Deploy
vercel

# Production deploy
vercel --prod
```

### Method 2: GitHub Integration

1. Vào [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import từ GitHub repository
4. Configure settings:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: `echo "No build required"`
   - **Output Directory**: `xhs-queue-server/static`

### Method 3: Manual Upload

1. Zip toàn bộ project
2. Upload lên Vercel dashboard
3. Configure environment variables

## ⚙️ Environment Variables

Trong Vercel dashboard → Settings → Environment Variables:

```bash
# Database (Required)
DATABASE_URL=postgresql://user:pass@host:port/db?sslmode=require

# XHS API (Optional - for worker)
XHS_API_URL=https://your-xhs-api.herokuapp.com/xhs/detail

# Other configs
DELAY_SECONDS=120
```

## 🔧 Vercel Configuration

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "xhs-queue-server/server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "xhs-queue-server/server.py"
    },
    {
      "src": "/(.*)",
      "dest": "xhs-queue-server/static/index.html"
    }
  ]
}
```

## 🤖 GitHub Actions (Optional)

Auto deploy khi push code:

1. Tạo Vercel token: [vercel.com/account/tokens](https://vercel.com/account/tokens)
2. Thêm secrets trong GitHub repo:
   - `VERCEL_TOKEN`: Your Vercel token
   - `ORG_ID`: Vercel org ID
   - `PROJECT_ID`: Vercel project ID

## 🧪 Testing Deployment

### 1. Check URLs
```bash
# Web interface
curl https://your-app.vercel.app/

# API health
curl https://your-app.vercel.app/api/queue

# Dashboard
curl https://your-app.vercel.app/dashboard
```

### 2. Test functionality
1. Open web interface
2. Try adding a link
3. Check database connection
4. Verify API responses

## 🔍 Troubleshooting

### Common Issues

**1. Database connection failed**
```bash
# Check connection string format
DATABASE_URL=postgresql://user:pass@host:port/db?sslmode=require

# Test connection
python -c "import psycopg2; psycopg2.connect('your-connection-string')"
```

**2. Static files not loading**
```bash
# Check vercel.json routes
# Ensure static files are in correct directory
```

**3. API endpoints not working**
```bash
# Check function timeout (max 30s on free plan)
# Verify Python dependencies in requirements.txt
```

**4. CORS issues**
```python
# Already configured in server.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Debug Commands

```bash
# Local testing
cd xhs-queue-server
python server.py

# Check logs
vercel logs your-deployment-url

# Function info
vercel inspect your-deployment-url
```

## 📊 Monitoring

### 1. Vercel Analytics
- Enable in project settings
- Monitor performance
- Track usage

### 2. Database monitoring
- Check connection pool
- Monitor query performance
- Set up alerts

### 3. Error tracking
- Check Vercel function logs
- Monitor API response times
- Set up health checks

## 🔄 Updates

### Deploy updates
```bash
# Make changes
git add .
git commit -m "Update: description"
git push origin main

# Auto deploy via GitHub Actions
# Or manual: vercel --prod
```

### Rollback
```bash
# List deployments
vercel ls

# Promote previous deployment
vercel promote deployment-url
```

## 🎯 Production Checklist

- [ ] Database connection working
- [ ] Environment variables set
- [ ] API endpoints responding
- [ ] Static files loading
- [ ] CORS configured
- [ ] Error handling working
- [ ] Performance optimized
- [ ] Security headers set
- [ ] Monitoring enabled
- [ ] Backup strategy planned

## 🔗 Useful Links

- [Vercel Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [FastAPI on Vercel](https://vercel.com/guides/deploying-fastapi-with-vercel)
- [PostgreSQL on Neon](https://neon.tech/docs/get-started-with-neon/signing-up)
- [GitHub Actions](https://docs.github.com/en/actions)