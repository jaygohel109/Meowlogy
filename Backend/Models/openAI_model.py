"""
Data models for OpenAI API interactions.
"""
from typing import Optional
from pydantic import BaseModel, Field, validator
from constants import VALIDATION_RULES


class AIRequest(BaseModel):
    """Request model for AI chat endpoint."""
    question: str = Field(..., description="The question to ask the AI assistant")
    
    @validator('question')
    def validate_question(cls, v):
        if not v or not v.strip():
            raise ValueError("Question cannot be empty")
        if len(v.strip()) > VALIDATION_RULES["max_fact_length"]:
            raise ValueError(f"Question too long. Maximum {VALIDATION_RULES['max_fact_length']} characters allowed.")
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "question": "How often should I feed my cat?"
            }
        }


class AIResponse(BaseModel):
    """Response model for AI chat endpoint."""
    answer: str = Field(..., description="The AI assistant's response")
    model_used: str = Field(..., description="The AI model used for the response")
    
    class Config:
        schema_extra = {
            "example": {
                "answer": "Adult cats should be fed 2-3 times per day with appropriate portion sizes.",
                "model_used": "gpt-3.5-turbo"
            }
        }