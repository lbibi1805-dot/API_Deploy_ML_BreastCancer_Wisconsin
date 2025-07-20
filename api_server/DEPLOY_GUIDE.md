# 🌍 DEPLOYMENT GUIDE - Host API Online

## 🎯 **TL;DR - Quickest Deploy**

**⚡ Render.com (Recommended - Free):**
1. Upload code lên GitHub
2. Connect tại https://render.com  
3. Deploy với 1 click
4. URL: `https://your-app.onrender.com`

---

## 🆓 **MIỄN PHÍ OPTIONS**

### 1. 🔥 **Render.com** (Most Recommended)
**GitHub Desktop:**
1. Mở GitHub Desktop
2. File → Add Local Repository → Chọn thư mục `api_server`
3. "Create repository on GitHub.com"
4. Repository name: `knn-cancer-api`
5. Commit: "Initial commit"
6. Publish repository

**Manual Git:**
```bash
# Step 1: Push to GitHub
git init
git add .
git commit -m "KNN Cancer API"
git push origin main

# Step 2: Deploy on Render.com
# - Connect GitHub repo
# - Build: pip install -r requirements.txt  
# - Start: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

**✅ Pros:** Miễn phí, auto-deploy, custom domain, SSL
**❌ Cons:** Sleep sau 15 phút không dùng

---

### 2. 🚀 **Railway.app**
```bash
# 1 click deploy từ GitHub
# Auto-detect Python app
# Free 500 hours/month
```

**URL Example:** `https://knn-cancer-api.up.railway.app`

---

### 3. ⚡ **Vercel** (Serverless)
```bash
npm i -g vercel
vercel --prod
```

**✅ Pros:** Nhanh, không sleep, global CDN
**❌ Cons:** Serverless limits (execution time)

---

### 4. 🔵 **Heroku** 
```bash
heroku create your-app-name
git push heroku main
heroku ps:scale web=1
```

**⚠️ Note:** Heroku đã ngừng free tier từ 2022

---

## 💰 **PAID OPTIONS (Professional)**

### 1. 💧 **DigitalOcean App Platform** ($5/month)
- 1-click deploy from GitHub
- Auto-scaling
- Custom domains
- Database support

### 2. ☁️ **AWS EC2** ($3-10/month)
- Full control server
- Custom setup
- Scalable
- Requires Linux knowledge

### 3. 🌊 **Google Cloud Run** (Pay-per-use)
- Container-based
- Auto-scaling 0-1000+
- Only pay when used

---

## 🔧 **STEP-BY-STEP: Render.com Deploy**

### Step 1: Prepare Code
```bash
# Trong thư mục api_server, check files:
ls -la
# Cần có: app.py, requirements.txt, Procfile, render.yaml
```

### Step 2: GitHub Upload (GitHub Desktop)
**Cách 1: GitHub Desktop (Recommended)**
1. Mở GitHub Desktop
2. File → "Add Local Repository" → Chọn thư mục `api_server`
3. "Create a repository on GitHub.com"
   - **Repository name:** `knn-cancer-api`
   - **Description:** `KNN Breast Cancer Prediction API`
   - **Keep this code private:** ✅ (hoặc public nếu muốn)
4. Click "Create repository"
5. Commit message: `Initial commit: KNN Cancer Prediction API`
6. Click "Commit to main"
7. Click "Publish repository" (push lên GitHub)

**Cách 2: Manual Git (nếu có git)**
```bash
git init
git add .
git commit -m "Initial commit: KNN Cancer Prediction API"
git remote add origin https://github.com/USERNAME/knn-cancer-api.git
git branch -M main
git push -u origin main
```

### Step 3: Render Deploy
1. Đăng ký tại https://render.com (free)
2. Click "New +" → "Web Service"
3. Connect GitHub repository: `knn-cancer-api`
4. Settings:
   - **Name:** `knn-cancer-prediction`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
   - **Plan:** `Free`

### Step 4: Environment Variables (Optional)
```
FLASK_ENV=production
FLASK_DEBUG=0
```

### Step 5: Deploy!
- Click "Create Web Service"
- Wait 5-10 minutes
- URL: `https://knn-cancer-prediction.onrender.com`

---

## 🧪 **Test Online API**

```javascript
// Test với online URL
const API_URL = 'https://your-app.onrender.com';

const testAPI = async () => {
  // Health check
  const health = await fetch(`${API_URL}/`);
  console.log(await health.json());
  
  // Prediction test
  const prediction = await fetch(`${API_URL}/predict`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      features: [2, 1, 1, 1, 2, 1, 2, 1, 1]
    })
  });
  console.log(await prediction.json());
};

testAPI();
```

---

## 🔒 **Security & Production Tips**

### 1. Environment Variables
```bash
# Thêm vào Render/Heroku
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-secret-key-here
```

### 2. Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/predict', methods=['POST'])
@limiter.limit("10 per minute")
def predict():
    # Your prediction code
```

### 3. API Key Authentication (Optional)
```python
@app.before_request
def require_api_key():
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key != os.environ.get('API_KEY'):
        return jsonify({'error': 'Invalid API key'}), 401
```

---

## 📊 **Cost Comparison**

| Platform | Cost | Pros | Cons |
|----------|------|------|------|
| **Render** | Free | Easy, Auto-deploy, SSL | Sleep after 15min |
| **Railway** | Free 500h | Fast, No sleep | Limited hours |
| **Vercel** | Free | Global CDN, Fast | Serverless limits |
| **DigitalOcean** | $5/month | Reliable, No limits | Paid |
| **AWS EC2** | $3-10/month | Full control | Setup complexity |

---

## 🎯 **Recommended Flow**

### For Testing/Demo:
1. **Render.com** - Free, easy setup
2. Share URL: `https://your-app.onrender.com`

### For Production:
1. **DigitalOcean App Platform** - $5/month
2. Custom domain + SSL
3. Better performance

### For High Traffic:
1. **AWS EC2** with Load Balancer
2. Auto-scaling
3. Database optimization

---

## 🚀 **After Deploy - Share Your API**

### API Documentation
```
🔗 API Base URL: https://your-app.onrender.com

📡 Endpoints:
- GET  /           → Health check
- GET  /model/info → Model information  
- POST /predict    → Single prediction
- POST /predict/batch → Batch predictions

📝 Example:
curl -X POST https://your-app.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [2,1,1,1,2,1,2,1,1]}'
```

### Share với Team
- **Frontend devs:** API URL + endpoints
- **Mobile devs:** API documentation
- **Data scientists:** Model accuracy & features
- **Product team:** Demo link

---

## 🆘 **Troubleshooting Online Deploy**

### Build Failed
```bash
# Check requirements.txt có đầy đủ
# Check Python version compatibility
# Check file paths (case-sensitive on Linux)
```

### App Crashes
```bash
# Check logs trong Render dashboard
# Verify model files được upload
# Check environment variables
```

### Slow Performance
```bash
# Upgrade to paid plan
# Optimize model loading
# Add caching
# Use lighter dependencies
```

### CORS Issues
```python
# Đã có CORS support trong app.py
# Nếu vẫn lỗi, check domain whitelist
```

---

## 🎉 **Success! Your API is Live**

Sau khi deploy thành công:

✅ **API URL:** `https://your-app.onrender.com`  
✅ **React Integration:** Update API_BASE_URL  
✅ **Mobile Apps:** Use online URL  
✅ **Sharing:** Send URL to collaborators  
✅ **Monitoring:** Check Render dashboard for logs  

**Your KNN Cancer Prediction API is now accessible worldwide! 🌍**
