from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class GPTMemory(Base):
    __tablename__ = "gpt_memory"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    created_at = Column(String, default=datetime.utcnow().isoformat)  # Timestamp
