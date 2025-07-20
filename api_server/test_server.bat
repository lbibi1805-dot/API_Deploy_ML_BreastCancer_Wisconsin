@echo off
echo 🧪 Testing KNN API Server...
echo ============================

echo 📦 Installing test dependencies...
pip install requests

echo.
echo 🔍 Running API tests...
python test_api.py

pause
