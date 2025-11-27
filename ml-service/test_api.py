"""Test script to verify ML Service API implementation."""

import requests
import json
import sys

# Test configuration
BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the /health endpoint."""
    print("\n=== Testing /health endpoint ===")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy" and data.get("models_loaded"):
                print("✓ Health check passed - models loaded")
                return True
            else:
                print("✗ Health check failed - models not loaded")
                return False
        else:
            print("✗ Health check failed - unexpected status code")
            return False
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False


def test_predict_endpoint_valid():
    """Test the /predict endpoint with valid data."""
    print("\n=== Testing /predict endpoint with valid data ===")
    
    test_data = {
        "income": 75000.0,
        "spending_score": 65.0,
        "saving_frequency": 5.0,
        "loan_behavior": 2.0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=test_data,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
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
            all_non_empty = all(
                data[field] != "" for field in required_fields[:4]
            )
            
            if all_present and all_non_empty:
                print("✓ Prediction successful - all fields present and non-empty")
                return True
            else:
                print("✗ Prediction failed - missing or empty fields")
                return False
        else:
            print("✗ Prediction failed - unexpected status code")
            return False
    except Exception as e:
        print(f"✗ Prediction failed: {e}")
        return False


def test_predict_endpoint_missing_field():
    """Test the /predict endpoint with missing required field."""
    print("\n=== Testing /predict endpoint with missing field ===")
    
    test_data = {
        "income": 75000.0,
        "spending_score": 65.0,
        "saving_frequency": 5.0
        # Missing loan_behavior
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=test_data,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 422:
            print("✓ Validation error correctly returned for missing field")
            return True
        else:
            print("✗ Expected 422 status code for missing field")
            return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_predict_endpoint_invalid_range():
    """Test the /predict endpoint with out-of-range values."""
    print("\n=== Testing /predict endpoint with out-of-range values ===")
    
    test_data = {
        "income": -1000.0,  # Invalid: negative income
        "spending_score": 65.0,
        "saving_frequency": 5.0,
        "loan_behavior": 2.0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=test_data,
            timeout=5
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 422:
            print("✓ Validation error correctly returned for out-of-range value")
            return True
        else:
            print("✗ Expected 422 status code for out-of-range value")
            return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("ML Service API Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test health endpoint
    results.append(("Health Check", test_health_endpoint()))
    
    # Test predict endpoint with valid data
    results.append(("Valid Prediction", test_predict_endpoint_valid()))
    
    # Test predict endpoint with missing field
    results.append(("Missing Field Validation", test_predict_endpoint_missing_field()))
    
    # Test predict endpoint with invalid range
    results.append(("Invalid Range Validation", test_predict_endpoint_invalid_range()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
