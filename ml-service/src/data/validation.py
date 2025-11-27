"""Data validation functions for ensuring data quality."""

import pandas as pd
import numpy as np
from typing import Tuple, List

try:
    from ..utils import BASE_FEATURES, ALL_FEATURES, FEATURE_RANGES, setup_logger
except ImportError:
    from utils import BASE_FEATURES, ALL_FEATURES, FEATURE_RANGES, setup_logger

logger = setup_logger(__name__)


class DataValidator:
    """Validate datasets to ensure all required features are present and properly formatted."""
    
    def validate_dataset(self, df: pd.DataFrame, require_derived: bool = False) -> Tuple[bool, List[str]]:
        """
        Validate a dataset for completeness and correctness.
        
        Args:
            df: DataFrame to validate
            require_derived: If True, check for derived features as well
        
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Check if DataFrame is empty
        if df.empty:
            errors.append("Dataset is empty")
            return False, errors
        
        # Determine which features to check
        required_features = ALL_FEATURES if require_derived else BASE_FEATURES
        
        # Check for missing columns
        missing_columns = [col for col in required_features if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Check for null values in required columns
        for col in required_features:
            if col in df.columns:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    errors.append(f"Column '{col}' has {null_count} null values")
        
        # Validate feature ranges for base features
        for feature, (min_val, max_val) in FEATURE_RANGES.items():
            if feature in df.columns:
                out_of_range = ((df[feature] < min_val) | (df[feature] > max_val)).sum()
                if out_of_range > 0:
                    errors.append(
                        f"Column '{feature}' has {out_of_range} values outside valid range [{min_val}, {max_val}]"
                    )
        
        # Check data types
        for col in required_features:
            if col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    errors.append(f"Column '{col}' is not numeric (type: {df[col].dtype})")
        
        # Check for infinite values
        for col in required_features:
            if col in df.columns:
                inf_count = np.isinf(df[col]).sum()
                if inf_count > 0:
                    errors.append(f"Column '{col}' has {inf_count} infinite values")
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.info(f"Dataset validation passed for {len(df)} records")
        else:
            logger.error(f"Dataset validation failed with {len(errors)} errors")
            for error in errors:
                logger.error(f"  - {error}")
        
        return is_valid, errors
    
    def validate_profile(self, profile: dict) -> Tuple[bool, List[str]]:
        """
        Validate a single user profile.
        
        Args:
            profile: Dictionary with user profile data
        
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Check for missing fields
        missing_fields = [field for field in BASE_FEATURES if field not in profile]
        if missing_fields:
            errors.append(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Validate ranges
        for feature, (min_val, max_val) in FEATURE_RANGES.items():
            if feature in profile:
                value = profile[feature]
                if not isinstance(value, (int, float)):
                    errors.append(f"Field '{feature}' must be numeric, got {type(value).__name__}")
                elif value < min_val or value > max_val:
                    errors.append(f"Field '{feature}' value {value} is outside valid range [{min_val}, {max_val}]")
                elif np.isnan(value) or np.isinf(value):
                    errors.append(f"Field '{feature}' has invalid value (NaN or Inf)")
        
        is_valid = len(errors) == 0
        return is_valid, errors
