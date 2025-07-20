# KNN Breast Cancer Prediction API

Flask-based REST API server để serve model KNN cho web applications.

**🎯 Model Performance:**
- **Algorithm**: K-Nearest Neighbors (k=3)
- **Test Accuracy**: 97.08%
- **F1-Score**: 97.09%
- **Dataset**: Wisconsin Breast Cancer Dataset (699 samples)

**🔧 Technical Details:**
- **Framework**: Flask + gunicorn
- **CORS**: Enabled for React/Express integration
- **Feature Scaling**: StandardScaler applied (CRITICAL for correct predictions)
- **Input Format**: Raw features (1-10 range) → Auto-scaled internally
- **Output**: JSON với medical interpretation

## 🚀 Quick Start

**Production URL:** https://api-deploy-ml-breastcancer-wisconsin.onrender.com

```bash
# Test API
curl https://api-deploy-ml-breastcancer-wisconsin.onrender.com/

# Benign prediction
curl -X POST https://api-deploy-ml-breastcancer-wisconsin.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [2, 1, 1, 1, 2, 1, 2, 1, 1]}'

# Malignant prediction  
curl -X POST https://api-deploy-ml-breastcancer-wisconsin.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8, 7, 8, 7, 6, 9, 7, 8, 3]}'
```

**Local Development:**
```bash
pip install -r requirements.txt
python app.py
# Server: http://localhost:5000
```

### 1. Cài đặt dependencies
```bash
cd api_server
pip install -r requirements.txt
```

### 2. Chạy server
```bash
python app.py
```

Server sẽ chạy tại: `http://localhost:5000`

## 📡 API Endpoints

### Health Check
```
GET /
```
Response:
```json
{
  "status": "healthy",
  "service": "KNN Breast Cancer Prediction API",
  "model_loaded": true,
  "timestamp": "2025-07-20T10:04:19.123456"
}
```

### Model Information
```
GET /model/info
```
Response:
```json
{
  "status": "success",
  "model_info": {
    "algorithm": "K-Nearest Neighbors",
    "k_value": 3,
    "accuracy": 0.9708,
    "f1_score": 0.9655,
    "features": [
      "clump_thickness",
      "uniform_cell_size",
      "uniform_cell_shape",
      "marginal_adhesion",
      "single_epithelial_cell_size",
      "bare_nuclei",
      "bland_chromatin",
      "normal_nucleoli",
      "mitoses"
    ],
    "feature_range": "1-10 (scaled)",
    "classes": {
      "2": "Benign",
      "4": "Malignant"
    }
  }
}
```

### Single Prediction
```
POST /predict
Content-Type: application/json

{
  "features": [2, 1, 1, 1, 2, 1, 2, 1, 1]
}
```

Response:
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
    "disclaimer": "This prediction is for research purposes only and should not replace professional medical diagnosis."
  },
  "input_features": {
    "clump_thickness": 2,
    "uniform_cell_size": 1,
    "uniform_cell_shape": 1,
    "marginal_adhesion": 1,
    "single_epithelial_cell_size": 2,
    "bare_nuclei": 1,
    "bland_chromatin": 2,
    "normal_nucleoli": 1,
    "mitoses": 1
  },
  "timestamp": "2025-07-20T10:04:19.123456"
}
```

### Batch Predictions
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

Response:
```json
{
  "status": "success",
  "batch_size": 2,
  "results": [
    {
      "sample_index": 1,
      "diagnosis": "Benign",
      "confidence": 0.667,
      "raw_prediction": 2,
      "probabilities": {
        "benign": 0.667,
        "malignant": 0.333
      }
    },
    {
      "sample_index": 2,
      "diagnosis": "Malignant",
      "confidence": 1.0,
      "raw_prediction": 4,
      "probabilities": {
        "benign": 0.0,
        "malignant": 1.0
      }
    }
  ],
  "timestamp": "2025-07-20T10:04:19.123456"
}
```

## 🌐 Sử dụng với React/Express

### React Example (JavaScript)
```javascript
// Gọi API từ React
const predictCancer = async (features) => {
  try {
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        features: features
      })
    });
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Prediction error:', error);
    throw error;
  }
};

