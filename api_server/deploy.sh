#!/bin/bash

echo "🚀 KNN Cancer API - Auto Deploy Script"
echo "====================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}📁 Initializing git repository...${NC}"
    git init
fi

# Check if remote exists
if ! git remote | grep -q "origin"; then
    echo -e "${RED}❌ No git remote found!${NC}"
    echo "Please add your GitHub repository:"
    echo "git remote add origin https://github.com/USERNAME/REPO.git"
    exit 1
fi

echo -e "${GREEN}✅ Git repository ready${NC}"

# Add all files
echo -e "${YELLOW}📦 Adding files to git...${NC}"
git add .

# Commit with timestamp
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
echo -e "${YELLOW}💾 Committing changes...${NC}"
git commit -m "Deploy KNN Cancer API - $timestamp"

# Push to GitHub
echo -e "${YELLOW}⬆️  Pushing to GitHub...${NC}"
git push origin main

echo -e "${GREEN}🎉 Code pushed to GitHub successfully!${NC}"
echo ""
echo "Next steps for deployment:"
echo "1. Go to https://render.com"
echo "2. Connect your GitHub repository"
echo "3. Create new Web Service"
echo "4. Use these settings:"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn -w 4 -b 0.0.0.0:\$PORT app:app"
echo "   - Environment: Python 3"
echo "   - Plan: Free"
echo ""
echo "Your API will be available at: https://your-app-name.onrender.com"
