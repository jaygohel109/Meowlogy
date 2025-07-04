"""
Data models for the Cat Facts API.
"""

from .openAI_model import AIRequest
from .cat_facts_models import (
    CatFactResponse,
    CatFactListResponse,
    CatFactCreateRequest,
    CatFactCreateResponse,
    CatFactLikeResponse,
    CatFactDeleteResponse,
    HealthCheckResponse,
    ErrorResponse,
    SuccessResponse,
    ImportFactsRequest,
    ImportFactsResponse,
    UserSignupRequest,
    UserLoginRequest,
    AuthResponse
)

__all__ = [
    "AIRequest",
    "CatFactResponse",
    "CatFactListResponse", 
    "CatFactCreateRequest",
    "CatFactCreateResponse",
    "CatFactLikeResponse",
    "CatFactDeleteResponse",
    "HealthCheckResponse",
    "ErrorResponse",
    "SuccessResponse",
    "ImportFactsRequest",
    "ImportFactsResponse",
    "UserSignupRequest",
    "UserLoginRequest",
    "AuthResponse"
] 