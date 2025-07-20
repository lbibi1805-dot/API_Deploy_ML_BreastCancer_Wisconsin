# 📱 GITHUB DESKTOP DEPLOYMENT GUIDE

**Hướng dẫn deploy API lên online với GitHub Desktop (không cần command line)**

## 🎯 **TL;DR - Quick Steps**
1. GitHub Desktop → Add Local Repository → Chọn thư mục `api_server`
2. Create repository → `knn-cancer-api`
3. Commit → Publish repository  
4. Render.com → Connect GitHub → Deploy
5. ✅ API online tại `https://your-app.onrender.com`

---

## 📂 **STEP 1: Setup GitHub Desktop**

### Tải GitHub Desktop (nếu chưa có)
- Download tại: https://desktop.github.com/
- Install và đăng nhập GitHub account

### Add Repository
1. **Mở GitHub Desktop**
2. **File** → **"Add Local Repository"**
3. **Choose** thư mục: `e:\ML_BreastCancer_Wisonsin_Original\ML_BreastCancerWisconsin_Prediction\api_server`
4. Click **"Add Repository"**

---

## 🌐 **STEP 2: Create GitHub Repository**

### Nếu thư mục chưa có git:
1. GitHub Desktop sẽ hiện: **"Create a repository"**
2. Click **"Create a repository on GitHub.com"**

### Repository Settings:
```
Repository name: knn-cancer-api
Description: KNN Breast Cancer Prediction API
Local path: (đã có sẵn)
Keep this code private: ✅ (hoặc public)
```

3. Click **"Create repository"**

---

## 💾 **STEP 3: Commit & Push**

### Initial Commit:
1. GitHub Desktop sẽ hiện tất cả files
2. **Summary:** `Initial commit: KNN Cancer API`
3. **Description:** `Flask API server for KNN breast cancer prediction`
4. Click **"Commit to main"**

### Publish to GitHub:
1. Click **"Publish repository"** (button xanh to)
2. Đợi upload hoàn thành
3. ✅ Repository đã có trên GitHub!

---

## 🚀 **STEP 4: Deploy on Render.com**

### 4.1 Đăng ký Render
1. Truy cập: https://render.com
2. **Sign up** với GitHub account
3. **Authorize** Render to access GitHub

### 4.2 Create Web Service
1. Click **"New +"** → **"Web Service"**
2. **Connect a repository** → Chọn **"knn-cancer-api"**
3. Click **"Connect"**

### 4.3 Configure Service
```
Name: knn-cancer-prediction
Environment: Python 3
Region: Oregon (US West)
Branch: main
Root Directory: (để trống)

Build Command: pip install -r requirements.txt
Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT app:app

Plan: Free
```

4. Click **"Create Web Service"**

### 4.4 Wait for Deployment
- Render sẽ build app (5-10 phút)
- Status: **"Live"** = thành công
- URL: `https://knn-cancer-prediction.onrender.com`

---

## 🧪 **STEP 5: Test Your API**

### Health Check
```
https://knn-cancer-prediction.onrender.com/
```

### Test Prediction
```javascript
fetch('https://knn-cancer-prediction.onrender.com/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    features: [2, 1, 1, 1, 2, 1, 2, 1, 1]
  })
});
```

---

## 🔄 **Update Your API (sau này)**

### Khi cần update code:
1. **Edit** files trong local folder
2. **GitHub Desktop** sẽ hiện changes
3. **Commit** với message mô tả thay đổi
4. **Push origin** (sync button)
5. **Render** sẽ tự động deploy lại

---

## ⚠️ **Troubleshooting**

### Build Failed trên Render:
1. Check **logs** trong Render dashboard
2. Verify `requirements.txt` có đầy đủ packages
3. Ensure Python version compatibility

### GitHub Desktop issues:
1. **Repository not found:** Check repository đã public/private đúng
2. **Permission denied:** Re-authorize GitHub connection
3. **Large files:** GitHub có limit 100MB per file

### Model không load:
1. Ensure thư mục `Models/` có KNN model files
2. Check file paths trong code
3. Verify model files không corrupted

---

## 🎉 **Success Checklist**

- ✅ GitHub Desktop repository created
- ✅ Code pushed to GitHub successfully  
- ✅ Render service deployed
- ✅ API responding at online URL
- ✅ Health check returns "healthy"
- ✅ Prediction endpoint works
- ✅ CORS enabled for web apps

---

## 📱 **Share Your API**

### With Frontend Developers:
```javascript
const API_URL = 'https://knn-cancer-prediction.onrender.com';
// Use this URL instead of localhost:5000
```

### With Mobile Developers:
```
Base URL: https://knn-cancer-prediction.onrender.com
Documentation: See README.md for endpoints
```

### With Team:
- **Demo URL:** `https://knn-cancer-prediction.onrender.com`
- **API Docs:** Share `SETUP_GUIDE.md`
- **Source Code:** `https://github.com/yourusername/knn-cancer-api`

---

## 🔒 **Security Notes**

- API deployed on free Render plan
- Auto-sleep after 15 minutes inactive
- CORS enabled for web browsers
- Input validation for all endpoints
- No API key required (research use)

---

## 🚀 **Next Steps**

### For Production Use:
1. **Upgrade** to Render paid plan ($7/month)
2. **Add** custom domain
3. **Enable** monitoring & alerts
4. **Implement** API key authentication

### For Development:
1. **Clone** repository on other machines
2. **Collaborate** với team members
3. **Version control** với git branches
4. **CI/CD** pipeline với GitHub Actions

**🎉 Your KNN Cancer Prediction API is now live and accessible worldwide!**
