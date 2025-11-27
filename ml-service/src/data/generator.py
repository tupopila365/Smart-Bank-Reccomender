"""Synthetic dataset generator for training ML models."""

import numpy as np
import pandas as pd
from typing import Optional

try:
    from ..utils import MIN_SAMPLES, MAX_SAMPLES, setup_logger
except ImportError:
    from utils import MIN_SAMPLES, MAX_SAMPLES, setup_logger

logger = setup_logger(__name__)


class SyntheticDataGenerator:
    """Generate synthetic user profiles with realistic distributions."""
    
    def __init__(self, random_state: Optional[int] = 42):
        """Initialize the generator with a random state for reproducibility."""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def generate(self, n_samples: Optional[int] = None) -> pd.DataFrame:
        """
        Generate synthetic user profiles.
        
        Args:
            n_samples: Number of samples to generate. If None, randomly choose between MIN_SAMPLES and MAX_SAMPLES.
        
        Returns:
            DataFrame with synthetic user profiles.
        """
        if n_samples is None:
            n_samples = self.rng.randint(MIN_SAMPLES, MAX_SAMPLES + 1)
        
        logger.info(f"Generating {n_samples} synthetic user profiles")
        
        # Generate base features with realistic distributions
        data = {
            'user_id': range(1, n_samples + 1),
            'income': self._generate_income(n_samples),
            'spending_score': self._generate_spending_score(n_samples),
            'saving_frequency': self._generate_saving_frequency(n_samples),
            'loan_behavior': self._generate_loan_behavior(n_samples),
            'age_group': self._generate_age_group(n_samples),
            'employment_type': self._generate_employment_type(n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Generate target labels based on patterns
        df['target_account'] = self._generate_account_labels(df)
        df['target_savings'] = self._generate_savings_labels(df)
        df['target_loan'] = self._generate_loan_labels(df)
        df['target_digital_service'] = self._generate_digital_service_labels(df)
        
        logger.info(f"Successfully generated {len(df)} user profiles")
        return df
    
    def _generate_income(self, n: int) -> np.ndarray:
        """Generate income with log-normal distribution."""
        # Log-normal distribution for realistic income distribution
        mean_log = 10.5  # Approximately $36,000 median
        std_log = 0.8
        income = self.rng.lognormal(mean_log, std_log, n)
        # Clip to reasonable range
        return np.clip(income, 15000, 200000)
    
    def _generate_spending_score(self, n: int) -> np.ndarray:
        """Generate spending score with normal distribution."""
        # Normal distribution centered around 50
        spending = self.rng.normal(50, 20, n)
        return np.clip(spending, 0, 100)
    
    def _generate_saving_frequency(self, n: int) -> np.ndarray:
        """Generate saving frequency with beta distribution."""
        # Beta distribution skewed towards lower values (most people save less frequently)
        saving = self.rng.beta(2, 5, n) * 10
        return np.clip(saving, 0, 10)
    
    def _generate_loan_behavior(self, n: int) -> np.ndarray:
        """Generate loan behavior with discrete distribution."""
        # Most people have low loan behavior
        return self.rng.choice([0, 1, 2, 3, 4, 5], n, p=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03])
    
    def _generate_age_group(self, n: int) -> np.ndarray:
        """Generate age group (auxiliary feature)."""
        # 0: 18-25, 1: 26-35, 2: 36-45, 3: 46-55, 4: 56+
        return self.rng.choice([0, 1, 2, 3, 4], n, p=[0.15, 0.25, 0.25, 0.20, 0.15])
    
    def _generate_employment_type(self, n: int) -> np.ndarray:
        """Generate employment type (auxiliary feature)."""
        # 0: Full-time, 1: Part-time, 2: Self-employed, 3: Student, 4: Retired
        return self.rng.choice([0, 1, 2, 3, 4], n, p=[0.50, 0.15, 0.15, 0.10, 0.10])
    
    def _generate_account_labels(self, df: pd.DataFrame) -> np.ndarray:
        """Generate account type labels based on income and age with clearer income tiers."""
        labels = np.zeros(len(df), dtype=int)
        
        # Student Account: low income (<$35k), young age
        labels[(df['income'] < 35000) & (df['age_group'] <= 1)] = 2
        
        # Basic Checking: low to medium income (<$55k)
        labels[(df['income'] < 55000) & (labels == 0)] = 0
        
        # Business Account: high income (>$90k), self-employed
        labels[(df['income'] > 90000) & (df['employment_type'] == 2)] = 3
        
        # Premium Checking: high income (>$75k)
        labels[(df['income'] > 75000) & (labels == 0)] = 1
        
        return labels
    
    def _generate_savings_labels(self, df: pd.DataFrame) -> np.ndarray:
        """Generate savings product labels based on income and saving frequency with clearer tiers."""
        labels = np.zeros(len(df), dtype=int)
        
        # Standard Savings: low saving frequency OR low income
        labels[(df['saving_frequency'] < 3) | (df['income'] < 35000)] = 0
        
        # High-Yield Savings: medium saving frequency and medium income
        labels[(df['saving_frequency'] >= 3) & (df['saving_frequency'] < 7) & 
               (df['income'] >= 35000) & (df['income'] < 70000)] = 1
        
        # Money Market: high saving frequency and good income
        labels[(df['saving_frequency'] >= 7) & (df['income'] >= 70000) & (df['income'] < 100000)] = 2
        
        # Certificate of Deposit: very high saving frequency and high income
        labels[(df['saving_frequency'] >= 8) & (df['income'] >= 100000)] = 3
        
        return labels
    
    def _generate_loan_labels(self, df: pd.DataFrame) -> np.ndarray:
        """Generate loan product labels based on loan behavior and income."""
        labels = np.zeros(len(df), dtype=int)
        
        # No Loan Recommended: low loan behavior
        labels[df['loan_behavior'] <= 1] = 3
        
        # Personal Loan: medium loan behavior, lower income
        labels[(df['loan_behavior'] >= 2) & (df['loan_behavior'] <= 3) & (df['income'] < 60000)] = 0
        
        # Auto Loan: medium loan behavior, medium income
        labels[(df['loan_behavior'] >= 2) & (df['loan_behavior'] <= 3) & (df['income'] >= 60000)] = 2
        
        # Home Mortgage: high loan behavior, high income
        labels[(df['loan_behavior'] >= 4) & (df['income'] > 70000)] = 1
        
        return labels
    
    def _generate_digital_service_labels(self, df: pd.DataFrame) -> np.ndarray:
        """Generate digital service labels based on age and income with clearer income tiers."""
        labels = np.zeros(len(df), dtype=int)
        
        # Basic Mobile Banking: older age groups OR low income
        labels[(df['age_group'] >= 3) | (df['income'] < 35000)] = 0
        
        # Budgeting Tools: younger age, lower to medium income
        labels[(df['age_group'] <= 1) & (df['income'] >= 35000) & (df['income'] < 60000)] = 3
        
        # Investment Platform: high income (>$90k)
        labels[df['income'] > 90000] = 2
        
        # Premium Digital Banking: medium to high income ($60k-$90k)
        labels[(df['income'] >= 60000) & (df['income'] <= 90000) & (labels == 0)] = 1
        
        return labels
