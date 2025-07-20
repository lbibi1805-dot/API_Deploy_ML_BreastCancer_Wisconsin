# 🏥 Breast Cancer Prediction API

**Live Production API for KNN Breast Cancer Prediction**

[![API](https://img.shields.io/badge/API-Live-brightgreen.svg)](https://api-deploy-ml-breastcancer-wisconsin.onrender.com)
[![Accuracy](https://img.shields.io/badge/Accuracy-97.08%25-blue.svg)]()
[![Algorithm](https://img.shields.io/badge/Algorithm-KNN%20(k=3)-orange.svg)]()

## 🚀 Quick Start

**Production URL:** https://api-deploy-ml-breastcancer-wisconsin.onrender.com

```bash
# Health check
curl https://api-deploy-ml-breastcancer-wisconsin.onrender.com/

# Make prediction (Benign case)
curl -X POST https://api-deploy-ml-breastcancer-wisconsin.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [2, 1, 1, 1, 2, 1, 2, 1, 1]}'

# Make prediction (Malignant case)  
curl -X POST https://api-deploy-ml-breastcancer-wisconsin.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8, 7, 8, 7, 6, 9, 7, 8, 3]}'
```

## 📡 API Endpoints

### 1. Health Check
```
GET /
```
**Response:**
```json
{
  "status": "healthy",
  "service": "KNN Breast Cancer Prediction API",
  "model_loaded": true,
  "timestamp": "2025-07-20T10:04:19.123456"
}
```

### 2. Model Information
```
GET /model/info
```
**Response:**
```json
{
  "status": "success",
  "model_info": {
    "algorithm": "K-Nearest Neighbors",
    "k_value": 3,
    "accuracy": 0.9708,
    "f1_score": 0.9709,
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
    ]
  }
}
```

### 3. Single Prediction
```
POST /predict
```
**Request:**
```json
{
  "features": [2, 1, 1, 1, 2, 1, 2, 1, 1]
}
```
**Response:**
```json
{
  "status": "success",
  "prediction": {
    "diagnosis": "Benign",
    "confidence": 0.667,
    "risk_level": "Low",
    "probabilities": {
      "benign": 0.667,
      "malignant": 0.333
    }
  },
  "medical_interpretation": {
    "interpretation": "The tissue sample shows characteristics consistent with benign (non-cancerous) cells.",
    "recommendation": "Continue regular screening as recommended by healthcare provider.",
    "disclaimer": "This prediction is for research purposes only and should not replace professional medical diagnosis."
  }
}
```

### 4. Batch Predictions
```
POST /predict/batch
```
**Request:**
```json
{
  "samples": [
    [2, 1, 1, 1, 2, 1, 2, 1, 1],
    [8, 7, 8, 7, 6, 9, 7, 8, 3],
    [5, 4, 4, 5, 7, 10, 3, 2, 1]
  ]
}
```

## 📊 Input Format

**Features (9 values, range 1-10):**
1. `clump_thickness` - Cell clump thickness
2. `uniform_cell_size` - Cell size uniformity  
3. `uniform_cell_shape` - Cell shape uniformity
4. `marginal_adhesion` - Cell adhesion quality
5. `single_epithelial_cell_size` - Epithelial cell size
6. `bare_nuclei` - Bare nuclei presence
7. `bland_chromatin` - Chromatin structure
8. `normal_nucleoli` - Nucleoli normality
9. `mitoses` - Mitosis frequency

**✅ Valid Examples:**
```json
// Benign case (low risk)
{"features": [2, 1, 1, 1, 2, 1, 2, 1, 1]}

// Malignant case (high risk)
{"features": [8, 7, 8, 7, 6, 9, 7, 8, 3]}

// Borderline case
{"features": [5, 4, 4, 5, 7, 10, 3, 2, 1]}
```

## 🧪 Testing with Postman

### Test Case 1: Benign Prediction
```
POST https://api-deploy-ml-breastcancer-wisconsin.onrender.com/predict
Content-Type: application/json

{
  "features": [2, 1, 1, 1, 2, 1, 2, 1, 1]
}
```
**Expected:** `"diagnosis": "Benign"`

### Test Case 2: Malignant Prediction
```
POST https://api-deploy-ml-breastcancer-wisconsin.onrender.com/predict
Content-Type: application/json

{
  "features": [8, 7, 8, 7, 6, 9, 7, 8, 3]
}
```
**Expected:** `"diagnosis": "Malignant"`

### Test Case 3: Error Handling
```json
// Invalid range
{"features": [15, 1, 1, 1, 2, 1, 2, 1, 1]}

// Wrong count
{"features": [1, 2, 3]}

// Missing field
{"data": [1, 2, 3, 4, 5, 6, 7, 8, 9]}
```

## 🌐 Frontend Integration

### JavaScript/React Example
```javascript
const predictCancer = async (features) => {
  try {
    const response = await fetch('https://api-deploy-ml-breastcancer-wisconsin.onrender.com/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ features })
    });
    
    const result = await response.json();
    
    if (result.status === 'success') {
      console.log('Diagnosis:', result.prediction.diagnosis);
      console.log('Confidence:', result.prediction.confidence);
      console.log('Recommendation:', result.medical_interpretation.recommendation);
    }
  } catch (error) {
    console.error('API Error:', error);
  }
};

// Usage
const patientData = [2, 1, 1, 1, 2, 1, 2, 1, 1];
predictCancer(patientData);
```

### Python Example
```python
import requests

def predict_cancer(features):
    url = 'https://api-deploy-ml-breastcancer-wisconsin.onrender.com/predict'
    data = {'features': features}
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        if result['status'] == 'success':
            print(f"Diagnosis: {result['prediction']['diagnosis']}")
            print(f"Confidence: {result['prediction']['confidence']}")
            print(f"Risk Level: {result['prediction']['risk_level']}")
        
        return result
    except Exception as e:
        print(f"Error: {e}")

# Usage
patient_data = [2, 1, 1, 1, 2, 1, 2, 1, 1]
predict_cancer(patient_data)
```

## 🎯 Model Performance

- **Algorithm**: K-Nearest Neighbors (k=3)
- **Test Accuracy**: 97.08%
- **F1-Score**: 97.09%
- **Type I Error**: 3.45% (False Positive)
- **Type II Error**: 2.00% (False Negative)
- **Dataset**: Wisconsin Breast Cancer Dataset (699 samples)

## ⚠️ Important Notes

### Feature Scaling
- API automatically scales input features from (1-10) range
- Model was trained with StandardScaler
- **Fixed Issue**: Previous version didn't scale → always predicted Malignant
- **Current Version**: Proper scaling → accurate predictions

### Medical Disclaimer
- **For research/educational purposes only**
- **Not for actual medical diagnosis**
- Always consult healthcare professionals
- Use as screening tool with expert review

### Rate Limits
- **Free tier**: ~100 requests/day
- **Response time**: ~1-3 seconds (cold start: ~10 seconds)
- **Availability**: 99%+ uptime on Render.com

## 🔧 Local Development

```bash
git clone [repository]
cd api_server
pip install -r requirements.txt
python app.py
# Server: http://localhost:5000
```

## 📞 Support

- **API Issues**: Check https://api-deploy-ml-breastcancer-wisconsin.onrender.com/ for status
- **Documentation**: This README
- **Source Code**: Main repository for training code and notebooks

---

**🏥 Always remember: This is a screening tool, not a replacement for professional medical diagnosis.**
