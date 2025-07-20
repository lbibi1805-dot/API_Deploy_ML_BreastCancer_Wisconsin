#!/usr/bin/env python3
"""
KNN Breast Cancer Prediction API Server
=======================================

Flask API server to serve KNN model predictions for web applications.
Supports CORS for React frontend integration.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
import joblib
import json
from datetime import datetime
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables for model
model = None
metadata = None
model_loaded = False

def load_knn_model():
    """Load KNN model and metadata on startup."""
    global model, metadata, model_loaded
    
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Models")
    
    try:
        # Find KNN files
        knn_model_file = None
        knn_metadata_file = None
        
        for filename in os.listdir(models_dir):
            if filename.startswith('KNN') and filename.endswith('.joblib'):
                knn_model_file = filename
            elif filename.startswith('KNN') and filename.endswith('_metadata.json'):
                knn_metadata_file = filename
        
        if not knn_model_file or not knn_metadata_file:
            print("❌ KNN model files not found")
            return False
        
        # Load model and metadata
        model_path = os.path.join(models_dir, knn_model_file)
        metadata_path = os.path.join(models_dir, knn_metadata_file)
        
        model = joblib.load(model_path)
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        model_loaded = True
        print(f"✅ KNN Model loaded successfully")
        print(f"   📊 Test Accuracy: {metadata['results']['test_accuracy']:.4f}")
        print(f"   🎯 Algorithm: K-Nearest Neighbors (k=3)")
        return True
        
    except Exception as e:
        print(f"❌ Error loading KNN model: {e}")
        traceback.print_exc()
        return False

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'KNN Breast Cancer Prediction API',
        'model_loaded': model_loaded,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/model/info', methods=['GET'])
def model_info():
    """Get model information and metadata."""
    if not model_loaded:
        return jsonify({
            'error': 'Model not loaded',
            'status': 'error'
        }), 500
    
    return jsonify({
        'status': 'success',
        'model_info': {
            'algorithm': 'K-Nearest Neighbors',
            'k_value': 3,
            'accuracy': metadata['results']['test_accuracy'],
            'f1_score': metadata['results']['f1_score'],
            'training_date': metadata['timestamp'],
            'features': [
                'clump_thickness',
                'uniform_cell_size', 
                'uniform_cell_shape',
                'marginal_adhesion',
                'single_epithelial_cell_size',
                'bare_nuclei',
                'bland_chromatin',
                'normal_nucleoli',
                'mitoses'
            ],
            'feature_range': '1-10 (scaled)',
            'classes': {
                '2': 'Benign',
                '4': 'Malignant'
            }
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction on breast cancer data."""
    if not model_loaded:
        return jsonify({
            'error': 'Model not loaded',
            'status': 'error'
        }), 500
    
    try:
        # Get data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No JSON data provided',
                'status': 'error'
            }), 400
        
        # Extract features
        if 'features' not in data:
            return jsonify({
                'error': 'Missing "features" field in request',
                'status': 'error',
                'expected_format': {
                    'features': [1, 1, 1, 1, 2, 1, 3, 1, 1]
                }
            }), 400
        
        features = data['features']
        
        # Validate features
        if not isinstance(features, list) or len(features) != 9:
            return jsonify({
                'error': 'Features must be a list of 9 numbers',
                'status': 'error',
                'provided_length': len(features) if isinstance(features, list) else 'not_a_list'
            }), 400
        
        # Check feature ranges (1-10)
        for i, feature in enumerate(features):
            if not isinstance(feature, (int, float)) or not (1 <= feature <= 10):
                return jsonify({
                    'error': f'Feature {i+1} must be a number between 1 and 10',
                    'status': 'error',
                    'provided_value': feature
                }), 400
        
        # Make prediction
        X = np.array(features).reshape(1, -1)
        prediction = model.predict(X)[0]
        
        # Get probabilities
        try:
            probs = model.predict_proba(X)[0]
            confidence = max(probs)
            prob_benign = probs[0] if len(probs) > 1 else (1.0 if prediction == 2 else 0.0)
            prob_malignant = probs[1] if len(probs) > 1 else (1.0 if prediction == 4 else 0.0)
        except:
            confidence = 1.0
            prob_benign = 1.0 if prediction == 2 else 0.0
            prob_malignant = 1.0 if prediction == 4 else 0.0
        
        # Format diagnosis
        diagnosis = "Benign" if prediction == 2 else "Malignant"
        risk_level = "Low" if prediction == 2 else "High"
        
        # Medical interpretation
        if prediction == 2:
            interpretation = "The tissue sample shows characteristics consistent with benign (non-cancerous) cells."
            recommendation = "Continue regular screening as recommended by healthcare provider."
        else:
            interpretation = "The tissue sample shows characteristics that may indicate malignant (cancerous) cells."
            recommendation = "Immediate consultation with oncologist recommended for further evaluation."
        
        return jsonify({
            'status': 'success',
            'prediction': {
                'diagnosis': diagnosis,
                'confidence': round(confidence, 3),
                'risk_level': risk_level,
                'raw_prediction': int(prediction),
                'probabilities': {
                    'benign': round(prob_benign, 3),
                    'malignant': round(prob_malignant, 3)
                }
            },
            'medical_interpretation': {
                'interpretation': interpretation,
                'recommendation': recommendation,
                'disclaimer': "This prediction is for research purposes only and should not replace professional medical diagnosis."
            },
            'input_features': {
                'clump_thickness': features[0],
                'uniform_cell_size': features[1],
                'uniform_cell_shape': features[2],
                'marginal_adhesion': features[3],
                'single_epithelial_cell_size': features[4],
                'bare_nuclei': features[5],
                'bland_chromatin': features[6],
                'normal_nucleoli': features[7],
                'mitoses': features[8]
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """Make predictions on multiple samples."""
    if not model_loaded:
        return jsonify({
            'error': 'Model not loaded',
            'status': 'error'
        }), 500
    
    try:
        data = request.get_json()
        
        if not data or 'samples' not in data:
            return jsonify({
                'error': 'Missing "samples" field in request',
                'status': 'error',
                'expected_format': {
                    'samples': [
                        [1, 1, 1, 1, 2, 1, 3, 1, 1],
                        [8, 7, 8, 7, 6, 9, 7, 8, 3]
                    ]
                }
            }), 400
        
        samples = data['samples']
        
        if not isinstance(samples, list) or len(samples) == 0:
            return jsonify({
                'error': 'Samples must be a non-empty list',
                'status': 'error'
            }), 400
        
        results = []
        
        for i, sample in enumerate(samples):
            if not isinstance(sample, list) or len(sample) != 9:
                return jsonify({
                    'error': f'Sample {i+1} must be a list of 9 numbers',
                    'status': 'error'
                }), 400
            
            # Make prediction for this sample
            X = np.array(sample).reshape(1, -1)
            prediction = model.predict(X)[0]
            
            try:
                probs = model.predict_proba(X)[0]
                confidence = max(probs)
                prob_benign = probs[0] if len(probs) > 1 else (1.0 if prediction == 2 else 0.0)
                prob_malignant = probs[1] if len(probs) > 1 else (1.0 if prediction == 4 else 0.0)
            except:
                confidence = 1.0
                prob_benign = 1.0 if prediction == 2 else 0.0
                prob_malignant = 1.0 if prediction == 4 else 0.0
            
            diagnosis = "Benign" if prediction == 2 else "Malignant"
            
            results.append({
                'sample_index': i + 1,
                'diagnosis': diagnosis,
                'confidence': round(confidence, 3),
                'raw_prediction': int(prediction),
                'probabilities': {
                    'benign': round(prob_benign, 3),
                    'malignant': round(prob_malignant, 3)
                }
            })
        
        return jsonify({
            'status': 'success',
            'batch_size': len(samples),
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Batch prediction error: {str(e)}',
            'status': 'error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'available_endpoints': [
            'GET /',
            'GET /model/info',
            'POST /predict',
            'POST /predict/batch'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    print("🚀 Starting KNN Breast Cancer Prediction API Server...")
    print("="*60)
    
    # Load model on startup
    success = load_knn_model()
    
    if not success:
        print("❌ Failed to load model. Server starting but predictions will not work.")
    
    print("\n🌐 API Endpoints:")
    print("   GET  /           - Health check")
    print("   GET  /model/info - Model information")
    print("   POST /predict    - Single prediction")
    print("   POST /predict/batch - Batch predictions")
    
    print("\n📝 Example request:")
    print('   POST /predict')
    print('   {')
    print('     "features": [2, 1, 1, 1, 2, 1, 2, 1, 1]')
    print('   }')
    
    print(f"\n🚀 Server starting on http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
