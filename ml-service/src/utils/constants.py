"""Constants for the ML service."""

# Feature names
BASE_FEATURES = ['income', 'spending_score', 'saving_frequency', 'loan_behavior']
DERIVED_FEATURES = ['income_to_spending_ratio', 'savings_capacity', 'financial_health_score']
ALL_FEATURES = BASE_FEATURES + DERIVED_FEATURES

# Data generation parameters
MIN_SAMPLES = 500
MAX_SAMPLES = 1000

# Feature ranges for validation
FEATURE_RANGES = {
    'income': (0, 200000),
    'spending_score': (0, 100),
    'saving_frequency': (0, 10),
    'loan_behavior': (0, 5)
}

# Product mappings
PRODUCT_MAPPING = {
    'account': {
        0: 'Basic Checking Account',
        1: 'Premium Checking Account',
        2: 'Student Account',
        3: 'Business Account'
    },
    'savings': {
        0: 'Standard Savings Account',
        1: 'High-Yield Savings Account',
        2: 'Money Market Account',
        3: 'Certificate of Deposit'
    },
    'loan': {
        0: 'Personal Loan',
        1: 'Home Mortgage',
        2: 'Auto Loan',
        3: 'No Loan Recommended'
    },
    'digital_service': {
        0: 'Basic Mobile Banking',
        1: 'Premium Digital Banking',
        2: 'Investment Platform',
        3: 'Budgeting Tools'
    }
}
