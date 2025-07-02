import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

class SupabaseCatFactsDB:
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        self.init_db()
    
    def init_db(self):
        """Initialize the database tables (this would be done via Supabase dashboard in production)"""
        # Note: In production, you would create these tables via Supabase dashboard
        # This is just for reference of the table structure
        
        # SQL for creating the cat_facts table:
        """
        CREATE TABLE cat_facts (
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
        CREATE TABLE fact_likes (
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
        AFTER INSERT OR DELETE ON fact_likes
        FOR EACH ROW EXECUTE FUNCTION update_likes_count();
        """
    
    def insert_fact(self, fact: str) -> Dict[str, Any]:
        """Insert a new cat fact, returns result with status and data"""
        try:
            # Check if fact already exists
            existing = self.client.table('cat_facts').select('id').eq('fact', fact).execute()
            if existing.data:
                return {
                    "success": False,
                    "message": "Fact already exists",
                    "status": "duplicate"
                }
            
            # Insert new fact
            result = self.client.table('cat_facts').insert({
                'fact': fact,
                'created_at': datetime.utcnow().isoformat()
            }).execute()
            
            if result.data:
                return {
                    "success": True,
                    "message": "Fact added successfully",
                    "status": "success",
                    "data": result.data[0]
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to add fact",
                    "status": "error"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Database error: {str(e)}",
                "status": "error"
            }
    
    def get_all_facts(self) -> List[Dict[str, Any]]:
        """Get all active cat facts from the database"""
        try:
            result = self.client.table('cat_facts')\
                .select('id, fact, created_at, likes_count')\
                .eq('is_active', True)\
                .order('created_at', desc=True)\
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f"Error fetching facts: {e}")
            return []
    
    def get_random_fact(self) -> Optional[Dict[str, Any]]:
        """Get a random cat fact from the database"""
        try:
            # Using PostgreSQL's RANDOM() function
            result = self.client.rpc('get_random_fact').execute()
            
            if result.data:
                return result.data[0]
            else:
                # Fallback method if RPC function doesn't exist
                result = self.client.table('cat_facts')\
                    .select('id, fact, created_at, likes_count')\
                    .eq('is_active', True)\
                    .limit(1)\
                    .execute()
                
                return result.data[0] if result.data else None
                
        except Exception as e:
            print(f"Error fetching random fact: {e}")
            return None
    
    def fact_exists(self, fact: str) -> bool:
        """Check if a fact already exists in the database"""
        try:
            result = self.client.table('cat_facts')\
                .select('id')\
                .eq('fact', fact)\
                .eq('is_active', True)\
                .execute()
            
            return len(result.data) > 0
        except Exception as e:
            print(f"Error checking fact existence: {e}")
            return False
    
    def like_fact(self, fact_id: str, user_id: str = None) -> Dict[str, Any]:
        """Like a fact (for future use)"""
        try:
            # For now, we'll use a simple approach without user authentication
            # In the future, you can integrate with Supabase Auth
            temp_user_id = user_id or str(uuid.uuid4())
            
            result = self.client.table('fact_likes').insert({
                'fact_id': fact_id,
                'user_id': temp_user_id
            }).execute()
            
            if result.data:
                return {
                    "success": True,
                    "message": "Fact liked successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to like fact"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error liking fact: {str(e)}"
            }
    
    def unlike_fact(self, fact_id: str, user_id: str = None) -> Dict[str, Any]:
        """Unlike a fact (for future use)"""
        try:
            temp_user_id = user_id or str(uuid.uuid4())
            
            result = self.client.table('fact_likes')\
                .delete()\
                .eq('fact_id', fact_id)\
                .eq('user_id', temp_user_id)\
                .execute()
            
            return {
                "success": True,
                "message": "Fact unliked successfully"
            }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error unliking fact: {str(e)}"
            }
    
    def get_fact_by_id(self, fact_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific fact by ID"""
        try:
            result = self.client.table('cat_facts')\
                .select('id, fact, created_at, likes_count')\
                .eq('id', fact_id)\
                .eq('is_active', True)\
                .execute()
            
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error fetching fact by ID: {e}")
            return None
    
    def delete_fact(self, fact_id: str) -> Dict[str, Any]:
        """Soft delete a fact (set is_active to False)"""
        try:
            result = self.client.table('cat_facts')\
                .update({'is_active': False, 'updated_at': datetime.utcnow().isoformat()})\
                .eq('id', fact_id)\
                .execute()
            
            if result.data:
                return {
                    "success": True,
                    "message": "Fact deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Fact not found"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error deleting fact: {str(e)}"
            } 