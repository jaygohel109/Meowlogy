import requests
import time
from supabase_db import SupabaseCatFactsDB

def fetch_cat_fact():
    """Fetch a single cat fact from the API"""
    try:
        response = requests.get("https://catfact.ninja/fact")
        response.raise_for_status()
        data = response.json()
        return data.get("fact")
    except requests.RequestException as e:
        print(f"Error fetching cat fact: {e}")
        return None

def import_cat_facts(num_facts=5):
    """Import cat facts from the API into the database"""
    try:
        db = SupabaseCatFactsDB()
        print("✓ Connected to Supabase successfully!")
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        print("Please make sure your SUPABASE_URL and SUPABASE_ANON_KEY are set in your .env file")
        return
    
    print(f"Fetching {num_facts} cat facts from https://catfact.ninja/fact...")
    print("-" * 50)
    
    facts_imported = 0
    attempts = 0
    max_attempts = num_facts * 3  # Allow some retries for duplicates
    
    while facts_imported < num_facts and attempts < max_attempts:
        fact = fetch_cat_fact()
        attempts += 1
        
        if not fact:
            print(f"Attempt {attempts}: Failed to fetch fact, retrying...")
            time.sleep(1)
            continue
        
        # Try to insert the fact
        result = db.insert_fact(fact)
        if result["success"]:
            print(f"✓ Imported: {fact}")
            facts_imported += 1
        else:
            print(f"⚠ Skipped ({result['status']}): {fact}")
        
        # Small delay to be respectful to the API
        time.sleep(0.5)
    
    print("-" * 50)
    print(f"Import complete! {facts_imported} facts imported out of {num_facts} requested.")
    
    if facts_imported < num_facts:
        print(f"Note: Some facts were duplicates and were skipped.")
    
    # Show current database status
    all_facts = db.get_all_facts()
    print(f"Total facts in database: {len(all_facts)}")
    
    if facts_imported < num_facts:
        print(f"Note: Some facts were duplicates and were skipped.")
    else:
        print(f"Successfully imported all {num_facts} facts!")

if __name__ == "__main__":
    import_cat_facts(5) 