"""
Data models for cat facts API endpoints.
"""
from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, validator
from constants import VALIDATION_RULES


class CatFactBase(BaseModel):
    """Base model for cat fact data."""
    fact: str = Field(..., description="The cat fact text")
    
    @validator('fact')
    def validate_fact(cls, v):
        if not v or not v.strip():
            raise ValueError("Fact cannot be empty")
        if len(v.strip()) > VALIDATION_RULES["max_fact_length"]:
            raise ValueError(f"Fact too long. Maximum {VALIDATION_RULES['max_fact_length']} characters allowed.")
        if len(v.strip()) < VALIDATION_RULES["min_fact_length"]:
            raise ValueError(f"Fact too short. Minimum {VALIDATION_RULES['min_fact_length']} character required.")
        return v.strip()


class CatFactResponse(CatFactBase):
    """Response model for a single cat fact."""
    id: str = Field(..., description="Unique identifier for the fact")
    created_at: datetime = Field(..., description="When the fact was created")
    likes_count: int = Field(default=0, description="Number of likes for this fact")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "fact": "Cats have over 20 muscles that control their ears.",
                "created_at": "2024-01-15T10:30:00Z",
                "likes_count": 5
            }
        }


class CatFactListResponse(BaseModel):
    """Response model for a list of cat facts."""
    facts: List[CatFactResponse] = Field(..., description="List of cat facts")
    total_count: int = Field(..., description="Total number of facts")
    
    class Config:
        schema_extra = {
            "example": {
                "facts": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "fact": "Cats have over 20 muscles that control their ears.",
                        "created_at": "2024-01-15T10:30:00Z",
                        "likes_count": 5
                    }
                ],
                "total_count": 1
            }
        }


class CatFactCreateRequest(BaseModel):
    """Request model for creating a new cat fact."""
    fact: str = Field(..., description="The cat fact to add")
    
    @validator('fact')
    def validate_fact(cls, v):
        if not v or not v.strip():
            raise ValueError("Fact cannot be empty")
        if len(v.strip()) > VALIDATION_RULES["max_fact_length"]:
            raise ValueError(f"Fact too long. Maximum {VALIDATION_RULES['max_fact_length']} characters allowed.")
        if len(v.strip()) < VALIDATION_RULES["min_fact_length"]:
            raise ValueError(f"Fact too short. Minimum {VALIDATION_RULES['min_fact_length']} character required.")
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "fact": "Cats spend 70% of their lives sleeping."
            }
        }


class CatFactCreateResponse(BaseModel):
    """Response model for creating a cat fact."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Status of the operation")
    data: Optional[CatFactResponse] = Field(None, description="Created fact data if successful")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Fact added successfully",
                "status": "success",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "fact": "Cats spend 70% of their lives sleeping.",
                    "created_at": "2024-01-15T10:30:00Z",
                    "likes_count": 0
                }
            }
        }


class CatFactLikeResponse(BaseModel):
    """Response model for liking/unliking a cat fact."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Fact liked successfully"
            }
        }


class CatFactDeleteResponse(BaseModel):
    """Response model for deleting a cat fact."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Fact deleted successfully"
            }
        }


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(..., description="Overall health status")
    database: str = Field(..., description="Database connection status")
    backend: str = Field(..., description="Backend type")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "database": "connected",
                "backend": "Supabase",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    status_code: int = Field(..., description="HTTP status code")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "Database error",
                "detail": "Connection failed",
                "status_code": 500
            }
        }


class SuccessResponse(BaseModel):
    """Standard success response model."""
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Operation completed successfully",
                "data": {"id": "123"}
            }
        }


class ImportFactsRequest(BaseModel):
    """Request model for importing facts from external API."""
    num_facts: int = Field(
        default=VALIDATION_RULES["default_import_facts"],
        ge=1,
        le=VALIDATION_RULES["max_import_facts"],
        description="Number of facts to import"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "num_facts": 5
            }
        }


class ImportFactsResponse(BaseModel):
    """Response model for importing facts."""
    success: bool = Field(..., description="Whether the operation was successful")
    imported_count: int = Field(..., description="Number of facts successfully imported")
    requested_count: int = Field(..., description="Number of facts requested")
    message: str = Field(..., description="Response message")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "imported_count": 5,
                "requested_count": 5,
                "message": "Successfully imported 5 facts"
            }
        } 