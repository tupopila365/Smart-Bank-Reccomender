"""Script to generate synthetic dataset for training."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data import SyntheticDataGenerator, FeatureEngineer, DataValidator
from src.utils import setup_logger

logger = setup_logger(__name__)


def main():
    """Generate synthetic dataset and save to CSV."""
    # Create data directory if it doesn't exist
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Generate synthetic data
    logger.info("Starting synthetic data generation")
    generator = SyntheticDataGenerator(random_state=42)
    df = generator.generate(n_samples=800)  # Generate 800 samples
    
    # Apply feature engineering
    logger.info("Applying feature engineering")
    engineer = FeatureEngineer()
    df_engineered = engineer.transform(df)
    
    # Validate the dataset
    logger.info("Validating dataset")
    validator = DataValidator()
    is_valid, errors = validator.validate_dataset(df_engineered, require_derived=True)
    
    if not is_valid:
        logger.error("Dataset validation failed!")
        for error in errors:
            logger.error(f"  - {error}")
        sys.exit(1)
    
    # Save to CSV
    output_path = data_dir / 'synthetic_users.csv'
    df_engineered.to_csv(output_path, index=False)
    logger.info(f"Dataset saved to {output_path}")
    logger.info(f"Dataset shape: {df_engineered.shape}")
    logger.info(f"Columns: {list(df_engineered.columns)}")
    
    # Print summary statistics
    logger.info("\nDataset Summary:")
    logger.info(f"  Total records: {len(df_engineered)}")
    logger.info(f"  Income range: ${df_engineered['income'].min():.2f} - ${df_engineered['income'].max():.2f}")
    logger.info(f"  Spending score range: {df_engineered['spending_score'].min():.2f} - {df_engineered['spending_score'].max():.2f}")
    logger.info(f"  Saving frequency range: {df_engineered['saving_frequency'].min():.2f} - {df_engineered['saving_frequency'].max():.2f}")
    logger.info(f"  Loan behavior range: {df_engineered['loan_behavior'].min():.2f} - {df_engineered['loan_behavior'].max():.2f}")
    
    logger.info("\nTarget distribution:")
    logger.info(f"  Account types: {df_engineered['target_account'].value_counts().to_dict()}")
    logger.info(f"  Savings types: {df_engineered['target_savings'].value_counts().to_dict()}")
    logger.info(f"  Loan types: {df_engineered['target_loan'].value_counts().to_dict()}")
    logger.info(f"  Digital service types: {df_engineered['target_digital_service'].value_counts().to_dict()}")


if __name__ == '__main__':
    main()
