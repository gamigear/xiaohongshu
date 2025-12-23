#!/bin/bash

echo "🚀 Deploying XHS Queue Manager..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# Check if GitHub remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ Please add GitHub remote first:"
    echo "git remote add origin https://github.com/yourusername/xhs-queue-manager.git"
    exit 1
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git add .
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
git push origin main

# Deploy to Vercel
echo "🌐 Deploying to Vercel..."
if command -v vercel &> /dev/null; then
    vercel --prod
else
    echo "❌ Vercel CLI not found. Install with: npm i -g vercel"
    echo "Then run: vercel --prod"
fi

echo "✅ Deployment complete!"
echo "🔗 Check your deployment at: https://vercel.com/dashboard"