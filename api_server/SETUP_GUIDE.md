# 🚀 KNN BREAST CANCER PREDICTION API

**Flask REST API server để deploy model KNN breast cancer prediction lên online cho các dự án React, Express, hoặc bất kỳ web framework nào khác.**

## 📁 Cấu trúc thư mục
```
api_server/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── start_server.bat         # Windows batch file để khởi động server
├── test_server.bat          # Windows batch file để test API
├── test_api.py              # API test client
├── react_example.py         # React component example
└── README.md               # Hướng dẫn này
```

## 🔧 Cài đặt và khởi động

### Cách 1: Sử dụng batch file (Windows)
```bash
# Khởi động server
double-click start_server.bat
```

### Cách 2: Manual setup
```bash
# 1. Cài đặt dependencies
cd api_server
pip install -r requirements.txt

# 2. Khởi động server
python app.py
```

Server sẽ chạy tại: **http://localhost:5000**

## 🧪 Testing API

### Cách 1: Sử dụng batch file
```bash
double-click test_server.bat
```

### Cách 2: Manual testing
```bash
python test_api.py
```

### Cách 3: curl commands
```bash
# Health check
curl http://localhost:5000/

# Model info
curl http://localhost:5000/model/info

# Single prediction
curl -X POST http://localhost:5000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"features\": [2, 1, 1, 1, 2, 1, 2, 1, 1]}"
```

## 📡 API Endpoints

### 🔍 Health Check
```
GET /
```

### 📊 Model Information
```
GET /model/info
```

### 🎯 Single Prediction
```
POST /predict
Content-Type: application/json

{
  "features": [2, 1, 1, 1, 2, 1, 2, 1, 1]
}
```

### 📊 Batch Prediction
```
POST /predict/batch
Content-Type: application/json

{
  "samples": [
    [2, 1, 1, 1, 2, 1, 2, 1, 1],
    [8, 7, 8, 7, 6, 9, 7, 8, 3]
  ]
}
```

## 🌐 Integration với Web Apps

### React Integration
```javascript
// Gọi API từ React component
const predictCancer = async (features) => {
  const response = await fetch('http://localhost:5000/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      features: features
    })
  });
  
  return await response.json();
};

// Usage
const features = [2, 1, 1, 1, 2, 1, 2, 1, 1];
const result = await predictCancer(features);
console.log(result.prediction.diagnosis); // "Benign" or "Malignant"
```

### Express.js Proxy
```javascript
const express = require('express');
const axios = require('axios');
const app = express();

app.post('/api/cancer-prediction', async (req, res) => {
  try {
    const response = await axios.post('http://localhost:5000/predict', req.body);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Prediction failed' });
  }
});
```

### Vue.js Integration
```javascript
// Vue component method
async makePrediction(features) {
  try {
    const response = await this.$http.post('http://localhost:5000/predict', {
      features: features
    });
    this.result = response.data;
  } catch (error) {
    console.error('Prediction error:', error);
  }
}
```

## 📊 Input Format

**Tất cả 9 features phải là số từ 1-10:**

1. **clump_thickness**: Độ dày khối tế bào (1-10)
2. **uniform_cell_size**: Kích thước đồng đều tế bào (1-10)  
3. **uniform_cell_shape**: Hình dạng đồng đều tế bào (1-10)
4. **marginal_adhesion**: Độ bám dính rìa (1-10)
5. **single_epithelial_cell_size**: Kích thước tế bào biểu mô đơn (1-10)
6. **bare_nuclei**: Nhân trần (1-10)
7. **bland_chromatin**: Chất nhiễm sắc nhạt (1-10)
8. **normal_nucleoli**: Nhân con bình thường (1-10)
9. **mitoses**: Phân bào (1-10)

## 📝 Response Format

```json
{
  "status": "success",
  "prediction": {
    "diagnosis": "Benign",
    "confidence": 0.667,
    "risk_level": "Low",
    "raw_prediction": 2,
    "probabilities": {
      "benign": 0.667,
      "malignant": 0.333
    }
  },
  "medical_interpretation": {
    "interpretation": "The tissue sample shows characteristics consistent with benign (non-cancerous) cells.",
    "recommendation": "Continue regular screening as recommended by healthcare provider.",
    "disclaimer": "This prediction is for research purposes only..."
  },
  "input_features": {
    "clump_thickness": 2,
    "uniform_cell_size": 1,
    ...
  },
  "timestamp": "2025-07-20T10:04:19.123456"
}
```

## 🌍 HOST ONLINE - Deploy lên Internet

### 🆓 **MIỄN PHÍ - Render.com (Recommended)**

