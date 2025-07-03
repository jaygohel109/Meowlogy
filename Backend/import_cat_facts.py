import requests
import time
import logging
from Meowlogy.Backend.database.supabase_db import SupabaseCatFactsDB
from constants import (
    CAT_FACTS_API_URL, 
    CAT_FACTS_API_DELAY, 
    VALIDATION_RULES,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES
)
from exceptions import ExternalAPIException, DatabaseException

logger = logging.getLogger(__name__)

def fetch_cat_fact():
    """Fetch a single cat fact from the API"""
    try:
        response = requests.get(CAT_FACTS_API_URL)
        response.raise_for_status()
        data = response.json()
        fact = data.get("fact")
        logger.debug(f"Fetched fact from external API: {fact[:50]}...")
        return fact
    except requests.RequestException as e:
        logger.error(f"Error fetching cat fact from {CAT_FACTS_API_URL}: {e}")
        raise ExternalAPIException(f"Failed to fetch cat fact: {e}")

def import_cat_facts(num_facts=VALIDATION_RULES["default_import_facts"]):
    """Import cat facts from the API into the database"""
    try:
        db = SupabaseCatFactsDB()
        logger.info(SUCCESS_MESSAGES["database_connected"])
    except Exception as e:
        logger.error(f"Error connecting to Supabase: {e}")
        logger.error("Please make sure your SUPABASE_URL and SUPABASE_ANON_KEY are set in your .env file")
        raise DatabaseException(f"Failed to connect to database: {e}")
    
    logger.info(f"Fetching {num_facts} cat facts from {CAT_FACTS_API_URL}...")
    print("-" * 50)
    
    facts_imported = 0
    attempts = 0
    max_attempts = num_facts * 3  # Allow some retries for duplicates
    
    while facts_imported < num_facts and attempts < max_attempts:
        try:
            fact = fetch_cat_fact()
            attempts += 1
            
            # Try to insert the fact
            result = db.insert_fact(fact)
            if result["success"]:
                logger.info(f"✓ Imported: {fact}")
                facts_imported += 1
            else:
                logger.warning(f"⚠ Skipped ({result['status']}): {fact}")
            
            # Small delay to be respectful to the API
            time.sleep(CAT_FACTS_API_DELAY)
            
        except ExternalAPIException as e:
            logger.error(f"Attempt {attempts}: Failed to fetch fact, retrying... Error: {e}")
            time.sleep(1)
            continue
    
    print("-" * 50)
    logger.info(f"Import complete! {facts_imported} facts imported out of {num_facts} requested.")
    
    if facts_imported < num_facts:
        logger.info("Note: Some facts were duplicates and were skipped.")
    
    # Show current database status
    try:
        all_facts = db.get_all_facts()
        logger.info(f"Total facts in database: {len(all_facts)}")
    except Exception as e:
        logger.error(f"Failed to get total facts count: {e}")
    
    if facts_imported < num_facts:
        print(f"Note: Some facts were duplicates and were skipped.")
    else:
        logger.info(f"Successfully imported all {num_facts} facts!")

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        import_cat_facts(VALIDATION_RULES["default_import_facts"])
    except Exception as e:
        logger.error(f"Import failed: {e}")
        exit(1) 