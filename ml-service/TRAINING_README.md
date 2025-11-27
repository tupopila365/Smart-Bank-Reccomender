# ML Model Training Guide

This guide explains how to train the K-Means clustering and Decision Tree classification models for the SmartBank Recommender system.

## Overview

The training pipeline consists of:
1. **K-Means Clustering**: Segments users into 5 distinct financial behavior groups
2. **Decision Tree Classifiers**: Predicts optimal banking products for each user segment
   - Account recommendations
   - Savings product recommendations
   - Loan recommendations
   - Digital service recommendations

## Prerequisites

Ensure you have:
- Python 3.9+
- All dependencies installed: `pip install -r requirements.txt`
- Synthetic dataset generated: `python scripts/generate_data.py`

## Training the Models

### Quick Start

Train all models with default settings:

```bash
cd ml-service
python scripts/train_models.py
```

This will:
1. Load the synthetic dataset from `data/synthetic_users.csv`
2. Apply feature engineering (if not already done)
3. Train K-Means clustering model (5 clusters)
4. Train Decision Tree classifiers for all product types
5. Save all models to `models/` directory

### Output

The training script saves the following files to `models/`:
- `kmeans_model.joblib` - K-Means clustering model
- `scaler.joblib` - StandardScaler for feature normalization
- `decision_tree_account.joblib` - Account recommendation model
- `decision_tree_savings.joblib` - Savings product recommendation model
- `decision_tree_loan.joblib` - Loan recommendation model
- `decision_tree_digital_service.joblib` - Digital service recommendation model

### Training Metrics

The training script outputs:

**K-Means Metrics:**
- Silhouette Score: Measures cluster quality (-1 to 1, higher is better)
- Inertia: Within-cluster sum of squares (lower is better)
- Number of Clusters: 5

**Decision Tree Metrics (for each product type):**
- Accuracy: Overall prediction accuracy
- Precision: Weighted precision across all classes
- Recall: Weighted recall across all classes
- F1 Score: Harmonic mean of precision and recall

## Model Evaluation

For detailed evaluation with classification reports and confusion matrices:

```bash
python scripts/evaluate_models.py
```

This provides:
- Detailed clustering quality metrics (Silhouette, Davies-Bouldin, Calinski-Harabasz)
- Cluster size distribution
- Per-class precision, recall, and F1 scores for each product type
- Confusion matrices showing prediction patterns

## Model Architecture

### K-Means Clustering

**Configuration:**
- Number of clusters: 5
- Features: All 7 features (4 base + 3 derived)
- Preprocessing: StandardScaler normalization
- Initialization: k-means++ (10 runs)
- Max iterations: 300

**Features Used:**
1. income
2. spending_score
3. saving_frequency
4. loan_behavior
5. income_to_spending_ratio (derived)
6. savings_capacity (derived)
7. financial_health_score (derived)

### Decision Tree Classifiers

**Configuration:**
- Max depth: 8
- Min samples split: 30
- Features: 7 base features + cluster assignment
- Criterion: Gini impurity

**Product Types:**
1. **Account**: 4 classes (Basic, Premium, Student, Business)
2. **Savings**: 4 classes (Standard, High-Yield, Money Market, CD)
3. **Loan**: 4 classes (Personal, Mortgage, Auto, None)
4. **Digital Service**: 4 classes (Basic Mobile, Premium Digital, Investment, Budgeting)

## Testing Predictions

Test the trained models with a sample profile:

```bash
python test_prediction.py
```

This loads the models and makes predictions for a sample user profile.

## Retraining

To retrain models with different parameters:

1. Edit `ml-service/src/models/trainer.py` to adjust hyperparameters
2. Run the training script again
3. Models will be overwritten in the `models/` directory

## Model Persistence

Models are saved using `joblib` for efficient serialization:
- Fast loading times
- Preserves scikit-learn model state
- Compatible with the prediction API

## Next Steps

After training:
1. Start the ML Service API: `uvicorn src.api.main:app --reload`
2. Test predictions via the `/predict` endpoint
3. Integrate with the Backend Service

## Troubleshooting

**Issue: "Dataset not found"**
- Solution: Run `python scripts/generate_data.py` first

**Issue: "Models directory not found" (during evaluation)**
- Solution: Run `python scripts/train_models.py` first

**Issue: Import errors**
- Solution: Ensure you're running from the `ml-service` directory
- Solution: Check that all dependencies are installed

## Performance Notes

- Training time: ~2-5 seconds on typical hardware
- Dataset size: 500-1000 samples
- Model file sizes: ~50-200 KB total
- Prediction latency: <10ms per request
