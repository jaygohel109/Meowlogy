from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from supabase_db import SupabaseCatFactsDB
from typing import List, Dict, Any
from Models.openAI_model import AIRequest
from dotenv import load_dotenv
import os
import uvicorn
import openai

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="Cat Facts API", description="API for managing cat facts with Supabase")

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, limit this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase database
try:
    db = SupabaseCatFactsDB()
except ValueError as e:
    print(f"Database initialization error: {e}")
    print("Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables")
    db = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Cat Facts API is running with Supabase! 🐱"}

@app.get("/catfacts", response_model=List[Dict[str, Any]])
async def get_all_facts():
    """Get all cat facts from the database"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        facts = db.get_all_facts()
        return facts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/catfacts/random", response_model=Dict[str, Any])
async def get_random_fact():
    """Get a random cat fact from the database"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        fact = db.get_random_fact()
        if fact:
            return fact
        else:
            raise HTTPException(status_code=404, detail="No facts found in database")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/catfacts")
async def add_fact(fact: str = Form(...)):
    """Add a new cat fact to the database"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    if not fact or not fact.strip():
        raise HTTPException(status_code=400, detail="Fact cannot be empty")
    
    try:
        result = db.insert_fact(fact.strip())
        return {
            "message": result["message"],
            "status": result["status"],
            "data": result.get("data")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/catfacts/{fact_id}/like")
async def like_fact(fact_id: str):
    """Like a cat fact (for future use)"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        result = db.like_fact(fact_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/catfacts/{fact_id}/like")
async def unlike_fact(fact_id: str):
    """Unlike a cat fact (for future use)"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        result = db.unlike_fact(fact_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/catfacts/{fact_id}")
async def get_fact_by_id(fact_id: str):
    """Get a specific cat fact by ID"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        fact = db.get_fact_by_id(fact_id)
        if fact:
            return fact
        else:
            raise HTTPException(status_code=404, detail="Fact not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/catfacts/{fact_id}")
async def delete_fact(fact_id: str):
    """Soft delete a cat fact"""
    if not db:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        result = db.delete_fact(fact_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "connected" if db else "disconnected"
    return {
        "status": "healthy", 
        "database": db_status,
        "backend": "Supabase"
    }

@app.post("/api/ask-ai")
async def ask_ai(request: AIRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OpenAI API key not set")
    try:
        system_prompt = (
            "You are a helpful assistant for cat care questions. "
            "Always be friendly, concise, and accurate."
        )
        # Use OpenAI's streaming API
        def stream():
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # or "gpt-4"
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.question}
                ],
                max_tokens=256,
                temperature=0.7,
                stream=True
            )
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield content

        return StreamingResponse(stream(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 