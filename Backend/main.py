"""
Main FastAPI application for the Cat Facts API.
"""
import logging
from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi import status
from typing import List

# Import our modules
from config import config
from database.supabase_db import SupabaseCatFactsDB
from services import CatFactsService, AIService
from Models import (
    CatFactResponse,
    CatFactListResponse,
    CatFactCreateRequest,
    CatFactCreateResponse,
    CatFactLikeResponse,
    CatFactDeleteResponse,
    HealthCheckResponse,
    AIRequest,
    ErrorResponse,
    SuccessResponse,
    ImportFactsRequest,
    ImportFactsResponse
)
from exceptions import (
    CatFactsException,
    DatabaseException,
    ValidationException,
    AIServiceException,
    ConfigurationException,
    ExternalAPIException,
    FactNotFoundException,
    DuplicateFactException
)

# Setup logging
config.setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
    docs_url="/docs" if config.DEBUG else None,
    redoc_url="/redoc" if config.DEBUG else None
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    **config.get_cors_config()
)

# Global service instances
cat_facts_service: CatFactsService = None
ai_service: AIService = None


def get_cat_facts_service() -> CatFactsService:
    """Dependency to get cat facts service."""
    if cat_facts_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cat facts service not initialized"
        )
    return cat_facts_service


def get_ai_service() -> AIService:
    """Dependency to get AI service."""
    if ai_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service not initialized"
        )
    return ai_service


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global cat_facts_service, ai_service
    
    try:
        # Validate configuration
        if not config.validate():
            logger.error("Configuration validation failed")
            return
        
        # Initialize database and services
        db = SupabaseCatFactsDB()
        cat_facts_service = CatFactsService(db)
        
        # Initialize AI service if API key is available
        if config.OPENAI_API_KEY:
            ai_service = AIService()
            logger.info("AI service initialized successfully")
        else:
            logger.warning("OpenAI API key not set - AI features will be disabled")
        
        logger.info("Application startup completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Application shutting down")


@app.get("/", response_model=SuccessResponse)
async def root():
    """Root endpoint."""
    return SuccessResponse(
        message="Cat Facts API is running with Supabase! 🐱",
        data={"version": config.API_VERSION}
    )


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    db_status = "connected" if cat_facts_service else "disconnected"
    ai_status = "connected" if ai_service else "disconnected"
    
    return HealthCheckResponse(
        status="healthy",
        database=db_status,
        backend="Supabase",
        ai_service=ai_status
    )


@app.get("/catfacts", response_model=CatFactListResponse)
async def get_all_facts(
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """Get all cat facts from the database."""
    try:
        facts = service.get_all_facts()
        return CatFactListResponse(
            facts=facts,
            total_count=len(facts)
        )
    except DatabaseException as e:
        logger.error(f"Database error in get_all_facts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_all_facts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get("/catfacts/random", response_model=CatFactResponse)
async def get_random_fact(
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """Get a random cat fact from the database."""
    try:
        fact = service.get_random_fact()
        if fact:
            return fact
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No facts found in database"
            )
    except HTTPException:
        raise
    except DatabaseException as e:
        logger.error(f"Database error in get_random_fact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_random_fact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.post("/catfacts", response_model=CatFactCreateResponse)
async def add_fact(
    fact: str = Form(...),
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """Add a new cat fact to the database."""
    try:
        # Validate input
        if not fact or not fact.strip():
            raise ValidationException("Fact cannot be empty")
        
        result = service.create_fact(fact.strip())
        return result
        
    except ValidationException as e:
        logger.warning(f"Validation error in add_fact: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except DatabaseException as e:
        logger.error(f"Database error in add_fact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in add_fact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.post("/catfacts/{fact_id}/like", response_model=CatFactLikeResponse)
async def like_fact(
    fact_id: str,
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """Like a cat fact."""
    try:
        result = service.like_fact(fact_id)
        return result
    except DatabaseException as e:
        logger.error(f"Database error in like_fact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in like_fact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.delete("/catfacts/{fact_id}/like", response_model=CatFactLikeResponse)
async def unlike_fact(
    fact_id: str,
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """Unlike a cat fact."""
    try:
        result = service.unlike_fact(fact_id)
        return result
    except DatabaseException as e:
        logger.error(f"Database error in unlike_fact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in unlike_fact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get("/catfacts/{fact_id}", response_model=CatFactResponse)
async def get_fact_by_id(
    fact_id: str,
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """Get a specific cat fact by ID."""
    try:
        fact = service.get_fact_by_id(fact_id)
        if fact:
            return fact
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fact not found"
            )
    except HTTPException:
        raise
    except DatabaseException as e:
        logger.error(f"Database error in get_fact_by_id: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_fact_by_id: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.delete("/catfacts/{fact_id}", response_model=CatFactDeleteResponse)
async def delete_fact(
    fact_id: str,
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """Soft delete a cat fact."""
    try:
        result = service.delete_fact(fact_id)
        return result
    except DatabaseException as e:
        logger.error(f"Database error in delete_fact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in delete_fact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.post("/api/ask-ai")
async def ask_ai(
    request: AIRequest,
    service: AIService = Depends(get_ai_service)
):
    """Ask AI for cat care advice with streaming response."""
    try:
        def stream():
            try:
                for chunk in service.generate_response_stream(request):
                    yield chunk
            except Exception as e:
                logger.error(f"Error in AI streaming: {e}")
                yield f"Error: {str(e)}"

        return StreamingResponse(stream(), media_type="text/plain")
        
    except AIServiceException as e:
        logger.error(f"AI service error in ask_ai: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in ask_ai: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.post("/import-facts", response_model=ImportFactsResponse)
async def import_facts(
    request: ImportFactsRequest,
    service: CatFactsService = Depends(get_cat_facts_service)
):
    """Import facts from external API."""
    try:
        from import_cat_facts import import_cat_facts
        
        # This is a simplified version - in a real app, you'd want to make this async
        # and run it in a background task
        import_cat_facts(request.num_facts)
        
        return ImportFactsResponse(
            success=True,
            imported_count=request.num_facts,
            requested_count=request.num_facts,
            message=f"Successfully imported {request.num_facts} facts"
        )
        
    except Exception as e:
        logger.error(f"Error importing facts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import facts: {str(e)}"
        )


# Global exception handlers
@app.exception_handler(CatFactsException)
async def cat_facts_exception_handler(request, exc):
    """Handle custom CatFacts exceptions."""
    logger.error(f"CatFacts exception: {exc}")
    return ErrorResponse(
        error=str(exc),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@app.exception_handler(ValidationException)
async def validation_exception_handler(request, exc):
    """Handle validation exceptions."""
    logger.warning(f"Validation exception: {exc}")
    return ErrorResponse(
        error=str(exc),
        status_code=status.HTTP_400_BAD_REQUEST
    )


@app.exception_handler(FactNotFoundException)
async def fact_not_found_exception_handler(request, exc):
    """Handle fact not found exceptions."""
    logger.warning(f"Fact not found: {exc}")
    return ErrorResponse(
        error=str(exc),
        status_code=status.HTTP_404_NOT_FOUND
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {config.HOST}:{config.PORT}")
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower()
    ) 