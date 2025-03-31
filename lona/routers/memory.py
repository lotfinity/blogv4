import os
from datetime import datetime  # Add this import
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models.gpt_memory import GPTMemory, Base
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///element_assets.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

def get_db():
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class GPTMemoryRequest(BaseModel):
    title: str
    summary: str

@router.post("/gpt/memory", tags=["GPT Memory"])
async def commit_gpt_memory(request: GPTMemoryRequest, db: Session = Depends(get_db)):
    try:
        session_id = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        memory_entry = GPTMemory(
            title=request.title,
            summary=request.summary,
            session_id=session_id
        )
        db.add(memory_entry)
        db.commit()
        db.refresh(memory_entry)
        return {"message": "Memory committed successfully", "memory_id": memory_entry.id, "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error committing memory: {str(e)}")

@router.get("/gpt/memory", tags=["GPT Memory"])
async def get_all_gpt_memory(db: Session = Depends(get_db)):
    try:
        memories = db.query(GPTMemory).order_by(GPTMemory.id.desc()).all()
        return memories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching memory: {str(e)}")

@router.get("/gpt/memory/search", tags=["GPT Memory"])
async def search_gpt_memory(query: str, db: Session = Depends(get_db)):
    try:
        memories = db.query(GPTMemory).filter(
            GPTMemory.title.contains(query) | GPTMemory.summary.contains(query)
        ).all()
        return memories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching memory: {str(e)}")

@router.get("/gpt/memory/{memory_id}", tags=["GPT Memory"])
async def get_memory_by_id(memory_id: int, db: Session = Depends(get_db)):
    try:
        memory_entry = db.query(GPTMemory).filter(GPTMemory.id == memory_id).first()
        if not memory_entry:
            raise HTTPException(status_code=404, detail="Memory entry not found.")
        return memory_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching memory: {str(e)}")

@router.delete("/gpt/memory/{memory_id}", tags=["GPT Memory"])
async def delete_gpt_memory(memory_id: int, db: Session = Depends(get_db)):
    try:
        memory_entry = db.query(GPTMemory).filter(GPTMemory.id == memory_id).first()
        if not memory_entry:
            raise HTTPException(status_code=404, detail="Memory entry not found.")
        db.delete(memory_entry)
        db.commit()
        return {"message": "Memory entry deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting memory: {str(e)}")
