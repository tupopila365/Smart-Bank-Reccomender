"""Model predictor for generating banking recommendations."""

import os
import joblib
import numpy as np
from typing import Dict

try:
    from ..utils import setup_logger, PRODUCT_MAPPING
    from ..data.feature_engineering import FeatureEngineer
except ImportError:
    from utils import setup_logger, PRODUCT_MAPPING
    from data.feature_engineering import FeatureEngineer

logger = setup_logger(__name__)


class ModelPredictor:
    """Handles model loading and prediction pipeline."""
    
    def __init__(self, model_path: str = "models"):
        """
        Initialize predictor and load trained models.
        
        Args:
            model_path: Directory containing trained model files
        """
        self.model_path = model_path
        self.kmeans = None
        self.scaler = None
        self.decision_trees = {}
        self.feature_engineer = FeatureEngineer()
        
        self._load_models()
    
    def _load_models(self):
        """Load all trained models from disk."""
        try:
            # Load K-Means clustering model
            kmeans_path = os.path.join(self.model_path, "kmeans_model.joblib")
            self.kmeans = joblib.load(kmeans_path)
            logger.info(f"Loaded K-Means model from {kmeans_path}")
            
            # Load scaler
            scaler_path = os.path.join(self.model_path, "scaler.joblib")
            self.scaler = joblib.load(scaler_path)
            logger.info(f"Loaded scaler from {scaler_path}")
            
            # Load Decision Tree models for each product category
            product_categories = ['account', 'savings', 'loan', 'digital_service']
            for category in product_categories:
                dt_path = os.path.join(self.model_path, f"decision_tree_{category}.joblib")
                self.decision_trees[category] = joblib.load(dt_path)
                logger.info(f"Loaded Decision Tree model for {category} from {dt_path}")
            
            logger.info("All models loaded successfully")
            
        except FileNotFoundError as e:
            logger.error(f"Model file not found: {e}")
            raise RuntimeError(f"Failed to load models: {e}. Ensure models are trained and saved.")
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise RuntimeError(f"Failed to load models: {e}")
    
    def predict(self, income: float, spending_score: float, 
                saving_frequency: float, loan_behavior: float) -> Dict:
        """
        Generate personalized banking recommendations.
        
        Args:
            income: Annual income
            spending_score: Spending behavior score (0-100)
            saving_frequency: Monthly saving frequency (0-10)
            loan_behavior: Loan usage pattern (0-5)
        
        Returns:
            Dictionary with recommended products and cluster segment
        """
        try:
            # Step 1: Create feature array from input
            import pandas as pd
            input_df = pd.DataFrame([{
                'income': income,
                'spending_score': spending_score,
                'saving_frequency': saving_frequency,
                'loan_behavior': loan_behavior
            }])
            
            # Step 2: Apply feature engineering
            features_df = self.feature_engineer.transform(input_df)
            logger.info(f"Engineered features: {features_df.to_dict('records')[0]}")
            
            # Step 3: Scale features
            features_scaled = self.scaler.transform(features_df)
            
            # Step 4: Apply K-Means clustering to determine user segment
            cluster_segment = int(self.kmeans.predict(features_scaled)[0])
            logger.info(f"User assigned to cluster segment: {cluster_segment}")
            
            # Step 5: Add cluster as a feature for Decision Trees
            # Decision Trees were trained with features + cluster label
            features_with_cluster = np.column_stack([features_df.values, cluster_segment])
            
            # Step 6: Apply Decision Tree classifiers for each product category
            predictions = {}
            for category, model in self.decision_trees.items():
                prediction_idx = int(model.predict(features_with_cluster)[0])
                product_name = PRODUCT_MAPPING[category].get(
                    prediction_idx, 
                    f"Unknown {category.title()}"
                )
                predictions[f"recommended_{category}"] = product_name
                logger.info(f"Predicted {category}: {product_name}")
            
            # Step 7: Add cluster segment to response
            predictions['cluster_segment'] = cluster_segment
            
            return predictions
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise RuntimeError(f"Failed to generate predictions: {e}")
    
    def is_loaded(self) -> bool:
        """Check if all models are loaded."""
        return (
            self.kmeans is not None and 
            self.scaler is not None and 
            len(self.decision_trees) == 4
        )

