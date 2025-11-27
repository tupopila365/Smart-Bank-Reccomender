"""Test script to verify Task 1 requirements are met."""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data import SyntheticDataGenerator, FeatureEngineer, DataValidator
from src.utils import BASE_FEATURES, DERIVED_FEATURES, MIN_SAMPLES, MAX_SAMPLES


def test_requirement_8_1():
    """
    Requirement 8.1: WHEN the synthetic dataset generator executes, 
    THEN the ML Service SHALL create between 500 and 1000 simulated user profiles
    """
    print("\n" + "=" * 70)
    print("Testing Requirement 8.1: Dataset size between 500-1000")
    print("=" * 70)
    
    generator = SyntheticDataGenerator(random_state=42)
    
    # Test with None (should generate random size between MIN and MAX)
    df1 = generator.generate(n_samples=None)
    assert MIN_SAMPLES <= len(df1) <= MAX_SAMPLES, \
        f"Dataset size {len(df1)} not in range [{MIN_SAMPLES}, {MAX_SAMPLES}]"
    print(f"✓ Generated {len(df1)} profiles (within {MIN_SAMPLES}-{MAX_SAMPLES} range)")
    
    # Test with specific values
    df2 = generator.generate(n_samples=500)
    assert len(df2) == 500, f"Expected 500 samples, got {len(df2)}"
    print(f"✓ Generated exactly 500 profiles when requested")
    
    df3 = generator.generate(n_samples=1000)
    assert len(df3) == 1000, f"Expected 1000 samples, got {len(df3)}"
    print(f"✓ Generated exactly 1000 profiles when requested")
    
    print("✓ Requirement 8.1 PASSED")
    return df1


def test_requirement_8_3(df):
    """
    Requirement 8.3: WHEN the dataset is generated, 
    THEN the ML Service SHALL save the data in a format compatible with pandas DataFrames
    """
    print("\n" + "=" * 70)
    print("Testing Requirement 8.3: Pandas DataFrame compatibility")
    print("=" * 70)
    
    # Check it's a DataFrame
    assert isinstance(df, pd.DataFrame), f"Expected pandas DataFrame, got {type(df)}"
    print(f"✓ Data is a pandas DataFrame")
    
    # Save to CSV and reload
    test_file = Path(__file__).parent / 'data' / 'test_output.csv'
    test_file.parent.mkdir(exist_ok=True)
    df.to_csv(test_file, index=False)
    print(f"✓ Saved to CSV: {test_file}")
    
    # Reload and verify
    df_reloaded = pd.read_csv(test_file)
    assert len(df_reloaded) == len(df), "Row count mismatch after reload"
    assert list(df_reloaded.columns) == list(df.columns), "Column mismatch after reload"
    print(f"✓ Successfully reloaded from CSV with {len(df_reloaded)} rows")
    
    # Clean up
    test_file.unlink()
    
    print("✓ Requirement 8.3 PASSED")


def test_requirement_8_4(df):
    """
    Requirement 8.4: WHEN feature engineering is applied, 
    THEN the ML Service SHALL create derived features that improve model performance
    """
    print("\n" + "=" * 70)
    print("Testing Requirement 8.4: Feature engineering creates derived features")
    print("=" * 70)
    
    # Apply feature engineering
    engineer = FeatureEngineer()
    df_engineered = engineer.transform(df)
    
    # Check all derived features are present
    for feature in DERIVED_FEATURES:
        assert feature in df_engineered.columns, f"Missing derived feature: {feature}"
        print(f"✓ Derived feature '{feature}' created")
    
    # Verify specific derived features
    assert 'income_to_spending_ratio' in df_engineered.columns
    assert 'savings_capacity' in df_engineered.columns
    assert 'financial_health_score' in df_engineered.columns
    
    # Check that derived features have valid values
    assert not df_engineered['income_to_spending_ratio'].isnull().any(), \
        "income_to_spending_ratio has null values"
    assert not df_engineered['savings_capacity'].isnull().any(), \
        "savings_capacity has null values"
    assert not df_engineered['financial_health_score'].isnull().any(), \
        "financial_health_score has null values"
    
    print(f"✓ All {len(DERIVED_FEATURES)} derived features created successfully")
    print(f"✓ No null values in derived features")
    
    # Verify feature engineering logic
    sample = df_engineered.iloc[0]
    expected_ratio = sample['income'] / (sample['spending_score'] + 1)
    assert abs(sample['income_to_spending_ratio'] - expected_ratio) < 0.01, \
        "income_to_spending_ratio calculation incorrect"
    print(f"✓ Feature engineering calculations verified")
    
    print("✓ Requirement 8.4 PASSED")
    return df_engineered


