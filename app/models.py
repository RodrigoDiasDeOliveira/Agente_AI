from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict

Base = declarative_base()

class SearchTarget(Base):
    __tablename__ = "search_targets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    target_id = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    alternative_phrases = Column(JSON)           # lista de strings
    match_document = Column(JSON, nullable=False)
    embedding = Column(Text)                     # vetor como string JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(Text, nullable=False)
    target_id = Column(String(100))
    similarity = Column(Float)
    feedback_type = Column(String(20))   # "positive", "negative", "ignored"
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic
class MatchDocument(BaseModel):
    type: str                      # report, policy, action, section
    url: Optional[str] = None
    title: Optional[str] = None
    parameters: Dict = {}
    content_summary: Optional[str] = None

class SearchTargetCreate(BaseModel):
    target_id: str
    description: str
    alternative_phrases: List[str] = []
    match_document: MatchDocument