@echo off
echo 🚀 Starting KNN Breast Cancer Prediction API Server...
echo ========================================================

echo 📦 Installing dependencies...
pip install flask flask-cors numpy scikit-learn joblib requests

echo.
echo 🌐 Starting Flask server...
python app.py

pause
