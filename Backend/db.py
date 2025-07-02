import sqlite3
from datetime import datetime
from typing import List, Optional

class CatFactsDB:
    def __init__(self, db_path: str = "cat_facts.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database and create the cat_facts table"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cat_facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fact TEXT UNIQUE,
                    created_at DATE DEFAULT (DATE('now'))
                )
            ''')
            conn.commit()
    
    def insert_fact(self, fact: str) -> bool:
        """Insert a new cat fact, returns True if inserted, False if duplicate"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO cat_facts (fact) VALUES (?)', (fact,))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False  # Duplicate fact
    
    def get_all_facts(self) -> List[dict]:
        """Get all cat facts from the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, fact, created_at FROM cat_facts ORDER BY created_at DESC')
            rows = cursor.fetchall()
            return [
                {"id": row[0], "fact": row[1], "created_at": row[2]}
                for row in rows
            ]
    
    def get_random_fact(self) -> Optional[dict]:
        """Get a random cat fact from the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT fact FROM cat_facts ORDER BY RANDOM() LIMIT 1')
            row = cursor.fetchone()
            return {"fact": row[0]} if row else None
    
    def fact_exists(self, fact: str) -> bool:
        """Check if a fact already exists in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM cat_facts WHERE fact = ?', (fact,))
            count = cursor.fetchone()[0]
            return count > 0 