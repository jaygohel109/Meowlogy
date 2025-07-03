"""
Service layer for AI operations.
"""
import logging
import openai
from typing import Generator
from Models.openAI_model import AIRequest
from constants import (
    OPENAI_API_KEY, 
    OPENAI_MODEL, 
    OPENAI_MAX_TOKENS, 
    OPENAI_TEMPERATURE,
    CAT_CARE_SYSTEM_PROMPT,
    ERROR_MESSAGES
)

logger = logging.getLogger(__name__)


class AIService:
    """Service class for AI operations."""
    
    def __init__(self):
        """Initialize the AI service with OpenAI client."""
        if not OPENAI_API_KEY:
            raise ValueError(ERROR_MESSAGES["openai_key_missing"])
        
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.max_tokens = OPENAI_MAX_TOKENS
        self.temperature = OPENAI_TEMPERATURE
        self.system_prompt = CAT_CARE_SYSTEM_PROMPT
    
    def generate_response_stream(self, request: AIRequest) -> Generator[str, None, None]:
        """Generate a streaming response from OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": request.question}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=True
            )
            
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
                    
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            raise
    
    def generate_response(self, request: AIRequest) -> str:
        """Generate a non-streaming response from OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": request.question}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            raise 