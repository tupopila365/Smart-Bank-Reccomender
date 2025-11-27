"""Simple test script to verify the ML service setup."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data import SyntheticDataGenerator, FeatureEngineer, DataValidator
from src.utils import BASE_FEATURES, DERIVED_FEATURES, ALL_FEATURES


def test_data_generation():
    """Test synthetic data generation."""
    print("Testing synthetic data generation...")
    generator = SyntheticDataGenerator(random_state=42)
    df = generator.generate(n_samples=100)
    
    assert len(df) == 100, f"Expected 100 samples, got {len(df)}"
    assert all(col in df.columns for col in BASE_FEATURES), "Missing base features"
    print(f"✓ Generated {len(df)} samples with base features")
    return df


def test_feature_engineering(df):
    """Test feature engineering."""
    print("\nTesting feature engineering...")
    engineer = FeatureEngineer()
    df_engineered = engineer.transform(df)
    
    assert all(col in df_engineered.columns for col in DERIVED_FEATURES), "Missing derived features"
    assert 'income_to_spending_ratio' in df_engineered.columns
    assert 'savings_capacity' in df_engineered.columns
    assert 'financial_health_score' in df_engineered.columns
    print(f"✓ Added {len(DERIVED_FEATURES)} derived features")
    return df_engineered


def test_validation(df):
    """Test data validation."""
    print("\nTesting data validation...")
    validator = DataValidator()
    
    # Test with base features only
    is_valid, errors = validator.validate_dataset(df[BASE_FEATURES], require_derived=False)
    assert is_valid, f"Base feature validation failed: {errors}"
    print("✓ Base feature validation passed")
    
    # Test with all features
    is_valid, errors = validator.validate_dataset(df, require_derived=True)
    assert is_valid, f"Full dataset validation failed: {errors}"
    print("✓ Full dataset validation passed")
    
    # Test profile validation
    profile = {
        'income': 50000,
        'spending_score': 65,
        'saving_frequency': 5,
        'loan_behavior': 2
    }
    is_valid, errors = validator.validate_profile(profile)
    assert is_valid, f"Profile validation failed: {errors}"
    print("✓ Profile validation passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("ML Service Setup Verification")
    print("=" * 60)
    
    try:
        # Test data generation
        df = test_data_generation()
        
        # Test feature engineering
        df_engineered = test_feature_engineering(df)
        
        # Test validation
        test_validation(df_engineered)
        
        print("\n" + "=" * 60)
        print("✓ All tests passed! ML Service foundation is set up correctly.")
        print("=" * 60)
        
        print("\nDataset info:")
        print(f"  Shape: {df_engineered.shape}")
        print(f"  Columns: {list(df_engineered.columns)}")
        print(f"\nSample data:")
        print(df_engineered[ALL_FEATURES].head())
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
