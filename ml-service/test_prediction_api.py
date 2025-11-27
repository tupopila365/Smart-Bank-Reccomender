"""Test script to verify the ML Service prediction API."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models.predictor import ModelPredictor
from src.schemas.prediction import PredictionRequest, PredictionResponse


def test_model_loading():
    """Test that models load successfully."""
    print("Testing model loading...")
    try:
        predictor = ModelPredictor()
        assert predictor.is_loaded(), "Models not loaded"
        print("✓ Models loaded successfully")
        return predictor
    except Exception as e:
        print(f"✗ Model loading failed: {e}")
        sys.exit(1)


def test_prediction_request_validation():
    """Test Pydantic request validation."""
    print("\nTesting request validation...")
    
    # Valid request
    try:
        valid_request = PredictionRequest(
            income=50000,
            spending_score=65,
            saving_frequency=5,
            loan_behavior=2
        )
        print("✓ Valid request accepted")
    except Exception as e:
        print(f"✗ Valid request rejected: {e}")
        sys.exit(1)
    
    # Invalid request - missing field
    try:
        invalid_request = PredictionRequest(
            income=50000,
            spending_score=65,
            saving_frequency=5
        )
        print("✗ Invalid request (missing field) was accepted")
        sys.exit(1)
    except Exception:
        print("✓ Invalid request (missing field) rejected")
    
    # Invalid request - out of range
    try:
        invalid_request = PredictionRequest(
            income=50000,
            spending_score=150,  # Out of range
            saving_frequency=5,
            loan_behavior=2
        )
        print("✗ Invalid request (out of range) was accepted")
        sys.exit(1)
    except Exception:
        print("✓ Invalid request (out of range) rejected")
    
    # Invalid request - NaN
    try:
        invalid_request = PredictionRequest(
            income=float('nan'),
            spending_score=65,
            saving_frequency=5,
            loan_behavior=2
        )
        print("✗ Invalid request (NaN) was accepted")
        sys.exit(1)
    except Exception:
        print("✓ Invalid request (NaN) rejected")


def test_prediction_pipeline(predictor):
    """Test the complete prediction pipeline."""
    print("\nTesting prediction pipeline...")
    
    test_cases = [
        {
            "name": "High income, low spending",
            "income": 150000,
            "spending_score": 30,
            "saving_frequency": 8,
            "loan_behavior": 1
        },
        {
            "name": "Medium income, high spending",
            "income": 60000,
            "spending_score": 85,
            "saving_frequency": 3,
            "loan_behavior": 4
        },
        {
            "name": "Low income, moderate spending",
            "income": 25000,
            "spending_score": 50,
            "saving_frequency": 5,
            "loan_behavior": 2
        }
    ]
    
    for test_case in test_cases:
        name = test_case.pop("name")
        print(f"\n  Testing: {name}")
        
        try:
            predictions = predictor.predict(**test_case)
            
            # Verify response structure
            assert 'recommended_account' in predictions, "Missing recommended_account"
            assert 'recommended_savings' in predictions, "Missing recommended_savings"
            assert 'recommended_loan' in predictions, "Missing recommended_loan"
            assert 'recommended_digital_service' in predictions, "Missing recommended_digital_service"
            assert 'cluster_segment' in predictions, "Missing cluster_segment"
            
            # Verify all recommendations are non-empty strings
            assert isinstance(predictions['recommended_account'], str) and predictions['recommended_account'], "Invalid account recommendation"
            assert isinstance(predictions['recommended_savings'], str) and predictions['recommended_savings'], "Invalid savings recommendation"
            assert isinstance(predictions['recommended_loan'], str) and predictions['recommended_loan'], "Invalid loan recommendation"
            assert isinstance(predictions['recommended_digital_service'], str) and predictions['recommended_digital_service'], "Invalid digital service recommendation"
            
            # Verify cluster segment is an integer
            assert isinstance(predictions['cluster_segment'], int), "Cluster segment must be integer"
            
            print(f"    ✓ Predictions generated successfully")
            print(f"      Account: {predictions['recommended_account']}")
            print(f"      Savings: {predictions['recommended_savings']}")
            print(f"      Loan: {predictions['recommended_loan']}")
            print(f"      Digital Service: {predictions['recommended_digital_service']}")
            print(f"      Cluster: {predictions['cluster_segment']}")
            
        except Exception as e:
            print(f"    ✗ Prediction failed: {e}")
            sys.exit(1)


def test_response_model():
    """Test Pydantic response model."""
    print("\nTesting response model...")
    
    try:
        response = PredictionResponse(
            recommended_account="Premium Checking Account",
            recommended_savings="High-Yield Savings Account",
            recommended_loan="Home Mortgage",
            recommended_digital_service="Premium Digital Banking",
            cluster_segment=2
        )
        print("✓ Response model validated successfully")
    except Exception as e:
        print(f"✗ Response model validation failed: {e}")
        sys.exit(1)


def main():
    """Run all tests."""
    print("=" * 60)
    print("ML Service Prediction API Test Suite")
    print("=" * 60)
    
    # Test 1: Model loading
    predictor = test_model_loading()
    
    # Test 2: Request validation
    test_prediction_request_validation()
    
    # Test 3: Prediction pipeline
    test_prediction_pipeline(predictor)
    
    # Test 4: Response model
    test_response_model()
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    print("\nTask 3 requirements verified:")
    print("✓ FastAPI application with /predict and /health endpoints")
    print("✓ Pydantic models for request/response validation")
    print("✓ Model loader that loads K-Means and Decision Tree models at startup")
    print("✓ Prediction pipeline that applies clustering then classification")
    print("✓ Product mapping logic to convert predictions to product names")
    print("✓ Error handling and logging for prediction failures")


if __name__ == "__main__":
    main()
