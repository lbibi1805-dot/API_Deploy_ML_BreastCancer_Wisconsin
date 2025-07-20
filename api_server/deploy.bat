@echo off
echo 🚀 KNN Cancer API - GitHub Desktop Deploy Guide
echo ==============================================

echo.
echo 📁 Current directory: %CD%
echo.
echo 🎯 STEP-BY-STEP DEPLOYMENT GUIDE:
echo.
echo 📂 Step 1: GitHub Desktop Setup
echo    1. Open GitHub Desktop
echo    2. File → "Add Local Repository"
echo    3. Choose this folder: %CD%
echo    4. Click "Create a repository on GitHub.com"
echo.
echo ⚙️  Step 2: Repository Settings
echo    - Repository name: knn-cancer-api
echo    - Description: KNN Breast Cancer Prediction API
echo    - Keep private: ✅ (or public if you want)
echo    - Click "Create repository"
echo.
echo 💾 Step 3: Commit and Push
echo    - Commit message: "Initial commit: KNN Cancer API"
echo    - Click "Commit to main"
echo    - Click "Publish repository"
echo.
echo 🌐 Step 4: Deploy on Render.com
echo    1. Go to https://render.com (sign up free)
echo    2. Click "New +" → "Web Service"
echo    3. Connect GitHub → Select "knn-cancer-api"
echo    4. Settings:
echo       - Name: knn-cancer-prediction
echo       - Environment: Python 3
echo       - Build Command: pip install -r requirements.txt
echo       - Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
echo       - Plan: Free
echo    5. Click "Create Web Service"
echo    6. Wait 5-10 minutes for deployment
echo.
echo 🎉 Your API will be live at:
echo    https://knn-cancer-prediction.onrender.com
echo.
echo 📋 Files in this directory:
dir /b
echo.
echo ✅ All deployment files are ready!
echo    Just follow the GitHub Desktop steps above.
echo.
pause