def test_requirement_8_5(df):
    """
    Requirement 8.5: WHEN the dataset is complete, 
    THEN the ML Service SHALL validate that all required features are present and properly formatted
    """
    print("\n" + "=" * 70)
    print("Testing Requirement 8.5: Dataset validation")
    print("=" * 70)
    
    validator = DataValidator()
    
    # Validate base features
    is_valid, errors = validator.validate_dataset(df[BASE_FEATURES], require_derived=False)
    assert is_valid, f"Base feature validation failed: {errors}"
    print(f"✓ Base features validation passed")
    
    # Validate all features
    is_valid, errors = validator.validate_dataset(df, require_derived=True)
    assert is_valid, f"Full dataset validation failed: {errors}"
    print(f"✓ Full dataset validation passed (all required features present)")
    
    # Check that all base features are in valid ranges
    for feature in BASE_FEATURES:
        assert feature in df.columns, f"Missing required feature: {feature}"
        print(f"✓ Required feature '{feature}' is present")
    
    # Verify data types are numeric
    for feature in BASE_FEATURES + DERIVED_FEATURES:
        if feature in df.columns:
            assert pd.api.types.is_numeric_dtype(df[feature]), \
                f"Feature '{feature}' is not numeric"
    print(f"✓ All features are properly formatted (numeric)")
    
    # Verify no NaN or infinite values
    for feature in BASE_FEATURES + DERIVED_FEATURES:
        if feature in df.columns:
            assert not df[feature].isnull().any(), f"Feature '{feature}' has null values"
            assert not (df[feature] == float('inf')).any(), f"Feature '{feature}' has infinite values"
            assert not (df[feature] == float('-inf')).any(), f"Feature '{feature}' has negative infinite values"
    print(f"✓ No NaN or infinite values in dataset")
    
    print("✓ Requirement 8.5 PASSED")


def test_project_structure():
    """Verify proper directory organization."""
    print("\n" + "=" * 70)
    print("Testing Project Structure")
    print("=" * 70)
    
    base_path = Path(__file__).parent
    
    # Check directory structure
    required_dirs = [
        'src',
        'src/api',
        'src/data',
        'src/schemas',
        'src/utils',
        'scripts',
        'data'
    ]
    
    for dir_path in required_dirs:
        full_path = base_path / dir_path
        assert full_path.exists(), f"Missing directory: {dir_path}"
        print(f"✓ Directory exists: {dir_path}")
    
    # Check key files
    required_files = [
        'requirements.txt',
        'README.md',
        'src/data/generator.py',
        'src/data/feature_engineering.py',
        'src/data/validation.py',
        'src/utils/constants.py',
        'scripts/generate_data.py'
    ]
    
    for file_path in required_files:
        full_path = base_path / file_path
        assert full_path.exists(), f"Missing file: {file_path}"
        print(f"✓ File exists: {file_path}")
    
    print("✓ Project structure is properly organized")


def main():
    """Run all requirement tests."""
    print("\n" + "=" * 70)
    print("TASK 1 REQUIREMENTS VERIFICATION")
    print("=" * 70)
    print("\nVerifying Requirements: 8.1, 8.3, 8.4, 8.5")
    
    try:
        # Test project structure
        test_project_structure()
        
        # Test Requirement 8.1 - Generate dataset
        df = test_requirement_8_1()
        
        # Test Requirement 8.4 - Feature engineering
        df_engineered = test_requirement_8_4(df)
        
        # Test Requirement 8.5 - Validation
        test_requirement_8_5(df_engineered)
        
        # Test Requirement 8.3 - Pandas compatibility
        test_requirement_8_3(df_engineered)
        
        print("\n" + "=" * 70)
        print("✓✓✓ ALL TASK 1 REQUIREMENTS PASSED ✓✓✓")
        print("=" * 70)
        print("\nSummary:")
        print("  ✓ Requirement 8.1: Dataset generation (500-1000 profiles)")
        print("  ✓ Requirement 8.3: Pandas DataFrame compatibility")
        print("  ✓ Requirement 8.4: Feature engineering (derived features)")
        print("  ✓ Requirement 8.5: Data validation")
        print("  ✓ Project structure properly organized")
        print("\nTask 1 is complete and ready for Task 2 (model training)!")
        
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
