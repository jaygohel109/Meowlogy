"""
Service layer for cat facts business logic.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from database.supabase_db import SupabaseCatFactsDB
from Models.cat_facts_models import CatFactResponse, CatFactCreateResponse, CatFactLikeResponse, CatFactDeleteResponse
from constants import ERROR_MESSAGES, SUCCESS_MESSAGES

logger = logging.getLogger(__name__)


class CatFactsService:
    """Service class for cat facts operations."""
    
    def __init__(self, db: SupabaseCatFactsDB):
        """Initialize the service with a database instance."""
        self.db = db
    
    def get_all_facts(self) -> List[CatFactResponse]:
        """Get all cat facts from the database."""
        try:
            facts_data = self.db.get_all_facts()
            return [CatFactResponse(**fact) for fact in facts_data]
        except Exception as e:
            logger.error(f"Error fetching all facts: {e}")
            raise
    
    def get_random_fact(self) -> Optional[CatFactResponse]:
        """Get a random cat fact from the database."""
        try:
            fact_data = self.db.get_random_fact()
            if fact_data:
                return CatFactResponse(**fact_data)
            return None
        except Exception as e:
            logger.error(f"Error fetching random fact: {e}")
            raise
    
    def get_fact_by_id(self, fact_id: str) -> Optional[CatFactResponse]:
        """Get a specific cat fact by ID."""
        try:
            fact_data = self.db.get_fact_by_id(fact_id)
            if fact_data:
                return CatFactResponse(**fact_data)
            return None
        except Exception as e:
            logger.error(f"Error fetching fact by ID {fact_id}: {e}")
            raise
    
    def create_fact(self, fact: str) -> CatFactCreateResponse:
        """Create a new cat fact."""
        try:
            result = self.db.insert_fact(fact)
            
            if result["success"]:
                return CatFactCreateResponse(
                    success=True,
                    message=SUCCESS_MESSAGES["fact_added"],
                    status="success",
                    data=CatFactResponse(**result["data"]) if result.get("data") else None
                )
            else:
                return CatFactCreateResponse(
                    success=False,
                    message=result["message"],
                    status=result["status"],
                    data=None
                )
        except Exception as e:
            logger.error(f"Error creating fact: {e}")
            return CatFactCreateResponse(
                success=False,
                message=ERROR_MESSAGES["failed_to_add_fact"],
                status="error",
                data=None
            )
    
    def like_fact(self, fact_id: str, user_id: str = None) -> CatFactLikeResponse:
        """Like a cat fact."""
        try:
            result = self.db.like_fact(fact_id, user_id)
            
            if result["success"]:
                return CatFactLikeResponse(
                    success=True,
                    message=SUCCESS_MESSAGES["fact_liked"]
                )
            else:
                return CatFactLikeResponse(
                    success=False,
                    message=result["message"]
                )
        except Exception as e:
            logger.error(f"Error liking fact {fact_id}: {e}")
            return CatFactLikeResponse(
                success=False,
                message=ERROR_MESSAGES["failed_to_like_fact"]
            )
    
    def unlike_fact(self, fact_id: str, user_id: str = None) -> CatFactLikeResponse:
        """Unlike a cat fact."""
        try:
            result = self.db.unlike_fact(fact_id, user_id)
            
            if result["success"]:
                return CatFactLikeResponse(
                    success=True,
                    message=SUCCESS_MESSAGES["fact_unliked"]
                )
            else:
                return CatFactLikeResponse(
                    success=False,
                    message=result["message"]
                )
        except Exception as e:
            logger.error(f"Error unliking fact {fact_id}: {e}")
            return CatFactLikeResponse(
                success=False,
                message=ERROR_MESSAGES["failed_to_unlike_fact"]
            )
    
    def delete_fact(self, fact_id: str) -> CatFactDeleteResponse:
        """Soft delete a cat fact."""
        try:
            result = self.db.delete_fact(fact_id)
            
            if result["success"]:
                return CatFactDeleteResponse(
                    success=True,
                    message=SUCCESS_MESSAGES["fact_deleted"]
                )
            else:
                return CatFactDeleteResponse(
                    success=False,
                    message=result["message"]
                )
        except Exception as e:
            logger.error(f"Error deleting fact {fact_id}: {e}")
            return CatFactDeleteResponse(
                success=False,
                message=ERROR_MESSAGES["failed_to_delete_fact"]
            )
    
    def fact_exists(self, fact: str) -> bool:
        """Check if a fact already exists in the database."""
        try:
            return self.db.fact_exists(fact)
        except Exception as e:
            logger.error(f"Error checking fact existence: {e}")
            return False 