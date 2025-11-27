"""Verification script for Task 2: ML Model Training Pipeline.

This script verifies that all requirements for Task 2 have been met:
- Requirement 9.1: K-Means clustering training
- Requirement 9.2: K-Means model persistence with joblib
- Requirement 9.3: Decision Tree classifier training
- Requirement 9.4: Decision Tree model persistence with joblib
- Requirement 9.5: Training metrics output
"""

import sys
import os
from pathlib import Path
import joblib

sys.path.insert(0, 'src')

print("=" * 70)
print("TASK 2 VERIFICATION: ML Model Training Pipeline")
print("=" * 70)

# Check 1: Verify models directory exists
print("\n[CHECK 1] Models directory exists...")
models_dir = Path('models')
if models_dir.exists():
    print("✅ PASS: models/ directory found")
else:
    print("❌ FAIL: models/ directory not found")
    sys.exit(1)

# Check 2: Verify K-Means model file exists (Requirement 9.2)
print("\n[CHECK 2] K-Means model file exists (Requirement 9.2)...")
kmeans_path = models_dir / 'kmeans_model.joblib'
if kmeans_path.exists():
    print(f"✅ PASS: {kmeans_path} exists")
    # Try loading it
    try:
        kmeans = joblib.load(kmeans_path)
        print(f"   Model type: {type(kmeans).__name__}")
        print(f"   Number of clusters: {kmeans.n_clusters}")
    except Exception as e:
        print(f"❌ FAIL: Could not load K-Means model: {e}")
        sys.exit(1)
else:
    print(f"❌ FAIL: {kmeans_path} not found")
    sys.exit(1)

# Check 3: Verify scaler exists
print("\n[CHECK 3] Scaler file exists...")
scaler_path = models_dir / 'scaler.joblib'
if scaler_path.exists():
    print(f"✅ PASS: {scaler_path} exists")
    try:
        scaler = joblib.load(scaler_path)
        print(f"   Scaler type: {type(scaler).__name__}")
    except Exception as e:
        print(f"❌ FAIL: Could not load scaler: {e}")
        sys.exit(1)
else:
    print(f"❌ FAIL: {scaler_path} not found")
    sys.exit(1)

# Check 4: Verify Decision Tree model files exist (Requirement 9.4)
print("\n[CHECK 4] Decision Tree model files exist (Requirement 9.4)...")
product_types = ['account', 'savings', 'loan', 'digital_service']
all_dt_exist = True

for product_type in product_types:
    dt_path = models_dir / f'decision_tree_{product_type}.joblib'
    if dt_path.exists():
        print(f"✅ PASS: {dt_path} exists")
        try:
            dt = joblib.load(dt_path)
            print(f"   Model type: {type(dt).__name__}")
            print(f"   Max depth: {dt.max_depth}")
        except Exception as e:
            print(f"❌ FAIL: Could not load Decision Tree for {product_type}: {e}")
            all_dt_exist = False
    else:
        print(f"❌ FAIL: {dt_path} not found")
        all_dt_exist = False

if not all_dt_exist:
    sys.exit(1)

# Check 5: Verify training scripts exist
print("\n[CHECK 5] Training scripts exist...")
train_script = Path('scripts/train_models.py')
eval_script = Path('scripts/evaluate_models.py')

if train_script.exists():
    print(f"✅ PASS: {train_script} exists")
else:
    print(f"❌ FAIL: {train_script} not found")
    sys.exit(1)

if eval_script.exists():
    print(f"✅ PASS: {eval_script} exists")
else:
    print(f"❌ FAIL: {eval_script} not found")
    sys.exit(1)

# Check 6: Verify ModelTrainer class exists and has required methods
print("\n[CHECK 6] ModelTrainer class has required methods...")
from models.trainer import ModelTrainer

required_methods = [
    'train_kmeans',           # Requirement 9.1
    'train_decision_tree',    # Requirement 9.3
    'train_all_models',       # Complete pipeline
    'save_models',            # Requirements 9.2, 9.4
    'load_models'             # For prediction service
]

trainer = ModelTrainer()
all_methods_exist = True

for method_name in required_methods:
    if hasattr(trainer, method_name):
        print(f"✅ PASS: ModelTrainer.{method_name}() exists")
    else:
        print(f"❌ FAIL: ModelTrainer.{method_name}() not found")
        all_methods_exist = False

if not all_methods_exist:
    sys.exit(1)

# Check 7: Verify metrics are computed (Requirement 9.5)
print("\n[CHECK 7] Training metrics computation (Requirement 9.5)...")
print("   Testing with sample data...")

import numpy as np
import pandas as pd

# Create minimal test data
test_data = pd.DataFrame({
    'income': np.random.uniform(20000, 100000, 100),
    'spending_score': np.random.uniform(0, 100, 100),
    'saving_frequency': np.random.uniform(0, 10, 100),
    'loan_behavior': np.random.randint(0, 6, 100),
    'income_to_spending_ratio': np.random.uniform(100, 2000, 100),
    'savings_capacity': np.random.uniform(0, 10000, 100),
    'financial_health_score': np.random.uniform(0, 100, 100),
    'target_account': np.random.randint(0, 4, 100),
    'target_savings': np.random.randint(0, 4, 100),
    'target_loan': np.random.randint(0, 4, 100),
    'target_digital_service': np.random.randint(0, 4, 100)
})

test_trainer = ModelTrainer(n_clusters=3, random_state=42)
X_test = test_data[['income', 'spending_score', 'saving_frequency', 'loan_behavior',
                     'income_to_spending_ratio', 'savings_capacity', 'financial_health_score']].values

# Test K-Means metrics
kmeans_model, kmeans_metrics = test_trainer.train_kmeans(X_test)

required_kmeans_metrics = ['silhouette_score', 'inertia', 'n_clusters']
for metric in required_kmeans_metrics:
    if metric in kmeans_metrics:
        print(f"✅ PASS: K-Means metric '{metric}' computed: {kmeans_metrics[metric]}")
    else:
        print(f"❌ FAIL: K-Means metric '{metric}' not found")
        sys.exit(1)

# Test Decision Tree metrics
X_scaled = test_trainer.scaler.transform(X_test)
clusters = kmeans_model.predict(X_scaled)
X_with_clusters = np.column_stack([X_test, clusters])
y_test = test_data['target_account'].values

dt_model, dt_metrics = test_trainer.train_decision_tree(X_with_clusters, y_test, 'account')

required_dt_metrics = ['accuracy', 'precision', 'recall', 'f1_score']
for metric in required_dt_metrics:
    if metric in dt_metrics:
        print(f"✅ PASS: Decision Tree metric '{metric}' computed: {dt_metrics[metric]:.4f}")
    else:
        print(f"❌ FAIL: Decision Tree metric '{metric}' not found")
        sys.exit(1)

# Final summary
print("\n" + "=" * 70)
print("VERIFICATION COMPLETE: ALL CHECKS PASSED ✅")
print("=" * 70)
print("\nTask 2 Requirements Met:")
print("  ✅ 9.1: K-Means clustering training script")
print("  ✅ 9.2: K-Means model persistence (kmeans_model.joblib)")
print("  ✅ 9.3: Decision Tree classifier training")
print("  ✅ 9.4: Decision Tree model persistence (decision_tree_*.joblib)")
print("  ✅ 9.5: Training metrics output (silhouette, accuracy, precision, recall)")
print("\nAll models trained and saved successfully!")
print(f"Models location: {models_dir.absolute()}")
