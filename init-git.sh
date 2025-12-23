#!/bin/bash

echo "🔧 Initializing Git repository for XHS Queue Manager..."

# Check if already a git repo
if [ -d ".git" ]; then
    echo "✅ Git repository already exists"
else
    echo "📦 Initializing new Git repository..."
    git init
fi

# Add all files
echo "📁 Adding files to Git..."
git add .

# Initial commit
echo "💾 Creating initial commit..."
git commit -m "feat: Initial commit - XHS Queue Manager

- Chrome extension for quick link adding
- FastAPI backend with PostgreSQL
- Web interface for queue management
- Auto download worker with delay
- Category system for organization
- Real-time dashboard and stats
- Docker deployment ready
- Vercel deployment configured" || echo "No changes to commit"

echo "🎯 Next steps:"
echo "1. Create GitHub repository: https://github.com/new"
echo "2. Add remote: git remote add origin https://github.com/yourusername/xhs-queue-manager.git"
echo "3. Push: git push -u origin main"
echo "4. Deploy: ./deploy.sh"

echo "✅ Git initialization complete!"