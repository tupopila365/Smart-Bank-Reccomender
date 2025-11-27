"""
Integration test for ML Service
Tests all ML service functionality
"""

import sys
import requests
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def log_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def log_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def log_info(message):
    print(f"{Colors.BLUE}{message}{Colors.RESET}")

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy" and data.get("models_loaded"):
                log_success("Health check passed - models loaded")
                return True
            else:
                log_error("Health check failed - models not loaded")
                return False
        else:
            log_error(f"Health check failed - status code {response.status_code}")
            return False
    except Exception as e:
        log_error(f"Health check failed: {e}")
        return False

def test_prediction_valid():
    """Test prediction with valid data"""
    test_data = {
        "income": 75000.0,
        "spending_score": 65.0,
        "saving_frequency": 5.0,
        "loan_behavior": 2.0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=test_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            required_fields = [
                "recommended_account",
                "recommended_savings",
                "recommended_loan",
                "recommended_digital_service",
                "cluster_segment"
            ]
            
            all_present = all(field in data for field in required_fields)
            all_non_empty = all(data[field] != "" for field in required_fields[:4])
            
            if all_present and all_non_empty:
                log_success("Valid prediction test passed")
                log_info(f"  Cluster: {data['cluster_segment']}")
                log_info(f"  Account: {data['recommended_account']}")
                return True
            else:
                log_error("Prediction failed - missing or empty fields")
                return False
        else:
            log_error(f"Prediction failed - status code {response.status_code}")
            return False
    except Exception as e:
        log_error(f"Prediction test failed: {e}")
        return False

def test_prediction_missing_field():
    """Test prediction with missing field"""
    test_data = {
        "income": 75000.0,
        "spending_score": 65.0,
        "saving_frequency": 5.0
        # Missing loan_behavior
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=test_data, timeout=5)
        if response.status_code == 422:
            log_success("Missing field validation test passed")
            return True
        else:
            log_error(f"Expected 422 status code, got {response.status_code}")
            return False
    except Exception as e:
        log_error(f"Validation test failed: {e}")
        return False

def test_prediction_invalid_type():
    """Test prediction with invalid data type"""
    test_data = {
        "income": "not a number",
        "spending_score": 65.0,
        "saving_frequency": 5.0,
        "loan_behavior": 2.0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=test_data, timeout=5)
        if response.status_code == 422:
            log_success("Invalid type validation test passed")
            return True
        else:
            log_error(f"Expected 422 status code, got {response.status_code}")
            return False
    except Exception as e:
        log_error(f"Type validation test failed: {e}")
        return False

def test_multiple_predictions():
    """Test multiple predictions with different profiles"""
    test_profiles = [
        {
            "name": "High income, low spending",
            "data": {
                "income": 150000.0,
                "spending_score": 30.0,
                "saving_frequency": 9.0,
                "loan_behavior": 1.0
            }
        },
        {
            "name": "Low income, high spending",
            "data": {
                "income": 25000.0,
                "spending_score": 85.0,
                "saving_frequency": 2.0,
                "loan_behavior": 4.0
            }
        },
        {
            "name": "Medium income, medium spending",
            "data": {
                "income": 60000.0,
                "spending_score": 50.0,
                "saving_frequency": 5.0,
                "loan_behavior": 2.0
            }
        }
    ]
    
    all_passed = True
    for profile in test_profiles:
        try:
            response = requests.post(f"{BASE_URL}/predict", json=profile["data"], timeout=5)
            if response.status_code == 200:
                data = response.json()
                log_info(f"  {profile['name']}: {data['recommended_account']}")
            else:
                log_error(f"  {profile['name']}: Failed with status {response.status_code}")
                all_passed = False
        except Exception as e:
            log_error(f"  {profile['name']}: {e}")
            all_passed = False
    
    if all_passed:
        log_success("Multiple predictions test passed")
        return True
    else:
        log_error("Multiple predictions test failed")
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    log_info("ML Service Integration Tests")
    print("=" * 70)
    
    results = []
    
    # Run tests
    log_info("\n1. Testing health endpoint...")
    results.append(("Health Check", test_health()))
    
    log_info("\n2. Testing valid prediction...")
    results.append(("Valid Prediction", test_prediction_valid()))
    
    log_info("\n3. Testing missing field validation...")
    results.append(("Missing Field Validation", test_prediction_missing_field()))
    
    log_info("\n4. Testing invalid type validation...")
    results.append(("Invalid Type Validation", test_prediction_invalid_type()))
    
    log_info("\n5. Testing multiple predictions...")
    results.append(("Multiple Predictions", test_multiple_predictions()))
    
    # Print summary
    print("\n" + "=" * 70)
    log_info("Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            log_success(test_name)
        else:
            log_error(test_name)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        log_success("\n✓ ALL ML SERVICE TESTS PASSED!")
        return 0
    else:
        log_error(f"\n✗ {total - passed} TEST(S) FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
