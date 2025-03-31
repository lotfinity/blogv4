from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models.gpt_memory import GPTMemory
from typing import List
import os

router = APIRouter()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///element_assets.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def get_db():
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/start", description="Fetch the system message and the last five memories.")
async def start_endpoint(db: Session = Depends(get_db)):
    try:
        # Fetch the system message from the environment file
        system_message = os.getenv("SYSTEM_MESSAGE", "Welcome! How can I assist you today?")

        # Fetch the last five memories from the database
        memories = db.query(GPTMemory).order_by(GPTMemory.id.desc()).limit(5).all()

        # Format the response
        formatted_memories = [
            {
                "id": memory.id,
                "title": memory.title,
                "summary": memory.summary,
                "session_id": memory.session_id,
                "created_at": memory.created_at,
            }
            for memory in memories
        ]

        return {
            "system_message": system_message,
            "last_memories": formatted_memories,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching start data: {str(e)}")