// Usage
const features = [2, 1, 1, 1, 2, 1, 2, 1, 1];
predictCancer(features)
  .then(result => {
    console.log('Diagnosis:', result.prediction.diagnosis);
    console.log('Confidence:', result.prediction.confidence);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

### Express.js Proxy Example
```javascript
// Express server để proxy requests
const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
app.use(cors());
app.use(express.json());

// Proxy endpoint
app.post('/api/cancer-prediction', async (req, res) => {
  try {
    const response = await axios.post('http://localhost:5000/predict', req.body);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ 
      error: 'Prediction service unavailable',
      details: error.message 
    });
  }
});

app.listen(3001, () => {
  console.log('Proxy server running on port 3001');
});
```

## 🔧 Production Deployment

### Sử dụng Gunicorn
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

## 📊 Features Input Format

**Input Features (9 features, range 1-10):**
```javascript
{
  "features": [
    clump_thickness,        // 1-10
    uniform_cell_size,      // 1-10  
    uniform_cell_shape,     // 1-10
    marginal_adhesion,      // 1-10
    single_epithelial_cell_size, // 1-10
    bare_nuclei,           // 1-10
    bland_chromatin,       // 1-10
    normal_nucleoli,       // 1-10
    mitoses               // 1-10
  ]
}
```

**✅ Valid Examples:**
```json
// Benign case
{"features": [2, 1, 1, 1, 2, 1, 2, 1, 1]}

// Malignant case  
{"features": [8, 7, 8, 7, 6, 9, 7, 8, 3]}

// Borderline case
{"features": [5, 4, 4, 5, 7, 10, 3, 2, 1]}
```

**⚠️ Important Notes:**
- **Feature Scaling**: API tự động scale input từ (1-10) về training format
- **Range Validation**: Tất cả features phải trong khoảng 1-10
- **Count Validation**: Phải có đúng 9 features
- **Type Validation**: Chỉ chấp nhận numbers (int/float)

Tất cả features phải là số từ 1-10:

1. **clump_thickness**: Độ dày của khối tế bào (1-10)
2. **uniform_cell_size**: Kích thước đồng đều của tế bào (1-10)
3. **uniform_cell_shape**: Hình dạng đồng đều của tế bào (1-10)
4. **marginal_adhesion**: Độ bám dính ở rìa (1-10)
5. **single_epithelial_cell_size**: Kích thước tế bào biểu mô đơn (1-10)
6. **bare_nuclei**: Nhân trần (1-10)
7. **bland_chromatin**: Chất nhiễm sắc nhạt (1-10)
8. **normal_nucleoli**: Nhân con bình thường (1-10)
9. **mitoses**: Phân bào (1-10)

## ⚠️ Lưu ý quan trọng

### 🔧 Feature Scaling (CRITICAL)
- **Model Training**: KNN được train với StandardScaler (mean=0, std=1)
- **API Input**: Nhận raw data (1-10) và tự động scale
- **Fixed Issue**: Trước đây API không scale → luôn predict Malignant
- **Current Fix**: API áp dụng scaling chính xác → predictions đúng

### 🎯 Model Accuracy
- **Algorithm**: K-Nearest Neighbors with k=3
- **Training Accuracy**: 97.25%
- **Test Accuracy**: 97.08%
- **Cross-validation**: Stable performance across folds
- **Dataset Split**: 80% train, 20% test (stratified)

### 🌐 Production Deployment
- **Platform**: Render.com (free tier)
- **URL**: https://api-deploy-ml-breastcancer-wisconsin.onrender.com
- **Auto-deploy**: Linked to GitHub repository
- **Health Check**: GET / endpoint để kiểm tra status
- **CORS**: Enabled for cross-origin requests

- API này chỉ dành cho mục đích nghiên cứu
- Không thay thế chẩn đoán y tế chuyên nghiệp
- Model được train trên Wisconsin Breast Cancer Dataset
- Luôn kiểm tra tính khả dụng của model trước khi deploy production

## 🔍 Testing API

### Postman Test Cases

**1. Health Check:**
```
GET https://api-deploy-ml-breastcancer-wisconsin.onrender.com/
```

**2. Benign Prediction:**
```json
POST /predict
{
  "features": [2, 1, 1, 1, 2, 1, 2, 1, 1]
}
// Expected: "Benign"
```

**3. Malignant Prediction:**
```json
POST /predict  
{
  "features": [8, 7, 8, 7, 6, 9, 7, 8, 3]
}
// Expected: "Malignant"
```

**4. Batch Prediction:**
```json
POST /predict/batch
{
  "samples": [
    [2, 1, 1, 1, 2, 1, 2, 1, 1],
    [8, 7, 8, 7, 6, 9, 7, 8, 3],
    [5, 4, 4, 5, 7, 10, 3, 2, 1]
  ]
}
```

**5. Error Test Cases:**
```json
// Invalid range
{"features": [15, 1, 1, 1, 2, 1, 2, 1, 1]}

// Wrong count
{"features": [1, 2, 3]}

// Missing field
{"data": [1, 2, 3, 4, 5, 6, 7, 8, 9]}
```

```bash
# Test health check
curl http://localhost:5000/

# Test prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [2, 1, 1, 1, 2, 1, 2, 1, 1]}'

# Test model info
curl http://localhost:5000/model/info
```
