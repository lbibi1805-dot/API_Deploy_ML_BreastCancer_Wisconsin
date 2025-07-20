#!/usr/bin/env python3
"""
API Test Client
===============

Simple test client to verify the KNN API server is working correctly.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint."""
    print("🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_model_info():
    """Test model info endpoint."""
    print("\n🔍 Testing Model Info...")
    try:
        response = requests.get(f"{BASE_URL}/model/info")
        print(f"   Status: {response.status_code}")
        data = response.json()
        if response.status_code == 200:
            print(f"   Algorithm: {data['model_info']['algorithm']}")
            print(f"   Accuracy: {data['model_info']['accuracy']:.4f}")
            print(f"   K-Value: {data['model_info']['k_value']}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_single_prediction():
    """Test single prediction endpoint."""
    print("\n🔍 Testing Single Prediction...")
    
    # Test cases
    test_cases = [
        {
            'name': 'Benign Case',
            'features': [2, 1, 1, 1, 2, 1, 2, 1, 1],
            'expected': 'Benign'
        },
        {
            'name': 'Malignant Case',
            'features': [8, 7, 8, 7, 6, 9, 7, 8, 3],
            'expected': 'Malignant'
        }
    ]
    
    success_count = 0
    
    for test_case in test_cases:
        print(f"\n   📋 {test_case['name']}:")
        try:
            payload = {"features": test_case['features']}
            response = requests.post(
                f"{BASE_URL}/predict",
                headers={"Content-Type": "application/json"},
                json=payload
            )
            
            print(f"      Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                diagnosis = data['prediction']['diagnosis']
                confidence = data['prediction']['confidence']
                
                print(f"      Prediction: {diagnosis}")
                print(f"      Confidence: {confidence:.3f}")
                print(f"      Expected: {test_case['expected']}")
                
                if diagnosis == test_case['expected']:
                    print(f"      ✅ CORRECT")
                    success_count += 1
                else:
                    print(f"      ❌ INCORRECT")
            else:
                print(f"      ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    return success_count == len(test_cases)

def test_batch_prediction():
    """Test batch prediction endpoint."""
    print("\n🔍 Testing Batch Prediction...")
    try:
        payload = {
            "samples": [
                [2, 1, 1, 1, 2, 1, 2, 1, 1],  # Benign
                [8, 7, 8, 7, 6, 9, 7, 8, 3],  # Malignant
                [5, 3, 4, 3, 3, 5, 4, 4, 1]   # Borderline
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/predict/batch",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Batch Size: {data['batch_size']}")
            
            for result in data['results']:
                print(f"   Sample {result['sample_index']}: {result['diagnosis']} (confidence: {result['confidence']:.3f})")
            
            return True
        else:
            print(f"   ❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_error_cases():
    """Test error handling."""
    print("\n🔍 Testing Error Cases...")
    
    # Test invalid endpoint
    print("   📋 Invalid endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/invalid")
        print(f"      Status: {response.status_code} (expected 404)")
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    # Test invalid features
    print("   📋 Invalid features (wrong length):")
    try:
        payload = {"features": [1, 2, 3]}  # Only 3 features instead of 9
        response = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print(f"      Status: {response.status_code} (expected 400)")
        if response.status_code == 400:
            print(f"      Error message: {response.json()['error']}")
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    # Test out of range features
    print("   📋 Out of range features:")
    try:
        payload = {"features": [15, 1, 1, 1, 2, 1, 2, 1, 1]}  # 15 is out of range (1-10)
        response = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print(f"      Status: {response.status_code} (expected 400)")
        if response.status_code == 400:
            print(f"      Error message: {response.json()['error']}")
    except Exception as e:
        print(f"      ❌ Error: {e}")

def main():
    """Run all API tests."""
    print("🧪 KNN BREAST CANCER API TEST CLIENT")
    print("="*50)
    print(f"Testing API at: {BASE_URL}")
    print("Make sure the API server is running first!")
    print("-"*50)
    
    # Wait a moment
    time.sleep(1)
    
    tests = [
        ("Health Check", test_health_check),
        ("Model Info", test_model_info),
        ("Single Prediction", test_single_prediction),
        ("Batch Prediction", test_batch_prediction)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Test error cases (these are expected to fail)
    test_error_cases()
    
    # Summary
    print("\n📊 TEST RESULTS SUMMARY:")
    print("-"*50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API server.")
    
    print("\n📝 API Usage Examples:")
    print("   React: fetch('http://localhost:5000/predict', {method: 'POST', ...})")
    print("   Express: axios.post('http://localhost:5000/predict', data)")
    print("   curl: curl -X POST http://localhost:5000/predict -H 'Content-Type: application/json' -d '{\"features\": [...]}'")

if __name__ == "__main__":
    main()
