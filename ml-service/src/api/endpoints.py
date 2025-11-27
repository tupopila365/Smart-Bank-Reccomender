"""API endpoints for the ML service."""

from fastapi import APIRouter, HTTPException
from ..schemas import PredictionRequest, PredictionResponse
from ..utils import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Generate personalized banking recommendations based on user profile.
    
    Args:
        request: User financial profile with income, spending_score, 
                 saving_frequency, and loan_behavior
    
    Returns:
        Personalized product recommendations and cluster segment
    
    Raises:
        HTTPException: If models are not loaded or prediction fails
    """
    from .main import predictor
    
    logger.info(f"Received prediction request: {request.model_dump()}")
    
    # Check if models are loaded
    if predictor is None or not predictor.is_loaded():
        logger.error("Models not loaded")
        raise HTTPException(
            status_code=503,
            detail="ML models are not loaded. Service is not ready."
        )
    
    try:
        # Generate predictions using the model predictor
        predictions = predictor.predict(
            income=request.income,
            spending_score=request.spending_score,
            saving_frequency=request.saving_frequency,
            loan_behavior=request.loan_behavior
        )
        
        logger.info(f"Generated predictions: {predictions}")
        
        # Return response
        return PredictionResponse(**predictions)
        
    except ValueError as e:
        logger.error(f"Validation error during prediction: {e}")
        raise HTTPException(
            status_code=422,
            detail=f"Invalid input data: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