**Bước 1:** Upload code lên GitHub
```bash
git init
git add .
git commit -m "KNN Cancer Prediction API"
git remote add origin https://github.com/yourusername/knn-cancer-api.git
git push -u origin main
```

**Bước 2:** Deploy trên Render
1. Đăng ký tại https://render.com
2. Connect GitHub repository  
3. Chọn "Web Service"
4. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
   - **Environment**: Python 3
   - **Plan**: Free

**Bước 3:** Tạo file `render.yaml` (optional)
```yaml
services:
  - type: web
    name: knn-cancer-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
    envVars:
      - key: FLASK_ENV
        value: production
```

**Result:** API sẽ có URL như `https://your-app-name.onrender.com`

---

### 🆓 **Heroku (Miễn phí với giới hạn)**

**Bước 1:** Tạo `Procfile`
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

**Bước 2:** Deploy
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
```

**Bước 3:** Scale app
```bash
heroku ps:scale web=1
```

**Result:** API tại `https://your-app-name.herokuapp.com`

---

### 🆓 **Railway.app**

**Bước 1:** Connect GitHub tại https://railway.app
**Bước 2:** Deploy với 1 click
**Bước 3:** Environment variables:
```
PORT=5000
FLASK_ENV=production
```

**Result:** Auto-generated URL như `https://your-app.up.railway.app`

---

### 🆓 **Vercel (Serverless)**

**Bước 1:** Tạo `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

**Bước 2:** Deploy
```bash
npm i -g vercel
vercel --prod
```

---

### 💰 **DigitalOcean App Platform**

**Bước 1:** Connect GitHub
**Bước 2:** App Spec:
```yaml
name: knn-cancer-api
services:
- name: api
  source_dir: /
  github:
    repo: yourusername/knn-cancer-api
    branch: main
  run_command: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
```

**Cost:** ~$5/month

---

### 💰 **AWS EC2 (Full Control)**

**Bước 1:** Launch EC2 instance (Ubuntu)
**Bước 2:** SSH và setup
```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@your-instance-ip

# Install Python & dependencies
sudo apt update
sudo apt install python3 python3-pip nginx
pip3 install -r requirements.txt

# Run with systemd
sudo nano /etc/systemd/system/knn-api.service
```

**Systemd service file:**
```ini
[Unit]
Description=KNN Cancer API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/knn-cancer-api
ExecStart=/usr/bin/python3 -m gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔒 Production Deployment (Local/VPS)

### Gunicorn (Linux/Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Environment Variables
```bash
# Development
export FLASK_ENV=development
export FLASK_DEBUG=1

# Production  
export FLASK_ENV=production
export FLASK_DEBUG=0
```

## ⚠️ Lưu ý quan trọng

- **Chỉ dành cho nghiên cứu**: API này không thay thế chẩn đoán y tế chuyên nghiệp
- **CORS enabled**: API hỗ trợ cross-origin requests cho web apps
- **Error handling**: API trả về error messages chi tiết
- **Model validation**: Kiểm tra tự động model có tải được không
- **Input validation**: Validate tất cả input features (1-10 range)

## 🎯 Sample Test Cases

```javascript
// Benign case (expected: Benign)
const benignCase = [2, 1, 1, 1, 2, 1, 2, 1, 1];

// Malignant case (expected: Malignant)  
const malignantCase = [8, 7, 8, 7, 6, 9, 7, 8, 3];

// Borderline case
const borderlineCase = [5, 3, 4, 3, 3, 5, 4, 4, 1];
```

## 🔗 Links và Resources

- **Model accuracy**: ~97.08% trên test set
- **Algorithm**: K-Nearest Neighbors (k=3)
- **Dataset**: Wisconsin Breast Cancer Dataset
- **Flask docs**: https://flask.palletsprojects.com/
- **React integration**: Xem file `react_example.py`

## 📞 Troubleshooting

### API Server không start được
1. Check Python version (≥3.7)
2. Install dependencies: `pip install -r requirements.txt`
3. Check port 5000 không bị chiếm

### Model không load được  
1. Đảm bảo file KNN model tồn tại trong `../Models/`
2. Check file permissions
3. Verify model file không corrupted

### CORS issues từ browser
API đã enable CORS mặc định. Nếu vẫn có vấn đề:
```javascript
// Thêm mode: 'cors' vào fetch request
fetch('http://localhost:5000/predict', {
  method: 'POST',
  mode: 'cors',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({features: [...]}),
});
```

## 🎉 Ready to Use!

API server đã sẵn sàng để integrate với:
- ✅ React applications
- ✅ Vue.js applications  
- ✅ Express.js backends
- ✅ Next.js full-stack apps
- ✅ Mobile apps (React Native, Flutter)
- ✅ Desktop apps (Electron)
- ✅ Bất kỳ platform nào support HTTP requests
