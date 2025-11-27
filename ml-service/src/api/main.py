"""FastAPI application main entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoints import router
from ..utils import setup_logger
from ..models.predictor import ModelPredictor

logger = setup_logger(__name__)

app = FastAPI(
    title="SmartBank ML Service",
    description="Machine learning service for personalized banking recommendations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global predictor instance
predictor = None

# Include API routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    global predictor
    logger.info("ML Service starting up")
    
    try:
        # Load models at startup
        predictor = ModelPredictor()
        logger.info("Models loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load models at startup: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("ML Service shutting down")


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns service status and model loading state.
    Returns 200 OK if service is healthy, 503 if degraded.
    """
    models_loaded = predictor is not None and predictor.is_loaded()
    
    status_code = 200 if models_loaded else 503
    
    from fastapi import Response
    
    return Response(
        content='{"status":"ok","service":"ml-service","models_loaded":true}' if models_loaded else '{"status":"degraded","service":"ml-service","models_loaded":false}',
        status_code=status_code,
        media_type="application/json"
    )
