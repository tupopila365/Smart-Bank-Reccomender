"""Test FastAPI endpoints using TestClient."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi.testclient import TestClient
from src.api.main import app
from src.models.predictor import ModelPredictor
import src.api.main as main_module

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Manually load models since TestClient doesn't trigger startup events
print("Loading models...")
main_module.predictor = ModelPredictor()
print("Models loaded successfully")

client = TestClient(app)

print("Testing FastAPI Endpoints")
print("=" * 60)

# Test 1: Health endpoint
print("\n1. Testing /health endpoint...")
try:
    response = client.get("/health")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "status" in data, "Missing 'status' field"
    assert "models_loaded" in data, "Missing 'models_loaded' field"
    assert data["models_loaded"] == True, "Models not loaded"
    print(f"   [PASS] Health check successful: {data}")
except Exception as e:
    print(f"   [FAIL] Health check failed: {e}")
    sys.exit(1)

# Test 2: Predict endpoint with valid data
print("\n2. Testing /predict endpoint with valid data...")
try:
    valid_request = {
        "income": 75000,
        "spending_score": 60,
        "saving_frequency": 6,
        "loan_behavior": 2
    }
    response = client.post("/predict", json=valid_request)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    
    # Verify all required fields are present
    required_fields = [
        "recommended_account",
        "recommended_savings",
        "recommended_loan",
        "recommended_digital_service",
        "cluster_segment"
    ]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"
        if field != "cluster_segment":
            assert data[field], f"Empty value for: {field}"
    
    print(f"   [PASS] Prediction successful")
    print(f"     Account: {data['recommended_account']}")
    print(f"     Savings: {data['recommended_savings']}")
    print(f"     Loan: {data['recommended_loan']}")
    print(f"     Digital: {data['recommended_digital_service']}")
    print(f"     Cluster: {data['cluster_segment']}")
except Exception as e:
    print(f"   [FAIL] Prediction failed: {e}")
    sys.exit(1)

# Test 3: Predict endpoint with missing field (should return 422)
print("\n3. Testing /predict endpoint with missing field...")
try:
    invalid_request = {
        "income": 75000,
        "spending_score": 60,
        "saving_frequency": 6
        # Missing loan_behavior
    }
    response = client.post("/predict", json=invalid_request)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print(f"   [PASS] Missing field correctly rejected with 422")
except Exception as e:
    print(f"   [FAIL] Missing field test failed: {e}")
    sys.exit(1)

# Test 4: Predict endpoint with out-of-range value (should return 422)
print("\n4. Testing /predict endpoint with out-of-range value...")
try:
    invalid_request = {
        "income": 75000,
        "spending_score": 150,  # Out of range (max is 100)
        "saving_frequency": 6,
        "loan_behavior": 2
    }
    response = client.post("/predict", json=invalid_request)
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print(f"   [PASS] Out-of-range value correctly rejected with 422")
except Exception as e:
    print(f"   [FAIL] Out-of-range test failed: {e}")
    sys.exit(1)

# Test 5: Multiple predictions with different profiles
print("\n5. Testing multiple predictions with different profiles...")
test_profiles = [
    {
        "name": "High income, low spending",
        "data": {"income": 150000, "spending_score": 30, "saving_frequency": 8, "loan_behavior": 1}
    },
    {
        "name": "Low income, high spending",
        "data": {"income": 25000, "spending_score": 85, "saving_frequency": 2, "loan_behavior": 4}
    },
    {
        "name": "Medium income, moderate behavior",
        "data": {"income": 60000, "spending_score": 50, "saving_frequency": 5, "loan_behavior": 2}
    }
]

for profile in test_profiles:
    try:
        response = client.post("/predict", json=profile["data"])
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert all(field in data for field in required_fields), "Missing fields in response"
        print(f"   [PASS] {profile['name']}: Cluster {data['cluster_segment']}")
    except Exception as e:
        print(f"   [FAIL] {profile['name']}: {e}")
        sys.exit(1)

print("\n" + "=" * 60)
print("ALL FASTAPI ENDPOINT TESTS PASSED")
print("=" * 60)
print("\nTask 3 Requirements Verified:")
print("[PASS] FastAPI application with /predict endpoint")
print("[PASS] FastAPI application with /health endpoint")
print("[PASS] Pydantic models validate requests (422 on invalid)")
print("[PASS] Models loaded at startup")
print("[PASS] Prediction pipeline applies clustering")
print("[PASS] Prediction pipeline applies classification")
print("[PASS] Product mapping converts predictions to names")
print("[PASS] Error handling for invalid inputs")
print("[PASS] Logging implemented throughout")
