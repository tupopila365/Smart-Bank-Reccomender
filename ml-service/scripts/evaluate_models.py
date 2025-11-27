"""Model evaluation script with detailed metrics and analysis."""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from models.trainer import ModelTrainer
from data.feature_engineering import FeatureEngineer
from utils import ALL_FEATURES, PRODUCT_MAPPING, setup_logger

logger = setup_logger(__name__)


def evaluate_clustering(kmeans, scaler, X, labels):
    """Evaluate clustering quality."""
    from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
    
    X_scaled = scaler.transform(X)
    
    silhouette = silhouette_score(X_scaled, labels)
    davies_bouldin = davies_bouldin_score(X_scaled, labels)
    calinski_harabasz = calinski_harabasz_score(X_scaled, labels)
    
    logger.info("\nClustering Quality Metrics:")
    logger.info(f"  Silhouette Score: {silhouette:.4f} (higher is better, range: -1 to 1)")
    logger.info(f"  Davies-Bouldin Index: {davies_bouldin:.4f} (lower is better)")
    logger.info(f"  Calinski-Harabasz Score: {calinski_harabasz:.2f} (higher is better)")
    
    # Cluster size distribution
    unique, counts = np.unique(labels, return_counts=True)
    logger.info("\nCluster Size Distribution:")
    for cluster_id, count in zip(unique, counts):
        percentage = (count / len(labels)) * 100
        logger.info(f"  Cluster {cluster_id}: {count} samples ({percentage:.1f}%)")


def evaluate_classifier(model, X, y, product_type):
    """Evaluate classifier with detailed metrics."""
    y_pred = model.predict(X)
    
    logger.info(f"\n{'=' * 60}")
    logger.info(f"Detailed Evaluation: {product_type.upper()}")
    logger.info(f"{'=' * 60}")
    
    # Get unique classes in the data
    unique_classes = sorted(np.unique(y))
    
    # Classification report
    logger.info("\nClassification Report:")
    try:
        target_names = [PRODUCT_MAPPING[product_type].get(i, f"Class {i}") for i in unique_classes]
        report = classification_report(
            y, y_pred,
            labels=unique_classes,
            target_names=target_names,
            zero_division=0
        )
        logger.info(f"\n{report}")
    except Exception as e:
        logger.error(f"Error generating classification report: {e}")
    
    # Confusion matrix
    cm = confusion_matrix(y, y_pred)
    logger.info("\nConfusion Matrix:")
    logger.info(f"{cm}")


def main():
    """Main evaluation pipeline."""
    logger.info("=" * 60)
    logger.info("Model Evaluation Pipeline")
    logger.info("=" * 60)
    
    # Load dataset
    data_path = Path(__file__).parent.parent / 'data' / 'synthetic_users.csv'
    logger.info(f"\nLoading dataset from {data_path}")
    
    if not data_path.exists():
        logger.error(f"Dataset not found at {data_path}")
        sys.exit(1)
    
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df)} samples")
    
    # Apply feature engineering if needed
    feature_engineer = FeatureEngineer()
    required_features = feature_engineer.get_feature_names()
    
    if not all(feat in df.columns for feat in required_features):
        logger.info("Applying feature engineering")
        df = feature_engineer.transform(df)
    
    # Load trained models
    models_dir = Path(__file__).parent.parent / 'models'
    logger.info(f"\nLoading models from {models_dir}")
    
    if not models_dir.exists():
        logger.error(f"Models directory not found at {models_dir}")
        logger.error("Please run train_models.py first")
        sys.exit(1)
    
    trainer = ModelTrainer()
    models_dict = trainer.load_models(str(models_dir))
    
    # Extract features
    X_features = df[ALL_FEATURES].values
    
    # Evaluate K-Means
    logger.info("\n" + "=" * 60)
    logger.info("K-Means Clustering Evaluation")
    logger.info("=" * 60)
    
    X_scaled = models_dict['scaler'].transform(X_features)
    cluster_labels = models_dict['kmeans'].predict(X_scaled)
    evaluate_clustering(models_dict['kmeans'], models_dict['scaler'], X_features, cluster_labels)
    
    # Evaluate Decision Trees
    logger.info("\n" + "=" * 60)
    logger.info("Decision Tree Classification Evaluation")
    logger.info("=" * 60)
    
    X_with_clusters = np.column_stack([X_features, cluster_labels])
    
    for product_type in ['account', 'savings', 'loan', 'digital_service']:
        target_col = f'target_{product_type}'
        if target_col in df.columns and product_type in models_dict['decision_trees']:
            y = df[target_col].values
            model = models_dict['decision_trees'][product_type]
            evaluate_classifier(model, X_with_clusters, y, product_type)
    
    logger.info("\n" + "=" * 60)
    logger.info("Evaluation Complete!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
