"""
Constants and configuration values for the Cat Facts API.
"""
import os
from typing import List

# API Configuration
API_TITLE = "Cat Facts API"
API_DESCRIPTION = "API for managing cat facts with Supabase"
API_VERSION = "1.0.0"

# Server Configuration
DEFAULT_PORT = 8000
DEFAULT_HOST = "0.0.0.0"

# CORS Configuration
ALLOWED_ORIGINS = ["*"]  # In production, limit this to your frontend URL
ALLOWED_CREDENTIALS = True
ALLOWED_METHODS = ["*"]
ALLOWED_HEADERS = ["*"]

# Database Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MAX_TOKENS = 256
OPENAI_TEMPERATURE = 0.7

# AI System Prompts
CAT_CARE_SYSTEM_PROMPT = (
    "You are a helpful, cat-loving assistant for answering cat care questions. "
    "Greet users with a cheerful 'Meow!' or playful purr to start the conversation. "
    "Always be friendly, concise, and accurate. "
    "Feel free to sprinkle in cat puns or playful language to make the experience fun and welcoming."
)

# External API Configuration
CAT_FACTS_API_URL = "https://catfact.ninja/fact"
CAT_FACTS_API_DELAY = 0.5  # seconds between requests

# Database Table Names
CAT_FACTS_TABLE = "cat_facts"
FACT_LIKES_TABLE = "fact_likes"
USERS_TABLE = "users"

# Error Messages
ERROR_MESSAGES = {
    "database_not_initialized": "Database not initialized",
    "fact_not_found": "Fact not found",
    "fact_empty": "Fact cannot be empty",
    "openai_key_missing": "OpenAI API key not set",
    "supabase_credentials_missing": "SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables",
    "no_facts_found": "No facts found in database",
    "duplicate_fact": "Fact already exists",
    "failed_to_add_fact": "Failed to add fact",
    "failed_to_like_fact": "Failed to like fact",
    "failed_to_unlike_fact": "Failed to unlike fact",
    "failed_to_delete_fact": "Failed to delete fact",
}

# Success Messages
SUCCESS_MESSAGES = {
    "fact_added": "Fact added successfully",
    "fact_liked": "Fact liked successfully",
    "fact_unliked": "Fact unliked successfully",
    "fact_deleted": "Fact deleted successfully",
    "database_connected": "Connected to Supabase successfully!",
}

# HTTP Status Codes
HTTP_STATUS = {
    "OK": 200,
    "CREATED": 201,
    "BAD_REQUEST": 400,
    "NOT_FOUND": 404,
    "INTERNAL_SERVER_ERROR": 500,
}

# Database Fields
CAT_FACTS_FIELDS = ["id", "fact", "created_at", "likes_count"]
FACT_LIKES_FIELDS = ["id", "fact_id", "user_id", "created_at"]

# Validation Rules
VALIDATION_RULES = {
    "max_fact_length": 1000,
    "min_fact_length": 1,
    "max_import_facts": 100,
    "default_import_facts": 5,
} 