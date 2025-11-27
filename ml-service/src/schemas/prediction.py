"""Pydantic schemas for API request/response validation."""

from pydantic import BaseModel, Field, field_validator


class PredictionRequest(BaseModel):
    """Request model for prediction endpoint."""
    
    income: float = Field(..., ge=0, le=200000, description="Annual income in currency units")
    spending_score: float = Field(..., ge=0, le=100, description="Spending behavior score")
    saving_frequency: float = Field(..., ge=0, le=10, description="Monthly saving frequency")
    loan_behavior: float = Field(..., ge=0, le=5, description="Loan usage pattern")
    
    @field_validator('income', 'spending_score', 'saving_frequency', 'loan_behavior')
    @classmethod
    def check_not_nan_or_inf(cls, v):
        """Ensure values are not NaN or infinite."""
        import math
        if math.isnan(v) or math.isinf(v):
            raise ValueError('Value cannot be NaN or infinite')
        return v


class PredictionResponse(BaseModel):
    """Response model for prediction endpoint."""
    
    recommended_account: str
    recommended_savings: str
    recommended_loan: str
    recommended_digital_service: str
    cluster_segment: int
