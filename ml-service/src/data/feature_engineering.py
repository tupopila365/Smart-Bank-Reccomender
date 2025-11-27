"""Feature engineering module for creating derived features."""

import pandas as pd
import numpy as np

try:
    from ..utils import BASE_FEATURES, DERIVED_FEATURES, setup_logger
except ImportError:
    from utils import BASE_FEATURES, DERIVED_FEATURES, setup_logger

logger = setup_logger(__name__)


class FeatureEngineer:
    """Create derived features from base financial profile features."""
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply feature engineering to create derived features.
        
        Args:
            df: DataFrame with base features (income, spending_score, saving_frequency, loan_behavior)
        
        Returns:
            DataFrame with base features plus derived features
        """
        logger.info("Applying feature engineering")
        
        # Create a copy to avoid modifying the original
        df_transformed = df.copy()
        
        # Derived feature 1: Income to spending ratio
        # Higher ratio means more conservative spending relative to income
        df_transformed['income_to_spending_ratio'] = df_transformed['income'] / (df_transformed['spending_score'] + 1)
        
        # Derived feature 2: Savings capacity
        # Estimate of how much the user can save based on income and saving frequency
        # This amplifies income differences by combining with saving behavior
        df_transformed['savings_capacity'] = (df_transformed['income'] * df_transformed['saving_frequency']) / 100
        
        # Derived feature 3: Financial health score
        # Composite score combining multiple factors
        # Higher income, lower spending, higher saving frequency, lower loan behavior = better health
        # Increased income weight to better differentiate income brackets
        income_normalized = df_transformed['income'] / 200000  # Normalize to 0-1
        spending_normalized = 1 - (df_transformed['spending_score'] / 100)  # Invert so lower is better
        saving_normalized = df_transformed['saving_frequency'] / 10
        loan_normalized = 1 - (df_transformed['loan_behavior'] / 5)  # Invert so lower is better
        
        # Increased income weight from 0.3 to 0.4 to better separate income brackets
        df_transformed['financial_health_score'] = (
            income_normalized * 0.4 +
            spending_normalized * 0.2 +
            saving_normalized * 0.2 +
            loan_normalized * 0.2
        ) * 100  # Scale to 0-100
        
        logger.info(f"Feature engineering complete. Added {len(DERIVED_FEATURES)} derived features")
        
        return df_transformed
    
    def get_feature_names(self) -> list:
        """Get list of all feature names after transformation."""
        return BASE_FEATURES + DERIVED_FEATURES
