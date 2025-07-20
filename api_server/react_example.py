#!/usr/bin/env python3
"""
React Integration Example
========================

Example React component để sử dụng KNN Cancer Prediction API.
"""

# React Component Example (Save as PredictionComponent.jsx)
REACT_COMPONENT = '''
import React, { useState, useEffect } from 'react';

const API_BASE_URL = 'http://localhost:5000';

const CancerPredictionComponent = () => {
  const [features, setFeatures] = useState([
    2, 1, 1, 1, 2, 1, 2, 1, 1  // Default benign case
  ]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [modelInfo, setModelInfo] = useState(null);

  const featureNames = [
    'Clump Thickness',
    'Uniform Cell Size', 
    'Uniform Cell Shape',
    'Marginal Adhesion',
    'Single Epithelial Cell Size',
    'Bare Nuclei',
    'Bland Chromatin',
    'Normal Nucleoli',
    'Mitoses'
  ];

  // Load model info on component mount
  useEffect(() => {
    const loadModelInfo = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/model/info`);
        const data = await response.json();
        if (data.status === 'success') {
          setModelInfo(data.model_info);
        }
      } catch (error) {
        console.error('Error loading model info:', error);
      }
    };

    loadModelInfo();
  }, []);

  const handleFeatureChange = (index, value) => {
    const newFeatures = [...features];
    newFeatures[index] = Math.max(1, Math.min(10, parseInt(value) || 1));
    setFeatures(newFeatures);
  };

  const makePrediction = async () => {
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          features: features
        })
      });

      const data = await response.json();
      
      if (data.status === 'success') {
        setResult(data);
      } else {
        throw new Error(data.error || 'Prediction failed');
      }
    } catch (error) {
      console.error('Prediction error:', error);
      setResult({
        error: error.message
      });
    } finally {
      setLoading(false);
    }
  };

  const loadSampleCase = (sampleType) => {
    const samples = {
      benign: [2, 1, 1, 1, 2, 1, 2, 1, 1],
      malignant: [8, 7, 8, 7, 6, 9, 7, 8, 3],
      borderline: [5, 3, 4, 3, 3, 5, 4, 4, 1]
    };
    setFeatures(samples[sampleType]);
    setResult(null);
  };

  return (
    <div style={{ 
      maxWidth: '800px', 
      margin: '0 auto', 
      padding: '20px',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1>🔬 Breast Cancer Prediction Tool</h1>
      
      {/* Model Info */}
      {modelInfo && (
        <div style={{ 
          backgroundColor: '#f0f8ff', 
          padding: '15px', 
          borderRadius: '8px',
          marginBottom: '20px'
        }}>
          <h3>📊 Model Information</h3>
          <p><strong>Algorithm:</strong> {modelInfo.algorithm}</p>
          <p><strong>Accuracy:</strong> {(modelInfo.accuracy * 100).toFixed(2)}%</p>
          <p><strong>K-Value:</strong> {modelInfo.k_value}</p>
        </div>
      )}

      {/* Sample Cases */}
      <div style={{ marginBottom: '20px' }}>
        <h3>📋 Load Sample Cases:</h3>
        <button 
          onClick={() => loadSampleCase('benign')}
          style={{ margin: '5px', padding: '8px 16px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px' }}
        >
          Benign Sample
        </button>
        <button 
          onClick={() => loadSampleCase('malignant')}
          style={{ margin: '5px', padding: '8px 16px', backgroundColor: '#f44336', color: 'white', border: 'none', borderRadius: '4px' }}
        >
          Malignant Sample
        </button>
        <button 
          onClick={() => loadSampleCase('borderline')}
          style={{ margin: '5px', padding: '8px 16px', backgroundColor: '#ff9800', color: 'white', border: 'none', borderRadius: '4px' }}
        >
          Borderline Sample
        </button>
      </div>

      {/* Feature Inputs */}
      <div style={{ marginBottom: '20px' }}>
        <h3>🔢 Enter Feature Values (1-10):</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '10px' }}>
          {features.map((value, index) => (
            <div key={index} style={{ display: 'flex', alignItems: 'center' }}>
              <label style={{ minWidth: '180px', fontSize: '14px' }}>
                {featureNames[index]}:
              </label>
              <input
                type="number"
                min="1"
                max="10"
                value={value}
                onChange={(e) => handleFeatureChange(index, e.target.value)}
                style={{ 
                  width: '60px', 
                  padding: '4px', 
                  border: '1px solid #ccc', 
                  borderRadius: '4px' 
                }}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Predict Button */}
      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <button
          onClick={makePrediction}
          disabled={loading}
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            backgroundColor: loading ? '#ccc' : '#2196F3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? '🔄 Predicting...' : '🔍 Make Prediction'}
        </button>
      </div>

      {/* Results */}
      {result && (
        <div style={{ 
          border: '1px solid #ddd', 
          borderRadius: '8px', 
          padding: '20px',
          backgroundColor: result.error ? '#ffebee' : '#f9f9f9'
        }}>
          {result.error ? (
            <div>
              <h3 style={{ color: '#f44336' }}>❌ Error</h3>
              <p>{result.error}</p>
            </div>
          ) : (
            <div>
              <h3>🎯 Prediction Results</h3>
              
              <div style={{ 
                fontSize: '24px', 
                fontWeight: 'bold',
                color: result.prediction.diagnosis === 'Benign' ? '#4CAF50' : '#f44336',
                marginBottom: '15px'
              }}>
                Diagnosis: {result.prediction.diagnosis}
              </div>
              
              <p><strong>Confidence:</strong> {(result.prediction.confidence * 100).toFixed(1)}%</p>
              <p><strong>Risk Level:</strong> {result.prediction.risk_level}</p>
              
              <div style={{ marginTop: '15px' }}>
                <h4>📊 Probabilities:</h4>
                <div style={{ display: 'flex', gap: '20px' }}>
                  <div>
                    <strong>Benign:</strong> {(result.prediction.probabilities.benign * 100).toFixed(1)}%
                  </div>
                  <div>
                    <strong>Malignant:</strong> {(result.prediction.probabilities.malignant * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
              
              <div style={{ 
                marginTop: '20px', 
                padding: '15px', 
                backgroundColor: '#fff3cd',
                borderRadius: '4px'
              }}>
                <h4>🏥 Medical Interpretation:</h4>
                <p><strong>Interpretation:</strong> {result.medical_interpretation.interpretation}</p>
                <p><strong>Recommendation:</strong> {result.medical_interpretation.recommendation}</p>
                <p style={{ 
                  fontSize: '12px', 
                  fontStyle: 'italic',
                  color: '#666'
                }}>
                  {result.medical_interpretation.disclaimer}
                </p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CancerPredictionComponent;
'''

def save_react_component():
    """Save React component to file."""
    with open('PredictionComponent.jsx', 'w', encoding='utf-8') as f:
        f.write(REACT_COMPONENT)
    print("✅ React component saved as PredictionComponent.jsx")

if __name__ == "__main__":
    print("📝 React Integration Example")
    print("="*50)
    print("This file contains a complete React component for cancer prediction.")
    print("\nTo use:")
    print("1. Copy PredictionComponent.jsx to your React project")
    print("2. Import and use the component")
    print("3. Make sure the API server is running on localhost:5000")
    print("4. Install axios if needed: npm install axios")
    
    save_react_component()
    
    print(f"\n🌐 Usage in your React app:")
    print('''
import CancerPredictionComponent from './PredictionComponent';

function App() {
  return (
    <div className="App">
      <CancerPredictionComponent />
    </div>
  );
}

export default App;
    ''')
