"""Model training module for K-Means clustering and Decision Tree classification."""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from typing import Tuple, Dict, Any
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, accuracy_score, precision_score, recall_score, f1_score

try:
    from ..utils import ALL_FEATURES, PRODUCT_MAPPING, setup_logger
except ImportError:
    from utils import ALL_FEATURES, PRODUCT_MAPPING, setup_logger

logger = setup_logger(__name__)


class ModelTrainer:
    """Train K-Means clustering and Decision Tree models."""
    
    def __init__(self, n_clusters: int = 5, random_state: int = 42):
        """
        Initialize the model trainer.
        
        Args:
            n_clusters: Number of clusters for K-Means (4-6 recommended)
            random_state: Random state for reproducibility
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.kmeans = None
        self.decision_trees = {}
        
    def train_kmeans(self, X: np.ndarray) -> Tuple[KMeans, Dict[str, float]]:
        """
        Train K-Means clustering model.
        
        Args:
            X: Feature matrix (n_samples, n_features)
        
        Returns:
            Tuple of (trained model, metrics dict)
        """
        logger.info(f"Training K-Means with {self.n_clusters} clusters")
        
        # Scale features for K-Means
        X_scaled = self.scaler.fit_transform(X)
        
        # Train K-Means
        self.kmeans = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10,
            max_iter=300
        )
        self.kmeans.fit(X_scaled)
        
        # Calculate metrics
        silhouette = silhouette_score(X_scaled, self.kmeans.labels_)
        inertia = self.kmeans.inertia_
        
        metrics = {
            'silhouette_score': silhouette,
            'inertia': inertia,
            'n_clusters': self.n_clusters
        }
        
        logger.info(f"K-Means training complete. Silhouette score: {silhouette:.4f}, Inertia: {inertia:.2f}")
        
        return self.kmeans, metrics
    
    def train_decision_tree(
        self, 
        X: np.ndarray, 
        y: np.ndarray,
        product_type: str,
        max_depth: int = 8,
        min_samples_split: int = 30
    ) -> Tuple[DecisionTreeClassifier, Dict[str, float]]:
        """
        Train Decision Tree classifier for a specific product type.
        
        Args:
            X: Feature matrix including cluster assignments
            y: Target labels
            product_type: Type of product ('account', 'savings', 'loan', 'digital_service')
            max_depth: Maximum depth of the tree
            min_samples_split: Minimum samples required to split a node
        
        Returns:
            Tuple of (trained model, metrics dict)
        """
        logger.info(f"Training Decision Tree for {product_type}")
        
        # Train Decision Tree
        dt = DecisionTreeClassifier(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=self.random_state
        )
        dt.fit(X, y)
        
        # Calculate metrics
        y_pred = dt.predict(X)
        accuracy = accuracy_score(y, y_pred)
        
        # Calculate precision, recall, F1 with average='weighted' for multiclass
        precision = precision_score(y, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y, y_pred, average='weighted', zero_division=0)
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'n_classes': len(np.unique(y))
        }
        
        logger.info(
            f"Decision Tree training complete for {product_type}. "
            f"Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, "
            f"Recall: {recall:.4f}, F1: {f1:.4f}"
        )
        
        self.decision_trees[product_type] = dt
        
        return dt, metrics
    
    def train_all_models(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Train all models (K-Means + Decision Trees for all product types).
        
        Args:
            df: DataFrame with features and target labels
        
        Returns:
            Dictionary containing all models and their metrics
        """
        logger.info("Starting complete training pipeline")
        
        # Extract features for clustering
        X_features = df[ALL_FEATURES].values
        
        # Train K-Means
        kmeans_model, kmeans_metrics = self.train_kmeans(X_features)
        
        # Get cluster assignments
        X_scaled = self.scaler.transform(X_features)
        cluster_labels = kmeans_model.predict(X_scaled)
        
        # Add cluster as a feature for Decision Trees
        X_with_clusters = np.column_stack([X_features, cluster_labels])
        
        # Train Decision Trees for each product type
        dt_models = {}
        dt_metrics = {}
        
        for product_type in ['account', 'savings', 'loan', 'digital_service']:
            target_col = f'target_{product_type}'
            if target_col in df.columns:
                y = df[target_col].values
                model, metrics = self.train_decision_tree(X_with_clusters, y, product_type)
                dt_models[product_type] = model
                dt_metrics[product_type] = metrics
        
        logger.info("Complete training pipeline finished")
        
        return {
            'kmeans': kmeans_model,
            'scaler': self.scaler,
            'decision_trees': dt_models,
            'kmeans_metrics': kmeans_metrics,
            'decision_tree_metrics': dt_metrics
        }
    
    def save_models(self, models_dict: Dict[str, Any], output_dir: str = 'models'):
        """
        Save all trained models to disk using joblib.
        
        Args:
            models_dict: Dictionary containing all models
            output_dir: Directory to save models
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving models to {output_path}")
        
        # Save K-Means model
        kmeans_path = output_path / 'kmeans_model.joblib'
        joblib.dump(models_dict['kmeans'], kmeans_path)
        logger.info(f"Saved K-Means model to {kmeans_path}")
        
        # Save scaler
        scaler_path = output_path / 'scaler.joblib'
        joblib.dump(models_dict['scaler'], scaler_path)
        logger.info(f"Saved scaler to {scaler_path}")
        
        # Save Decision Tree models
        for product_type, model in models_dict['decision_trees'].items():
            dt_path = output_path / f'decision_tree_{product_type}.joblib'
            joblib.dump(model, dt_path)
            logger.info(f"Saved Decision Tree for {product_type} to {dt_path}")
        
        logger.info("All models saved successfully")
    
    def load_models(self, models_dir: str = 'models') -> Dict[str, Any]:
        """
        Load all trained models from disk.
        
        Args:
            models_dir: Directory containing saved models
        
        Returns:
            Dictionary containing all loaded models
        """
        models_path = Path(models_dir)
        
        logger.info(f"Loading models from {models_path}")
        
        # Load K-Means model
        kmeans_path = models_path / 'kmeans_model.joblib'
        kmeans = joblib.load(kmeans_path)
        logger.info(f"Loaded K-Means model from {kmeans_path}")
        
        # Load scaler
        scaler_path = models_path / 'scaler.joblib'
        scaler = joblib.load(scaler_path)
        logger.info(f"Loaded scaler from {scaler_path}")
        
        # Load Decision Tree models
        decision_trees = {}
        for product_type in ['account', 'savings', 'loan', 'digital_service']:
            dt_path = models_path / f'decision_tree_{product_type}.joblib'
            if dt_path.exists():
                decision_trees[product_type] = joblib.load(dt_path)
                logger.info(f"Loaded Decision Tree for {product_type} from {dt_path}")
        
        logger.info("All models loaded successfully")
        
        return {
            'kmeans': kmeans,
            'scaler': scaler,
            'decision_trees': decision_trees
        }
