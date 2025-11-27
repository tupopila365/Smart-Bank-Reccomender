"""Training script for K-Means and Decision Tree models."""

import sys
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from models.trainer import ModelTrainer
from data.feature_engineering import FeatureEngineer
from utils import setup_logger

logger = setup_logger(__name__)


def main():
    """Main training pipeline execution."""
    logger.info("=" * 60)
    logger.info("Starting ML Model Training Pipeline")
    logger.info("=" * 60)
    
    # Load synthetic dataset
    data_path = Path(__file__).parent.parent / 'data' / 'synthetic_users.csv'
    logger.info(f"Loading dataset from {data_path}")
    
    if not data_path.exists():
        logger.error(f"Dataset not found at {data_path}")
        logger.error("Please run generate_data.py first to create the synthetic dataset")
        sys.exit(1)
    
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df)} samples with {len(df.columns)} columns")
    
    # Apply feature engineering if needed
    feature_engineer = FeatureEngineer()
    required_features = feature_engineer.get_feature_names()
    
    # Check if derived features already exist
    if not all(feat in df.columns for feat in required_features):
        logger.info("Applying feature engineering")
        df = feature_engineer.transform(df)
    else:
        logger.info("Derived features already present in dataset")
    
    # Initialize trainer
    logger.info("\nInitializing model trainer with 5 clusters")
    trainer = ModelTrainer(n_clusters=5, random_state=42)
    
    # Train all models
    logger.info("\n" + "=" * 60)
    logger.info("Training Models")
    logger.info("=" * 60)
    
    models_dict = trainer.train_all_models(df)
    
    # Print metrics summary
    logger.info("\n" + "=" * 60)
    logger.info("Training Metrics Summary")
    logger.info("=" * 60)
    
    logger.info("\nK-Means Clustering Metrics:")
    kmeans_metrics = models_dict['kmeans_metrics']
    logger.info(f"  Number of Clusters: {kmeans_metrics['n_clusters']}")
    logger.info(f"  Silhouette Score: {kmeans_metrics['silhouette_score']:.4f}")
    logger.info(f"  Inertia: {kmeans_metrics['inertia']:.2f}")
    
    logger.info("\nDecision Tree Classification Metrics:")
    for product_type, metrics in models_dict['decision_tree_metrics'].items():
        logger.info(f"\n  {product_type.upper()}:")
        logger.info(f"    Accuracy:  {metrics['accuracy']:.4f}")
        logger.info(f"    Precision: {metrics['precision']:.4f}")
        logger.info(f"    Recall:    {metrics['recall']:.4f}")
        logger.info(f"    F1 Score:  {metrics['f1_score']:.4f}")
        logger.info(f"    Classes:   {metrics['n_classes']}")
    
    # Save models
    logger.info("\n" + "=" * 60)
    logger.info("Saving Models")
    logger.info("=" * 60)
    
    models_dir = Path(__file__).parent.parent / 'models'
    trainer.save_models(models_dict, output_dir=str(models_dir))
    
    logger.info("\n" + "=" * 60)
    logger.info("Training Pipeline Complete!")
    logger.info("=" * 60)
    logger.info(f"\nModels saved to: {models_dir}")
    logger.info("\nYou can now start the ML service API with:")
    logger.info("  cd ml-service")
    logger.info("  uvicorn src.api.main:app --reload")


if __name__ == "__main__":
    main()
