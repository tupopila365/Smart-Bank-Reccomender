"""
Demo: Complete ML Training Pipeline

This script demonstrates the complete training pipeline from data loading
to model training, evaluation, and prediction.
"""

import sys
import numpy as np
sys.path.insert(0, 'src')

from models.trainer import ModelTrainer
from data.feature_engineering import FeatureEngineer
from utils import PRODUCT_MAPPING
import pandas as pd

print("=" * 70)
print("SMARTBANK RECOMMENDER - ML TRAINING PIPELINE DEMO")
print("=" * 70)

# Step 1: Load dataset
print("\n[STEP 1] Loading synthetic dataset...")
df = pd.read_csv('data/synthetic_users.csv')
print(f"✓ Loaded {len(df)} user profiles")
print(f"✓ Features: {list(df.columns[:7])}")

# Step 2: Feature engineering
print("\n[STEP 2] Checking feature engineering...")
fe = FeatureEngineer()
if 'financial_health_score' not in df.columns:
    print("✓ Applying feature engineering...")
    df = fe.transform(df)
else:
    print("✓ Derived features already present")

# Step 3: Initialize trainer
print("\n[STEP 3] Initializing model trainer...")
trainer = ModelTrainer(n_clusters=5, random_state=42)
print("✓ Trainer initialized with 5 clusters")

# Step 4: Train models
print("\n[STEP 4] Training models...")
print("  - Training K-Means clustering...")
print("  - Training Decision Tree classifiers...")
models_dict = trainer.train_all_models(df)
print("✓ All models trained successfully")

# Step 5: Display metrics
print("\n[STEP 5] Training Metrics:")
print("\n  K-Means Clustering:")
km_metrics = models_dict['kmeans_metrics']
print(f"    Silhouette Score: {km_metrics['silhouette_score']:.4f}")
print(f"    Inertia: {km_metrics['inertia']:.2f}")
print(f"    Clusters: {km_metrics['n_clusters']}")

print("\n  Decision Tree Classifiers:")
for product_type, metrics in models_dict['decision_tree_metrics'].items():
    print(f"\n    {product_type.upper()}:")
    print(f"      Accuracy:  {metrics['accuracy']:.4f}")
    print(f"      Precision: {metrics['precision']:.4f}")
    print(f"      Recall:    {metrics['recall']:.4f}")
    print(f"      F1 Score:  {metrics['f1_score']:.4f}")

# Step 6: Save models
print("\n[STEP 6] Saving models...")
trainer.save_models(models_dict, output_dir='models')
print("✓ All models saved to models/ directory")

# Step 7: Test prediction
print("\n[STEP 7] Testing prediction with sample profile...")
sample_profile = {
    'income': 75000,
    'spending_score': 55,
    'saving_frequency': 6,
    'loan_behavior': 1
}

print(f"\n  Sample User Profile:")
print(f"    Income: ${sample_profile['income']:,}")
print(f"    Spending Score: {sample_profile['spending_score']}/100")
print(f"    Saving Frequency: {sample_profile['saving_frequency']}/10")
print(f"    Loan Behavior: {sample_profile['loan_behavior']}/5")

# Calculate derived features
income_to_spending_ratio = sample_profile['income'] / (sample_profile['spending_score'] + 1)
savings_capacity = (sample_profile['income'] * sample_profile['saving_frequency']) / 100
income_normalized = sample_profile['income'] / 200000
spending_normalized = 1 - (sample_profile['spending_score'] / 100)
saving_normalized = sample_profile['saving_frequency'] / 10
loan_normalized = 1 - (sample_profile['loan_behavior'] / 5)
financial_health_score = (
    income_normalized * 0.3 +
    spending_normalized * 0.25 +
    saving_normalized * 0.25 +
    loan_normalized * 0.2
) * 100

# Create feature vector
features = np.array([[
    sample_profile['income'],
    sample_profile['spending_score'],
    sample_profile['saving_frequency'],
    sample_profile['loan_behavior'],
    income_to_spending_ratio,
    savings_capacity,
    financial_health_score
]])

# Predict cluster
features_scaled = models_dict['scaler'].transform(features)
cluster = models_dict['kmeans'].predict(features_scaled)[0]

# Predict products
features_with_cluster = np.column_stack([features, cluster])

print(f"\n  Predictions:")
print(f"    User Segment: Cluster {cluster}")

for product_type, model in models_dict['decision_trees'].items():
    prediction = model.predict(features_with_cluster)[0]
    product_name = PRODUCT_MAPPING[product_type][prediction]
    print(f"    {product_type.title()}: {product_name}")

# Final summary
print("\n" + "=" * 70)
print("DEMO COMPLETE!")
print("=" * 70)
print("\nThe ML training pipeline is fully operational and ready for:")
print("  • Integration with the ML Service API")
print("  • Real-time predictions via /predict endpoint")
print("  • Backend service integration")
print("\nNext: Run 'uvicorn src.api.main:app --reload' to start the API")
print("=" * 70)
