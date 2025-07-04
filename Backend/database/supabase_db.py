import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from supabase import create_client, Client
import uuid
import logging
import hashlib
import secrets
from constants import (
    SUPABASE_URL, 
    SUPABASE_ANON_KEY, 
    CAT_FACTS_TABLE, 
    FACT_LIKES_TABLE,
    USERS_TABLE,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES
)
from exceptions import DatabaseException, ConfigurationException

logger = logging.getLogger(__name__)

class SupabaseCatFactsDB:
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase_url = SUPABASE_URL
        self.supabase_key = SUPABASE_ANON_KEY
        
        if not self.supabase_url or not self.supabase_key:
            raise ConfigurationException(ERROR_MESSAGES["supabase_credentials_missing"])
        
        try:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)
            logger.info(SUCCESS_MESSAGES["database_connected"])
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise DatabaseException(f"Failed to connect to Supabase: {e}")
        
        self.init_db()
    
    def init_db(self):
        """Initialize the database tables (this would be done via Supabase dashboard in production)"""
        # Note: In production, you would create these tables via Supabase dashboard
        # This is just for reference of the table structure
        
        # SQL for creating the cat_facts table:
        """
        CREATE TABLE {CAT_FACTS_TABLE} (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            fact TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            likes_count INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE
        );
        
        -- Enable Row Level Security
        ALTER TABLE cat_facts ENABLE ROW LEVEL SECURITY;
        
        -- Create policy to allow all operations for now (you can restrict this later)
        CREATE POLICY "Allow all operations" ON cat_facts FOR ALL USING (true);
        
        -- Create likes table for future use
        CREATE TABLE {FACT_LIKES_TABLE} (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            fact_id UUID REFERENCES cat_facts(id) ON DELETE CASCADE,
            user_id UUID, -- Will be used when you add authentication
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            UNIQUE(fact_id, user_id)
        );
        
        -- Enable RLS on likes table
        ALTER TABLE fact_likes ENABLE ROW LEVEL SECURITY;
        CREATE POLICY "Allow all operations" ON fact_likes FOR ALL USING (true);
        
        -- Create function to update likes_count
        CREATE OR REPLACE FUNCTION update_likes_count()
        RETURNS TRIGGER AS $$
        BEGIN
            IF TG_OP = 'INSERT' THEN
                UPDATE cat_facts SET likes_count = likes_count + 1 WHERE id = NEW.fact_id;
                RETURN NEW;
            ELSIF TG_OP = 'DELETE' THEN
                UPDATE cat_facts SET likes_count = likes_count - 1 WHERE id = OLD.fact_id;
                RETURN OLD;
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Create trigger for likes_count
        CREATE TRIGGER update_likes_count_trigger
        AFTER INSERT OR DELETE ON {FACT_LIKES_TABLE}
        FOR EACH ROW EXECUTE FUNCTION update_likes_count();
        """
    
    def insert_fact(self, fact: str) -> Dict[str, Any]:
        """Insert a new cat fact, returns result with status and data"""
        try:
            # Check if fact already exists
            existing = self.client.table(CAT_FACTS_TABLE).select('id').eq('fact', fact).execute()
            if existing.data:
                logger.warning(f"Attempted to insert duplicate fact: {fact[:50]}...")
                return {
                    "success": False,
                    "message": ERROR_MESSAGES["duplicate_fact"],
                    "status": "duplicate"
                }
            
            # Insert new fact
            result = self.client.table(CAT_FACTS_TABLE).insert({
                'fact': fact,
                'created_at': datetime.utcnow().isoformat()
            }).execute()
            
            if result.data:
                logger.info(f"Successfully inserted fact: {fact[:50]}...")
                return {
                    "success": True,
                    "message": SUCCESS_MESSAGES["fact_added"],
                    "status": "success",
                    "data": result.data[0]
                }
            else:
                logger.error("Failed to insert fact - no data returned")
                return {
                    "success": False,
                    "message": ERROR_MESSAGES["failed_to_add_fact"],
                    "status": "error"
                }
                
        except Exception as e:
            logger.error(f"Database error while inserting fact: {e}")
            return {
                "success": False,
                "message": f"Database error: {str(e)}",
                "status": "error"
            }
    
    def get_all_facts(self) -> List[Dict[str, Any]]:
        """Get all active cat facts from the database"""
        try:
            result = self.client.table(CAT_FACTS_TABLE)\
                .select('id, fact, created_at, likes_count')\
                .eq('is_active', True)\
                .order('created_at', desc=True)\
                .execute()
            
            facts = result.data if result.data else []
            logger.info(f"Retrieved {len(facts)} facts from database")
            return facts
        except Exception as e:
            logger.error(f"Error fetching facts: {e}")
            raise DatabaseException(f"Failed to fetch facts: {e}")
    
    def get_random_fact(self) -> Optional[Dict[str, Any]]:
        """Get a random cat fact from the database"""
        try:
            # Using PostgreSQL's RANDOM() function
            result = self.client.rpc('get_random_fact', {}).execute()
            
            if result.data:
                logger.info("Retrieved random fact using RPC function")
                return result.data[0]
            else:
                # Fallback method if RPC function doesn't exist
                result = self.client.table(CAT_FACTS_TABLE)\
                    .select('id, fact, created_at, likes_count')\
                    .eq('is_active', True)\
                    .limit(1)\
                    .execute()
                
                fact = result.data[0] if result.data else None
                if fact:
                    logger.info("Retrieved random fact using fallback method")
                else:
                    logger.warning("No facts found in database")
                return fact
                
        except Exception as e:
            logger.error(f"Error fetching random fact: {e}")
            raise DatabaseException(f"Failed to fetch random fact: {e}")
    
    def fact_exists(self, fact: str) -> bool:
        """Check if a fact already exists in the database"""
        try:
            result = self.client.table(CAT_FACTS_TABLE)\
                .select('id')\
                .eq('fact', fact)\
                .eq('is_active', True)\
                .execute()
            
            exists = len(result.data) > 0
            logger.debug(f"Fact existence check for '{fact[:30]}...': {exists}")
            return exists
        except Exception as e:
            logger.error(f"Error checking fact existence: {e}")
            raise DatabaseException(f"Failed to check fact existence: {e}")
    
    def like_fact(self, fact_id: str, user_id: str = None) -> Dict[str, Any]:
        """Like a fact (for future use)"""
        try:
            # For now, we'll use a simple approach without user authentication
            # In the future, you can integrate with Supabase Auth
            temp_user_id = user_id or str(uuid.uuid4())
            
            result = self.client.table(FACT_LIKES_TABLE).insert({
                'fact_id': fact_id,
                'user_id': temp_user_id
            }).execute()
            
            if result.data:
                logger.info(f"Successfully liked fact: {fact_id}")
                return {
                    "success": True,
                    "message": SUCCESS_MESSAGES["fact_liked"]
                }
            else:
                logger.error(f"Failed to like fact: {fact_id}")
                return {
                    "success": False,
                    "message": ERROR_MESSAGES["failed_to_like_fact"]
                }
                
        except Exception as e:
            logger.error(f"Error liking fact {fact_id}: {e}")
            return {
                "success": False,
                "message": f"Error liking fact: {str(e)}"
            }
    
    def unlike_fact(self, fact_id: str, user_id: str = None) -> Dict[str, Any]:
        """Unlike a fact (for future use)"""
        try:
            temp_user_id = user_id or str(uuid.uuid4())
            
            result = self.client.table(FACT_LIKES_TABLE)\
                .delete()\
                .eq('fact_id', fact_id)\
                .eq('user_id', temp_user_id)\
                .execute()
            
            logger.info(f"Successfully unliked fact: {fact_id}")
            return {
                "success": True,
                "message": SUCCESS_MESSAGES["fact_unliked"]
            }
                
        except Exception as e:
            logger.error(f"Error unliking fact {fact_id}: {e}")
            return {
                "success": False,
                "message": f"Error unliking fact: {str(e)}"
            }
    
    def get_fact_by_id(self, fact_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific fact by ID"""
        try:
            result = self.client.table(CAT_FACTS_TABLE)\
                .select('id, fact, created_at, likes_count')\
                .eq('id', fact_id)\
                .eq('is_active', True)\
                .execute()
            
            fact = result.data[0] if result.data else None
            if fact:
                logger.info(f"Retrieved fact by ID: {fact_id}")
            else:
                logger.warning(f"Fact not found with ID: {fact_id}")
            return fact
        except Exception as e:
            logger.error(f"Error fetching fact by ID {fact_id}: {e}")
            raise DatabaseException(f"Failed to fetch fact by ID: {e}")
    
    def delete_fact(self, fact_id: str) -> Dict[str, Any]:
        """Soft delete a fact (set is_active to False)"""
        try:
            result = self.client.table(CAT_FACTS_TABLE)\
                .update({'is_active': False, 'updated_at': datetime.utcnow().isoformat()})\
                .eq('id', fact_id)\
                .execute()
            
            if result.data:
                logger.info(f"Successfully deleted fact: {fact_id}")
                return {
                    "success": True,
                    "message": SUCCESS_MESSAGES["fact_deleted"]
                }
            else:
                logger.warning(f"Attempted to delete non-existent fact: {fact_id}")
                return {
                    "success": False,
                    "message": ERROR_MESSAGES["fact_not_found"]
                }
                
        except Exception as e:
            logger.error(f"Error deleting fact {fact_id}: {e}")
            return {
                "success": False,
                "message": f"Error deleting fact: {str(e)}"
            }
    
    # User Authentication Methods
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256 with salt."""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256()
        hash_obj.update((password + salt).encode('utf-8'))
        return f"{salt}${hash_obj.hexdigest()}"
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            salt, hash_value = hashed_password.split('$', 1)
            hash_obj = hashlib.sha256()
            hash_obj.update((password + salt).encode('utf-8'))
            return hash_obj.hexdigest() == hash_value
        except Exception:
            return False
    
    def create_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Create a new user in the database."""
        try:
            # Check if username already exists
            existing_username = self.client.table(USERS_TABLE).select('id').eq('username', username).execute()
            if existing_username.data:
                return {
                    "success": False,
                    "message": "Username already exists",
                    "status": "duplicate_username"
                }
            
            # Check if email already exists
            existing_email = self.client.table(USERS_TABLE).select('id').eq('email', email.lower()).execute()
            if existing_email.data:
                return {
                    "success": False,
                    "message": "Email already exists",
                    "status": "duplicate_email"
                }
            
            # Hash password
            hashed_password = self._hash_password(password)
            
            # Insert new user
            result = self.client.table(USERS_TABLE).insert({
                'username': username,
                'email': email.lower(),
                'password_hash': hashed_password,
                'auth_provider': 'local'
            }).execute()
            
            if result.data:
                user_data = result.data[0]
                # Remove password from response
                user_data.pop('password_hash', None)
                logger.info(f"Successfully created user: {username}")
                return {
                    "success": True,
                    "message": "User created successfully",
                    "status": "success",
                    "data": user_data
                }
            else:
                logger.error("Failed to create user - no data returned")
                return {
                    "success": False,
                    "message": "Failed to create user",
                    "status": "error"
                }
                
        except Exception as e:
            logger.error(f"Database error while creating user: {e}")
            return {
                "success": False,
                "message": f"Database error: {str(e)}",
                "status": "error"
            }
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate a user with username/email and password."""
        try:
            # Try to find user by username or email
            # First try username
            result = self.client.table(USERS_TABLE).select('*').eq('username', username).execute()
            
            # If not found by username, try email
            if not result.data:
                result = self.client.table(USERS_TABLE).select('*').eq('email', username.lower()).execute()
            
            if not result.data:
                return {
                    "success": False,
                    "message": "Invalid username or password",
                    "status": "invalid_credentials"
                }
            
            user = result.data[0]
            
            # Verify password
            if not self._verify_password(password, user['password_hash']):
                return {
                    "success": False,
                    "message": "Invalid username or password",
                    "status": "invalid_credentials"
                }
            
            # Remove password from response
            user.pop('password_hash', None)
            logger.info(f"Successfully authenticated user: {user['username']}")
            return {
                "success": True,
                "message": "Authentication successful",
                "status": "success",
                "data": user
            }
                
        except Exception as e:
            logger.error(f"Database error while authenticating user: {e}")
            return {
                "success": False,
                "message": f"Database error: {str(e)}",
                "status": "error"
            }